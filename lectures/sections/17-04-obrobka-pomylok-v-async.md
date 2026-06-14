---
chapter: 17
chapterTitle: "Розділ 17. Асинхронне програмування"
section: 4
number: "17.4"
title: "Обробка помилок в async-методах"
source: ""
---

## 17.4. Обробка помилок в async-методах

Асинхронний код вимагає особливої уваги до обробки помилок. Виняток, кинутий у асинхронному методі, не поширюється миттєво — він «консервується» у Task і чекає, поки хтось зробить `await`. Якщо `await` ніколи не відбудеться, виняток може бути втрачений назавжди або з'явитися в непередбаченому місці.

![Поширення помилок в async-методах](_assets/17-04/async-error-flow.png)

## Базова обробка через try/catch навколо await

Найпростіший і найправильніший підхід: обгорніть `await`-вираз у `try/catch`. Компілятор гарантує, що виняток із завдання буде «розгорнутий» і кинутий у точці `await`:

```csharp run
using System;
using System.Threading.Tasks;

async Task<string> LoadPatientDataAsync(string id)
{
    await Task.Delay(100);
    if (id == "DELETED")
        throw new InvalidOperationException($"Пацієнт {id} видалений з системи");
    return $"Дані пацієнта {id}: Петренко І.О., 45р";
}

// Правильний підхід: try/catch навколо await
Console.WriteLine("=== Спроба 1: неіснуючий пацієнт ===");
try
{
    string data = await LoadPatientDataAsync("DELETED");
    Console.WriteLine(data);
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"[Catch] Помилка доступу: {ex.Message}");
}

Console.WriteLine("\n=== Спроба 2: звичайний пацієнт ===");
try
{
    string data = await LoadPatientDataAsync("PT-001");
    Console.WriteLine($"[OK] {data}");
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"[Catch] {ex.Message}");
}
```

`try/catch` навколо `await` перехоплює виняток точно так само, як при синхронному виклику. Це одна з головних переваг `async/await` над старішими підходами (callback, ContinueWith) — обробка помилок виглядає природньо.

## async void і загублені винятки

Найнебезпечніша помилка в асинхронному коді — виняток у методі `async void`. Оскільки `async void` не повертає Task, кидати й перехоплювати виняток нема де: він потрапляє безпосередньо у `SynchronizationContext` або у `ThreadPool`, що призводить до аварійного завершення застосунку:

```csharp run
using System;
using System.Threading.Tasks;

// НЕБЕЗПЕЧНО: async void — виняток не можна перехопити ззовні
async void DangerousFireAndForget()
{
    await Task.Delay(50);
    Console.WriteLine("[Dangerous] Зараз кину виняток...");
    throw new Exception("Ця помилка НЕ перехоплюється через try/catch зовні!");
}

// ПРАВИЛЬНО: async Task — виняток «зберігається» у Task і розгортається при await
async Task SafeOperation()
{
    await Task.Delay(50);
    throw new Exception("Ця помилка перехоплюється при await");
}

// Демонстрація: async Task — виняток перехоплюється нормально
Console.WriteLine("=== async Task: виняток перехоплюється ===");
try
{
    await SafeOperation();
}
catch (Exception ex)
{
    Console.WriteLine($"[Catch] Перехоплено: {ex.Message}");
}

// Демонстрація: async void — try/catch навколо виклику НЕ допомагає
Console.WriteLine("\n=== async void: try/catch НЕ допомагає ===");
try
{
    DangerousFireAndForget(); // виняток виникне ПІСЛЯ того, як ми вийдемо з try
    await Task.Delay(200);    // чекаємо, щоб виняток мав час виникнути
}
catch (Exception ex)
{
    Console.WriteLine($"Цей рядок НІКОЛИ не виконається: {ex.Message}");
}

Console.WriteLine("async void виняток пройшов повз catch — в реальному застосунку це крашить програму");
```

Правило абсолютне: **ніколи не використовуйте `async void` поза обробниками подій**. Якщо вам потрібна операція «запустив і забув» без очікування — збережіть Task у змінну (і переконайтесь, що виняток десь оброблюється):

```csharp run
using System;
using System.Threading.Tasks;

async Task SendAlertAsync(string message)
{
    await Task.Delay(100);
    Console.WriteLine($"[Alert] {message}");
    // Якщо тут кинути виняток — він залишиться у Task без обробки
}

// "Запустив і забув" — правильний спосіб
Task alertTask = SendAlertAsync("Критичне сповіщення персоналу");
// alertTask не awaited — якщо виникне виняток, він буде у Task.Exception
// Якщо потрібна обробка помилок — зберігай Task і аналізуй пізніше

await Task.Delay(200); // даємо час завершитись
Console.WriteLine($"Alert завершено: {alertTask.IsCompletedSuccessfully.ToString()}");
```

## Обробка кількох помилок з Task.WhenAll

Коли `Task.WhenAll` чекає кількох завдань, і деякі з них завершуються з помилкою, `await Task.WhenAll(...)` розгортає лише **першу** помилку. Інші помилки залишаються у `AggregateException`, доступній через `task.Exception`:

```csharp run
using System;
using System.Threading.Tasks;

async Task<string> FetchFromSystemAsync(string system, bool fail)
{
    await Task.Delay(100);
    if (fail) throw new Exception($"Система '{system}' не відповідає");
    return $"Дані з {system}";
}

Task<string> lab    = FetchFromSystemAsync("Лабораторія",   fail: false);
Task<string> xray   = FetchFromSystemAsync("Рентген",       fail: true);  // помилка
Task<string> ecg    = FetchFromSystemAsync("ЕКГ",           fail: false);
Task<string> pharma = FetchFromSystemAsync("Аптека",        fail: true);  // помилка

Task<string[]> allTasks = Task.WhenAll(lab, xray, ecg, pharma);

try
{
    string[] results = await allTasks;
}
catch (Exception ex)
{
    // await розгортає ТІЛЬКИ першу помилку
    Console.WriteLine($"Перша помилка: {ex.Message}");
}

// Щоб отримати ВСІ помилки — перевіряємо AggregateException у Task.Exception
if (allTasks.Exception != null)
{
    Console.WriteLine($"\nВсі помилки ({allTasks.Exception.InnerExceptions.Count.ToString()}):");
    foreach (Exception inner in allTasks.Exception.InnerExceptions)
        Console.WriteLine($"  ✗ {inner.Message}");
}

// Успішні результати доступні через окремі Task
Console.WriteLine("\nУспішні відповіді:");
foreach (Task<string> t in new[] { lab, xray, ecg, pharma })
    if (t.IsCompletedSuccessfully)
        Console.WriteLine($"  ✓ {t.Result}");
```

Паттерн: зберігати посилання на `Task<T[]>`, що повертає `WhenAll`, і перевіряти `task.Exception.InnerExceptions` для повного списку помилок.

## finally у async-методах

`finally`-блок у async-методах працює так само, як у синхронних: виконується незалежно від того, успішно чи з помилкою завершився try-блок. Це важливо для гарантованого звільнення ресурсів:

```csharp run
using System;
using System.Threading.Tasks;

async Task ProcessPatientAsync(string patientId)
{
    Console.WriteLine($"[Process] Відкриваю з'єднання для {patientId}");
    try
    {
        Console.WriteLine($"[Process] Обробляю дані...");
        await Task.Delay(100);

        if (patientId == "ERROR")
            throw new Exception("Помилка обробки даних");

        Console.WriteLine($"[Process] Дані {patientId} оброблено");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"[Catch] Помилка: {ex.Message}");
        // Перекидаємо виняток далі
        throw;
    }
    finally
    {
        // Цей блок ЗАВЖДИ виконається — навіть при throw
        Console.WriteLine($"[Finally] Закриваю з'єднання для {patientId}");
    }
}

// Успішний випадок
try
{
    await ProcessPatientAsync("PT-001");
}
catch { }

Console.WriteLine();

// Випадок з помилкою
try
{
    await ProcessPatientAsync("ERROR");
}
catch (Exception ex)
{
    Console.WriteLine($"[Main] Перехоплено: {ex.Message}");
}
```

`await` можна використовувати і в `catch`, і в `finally`-блоках (починаючи з C# 6). Це дозволяє виконувати асинхронне очищення ресурсів:

```csharp run
using System;
using System.Threading.Tasks;

async Task PerformOperationAsync()
{
    try
    {
        await Task.Delay(50);
        throw new Exception("Щось пішло не так");
    }
    catch (Exception ex)
    {
        // await у catch — дозволено з C# 6
        Console.WriteLine($"[Catch] Логую помилку асинхронно: {ex.Message}");
        await Task.Delay(30); // асинхронне логування
        Console.WriteLine("[Catch] Помилку заlogовано");
    }
    finally
    {
        // await у finally — теж дозволено
        Console.WriteLine("[Finally] Асинхронне закриття ресурсів...");
        await Task.Delay(20);
        Console.WriteLine("[Finally] Ресурси звільнено");
    }
}

await PerformOperationAsync();
Console.WriteLine("[Main] Операція завершена");
```

## Глобальна обробка необроблених виключень

У продакшн-застосунках важливо передбачити глобальний обробник для необроблених async-виключень. Для консольних застосунків та ASP.NET Core це `AppDomain.CurrentDomain.UnhandledException` та `TaskScheduler.UnobservedTaskException`:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

// Підписуємось на необроблені Task-виключення
TaskScheduler.UnobservedTaskException += (sender, args) =>
{
    Console.WriteLine($"[Global] Необроблений виняток у Task: {args.Exception.InnerException?.Message}");
    args.SetObserved(); // позначаємо як оброблений — не крашить застосунок
};

// Запускаємо Task без await — виняток залишиться необробленим
Task.Run(async () =>
{
    await Task.Delay(50);
    throw new Exception("Виняток без await");
});

// Чекаємо і примусово збираємо сміття для тригеру UnobservedTaskException
await Task.Delay(200);
GC.Collect();
GC.WaitForPendingFinalizers();

Console.WriteLine("[Main] Продовжую роботу після глобального перехоплення");
```

`UnobservedTaskException` спрацьовує, коли Task з необробленим винятком збирається GC. Це остання лінія захисту, але покладатись на неї як на основний механізм обробки помилок — погана практика.

## Типові помилки та їх рішення

**1. Забув await — виняток загублений:**
```csharp run
using System;
using System.Threading.Tasks;

async Task ThrowAsync()
{
    await Task.Delay(10);
    throw new Exception("Помилка!");
}

// НЕПРАВИЛЬНО: без await виняток загублений у Task
Task t = ThrowAsync(); // виняток є, але ніхто не перевірить t.Exception

await Task.Delay(100);
Console.WriteLine($"Task завершений: {t.IsCompleted.ToString()}, Faulted: {t.IsFaulted.ToString()}");
Console.WriteLine($"Виняток: {t.Exception?.InnerException?.Message ?? "null"}");
// Виняток існує у Task, але не "вистрілив" назовні
```

**2. .Result або .Wait() у async-контексті — дедлок:**

Виклик `.Result` або `.Wait()` у async-контексті з `SynchronizationContext` (ASP.NET Classic, WinForms, WPF) призводить до дедлоку: `await` чекає потоку UI, а потік UI заблокований на `.Result`. Вирішення — завжди використовувати `await`:

```csharp run
using System;
using System.Threading.Tasks;

async Task<string> GetDataAsync()
{
    await Task.Delay(100);
    return "дані";
}

// БЕЗПЕЧНО в консольному застосунку, але ДЕДЛОК у WinForms/WPF/ASP.NET Classic:
// string data = GetDataAsync().Result; // НЕБЕЗПЕЧНО

// ПРАВИЛЬНО — завжди:
string data = await GetDataAsync();
Console.WriteLine($"Отримано: {data}");
```

Загальне правило: **async вниз по стеку до кінця**. Якщо один метод async — всі методи, що його викликають, теж мають бути async. Змішування синхронного і асинхронного коду через `.Result` є джерелом найважчих для діагностики дедлоків.

## ConfigureAwait(false) та SynchronizationContext

Щоб зрозуміти `ConfigureAwait(false)`, потрібно спочатку зрозуміти **SynchronizationContext**. Це механізм, що дозволяє продовженню (continuation) після `await` повернутися до «правильного» потоку:

- У **WinForms/WPF**: після `await` виконання продовжується у **потоці UI** — щоб можна було оновити елементи форми
- У **ASP.NET Classic**: після `await` виконання повертається до **того самого HTTP-потоку**
- У **ASP.NET Core** і **консольних** застосунках: SynchronizationContext відсутній, `await` продовжується у довільному ThreadPool-потоці

Саме через SynchronizationContext і виникає класичний дедлок з `.Result`:

```
1. Потік UI (або HTTP-потік) викликає GetDataAsync().Result
2. GetDataAsync() всередині робить await Task.Delay(100)
3. Task.Delay завершується — continuation чекає захоплення потоку UI
4. Але потік UI заблокований на .Result!
5. Дедлок: потік UI чекає Task, Task чекає потік UI
```

`ConfigureAwait(false)` каже `await`: «не намагайся повертатись на той самий SynchronizationContext — продовжуй у ThreadPool-потоці». Це ламає дедлок і підвищує продуктивність у бібліотечному коді:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

async Task<string> LibraryMethodAsync()
{
    // ConfigureAwait(false): після await продовжуємо в ThreadPool, не на UI-потоці
    await Task.Delay(100).ConfigureAwait(false);
    
    // Ця частина виконується в ThreadPool — НЕ чіпати UI-елементи тут!
    Console.WriteLine($"[Library] Потік: {Thread.CurrentThread.ManagedThreadId} (ThreadPool)");
    
    return "результат";
}

async Task AppMethodAsync()
{
    // У застосунку: await БЕЗ ConfigureAwait(false) — повертаємось на UI-потік
    // (у консолі SynchronizationContext == null, тому різниці немає)
    string result = await LibraryMethodAsync();
    
    Console.WriteLine($"[App] Потік: {Thread.CurrentThread.ManagedThreadId}");
    Console.WriteLine($"[App] Результат: {result}");
}

Console.WriteLine($"[Main] Стартовий потік: {Thread.CurrentThread.ManagedThreadId}");
await AppMethodAsync();
```

**Правило використання `ConfigureAwait(false)`:**

| Де | Рекомендація |
|----|-------------|
| **Бібліотечний код** (NuGet-пакети, спільні сервіси) | **Завжди** `ConfigureAwait(false)` — бібліотека не знає, де її використають |
| **Код застосунку** (UI, контролери) | **Без** `ConfigureAwait(false)` — потрібно оновлювати UI або залишатись у контексті HTTP-запиту |
| **ASP.NET Core** | Можна не турбуватись — SynchronizationContext відсутній, `ConfigureAwait(false)` нічого не змінює |

```csharp run
using System;
using System.Threading.Tasks;

// Бібліотечний метод — ConfigureAwait(false) скрізь
async Task<byte[]> ReadMedicalFileAsync(string path)
{
    // Симуляція читання файлу
    await Task.Delay(50).ConfigureAwait(false);
    await Task.Delay(30).ConfigureAwait(false);
    
    // Повертаємо результат — caller сам вирішить, що з ним робити
    byte[] fakeData = { 0x50, 0x44, 0x46 }; // "PDF" header
    Console.WriteLine("[Lib] Файл зчитано");
    return fakeData;
}

// Код застосунку — await без ConfigureAwait(false)
async Task HandlePatientDocumentAsync(string patientId)
{
    Console.WriteLine($"[App] Читаю документ для {patientId}...");
    
    byte[] content = await ReadMedicalFileAsync($"/records/{patientId}.pdf");
    
    // Тут ми в правильному контексті — можна оновити UI або зберегти в БД
    Console.WriteLine($"[App] Документ отримано, розмір: {content.Length} байт");
}

await HandlePatientDocumentAsync("PT-1001");
