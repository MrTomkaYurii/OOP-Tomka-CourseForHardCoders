---
chapter: 16
chapterTitle: "Розділ 16. Паралельне програмування та TPL"
section: 1
number: "16.1"
title: "Клас Task. Основи TPL"
source: ""
---

## 16.1. Клас Task. Основи TPL

У попередньому розділі ми розглядали багатопоточність через клас `Thread` — прямий, але низькорівневий інструмент. Ми вручну створювали потоки, передавали делегати, викликали `Join()`, піклувались про пріоритети і тип потоку (передній чи фоновий). Для простих сценаріїв це цілком прийнятно, але у реальних системах з десятками паралельних операцій такий підхід стає громіздким.

**TPL (Task Parallel Library)** — бібліотека паралельного програмування, що входить до складу .NET, починаючи з версії 4.0. Її мета — підняти рівень абстракції: замість того щоб думати про потоки, потокові пули і синхронізацію вручну, розробник описує **завдання** (tasks) — логічні одиниці роботи — і довіряє TPL ефективно їх виконати. TPL розміщена у просторі імен `System.Threading.Tasks`.

## Thread vs Task: у чому різниця

Ключова відмінність між `Thread` і `Task` — у тому, як вони використовують ресурси операційної системи. Кожен `Thread` — це окремий потік ОС із власним стеком пам'яті (~1 МБ). Створення і знищення потоку — дорога операція. Якщо програма постійно створює і знищує сотні потоків, продуктивність падає.

`Task` натомість використовує **пул потоків** (ThreadPool) — набір вже створених потоків, які очікують нової роботи. Коли завдання завершується, потік не знищується, а повертається у пул і чекає наступного завдання. Це суттєво знижує накладні витрати на створення і знищення потоків. Крім того, `Task` підтримує повернення результатів, ланцюги продовжень і скасування — все те, що з `Thread` довелось би реалізовувати вручну.

![Thread vs Task: модель виконання](_assets/16-01/thread-vs-task.png)

## Три способи створення завдання

### Спосіб 1: конструктор + Start()

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task task = new Task(() =>
{
    Console.WriteLine($"[Task {Task.CurrentId}] Реєстрація пацієнта розпочата");
    Thread.Sleep(200);
    Console.WriteLine($"[Task {Task.CurrentId}] Реєстрацію завершено");
});

task.Start(); // явний запуск
task.Wait();  // чекаємо завершення

Console.WriteLine("Головний потік: реєстрацію підтверджено");
```

Конструктор + `Start()` — найбільш явний спосіб. Він дає контроль над моментом запуску: завдання можна створити заздалегідь і запустити пізніше. `Task.CurrentId` повертає числовий ідентифікатор поточного виконуваного завдання.

### Спосіб 2: Task.Factory.StartNew()

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task task = Task.Factory.StartNew(() =>
{
    Console.WriteLine($"[Task {Task.CurrentId}] Лабораторний аналіз запущено через Factory");
    Thread.Sleep(150);
    Console.WriteLine($"[Task {Task.CurrentId}] Аналіз завершено");
});

task.Wait();
Console.WriteLine("Результат аналізу отримано");
```

`Task.Factory.StartNew()` — старіший API, що залишається актуальним для складних сценаріїв: він приймає додаткові параметри `TaskCreationOptions` і `TaskScheduler`, недоступні в `Task.Run()`. Для звичайних завдань зручніший `Task.Run()`.

### Спосіб 3: Task.Run() — сучасний рекомендований підхід

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task task = Task.Run(() =>
{
    Console.WriteLine($"[Task {Task.CurrentId}] МРТ-сканування через Task.Run");
    Thread.Sleep(300);
    Console.WriteLine($"[Task {Task.CurrentId}] МРТ завершено");
});

task.Wait();
Console.WriteLine("Знімки МРТ збережено в системі");
```

`Task.Run()` — найпростіший і найпоширеніший спосіб у сучасному коді. Він автоматично запускає завдання у пулі потоків без додаткових налаштувань. Це рекомендований підхід для переважної більшості сценаріїв.

## Властивості класу Task

Кожен об'єкт `Task` має набір властивостей, що дозволяють отримати інформацію про стан і результат виконання:

| Властивість | Тип | Опис |
|-------------|-----|------|
| `Id` | `int` | Унікальний ідентифікатор завдання (статично для зовнішнього коду) |
| `Status` | `TaskStatus` | Поточний стан: Created, Running, RanToCompletion тощо |
| `IsCompleted` | `bool` | `true` якщо завдання завершилось (успішно, з помилкою або скасоване) |
| `IsCompletedSuccessfully` | `bool` | `true` тільки при успішному завершенні |
| `IsCanceled` | `bool` | `true` якщо завдання скасовано через CancellationToken |
| `IsFaulted` | `bool` | `true` якщо завдання завершилось із необробленим винятком |
| `Exception` | `AggregateException?` | Виняток (або null) — обгортка навколо всіх внутрішніх винятків |

Статична властивість `Task.CurrentId` доступна лише всередині виконуваного завдання — повертає id поточного Task або `null` поза завданням.

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task task = Task.Run(() =>
{
    Console.WriteLine($"Id: {Task.CurrentId.ToString()}");
    Console.WriteLine($"Status всередині: {Task.CompletedTask.Status}");
    Thread.Sleep(100);
});

Console.WriteLine($"Status після Run(): {task.Status}");
task.Wait();
Console.WriteLine($"Status після Wait(): {task.Status}");
Console.WriteLine($"IsCompleted: {task.IsCompleted.ToString()}");
Console.WriteLine($"IsCompletedSuccessfully: {task.IsCompletedSuccessfully.ToString()}");
Console.WriteLine($"IsFaulted: {task.IsFaulted.ToString()}");
```

## Стани завдання (TaskStatus)

Завдання проходить через кілька станів протягом свого часу існування. Їх описує перерахування `TaskStatus`:

![Стани завдання (TaskStatus)](_assets/16-01/task-lifecycle.png)

- **Created** — завдання створено через `new Task(...)`, але ще не запущено. Стан перед `Start()`.
- **WaitingForActivation** — завдання очікує активації планувальником. У цей стан потрапляють завдання, створені через `Task.Run()` або `ContinueWith()`.
- **WaitingToRun** — завдання заплановано до виконання у пулі потоків, але вільний потік ще не отримано.
- **Running** — завдання активно виконується у потоці пулу.
- **RanToCompletion** — завдання успішно завершило виконання без винятків і скасування.
- **Canceled** — завдання завершилось через скасування за допомогою `CancellationToken`.
- **Faulted** — завдання завершилось із необробленим винятком.

## Очікування завершення завдань

### Wait() — очікування одного завдання

`task.Wait()` блокує поточний (головний) потік до завершення завдання. Якщо завдання завершилось з винятком, `Wait()` викидає `AggregateException`:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task ecg = Task.Run(() =>
{
    Console.WriteLine("[ЕКГ] Запис кардіограми...");
    Thread.Sleep(300);
    Console.WriteLine("[ЕКГ] Запис завершено");
});

Console.WriteLine("[Main] ЕКГ запущено. Чекаю результату...");
ecg.Wait(); // головний потік заблокований тут
Console.WriteLine("[Main] Кардіограма готова — аналізую");
```

### WaitAll() — очікування кількох завдань

`Task.WaitAll(tasks)` блокує поточний потік до завершення **всіх** переданих завдань:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task blood  = Task.Run(() => { Thread.Sleep(400); Console.WriteLine("Аналіз крові готовий"); });
Task urine  = Task.Run(() => { Thread.Sleep(250); Console.WriteLine("Аналіз сечі готовий"); });
Task xray   = Task.Run(() => { Thread.Sleep(350); Console.WriteLine("Рентген готовий"); });

Console.WriteLine("Всі аналізи запущені паралельно...");
Task.WaitAll(blood, urine, xray); // чекаємо всіх трьох
Console.WriteLine("Всі результати отримано — формую загальний висновок");
```

### WaitAny() — очікування першого завершеного

`Task.WaitAny(tasks)` повертає індекс першого завдання, що завершилось, і розблоковує поточний потік. Решта завдань продовжують виконуватись:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task[] tests = new Task[]
{
    Task.Run(() => { Thread.Sleep(500); Console.WriteLine("Аналіз крові готовий (500мс)"); }),
    Task.Run(() => { Thread.Sleep(200); Console.WriteLine("Аналіз сечі готовий (200мс)"); }),
    Task.Run(() => { Thread.Sleep(350); Console.WriteLine("ЕКГ готово (350мс)"); }),
};

Console.WriteLine("Чекаю на перший готовий результат...");
int firstIdx = Task.WaitAny(tests); // розблокується після першого
Console.WriteLine($"Перший результат отримано: завдання #{firstIdx.ToString()}");
Console.WriteLine("Продовжую роботу, решта завдань ще виконуються...");

Task.WaitAll(tests); // дочекаємось і решти
Console.WriteLine("Всі завдання завершено");
```

`WaitAll` підходить для сценарію «потрібні всі результати перед наступним кроком», `WaitAny` — для «почни обробку як тільки з'явиться перший результат» або реалізації тайм-аутів.

## Синхронний запуск: RunSynchronously()

Метод `RunSynchronously()` виконує завдання **синхронно в поточному потоці**, без передачі до пулу потоків. Використовується рідко — наприклад, для тестування або коли потрібно явно контролювати, у якому потоці виконується завдання:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task task = new Task(() =>
{
    Console.WriteLine($"Завдання виконується у потоці: {Thread.CurrentThread.ManagedThreadId.ToString()}");
    Console.WriteLine($"Це пул потоків? {Thread.CurrentThread.IsThreadPoolThread.ToString()}");
});

Console.WriteLine($"Головний потік: {Thread.CurrentThread.ManagedThreadId.ToString()}");
task.RunSynchronously(); // виконується тут, у поточному потоці
Console.WriteLine("Завдання завершено синхронно");
```

## Обробка винятків у завданнях

Коли в завданні виникає виняток, він не зупиняє програму автоматично. Натомість він зберігається у властивості `Task.Exception` і повторно кидається при виклику `Wait()`, `Result` або доступі до `Task.Exception`. Виняток завжди обгорнутий у `AggregateException`:

```csharp run
using System;
using System.Threading.Tasks;

Task task = Task.Run(() =>
{
    Console.WriteLine("[Task] Перевіряю дані пацієнта...");
    throw new InvalidOperationException("Медична картка не знайдена в системі");
});

try
{
    task.Wait(); // тут виняток перекидається
}
catch (AggregateException ae)
{
    foreach (var inner in ae.InnerExceptions)
        Console.WriteLine($"Помилка: {inner.Message}");
}

Console.WriteLine($"IsFaulted: {task.IsFaulted.ToString()}");
Console.WriteLine($"Status: {task.Status}");
```

`AggregateException` є оберткою, бо одне завдання теоретично може містити кілька вкладених завдань, кожне з яких може кинути свій виняток. `InnerExceptions` — колекція всіх внутрішніх винятків. У простих сценаріях вона містить один елемент.
