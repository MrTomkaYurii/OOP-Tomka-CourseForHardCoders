---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 6
number: "4.6"
title: "Абстрактні класи та члени класів"
source: "../_combined/23-abstraktni-klasy-ta-chleny-klasiv.md"
---

## 4.6. Абстрактні класи та члени класів

## Навіщо потрібні абстрактні класи

Класи зазвичай представляють конкретні сутності, з яких можна створювати об'єкти: `Patient`, `Doctor`, `Appointment`. Але іноді корисно мати клас, який описує загальний шаблон або контракт для цілої групи класів, і при цьому самостійно не має сенсу як окремий об'єкт.

Наприклад, «медичний персонал» — це абстракція. У клініці є конкретні лікарі, медсестри, хірурги, але «медичного персоналу взагалі» як конкретної людини не існує. Проте всі вони мають спільне: ім'я, роль, спосіб виконання своїх обов'язків. Для опису таких сутностей у C# призначені **абстрактні класи**.

Абстрактний клас оголошується з ключовим словом `abstract`. Його головна особливість: **неможливо створити екземпляр абстрактного класу безпосередньо**. Він існує лише як база для похідних класів.

## Абстрактний клас з конкретними методами

Абстрактний клас може мати звичайні поля, властивості, конструктори та методи — і похідні класи успадкують їх без необхідності перевизначення:

```csharp run
using System;

MedicalStaff doctor = new Doctor("Олена Коваль", 38, "Кардіологія");
MedicalStaff nurse  = new Nurse("Тетяна Мороз", 29, "Терапія");

doctor.PrintCard();
nurse.PrintCard();

// new MedicalStaff("...", 0); // Помилка — абстрактний клас!

abstract class MedicalStaff
{
    public string Name { get; set; }
    public int Age { get; set; }

    public MedicalStaff(string name, int age)
    {
        Name = name;
        Age  = age;
    }

    // Звичайний метод — успадковується всіма похідними
    public void PrintCard()
    {
        Console.WriteLine($"Співробітник: {Name}, {Age} р.");
    }
}

class Doctor : MedicalStaff
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age)
    { Specialization = spec; }
}

class Nurse : MedicalStaff
{
    public string Ward { get; set; }
    public Nurse(string name, int age, string ward) : base(name, age)
    { Ward = ward; }
}
```

Хоча `MedicalStaff` абстрактний, він може мати конструктор — але він викликається лише через `base(...)` у похідних класах. Звернення `new MedicalStaff(...)` безпосередньо заборонено компілятором.

## Абстрактні методи

Абстрактний клас може визначати **абстрактні методи** — методи без реалізації, позначені ключовим словом `abstract`. Вони задають **контракт**: кожен неабстрактний похідний клас зобов'язаний реалізувати такий метод через `override`. Абстрактний метод не може мати тіла — лише сигнатуру:

```csharp run
using System;

MedicalStaff[] staff = {
    new Doctor("Олена Коваль", 38, "Кардіологія"),
    new Nurse("Тетяна Мороз", 29, "Терапія"),
};

foreach (MedicalStaff m in staff)
{
    m.PrintCard();
    m.Examine();   // кожен виконує по-своєму
    Console.WriteLine();
}

abstract class MedicalStaff
{
    public string Name { get; set; }
    public int Age { get; set; }

    public MedicalStaff(string name, int age) { Name = name; Age = age; }

    public void PrintCard() =>
        Console.WriteLine($"Співробітник: {Name}, {Age} р.");

    // Абстрактний метод — реалізація обов'язкова у похідних
    public abstract void Examine();
}

class Doctor : MedicalStaff
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age)
    { Specialization = spec; }

    public override void Examine()
    {
        Console.WriteLine($"Лікар {Name} проводить огляд за спеціалізацією: {Specialization}");
    }
}

class Nurse : MedicalStaff
{
    public string Ward { get; set; }
    public Nurse(string name, int age, string ward) : base(name, age)
    { Ward = ward; }

    public override void Examine()
    {
        Console.WriteLine($"Медсестра {Name} вимірює показники у палаті: {Ward}");
    }
}
```

![Ієрархія абстрактного класу MedicalStaff](_assets/04-06/abstract-hierarchy.png)

Абстрактні методи є частиною поліморфного інтерфейсу: виклик `m.Examine()` через змінну `MedicalStaff` завжди виконає реалізацію реального типу — так само, як і `virtual` + `override`. Різниця в тому, що `abstract` **не має реалізації за замовчуванням** і похідний клас **не може** відмовитись від реалізації (якщо сам не є абстрактним).

## Абстрактні властивості

Крім методів, абстрактними можуть бути й **властивості**. Їх оголошення схоже на автовластивість, але без реального тіла — лише порожні блоки `get` та `set`:

```csharp run
using System;

MedicalStaff[] staff = {
    new Doctor("Олена Коваль", 38, "Кардіологія"),
    new Nurse("Тетяна Мороз", 29, "Терапія"),
};

foreach (MedicalStaff m in staff)
    Console.WriteLine($"{m.Name} — {m.Role}, ставка: {m.HourlyRate.ToString()} грн/год");

abstract class MedicalStaff
{
    public string Name { get; set; }
    public int Age { get; set; }

    public MedicalStaff(string name, int age) { Name = name; Age = age; }

    public abstract string Role { get; }           // абстрактна властивість
    public abstract decimal HourlyRate { get; }    // абстрактна властивість
}

class Doctor : MedicalStaff
{
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec) : base(name, age)
    { Specialization = spec; }

    public override string Role => "Лікар";
    public override decimal HourlyRate => 250m;
}

class Nurse : MedicalStaff
{
    public string Ward { get; set; }
    public Nurse(string name, int age, string ward) : base(name, age)
    { Ward = ward; }

    public override string Role => "Медсестра";
    public override decimal HourlyRate => 120m;
}
```

При перевизначенні абстрактної властивості у похідному класі її можна реалізувати як повноцінну властивість з полем або як автовластивість — залежно від потреб. У прикладі вище використані вирази-тіла (`=>`), що повертають константу.

## Відмова від реалізації в проміжному класі

Якщо похідний клас не бажає або не може реалізувати всі абстрактні члени базового — він сам повинен бути оголошений як `abstract`. У такому разі обов'язок реалізації переходить до його нащадків:

```csharp run
using System;

MedicalStaff surgeon = new CardiacSurgeon("Андрій Мельник", 45);
surgeon.PrintCard();
surgeon.Examine();

abstract class MedicalStaff
{
    public string Name { get; set; }
    public int Age { get; set; }
    public MedicalStaff(string name, int age) { Name = name; Age = age; }
    public void PrintCard() => Console.WriteLine($"{Name}, {Age} р.");
    public abstract void Examine();
    public abstract string Role { get; }
}

// Хірург — ще абстрактний: не реалізує Examine() і Role
abstract class Surgeon : MedicalStaff
{
    public string SurgeryType { get; set; }
    public Surgeon(string name, int age, string surgeryType) : base(name, age)
    { SurgeryType = surgeryType; }
    // Examine() та Role — досі не реалізовані
}

// Конкретний клас — зобов'язаний реалізувати все
class CardiacSurgeon : Surgeon
{
    public CardiacSurgeon(string name, int age)
        : base(name, age, "Кардіохірургія") { }

    public override string Role => "Кардіохірург";

    public override void Examine()
    {
        Console.WriteLine($"{Name} проводить передопераційний огляд ({SurgeryType})");
    }
}
```

Клас `Surgeon` є проміжним абстрактним класом: він додає власну властивість `SurgeryType`, але не реалізує `Examine()` та `Role`. Клас `CardiacSurgeon` вже конкретний — і зобов'язаний реалізувати всі успадковані абстрактні члени.

## abstract vs virtual: коли що обирати

| | `abstract` | `virtual` |
|---|---|---|
| Реалізація у базовому | Відсутня | Є (за замовчуванням) |
| Похідний зобов'язаний | Так (або бути abstract) | Ні (може не перевизначати) |
| Клас має бути abstract | Так | Ні |
| Поліморфізм | Так | Так |

Правило вибору: якщо у базовому класі немає і не може бути розумної реалізації за замовчуванням — використовуйте `abstract`. Якщо базова реалізація має сенс, але похідні можуть її уточнити — використовуйте `virtual`.
