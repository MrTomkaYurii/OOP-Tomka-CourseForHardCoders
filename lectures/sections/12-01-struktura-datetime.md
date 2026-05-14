---
chapter: 12
chapterTitle: "Розділ 12. Робота з датами та часом"
section: 1
number: "12.1"
title: "Структура DateTime"
source: "../_combined/75-struktura-datetime.md"
---

## 12.1. Структура DateTime

Для роботи з датами та часом у .NET призначена структура `DateTime`. Вона представляє дату та час від 00:00:00 1 січня 0001 до 23:59:59 31 грудня 9999 року.

Для створення нового об'єкта `DateTime` можна також використовувати конструктор. Порожній конструктор створює початкову дату:

```csharp
DateTime dateTime = new DateTime();
Console.WriteLine(dateTime); // 01.01.0001 0:00:00
```

Тобто ми отримаємо мінімально можливе значення, яке також можна одержати так:

```csharp
Console.WriteLine(DateTime.MinValue);
```

Щоб задати конкретну дату, потрібно використовувати один із конструкторів, які приймають параметри:

```csharp
DateTime date1 = new DateTime(2015, 7, 20); // рік - місяць - день
Console.WriteLine(date1); // 20.07.2015 0:00:00
```

Встановлення часу:

```csharp
DateTime date1 = new DateTime(2015, 7, 20, 18, 30, 25); // рік - місяць - день - година - хвилина - секунда
Console.WriteLine(date1); // 20.07.2015 18:30:25
```

Якщо необхідно отримати поточний час і дату, можна використовувати ряд властивостей `DateTime`:

```csharp
Console.WriteLine(DateTime.Now);
Console.WriteLine(DateTime.UtcNow);
Console.WriteLine(DateTime.Today);
```

Консольний вивід:

```text
20.07.2015 11:43:33
20.07.2015 8:43:33
20.07.2015 0:00:00
```

Властивість `DateTime.Now` бере поточну дату та час комп'ютера, `DateTime.UtcNow` - дата та час щодо часу за Грінвічем (GMT) та `DateTime.Today` - лише поточна дата.

Працюючи з датами треба враховувати, що за умовчанням подання дат застосовується григоріанський календар. Але що буде, якщо ми захочемо отримати день тижня для 5 жовтня 1582:

```csharp
DateTime someDate = new DateTime(1582, 10, 5);
Console.WriteLine(someDate.DayOfWeek);
```

Консоль висвітить значення `Tuesday`, тобто вівторок. Проте, як відомо з історії, вперше перехід з юліанського календаря на григоріанський відбувся у жовтні 1582 року. Тоді після дати 4 жовтня (четвер) (ще за юліанським календарем) відразу перейшли до 15 жовтня (п'ятниця) (вже за григоріанським календарем). Таким чином фактично викинули 10 днів. Тобто після 4 жовтня йшло 15 жовтня.

У більшості випадків цей факт навряд чи якось вплине на обчислення, проте при роботі з дуже давніми датами цей аспект слід враховувати.

### Операції з DateTime

Основні операції зі структурою `DateTime` пов'язані зі складанням чи відніманням дат. Наприклад, треба до деякої дати додати або, навпаки, забрати кілька днів.

Для додавання дат використовується низка методів:

- `Add(TimeSpan value)`: додає до дати значення `TimeSpan`
- `AddDays(double value)`: додає до поточної дати кілька днів
- `AddHours(double value)`: додає до поточної дати кілька годин
- `AddMinutes(double value)`: додає кілька хвилин до поточної дати
- `AddMonths(int value)`: додає до поточної дати кілька місяців
- `AddYears(int value)`: додає до поточної дати кілька років

Наприклад, додамо до деякої дати 3 години:

```csharp
DateTime date1 = new DateTime(2015, 7, 20, 18, 30, 25); // 20.07.2015 18:30:25
Console.WriteLine(date1.AddHours(3)); // 20.07.2015 21:30:25
```

Для віднімання дат використовується метод `Subtract(DateTime date)`:

```csharp
DateTime date1 = new DateTime(2015, 7, 20, 18, 30, 25); // 20.07.2015 18:30:25
DateTime date2 = new DateTime(2015, 7, 20, 15, 30, 25); // 20.07.2015 15:30:25
Console.WriteLine(date1.Subtract(date2)); // 03:00:00
```

Тут дати розрізняються на три години, тож результатом буде дата `"03:00:00"`.

Метод `Subtract` не має можливостей для окремого віднімання днів, годин і таке інше. Але це й не треба, тому що ми можемо передавати в метод `AddDays()` та інші методи додавання негативних значень:

```csharp
// віднімемо три години
DateTime date1 = new DateTime(2015, 7, 20, 18, 30, 25); // 20.07.2015 18:30:25
Console.WriteLine(date1.AddHours(-3)); // 20.07.2015 15:30:25
```

Крім операцій складання та віднімання ще є ряд методів форматування дат:

```csharp
DateTime date1 = new DateTime(2015, 7, 20, 18, 30, 25);
Console.WriteLine(date1.ToLocalTime()); // 20.07.2015 21:30:25
Console.WriteLine(date1.ToUniversalTime()); // 20.07.2015 15:30:25
Console.WriteLine(date1.ToLongDateString()); // 20 липня 2015 р.
Console.WriteLine(date1.ToShortDateString()); // 20.07.2015
Console.WriteLine(date1.ToLongTimeString()); // 18:30:25
Console.WriteLine(date1.ToShortTimeString()); // 18:30
```

Метод `ToLocalTime()` перетворює час UTC на локальний час, додаючи зсув щодо часу за Грінвічем. Метод `ToUniversalTime()`, навпаки, перетворює локальний час на час UTC, тобто віднімає зсув щодо часу за Грінвічем. Інші методи перетворять дату до певного формату.

### Форматування дат та часу

Для форматування виведення дат та часу застосовується ряд строкових форматів:

Виведемо поточну дату та час у всіх форматах:

```csharp
DateTime now = DateTime.Now;
Console.WriteLine($"D: {now.ToString("D")}");
Console.WriteLine($"d: {now.ToString("d")}");
Console.WriteLine($"F: {now.ToString("F")}");
Console.WriteLine($"f: {now:f}");
Console.WriteLine($"G: {now:G}");
Console.WriteLine($"g: {now:g}");
Console.WriteLine($"M: {now:M}");
Console.WriteLine($"O: {now:O}");
Console.WriteLine($"o: {now:o}");
Console.WriteLine($"R: {now:R}");
Console.WriteLine($"s: {now:s}");
Console.WriteLine($"T: {now:T}");
Console.WriteLine($"t: {now:t}");
Console.WriteLine($"U: {now:U}");
Console.WriteLine($"u: {now:u}");
Console.WriteLine($"Y: {now:Y}");
```

Консольний вивід:

```text
D: 6 січня 2022 р.
d: 06.01.2022
F: 6 січня 2022 р. 14:45:20
f: 6 січня 2022 р. 14:45
G: 06.01.2022 14:45:20
g: 06.01.2022 14:45
M: 6 січня
O: 2022-01-06T14:45:20.3942344+04:00
o: 2022-01-06T14:45:20.3942344+04:00
R: Thu, 06 Jan 2022 14:45:20 GMT
s: 2022-01-06T14:45:20
T: 14:45:20
t: 14:45
U: 6 січня 2022 р. 10:45:20
u: 2022-01-06 14:45:20Z
Y: січень 2022 р.
```
