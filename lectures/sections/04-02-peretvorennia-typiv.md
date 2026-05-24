---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 2
number: "4.2"
title: "Перетворення типів"
source: "../_combined/19-peretvorennia-typiv.md"
---

## 4.2. Перетворення типів

У попередньому розділі ми говорили про успадкування та відношення is-a між класами. З цим відношенням безпосередньо пов'язана можливість **перетворення типів** у ієрархії класів: об'єкт похідного класу в будь-який момент може бути представлений як об'єкт базового класу, і навпаки — за певних умов. Розуміння правил таких перетворень є обов'язковим для написання гнучкого коду, що працює з ієрархіями об'єктів.

Розглянемо клінічну ієрархію класів:

```csharp
class Person
{
    public string Name { get; set; }
    public int Age { get; set; }

    public Person(string name, int age)
    {
        Name = name;
        Age  = age;
    }

    public void Print()
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
}

class Doctor : Person
{
    public string Specialization { get; set; }

    public Doctor(string name, int age, string specialization) : base(name, age)
    {
        Specialization = specialization;
    }
}
```

Ланцюг успадкування: `Object` (неявно) → `Person` → `Patient | Doctor`. Базові типи знаходяться вгорі ієрархії, похідні — внизу.

![Ієрархія типів у клінічній системі](_assets/04-02/type-hierarchy.png)

## Висхідні перетворення. Upcasting

Об'єкт похідного типу одночасно є об'єктом базового типу. Пацієнт (`Patient`) — це людина (`Person`), тому посилання на `Patient` можна зберегти у змінній типу `Person`. Таке перетворення від похідного до базового типу називається **висхідним** (upcasting) і відбувається **неявно** — без жодного додаткового синтаксису:

```csharp run
using System;

Patient patient = new Patient("Іван Петренко", 45, "Гіпертонія");
Person  person  = patient;   // upcasting: Patient → Person (неявно)

person.Print();              // Особа: Іван Петренко, 45 р.
Console.WriteLine(person.Name); // Іван Петренко

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }
    public void Print() => Console.WriteLine($"Особа: {Name}, {Age} р.");
}

class Patient : Person
{
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diag) : base(name, age)
    { Diagnosis = diag; }
}
```

Змінні `patient` і `person` вказують на **один і той самий об'єкт** у пам'яті. Але через змінну `person` доступна лише та частина функціоналу, яку визначає тип `Person` — властивість `Diagnosis` буде недоступна.

Висхідне перетворення відбувається і під час присвоєння до типу `object`, оскільки він є базовим для всіх:

```csharp run
using System;

object obj1 = new Patient("Іван Петренко", 45, "Гіпертонія"); // Patient → object
object obj2 = new Doctor("Олена Коваль", 38, "Кардіологія");  // Doctor → object
object obj3 = new Person("Сергій Бойко", 52);                 // Person → object

Console.WriteLine(obj1.GetType().Name); // Patient
Console.WriteLine(obj2.GetType().Name); // Doctor
Console.WriteLine(obj3.GetType().Name); // Person

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }
}
class Patient : Person
{
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diag) : base(name, age) { Diagnosis = diag; }
}
class Doctor : Person
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age) { Specialization = spec; }
}
```

Зверніть увагу: метод `GetType()` завжди повертає **реальний тип об'єкта**, незалежно від типу змінної, що його зберігає.

![Upcasting та Downcasting у ієрархії класів](_assets/04-02/upcasting-downcasting.png)

## Низхідні перетворення. Downcasting

Якщо upcasting — це завжди безпечно і неявно, то зворотна операція — **низхідне перетворення** (downcasting) від базового до похідного типу — вимагає **явного вказання типу** і несе в собі ризик. Не кожна людина є пацієнтом, тому компілятор не може самостійно вирішити, чи допустиме таке перетворення:

```csharp run
using System;

Patient patient1 = new Patient("Іван Петренко", 45, "Гіпертонія");
Person  person   = patient1;              // upcasting (неявне)

Patient patient2 = (Patient)person;       // downcasting (явне)
Console.WriteLine(patient2.Diagnosis);    // Гіпертонія

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }
}
class Patient : Person
{
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diag) : base(name, age) { Diagnosis = diag; }
}
```

Якщо ж реальний тип об'єкта не відповідає типу, до якого відбувається приведення, виникає виняток `InvalidCastException` під час виконання програми:

```csharp run
using System;

try
{
    Person person = new Person("Сергій Бойко", 52); // звичайна Person, не Patient
    Patient patient = (Patient)person;               // InvalidCastException!
    Console.WriteLine(patient.Diagnosis);
}
catch (InvalidCastException ex)
{
    Console.WriteLine($"Помилка перетворення: {ex.Message}");
}

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }
}
class Patient : Person
{
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diag) : base(name, age) { Diagnosis = diag; }
}
```

Підступність у тому, що компілятор не завжди може виявити некоректне перетворення — код скомпілюється, але впаде під час виконання. Тому для downcasting завжди потрібна додаткова перевірка.

## Оператор as

Оператор `as` намагається виконати перетворення і у разі невдачі повертає `null` замість викидання винятку. Це безпечна альтернатива явному приведенню:

```csharp run
using System;

Person person1 = new Patient("Іван Петренко", 45, "Гіпертонія");
Person person2 = new Doctor("Олена Коваль", 38, "Кардіологія");

Patient? p = person1 as Patient;
Doctor?  d = person1 as Doctor;

if (p != null)
    Console.WriteLine($"Пацієнт: {p.Diagnosis}");  // Гіпертонія
else
    Console.WriteLine("Не є пацієнтом");

if (d != null)
    Console.WriteLine($"Лікар: {d.Specialization}");
else
    Console.WriteLine("Не є лікарем");              // Не є лікарем

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }
}
class Patient : Person
{
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diag) : base(name, age) { Diagnosis = diag; }
}
class Doctor : Person
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age) { Specialization = spec; }
}
```

Тип результату після `as` завжди nullable (`Patient?`, `Doctor?`) — тобто може містити або об'єкт, або `null`. Перевірка на `null` перед використанням є обов'язковою.

## Оператор is

Оператор `is` перевіряє, чи є об'єкт представником певного типу, і повертає `true` або `false`. Починаючи з C# 7, він підтримує **перевірку з одночасним перетворенням** (pattern matching): якщо перевірка успішна, об'єкт автоматично приводиться до потрібного типу і зберігається у нову змінну:

```csharp run
using System;

Person person = new Patient("Марія Сидоренко", 32, "Бронхіт");

if (person is Patient patient)
{
    // patient вже є типом Patient — не потрібне явне приведення
    Console.WriteLine($"Пацієнт: {patient.Name}, діагноз: {patient.Diagnosis}");
}
else
{
    Console.WriteLine("Не є пацієнтом");
}

// Без захоплення змінної — просто перевірка
if (person is Doctor)
    Console.WriteLine("Це лікар");
else
    Console.WriteLine("Це не лікар"); // виведе це

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }
}
class Patient : Person
{
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diag) : base(name, age) { Diagnosis = diag; }
}
class Doctor : Person
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age) { Specialization = spec; }
}
```

Вираз `person is Patient patient` робить одразу дві речі: перевіряє тип і, якщо він відповідає, зберігає вже приведений об'єкт у змінну `patient`. Це лаконічніше і безпечніше, ніж окрема перевірка + явне приведення.

## Pattern matching з switch

Починаючи з C# 8, оператор `switch` підтримує pattern matching по типах. Це зручно, коли потрібно обробити кілька різних типів з однієї ієрархії:

```csharp run
using System;

Person[] staff = {
    new Patient("Іван Петренко", 45, "Гіпертонія"),
    new Doctor("Олена Коваль", 38, "Кардіологія"),
    new Person("Адміністратор", 30),
};

foreach (Person p in staff)
{
    string info = p switch
    {
        Patient pat => $"[Пацієнт] {pat.Name} — {pat.Diagnosis}",
        Doctor  doc => $"[Лікар]   {doc.Name} — {doc.Specialization}",
        Person  per => $"[Особа]   {per.Name}",
    };
    Console.WriteLine(info);
}

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }
}
class Patient : Person
{
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diag) : base(name, age) { Diagnosis = diag; }
}
class Doctor : Person
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age) { Specialization = spec; }
}
```

Важливий нюанс: гілки `switch` перевіряються **зверху донизу**, тому більш специфічні типи (`Patient`, `Doctor`) мають стояти **перед** більш загальним (`Person`). Якщо поставити `Person per` першим, він захопить усі об'єкти і до гілок `Patient` та `Doctor` справа не дійде.

Switch з pattern matching є найчистішим і найбезпечнішим способом роботи з поліморфними колекціями, оскільки компілятор перевіряє повноту гілок і видає попередження, якщо якийсь тип не оброблено.
