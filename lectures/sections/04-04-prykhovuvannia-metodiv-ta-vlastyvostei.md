---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 4
number: "4.4"
title: "Приховування методів та властивостей"
source: "../_combined/21-prykhovuvannia-metodiv-ta-vlastyvostei.md"
---

## 4.4. Приховування методів та властивостей

У минулій темі було розглянуто визначення та перевизначення віртуальних методів. Іншим способом змінити функціональність методу, успадкованого від базового класу, є приховування (shadowing/hiding).

Фактично приховування методу/властивості представляє визначення в класі-спадкоємці методу або властивості, які відповідають за ім'ям та набором параметрів методу або властивості базового класу. Для приховування членів класу застосовується ключове слово `new`. Наприклад:

```csharp
class Person
{
    public string Name { get; set; }

    public Person(string name)
    {
        Name = name;
    }

    public void Print()
    {
        Console.WriteLine($"Name: {Name}");
    }
}

class Employee : Person
{
    public string Company { get; set; }

    public Employee(string name, string company)
    : base(name)
    {
        Company = company;
    }

    public new void Print()
    {
        Console.WriteLine($"Name: {Name}   Company: {Company}");
    }
}
```

Тут визначено клас `Person`, який представляє людину, та клас `Employee`, який представляє працівника підприємства. `Employee` успадковує від `Person` всі властивості та методи. Але в класі `Employee`, крім успадкованих властивостей, є також і власна властивість `Company`, яка зберігає назву компанії. І ми хотіли б у методі `Print` виводити інформацію про компанію разом із ім'ям на консоль. Для цього визначається метод `Print` з ключовим словом `new`, який приховує реалізацію методу з базового класу.

У яких ситуаціях можна використовувати приховування? Наприклад, у прикладі вище метод `Print` у базовому класі не є віртуальним, ми не можемо його перевизначити, але, припустимо, нас не влаштовує його реалізація для похідного класу, тому ми можемо скористатися приховуванням, щоб визначити потрібний нам функціонал.

Використовуємо ці класи у програмі у методі `Main`:

```csharp
Person bob = new Person("Bob");
bob.Print();    // Name: Bob

Employee tom = new Employee("Tom", "Microsoft");
tom.Print();    // Name: Tom  Company: Microsoft
```

Консольний вивід програми:

![Консольний вивід прихованого методу Print](assets/docx/image89.png)

При цьому якщо ми хочемо звернутися саме до реалізації властивості або методу в базовому класі, то ми можемо знову використовувати ключове слово `base` і через нього звертатися до функціональності базового класу.

```csharp
class Employee : Person
{
    public string Company { get; set; }

    public Employee(string name, string company)
    : base(name)
    {
        Company = company;
    }

    public new void Print()
    {
        base.Print(); // Викликаємо метод Print з базового класу Person
        Console.WriteLine($"Company: {Company}");
    }
}
```

## Приховування властивостей

Подібним образом ми можемо організувати приховування властивостей:

```csharp
Person bob = new Person("Bob");
Console.WriteLine(bob.Name); // Bob

Employee tom = new Employee("Tom", "Microsoft");
Console.WriteLine(tom.Name); // Mr./Ms. Tom

class Person
{
    public string Name { get; set; }

    public Person(string name)
    {
        Name = name;
    }
}

class Employee : Person
{
    // приховуємо властивість Name базового класу
    public new string Name
    {
        get => $"Mr./Ms. {base.Name}";
        set => base.Name = value;
    }

    public string Company { get; set; }

    public Employee(string name, string company)
    : base(name)
    {
        Company = company;
    }
}
```

У разі в класі `Employee` перевизначено властивість `Name`. У блоці `get` беремо значення властивості з базового класу `Person` і приєднуємо до нього `"Mr./Ms."`. У блоці `set` передаємо отримане значення на реалізацію властивості `Name` базового класу `Person`.

## Приховування змінних та констант

На відміну від перевизначення C# дозволяє застосовувати приховування до змінних (як статичних, так і нестатичних) і константів, також використовуючи ключове слово `new`:

```csharp
Console.WriteLine(Person.minAge); // 1
Console.WriteLine(Person.typeName); // Person

Console.WriteLine(Employee.minAge); // 18
Console.WriteLine(Employee.typeName); // Employee

class Person
{
    public readonly static int minAge = 1;
    public const string typeName = "Person";
}

class Employee : Person
{
    // приховуємо поля та константи базового класу
    public new readonly static int minAge = 18;
    public new const string typeName = "Employee";
}
```
