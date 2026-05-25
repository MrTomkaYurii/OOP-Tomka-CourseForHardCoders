---
chapter: 17
chapterTitle: "Розділ 17. Асинхронне програмування"
section: 2
number: "17.2"
title: "Типи повернення async-методів"
source: ""
---

## 17.2. Типи повернення async-методів

Асинхронні методи в C# можуть повертати чотири типи: `void`, `Task`, `Task<T>` і `ValueTask<T>`. Вибір між ними — не питання смаку: кожен тип має своє призначення, обмеження та вплив на продуктивність. Правильний вибір типу повернення — ознака грамотного асинхронного коду.

![Типи повернення async-методів](_assets/17-02/return-types.png)

## async void — тільки для обробників подій

`async void` — найнебезпечніший тип повернення. Метод нічого не повертає, тому викликаючий код не може ні отримати результат, ні дочекатися завершення, ні перехопити виняток через `try/catch`.

Єдиний законний сценарій використання `async void` — обробники подій, де підпис методу встановлений зовнішнім інтерфейсом і не може бути змінений:

```csharp run
using System;
using System.Threading.Tasks;

// Симуляція обробника події — такий підпис вимагає система подій
void SimulateButton_Click(object? sender, EventArgs e)
{
    // Тут ми не можемо повернути Task, бо підпис встановлений делегатом EventHandler
    // Тому async void — єдиний варіант для обробників подій
    _ = HandleButtonClickAsync(); // запускаємо і не чекаємо (в реальному EventHandler це async void)
}

async Task HandleButtonClickAsync()
{
    Console.WriteLine("[UI] Кнопка натиснута — початок реєстрації...");
    await Task.Delay(300); // симуляція збереження до БД
    Console.WriteLine("[UI] Пацієнта зареєстровано успішно");
}

// Демонстрація проблеми async void: виняток губиться
async void DangerousAsyncVoid()
{
    await Task.Delay(50);
    throw new InvalidOperationException("Ця помилка НЕ буде перехоплена зовні!");
}

// Правильна версія — async Task, виняток можна перехопити
async Task SafeAsyncTask()
{
    await Task.Delay(50);
    throw new InvalidOperationException("Ця помилка перехоплюється через await");
}

// Демонстрація
Console.WriteLine("=== async void: виняток не перехоплюється ===");
try
{
    DangerousAsyncVoid(); // виняток виникне, але try/catch його НЕ впіймає
    await Task.Delay(200); // чекаємо завершення
}
catch (Exception ex)
{
    Console.WriteLine($"Цей рядок НІКОЛИ не виконається: {ex.Message}");
}
Console.WriteLine("async void: виняток пройшов повз catch");

Console.WriteLine("\n=== async Task: виняток перехоплюється ===");
try
{
    await SafeAsyncTask(); // виняток поширюється через await
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"Перехоплено: {ex.Message}");
}
```

Ключове правило: **ніколи не використовуйте `async void` поза обробниками подій**. `async void`-метод не можна очікувати, не можна обробити його виняток ззовні, не можна перевірити його стан. Це «запустив і забув» у найгіршому сенсі.

## async Task — операція без результату

`async Task` — стандартний тип повернення для асинхронних методів, що не повертають значення. На відміну від `async void`, `Task` дозволяє:
- очікувати завершення через `await`
- перехоплювати винятки через `try/catch` навколо `await`
- передавати завдання у `Task.WhenAll` та інші комбінатори

```csharp run
using System;
using System.Threading.Tasks;

// async Task — повертає Task, але без значення всередині
async Task SavePatientAsync(string patientId, string data)
{
    Console.WriteLine($"[Save] Збереження даних пацієнта {patientId}...");
    await Task.Delay(200); // симуляція запиту до БД
    Console.WriteLine($"[Save] Дані {patientId} збережено успішно");
    // return не потрібен — метод "повертає" Task, що сигналізує про завершення
}

async Task DeletePatientAsync(string patientId)
{
    Console.WriteLine($"[Delete] Видалення пацієнта {patientId}...");
    await Task.Delay(100);
    // Симулюємо помилку — вона поширюється через Task
    throw new UnauthorizedAccessException($"Пацієнт {patientId} захищений від видалення");
}

// Очікування завершення — викликаючий знає, коли операція завершилась
await SavePatientAsync("PT-001", "Анамнез: ...");

// Обробка помилок через try/catch навколо await
try
{
    await DeletePatientAsync("PT-002");
}
catch (UnauthorizedAccessException ex)
{
    Console.WriteLine($"[Main] Помилка: {ex.Message}");
}

Console.WriteLine("[Main] Продовжуємо роботу після обох операцій");
```

`async Task` завжди кращий за `async void` там, де підпис методу під вашим контролем. Поверніть `Task` — і ваш код стає тестованим, перехоплюваним і сумісним з усіма async-комбінаторами.

## async Task\<T\> — операція з результатом

`Task<T>` — тип повернення для асинхронних методів, що обчислюють або отримують значення. Оператор `await` «розгортає» Task і повертає значення типу `T`. Це найпоширеніший тип для реальних асинхронних операцій:

```csharp run
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

// async Task<string> — повертає рядок через Task
async Task<string> GetPatientNameAsync(string id)
{
    Console.WriteLine($"[DB] Запит імені для {id}...");
    await Task.Delay(150);
    return $"Петренко І.О. (id={id})"; // return T, компілятор загортає у Task<T>
}

// async Task<List<string>> — повертає список
async Task<List<string>> GetPatientLabResultsAsync(string id)
{
    Console.WriteLine($"[Lab] Завантаження результатів для {id}...");
    await Task.Delay(200);
    return new List<string>
    {
        "Гемоглобін: 135 г/л — норма",
        "Лейкоцити: 6.2 × 10⁹/л — норма",
        "ШОЕ: 8 мм/год — норма"
    };
}

// async Task<bool> — повертає булеве значення
async Task<bool> CheckBedAvailabilityAsync(string ward)
{
    await Task.Delay(100);
    return ward != "ВІТ"; // ВІТ — переповнене
}

// Використання: await "розгортає" Task<T> до T
string name = await GetPatientNameAsync("PT-2024-007");
Console.WriteLine($"Пацієнт: {name}");

List<string> results = await GetPatientLabResultsAsync("PT-2024-007");
Console.WriteLine("\nРезультати аналізів:");
foreach (string r in results)
    Console.WriteLine($"  {r}");

bool available = await CheckBedAvailabilityAsync("ВІТ");
Console.WriteLine($"\nВІТ вільне: {available.ToString()}");
```

Зверніть на `return` у `async Task<T>`: ви повертаєте значення типу `T`, а не `Task<T>`. Компілятор автоматично «загортає» його у `Task<T>`. Це симетрично до того, як `await` «розгортає» `Task<T>` назад до `T`.

## ValueTask\<T\> — для hot path без алокації

`ValueTask<T>` — оптимізований тип для сценаріїв, де метод **часто завершується синхронно** (без реального очікування). Різниця з `Task<T>`: якщо результат вже відомий і очікування не потрібне, `ValueTask<T>` не виділяє пам'яті у heap, оскільки є структурою (struct), а не класом.

```csharp run
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

// Кеш результатів — більшість запитів повертатимуть синхронно
Dictionary<string, string> _cache = new Dictionary<string, string>
{
    ["PT-001"] = "Коваль М.А.",
    ["PT-002"] = "Бойко О.П."
};

// ValueTask<T>: якщо є в кеші — повертає синхронно (без алокації Task)
// якщо немає — виконує реальний асинхронний запит
async ValueTask<string> GetPatientFastAsync(string id)
{
    if (_cache.TryGetValue(id, out string? cached))
    {
        // Синхронне повернення — ValueTask не виділяє пам'яті
        Console.WriteLine($"[Cache] HIT: {id} → {cached}");
        return cached;
    }

    // Асинхронний шлях — звернення до бази даних
    Console.WriteLine($"[Cache] MISS: {id} — запит до БД...");
    await Task.Delay(200);
    string name = $"Невідомий пацієнт (id={id})";
    _cache[id] = name;
    return name;
}

// Використання: синтаксично ідентичне Task<T>
string p1 = await GetPatientFastAsync("PT-001"); // з кешу — синхронно
string p2 = await GetPatientFastAsync("PT-002"); // з кешу — синхронно
string p3 = await GetPatientFastAsync("PT-999"); // не в кеші — асинхронно

Console.WriteLine($"\nРезультати: {p1}, {p2}, {p3}");
```

`ValueTask<T>` слід використовувати лише коли є вимірювані докази, що алокація `Task<T>` є вузьким місцем (hot path, мільйони викликів). В усіх інших випадках — `Task<T>` є правильним вибором: він простіший, безпечніший і добре оптимізований у .NET.

**Важливе обмеження**: `ValueTask<T>` можна `await`-ати лише один раз. Якщо вам потрібно зберегти завдання у змінну і очікувати кілька разів — використовуйте `Task<T>`.

## Task.FromResult і Task.CompletedTask — синхронні обгортки

Іноді потрібно повернути `Task<T>` або `Task` з методу, де фактична робота виконується синхронно. Найпоширенісний сценарій — реалізація інтерфейсу або тест-дублер:

```csharp run
using System;
using System.Threading.Tasks;

// Інтерфейс репозиторію
interface IPatientRepository
{
    Task<string> GetNameAsync(string id);
    Task SaveAsync(string id, string data);
}

// Реальна реалізація — справді асинхронна (звертається до БД)
class DatabaseRepository : IPatientRepository
{
    public async Task<string> GetNameAsync(string id)
    {
        await Task.Delay(100); // реальний асинхронний запит
        return $"Пацієнт {id} з бази даних";
    }

    public async Task SaveAsync(string id, string data)
    {
        await Task.Delay(50);
        Console.WriteLine($"[DB] Збережено: {id}");
    }
}

// Фейкова реалізація для тестів — синхронна, але мусить відповідати інтерфейсу
class FakeRepository : IPatientRepository
{
    public Task<string> GetNameAsync(string id)
        => Task.FromResult($"Тестовий пацієнт {id}"); // синхронно, без async

    public Task SaveAsync(string id, string data)
    {
        Console.WriteLine($"[Fake] Зберігаю (імітація): {id}");
        return Task.CompletedTask; // Task, що вже завершений
    }
}

// Використання
IPatientRepository repo = new FakeRepository();
string name = await repo.GetNameAsync("PT-001");
Console.WriteLine($"Отримано: {name}");

await repo.SaveAsync("PT-001", "дані");
Console.WriteLine("[Main] Операції завершено");
```

`Task.FromResult<T>(value)` створює Task, що вже завершений зі значенням — без жодних алокацій стейт-машини. `Task.CompletedTask` — синглтон-Task для `Task`-методів без значення, що не вимагає реальної асинхронності. Обидва широко використовуються при реалізації інтерфейсів, заглушок і тест-дублерів.

## Зведена таблиця типів повернення

| Тип | Коли використовувати | Awaitable | Перехоплення помилок | Алокація |
|-----|---------------------|-----------|---------------------|---------|
| `async void` | Тільки EventHandler | Ні | Ні (глобально) | Немає |
| `async Task` | Операція без результату | Так | Так | Task |
| `async Task<T>` | Операція з результатом | Так | Так | Task |
| `async ValueTask<T>` | Hot path з частим sync-шляхом | Так (1 раз) | Так | Немає (sync) |

Правило вибору: за замовчуванням — `Task` або `Task<T>`. `async void` — лише для EventHandler. `ValueTask<T>` — тільки при підтвердженому профілюванням вузькому місці.
