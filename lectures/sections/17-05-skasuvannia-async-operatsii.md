---
chapter: 17
chapterTitle: "Розділ 17. Асинхронне програмування"
section: 5
number: "17.5"
title: "Скасування async-операцій. CancellationToken"
source: ""
---

## 17.5. Скасування async-операцій. CancellationToken

Скасування — невід'ємна частина асинхронного програмування. Користувач натискає «Скасувати», сплив тайм-аут, програма завершує роботу — у всіх цих випадках потрібно коректно зупинити async-операцію, що виконується. `CancellationToken` у async-контексті працює за тим самим кооперативним принципом, що і у TPL (розділ 16.5), але має ряд async-специфічних особливостей.

![Скасування async-операцій через CancellationToken](_assets/17-05/async-cancellation.png)

## CancellationToken у async-методах

Async-метод приймає `CancellationToken` як параметр — за угодою, останній або передостанній. Токен передається у вбудовані async-методи (.NET BCL весь побудований на цій угоді), а також перевіряється вручну між операціями:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

// Async-метод з CancellationToken: прийнятий останнім параметром
async Task<string> LoadMedicalRecordAsync(string patientId, CancellationToken ct = default)
{
    Console.WriteLine($"[Load] Запит картки {patientId}...");

    // Передаємо token у Task.Delay — він підтримує скасування нативно
    await Task.Delay(300, ct); // кине OperationCanceledException при Cancel()

    Console.WriteLine($"[Load] Картка {patientId} завантажена");
    return $"Картка: Петренко І.О. (id={patientId})";
}

// Демонстрація успішного завершення
Console.WriteLine("=== Успішне завантаження ===");
using CancellationTokenSource cts1 = new CancellationTokenSource();
string record = await LoadMedicalRecordAsync("PT-001", cts1.Token);
Console.WriteLine($"Результат: {record}");

// Демонстрація скасування
Console.WriteLine("\n=== Скасування під час завантаження ===");
using CancellationTokenSource cts2 = new CancellationTokenSource();
cts2.CancelAfter(150); // скасуємо через 150мс (до завершення 300мс)

try
{
    string cancelled = await LoadMedicalRecordAsync("PT-002", cts2.Token);
    Console.WriteLine($"Результат: {cancelled}");
}
catch (OperationCanceledException)
{
    Console.WriteLine("[Main] Завантаження скасовано (тайм-аут або запит користувача)");
}
```

`Task.Delay(ms, token)` — async-версія затримки зі скасуванням. Коли токен скасовується, `Task.Delay` кидає `OperationCanceledException` одразу, не чекаючи завершення таймера.

## Перевірка токену між операціями

У довгих async-методах, що виконують кілька кроків, важливо перевіряти токен між кроками — щоб не починати нову операцію після сигналу скасування:

```csharp run
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

async Task ProcessPatientBatchAsync(List<string> patientIds, CancellationToken ct)
{
    Console.WriteLine($"[Batch] Початок обробки {patientIds.Count.ToString()} пацієнтів");

    for (int i = 0; i < patientIds.Count; i++)
    {
        // Перевіряємо перед кожною операцією
        ct.ThrowIfCancellationRequested();

        string id = patientIds[i];
        Console.WriteLine($"[Batch] Обробка {i + 1}/{patientIds.Count.ToString()}: {id}");

        await Task.Delay(150, ct); // симуляція async-операції з токеном

        Console.WriteLine($"[Batch] {id} — оброблено");
    }

    Console.WriteLine("[Batch] Всі пацієнти оброблені");
}

List<string> patients = new List<string> { "PT-001", "PT-002", "PT-003", "PT-004", "PT-005" };

using CancellationTokenSource cts = new CancellationTokenSource();
cts.CancelAfter(400); // скасуємо через 400мс (після ~2-3 пацієнтів)

try
{
    await ProcessPatientBatchAsync(patients, cts.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("[Main] Пакетну обробку скасовано — оброблено часткові результати");
}
```

`ct.ThrowIfCancellationRequested()` — синхронна перевірка, що кидає `OperationCanceledException` без затримки. Розміщуйте її на початку кожного кроку або ітерації.

## CancelAfter — тайм-аут для async-операцій

`CancellationTokenSource.CancelAfter(ms)` — стандартний спосіб реалізації тайм-ауту для async-операцій. Замість складних конструкцій з `Task.WhenAny + Task.Delay`, він пряно і чисто обмежує час операції:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

async Task<byte[]> DownloadXRayAsync(string patientId, CancellationToken ct)
{
    Console.WriteLine($"[Download] Завантаження рентгену {patientId}...");
    await Task.Delay(800, ct); // симуляція тривалого завантаження
    Console.WriteLine($"[Download] Рентген {patientId} завантажено");
    return new byte[1024]; // симуляція даних
}

// Тайм-аут 500мс: якщо завантаження займає більше — скасовуємо
using CancellationTokenSource cts = new CancellationTokenSource(500); // або CancelAfter(500)

try
{
    byte[] xray = await DownloadXRayAsync("PT-007", cts.Token);
    Console.WriteLine($"[Main] Завантажено {xray.Length.ToString()} байт");
}
catch (OperationCanceledException)
{
    Console.WriteLine("[Main] Тайм-аут! Рентген завантажується надто довго");
    Console.WriteLine("[Main] Показую кешовану версію");
}
```

Конструктор `new CancellationTokenSource(ms)` — скорочення для `CancelAfter(ms)`. Для сучасного async-коду це набагато зручніше, ніж ручна конструкція з `Task.WhenAny`.

## Пов'язані токени у async-контексті

Реальні системи часто мають кілька незалежних причин для скасування: глобальний тайм-аут застосунку, тайм-аут конкретного запиту, та сигнал від користувача. `CancellationTokenSource.CreateLinkedTokenSource` об'єднує кілька токенів — новий токен спрацьовує при скасуванні будь-якого:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

async Task<string> FetchPatientSummaryAsync(string id, CancellationToken ct)
{
    Console.WriteLine($"[Fetch] Запит зведення для {id}...");

    // Крок 1: завантаження даних
    ct.ThrowIfCancellationRequested();
    await Task.Delay(200, ct);
    Console.WriteLine($"[Fetch] Базові дані {id} завантажено");

    // Крок 2: обробка
    ct.ThrowIfCancellationRequested();
    await Task.Delay(200, ct);
    Console.WriteLine($"[Fetch] Дані {id} оброблено");

    return $"Зведення: пацієнт {id} — стабільний стан";
}

// Два рівні скасування: глобальний і per-request
using CancellationTokenSource appShutdown = new CancellationTokenSource(); // глобальний
using CancellationTokenSource requestTimeout = new CancellationTokenSource(350); // тайм-аут запиту 350мс

// Об'єднаний токен — спрацьовує при будь-якому скасуванні
using CancellationTokenSource linked =
    CancellationTokenSource.CreateLinkedTokenSource(appShutdown.Token, requestTimeout.Token);

try
{
    string summary = await FetchPatientSummaryAsync("PT-010", linked.Token);
    Console.WriteLine($"[Main] Результат: {summary}");
}
catch (OperationCanceledException)
{
    string reason = appShutdown.IsCancellationRequested   ? "завершення застосунку"
                  : requestTimeout.IsCancellationRequested ? "тайм-аут запиту"
                  :                                          "невідома причина";
    Console.WriteLine($"[Main] Операцію скасовано: {reason}");
}
```

Пов'язані токени — ключовий інструмент для ієрархічного скасування: батьківський scope (застосунок) → дочірній scope (запит) → конкретна операція.

## Передача токену у бібліотечні async-методи

Більшість async-методів у .NET BCL приймають `CancellationToken`. Завжди передавайте токен — це гарантує коректне скасування на кожному рівні:

```csharp run
using System;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

async Task<string> FetchFromApiAsync(string url, CancellationToken ct)
{
    using HttpClient http = new HttpClient();
    http.Timeout = TimeSpan.FromSeconds(5);

    try
    {
        // HttpClient.GetStringAsync приймає CancellationToken — передаємо!
        string response = await http.GetStringAsync(url, ct);
        return response[..Math.Min(100, response.Length)]; // перші 100 символів
    }
    catch (HttpRequestException ex)
    {
        return $"Помилка HTTP: {ex.StatusCode}";
    }
}

using CancellationTokenSource cts = new CancellationTokenSource(2000); // 2 секунди

try
{
    // Спробуємо запит до публічного API
    string result = await FetchFromApiAsync("https://httpbin.org/delay/1", cts.Token);
    Console.WriteLine($"[API] Відповідь: {result}");
}
catch (OperationCanceledException)
{
    Console.WriteLine("[API] Тайм-аут або скасовано користувачем");
}
catch (Exception ex)
{
    Console.WriteLine($"[API] Помилка: {ex.Message}");
}
```

## Коректна відповідь на скасування: OperationCanceledException

Коли операція скасовується, правильна поведінка — перекинути `OperationCanceledException` (або `TaskCanceledException`), а не повернути пустий результат чи ковтнути виняток. Це дозволяє коду вище в стеку знати, що операція не просто завершилась — вона була скасована:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

async Task<string> ProcessAsync(CancellationToken ct)
{
    for (int i = 1; i <= 5; i++)
    {
        ct.ThrowIfCancellationRequested(); // кидає OperationCanceledException

        Console.WriteLine($"  Крок {i.ToString()}/5...");
        await Task.Delay(100, ct);
    }
    return "Результат обробки";
}

async Task RunWithRetryAsync(CancellationToken globalCt)
{
    for (int attempt = 1; attempt <= 3; attempt++)
    {
        // Тайм-аут для кожної спроби — але зберігаємо глобальне скасування
        using CancellationTokenSource attemptCts = CancellationTokenSource.CreateLinkedTokenSource(globalCt);
        attemptCts.CancelAfter(250); // кожна спроба — до 250мс

        try
        {
            Console.WriteLine($"\n[Retry] Спроба {attempt.ToString()}/3:");
            string result = await ProcessAsync(attemptCts.Token);
            Console.WriteLine($"[Retry] Успіх: {result}");
            return; // виходимо при успіху
        }
        catch (OperationCanceledException) when (!globalCt.IsCancellationRequested)
        {
            // Тайм-аут спроби — але глобальне скасування не надійшло, повторюємо
            Console.WriteLine($"[Retry] Спроба {attempt.ToString()} перевищила тайм-аут — повтор");
        }
        // OperationCanceledException з globalCt — пробрасуємо далі (не ловимо)
    }
    Console.WriteLine("[Retry] Всі спроби вичерпано");
}

using CancellationTokenSource globalCts = new CancellationTokenSource(1000);
try
{
    await RunWithRetryAsync(globalCts.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("\n[Main] Глобальне скасування — зупиняємо повністю");
}
```

Конструкція `catch (OperationCanceledException) when (!globalCt.IsCancellationRequested)` — фільтр виключень. Вона перехоплює скасування **тільки** від тайм-ауту спроби, але пропускає через себе скасування від глобального токену. Це точний контроль над тим, яке саме скасування обробляється.

## Стан Task після скасування

Async-метод, скасований через `OperationCanceledException`, переходить у стан `Canceled` — якщо токен, що спричинив виняток, був переданий у Task при його старті. Якщо ж виняток кинутий від **іншого** токену (не того, що у Task), стан буде `Faulted`:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

using CancellationTokenSource cts = new CancellationTokenSource();

// Передаємо token у Task.Run — він знає про "свій" токен
Task task = Task.Run(async () =>
{
    await Task.Delay(500, cts.Token);
}, cts.Token);

cts.Cancel(); // скасовуємо

try { await task; } catch (OperationCanceledException) { }

// Task знає, що скасовано через "свій" токен → Canceled
Console.WriteLine($"Status:      {task.Status}");      // Canceled
Console.WriteLine($"IsCanceled:  {task.IsCanceled.ToString()}");   // true
Console.WriteLine($"IsFaulted:   {task.IsFaulted.ToString()}");    // false
```

Розрізнення `Canceled` і `Faulted` важливе для коду, що аналізує стан завдань після їх завершення — наприклад, при побудові retry-логіки або логування помилок.
