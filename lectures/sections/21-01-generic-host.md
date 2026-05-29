---
chapter: 21
chapterTitle: "Розділ 21. Generic Host та Dependency Injection"
section: 1
number: "21.1"
title: "Generic Host — архітектура та життєвий цикл додатку"
source: ""
---

## 21.1. Generic Host — архітектура та життєвий цикл додатку

Будь-який реальний додаток потребує більше, ніж просто виконання рядків коду зверху вниз. Йому потрібно запуститися, налаштуватись, підключитись до баз даних, логерів, черг повідомлень, дочекатись сигналу зупинки і правильно завершити роботу — зберегти стан, закрити з'єднання, завершити незакінчені операції. Якщо все це реалізовувати вручну у кожному проекті, код `Main()` перетвориться на величезний монолітний метод, а будь-яка зміна в порядку ініціалізації ризикує зламати всю систему.

Саме для вирішення цієї проблеми Microsoft у .NET Core 2.1 (2018) ввів концепцію **Generic Host** (`Microsoft.Extensions.Hosting`). Generic Host — це інфраструктурна оболонка, що бере на себе відповідальність за **управління життєвим циклом додатку**: запуск, виконання фонових сервісів, обробку сигналів завершення і коректний shutdown. До цього аналогічний механізм існував лише для ASP.NET Core (WebHost), але з появою Generic Host він став доступним для будь-якого типу додатків — консольних, Windows Services, worker services, мікросервісів.

## Проблема: «розсипаний» Main без хоста

Розглянемо типову еволюцію консольного додатку для клінічної системи. Спочатку все здається простим:

```csharp run
using System;
using System.Collections.Generic;
using System.Threading;

// ─── Проблема: Main без хоста ─────────────────────────────────────
// Усе в одному місці. З кожним тижнем Main росте.

class DatabaseConnection
{
    public string ConnectionString { get; }
    public DatabaseConnection(string cs) { ConnectionString = cs; }
    public void Open()  { Console.WriteLine($"[DB] Відкрито: {ConnectionString}"); }
    public void Close() { Console.WriteLine("[DB] З'єднання закрито"); }
}

class AppointmentService
{
    private readonly DatabaseConnection _db;
    private readonly bool _sendNotifications;

    // AppointmentService сам створює залежності — порушення DIP
    public AppointmentService()
    {
        _db = new DatabaseConnection("Server=prod;Database=clinic"); // hardcoded!
        _sendNotifications = true;
    }

    public void BookAppointment(string patient, string doctor)
    {
        Console.WriteLine($"[Service] Бронювання: {patient} -> {doctor}");
    }
}

class ReportService
{
    // ReportService теж сам знає про рядок з'єднання
    private readonly DatabaseConnection _db =
        new DatabaseConnection("Server=prod;Database=clinic"); // дублювання!

    public void GenerateMonthlyReport()
    {
        Console.WriteLine("[Report] Генерується місячний звіт...");
    }
}

class Program
{
    static void Main(string[] args)
    {
        // ─── Проблеми цього підходу ───────────────────────────────
        // 1. Кожен сервіс сам створює свої залежності (немає DI)
        // 2. Рядки конфігурації розкидані по коду
        // 3. Немає єдиного місця для ініціалізації ресурсів
        // 4. Немає обробки Ctrl+C / сигналів завершення
        // 5. Не зрозумілий порядок shutdown (що закривати першим?)

        Console.WriteLine("=== Запуск клінічної системи (БЕЗ хоста) ===");

        var db = new DatabaseConnection("Server=prod;Database=clinic");
        db.Open();

        var appointmentService = new AppointmentService();
        var reportService = new ReportService();

        appointmentService.BookAppointment("Іваненко О.", "Лікар Петренко");
        reportService.GenerateMonthlyReport();

        // Немає обробки Ctrl+C — додаток просто завершиться або зависне
        Console.WriteLine("Натисніть Enter для завершення...");
        Console.ReadLine();

        db.Close();
        // А якщо між db.Open() та db.Close() трапиться виняток?
        // З'єднання залишиться відкритим назавжди.
    }
}
```

Цей код має щонайменше п'ять структурних проблем. Жодна з них не критична сама по собі — але разом вони перетворюють додаток на крихку конструкцію, яку важко розширювати й майже неможливо тестувати.

## Що таке Generic Host

**Generic Host** — це об'єкт типу `IHost`, що виконує три ролі одночасно:

**1. Service Container (DI-контейнер)** — зберігає реєстрацію всіх сервісів і відповідає за їхнє створення та управління їхнім часом життя. Замість того, щоб кожен клас сам створював свої залежності через `new`, він отримує їх через конструктор — а контейнер знає, як їх побудувати.

**2. Configuration Provider** — агрегує конфігурацію з різних джерел: `appsettings.json`, змінні середовища, аргументи командного рядка, секрети — і надає єдиний уніфікований доступ через `IConfiguration`.

**3. Lifecycle Manager** — відстежує стан додатку, запускає фонові сервіси (`IHostedService`), перехоплює системні сигнали (`SIGTERM`, `Ctrl+C`) і гарантує коректний порядок зупинки компонентів.

```
┌─────────────────────────── IHost ────────────────────────────────┐
│                                                                   │
│   ┌─────────────────┐   ┌──────────────────┐   ┌─────────────┐  │
│   │ IServiceProvider│   │ IConfiguration   │   │  Lifecycle  │  │
│   │ (DI Container)  │   │ (Config Sources) │   │  Manager    │  │
│   └─────────────────┘   └──────────────────┘   └─────────────┘  │
│          │                       │                     │          │
│    реєстрація             appsettings.json        Start / Stop   │
│    та resolve             env variables          IHostedService   │
│    сервісів               cmd args               CancellationToken│
└─────────────────────────────────────────────────────────────────┘
```

## Архітектура: Builder Pattern для хоста

Generic Host будується за **Builder Pattern**: спочатку конфігурується `IHostBuilder`, потім викликається `.Build()` і отримується `IHost`. Реальний API виглядає так:

```csharp
// Реальний код з Microsoft.Extensions.Hosting (не runnable в браузері)
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;

IHost host = Host.CreateDefaultBuilder(args)
    .ConfigureServices(services =>
    {
        // Реєструємо сервіси
        services.AddSingleton<DatabaseConnection>();
        services.AddScoped<AppointmentService>();
        services.AddTransient<ReportService>();
    })
    .Build();

await host.RunAsync();
```

`Host.CreateDefaultBuilder()` — це фабричний метод, що автоматично налаштовує:
- завантаження `appsettings.json` та `appsettings.{Environment}.json`
- читання змінних середовища з префіксом `DOTNET_`
- читання аргументів командного рядка
- базове логування в консоль та Debug
- встановлення кореневого каталогу додатку

## Реалізуємо спрощений хост «з нуля»

Щоб зрозуміти, що відбувається всередині `IHost`, побудуємо власну спрощену реалізацію. Це найкращий спосіб зрозуміти будь-яку інфраструктурну абстракцію — побудувати її самостійно.

```csharp run
using System;
using System.Collections.Generic;
using System.Threading;

// ═══════════════════════════════════════════════════════════════
// КРОК 1: Сервіси та інтерфейси
// ═══════════════════════════════════════════════════════════════

interface IPatientRepository
{
    void Save(string patientName);
    List<string> GetAll();
}

interface INotificationService
{
    void Send(string recipient, string message);
}

class InMemoryPatientRepository : IPatientRepository
{
    private readonly List<string> _patients = new();

    public void Save(string patientName)
    {
        _patients.Add(patientName);
        Console.WriteLine($"  [Repo] Збережено пацієнта: {patientName}");
    }

    public List<string> GetAll() => _patients;
}

class ConsoleNotificationService : INotificationService
{
    public void Send(string recipient, string message)
    {
        Console.WriteLine($"  [Notify] -> {recipient}: {message}");
    }
}

class AppointmentService
{
    private readonly IPatientRepository _repo;
    private readonly INotificationService _notify;

    // Залежності отримуємо через конструктор — ніяких new усередині!
    public AppointmentService(
        IPatientRepository repo,
        INotificationService notify)
    {
        _repo   = repo;
        _notify = notify;
    }

    public void RegisterPatient(string name)
    {
        _repo.Save(name);
        _notify.Send(name, "Вас зареєстровано у клініці. Ласкаво просимо!");
    }

    public void PrintAllPatients()
    {
        var all = _repo.GetAll();
        Console.WriteLine($"  [Service] Усього пацієнтів: {all.Count.ToString()}");
        foreach (var p in all)
            Console.WriteLine($"    - {p}");
    }
}

// ═══════════════════════════════════════════════════════════════
// КРОК 2: Спрощений DI-контейнер
// ═══════════════════════════════════════════════════════════════

class SimpleServiceCollection
{
    // Зберігаємо фабрики: тип → функція створення об'єкта
    private readonly Dictionary<Type, Func<SimpleServiceProvider, object>> _factories = new();

    public void AddSingleton<TService, TImplementation>()
        where TImplementation : TService
    {
        object? instance = null;
        _factories[typeof(TService)] = provider =>
        {
            // Singleton: один екземпляр на весь час роботи
            instance ??= provider.Resolve(typeof(TImplementation));
            return instance!;
        };
        _factories[typeof(TImplementation)] = provider =>
            (TImplementation)Activator.CreateInstance(typeof(TImplementation),
                GetConstructorArgs(typeof(TImplementation), provider))!;
    }

    public void AddTransient<TService, TImplementation>()
        where TImplementation : TService
    {
        _factories[typeof(TService)] = provider =>
            // Transient: новий екземпляр при кожному запиті
            provider.Resolve(typeof(TImplementation));

        _factories[typeof(TImplementation)] = provider =>
            (TImplementation)Activator.CreateInstance(typeof(TImplementation),
                GetConstructorArgs(typeof(TImplementation), provider))!;
    }

    private object[] GetConstructorArgs(Type type, SimpleServiceProvider provider)
    {
        var ctor = type.GetConstructors()[0];
        var parameters = ctor.GetParameters();
        var args = new object[parameters.Length];
        for (int i = 0; i < parameters.Length; i++)
            args[i] = provider.Resolve(parameters[i].ParameterType);
        return args;
    }

    public SimpleServiceProvider BuildServiceProvider()
        => new SimpleServiceProvider(_factories);
}

class SimpleServiceProvider
{
    private readonly Dictionary<Type, Func<SimpleServiceProvider, object>> _factories;

    public SimpleServiceProvider(Dictionary<Type, Func<SimpleServiceProvider, object>> factories)
        => _factories = factories;

    public object Resolve(Type type)
    {
        if (_factories.TryGetValue(type, out var factory))
            return factory(this);
        throw new InvalidOperationException($"Сервіс не зареєстрований: {type.Name}");
    }

    public T Resolve<T>() => (T)Resolve(typeof(T));
}

// ═══════════════════════════════════════════════════════════════
// КРОК 3: Спрощений хост із lifecycle management
// ═══════════════════════════════════════════════════════════════

interface IHostedService
{
    void Start();
    void Stop();
}

class SimpleHost
{
    private readonly SimpleServiceProvider _services;
    private readonly List<IHostedService> _hostedServices = new();
    private readonly CancellationTokenSource _cts = new();

    public SimpleHost(SimpleServiceProvider services) => _services = services;

    public SimpleServiceProvider Services => _services;

    public void AddHostedService(IHostedService service)
        => _hostedServices.Add(service);

    public void Run()
    {
        Console.WriteLine("[Host] Запуск хоста...");

        // Запуск усіх фонових сервісів
        foreach (var svc in _hostedServices)
        {
            Console.WriteLine($"[Host] Запуск {svc.GetType().Name}");
            svc.Start();
        }

        Console.WriteLine("[Host] Хост запущено. Натисніть Ctrl+C або Enter для зупинки.");
        Console.ReadLine(); // У реальному хості тут — очікування CancellationToken

        Shutdown();
    }

    private void Shutdown()
    {
        Console.WriteLine("[Host] Отримано сигнал зупинки...");
        // Зупинка у зворотному порядку — важливо!
        for (int i = _hostedServices.Count - 1; i >= 0; i--)
        {
            Console.WriteLine($"[Host] Зупинка {_hostedServices[i].GetType().Name}");
            _hostedServices[i].Stop();
        }
        Console.WriteLine("[Host] Хост зупинено.");
    }
}

// ═══════════════════════════════════════════════════════════════
// КРОК 4: Фоновий сервіс
// ═══════════════════════════════════════════════════════════════

class AppointmentReminderService : IHostedService
{
    private readonly INotificationService _notify;

    public AppointmentReminderService(INotificationService notify)
        => _notify = notify;

    public void Start()
    {
        Console.WriteLine("  [Reminder] Сервіс нагадувань активовано");
        // У реальному коді тут запускається Timer або Task з циклом
        _notify.Send("Всі пацієнти з прийомом завтра",
                     "Нагадуємо про ваш прийом о 10:00");
    }

    public void Stop()
        => Console.WriteLine("  [Reminder] Сервіс нагадувань зупинено");
}

// ═══════════════════════════════════════════════════════════════
// КРОК 5: Збираємо все разом — аналог Program.cs з Generic Host
// ═══════════════════════════════════════════════════════════════

class Program
{
    static void Main()
    {
        // ─── Реєстрація сервісів (аналог ConfigureServices) ──────
        var services = new SimpleServiceCollection();
        services.AddSingleton<IPatientRepository, InMemoryPatientRepository>();
        services.AddTransient<INotificationService, ConsoleNotificationService>();
        services.AddTransient<AppointmentService, AppointmentService>();

        var provider = services.BuildServiceProvider();

        // ─── Будуємо хост ────────────────────────────────────────
        var host = new SimpleHost(provider);

        // Додаємо фоновий сервіс
        var reminderNotify = provider.Resolve<INotificationService>();
        host.AddHostedService(new AppointmentReminderService(reminderNotify));

        // ─── Використовуємо сервіси через DI ─────────────────────
        Console.WriteLine("\n=== Реєстрація пацієнтів ===");
        var apptService = provider.Resolve<AppointmentService>();
        apptService.RegisterPatient("Іваненко Олег");
        apptService.RegisterPatient("Мельник Ганна");
        apptService.RegisterPatient("Коваль Дмитро");

        Console.WriteLine("\n=== Список пацієнтів ===");
        apptService.PrintAllPatients();

        // ─── Демонстрація Singleton ───────────────────────────────
        Console.WriteLine("\n=== Перевірка Singleton (IPatientRepository) ===");
        var repo1 = provider.Resolve<IPatientRepository>();
        var repo2 = provider.Resolve<IPatientRepository>();
        Console.WriteLine($"  repo1 == repo2: {object.ReferenceEquals(repo1, repo2).ToString()}");
        // Singleton → той самий об'єкт
    }
}
```

## Ключові компоненти реального Generic Host

Розглянемо API, що ви побачите у реальному коді .NET-проектів:

**`IHost`** — центральний інтерфейс. Надає доступ до `IServiceProvider` через властивість `Services`. Методи `StartAsync()` / `StopAsync()` / `RunAsync()` керують lifecycle.

**`IHostBuilder`** — будівельник хоста. Надає fluent API для конфігурації:
- `ConfigureServices(Action<IServiceCollection>)` — реєстрація сервісів
- `ConfigureAppConfiguration(Action<IConfigurationBuilder>)` — додаткові джерела конфігурації
- `ConfigureLogging(Action<ILoggingBuilder>)` — налаштування логування
- `UseEnvironment(string)` — встановлення середовища (`Development`, `Production`)

**`IHostedService`** — інтерфейс фонового сервісу. Два методи: `StartAsync(CancellationToken)` і `StopAsync(CancellationToken)`. Хост запускає всі зареєстровані `IHostedService` при старті і зупиняє у зворотному порядку при shutdown.

**`BackgroundService`** — абстрактний базовий клас, що реалізує `IHostedService`. Достатньо перевизначити один метод: `ExecuteAsync(CancellationToken stoppingToken)` — і писати в ньому нескінченний цикл або очікування.

![Generic Host — архітектура та потік запуску](_assets/21-01/host-architecture.png)

## Порядок старту та shutdown

Розуміння порядку є критичним для коректної роботи:

**Запуск:**
1. `IHostBuilder.Build()` — збирається DI-контейнер, перевіряється реєстрація
2. `IHost.StartAsync()` — послідовно викликає `StartAsync()` у кожного `IHostedService` у порядку реєстрації
3. Хост входить у стан «running» і чекає сигналу зупинки

**Shutdown** (при `Ctrl+C`, `SIGTERM` або явному виклику `StopAsync()`):
1. `IHostApplicationLifetime` сповіщає підписників `ApplicationStopping`
2. `IHost.StopAsync()` — послідовно викликає `StopAsync()` у кожного `IHostedService` **у зворотному порядку**
3. `IHostApplicationLifetime` сповіщає підписників `ApplicationStopped`
4. DI-контейнер диспозиться — викликається `Dispose()` на всіх `IDisposable` singleton-сервісах

Зворотний порядок shutdown є навмисним і важливим: перший зупинений сервіс може залежати від ресурсів, що надають пізніше зупинені сервіси. Наприклад, `EmailSender` (зупиняється першим) може надсилати `Shutdown notification` через `SmtpClient` (зупиняється останнім).

## Generic Host vs WebApplication

Починаючи з .NET 6, для ASP.NET Core проектів з'явився `WebApplication` — ще більш спрощений API (`var app = WebApplication.Create()`). Він побудований поверх Generic Host і фактично є синтаксичним цукром для найпоширенішого сценарію — веб-додатків. Для консольних програм, Worker Services, мікросервісів без HTTP — Generic Host залишається правильним вибором.

| | Generic Host | WebApplication |
|---|---|---|
| Тип додатку | будь-який | ASP.NET Core |
| NuGet пакет | `Microsoft.Extensions.Hosting` | `Microsoft.AspNetCore.App` |
| HTTP pipeline | немає | є (middleware) |
| Запуск | `host.RunAsync()` | `app.RunAsync()` |
| IServiceCollection | `ConfigureServices()` | `builder.Services` |

## Підсумок

Generic Host вирішує проблему «розсипаного Main» шляхом введення чіткої відповідальності: хост знає про lifecycle, конфігурацію і контейнер сервісів — а бізнес-код нічого цього не знає і не зобов'язаний знати. Це пряме втілення принципів SRP та DIP зі SOLID: кожна частина системи відповідає за одне, і залежності течуть через абстракції.
