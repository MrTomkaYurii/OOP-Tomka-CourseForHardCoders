---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 4
number: "4.4"
title: "Приховування методів та властивостей"
source: "../_combined/21-prykhovuvannia-metodiv-ta-vlastyvostei.md"
---

## 4.4. Приховування методів та властивостей

У попередньому розділі ми розглянули перевизначення — механізм заміни реалізації віртуального методу в похідному класі. Проте іноді виникає ситуація, коли метод у базовому класі не є `virtual`, а отже не може бути перевизначений. Або ж нас влаштовує поточна реалізація для базового типу, але в похідному класі потрібна інша поведінка. У таких випадках застосовується **приховування** (hiding / shadowing).

Приховування полягає у визначенні в похідному класі члена з тим самим іменем і набором параметрів, що й у базовому класі. Для явного позначення приховування використовується ключове слово `new`. Якщо `new` не вказати — компілятор видасть попередження, але код скомпілюється.

## Приховування методів

Розглянемо базовий клас `Person` із звичайним (не `virtual`) методом `Print()`. Клас `Doctor` хоче вивести у `Print()` додаткову інформацію про спеціалізацію, але перевизначити невіртуальний метод неможливо — тому використовується `new`:

```csharp run
using System;

Person person = new Person("Сергій Бойко", 52);
person.Print();   // Person.Print()

Doctor doctor = new Doctor("Олена Коваль", 38, "Кардіологія");
doctor.Print();   // Doctor.Print() — прихований метод

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }

    public Person(string name, int age) { Name = name; Age = age; }

    public void Print()   // НЕ virtual
    {
        Console.WriteLine($"Особа: {Name}, {Age} р.");
    }
}

class Doctor : Person
{
    public string Specialization { get; set; }

    public Doctor(string name, int age, string spec) : base(name, age)
    {
        Specialization = spec;
    }

    public new void Print()   // приховуємо метод базового класу
    {
        Console.WriteLine($"Лікар: {Name}, {Age} р. | {Specialization}");
    }
}
```

Ключове слово `new` сигналізує компілятору та читачу коду: «це навмисне приховування, а не помилка». Без `new` код працює так само, але компілятор виведе попередження CS0108.

## Виклик базового методу через base

Якщо у прихованому методі потрібно скористатися реалізацією базового класу, можна звернутися до неї через `base`:

```csharp run
using System;

Doctor doctor = new Doctor("Олена Коваль", 38, "Кардіологія");
doctor.Print();

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }

    public void Print()
    {
        Console.WriteLine($"Особа: {Name}, {Age} р.");
    }
}

class Doctor : Person
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age) { Specialization = spec; }

    public new void Print()
    {
        base.Print();                                        // Особа: Олена Коваль, 38 р.
        Console.WriteLine($"  Спеціалізація: {Specialization}");
    }
}
```

## Ключова відмінність від override

Приховування і перевизначення виглядають схоже, але поводяться принципово по-різному. Якщо об'єкт `Doctor` зберігається у змінній типу `Person`, то:
- при **перевизначенні** (`override`) — виконається `Doctor.Print()`
- при **приховуванні** (`new`) — виконається `Person.Print()`

```csharp run
using System;

// Змінна типу Person, об'єкт Doctor
Person p = new Doctor("Олена Коваль", 38, "Кардіологія");
p.Print(); // яка реалізація?

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }

    public void Print()   // не virtual — hiding
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

Результат: **`Person.Print: Олена Коваль`** — виконується метод класу `Person`, хоча реальний об'єкт є `Doctor`. Саме тому для поліморфної поведінки потрібен `override`, а не `new`.

![new (приховування) vs override (перевизначення) — поведінка через змінну базового типу](_assets/04-04/hiding-vs-override.png)

## Приховування властивостей

Так само як і методи, можна приховувати властивості. Це корисно, коли потрібно змінити логіку доступу у похідному класі без оголошення `virtual` у базовому:

```csharp run
using System;

Person person = new Person("Іван Петренко");
Console.WriteLine(person.Name); // Іван Петренко

Patient patient = new Patient("Марія Сидоренко", "MR-001");
Console.WriteLine(patient.Name); // [MR-001] Марія Сидоренко

class Person
{
    public string Name { get; set; }
    public Person(string name) { Name = name; }
}

class Patient : Person
{
    public string RecordId { get; set; }

    public Patient(string name, string recordId) : base(name)
    {
        RecordId = recordId;
    }

    // приховуємо властивість Name — додаємо номер картки пацієнта
    public new string Name
    {
        get => $"[{RecordId}] {base.Name}";
        set => base.Name = value;
    }
}
```

У блоці `get` звертаємось до `base.Name`, щоб отримати оригінальне ім'я і доповнити його. У блоці `set` передаємо значення безпосередньо властивості базового класу.

## Приховування полів і констант

На відміну від `override`, `new` можна застосовувати не тільки до методів і властивостей, але й до **полів** та **констант**. Це дозволяє перевизначати статичні метадані класу в ієрархії:

```csharp run
using System;

Console.WriteLine(Person.MinAge.ToString());   // 0
Console.WriteLine(Person.TypeLabel);           // Особа

Console.WriteLine(Patient.MinAge.ToString());  // 0
Console.WriteLine(Patient.TypeLabel);          // Пацієнт

Console.WriteLine(Doctor.MinAge.ToString());   // 25
Console.WriteLine(Doctor.TypeLabel);           // Лікар

class Person
{
    public static readonly int MinAge = 0;
    public const string TypeLabel = "Особа";
}

class Patient : Person
{
    public new const string TypeLabel = "Пацієнт";
    // MinAge не приховується — успадковується зі значенням 0
}

class Doctor : Person
{
    public new static readonly int MinAge = 25;
    public new const string TypeLabel = "Лікар";
}
```

Кожен клас має свою версію констант і полів, незалежну від базового класу. Звернення через тип (`Doctor.MinAge`) повертає значення саме того класу, через який звертаємось.

## Коли використовувати new замість override

Приховування є вузькоспеціалізованим інструментом. Типові сценарії:

- **Метод базового класу не є `virtual`** — якщо немає доступу до вихідного коду або змінювати базовий клас небажано.
- **Навмисна ізоляція поведінки** — потрібна різна реалізація залежно від типу змінної (не об'єкта), що є рідкісною але законною архітектурною потребою.
- **Статичні поля та константи** — єдиний спосіб «замінити» статичний член у похідному класі.

В усіх інших випадках, де потрібна поліморфна поведінка, слід надавати перевагу `virtual` + `override`. Приховування через `new` без чіткого розуміння наслідків є поширеним джерелом помилок.
