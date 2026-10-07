---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
section: 4
number: "14.4"
title: "Дослідження полів та властивостей за допомогою рефлексії"
---

## 14.4. Дослідження полів та властивостей за допомогою рефлексії

У попередньому розділі ми досліджували методи та конструктори через `MethodInfo` і `ConstructorInfo`. Тепер розглянемо, як рефлексія дозволяє читати і змінювати **дані** типу — поля через `FieldInfo` та властивості через `PropertyInfo`.

Ці два класи виглядають схожими (обидва мають `GetValue` і `SetValue`), але представляють різні рівні абстракції. **Поле** — це пряма ділянка пам'яті об'єкта. **Властивість** — абстракція з get/set-аксесорами, які можуть містити довільну логіку, кидати виключення і бути реалізовані через backing-field або взагалі обчислюватись динамічно.

![FieldInfo та PropertyInfo — читання та запис значень через рефлексію](_assets/14-04/fields-properties.png)

## Клас FieldInfo

`FieldInfo` описує одне поле класу або структури. Ключові властивості:

| Властивість | Що повертає |
|-------------|-------------|
| `.Name` | ім'я поля: `"_bmi"`, `"<FullName>k__BackingField"` |
| `.FieldType` | `Type` поля |
| `.IsPublic` | `true` якщо `public` |
| `.IsPrivate` | `true` якщо `private` |
| `.IsFamily` | `true` якщо `protected` |
| `.IsAssembly` | `true` якщо `internal` |
| `.IsStatic` | `true` якщо `static` |
| `.IsInitOnly` | `true` якщо `readonly` |
| `.IsLiteral` | `true` якщо `const` (значення вбудовано на етапі компіляції) |
| `.IsNotSerialized` | `true` якщо є `[NonSerialized]` |
| `.GetValue(obj)` | прочитати значення поля у об'єкта `obj` |
| `.SetValue(obj, val)` | записати значення `val` у поле об'єкта `obj` |

### const vs readonly через рефлексію

Обидва ключових слова задають поля, значення яких не змінюється — але механізм різний, і рефлексія це чітко розрізняє:

| Модифікатор | `IsLiteral` | `IsInitOnly` | `SetValue` | Примітки |
|-------------|-------------|--------------|------------|----------|
| `const` | `true` | `false` | `FieldAccessException` | значення вбудоване в IL; завжди `static` логічно |
| `static readonly` | `false` | `true` + `IsStatic=true` | `FieldAccessException` | після ініціалізації типу змінити не можна |
| `readonly` (екземпляра) | `false` | `true` | **працює** | `readonly` — обмеження компілятора, не рефлексії |
| Звичайне поле | `false` | `false` | працює | — |

Для **`const`**-поля `GetValue(null)` повертає вбудоване значення (аргумент `obj` ігнорується — поле не прив'язане до екземпляра). Записати його неможливо в принципі: значення `const` компілятор **копіює** в IL кожного місця використання, тож у пам'яті немає комірки, яку можна було б змінити. Тому `SetValue` на `const` кидає `FieldAccessException`:

```csharp
FieldInfo maxAgeField = typeof(PatientRecord)
    .GetField("MaxAge", BindingFlags.Public | BindingFlags.Static)!;

// const — читаємо через null
object? val = maxAgeField.GetValue(null);
Console.WriteLine($"MaxAge = {val}"); // MaxAge = 150

// SetValue → FieldAccessException
maxAgeField.SetValue(null, 200); // кидає!
```

З `readonly`-полями ситуація інша, і вона часто дивує. Ключове слово `readonly` — це обіцянка, яку перевіряє **компілятор C#**: він не дозволить написати присвоєння поза конструктором. Але рефлексія працює вже на рівні CLR, тож для `readonly`-поля **екземпляра** `SetValue` спрацьовує без жодних хаків:

```csharp
// у класі PatientRecord: private readonly double _weight;
FieldInfo weight = typeof(PatientRecord)
    .GetField("_weight", BindingFlags.NonPublic | BindingFlags.Instance)!;

Console.WriteLine(weight.IsInitOnly);   // True — поле readonly
weight.SetValue(patient, 82.5);         // працює: значення змінено
```

Винятком є **`static readonly`**-поля: починаючи з .NET Core 3.0, після того як статичний конструктор типу відпрацював, CLR забороняє їх змінювати — `SetValue` кидає `FieldAccessException`. Причина в оптимізації: JIT має право вбудувати значення `static readonly` у машинний код як константу, і зміна поля після цього призвела б до неузгодженого стану.

Практичний висновок: `readonly` захищає від помилок у **вашому** коді, але не від рефлексії. Якщо бібліотека чи серіалізатор має доступ до об'єкта через рефлексію, він технічно може змінити його `readonly`-поля. Робити так у продакшн-коді не варто — це руйнує інваріанти класу; такий прийом трапляється хіба що в тестових інструментах і десеріалізаторах.

## Клас PropertyInfo

`PropertyInfo` описує одну властивість. Ключові члени:

| Властивість / Метод | Що повертає |
|---------------------|-------------|
| `.Name` | ім'я властивості: `"FullName"`, `"BirthDate"` |
| `.PropertyType` | `Type` значення властивості |
| `.CanRead` | `true` якщо є getter |
| `.CanWrite` | `true` якщо є setter або init-accessor |
| `.GetMethod` | `MethodInfo?` — getter як метод |
| `.SetMethod` | `MethodInfo?` — setter як метод |
| `.GetValue(obj)` | прочитати значення властивості |
| `.SetValue(obj, val)` | записати значення властивості |
| `.GetIndexParameters()` | `ParameterInfo[]` — для індексаторів (`this[int]`) |
| `.GetAccessors()` | масив `MethodInfo` — get + set разом |

Ключовий момент: `.GetMethod` і `.SetMethod` — це справжні `MethodInfo`. Через них можна перевірити модифікатор доступу аксесора:

```csharp
PropertyInfo prop = typeof(PatientRecord).GetProperty("RecordId")!;

Console.WriteLine(prop.CanRead);               // true
Console.WriteLine(prop.CanWrite);              // true (init)
Console.WriteLine(prop.GetMethod!.IsPublic);   // true
Console.WriteLine(prop.SetMethod!.IsPublic);   // true (але init-only)
```

### init-only setter (C# 9) — обмеження лише для компілятора

C# 9 ввів `init`-аксесор: `public string Name { get; init; }`. Такий аксесор — це звичайний метод-setter (`set_Name`), у сигнатурі якого компілятор залишає спеціальну позначку — обов'язковий модифікатор `IsExternalInit`. Компілятор C#, побачивши цю позначку, дозволяє викликати setter лише з конструктора або ініціалізатора об'єкта (`new PatientRecord { Name = "…" }`). А от для рефлексії й CLR це звичайний setter.

Тому рефлексія показує `CanWrite = true`, і `SetValue` **справді записує** значення — навіть після того, як об'єкт уже створено:

```csharp
PropertyInfo nameProp = typeof(PatientRecord).GetProperty("FullName")!;
Console.WriteLine(nameProp.CanWrite); // True — setter існує

var patient = new PatientRecord("Іван Коваль", new DateTime(1980, 1, 1));

nameProp.SetValue(patient, "Петро Мельник"); // працює
Console.WriteLine(patient.FullName);         // Петро Мельник
```

Так само працює і запис у приховане backing-поле властивості (`<FullName>k__BackingField`): компілятор позначає його як `readonly` (`IsInitOnly = true`), але, як ми бачили вище, для полів екземпляра це не заважає `FieldInfo.SetValue`.

Як відрізнити `init` від звичайного `set`, якщо це потрібно (наприклад, генератору документації)? Перевірити модифікатор у сигнатурі setter-а:

```csharp
bool isInit = nameProp.SetMethod?.ReturnParameter
    .GetRequiredCustomModifiers()
    .Any(m => m.Name == "IsExternalInit") ?? false;
```

Отже, `init`, як і `readonly`, — це гарантія **компілятора** для звичайного коду, а не захист від рефлексії. Серіалізатори (наприклад, `System.Text.Json`) якраз користуються цим, щоб заповнювати `init`-властивості під час десеріалізації. У прикладному коді змінювати `init`-властивості через рефлексію після створення об'єкта — антипатерн: це порушує задум автора класу, який розраховував на незмінність.

## Workflow GetValue і SetValue

Порядок дій при роботі з полями і властивостями через рефлексію відповідає трьом крокам з діаграми (знайти → прочитати → записати):

```csharp
Type t = typeof(PatientRecord);
var patient = new PatientRecord("Олена Петренко", new DateTime(1985, 3, 12));

// 1. Отримати FieldInfo / PropertyInfo з BindingFlags
FieldInfo? bmiField = t.GetField("_bmi",
    BindingFlags.NonPublic | BindingFlags.Instance);

PropertyInfo? fullNameProp = t.GetProperty("FullName",
    BindingFlags.Public | BindingFlags.Instance);

// 2. Перевірити CanRead / CanWrite (для Property)
if (fullNameProp is { CanRead: true, CanWrite: true })
{
    // 3. GetValue → object? (boxing для value-типів)
    object? name = fullNameProp.GetValue(patient);
    Console.WriteLine(name); // Олена Петренко

    // 4. SetValue — val приводиться до PropertyType
    fullNameProp.SetValue(patient, "Марія Гончар");

    // 5. Розкастити результат
    string updated = (string)fullNameProp.GetValue(patient)!;
    Console.WriteLine(updated); // Марія Гончар
}

// Читання приватного поля через FieldInfo
object? rawBmi = bmiField?.GetValue(patient);
decimal bmi = rawBmi is null ? 0m : (decimal)rawBmi;
```

Для **статичних** полів і властивостей аргумент `obj` у `GetValue`/`SetValue` передається як `null`:

```csharp
FieldInfo? maxAge = t.GetField("MaxAge", BindingFlags.Public | BindingFlags.Static);
object? val = maxAge?.GetValue(null);  // null для static
```

## Практичне застосування

**Серіалізація** — JSON/XML-серіалізатори проходять по всіх публічних властивостях типу і перетворюють значення в рядок. Базова схема:

```csharp
var props = t.GetProperties(BindingFlags.Public | BindingFlags.Instance)
             .Where(p => p.CanRead);
foreach (var p in props)
    json[p.Name] = p.GetValue(obj)?.ToString() ?? "null";
```

**ORM (Entity Framework Core)** — при матеріалізації запиту EF Core записує значення кожної колонки в відповідну властивість об'єкта через `SetValue` або через скомпільований `Expression`. Рефлексія тут — фундамент маппінгу колонка↔властивість.

**AutoMapper** — при конфігурації маппінгу бібліотека одноразово будує словник `PropertyInfo` для джерела і цілі, потім кожен маппінг читає `GetValue` і пише `SetValue`. Кешування `PropertyInfo` є обов'язковим.

**Клонування об'єктів** — deep copy через перебір `GetFields` з копіюванням `GetValue→SetValue` для кожного поля нового примірника. Правильна реалізація пропускає `IsLiteral`-поля і backing-поля, які обробляються через властивості.

**Валідатори** — перевірка атрибутів на властивостях `[Required]`, `[Range]`, `[MaxLength]` через `GetCustomAttributes()` + `GetValue()` для отримання фактичного значення.

---

## Приклад 1 — PatientRecord: інспекція полів і маніпуляції значеннями

```csharp
using System;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;

Type t = typeof(PatientRecord);
var patient = new PatientRecord("Олена Петренко", new DateTime(1985, 3, 12)) { RecordId = 42 };

Console.WriteLine("=== Усі поля (з категоризацією) ===\n");

var allFields = t.GetFields(
    BindingFlags.Public | BindingFlags.NonPublic |
    BindingFlags.Instance | BindingFlags.Static);

foreach (var f in allFields)
{
    bool isBacking = f.IsDefined(typeof(CompilerGeneratedAttribute), false);
    string category = f.IsLiteral ? "const" : f.IsInitOnly ? "readonly"
                    : isBacking ? "backing" : "field";
    string access   = f.IsPublic ? "public" : f.IsFamily ? "protected" : "private";
    string stat     = f.IsStatic ? " static" : "";

    object? val = f.IsStatic ? f.GetValue(null) : f.GetValue(patient);
    Console.WriteLine($"  [{category}] {access}{stat} {f.FieldType.Name,-12} {f.Name,-30} = {val}");
}

Console.WriteLine("\n=== Властивості з CanRead/CanWrite ===\n");

foreach (var p in t.GetProperties(BindingFlags.Public | BindingFlags.Instance))
{
    string rw = (p.CanRead ? "get" : "") + (p.CanWrite ? "; set" : "");
    bool isInit = p.SetMethod?.ReturnParameter
                    .GetRequiredCustomModifiers()
                    .Any(m => m.Name == "IsExternalInit") ?? false;
    if (isInit) rw += " [init-only]";

    object? val = p.CanRead ? p.GetValue(patient) : "—";
    Console.WriteLine($"  {p.PropertyType.Name,-12} {p.Name,-15} [{rw}]  = {val}");
}

Console.WriteLine("\n=== SetValue через PropertyInfo ===\n");

var ageProp = t.GetProperty("BirthDate");
ageProp?.SetValue(patient, new DateTime(1990, 7, 22));
Console.WriteLine($"  BirthDate після SetValue: {patient.BirthDate:yyyy-MM-dd}");

Console.WriteLine("\n=== SetValue через FieldInfo (приватне поле _bmi) ===\n");

var bmiField = t.GetField("_bmi", BindingFlags.NonPublic | BindingFlags.Instance);
bmiField?.SetValue(patient, 27.4m);
Console.WriteLine($"  _bmi через GetValue: {bmiField?.GetValue(patient)}");
Console.WriteLine($"  GetBmi(): {patient.GetBmi()}");

Console.WriteLine("\n=== const-поле через GetValue(null) ===\n");

var maxAgeField = t.GetField("MaxAge", BindingFlags.Public | BindingFlags.Static);
Console.WriteLine($"  MaxAge = {maxAgeField?.GetValue(null)}");

public class PatientRecord
{
    public const int MaxAge = 150;
    public static readonly string DefaultWard = "Загальна терапія";

    public string FullName { get; set; }
    public DateTime BirthDate { get; set; }
    public int RecordId { get; init; }

    private decimal _bmi;
    private string? _notes;

    public PatientRecord(string fullName, DateTime birthDate)
    {
        FullName = fullName;
        BirthDate = birthDate;
    }

    public void SetBmi(decimal bmi) => _bmi = Math.Max(0, bmi);
    public decimal GetBmi() => _bmi;
    public void AddNote(string text) => _notes = text;
    public string GetSummary() => $"Пацієнт: {FullName}, ІМТ: {_bmi:F1}";
}
```

---

## Приклад 2 — ObjectCloner<T>: deep copy через FieldInfo

```csharp
using System;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;

var original = new PatientRecord("Іван Коваль", new DateTime(1975, 5, 20)) { RecordId = 7 };
original.SetBmi(25.1m);
original.AddNote("Перший візит");

var clone = ObjectCloner<PatientRecord>.Clone(original);

Console.WriteLine("=== Оригінал ===");
Console.WriteLine(original.GetSummary());
Console.WriteLine($"RecordId: {original.RecordId}");

Console.WriteLine("\n=== Клон (після Clone) ===");
Console.WriteLine(clone.GetSummary());
Console.WriteLine($"RecordId: {clone.RecordId}");

// Перевірка незалежності
original.SetBmi(30.0m);
Console.WriteLine("\n=== Після зміни оригіналу ===");
Console.WriteLine($"Оригінал ІМТ: {original.GetBmi()}");
Console.WriteLine($"Клон ІМТ:     {clone.GetBmi()}");

public class PatientRecord
{
    public const int MaxAge = 150;

    public string FullName { get; set; }
    public DateTime BirthDate { get; set; }
    public int RecordId { get; init; }

    private decimal _bmi;
    private string? _notes;

    public PatientRecord(string fullName, DateTime birthDate)
    {
        FullName = fullName;
        BirthDate = birthDate;
    }

    public void SetBmi(decimal bmi) => _bmi = Math.Max(0, bmi);
    public decimal GetBmi() => _bmi;
    public void AddNote(string text) => _notes = text;
    public string GetSummary() => $"Пацієнт: {FullName}, ІМТ: {_bmi:F1}, Нотатка: {_notes}";
}

public static class ObjectCloner<T> where T : class
{
    private static readonly FieldInfo[] Fields = typeof(T)
        .GetFields(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance)
        .Where(f => !f.IsLiteral)  // пропускаємо const (IsLiteral)
        .ToArray();

    public static T Clone(T source)
    {
        // Створюємо порожній об'єкт без виклику конструктора
        T target = (T)RuntimeHelpers.GetUninitializedObject(typeof(T));

        foreach (var field in Fields)
        {
            object? val = field.GetValue(source);

            // readonly-поля і backing-поля init-властивостей мають IsInitOnly=true,
            // але для полів екземпляра SetValue все одно працює
            // Для value-типів та рядків shallow copy достатньо
            field.SetValue(target, val);
        }

        return target;
    }

    public static void PrintCopiedFields()
    {
        Console.WriteLine($"\nObjectCloner<{typeof(T).Name}> копіює {Fields.Length} полів:");
        foreach (var f in Fields)
        {
            bool isBacking = f.IsDefined(typeof(CompilerGeneratedAttribute), false);
            bool isReadonly = f.IsInitOnly;
            string tags = string.Join(", ", new[]
            {
                isBacking  ? "backing" : null,
                isReadonly ? "readonly/init" : null,
                f.IsStatic ? "static" : null,
            }.Where(x => x is not null));

            Console.WriteLine($"  {f.FieldType.Name,-15} {f.Name}" +
                              (tags.Length > 0 ? $"  [{tags}]" : ""));
        }
    }
}
```

`ObjectCloner<T>` демонструє реальну техніку клонування через рефлексію: `RuntimeHelpers.GetUninitializedObject` створює об'єкт в обхід конструктора (не потрібно знати, які аргументи йому передати; старий аналог `FormatterServices.GetUninitializedObject` позначено застарілим), `IsLiteral` фільтрує `const`-поля (вони не копіюються, бо належать типу, а не екземпляру), а копіювання на рівні полів автоматично охоплює і backing-поля `init`-властивостей: хоча вони мають `IsInitOnly = true`, для полів екземпляра `FieldInfo.SetValue` працює. Копіювати саме поля, а не властивості, тут правильно: так ми не викликаємо логіку setter-ів і отримуємо точну копію стану.
