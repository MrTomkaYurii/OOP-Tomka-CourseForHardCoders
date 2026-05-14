---
chapter: 10
chapterTitle: "Розділ 10. Колекції"
section: 2
number: "10.2"
title: "Двозв'язаний список LinkedList<T>"
source: "../_combined/63-dvozviazanyi-spysok-linkedlist-t.md"
---

## 10.2. Двозв'язаний список LinkedList<T>

Клас `LinkedList<T>` представляє двозв'язковий список, в якому кожен елемент зберігає посилання одночасно на наступний і попередній елемент.

### Створення зв'язаного списку

Для створення зв'язкового списку можна використати один із його конструкторів. Наприклад, створимо порожній зв'язковий список:

```csharp
LinkedList<string> people = new LinkedList<string>();
```

У цьому випадку пов'язаний список `people` призначений для зберігання рядків.

Також можна до конструктора передати колекцію елементів, наприклад, список `List`, за яким буде створено зв'язковий список:

```csharp
var employees = new List<string> { "Tom", "Sam", "Bob" };

LinkedList<string> people = new LinkedList<string>(employees);

foreach (string person in people)
{
    Console.WriteLine(person);
}
```

### LinkedListNode

Якщо у простому списку `List<T>` кожен елемент представляє об'єкт типу `T`, то в `LinkedList<T>` кожен вузол представляє об'єкт класу `LinkedListNode<T>`. А елементи `T`, що додаються до пов'язаного списку, фактично обертаються в об'єкт `LinkedListNode`.

Клас `LinkedListNode` має такі властивості:

- `Value`: повертає або встановлює значення вузла, представлене типом `T`
- `Next`: повертає посилання на наступний елемент типу `LinkedListNode<T>` у списку. Якщо наступний елемент відсутній, має значення `null`
- `Previous`: повертає посилання на попередній елемент типу `LinkedListNode<T>` у списку. Якщо попередній елемент відсутній, має значення `null`

### Властивості LinkedList

Клас `LinkedList` визначає такі властивості:

- `Count`: кількість елементів у зв'язаному списку
- `First`: перший вузол у списку як об'єкт `LinkedListNode<T>`
- `Last`: останній вузол у списку як об'єкт `LinkedListNode<T>`

Використовуємо ці властивості:

```csharp
var employees = new List<string> { "Tom", "Sam", "Bob" };

LinkedList<string> people = new LinkedList<string>(employees);
Console.WriteLine(people.Count);        // 3
Console.WriteLine(people.First?.Value); // Tom
Console.WriteLine(people.Last?.Value);  // Bob
```

Використовуючи властивості `LinkedList` і `LinkedListNode`, можна пройтись по всіх елементах списку у прямому або зворотному порядку:

```csharp
LinkedList<string> people = new LinkedList<string>(new[] { "Tom", "Sam", "Bob" });

// від початку до кінця списку
var currentNode = people.First;
while (currentNode != null)
{
    Console.WriteLine(currentNode.Value);
    currentNode = currentNode.Next;
}

// з кінця до початку списку
currentNode = people.Last;
while (currentNode != null)
{
    Console.WriteLine(currentNode.Value);
    currentNode = currentNode.Previous;
}
```

### Методи LinkedList

Використовуючи методи класу `LinkedList<T>`, можна звертатися до різних елементів як наприкінці, так і на початку списку:

- `AddAfter(LinkedListNode<T> node, LinkedListNode<T> newNode)`: вставляє вузол `newNode` у список після вузла `node`.
- `AddAfter(LinkedListNode<T> node, T value)`: вставляє новий вузол зі значенням `value` після вузла `node`.
- `AddBefore(LinkedListNode<T> node, LinkedListNode<T> newNode)`: вставляє в список вузол `newNode` перед вузлом `node`.
- `AddBefore(LinkedListNode<T> node, T value)`: вставляє новий вузол зі значенням `value` перед вузлом `node`.
- `AddFirst(LinkedListNode<T> node)`: вставляє новий вузол на початок списку
- `AddFirst(T value)`: вставляє новий вузол зі значенням `value` на початок списку
- `AddLast(LinkedListNode<T> node)`: вставляє новий вузол у кінець списку
- `AddLast(T value)`: вставляє новий вузол зі значенням `value` до кінця списку
- `RemoveFirst()`: видаляє перший вузол зі списку. Після цього новим першим вузлом стає вузол, що йде за видаленим
- `RemoveLast()`: видаляє останній вузол зі списку

Застосуємо деякі з цих методів:

```csharp
var people = new LinkedList<string>();

people.AddLast("Tom"); // вставляємо вузол зі значенням Tom на останнє місце
// так як у списку немає вузлів, то останній буде також першим

people.AddFirst("Bob"); // вставляємо вузол зі значенням Bob на перше місце

// вставляємо після першого вузла новий вузол зі значенням Mike
if (people.First != null)
{
    people.AddAfter(people.First, "Mike");
}

// тепер у нас список має таку послідовність: Bob Mike Tom
foreach (var person in people)
{
    Console.WriteLine(person);
}
```

Подібним чином можна створювати пов'язані списки та інші типи:

```csharp
var company = new LinkedList<Person>();

company.AddLast(new Person("Tom"));
company.AddLast(new Person("Sam"));
company.AddFirst(new Person("Bill"));

foreach (var person in company)
{
    Console.WriteLine(person.Name);
}

class Person
{
    public string Name { get; }
    public Person(string name) => Name = name;
}
```
