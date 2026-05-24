---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 1
number: "4.1"
title: "Успадкування"
source: "../_combined/18-uspadkuvannia.md"
---

## 4.1. Успадкування

Успадкування (inheritance) — один із трьох фундаментальних принципів об'єктно-орієнтованого програмування поряд із інкапсуляцією та поліморфізмом. Воно дозволяє одному класу перейняти функціональність іншого: поля, властивості та методи базового класу стають доступними в похідному без повторного написання коду. Це не просто зручність — це архітектурний інструмент для моделювання реальних відносин між сутностями.

Уявімо клінічну систему, де є різні типи людей: пацієнти, лікарі, адміністратори. Всі вони мають спільні атрибути (ім'я, вік) і спільні дії (ідентифікація, виведення інформації). Замість того, щоб дублювати цей код у кожному класі окремо, ми виносимо спільне в базовий клас `Person` і успадковуємо від нього.

## Базовий та похідний клас

Клас, від якого успадковують, називається **базовим класом** (base class, superclass, батьківський клас). Клас, який успадковує, — **похідним класом** (derived class, subclass, дочірній клас). Для позначення успадкування після назви похідного класу через двокрапку вказується базовий клас:

```csharp
class ПохіднийКлас : БазовийКлас
{
    // нові члени похідного класу
}
```

Нехай у нас є базовий клас `Person`:

```csharp
class Person
{
    public string Name { get; set; }
    public int Age { get; set; }

    public void Print()
    {
        Console.WriteLine($"{Name}, {Age} років");
    }
}
```

Тоді `Patient` і `Doctor` — похідні класи від `Person`:

```csharp run
using System;

Person p = new Person { Name = "Невідомий", Age = 0 };
p.Print();

Patient patient = new Patient { Name = "Іван Петренко", Age = 45, Diagnosis = "Гіпертонія" };
patient.Print();      // успадкований метод Print()
patient.PrintInfo();  // власний метод класу Patient

Doctor doctor = new Doctor { Name = "Олена Коваль", Age = 38, Specialization = "Кардіологія" };
doctor.Print();
doctor.PrintInfo();

class Person
{
    public string Name { get; set; } = "";
    public int Age { get; set; }

    public void Print()
    {
        Console.WriteLine($"{Name}, {Age} років");
    }
}

class Patient : Person
{
    public string Diagnosis { get; set; } = "";

    public void PrintInfo()
    {
        Console.WriteLine($"Пацієнт: {Name}, {Age} р. | Діагноз: {Diagnosis}");
    }
}

class Doctor : Person
{
    public string Specialization { get; set; } = "";

    public void PrintInfo()
    {
        Console.WriteLine($"Лікар: {Name}, {Age} р. | Спеціалізація: {Specialization}");
    }
}
```

Клас `Patient` успадкував від `Person` властивості `Name`, `Age` та метод `Print()` — і не потрібно було їх писати заново. Додатково `Patient` визначає власну властивість `Diagnosis` та метод `PrintInfo()`. Те саме для `Doctor`.

![Ієрархія успадкування: Person → Patient, Doctor](_assets/04-01/inheritance-hierarchy.png)

## Відношення is-a та has-a

Успадкування моделює відношення **is-a** («є»): об'єкт похідного класу є об'єктом базового класу. `Patient` is-a `Person` — пацієнт є людиною. Це означає, що там, де очікується `Person`, можна передати `Patient`:

```csharp run
using System;

Person p1 = new Patient { Name = "Іван Петренко", Age = 45, Diagnosis = "Гіпертонія" };
Person p2 = new Doctor  { Name = "Олена Коваль",  Age = 38, Specialization = "Кардіологія" };

p1.Print(); // метод Person.Print()
p2.Print(); // метод Person.Print()

class Person
{
    public string Name { get; set; } = "";
    public int Age { get; set; }
    public void Print() => Console.WriteLine($"{Name}, {Age} років");
}

class Patient : Person
{
    public string Diagnosis { get; set; } = "";
}

class Doctor : Person
{
    public string Specialization { get; set; } = "";
}
```

Змінна типу `Person` може зберігати будь-який об'єкт з ієрархії — це основа поліморфізму, який детально розглядається в наступних розділах.

Відношення is-a слід відрізняти від **has-a** («має»): якщо одна сутність містить іншу як компонент, використовується **композиція**, а не успадкування. Наприклад, клас `Appointment` (прийом) має `Patient` і `Doctor` — це has-a, тому `Appointment` не має від них успадковувати. Чіткий вибір між is-a і has-a є ознакою правильно спроектованої об'єктної моделі.

## Клас Object як базовий для всіх

За замовчуванням усі класи в C# неявно успадковують від базового класу `System.Object` (або просто `object`). Це означає, що навіть клас `Person`, для якого не вказано явного базового класу, насправді успадковує від `Object`. А `Patient` і `Doctor` перебувають у ланцюжку: `Patient → Person → Object`.

Саме тому будь-який об'єкт у C# завжди має такі методи:
- `ToString()` — рядкове представлення об'єкта
- `Equals(object obj)` — перевірка рівності
- `GetHashCode()` — хеш-код для колекцій
- `GetType()` — тип об'єкта під час виконання

```csharp run
using System;

Patient patient = new Patient { Name = "Іван Петренко", Age = 45 };

Console.WriteLine(patient.GetType().Name); // Patient
Console.WriteLine(patient.ToString());     // Patient (за замовчуванням — назва типу)

class Person
{
    public string Name { get; set; } = "";
    public int Age { get; set; }
}

class Patient : Person
{
    public string Diagnosis { get; set; } = "";
}
```

## Обмеження успадкування

C# накладає кілька важливих обмежень:

- **Одиночне успадкування** — клас може мати лише один безпосередній базовий клас. Множинне успадкування класів не підтримується (на відміну від інтерфейсів, які розглядаються в наступних розділах).
- **Рівні доступу** — якщо базовий клас має модифікатор `internal`, похідний клас може бути лише `internal` або `private`, але не `public`. Якщо класи в різних збірках, похідний клас може успадковувати лише від `public`-класу.
- **Статичний клас** — від статичного класу неможливо успадковувати.
- **Запечатаний клас** — клас з модифікатором `sealed` не допускає спадкоємців.

```csharp
sealed class AdministratorAccount
{
    // Від цього класу не можна успадковувати
}
```

Модифікатор `sealed` корисний там, де необхідно запобігти зміні поведінки класу через похідні класи — наприклад, для критичних класів безпеки або коли клас спроектований настільки специфічно, що розширення може порушити його коректність. У стандартній бібліотеці .NET клас `String` є `sealed` саме з міркувань безпеки та продуктивності.

## Доступ до членів базового класу

Похідний клас успадковує члени базового, але рівні доступу залишаються в силі. Розглянемо ситуацію, коли `Person` має приватне поле:

```csharp run
using System;

Doctor doctor = new Doctor { Age = 38, Specialization = "Кардіологія" };
doctor.SetName("Олена Коваль");
doctor.PrintInfo();

class Person
{
    private string _name = ""; // приватне поле — недоступне ззовні

    public string Name
    {
        get { return _name; }
        set { _name = value; }
    }

    public int Age { get; set; }

    public void Print() => Console.WriteLine($"{Name}, {Age} років");
}

class Doctor : Person
{
    public string Specialization { get; set; } = "";

    public void SetName(string name)
    {
        // _name = name; // Помилка! _name — private, доступний лише в Person
        Name = name;    // Правильно: через public-властивість
    }

    public void PrintInfo() => Console.WriteLine($"Лікар: {Name}, {Age} р. | {Specialization}");
}
```

Похідний клас може звертатися лише до членів базового класу з такими модифікаторами:
- `public` — доступний усюди
- `protected` — доступний у базовому та всіх похідних класах
- `internal` — доступний у межах однієї збірки
- `protected internal` — union: збірка або похідний клас
- `private protected` — intersection: та сама збірка і похідний клас

Члени з `private` залишаються виключно в тому класі, де оголошені.

## Модифікатор protected

Модифікатор `protected` створений спеціально для ієрархій успадкування. Він дозволяє базовому класу відкрити доступ до своїх членів для всіх похідних класів, але закрити їх від зовнішнього світу. Це золота середина між `public` (надто відкрито) і `private` (повністю закрито):

```csharp run
using System;

Patient patient = new Patient("Іван Петренко", 45, "Гіпертонія");
patient.PrintInfo();

// patient.medicalRecordId — помилка: protected
// patient._internalCode  — помилка: private

class Person
{
    private string _internalCode;          // тільки Person
    protected string medicalRecordId;      // Person та похідні

    public string Name { get; set; }
    public int Age { get; set; }

    public Person(string name, int age)
    {
        Name = name;
        Age  = age;
        _internalCode   = $"INT-{age}";
        medicalRecordId = $"MR-{name[0]}{age}";
    }
}

class Patient : Person
{
    public string Diagnosis { get; set; }

    public Patient(string name, int age, string diagnosis) : base(name, age)
    {
        Diagnosis = diagnosis;
    }

    public void PrintInfo()
    {
        // medicalRecordId доступний — він protected
        Console.WriteLine($"[{medicalRecordId}] Пацієнт: {Name}, {Age} р. | {Diagnosis}");
        // _internalCode — НЕ доступний
    }
}
```

Поле `medicalRecordId` оголошене як `protected`: клас `Patient` може його читати і використовувати, але зовнішній код (`patient.medicalRecordId`) отримає помилку компіляції. Поле `_internalCode` залишається `private` — недоступне навіть для `Patient`.

## Ключове слово base

Ключове слово `base` дозволяє явно звернутися до членів **безпосереднього** базового класу: викликати конструктор або метод. Це особливо важливо, коли похідний клас перевизначає метод базового і водночас хоче використати оригінальну реалізацію.

```csharp run
using System;

Doctor doctor = new Doctor("Олена Коваль", 38, "Кардіологія", "UA-12345");
doctor.Print();     // базовий метод
doctor.PrintInfo(); // розширений метод

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
        Console.WriteLine($"{Name}, {Age} років");
    }
}

class Doctor : Person
{
    public string Specialization { get; set; }
    public string LicenseNumber  { get; set; }

    public Doctor(string name, int age, string specialization, string licenseNumber)
        : base(name, age)       // викликаємо конструктор Person
    {
        Specialization = specialization;
        LicenseNumber  = licenseNumber;
    }

    public void PrintInfo()
    {
        base.Print();           // викликаємо метод Person.Print()
        Console.WriteLine($"  Спеціалізація: {Specialization} | Ліцензія: {LicenseNumber}");
    }
}
```

У конструкторі `Doctor` вираз `: base(name, age)` передає ім'я та вік конструктору `Person` — немає потреби дублювати код ініціалізації. У методі `PrintInfo()` виклик `base.Print()` виконує базову реалізацію, після чого виводить додаткову інформацію.

## Конструктори у похідних класах

Конструктори **не передаються** похідному класу при успадкуванні — це принципова відмінність від методів і властивостей. Кожен клас повинен мати власні конструктори.

Якщо в базовому класі є лише конструктори з параметрами (і немає конструктора без параметрів), то кожен конструктор похідного класу зобов'язаний явно викликати один із конструкторів базового через `base(...)`:

```csharp run
using System;

// Коректне визначення
Patient patient = new Patient("Марія Сидоренко", 32, "Бронхіт");
patient.PrintInfo();

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }

    // Є лише параметризований конструктор — без параметрів недоступний
    public Person(string name, int age)
    {
        Name = name;
        Age  = age;
    }
}

class Patient : Person
{
    public string Diagnosis { get; set; }

    // Обов'язково викликаємо base(name, age)
    public Patient(string name, int age, string diagnosis)
        : base(name, age)
    {
        Diagnosis = diagnosis;
    }

    public void PrintInfo() =>
        Console.WriteLine($"Пацієнт: {Name}, {Age} р. | Діагноз: {Diagnosis}");
}
```

Якщо `Patient` не викличе `base(name, age)`, компілятор видасть помилку — він не знає, як ініціалізувати успадковані властивості `Name` і `Age`.

Якщо ж базовий клас **має** конструктор без параметрів, похідний клас може не викликати `base()` явно — компілятор підставить його неявно. У такому разі наступні два конструктори еквівалентні:

```csharp
// Явний виклик
public Patient(string diagnosis) : base()
{
    Diagnosis = diagnosis;
}

// Неявний виклик (компілятор додасть base() автоматично)
public Patient(string diagnosis)
{
    Diagnosis = diagnosis;
}
```

## Порядок виклику конструкторів

При створенні об'єкта похідного класу конструктори викликаються в строго визначеному порядку: **від найбазовішого до найпохіднішого**. Тіла конструкторів виконуються у зворотному порядку відносно делегування — спочатку відпрацьовують більш загальні класи, потім — специфічні.

Розглянемо приклад з ланцюжком:

```csharp run
using System;

Doctor doctor = new Doctor("Олена Коваль", 38, "Кардіологія");

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }

    public Person(string name)
    {
        Name = name;
        Console.WriteLine($"Person(name): {name}");
    }

    public Person(string name, int age) : this(name)
    {
        Age = age;
        Console.WriteLine($"Person(name, age): {name}, {age}");
    }
}

class Doctor : Person
{
    public string Specialization { get; set; }

    public Doctor(string name, int age, string specialization)
        : base(name, age)
    {
        Specialization = specialization;
        Console.WriteLine($"Doctor(name, age, spec): {specialization}");
    }
}
```

Виконання розгортається так:
1. `new Doctor(...)` → викликається `Doctor(name, age, spec)`, але спочатку делегує `base(name, age)`
2. `Person(name, age)` → не виконується одразу, делегує `this(name)`
3. `Person(name)` → делегує неявно `Object()`
4. **Виконується** `Object()` — найбазовіший конструктор
5. **Виконується** тіло `Person(name)` → виводить `Person(name): Олена Коваль`
6. **Виконується** тіло `Person(name, age)` → виводить `Person(name, age): Олена Коваль, 38`
7. **Виконується** тіло `Doctor(...)` → виводить `Doctor(name, age, spec): Кардіологія`

![Порядок виклику конструкторів у ланцюжку успадкування](_assets/04-01/constructor-order.png)

Цей порядок гарантує, що до моменту виконання конструктора похідного класу базовий клас вже повністю ініціалізований. Якби `Doctor` намагався звернутися до `Name` у своєму конструкторі — властивість вже була б встановлена конструктором `Person`.

## Запечатаний клас: sealed

Модифікатор `sealed` повністю забороняє успадкування від класу. Це явна архітектурна декларація: «цей клас спроектований як кінцевий, розширення через успадкування не передбачено».

```csharp run
using System;

// Звичайне використання — працює
CertifiedSurgeon surgeon = new CertifiedSurgeon("Андрій Мельник", "Кардіохірургія");
surgeon.PrintInfo();

// class SpecialSurgeon : CertifiedSurgeon { }  // Помилка компіляції!

class Doctor
{
    public string Name { get; set; }

    public Doctor(string name) { Name = name; }

    public virtual void PrintInfo() =>
        Console.WriteLine($"Лікар: {Name}");
}

sealed class CertifiedSurgeon : Doctor
{
    public string Specialization { get; set; }

    public CertifiedSurgeon(string name, string specialization) : base(name)
    {
        Specialization = specialization;
    }

    public override void PrintInfo() =>
        Console.WriteLine($"Сертифікований хірург: {Name} | {Specialization}");
}
```

`sealed` клас може сам успадковувати від інших класів (як `CertifiedSurgeon` від `Doctor`), але не дозволяє мати власних нащадків. У стандартній бібліотеці .NET таким чином оголошені `String`, `StringBuilder` та багато інших класів — їх не можна розширити через успадкування.

Окрім захисту архітектури, `sealed` дає компілятору можливість генерувати ефективніший код: якщо клас запечатаний, виклики його методів можна не диспетчеризувати через таблицю віртуальних методів.
