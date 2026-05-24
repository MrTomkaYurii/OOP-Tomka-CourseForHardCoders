---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 7
number: "4.7"
title: "Клас System.Object та його методи"
source: "../_combined/24-system-object-ta-ioho-metody.md"
---

## 4.7. Клас System.Object та його методи

Усі класи в .NET — як вбудовані (`int`, `string`, `DateTime`), так і ті, що ми створюємо самостійно — є похідними від класу `System.Object`. Навіть якщо ми не вказуємо `Object` як базовий, компілятор додає це успадкування неявно. Це означає, що кожен об'єкт у C# гарантовано має чотири методи: `ToString()`, `GetHashCode()`, `Equals()` та `GetType()`.

![Методи System.Object доступні у кожному класі](_assets/04-07/object-methods.png)

## Метод ToString

Метод `ToString()` повертає рядкове представлення об'єкта. Для числових типів це їхнє значення у вигляді рядка. Для власних класів стандартна реалізація повертає повну назву типу з простором імен:

```csharp run
using System;

int age = 45;
double temperature = 36.6;

Console.WriteLine(age.ToString());         // 45
Console.WriteLine(temperature.ToString()); // 36,6

Patient patient = new Patient("Іван Петренко", 45, "Гіпертонія");
Console.WriteLine(patient.ToString()); // назва типу: Patient

class Patient
{
    public string Name { get; set; }
    public int Age { get; set; }
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diagnosis)
    { Name = name; Age = age; Diagnosis = diagnosis; }
}
```

Ми можемо перевизначити `ToString()`, щоб повертати змістовний рядок замість назви типу:

```csharp run
using System;

Patient patient = new Patient("Іван Петренко", 45, "Гіпертонія");
Doctor  doctor  = new Doctor("Олена Коваль", 38, "Кардіологія");

Console.WriteLine(patient.ToString());
Console.WriteLine(doctor.ToString());

// Console.WriteLine автоматично викликає ToString()
Console.WriteLine(patient);
Console.WriteLine(doctor);

class Patient
{
    public string Name { get; set; }
    public int Age { get; set; }
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diagnosis)
    { Name = name; Age = age; Diagnosis = diagnosis; }

    public override string ToString()
    {
        return $"Пацієнт: {Name}, {Age} р. | {Diagnosis}";
    }
}

class Doctor
{
    public string Name { get; set; }
    public int Age { get; set; }
    public string Specialization { get; set; }
    public Doctor(string name, int age, string spec)
    { Name = name; Age = age; Specialization = spec; }

    public override string ToString()
    {
        return $"Лікар: {Name}, {Age} р. | {Specialization}";
    }
}
```

Зверніть увагу: `Console.WriteLine(patient)` автоматично викликає `ToString()` без явного звернення. Це справедливо для рядкової інтерполяції та конкатенації рядків — `$"Пацієнт: {patient}"` теж неявно викликає `ToString()`.

Якщо клас частково заповнений (наприклад, відсутнє ім'я), можна повернути результат базової реалізації через `base.ToString()`:

```csharp run
using System;

Patient named   = new Patient("Іван Петренко", 45);
Patient unnamed = new Patient("", 0);

Console.WriteLine(named.ToString());    // Іван Петренко, 45 р.
Console.WriteLine(unnamed.ToString());  // Patient (базова реалізація)

class Patient
{
    public string Name { get; set; } = "";
    public int Age { get; set; }
    public Patient(string name, int age) { Name = name; Age = age; }

    public override string? ToString()
    {
        if (string.IsNullOrEmpty(Name))
            return base.ToString(); // повертає "Patient"
        return $"{Name}, {Age} р.";
    }
}
```

## Метод GetHashCode

Метод `GetHashCode()` повертає ціле число — **хеш-код** об'єкта. Хеш-коди використовуються колекціями на основі хеш-таблиць (`Dictionary<K,V>`, `HashSet<T>`) для швидкого пошуку та зберігання об'єктів.

```csharp run
using System;

Patient p1 = new Patient("Іван Петренко", 45);
Patient p2 = new Patient("Іван Петренко", 45);
Patient p3 = new Patient("Марія Сидоренко", 32);

Console.WriteLine(p1.GetHashCode().ToString());
Console.WriteLine(p2.GetHashCode().ToString()); // однаковий з p1
Console.WriteLine(p3.GetHashCode().ToString()); // інший

class Patient
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Patient(string name, int age) { Name = name; Age = age; }

    public override int GetHashCode()
    {
        // Комбінуємо хеш-коди всіх полів, що беруть участь у порівнянні
        return HashCode.Combine(Name, Age);
    }
}
```

`HashCode.Combine(...)` — зручний вбудований спосіб об'єднати хеш-коди кількох полів. Два об'єкти, які рівні за `Equals`, **зобов'язані** повертати однаковий хеш-код — це фундаментальний контракт, який забезпечує коректну роботу колекцій.

## Контракт рівності: Equals і GetHashCode завжди разом

Методи `Equals` і `GetHashCode` утворюють **контракт рівності**: якщо два об'єкти рівні (`Equals` повертає `true`), вони повинні мати однаковий хеш-код. Порушення цього правила призводить до некоректної поведінки словників і множин — об'єкти, які логічно рівні, не знаходитимуться у колекції.

Тому: **якщо перевизначаєте `Equals` — завжди перевизначайте `GetHashCode`**, і навпаки.

```csharp run
using System;

Patient p1 = new Patient("Іван Петренко", "P-001");
Patient p2 = new Patient("Марія Сидоренко", "P-002");
Patient p3 = new Patient("Іван Петренко", "P-001");

Console.WriteLine(p1.Equals(p2).ToString()); // False
Console.WriteLine(p1.Equals(p3).ToString()); // True — однаковий recordId
Console.WriteLine((p1.GetHashCode() == p3.GetHashCode()).ToString()); // True

class Patient
{
    public string Name { get; set; }
    public string RecordId { get; set; }

    public Patient(string name, string recordId)
    { Name = name; RecordId = recordId; }

    public override bool Equals(object? obj)
    {
        if (obj is Patient other)
            return RecordId == other.RecordId; // рівність за унікальним ID картки
        return false;
    }

    public override int GetHashCode() => RecordId.GetHashCode();

    public override string ToString() => $"{Name} [{RecordId}]";
}
```

У клінічному контексті логічно вважати двох пацієнтів однаковими, якщо збігається їхній унікальний ідентифікатор картки (`RecordId`), — навіть якщо ім'я записане по-різному.

## Метод GetType

Метод `GetType()` повертає об'єкт типу `Type`, який описує реальний тип об'єкта під час виконання. На відміну від інших методів `Object`, `GetType()` **не можна перевизначити** — це гарантує надійність системи типів:

```csharp run
using System;

Person person  = new Patient("Іван Петренко", 45, "Гіпертонія");
Patient patient = new Patient("Марія Сидоренко", 32, "Бронхіт");

Console.WriteLine(person.GetType().Name);   // Patient (реальний тип!)
Console.WriteLine(patient.GetType().Name);  // Patient

// Порівняння типів через typeof
if (person.GetType() == typeof(Patient))
    Console.WriteLine("Це Patient");

// Коротший спосіб — оператор is
if (person is Patient p)
    Console.WriteLine($"Діагноз: {p.Diagnosis}");

class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age) { Name = name; Age = age; }
}

class Patient : Person
{
    public string Diagnosis { get; set; }
    public Patient(string name, int age, string diagnosis) : base(name, age)
    { Diagnosis = diagnosis; }
}
```

`GetType()` завжди повертає реальний тип об'єкта, навіть якщо змінна оголошена як базовий тип. Це відрізняє його від оператора `is`, який також перевіряє сумісність з ієрархією (тобто `patient is Person` поверне `true`), тоді як `GetType() == typeof(Person)` поверне `false` для об'єкта `Patient`.
