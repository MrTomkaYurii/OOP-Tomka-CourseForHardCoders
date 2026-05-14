---
chapter: 12
chapterTitle: "Розділ 12. Робота з датами та часом"
section: 3
number: "12.3"
title: "DateOnly та TimeOnly"
source: "../_combined/77-dateonly-ta-timeonly.md"
---

## 12.3. DateOnly та TimeOnly

Для спрощення роботи з датами та часом до .NET 6 було додано дві додаткові структури - `DateOnly` та `TimeOnly`.

### DateOnly

Структура `DateOnly` представляє дату. Для створення структури можна використовувати низку її конструкторів.

```csharp
DateOnly()
DateOnly(int year, int month, int day)
DateOnly(int year, int month, int day, System.Globalization.Calendar calendar)
```

При використанні конструктора без параметрів структура ініціалізується датою 01.01.0001:

```csharp
DateOnly someDate = new DateOnly();
Console.WriteLine(someDate); // 01.01.0001
```

Друга версія конструктора приймає рік, місяць та число, якими ініціалізується структура:

```csharp
DateOnly someDate = new DateOnly(2022, 1, 6); // 6 січня 2022 року
Console.WriteLine(someDate); // 06.01.2022
```

Третя версія конструктора на додаток до року, місяця та числа також приймає об'єкт календаря - об'єкт `System.Globalization.Calendar`, щодо якого буде розраховуватися дата. Клас `Calendar` є абстрактним, але .NET надає низку вбудованих типів календарів. Наприклад, розрахуємо дату щодо юліанського календаря:

```csharp
using System.Globalization;

DateOnly julianDate = new DateOnly(2022, 1, 6, new JulianCalendar());
Console.WriteLine(julianDate); // 19.01.2022
```

У даному випадку для .NET передана конструктору дата - 06.01.2022 розцінюється як дата юліанського календаря. При виведенні на консоль ми бачимо той самий день лише щодо григоріанського календаря.

### Властивості DateOnly

За допомогою властивостей структури можна отримати окремі складові дати:

- `Day`: повертає день дати
- `DayNumber`: повертає кількість минулих днів з 1 січня 0001 року щодо григоріанського календаря
- `DayOfWeek`: повертає день тижня
- `DayOfYear`: повертає день року
- `MaxValue`: повертає максимально можливу дату (статична властивість)
- `MinValue`: повертає ранню можливу дату (статична властивість)
- `Month`: повертає місяць
- `Year`: повертає рік

Застосування властивостей:

```csharp
DateOnly now = new DateOnly(2022, 1, 6);
Console.WriteLine(now.Day);       // 6
Console.WriteLine(now.DayNumber); // 738160
Console.WriteLine(now.DayOfWeek); // Thursday
Console.WriteLine(now.DayOfYear); // 6
Console.WriteLine(now.Month);     // 1
Console.WriteLine(now.Year);      // 2022
```

### Методи DateOnly

За допомогою методів `DateOnly` можна виконувати деякі операції з датами. Деякі з них:

- `AddDays(int days)`: додає до дати кілька днів
- `AddMonths(int months)`: додає до дати кілька місяців
- `AddYears(int years)`: додає до дати кілька років
- `ToDateTime(TimeOnly)`: повертає об'єкт `DateTime`, який як дати використовує поточний об'єкт `DateOnly`, а як час - значення параметра у вигляді `TimeOnly`
- `ToLongDateString()`: виводить поточний об'єкт `DateOnly` у вигляді докладної дати
- `ToShortDateString()`: виводить поточний об'єкт `DateOnly` у вигляді стислої дати

Також у класі є низка статичних методів. Деякі з них:

- `FromDateTime(DateTime dateTime)`: на основі значення `DateTime`, переданого через параметр, створює та повертає об'єкт `DateOnly`
- `FromDayNumber(int days)`: на основі кількості днів створює та повертає об'єкт `DateOnly`
- `Parse(string date)`: конвертує строкове подання дати в об'єкт `DateOnly`
- `ParseExact(string date, string format)`: конвертує строкове подання дати в об'єкт `DateOnly`, застосовуючи певний формат
- `TryParse(string date, out DateOnly result)`: конвертує строкове подання дати в об'єкт `DateOnly`. При успішному конвертуванні повертає `true`, а параметр типу `DateOnly` містить створену дату
- `TryParseExact(string date, string format, out DateOnly result)`: конвертує строкове подання дати в об'єкт `DateOnly`, використовуючи певний формат. При успішному конвертуванні повертає `true`, а параметр типу `DateOnly` містить створену дату

Приклад деяких операцій:

```csharp
DateOnly now = DateOnly.Parse("06.01.2022");
Console.WriteLine(now); // 06.01.2022

now = now.AddDays(1); // 07.01.2022
now = now.AddMonths(4); // 07.05.2022
now = now.AddYears(-1); // 07.05.2021

Console.WriteLine(now.ToShortDateString()); // 07.05.2021
Console.WriteLine(now.ToLongDateString()); // 7 травня 2021 р.
```

### TimeOnly

Структура `TimeOnly` представляє час у діапазоні від 00:00:00 до 23:59:59.9999999. Для створення структури можна використовувати низку її конструкторів.

```csharp
TimeOnly()
TimeOnly(long ticks)
TimeOnly(int hour, int minute)
TimeOnly(int hour, int minute, int second)
TimeOnly(int hour, int minute, int second, int millisecond)
```

При використанні конструктора без параметрів структура ініціалізується часом 0.00:

```csharp
TimeOnly time = new TimeOnly();
Console.WriteLine(time); // 0:00
```

Додатково за допомогою інших версій конструктора можна встановити кількість годин, хвилин, секунд та мілісекунд:

```csharp
TimeOnly time1 = new TimeOnly(4, 30);
Console.WriteLine(time1); // 4:30

TimeOnly time2 = new TimeOnly(14, 23, 30);
Console.WriteLine(time2); // 14:23
```

### Властивості TimeOnly

За допомогою властивостей структури можна отримати окремі складові часу:

- `Hour`: повертає кількість годин
- `Minute`: повертає кількість хвилин
- `Second`: повертає кількість секунд
- `Millisecond`: повертає кількість мілісекунд
- `Ticks`: повертає кількість тиків
- `MaxValue`: повертає максимально можливий час (статична властивість)
- `MinValue`: повертає мінімально можливий час (статична властивість)

Застосування властивостей:

```csharp
TimeOnly time = new TimeOnly(14, 23, 30);
Console.WriteLine(time.Hour); // 14
Console.WriteLine(time.Minute); // 23
Console.WriteLine(time.Second); // 30
```

### Методи TimeOnly

За допомогою методів `TimeOnly` можна виконувати деякі операції з часом. Деякі з них:

- `AddHours(double hours)`: додає до часу кілька годин
- `AddMinutes(double minutes)`: додає до часу кілька хвилин
- `Add(TimeSpan value)`: додає час з об'єкта `TimeSpan`
- `ToLongTimeString()`: виводить поточний об'єкт `TimeOnly` у вигляді докладного часу
- `ToShortTimeString()`: виводить поточний об'єкт `TimeOnly` у вигляді стисненого часу

Також у класі є низка статичних методів. Деякі з них:

- `FromDateTime(DateTime dateTime)`: на основі значення `DateTime`, переданого через параметр, створює та повертає об'єкт `TimeOnly`
- `FromTimeSpan(TimeSpan value)`: на основі об'єкта `TimeSpan` створює та повертає об'єкт `TimeOnly`
- `Parse(string time)`: конвертує строкове подання часу в об'єкт `TimeOnly`
- `ParseExact(string time, string format)`: конвертує строкове подання часу в об'єкт `TimeOnly`, застосовуючи певний формат
- `TryParse(string time, out TimeOnly result)`: конвертує строкове подання часу в об'єкт `TimeOnly`. При успішній конвертації повертає `true`, а параметр типу `TimeOnly` містить конвертований час
- `TryParseExact(string time, string format, out TimeOnly result)`: конвертує строкове подання часу в об'єкт `TimeOnly`, застосовуючи певний формат. При успішній конвертації повертає `true`, а параметр типу `TimeOnly` містить конвертований час

Приклад деяких операцій:

```csharp
TimeOnly time = TimeOnly.Parse("06:33:22");
Console.WriteLine(time); // 6:33

time = time.AddHours(1); // 7:33
time = time.AddMinutes(-23); // 7:10

Console.WriteLine(time.ToShortTimeString()); // 7:10
Console.WriteLine(time.ToLongTimeString());  // 7:10:22
```
