---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
section: 2
number: "14.2"
title: "Застосування рефлексії та дослідження типів"
source: "../_combined/85-zastosuvannia-refleksii-ta-doslidzhennia-typiv.md"
---

## 14.2. Застосування рефлексії та дослідження типів

Після того як ми отримали об'єкт `Type`, наступний крок — дослідити його **членів** (members): методи, поля, властивості, конструктори, події. Саме це і є серцем рефлексії: не просто знати, що тип існує, а отримати структурований опис кожного його елемента і, якщо потрібно, взаємодіяти з ним.

Базовим класом для всіх членів типу є абстрактний `MemberInfo` з простору імен `System.Reflection`. Від нього успадковують: `MethodInfo`, `ConstructorInfo`, `FieldInfo`, `PropertyInfo`, `EventInfo`. Кожен із них надає специфічний для свого виду API, але всі мають спільний базовий функціонал `MemberInfo`.

![GetMembers та BindingFlags — дослідження членів типу](_assets/14-02/binding-flags.png)

## Клас MemberInfo та його спільні властивості

Оскільки `GetMembers()` повертає `MemberInfo[]`, варто знати, що доступно через базовий клас для будь-якого члена незалежно від його виду:

| Властивість / Метод | Що повертає |
|---------------------|-------------|
| `.Name` | Ім'я члена: `"GetSummary"`, `"_bmi"`, `"Age"` |
| `.DeclaringType` | Тип, де **оголошено** цей член |
| `.ReflectedType` | Тип, через який **отримано** цей член |
| `.MemberType` | `MemberTypes.Method`, `.Field`, `.Property`, `.Constructor`, `.Event` |
| `.GetCustomAttributes(bool)` | Масив атрибутів, декорованих на члені |
| `.IsDefined(Type, bool)` | `true` якщо атрибут певного типу присутній |

### DeclaringType vs ReflectedType

Ця різниця важлива при роботі з ієрархіями класів. `DeclaringType` — тип, де метод або поле **фізично написане**. `ReflectedType` — тип, через `typeof(...)` якого ми дісталися до цього члена.

```csharp
class MedicalRecord
{
    public string GetSummary() => "Base summary";
}

class PatientRecord : MedicalRecord { }
```

```csharp
// Отримуємо GetSummary через нащадка PatientRecord
MethodInfo m = typeof(PatientRecord).GetMethod("GetSummary");

Console.WriteLine(m.DeclaringType.Name);  // MedicalRecord — де оголошено
Console.WriteLine(m.ReflectedType.Name);  // PatientRecord  — через кого отримано
```

`DeclaringType` відповідає на питання «де це написано?», `ReflectedType` — «через який клас ми запитали?». При використанні `DeclaredOnly` обидва збігаються.

### Отримання всіх компонентів типу

Метод `GetMembers()` повертає всі доступні компоненти типу як об'єкт `MemberInfo`. Цей об'єкт дозволяє отримати інформацію про компонент типу. Зокрема, деякі його властивості:

- `DeclaringType`: повертає повну назву типу
- `MemberType`: повертає значення з переліку `MemberTypes`:
  - `MemberTypes.Constructor`
  - `MemberTypes.Method`
  - `MemberTypes.Field`
  - `MemberTypes.Event`
  - `MemberTypes.Property`
  - `MemberTypes.NestedType`
- `Name`: повертає назву компонента

Застосуємо метод `GetMembers` і виведемо всі доступні елементи типу:

```csharp
using System.Reflection; // Підключаємо функціонал рефлексії.

Type myType = typeof(Person);

foreach (MemberInfo member in myType.GetMembers())
{
    Console.WriteLine($"{member.DeclaringType} {member.MemberType} {member.Name}");
}

public class Person
{
    string name;
    public int Age { get; set; }
    public Person(string name, int age)
    {
        this.name = name;
        this.Age = age;
    }
    public void Print() => Console.WriteLine($"Name: {name} Age: {Age}");
}
```

В даному випадку ми отримаємо всі доступні члени класу `Person`.

```text
Person Method get_Age
Person Method set_Age
Person Method Print

System.Object Method GetType
System.Object Method ToString
System.Object Method Equals
System.Object Method GetHashCode
Person Constructor .ctor
Person Property Age
```

Зверніть увагу, що в даному випадку ми отримуємо тільки всі публічні компоненти класу, і нам не виводиться інформація про приватну змінну `name`.

З іншого боку, властивості виводяться методи доступу - геттер (тут `get_Age`) і сеттер (тут `set_Age`).

Третій момент, який слід зазначити, що за умовчанням ми отримуємо весь функціонал, у тому числі успадкований від базових класів (у цьому випадку функціонал базового класу `Object`).

### BindingFlags — бітова маска фільтрації

У прикладі вище використовувалася проста форма `GetMembers()` без аргументів. Вона повертає лише **публічні** члени типу, включаючи успадковані від базових класів. Щоб отримати непублічні, статичні або тільки власні члени, використовується перевантаження `GetMembers(BindingFlags)`.

`BindingFlags` — це перелік-прапорець (`[Flags] enum`), значення якого комбінуються через побітове АБО (`|`). Кожен прапорець вмикає або вимикає певну категорію членів. Важлива особливість: якщо не передати жодного прапорця, CLR застосовує внутрішній дефолт — еквівалент `Public | Instance | Static` з включеними успадкованими. Щойно ви передаєте хоча б один прапорець явно, CLR починає вимагати _всі_ потрібні категорії.

**Ключові прапорці:**

| Прапорець | Що вмикає |
|-----------|-----------|
| `Public` | публічні члени (`public`) |
| `NonPublic` | непублічні (`private`, `protected`, `internal`) |
| `Instance` | члени екземпляра (нестатичні) |
| `Static` | статичні члени (`static`) |
| `DeclaredOnly` | тільки члени _цього_ класу, успадковані виключаються |
| `FlattenHierarchy` | включити статичні члени базових класів (актуально при `Static`) |
| `IgnoreCase` | ігнорувати регістр у `GetMethod(name)` / `GetProperty(name)` |

Основна пастка: при явній передачі прапорців CLR не додає нічого автоматично. Якщо написати лише `NonPublic`, без `Instance` — результат буде порожнім, бо жоден член не задовольняє комбінацію «непублічний і не-екземпляр і не-статичний».

**Типові практичні комбінації:**

```csharp
// Усі публічні методи екземпляра (стандартний запит для DI)
BindingFlags.Public | BindingFlags.Instance

// Усі приватні поля об'єкта (для серіалізаторів, ORM)
BindingFlags.NonPublic | BindingFlags.Instance

// Тільки власні члени класу без успадкованих (для документації)
BindingFlags.DeclaredOnly | BindingFlags.Public | BindingFlags.Instance

// Абсолютно всі члени: public/private, instance/static
BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static

// Тільки публічні статичні (константи, factory-методи)
BindingFlags.Public | BindingFlags.Static
```

### BackingField — прихована ціна автовластивостей

Коли компілятор C# обробляє автоматично реалізовану властивість (`public string Name { get; set; }`), він **генерує** приватне поле зберігання за ім'ям `<Name>k__BackingField`. Це поле існує в IL-коді збірки і повністю видиме через рефлексію.

```csharp
public class PatientRecord
{
    public string FullName { get; set; }   // → <FullName>k__BackingField
    public DateTime BirthDate { get; set; } // → <BirthDate>k__BackingField
    private decimal _bmi;                  // → явне поле _bmi
}
```

При виклику `GetFields()` без `NonPublic` — backing-поля **не видно**, бо вони `private`. Але щойно додається `NonPublic | Instance`, вони з'являються поруч із явними приватними полями:

```text
Field  <FullName>k__BackingField
Field  <BirthDate>k__BackingField
Field  _bmi
```

На практиці це має значення для:
- **Серіалізаторів**, які обходять властивості і читають поля напряму — вони повинні відфільтровувати `k__BackingField` або знати, що він є.
- **ORM-маперів**, де треба розрізнити «бізнесове» поле від backing-поля.
- **Клонування об'єктів** через рефлексію — необхідно копіювати або поле, або властивість, але не обидва одночасно.

Для надійної фільтрації backing-полів перевіряють `field.Name.StartsWith("<")` та наявність атрибута `[CompilerGenerated]`:

```csharp
bool isBackingField = field.IsDefined(typeof(System.Runtime.CompilerServices.CompilerGeneratedAttribute), false);
```

### GetMember — отримання члена за ім'ям

Метод `GetMember(string name)` повертає `MemberInfo[]`, а не один об'єкт. Це свідоме рішення: у класі може бути _кілька_ членів з однаковим ім'ям — перевантажені методи:

```csharp
public class PatientRecord
{
    public void AddNote(string text) { }
    public void AddNote(string text, DateTime timestamp) { }
    public void AddNote(NoteDto dto) { }
}
```

```csharp
Type t = typeof(PatientRecord);
MemberInfo[] notes = t.GetMember("AddNote", BindingFlags.Instance | BindingFlags.Public);
Console.WriteLine(notes.Length); // 3 — три перевантаження
```

Якщо потрібен _конкретний_ перевантажений варіант, використовують `GetMethod(name, Type[])` з масивом типів параметрів:

```csharp
MethodInfo specific = t.GetMethod("AddNote", new[] { typeof(string), typeof(DateTime) });
```

---

## Приклад 1 — PatientRecord: порівняння GetMembers з різними BindingFlags

```csharp
using System;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;

Type t = typeof(PatientRecord);

Console.WriteLine("=== GetMembers() — публічні + успадковані ===");
foreach (var m in t.GetMembers())
    Console.WriteLine($"  [{m.MemberType,-11}] {m.Name,-30} (з {m.DeclaringType!.Name})");

Console.WriteLine();
Console.WriteLine("=== GetFields(NonPublic|Instance) — приватні поля + BackingField ===");
var allFields = t.GetFields(BindingFlags.NonPublic | BindingFlags.Instance);
foreach (var f in allFields)
{
    bool isBacking = f.IsDefined(typeof(CompilerGeneratedAttribute), false);
    string tag = isBacking ? " [backing]" : "";
    Console.WriteLine($"  {f.Name}{tag}  ({f.FieldType.Name})");
}

Console.WriteLine();
Console.WriteLine("=== DeclaredOnly — тільки власні члени ===");
var declared = t.GetMembers(BindingFlags.DeclaredOnly | BindingFlags.Public
                           | BindingFlags.NonPublic | BindingFlags.Instance);
foreach (var m in declared.OrderBy(m => m.MemberType.ToString()))
    Console.WriteLine($"  [{m.MemberType,-11}] {m.Name}");

public class MedicalRecord
{
    public int RecordId { get; set; }
    public virtual string GetSummary() => $"Record #{RecordId}";
}

public class PatientRecord : MedicalRecord
{
    public string FullName { get; set; } = "";
    public DateTime BirthDate { get; set; }
    private decimal _bmi;
    private string? _notes;

    public PatientRecord(string fullName, DateTime birthDate)
    {
        FullName = fullName;
        BirthDate = birthDate;
    }

    public void SetBmi(decimal bmi) => _bmi = bmi;
    public decimal GetBmi() => _bmi;

    public void AddNote(string text) => _notes = text;
    public void AddNote(string text, DateTime timestamp)
        => _notes = $"[{timestamp:d}] {text}";

    public override string GetSummary() =>
        $"Пацієнт: {FullName}, ІМТ: {_bmi:F1}";
}
```

Очікуваний вивід ілюструє три рівні видимості: публічні (включно з успадкованими від `MedicalRecord` та `Object`), приватні поля зі згенерованими backing-полями, і лише власні задекларовані члени `PatientRecord`.

---

## Приклад 2 — TypeExplorer: структурований звіт про тип

```csharp
using System;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text;

Console.WriteLine(TypeExplorer.Report(typeof(PatientRecord)));

public class PatientRecord
{
    public string FullName { get; set; } = "";
    public DateTime BirthDate { get; set; }
    public int RecordId { get; init; }
    private decimal _bmi;
    private readonly string _ward = "Cardiology";

    public PatientRecord() { }
    public PatientRecord(string fullName) => FullName = fullName;

    public void SetBmi(decimal v) => _bmi = v;
    public decimal GetBmi() => _bmi;
    public static PatientRecord CreateAnonymous() => new();
    public override string ToString() => $"Patient: {FullName}";
}

public static class TypeExplorer
{
    public static string Report(Type t)
    {
        var sb = new StringBuilder();
        var flags = BindingFlags.Public | BindingFlags.NonPublic
                  | BindingFlags.Instance | BindingFlags.Static
                  | BindingFlags.DeclaredOnly;

        sb.AppendLine($"╔══ Тип: {t.FullName} ══╗");
        sb.AppendLine($"  Base   : {t.BaseType?.Name ?? "—"}");
        sb.AppendLine($"  IsClass: {t.IsClass}  IsAbstract: {t.IsAbstract}");

        // Конструктори
        var ctors = t.GetConstructors(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
        sb.AppendLine($"\n  ── Конструктори ({ctors.Length}) ──");
        foreach (var c in ctors)
        {
            var ps = string.Join(", ", c.GetParameters().Select(p => $"{p.ParameterType.Name} {p.Name}"));
            sb.AppendLine($"    .ctor({ps})");
        }

        // Властивості
        var props = t.GetProperties(flags);
        sb.AppendLine($"\n  ── Властивості ({props.Length}) ──");
        foreach (var p in props)
        {
            string rw = (p.CanRead ? "get" : "") + (p.CanWrite ? ";set" : "");
            sb.AppendLine($"    {p.PropertyType.Name,-15} {p.Name,-20} [{rw}]");
        }

        // Поля (без backing)
        var fields = t.GetFields(flags);
        var realFields  = fields.Where(f => !f.IsDefined(typeof(CompilerGeneratedAttribute), false)).ToArray();
        var backings    = fields.Where(f =>  f.IsDefined(typeof(CompilerGeneratedAttribute), false)).ToArray();

        sb.AppendLine($"\n  ── Явні поля ({realFields.Length}) ──");
        foreach (var f in realFields)
        {
            string mod = f.IsStatic ? "static " : "";
            string ro  = f.IsInitOnly ? "readonly " : "";
            sb.AppendLine($"    {mod}{ro}{f.FieldType.Name,-15} {f.Name}");
        }

        sb.AppendLine($"\n  ── BackingFields ({backings.Length}) ──");
        foreach (var f in backings)
            sb.AppendLine($"    {f.Name}  ({f.FieldType.Name})");

        // Методи
        var methods = t.GetMethods(flags)
                       .Where(m => !m.IsSpecialName)  // прибираємо get_*/set_*
                       .ToArray();
        sb.AppendLine($"\n  ── Методи ({methods.Length}) ──");
        foreach (var m in methods)
        {
            string mod = m.IsStatic ? "static " : "";
            var ps = string.Join(", ", m.GetParameters().Select(p => p.ParameterType.Name));
            sb.AppendLine($"    {mod}{m.ReturnType.Name,-10} {m.Name}({ps})");
        }

        sb.AppendLine("╚══════════════════════╝");
        return sb.ToString();
    }
}
```

`TypeExplorer.Report` демонструє реальну практику: конструктори через окремий `GetConstructors`, властивості з `CanRead`/`CanWrite`, явні поля відокремлені від `k__BackingField` через атрибут `[CompilerGenerated]`, методи без `IsSpecialName` (щоб не показувати `get_FullName`). Такий підхід використовується в документаційних генераторах, Coverage-аналізаторах та ORM-інспекторах.
