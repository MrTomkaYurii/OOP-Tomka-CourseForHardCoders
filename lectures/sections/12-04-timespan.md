---
chapter: 12
chapterTitle: "Розділ 12. Робота з датами та часом"
section: 4
number: "12.4"
title: "Структура TimeSpan"
source: "../_combined/78-timespan.md"
---

## 12.4. Структура TimeSpan

Якщо `DateTime` відповідає на питання «**коли?**» (конкретна точка в часі), то `TimeSpan` відповідає на питання «**скільки?**» (тривалість інтервалу). Наприклад: скільки тривала госпіталізація? Через скільки годин призначити повторний прийом? Яка різниця між часом надходження пацієнта і виконанням аналізу?

`TimeSpan` — це структура (value type) з простору імен `System`, що внутрішньо зберігає одне `long`-значення — кількість **тіків** (тих самих 100-наносекундних тіків, що й `DateTime`). Тому `TimeSpan` може представляти тривалість від мінусових тисячоліть до позитивних — або, точніше, від `TimeSpan.MinValue` (близько -10 мільйонів днів) до `TimeSpan.MaxValue` (близько +10 мільйонів днів).

![TimeSpan — представлення тривалості часового інтервалу](_assets/12-04/timespan-overview.png)

## TimeSpan vs DateTime vs TimeOnly

Ці три типи часто плутають. Принципова різниця:

| Тип | Що представляє | Діапазон | Може бути від'ємним? |
|-----|---------------|---------|---------------------|
| `DateTime` | Момент в часі | 01.01.0001 – 31.12.9999 | Ні |
| `TimeOnly` | Час на годиннику | 00:00:00 – 23:59:59 | Ні |
| `TimeSpan` | Тривалість | ±10 млн днів | Так |

`TimeSpan` є результатом **різниці** двох `DateTime`: `dt1 - dt2 = TimeSpan`. Але він може також виражати довільну тривалість: «через 72 години», «за 21 день», «відняти 30 хвилин».

## Створення TimeSpan

Є кілька способів створити `TimeSpan`:

```csharp
// 1. Конструктори
var ts1 = new TimeSpan(2, 30, 0);          // 2 год 30 хв 0 сек = 02:30:00
var ts2 = new TimeSpan(7, 0, 0, 0);        // 7 днів
var ts3 = new TimeSpan(0, 36, 0, 0);       // 36 годин (= 1 день 12 год)
var ts4 = new TimeSpan(1, 14, 30, 20, 500); // 1 дн 14 год 30 хв 20 сек 500 мс

// 2. Статичні методи From*
TimeSpan week   = TimeSpan.FromDays(7);       // 7 днів (7.5 = 7 днів 12 год)
TimeSpan day    = TimeSpan.FromHours(24);     // 1 день
TimeSpan hour   = TimeSpan.FromMinutes(60);   // 1 година
TimeSpan minute = TimeSpan.FromSeconds(60);   // 1 хвилина
TimeSpan zero   = TimeSpan.Zero;              // 00:00:00

// 3. З тіків
TimeSpan fromTicks = new TimeSpan(36_000_000_000L); // 1 година = 10^7 тіків/сек * 3600

// 4. Різниця двох DateTime (найчастіший спосіб)
DateTime admission = new DateTime(2026, 6, 1, 9, 0, 0);
DateTime discharge = new DateTime(2026, 6, 8, 14, 30, 0);
TimeSpan stay = discharge - admission; // 7 днів 5 год 30 хв
```

## Властивості TimeSpan: компоненти та Total*

Клас `TimeSpan` має два набори властивостей, які легко переплутати:

**Компонентні властивості** — цілочисельна частина відповідного компонента:

```csharp
TimeSpan ts = new TimeSpan(1, 14, 30, 20); // 1 день 14 год 30 хв 20 сек

Console.WriteLine(ts.Days);         // 1   — тільки дні
Console.WriteLine(ts.Hours);        // 14  — тільки години (0-23)
Console.WriteLine(ts.Minutes);      // 30  — тільки хвилини (0-59)
Console.WriteLine(ts.Seconds);      // 20  — тільки секунди (0-59)
Console.WriteLine(ts.Milliseconds); // 0
```

**Total-властивості** — загальна тривалість, виражена у відповідній одиниці як `double`:

```csharp
Console.WriteLine(ts.TotalDays);    // 1.604...  — усі дні включно із годинами
Console.WriteLine(ts.TotalHours);   // 38.50...  — усього годин (1*24 + 14 = 38)
Console.WriteLine(ts.TotalMinutes); // 2310.333  — усього хвилин
Console.WriteLine(ts.TotalSeconds); // 138620.0  — усього секунд
```

**Правило**: для відображення («госпіталізація тривала 7 днів і 5 годин») — використовуйте компонентні властивості `Days` + `Hours`; для порівняння або арифметики («чи пройшло більше 72 годин?») — `TotalHours`:

```csharp
if (stay.TotalHours > 72)
    Console.WriteLine("Пацієнт перебуває понад 3 дні");
```

## Арифметика TimeSpan

`TimeSpan` підтримує такі операції:

```csharp
TimeSpan t1 = TimeSpan.FromDays(3);
TimeSpan t2 = TimeSpan.FromHours(12);

TimeSpan sum  = t1 + t2;           // 3 дні 12 годин
TimeSpan diff = t1 - t2;           // 2 дні 12 годин
TimeSpan neg  = -t1;               // -3 дні (від'ємний)
TimeSpan abs  = t1.Duration();     // завжди невід'ємний (як Math.Abs)

// DateTime + TimeSpan → DateTime
DateTime admission  = new DateTime(2026, 6, 1, 9, 0, 0);
DateTime scheduledD = admission + TimeSpan.FromDays(21); // плановий повторний огляд
DateTime reminderT  = scheduledD - TimeSpan.FromHours(24); // нагадування за добу

// DateTime - DateTime → TimeSpan
TimeSpan elapsed    = DateTime.Now - admission; // скільки часу пройшло
```

Від'ємний `TimeSpan` виникає, коли перша дата пізніша за другу: `dt1 - dt2` де `dt1 < dt2`. Для отримання абсолютного значення — метод `Duration()` або статичний `TimeSpan.FromTicks(Math.Abs(ts.Ticks))`.

## Властивість Duration

`ts.Duration()` завжди повертає невід'ємний `TimeSpan` — аналог `Math.Abs()` для тривалості:

```csharp
DateTime d1 = new DateTime(2026, 6, 1);
DateTime d2 = new DateTime(2026, 6, 10);

TimeSpan diff1 = d2 - d1;          // +9 днів
TimeSpan diff2 = d1 - d2;          // -9 днів

Console.WriteLine(diff2.Duration()); // 9.00:00:00 (без знаку)
```

Це зручно, коли порядок дат невідомий заздалегідь — наприклад, при обчисленні відстані між двома датами в медичній статистиці без знання, яка з них раніша.

## Форматування TimeSpan

`TimeSpan` можна форматувати через `ToString()` або `$"..."`:

```csharp
TimeSpan stay = new TimeSpan(7, 5, 30, 0);

Console.WriteLine(stay);               // 7.05:30:00  — формат за замовчуванням
Console.WriteLine(stay.ToString(@"d\d\ hh\:mm")); // 7d 05:30
Console.WriteLine($"{(int)stay.TotalDays} днів {stay.Hours} годин"); // 7 днів 5 годин
```

Формат за замовчуванням `d.hh:mm:ss` — `7.05:30:00` — де перша цифра є кількістю днів. Для виводу в людиночитному вигляді зазвичай будують рядок вручну через компонентні властивості.

## Медична картка: тривалість госпіталізації — runnable приклад

```csharp run
using System;

Console.WriteLine("=== Тривалість госпіталізації ===");
Console.WriteLine($"{"Пацієнт",-22} {"Вступ",12} {"Виписка",12} {"Тривалість"}");
Console.WriteLine(new string('-', 65));

var records = new[]
{
    ("Петренко Іван",    new DateTime(2026,6,1,  9,  0, 0), new DateTime(2026,6, 8, 14, 30, 0)),
    ("Коваль Марія",     new DateTime(2026,6,3,  11, 30, 0), new DateTime(2026,6,10, 10,  0, 0)),
    ("Сидоренко Олег",   new DateTime(2026,6,10, 8,  0, 0), new DateTime(2026,6,15, 16,  0, 0)),
};

TimeSpan total = TimeSpan.Zero;
foreach (var (name, adm, dis) in records)
{
    TimeSpan stay = dis - adm;
    total += stay;
    string duration = $"{stay.Days} д. {stay.Hours} год.";
    Console.WriteLine($"{name,-22} {adm:dd.MM.yy,12} {dis:dd.MM.yy,12} {duration}");
}

Console.WriteLine(new string('-', 65));
double avgDays = total.TotalDays / records.Length;
Console.WriteLine($"Середня тривалість: {avgDays:F1} днів");

Console.WriteLine("\n=== Перевірка тривалості лікування ===");
var (_, admission, _) = records[0];
DateTime now = new DateTime(2026, 6, 5, 12, 0, 0);
TimeSpan elapsed = now - admission;

Console.WriteLine($"Пацієнт Петренко: у лікарні {elapsed.Days} дн. {elapsed.Hours} год.");
if (elapsed.TotalHours > 72)
    Console.WriteLine("  → Пройшло більше 3 діб. Потрібен повторний аналіз крові.");
```

## Планування лікування та цикли — runnable приклад

Розрахунок дат повторних прийомів і перевірка відповідності розкладу:

```csharp run
using System;

DateTime firstVisit = new DateTime(2026, 6, 11, 10, 30, 0);
TimeSpan treatmentCycle = TimeSpan.FromDays(21); // цикл лікування — 21 день
int totalCycles = 6;

Console.WriteLine("=== Розклад хіміотерапії ===");
Console.WriteLine($"Перший прийом: {firstVisit:dd.MM.yyyy HH:mm}");
Console.WriteLine($"Цикл:          {(int)treatmentCycle.TotalDays} днів");
Console.WriteLine();

Console.WriteLine($"{"Цикл",-6} {"Дата",12} {"День тижня",-12}");
Console.WriteLine(new string('-', 32));

DateTime current = firstVisit;
for (int i = 1; i <= totalCycles; i++)
{
    Console.WriteLine($"{i,-6} {current:dd.MM.yyyy,12} {current.DayOfWeek,-12}");
    current += treatmentCycle;
}

Console.WriteLine("\n=== Оцінка часу з останнього візиту ===");
DateTime lastVisit = new DateTime(2026, 5, 21, 10, 30, 0);
DateTime today     = new DateTime(2026, 6, 11, 9,  0, 0);

TimeSpan sinceVisit = today - lastVisit;
Console.WriteLine($"Минуло: {sinceVisit.Days} днів {sinceVisit.Hours} год. ({sinceVisit.TotalHours:F0} год. усього)");

TimeSpan expectedInterval = TimeSpan.FromDays(21);
TimeSpan diff = sinceVisit - expectedInterval;

if (diff.Duration().TotalHours < 48)
    Console.WriteLine("  → Пацієнт прийшов вчасно (±2 дні від плану)");
else if (diff.TotalHours > 0)
    Console.WriteLine($"  → Запізнення на {(int)diff.TotalDays} днів");
else
    Console.WriteLine($"  → Прийшов на {(int)diff.Duration().TotalDays} днів раніше");
```
