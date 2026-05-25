---
chapter: 17
chapterTitle: "Розділ 17. Асинхронне програмування"
section: 3
number: "17.3"
title: "Послідовне та паралельне виконання. Task.WhenAll та Task.WhenAny"
source: ""
---

## 17.3. Послідовне та паралельне виконання. Task.WhenAll та Task.WhenAny

У реальних асинхронних системах рідко виникає потреба виконати лише одну операцію. Зазвичай потрібно координувати кілька: завантажити кілька ресурсів, дочекатися першого результату з набору джерел, або збудувати складний конвеєр обробки. Для цього C# надає два потужні комбінатори: `Task.WhenAll` і `Task.WhenAny`.

![Послідовне vs паралельне виконання в async](_assets/17-03/sequential-vs-parallel-async.png)

## Послідовне виконання — коли порядок має значення

Якщо кожна наступна операція залежить від результату попередньої, виконання мусить бути послідовним. `await` кожного кроку по черзі — природній спосіб висловити цю залежність:

```csharp run
using System;
using System.Threading.Tasks;

// Крок 1: авторизація → Крок 2: завантаження картки → Крок 3: збереження змін
// Кожен крок залежить від попереднього — порядок обов'язковий

async Task<string> AuthorizeUserAsync(string login)
{
    Console.WriteLine($"[Auth] Перевірка облікових даних: {login}");
    await Task.Delay(100);
    return $"token_{login}_2024";
}

async Task<string> LoadPatientCardAsync(string authToken, string patientId)
{
    Console.WriteLine($"[Load] Завантаження картки {patientId} (token: {authToken[..8]}...)");
    await Task.Delay(200);
    return $"Карта {patientId}: Петренко І.О., 45р, Діагноз: J06.9";
}

async Task SaveDiagnosisAsync(string authToken, string cardData, string diagnosis)
{
    Console.WriteLine($"[Save] Збереження діагнозу для: {cardData[..20]}...");
    await Task.Delay(150);
    Console.WriteLine($"[Save] Діагноз '{diagnosis}' збережено успішно");
}

var sw = System.Diagnostics.Stopwatch.StartNew();

// Послідовно — крок за кроком, кожен чекає попереднього
string token    = await AuthorizeUserAsync("dr.petrenko");
string card     = await LoadPatientCardAsync(token, "PT-2024-007");
await SaveDiagnosisAsync(token, card, "J06.9 — ГРВІ");

sw.Stop();
Console.WriteLine($"\nЗагальний час: {sw.ElapsedMilliseconds.ToString()} мс (послідовно)");
```

Послідовне виконання — правильний вибір, коли операції пов'язані ланцюгом залежностей. Загальний час дорівнює сумі часів усіх кроків.

## Паралельне виконання — коли операції незалежні

Якщо кілька операцій не залежать одна від одної, їх можна запустити одночасно. Ключова ідея: **не `await` кожну операцію одразу — спочатку запусти всі, потім очікуй всіх**:

```csharp run
using System;
using System.Threading.Tasks;

async Task<string> RunLabTestAsync(string testName, int durationMs)
{
    Console.WriteLine($"  → Розпочато: {testName}");
    await Task.Delay(durationMs);
    string result = $"{testName}: норма";
    Console.WriteLine($"  ✓ Завершено: {result} ({durationMs.ToString()} мс)");
    return result;
}

Console.WriteLine("=== Послідовно ===");
var sw1 = System.Diagnostics.Stopwatch.StartNew();
string r1 = await RunLabTestAsync("Аналіз крові",  400);
string r2 = await RunLabTestAsync("Аналіз сечі",   250);
string r3 = await RunLabTestAsync("ЕКГ",           300);
sw1.Stop();
Console.WriteLine($"Послідовно: {sw1.ElapsedMilliseconds.ToString()} мс\n");

Console.WriteLine("=== Паралельно (запускаємо всі, потім очікуємо) ===");
var sw2 = System.Diagnostics.Stopwatch.StartNew();
Task<string> t1 = RunLabTestAsync("Аналіз крові",  400); // запуск — не await
Task<string> t2 = RunLabTestAsync("Аналіз сечі",   250); // запуск — не await
Task<string> t3 = RunLabTestAsync("ЕКГ",           300); // запуск — не await

// Тепер очікуємо всі три
string res1 = await t1;
string res2 = await t2;
string res3 = await t3;
sw2.Stop();
Console.WriteLine($"Паралельно: {sw2.ElapsedMilliseconds.ToString()} мс");
Console.WriteLine($"Виграш: ~{(sw1.ElapsedMilliseconds - sw2.ElapsedMilliseconds).ToString()} мс");
```

Загальний час паралельного виконання — час найдовшої операції (~400 мс замість ~950 мс). Звісно, це справедливо тільки для справді незалежних операцій.

## Task.WhenAll — очікування всіх завдань

`Task.WhenAll` — найчистіший спосіб запустити кілька завдань паралельно і дочекатися їх усіх. Він приймає колекцію Task або масив Task<T> і повертає Task, що завершується, коли завершаться **всі** передані завдання:

```csharp run
using System;
using System.Threading.Tasks;

async Task<double> MeasureGlucoseAsync()
{
    await Task.Delay(300);
    return 5.4; // ммоль/л
}

async Task<int> MeasurePulseAsync()
{
    await Task.Delay(200);
    return 72; // уд/хв
}

async Task<string> GetPatientStatusAsync()
{
    await Task.Delay(250);
    return "Стабільний";
}

var sw = System.Diagnostics.Stopwatch.StartNew();

// Task.WhenAll з Task<T> різних типів — запускаємо всі одразу
Task<double> glucoseTask = MeasureGlucoseAsync();
Task<int>    pulseTask   = MeasurePulseAsync();
Task<string> statusTask  = GetPatientStatusAsync();

await Task.WhenAll(glucoseTask, pulseTask, statusTask);

sw.Stop();

// Результати доступні через .Result (Task вже завершений — Result не блокує)
Console.WriteLine($"Глюкоза:  {glucoseTask.Result.ToString()} ммоль/л");
Console.WriteLine($"Пульс:    {pulseTask.Result.ToString()} уд/хв");
Console.WriteLine($"Статус:   {statusTask.Result}");
Console.WriteLine($"Час:      {sw.ElapsedMilliseconds.ToString()} мс (паралельно)");
```

### Task.WhenAll з масивом однотипних завдань

Якщо всі завдання мають однаковий тип `Task<T>`, `WhenAll` повертає `Task<T[]>` — масив результатів у порядку вихідних завдань:

```csharp run
using System;
using System.Linq;
using System.Threading.Tasks;

async Task<string> GetPatientHistoryAsync(string id)
{
    await Task.Delay(100 + id.GetHashCode() % 100);
    return $"Анамнез {id}: без особливостей";
}

string[] patientIds = { "PT-001", "PT-002", "PT-003", "PT-004", "PT-005" };

// Запускаємо завдання для всіх пацієнтів одночасно
Task<string>[] tasks = patientIds
    .Select(id => GetPatientHistoryAsync(id))
    .ToArray();

// WhenAll з Task<T>[] повертає Task<T[]>
string[] histories = await Task.WhenAll(tasks);

Console.WriteLine("Анамнези всіх пацієнтів:");
foreach (string h in histories)
    Console.WriteLine($"  {h}");
```

### Обробка помилок у Task.WhenAll

`Task.WhenAll` дочікується **всіх** завдань, навіть якщо деякі завершились з помилкою. Після завершення він кидає `AggregateException`, що містить всі помилки від усіх завдань, що завершились невдало:

```csharp run
using System;
using System.Threading.Tasks;

async Task<string> FetchDataAsync(string source, bool willFail)
{
    await Task.Delay(100);
    if (willFail) throw new Exception($"Сервер '{source}' недоступний");
    return $"Дані з {source}";
}

Task<string> t1 = FetchDataAsync("Лабораторія",  willFail: false);
Task<string> t2 = FetchDataAsync("Рентген",       willFail: true);  // помилка
Task<string> t3 = FetchDataAsync("ЕКГ-система",  willFail: false);
Task<string> t4 = FetchDataAsync("Аптека",        willFail: true);  // помилка

try
{
    string[] results = await Task.WhenAll(t1, t2, t3, t4);
    // Цей рядок НЕ виконається — є помилки
}
catch (Exception ex)
{
    // await розгортає першу помилку з AggregateException
    Console.WriteLine($"Перша помилка: {ex.Message}");
}

// Щоб отримати ВСІ помилки — аналізуємо Task.Exception після WhenAll
Console.WriteLine("\nВсі помилки:");
foreach (Task<string> t in new[] { t1, t2, t3, t4 })
{
    if (t.IsFaulted)
        Console.WriteLine($"  ✗ {t.Exception?.InnerException?.Message}");
    else if (t.IsCompletedSuccessfully)
        Console.WriteLine($"  ✓ {t.Result}");
}
```

Важлива деталь: `await Task.WhenAll(...)` при помилці розгортає лише першу з виключень. Щоб отримати всі помилки, потрібно аналізувати `task.Exception.InnerExceptions` для кожного завдання після завершення WhenAll.

## Task.WhenAny — очікування першого завдання

`Task.WhenAny` завершується, щойно **перше** з переданих завдань завершиться (успішно або з помилкою). Це корисно для сценаріїв: «отримати відповідь від найшвидшого сервера», «реалізувати тайм-аут», «обробляти результати по мірі готовності»:

```csharp run
using System;
using System.Threading.Tasks;

async Task<string> QueryServerAsync(string server, int delay)
{
    Console.WriteLine($"  → Запит до {server}...");
    await Task.Delay(delay);
    Console.WriteLine($"  ✓ Відповідь від {server} ({delay.ToString()} мс)");
    return $"Дані від {server}";
}

// Надсилаємо запит до трьох серверів одночасно — беремо найшвидшу відповідь
Task<string> server1 = QueryServerAsync("Київ",    500);
Task<string> server2 = QueryServerAsync("Харків",  200); // найшвидший
Task<string> server3 = QueryServerAsync("Львів",   350);

Task<string> fastest = await Task.WhenAny(server1, server2, server3);
Console.WriteLine($"\nПерша відповідь: {await fastest}");
Console.WriteLine("(Інші запити продовжуються у фоні)");
```

### Тайм-аут через Task.WhenAny + Task.Delay

Один з найпоширеніших патернів з `WhenAny` — реалізація тайм-ауту для асинхронної операції:

```csharp run
using System;
using System.Threading.Tasks;

async Task<string> SlowDatabaseQueryAsync()
{
    Console.WriteLine("[DB] Виконую складний запит...");
    await Task.Delay(800); // запит займає 800мс
    return "Результат запиту";
}

int timeoutMs = 500; // тайм-аут 500мс

Task<string> queryTask   = SlowDatabaseQueryAsync();
Task         timeoutTask = Task.Delay(timeoutMs);

Task completed = await Task.WhenAny(queryTask, timeoutTask);

if (completed == timeoutTask)
{
    Console.WriteLine($"[Main] Тайм-аут! Запит перевищив {timeoutMs.ToString()} мс");
    Console.WriteLine("[Main] Використовую кешовані дані");
}
else
{
    string result = await queryTask; // queryTask вже завершений — await не блокує
    Console.WriteLine($"[Main] Отримано вчасно: {result}");
}
```

Зверніть: `Task.WhenAny` не скасовує інші завдання — `SlowDatabaseQueryAsync` продовжить виконуватись у фоні навіть після тайм-ауту. Щоб коректно скасувати, потрібно `CancellationToken` (розглядається у розділі 17.5).

### Обробка результатів по мірі готовності

`WhenAny` дозволяє обробляти результати одразу, як вони з'являються, без очікування всіх:

```csharp run
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

async Task<string> ProcessSampleAsync(int sampleId, int ms)
{
    await Task.Delay(ms);
    return $"Зразок #{sampleId.ToString()}: аналіз завершено ({ms.ToString()} мс)";
}

// Запускаємо аналіз 5 зразків паралельно
List<Task<string>> pending = new List<Task<string>>
{
    ProcessSampleAsync(1, 400),
    ProcessSampleAsync(2, 100),
    ProcessSampleAsync(3, 250),
    ProcessSampleAsync(4, 180),
    ProcessSampleAsync(5, 320)
};

Console.WriteLine("Обробляємо результати по мірі готовності:");
while (pending.Count > 0)
{
    Task<string> done = await Task.WhenAny(pending);
    pending.Remove(done);
    Console.WriteLine($"  ✓ {await done}");
}
Console.WriteLine("Всі зразки оброблено");
```

Цей патерн дозволяє одразу реагувати на перші результати, не чекаючи найповільніших — важливо для інтерактивних систем.

## Порівняння: WhenAll vs WhenAny

| Аспект | `Task.WhenAll` | `Task.WhenAny` |
|--------|---------------|---------------|
| Завершується коли | Всі задачі завершились | Перша задача завершилась |
| Результат | `T[]` (для `Task<T>[]`) | Перша завершена `Task<T>` |
| Помилки | Збирає всі, кидає AggregateException | Тільки від першої завершеної |
| Типові сценарії | Паралельне збирання даних | Тайм-аут, перший відповів, обробка по черзі |
| Скасовує інші | Ні | Ні |

Обидва методи є фундаментальними інструментами координації async-операцій. Їх комбінація дозволяє будувати складні стратегії паралельного виконання без явного управління потоками.
