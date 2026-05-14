## 10.3. Черга Queue

Клас `Queue` представляє звичайну чергу, яка працює за алгоритмом FIFO ("перший увійшов - перший вийшов").

### Створення черги

Для створення черги можна використовувати один із трьох її конструкторів. Насамперед можна створити порожню чергу:

```csharp
Queue<string> people = new Queue<string>();
```

Під час створення порожньої черги можна вказати ємність черги:

```csharp
Queue<string> people = new Queue<string>(16);
```

Також можна ініціалізувати чергу елементами з іншої колекції або масивом:

```csharp
var employees = new List<string> { "Tom", "Sam", "Bob" };
Queue<string> people = new Queue<string>(employees);

foreach (var person in people)
{
    Console.WriteLine(person);
}

Console.WriteLine(people.Count); // 3
```

Для перебору черги можна використовувати стандартний цикл `foreach`.

Для отримання кількості елементів у черзі у класі визначено властивість `Count`.

### Методи Queue

У класу `Queue<T>` можна назвати такі методи:

- `void Clear()`: очищає чергу
- `bool Contains(T item)`: повертає `true`, якщо елемент `item` є в черзі
- `T Dequeue()`: витягує та повертає перший елемент черги
- `void Enqueue(T item)`: додає елемент до кінця черги
- `T Peek()`: просто повертає перший елемент із початку черги без його видалення

Подивимося застосування черги практично:

```csharp
var people = new Queue<string>();

// додаємо елементи
people.Enqueue("Tom"); // people = { Tom }
people.Enqueue("Bob"); // people = { Tom, Bob }
people.Enqueue("Sam"); // people = { Tom, Bob, Sam }

// отримуємо елемент із самого початку черги
var firstPerson = people.Peek();
Console.WriteLine(firstPerson); // Tom

// видаляємо елементи
var person1 = people.Dequeue(); // people = { Bob, Sam }
Console.WriteLine(person1); // Tom

var person2 = people.Dequeue(); // people = { Sam }
Console.WriteLine(person2); // Bob

var person3 = people.Dequeue(); // people = { }
Console.WriteLine(person3); // Sam
```

Варто зазначити, що якщо за допомогою методів `Peek` або `Dequeue` ми спробуємо отримати перший елемент черги, яка порожня, програма видасть виняток. Відповідно перед отриманням елемента ми можемо перевіряти кількість елементів у черзі:

```csharp
if (people.Count > 0)
{
    var person = people.Peek();
    people.Dequeue();
}
```

Або можна використовувати пару методів:

- `bool TryDequeue(out T result)`: передає в змінну `result` перший елемент черги з його видаленням з черги, повертає `true`, якщо черга не порожня і успішно отриманий елемент.
- `bool TryPeek(out T result)`: передає в змінну `result` перший елемент черги без його вилучення з черги, повертає `true`, якщо черга не порожня і успішно отриманий елемент.

Застосування методів:

```csharp
var people = new Queue<string>();

// додаємо елементи
people.Enqueue("Tom"); // people = { Tom }

// видаляємо елементи
var success1 = people.TryDequeue(out var person1); // success1 = true
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

Черги досить часто зустрічаються в реальному житті. Наприклад, черга пацієнтів на прийом до лікаря. Реалізуємо цю ситуацію:

```csharp
var patients = new Queue<Person>();
patients.Enqueue(new Person("Tom"));
patients.Enqueue(new Person("Bob"));
patients.Enqueue(new Person("Sam"));

var practitioner = new Doctor();
practitioner.TakePatients(patients);

class Person
{
    public string Name { get; }
    public Person(string name) => Name = name;
}

class Doctor
{
    public void TakePatients(Queue<Person> patients)
    {
        while (patients.Count > 0)
        {
            var patient = patients.Dequeue();
            Console.WriteLine($"Огляд пацієнта {patient.Name}");
        }

        Console.WriteLine("Лікар завершив огляд пацієнтів");
    }
}
```

Тут клас лікаря - клас `Doctor` у методі `TakePatients` приймає чергу пацієнтів у вигляді об'єктів `Person`. І поки в черзі є об'єкти, витягує по одному об'єкту. Консольний вивід:

```text
Огляд пацієнта Tom
Огляд пацієнта Bob
Огляд пацієнта Sam
Лікар завершив огляд пацієнтів
```
