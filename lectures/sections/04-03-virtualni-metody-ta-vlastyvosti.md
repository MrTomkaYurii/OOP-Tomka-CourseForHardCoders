---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 3
number: "4.3"
title: "Віртуальні методи та властивості"
source: "../_combined/20-virtualni-metody-ta-vlastyvosti.md"
---

## 4.3. Віртуальні методи та властивості

При успадкуванні нерідко виникає необхідність змінити в похідному класі поведінку методу, успадкованого від базового. Стандартний метод неможливо перевизначити у нащадку — для цього базовий клас має явно **дозволити** перевизначення за допомогою ключового слова `virtual`. Такі методи та властивості називаються **віртуальними**.

У похідному класі метод, що замінює реалізацію базового, позначається ключовим словом `override`. Сигнатура перевизначеного методу — ім'я та параметри — повинна точно збігатися з сигнатурою базового віртуального методу.

## Оголошення virtual та override

Розглянемо клінічну ієрархію: базовий клас `Person` з віртуальним методом `Print()`, та похідні класи `Patient` і `Doctor`, кожен з яких перевизначає цей метод по-своєму:

```csharp run
using System;

Person p  = new Person("Сергій Бойко", 52);
Patient pt = new Patient("Іван Петренко", 45, "Гіпертонія");
Doctor  dr = new Doctor("Олена Коваль", 38, "Кардіологія");

p.Print();   // Person.Print()
pt.Print();  // Patient.Print() — перевизначений
dr.Print();  // Doctor.Print()  — перевизначений

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }

    public Person(string name, int age) { Name = name; Age = age; }

    public virtual void Print()
    {
        Console.WriteLine($"Особа: {Name}, {Age} р.");
    }
}

class Patient : Person
{
    public string Diagnosis { get; set; }

    public Patient(string name, int age, string diagnosis) : base(name, age)
    {
        Diagnosis = diagnosis;
    }

    public override void Print()
    {
        Console.WriteLine($"Пацієнт: {Name}, {Age} р. | Діагноз: {Diagnosis}");
    }
}

class Doctor : Person
{
    public string Specialization { get; set; }

    public Doctor(string name, int age, string spec) : base(name, age)
    {
        Specialization = spec;
    }

    public override void Print()
    {
        Console.WriteLine($"Лікар: {Name}, {Age} р. | {Specialization}");
    }
}
```

Якщо похідний клас не перевизначає віртуальний метод — використовується реалізація базового класу. Тобто `virtual` лише **дозволяє** перевизначення, але не зобов'язує до нього.

При перевизначенні слід враховувати кілька обмежень:

- Модифікатор доступу перевизначеного методу повинен **збігатися** з модифікатором базового (`public virtual` → `public override`).
- Неможливо оголосити `virtual` або перевизначити `static`-метод.
- Неможливо перевизначити метод без `virtual` у базовому класі (для цього є приховування, яке розглядається в розділі 4.4).

## Поліморфізм: виклик за реальним типом об'єкта

Справжня сила віртуальних методів розкривається через **поліморфізм** — здатність коду однаково звертатись до об'єктів різних типів через змінну базового класу, але при цьому кожен об'єкт виконує свою власну реалізацію методу.

Коли через змінну типу `Person` викликається метод `Print()`, середовище виконання визначає **реальний тип об'єкта** під час виконання програми і викликає відповідну реалізацію — `Patient.Print()` для пацієнта, `Doctor.Print()` для лікаря:

```csharp run
using System;

Person[] staff = {
    new Person("Адміністратор", 30),
    new Patient("Іван Петренко", 45, "Гіпертонія"),
    new Doctor("Олена Коваль", 38, "Кардіологія"),
    new Patient("Марія Сидоренко", 32, "Бронхіт"),
};

foreach (Person p in staff)
{
    p.Print(); // кожен об'єкт виконує свою реалізацію
}

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }
    public virtual void Print() =>
        Console.WriteLine($"Особа: {Name}");
}

class Patient : Person
{
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diag) : base(name, age) { Diagnosis = diag; }
    public override void Print() =>
        Console.WriteLine($"Пацієнт: {Name} | {Diagnosis}");
}

class Doctor : Person
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age) { Specialization = spec; }
    public override void Print() =>
        Console.WriteLine($"Лікар: {Name} | {Specialization}");
}
```

Масив оголошено як `Person[]`, але кожен елемент зберігає об'єкт свого реального типу. Під час виклику `p.Print()` C# не дивиться на тип змінної — він шукає реалізацію методу у фактичному типі об'єкта. Цей механізм називається **пізнім зв'язуванням** (late binding або dynamic dispatch).

![Virtual dispatch — виклик методу за реальним типом об'єкта](_assets/04-03/virtual-dispatch.png)

Поліморфізм є фундаментальним принципом ООП: він дозволяє писати код, який працює з абстракцією (`Person`), не знаючи конкретних типів — і при цьому кожен об'єкт поводиться відповідно до своєї природи.

## Звернення до базового методу через base

Перевизначений метод у похідному класі може викликати реалізацію базового класу через ключове слово `base`. Це дозволяє **розширити** поведінку, а не повністю замінити її:

```csharp run
using System;

Doctor doctor = new Doctor("Олена Коваль", 38, "Кардіологія");
doctor.Print();

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }

    public virtual void Print()
    {
        Console.WriteLine($"{Name}, {Age} р.");
    }
}

class Doctor : Person
{
    public string Specialization { get; set; }

    public Doctor(string name, int age, string spec) : base(name, age)
    {
        Specialization = spec;
    }

    public override void Print()
    {
        base.Print();                                    // виводить: Олена Коваль, 38 р.
        Console.WriteLine($"  Спеціалізація: {Specialization}"); // додає рядок
    }
}
```

Виклик `base.Print()` запускає саме реалізацію класу `Person`, навіть якщо викликається через об'єкт `Doctor`. Це типовий патерн для поступового збагачення поведінки в ланцюжку успадкування.

## Ланцюжок перевизначень

Перевизначення може тривати через кілька рівнів ієрархії. Кожен похідний клас може перевизначити метод далі — або знову використати `base`:

```csharp run
using System;

Person p   = new Inpatient("Іван Петренко", 45, "Гіпертонія", "Палата 12");
p.Print();

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }
    public virtual void Print() => Console.WriteLine($"Особа: {Name}");
}

class Patient : Person
{
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diag) : base(name, age) { Diagnosis = diag; }

    public override void Print()
    {
        base.Print();
        Console.WriteLine($"  Діагноз: {Diagnosis}");
    }
}

class Inpatient : Patient  // стаціонарний пацієнт
{
    public string Room { get; set; }
    public Inpatient(string name, int age, string diag, string room)
        : base(name, age, diag) { Room = room; }

    public override void Print()
    {
        base.Print();                          // викликає Patient.Print() → Person.Print()
        Console.WriteLine($"  Палата: {Room}");
    }
}
```

![Ланцюжок перевизначень virtual → override](_assets/04-03/override-chain.png)

При виклику `p.Print()` через змінну типу `Person`, де реальний тип `Inpatient`, спочатку виконується `Inpatient.Print()`, яка через `base.Print()` викликає `Patient.Print()`, яка у свою чергу через `base.Print()` викликає `Person.Print()`.

## Перевизначення властивостей

Так само як і методи, властивості можна оголошувати `virtual` і перевизначати в нащадках за допомогою `override`. Це корисно, коли похідний клас має накладати додаткові обмеження або змінювати логіку доступу:

```csharp run
using System;

Person person = new Person("Сергій Бойко");
person.Age = 5;
Console.WriteLine($"Person.Age = {person.Age.ToString()}");   // 5

Doctor doctor = new Doctor("Олена Коваль", "Кардіологія");
doctor.Age = 16;
Console.WriteLine($"Doctor.Age = {doctor.Age.ToString()}");   // 18 (мін. для лікаря)
doctor.Age = 35;
Console.WriteLine($"Doctor.Age = {doctor.Age.ToString()}");   // 35

class Person
{
    private int _age = 1;

    public virtual int Age
    {
        get => _age;
        set { if (value > 0 && value < 120) _age = value; }
    }

    public string Name { get; set; }
    public Person(string name) { Name = name; }
}

class Doctor : Person
{
    public string Specialization { get; set; }

    public Doctor(string name, string spec) : base(name)
    {
        Specialization = spec;
        base.Age = 25; // вік за замовчуванням для лікаря
    }

    public override int Age
    {
        get => base.Age;
        set
        {
            // Лікар повинен мати не менше 25 років (мінімум для спеціаліста)
            if (value >= 25 && value < 120) base.Age = value;
        }
    }
}
```

У класі `Person` властивість `Age` перевіряє лише загальний діапазон (1..119). У класі `Doctor` перевизначена властивість додає вимогу мінімального віку 25 років. При встановленні значення менше допустимого воно просто ігнорується.

## Заборона подальшого перевизначення: sealed

Якщо перевизначений метод у похідному класі не повинен перевизначатися у його нащадках, його оголошують з модифікатором `sealed`. Цей модифікатор завжди використовується разом з `override`:

```csharp run
using System;

ChiefDoctor chief = new ChiefDoctor("Андрій Мельник", "Хірургія", "Клінічна лікарня №1");
chief.Print();

// Якби існував клас SeniorChiefDoctor : ChiefDoctor,
// він не зміг би перевизначити Print() — компілятор видасть помилку.

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name) { Name = name; }
    public virtual void Print() => Console.WriteLine($"Особа: {Name}");
}

class Doctor : Person
{
    public string Specialization { get; set; }
    public Doctor(string name, string spec) : base(name) { Specialization = spec; }

    public override void Print() =>
        Console.WriteLine($"Лікар: {Name} | {Specialization}");
}

class ChiefDoctor : Doctor
{
    public string Hospital { get; set; }

    public ChiefDoctor(string name, string spec, string hospital)
        : base(name, spec) { Hospital = hospital; }

    public override sealed void Print()  // sealed: подальше перевизначення заборонено
    {
        base.Print();
        Console.WriteLine($"  Головний лікар: {Hospital}");
    }
}
```

`sealed override` означає: «я перевизначаю метод базового класу, але забороняю будь-якому нащадку перевизначати його далі». Це корисно, коли реалізація є критичною і не повинна бути змінена у підкласах — наприклад, метод, що реалізує специфічну логіку ліцензування або безпеки.
