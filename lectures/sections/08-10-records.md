---
chapter: 8
chapterTitle: "Розділ 8. Додаткові можливості ООП у C#"
section: 10
number: "8.10"
title: "Records"
source: "../_combined/55-records.md"
---

## 8.10. Records

Records представляють новий тип посилань, який з'явився в C# 9. Ключова особливість records полягає в тому, що вони можуть представляти незмінний (immutable) тип, який за умовчанням має низку додаткових можливостей у порівнянні з класами та структурами. Навіщо нам потрібні незмінні типи? Такі типи безпечніші в тих ситуаціях, коли нам треба гарантувати, що дані об'єкта не будуть змінюватися. У .NET у принципі вже є незмінні типи, наприклад, String.

Варто зазначити, що починаючи з версії C# 10 додано підтримку структур record, відповідно ми можемо створювати record-класи та record-структури.

Для визначення records використовується ключове слово record. Якщо визначається клас record, то ключове слово class можна не використовувати щодо типу:

```csharp
public record Person
{
    public string Name { get; set; }
    public Person(string name) => Name = name;
}
```

або так

```csharp
public record class Person
{
    public string Name { get; set; }
    public Person(string name) => Name = name;
}
```

При визначенні структури record при оголошенні типу треба використовувати ключове слово struct:

```csharp
public record struct Person
{
    public string Name { get; set; }
    public Person(string name) => Name = name;
}
```

Хоча типи record призначені для створення незмінних типів, проте одне тільки застосування ключового слова record не гарантує незмінність об'єктів record. Вони є незмінними (immutable) лише за певних умов. Наприклад, ми можемо написати так:

```csharp
var person = new Person("Tom");
person.Name = "Bob";
Console.WriteLine(person.Name); // Bob - дані змінилися

public record Person
{
    public string Name { get; set; }
    public Person(string name) => Name = name;
}
```

При виконанні цього коду не виникне помилки, ми спокійно зможемо змінювати значення властивостей об'єкта Person. Щоб зробити його справді незмінним, для властивостей замість звичайних сеттерів треба використовувати модифікатор init.

```csharp
var person = new Person("Tom");
person.Name = "Bob";    // ! помилка - властивість змінити не можна

public record Person
{
    public string Name { get; init; }
    public Person(string name) => Name = name;
}
```

У цьому випадку ми отримаємо помилку при спробі змінити значення властивостей об'єкта Person.

У багатьох records схожі на звичайні класи і структури, наприклад, вони можуть бути абстрактними, їх також можна успадковувати або забороняти успадкування за допомогою оператора sealed. Проте є й низка відмінностей. Розглянемо деякі основні відмінності записів від стандартних класів і структур.

### Порівняння на рівність

При визначенні record компілятор генерує метод Equals() порівняння з іншим об'єктом. При цьому порівняння двох records проводиться з урахуванням їх значень. Наприклад, розглянемо наступний приклад

```csharp
var person1 = new Person("Tom");
var person2 = new Person("Tom");
Console.WriteLine(person1.Equals(person2)); // true

var user1 = new User("Tom");
var user2 = new User("Tom");
Console.WriteLine(user1.Equals(user2));     // false

public record Person
{
    public string Name { get; init; }

    public Person(string name) => Name = name;
}
public class User
{
    public string Name { get; init; }
    public User(string name) => Name = name;
}
```

У разі при порівнянні двох об'єктів record Person ми побачимо, що вони рівні, оскільки їх значення (значення властивостей Name) рівні. Однак у випадку з об'єктами класу User, які мають однакові значення, ми побачимо, що вони не рівні. Оскільки порівняння records проводиться саме за значенням.

Крім того, для record вже за замовчуванням реалізовані оператори == і !=, які також порівнюють дві record за значенням:

```csharp
var person1 = new Person("Tom");
var person2 = new Person("Tom");
Console.WriteLine(person1 == person2); // true

var user1 = new User("Tom");
var user2 = new User("Tom");
Console.WriteLine(user1 == user2);     // false
```

### Оператор with

На відміну від класів records підтримують ініціалізацію за допомогою оператора with. Він дозволяє створити одну record на основі іншої record:

```csharp
var tom = new Person("Tom", 37);
var sam = tom with { Name = "Sam" };
Console.WriteLine($"{sam.Name} - {sam.Age}"); // Sam - 37

public record Person
{
    public string Name { get; init; }
    public int Age { get; init; }
    public Person(string name, int age)
    {
        Name = name; Age = age;
    }
}
```

Після record, значення якої хочемо скопіювати, вказується оператор with, після якого у фігурних дужках вказуються значення тих властивостей, які хочемо змінити. Так, у разі змінна sam отримує властивості Age значення з tom, а властивість Name змінюється.

Ця можливість може бути особливо актуальною, якщо в record, яку ми хочемо скопіювати, безліч властивостей, з яких хочемо поміняти одне-два.

Якщо треба скопіювати значення всіх властивостей, можна залишити порожні фігурні дужки:

```csharp
var person1 = new Person("Tom", 37);
var person2 = person1 with { };
```

### Позиційні records

Records можуть приймати дані властивостей через конструктор, і в цьому разі ми можемо скоротити їх визначення. Наприклад, нехай у нас є наступна record Person:

```csharp
public record struct Person
{
    public string Name { get; init; }
    public int Age { get; init; }
    public Person(string name, int age)
    {
        Name = name; Age = age;
    }
    public void Deconstruct(out string name, out int age) =>
        (name, age) = (Name, Age);
}
```

Крім конструктора, тут реалізований деконструктор, який дозволяє розкласти об'єкт Person на кортеж значень. І ми могли б застосувати його, наприклад, так:

```csharp
var person = new Person("Tom", 37);
Console.WriteLine(person.Name); // Tom

var (personName, personAge) = person;

Console.WriteLine(personAge);     // 37
Console.WriteLine(personName);    // Tom
```

Вище визначену record Person можна скоротити до позиційної record:

```csharp
public record Person(string Name, int Age);
```

Це все визначення типу. Тобто ми говоримо, що для типу Person буде створюватися конструктор, який приймає два параметри і присвоює їх значення відповідно до властивостей Name і Age, і що також автоматично створюватиметься деконструктор. Його використання буде аналогічним:

```csharp
var person = new Person("Tom", 37);
Console.WriteLine(person); // Person { Name = Tom, Age = 37 }

var (personName, personAge) = person;

Console.WriteLine(personAge);     // 37
Console.WriteLine(personName);    // Tom

public record Person(string Name, int Age);
```

При необхідності також можна поєднувати стандартне визначення властивостей та визначення властивостей через конструктор:

```csharp
var person = new Person("Tom", 37) { Company = "Google" };
Console.WriteLine(person.Company); // Google
person.Company = "Microsoft";
Console.WriteLine(person.Company); // Microsoft

public record Person(string Name, int Age)
{
    public string Company { get; set; } = "";
}
```

### Позиційні структури для читання

Слід зазначити різницю між позиційними класами і структурами record. Властивості класу record, які встановлюються через параметри конструктора, за замовчуванням матимуть модифікатор init. Тобто після встановлення їх значень через конструктор ми більше не зможемо їх змінити:

```csharp
var person = new Person("Tom", 37);
person.Name = "Bob";    // ! Помилка - значення не можна змінити
public record Person(string Name, int Age);
```

Це стосується тільки тих властивостей, які встановлюються через конструктор.

Однак для позиційних структур record властивості матимуть стандартні сеттери, які дозволять змінювати значення властивостей:

```csharp
var person = new Person("Tom", 37);
person.Name = "Bob";
Console.WriteLine(person.Name); // Bob - значення змінилося
// структура record
public record struct Person(string Name, int Age);
```

Щоб для подібних властивостей структури record використовувався модифікатор init замість звичайних сеттерів, таку структуру треба визначити ключовим словом readonly:

```csharp
var person = new Person("Tom", 37);
person.Name = "Bob";    // ! Помилка - значення властивості не можна змінити
// структура record доступна лише для читання
public readonly record struct Person(string Name, int Age);
```

### ToString

Невеликою перевагою типів record також є те, що для них вже за умовчанням реалізовано метод ToString(), який виводить стан об'єкта у відформатованому вигляді:

```csharp
var person = new Person("Tom", 37);
Console.WriteLine(person); // Person {Name = Tom, Age = 37}

public record Person(string Name, int Age);
```

### Успадкування

Як і звичайні класи record-класи можуть успадковуватися:

```csharp
var tom = new Person("Tom", 37);
var bob = new Employee("Bob", 41, "Microsoft");
Console.WriteLine(tom); // Person {Name = Tom, Age = 37}
Console.WriteLine(bob); // Employee {Name = Bob, Age = 41, Company = Microsoft}

public record Person(string Name, int Age);
public record Employee(string Name, int Age, string Company) : Person(Name, Age);
```

У даному випадку клас record Employee успадковується від Person.
