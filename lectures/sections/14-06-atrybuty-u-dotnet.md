---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
section: 6
number: "14.6"
title: "Атрибути у .NET"
source: "../_combined/89-atrybuty-u-dotnet.md"
---

## 14.6. Атрибути у .NET

Атрибути — це спосіб додати **декларативні метадані** до елементів коду: класів, методів, властивостей, параметрів, полів, або навіть до цілої збірки. На відміну від коментарів, атрибути вбудовуються в IL-код збірки і доступні через рефлексію під час виконання. Саме це робить їх потужним інструментом: фреймворки читають атрибути і автоматично змінюють поведінку — валідують, серіалізують, маплять на БД, реєструють у DI.

Усі атрибути успадковують від абстрактного класу `System.Attribute`. Синтаксично атрибут — це клас із конструктором; значення, передані у квадратних дужках, — це аргументи конструктора або іменовані властивості.

![Атрибути — Attribute, AttributeUsage, читання через рефлексію](_assets/14-06/attributes.png)

## Вбудовані атрибути .NET

.NET постачає велику кількість стандартних атрибутів для різних потреб:

| Атрибут | Де застосовується | Призначення |
|---------|-------------------|-------------|
| `[Obsolete]` | метод, клас | попереджає про застарілий API, опціонально — помилка компіляції |
| `[Serializable]` | клас | дозволяє серіалізацію (BinaryFormatter) |
| `[NonSerialized]` | поле | виключає поле з серіалізації |
| `[DllImport]` | метод | P/Invoke — виклик нативного коду |
| `[Flags]` | enum | дозволяє бітові операції над значеннями |
| `[AttributeUsage]` | клас атрибута | обмежує де і як може застосовуватись атрибут |
| `[CallerMemberName]` | параметр | компілятор підставляє ім'я викликача (для `INotifyPropertyChanged`) |
| `[Required]` | властивість | валідація — поле обов'язкове (DataAnnotations) |
| `[JsonPropertyName]` | властивість | ім'я ключа при JSON-серіалізації |
| `[CompilerGenerated]` | будь-що | позначає згенерований компілятором код (backing fields і т.д.) |

### Суфікс Attribute — конвенція

За конвенцією .NET класи атрибутів мають суфікс `Attribute`. При застосуванні суфікс можна **опустити**: `[Obsolete]` і `[ObsoleteAttribute]` — повністю еквівалентні записи. Компілятор шукає обидва варіанти. Якщо є обидва класи (`Foo` і `FooAttribute`), використовується повне ім'я з `Attribute`.

## Власний атрибут — анатомія

Власний атрибут — це звичайний клас, успадкований від `System.Attribute`. Йому можна додати конструктор з позиційними параметрами і публічні властивості для іменованих параметрів.

```csharp
[AttributeUsage(AttributeTargets.Property, AllowMultiple = false, Inherited = true)]
public sealed class ValidationRangeAttribute : Attribute
{
    public double Min { get; }
    public double Max { get; }
    public string? Message { get; set; }

    public ValidationRangeAttribute(double min, double max)
    {
        Min = min;
        Max = max;
    }
}
```

Застосування з позиційними і іменованими параметрами:

```csharp
public class PatientRecord
{
    [ValidationRange(0, 300, Message = "ІМТ поза нормою")]
    public decimal Bmi { get; set; }

    [ValidationRange(30, 220)]
    public int HeartRate { get; set; }
}
```

- `0, 300` — позиційні аргументи → передаються в конструктор
- `Message = "..."` — іменований аргумент → встановлюється як властивість після виклику конструктора

Клас атрибута рекомендується оголошувати `sealed` — атрибути рідко потребують успадкування, а `sealed` запобігає випадковому розширенню і прискорює перевірку CLR.

## [AttributeUsage] — обмеження застосування

`[AttributeUsage]` декорує сам клас атрибута і задає три речі:

**1. `AttributeTargets` — де може застосовуватись атрибут:**

```csharp
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct)]
// Тільки на класах і структурах

[AttributeUsage(AttributeTargets.Property | AttributeTargets.Field)]
// Тільки на властивостях і полях

[AttributeUsage(AttributeTargets.All)]
// Будь-який елемент коду
```

Повний список цілей: `Assembly`, `Module`, `Class`, `Struct`, `Enum`, `Constructor`, `Method`, `Property`, `Field`, `Event`, `Interface`, `Parameter`, `Delegate`, `ReturnValue`, `GenericParameter`, `All`.

**2. `AllowMultiple` — чи можна застосувати кілька разів:**

```csharp
[AttributeUsage(AttributeTargets.Method, AllowMultiple = true)]
public sealed class RouteAttribute : Attribute
{
    public string Path { get; }
    public RouteAttribute(string path) => Path = path;
}

// Тепер можна:
[Route("/patients")]
[Route("/records")]
public class PatientController { }
```

За замовчуванням `AllowMultiple = false` — компілятор заборонить дублювання.

**3. `Inherited` — чи передається атрибут нащадкам:**

```csharp
[AttributeUsage(AttributeTargets.Class, Inherited = false)]
// Атрибут на BaseClass НЕ видно через typeof(DerivedClass).GetCustomAttributes(true)

[AttributeUsage(AttributeTargets.Class, Inherited = true)]  // за замовчуванням
// Атрибут успадковується нащадками
```

**Важливо:** для **інтерфейсів** `Inherited` завжди `false` незалежно від налаштування — це рішення CLR. Клас, що реалізує інтерфейс, не «успадковує» атрибути цього інтерфейсу.

## Читання атрибутів через рефлексію

Усі `MemberInfo`-нащадки — `Type`, `MethodInfo`, `PropertyInfo`, `FieldInfo`, `ParameterInfo`, а також `Assembly` — підтримують один і той самий API читання атрибутів:

| Метод | Що повертає |
|-------|-------------|
| `IsDefined(Type, bool)` | `true`/`false` — найшвидша перевірка наявності |
| `GetCustomAttribute<T>()` | `T?` — один атрибут або `null` |
| `GetCustomAttributes<T>()` | `IEnumerable<T>` — усі атрибути типу T |
| `GetCustomAttributes(bool inherit)` | `object[]` — усі атрибути |
| `GetCustomAttributesData()` | `IList<CustomAttributeData>` — сирі дані без інстанціювання |

Параметр `inherit` у `GetCustomAttributes(bool)`:
- `true` — шукати атрибут і в базових класах (для методів і класів)
- `false` — тільки на цьому конкретному елементі

```csharp
Type t = typeof(PatientRecord);

// Перевірити наявність (без виділення пам'яті)
bool hasRange = t.GetProperty("Bmi")!
    .IsDefined(typeof(ValidationRangeAttribute), false);

// Отримати один конкретний атрибут
ValidationRangeAttribute? attr = t.GetProperty("Bmi")!
    .GetCustomAttribute<ValidationRangeAttribute>();

if (attr is not null)
    Console.WriteLine($"ІМТ: [{attr.Min}..{attr.Max}]");

// Отримати всі атрибути методу
MethodInfo m = t.GetMethod("GetSummary")!;
foreach (var a in m.GetCustomAttributes(inherit: false))
    Console.WriteLine(a.GetType().Name);
```

### GetCustomAttributesData — без інстанціювання атрибута

`GetCustomAttributesData()` повертає `CustomAttributeData` — опис атрибута через його конструктор і аргументи **без** виклику `new`. Це корисно для інструментів аналізу коду та генераторів, де інстанціювати атрибут може бути небажаним:

```csharp
foreach (var data in typeof(PatientRecord).GetCustomAttributesData())
{
    Console.WriteLine($"Атрибут: {data.AttributeType.Name}");
    foreach (var arg in data.ConstructorArguments)
        Console.WriteLine($"  arg: {arg.Value}");
    foreach (var named in data.NamedArguments)
        Console.WriteLine($"  {named.MemberName} = {named.TypedValue.Value}");
}
```

---

## Приклад 1 — PatientRecord: власні атрибути та рефлексійний валідатор

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;

// Валідація через атрибути
var patient1 = new PatientRecord("Іван Коваль",   26.5m, 72,  38.6f);
var patient2 = new PatientRecord("Марія Гончар",  35.0m, 110, 36.6f);
var patient3 = new PatientRecord("Петро Мельник", 15.0m, 55,  40.2f);

var validator = new AttributeValidator<PatientRecord>();

foreach (var patient in new[] { patient1, patient2, patient3 })
{
    var errors = validator.Validate(patient);
    if (errors.Count == 0)
        Console.WriteLine($"  {patient.FullName}: ✓ валідний");
    else
    {
        Console.WriteLine($"  {patient.FullName}: {errors.Count} помилок");
        foreach (var e in errors)
            Console.WriteLine($"    [{e.Property}] {e.Message}");
    }
}

// ===================== Атрибути =====================
[AttributeUsage(AttributeTargets.Property, AllowMultiple = false, Inherited = true)]
public sealed class MedRangeAttribute : Attribute
{
    public double Min { get; }
    public double Max { get; }
    public string Message { get; set; } = "Значення поза допустимим діапазоном";

    public MedRangeAttribute(double min, double max)
    {
        Min = min;
        Max = max;
    }
}

[AttributeUsage(AttributeTargets.Property)]
public sealed class MedRequiredAttribute : Attribute
{
    public string Message { get; set; } = "Поле обов'язкове";
}

// ===================== Модель =====================
public class PatientRecord
{
    [MedRequired(Message = "ПІБ пацієнта обов'язкове")]
    public string FullName { get; }

    [MedRange(10.0, 60.0, Message = "ІМТ має бути від 10 до 60")]
    public decimal Bmi { get; }

    [MedRange(30, 200, Message = "ЧСС має бути від 30 до 200")]
    public int HeartRate { get; }

    [MedRange(35.0, 40.0, Message = "Температура поза нормою (35–40°C)")]
    public float Temperature { get; }

    public PatientRecord(string fullName, decimal bmi, int heartRate, float temperature)
    {
        FullName = fullName;
        Bmi = bmi;
        HeartRate = heartRate;
        Temperature = temperature;
    }
}

// ===================== Валідатор =====================
public record ValidationError(string Property, string Message);

public class AttributeValidator<T>
{
    private static readonly PropertyInfo[] Props = typeof(T)
        .GetProperties(BindingFlags.Public | BindingFlags.Instance);

    public List<ValidationError> Validate(T obj)
    {
        var errors = new List<ValidationError>();

        foreach (var prop in Props)
        {
            object? value = prop.GetValue(obj);

            // [MedRequired]
            var required = prop.GetCustomAttribute<MedRequiredAttribute>();
            if (required is not null)
            {
                if (value is null || (value is string s && string.IsNullOrWhiteSpace(s)))
                    errors.Add(new ValidationError(prop.Name, required.Message));
            }

            // [MedRange]
            var range = prop.GetCustomAttribute<MedRangeAttribute>();
            if (range is not null && value is not null)
            {
                double numeric = Convert.ToDouble(value);
                if (numeric < range.Min || numeric > range.Max)
                    errors.Add(new ValidationError(prop.Name, range.Message));
            }
        }

        return errors;
    }
}
```

---

## Приклад 2 — AttributeInspector: повна карта атрибутів типу

```csharp
using System;
using System.Linq;
using System.Reflection;

// Виводимо повну карту атрибутів PatientRecord
AttributeInspector.Inspect(typeof(PatientRecord));

// ===================== Атрибути =====================
[AttributeUsage(AttributeTargets.Property, AllowMultiple = true)]
public sealed class TagAttribute : Attribute
{
    public string Value { get; }
    public TagAttribute(string value) => Value = value;
}

[AttributeUsage(AttributeTargets.Method)]
public sealed class AuditLogAttribute : Attribute
{
    public string Action { get; set; } = "read";
    public bool IncludeArgs { get; set; } = false;
}

// ===================== Модель =====================
[Obsolete("Використовуйте ExtendedPatientRecord з версії 2.0", error: false)]
public class PatientRecord
{
    [Tag("pii"), Tag("required")]
    public string FullName { get; set; } = "";

    [Tag("metric")]
    public decimal Bmi { get; set; }

    public int HeartRate { get; set; }

    [AuditLog(Action = "export", IncludeArgs = true)]
    public string GetSummary() => $"{FullName}, ІМТ: {Bmi}";

    [AuditLog(Action = "update")]
    public void UpdateBmi(decimal newBmi) => Bmi = newBmi;
}

// ===================== Inspector =====================
public static class AttributeInspector
{
    public static void Inspect(Type t)
    {
        Console.WriteLine($"╔══ Атрибути типу: {t.Name} ══╗\n");

        // Атрибути типу
        var typeAttrs = t.GetCustomAttributes(inherit: false);
        Console.WriteLine($"  [Type] {t.Name}");
        foreach (var a in typeAttrs)
            Console.WriteLine($"    ← [{a.GetType().Name.Replace("Attribute", "")}] {FormatAttr(a)}");

        // Властивості
        Console.WriteLine("\n  [Properties]");
        foreach (var p in t.GetProperties(BindingFlags.Public | BindingFlags.Instance))
        {
            var attrs = p.GetCustomAttributes(inherit: false);
            if (!attrs.Any()) continue;
            Console.WriteLine($"    {p.PropertyType.Name,-12} {p.Name}");
            foreach (var a in attrs)
                Console.WriteLine($"      ← [{a.GetType().Name.Replace("Attribute", "")}] {FormatAttr(a)}");
        }

        // Методи
        Console.WriteLine("\n  [Methods]");
        var flags = BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly;
        foreach (var m in t.GetMethods(flags).Where(x => !x.IsSpecialName))
        {
            var attrs = m.GetCustomAttributes(inherit: false);
            if (!attrs.Any()) continue;
            var ps = string.Join(", ", m.GetParameters().Select(p => p.ParameterType.Name));
            Console.WriteLine($"    {m.ReturnType.Name,-10} {m.Name}({ps})");
            foreach (var a in attrs)
                Console.WriteLine($"      ← [{a.GetType().Name.Replace("Attribute", "")}] {FormatAttr(a)}");
        }

        Console.WriteLine("\n╚══════════════════════╝");
    }

    private static string FormatAttr(object attr) => attr switch
    {
        TagAttribute t          => $"Value=\"{t.Value}\"",
        AuditLogAttribute al    => $"Action=\"{al.Action}\", IncludeArgs={al.IncludeArgs}",
        ObsoleteAttribute obs   => $"\"{obs.Message}\" IsError={obs.IsError}",
        _                       => attr.ToString() ?? ""
    };
}
```

`AttributeInspector` демонструє ключові техніки: `GetCustomAttributes(inherit: false)` на `Type`, `PropertyInfo` і `MethodInfo`, фільтрацію `IsSpecialName` для пропуску `get_*`/`set_*`, підтримку `AllowMultiple = true` через `[Tag]` (кілька атрибутів на одній властивості), і роботу зі стандартними атрибутами на кшталт `[Obsolete]` — всі вони читаються абсолютно так само, як і власні.
