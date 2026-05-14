---
chapter: 13
chapterTitle: "Розділ 13. Додаткові класи та структури .NET"
section: 6
number: "13.6"
title: "Індекси та діапазони"
source: "../_combined/83-indeksy-ta-diapazony.md"
---

## 13.6. Індекси та діапазони

У C# 8.0 було додано нову функціональність - індекси і діапазони, які спрощують отримання з масивів підмасивів. Для цього в C# є два типи: `System.Range` і `System.Index`. Обидва типи є структурами. Тип `Range` представляє деякий діапазон значень деякою послідовністю, а тип `Index` - індекс в послідовності.

### Індекси

Індекс фактично представляє числове значення, і щодо індексу ми можемо вказати це значення:

```csharp
Index myIndex = 2;
```

У разі індекс представляє третій елемент послідовності (індексація починається з 0).

За допомогою спеціального оператора `^` можна задати індекс щодо кінця послідовності.

```csharp
Index myIndex = ^2;
```

Тепер індекс представляє другий елемент кінця послідовності, тобто передостанній елемент.

Використовуємо індекси для отримання елементів масиву:

```csharp
Index myIndex1 = 2; // третій елемент
Index myIndex2 = ^2; // передостанній елемент

string[] people = { "Tom", "Bob", "Sam", "Kate", "Alice" };
string selected1 = people[myIndex1]; // Sam
string selected2 = people[myIndex2]; // Kate
Console.WriteLine(selected1);
Console.WriteLine(selected2);
```

Фактично, індекси не потрібні для цього завдання, і ми можемо використовувати стандартні функції масиву:

```csharp
string[] people = { "Tom", "Bob", "Sam", "Kate", "Alice" };
string selected1 = people[2]; // Sam
string selected2 = people[people.Length - 2]; // Kate
Console.WriteLine(selected1);
Console.WriteLine(selected2);
```

Тобто в подібних ситуаціях плюсом індексів є велика зручність для читання. Так, `people[^2]` більш читальна, ніж `people[people.Length - 2]`.

### Діапазон

Діапазон є частиною послідовності, яка обмежена двома індексами. Початковий індекс включається до діапазону, а кінцевий індекс НЕ входить у діапазон. Для визначення діапазону застосовується оператор `..`:

```csharp
Range myRange1 = 1..4; // з 1-го індексу включно по 4-й індекс не включно
```

У даному випадку діапазон `myRange1` включає елементи з 1 індексу по 4-й індекс (не включаючи). При цьому елемент за 4 індексом не включається в діапазон. При цьому межі діапазону задаються не просто числами, а об'єктами `Index`. Тобто такі визначення діапазонів будуть рівноцінні:

```csharp
Index start = 1;
Index end = 4;
Range myRange1 = start..end;

Range myRange2 = 1..4;
```

Практичне застосування діапазонів - отримаємо з другого до четвертого елементи масиву:

```csharp
string[] people = { "Tom", "Bob", "Sam", "Kate", "Alice" };
string[] peopleRange = people[1..4]; // отримуємо 2, 3 та 4-й елементи з масиву
foreach (var person in peopleRange)
{
    Console.WriteLine(person);
}
```

Результатом операції `people[1..4]` є підмасив елементів з 1 по 3 індекси (включаючи). Консольний вивід:

```text
Bob
Sam
Kate
```

Ми можемо встановити для діапазону тільки кінцевий індекс. У цьому випадку початковим індексом за промовчанням буде 0.

```csharp
string[] people = { "Tom", "Bob", "Sam", "Kate", "Alice" };
string[] peopleRange = people[..4]; // Tom, Bob, Sam, Kate
```

Або, навпаки, задати лише початковий індекс, тоді кінцевим індексом буде останній індекс послідовності:

```csharp
string[] people = { "Tom", "Bob", "Sam", "Kate", "Alice" };
string[] peopleRange = people[1..]; // Bob, Sam, Kate, Alice
```

Використовуючи індекси щодо кінця послідовності, можна отримувати діапазон щодо кінця послідовності:

```csharp
string[] people = { "Tom", "Bob", "Sam", "Kate", "Alice" };
string[] peopleRange1 = people[^2..]; // два останні - Kate, Alice
string[] peopleRange2 = people[..^1]; // всі, крім останнього - Tom, Bob, Sam, Kate
string[] peopleRange3 = people[^3..^1]; // два елементи перед останнім - Sam, Kate
```

Крім масивів індекси та діапазони також застосовуються до об'єктів `Span` та `ReadOnlySpan`:

```csharp
string[] people = { "Tom", "Bob", "Sam", "Kate", "Alice" };
Span<string> peopleSpan = people;
Span<string> selectedPeopleSpan = peopleSpan[1..4];
foreach (var person in selectedPeopleSpan)
{
    Console.WriteLine(person);
}
```
