---
chapter: 21
chapterTitle: "Розділ 21. Generic Host та Dependency Injection"
section: 4
number: "21.4"
title: "Options Pattern — типізована конфігурація з IOptions<T>"
source: ""
---

## 21.4. Options Pattern — типізована конфігурація з IOptions&lt;T&gt;

Конфігурація — невід'ємна частина будь-якого реального додатку. Рядок підключення до бази даних, адреса SMTP-сервера, максимальна кількість записів у черзі, тайм-аути — усе це параметри, що змінюються між середовищами (`Development`, `Staging`, `Production`) і не повинні бути захардкоджені у коді. У .NET для роботи з конфігурацією існує ціла екосистема, центром якої є **Options Pattern**.

Options Pattern — це узгоджений підхід до читання конфігурації через типізовані класи. Замість читання рядків через `IConfiguration["Section:Key"]` скрізь по коду, ви оголошуєте POCO-клас (Plain Old C# Object), прив'язуєте його до секції конфігурації один раз при старті — і далі отримуєте через DI вже готовий, типізований, перевірений об'єкт.

## Проблема: IConfiguration по всьому коду

Розглянемо типову еволюцію роботи з конфігурацією без Options Pattern:

```csharp
// Антипаттерн: рядок ключа розкиданий по коду
class AppointmentService
{
    private readonly IConfiguration _config;
    public AppointmentService(IConfiguration config) { _config = config; }

    public void Book(...)
    {
        var maxPerDay = int.Parse(_config["Appointments:MaxPerDay"]); // magic string!
        var timeout   = TimeSpan.FromSeconds(
                            double.Parse(_config["Appointments:TimeoutSeconds"])); // дублювання!
        // ...
    }
}

class ReportService
{
    private readonly IConfiguration _config;
    public void Generate()
    {
        var maxPerDay = int.Parse(_config["Appointments:MaxPerDay"]); // ще раз дублювання
        // Якщо назву ключа зміните — помилка лише в runtime, не в compile time!
    }
}
```

Ця практика має щонайменше чотири вади:
1. **Magic strings** — будь-яка помилка в ключі виявляється лише у runtime
2. **Дублювання** — один ключ читається в десяти місцях
3. **Немає типізації** — `IConfiguration` повертає `string?`, потрібне ручне парсування
4. **Важко тестувати** — для тесту `AppointmentService` потрібно мокати весь `IConfiguration`

## Options Pattern: рішення

Options Pattern пропонує три кроки:

**1. Оголошення класу налаштувань:**
```csharp
class AppointmentOptions
{
    public int MaxPerDay    { get; set; } = 20;
    public int TimeoutSeconds { get; set; } = 30;
    public string AllowedStatuses { get; set; } = "Scheduled,Confirmed";
}
```

**2. Реєстрація і прив'язка до секції:**
```csharp
services.Configure<AppointmentOptions>(
    configuration.GetSection("Appointments"));
```

**3. Ін'єкція через `IOptions<T>`:**
```csharp
class AppointmentService
{
    private readonly AppointmentOptions _opts;
    public AppointmentService(IOptions<AppointmentOptions> opts)
        => _opts = opts.Value;

    public void Book(...)
    {
        if (_opts.MaxPerDay < 1) throw new ...;
        // Типізовано, з автодоповненням, без magic strings
    }
}
```

## Три варіанти IOptions

| Інтерфейс | Оновлення | Scope | Використання |
|---|---|---|---|
| `IOptions<T>` | ні (Singleton) | будь-який | типові налаштування |
| `IOptionsSnapshot<T>` | при кожному Scoped | Scoped | перезавантаження при зміні файлу |
| `IOptionsMonitor<T>` | реактивно (колбек) | Singleton | hot reload, повідомлення про зміни |

`IOptions<T>` реєструється як Singleton: значення зчитується один раз при запуску.
`IOptionsSnapshot<T>` — Scoped: якщо файл конфігурації змінився між двома HTTP-запитами, другий запит отримає нові значення.
`IOptionsMonitor<T>` — Singleton, але надає метод `OnChange(Action<T>)` для реакції на зміни в реальному часі.

## Реалізуємо Options Pattern «з нуля»

```csharp run
using System;
using System.Collections.Generic;

// ════════════════════════════════════════════════════════════════
// Options Pattern — повна самописна реалізація
// ════════════════════════════════════════════════════════════════

// ─── 1. Аналог IOptions<T> ───────────────────────────────────

interface IOptions<T> where T : class
{
    T Value { get; }
}

class Options<T> : IOptions<T> where T : class
{
    public T Value { get; }
    public Options(T value) => Value = value;
}

// ─── 2. Аналог IOptionsSnapshot<T> ──────────────────────────
// Snapshot читає конфіг щоразу заново (у нас — з Dictionary)

interface IOptionsSnapshot<T> where T : class
{
    T Value { get; }
}

// ─── 3. Аналог IOptionsMonitor<T> ────────────────────────────

interface IOptionsMonitor<T> where T : class
{
    T CurrentValue { get; }
    IDisposable OnChange(Action<T> listener);
}

// ─── 4. Джерело конфігурації (аналог appsettings.json) ───────

class ConfigurationSource
{
    private readonly Dictionary<string, string> _values;
    private readonly List<Action> _changeListeners = new();

    public ConfigurationSource(Dictionary<string, string> values)
        => _values = values;

    public string? Get(string key)
        => _values.TryGetValue(key, out var v) ? v : null;

    public void Set(string key, string value)
    {
        _values[key] = value;
        // Сповіщаємо слухачів про зміну
        foreach (var listener in _changeListeners) listener();
    }

    public void OnChange(Action callback) => _changeListeners.Add(callback);
}

// ─── 5. Прив'язка: конфіг → клас налаштувань ─────────────────

class ConfigurationBinder
{
    public static T Bind<T>(ConfigurationSource source, string prefix) where T : new()
    {
        var obj = new T();
        var props = typeof(T).GetProperties();
        foreach (var prop in props)
        {
            var key = string.IsNullOrEmpty(prefix)
                ? prop.Name
                : $"{prefix}:{prop.Name}";
            var raw = source.Get(key);
            if (raw is null) continue;

            object? converted = prop.PropertyType switch
            {
                var t when t == typeof(string)  => raw,
                var t when t == typeof(int)     => int.Parse(raw),
                var t when t == typeof(double)  => double.Parse(raw),
                var t when t == typeof(bool)    => bool.Parse(raw),
                var t when t == typeof(TimeSpan)=> TimeSpan.Parse(raw),
                _ => null
            };

            if (converted is not null) prop.SetValue(obj, converted);
        }
        return obj;
    }
}

// ════════════════════════════════════════════════════════════════
// Класи налаштувань (POCO — Plain Old C# Object)
// ════════════════════════════════════════════════════════════════

class DatabaseOptions
{
    public string ConnectionString { get; set; } = "Server=localhost;Database=clinic";
    public int MaxConnections      { get; set; } = 10;
    public int CommandTimeoutSec   { get; set; } = 30;
}

class SmtpOptions
{
    public string Host     { get; set; } = "smtp.localhost";
    public int    Port     { get; set; } = 587;
    public bool   UseSsl   { get; set; } = true;
    public string From     { get; set; } = "clinic@example.com";
}

class AppointmentOptions
{
    public int MaxPerDayPerDoctor { get; set; } = 20;
    public int ReminderHoursBefore { get; set; } = 24;
    public bool AutoConfirm { get; set; } = false;
}

// ════════════════════════════════════════════════════════════════
// Реалізація IOptionsMonitor з підтримкою OnChange
// ════════════════════════════════════════════════════════════════

class LiveOptionsMonitor<T> : IOptionsMonitor<T> where T : class, new()
{
    private readonly ConfigurationSource _source;
    private readonly string _prefix;
    private T _current;
    private readonly List<Action<T>> _listeners = new();

    public LiveOptionsMonitor(ConfigurationSource source, string prefix)
    {
        _source  = source;
        _prefix  = prefix;
        _current = ConfigurationBinder.Bind<T>(_source, _prefix);

        // При зміні конфігурації — перечитуємо і сповіщаємо
        _source.OnChange(() =>
        {
            _current = ConfigurationBinder.Bind<T>(_source, _prefix);
            foreach (var l in _listeners) l(_current);
        });
    }

    public T CurrentValue => _current;

    public IDisposable OnChange(Action<T> listener)
    {
        _listeners.Add(listener);
        return new Unsubscriber(() => _listeners.Remove(listener));
    }

    private class Unsubscriber : IDisposable
    {
        private readonly Action _remove;
        public Unsubscriber(Action remove) => _remove = remove;
        public void Dispose() => _remove();
    }
}

// ════════════════════════════════════════════════════════════════
// Сервіси, що використовують Options
// ════════════════════════════════════════════════════════════════

class DatabaseService
{
    private readonly DatabaseOptions _opts;

    public DatabaseService(IOptions<DatabaseOptions> opts)
        => _opts = opts.Value;

    public void Connect()
    {
        Console.WriteLine($"  [DB] Підключення до {_opts.ConnectionString}");
        Console.WriteLine($"  [DB] MaxConnections={_opts.MaxConnections.ToString()}, " +
                          $"Timeout={_opts.CommandTimeoutSec.ToString()}s");
    }
}

class NotificationService
{
    private readonly SmtpOptions _opts;

    public NotificationService(IOptions<SmtpOptions> opts)
        => _opts = opts.Value;

    public void SendReminder(string to, string message)
    {
        var ssl = _opts.UseSsl ? "SSL" : "plain";
        Console.WriteLine($"  [SMTP] {_opts.From} → {to} " +
                          $"via {_opts.Host}:{_opts.Port.ToString()} ({ssl})");
        Console.WriteLine($"         Повідомлення: {message}");
    }
}

class AppointmentService
{
    private readonly IOptionsMonitor<AppointmentOptions> _monitor;

    public AppointmentService(IOptionsMonitor<AppointmentOptions> monitor)
    {
        _monitor = monitor;
        // Реагуємо на зміни конфігурації в реальному часі
        _monitor.OnChange(opts =>
            Console.WriteLine($"  [!] Конфіг оновлено: MaxPerDay={opts.MaxPerDayPerDoctor.ToString()}"));
    }

    public void Book(string patient, string doctor)
    {
        var opts = _monitor.CurrentValue;
        var confirm = opts.AutoConfirm ? "автоматично підтверджено" : "очікує підтвердження";
        Console.WriteLine($"  [Appt] {patient} → {doctor} | {confirm} | " +
                          $"нагадування за {opts.ReminderHoursBefore.ToString()}год");
    }
}

// ════════════════════════════════════════════════════════════════
// Аналог ConfigureServices + appsettings.json
// ════════════════════════════════════════════════════════════════

class Program
{
    static void Main()
    {
        // ─── «appsettings.json» у вигляді Dictionary ─────────────
        var source = new ConfigurationSource(new Dictionary<string, string>
        {
            ["Database:ConnectionString"]  = "Server=prod-db;Database=clinic_prod",
            ["Database:MaxConnections"]    = "50",
            ["Database:CommandTimeoutSec"] = "60",
            ["Smtp:Host"]    = "smtp.clinic.ua",
            ["Smtp:Port"]    = "465",
            ["Smtp:UseSsl"]  = "true",
            ["Smtp:From"]    = "no-reply@clinic.ua",
            ["Appointments:MaxPerDayPerDoctor"]  = "15",
            ["Appointments:ReminderHoursBefore"] = "48",
            ["Appointments:AutoConfirm"]         = "false",
        });

        // ─── Реєстрація Options (аналог services.Configure<T>) ───
        IOptions<DatabaseOptions> dbOpts = new Options<DatabaseOptions>(
            ConfigurationBinder.Bind<DatabaseOptions>(source, "Database"));

        IOptions<SmtpOptions> smtpOpts = new Options<SmtpOptions>(
            ConfigurationBinder.Bind<SmtpOptions>(source, "Smtp"));

        IOptionsMonitor<AppointmentOptions> apptMonitor =
            new LiveOptionsMonitor<AppointmentOptions>(source, "Appointments");

        // ─── Використання сервісів ────────────────────────────────
        Console.WriteLine("=== Запуск сервісів ===\n");

        var dbService    = new DatabaseService(dbOpts);
        var notifyService = new NotificationService(smtpOpts);
        var apptService  = new AppointmentService(apptMonitor);

        dbService.Connect();

        Console.WriteLine();
        apptService.Book("Іваненко Олег",  "Лікар Петренко");
        apptService.Book("Мельник Ганна",  "Лікар Сидоренко");

        Console.WriteLine();
        notifyService.SendReminder("Іваненко Олег",
            "Нагадуємо про ваш прийом завтра о 10:00");

        // ─── Симуляція hot reload ─────────────────────────────────
        Console.WriteLine("\n=== Зміна конфігурації (hot reload) ===");
        source.Set("Appointments:MaxPerDayPerDoctor", "25");
        source.Set("Appointments:AutoConfirm",        "true");

        Console.WriteLine();
        apptService.Book("Коваль Дмитро", "Лікар Петренко");

        // ─── Перевірка IOptions (Singleton — не оновлюється) ─────
        Console.WriteLine("\n=== IOptions vs IOptionsMonitor ===");
        var staticOpts = new Options<AppointmentOptions>(
            ConfigurationBinder.Bind<AppointmentOptions>(source, "Appointments"));

        Console.WriteLine($"  IOptions MaxPerDay (зафіксовано): {staticOpts.Value.MaxPerDayPerDoctor.ToString()}");
        Console.WriteLine($"  IOptionsMonitor MaxPerDay (live): {apptMonitor.CurrentValue.MaxPerDayPerDoctor.ToString()}");
    }
}
```

## Валідація налаштувань

Реальний `IOptions` підтримує валідацію через Data Annotations або кастомний `IValidateOptions<T>`. Це дозволяє перевірити конфігурацію при запуску і не запускати додаток з некоректними налаштуваннями:

```csharp
using System.ComponentModel.DataAnnotations;

class DatabaseOptions
{
    [Required]
    [MinLength(10)]
    public string ConnectionString { get; set; } = "";

    [Range(1, 1000)]
    public int MaxConnections { get; set; } = 10;
}

// У реєстрації:
services.AddOptions<DatabaseOptions>()
        .Bind(configuration.GetSection("Database"))
        .ValidateDataAnnotations()     // перевірка через атрибути
        .ValidateOnStart();            // викид виключення при запуску, якщо невалідно
```

Це позволяє уникнути ситуацій, коли додаток запускається, але падає через відсутнє або некоректне значення конфігурації через кілька хвилин роботи.

## Named Options

Іноді потрібні кілька різних екземплярів одного класу налаштувань. Типовий приклад — два SMTP-сервери: один для транзакційних листів, інший для маркетингових:

```csharp
services.Configure<SmtpOptions>("Transactional",
    configuration.GetSection("Smtp:Transactional"));
services.Configure<SmtpOptions>("Marketing",
    configuration.GetSection("Smtp:Marketing"));

// Використання:
class EmailService
{
    private readonly SmtpOptions _transactional;
    private readonly SmtpOptions _marketing;

    public EmailService(IOptionsSnapshot<SmtpOptions> opts)
    {
        _transactional = opts.Get("Transactional");
        _marketing     = opts.Get("Marketing");
    }
}
```

![Options Pattern — IOptions, IOptionsSnapshot, IOptionsMonitor](_assets/21-04/options-pattern.png)

## Де зберігати конфігурацію

Generic Host автоматично завантажує конфігурацію з декількох джерел у порядку зростаючого пріоритету (кожне наступне перекриває попереднє):

1. `appsettings.json` — базова конфігурація для всіх середовищ
2. `appsettings.{Environment}.json` — специфічна для середовища (наприклад, `appsettings.Development.json`)
3. Секрети (User Secrets) — для чутливих даних у Development
4. Змінні середовища — стандартний спосіб конфігурації в контейнерах (Docker/Kubernetes)
5. Аргументи командного рядка — найвищий пріоритет, зручно для тестів та CI/CD

Чутливі дані (паролі, API-ключі, рядки з'єднань) **ніколи** не повинні потрапляти до `appsettings.json`, що зберігається у git. Для Production використовують змінні середовища або секретні сховища (Azure Key Vault, AWS Secrets Manager тощо).

## Підсумок

Options Pattern вирішує проблему розсипаної конфігурації так само, як DI вирішує проблему розсипаних залежностей: збирає все в одному місці, дає типізацію і перевірку при запуску, і надає через DI вже готовий об'єкт — без magic strings і ручного парсування. Разом Generic Host, `IServiceCollection` і Options Pattern утворюють повну інфраструктуру для побудови добре структурованих, конфігурованих і тестованих .NET-додатків.
