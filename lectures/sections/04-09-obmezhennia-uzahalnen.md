---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 9
number: "4.9"
title: "Обмеження узагальнень"
source: "../_combined/26-obmezhennia-uzahalnen.md"
---

## 4.9. Обмеження узагальнень

Узагальнені типи дозволяють використовувати будь-який тип як параметр. Але іноді всередині узагальненого класу чи методу необхідно звертатися до конкретних членів об'єкта — властивостей, методів. Компілятор не дозволить цього, якщо параметр `T` нічим не обмежений, бо у такому разі `T` може бути будь-яким типом, і немає гарантії, що потрібний член існує.

**Обмеження узагальнень** (generic constraints) через ключове слово `where` дозволяють вказати, яким типам відповідає параметр `T`. Це дає компілятору достатньо інформації для перевірки коректності звернень до членів.

## Проблема без обмежень

Розглянемо клінічний приклад. У нас є клас `Notification` з властивістю `Text`, і ми хочемо написати узагальнений метод `Send<T>`:

```csharp run
using System;

// Без обмеження — компілятор не знає що таке T
// і не дозволяє звертатися до message.Text

Notification sms   = new SmsNotification("Ваш прийом о 10:00");
Notification email = new EmailNotification("Нагадування про аналізи");

// Send(sms);  // помилка: T не має властивості Text

class Notification
{
    public string Text { get; }
    public Notification(string text) { Text = text; }
}

class SmsNotification : Notification
{
    public SmsNotification(string text) : base(text) {}
}

class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) {}
}
```

Якщо написати `void Send<T>(T message) { Console.WriteLine(message.Text); }` — компілятор видасть помилку: `T` може бути чим завгодно, і не факт, що в нього є `Text`. Саме тут на допомогу приходять обмеження.

## Обмеження методу: where T : ТипКласу

Обмеження методу вказується після списку параметрів через `where`:

```csharp run
using System;

Send(new SmsNotification("Ваш прийом о 10:00"));
Send(new EmailNotification("Нагадування про аналізи"));
Send<Notification>(new Notification("Загальне повідомлення"));

// Send("просто рядок");  // помилка компіляції — string не є Notification

void Send<T>(T message) where T : Notification
{
    // T гарантовано є Notification або похідним — Text доступний
    Console.WriteLine($"Надсилається: {message.Text}");
}

class Notification
{
    public string Text { get; }
    public Notification(string text) { Text = text; }
}

class SmsNotification : Notification
{
    public SmsNotification(string text) : base(text) {}
}

class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) {}
}
```

Вираз `where T : Notification` каже компілятору: «T — це завжди `Notification` або похідний від нього клас». Тому звернення до `message.Text` стає безпечним і дозволеним. При виклику `Send(new SmsNotification(...))` компілятор сам визначає `T = SmsNotification` — явно вказувати тип не обов'язково.

## Обмеження класу: where T : ТипКласу

Так само обмеження застосовуються до узагальнених класів. Синтаксис:

```
class Ім'яКласу<T> where T : ТипОбмеження
```

```csharp run
using System;

NotificationSender<SmsNotification> smsSender = new();
smsSender.Send(new SmsNotification("Підтвердження запису"));
smsSender.Send(new SmsNotification("Нагадування о 09:00"));

NotificationSender<EmailNotification> emailSender = new();
emailSender.Send(new EmailNotification("Результати аналізів готові"));

class NotificationSender<T> where T : Notification
{
    public void Send(T message)
    {
        Console.WriteLine($"[{typeof(T).Name}] {message.Text}");
    }
}

class Notification
{
    public string Text { get; }
    public Notification(string text) { Text = text; }
}

class SmsNotification : Notification
{
    public SmsNotification(string text) : base(text) {}
}

class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) {}
}
```

![Типи обмежень узагальнень у C#](_assets/04-09/constraints-overview.png)

## Стандартні обмеження: class, struct, new()

Окрім конкретних класів та інтерфейсів, є вбудовані обмеження:

**`where T : class`** — T має бути reference type (клас, інтерфейс, рядок):

```csharp run
using System;

Repository<Patient> repo = new();
repo.Add(new Patient("Іван Петренко", 45));
repo.Add(new Patient("Марія Сидоренко", 32));
repo.PrintAll();

class Repository<T> where T : class
{
    private T[] _items = new T[10];
    private int _count = 0;

    public void Add(T item) => _items[_count++] = item;

    public void PrintAll()
    {
        for (int i = 0; i < _count; i++)
            Console.WriteLine(_items[i]!.ToString());
    }
}

class Patient
{
    public string Name { get; }
    public int Age { get; }
    public Patient(string name, int age) { Name = name; Age = age; }
    public override string ToString() => $"Пацієнт: {Name}, {Age} р.";
}
```

**`where T : struct`** — T має бути value type (int, double, struct і т.д.):

```csharp run
using System;

MeasurementLog<int>    log1 = new("Пульс");
MeasurementLog<double> log2 = new("Температура");

log1.Add(72); log1.Add(80); log1.PrintAll();
log2.Add(36.6); log2.Add(37.2); log2.PrintAll();

class MeasurementLog<T> where T : struct
{
    private string _label;
    private T[] _values = new T[100];
    private int _count = 0;

    public MeasurementLog(string label) { _label = label; }
    public void Add(T value) => _values[_count++] = value;

    public void PrintAll()
    {
        Console.Write($"{_label}: ");
        for (int i = 0; i < _count; i++)
            Console.Write(_values[i].ToString() + " ");
        Console.WriteLine();
    }
}
```

**`where T : new()`** — T має публічний конструктор без параметрів. Це дозволяє всередині узагальненого класу створювати екземпляри типу `T` через `new T()`:

```csharp run
using System;

Factory<Patient> factory = new();
Patient p = factory.Create();
Console.WriteLine(p.ToString());

class Factory<T> where T : new()
{
    public T Create() => new T(); // можливо лише з обмеженням new()
}

class Patient
{
    public string Name { get; set; } = "Невідомий";
    public int Age { get; set; } = 0;
    public override string ToString() => $"Пацієнт: {Name}, {Age} р.";
}
```

## Обмеження за інтерфейсом

Як обмеження можна вказати **інтерфейс** — тоді T гарантовано реалізує всі члени цього інтерфейсу. Це дозволяє звертатися до методів інтерфейсу всередині узагальненого класу:

```csharp run
using System;

Sorter<int> sorter = new();
int[] ages = { 45, 32, 58, 27, 41 };
sorter.BubbleSort(ages);
foreach (int age in ages)
    Console.Write(age.ToString() + " "); // 27 32 41 45 58
Console.WriteLine();

class Sorter<T> where T : IComparable<T>
{
    public void BubbleSort(T[] array)
    {
        for (int i = 0; i < array.Length - 1; i++)
            for (int j = 0; j < array.Length - 1 - i; j++)
                if (array[j].CompareTo(array[j+1]) > 0)
                {
                    T temp = array[j];
                    array[j] = array[j+1];
                    array[j+1] = temp;
                }
    }
}
```

`IComparable<T>` гарантує наявність методу `CompareTo()`, тому сортування працює для будь-якого типу, що його реалізує: `int`, `string`, `DateTime`, або власний клас.

## Кілька обмежень одночасно

Для одного параметра можна задати кілька обмежень. Вони вказуються у строгому порядку: спочатку клас або `class`/`struct`, потім інтерфейси, в кінці `new()`:

```csharp run
using System;

MedicalProtocol<Patient, Doctor> protocol = new(
    new Patient("Іван Петренко", 45),
    new Doctor("Олена Коваль", 38, "Кардіологія"),
    "Обстеження серцево-судинної системи"
);
protocol.Execute();

class MedicalProtocol<TPatient, TDoctor>
    where TPatient : Patient, new()
    where TDoctor  : Doctor
{
    private TPatient _patient;
    private TDoctor  _doctor;
    private string   _purpose;

    public MedicalProtocol(TPatient patient, TDoctor doctor, string purpose)
    {
        _patient = patient;
        _doctor  = doctor;
        _purpose = purpose;
    }

    public void Execute()
    {
        Console.WriteLine($"Протокол: {_purpose}");
        Console.WriteLine($"  Пацієнт: {_patient.Name}, {_patient.Age} р.");
        Console.WriteLine($"  Лікар:   {_doctor.Name}, {_doctor.Specialization}");
    }
}

class Patient
{
    public string Name { get; set; } = "";
    public int Age { get; set; }
    public Patient() {}
    public Patient(string name, int age) { Name = name; Age = age; }
}

class Doctor
{
    public string Name { get; set; } = "";
    public int Age { get; set; }
    public string Specialization { get; set; } = "";
    public Doctor(string name, int age, string spec)
    { Name = name; Age = age; Specialization = spec; }
}
```

`where TPatient : Patient, new()` означає: `TPatient` повинен бути `Patient` або похідним класом **і** мати публічний конструктор без параметрів. Для різних параметрів типу обмеження задаються окремими рядками `where`.

## Порядок та правила обмежень

Кілька правил, які слід пам'ятати:

- Одночасно можна вказати лише одне з: конкретний клас, `class`, `struct` (вони несумісні між собою)
- Інтерфейсів може бути кілька
- `new()` завжди стоїть останнім
- `struct` несумісне з `new()` — структури за визначенням мають конструктор без параметрів

```csharp
// Правильно:
void Process<T>(T item) where T : Notification, new() { }

// Правильно — кілька інтерфейсів:
void Compare<T>(T a, T b) where T : class, IComparable<T>, IEquatable<T> { }

// Помилка — не можна одночасно class і struct:
// void Wrong<T>() where T : class, struct { }
```
