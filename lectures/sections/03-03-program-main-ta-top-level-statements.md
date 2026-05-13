---
chapter: 3
chapterTitle: "Розділ 3. Класи, структури та простір імен"
section: 3
number: "3.3"
title: "Клас Program та метод Main. Програми верхнього рівня"
source: "../_combined/15-program-main-ta-top-level-statements.md"
---
## 3.3. Клас Program та метод Main. Програми верхнього рівня

Точкою входу до програми мовою C# є метод `Main`. Саме з цього починається виконання програми на C#. І програма на C# повинна обов'язково мати метод `Main`. Однак може виникнути питання, який ще метод `Main`, якщо Visual Studio 2022 за замовчуванням створює проект консольної програми з наступним кодом:

```csharp
// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");
```

І ця програма жодних методів `Main` не містить, але при цьому нормально виконується та виводить на консоль рядок `"Hello, World!"`, як і заплановано. Це так звана програма верхнього рівня (top-level program). А виклик `Console.WriteLine("Hello, World!")` представляє інструкцію рівня (top-level statement).

Проте насправді цей код неявно поміщається компілятором у метод `Main`, який, своєю чергою, міститься у класі `Program`. Насправді назва класу може бути будь-якою (як правило, це клас `Program`, власне тому файл коду, що генерується за умовчанням, називається `Program.cs`). Але метод `Main` є обов'язковою частиною консольної програми. Тому вище поданий код фактично еквівалентний наступній програмі:

```csharp
class Program
{
    static void Main(string[] args)
    {
        // See https://aka.ms/new-console-template for more information
        Console.WriteLine("Hello, World!");
    }
}
```

Визначення методу `Main` обов'язково починається зі статичного модифікатора, який вказує, що метод `Main` - статичний. Пізніше ми докладніше розберемо, що це означає.

Типом методу `Main`, що повертається, обов'язково є тип `void`. Крім того, як параметр він приймає масив рядків - `string[] args` - в реальній програмі це параметри, через які при запуску програми з консолі ми можемо передати їй деякі значення. Усередині методу розташовуються дії, які виконує програма.

До Visual Studio 2022 усі попередні студії створювали за умовчанням приблизно такий код. Але, починаючи з Visual Studio 2022, нам необов'язково вручну визначати клас `Program` і в ньому метод `Main` - компілятор генерує їх самостійно.

Якщо ми визначаємо якісь змінні, константи, методи та звертаємося до них, вони поміщаються у метод `Main`. Наприклад, наступна програма верхнього рівня

```csharp
string hello = "Hello METANIT.COM";

Print(hello);

void Print(string message)
{
    Console.WriteLine(message);
}
```

буде аналогічна наступній програмі:

```csharp
class Program
{
    static void Main(string[] args)
    {
        string hello = "Hello METANIT.COM";

        Print(hello);

        void Print(string message)
        {
            Console.WriteLine(message);
        }
    }
}
```

Якщо визначаються нові типи, наприклад, класи, вони розміщуються поза класом `Program`. Наприклад, код:

```csharp
Person tom = new();
tom.SayHello();

class Person
{
    public void SayHello() => Console.WriteLine("Hello");
}
```

буде аналогічний наступному

```csharp
class Program
{
    static void Main(string[] args)
    {
        Person tom = new();
        tom.SayHello();
    }
}

class Person
{
    public void SayHello() => Console.WriteLine("Hello");
}
```

Однак слід враховувати, що визначення типів (зокрема класів) повинні йти в кінці файлу після інструкцій верхнього рівня. Тобто:

```csharp
// інструкції верхнього рівня (top-level statements)
Person tom = new();
tom.SayHello();

// Визначення класу йде після інструкцій верхнього рівня
class Person
{
    public void SayHello() => Console.WriteLine("Hello");
}
```

Таким чином, ми можемо продовжувати писати програми верхнього рівня без явного визначення методу `Main`. Або ми можемо явно визначити метод `Main` і клас `Program`:

![Явне визначення класу Program і методу Main](assets/docx/image45.png)

```csharp
class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
    }
}
```

І цей код буде виконуватися аналогічним чином, ніби ми не використовували клас `Program` і метод `Main`.
