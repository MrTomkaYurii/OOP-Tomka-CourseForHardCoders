---
chapter: 8
chapterTitle: "Розділ 8. Додаткові можливості ООП у C#"
section: 2
number: "8.2"
title: "Визначення інкременту та декременту"
source: "../_combined/47-vyznachennia-inkrementu-ta-dekrementu.md"
---

## 8.2. Визначення інкременту та декременту

Слід враховувати, що в коді оператора не повинні змінюватися об'єкти, які передаються в оператор через параметри. Наприклад, ми можемо визначити для класу Counter оператор інкременту:

```csharp
public static Counter operator ++(Counter counter1)
{
    counter1.Value += 10;
    return counter1;
}
```
Оскільки оператор унарний, він приймає лише один параметр – об'єкт того класу, в якому даний оператор визначено. Але це неправильне визначення інкременту, оскільки оператор не повинен змінювати значення своїх параметрів.

І коректніше визначення оператора інкременту виглядатиме так:

```csharp
public static Counter operator ++(Counter counter1)
{
    return new Counter { Value = counter1.Value + 10 };
}
```
Тобто повертається новий об'єкт, який містить у властивості Value інкрементоване значення. При цьому нам не треба визначати окремо оператори для префіксного та постфіксного інкременту (а також декременту), оскільки одна реалізація працюватиме в обох випадках.

```csharp
Counter counter1 = new Counter() { Value = 10 };
Counter counter2 = counter1++;
Console.WriteLine(counter1.Value); // 20
Console.WriteLine(counter2.Value); // 10
Counter counter3 = ++counter1;
Console.WriteLine(counter1.Value); // 30
Console.WriteLine(counter3.Value); // 30
```
При операції постфіксного інкременту (counter1++) компілятор спочатку створює тимчасову змінну, у яку зберігає поточний об'єкт. Потім поточний об'єкт замінює значення, отримане з функції оператора. Як результат операції повертається значення тимчасової змінної. При префіксному інкременті (++counter1) компілятор повертає нове значення, отримане з функції оператора.

### Визначення операцій true та false

Окремо варто відзначити визначення операторів true та false. Ці оператори визначаються, коли ми хочемо використовувати об'єкт типу як умову. Наприклад, визначимо дані оператори у класі Counter:

```csharp
class Counter
{
    public int Value { get; set; }
    public static bool operator true(Counter counter1)
    {
        return counter1.Value != 0;
    }
    public static bool operator false(Counter counter1)
    {
        return counter1.Value == 0;
    }
}
```
Наприклад:

```csharp
Counter counter = new Counter() { Value = 0 };
if (counter)
    Console.WriteLine(true);
else
    Console.WriteLine(false);
```
Також варто зазначити, що якщо ми хочемо використовувати операцію заперечення, типу if (!counter), то нам також необхідно визначити для типу операцію !:

```csharp
Counter counter = new Counter() { Value = 2 };
if (!counter)
    Console.WriteLine(true);
else
    Console.WriteLine(false);
class Counter
{
    public int Value { get; set; }
    public static bool operator !(Counter counter1)
    {
        return counter1.Value == 0;
    }
    public static bool operator true(Counter counter1)
    {
        return counter1.Value != 0;
    }
    public static bool operator false(Counter counter1)
    {
        return counter1.Value == 0;
    }
}
```
Операція заперечення фактично синонімічна операції false, тому містить аналогічну умову.
