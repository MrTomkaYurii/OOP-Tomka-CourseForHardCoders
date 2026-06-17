---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
section: 3
number: "14.3"
title: "Дослідження методів та конструкторів за допомогою рефлексії"
source: "../_combined/86-doslidzhennia-metodiv-ta-konstruktoriv-za-dopomohoiu-refleksii.md"
---

## 14.3. Дослідження методів та конструкторів за допомогою рефлексії

Якщо `System.Type` — це паспорт типу, то `MethodInfo` — це докладна анкета кожного його методу. `MethodInfo` успадковує від `MemberInfo` і доповнює базові властивості (`.Name`, `.DeclaringType`, `.MemberType`) специфічним для методів API: типом повернення, параметрами, модифікаторами, а головне — можливістю **викликати метод під час виконання** через `Invoke`.

Саме ця пара — дослідження (`GetParameters`) і виклик (`Invoke`) — лежить в основі ін'єкції залежностей, тестових фреймворків, генераторів документації та протоколів серіалізації.

![MethodInfo та ConstructorInfo — виклик через рефлексію](_assets/14-03/methods-constructors.png)

## Клас MethodInfo та його властивості

`MethodInfo` надає повний опис одного методу. Його ключові властивості:

| Властивість | Що повертає |
|-------------|-------------|
| `.Name` | ім'я методу: `"SetBmi"`, `"GetSummary"` |
| `.ReturnType` | `Type` типу, що повертається; `typeof(void)` для `void` |
| `.IsPublic` | `true` якщо `public` |
| `.IsPrivate` | `true` якщо `private` |
| `.IsFamily` | `true` якщо `protected` |
| `.IsAssembly` | `true` якщо `internal` |
| `.IsStatic` | `true` якщо статичний метод |
| `.IsVirtual` | `true` якщо `virtual` або `override` |
| `.IsAbstract` | `true` якщо `abstract` (обов'язково є `IsVirtual = true`) |
| `.IsFinal` | `true` якщо `sealed override` |
| `.IsGenericMethod` | `true` якщо метод generic |
| `.IsSpecialName` | `true` для `get_*`, `set_*`, `add_*` — обслуговуючих методів |
| `.GetParameters()` | `ParameterInfo[]` — масив параметрів |
| `.GetGenericArguments()` | `Type[]` — типові параметри generic-методу |
| `.MakeGenericMethod(types)` | конкретизація generic-методу для певних типів |
| `.Invoke(obj, args)` | динамічний виклик методу |

### IsSpecialName — чому get_Age з'являється серед методів

При виклику `GetMethods()` без фільтрів у списку опиняються методи `get_FullName`, `set_BirthDate`, `add_StatusChanged`, `remove_StatusChanged`. Це **обслуговуючі методи** (accessor methods), автоматично згенеровані компілятором для властивостей та подій.

Щоб відфільтрувати їх, перевіряємо `IsSpecialName`:

```csharp
var methods = typeof(PatientRecord)
    .GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
    .Where(m => !m.IsSpecialName);
```

`IsSpecialName = true` не означає, що метод недоступний — він цілком придатний для `Invoke`. Прапорець лише сигналізує: «цей метод генерується компілятором, а не написаний вручну».

## Клас ParameterInfo — деталі сигнатури

`GetParameters()` повертає `ParameterInfo[]` — масив дескрипторів параметрів у порядку їхнього оголошення в сигнатурі:

| Властивість | Що повертає |
|-------------|-------------|
| `.Name` | ім'я параметра: `"bmi"`, `"timestamp"` |
| `.ParameterType` | `Type` параметра |
| `.Position` | індекс у сигнатурі (від 0) |
| `.IsOptional` | `true` якщо параметр має значення за замовчуванням |
| `.HasDefaultValue` | `true` якщо `.DefaultValue` доступний |
| `.DefaultValue` | значення за замовчуванням або `DBNull.Value` |
| `.IsOut` | `true` якщо `out`-параметр |
| `.IsIn` | `true` якщо `in`-параметр |
| `.GetCustomAttributes()` | атрибути на параметрі (наприклад, `[FromBody]`) |

Якщо параметр передається через `ref`, `in` або `out`, то `.ParameterType.Name` отримує суфікс `&`: `"String&"`, `"Int32&"`. Для `out` додатково `IsOut = true`, для `in` — `IsIn = true`.

При побудові документаційних генераторів або IoC-контейнерів `IsOptional` і `DefaultValue` дозволяють визначити, які аргументи можна не передавати:

```csharp
void Register(PatientRecord record, bool urgent = false, string ward = "General")
```

```csharp
MethodInfo m = typeof(PatientService).GetMethod("Register")!;
foreach (var p in m.GetParameters())
{
    string defaultStr = p.HasDefaultValue ? $" = {p.DefaultValue}" : "";
    Console.WriteLine($"  {p.ParameterType.Name} {p.Name}{defaultStr}");
}
// PatientRecord record
// Boolean urgent = False
// String ward = General
```

## Invoke — динамічний виклик методу

`Invoke` — найпотужніша операція `MethodInfo`. Її сигнатура:

```csharp
public object? Invoke(object? obj, object?[]? parameters);
```

- **`obj`** — екземпляр, для якого викликається метод. Для `static` передається `null`.
- **`parameters`** — масив аргументів у порядку оголошення. Якщо метод безпараметровий — передати `null` або `[]`.
- **Результат** — `object?`. Для `void`-методів завжди `null`. Для value-типів відбувається **boxing**.

Повний workflow виклику відповідає п'яти крокам з діаграми:

```csharp
// 1. Отримати Type
Type t = typeof(PatientRecord);

// 2. Знайти метод
MethodInfo? mi = t.GetMethod("SetBmi",
    BindingFlags.Public | BindingFlags.Instance);

// 3. Перевірити параметри (опціонально)
foreach (var p in mi!.GetParameters())
    Console.WriteLine($"  {p.ParameterType.Name} {p.Name}");

// 4. Викликати Invoke
var patient = new PatientRecord("Олена Петренко", new DateTime(1985, 3, 12));
mi.Invoke(patient, new object[] { 24.7m });  // аргументи у масиві

// 5. Отримати і розкастувати результат
MethodInfo? getBmi = t.GetMethod("GetBmi");
object? raw = getBmi!.Invoke(patient, null);
decimal bmi = (decimal)raw!;
Console.WriteLine($"ІМТ: {bmi}");
```

При передачі аргументів через `object[]` відбувається **boxing** value-типів (`decimal`, `int`, `bool`). Саме тут криється основна ціна продуктивності: CLR упаковує значення в heap-об'єкти і одразу виконує security-check.

### TargetInvocationException — обгортка справжнього виключення

Якщо метод, викликаний через `Invoke`, кидає виключення, CLR **перехоплює його** і перепакує у `TargetInvocationException`. Причина — захистити call stack від змішування рефлексійного і прикладного стеків.

```csharp
try
{
    mi.Invoke(patient, new object[] { -5.0m });  // SetBmi(-5) — кидає
}
catch (TargetInvocationException ex)
{
    // ex.Message — технічний опис обгортки
    // ex.InnerException — справжнє виключення з методу
    Console.WriteLine($"Помилка: {ex.InnerException?.Message}");
}
```

Якщо треба перекинути справжнє виключення зі збереженням оригінального стеку, використовують `ExceptionDispatchInfo`:

```csharp
catch (TargetInvocationException ex) when (ex.InnerException is not null)
{
    System.Runtime.ExceptionServices.ExceptionDispatchInfo
        .Capture(ex.InnerException)
        .Throw();
}
```

Це стандартний патерн у фреймворках: тестові раннери (xUnit, NUnit) завжди «розпаковують» `TargetInvocationException`, щоб показати оригінальний `AssertionException`, а не обгортку.

## ConstructorInfo та Activator

### .ctor vs .cctor

Рефлексія розрізняє два типи конструкторів:

- **`.ctor`** — звичайний конструктор екземпляра. Присутній у `GetConstructors()`.
- **`.cctor`** — статичний конструктор (`static PatientRecord() { ... }`). Виконується CLR автоматично перед першим використанням типу. Видимий через `GetConstructors(BindingFlags.Static | BindingFlags.NonPublic)`, але **не може бути викликаний через `Invoke`** — тільки CLR вирішує, коли його запустити.

### Invoke vs Activator.CreateInstance

Два способи динамічно створити об'єкт:

```csharp
// Спосіб 1 — через ConstructorInfo.Invoke
ConstructorInfo? ctor = typeof(PatientRecord)
    .GetConstructor(new[] { typeof(string), typeof(DateTime) });
object? instance = ctor?.Invoke(new object[] { "Іван Коваль", new DateTime(1972, 7, 1) });

// Спосіб 2 — через Activator (спрощений API)
object? instance2 = Activator.CreateInstance(
    typeof(PatientRecord), "Іван Коваль", new DateTime(1972, 7, 1));
```

`Activator.CreateInstance` — зручна обгортка, що всередині так само знаходить конструктор за типами аргументів і викликає `Invoke`. Різниця:

| Критерій | `ConstructorInfo.Invoke` | `Activator.CreateInstance` |
|----------|--------------------------|---------------------------|
| Контроль | явний вибір конструктора | CLR шукає сам за аргументами |
| Перевантаження | повний контроль | може знайти не той, якщо є неоднозначність |
| Безпараметровий | `Invoke(null)` | `CreateInstance(type)` |
| Приватний конструктор | потрібен `NonPublic` у `BindingFlags` | не підтримує без явного ctor |
| Рекомендація | для складних сценаріїв | для простого factory за типом |

Для безпараметрового конструктора є ще `FormatterServices.GetUninitializedObject(type)` — він обходить **будь-який** конструктор і повертає «сирий» об'єкт з нульовими полями. Використовується в десеріалізаторах, де конструктор викликається окремо або взагалі не викликається.

## Продуктивність: чотири рівні

Рефлексійний виклик через `Invoke` — не безкоштовний. Бенчмарки на типовому .NET 8 сервері:

| Спосіб | Швидкість | Примітка |
|--------|-----------|----------|
| Прямий виклик | ~1 нс | JIT може вбудувати метод |
| `MethodInfo.Invoke` | ~200–500 нс | boxing + security check кожен раз |
| Кешований `MethodInfo` | ~150–300 нс | не шукати `GetMethod()` повторно |
| `CreateDelegate` / скомпільований `Expression` | ~5–20 нс | один раз будуємо, багато разів викликаємо |

### Кешування MethodInfo

Якщо метод викликається у циклі або на «гарячому шляху», `GetMethod()` не можна викликати всередині циклу:

```csharp
// Неефективно — пошук по метаданих на кожній ітерації
foreach (var patient in patients)
    typeof(PatientRecord).GetMethod("Validate")!.Invoke(patient, null);

// Ефективно — кешуємо одноразово
static readonly MethodInfo ValidateMethod =
    typeof(PatientRecord).GetMethod("Validate")!;

foreach (var patient in patients)
    ValidateMethod.Invoke(patient, null);
```

### CreateDelegate — майже пряма швидкість

`MethodInfo.CreateDelegate<TDelegate>()` компілює обгортку навколо методу, що по продуктивності близька до прямого виклику:

```csharp
// Один раз будуємо делегат
static readonly Action<PatientRecord, decimal> SetBmiDelegate =
    (Action<PatientRecord, decimal>)
    typeof(PatientRecord)
        .GetMethod("SetBmi")!
        .CreateDelegate(typeof(Action<PatientRecord, decimal>));

// Гарячий шлях — майже без overhead
foreach (var patient in patients)
    SetBmiDelegate(patient, 22.5m);
```

Цей підхід використовує Entity Framework для виклику методів властивостей, ASP.NET для прив'язки параметрів запиту, AutoMapper для маппінгу значень.

---

## Приклад 1 — PatientRecord: дослідження сигнатур та виклик через Invoke

```csharp
using System;
using System.Linq;
using System.Reflection;

Type t = typeof(PatientRecord);

Console.WriteLine("=== Методи PatientRecord (власні, без IsSpecialName) ===\n");

var flags = BindingFlags.Public | BindingFlags.NonPublic
          | BindingFlags.Instance | BindingFlags.Static
          | BindingFlags.DeclaredOnly;

foreach (MethodInfo m in t.GetMethods(flags).Where(m => !m.IsSpecialName))
{
    string access = m.IsPublic ? "public" : m.IsFamily ? "protected" : "private";
    string modifier = m.IsStatic ? " static" : m.IsAbstract ? " abstract"
                    : m.IsVirtual ? " virtual" : "";

    string ret = m.ReturnType == typeof(void) ? "void" : m.ReturnType.Name;

    var pars = m.GetParameters().Select(p =>
    {
        string mod = p.IsOut ? "out " : p.IsIn ? "in " : "";
        string def = p.HasDefaultValue ? $" = {p.DefaultValue}" : "";
        return $"{mod}{p.ParameterType.Name} {p.Name}{def}";
    });

    Console.WriteLine($"  {access}{modifier} {ret} {m.Name}({string.Join(", ", pars)})");
}

Console.WriteLine("\n=== Invoke: SetBmi → GetBmi ===\n");

var patient = new PatientRecord("Олена Петренко", new DateTime(1985, 3, 12));

MethodInfo setBmi = t.GetMethod("SetBmi", flags)!;
setBmi.Invoke(patient, new object[] { 26.3m });

MethodInfo getBmi = t.GetMethod("GetBmi", flags)!;
object? result = getBmi.Invoke(patient, null);
Console.WriteLine($"ІМТ після Invoke: {result}");

Console.WriteLine("\n=== TargetInvocationException ===\n");

try
{
    setBmi.Invoke(patient, new object[] { -1.0m });
}
catch (TargetInvocationException ex)
{
    Console.WriteLine($"TargetInvocationException: {ex.Message}");
    Console.WriteLine($"InnerException: {ex.InnerException?.GetType().Name} — {ex.InnerException?.Message}");
}

Console.WriteLine("\n=== Конструктори PatientRecord ===\n");

foreach (ConstructorInfo ctor in t.GetConstructors(
    BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic))
{
    string access = ctor.IsPublic ? "public" : ctor.IsPrivate ? "private" : "protected";
    var ps = ctor.GetParameters()
                 .Select(p => $"{p.ParameterType.Name} {p.Name}");
    Console.WriteLine($"  {access} PatientRecord({string.Join(", ", ps)})");
}

public class PatientRecord
{
    public string FullName { get; set; }
    public DateTime BirthDate { get; set; }
    private decimal _bmi;
    private string? _notes;

    public PatientRecord(string fullName, DateTime birthDate)
    {
        FullName = fullName;
        BirthDate = birthDate;
    }

    private PatientRecord() : this("Анонімний", DateTime.MinValue) { }

    public void SetBmi(decimal bmi)
    {
        if (bmi <= 0) throw new ArgumentOutOfRangeException(nameof(bmi), "ІМТ має бути додатнім");
        _bmi = bmi;
    }

    public decimal GetBmi() => _bmi;

    public void AddNote(string text) => _notes = text;
    public void AddNote(string text, DateTime timestamp)
        => _notes = $"[{timestamp:d}] {text}";

    public string GetSummary() => $"Пацієнт: {FullName}, ІМТ: {_bmi:F1}";
    public static PatientRecord CreateAnonymous() => new();

    protected virtual string FormatForExport() =>
        $"{FullName};{BirthDate:yyyy-MM-dd};{_bmi}";
}
```

---

## Приклад 2 — MethodDispatcher<T>: кешування та CreateDelegate

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;

// Демонстрація кешування MethodInfo і CreateDelegate для гарячого шляху.
var patients = new[]
{
    new PatientRecord("Іван Коваль",   new DateTime(1980, 5, 15)),
    new PatientRecord("Марія Гончар",  new DateTime(1992, 11, 3)),
    new PatientRecord("Петро Мельник", new DateTime(1965, 8, 22)),
};

// Стандартний MethodDispatcher через кешований MethodInfo
var dispatcher = new MethodDispatcher<PatientRecord>();

Console.WriteLine("=== Invoke через кешований MethodInfo ===\n");

dispatcher.Invoke(patients[0], "SetBmi", 23.1m);
dispatcher.Invoke(patients[1], "SetBmi", 30.4m);
dispatcher.Invoke(patients[2], "SetBmi", 26.7m);

foreach (var p in patients)
{
    object? summary = dispatcher.Invoke(p, "GetSummary");
    Console.WriteLine($"  {summary}");
}

Console.WriteLine("\n=== CreateDelegate — гарячий шлях ===\n");

// Будуємо делегат одноразово
Action<PatientRecord, decimal> fastSetBmi =
    (Action<PatientRecord, decimal>)
    typeof(PatientRecord)
        .GetMethod("SetBmi")!
        .CreateDelegate(typeof(Action<PatientRecord, decimal>));

Func<PatientRecord, string> fastGetSummary =
    (Func<PatientRecord, string>)
    typeof(PatientRecord)
        .GetMethod("GetSummary")!
        .CreateDelegate(typeof(Func<PatientRecord, string>));

// Гарячий шлях: майже без overhead рефлексії
foreach (var p in patients)
{
    fastSetBmi(p, 25.0m);
    Console.WriteLine($"  {fastGetSummary(p)}");
}

Console.WriteLine("\n=== Activator.CreateInstance ===\n");

// Динамічне створення за Type (наприклад, з рядка конфігурації)
Type recordType = Type.GetType("PatientRecord") ?? typeof(PatientRecord);
object? newRecord = Activator.CreateInstance(
    recordType, "Оксана Лисенко", new DateTime(1990, 2, 14));
Console.WriteLine(dispatcher.Invoke(newRecord!, "GetSummary"));

public class PatientRecord
{
    public string FullName { get; set; }
    public DateTime BirthDate { get; set; }
    private decimal _bmi;

    public PatientRecord(string fullName, DateTime birthDate)
    {
        FullName = fullName;
        BirthDate = birthDate;
    }

    public void SetBmi(decimal bmi) => _bmi = Math.Max(0, bmi);
    public decimal GetBmi() => _bmi;
    public string GetSummary() => $"Пацієнт: {FullName}, ІМТ: {_bmi:F1}";
}

public class MethodDispatcher<T>
{
    private readonly Dictionary<string, MethodInfo> _cache = new();

    private MethodInfo Resolve(string name)
    {
        if (!_cache.TryGetValue(name, out var mi))
        {
            mi = typeof(T).GetMethod(name,
                     BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance)
                 ?? throw new MissingMethodException(typeof(T).Name, name);
            _cache[name] = mi;
        }
        return mi;
    }

    public object? Invoke(object target, string methodName, params object[] args)
    {
        try
        {
            return Resolve(methodName).Invoke(target, args.Length == 0 ? null : args);
        }
        catch (TargetInvocationException ex) when (ex.InnerException is not null)
        {
            System.Runtime.ExceptionServices.ExceptionDispatchInfo
                .Capture(ex.InnerException).Throw();
            return null; // недосяжний код
        }
    }

    public int CacheSize => _cache.Count;
}
```

`MethodDispatcher<T>` демонструє три речі: кешування `MethodInfo` у словнику за ім'ям, «розпакування» `TargetInvocationException` через `ExceptionDispatchInfo`, і параметр `params object[]` для зручного синтаксису виклику. Поруч — делегати через `CreateDelegate` як найефективніший варіант для повторюваних викликів на одному типі.
