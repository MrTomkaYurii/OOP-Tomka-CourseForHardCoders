---
chapter: 16
chapterTitle: "Розділ 16. Паралельне програмування та TPL"
section: 5
number: "16.5"
title: "Скасування завдань. CancellationToken"
source: ""
---

## 16.5. Скасування завдань. CancellationToken

У реальних системах завдання нерідко потрібно зупинити достроково: користувач натиснув «Скасувати», сплив тайм-аут, виникла аварійна ситуація або система перевантажена. Примусове завершення потоку через `Thread.Abort()` давно застаріло і вилучено з .NET 5+: воно небезпечне, бо залишає ресурси неприбраними. Правильний підхід — **кооперативне скасування** через `CancellationToken`.

Концепція кооперативного скасування полягає в тому, що завдання саме перевіряє, чи не надійшов сигнал скасування, і коректно завершується у зручний момент — після звільнення ресурсів, запису незавершеного результату, закриття з'єднань. Жодного примусового переривання — лише добровільна відповідь на запит.

## Ключові типи

| Тип | Роль |
|-----|------|
| `CancellationTokenSource` | Джерело сигналу скасування. Тільки він може викликати `Cancel()` |
| `CancellationToken` | Токен — «квиток» з інформацією про скасування. Передається у завдання |
| `OperationCanceledException` | Виняток, що сигналізує про кооперативне скасування |

Розподіл ролей чіткий: **той хто управляє** (зовнішній код) тримає `CancellationTokenSource` і вирішує, коли скасувати. **Завдання** отримує лише `CancellationToken` — воно може лише перевірити стан, але не може само себе скасувати через чужий джерело.

![Механізм скасування завдань: CancellationToken](_assets/16-05/cancellation-flow.png)

## Спосіб 1: м'яке скасування через IsCancellationRequested

Найпростіший підхід — завдання регулярно перевіряє `token.IsCancellationRequested` і виходить через `return` при виявленні сигналу. Стан завдання після цього — `RanToCompletion` (успішне завершення), оскільки виняток не кидався:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

CancellationTokenSource cts = new CancellationTokenSource();
CancellationToken token = cts.Token;

Task monitoring = Task.Run(() =>
{
    Console.WriteLine("[Моніторинг] Систему моніторингу запущено");
    int cycle = 0;

    while (!token.IsCancellationRequested) // цикл до сигналу скасування
    {
        cycle++;
        Console.WriteLine($"[Моніторинг] Цикл {cycle.ToString()}: пульс 72, тиск 120/80");
        Thread.Sleep(200);
    }

    // Виходимо коректно — зберігаємо стан, звільняємо ресурси
    Console.WriteLine($"[Моніторинг] Отримано сигнал зупинки. Завершено після {cycle.ToString()} циклів.");
}, token);

Thread.Sleep(700); // даємо поопрацювати
Console.WriteLine("[Main] Надсилаю сигнал скасування моніторингу...");
cts.Cancel();

monitoring.Wait();
Console.WriteLine($"[Main] Статус: {monitoring.Status}"); // RanToCompletion
cts.Dispose();
```

М'яке скасування підходить для довгих циклічних операцій, де є зручна точка перевірки між ітераціями.

## Спосіб 2: жорстке скасування через ThrowIfCancellationRequested

`token.ThrowIfCancellationRequested()` кидає `OperationCanceledException`, якщо надійшов сигнал скасування. Завдання переходить у стан `Canceled`. При виклику `Wait()` або `Result` зовнішній код отримає `AggregateException` з `TaskCanceledException` всередині:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

CancellationTokenSource cts = new CancellationTokenSource();

Task dataExport = Task.Run(() =>
{
    Console.WriteLine("[Експорт] Початок експорту медичних даних...");

    for (int i = 1; i <= 20; i++)
    {
        token.ThrowIfCancellationRequested(); // кидає виняток при Cancel()

        Console.WriteLine($"[Експорт] Пакет {i.ToString()}/20 відправлено");
        Thread.Sleep(100);
    }

    Console.WriteLine("[Експорт] Експорт завершено повністю");
}, cts.Token);

CancellationToken token = cts.Token;

Thread.Sleep(450); // скасовуємо після ~4 пакетів
Console.WriteLine("[Main] Скасовую експорт (адміністратор зупинив)...");
cts.Cancel();

try
{
    dataExport.Wait();
}
catch (AggregateException ae)
{
    foreach (var ex in ae.InnerExceptions)
    {
        if (ex is TaskCanceledException)
            Console.WriteLine("[Main] Завдання коректно скасовано");
        else
            Console.WriteLine($"[Main] Неочікувана помилка: {ex.Message}");
    }
}

Console.WriteLine($"[Main] Статус: {dataExport.Status}"); // Canceled
cts.Dispose();
```

Жорстке скасування підходить для задач, де після отримання сигналу скасування продовжувати виконання немає сенсу і завдання може бути перервано в будь-якій точці перевірки.

## Перевірка стану: IsCanceled vs IsFaulted

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

CancellationTokenSource cts = new CancellationTokenSource();

Task task = Task.Run(() =>
{
    Thread.Sleep(500);
    cts.Token.ThrowIfCancellationRequested();
}, cts.Token);

cts.Cancel(); // скасовуємо одразу

try { task.Wait(); } catch (AggregateException) { }

Console.WriteLine($"IsCanceled:  {task.IsCanceled.ToString()}");   // true
Console.WriteLine($"IsFaulted:   {task.IsFaulted.ToString()}");    // false
Console.WriteLine($"IsCompleted: {task.IsCompleted.ToString()}");  // true (всі завершені стани)
Console.WriteLine($"Status:      {task.Status}");                   // Canceled
cts.Dispose();
```

## Реєстрація обробника: Register()

`CancellationToken.Register()` дозволяє зареєструвати делегат, який буде викликаний **при скасуванні**. Це аналог події скасування — корисний для звільнення ресурсів, логування або надсилання повідомлень:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

CancellationTokenSource cts = new CancellationTokenSource();

// Реєструємо обробник скасування
cts.Token.Register(() =>
{
    Console.WriteLine("[Register] Сигнал скасування отримано — повідомляю адміністратора");
    Console.WriteLine("[Register] Зберігаю проміжний стан до бази даних...");
});

Task longTask = Task.Run(() =>
{
    Console.WriteLine("[Task] Тривала обробка даних розпочата...");
    for (int i = 0; i < 10; i++)
    {
        cts.Token.ThrowIfCancellationRequested();
        Console.WriteLine($"[Task] Крок {i.ToString()}...");
        Thread.Sleep(150);
    }
}, cts.Token);

Thread.Sleep(400);
cts.Cancel(); // обробник Register() викличеться тут

try { longTask.Wait(); } catch (AggregateException) { }
Console.WriteLine("[Main] Завдання завершено");
cts.Dispose();
```

Обробник `Register()` викликається синхронно в тому потоці, що викликав `Cancel()`. Якщо зареєстровано кілька обробників, вони викликаються у порядку реєстрації.

## CancelAfter — автоматичне скасування за тайм-аутом

`CancellationTokenSource.CancelAfter(ms)` автоматично надсилає сигнал скасування через вказану кількість мілісекунд. Це стандартний спосіб реалізації тайм-аутів:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

using CancellationTokenSource cts = new CancellationTokenSource();
cts.CancelAfter(500); // автоматичне скасування через 500мс

Task networkCall = Task.Run(() =>
{
    Console.WriteLine("[Запит] Звертаюсь до зовнішньої бази даних...");
    Thread.Sleep(800); // запит займає 800мс — більше за тайм-аут
    cts.Token.ThrowIfCancellationRequested();
    Console.WriteLine("[Запит] Дані отримано");
}, cts.Token);

try
{
    networkCall.Wait();
    Console.WriteLine("[Main] Запит успішний");
}
catch (AggregateException)
{
    Console.WriteLine("[Main] Тайм-аут: зовнішня база не відповіла вчасно");
    Console.WriteLine("[Main] Використовую кешовані дані");
}
```

## Скасування у Parallel.For і Parallel.ForEach

`CancellationToken` передається у `Parallel` через `ParallelOptions`. При скасуванні `Parallel` зупиняє нові ітерації і кидає `OperationCanceledException`:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

CancellationTokenSource cts = new CancellationTokenSource();

ParallelOptions options = new ParallelOptions
{
    CancellationToken    = cts.Token,
    MaxDegreeOfParallelism = 3
};

// Скасовуємо через 300мс
Task.Run(() => { Thread.Sleep(300); cts.Cancel(); });

try
{
    Parallel.For(0, 20, options, i =>
    {
        Console.WriteLine($"[Parallel] Обробка пацієнта #{i.ToString()}...");
        Thread.Sleep(200);
        Console.WriteLine($"[Parallel] Пацієнт #{i.ToString()} оброблено");
    });
}
catch (OperationCanceledException)
{
    Console.WriteLine("[Main] Паралельний цикл скасовано — отримано сигнал зупинки");
}

Console.WriteLine("[Main] Система зупинена коректно");
cts.Dispose();
```

## Пов'язані токени (Linked tokens)

Іноді потрібно об'єднати кілька джерел скасування: наприклад, зовнішній тайм-аут **або** натискання «Скасувати». `CancellationTokenSource.CreateLinkedTokenSource` створює новий токен, що спрацьовує при скасуванні будь-якого з переданих:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

// Два незалежних джерела скасування
using CancellationTokenSource userCancel    = new CancellationTokenSource();
using CancellationTokenSource timeoutCancel = new CancellationTokenSource();
timeoutCancel.CancelAfter(600); // тайм-аут 600мс

// Об'єднаний токен — спрацює при Cancel() на будь-якому з двох
using CancellationTokenSource linked =
    CancellationTokenSource.CreateLinkedTokenSource(userCancel.Token, timeoutCancel.Token);

Task surgery = Task.Run(() =>
{
    Console.WriteLine("[Операція] Хірургічна операція розпочата...");
    for (int i = 1; i <= 20; i++)
    {
        linked.Token.ThrowIfCancellationRequested();
        Console.WriteLine($"[Операція] Крок {i.ToString()}/20");
        Thread.Sleep(100);
    }
    Console.WriteLine("[Операція] Операція завершена успішно");
}, linked.Token);

// Симулюємо: або користувач скасує, або тайм-аут — хто перший
// userCancel.Cancel(); // розкоментуйте, щоб перевірити ручне скасування

try
{
    surgery.Wait();
    Console.WriteLine("[Main] Операція пройшла успішно");
}
catch (AggregateException)
{
    string reason = userCancel.IsCancellationRequested ? "рішення хірурга" : "перевищено тайм-аут";
    Console.WriteLine($"[Main] Операцію зупинено: {reason}");
}
```

Пов'язані токени — потужний інструмент для реалізації складних стратегій скасування, де кілька незалежних подій можуть ініціювати зупинку однієї операції. Після завершення їх потрібно утилізувати через `Dispose()` (або `using`), щоб звільнити ресурси.
