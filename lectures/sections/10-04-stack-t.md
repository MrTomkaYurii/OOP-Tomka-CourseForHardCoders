---
chapter: 10
chapterTitle: "Розділ 10. Колекції"
section: 4
number: "10.4"
title: "Stack<T>"
source: "../_combined/65-stack-t.md"
---

## 10.4. Stack<T>

Клас `Stack` представляє колекцію, яка використовує алгоритм LIFO ("останній увійшов - перший вийшов"). За такої організації кожен наступний доданий елемент поміщається поверх попереднього. Вилучення з колекції відбувається у зворотному порядку - витягується той елемент, який знаходиться вище за всіх у стеку.

Стек - структура даних, що досить часто зустрічається в реальному житті. Банальні приклади стеків - стопка книг або тарілок, де кожну нову книгу або тарілку поміщають поверх попередньої. А витягують із цієї стопки книги/тарілки у зворотному порядку - спочатку найвищу і так далі. Інший приклад - одяг: припустимо, людина виходить на вулицю в зимову погоду і для цього спочатку одягає майку, потім сорочку, потім светр, і наприкінці куртку. Коли людина знімає з себе одяг - вона робить це у зворотному порядку: спочатку знімає куртку, потім светр і таке інше.

### Створення стеку

Для створення стека можна використовувати один із трьох конструкторів. Насамперед можна створити порожній стек:

```csharp
Stack<string> people = new Stack<string>();
```

При створенні порожнього стека можна вказати ємність стека:

```csharp
Stack<string> people = new Stack<string>(16);
```

Також можна ініціалізувати стек елементами з іншої колекції або масивом:

```csharp
var employees = new List<string> { "Tom", "Sam", "Bob" };
Stack<string> people = new Stack<string>(employees);

foreach (var person in people)
{
    Console.WriteLine(person);
}

Console.WriteLine(people.Count); // 3
```

Для перебору стека можна використовувати стандартний цикл `foreach`. Причому в циклі відповідно до алгоритму стека LIFO дані витягуються в порядку, зворотному додаванню. Консольний вивід у цьому випадку:

```text
Bob
Sam
Tom
3
```

Для отримання кількості елементів стека застосовується властивість `Count`.

### Методи Stack

У класі `Stack` можна виділити такі методи:

- `Clear`: очищує стек
- `Contains`: перевіряє наявність у стеку елемента та повертає `true` за його наявності
- `Push`: додає елемент у стек у верхівку стека
- `Pop`: витягує та повертає перший елемент зі стека
- `Peek`: просто повертає перший елемент зі стека без його видалення

Подивимося на прикладі:

```csharp
var people = new Stack<string>();

people.Push("Tom");
// people = { Tom }

people.Push("Sam");
// people = { Sam, Tom }

people.Push("Bob");
// people = { Bob, Sam, Tom }

// отримуємо перший елемент стека без його видалення
string headPerson = people.Peek();
Console.WriteLine(headPerson); // Bob

string person1 = people.Pop();
// people = { Sam, Tom }
Console.WriteLine(person1); // Bob

string person2 = people.Pop();
// people = { Tom }
Console.WriteLine(person2); // Sam

string person3 = people.Pop();
// people = { }
Console.WriteLine(person3); // Tom
```

Роботу стека можна представити такою ілюстрацією:

![Рисунок з оригінального документа](_assets/_docx/image100.png)

Варто відзначити, що якщо за допомогою методів `Peek` або `Pop` ми спробуємо отримати перший елемент стеку, який порожній, програма видасть виняток. Відповідно перед отриманням елемента ми можемо перевіряти кількість елементів у стеку:

```csharp
if (people.Count > 0)
{
    var person = people.Peek();
    people.Pop();
}
```

Або можна використовувати пару методів:

- `bool TryPop(out T result)`: видаляє зі стека перший елемент і передає його в змінну `result`, повертає `true`, якщо стек не порожній і успішно отриманий елемент.
- `bool TryPeek(out T result)`: передає в змінну `result` перший елемент стека без його вилучення, повертає `true`, якщо елемент успішно отримано.

Застосування методів:

```csharp
var people = new Stack<string>();

people.Push("Tom");
// people = { Tom }

// видаляємо елементи
var success1 = people.TryPop(out var person1); // success1 = true
if (success1)
{
    Console.WriteLine(person1); // Tom
}

var success2 = people.TryPeek(out var person2); // success2 = false
if (success2)
{
    Console.WriteLine(person2);
}
```
