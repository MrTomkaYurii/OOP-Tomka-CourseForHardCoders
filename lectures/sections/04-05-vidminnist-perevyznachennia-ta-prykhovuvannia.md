---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 5
number: "4.5"
title: "Відмінність перевизначення та приховування методів"
source: "../_combined/22-vidminnist-perevyznachennia-ta-prykhovuvannia.md"
---

## 4.5. Відмінність перевизначення та приховування методів

У попередніх розділах ми розглянули два способи змінити поведінку методу в похідному класі: **перевизначення** (`virtual` + `override`) і **приховування** (`new`). Зовні вони схожі — в обох випадках похідний клас має метод з тим самим іменем, що й базовий. Але поводяться вони принципово по-різному, і розуміння цієї різниці є критичним для написання коректного поліморфного коду.

## Перевизначення: пізнє зв'язування

При перевизначенні через `virtual` + `override` рішення про те, яку реалізацію методу викликати, приймається **під час виконання програми** на основі реального типу об'єкта. Цей механізм називається **пізнім зв'язуванням** (late binding або dynamic dispatch).

```csharp run
using System;

Person p = new Doctor("Олена Коваль", 38, "Кардіологія");
p.Print(); // Doctor.Print() — незважаючи на тип змінної Person

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }

    public virtual void Print()
    {
        Console.WriteLine($"Person.Print: {Name}");
    }
}

class Doctor : Person
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age) { Specialization = spec; }

    public override void Print()
    {
        Console.WriteLine($"Doctor.Print: {Name} | {Specialization}");
    }
}
```

Змінна `p` оголошена як `Person`, але реальний об'єкт у пам'яті — `Doctor`. При виклику `p.Print()` середовище виконання перевіряє реальний тип об'єкта і знаходить реалізацію `Doctor.Print()`.

## Таблиця віртуальних методів (VMT)

Для реалізації пізнього зв'язування компілятор C# формує для кожного класу **таблицю віртуальних методів** (Virtual Method Table, VMT). У цій таблиці зберігаються адреси реалізацій усіх віртуальних методів класу. Коли створюється об'єкт, він отримує посилання на VMT свого реального класу.

При виклику `p.Print()`:
1. Середовище виконання бере посилання на VMT з об'єкта — це VMT класу `Doctor`
2. У VMT `Doctor` знаходить адресу `Doctor.Print()`
3. Виконує `Doctor.Print()`

Саме тому тип змінної не має значення — вирішує VMT об'єкта. Варто врахувати, що через необхідність звернення до VMT виклик віртуального методу є трохи повільнішим порівняно зі звичайним. Проте у переважній більшості задач ця різниця непомітна.

## Приховування: раннє зв'язування

При приховуванні через `new` рішення приймається **під час компіляції** на основі типу змінної. Це **раннє зв'язування** (early binding або static dispatch). Похідний клас не замінює метод у VMT — він просто визначає новий метод, який існує паралельно:

```csharp run
using System;

Person p = new Doctor("Олена Коваль", 38, "Кардіологія");
p.Print(); // Person.Print() — тип змінної вирішує!

Doctor d = new Doctor("Олена Коваль", 38, "Кардіологія");
d.Print(); // Doctor.Print() — тип змінної Doctor

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }

    public void Print()   // не virtual
    {
        Console.WriteLine($"Person.Print: {Name}");
    }
}

class Doctor : Person
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age) { Specialization = spec; }

    public new void Print()
    {
        Console.WriteLine($"Doctor.Print: {Name} | {Specialization}");
    }
}
```

Той самий об'єкт `Doctor` — але залежно від типу змінної викликається різна реалізація. Через `Person p` — `Person.Print()`, через `Doctor d` — `Doctor.Print()`. Компілятор прив'язує виклик до методу ще при компіляції, дивлячись лише на тип змінної.

## Порівняння на одному прикладі

Щоб побачити різницю повністю, розглянемо масив `Person[]`, де зберігаються різні об'єкти:

```csharp run
using System;

Person[] staff = {
    new Person("Адміністратор", 30),
    new Doctor("Олена Коваль", 38, "Кардіологія"),
    new Patient("Іван Петренко", 45, "Гіпертонія"),
};

Console.WriteLine("=== override (virtual) ===");
foreach (Person p in staff)
    p.Print(); // кожен виконує свою реалізацію

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }
    public virtual void Print() => Console.WriteLine($"Person: {Name}");
}

class Doctor : Person
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age) { Specialization = spec; }
    public override void Print() => Console.WriteLine($"Doctor: {Name} | {Specialization}");
}

class Patient : Person
{
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diag) : base(name, age) { Diagnosis = diag; }
    public override void Print() => Console.WriteLine($"Patient: {Name} | {Diagnosis}");
}
```

Якби замість `override` використовувалось `new` — всі три виклики у циклі виводили б `Person.Print()`, оскільки змінна циклу `p` має тип `Person`.

![VMT та статична прив'язка — як вирішується виклик методу](_assets/04-05/vmt-vs-static.png)

## Підсумок

| | `override` (перевизначення) | `new` (приховування) |
|---|---|---|
| Зв'язування | Пізнє (runtime) | Раннє (compile time) |
| Визначає виклик | Реальний тип об'єкта | Тип змінної |
| Поведінка | Поліморфна | Залежить від змінної |
| Потребує | `virtual` у базовому | Будь-який метод |
| VMT | Замінює запис | Не змінює VMT |

Загальне правило: якщо потрібна поліморфна поведінка — `virtual` + `override`. Якщо потрібно локально перевизначити невіртуальний метод без поліморфізму — `new`. Змішування цих підходів без чіткого розуміння є одним із найпоширеніших джерел прихованих помилок у C#.
