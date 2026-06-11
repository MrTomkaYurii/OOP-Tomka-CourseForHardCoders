---
chapter: 13
chapterTitle: "Розділ 13. Додаткові класи та структури .NET"
section: 1
number: "13.1"
title: "Відкладена ініціалізація та тип Lazy<T>"
source: "../_combined/78-vidkladena-initsializatsiia-ta-typ-lazy.md"
---

## 13.1. Відкладена ініціалізація та тип `Lazy<T>`

У реальних застосунках, зокрема медичних інформаційних системах, далеко не кожен об'єкт потрібний при кожному запуску програми. Наприклад, клас `PatientRecord` може містити посилання на об'єкт, що завантажує повну медичну картку пацієнта з бази даних — але лікар відкриває детальний вигляд лише для деяких пацієнтів. Якщо завантажувати картку завжди при створенні `PatientRecord`, програма даремно витрачатиме час і пам'ять на дані, які ніхто не переглядатиме.

Це фундаментальний компроміс: **ініціалізувати заздалегідь** (eager) означає завжди бути готовим, але платити вартість навіть за непотрібні об'єкти; **ініціалізувати відкладено** (lazy) означає нести витрати тільки тоді, коли об'єкт справді потрібен.

![Lazy\<T\> — відкладена ініціалізація: Eager vs Lazy](_assets/13-01/lazy-init.png)

## Проблема eager-ініціалізації

Розглянемо клас читача, який зберігає посилання на бібліотеку — об'єкт, що займає значну кількість пам'яті:

```csharp
class Reader
{
    Library library = new Library(); // створюється ЗАВЖДИ при new Reader()

    public void ReadBook()
    {
        library.GetBook();
        Console.WriteLine("Читаємо паперову книгу");
    }

    public void ReadEbook()
    {
        Console.WriteLine("Читаємо книгу на комп'ютері");
    }
}

class Library
{
    private string[] books = new string[99]; // займає пам'ять

    public void GetBook()
    {
        Console.WriteLine("Видаємо книгу читачеві");
    }
}
```

Якщо читач використовує лише електронні книги:

```csharp
Reader reader = new Reader();
reader.ReadEbook(); // library нікуди не використовується, але вже в пам'яті
```

Об'єкт `library` вже виділив пам'ять під масив книг, хоча він ніколи не буде використаний. У клінічному контексті це може бути об'єкт, що завантажує тисячі записів аналізів, будує кеш нормативів або відкриває з'єднання з базою даних — усе це відбувається навіть тоді, коли поточний сценарій використання не потребує цих даних.

## Клас `Lazy<T>` — відкладений обгортувач

Для вирішення цієї проблеми .NET надає узагальнений клас `Lazy<T>`. Він є легким обгортувачем (wrapper): сам по собі `Lazy<T>` займає мінімум пам'яті і не створює об'єкт `T` до першого звернення через властивість `Value`.

Перепишемо клас читача:

```csharp
class Reader
{
    Lazy<Library> library = new Lazy<Library>();

    public void ReadBook()
    {
        library.Value.GetBook(); // .Value — перший виклик створює Library
        Console.WriteLine("Читаємо паперову книгу");
    }

    public void ReadEbook()
    {
        Console.WriteLine("Читаємо книгу на комп'ютері");
    }
}
```

Тепер при `new Reader()` об'єкт `Library` **не створюється** — лише легкий `Lazy<Library>`. Об'єкт `Library` з'явиться в heap тільки при першому виклику `library.Value`, тобто тільки якщо хтось викликав `ReadBook()`.

## Конструктори Lazy\<T\>

`Lazy<T>()` без параметрів вимагає, щоб `T` мав публічний конструктор без параметрів — він буде викликаний при першому зверненні до `Value`:

```csharp
Lazy<Library> library = new Lazy<Library>(); // new Library() відкладено
```

Якщо потрібна **фабрична функція** (конструктор з параметрами або складна ініціалізація), передається лямбда:

```csharp
Lazy<PatientHistory> history = new Lazy<PatientHistory>(
    () => new PatientHistory(patientId, connectionString));
```

Це найпоширеніший варіант у реальному коді: завдяки замиканню лямбда може захопити будь-які необхідні аргументи, доступні на момент оголошення поля.

## Властивості Value та IsValueCreated

**`Value`** — єдина точка доступу до обгорнутого об'єкта. При першому зверненні викликає фабрику або конструктор і кешує результат. Усі наступні звернення повертають той самий кешований об'єкт миттєво:

```csharp
Lazy<Library> library = new Lazy<Library>();

// Перше звернення — тригер ініціалізації
var lib1 = library.Value; // new Library() викликається тут

// Наступні звернення — кеш, без повторного виклику конструктора
var lib2 = library.Value; // той самий об'єкт, що й lib1
Console.WriteLine(object.ReferenceEquals(lib1, lib2)); // true
```

**`IsValueCreated`** — властивість типу `bool`, яка дозволяє **перевірити** стан без запуску ініціалізації:

```csharp
Lazy<Library> library = new Lazy<Library>();

Console.WriteLine(library.IsValueCreated); // false — ще не створено
var lib = library.Value;                   // ініціалізація тут
Console.WriteLine(library.IsValueCreated); // true
```

Це корисно в сценаріях, де потрібно з'ясувати, чи вже виконувалася дорога операція — наприклад, для виведення стану кешу в діагностиці або логуванні.

## Потокова безпека: LazyThreadSafetyMode

Третій параметр конструктора `Lazy<T>` — режим потокової безпеки:

```csharp
// За замовчуванням: ExecutionAndPublication
Lazy<Service> s1 = new Lazy<Service>(
    () => new Service(),
    LazyThreadSafetyMode.ExecutionAndPublication);

// Без синхронізації (однопотоковий код)
Lazy<Service> s2 = new Lazy<Service>(
    () => new Service(),
    LazyThreadSafetyMode.None);
```

| Режим | Поведінка | Коли обирати |
|-------|-----------|-------------|
| `ExecutionAndPublication` | Тільки один потік виконує ініціалізацію; решта чекають | За замовчуванням, якщо є ризик конкурентного доступу |
| `PublicationOnly` | Кілька потоків можуть ініціалізувати паралельно; збережеться перший результат | Якщо ініціалізація ідемпотентна і без побічних ефектів |
| `None` | Жодної синхронізації | Тільки для однопотокових сценаріїв |

У типових додатках без явного багатопотоку (наприклад, у веб-запитах, де кожен запит має свій потік) достатньо значення за замовчуванням.

## Медична картка з відкладеним завантаженням — runnable приклад

Демонструємо `IsValueCreated` та момент ініціалізації:

```csharp run
using System;

class PatientRecord
{
    public string Name { get; }
    public string IcdCode { get; }

    // Анамнез — важкий об'єкт, завантажується лише при потребі
    private Lazy<string[]> _history;

    public PatientRecord(string name, string icd)
    {
        Name    = name;
        IcdCode = icd;
        // Фабрика захоплює Name через замикання
        _history = new Lazy<string[]>(() => LoadHistory(name));
    }

    private static string[] LoadHistory(string name)
    {
        Console.WriteLine($"  [ЗАВАНТАЖЕННЯ анамнезу: {name}]");
        return new[] {
            $"2024-01 — первинний огляд",
            $"2024-06 — призначення лікування",
            $"2026-06 — плановий контроль",
        };
    }

    public bool IsHistoryLoaded => _history.IsValueCreated;
    public string[] History => _history.Value; // тригер
}

var p1 = new PatientRecord("Петренко Іван", "I10.9");
var p2 = new PatientRecord("Коваль Марія",  "J45.0");

Console.WriteLine("=== Списку пацієнтів ===");
Console.WriteLine($"{p1.Name} | {p1.IcdCode} | Анамнез завантажено: {p1.IsHistoryLoaded}");
Console.WriteLine($"{p2.Name} | {p2.IcdCode} | Анамнез завантажено: {p2.IsHistoryLoaded}");

Console.WriteLine("\n=== Лікар відкриває картку Петренка ===");
foreach (var item in p1.History)
    Console.WriteLine($"  • {item}");

Console.WriteLine($"\nПетренко: IsHistoryLoaded = {p1.IsHistoryLoaded}");
Console.WriteLine($"Коваль:   IsHistoryLoaded = {p2.IsHistoryLoaded}");
Console.WriteLine("(Анамнез Коваль так і не завантажено — економія ресурсів)");
```

## Сервіс нормативів — runnable приклад

`Lazy<T>` для відкладеної побудови кешу нормативних значень аналізів:

```csharp run
using System;
using System.Collections.Generic;

class LabNormService
{
    // Таблиця норм будується один раз при першому зверненні
    private static readonly Lazy<Dictionary<string, (double Min, double Max, string Unit)>> _norms
        = new Lazy<Dictionary<string, (double, double, string)>>(() =>
        {
            Console.WriteLine("  [ІНІЦІАЛІЗАЦІЯ таблиці норм — відбувається один раз]");
            return new Dictionary<string, (double, double, string)>
            {
                ["glucose"]      = (3.9,  6.1,  "ммоль/л"),
                ["hemoglobin"]   = (120,  160,  "г/л"),
                ["erythrocytes"] = (3.8,  5.2,  "10¹²/л"),
                ["leukocytes"]   = (4.0,  9.0,  "10⁹/л"),
                ["cholesterol"]  = (0,    5.2,  "ммоль/л"),
            };
        });

    public static (bool ok, string msg) Check(string test, double value)
    {
        var norms = _norms.Value; // тригер при першому виклику
        if (!norms.TryGetValue(test, out var norm))
            return (false, $"Невідомий показник: {test}");

        bool ok = value >= norm.Min && value <= norm.Max;
        string status = ok ? "НОРМА" : (value < norm.Min ? "НИЖЧЕ НОРМИ" : "ВИЩЕ НОРМИ");
        return (ok, $"{value:F2} {norm.Unit} [{norm.Min}–{norm.Max}] → {status}");
    }
}

Console.WriteLine("=== Лабораторні показники — Петренко Іван ===");
Console.WriteLine($"IsValueCreated перед першим зверненням: (перевіряємо через Check)");
Console.WriteLine();

var results = new[]
{
    ("glucose",      7.3),
    ("hemoglobin",   135.0),
    ("leukocytes",   11.5),
    ("cholesterol",  4.8),
    ("erythrocytes", 4.2),
};

foreach (var (test, val) in results)
{
    var (ok, msg) = LabNormService.Check(test, val);
    string mark = ok ? "✓" : "!";
    Console.WriteLine($"  [{mark}] {test,-14}: {msg}");
}
```
