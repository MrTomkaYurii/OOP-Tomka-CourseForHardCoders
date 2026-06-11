---
chapter: 12
chapterTitle: "Розділ 12. Робота з датами та часом"
section: 3
number: "12.3"
title: "DateOnly та TimeOnly"
source: "../_combined/77-dateonly-ta-timeonly.md"
---

## 12.3. DateOnly та TimeOnly

Починаючи з .NET 6, мова отримала два спеціалізовані типи: `DateOnly` — лише дата без часу, і `TimeOnly` — лише час без дати. Обидва є **структурами** (struct) і розташовані в просторі імен `System`.

Навіщо вони потрібні, якщо є `DateTime`? Причина принципова: `DateTime` завжди містить обидва компоненти — і дату, і час. Для ситуацій, де час не має значення, використання `DateTime` породжує небажані питання: а що означає `00:00:00` у полі «дата народження»? Це північ UTC? Місцевий час? Відсутність часу? При передачі таких значень між серверами різних часових поясів виникають помилки конвертації.

`DateOnly` і `TimeOnly` усувають цю двозначність: вони фізично не можуть містити компонент, якого не повинно бути.

![DateOnly та TimeOnly — спеціалізовані типи для дати та часу](_assets/12-03/dateonly-timeonly.png)

## DateOnly — тільки дата

Структура `DateOnly` представляє календарну дату без будь-якої прив'язки до часу. Це ідеальний тип для: дати народження пацієнта, дати госпіталізації або виписки (якщо точний час не важливий), дати проведення аналізу, дати складання документа.

### Конструктори

```csharp
// Рік, місяць, день
DateOnly birth  = new DateOnly(1958, 4, 15);
DateOnly today  = DateOnly.FromDateTime(DateTime.Today);  // з DateTime

// Із рядка
DateOnly parsed = DateOnly.Parse("11.06.2026");

// Із порядкового номера дня від 01.01.0001
DateOnly fromN  = DateOnly.FromDayNumber(738920);
```

При використанні конструктора без параметрів структура ініціалізується датою `01.01.0001`:

```csharp
DateOnly empty = new DateOnly();
Console.WriteLine(empty); // 01.01.0001
```

Конструктор також приймає об'єкт календаря — `System.Globalization.Calendar`. Наприклад, розрахунок за юліанським календарем:

```csharp
using System.Globalization;

DateOnly julianDate = new DateOnly(2026, 1, 6, new JulianCalendar());
Console.WriteLine(julianDate); // 19.01.2026 — той самий день за григоріанським
```

Це корисно при роботі зі старими медичними архівами або документами, де дати записані за іншою системою числення.

### Властивості DateOnly

| Властивість | Опис |
|-------------|------|
| `Year` | Рік |
| `Month` | Місяць (1-12) |
| `Day` | День (1-31) |
| `DayOfWeek` | День тижня (`DayOfWeek.Monday` тощо) |
| `DayOfYear` | Порядковий номер дня у році |
| `DayNumber` | Кількість днів від 01.01.0001 |

```csharp
DateOnly date = new DateOnly(2026, 6, 11);

Console.WriteLine(date.Year);       // 2026
Console.WriteLine(date.Month);      // 6
Console.WriteLine(date.Day);        // 11
Console.WriteLine(date.DayOfWeek);  // Thursday
Console.WriteLine(date.DayOfYear);  // 162
Console.WriteLine(date.DayNumber);  // 738931
```

### Методи DateOnly

**Арифметика дат:**

```csharp
DateOnly admission = new DateOnly(2026, 6, 11);

DateOnly discharge  = admission.AddDays(7);   // 18.06.2026
DateOnly nextVisit  = discharge.AddMonths(1); // 18.07.2026
DateOnly nextYear   = admission.AddYears(1);  // 11.06.2027
DateOnly yesterday  = admission.AddDays(-1);  // 10.06.2026
```

**Різниця між датами** — через `DayNumber`:

```csharp
DateOnly start = new DateOnly(2026, 6, 1);
DateOnly end   = new DateOnly(2026, 6, 18);
int daysBetween = end.DayNumber - start.DayNumber; // 17
```

**Форматування та конвертація:**

```csharp
DateOnly date = new DateOnly(2026, 6, 11);

Console.WriteLine(date.ToShortDateString()); // 11.06.2026
Console.WriteLine(date.ToLongDateString());  // 11 червня 2026 р.
Console.WriteLine(date.ToString("yyyy-MM-dd")); // 2026-06-11

// Комбінування з часом → DateTime
TimeOnly time = new TimeOnly(9, 30);
DateTime appointment = date.ToDateTime(time); // 11.06.2026 09:30:00
```

**Порівняння:**

```csharp
DateOnly d1 = new DateOnly(2026, 6, 1);
DateOnly d2 = new DateOnly(2026, 7, 1);

bool earlier = d1 < d2;  // true
bool equal   = d1 == d1; // true
```

## TimeOnly — тільки час

Структура `TimeOnly` представляє час доби в діапазоні від `00:00:00.0000000` до `23:59:59.9999999`, без прив'язки до конкретної дати. Це ідеальний тип для: часу прийому пацієнта (понеділок 09:00), робочих годин відділення, розкладу змін медперсоналу.

Важлива відмінність від `TimeSpan` (розд. 12.4): `TimeOnly` завжди представляє **час на годиннику** (0 – 23:59), тоді як `TimeSpan` може бути більшим за 24 години або від'ємним — це **тривалість**, а не час доби.

### Конструктори

```csharp
// Різна точність
TimeOnly t1 = new TimeOnly(9, 30);         // 09:30:00
TimeOnly t2 = new TimeOnly(14, 45, 20);    // 14:45:20
TimeOnly t3 = new TimeOnly(8, 0, 0, 500);  // 08:00:00.500

// Із DateTime
TimeOnly fromDt = TimeOnly.FromDateTime(DateTime.Now);

// Із рядка
TimeOnly parsed = TimeOnly.Parse("14:30");

// Із TimeSpan
TimeOnly fromTs = TimeOnly.FromTimeSpan(new TimeSpan(9, 30, 0));
```

При використанні конструктора без параметрів — `0:00`:

```csharp
TimeOnly empty = new TimeOnly();
Console.WriteLine(empty); // 0:00
```

### Властивості TimeOnly

| Властивість | Опис |
|-------------|------|
| `Hour` | Година (0-23) |
| `Minute` | Хвилини (0-59) |
| `Second` | Секунди (0-59) |
| `Millisecond` | Мілісекунди (0-999) |
| `Ticks` | Тіки від початку дня |

```csharp
TimeOnly time = new TimeOnly(14, 23, 30);

Console.WriteLine(time.Hour);   // 14
Console.WriteLine(time.Minute); // 23
Console.WriteLine(time.Second); // 30
```

### Методи TimeOnly

**Арифметика:**

```csharp
TimeOnly start = new TimeOnly(9, 0);

TimeOnly end  = start.AddHours(8);     // 17:00 (завершення зміни)
TimeOnly mid  = start.AddMinutes(30);  // 09:30

// AddHours з переповненням через 24:00 не кидає виняток — обертається
TimeOnly night = new TimeOnly(23, 0);
TimeOnly next  = night.AddHours(2);    // 01:00 (наступний день)
```

**`IsBetween`** — перевірка, чи потрапляє час у проміжок. Корисно для перевірки, чи прийом проводиться в межах робочого часу:

```csharp
TimeOnly workStart = new TimeOnly(8, 0);
TimeOnly workEnd   = new TimeOnly(17, 0);
TimeOnly appoint   = new TimeOnly(10, 30);

bool inWork = appoint.IsBetween(workStart, workEnd); // true
```

**Конвертація:**

```csharp
TimeOnly time = new TimeOnly(14, 30, 0);

TimeSpan ts = time.ToTimeSpan(); // 14:30:00 як TimeSpan
Console.WriteLine(time.ToShortTimeString()); // 14:30
Console.WriteLine(time.ToLongTimeString());  // 14:30:00
```

## Комбінування DateOnly і TimeOnly

Найпоширеніший сценарій — призначення прийому: є дата і є час, потрібно отримати повний `DateTime`:

```csharp
DateOnly date = new DateOnly(2026, 6, 15);   // дата прийому
TimeOnly time = new TimeOnly(10, 30);         // час прийому

DateTime appointment = date.ToDateTime(time); // 15.06.2026 10:30:00
Console.WriteLine(appointment);
```

Зворотня операція — розкладання `DateTime` на компоненти:

```csharp
DateTime dt = new DateTime(2026, 6, 15, 10, 30, 0);

DateOnly d = DateOnly.FromDateTime(dt); // 15.06.2026
TimeOnly t = TimeOnly.FromDateTime(dt); // 10:30:00
```

Цей підхід особливо зручний при зберіганні розкладу в базі даних: дата і час прийому зберігаються в окремих колонках (типи SQL `date` і `time`), і при читанні легко об'єднуються назад.

## Розклад прийомів та дати народження — runnable приклад

```csharp run
using System;

Console.WriteLine("=== Список пацієнтів — дата народження ===");
var patients = new[]
{
    ("Петренко Іван",   new DateOnly(1958, 4, 15)),
    ("Коваль Марія",    new DateOnly(1978, 11, 3)),
    ("Сидоренко Олег",  new DateOnly(1951, 7, 22)),
};

DateOnly today = DateOnly.FromDateTime(DateTime.Today);
Console.WriteLine($"{"Пацієнт",-22} {"Народження",12} {"Вік",5}");
Console.WriteLine(new string('-', 42));

foreach (var (name, birth) in patients)
{
    int age = today.Year - birth.Year;
    if (birth > today.AddYears(-age)) age--;
    Console.WriteLine($"{name,-22} {birth:dd.MM.yyyy,12} {age,5}");
}

Console.WriteLine("\n=== Розклад прийомів — комбінування DateOnly + TimeOnly ===");
var schedule = new[]
{
    (new DateOnly(2026, 6, 15), new TimeOnly(9,  0)),
    (new DateOnly(2026, 6, 15), new TimeOnly(10, 30)),
    (new DateOnly(2026, 6, 16), new TimeOnly(14, 0)),
};

TimeOnly workStart = new TimeOnly(8, 0);
TimeOnly workEnd   = new TimeOnly(17, 0);

Console.WriteLine($"{"Дата",-14}{"Час",-8}{"У робочий час"}");
Console.WriteLine(new string('-', 35));
foreach (var (d, t) in schedule)
{
    bool inWork = t.IsBetween(workStart, workEnd);
    DateTime appoint = d.ToDateTime(t);
    Console.WriteLine($"{d:dd.MM.yyyy,-14}{t:HH:mm,-8}{(inWork ? "Так" : "Ні")}");
}
```

## Парсинг і статичні методи — runnable приклад

```csharp run
using System;
using System.Globalization;

Console.WriteLine("=== DateOnly — Parse та статичні методи ===");
DateOnly d1 = DateOnly.Parse("11.06.2026");
Console.WriteLine($"Parse: {d1}");
Console.WriteLine($"DayNumber: {d1.DayNumber}");
Console.WriteLine($"FromDayNumber: {DateOnly.FromDayNumber(d1.DayNumber)}");

DateOnly d2 = DateOnly.ParseExact("2026-06-11", "yyyy-MM-dd", CultureInfo.InvariantCulture);
Console.WriteLine($"ParseExact ISO: {d2:dd.MM.yyyy}");

bool ok = DateOnly.TryParse("29.02.2026", out DateOnly d3); // 2026 не високосний
Console.WriteLine($"TryParse 29.02.2026: ok={ok}");

Console.WriteLine("\n=== TimeOnly — IsBetween і AddHours ===");
TimeOnly shift1Start = new TimeOnly(7, 0);
TimeOnly shift1End   = new TimeOnly(15, 0);
TimeOnly shift2Start = new TimeOnly(15, 0);
TimeOnly shift2End   = new TimeOnly(23, 0);

TimeOnly[] calls = { new TimeOnly(9, 0), new TimeOnly(14, 30), new TimeOnly(18, 0), new TimeOnly(6, 0) };
foreach (var call in calls)
{
    string shift = call.IsBetween(shift1Start, shift1End) ? "Зміна 1 (07-15)" :
                   call.IsBetween(shift2Start, shift2End) ? "Зміна 2 (15-23)" : "Поза змінами";
    Console.WriteLine($"  {call:HH:mm} -> {shift}");
}

Console.WriteLine("\n=== ToDateTime: об'єднання DateOnly + TimeOnly ===");
DateOnly date = new DateOnly(2026, 6, 20);
TimeOnly time = new TimeOnly(11, 15);
DateTime dt   = date.ToDateTime(time);
Console.WriteLine($"DateOnly: {date}  TimeOnly: {time}  -> DateTime: {dt:dd.MM.yyyy HH:mm}");
```
