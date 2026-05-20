---
chapter: 3
chapterTitle: "Розділ 3. Класи, структури та простір імен"
section: 3
number: "3.3"
title: "Клас Program та метод Main. Програми верхнього рівня"
source: "../_combined/15-program-main-ta-top-level-statements.md"
---

## 3.3. Клас Program та метод Main. Програми верхнього рівня

Коли ви пишете перший рядок C#-коду і натискаєте «Запустити», виникає закономірне питання: з якого саме місця починається виконання програми? На відміну від скриптових мов, де інтерпретатор просто читає файл зверху донизу, у C# є чітко визначена **точка входу** — спеціальний метод, якому середовище виконання передає управління при старті. Розуміння цього механізму важливе, бо воно пояснює, чому одні змінні і методи доступні «скрізь», а інші — лише всередині класу, і яку роль відіграє структура файлу у великих проектах.

## Метод Main як точка входу

Точкою входу до програми мовою C# є метод `Main`. Саме з нього починається виконання, і програма обов'язково повинна містити цей метод. Класично він виглядає так:

```csharp
class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Клінічна система запущена.");
    }
}
```

Метод `Main` завжди оголошується зі статичним модифікатором `static` — це означає, що він належить класу, а не конкретному об'єкту, і може бути викликаний без створення екземпляра класу. Детальніше про `static` йтиметься в наступних розділах. Тип, що повертається, — `void` (метод нічого не повертає) або `int` (код завершення процесу). Параметр `string[] args` — масив рядків, через який можна передати аргументи при запуску програми з командного рядка.

## Програми верхнього рівня

Починаючи з C# 9 і Visual Studio 2022, створення нового консольного проекту генерує набагато лаконічніший стартовий код:

```csharp
// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");
```

Тут немає жодного визначення класу `Program` і методу `Main` — але програма повністю коректна і виконується без помилок. Це так звана **програма верхнього рівня** (top-level program), а рядки коду в ній — **інструкції верхнього рівня** (top-level statements).

Насправді компілятор C# сам генерує клас `Program` і метод `Main`, поміщаючи туди всі ваші інструкції верхнього рівня. Код вище фактично еквівалентний:

```csharp
class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
    }
}
```

Тобто розробник звільнений від написання цього шаблонного коду — компілятор робить це автоматично. Обидва варіанти дають той самий скомпільований результат.

![Top-level statements → компілятор генерує клас Program і метод Main](_assets/03-03/toplevel-to-main.png)

## Змінні, методи і класи у top-level програмах

Розміщення різних елементів у top-level програмі підпорядковується чітким правилам. Якщо ми оголошуємо змінні та локальні методи, вони потрапляють всередину згенерованого методу `Main`. Наприклад, ця програма верхнього рівня:

```csharp
string greeting = "Ласкаво просимо до клінічної системи";

PrintGreeting(greeting);

void PrintGreeting(string message)
{
    Console.WriteLine(message);
}
```

є повністю еквівалентною такому явному запису:

```csharp
class Program
{
    static void Main(string[] args)
    {
        string greeting = "Ласкаво просимо до клінічної системи";

        PrintGreeting(greeting);

        void PrintGreeting(string message)
        {
            Console.WriteLine(message);
        }
    }
}
```

Ситуація з класами інша: якщо в top-level програмі визначається новий клас, він розміщується **поза** класом `Program`, на рівні простору імен. Тому наступний код:

```csharp
Patient patient = new("Іван Петренко", 45);
patient.PrintInfo();

class Patient
{
    public string Name;
    public int Age;

    public Patient(string name, int age) { Name = name; Age = age; }
    public void PrintInfo() => Console.WriteLine($"Пацієнт: {Name}, {Age} років");
}
```

еквівалентний такому розгорнутому запису:

```csharp
class Program
{
    static void Main(string[] args)
    {
        Patient patient = new("Іван Петренко", 45);
        patient.PrintInfo();
    }
}

class Patient
{
    public string Name;
    public int Age;

    public Patient(string name, int age) { Name = name; Age = age; }
    public void PrintInfo() => Console.WriteLine($"Пацієнт: {Name}, {Age} років");
}
```

Клас `Patient` знаходиться поза `Program` в обох випадках — top-level синтаксис лише приховує від нас шаблонний код `Program`.

Є одне важливе обмеження: **визначення типів (класів, структур тощо) повинні йти в кінці файлу**, після всіх інструкцій верхнього рівня. Якщо розмістити клас перед інструкціями — компілятор видасть помилку. Правильний порядок:

```csharp
// Спочатку — інструкції верхнього рівня
Patient patient = new("Іван Петренко", 45);
patient.PrintInfo();

// Потім — визначення класів
class Patient
{
    public string Name;
    public int Age;

    public Patient(string name, int age) { Name = name; Age = age; }
    public void PrintInfo() => Console.WriteLine($"Пацієнт: {Name}, {Age} років");
}
```

## Явне визначення Main та його застосування

Незважаючи на зручність top-level синтаксису, явне визначення класу `Program` і методу `Main` залишається цілком коректним і досі широко використовується. Такий підхід обов'язковий у великих проектах, де потрібно мати кілька класів і чітко контролювати структуру коду, або коли інструменти і шаблони проекту вимагають явного `Main`.

```csharp run
using System;

class Program
{
    static void Main(string[] args)
    {
        Patient patient = new Patient("Марія Сидоренко", 32);
        patient.PrintInfo();
    }
}

class Patient
{
    public string Name;
    public int Age;

    public Patient(string name, int age)
    {
        Name = name;
        Age  = age;
    }

    public void PrintInfo()
    {
        Console.WriteLine($"Пацієнт: {Name}, {Age} років");
    }
}
```

Обидва підходи — top-level і явний `Main` — дають однаковий скомпільований результат. Вибір між ними — питання стилю, вимог команди або розміру проекту. Для навчальних прикладів і невеликих утиліт top-level синтаксис значно скорочує обсяг шаблонного коду і дозволяє зосередитись на суті задачі.
