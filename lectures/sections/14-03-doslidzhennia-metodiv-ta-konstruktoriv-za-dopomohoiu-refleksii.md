---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
section: 3
number: "14.3"
title: "Дослідження методів та конструкторів за допомогою рефлексії"
source: "../_combined/86-doslidzhennia-metodiv-ta-konstruktoriv-za-dopomohoiu-refleksii.md"
---

## 14.3. Дослідження методів та конструкторів за допомогою рефлексії

### Отримання інформації про методи

Для отримання інформації окремо про методи застосовується метод `GetMethods()`. Цей метод повертає всі методи типу у вигляді масиву об'єктів `MethodInfo`. Його властивості надають інформацію про метод. Зазначимо деякі з його властивостей:

- `IsAbstract`: повертає `true`, якщо метод абстрактний
- `IsFamily`: повертає `true`, якщо метод має модифікатор доступу `protected`
- `IsFamilyAndAssembly`: повертає `true`, якщо метод має модифікатор доступу `private protected`
- `IsFamilyOrAssembly`: повертає `true`, якщо метод має модифікатор доступу `protected internal`
- `IsAssembly`: повертає `true`, якщо метод має модифікатор доступу `internal`
- `IsPrivate`: повертає `true`, якщо метод має модифікатор доступу `private`
- `IsPublic`: повертає `true`, якщо метод має модифікатор доступу `public`
- `IsConstructor`: повертає `true`, якщо метод надає конструктор
- `IsStatic`: повертає `true`, якщо статичний метод
- `IsVirtual`: повертає `true`, якщо метод віртуальний
- `ReturnType`: повертає тип значення, що повертається

Деякі з методів `MethodInfo`:

- `GetMethodBody()`: повертає тіло методу у вигляді об'єкта `MethodBody`
- `GetParameters()`: повертає масив параметрів, де кожен параметр представлений об'єктом типу `ParameterInfo`
- `Invoke()`: викликає метод

Застосуємо ряд властивостей для дослідження методів класу:

```csharp
using System.Reflection;

Type myType = typeof(Printer);

Console.WriteLine("Методи:");
foreach (MethodInfo method in myType.GetMethods())
{
    string modificator = "";

    // Якщо метод статичний.
    if (method.IsStatic) modificator += "static ";
    // Якщо метод віртуальний.
    if (method.IsVirtual) modificator += "virtual ";

    Console.WriteLine($"{modificator}{method.ReturnType.Name} {method.Name}()");
}

class Printer
{
    public string DefaultMessage { get; set; } = "Hello";
    public void PrintMessage(string message, int times = 1)
    {
        while (times-- > 0) Console.WriteLine(message);
    }
    public string CreateMessage() => DefaultMessage;
}
```

На виході отримаємо таку інформацію:

```text
Методи:

String get_DefaultMessage()
Void set_DefaultMessage()
Void PrintMessage()
String CreateMessage()
Type GetType()
virtual String ToString()
virtual Boolean Equals()
virtual Int32 GetHashCode()
```

Як видно з виводу в категорію методів, також потрапляють і властивості, які по суті представляють два методи: `get` і `set`. Якщо така ситуація не влаштовує, можна додатково фільтрувати список методів:

```csharp
foreach (MethodInfo method in myType.GetMethods()
             .Where(m => !m.Name.StartsWith("get_") && !m.Name.StartsWith("set_")))
{
    // ...
}
```

### BindingFlags

У прикладі вище використовувалася проста форма методу `GetMethods()`, яка витягує всі загальнодоступні публічні методи. Але ми можемо використовувати й іншу форму методу: `MethodInfo[] GetMethods(BindingFlags)`. Об'єднуючи значення `BindingFlags`, можна комбінувати вивід. Наприклад, отримаємо лише методи самого класу без успадкованих, як публічні, і всі інші:

```csharp
using System.Reflection;

Type myType = typeof(Printer);

Console.WriteLine("Методи:");
foreach (MethodInfo method in myType.GetMethods(
             BindingFlags.DeclaredOnly |
             BindingFlags.Instance |
             BindingFlags.NonPublic |
             BindingFlags.Public))
{
    Console.WriteLine($"{method.ReturnType.Name} {method.Name}()");
}

class Printer
{
    public string DefaultMessage { get; set; } = "Hello";
    protected internal void PrintMessage(string message, int times = 1)
    {
        while (times-- > 0) Console.WriteLine(message);
    }
    private string CreateMessage() => DefaultMessage;
}
```

Тепер метод `PrintMessage` у класі `Printer` є `protected internal`, а метод `CreateMessage` має модифікатор `private`.

Для отримання всіх непублічних методів методу `GetMethods()` передається набір прапорів `BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public`, тобто отримуємо всі методи екземпляра, як публічні, так і непублічні, але виключаємо статичні. Відповідно тепер отримаємо наступний вивід:

```text
Методи:

String get_DefaultMessage()
Void set_DefaultMessage()
Void PrintMessage()
String CreateMessage()
```

### Дослідження параметрів

За допомогою методу `GetParameters()` можна отримати всі параметри методу як масив об'єктів `ParameterInfo`. Відзначимо деякі з властивостей `ParameterInfo`, які дозволяють отримати інформацію про параметри:

- `Attributes`: повертає атрибути параметра
- `DefaultValue`: повертає значення параметра за замовчуванням
- `HasDefaultValue`: повертає `true`, якщо параметр має значення за промовчанням
- `IsIn`: повертає `true`, якщо параметр має модифікатор `in`
- `IsOptional`: повертає `true`, якщо параметр є необов'язковим
- `IsOut`: повертає `true`, якщо параметр вихідний, тобто має модифікатор `out`
- `Name`: повертає назву параметра
- `ParameterType`: повертає тип параметра

Використовуємо тип `ParameterInfo` для дослідження параметрів:

```csharp
using System.Reflection;

foreach (MethodInfo method in typeof(Printer).GetMethods())
{
    Console.Write($"{method.ReturnType.Name} {method.Name}(");
    // Отримуємо всі параметри.
    ParameterInfo[] parameters = method.GetParameters();
    for (int i = 0; i < parameters.Length; i++)
    {
        var param = parameters[i];
        // Отримуємо модифікатори параметра.
        string modificator = "";
        if (param.IsIn) modificator = "in";
        else if (param.IsOut) modificator = "out";

        Console.Write($"{param.ParameterType.Name} {modificator} {param.Name}");
        // Якщо параметр має значення за замовчуванням.
        if (param.HasDefaultValue) Console.Write($"={param.DefaultValue}");
        // Якщо не останній параметр, додаємо кому.
        if (i < parameters.Length - 1) Console.Write(", ");
    }
    Console.WriteLine(")");
}

class Printer
{
    public void PrintMessage(string message, int times = 1)
    {
        while (times-- > 0) Console.WriteLine(message);
    }

    public void CreateMessage(out string message) => message = "Hello Metanit.com";
}
```

Консольний вивід:

```text
Void PrintMessage(String message, Int32 times=1)
Void CreateMessage(String& out message)
Type GetType()
String ToString()
Boolean Equals(Object obj)
Int32 GetHashCode()
```

Якщо параметр має модифікатор `ref`, `in`, `out`, то в кінці назви типу додається амперсанд - `String&`.

### Виклик методів

За допомогою методу `Invoke()` можна викликати метод:

```csharp
public object? Invoke(object? obj, object?[]? parameters);
```

Перший параметр є об'єкт, для якого викликається метод. Другий об'єкт є масив значень, які передаються параметрам методу. І також метод може повертати результат як значення `object?`.

Виклик методу:

```csharp
using System.Reflection;

var myPrinter = new Printer("Hello");

// Отримуємо метод Print.
var print = typeof(Printer).GetMethod("Print");
// Викликаємо метод Print.
print?.Invoke(myPrinter, parameters: null); // Hello

class Printer
{
    public string Text { get; }
    public Printer(string text) => Text = text;
    public void Print() => Console.WriteLine(Text);
}
```

Метод `GetMethod()` повертає метод, який має певне ім'я - у цьому випадку метод `Print`. Далі, використовуючи отриманий метод, його можна викликати. Тут при виклику як перший параметр передається об'єкт, для якого викликається метод `Print` - об'єкт `myPrinter`. І оскільки метод `Print` не приймає параметрів, параметру `parameters` передається значення `null`.

Якщо метод непублічний, то для отримання методу ми можемо передати прапори у виклик `GetMethod`:

```csharp
using System.Reflection;

var myPrinter = new Printer("Hello Guys");

// Отримуємо метод Print.
var print = typeof(Printer).GetMethod("Print",
    BindingFlags.Instance |
    BindingFlags.Public |
    BindingFlags.NonPublic);
// Викликаємо метод Print.
print?.Invoke(myPrinter, parameters: null); // Hello Guys

class Printer
{
    public string Text { get; }
    public Printer(string text) => Text = text;
    private void Print() => Console.WriteLine(Text);
}
```

Отримання результату:

```csharp
using System.Reflection;

var myPrinter = new Printer();
// Отримуємо метод CreateMessage.
var createMessage = typeof(Printer).GetMethod("CreateMessage");
// Викликаємо метод CreateMessage і отримуємо його результат.
var result = createMessage?.Invoke(myPrinter, parameters: null);
Console.WriteLine(result); // Hello Metanit.com

class Printer
{
    public string CreateMessage() => "Hello Metanit.com";
}
```

Варто зазначити, що результат методу є типом `object?`, відповідно при необхідності може знадобитися виконати приведення типів.

Передача параметрів:

```csharp
using System.Reflection;

var myPrinter = new Printer();
// Отримуємо метод PrintMessage.
var printMessage = typeof(Printer).GetMethod("PrintMessage");
// Викликаємо метод PrintMessage, передаючи йому два аргументи.
printMessage?.Invoke(myPrinter, new object[] { "Hi world", 3 });

class Printer
{
    public void PrintMessage(string message, int times)
    {
        while (times-- > 0) Console.WriteLine(message);
    }
}
```

Тут метод `PrintMessage` має два параметри - `message` (деяке повідомлення) і `times` (кілька разів треба вивести повідомлення на консоль). І для цих параметрів передаємо масив аргументів `new object[] { "Hi world", 3 }`. Таким чином, метод тричі виведе рядок `"Hi world"`.

Виклик узагальненого методу:

```csharp
using System.Reflection;

var myPrinter = new Printer();
// Отримуємо метод PrintValue.
var printValue = typeof(Printer).GetMethod("PrintValue");
// Отримуємо узагальнену версію методу для типу string.
var printStringValue = printValue?.MakeGenericMethod(typeof(string));
// Викликаємо метод PrintValue, передаючи йому рядок.
printStringValue?.Invoke(myPrinter, new object[] { "Hello world" });

class Printer
{
    public void PrintValue<T>(T value)
    {
        Console.WriteLine(value);
    }
}
```

Для отримання узагальненої версії методу, типізованої певним типом, у об'єкта `MethodInfo` викликається метод `MakeGenericMethod` - у нього передається тип, яким типізується метод.

### Отримання конструкторів

Для отримання конструкторів застосовується метод `GetConstructors()`, який повертає масив об'єктів класу `ConstructorInfo`. Цей клас багато в чому схожий на `MethodInfo` і має низку загальної функціональності. Деякі основні властивості та методи:

- `IsFamily`: повертає `true`, якщо конструктор має модифікатор доступу `protected`
- `IsFamilyAndAssembly`: повертає `true`, якщо конструктор має модифікатор доступу `private protected`
- `IsFamilyOrAssembly`: повертає `true`, якщо конструктор має модифікатор доступу `protected internal`
- `IsAssembly`: повертає `true`, якщо конструктор має модифікатор доступу `internal`
- `IsPrivate`: повертає `true`, якщо конструктор має модифікатор доступу `private`
- `IsPublic`: повертає `true`, якщо конструктор має модифікатор доступу `public`
- Метод `GetMethodBody()`: повертає тіло конструктора у вигляді об'єкта `MethodBody`
- Метод `GetParameters()`: повертає масив параметрів, де кожен параметр представлений об'єктом типу `ParameterInfo`
- Метод `Invoke()`: викликає конструктор

Досліджуємо конструктори:

```csharp
using System.Reflection;

Type myType = typeof(Person);

Console.WriteLine("Конструктори:");
foreach (ConstructorInfo ctor in myType.GetConstructors(
    BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public))
{
    string modificator = "";

    // Отримуємо модифікатор доступу.
    if (ctor.IsPublic)
        modificator += "public";
    else if (ctor.IsPrivate)
        modificator += "private";
    else if (ctor.IsAssembly)
        modificator += "internal";
    else if (ctor.IsFamily)
        modificator += "protected";
    else if (ctor.IsFamilyAndAssembly)
        modificator += "private protected";
    else if (ctor.IsFamilyOrAssembly)
        modificator += "protected internal";

    Console.Write($"{modificator} {myType.Name}(");
    // Отримуємо параметри конструктора.
    ParameterInfo[] parameters = ctor.GetParameters();
    for (int i = 0; i < parameters.Length; i++)
    {
        var param = parameters[i];
        Console.Write($"{param.ParameterType.Name} {param.Name}");
        if (i < parameters.Length - 1) Console.Write(", ");
    }
    Console.WriteLine(")");
}

class Person
{
    public string Name { get; }
    public int Age { get; }
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
    public Person(string name) : this(name, 1) { }
    private Person() : this("Tom") { }
}
```

У цьому випадку досліджуємо конструктори класу `Person`, один із яких є приватним. Консольний вивід:

```text
Конструктори:

public Person(String name, Int32 age)
public Person(String name)
private Person()
```
