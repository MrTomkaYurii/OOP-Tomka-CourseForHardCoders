---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 5
number: "7.5"
title: "Інтерфейси в узагальненнях"
source: "../_combined/43-interfeisy-v-uzahalnenniakh.md"
---

## 7.5. Інтерфейси в узагальненнях

Інтерфейси та узагальнення (generics) тісно взаємодіють між собою у C#. З одного боку, інтерфейси виступають як **обмеження (constraints)** для узагальнених типів — вони гарантують, що параметр типу T реалізує певний контракт. З іншого боку, самі інтерфейси можуть бути **узагальненими** — тобто мати власний параметр типу T, яким їхні члени типізуються під час реалізації.

### Інтерфейси як обмеження узагальнень

Коли ви оголошуєте узагальнений клас або метод, ви можете обмежити допустимі типи для параметра T за допомогою ключового слова `where`. Інтерфейс у ролі обмеження означає: «T повинен реалізовувати цей інтерфейс». Компілятор перевіряє це під час збірки — і якщо спробувати підставити тип, що не відповідає обмеженню, виникне помилка до запуску програми.

Ключова перевага перед обмеженнями за класом: **обмежень-інтерфейсів можна вказати скільки завгодно**, тоді як базовий клас у `where` може бути лише один.

```csharp
// можна вказати кілька інтерфейсів:
class ClinicReporter<T> where T : IExaminable, IPrintable { }

// але базовий клас — тільки один (і він йде першим):
class ClinicReporter<T> where T : BaseMedical, IExaminable, IPrintable { }
```

Розглянемо практичний приклад. У клінічній системі є два інтерфейси: `IExaminable` описує об'єкти, щодо яких можна провести огляд, а `IPrintable` — об'єкти, що підтримують виведення звіту. Клас `ClinicReporter<T>` приймає лише ті типи, що реалізують обидва:

![Обмеження узагальнень](_assets/07-05/generic-constraint.png)

```csharp run
using System;

interface IExaminable
{
    string Summary { get; }
    void Examine();
}

interface IPrintable
{
    void Print();
}

// Doctor реалізує обидва інтерфейси — допустимий тип для T
class Doctor : IExaminable, IPrintable
{
    public string Name { get; }
    public string Summary => $"Лікар: {Name}";

    public Doctor(string name) { Name = name; }

    public void Examine() =>
        Console.WriteLine($"{Name} проводить огляд пацієнта.");

    public void Print() =>
        Console.WriteLine($"[Звіт] {Summary}");
}

// Nurse реалізує лише IExaminable — НЕ допустимий для ClinicReporter<T>
class Nurse : IExaminable
{
    public string Name { get; }
    public string Summary => $"Медсестра: {Name}";

    public Nurse(string name) { Name = name; }

    public void Examine() =>
        Console.WriteLine($"{Name} вимірює температуру.");
}

// Клас приймає лише T, що реалізує обидва інтерфейси
class ClinicReporter<T> where T : IExaminable, IPrintable
{
    public void GenerateReport(T worker)
    {
        Console.WriteLine($"--- Генерація звіту ---");
        worker.Examine();
        worker.Print();
        Console.WriteLine($"Зведення: {worker.Summary}");
    }
}

class Program
{
    static void Main()
    {
        var reporter = new ClinicReporter<Doctor>();
        reporter.GenerateReport(new Doctor("Ковальчук"));

        // ClinicReporter<Nurse> — помилка компіляції:
        // Nurse не реалізує IPrintable
    }
}
```

Зверніть увагу: `ClinicReporter<Nurse>` не скомпілюється взагалі — компілятор повідомить про порушення обмеження ще на етапі збірки. Це набагато безпечніше, ніж перевірка типу під час виконання.

#### Інтерфейс як параметр типу

Обмеження `where T : IExaminable, IPrintable` задовольняє не лише клас, а й **інтерфейс, що успадковує обидва**. Наприклад:

```csharp run
using System;

interface IExaminable
{
    string Summary { get; }
    void Examine();
}

interface IPrintable
{
    void Print();
}

// Інтерфейс, що об'єднує обидва — також задовольняє обмеження
interface IClinicWorker : IExaminable, IPrintable
{
    string Department { get; }
}

class Cardiologist : IClinicWorker
{
    public string Name { get; }
    public string Department => "Кардіологія";
    public string Summary => $"Кардіолог {Name} ({Department})";

    public Cardiologist(string name) { Name = name; }

    public void Examine() =>
        Console.WriteLine($"{Name}: ЕКГ + ехокардіографія.");

    public void Print() =>
        Console.WriteLine($"[Звіт] {Summary}");
}

class ClinicReporter<T> where T : IExaminable, IPrintable
{
    public void GenerateReport(T worker)
    {
        worker.Examine();
        worker.Print();
    }
}

class Program
{
    static void Main()
    {
        // Cardiologist реалізує IClinicWorker, який включає обидва інтерфейси
        var reporter = new ClinicReporter<Cardiologist>();
        reporter.GenerateReport(new Cardiologist("Іваненко"));

        // Можна також типізувати самим інтерфейсом IClinicWorker:
        // ClinicReporter<IClinicWorker> — теж допустимо
    }
}
```

### Узагальнені інтерфейси

Інтерфейси, як і класи, можуть бути **узагальненими** — тобто мати власний параметр типу `T`. Це дозволяє визначати гнучкі контракти, де конкретні типи підставляються під час реалізації.

Типовий приклад: інтерфейс сутності зі значенням ідентифікатора, тип якого може варіюватися:

```csharp
interface IEntity<TId>
{
    TId Id { get; }
}
```

Клас `Patient` може використовувати `int` як тип ідентифікатора, а `InsurancePolicy` — рядок (GUID або номер поліса):

```csharp run
using System;

interface IEntity<TId>
{
    TId Id { get; }
    string DisplayName { get; }
}

class Patient : IEntity<int>
{
    public int Id { get; }
    public string Name { get; }
    public string DisplayName => $"Пацієнт #{Id}: {Name}";

    public Patient(int id, string name)
    {
        Id = id;
        Name = name;
    }
}

class InsurancePolicy : IEntity<string>
{
    public string Id { get; }           // номер поліса — рядок
    public string HolderName { get; }
    public string DisplayName => $"Поліс {Id} — {HolderName}";

    public InsurancePolicy(string policyNumber, string holder)
    {
        Id = policyNumber;
        HolderName = holder;
    }
}

class Program
{
    static void Main()
    {
        IEntity<int> patient = new Patient(1042, "Петренко Іван");
        Console.WriteLine(patient.DisplayName);
        Console.WriteLine($"ID (int): {patient.Id.ToString()}");

        Console.WriteLine("---");

        IEntity<string> policy = new InsurancePolicy("UA-2024-00789", "Петренко Іван");
        Console.WriteLine(policy.DisplayName);
        Console.WriteLine($"ID (string): {policy.Id}");
    }
}
```

#### Фіксований параметр типу

Під час реалізації узагальненого інтерфейсу клас може відразу **зафіксувати** конкретний тип замість `T`, не стаючи сам узагальненим:

```csharp run
using System;

interface IEntity<TId>
{
    TId Id { get; }
}

// Клас фіксує TId = int — сам вже не є узагальненим
class Doctor : IEntity<int>
{
    public int Id { get; }
    public string Name { get; }
    public string Specialty { get; }

    public Doctor(int id, string name, string specialty)
    {
        Id = id;
        Name = name;
        Specialty = specialty;
    }
}

// Клас фіксує TId = string — використовує ліцензійний номер
class MedicalLicense : IEntity<string>
{
    public string Id { get; }       // наприклад "UA-LIC-2024-5571"
    public string IssuedTo { get; }

    public MedicalLicense(string licenseNumber, string issuedTo)
    {
        Id = licenseNumber;
        IssuedTo = issuedTo;
    }
}

class Program
{
    static void Main()
    {
        Doctor doc = new Doctor(101, "Ковальчук О.П.", "Хірургія");
        IEntity<int> entity = doc;
        Console.WriteLine($"Лікар ID={entity.Id.ToString()}: {doc.Name}, {doc.Specialty}");

        MedicalLicense lic = new MedicalLicense("UA-LIC-2024-5571", "Ковальчук О.П.");
        Console.WriteLine($"Ліцензія {lic.Id} видана: {lic.IssuedTo}");
    }
}
```

Фіксація типу корисна, коли клас точно знає, який тип ідентифікатора він використовує, і не потребує гнучкості: лікарі завжди мають числовий id, а ліцензії — рядковий номер.

### Підсумок

Інтерфейси та узагальнення взаємодіють у двох напрямах:

- **Інтерфейс як обмеження** (`where T : IExaminable, IPrintable`) — гарантує, що тип T реалізує необхідний контракт. Допускається декілька інтерфейсів одночасно. Компілятор перевіряє обмеження під час збірки.
- **Узагальнений інтерфейс** (`IEntity<TId>`) — дозволяє параметризувати контракт типом. Клас реалізує інтерфейс або підставляючи конкретний тип, або залишаючись узагальненим сам.
