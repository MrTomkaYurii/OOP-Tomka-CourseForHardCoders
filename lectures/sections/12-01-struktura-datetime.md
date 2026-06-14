---
chapter: 12
chapterTitle: "Розділ 12. Робота з датами та часом"
section: 1
number: "12.1"
title: "Структура DateTime"
source: "../_combined/75-struktura-datetime.md"
---

## 12.1. Структура DateTime

Дата і час — невід'ємна частина медичних інформаційних систем. Час прийому пацієнта, дата виписки, вік пацієнта в роках, тривалість госпіталізації, терміни зберігання аналізів — усе це вимагає роботи з датами. Центральний тип у .NET для цього завдання — структура `DateTime` з простору імен `System`.

`DateTime` — це **структура** (struct), тобто **значущий тип** (value type). На відміну від класів, екземпляр `DateTime` зберігається безпосередньо на стеку або всередині об'єкта і копіюється при присвоєнні — так само як `int` або `double`. Порівняння двох `DateTime` через `==` порівнює їхні **значення**, а не посилання.

![Структура DateTime — внутрішня будова та ключові властивості](_assets/12-01/datetime-structure.png)

## Внутрішнє представлення: тіки

Внутрішньо `DateTime` зберігає єдине 64-бітне ціле число — кількість **тіків** (ticks). Один тік дорівнює 100 наносекундам. Відлік іде від полудня 1 січня 0001 року (00:00:00.0000000) за григоріанським календарем. Доступ до тіків — через властивість `Ticks`:

```csharp
DateTime admission = new DateTime(2026, 6, 11, 9, 30, 0);
Console.WriteLine(admission.Ticks); // 638 814 126 000 000 000
```

Знання про тіки важливе для двох причин: по-перше, всі операції порівняння і арифметика дат зводяться до порівняння та арифметики цих цілих чисел, що є дуже швидким; по-друге, `TimeSpan` (розд. 12.4) також зберігає тіки — тому два типи легко взаємодіють.

## DateTimeKind: прив'язка до часового поясу

Кожен об'єкт `DateTime` має властивість `Kind` типу `DateTimeKind` — вона визначає, до якого часового поясу прив'язане значення:

| Kind | Значення | Коли використовується |
|------|---------|----------------------|
| `Unspecified` | Невідомо (за замовчуванням) | Локальні розрахунки без прив'язки до поясу |
| `Local` | Локальний час ОС | Відображення в UI поточного сервера/комп'ютера |
| `Utc` | Час UTC (Coordinated Universal Time) | Зберігання у БД, API, аудит-журнали |

```csharp
DateTime local = DateTime.Now;        // Kind = Local
DateTime utc   = DateTime.UtcNow;     // Kind = Utc
DateTime unsp  = new DateTime(2026, 6, 11); // Kind = Unspecified
```

**Чому це критично в медичних системах:** якщо лікарня або телемедичний сервіс працює в кількох часових поясах, зберігання `DateTime.Now` (Local) у базі даних призводить до помилок при агрегації даних. Правило: **завжди зберігати у БД UTC** (`DateTime.UtcNow`), а конвертацію у локальний час виконувати на рівні UI.

## UTC vs Local: практична пастка та конвертація

Порушення правила «зберігати UTC, відображати локальний час» призводить до важко діагностованих помилок:

```csharp run
using System;

// === ПРОБЛЕМА: зберігаємо Local, порівнюємо неправильно ===
Console.WriteLine("=== Антипатерн: змішування Local і Utc ===");

DateTime localAdmission = DateTime.Now;          // Kind = Local
DateTime utcAuditLog    = DateTime.UtcNow;       // Kind = Utc

// Ці два значення в один момент відрізняються на offset часового поясу!
Console.WriteLine($"Local: {localAdmission:HH:mm:ss}  Kind={localAdmission.Kind}");
Console.WriteLine($"Utc:   {utcAuditLog:HH:mm:ss}  Kind={utcAuditLog.Kind}");

// Порівняння Local з Utc дає НЕПРАВИЛЬНИЙ результат:
bool wrongComparison = localAdmission > utcAuditLog; // на UTC+2/UTC+3 буде true!
Console.WriteLine($"\nlocalAdmission > utcAuditLog = {wrongComparison}  ← НЕПРАВИЛЬНО");
Console.WriteLine("(DateTime порівнює тіки без урахування Kind)");

// === ПРАВИЛЬНО: завжди одна «мова» — UTC ===
Console.WriteLine("\n=== Правильно: конвертація та порівняння в UTC ===");

DateTime utcAdmission = DateTime.UtcNow;  // зберігаємо в БД UTC
DateTime utcEvent     = DateTime.UtcNow.AddMinutes(5);

bool correctComparison = utcAdmission < utcEvent; // true — правильно
Console.WriteLine($"utcAdmission < utcEvent = {correctComparison}  ← ПРАВИЛЬНО");

// Конвертація UTC -> Local для відображення в UI
DateTime displayTime = utcAdmission.ToLocalTime();
Console.WriteLine($"\nДля відображення в UI: {displayTime:dd.MM.yyyy HH:mm:ss} (local)");
Console.WriteLine($"Зберігаємо в БД:       {utcAdmission:dd.MM.yyyy HH:mm:ss} (utc)");
```

Методи конвертації:

| Метод | Що робить |
|-------|-----------|
| `.ToUniversalTime()` | Local → UTC (або Unspecified → UTC припускаючи Local) |
| `.ToLocalTime()` | UTC → Local |
| `DateTime.SpecifyKind(dt, kind)` | Перепозначити Kind без зміни значення |

```csharp run
using System;

// SpecifyKind: якщо з БД прийшов DateTime без Kind (Unspecified),
// але ми знаємо, що це UTC:
DateTime fromDb = new DateTime(2026, 6, 11, 7, 30, 0); // Kind = Unspecified
Console.WriteLine($"З БД (Unspecified): {fromDb.Kind}");

DateTime asUtc = DateTime.SpecifyKind(fromDb, DateTimeKind.Utc);
Console.WriteLine($"Після SpecifyKind:  {asUtc.Kind}");

DateTime localForDisplay = asUtc.ToLocalTime();
Console.WriteLine($"Для UI (Local):     {localForDisplay:HH:mm} ({localForDisplay.Kind})");
```

Правило для медичних систем: **все, що стосується аудиту, журналів, зберігання у БД, API** — тільки UTC. **Відображення у UI або при звітуванні** — конвертувати у Local прямо перед виводом.

## Конструктори DateTime

```csharp
// Мінімальна дата (01.01.0001 00:00:00)
DateTime zero = new DateTime();
Console.WriteLine(DateTime.MinValue); // 01.01.0001 0:00:00

// Рік, місяць, день
DateTime birthDate = new DateTime(1958, 4, 15); // 15 квітня 1958 р.

// Рік, місяць, день, година, хвилина, секунда
DateTime admission = new DateTime(2026, 6, 11, 9, 30, 0); // 09:30:00

// Повна точність: + мілісекунди
DateTime precise  = new DateTime(2026, 6, 11, 9, 30, 0, 123); // 09:30:00.123

// З явним Kind
DateTime utc = new DateTime(2026, 6, 11, 7, 30, 0, DateTimeKind.Utc);
```

## Статичні властивості

| Властивість | Що повертає |
|-------------|-----------|
| `DateTime.Now` | Поточна дата і час (Kind=Local) |
| `DateTime.UtcNow` | Поточна дата і час (Kind=Utc) |
| `DateTime.Today` | Поточна дата, час = 00:00:00 |
| `DateTime.MinValue` | 01.01.0001 00:00:00 |
| `DateTime.MaxValue` | 31.12.9999 23:59:59 |

```csharp
Console.WriteLine(DateTime.Now);    // 11.06.2026 11:43:33
Console.WriteLine(DateTime.UtcNow); // 11.06.2026  8:43:33 (UTC+3 → -3 год)
Console.WriteLine(DateTime.Today);  // 11.06.2026  0:00:00
```

## Властивості екземпляра

Об'єкт `DateTime` надає доступ до кожного компоненту окремо:

| Властивість | Тип | Опис |
|-------------|-----|------|
| `Year` / `Month` / `Day` | int | Рік, місяць (1-12), день (1-31) |
| `Hour` / `Minute` / `Second` | int | Година (0-23), хвилина (0-59), секунда (0-59) |
| `Millisecond` | int | Мілісекунди (0-999) |
| `DayOfWeek` | DayOfWeek | День тижня (`DayOfWeek.Monday` тощо) |
| `DayOfYear` | int | Порядковий номер дня у році (1-366) |
| `TimeOfDay` | TimeSpan | Час доби від початку дня |
| `Date` | DateTime | Лише дата, час = 00:00:00 |
| `Kind` | DateTimeKind | Тип часової прив'язки |
| `Ticks` | long | Кількість тіків |

```csharp
DateTime dt = new DateTime(2026, 6, 11, 14, 30, 25);

Console.WriteLine(dt.Year);        // 2026
Console.WriteLine(dt.DayOfWeek);   // Thursday
Console.WriteLine(dt.DayOfYear);   // 162
Console.WriteLine(dt.TimeOfDay);   // 14:30:25
Console.WriteLine(dt.Date);        // 11.06.2026 0:00:00
```

## Арифметика дат: методи Add*

Усі методи `Add*` повертають **новий** об'єкт `DateTime` — не змінюють оригінал (структура є незмінним значенням у цьому сенсі):

| Метод | Опис |
|-------|------|
| `AddYears(n)` | Додати/відняти роки |
| `AddMonths(n)` | Додати/відняти місяці |
| `AddDays(n)` | Додати/відняти дні |
| `AddHours(n)` | Додати/відняти години |
| `AddMinutes(n)` | Додати/відняти хвилини |
| `AddSeconds(n)` | Додати/відняти секунди |
| `Add(TimeSpan)` | Додати довільний інтервал |

Для віднімання передають **від'ємне число**:

```csharp
DateTime admission = new DateTime(2026, 6, 11, 9, 30, 0);

DateTime discharge = admission.AddDays(7);        // виписка через 7 днів
DateTime nextVisit = discharge.AddMonths(1);       // повторний огляд за місяць
DateTime before    = admission.AddHours(-2);       // 2 години до прийому

Console.WriteLine(discharge);  // 18.06.2026 9:30:00
Console.WriteLine(nextVisit);  // 18.07.2026 9:30:00
```

## Різниця між датами: Subtract і оператор –

Метод `Subtract(DateTime)` і оператор `–` між двома датами повертають **`TimeSpan`** — об'єкт, що представляє тривалість інтервалу (розд. 12.4):

```csharp
DateTime admission  = new DateTime(2026, 6, 1, 10, 0, 0);
DateTime discharge  = new DateTime(2026, 6, 8, 14, 30, 0);

TimeSpan stay = discharge - admission;          // або discharge.Subtract(admission)
Console.WriteLine(stay.Days);                   // 7
Console.WriteLine(stay.TotalHours);             // 172.5
```

## Порівняння дат

Оператори `>`, `<`, `>=`, `<=`, `==`, `!=` для `DateTime` порівнюють значення хронологічно:

```csharp
DateTime d1 = new DateTime(2026, 6, 1);
DateTime d2 = new DateTime(2026, 7, 1);

bool earlier = d1 < d2;  // true — червень раніше за липень
bool equal   = d1 == d1; // true

int cmp = DateTime.Compare(d1, d2); // -1 (d1 < d2), 0 (рівні), +1 (d1 > d2)
```

Для перевірки чи дата потрапляє у діапазон достатньо двох умов:

```csharp
DateTime start = new DateTime(2026, 6, 1);
DateTime end   = new DateTime(2026, 6, 30);
DateTime today = DateTime.Today;

bool inRange = today >= start && today <= end;
```

## Корисні статичні методи

```csharp
// Перевірка високосного року
bool leap = DateTime.IsLeapYear(2024); // true

// Кількість днів у місяці
int days = DateTime.DaysInMonth(2024, 2); // 29 (2024 — високосний)
```

## Дата народження та вік пацієнта — runnable приклад

Розрахунок віку пацієнта та основні операції з датами прийому:

```csharp run
using System;

DateTime birthDate = new DateTime(1958, 4, 15);
DateTime admission = new DateTime(2026, 6, 11, 9, 30, 0);
DateTime discharge = admission.AddDays(7);

Console.WriteLine("=== Картка пацієнта ===");
Console.WriteLine($"Дата народження: {birthDate:dd.MM.yyyy}");
Console.WriteLine($"День народження: {birthDate.DayOfWeek}");

int age = admission.Year - birthDate.Year;
if (birthDate.Date > admission.AddYears(-age).Date) age--;
Console.WriteLine($"Вік при вступі: {age} р.");

Console.WriteLine($"\n=== Госпіталізація ===");
Console.WriteLine($"Прийом:  {admission:dd.MM.yyyy HH:mm}");
Console.WriteLine($"Виписка: {discharge:dd.MM.yyyy HH:mm}");

TimeSpan stay = discharge - admission;
Console.WriteLine($"Тривалість: {stay.Days} днів");

DateTime nextVisit = discharge.AddMonths(1);
Console.WriteLine($"Повторний огляд: {nextVisit:dd.MM.yyyy}");

Console.WriteLine($"\n=== Властивості DateTime ===");
Console.WriteLine($"DayOfYear: {admission.DayOfYear}");
Console.WriteLine($"Kind:      {DateTime.UtcNow.Kind}");
Console.WriteLine($"IsLeapYear(2026): {DateTime.IsLeapYear(2026)}");
Console.WriteLine($"DaysInMonth(2026,2): {DateTime.DaysInMonth(2026, 2)}");
```

## Розклад прийомів у відділенні — runnable приклад

Робота з датами та часом в контексті розкладу пацієнтів:

```csharp run
using System;

Console.WriteLine("=== Розклад прийомів кардіологічного відділення ===");
Console.WriteLine($"{"Пацієнт",-22} {"Прийом",16} {"Виписка",16} {"Днів",6}");
Console.WriteLine(new string('-', 65));

var records = new[]
{
    ("Петренко Іван",     new DateTime(2026,6,1,  9,  0, 0), new DateTime(2026,6, 8, 14, 0, 0)),
    ("Коваль Марія",      new DateTime(2026,6,3,  11, 30, 0), new DateTime(2026,6,10, 10, 0, 0)),
    ("Сидоренко Олег",    new DateTime(2026,6,10, 8,  0, 0), new DateTime(2026,6,15, 16, 0, 0)),
};

TimeSpan totalStay = TimeSpan.Zero;
foreach (var (name, adm, dis) in records)
{
    TimeSpan stay = dis - adm;
    totalStay += stay;
    Console.WriteLine($"{name,-22} {adm:dd.MM.yy HH:mm,16} {dis:dd.MM.yy HH:mm,16} {stay.Days,6}");
}

Console.WriteLine(new string('-', 65));
Console.WriteLine($"{"Середня тривалість:",-22} {totalStay.TotalDays / records.Length,39:F1} днів");

Console.WriteLine($"\n=== Порівняння дат ===");
DateTime today  = new DateTime(2026, 6, 11);
DateTime future = today.AddDays(30);
Console.WriteLine($"Сьогодні: {today:dd.MM.yyyy}");
Console.WriteLine($"За 30 днів: {future:dd.MM.yyyy}  Day={future.DayOfWeek}");
Console.WriteLine($"Compare(today, future) = {DateTime.Compare(today, future)}");
```
