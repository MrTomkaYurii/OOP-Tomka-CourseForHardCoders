---
chapter: 10
chapterTitle: "Розділ 10. Колекції"
section: 1
number: "10.1"
title: "Список List<T>"
source: "../_combined/62-spysok-list-t.md"
---

## 10.1. Список List<T>

Хоча у мові C# є масиви, які зберігають у собі набори однотипних об'єктів, але працювати з ними не завжди зручно. Наприклад, масив зберігає фіксовану кількість об'єктів, проте якщо ми заздалегідь не знаємо, скільки нам потрібно об'єктів. І в цьому випадку набагато зручніше використовувати колекції. Ще один плюс колекцій полягає в тому, що деякі з них реалізують стандартні структури даних, наприклад, стек, черга, словник, які можуть стати в нагоді для вирішення різних спеціальних завдань. Більшість класів колекцій міститься у просторі імен `System.Collections.Generic`.

Клас `List<T>` із простору імен `System.Collections.Generic` представляє найпростіший список однотипних об'єктів. Клас `List` типізується типом, об'єкти якого зберігаються у списку.

Ми можемо створити порожній список:

```csharp
List<string> people = new List<string>();
```

У разі об'єкт `List` типізується типом `string`. А це означає, що зберігати у цьому списку ми можемо лише рядки.

Можна відразу під час створення списку ініціалізувати його початковими значеннями. У цьому випадку елементи списку розміщуються після виклику конструктора у фігурних дужках

```csharp
List<string> people = new List<string>() { "Tom", "Bob", "Sam" };
```

У даному випадку до списку поміщаються три рядки

Також можна під час створення списку ініціалізувати його елементами з іншої колекції, наприклад іншого списку:

```csharp
var people = new List<string>() { "Tom", "Bob", "Sam" };
var employees = new List<string>(people);
```

Можна поєднати обидва способи:

```csharp
var people = new List<string>() { "Tom", "Bob", "Sam" };
var employees = new List<string>(people) { "Mike" };
```

У даному випадку в списку `employees` буде чотири елементи (`{ "Tom", "Bob", "Sam", "Mike" }`) - три додаються зі списку людей і один елемент задається при ініціалізації.

Так само можна працювати зі списками інших типів, наприклад:

```csharp
List<Person> people = new List<Person>()
{
    new Person("Tom"),
    new Person("Bob"),
    new Person("Sam")
};

class Person
{
    public string Name { get; }
    public Person(string name) => Name = name;
}
```

### Встановлення початкової ємності списку

Ще один конструктор класу `List` приймає як параметр початкову ємність списку:

```csharp
List<string> people = new List<string>(16);
```

Вказівка початкової ємності списку дозволяє у майбутньому збільшити продуктивність і зменшити витрати виділення пам'яті при додаванні елементів. Оскільки динамічне додавання до списку може призводити на низькому рівні додаткового виділення пам'яті, що знижує продуктивність. Якщо ж ми знаємо, що список не перевищуватиме певний розмір, то ми можемо передати цей розмір як ємність списку та уникнути додаткових виділень пам'яті.

Також початкову ємність можна встановити за допомогою властивості `Capacity`, яка є у класу `List`.

### Звернення до елементів списку

Як і масиви, списки підтримують індекси, за допомогою яких можна звернутися до певних елементів:

```csharp
var people = new List<string>() { "Tom", "Bob", "Sam" };

string firstPerson = people[0];
// отримуємо перший елемент
Console.WriteLine(firstPerson); // Tom

people[0] = "Mike";
// змінюємо перший елемент
Console.WriteLine(people[0]); // Mike
```

### Довжина списку

За допомогою властивості `Count` можна отримати довжину списку:

```csharp
var people = new List<string>() { "Tom", "Bob", "Sam" };
Console.WriteLine(people.Count); // 3
```

### Перебір списку

C# дозволяє здійснити перебір списку за допомогою стандартного циклу `foreach`

```csharp
var people = new List<string>() { "Tom", "Bob", "Sam" };

foreach (var person in people)
{
    Console.WriteLine(person);
}

// Вивід програми:
// Tom
// Bob
// Sam
```

Також можна використовувати інші типи циклів та в комбінації з індексами перебирати списки:

```csharp
var people = new List<string>() { "Tom", "Bob", "Sam" };

for (int i = 0; i < people.Count; i++)
{
    Console.WriteLine(people[i]);
}
```

### Методи списку

Серед його методів можна виділити такі:

- `void Add(T item)`: додавання нового елемента до списку
- `void AddRange(IEnumerable<T> collection)`: додавання до списку колекції або масиву
- `int BinarySearch(T item)`: бінарний пошук елемента у списку. Якщо елемент знайдено, метод повертає індекс цього елемента в колекції. При цьому список має бути відсортований.
- `void CopyTo(T[] array)`: копіює список у масив `array`
- `void CopyTo(int index, T[] array, int arrayIndex, int count)`: копіює зі списку з індексу `index` елементи, кількість яких дорівнює `count`, і вставляє їх в масив `array` починаючи з індексу `arrayIndex`
- `bool Contains(T item)`: повертає `true`, якщо елемент `item` є у списку
- `void Clear()`: видаляє всі елементи зі списку
- `bool Exists(Predicate<T> match)`: повертає `true`, якщо у списку є елемент, який відповідає делегату `match`
- `T? Find(Predicate<T> match)`: повертає перший елемент, який відповідає делегату `match`. Якщо елемент не знайдено, повертається `null`
- `T? FindLast(Predicate<T> match)`: повертає останній елемент, який відповідає делегату `match`. Якщо елемент не знайдено, повертається `null`
- `List<T> FindAll(Predicate<T> match)`: повертає список елементів, які відповідають делегату `match`
- `int IndexOf(T item)`: повертає індекс першого входження елемента у списку
- `int LastIndexOf(T item)`: повертає індекс останнього входження елемента у списку
- `List<T> GetRange(int index, int count)`: повертає список елементів, кількість яких дорівнює `count`, починаючи з індексу `index`.
- `void Insert(int index, T item)`: вставляє елемент `item` до списку за індексом `index`. Якщо такого індексу у списку немає, то генерується виняток
- `void InsertRange(int index, IEnumerable<T> collection)`: вставляє колекцію елементів `collection` у поточний список, починаючи з індексу `index`. Якщо такого індексу у списку немає, то генерується виняток
- `bool Remove(T item)`: видаляє елемент `item` зі списку і якщо видалення пройшло успішно, то повертає `true`. Якщо у списку кілька однакових елементів, видаляється лише перший з них
- `void RemoveAt(int index)`: видалення елемента за вказаним індексом `index`. Якщо такого індексу у списку немає, то генерується виняток
- `void RemoveRange(int index, int count)`: параметр `index` задає індекс, з якого треба видалити елементи, а параметр `count` задає кількість елементів, що видаляються.
- `int RemoveAll(Predicate<T> match)`: видаляє всі елементи, які відповідають делегату `match`. Повертає кількість видалених елементів
- `void Reverse()`: змінює порядок елементів
- `void Reverse(int index, int count)`: змінює порядок на зворотний для елементів, кількість яких дорівнює `count`, починаючи з індексу `index`
- `void Sort()`: сортування списку
- `Sort(IComparer<T>? comparer)`: сортування списку за допомогою об'єкта `comparer`, який передається як параметр

### Додавання до списку

```csharp
List<string> people = new List<string>() { "Tom" };

people.Add("Bob"); // додавання елемента
// people = { "Tom", "Bob" };

people.AddRange(new[] { "Sam", "Alice" });
// додаємо масив
// people = { "Tom", "Bob", "Sam", "Alice" };

// також можна було б додати інший список
// people.AddRange(new List<string>() { "Sam", "Alice" });

people.Insert(0, "Eugene");
// вставляємо на перше місце
// people = { "Eugene", "Tom", "Bob", "Sam", "Alice" };

people.InsertRange(1, new string[] { "Mike", "Kate" });
// вставляємо масив з індексу 1
// people = { "Eugene", "Mike", "Kate", "Tom", "Bob", "Sam", "Alice" };

// також можна було б додати інший список
// people.InsertRange(1, new List<string>() { "Mike", "Kate" });
```

### Видалення зі списку

```csharp
var people = new List<string>() { "Eugene", "Mike", "Kate", "Tom", "Bob", "Sam", "Tom", "Alice" };

people.RemoveAt(1);
// видаляємо другий елемент
// people = { "Eugene", "Kate", "Tom", "Bob", "Sam", "Tom", "Alice" };

people.Remove("Tom");
// видаляємо елемент "Tom"
// people = { "Eugene", "Kate", "Bob", "Sam", "Tom", "Alice" };

// видаляємо зі списку всі елементи, довжина рядка яких дорівнює 3
people.RemoveAll(person => person.Length == 3);
// people = { "Eugene", "Kate", "Alice" };

// видаляємо зі списку 2 елементи, починаючи з індексу 1
people.RemoveRange(1, 2);
// people = { "Eugene" };

// повністю очищаємо список
people.Clear();
// people = { };
```

### Пошук та перевірка елемента

```csharp
var people = new List<string>() { "Eugene", "Mike", "Kate", "Tom", "Bob", "Sam" };

var containsBob = people.Contains("Bob");
// true

var containsBill = people.Contains("Bill");
// false

// перевіряємо, чи є у списку рядки з довжиною 3 символи
var existsLength3 = people.Exists(p => p.Length == 3); // true

// перевіряємо, чи є у списку рядки з довжиною 7 символів
var existsLength7 = people.Exists(p => p.Length == 7); // false

// отримати перший елемент з довжиною в 3 символи
var firstWithLength3 = people.Find(p => p.Length == 3); // Tom

// отримати останній елемент з довжиною в 3 символи
var lastWithLength3 = people.FindLast(p => p.Length == 3); // Sam

// отримуємо всі елементи з довжиною 3 символи у вигляді списку
List<string> peopleWithLength3 = people.FindAll(p => p.Length == 3);
// peopleWithLength3 { "Tom", "Bob", "Sam" }
```

### Отримання діапазону та копіювання в масив

```csharp
List<string> people = new List<string>() { "Eugene", "Tom", "Mike", "Sam", "Bob" };

// отримуємо діапазон з другого по четвертий елемент
var range = people.GetRange(1, 3);
// range = { "Tom", "Mike", "Sam" };

// копіюємо в масив перші три елементи
string[] partOfPeople = new string[3];
people.CopyTo(0, partOfPeople, 0, 3);
// partOfPeople = { "Eugene", "Tom", "Mike" };
```

### Розташування елементів у зворотному порядку

```csharp
var people = new List<string>() { "Eugene", "Tom", "Mike", "Sam", "Bob" };

// перевертаємо весь список
people.Reverse();
// people = { "Bob", "Sam", "Mike", "Tom", "Eugene" };

var people2 = new List<string>() { "Eugene", "Tom", "Mike", "Sam", "Bob" };

// перевертаємо частину лише 3 елементи з індексу 1
people2.Reverse(1, 3);
// people2 = { "Eugene", "Sam", "Mike", "Tom", "Bob" };
```
