---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
section: 4
number: "14.4"
title: "Дослідження полів та властивостей за допомогою рефлексії"
source: "../_combined/87-doslidzhennia-poliv-ta-vlastyvostei-za-dopomohoiu-refleksii.md"
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

| Модифікатор | `IsLiteral` | `IsInitOnly` | Примітки |
|-------------|-------------|--------------|----------|
| `const` | `true` | `false` | значення вбудоване в IL; завжди `static` логічно |
| `readonly` | `false` | `true` | може бути instance або static |
| `static readonly` | `false` | `true` + `IsStatic=true` | поєднання обох |
| Звичайне поле | `false` | `false` | — |

Для **`const`**-поля `GetValue(null)` повертає вбудоване значення (аргумент `obj` ігнорується — поле не прив'язане до екземпляра). Спроба `SetValue` на `const` або `readonly` кидає `FieldAccessException`:

```csharp
FieldInfo maxAgeField = typeof(PatientRecord)
    .GetField("MaxAge", BindingFlags.Public | BindingFlags.Static)!;

// const — читаємо через null
object? val = maxAgeField.GetValue(null);
Console.WriteLine($"MaxAge = {val}"); // MaxAge = 150

// SetValue → FieldAccessException
maxAgeField.SetValue(null, 200); // кидає!
```

Є один спосіб обійти захист `readonly` (але не `const`) — через хак з `RuntimeFieldHandle` чи встановлення через IL-генерацію. У реальних проєктах це вважається небезпечним патерном і застосовується тільки в тестових фреймворках для заміни залежностей.

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

### init-only setter (C# 9) — прихована пастка

C# 9 ввів `init`-аксесор: `public string Name { get; init; }`. Рефлексія показує `CanWrite = true`, бо setter технічно існує. Але `SetValue` все одно кидає `FieldAccessException`, оскільки init-setter позначений атрибутом `[IsExternalInit]` і компілятор дозволяє його виклик лише з конструктора або ініціалізатора об'єкта.

```csharp
PropertyInfo nameProp = typeof(PatientRecord).GetProperty("FullName")!;
Console.WriteLine(nameProp.CanWrite); // true — вводить в оману!

var patient = new PatientRecord("Іван Коваль", new DateTime(1980, 1, 1));

// Кидає FieldAccessException:
nameProp.SetValue(patient, "Петро Мельник");
```

**Обхід**: знайти backing field і записати напряму через `FieldInfo.SetValue`:

```csharp
FieldInfo? backing = typeof(PatientRecord)
    .GetField("<FullName>k__BackingField",
              BindingFlags.NonPublic | BindingFlags.Instance);
backing?.SetValue(patient, "Петро Мельник");
```

Цей підхід використовується в тестових фреймворках (Moq, NSubstitute) для підміни значень `init`-властивостей під час налаштування тестових об'єктів. У продакшн-коді це вважається антипатерном — краще переробити дизайн.

## Workflow GetValue і SetValue

Порядок дій при роботі з полями і властивостями через рефлексію відповідає п'яти крокам з діаграми:

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

## Приклад 2 — ObjectCloner\<T\>: deep copy через FieldInfo

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
        T target = (T)System.Runtime.Serialization.FormatterServices
            .GetUninitializedObject(typeof(T));

        foreach (var field in Fields)
        {
            object? val = field.GetValue(source);

            // init-only (IsInitOnly) — записуємо через поле, а не setter
            // readonly та init-only поля: IsInitOnly=true
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

`ObjectCloner<T>` демонструє реальну техніку клонування через рефлексію: `FormatterServices.GetUninitializedObject` обходить конструктор (критично для `init`-властивостей, де конструктор може бути незрозумілим), `IsLiteral` фільтрує `const`-поля (вони не копіюються, бо належать типу, а не екземпляру), а `IsInitOnly` документує, що backing-поля `init`-властивостей все одно записуються через `FieldInfo.SetValue` — це єдиний легальний спосіб обійти init-обмеження після конструктора.
