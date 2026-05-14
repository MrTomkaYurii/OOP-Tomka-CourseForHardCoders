---
chapter: 8
chapterTitle: "Розділ 8. Додаткові можливості ООП у C#"
section: 9
number: "8.9"
title: "Кортежі"
source: "../_combined/54-kortezhi.md"
---

## 8.9. Кортежі

Кортежі надають зручний спосіб роботи з набором значень, який було додано у версії C# 7.0.

Кортеж представляє набір значень, укладених у круглі дужки:

```csharp
var tuple = (5, 10);
```

У даному випадку визначено кортеж tuple, який має два значення: 5 та 10. Надалі ми можемо звертатися до кожного з цих значень через поля з назвами:

```text
Item[порядковий_номер_поля_в_кортежі]
```

Наприклад:

```csharp
var tuple = (5, 10);
Console.WriteLine(tuple.Item1); // 5
Console.WriteLine(tuple.Item2); // 10
tuple.Item1 += 26;
Console.WriteLine(tuple.Item1); // 31
```

У разі тип визначається неявно. Але ми також можемо явно вказати для змінної кортежу тип:

```csharp
(int, int) tuple = (5, 10);
```

Оскільки кортеж містить два числа, то у визначенні типу нам треба зазначити два числових типи. Або інший приклад визначення кортежу:

```csharp
(string, int, double) person = ("Tom", 25, 81.23);
```

Перший елемент кортежу у разі представляє рядок, другий елемент - тип int, а третій - тип double.

Ми також можемо дати назви полям кортежу:

```csharp
var tuple = (count: 5, sum: 10);
Console.WriteLine(tuple.count); // 5
Console.WriteLine(tuple.sum); // 10
```

Тепер, щоб звернутися до полів кортежу використовуються їхні імена, а не назви Item1 та Item2.

Ми навіть можемо виконати декомпозицію кортежу на окремі змінні:

```csharp
var (name, age) = ("Tom", 23);
Console.WriteLine(name);    // Tom
Console.WriteLine(age);     // 23
```

Одне із завдань, яке кортеж дозволяє елегантно вирішити, - це обмін значеннями:

```csharp
string main = "Java";
string second = "C#";
(main, second) = (second, main);
Console.WriteLine(main);    // C#
Console.WriteLine(second);  // Java
```

Що можна використовувати, наприклад, при найпростішому сортуванні масиву:

```csharp
int[] nums = { 54, 7, -41, 2, 4, 2, 89, 33, -5, 12 };

// сортування
for (int i = 0; i < nums.Length - 1; i++)
{
    for (int j = i + 1; j < nums.Length; j++)
    {
        if (nums[i] > nums[j])
            (nums[i], nums[j]) = (nums[j], nums[i]);
    }
}

// Вивід
Console.WriteLine("Виведення відсортованого масиву");
for (int i = 0; i < nums.Length; i++)
{
    Console.WriteLine(nums[i]);
}
```

### Кортеж як результат методу

Кортежі можуть виступати як результат функції. Наприклад, однією з найпоширеніших ситуацій є повернення з функції двох і більше значень, тоді як функція може повертати лише одне значення. І кортежі представляють оптимальний спосіб вирішення цього завдання:

```csharp
var tuple = GetValues();
Console.WriteLine(tuple.Item1); // 1
Console.WriteLine(tuple.Item2); // 3

(int, int) GetValues()
{
    var result = (1, 3);
    return result;
}
```

Тут визначено метод GetValues(), який повертає кортеж. Кортеж визначається як набір значень, поміщених у круглі дужки. І в даному випадку ми повертаємо кортеж із двох елементів типу int, тобто два числа.

Інший приклад:

```csharp
var tuple = GetValuesData(new int[] { 1, 2, 3, 4, 5, 6, 7 });
Console.WriteLine(tuple.count);
Console.WriteLine(tuple.sum);

(int sum, int count) GetValuesData(int[] numbers)
{
    var result = (sum: 0, count: numbers.Length);
    foreach (var n in numbers)
    {
        result.sum += n;
    }
    return result;
}
```

### Кортеж як параметр методу

І також кортеж може передаватися як параметр методу:

```csharp
PrintPerson(("Tom", 37));   // Tom - 37
PrintPerson(("Bob", 41));   // Bob - 41

void PrintPerson((string name, int age) person)
{
    Console.WriteLine($"{person.name} - {person.age}");
}
```

Тут методу PrintPerson передається кортеж із двох елементів, перший з яких надає рядок, а другий - значення типу int.
