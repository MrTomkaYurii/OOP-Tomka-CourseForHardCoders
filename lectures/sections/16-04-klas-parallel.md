---
chapter: 16
chapterTitle: "Розділ 16. Паралельне програмування та TPL"
section: 4
number: "16.4"
title: "Клас Parallel"
source: ""
---

## 16.4. Клас Parallel

Клас `System.Threading.Tasks.Parallel` надає зручні статичні методи для паралельного виконання операцій, не вимагаючи явного створення і управління завданнями. Він автоматично розподіляє роботу між доступними ядрами процесора і чекає завершення всіх паралельних операцій перед поверненням.

На відміну від `Task.Run()`, де розробник явно описує кожне завдання, `Parallel` орієнтований на масові паралельні операції: виконання набору незалежних дій, паралельний обхід колекцій, паралельний цикл. Він ефективний, коли є багато однотипних незалежних завдань, що добре розпаралелюються.

## Parallel.Invoke — паралельне виконання дій

`Parallel.Invoke` приймає довільний набір делегатів `Action` і виконує їх паралельно. Метод повертається тільки після завершення **всіх** переданих дій:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Console.WriteLine("Початок комплексного обстеження пацієнта Петренко І.О.");

Parallel.Invoke(
    () => {
        Console.WriteLine($"[Task {Task.CurrentId}] Аналіз крові...");
        Thread.Sleep(400);
        Console.WriteLine($"[Task {Task.CurrentId}] Аналіз крові: готово");
    },
    () => {
        Console.WriteLine($"[Task {Task.CurrentId}] ЕКГ-запис...");
        Thread.Sleep(300);
        Console.WriteLine($"[Task {Task.CurrentId}] ЕКГ: готово");
    },
    () => {
        Console.WriteLine($"[Task {Task.CurrentId}] УЗД черевної порожнини...");
        Thread.Sleep(500);
        Console.WriteLine($"[Task {Task.CurrentId}] УЗД: готово");
    },
    () => {
        Console.WriteLine($"[Task {Task.CurrentId}] Рентген грудної клітини...");
        Thread.Sleep(350);
        Console.WriteLine($"[Task {Task.CurrentId}] Рентген: готово");
    }
);

Console.WriteLine("Комплексне обстеження завершено — всі результати готові");
```

`Parallel.Invoke` не гарантує порядку виконання і не гарантує, що кожна дія виконається в окремому потоці — якщо ядер менше, ніж дій, деякі дії будуть почергувати. Але результат завжди правильний: метод поверне управління тільки після завершення всіх.

## Parallel.For — паралельний цикл for

`Parallel.For(fromInclusive, toExclusive, body)` виконує тіло циклу паралельно для всіх індексів у діапазоні `[from, to)`. Планувальник TPL автоматично розбиває діапазон на пакети і виконує їх у потоках пулу:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

string[] patients = { "Коваль М.", "Петренко І.", "Бойко О.", "Мороз В.", "Сидоренко Т." };

Console.WriteLine("Масовий розрахунок ризиків для пацієнтів:");

Parallel.For(0, patients.Length, i =>
{
    // i — індекс ітерації, кожна може виконуватись у різних потоках
    string patient = patients[i];
    Console.WriteLine($"[Потік {Thread.CurrentThread.ManagedThreadId.ToString()}] Розрахунок ризику: {patient}");
    Thread.Sleep(200); // імітуємо обчислення
    Console.WriteLine($"[Потік {Thread.CurrentThread.ManagedThreadId.ToString()}] Ризик {patient}: низький");
});

Console.WriteLine("Розрахунок завершено для всіх пацієнтів");
```

Зверніть: в одній ітерації використовується `Thread.CurrentThread.ManagedThreadId` — він показує, що різні ітерації можуть виконуватись у різних потоках пулу.

## Parallel.ForEach — паралельний обхід колекції

`Parallel.ForEach` — аналог `Parallel.For`, але замість індексів він приймає колекцію `IEnumerable<T>` і виконує тіло для кожного елемента паралельно:

```csharp run
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

List<string> labOrders = new List<string>
{
    "Кров-Коваль",  "Сеча-Бойко",   "Мокрота-Мороз",
    "Кров-Руденко", "ЕКГ-Шевченко", "Кров-Гриценко"
};

Console.WriteLine("Лабораторія: паралельна обробка замовлень");

ParallelLoopResult result = Parallel.ForEach(labOrders, order =>
{
    Console.WriteLine($"[Потік {Thread.CurrentThread.ManagedThreadId.ToString()}] Обробка: {order}");
    Thread.Sleep(200);
    Console.WriteLine($"[Потік {Thread.CurrentThread.ManagedThreadId.ToString()}] Готово: {order}");
});

Console.WriteLine($"IsCompleted: {result.IsCompleted.ToString()}");
Console.WriteLine("Всі замовлення оброблено");
```

Метод повертає структуру `ParallelLoopResult` з двома властивостями:
- `IsCompleted` — `true`, якщо цикл пройшов до кінця без переривань
- `LowestBreakIteration` — індекс, на якому відбулось переривання через `Break()`, або `null`

![Послідовне vs паралельне виконання](_assets/16-04/parallel-vs-sequential.png)

## ParallelLoopState: керування циклом

Звичайний `break` у тілі `Parallel.For` викличе помилку компілятора — ви не можете використовувати `break` у лямбді. Натомість `Parallel` надає об'єкт `ParallelLoopState`, який передається як другий параметр:

### Break() — зупинка після поточного діапазону

`pls.Break()` сигналізує планувальнику, що після завершення всіх ітерацій **з індексом, меншим за поточний**, подальші ітерації не потрібні. Це не негайна зупинка — ітерації з вищими індексами, що вже запущені, продовжать виконуватись:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Console.WriteLine("Пошук першого пацієнта з критичним показником:");

ParallelLoopResult result = Parallel.For(0, 20, (i, pls) =>
{
    if (pls.ShouldExitCurrentIteration) return; // перевіряємо перед роботою

    int pulse = 60 + i * 4; // симуляція: пульс зростає з індексом
    Console.WriteLine($"  Пацієнт #{i.ToString()}: пульс {pulse.ToString()} уд/хв");
    Thread.Sleep(30);

    if (pulse > 110) // знайшли критичний показник
    {
        Console.WriteLine($"  *** Критичний пульс у пацієнта #{i.ToString()} — зупиняю пошук ***");
        pls.Break();
    }
});

Console.WriteLine($"\nIsCompleted: {result.IsCompleted.ToString()}");
Console.WriteLine($"LowestBreakIteration: {result.LowestBreakIteration?.ToString() ?? "null"}");
```

### Stop() — негайна зупинка

`pls.Stop()` вимагає припинити весь цикл якнайшвидше — навіть вже запущені ітерації повинні перевіряти `pls.IsStopped` і завершуватись достроково. Після `Stop()` `LowestBreakIteration` завжди `null`, а `IsCompleted` — `false`:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Console.WriteLine("Перевірка показників: зупинка при виявленні небезпечного стану");

Parallel.ForEach(new[] { 72, 68, 145, 89, 55, 130 }, (pulse, pls) =>
{
    if (pls.IsStopped) return; // якщо зупинено — виходимо негайно

    Console.WriteLine($"[Потік {Thread.CurrentThread.ManagedThreadId.ToString()}] Пульс: {pulse.ToString()} уд/хв");

    if (pulse > 130)
    {
        Console.WriteLine($"  !!! НЕБЕЗПЕКА: пульс {pulse.ToString()} — НЕГАЙНА ЗУПИНКА СИСТЕМИ !!!");
        pls.Stop(); // зупиняємо весь цикл
    }
});

Console.WriteLine("Перевірку завершено");
```

**Break vs Stop**: `Break` гарантує, що всі ітерації до поточної будуть виконані (корисно для пошуку з гарантованим покриттям). `Stop` зупиняє якнайшвидше без гарантій покриття (корисно для раннього виходу при знайденні умови).

## ParallelOptions: налаштування паралелізму

`ParallelOptions` дозволяє налаштувати поведінку `Parallel.For/ForEach/Invoke`. Найважливіша властивість — `MaxDegreeOfParallelism`: максимальна кількість одночасно виконуваних ітерацій.

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

ParallelOptions options = new ParallelOptions
{
    MaxDegreeOfParallelism = 2 // не більше 2 паралельних операцій одночасно
};

string[] patients = { "Коваль", "Бойко", "Мороз", "Петренко", "Руденко", "Шевченко" };

Console.WriteLine("Обробка з обмеженням 2 паралельні операції:");

Parallel.ForEach(patients, options, patient =>
{
    Console.WriteLine($"[Потік {Thread.CurrentThread.ManagedThreadId.ToString()}] Початок: {patient}");
    Thread.Sleep(300);
    Console.WriteLine($"[Потік {Thread.CurrentThread.ManagedThreadId.ToString()}] Готово: {patient}");
});

Console.WriteLine("Завершено");
```

`MaxDegreeOfParallelism = 1` фактично перетворює паралельний цикл на послідовний — корисно для налагодження. `MaxDegreeOfParallelism = -1` (значення за замовчуванням) означає «без обмежень» — TPL сам вирішує.

У реальних системах обмеження паралелізму важливе: якщо кожен потік відкриває з'єднання з базою даних або відправляє мережевий запит, необмежений паралелізм може перевантажити зовнішній ресурс.

## Коли Parallel не прискорює

`Parallel` — не срібна куля. Є сценарії, де паралелізація не допомагає або навіть шкодить:

**Занадто короткі ітерації.** Якщо тіло циклу займає мікросекунди, накладні витрати на планування задач у TPL (теж мікросекунди) можуть перевищити виграш від паралелізму. `Parallel.For` є ефективним, коли кожна ітерація займає щонайменше кілька мілісекунд.

**Операції із спільним станом без синхронізації.** Якщо всі ітерації змінюють одну змінну без `lock`, виникне race condition. Якщо додати `lock` — паралелізм де-факто зникне через серіалізацію доступу.

**Послідовна природа даних.** Якщо кожна ітерація залежить від результату попередньої, паралелізація неможлива — задачу потрібно переосмислити.

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

// Приклад коректного паралельного накопичення через Interlocked
int totalProcessed = 0;

Parallel.For(0, 100, i =>
{
    Thread.Sleep(5); // коротка робота
    Interlocked.Increment(ref totalProcessed); // атомарний інкремент без lock
});

Console.WriteLine($"Оброблено записів: {totalProcessed.ToString()}");
```

`Interlocked.Increment` — атомарна операція збільшення цілого числа, яка не потребує `lock`. Для простих лічильників у паралельних циклах це ефективніше за `lock (obj) { count++; }`.
