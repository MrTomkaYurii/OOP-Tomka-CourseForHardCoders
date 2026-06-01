---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 6
number: "7.6"
title: "Копіювання об'єктів. Інтерфейс ICloneable"
source: "../_combined/44-kopiiuvannia-obiektiv-interfeis-icloneable.md"
---

## 7.6. Копіювання об'єктів. Інтерфейс ICloneable

Оскільки класи є **посилальними типами** (reference types), змінна класу зберігає не сам об'єкт, а адресу у пам'яті, де цей об'єкт знаходиться. Просте присвоєння `b = a` не створює нового об'єкта — воно лише копіює адресу: тепер обидві змінні вказують на **той самий** об'єкт у купі.

### Проблема копіювання посилальних типів

```csharp run
using System;

class Patient
{
    public string Name { get; set; }
    public int Age { get; set; }

    public Patient(string name, int age)
    {
        Name = name;
        Age = age;
    }
}

class Program
{
    static void Main()
    {
        var patient1 = new Patient("Петренко", 45);
        var patient2 = patient1;  // копіюємо ПОСИЛАННЯ, не об'єкт

        patient2.Name = "Іваненко";  // змінюємо через patient2...

        // ...але змінилось в обох, бо це один об'єкт!
        Console.WriteLine(patient1.Name);  // Іваненко (а не Петренко!)
        Console.WriteLine(patient2.Name);  // Іваненко
    }
}
```

Щоб `patient2` вказував на **новий**, незалежний об'єкт з такими самими даними, застосовують **клонування**.

### Інтерфейс ICloneable

Стандартна бібліотека .NET пропонує інтерфейс `ICloneable` з єдиним методом:

```csharp
public interface ICloneable
{
    object Clone();
}
```

Метод `Clone()` повертає `object` — незалежну копію поточного об'єкта. Конкретний спосіб копіювання клас реалізує самостійно, обираючи між поверхневим і глибоким копіюванням.

### Поверхневе копіювання

**Поверхневе копіювання** (shallow copy) створює новий об'єкт і копіює до нього всі поля поточного об'єкта «як є». Для полів-значень (int, bool, struct тощо) це повноцінна незалежна копія. Але для полів-посилань копіюється лише **адреса** — новий об'єкт і оригінал будуть вказувати на той самий вкладений об'єкт у пам'яті.

Метод `MemberwiseClone()`, успадкований від `object`, виконує саме поверхневе копіювання:

```csharp run
using System;

class Patient : ICloneable
{
    public string Name { get; set; }
    public int Age { get; set; }

    public Patient(string name, int age)
    {
        Name = name;
        Age = age;
    }

    public object Clone() => MemberwiseClone();
}

class Program
{
    static void Main()
    {
        var patient1 = new Patient("Петренко", 45);
        var patient2 = (Patient)patient1.Clone();

        patient2.Name = "Іваненко";
        patient2.Age = 32;

        // Тепер це незалежні об'єкти
        Console.WriteLine($"patient1: {patient1.Name}, {patient1.Age.ToString()} р.");
        Console.WriteLine($"patient2: {patient2.Name}, {patient2.Age.ToString()} р.");
    }
}
```

Для полів-значень поверхневе копіювання достатнє. Але якщо клас містить поле-посилання на інший об'єкт, виникає проблема:

```csharp run
using System;

class DiagnosisRecord
{
    public string Code { get; set; }
    public string Description { get; set; }

    public DiagnosisRecord(string code, string description)
    {
        Code = code;
        Description = description;
    }
}

class Patient : ICloneable
{
    public string Name { get; set; }
    public DiagnosisRecord Diagnosis { get; set; }

    public Patient(string name, DiagnosisRecord diagnosis)
    {
        Name = name;
        Diagnosis = diagnosis;
    }

    // Поверхневе копіювання — копіює ПОСИЛАННЯ на Diagnosis
    public object Clone() => MemberwiseClone();
}

class Program
{
    static void Main()
    {
        var patient1 = new Patient("Петренко", new DiagnosisRecord("J18.0", "Пневмонія"));
        var patient2 = (Patient)patient1.Clone();

        patient2.Name = "Іваненко";
        patient2.Diagnosis.Code = "I10";    // змінюємо діагноз у patient2...

        // ...але patient1.Diagnosis також змінився!
        Console.WriteLine($"patient1: {patient1.Name}, {patient1.Diagnosis.Code}");
        Console.WriteLine($"patient2: {patient2.Name}, {patient2.Diagnosis.Code}");
        // Обидва мають I10 — DiagnosisRecord спільний!
    }
}
```

### Глибоке копіювання

![Поверхневе та глибоке копіювання](_assets/07-06/shallow-deep-copy.png)

**Глибоке копіювання** (deep copy) вирішує проблему: для кожного поля-посилання вручну створюється новий об'єкт із тими самими даними. `Clone()` повністю будує незалежну копію всього графа об'єктів:

```csharp run
using System;

class DiagnosisRecord
{
    public string Code { get; set; }
    public string Description { get; set; }

    public DiagnosisRecord(string code, string description)
    {
        Code = code;
        Description = description;
    }
}

class Patient : ICloneable
{
    public string Name { get; set; }
    public DiagnosisRecord Diagnosis { get; set; }

    public Patient(string name, DiagnosisRecord diagnosis)
    {
        Name = name;
        Diagnosis = diagnosis;
    }

    // Глибоке копіювання — новий DiagnosisRecord для кожного клону
    public object Clone()
    {
        var diagnosisCopy = new DiagnosisRecord(Diagnosis.Code, Diagnosis.Description);
        return new Patient(Name, diagnosisCopy);
    }
}

class Program
{
    static void Main()
    {
        var patient1 = new Patient("Петренко", new DiagnosisRecord("J18.0", "Пневмонія"));
        var patient2 = (Patient)patient1.Clone();

        patient2.Name = "Іваненко";
        patient2.Diagnosis.Code = "I10";  // змінюємо лише в patient2

        Console.WriteLine($"patient1: {patient1.Name}, {patient1.Diagnosis.Code}");  // J18.0
        Console.WriteLine($"patient2: {patient2.Name}, {patient2.Diagnosis.Code}");  // I10
        // Тепер об'єкти повністю незалежні
    }
}
```

**Правило вибору**: якщо клас містить лише поля значимих типів або рядки (які незмінні в C#) — достатньо `MemberwiseClone()`. Якщо є вкладені об'єкти-посилання, що можуть змінюватися — потрібне глибоке копіювання.

### Сортування об'єктів. Інтерфейс IComparable

Вбудовані типи C# — числа, рядки — вміють порівнювати себе між собою: `Array.Sort` на масиві `int[]` спрацює одразу. Але для власних класів компілятор не знає, який порядок вважати «правильним». Для цього існує інтерфейс `IComparable<T>`:

```csharp
public interface IComparable<T>
{
    int CompareTo(T? other);
}
```

Метод `CompareTo` повертає:
- **від'ємне число** — поточний об'єкт стоїть **до** `other` у відсортованому порядку
- **нуль** — об'єкти рівні за критерієм порівняння
- **додатне число** — поточний об'єкт стоїть **після** `other`

Реалізуємо сортування пацієнтів за прізвищем:

```csharp run
using System;

class Patient : IComparable<Patient>
{
    public string LastName { get; }
    public string FirstName { get; }
    public int Age { get; }

    public Patient(string lastName, string firstName, int age)
    {
        LastName = lastName;
        FirstName = firstName;
        Age = age;
    }

    // Порівнюємо за прізвищем (алфавітний порядок)
    public int CompareTo(Patient? other)
    {
        if (other is null)
            throw new ArgumentException("Некоректне значення параметра");
        return LastName.CompareTo(other.LastName);
    }

    public override string ToString() =>
        $"{LastName} {FirstName}, {Age.ToString()} р.";
}

class Program
{
    static void Main()
    {
        Patient[] patients =
        {
            new Patient("Шевченко", "Оксана", 34),
            new Patient("Іваненко", "Петро",  52),
            new Patient("Бойко",    "Марія",  28),
            new Patient("Ковальчук","Андрій", 41),
        };

        Array.Sort(patients);  // використовує CompareTo

        Console.WriteLine("Пацієнти за алфавітом:");
        foreach (Patient p in patients)
            Console.WriteLine($"  {p.ToString()}");
    }
}
```

### Застосування компаратора IComparer

Іноді потрібно сортувати за різними критеріями в різних ситуаціях — наприклад, за прізвищем в одному місці програми і за віком в іншому. Один клас не може мати два різні `CompareTo`. Для цього існує окремий інтерфейс `IComparer<T>`:

```csharp
public interface IComparer<in T>
{
    int Compare(T? x, T? y);
}
```

Компаратор — це окремий клас, що описує **один конкретний спосіб порівняння**. Він передається як другий аргумент у `Array.Sort`:

```csharp run
using System;

class Patient
{
    public string LastName { get; }
    public int Age { get; }

    public Patient(string lastName, int age)
    {
        LastName = lastName;
        Age = age;
    }

    public override string ToString() => $"{LastName}, {Age.ToString()} р.";
}

// Компаратор за віком (від молодшого до старшого)
class PatientAgeComparer : IComparer<Patient>
{
    public int Compare(Patient? x, Patient? y)
    {
        if (x is null || y is null)
            throw new ArgumentException("Некоректне значення параметра");
        return x.Age.CompareTo(y.Age);
    }
}

// Компаратор за прізвищем
class PatientNameComparer : IComparer<Patient>
{
    public int Compare(Patient? x, Patient? y)
    {
        if (x is null || y is null)
            throw new ArgumentException("Некоректне значення параметра");
        return x.LastName.CompareTo(y.LastName);
    }
}

class Program
{
    static void Main()
    {
        Patient[] patients =
        {
            new Patient("Шевченко", 34),
            new Patient("Іваненко", 52),
            new Patient("Бойко",    28),
            new Patient("Ковальчук",41),
        };

        Array.Sort(patients, new PatientAgeComparer());
        Console.WriteLine("За віком:");
        foreach (Patient p in patients)
            Console.WriteLine($"  {p.ToString()}");

        Console.WriteLine();

        Array.Sort(patients, new PatientNameComparer());
        Console.WriteLine("За прізвищем:");
        foreach (Patient p in patients)
            Console.WriteLine($"  {p.ToString()}");
    }
}
```

Правила компаратора мають **вищий пріоритет** над `CompareTo`: якщо клас реалізує `IComparable<T>` і одночасно передається `IComparer<T>` — перемагає компаратор.

### Підсумок

| Інтерфейс | Призначення | Де реалізується |
|---|---|---|
| `ICloneable` | Копіювання об'єкта | У класі, що копіюється |
| `IComparable<T>` | Вбудований порядок сортування | У класі, що порівнюється |
| `IComparer<T>` | Зовнішній, змінний критерій сортування | В окремому класі-компараторі |

Поверхневе копіювання (`MemberwiseClone`) підходить для об'єктів без вкладених посилальних типів. Для складних об'єктів з вкладеними посиланнями потрібне глибоке копіювання через ручне створення копій кожного вкладеного об'єкта.
