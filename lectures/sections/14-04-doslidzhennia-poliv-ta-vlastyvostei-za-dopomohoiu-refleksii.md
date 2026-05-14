---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
section: 4
number: "14.4"
title: "Дослідження полів та властивостей за допомогою рефлексії"
source: "../_combined/87-doslidzhennia-poliv-ta-vlastyvostei-za-dopomohoiu-refleksii.md"
---

## 14.4. Дослідження полів та властивостей за допомогою рефлексії

### Отримання інформації про поля

Для отримання всіх полів застосовується метод `GetFields()`, який повертає масив об'єктів класу `FieldInfo`.

Деякі основні властивості та методи класу `FieldInfo`:

- `IsFamily`: повертає `true`, якщо поле має модифікатор доступу `protected`
- Властивість `IsFamilyAndAssembly`: повертає `true`, якщо поле має модифікатор доступу `private protected`
- `IsFamilyOrAssembly`: повертає `true`, якщо поле має модифікатор доступу `protected internal`
- `IsAssembly`: повертає `true`, якщо поле має модифікатор доступу `internal`
- `IsPrivate`: повертає `true`, якщо поле має модифікатор доступу `private`
- Властивість `IsPublic`: повертає `true`, якщо поле має модифікатор доступу `public`
- `IsStatic`: повертає `true`, якщо поле статичне
- Метод `GetValue()`: повертає значення поля
- Метод `SetValue()`: встановлює значення поля

Наприклад, отримаємо всі поля класу:

```csharp
using System.Reflection;

Type myType = typeof(Person);

Console.WriteLine("Поля:");
foreach (FieldInfo field in myType.GetFields(
    BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public | BindingFlags.Static))
{
    string modificator = "";

    // Отримуємо модифікатор доступу.
    if (field.IsPublic)
        modificator += "public ";
    else if (field.IsPrivate)
        modificator += "private ";
    else if (field.IsAssembly)
        modificator += "internal ";
    else if (field.IsFamily)
        modificator += "protected ";
    else if (field.IsFamilyAndAssembly)
        modificator += "private protected ";
    else if (field.IsFamilyOrAssembly)
        modificator += "protected internal ";

    // Якщо поле статичне.
    if (field.IsStatic) modificator += "static ";

    Console.WriteLine($"{modificator}{field.FieldType.Name} {field.Name}");
}

class Person
{
    static int minAge = 0;
    string name;
    int age;
    public Person(string name, int age)
    {
        this.name = name;
        this.age = age;
    }
    public void Print() => Console.WriteLine($"{name} - {age}");
}
```

Щоб отримати і статичні, і не статичні, і публічні, і непублічні поля, методу `GetFields()` передається набір прапорів:

```csharp
BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public | BindingFlags.Static
```

Консольний вивід:

```text
Поля:
private String name
private Int32 age
private static Int32 minAge
```

### Отримання та зміна значення поля

Для отримання одного поля на ім'я застосовується метод `GetField()`, якому передається ім'я поля:

```csharp
var name = myType.GetField("name", BindingFlags.Instance | BindingFlags.NonPublic);
```

Як другий необов'язковий параметр передається набір прапорів.

Причому рефлексія дозволяє набувати значень і змінювати їх навіть у приватних полів. Наприклад, отримаємо та змінимо значення поля `name`:

```csharp
using System.Reflection;

Type myType = typeof(Person);
Person tom = new Person("Tom", 37);

// Отримуємо приватне поле name.
var name = myType.GetField("name", BindingFlags.Instance | BindingFlags.NonPublic);

// Отримуємо значення поля name.
var value = name?.GetValue(tom);
Console.WriteLine(value); // Tom

// Змінюємо значення поля name.
name?.SetValue(tom, "Bob");
tom.Print(); // Bob - 37

class Person
{
    static int minAge = 1;
    string name;
    int age;
    public Person(string name, int age)
    {
        this.name = name;
        this.age = age;
    }
    public void Print() => Console.WriteLine($"{name} - {age}");
}
```

### Властивості

Для отримання всіх властивостей типу застосовується відповідно метод `GetProperties()`, який повертає масив об'єктів `PropertyInfo`. Для отримання однієї властивості на ім'я застосовується метод `GetProperty()`, якому передається назва властивості і який повертає об'єкт `PropertyInfo?`.

Деякий основний функціонал класу `PropertyInfo`:

- Властивість `Attributes`: повертає колекцію атрибутів властивості
- Властивість `CanRead`: повертає `true`, якщо властивість доступна для читання
- Властивість `CanWrite`: повертає `true`, якщо властивість доступна для запису
- Властивість `GetMethod`: повертає get-аксесор у вигляді об'єкта `MethodInfo?`
- Властивість `SetMethod`: повертає set-аксесор у вигляді об'єкта `MethodInfo?`
- Властивість `PropertyType`: повертає тип властивості
- Метод `GetValue()`: повертає значення властивості
- Метод `SetValue()`: встановлює значення властивості

Використовуємо деякі властивості `PropertyInfo` для отримання інформації про властивості:

```csharp
using System.Reflection;

Type myType = typeof(Person);
foreach (PropertyInfo prop in myType.GetProperties(
    BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public | BindingFlags.Static))
{
    Console.Write($"{prop.PropertyType} {prop.Name} {{");

    // Якщо властивість доступна для читання.
    if (prop.CanRead) Console.Write("get;");
    // Якщо властивість доступна для запису.
    if (prop.CanWrite) Console.Write("set;");
    Console.WriteLine("}");
}

class Person
{
    public string Name { get; }
    public int Age { get; set; }
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
    public void Print() => Console.WriteLine($"{Name} - {Age}");
}
```

```text
System.String Name {get;}
System.Int32 Age {get;set;}
```

За допомогою методів `PropertyInfo` можна маніпулювати значенням властивості. Наприклад, отримаємо та змінимо значення властивості:

```csharp
using System.Reflection;

Type myType = typeof(Person);
Person tom = new Person("Tom", 37);
// Отримуємо властивість Age.
var ageProp = myType.GetProperty("Age");
// Отримуємо значення властивості Age у об'єкта tom.

var age = ageProp?.GetValue(tom);
Console.WriteLine(age); // 37
// Встановлюємо нове значення для властивості Age об'єкта tom.
ageProp?.SetValue(tom, 22);
tom.Print(); // Tom - 22

class Person
{
    public string Name { get; }
    public int Age { get; set; }
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
    public void Print() => Console.WriteLine($"{Name} - {Age}");
}
```

Для отримання значення властивості методу `GetValue()` об'єкта `PropertyInfo` передається об'єкт, у якого викликається властивість. Результатом методу є значення властивості. Для встановлення значення методу `SetValue()` об'єкта `PropertyInfo` передається об'єкт, у якого встановлюється властивість, і власне нове значення властивості.
