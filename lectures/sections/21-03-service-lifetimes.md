---
chapter: 21
chapterTitle: "Розділ 21. Generic Host та Dependency Injection"
section: 3
number: "21.3"
title: "Часи життя сервісів — Singleton, Scoped, Transient"
source: ""
---

## 21.3. Часи життя сервісів — Singleton, Scoped, Transient

Вибір правильного часу життя сервісу (`ServiceLifetime`) — одне з найважливіших архітектурних рішень при роботі з DI-контейнером. Неправильний вибір не завжди призводить до видимої помилки одразу, але може спричинити тонкі баги: загальний стан там, де його не повинно бути, витоки пам'яті, баги в багатопотоковому середовищі або `ObjectDisposedException` у найнеочікуванішому місці.

.NET DI підтримує три часи життя. Їхні назви коротко описують правило:

| Lifetime | Екземпляр | Коли створюється | Коли знищується |
|---|---|---|---|
| **Singleton** | один на весь процес | перший запит | завершення додатку |
| **Scoped** | один на «область» (запит) | початок scope | кінець scope |
| **Transient** | новий при кожному запиті | кожен `GetService<T>()` | одразу після використання |

## Singleton

**Singleton** — контейнер створює рівно один екземпляр і повертає його при кожному запиті. Цей екземпляр живе весь час роботи додатку.

**Коли використовувати:**
- Об'єкти, що є дорогими для ініціалізації і можна безпечно розділяти між потоками: кеш, пул з'єднань, клієнт HTTP, конфігурація
- Сервіси без стану, що однаково поводяться при будь-якому виклику
- Реєстрація «готового екземпляра»: `services.AddSingleton<IConfiguration>(config)`

**Небезпеки:**
- Singleton повинен бути **потокобезпечним** (thread-safe), бо кілька потоків можуть одночасно звертатись до нього
- Singleton **не може залежати від Scoped-сервісів** — captive dependency (про це далі)
- Якщо Singleton зберігає змінний стан, може виникати «забруднення» між запитами

## Scoped

**Scoped** — контейнер створює один екземпляр на «область» (scope). У контексті ASP.NET Core один scope = один HTTP-запит. У Worker Service scope створюється вручну.

**Коли використовувати:**
- `DbContext` (Entity Framework) — класичний приклад: один контекст на запит гарантує, що всі операції в межах одного HTTP-запиту входять до одної транзакції
- `UnitOfWork` — паттерн, що агрегує кілька репозиторіїв і спільний контекст
- Будь-який сервіс, що повинен мати спільний стан у межах одного запиту, але незалежний від інших

**Небезпеки:**
- Scoped-сервіс, якого запитали поза scope, кидає виняток (`InvalidOperationException`)
- Якщо захопити scoped-сервіс у Singleton — він ніколи не буде знищений після запиту

## Transient

**Transient** — новий екземпляр при кожному запиті. DI-контейнер не зберігає жодного посилання на створені об'єкти.

**Коли використовувати:**
- Легкі сервіси без стану, що коштують мало для ініціалізації
- Сервіси, де важлива ізоляція між різними частинами коду (наприклад, ланцюжки обробників подій)
- `ILogger<T>` — кожен клас отримує свій власний логер з іменем типу

**Небезпеки:**
- Якщо Transient-сервіс реалізує `IDisposable`, контейнер не викликає `Dispose()` автоматично для root-scope — це потенційний витік ресурсів

## Детальна демонстрація всіх трьох

```csharp run
using System;
using System.Collections.Generic;
using System.Linq;

// ════════════════════════════════════════════════════════════════
// Спрощений контейнер з підтримкою Scope
// ════════════════════════════════════════════════════════════════

enum ServiceLifetime { Singleton, Scoped, Transient }

record ServiceDescriptor(
    Type ServiceType,
    Type ImplementationType,
    ServiceLifetime Lifetime);

class Container
{
    private readonly List<ServiceDescriptor> _descriptors = new();
    private readonly Dictionary<Type, object> _singletons = new();
    private bool _built;

    public void AddSingleton<TService, TImpl>() where TImpl : TService
        => Register<TService, TImpl>(ServiceLifetime.Singleton);

    public void AddScoped<TService, TImpl>() where TImpl : TService
        => Register<TService, TImpl>(ServiceLifetime.Scoped);

    public void AddTransient<TService, TImpl>() where TImpl : TService
        => Register<TService, TImpl>(ServiceLifetime.Transient);

    private void Register<TService, TImpl>(ServiceLifetime lt) where TImpl : TService
    {
        if (_built) throw new InvalidOperationException("Container is already built.");
        _descriptors.Add(new ServiceDescriptor(typeof(TService), typeof(TImpl), lt));
    }

    public Scope CreateScope()
    {
        _built = true;
        return new Scope(_descriptors, _singletons);
    }

    public TService Resolve<TService>() => CreateScope().Resolve<TService>();
}

class Scope : IDisposable
{
    private readonly List<ServiceDescriptor> _descriptors;
    private readonly Dictionary<Type, object> _singletons; // розділяється між scope
    private readonly Dictionary<Type, object> _scoped = new(); // тільки для цього scope
    private readonly List<IDisposable> _toDispose = new();
    private bool _disposed;

    public Scope(List<ServiceDescriptor> descriptors, Dictionary<Type, object> singletons)
    {
        _descriptors = descriptors;
        _singletons  = singletons;
    }

    public T Resolve<T>() => (T)Resolve(typeof(T));

    public object Resolve(Type t)
    {
        var d = _descriptors.LastOrDefault(x => x.ServiceType == t)
                ?? throw new InvalidOperationException($"Не зареєстровано: {t.Name}");

        return d.Lifetime switch
        {
            ServiceLifetime.Singleton  => GetOrCreate(_singletons, d),
            ServiceLifetime.Scoped     => GetOrCreate(_scoped, d),
            ServiceLifetime.Transient  => Create(d),
            _ => throw new NotSupportedException()
        };
    }

    private object GetOrCreate(Dictionary<Type, object> cache, ServiceDescriptor d)
    {
        if (!cache.TryGetValue(d.ServiceType, out var inst))
        {
            inst = Create(d);
            cache[d.ServiceType] = inst;
        }
        return inst;
    }

    private object Create(ServiceDescriptor d)
    {
        var ctor = d.ImplementationType.GetConstructors()
                    .OrderByDescending(c => c.GetParameters().Length).First();
        var args = ctor.GetParameters()
                       .Select(p => Resolve(p.ParameterType))
                       .ToArray();
        var inst = Activator.CreateInstance(d.ImplementationType, args)!;
        if (inst is IDisposable disposable) _toDispose.Add(disposable);
        return inst;
    }

    public void Dispose()
    {
        if (_disposed) return;
        _disposed = true;
        // Знищення у зворотному порядку створення
        for (int i = _toDispose.Count - 1; i >= 0; i--)
            _toDispose[i].Dispose();
        Console.WriteLine("  [Scope] Scope завершено та очищено");
    }
}

// ════════════════════════════════════════════════════════════════
// Сервіси для демонстрації часів життя
// ════════════════════════════════════════════════════════════════

// Лічильник викликів — допомагає відстежити кількість екземплярів
static class InstanceCounter
{
    private static int _singletonCount;
    private static int _scopedCount;
    private static int _transientCount;

    public static int NextSingleton() => ++_singletonCount;
    public static int NextScoped()    => ++_scopedCount;
    public static int NextTransient() => ++_transientCount;
}

// ─── Singleton сервіс ─────────────────────────────────────────

interface IAppConfiguration { string Get(string key); int InstanceId { get; } }

class AppConfiguration : IAppConfiguration
{
    public int InstanceId { get; } = InstanceCounter.NextSingleton();
    private readonly Dictionary<string, string> _settings = new()
    {
        ["DatabaseUrl"] = "Server=prod;Database=clinic",
        ["MaxConnections"] = "100"
    };
    public string Get(string key) => _settings.TryGetValue(key, out var v) ? v : "";
    public AppConfiguration()
        => Console.WriteLine($"  [NEW Singleton] AppConfiguration #{InstanceId.ToString()} створено");
}

// ─── Scoped сервіс ────────────────────────────────────────────

interface IUnitOfWork : IDisposable
{
    int InstanceId { get; }
    void SaveChanges();
}

class ClinicUnitOfWork : IUnitOfWork
{
    public int InstanceId { get; } = InstanceCounter.NextScoped();
    private readonly List<string> _pendingOperations = new();

    public ClinicUnitOfWork()
        => Console.WriteLine($"  [NEW Scoped]    ClinicUnitOfWork #{InstanceId.ToString()} створено");

    public void RegisterOperation(string op) => _pendingOperations.Add(op);
    public void SaveChanges()
    {
        Console.WriteLine($"  [UoW #{InstanceId.ToString()}] Зберігаю {_pendingOperations.Count.ToString()} операцій");
        _pendingOperations.Clear();
    }
    public void Dispose()
        => Console.WriteLine($"  [DISPOSE Scoped] ClinicUnitOfWork #{InstanceId.ToString()} знищено");
}

// ─── Transient сервіс ─────────────────────────────────────────

interface IPatientValidator { bool Validate(string name); int InstanceId { get; } }

class PatientValidator : IPatientValidator
{
    public int InstanceId { get; } = InstanceCounter.NextTransient();
    private readonly IAppConfiguration _config;

    public PatientValidator(IAppConfiguration config)
    {
        _config = config;
        Console.WriteLine($"  [NEW Transient]  PatientValidator #{InstanceId.ToString()} створено");
    }

    public bool Validate(string name) => !string.IsNullOrWhiteSpace(name) && name.Length >= 2;
}

// ─── AppointmentService — залежить від усіх трьох ─────────────

class AppointmentService
{
    private readonly IAppConfiguration _config;   // Singleton
    private readonly IUnitOfWork _uow;            // Scoped
    private readonly IPatientValidator _validator; // Transient

    public AppointmentService(
        IAppConfiguration config,
        IUnitOfWork uow,
        IPatientValidator validator)
    {
        _config    = config;
        _uow       = uow;
        _validator = validator;
    }

    public void BookAppointment(string patient, string doctor)
    {
        if (!_validator.Validate(patient))
        {
            Console.WriteLine($"    [!] Невалідне ім'я пацієнта: {patient}");
            return;
        }
        var db = _config.Get("DatabaseUrl");
        Console.WriteLine($"    Запис [{patient} -> {doctor}] через {db}");
    }
}

// ════════════════════════════════════════════════════════════════
// ДЕМОНСТРАЦІЯ
// ════════════════════════════════════════════════════════════════

class Program
{
    static void Main()
    {
        var container = new Container();
        container.AddSingleton<IAppConfiguration, AppConfiguration>();
        container.AddScoped<IUnitOfWork, ClinicUnitOfWork>();
        container.AddTransient<IPatientValidator, PatientValidator>();
        container.AddTransient<AppointmentService, AppointmentService>();

        // ─── Scope 1: перший «запит» ─────────────────────────────
        Console.WriteLine("\n╔══ Scope 1 (запит 1) ══╗");
        using (var scope1 = container.CreateScope())
        {
            var uow1a = scope1.Resolve<IUnitOfWork>();
            var uow1b = scope1.Resolve<IUnitOfWork>();
            Console.WriteLine($"  uow1a == uow1b (Scoped): {object.ReferenceEquals(uow1a, uow1b).ToString()}");

            var val1a = scope1.Resolve<IPatientValidator>();
            var val1b = scope1.Resolve<IPatientValidator>();
            Console.WriteLine($"  val1a == val1b (Transient): {object.ReferenceEquals(val1a, val1b).ToString()}");

            var cfg1 = scope1.Resolve<IAppConfiguration>();
            Console.WriteLine($"  Config InstanceId: {cfg1.InstanceId.ToString()}");
        }

        // ─── Scope 2: другий «запит» ─────────────────────────────
        Console.WriteLine("\n╔══ Scope 2 (запит 2) ══╗");
        using (var scope2 = container.CreateScope())
        {
            var uow2 = scope2.Resolve<IUnitOfWork>();
            var cfg2 = scope2.Resolve<IAppConfiguration>();

            Console.WriteLine($"  UoW InstanceId scope2:   {uow2.InstanceId.ToString()}");
            Console.WriteLine($"  Config InstanceId scope2: {cfg2.InstanceId.ToString()} (той самий Singleton!)");

            scope2.Resolve<AppointmentService>().BookAppointment("Іваненко Олег", "Лікар Петренко");
            scope2.Resolve<AppointmentService>().BookAppointment("!", "Лікар Сидоренко");
        }

        // ─── Підсумок ─────────────────────────────────────────────
        Console.WriteLine("\n=== Підсумок екземплярів ===");
        Console.WriteLine("  AppConfiguration: створено 1 раз (Singleton)");
        Console.WriteLine("  ClinicUnitOfWork: 1 на scope → створено 2 рази (Scoped)");
        Console.WriteLine("  PatientValidator: новий кожен раз (Transient)");
    }
}
```

## Captive Dependency — найпоширеніша помилка

**Captive dependency** — ситуація, коли сервіс з довшим часом життя тримає посилання на сервіс з коротшим часом життя, «захоплюючи» його і не даючи знищитися.

Класичний приклад:

```
Singleton(AppointmentService)
  └─ Scoped(ClinicUnitOfWork)   ← ПРОБЛЕМА!
```

`AppointmentService` живе весь час роботи додатку. Він отримав `ClinicUnitOfWork` при першому запиті. Але `ClinicUnitOfWork` мав жити тільки один запит — після його завершення він не знищується, бо Singleton тримає на нього посилання. При другому запиті `AppointmentService` продовжує використовувати **старий** `ClinicUnitOfWork` від першого запиту, замість нового. Якщо `UnitOfWork` зберігає відкрите з'єднання з базою даних або транзакцію — це буде або витік ресурсів, або баг зі спільним станом між запитами.

**Правило:** час життя залежності не може бути коротшим за час життя того, хто від неї залежить.

```
Singleton  → може залежати від: Singleton
Scoped     → може залежати від: Singleton, Scoped
Transient  → може залежати від: Singleton, Scoped, Transient
```

```csharp run
using System;

// ─── Демонстрація Captive Dependency ──────────────────────────

interface IRequestContext { string RequestId { get; } }

class RequestContext : IRequestContext
{
    public string RequestId { get; } = Guid.NewGuid().ToString("N")[..8];
    public RequestContext() => Console.WriteLine($"  [NEW] RequestContext RequestId={RequestId}");
}

class SingletonService
{
    private readonly IRequestContext _ctx; // Scoped захоплений у Singleton!

    public SingletonService(IRequestContext ctx)
    {
        _ctx = ctx;
        Console.WriteLine($"  [Singleton] Отримав ctx.RequestId={ctx.RequestId}");
    }

    public void DoWork()
    {
        // Завжди повертає RequestId з ПЕРШОГО запиту, навіть під час другого!
        Console.WriteLine($"  [DoWork] RequestId={_ctx.RequestId} (завжди той самий!)");
    }
}

// Ручна симуляція captive dependency:
class Program
{
    static void Main()
    {
        Console.WriteLine("=== Ілюстрація Captive Dependency ===\n");

        // «Перший запит» — RequestContext створюється
        var requestCtx1 = new RequestContext();
        var singleton   = new SingletonService(requestCtx1);

        Console.WriteLine("\n--- Запит 1 ---");
        singleton.DoWork(); // Виводить RequestId першого запиту

        // «Другий запит» — новий RequestContext, але Singleton вже має старий!
        var requestCtx2 = new RequestContext();
        Console.WriteLine($"\n--- Запит 2 --- (новий ctx.RequestId={requestCtx2.RequestId})");
        singleton.DoWork(); // Виводить RequestId ПЕРШОГО запиту — баг!

        Console.WriteLine("\nВисновок: SingletonService тримає застарілий RequestContext.");
        Console.WriteLine("Рішення: ніколи не ін'єктуйте Scoped у Singleton.");
        Console.WriteLine("Альтернатива: IServiceScopeFactory — отримати Scoped через фабрику.");
    }
}
```

## IServiceScopeFactory: правильний вихід

Якщо Singleton справді потребує scoped-сервісу (наприклад, BackgroundService обробляє один запис з черги і потребує `DbContext`), правильне рішення — ін'єктувати `IServiceScopeFactory` і самостійно керувати scope:

```csharp
class BackgroundProcessor // Singleton (IHostedService)
{
    private readonly IServiceScopeFactory _scopeFactory;

    public BackgroundProcessor(IServiceScopeFactory scopeFactory)
        => _scopeFactory = scopeFactory;

    public async Task ProcessAsync()
    {
        // Новий scope для кожної одиниці роботи
        using var scope = _scopeFactory.CreateScope();
        var dbContext = scope.ServiceProvider.GetRequiredService<ClinicDbContext>();
        // dbContext живе тільки в межах цього using-блоку
        // Після виходу scope.Dispose() → dbContext.Dispose()
    }
}
```

![Порівняння часів життя сервісів: Singleton, Scoped, Transient](_assets/21-03/service-lifetimes.png)

## Підсумок: як обирати lifetime

**Singleton** — якщо сервіс без стану або з незмінним станом, потокобезпечний, дорогий для ініціалізації.

**Scoped** — якщо сервіс має стан, специфічний для одного запиту (транзакція, UoW, контекст бази даних). Стандартний вибір для Entity Framework `DbContext`.

**Transient** — якщо сервіс легкий, без стану і не потребує спільності між різними споживачами. Стандартний вибір для дрібних утилітарних класів та валідаторів.

Коли маєте сумніви — починайте з **Transient**. Це найбезпечніший вибір з точки зору ізоляції, хоча й найдорожчий з точки зору алокацій. Перейдіть на Singleton або Scoped тільки тоді, коли це продиктовано конкретними вимогами до стану або продуктивності.
