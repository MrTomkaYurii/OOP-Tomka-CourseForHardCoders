---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 4
number: "7.4"
title: "Успадкування інтерфейсів"
source: "../_combined/42-uspadkuvannia-interfeisiv.md"
---

## 7.4. Успадкування інтерфейсів

Інтерфейси не лише описують контракти — вони можуть розширювати один одного. Механізм **успадкування інтерфейсів** (interface inheritance) дозволяє будувати ієрархії контрактів: від загального до конкретного. Клас, який реалізує похідний інтерфейс, зобов'язаний виконати контракти всіх інтерфейсів у ланцюжку.

Це дає змогу проектувати системи поступово: спочатку визначати базові здібності об'єкта, потім нашаровувати на них більш спеціалізовані вимоги — не змінюючи вже написаний код.

### Базовий синтаксис

Синтаксис успадкування інтерфейсів ідентичний синтаксису успадкування класів — через двокрапку:

```csharp
interface IExaminable
{
    void Examine();       // провести огляд пацієнта
}

interface IDiagnosable : IExaminable
{
    void Diagnose();      // поставити діагноз
}
```

Тут `IDiagnosable` розширює `IExaminable`. Це означає, що `IDiagnosable` включає в себе всі члени `IExaminable` плюс власні.

Будь-який клас чи структура, що реалізує `IDiagnosable`, зобов'язана реалізувати **обидва** методи — і `Examine()`, і `Diagnose()`:

```csharp run
using System;

interface IExaminable
{
    void Examine();
}

interface IDiagnosable : IExaminable
{
    void Diagnose();
}

class GeneralPractitioner : IDiagnosable
{
    public void Examine()
    {
        Console.WriteLine("Лікар проводить загальний огляд пацієнта.");
    }

    public void Diagnose()
    {
        Console.WriteLine("Лікар ставить діагноз на основі огляду.");
    }
}

class Program
{
    static void Main()
    {
        GeneralPractitioner gp = new GeneralPractitioner();

        // Використання через тип IDiagnosable — бачимо обидва методи
        IDiagnosable diagnosable = gp;
        diagnosable.Examine();
        diagnosable.Diagnose();

        Console.WriteLine("---");

        // Використання через тип IExaminable — бачимо лише Examine
        IExaminable examinable = gp;
        examinable.Examine();
    }
}
```

Зверніть увагу: змінна типу `IExaminable` дає доступ лише до `Examine()`, хоч і містить той самий об'єкт. Тип змінної визначає, який «зріз» контракту видно у конкретному місці коду.

### Ланцюжок успадкування

Інтерфейси можуть утворювати ланцюжки довільної довжини. Кожен новий інтерфейс у ланцюжку додає нові вимоги до контракту:

![Ланцюжок успадкування інтерфейсів](_assets/07-04/interface-inheritance-chain.png)

Клас `Doctor`, що реалізує `ITreatable`, зобов'язаний надати реалізацію всіх трьох методів — `Examine()`, `Diagnose()` і `Treat()`. Компілятор перевіряє це під час збірки: якщо хоча б один метод не реалізовано — отримаємо помилку компіляції.

```csharp run
using System;

interface IExaminable
{
    void Examine();
}

interface IDiagnosable : IExaminable
{
    void Diagnose();
}

interface ITreatable : IDiagnosable
{
    void Treat();
}

class Doctor : ITreatable
{
    private string _name;

    public Doctor(string name)
    {
        _name = name;
    }

    public void Examine()
    {
        Console.WriteLine($"Доктор {_name} проводить огляд.");
    }

    public void Diagnose()
    {
        Console.WriteLine($"Доктор {_name} ставить діагноз.");
    }

    public void Treat()
    {
        Console.WriteLine($"Доктор {_name} призначає лікування.");
    }
}

class Program
{
    static void Main()
    {
        Doctor doctor = new Doctor("Ковальчук");

        // Повний контракт через ITreatable
        ITreatable treatable = doctor;
        treatable.Examine();
        treatable.Diagnose();
        treatable.Treat();

        Console.WriteLine("---");

        // Частковий контракт через IExaminable
        IExaminable examinable = doctor;
        examinable.Examine();
        // examinable.Diagnose(); // помилка — IExaminable не знає про Diagnose
    }
}
```

### Множинне успадкування інтерфейсів

На відміну від класів, **інтерфейс може успадковувати відразу кілька батьківських інтерфейсів**. Це одна з ключових відмінностей інтерфейсів від класів у C# — множинне успадкування реалізації заборонене для класів, але множинне успадкування контракту — цілком допустиме для інтерфейсів.

Синтаксис: після двокрапки перераховуємо всі базові інтерфейси через кому:

```csharp
interface IClinicAppointment : ISchedulable, IPayable
{
    // ...
}
```

![Множинне успадкування інтерфейсів](_assets/07-04/multiple-interface-inheritance.png)

Клас `Appointment`, що реалізує `IClinicAppointment`, зобов'язаний виконати контракти обох батьківських інтерфейсів — `ISchedulable` і `IPayable` — а також власні члени `IClinicAppointment`:

```csharp run
using System;

interface ISchedulable
{
    void Schedule(string patientName, string time);
    string GetSlot();
}

interface IPayable
{
    decimal CalculateCost();
    void ApplyDiscount(int percent);
}

interface IClinicAppointment : ISchedulable, IPayable
{
    string DoctorName { get; }
}

class Appointment : IClinicAppointment
{
    private string _patient;
    private string _time;
    private decimal _baseCost;
    private int _discountPercent;

    public string DoctorName { get; }

    public Appointment(string doctor, decimal baseCost)
    {
        DoctorName = doctor;
        _baseCost = baseCost;
        _discountPercent = 0;
        _patient = "";
        _time = "";
    }

    public void Schedule(string patientName, string time)
    {
        _patient = patientName;
        _time = time;
        Console.WriteLine($"Записано: {_patient} до {DoctorName} на {_time}.");
    }

    public string GetSlot()
    {
        return $"{_time} ({_patient})";
    }

    public decimal CalculateCost()
    {
        decimal discount = _baseCost * _discountPercent / 100m;
        return _baseCost - discount;
    }

    public void ApplyDiscount(int percent)
    {
        _discountPercent = percent;
        Console.WriteLine($"Знижка {percent}% застосована.");
    }
}

class Program
{
    static void Main()
    {
        Appointment appt = new Appointment("Ковальчук", 800m);

        appt.Schedule("Петренко І.", "14:30");
        appt.ApplyDiscount(10);

        Console.WriteLine($"Вартість прийому: {appt.CalculateCost().ToString()} грн");
        Console.WriteLine($"Слот: {appt.GetSlot()}");
        Console.WriteLine($"Лікар: {appt.DoctorName}");
    }
}
```

### Ключове слово new — приховування членів базового інтерфейсу

Коли базовий інтерфейс має метод із **реалізацією за замовчуванням** (default interface implementation), похідний інтерфейс може її перевизначити за допомогою ключового слова `new`. Це приховування (hiding), а не перевизначення у звичному розумінні.

```csharp run
using System;

interface IExaminable
{
    // Реалізація за замовчуванням
    void Examine() => Console.WriteLine("Стандартний огляд: вимірювання температури і тиску.");
}

interface IDiagnosable : IExaminable
{
    // Приховуємо Examine з IExaminable і даємо нову реалізацію за замовчуванням
    new void Examine() => Console.WriteLine("Розширений огляд: аналізи + УЗД + огляд.");
}

class Patient { }  // Порожній клас — не реалізує жодного інтерфейсу

class Specialist : IDiagnosable { }  // Реалізації за замовчуванням не вимагають тіла

class Program
{
    static void Main()
    {
        Specialist s = new Specialist();

        // Тип IDiagnosable — викликається прихована версія
        IDiagnosable d = s;
        d.Examine();

        // Тип IExaminable — викликається оригінальна версія
        IExaminable e = s;
        e.Examine();
    }
}
```

Поведінка залежить від **типу змінної**, а не від фактичного об'єкта. Якщо змінна оголошена як `IDiagnosable` — буде викликана його версія `Examine()`. Якщо `IExaminable` — оригінальна. Це принципово відрізняється від поліморфізму через `virtual`/`override`, де завжди викликається версія фактичного об'єкта.

Клас може повністю взяти контроль і реалізувати `Examine()` самостійно — тоді обидва типи повертатимуть ту саму реалізацію:

```csharp run
using System;

interface IExaminable
{
    void Examine() => Console.WriteLine("Стандартний огляд.");
}

interface IDiagnosable : IExaminable
{
    new void Examine() => Console.WriteLine("Розширений огляд.");
}

class Cardiologist : IDiagnosable
{
    // Власна реалізація перекриває обидві
    public void Examine() => Console.WriteLine("Кардіологічний огляд: ЕКГ + ехокардіографія.");
}

class Program
{
    static void Main()
    {
        Cardiologist c = new Cardiologist();

        IDiagnosable d = c;
        d.Examine();  // Кардіологічний огляд

        IExaminable e = c;
        e.Examine();  // Кардіологічний огляд — однакова відповідь
    }
}
```

### Модифікатори sealed та abstract для інтерфейсів

Інтерфейси мають власні правила щодо модифікаторів доступу та структури:

**`sealed` — заборонений для інтерфейсів.** Модифікатор `sealed` у класах забороняє успадкування. Для інтерфейсів такого механізму не існує — будь-який інтерфейс можна успадкувати. Це відповідає природі інтерфейсу як відкритого контракту.

**`abstract` — надлишковий для інтерфейсів.** Інтерфейс вже за визначенням є абстрактним: він описує контракт без (обов'язкової) реалізації. Тому ключове слово `abstract` на рівні інтерфейсу не має сенсу і не допускається компілятором.

### Правила рівня доступу

При успадкуванні інтерфейсів діє таке саме правило, що й при успадкуванні класів: **похідний інтерфейс не може бути менш обмеженим, ніж базовий**.

Припустимо, що базовий інтерфейс є `public` — тоді похідний може бути або `public`, або `internal`:

```csharp
public interface IExaminable
{
    void Examine();
}

// Коректно: internal є більш суворим, ніж public
internal interface IDiagnosable : IExaminable
{
    void Diagnose();
}
```

Але не навпаки. Якщо базовий є `internal`, то похідний **не може бути `public`** — це порушує принцип інкапсуляції типів:

```csharp
internal interface IExaminable
{
    void Examine();
}

// ПОМИЛКА: IRunAction може бути лише internal,
// бо базовий IExaminable є internal
public interface IDiagnosable : IExaminable
{
    void Diagnose();
}
```

Компілятор поверне помилку: неможливо оголосити `public` тип, що успадковує `internal` тип, оскільки `internal` тип недоступний за межами збірки.

### Підсумок

Успадкування інтерфейсів — потужний інструмент для побудови гнучких та розширюваних систем. Основні правила:

- Інтерфейс успадковує члени всіх своїх базових інтерфейсів.
- Клас, що реалізує похідний інтерфейс, зобов'язаний реалізувати весь ланцюжок.
- Інтерфейс може успадковувати **кілька** базових інтерфейсів одночасно.
- `sealed` і `abstract` на рівні інтерфейсу не допускаються.
- `new` у похідному інтерфейсі приховує (а не перевизначає) метод базового.
- Доступ похідного інтерфейсу не може бути менш суворим, ніж базового.
