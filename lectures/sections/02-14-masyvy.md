---
chapter: 2
chapterTitle: "Розділ 2. Основи програмування на C#"
section: 14
number: "2.14"
title: "Масиви"
source: "../_migration/source-chunks/08-masyvy.md"
---

## 2.14. Масиви

До цього моменту кожне значення зберігалося в окремій змінній. Але якщо потрібно зберегти вік 50 пацієнтів або показники тиску за 30 вимірювань — оголошувати 50 або 30 окремих змінних украй незручно. Для зберігання наборів однотипних значень призначені **масиви**.

**Масив** — це послідовність фіксованого розміру, що зберігає елементи **одного типу** в суміжних комірках пам'яті. Після оголошення кількість елементів масиву не змінюється.

## Оголошення та ініціалізація масиву

Синтаксис оголошення відрізняється від звичайної змінної наявністю квадратних дужок після типу:

```text
тип[] назва = new тип[розмір];
```

```csharp run
using System;

// Масив з 5 цілих чисел (всі елементи = 0 за замовчуванням)
int[] bloodPressures = new int[5];

// Присвоїмо значення
bloodPressures[0] = 120;
bloodPressures[1] = 135;
bloodPressures[2] = 148;
bloodPressures[3] = 115;
bloodPressures[4] = 160;

Console.WriteLine($"Перший вимір: {bloodPressures[0].ToString()} мм рт.ст.");
Console.WriteLine($"П'ятий вимір: {bloodPressures[4].ToString()} мм рт.ст.");
```

Масив також можна ініціалізувати значеннями відразу при оголошенні. Усі варіанти еквівалентні:

```csharp run
using System;

int[] ages1 = new int[4] { 45, 32, 67, 28 };  // явний розмір і значення
int[] ages2 = new int[]  { 45, 32, 67, 28 };  // розмір виводиться автоматично
int[] ages3 = new[]      { 45, 32, 67, 28 };  // скорочений запис
int[] ages4 =            { 45, 32, 67, 28 };  // найкоротший варіант

Console.WriteLine($"Всі масиви мають довжину {ages1.Length.ToString()}");
Console.WriteLine($"Перший елемент: {ages1[0].ToString()}");
```

Аналогічно для рядків:

```csharp run
using System;

string[] patientNames = { "Іван Петренко", "Марія Сидоренко", "Олег Бойко" };

foreach (string name in patientNames)
    Console.WriteLine(name);
```

## Індекси та доступ до елементів

![Одновимірний масив: структура, індекси та Length](_assets/02-14/array-1d.png)

Кожен елемент масиву має **індекс** — ціле число, яке вказує його позицію. **Нумерація починається з нуля**: перший елемент має індекс `0`, другий — `1`, останній — `довжина - 1`.

```csharp run
using System;

int[] ages = { 45, 32, 67, 28, 55 };

Console.WriteLine($"Перший (індекс 0): {ages[0].ToString()}");
Console.WriteLine($"Третій (індекс 2): {ages[2].ToString()}");
Console.WriteLine($"Останній (індекс 4): {ages[4].ToString()}");
```

Елементи можна змінювати через індекс:

```csharp run
using System;

int[] temps = { 36, 37, 39, 38, 36 };
Console.WriteLine($"До корекції: {temps[2].ToString()}°C");

temps[2] = 38;  // виправили помилку введення
Console.WriteLine($"Після корекції: {temps[2].ToString()}°C");
```

Якщо вказати індекс за межами масиву, виникне виняток `IndexOutOfRangeException` під час виконання:

```csharp run
using System;

try
{
    int[] values = { 1, 2, 3 };
    Console.WriteLine(values[10].ToString()); // помилка!
}
catch (IndexOutOfRangeException ex)
{
    Console.WriteLine($"Помилка: {ex.Message}");
}
```

## Властивість Length

Кожен масив має властивість `Length`, що повертає загальну кількість його елементів. Її важливо використовувати у циклах замість «магічних чисел»:

```csharp run
using System;

int[] heartRates = { 72, 68, 75, 88, 65 };

Console.WriteLine($"Кількість вимірів: {heartRates.Length.ToString()}");

// Сума всіх значень
int sum = 0;
for (int i = 0; i < heartRates.Length; i++)
    sum += heartRates[i];

double avg = (double)sum / heartRates.Length;
Console.WriteLine($"Середній пульс: {avg.ToString("F1")} уд/хв");
```

## Оператор ^ (індекс від кінця)

Починаючи з C# 8.0, можна звертатися до елементів масиву **від кінця** за допомогою оператора `^`. `^1` — останній елемент, `^2` — передостанній тощо:

```csharp run
using System;

int[] readings = { 120, 135, 148, 160, 115 };

Console.WriteLine($"Останній вимір:         {readings[^1].ToString()}");
Console.WriteLine($"Передостанній вимір:    {readings[^2].ToString()}");
Console.WriteLine($"Те саме через Length:   {readings[readings.Length - 1].ToString()}");
```

`readings[^1]` — це лаконічний еквівалент `readings[readings.Length - 1]`.

## Перебір масиву

### foreach

Для послідовного перебору всіх елементів найбільш читабельним є `foreach`:

```csharp run
using System;

double[] temperatures = { 36.6, 37.2, 38.5, 37.0, 36.8 };

foreach (double temp in temperatures)
{
    string status = temp >= 38.0 ? "Гарячка!" : "Норма";
    Console.WriteLine($"{temp.ToString("F1")}°C — {status}");
}
```

### for

Якщо потрібен індекс або зміна елементів — використовуйте `for`:

```csharp run
using System;

int[] bps = { 120, 145, 155, 130, 160 };

Console.WriteLine("Нормалізація значень (до 140 мм рт.ст.):");
for (int i = 0; i < bps.Length; i++)
{
    if (bps[i] > 140)
        bps[i] = 140;
    Console.WriteLine($"  [{i.ToString()}] = {bps[i].ToString()}");
}
```

`foreach` **не дозволяє** змінювати елементи колекції через змінну циклу — лише читати. Тому для модифікації елементів завжди застосовуйте `for`.

## Багатовимірні масиви

Масиви можуть бути **багатовимірними**. Найчастіше використовуються двовимірні масиви — вони представляють таблиці (матриці).

![Двовимірний масив: структура, рядки та стовпці](_assets/02-14/array-2d.png)

Для оголошення двовимірного масиву в квадратних дужках вказується кома, що розділяє розміри:

```csharp run
using System;

// Розклад: 3 відділення × 4 зміни (кількість пацієнтів у зміні)
int[,] schedule = {
    { 8, 10, 12, 14 },
    { 9, 11, 13, 15 },
    { 8, 12, 14, 16 }
};

int rows    = schedule.GetUpperBound(0) + 1; // 3
int columns = schedule.GetUpperBound(1) + 1; // 4

Console.WriteLine($"Відділень: {rows.ToString()}, Змін: {columns.ToString()}");
Console.WriteLine($"Ранкова зміна, відділення 1: {schedule[0, 0].ToString()} пацієнтів");
Console.WriteLine($"Нічна зміна, відділення 3:   {schedule[2, 3].ToString()} пацієнтів");

// Перебір: зовнішній цикл — рядки, внутрішній — стовпці
for (int r = 0; r < rows; r++)
{
    for (int c = 0; c < columns; c++)
    {
        Console.Write($"{schedule[r, c].ToString(),4}");
    }
    Console.WriteLine();
}
```

`schedule.GetUpperBound(0) + 1` повертає кількість рядків, `GetUpperBound(1) + 1` — кількість стовпців. Загальна довжина двовимірного масиву через `Length` — це добуток усіх розмірностей (тут: 3 × 4 = 12).

Масиви можуть мати й більшу кількість вимірів (тривимірні тощо), але на практиці частіше застосовуються одно- та двовимірні.

## Зубчастий масив (масив масивів)

На відміну від прямокутного двовимірного масиву, **зубчастий масив** (jagged array) — це масив, що містить інші масиви, причому кожен підмасив може мати різну довжину. Оголошується через подвійні квадратні дужки `[][]`:

```csharp run
using System;

// Кількість пацієнтів по днях тижня (різна кількість прийомів)
int[][] dailyPatients = {
    new int[] { 12, 8, 10 },           // Понеділок: 3 прийоми
    new int[] { 15, 12, 9, 11 },       // Вівторок:  4 прийоми
    new int[] { 10, 7 },               // Середа:    2 прийоми
};

for (int day = 0; day < dailyPatients.Length; day++)
{
    string[] dayNames = { "Понеділок", "Вівторок", "Середа" };
    Console.Write($"{dayNames[day]}: ");

    foreach (int count in dailyPatients[day])
        Console.Write($"{count.ToString()} ");

    Console.WriteLine();
}
```

Зубчастий масив застосовується там, де підмасиви мають різні розміри. Якщо всі рядки однакової довжини — зручніше використовувати прямокутний `[,]`.

## Основні поняття масивів

| Поняття | Опис | Приклад |
|---------|------|---------|
| **Ранг** | Кількість вимірів | `int[,]` — ранг 2 |
| **Довжина виміру** | Розмір конкретного виміру | `new int[3, 4]` — 3 рядки, 4 стовпці |
| **Length** | Загальна кількість елементів | `3 × 4 = 12` |
| **Індекс** | Номер елемента (з нуля) | `arr[0]` — перший |
| **^-оператор** | Індекс від кінця | `arr[^1]` — останній |
