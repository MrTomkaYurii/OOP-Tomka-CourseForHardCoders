---
chapter: 17
chapterTitle: "Розділ 17. Асинхронне програмування"
section: 6
number: "17.6"
title: "Асинхронні потоки. IAsyncEnumerable<T>"
source: ""
---

## 17.6. Асинхронні потоки. IAsyncEnumerable\<T\>

Класичний `async Task<T>` відповідає на одне питання: «дай мені результат асинхронно». Але що, якщо результатів багато і вони надходять поступово — рядки з великого файлу, повідомлення з черги, дані з БД мільйонами рядків? Завантажити все у пам'ять і повернути `Task<List<T>>` — неефективно або неможливо. Саме для цього C# 8.0 ввів `IAsyncEnumerable<T>` — **асинхронні потоки даних**, де кожен елемент може бути отриманий асинхронно.

![Блокуюче vs стрімінгове завантаження](_assets/17-06/async-stream-flow.png)

## Проблема: завантажити все vs обробляти по мірі надходження

Порівняємо два підходи для завантаження великого набору медичних записів:

```csharp run
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

// Підхід 1: Task<List<T>> — чекаємо ВСЕ, потім обробляємо
async Task<List<string>> LoadAllRecordsAsync(int count)
{
    var result = new List<string>();
    for (int i = 1; i <= count; i++)
    {
        await Task.Delay(50); // симуляція затримки для кожного запису
        result.Add($"Запис #{i.ToString()}");
    }
    return result; // повертаємо ВСЕ одразу
}

// Підхід 2: IAsyncEnumerable<T> — отримуємо і обробляємо по одному
async IAsyncEnumerable<string> StreamRecordsAsync(int count)
{
    for (int i = 1; i <= count; i++)
    {
        await Task.Delay(50); // симуляція затримки
        yield return $"Запис #{i.ToString()}"; // повертаємо ОДРАЗУ як готовий
    }
}

// Демонстрація: Task<List<T>> — довге очікування, потім всі результати
Console.WriteLine("=== Task<List<T>>: чекаємо всього ===");
var sw1 = System.Diagnostics.Stopwatch.StartNew();
List<string> all = await LoadAllRecordsAsync(5);
sw1.Stop();
Console.WriteLine($"Отримано {all.Count.ToString()} записів через {sw1.ElapsedMilliseconds.ToString()} мс");
foreach (string r in all)
    Console.WriteLine($"  {r}");

Console.WriteLine("\n=== IAsyncEnumerable<T>: обробляємо по мірі надходження ===");
var sw2 = System.Diagnostics.Stopwatch.StartNew();
await foreach (string record in StreamRecordsAsync(5))
    Console.WriteLine($"  ✓ {record} (через {sw2.ElapsedMilliseconds.ToString()} мс від початку)");
sw2.Stop();
```

При `IAsyncEnumerable<T>` перший елемент доступний через ~50 мс, а не через 250 мс. Користувач бачить результати миттєво — це принципова різниця у сприйнятті швидкості.

## Оголошення та yield return

Метод, що повертає `IAsyncEnumerable<T>`, використовує:
- `async` у заголовку
- `IAsyncEnumerable<T>` як тип повернення
- `yield return` для кожного елемента
- `await` між елементами для асинхронних операцій

```csharp run
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

// Класичний приклад: стрімінг лабораторних результатів
async IAsyncEnumerable<string> GetLabResultsStreamAsync(string patientId)
{
    string[] tests = { "Аналіз крові", "Аналіз сечі", "ЕКГ", "Рентген", "УЗД" };

    Console.WriteLine($"[Lab] Починаю аналізи для {patientId}");

    foreach (string test in tests)
    {
        // Кожен аналіз займає різний час
        int duration = test.Length * 30; // умовна тривалість
        await Task.Delay(duration); // асинхронне очікування

        string result = $"{test}: показники в нормі";
        Console.WriteLine($"  [Lab] {test} завершено ({duration.ToString()} мс)");

        yield return result; // повертаємо результат одразу
    }

    Console.WriteLine($"[Lab] Всі аналізи для {patientId} завершено");
}

// Споживання: await foreach
Console.WriteLine("Реєстрація результатів у систему:");
await foreach (string labResult in GetLabResultsStreamAsync("PT-2024-007"))
{
    // Цей блок виконується одразу при появі кожного результату
    Console.WriteLine($"  ✓ Занесено: {labResult}");
}

Console.WriteLine("\nВсі результати зареєстровано");
```

`yield return` у async-методі — це точка, де метод «призупиняється» і повертає елемент споживачу. Споживач обробляє елемент, і лише потім метод продовжує генерувати наступний.

## await foreach — споживання асинхронного потоку

`await foreach` — спеціальна синтаксична конструкція для обходу `IAsyncEnumerable<T>`. Вона асинхронно очікує кожен наступний елемент і виконує тіло циклу:

```csharp run
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

async IAsyncEnumerable<int> GeneratePatientIdsAsync()
{
    int[] ids = { 101, 205, 318, 422, 537 };
    foreach (int id in ids)
    {
        await Task.Delay(80);
        yield return id;
    }
}

// await foreach: кожна ітерація асинхронно очікує наступний елемент
await foreach (int patientId in GeneratePatientIdsAsync())
{
    Console.WriteLine($"Обробляю пацієнта ID={patientId.ToString()}");
    await Task.Delay(20); // власна обробка теж може бути async
}

Console.WriteLine("Потік завершено");
```

Компілятор перетворює `await foreach` на виклики `GetAsyncEnumerator()`, `MoveNextAsync()` та `Current` — async-аналоги синхронного `IEnumerable<T>`.

## CancellationToken у асинхронних потоках

`IAsyncEnumerable<T>` підтримує скасування через атрибут `[EnumeratorCancellation]` у параметрах методу-генератора. Це дозволяє передавати токен через `WithCancellation()` при `await foreach`:

```csharp run
using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;

// [EnumeratorCancellation] дозволяє передавати токен через WithCancellation()
async IAsyncEnumerable<string> StreamDiagnosesAsync(
    string ward,
    [EnumeratorCancellation] CancellationToken ct = default)
{
    string[] diagnoses = {
        "J06.9 — ГРВІ",      "I10 — Гіпертонія",
        "E11.9 — Діабет 2",  "J18.9 — Пневмонія",
        "K29.5 — Гастрит",   "M54.5 — Люмбалгія"
    };

    Console.WriteLine($"[Stream] Завантаження діагнозів відділення {ward}...");

    foreach (string diagnosis in diagnoses)
    {
        ct.ThrowIfCancellationRequested(); // перевірка перед кожним елементом

        await Task.Delay(100, ct); // асинхронна затримка зі скасуванням

        Console.WriteLine($"  [Stream] Готово: {diagnosis}");
        yield return diagnosis;
    }
}

using CancellationTokenSource cts = new CancellationTokenSource();
cts.CancelAfter(350); // скасуємо через 350мс (~3 діагнози)

Console.WriteLine("Завантаження діагнозів (з обмеженням часу 350мс):");
try
{
    // WithCancellation() передає токен у генератор через [EnumeratorCancellation]
    await foreach (string diag in StreamDiagnosesAsync("Терапія").WithCancellation(cts.Token))
    {
        Console.WriteLine($"  ✓ Зареєстровано: {diag}");
    }
    Console.WriteLine("Всі діагнози завантажено");
}
catch (OperationCanceledException)
{
    Console.WriteLine("[Main] Стрімінг скасовано — тайм-аут");
}
```

Без `[EnumeratorCancellation]` токен, переданий через `WithCancellation()`, не потрапить у параметри методу-генератора і не спрацює.

## Фільтрація та трансформація потоку

Асинхронні потоки можна обробляти у pipeline: один метод генерує, інший фільтрує або трансформує. Це async-аналог LINQ-ланцюгів для синхронних колекцій:

```csharp run
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

// Генератор: потік пацієнтів з показниками
async IAsyncEnumerable<(string Name, int Pulse, double Glucose)> GetPatientMetricsAsync()
{
    var data = new (string, int, double)[]
    {
        ("Коваль М.",    72,  5.1),
        ("Бойко О.",    145,  8.7), // критичний пульс
        ("Мороз В.",     68,  4.8),
        ("Петренко І.", 110,  12.4), // критична глюкоза
        ("Руденко С.",   78,  5.5)
    };

    foreach (var patient in data)
    {
        await Task.Delay(50); // симуляція отримання з пристрою
        yield return patient;
    }
}

// Фільтр: передає тільки критичні стани
async IAsyncEnumerable<string> GetCriticalPatientsAsync()
{
    await foreach (var (name, pulse, glucose) in GetPatientMetricsAsync())
    {
        bool critical = pulse > 120 || glucose > 10.0;
        if (critical)
        {
            string reason = pulse > 120 ? $"пульс {pulse.ToString()} уд/хв"
                                        : $"глюкоза {glucose.ToString()} ммоль/л";
            yield return $"⚠ {name}: {reason}";
        }
    }
}

// Споживання: тільки критичні пацієнти
Console.WriteLine("Критичні стани (стрімінг з фільтрацією):");
await foreach (string alert in GetCriticalPatientsAsync())
    Console.WriteLine($"  {alert}");

Console.WriteLine("Моніторинг завершено");
```

Кожен метод у pipeline є незалежним async-генератором, що не зберігає всі дані у пам'яті — передає елемент далі одразу при отриманні.

## IAsyncEnumerable vs інші підходи

| Підхід | Повертає | Споживання | Зберігає в пам'яті | Підходить для |
|--------|----------|------------|-------------------|---------------|
| `Task<List<T>>` | Весь список одразу | `await` + `foreach` | Весь список | Малі набори даних |
| `IEnumerable<T>` | Елементи по одному | `foreach` | Один елемент | Синхронна генерація |
| `IAsyncEnumerable<T>` | Елементи по одному | `await foreach` | Один елемент | Async-генерація, стрімінг |
| `Channel<T>` | Черга повідомлень | `ReadAllAsync()` | Буфер | Продюсер-споживач |

`IAsyncEnumerable<T>` — правильний вибір, коли:
- Джерело даних велике або нескінченне (БД-курсор, черга, сенсорний потік)
- Перший результат потрібен якнайшвидше
- Продюсер і споживач можуть мати різну швидкість
- Обробка кожного елемента асинхронна

## Практичний приклад: стрімінг пацієнтів з БД

```csharp run
using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;

using CancellationTokenSource cts = new CancellationTokenSource(500);

try
{
    await ProcessWardPatientsAsync("Терапія", cts.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("[Main] Обробку зупинено за тайм-аутом");
}

// Сервісний рівень: обробка потоку
async Task ProcessWardPatientsAsync(string ward, CancellationToken ct)
{
    var repo = new PatientRepository();
    int count = 0;

    await foreach (string patient in repo.GetPatientsStreamAsync(ward, ct))
    {
        count++;
        Console.WriteLine($"  [{count.ToString()}] Оброблено: {patient}");
    }

    Console.WriteLine($"[Service] Відділення {ward}: оброблено {count.ToString()} пацієнтів");
}

// Симуляція репозиторію з підтримкою стрімінгу
class PatientRepository
{
    private readonly string[] _allPatients = {
        "Коваль М.А.", "Бойко О.П.", "Мороз В.І.", "Петренко І.О.",
        "Руденко С.В.", "Шевченко Т.М.", "Гриценко Д.Ю.", "Сидоренко Р.К."
    };

    // Стрімінг з пагінацією — симуляція курсору БД
    public async IAsyncEnumerable<string> GetPatientsStreamAsync(
        string ward,
        [EnumeratorCancellation] CancellationToken ct = default)
    {
        Console.WriteLine($"[Repo] Відкриваю курсор БД для відділення {ward}");

        for (int i = 0; i < _allPatients.Length; i++)
        {
            ct.ThrowIfCancellationRequested();
            await Task.Delay(60, ct); // симуляція мережевої затримки

            yield return $"{_allPatients[i]} (відділення: {ward})";
        }

        Console.WriteLine("[Repo] Курсор БД закрито");
    }
}
```

Цей патерн — «стрімінг репозиторій» — є стандартом для роботи з великими наборами даних у сучасних .NET-застосунках. `IAsyncEnumerable<T>` підтримується у Entity Framework Core через `ToAsyncEnumerable()`, у gRPC-стрімінгу, у SignalR і у всій екосистемі .NET.
