---
chapter: 8
chapterTitle: "Розділ 8. Додаткові можливості ООП у C#"
section: 9
number: "8.9"
title: "Кортежі"
source: "../_combined/54-kortezhi.md"
---

## 8.9. Кортежі

Класичне обмеження методу в C# — він може повертати лише одне значення. Щоб повернути два пов'язаних результати (наприклад, мінімум і максимум з масиву вимірювань), раніше доводилось або створювати спеціальний клас-обгортку, або використовувати `out`-параметри, або повертати масив. Усі ці підходи або зайво громіздкі, або не виразні. **Кортежі** (tuples), додані у C# 7.0, вирішують цю проблему елегантно: вони дозволяють групувати кілька значень в одну структуру без оголошення окремого класу.

## System.Tuple vs ValueTuple: важлива різниця

У .NET існують два різних механізми кортежів, які легко переплутати.

**System.Tuple<T1,T2,...>** з'явився ще у .NET 4.0. Це звичайний **клас** — тобто reference type. Об'єкт розміщується у heap, а доступ до елементів — лише через `Item1`, `Item2`... Властивості readonly, синтаксис громіздкий: `Tuple.Create("Іван", 45)`. Рівність — посилальна (як у всіх класів без перевизначення).

**System.ValueTuple<T1,T2,...>** з'явився у C# 7.0. Це **структура** — value type. Об'єкт розміщується на stack, що дає кращу продуктивність при частих виделеннях. Синтаксис короткий: `("Іван", 45)`. Поля мутабельні. Рівність — структурна (`==` порівнює значення). Саме цей варіант і має на увазі слово «кортеж» у сучасному C#.

![Кортежі в C#: System.Tuple (старий) vs ValueTuple (новий)](_assets/08-09/tuple-old-vs-new.png)

Надалі, говорячи про кортежі, ми маємо на увазі виключно `ValueTuple` — сучасний та рекомендований варіант.

## Синтаксис: оголошення та доступ

Кортеж визначається переліком значень у круглих дужках. Якщо не вказувати назви полів, доступ відбувається через `Item1`, `Item2` і так далі:

```csharp
var measurement = (36.6, 72);  // (double, int)
Console.WriteLine(measurement.Item1); // 36.6
Console.WriteLine(measurement.Item2); // 72
```

Рекомендований підхід — **іменовані поля**: вони роблять код значно зрозумілішим:

```csharp
var measurement = (Temperature: 36.6, Pulse: 72);
Console.WriteLine(measurement.Temperature); // 36.6
Console.WriteLine(measurement.Pulse);       // 72
```

Іменовані поля — це виключно **compile-time аліаси**. Компілятор перетворює `measurement.Temperature` у `measurement.Item1` під час компіляції. У скомпільованому IL-коді `Temperature` не існує — лише `Item1`. Це означає, що якщо ви передаєте кортеж у бібліотеку або зберігаєте у `object`, назви полів там будуть недоступні.

Тип кортежу можна вказати явно:

```csharp
(double Temperature, int Pulse) measurement = (36.6, 72);
```

Або визначити псевдонім типу через `using` (C# 12+):

```csharp
using Measurement = (double Temperature, int Pulse);
Measurement m = (37.2, 88);
```

## Декомпозиція кортежу

Кортеж можна **декомпозувати** — розкласти на окремі змінні. Це особливо зручно при отриманні результату методу:

```csharp
var (temperature, pulse) = GetVitals(patientId);
Console.WriteLine($"Температура: {temperature}, пульс: {pulse}");
```

Якщо деякі елементи кортежу непотрібні, їх можна пропустити за допомогою **discard** (`_`):

```csharp
var (temperature, _) = GetVitals(patientId); // пульс не потрібен
```

Discard — це не змінна, це явна вказівка компілятору, що значення нас не цікавить. Він не займає пам'яті і не створює змінної.

## Основний синтаксис у клінічному контексті

```csharp run
using System;

// Виконуваний код
// Явний кортеж
(string Name, int Age, double Temp) patient = ("Іван Петренко", 45, 38.2);
Console.WriteLine($"Пацієнт: {patient.Name}, вік: {patient.Age}, t°: {patient.Temp}");

// Декомпозиція
var (name, age, temp) = patient;
Console.WriteLine($"Після декомпозиції: {name}, {age} р., {temp}°C");

// Discard: нас цікавить лише ім'я
var (patientName, _, _) = patient;
Console.WriteLine($"Ім'я: {patientName}");

// Мутабельність — на відміну від анонімних типів
var visit = (Diagnosis: "Гіпертонія", Room: 7);
visit.Room = 12; // можна змінити
Console.WriteLine($"Діагноз: {visit.Diagnosis}, палата: {visit.Room}");

// Обмін значеннями через кортеж
string doctorA = "Олег Петренко";
string doctorB = "Марія Іванова";
(doctorA, doctorB) = (doctorB, doctorA);
Console.WriteLine($"Після ротації: {doctorA}, {doctorB}");
```

## Кортеж як результат методу

Найцінніше застосування кортежів — **повернення кількох значень з методу**. До C# 7 для цього використовували `out`-параметри або окремі класи. Тепер можна описати результат прямо в сигнатурі:

```csharp run
using System;

// Виконуваний код
double[] readings = { 36.6, 37.1, 38.5, 37.8, 36.9, 39.2, 37.4 };

var stats = AnalyzeReadings(readings);
Console.WriteLine($"Мін: {stats.Min:F1}°C");
Console.WriteLine($"Макс: {stats.Max:F1}°C");
Console.WriteLine($"Середнє: {stats.Average:F1}°C");
Console.WriteLine($"Кількість вимірювань з жаром: {stats.FeverCount}");

// Декомпозиція без збереження всього кортежу:
var (min, max, avg, _) = AnalyzeReadings(readings);
Console.WriteLine($"Діапазон: {min:F1}–{max:F1}°C");

// Метод повертає іменований кортеж
(double Min, double Max, double Average, int FeverCount)
    AnalyzeReadings(double[] values)
{
    double min = values[0], max = values[0], sum = 0;
    int feverCount = 0;
    foreach (var v in values)
    {
        if (v < min) min = v;
        if (v > max) max = v;
        sum += v;
        if (v > 37.5) feverCount++;
    }
    return (min, max, sum / values.Length, feverCount);
}
```

Іменований кортеж у сигнатурі методу виконує роль «легкого DTO»: він описує структуру результату прямо там, де метод визначений, без необхідності оголошувати окремий клас. Але на відміну від анонімного типу — може бути явно типізований і переданий між методами.

## Кортеж як параметр методу

Кортеж можна передати і як параметр:

```csharp run
using System;

// Виконуваний код
PrintVitals(("Іван Петренко", 38.2, 90));
PrintVitals(("Марія Коваль",  36.7, 72));

// Сортування масиву через tuple-swap
int[] pulseReadings = { 88, 62, 95, 71, 83, 55, 79 };
for (int i = 0; i < pulseReadings.Length - 1; i++)
    for (int j = i + 1; j < pulseReadings.Length; j++)
        if (pulseReadings[i] > pulseReadings[j])
            (pulseReadings[i], pulseReadings[j]) = (pulseReadings[j], pulseReadings[i]);

Console.WriteLine("Відсортований пульс:");
foreach (var p in pulseReadings)
    Console.WriteLine($"  {p} уд/хв");

// Метод із кортежем як параметром
void PrintVitals((string Name, double Temp, int Pulse) vitals)
{
    string status = vitals.Temp > 37.5 ? " [жар]" : "";
    Console.WriteLine($"{vitals.Name}: {vitals.Temp:F1}°C, {vitals.Pulse} уд/хв{status}");
}
```

## Рівність кортежів

`ValueTuple` підтримує структурну рівність через `==`: два кортежі рівні, якщо рівні всі їхні елементи в тому самому порядку. Назви полів при порівнянні не враховуються.

```csharp
var a = (Name: "Іван", Age: 45);
var b = (PatientName: "Іван", Years: 45); // інші назви — але однакові типи і значення
Console.WriteLine(a == b); // true — назви полів в IL відсутні
```

## Коли кортеж, а коли щось інше

| Потреба | Інструмент |
|---------|-----------|
| Повернути 2–4 пов'язаних значення з методу | **Кортеж** `(T1, T2, ...)` |
| Тимчасова проекція тільки в межах методу | Анонімний тип (8.8) |
| Тип потрібний в кількох місцях, має поведінку | `record` (8.10) або клас |
| Потрібне успадкування або складний конструктор | Клас |
| Просто обміняти два значення | Кортеж `(a, b) = (b, a)` |

Головна перевага кортежу перед анонімним типом — **можна вказати тип явно** і передати між методами. Головна перевага перед класом — не треба оголошувати тип, якщо структура використовується лише локально.
