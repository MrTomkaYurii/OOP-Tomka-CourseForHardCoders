
## 4.3. Віртуальні методи та властивості

При наслідуванні нерідко виникає необхідність змінити в класі-спадкоємці функціонал методу, який успадкував від базового класу. У цьому випадку клас-спадкоємець може перевизначати методи та властивості базового класу.

Ті методи та властивості, які ми хочемо зробити доступними для перевизначення, у базовому класі позначаються модифікатором `virtual`. Такі методи та властивості називають віртуальними.

А щоб перевизначити метод у класі-спадкоємці, цей метод визначається з модифікатором `override`. Перевизначений метод у класі-спадкоємці повинен мати той самий набір параметрів, що й віртуальний метод у базовому класі.

Наприклад, розглянемо такі класи:

```csharp
class Person
{
    public string Name { get; set; }

    public Person(string name)
    {
        Name = name;
    }

    public virtual void Print()
    {
        Console.WriteLine(Name);
    }
}

class Employee : Person
{
    public string Company { get; set; }

    public Employee(string name, string company) : base(name)
    {
        Company = company;
    }
}
```

Тут клас `Person` представляє людину. Клас `Employee` успадковується від `Person` і представляє співробітника підприємства. Цей клас крім успадкованої властивості `Name` має ще одну властивість - `Company`.

Щоб зробити метод `Print` доступним для перевизначення, цей метод визначено модифікатором `virtual`. Тому ми можемо перевизначити цей метод, але можемо не перевизначати. Допустимо, нас влаштовує реалізація методу з базового класу. У цьому випадку об'єкти `Employee` будуть використовувати реалізацію методу `Print` із класу `Person`:

```csharp
Person bob = new Person("Bob");
bob.Print(); // виклик методу Print із класу Person

Employee tom = new Employee("Tom", "Microsoft");
tom.Print(); // виклик методу Print із класу Person
```

Консольний вивід:

![Консольний вивід без перевизначення методу Print](assets/docx/image87.png)

Але можемо також перевизначити віртуальний метод. Для цього в класі-спадкоємці визначається метод з модифікатором `override`, який має те саме ім'я та набір параметрів:

```csharp
class Employee : Person
{
    public string Company { get; set; }

    public Employee(string name, string company)
    : base(name)
    {
        Company = company;
    }

    public override void Print()
    {
        Console.WriteLine($"{Name} працює в {Company}");
    }
}
```

Візьмемо ті самі об'єкти:

```csharp
Person bob = new Person("Bob");
bob.Print(); // виклик методу Print із класу Person

Employee tom = new Employee("Tom", "Microsoft");
tom.Print(); // виклик методу Print із класу Employee
```

Консольний вивід:

![Консольний вивід після перевизначення методу Print](assets/docx/image88.png)

Віртуальні методи базового класу визначають інтерфейс усієї ієрархії, тобто у будь-якому похідному класі, який не є прямим спадкоємцем від базового класу, можна перевизначити віртуальні методи. Наприклад, ми можемо визначити клас `Manager`, який буде похідним від `Employee`, та в ньому також перевизначити метод `Print`.

При перевизначенні віртуальних методів слід враховувати низку обмежень:

- Віртуальний і перевизначений методи повинні мати той самий модифікатор доступу. Тобто якщо віртуальний метод визначено за допомогою модифікатора `public`, то й перевизначений метод повинен мати модифікатор `public`.
- Не можна перевизначити чи оголосити віртуальним статичний метод.

## Ключове слово base

Крім конструкторів, ми можемо звернутись за допомогою ключового слова `base` до інших членів базового класу. У нашому випадку виклик `base.Print();` буде зверненням до методу `Print()` у класі `Person`:

```csharp
class Employee : Person
{
    public string Company { get; set; }

    public Employee(string name, string company)
    : base(name)
    {
        Company = company;
    }

    public override void Print()
    {
        base.Print();
        Console.WriteLine($"працює в {Company}");
    }
}
```

## Перевизначення властивостей

Так само як і методи, можна перевизначати властивості:

```csharp
class Person
{
    int age = 1;

    public virtual int Age
    {
        get => age;
        set { if (value > 0 && value < 110) age = value; }
    }

    public string Name { get; set; }

    public Person(string name)
    {
        Name = name;
    }

    public virtual void Print() => Console.WriteLine(Name);
}

class Employee : Person
{
    public override int Age
    {
        get => base.Age;
        set { if (value > 17 && value < 110) base.Age = value; }
    }

    public string Company { get; set; }

    public Employee(string name, string company)
    : base(name)
    {
        Company = company;
        base.Age = 18; // вік для працівників за умовчанням
    }
}
```

В даному випадку в класі `Person` визначено віртуальну властивість `Age`, яка встановлює значення, якщо вона більша за 0 і менше 110. У класі `Employee` ця властивість перевизначена - вік працівника повинен бути не меншим за 18.

```csharp
Person bob = new Person("Bob");
Console.WriteLine(bob.Age); // 1

Employee tom = new Employee("Tom", "Microsoft");
Console.WriteLine(tom.Age); // 18
tom.Age = 22;
Console.WriteLine(tom.Age); // 22
tom.Age = 12;
Console.WriteLine(tom.Age); // 22
```

## Заборона перевизначення методів

Також можна заборонити перевизначення методів та властивостей. В цьому випадку їх треба оголошувати з модифікатором `sealed`:

```csharp
class Employee : Person
{
    public string Company { get; set; }

    public Employee(string name, string company)
    : base(name)
    {
        Company = company;
    }

    public override sealed void Print()
    {
        Console.WriteLine($"{Name} працює в {Company}");
    }
}
```

При створенні методів з модифікатором `sealed` треба враховувати, що `sealed` застосовується в парі з `override`, тобто тільки в методах, що перевизначаються.

І в цьому випадку ми не зможемо перевизначити метод `Print` у класі, успадкованому від `Employee`.

