---
chapter: 21
chapterTitle: "Розділ 21. Generic Host та Dependency Injection"
section: 2
number: "21.2"
title: "IServiceCollection — реєстрація та розпізнавання сервісів"
source: ""
---

## 21.2. IServiceCollection — реєстрація та розпізнавання сервісів

У попередньому розділі ми побачили, що Generic Host бере на себе управління lifecycle і надає DI-контейнер. Сам контейнер будується в два окремі кроки: спочатку **реєстрація** (`IServiceCollection`), потім **розпізнавання** (`IServiceProvider`). Це навмисне розділення: список зареєстрованих сервісів формується один раз при запуску, а потім контейнер стає незмінним — жоден код у runtime не може додати новий сервіс або змінити вже зареєстрований.

Розуміння того, що саме зберігається в колекції сервісів і як контейнер вирішує, який об'єкт повернути, — це ключ до ефективної роботи з будь-яким DI-фреймворком у .NET.

## ServiceDescriptor: атомарна одиниця реєстрації

Кожна реєстрація в `IServiceCollection` — це один об'єкт `ServiceDescriptor`. Він містить три речі:

```
ServiceDescriptor
├── ServiceType   : Type      — який тип запитується (зазвичай інтерфейс)
├── ImplementationType / ImplementationFactory / ImplementationInstance
│                             — як створити об'єкт
└── Lifetime      : ServiceLifetime — Singleton | Scoped | Transient
```

Коли контейнер отримує запит на `IPatientRepository`, він шукає `ServiceDescriptor` з `ServiceType == typeof(IPatientRepository)`, дивиться на lifetime, і за допомогою `ImplementationType` або фабрики (`ImplementationFactory`) створює або повертає вже існуючий екземпляр.

## Три способи реєстрації

Реальний `IServiceCollection` надає три перевантажені методи, що відповідають трьом ситуаціям:

**Реєстрація через тип** — найчастіша форма:
```csharp
services.AddSingleton<IPatientRepository, SqlPatientRepository>();
services.AddScoped<AppointmentService>();          // ServiceType == ImplementationType
services.AddTransient<INotificationService, SmtpNotificationService>();
```

**Реєстрація через фабрику** — коли потрібна додаткова логіка при створенні:
```csharp
services.AddSingleton<IPatientRepository>(provider =>
{
    var config = provider.GetRequiredService<IConfiguration>();
    var connStr = config["Database:ConnectionString"];
    return new SqlPatientRepository(connStr);
});
```

**Реєстрація через готовий екземпляр** — тільки для Singleton (об'єкт уже існує):
```csharp
var sharedCache = new MemoryCache();
services.AddSingleton<ICache>(sharedCache);
```

## Побудуємо власну IServiceCollection

Розберемо механізм реєстрації та розпізнавання детально — реалізуємо повноцінний варіант, що підтримує всі три типи реєстрації і правильно обробляє циклічні залежності:

```csharp run
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;

// ════════════════════════════════════════════════════════════════
// ServiceDescriptor — опис однієї реєстрації
// ════════════════════════════════════════════════════════════════

enum ServiceLifetime { Singleton, Scoped, Transient }

class ServiceDescriptor
{
    public Type ServiceType        { get; }
    public Type? ImplementationType { get; }
    public Func<IServiceProvider, object>? Factory { get; }
    public object? Instance        { get; }
    public ServiceLifetime Lifetime { get; }

    // Конструктор 1: через тип реалізації
    public ServiceDescriptor(Type serviceType, Type implType, ServiceLifetime lifetime)
    {
        ServiceType        = serviceType;
        ImplementationType = implType;
        Lifetime           = lifetime;
    }

    // Конструктор 2: через фабрику
    public ServiceDescriptor(Type serviceType,
                              Func<IServiceProvider, object> factory,
                              ServiceLifetime lifetime)
    {
        ServiceType = serviceType;
        Factory     = factory;
        Lifetime    = lifetime;
    }

    // Конструктор 3: готовий екземпляр (тільки Singleton)
    public ServiceDescriptor(Type serviceType, object instance)
    {
        ServiceType = serviceType;
        Instance    = instance;
        Lifetime    = ServiceLifetime.Singleton;
    }
}

// ════════════════════════════════════════════════════════════════
// IServiceCollection — колекція реєстрацій (незмінна після Build)
// ════════════════════════════════════════════════════════════════

interface IServiceCollection
{
    void Add(ServiceDescriptor descriptor);
    IServiceProvider BuildServiceProvider();
}

interface IServiceProvider
{
    object? GetService(Type serviceType);
}

static class ServiceCollectionExtensions
{
    public static void AddSingleton<TService, TImpl>(this IServiceCollection col)
        where TImpl : TService
        => col.Add(new ServiceDescriptor(typeof(TService), typeof(TImpl), ServiceLifetime.Singleton));

    public static void AddSingleton<TService>(this IServiceCollection col,
                                               Func<IServiceProvider, TService> factory)
        where TService : class
        => col.Add(new ServiceDescriptor(typeof(TService),
                    p => factory(p), ServiceLifetime.Singleton));

    public static void AddTransient<TService, TImpl>(this IServiceCollection col)
        where TImpl : TService
        => col.Add(new ServiceDescriptor(typeof(TService), typeof(TImpl), ServiceLifetime.Transient));

    public static void AddScoped<TService, TImpl>(this IServiceCollection col)
        where TImpl : TService
        => col.Add(new ServiceDescriptor(typeof(TService), typeof(TImpl), ServiceLifetime.Scoped));

    public static T GetRequiredService<T>(this IServiceProvider provider)
    {
        var result = provider.GetService(typeof(T));
        if (result is null)
            throw new InvalidOperationException($"Сервіс {typeof(T).Name} не зареєстровано.");
        return (T)result;
    }
}

// ════════════════════════════════════════════════════════════════
// ServiceCollection + ServiceProvider — реалізація
// ════════════════════════════════════════════════════════════════

class ServiceCollection : IServiceCollection
{
    private readonly List<ServiceDescriptor> _descriptors = new();
    private bool _built = false;

    public void Add(ServiceDescriptor descriptor)
    {
        if (_built)
            throw new InvalidOperationException(
                "Не можна реєструвати сервіси після BuildServiceProvider().");
        _descriptors.Add(descriptor);
    }

    public IServiceProvider BuildServiceProvider()
    {
        _built = true;
        return new ServiceProvider(_descriptors);
    }
}

class ServiceProvider : IServiceProvider
{
    private readonly List<ServiceDescriptor> _descriptors;
    private readonly Dictionary<Type, object> _singletons = new();
    // Для виявлення циклічних залежностей
    private readonly HashSet<Type> _resolving = new();

    public ServiceProvider(List<ServiceDescriptor> descriptors)
        => _descriptors = descriptors;

    public object? GetService(Type serviceType)
    {
        var descriptor = _descriptors.LastOrDefault(d => d.ServiceType == serviceType);
        if (descriptor is null) return null;

        return descriptor.Lifetime switch
        {
            ServiceLifetime.Singleton  => GetOrCreateSingleton(descriptor),
            ServiceLifetime.Transient  => CreateInstance(descriptor),
            ServiceLifetime.Scoped     => GetOrCreateSingleton(descriptor), // спрощено
            _ => throw new NotSupportedException()
        };
    }

    private object GetOrCreateSingleton(ServiceDescriptor d)
    {
        if (_singletons.TryGetValue(d.ServiceType, out var existing))
            return existing;
        var instance = CreateInstance(d);
        _singletons[d.ServiceType] = instance;
        return instance;
    }

    private object CreateInstance(ServiceDescriptor d)
    {
        // Готовий екземпляр
        if (d.Instance is not null) return d.Instance;

        // Фабрика
        if (d.Factory is not null) return d.Factory(this);

        // Тип реалізації — знаходимо конструктор і вирішуємо аргументи
        var implType = d.ImplementationType!;

        // Захист від циклічних залежностей
        if (_resolving.Contains(implType))
            throw new InvalidOperationException(
                $"Циклічна залежність при розпізнаванні {implType.Name}");

        _resolving.Add(implType);
        try
        {
            var ctor = implType.GetConstructors()
                               .OrderByDescending(c => c.GetParameters().Length)
                               .First();

            var args = ctor.GetParameters()
                           .Select(p => GetService(p.ParameterType)
                                        ?? throw new InvalidOperationException(
                                            $"Немає реєстрації для {p.ParameterType.Name} " +
                                            $"(потрібен {implType.Name})"))
                           .ToArray();

            return Activator.CreateInstance(implType, args)!;
        }
        finally
        {
            _resolving.Remove(implType);
        }
    }
}

// ════════════════════════════════════════════════════════════════
// Доменні класи — клінічна система
// ════════════════════════════════════════════════════════════════

interface IPatientRepository
{
    void Save(string name);
    List<string> GetAll();
}

interface IAppointmentRepository
{
    void Save(string patient, string doctor, DateTime time);
    List<string> GetAll();
}

interface INotificationService
{
    void Notify(string to, string message);
}

class InMemoryPatientRepository : IPatientRepository
{
    private readonly List<string> _data = new();
    public void Save(string name) { _data.Add(name); }
    public List<string> GetAll() => _data;
}

class InMemoryAppointmentRepository : IAppointmentRepository
{
    private readonly List<string> _data = new();
    public void Save(string p, string d, DateTime t)
        => _data.Add($"{p} -> {d} о {t:HH:mm}");
    public List<string> GetAll() => _data;
}

class ConsoleNotificationService : INotificationService
{
    public void Notify(string to, string message)
        => Console.WriteLine($"  [Email] {to}: {message}");
}

class AppointmentService
{
    private readonly IPatientRepository _patients;
    private readonly IAppointmentRepository _appointments;
    private readonly INotificationService _notifications;

    public AppointmentService(
        IPatientRepository patients,
        IAppointmentRepository appointments,
        INotificationService notifications)
    {
        _patients      = patients;
        _appointments  = appointments;
        _notifications = notifications;
    }

    public void RegisterPatient(string name)
    {
        _patients.Save(name);
        _notifications.Notify(name, "Реєстрацію підтверджено");
    }

    public void BookAppointment(string patient, string doctor, DateTime time)
    {
        _appointments.Save(patient, doctor, time);
        _notifications.Notify(patient, $"Запис до {doctor} о {time:HH:mm} підтверджено");
    }

    public void PrintSummary()
    {
        var pts = _patients.GetAll();
        var apts = _appointments.GetAll();
        Console.WriteLine($"  Пацієнтів: {pts.Count.ToString()}, Записів: {apts.Count.ToString()}");
        foreach (var a in apts) Console.WriteLine($"    {a}");
    }
}

// ════════════════════════════════════════════════════════════════
// ДЕМОНСТРАЦІЯ
// ════════════════════════════════════════════════════════════════

class Program
{
    static void Main()
    {
        Console.WriteLine("=== Реєстрація сервісів ===");

        var collection = new ServiceCollection();

        // Реєстрація через тип
        collection.AddSingleton<IPatientRepository, InMemoryPatientRepository>();
        collection.AddSingleton<IAppointmentRepository, InMemoryAppointmentRepository>();
        collection.AddSingleton<INotificationService, ConsoleNotificationService>();
        collection.AddTransient<AppointmentService, AppointmentService>();

        Console.WriteLine("  [OK] IPatientRepository     → InMemoryPatientRepository (Singleton)");
        Console.WriteLine("  [OK] IAppointmentRepository → InMemoryAppointmentRepository (Singleton)");
        Console.WriteLine("  [OK] INotificationService   → ConsoleNotificationService (Singleton)");
        Console.WriteLine("  [OK] AppointmentService     → AppointmentService (Transient)");

        // ─── Build: після цього реєстрація заблокована ───────────
        Console.WriteLine("\n=== Build ServiceProvider ===");
        var provider = collection.BuildServiceProvider();
        Console.WriteLine("  [OK] ServiceProvider побудовано");

        // ─── Спроба зареєструвати після Build ────────────────────
        try
        {
            collection.AddSingleton<IPatientRepository, InMemoryPatientRepository>();
        }
        catch (InvalidOperationException ex)
        {
            Console.WriteLine($"  [X] Очікувана помилка: {ex.Message}");
        }

        // ─── Resolve та використання ──────────────────────────────
        Console.WriteLine("\n=== Resolve та використання ===");
        var service = provider.GetRequiredService<AppointmentService>();

        service.RegisterPatient("Іваненко Олег");
        service.RegisterPatient("Мельник Ганна");
        service.BookAppointment("Іваненко Олег", "Лікар Петренко", new DateTime(2026, 6, 10, 10, 0, 0));
        service.BookAppointment("Мельник Ганна", "Лікар Сидоренко", new DateTime(2026, 6, 11, 14, 30, 0));

        Console.WriteLine("\n=== Підсумок ===");
        service.PrintSummary();

        // ─── Перевірка Singleton: завжди той самий об'єкт ────────
        Console.WriteLine("\n=== Singleton: перевірка ідентичності ===");
        var r1 = provider.GetRequiredService<IPatientRepository>();
        var r2 = provider.GetRequiredService<IPatientRepository>();
        Console.WriteLine($"  r1 === r2: {object.ReferenceEquals(r1, r2).ToString()}");

        // ─── Перевірка Transient: завжди новий об'єкт ─────────────
        Console.WriteLine("\n=== Transient: перевірка ідентичності ===");
        var s1 = provider.GetRequiredService<AppointmentService>();
        var s2 = provider.GetRequiredService<AppointmentService>();
        Console.WriteLine($"  s1 === s2: {object.ReferenceEquals(s1, s2).ToString()}");
    }
}
```

## Множинна реєстрація одного інтерфейсу

Важлива особливість: один інтерфейс можна зареєструвати кілька разів з різними реалізаціями. При запиті через `GetService<T>()` повертається **остання** реєстрація. При запиті через `GetServices<T>()` (або `IEnumerable<T>`) — **всі** реєстрації. Це використовується у патернах типу «ланцюжок обробників» або «список валідаторів»:

```csharp
// Всі валідатори для AppointmentRequest
services.AddTransient<IAppointmentValidator, TimeSlotValidator>();
services.AddTransient<IAppointmentValidator, DoctorAvailabilityValidator>();
services.AddTransient<IAppointmentValidator, PatientInsuranceValidator>();

// У AppointmentService:
// IEnumerable<IAppointmentValidator> validators  ← отримуємо всі три
```

## TryAdd: реєстрація «якщо ще не зареєстровано»

Методи `TryAddSingleton`, `TryAddScoped`, `TryAddTransient` реєструють сервіс **тільки якщо** такого ServiceType ще немає в колекції. Це корисно для бібліотек, що хочуть надати реалізацію «за замовчуванням», але не перезаписувати ту, що встановив користувач:

```csharp
// У бібліотеці:
services.TryAddSingleton<IPatientRepository, DefaultPatientRepository>();

// Якщо користувач вже зареєстрував свій:
services.AddSingleton<IPatientRepository, CustomPatientRepository>();
// → DefaultPatientRepository ніколи не буде використано
```

![Реєстрація та розпізнавання сервісів у IServiceCollection](_assets/21-02/service-registration.png)

## Перевірка на валідність реєстрацій

Реальний `ServiceProvider` у .NET підтримує опцію `ValidateOnBuild = true`. При увімкненні вона перевіряє при `BuildServiceProvider()`:
- чи не є якийсь зареєстрований сервіс невирішуваним (залежність не зареєстрована)
- чи немає «captive dependencies» (Singleton залежить від Scoped — помилка, бо Scoped живе коротше)

У Development-середовищі Generic Host автоматично вмикає ці перевірки. В Production — вимикає заради продуктивності.

## Підсумок

`IServiceCollection` — це не просто список об'єктів. Це **специфікація** того, як система будується. Розділення реєстрації (`IServiceCollection`) і розпізнавання (`IServiceProvider`) — принципово важливе архітектурне рішення: воно гарантує, що склад системи визначається один раз на старті, а не довільно змінюється під час роботи. Це робить додаток передбачуваним, тестованим і правильно сконструйованим.
