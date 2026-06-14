---
chapter: 16
chapterTitle: "Розділ 16. Паралельне програмування та TPL"
section: 3
number: "16.3"
title: "Продовження завдань. ContinueWith"
source: ""
---

## 16.3. Продовження завдань. ContinueWith

Завдання-продовження (continuation task) — це завдання, яке автоматично запускається після завершення іншого завдання. Це ключовий механізм побудови **послідовних ланцюгів обробки** (pipelines): результат одного кроку передається наступному, а кожен крок запускається лише тоді, коли попередній завершено. На відміну від `Wait()`, де поточний потік блокується в очікуванні, `ContinueWith` не блокує — він лише реєструє «що виконати потім» і повертає управління негайно.

## Базовий синтаксис ContinueWith

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

// Перше завдання — реєстрація пацієнта
Task registration = new Task(() =>
{
    Console.WriteLine($"[Task {Task.CurrentId}] Реєстрація пацієнта Бойко О.П.");
    Thread.Sleep(200);
    Console.WriteLine($"[Task {Task.CurrentId}] Реєстрацію завершено");
});

// Завдання-продовження — запускається після registration
Task examination = registration.ContinueWith(prevTask =>
{
    Console.WriteLine($"[Task {Task.CurrentId}] Огляд лікаря (після завдання {prevTask.Id.ToString()})");
    Thread.Sleep(300);
    Console.WriteLine($"[Task {Task.CurrentId}] Огляд завершено");
});

registration.Start(); // запускаємо перше завдання
examination.Wait();   // чекаємо останнього в ланцюгу

Console.WriteLine("[Main] Маршрут пацієнта пройдено");
```

Метод `ContinueWith` приймає делегат `Action<Task>` або `Action<Task<T>>` — параметр `prevTask` це посилання на попереднє завдання, що щойно завершилось. Через нього можна отримати `Id`, `Status`, `Exception` і, у разі `Task<T>`, `Result` попереднього кроку.

## Передача результату між завданнями

Найпрактичніший сценарій `ContinueWith` — ланцюг обробки, де кожен крок отримує результат попереднього через `Task<T>`:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

// Крок 1: збір анамнезу → повертає код пацієнта
Task<string> anamnesis = Task.Run(() =>
{
    Console.WriteLine("[Анамнез] Збираю скарги пацієнта...");
    Thread.Sleep(200);
    string patientCode = "PT-2024-0897";
    Console.WriteLine($"[Анамнез] Карту відкрито: {patientCode}");
    return patientCode;
});

// Крок 2: діагностика → отримує код і повертає діагноз
Task<string> diagnosis = anamnesis.ContinueWith(prev =>
{
    string code = prev.Result; // результат попереднього кроку
    Console.WriteLine($"[Діагноз] Аналізую дані картки {code}...");
    Thread.Sleep(300);
    string diag = "J06.9 — ГРВІ";
    Console.WriteLine($"[Діагноз] Встановлено: {diag}");
    return diag;
});

// Крок 3: призначення → отримує діагноз і повертає план лікування
Task<string> treatment = diagnosis.ContinueWith(prev =>
{
    string diag = prev.Result;
    Console.WriteLine($"[Лікування] Підбираю терапію для {diag}...");
    Thread.Sleep(200);
    string plan = "Парацетамол 500мг × 3/день, рясне пиття, постільний режим";
    Console.WriteLine($"[Лікування] План: {plan}");
    return plan;
});

treatment.Wait(); // чекаємо кінця ланцюга

Console.WriteLine($"\n=== Підсумок ===");
Console.WriteLine($"Діагноз:  {diagnosis.Result}");
Console.WriteLine($"Лікування: {treatment.Result}");
```

![Ланцюг ContinueWith — клінічний маршрут пацієнта](_assets/16-03/continuation-chain.png)

## Довгий ланцюг — pipeline

Кілька `ContinueWith` можна об'єднати в лінійний ланцюг, де кожен наступний крок запускається після попереднього. Такий патерн називають **pipeline** (конвеєр):

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task step1 = new Task(() =>
{
    Console.WriteLine($"[Крок 1 / Task {Task.CurrentId}] Прийом та реєстрація");
    Thread.Sleep(100);
});

Task step2 = step1.ContinueWith(t =>
{
    Console.WriteLine($"[Крок 2 / Task {Task.CurrentId}] Попередній огляд медсестри (після Task {t.Id.ToString()})");
    Thread.Sleep(150);
});

Task step3 = step2.ContinueWith(t =>
{
    Console.WriteLine($"[Крок 3 / Task {Task.CurrentId}] Огляд лікаря та діагностика (після Task {t.Id.ToString()})");
    Thread.Sleep(200);
});

Task step4 = step3.ContinueWith(t =>
{
    Console.WriteLine($"[Крок 4 / Task {Task.CurrentId}] Призначення та видача рецепту (після Task {t.Id.ToString()})");
    Thread.Sleep(100);
});

step1.Start();
step4.Wait();

Console.WriteLine("[Main] Повний маршрут пацієнта пройдено успішно");
```

Кожен крок отримує посилання на попередній Task (параметр `t`) і може перевірити його статус. Ланцюг виконується суворо послідовно, але **не блокує головний потік** між кроками — між кроками головний потік вільний.

## TaskContinuationOptions: умовні продовження

За замовчуванням `ContinueWith` запускається після завершення попереднього завдання **незалежно від результату** — чи воно успішне, чи скасоване, чи завершилось з помилкою. `TaskContinuationOptions` дозволяє вказати умову, при якій продовження запуститься:

| Опція | Коли запускається |
|-------|------------------|
| `OnlyOnRanToCompletion` | Тільки якщо попереднє завершилось успішно |
| `OnlyOnFaulted` | Тільки якщо попереднє завершилось з винятком |
| `OnlyOnCanceled` | Тільки якщо попереднє було скасовано |
| `NotOnRanToCompletion` | Якщо попереднє НЕ успішне |
| `NotOnFaulted` | Якщо попереднє НЕ з помилкою |
| `ExecuteSynchronously` | Виконати синхронно в тому ж потоці |

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task riskyAnalysis = Task.Run(() =>
{
    Console.WriteLine("[Аналіз] Запускаю аналіз зразка...");
    Thread.Sleep(200);
    throw new Exception("Зразок пошкоджено при транспортуванні");
});

// Успішне продовження — спрацює тільки якщо аналіз пройшов без помилок
Task onSuccess = riskyAnalysis.ContinueWith(
    t => Console.WriteLine($"[Успіх] Результат аналізу занесено до системи"),
    TaskContinuationOptions.OnlyOnRanToCompletion
);

// Помилкове продовження — спрацює тільки при помилці
Task onError = riskyAnalysis.ContinueWith(
    t => Console.WriteLine($"[Помилка] {t.Exception?.InnerException?.Message} — повторне взяття зразка призначено"),
    TaskContinuationOptions.OnlyOnFaulted
);

try
{
    Task.WaitAll(onSuccess, onError);
}
catch (AggregateException ae)
{
    // Завдання, що не виконались (умова не спрацювала), переходять у Canceled
    // WaitAll кине виняток для них — ігноруємо
    foreach (var ex in ae.InnerExceptions)
        if (ex is not TaskCanceledException)
            Console.WriteLine($"Неочікувана помилка: {ex.Message}");
}
```

Зверніть: якщо умова `TaskContinuationOptions` не виконана, продовження переходить у стан `Canceled` (а не просто ігнорується). Тому `WaitAll` на набір умовних продовжень може кинути `AggregateException` з `TaskCanceledException` всередині — це очікувана поведінка, яку треба обробляти.

## Обробка помилок у ланцюгу

Коли у ланцюгу виникає помилка і не перехоплюється всередині завдання, вона «підіймається» вгору через `AggregateException`. Правильний патерн — розмістити завдання-обробник помилок наприкінці ланцюга з `OnlyOnFaulted`:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task<string> step1 = Task.Run(() =>
{
    Console.WriteLine("[Крок 1] Завантаження медичної картки...");
    Thread.Sleep(100);
    return "MED-2024-0042";
});

Task<string> step2 = step1.ContinueWith(t =>
{
    Console.WriteLine($"[Крок 2] Обробка картки {t.Result}...");
    Thread.Sleep(100);
    throw new InvalidOperationException("Картка заблокована адміністратором");
    return "processed"; // недосяжний код
}, TaskContinuationOptions.OnlyOnRanToCompletion);

// Продовження-обробник помилок
Task errorHandler = step2.ContinueWith(
    t => Console.WriteLine($"[Обробник] Помилка у ланцюгу: {t.Exception?.InnerException?.Message}"),
    TaskContinuationOptions.OnlyOnFaulted
);

// Продовження при успіху
Task successHandler = step2.ContinueWith(
    t => Console.WriteLine($"[Успіх] Обробку завершено успішно"),
    TaskContinuationOptions.OnlyOnRanToCompletion
);

try { Task.WaitAll(errorHandler, successHandler); }
catch (AggregateException) { }

Console.WriteLine("[Main] Ланцюг обробки завершено");
```

Такий підхід дозволяє будувати надійні ланцюги з розгалуженням на успішний і помилковий шляхи, не вдаючись до вкладених `try/catch` всередині кожного кроку.

## TaskCompletionSource — Task під ручним керуванням

`Task.Run()` і `new Task(...)` створюють завдання, що виконують певний делегат у ThreadPool. Але іноді потрібен `Task`, що завершується **не через виконання делегата**, а в момент, коли ми самі вирішуємо. Наприклад:

- Потрібно обернути callback-based API в async-стиль
- Потрібно «сигналізувати» між частинами системи через Task
- Потрібно створити Task, що чекає зовнішньої події (таймер, WebSocket-повідомлення, результат від іншого сервісу)

Для цього існує `TaskCompletionSource<T>` (або `TaskCompletionSource` без типового параметру для `Task`):

```csharp
var tcs = new TaskCompletionSource<string>();

Task<string> task = tcs.Task; // Task, що "ще не завершений"

// Пізніше, в будь-якому місці:
tcs.SetResult("значення");    // Task завершується успішно
tcs.SetException(ex);         // Task завершується з помилкою
tcs.SetCanceled();            // Task скасовується
```

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

// Симуляція: очікуємо результат аналізу з лабораторії
// Лабораторія "дзвонить" нам через callback — ми хочемо перетворити це на Task

TaskCompletionSource<string> analysisResult = new TaskCompletionSource<string>();

// Симулюємо "фонову лабораторну систему", що надсилає результат через 300 мс
Thread labSystem = new Thread(() =>
{
    Thread.Sleep(300);
    Console.WriteLine("[Лабораторія] Аналіз завершено, надсилаю результат...");
    
    // "Сигналізуємо" очікуючому завданню
    analysisResult.SetResult("Гемоглобін: 128 г/л — норма, Глюкоза: 5.4 ммоль/л — норма");
});
labSystem.IsBackground = true;
labSystem.Start();

// Головний потік чекає результат через Task — не через Thread.Join або callback
Console.WriteLine("[Лікар] Замовив аналіз, чекаю результату...");
string result = await analysisResult.Task; // блокує асинхронно, а не синхронно
Console.WriteLine($"[Лікар] Результат отримано: {result}");
```

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

// TaskCompletionSource з обробкою помилок
TaskCompletionSource<byte[]> imageLoad = new TaskCompletionSource<byte[]>();

Thread medicalImaging = new Thread(() =>
{
    Thread.Sleep(200);
    
    bool networkError = true; // симуляція помилки
    if (networkError)
    {
        imageLoad.SetException(
            new TimeoutException("Сервер DICOM-зображень не відповідає (timeout 200ms)"));
    }
    else
    {
        imageLoad.SetResult(new byte[] { 0xFF, 0xD8, 0xFF }); // JPEG header
    }
});
medicalImaging.IsBackground = true;
medicalImaging.Start();

Console.WriteLine("[PACS] Запитую рентгенівський знімок...");
try
{
    byte[] image = await imageLoad.Task;
    Console.WriteLine($"[PACS] Зображення отримано: {image.Length} байт");
}
catch (TimeoutException ex)
{
    Console.WriteLine($"[PACS] Помилка: {ex.Message}");
    Console.WriteLine("[PACS] Призначено повторний запит через 5 хв");
}
```

`TaskCompletionSource` є «мостом» між callback/event-моделлю і сучасним async/await. Якщо ви отримали API зі старою моделлю (`BeginXxx/EndXxx`, `EventHandler`, callbacks) — `TaskCompletionSource` перетворює її у `Task`, який можна `await`-ити.

Важливо: після виклику `SetResult`, `SetException` або `SetCanceled` стан Task зафіксований — повторний виклик кине `InvalidOperationException`. Для «одноразового сигналу» є зручна альтернатива `TrySetResult`/`TrySetException`/`TrySetCanceled`, що повертають `bool` замість кидання винятку.
