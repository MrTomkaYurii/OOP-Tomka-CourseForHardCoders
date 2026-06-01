---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 7
number: "7.7"
title: "Коваріантність та контраваріантність узагальнених інтерфейсів"
source: "../_combined/45-kovariantnist-ta-kontravariantnist-uzahalnenykh-interfeisiv.md"
---

## 7.7. Коваріантність та контраваріантність узагальнених інтерфейсів

Уявіть ієрархію: `Cardiologist` успадковує `Doctor`. Це означає, що `Cardiologist` **є** `Doctor`: де очікується `Doctor`, можна підставити `Cardiologist`. Але чи діє та ж логіка для узагальнених інтерфейсів? Чи можна підставити `IClinicFactory<Cardiologist>` туди, де очікується `IClinicFactory<Doctor>`?

Відповідь залежить від того, чи є інтерфейс **коваріантним**, **контраваріантним** або **інваріантним**. Ці три поняття описують, як напрям допустимого присвоєння між параметризованими типами співвідноситься з напрямом ієрархії між типами-аргументами.

![Коваріантність та контраваріантність](_assets/07-07/variance-directions.png)

**Три форми варіантності:**
- **Коваріантність** — присвоєння йде **в той самий бік**, що й ієрархія класів. Якщо `Cardiologist : Doctor`, то `IFactory<Cardiologist>` можна присвоїти `IFactory<Doctor>`.
- **Контраваріантність** — присвоєння йде **в зворотний бік**. `IHandler<Doctor>` можна присвоїти `IHandler<Cardiologist>`.
- **Інваріантність** — присвоєння неможливе в жодному напрямі (поведінка за замовчуванням).

### Інваріантність — поведінка за замовчуванням

Без спеціальних ключових слів усі узагальнені інтерфейси є **інваріантними**: `IRepository<Doctor>` і `IRepository<Cardiologist>` — абсолютно несумісні типи, навіть якщо `Cardiologist : Doctor`. Жодне присвоєння в жодному напрямі не дозволяється.

```csharp
interface IRepository<T>
{
    T GetById(int id);
    void Save(T item);
}

// IRepository<Cardiologist> НЕ можна присвоїти IRepository<Doctor> — помилка
// IRepository<Doctor> НЕ можна присвоїти IRepository<Cardiologist> — помилка
```

Це може здаватися надто суворим, але є підставовою безпекою: якби `IRepository<Cardiologist>` можна було підставити як `IRepository<Doctor>`, то через змінну типу `IRepository<Doctor>` хтось міг би викликати `Save(new Therapist())` — а `Therapist` не є `Cardiologist`. Тому без явного дозволу компілятор забороняє такі присвоєння.

### Коваріантні інтерфейси (out)

Коваріантний інтерфейс оголошується за допомогою ключового слова **`out`** перед параметром типу:

```csharp
interface IClinicFactory<out T>
{
    T Create();
}
```

Ключове слово `out` означає: «параметр T використовується лише як тип **значення, що повертається**». Тобто об'єкт типу T **виходить** з інтерфейсу (звідси `out`). У такому разі компілятор може гарантувати безпеку: якщо `Cardiologist : Doctor`, то всі кардіологи, яких повертає `IClinicFactory<Cardiologist>`, є і лікарями, тому `IClinicFactory<Cardiologist>` безпечно замінює `IClinicFactory<Doctor>`.

```csharp run
using System;

class Doctor
{
    public string Name { get; }
    public string Specialty { get; }

    public Doctor(string name, string specialty)
    {
        Name = name;
        Specialty = specialty;
    }

    public virtual void Introduce() =>
        Console.WriteLine($"Лікар {Name}, спеціальність: {Specialty}");
}

class Cardiologist : Doctor
{
    public Cardiologist(string name) : base(name, "Кардіологія") { }

    public override void Introduce() =>
        Console.WriteLine($"Кардіолог {Name}");
}

interface IClinicFactory<out T>
{
    T Create(string name);
}

class CardiologistFactory : IClinicFactory<Cardiologist>
{
    public Cardiologist Create(string name) => new Cardiologist(name);
}

class Program
{
    static void Main()
    {
        // Пряме використання
        IClinicFactory<Cardiologist> cardFactory = new CardiologistFactory();
        Cardiologist card = cardFactory.Create("Іваненко");
        card.Introduce();

        // Коваріантність: IClinicFactory<Cardiologist> → IClinicFactory<Doctor>
        IClinicFactory<Doctor> docFactory = cardFactory;
        Doctor doc = docFactory.Create("Петренко");
        doc.Introduce();

        Console.WriteLine();

        // Через проміжну змінну
        IClinicFactory<Cardiologist> src = new CardiologistFactory();
        IClinicFactory<Doctor> dst = src;   // [OK] коваріантність дозволяє
        Doctor created = dst.Create("Ковальчук");
        created.Introduce();
    }
}
```

**Обмеження коваріантного інтерфейсу**: параметр `T` з `out` можна використовувати **лише як тип, що повертається** — як тип вхідного аргументу методу він заборонений. Це гарантує, що через коваріантний інтерфейс не можна «записати» об'єкт неправильного типу.

### Контраваріантні інтерфейси (in)

Контраваріантний інтерфейс оголошується за допомогою ключового слова **`in`**:

```csharp
interface IDoctorHandler<in T>
{
    void Handle(T doctor);
}
```

Ключове слово `in` означає: «параметр T використовується лише як тип **вхідного аргументу**». Тобто об'єкт типу T **входить** у інтерфейс. Якщо `IDoctorHandler<Doctor>` вміє обробляти будь-якого лікаря, то він точно вміє обробляти і кардіолога (бо кардіолог є лікарем). Тому `IDoctorHandler<Doctor>` можна присвоїти `IDoctorHandler<Cardiologist>` — **зворотний** напрям відносно ієрархії.

```csharp run
using System;

class Doctor
{
    public string Name { get; }
    public Doctor(string name) { Name = name; }
}

class Cardiologist : Doctor
{
    public Cardiologist(string name) : base(name) { }
}

interface IDoctorHandler<in T>
{
    void Handle(T doctor);
}

class GeneralDoctorHandler : IDoctorHandler<Doctor>
{
    public void Handle(Doctor doctor) =>
        Console.WriteLine($"Обробляємо лікаря: {doctor.Name}");
}

class Program
{
    static void Main()
    {
        // Пряме використання
        IDoctorHandler<Doctor> generalHandler = new GeneralDoctorHandler();
        generalHandler.Handle(new Doctor("Ковальчук"));

        // Контраваріантність: IDoctorHandler<Doctor> → IDoctorHandler<Cardiologist>
        IDoctorHandler<Cardiologist> cardHandler = generalHandler;
        cardHandler.Handle(new Cardiologist("Іваненко"));

        Console.WriteLine();

        // Через проміжну змінну — теж працює
        IDoctorHandler<Doctor> src = new GeneralDoctorHandler();
        IDoctorHandler<Cardiologist> dst = src;  // [OK] контраваріантність
        dst.Handle(new Cardiologist("Петренко"));
    }
}
```

**Обмеження контраваріантного інтерфейсу**: параметр `T` з `in` можна використовувати **лише як тип вхідного аргументу** — як тип значення, що повертається, він заборонений. Це гарантує, що через контраваріантний інтерфейс не можна «прочитати» об'єкт неправильного типу.

### Поєднання коваріантності та контраваріантності

Один і той самий інтерфейс може мати кілька параметрів типу, одні з яких є `out`, а інші — `in`. Наприклад, інтерфейс клінічного месенджера, що **приймає** повідомлення одного типу і **повертає** відповідь іншого:

```csharp run
using System;

class Doctor
{
    public string Name { get; }
    public Doctor(string name) { Name = name; }
}

class Cardiologist : Doctor
{
    public Cardiologist(string name) : base(name) { }
}

class Report
{
    public string Text { get; }
    public Report(string text) { Text = text; }
}

class DetailedReport : Report
{
    public DetailedReport(string text) : base(text) { }
}

// in T — приймає повідомлення типу T
// out K — повертає відповідь типу K
interface IClinicMessenger<in T, out K>
{
    void Send(T request);
    K Receive();
}

class ClinicMessengerImpl : IClinicMessenger<Doctor, DetailedReport>
{
    private string _lastSender = "";

    public void Send(Doctor request)
    {
        _lastSender = request.Name;
        Console.WriteLine($"Повідомлення від {request.Name} отримано.");
    }

    public DetailedReport Receive() =>
        new DetailedReport($"Детальний звіт для {_lastSender}");
}

class Program
{
    static void Main()
    {
        ClinicMessengerImpl impl = new ClinicMessengerImpl();

        // Завдяки in T: IClinicMessenger<Doctor,...> → IClinicMessenger<Cardiologist,...>
        // Завдяки out K: IClinicMessenger<...,DetailedReport> → IClinicMessenger<...,Report>
        IClinicMessenger<Cardiologist, Report> messenger = impl;

        messenger.Send(new Cardiologist("Іваненко"));
        Report report = messenger.Receive();
        Console.WriteLine(report.Text);
    }
}
```

Завдяки обом модифікаторам об'єкт `ClinicMessengerImpl` (тип `IClinicMessenger<Doctor, DetailedReport>`) можна безпечно використовувати як `IClinicMessenger<Cardiologist, Report>` — контраваріантність по `T` (Doctor → Cardiologist, зворотний напрям) і коваріантність по `K` (DetailedReport → Report, прямий напрям).

### Правила і обмеження

| Модифікатор | Назва | Дозволено для T | Напрям присвоєння |
|---|---|---|---|
| `out T` | Коваріантний | Лише тип результату методу | `IFoo<Derived>` → `IFoo<Base>` |
| `in T` | Контраваріантний | Лише тип аргументу методу | `IFoo<Base>` → `IFoo<Derived>` |
| *(без модифікатора)* | Інваріантний | Будь-яке використання | Присвоєння заборонено |

Ці модифікатори доступні лише для **інтерфейсів** і **делегатів** — не для класів і структур. Саме тому в стандартній бібліотеці .NET такі інтерфейси, як `IEnumerable<out T>` (коваріантний) і `IComparer<in T>` (контраваріантний), ведуть себе інтуїтивно: послідовність кардіологів є послідовністю лікарів, а компаратор лікарів може порівнювати кардіологів.
