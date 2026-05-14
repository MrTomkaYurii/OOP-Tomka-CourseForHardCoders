
## 13.4. Клас Array та масиви

Всі масиви C# побудовані на основі класу `Array` з простору імен `System`. Цей клас визначає ряд властивостей та методів, які ми можемо використовувати під час роботи з масивами. Основні властивості та методи:

- Властивість `Length` повертає довжину масиву
- Властивість `Rank` повертає розмірність масиву
- `int BinarySearch(Array array, object? value)` виконує бінарний пошук у відсортованому масиві та повертає індекс знайденого елемента
- `void Clear(Array array)` очищає масив, встановлюючи для всіх його елементів значення за замовчуванням
- `void Copy(Array sourceArray, int sourceIndex, Array destinationArray, int destinationIndex, int length)` копіює з масиву `sourceArray`, починаючи з індексу `sourceIndex`, `length` елементів в масив `destinationArray`, починаючи з індексу `destinationIndex`
- `bool Exists<T>(T[] array, Predicate<T> match)` перевіряє, чи містить масив `array` елементи, які задовольняють умові делегата `match`
- `void Fill<T>(T[] array, T value)` заповнює масив `array` значенням `value`
- `T? Find<T>(T[] array, Predicate<T> match)` знаходить перший елемент, який задовольняє певну умову з делегата `match`. Якщо елемент не знайдено, то повертається `null`
- `T? FindLast<T>(T[] array, Predicate<T> match)` знаходить останній елемент, який задовольняє певну умову з делегата `match`. Якщо елемент не знайдено, то повертається `null`
- `int FindIndex<T>(T[] array, Predicate<T> match)` повертає індекс першого входження елемента, який задовольняє певну умову делегата `match`
- `int FindLastIndex<T>(T[] array, Predicate<T> match)` повертає індекс останнього входження елемента, який задовольняє певну умову
- `T[] FindAll<T>(T[] array, Predicate<T> match)` повертає всі елементи у вигляді масиву, які задовольняють певній умові з делегата `match`
- `int IndexOf(Array array, object? value)` повертає індекс першого входження елемента в масив
- `int LastIndexOf(Array array, object? value)` повертає індекс останнього входження елемента в масив
- `void Resize<T>(ref T[]? array, int newSize)` змінює розмір одновимірного масиву
- `void Reverse(Array array)` розміщує елементи масиву у зворотному порядку
- `void Sort(Array array)` сортує елементи одновимірного масиву

Розберемо найвикористаніші методи.

### Пошук індексу елемента

```csharp
var people = new string[] { "Tom", "Sam", "Bob", "Kate", "Tom", "Alice" };

// Знаходимо індекс елемента "Bob"
int bobIndex = Array.BinarySearch(people, "Bob");
// Знаходимо індекс першого елемента "Tom"
int tomFirstIndex = Array.IndexOf(people, "Tom");
// Знаходимо індекс останнього елемента "Tom"
int tomLastIndex = Array.LastIndexOf(people, "Tom");
// Знаходимо індекс першого елемента, у якого довжина рядка більше 3
int lengthFirstIndex = Array.FindIndex(people, person => person.Length > 3);
// Знаходимо індекс останнього елемента, у якого довжина рядка більше 3
int lengthLastIndex = Array.FindLastIndex(people, person => person.Length > 3);

Console.WriteLine($"bobIndex: {bobIndex}"); // 2
Console.WriteLine($"tomFirstIndex: {tomFirstIndex}"); // 0
Console.WriteLine($"tomLastIndex: {tomLastIndex}"); // 4
Console.WriteLine($"lengthFirstIndex: {lengthFirstIndex}"); // 3
Console.WriteLine($"lengthLastIndex: {lengthLastIndex}"); // 5
```

Якщо елемент не знайдено у масиві, то методи повертають -1.

### Пошук елемента за умовою

```csharp
var people = new string[] { "Tom", "Sam", "Bob", "Kate", "Tom", "Alice" };

// Знаходимо перший та останній елементи,
// де довжина рядка більше 3 символів.
string? first = Array.Find(people, person => person.Length > 3);
Console.WriteLine(first); // Kate
string? last = Array.FindLast(people, person => person.Length > 3);
Console.WriteLine(last); // Alice

// Знаходимо елементи, у яких довжина рядка дорівнює 3.
string[] group = Array.FindAll(people, person => person.Length == 3);
foreach (var person in group)
    Console.WriteLine(person);
// Tom Sam Bob Tom
```

### Зміна порядку елементів масиву

Наприклад, змінимо порядок елементів:

```csharp
var people = new string[] { "Tom", "Sam", "Bob", "Kate", "Tom", "Alice" };

Array.Reverse(people);

foreach (var person in people)
    Console.Write($"{person} ");
// "Alice", "Tom", "Kate", "Bob", "Sam", "Tom"
```

Також можна змінити порядок лише частини елементів:

```csharp
var people = new string[] { "Tom", "Sam", "Bob", "Kate", "Tom", "Alice" };

// Змінюємо порядок 3 елементів починаючи з індексу 1
Array.Reverse(people, 1, 3);

foreach (var person in people)
    Console.Write($"{person} ");
// "Tom", "Kate", "Bob", "Sam", "Tom", "Alice"
```

У цьому випадку змінюємо порядок лише 3 елементів, починаючи з індексу 1.

### Зміна розміру масиву

Для зміни розміру масиву застосовується метод `Resize`. Його перший параметр - масив, що змінюється, а другий параметр - кількість елементів, які повинні бути в масиві. Якщо другий параметр менший за довжину масиву, то масив усікається. Якщо значення параметра, навпаки, більше, масив доповнюється додатковими елементами, які мають значення за замовчуванням. Причому перший параметр передається за посиланням:

```csharp
var people = new string[] { "Tom", "Sam", "Bob", "Kate", "Tom", "Alice" };

// Зменшимо масив до 4 елементів.
Array.Resize(ref people, 4);

foreach (var person in people)
    Console.Write($"{person} ");
// "Tom", "Sam", "Bob", "Kate"
```

### Копіювання масиву

Метод `Copy` копіює частину одного масиву до іншого:

```csharp
var people = new string[] { "Tom", "Sam", "Bob", "Kate", "Tom", "Alice" };

var employees = new string[3];

// Копіюємо 3 елементи з масиву people з індексу 1
// і вставляємо їх у масив employees починаючи з індексу 0.
Array.Copy(people, 1, employees, 0, 3);

foreach (var person in employees)
    Console.Write($"{person} ");
// Sam Bob Kate
```

У даному випадку копіюємо 3 елементи з масиву людей починаючи з індексу 1 і вставляємо їх у масив `employees` починаючи з індексу 0.

### Сортування масиву

Відсортуємо масив за допомогою методу `Sort()`:

```csharp
var people = new string[] { "Tom", "Sam", "Bob", "Kate", "Tom", "Alice" };

Array.Sort(people);

foreach (var person in people)
    Console.Write($"{person} ");

// Alice Bob Kate Sam Tom Tom
```

Цей метод має багато перевантажень. Наприклад, одна з версій дозволяє відсортувати лише частину масиву:

```csharp
var people = new string[] { "Tom", "Sam", "Bob", "Kate", "Tom", "Alice" };

// Сортуємо з 1 індексу 3 елементи.
Array.Sort(people, 1, 3);

foreach (var person in people)
    Console.Write($"{person} ");

// Tom Bob Kate Sam Tom Alice
```
