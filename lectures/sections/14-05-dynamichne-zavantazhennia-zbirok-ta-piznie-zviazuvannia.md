---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
section: 5
number: "14.5"
title: "Динамічне завантаження збірок та пізнє зв'язування"
source: "../_combined/88-dynamichne-zavantazhennia-zbirok-ta-piznie-zviazuvannia.md"
---

## 14.5. Динамічне завантаження збірок та пізнє зв'язування

У попередніх розділах ми досліджували типи збірок, вже присутніх у програмі на момент старту. Але рефлексія дозволяє йти далі: **завантажувати збірки динамічно** — з файлової системи, з потоку байтів, або навіть з коду, згенерованого під час виконання. Саме це відкриває двері до плагінних архітектур, hot reload і DI-контейнерів, що сканують цілі папки з `.dll`.

Ключова різниця між статичним і динамічним завантаженням: при статичному посилання на збірку визначається в `.csproj` і CLR завантажує її автоматично перед запуском. При динамічному — збірка невідома компілятору, і вся відповідальність за пошук типів, перевірку сумісності і виклик методів лежить на коді рефлексії.

![Динамічне завантаження збірок — Assembly та AssemblyLoadContext](_assets/14-05/assembly-loading.png)

## Клас Assembly

`Assembly` з простору імен `System.Reflection` — центральний клас для роботи зі збірками. Він надає як методи **завантаження**, так і методи **дослідження** вмісту.

### Методи завантаження

| Метод | Коли використовувати |
|-------|---------------------|
| `Assembly.Load(name)` | завантаження за AssemblyName з кешу або GAC |
| `Assembly.LoadFrom(path)` | завантаження з файлу; CLR вирішує залежності |
| `Assembly.LoadFile(path)` | завантаження ізольовано, без резолюції залежностей |
| `Assembly.GetEntryAssembly()` | стартова збірка (`Program.cs`) |
| `Assembly.GetCallingAssembly()` | збірка, що викликала поточний метод |
| `Assembly.GetExecutingAssembly()` | збірка, де виконується поточний код |

**`LoadFrom` vs `LoadFile`:** `LoadFrom` реєструє шлях у CLR-завантажувачі і CLR може знайти залежності автоматично. `LoadFile` завантажує файл **ізольовано** — якщо збірка залежить від `SomeLib.dll`, CLR її не знайде автоматично. Тому `LoadFile` зазвичай використовують лише для інспекції метаданих.

### Властивості для дослідження

| Властивість / Метод | Що повертає |
|---------------------|-------------|
| `.FullName` | рядок `"MyMedApp, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"` |
| `.GetName().Version` | об'єкт `Version` (Major, Minor, Build, Revision) |
| `.Location` | повний шлях до `.dll` на диску |
| `.GetTypes()` | **всі** типи збірки, включаючи internal і compiler-generated |
| `.GetExportedTypes()` | тільки `public` типи — безпечніше для плагінного сканування |
| `.GetType(name)` | `Type?` — знайти конкретний тип за повним ім'ям |
| `.GetCustomAttributes()` | атрибути рівня збірки (`[assembly: AssemblyVersion(...)]`) |

Різниця між `GetTypes()` і `GetExportedTypes()` важлива: `GetTypes()` може кинути `ReflectionTypeLoadException`, якщо не вдається завантажити якийсь тип (наприклад, відсутня залежність). `GetExportedTypes()` надійніший у цьому сенсі, бо повертає тільки типи, доступні ззовні.

```csharp
// Безпечна версія GetTypes з обробкою ReflectionTypeLoadException
static IEnumerable<Type> SafeGetTypes(Assembly asm)
{
    try { return asm.GetExportedTypes(); }
    catch (ReflectionTypeLoadException ex)
    {
        // Повертаємо ті типи, що вдалося завантажити
        return ex.Types.Where(t => t is not null)!;
    }
}
```

## AssemblyLoadContext — ізоляція та Unload

У .NET Framework завантажені збірки не можна було вивантажити без перезапуску `AppDomain` (що фактично означало зупинку процесу). .NET Core і .NET 5+ вирішили цю проблему через `AssemblyLoadContext` (ALC).

**ALC** — це ізольований контекст завантаження. Кожен ALC має власний набір завантажених збірок. Один і той самий тип, завантажений у двох різних ALC, вважається **різними типами** з точки зору CLR.

```csharp
// Стандартний (незмінний) контекст — містить усі збірки програми
AssemblyLoadContext defaultCtx = AssemblyLoadContext.Default;

// Ізольований колектибельний контекст для плагіна
var pluginCtx = new AssemblyLoadContext("PluginCtx", isCollectible: true);
Assembly pluginAsm = pluginCtx.LoadFromAssemblyPath(fullPath);

// ... використання плагіна ...

// Вивантаження: CLR виконає збірку сміття після звільнення всіх посилань
pluginCtx.Unload();
```

**Умови для успішного `Unload`:**
1. ALC створений з `isCollectible: true`.
2. Немає жодних живих посилань на типи або екземпляри з цього ALC (у стеку, статичних полях, обробниках подій, делегатах).
3. `Unload()` — це сигнал, а не миттєве вивантаження. GC вирішує, коли фактично звільнити пам'ять.

| Метод | Ізоляція | Unload | Залежності |
|-------|----------|--------|-----------|
| `LoadFrom(path)` | у Default ALC | ні | CLR вирішує авто |
| `LoadFile(path)` | часткова | ні | не вирішує |
| `ALC.LoadFromAssemblyPath` | повна | так (якщо collectible) | треба реалізувати Load() |
| `ALC.LoadFromStream` | повна | так | з байтового потоку |

### Реалізація PluginLoadContext

Для коректного завантаження плагіна з власними залежностями необхідно перевизначити `Load(AssemblyName)`:

```csharp
class PluginLoadContext : AssemblyLoadContext
{
    private readonly AssemblyDependencyResolver _resolver;

    public PluginLoadContext(string pluginPath) : base(isCollectible: true)
    {
        _resolver = new AssemblyDependencyResolver(pluginPath);
    }

    protected override Assembly? Load(AssemblyName name)
    {
        string? path = _resolver.ResolveAssemblyToPath(name);
        return path is not null ? LoadFromAssemblyPath(path) : null;
        // null → CLR шукатиме у Default ALC (shared типи: System.*, Microsoft.*)
    }
}
```

`AssemblyDependencyResolver` читає `.deps.json` файл поруч з `.dll` і знає, де лежать залежності плагіна.

## Патерн Plugin через рефлексію

Плагінна архітектура — найпопулярніший сценарій динамічного завантаження. Вона складається з 6 кроків:

**Крок 1.** Визначити інтерфейс у **host-збірці** (окремий проєкт, на який посилається і host, і плагіни):

```csharp
// Збірка MedAnalysis.Contracts.dll
namespace MedAnalysis.Contracts;

public interface IAnalysisPlugin
{
    string Name { get; }
    string Description { get; }
    AnalysisResult Analyze(PatientRecord[] records);
}
```

**Крок 2.** Завантажити `.dll` плагіна через ALC:

```csharp
var ctx = new PluginLoadContext(pluginPath);
Assembly asm = ctx.LoadFromAssemblyPath(pluginPath);
```

**Крок 3.** Отримати всі public типи:

```csharp
IEnumerable<Type> types = SafeGetTypes(asm);
```

**Крок 4.** Відфільтрувати по інтерфейсу — тільки конкретні, не абстрактні класи:

```csharp
Type pluginInterface = typeof(IAnalysisPlugin);
IEnumerable<Type> pluginTypes = types
    .Where(t => pluginInterface.IsAssignableFrom(t)
             && !t.IsAbstract
             && !t.IsInterface);
```

`IsAssignableFrom(t)` — це «зворотний» `IsAssignableTo`: `pluginInterface.IsAssignableFrom(t)` означає «`t` реалізує `pluginInterface`». Аналогічно `t.IsAssignableTo(pluginInterface)` (з'явилось у .NET 5).

**Крок 5.** Створити екземпляри через `Activator`:

```csharp
var plugins = pluginTypes
    .Select(t => (IAnalysisPlugin)Activator.CreateInstance(t)!)
    .ToList();
```

**Крок 6.** Використовувати через інтерфейс:

```csharp
foreach (var plugin in plugins)
    Console.WriteLine($"[{plugin.Name}] {plugin.Analyze(records)}");
```

### Перевірка відповідності типу

При скануванні збірок часто потрібно перевірити різні умови відповідності:

| Перевірка | Що означає |
|-----------|------------|
| `t.IsAssignableTo(typeof(IPlugin))` | `t` реалізує інтерфейс або успадковує тип |
| `t.IsSubclassOf(typeof(BaseRecord))` | `t` є нащадком конкретного класу |
| `t.GetInterface("IAnalysisPlugin") != null` | реалізує інтерфейс за ім'ям (для cross-ALC) |
| `!t.IsAbstract && !t.IsInterface` | лише конкретні інстанційовані типи |

---

## Приклад 1 — Дослідження поточної збірки та пізнє зв'язування

```csharp
using System;
using System.Linq;
using System.Reflection;

// Досліджуємо власну збірку програми
Assembly self = Assembly.GetExecutingAssembly();

Console.WriteLine("=== Інформація про збірку ===\n");
Console.WriteLine($"  FullName  : {self.FullName}");
Console.WriteLine($"  Version   : {self.GetName().Version}");
Console.WriteLine($"  Location  : {self.Location}");

Console.WriteLine("\n=== Усі public типи ===\n");
foreach (Type t in self.GetExportedTypes())
{
    string kind = t.IsInterface ? "interface" : t.IsAbstract ? "abstract" : "class";
    Console.WriteLine($"  [{kind}] {t.Name}");
}

Console.WriteLine("\n=== Пізнє зв'язування: IAnalysisPlugin ===\n");

Type pluginInterface = typeof(IAnalysisPlugin);

// Знаходимо всі реалізації IAnalysisPlugin у поточній збірці
var plugins = self.GetExportedTypes()
    .Where(t => pluginInterface.IsAssignableFrom(t) && !t.IsAbstract && !t.IsInterface)
    .Select(t => (IAnalysisPlugin)Activator.CreateInstance(t)!)
    .ToList();

// Тестові записи
var records = new[]
{
    new PatientRecord("Іван Коваль",   28.5m, 72),
    new PatientRecord("Марія Гончар",  32.1m, 88),
    new PatientRecord("Петро Мельник", 22.3m, 65),
};

foreach (var plugin in plugins)
{
    Console.WriteLine($"Плагін: {plugin.Name} — {plugin.Description}");
    AnalysisResult result = plugin.Analyze(records);
    Console.WriteLine($"  Результат: {result.Summary}");
    Console.WriteLine();
}

// ===================== Контракти =====================
public interface IAnalysisPlugin
{
    string Name { get; }
    string Description { get; }
    AnalysisResult Analyze(PatientRecord[] records);
}

public record AnalysisResult(string Summary);
public record PatientRecord(string FullName, decimal Bmi, int HeartRate);

// ===================== Плагіни =====================
public class BmiAnalysisPlugin : IAnalysisPlugin
{
    public string Name => "BMI Analyzer";
    public string Description => "Аналіз ІМТ пацієнтів";

    public AnalysisResult Analyze(PatientRecord[] records)
    {
        int overweight = records.Count(r => r.Bmi >= 30);
        double avg = records.Average(r => (double)r.Bmi);
        return new AnalysisResult($"Середній ІМТ: {avg:F1}, з надмірною вагою: {overweight}/{records.Length}");
    }
}

public class HeartRatePlugin : IAnalysisPlugin
{
    public string Name => "HeartRate Analyzer";
    public string Description => "Аналіз частоти серцевих скорочень";

    public AnalysisResult Analyze(PatientRecord[] records)
    {
        int elevated = records.Count(r => r.HeartRate > 80);
        int min = records.Min(r => r.HeartRate);
        int max = records.Max(r => r.HeartRate);
        return new AnalysisResult($"ЧСС: min={min}, max={max}, підвищена у {elevated}/{records.Length}");
    }
}
```

---

## Приклад 2 — PluginScanner: динамічне сканування збірок у папці

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Loader;

// Демонстрація PluginScanner без реального запису на диск:
// симулюємо завантаження з поточної збірки як "зовнішнього" плагіна.
var scanner = new PluginScanner<IReportPlugin>();
scanner.ScanAssembly(Assembly.GetExecutingAssembly());

Console.WriteLine($"Знайдено плагінів: {scanner.Plugins.Count}\n");

var patients = new[]
{
    new MedRecord("Олена Петренко", new DateTime(1985, 3, 12), 25.4m),
    new MedRecord("Сергій Бондар",  new DateTime(1970, 8, 5),  31.2m),
    new MedRecord("Тетяна Кравець", new DateTime(1995, 1, 20), 19.8m),
};

foreach (var plugin in scanner.Plugins)
{
    Console.WriteLine($"=== {plugin.ReportName} ===");
    plugin.GenerateReport(patients);
    Console.WriteLine();
}

Console.WriteLine("=== PluginScanner статистика ===");
scanner.PrintStats();

// ===================== Контракт =====================
public interface IReportPlugin
{
    string ReportName { get; }
    void GenerateReport(MedRecord[] records);
}

public record MedRecord(string FullName, DateTime BirthDate, decimal Bmi);

// ===================== Реалізації =====================
public class DemographicsReport : IReportPlugin
{
    public string ReportName => "Демографічний звіт";

    public void GenerateReport(MedRecord[] records)
    {
        var today = DateTime.Today;
        foreach (var r in records)
        {
            int age = today.Year - r.BirthDate.Year;
            if (r.BirthDate.Date > today.AddYears(-age)) age--;
            Console.WriteLine($"  {r.FullName}: {age} років");
        }
        Console.WriteLine($"  Середній вік: {records.Average(r => today.Year - r.BirthDate.Year):F0}");
    }
}

public class BmiCategoryReport : IReportPlugin
{
    public string ReportName => "Звіт за категоріями ІМТ";

    public void GenerateReport(MedRecord[] records)
    {
        foreach (var r in records)
        {
            string cat = r.Bmi switch
            {
                < 18.5m => "Недостатня вага",
                < 25.0m => "Норма",
                < 30.0m => "Надмірна вага",
                _       => "Ожиріння"
            };
            Console.WriteLine($"  {r.FullName}: ІМТ {r.Bmi:F1} — {cat}");
        }
    }
}

// ===================== Scanner =====================
public class PluginScanner<TPlugin> where TPlugin : class
{
    private readonly List<TPlugin> _plugins = new();
    private readonly List<(string Assembly, string TypeName)> _found = new();

    public IReadOnlyList<TPlugin> Plugins => _plugins;

    public void ScanAssembly(Assembly asm)
    {
        Type contractType = typeof(TPlugin);
        IEnumerable<Type> candidates;

        try { candidates = asm.GetExportedTypes(); }
        catch (ReflectionTypeLoadException ex)
        { candidates = ex.Types.Where(t => t is not null)!; }

        foreach (var type in candidates.Where(t =>
            contractType.IsAssignableFrom(t) && !t.IsAbstract && !t.IsInterface))
        {
            try
            {
                var instance = (TPlugin)Activator.CreateInstance(type)!;
                _plugins.Add(instance);
                _found.Add((asm.GetName().Name ?? "?", type.Name));
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  [!] Не вдалося створити {type.Name}: {ex.InnerException?.Message ?? ex.Message}");
            }
        }
    }

    public void ScanDirectory(string directory)
    {
        foreach (string dll in Directory.GetFiles(directory, "*.dll"))
        {
            try
            {
                var ctx = new AssemblyLoadContext($"Plugin_{Path.GetFileNameWithoutExtension(dll)}", isCollectible: true);
                Assembly asm = ctx.LoadFromAssemblyPath(Path.GetFullPath(dll));
                ScanAssembly(asm);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  [!] Не вдалося завантажити {dll}: {ex.Message}");
            }
        }
    }

    public void PrintStats()
    {
        Console.WriteLine($"  Контракт  : {typeof(TPlugin).FullName}");
        Console.WriteLine($"  Знайдено  : {_plugins.Count} плагінів");
        foreach (var (asm, typeName) in _found)
            Console.WriteLine($"    [{asm}] {typeName}");
    }
}
```

`PluginScanner<TPlugin>` показує повний цикл: `GetExportedTypes()` з безпечним перехопленням `ReflectionTypeLoadException`, фільтрація за контрактним інтерфейсом через `IsAssignableFrom`, `Activator.CreateInstance` із перехопленням помилок ініціалізації, і `AssemblyLoadContext` з `isCollectible: true` для кожної папкової збірки — щоб пам'ять можна було звільнити після деактивації плагіна.
