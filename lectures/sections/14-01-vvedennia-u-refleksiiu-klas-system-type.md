---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
section: 1
number: "14.1"
title: "Введення у рефлексію. Клас System.Type"
source: "../_combined/84-vvedennia-u-refleksiiu-klas-system-type.md"
---

## 14.1. Введення у рефлексію. Клас System.Type

Рефлексія є процесом виявлення типів під час виконання програми. Кожна програма містить набір використовуваних класів, інтерфейсів, а також їх методів, властивостей та інших цеглинок, з яких складається програма. І рефлексія дозволяє визначити всі ці складові елементи застосунку — причому не статично під час написання коду, а **динамічно під час виконання**.

Щоб зрозуміти, чому рефлексія взагалі можлива, потрібно усвідомити ключову особливість .NET: компілятор зберігає у скомпільованій збірці (`.dll` або `.exe`) не лише виконуваний код, а й **метадані** — детальний опис усіх типів, їхніх членів, параметрів методів, атрибутів. Це так звані **метадані CLR** (Common Language Runtime). Саме цей опис і читає рефлексія, відповідаючи на запитання: «які поля є у цього класу?», «які методи він має?», «які інтерфейси реалізує?».

![Рефлексія: модель метаданих CLR та клас System.Type](_assets/14-01/reflection-type.png)

## Модель метаданих CLR

Збірка `.dll` або `.exe` — це не просто скомпільований байт-код. Вона має дворівневу структуру:

- **Метадані** — таблиці з описом усіх типів, методів, полів, властивостей, їх модифікаторів доступу, параметрів і атрибутів. CLR завантажує ці таблиці в пам'ять і надає до них доступ через `System.Reflection`.
- **IL-код** (Intermediate Language) — інструкції, що виконуються після JIT-компіляції. Метадані й IL зберігаються разом, тому рефлексія може не лише досліджувати тип, але й через `MethodInfo.Invoke` викликати його методи.

Ієрархія об'єктів рефлексії відображає структуру збірки:

```
Assembly (.dll)
  └── Module (зазвичай один на збірку)
        └── Type (клас, struct, інтерфейс, enum…)
              ├── MethodInfo[]      — методи
              ├── ConstructorInfo[] — конструктори
              ├── FieldInfo[]       — поля
              ├── PropertyInfo[]    — властивості
              └── EventInfo[]       — події
```

Усі класи `MethodInfo`, `FieldInfo`, `PropertyInfo`, `ConstructorInfo`, `EventInfo` є нащадками абстрактного класу `MemberInfo`, який визначає загальний функціонал: ім'я члена, тип, що його оголошує, і набір атрибутів.

## Де застосовується рефлексія

Рефлексія — це фундамент, на якому побудовані ключові інструменти сучасного .NET-розробника:

- **DI-контейнери** (Autofac, Microsoft.Extensions.DependencyInjection): сканують збірку на наявність типів, аналізують конструктори, визначають залежності і автоматично їх інжектують.
- **ORM** (Entity Framework Core): відображає властивості класу на колонки таблиці бази даних, генерує SQL-запити, читає і записує значення полів через рефлексію.
- **Серіалізація** (System.Text.Json, Newtonsoft.Json): перетворює об'єкт у JSON/XML, читаючи властивості типу через `GetProperties()`.
- **Тестові фреймворки** (NUnit, xUnit): знаходять усі методи з атрибутом `[Test]` або `[Fact]` і викликають їх через `MethodInfo.Invoke`.
- **Плагінна архітектура**: завантаження сторонніх збірок у рантаймі, пошук у них типів, що реалізують певний інтерфейс, і їх динамічне підключення.

Це пояснює, чому рефлексія є важливою темою, навіть якщо у власному коді ви рідко пишете `typeof(...)` або `GetMethods()` напряму: **інструменти, якими ви користуєтесь щодня, використовують рефлексію під капотом**.

## Важливе застереження: продуктивність

Рефлексія надає виняткову гнучкість, але **коштує продуктивністю**. Виклик методу через `MethodInfo.Invoke` у 10–100 разів повільніший за прямий виклик, оскільки кожного разу виконуються перевірки видимості, типів параметрів і розпакування `object`. Виклик `GetProperties()` теж не безкоштовний — він алокує масив `PropertyInfo[]`.

Практичне правило: рефлексія доречна в ініціалізаційному коді (один раз при старті застосунку), в інструментах і фреймворках — але не у гарячому шляху виконання (цикли, обробка запитів). У критично важливих сценаріях результати кешуються або замінюються `Expression<T>` / `source generators`.

## Простір імен System.Reflection

Основний функціонал рефлексії зосереджений у просторі імен `System.Reflection`. Ключові класи:

- `Assembly` — представляє збірку і дозволяє завантажувати, досліджувати її типи
- `AssemblyName` — зберігає ідентифікаційну інформацію збірки (ім'я, версію, культуру)
- `MemberInfo` — абстрактний базовий клас для всіх членів типу
- `EventInfo` — подія типу
- `FieldInfo` — поле типу (включно з приватними)
- `MethodInfo` — метод (включно з getters/setters властивостей)
- `PropertyInfo` — властивість
- `ConstructorInfo` — конструктор
- `ParameterInfo` — параметр методу або конструктора
- `Module` — модуль всередині збірки

Усі ці класи надають не лише інформацію про член, але й можливість діяти: `MethodInfo.Invoke` — викликати метод, `FieldInfo.SetValue` — змінити значення поля, `ConstructorInfo.Invoke` — створити екземпляр.

## Клас System.Type — центральний об'єкт рефлексії

Клас `System.Type` є точкою входу до всієї інформації про тип. Він інкапсулює повний опис класу, структури, інтерфейсу або переліку і надає методи для отримання всіх його складових.

Ключові властивості `Type`:

| Властивість | Повертає |
|-------------|----------|
| `Name` | Коротке ім'я: `"PatientRecord"` |
| `FullName` | Повне ім'я з namespace: `"Med.PatientRecord"` |
| `Namespace` | Простір імен |
| `Assembly` | Збірка, де визначено тип |
| `BaseType` | Базовий клас (`Type?`, `null` для `object`) |
| `IsClass` | `true` якщо клас (reference type) |
| `IsValueType` | `true` якщо struct або enum |
| `IsInterface` | `true` якщо інтерфейс |
| `IsAbstract` | `true` якщо abstract (або інтерфейс) |
| `IsSealed` | `true` якщо sealed |
| `IsGenericType` | `true` якщо `List<T>`, `Dictionary<K,V>` тощо |
| `IsArray` | `true` якщо масив |
| `IsEnum` | `true` якщо enum |
| `IsPublic` | `true` якщо публічний тип |

Методи `Type` для отримання членів:

| Метод | Повертає |
|-------|----------|
| `GetMembers()` | Всі публічні члени + успадковані |
| `GetMethods()` | Методи як `MethodInfo[]` |
| `GetConstructors()` | Конструктори як `ConstructorInfo[]` |
| `GetFields()` | Поля як `FieldInfo[]` |
| `GetProperties()` | Властивості як `PropertyInfo[]` |
| `GetEvents()` | Події як `EventInfo[]` |
| `GetInterfaces()` | Реалізовані інтерфейси як `Type[]` |
| `GetCustomAttributes()` | Атрибути типу |

Кожен метод також має перевантаження з `BindingFlags` для тонкого контролю — детальніше у розд. 14.2.

## Три способи отримати об'єкт Type

### Спосіб 1: `typeof(T)` — compile-time

Оператор `typeof` є найшвидшим і найбезпечнішим способом: тип `T` відомий на етапі компіляції, компілятор перевіряє коректність, ніяких рантайм-помилок:

```csharp
Type t = typeof(PatientRecord);
Console.WriteLine(t.Name);    // PatientRecord
Console.WriteLine(t.IsClass); // True
```

Якщо передати неіснуючий тип — отримаємо помилку компіляції, що значно краще за рантайм-виняток. Це рекомендований спосіб для більшості сценаріїв.

### Спосіб 2: `obj.GetType()` — runtime, є екземпляр

Метод `GetType()` успадкований від `object` і доступний для будь-якого об'єкта. Повертає **фактичний** тип об'єкта, а не тип змінної-посилання:

```csharp
PatientRecord p = new PatientRecord("P001", "Петренко", "I10.9");
Type t = p.GetType(); // PatientRecord

// Поліморфний приклад:
object obj = new PatientRecord("P001", "Петренко", "I10.9");
Console.WriteLine(obj.GetType().Name); // PatientRecord, НЕ object
```

Саме ця поліморфна поведінка робить `GetType()` незамінним у колекціях гетерогенних об'єктів.

### Спосіб 3: `Type.GetType(string)` — runtime, є рядок імені

Статичний метод `Type.GetType` дозволяє отримати тип за рядком з його повним іменем. Це єдиний спосіб, коли тип взагалі невідомий під час написання коду — наприклад, ім'я береться з конфігурації або бази даних:

```csharp
// Перший параметр — повне ім'я з namespace
// Другий — кидати TypeLoadException якщо не знайдено (false = повернути null)
// Третій — ігнорувати регістр
Type? t = Type.GetType("Med.PatientRecord", false, true);

if (t is not null)
    Console.WriteLine(t.FullName);
else
    Console.WriteLine("Тип не знайдено");
```

Якщо тип знаходиться в **іншій збірці**, після повного імені через кому вказується ім'я збірки:

```csharp
Type? t = Type.GetType("Med.PatientRecord, MedLibrary", false, true);
```

## Пошук реалізованих інтерфейсів

Метод `GetInterfaces()` повертає масив `Type[]` усіх інтерфейсів, що реалізує тип, — включно з успадкованими:

```csharp
Type myType = typeof(Person);

Console.WriteLine("Реалізовані інтерфейси:");
foreach (Type i in myType.GetInterfaces())
{
    Console.WriteLine(i.Name);
}

public class Person : IEater, IMovable
{
    public string Name { get; }
    public Person(string name) => Name = name;
    public void Eat() => Console.WriteLine($"{Name} eats");
    public void Move() => Console.WriteLine($"{Name} moves");
}

interface IEater  { void Eat(); }
interface IMovable { void Move(); }
```

Оскільки кожен інтерфейс представлений об'єктом `Type`, для нього також можна застосувати `GetMethods()`, `GetProperties()` тощо — отже, рефлексія однаково добре описує як конкретні класи, так і абстрактні інтерфейси.

## Дослідження типу PatientRecord — runnable приклад

```csharp run
using System;
using System.Reflection;

Type t = typeof(PatientRecord);

Console.WriteLine("=== Загальна інформація ===");
Console.WriteLine($"Name:        {t.Name}");
Console.WriteLine($"FullName:    {t.FullName}");
Console.WriteLine($"Namespace:   {t.Namespace ?? "(global)"}");
Console.WriteLine($"IsClass:     {t.IsClass}");
Console.WriteLine($"IsValueType: {t.IsValueType}");
Console.WriteLine($"IsAbstract:  {t.IsAbstract}");
Console.WriteLine($"BaseType:    {t.BaseType?.Name}");

Console.WriteLine("\n=== Реалізовані інтерфейси ===");
Type[] ifaces = t.GetInterfaces();
Console.WriteLine(ifaces.Length == 0 ? "  (немає)" : string.Join(", ", Array.ConvertAll(ifaces, i => i.Name)));

Console.WriteLine("\n=== 3 способи отримати Type ===");
// 1. typeof
Type t1 = typeof(PatientRecord);
Console.WriteLine($"typeof:     {t1.Name}");

// 2. GetType()
var p = new PatientRecord("P001", "Петренко", "I10.9", 67);
Type t2 = p.GetType();
Console.WriteLine($"GetType():  {t2.Name}");

// 3. Type.GetType з рядка
Type? t3 = Type.GetType("PatientRecord");
Console.WriteLine($"GetType(s): {(t3 != null ? t3.Name : "null (немає namespace)")}");

Console.WriteLine($"\nВсі три однакові: {t1 == t2}");

class PatientRecord
{
    public string  Id      { get; }
    public string  Name    { get; set; }
    public string  IcdCode { get; set; }
    public int     Age     { get; set; }
    private double _bmi;

    public PatientRecord(string id, string name, string icd, int age)
    {
        Id = id; Name = name; IcdCode = icd; Age = age;
    }

    public string GetSummary()    => $"{Name} ({Age} р.) — {IcdCode}";
    private bool  IsHighRisk()    => IcdCode.StartsWith("I") || IcdCode.StartsWith("C");
}
```

## Порівняння typeof і GetType() для поліморфних об'єктів — runnable приклад

```csharp run
using System;

MedicalRecord[] records = {
    new InpatientRecord("R001", 7),
    new OutpatientRecord("R002", "Кардіологія"),
    new InpatientRecord("R003", 3),
    new OutpatientRecord("R004", "Неврологія"),
};

Console.WriteLine("=== Поліморфне GetType() ===");
Console.WriteLine($"{"ID",-6} {"RecordType",-14} {"ActualType",-20} {"BaseType"}");
Console.WriteLine(new string('-', 58));

foreach (var rec in records)
{
    Type actual = rec.GetType();          // фактичний тип
    Type declared = typeof(MedicalRecord); // тип змінної — завжди MedicalRecord

    Console.WriteLine($"{rec.Id,-6} {rec.RecordType,-14} {actual.Name,-20} {actual.BaseType?.Name}");
}

Console.WriteLine("\n=== IsAssignableFrom — перевірка ієрархії ===");
Type baseType   = typeof(MedicalRecord);
Type inpatient  = typeof(InpatientRecord);
Type outpatient = typeof(OutpatientRecord);

Console.WriteLine($"MedicalRecord.IsAssignableFrom(InpatientRecord):  {baseType.IsAssignableFrom(inpatient)}");
Console.WriteLine($"MedicalRecord.IsAssignableFrom(OutpatientRecord): {baseType.IsAssignableFrom(outpatient)}");
Console.WriteLine($"InpatientRecord.IsAssignableFrom(MedicalRecord):  {inpatient.IsAssignableFrom(baseType)}");

Console.WriteLine("\n=== Підрахунок за типами ===");
int inCount  = 0; int outCount = 0;
foreach (var rec in records)
{
    if (rec.GetType() == typeof(InpatientRecord))  inCount++;
    if (rec.GetType() == typeof(OutpatientRecord)) outCount++;
}
Console.WriteLine($"Стаціонарних: {inCount}, Амбулаторних: {outCount}");

class MedicalRecord
{
    public string Id { get; }
    public MedicalRecord(string id) => Id = id;
    public virtual string RecordType => "Base";
}

class InpatientRecord : MedicalRecord
{
    public int StayDays { get; }
    public InpatientRecord(string id, int days) : base(id) => StayDays = days;
    public override string RecordType => "Inpatient";
}

class OutpatientRecord : MedicalRecord
{
    public string Clinic { get; }
    public OutpatientRecord(string id, string clinic) : base(id) => Clinic = clinic;
    public override string RecordType => "Outpatient";
}
```

### Отримання типу

Щоб керувати типом та отримувати всю інформацію про нього, нам треба спершу отримати цей тип. Це можна зробити трьома способами: за допомогою оператора `typeof`, за допомогою методу `GetType()` класу `Object` і застосовуючи статичний метод `Type.GetType()`.

Отримання типу через `typeof`:

```csharp
Type myType = typeof(Person);

Console.WriteLine(myType); // Person

public class Person
{
    public string Name { get; }
    public Person(string name) => Name = name;
}
```

Тут визначено клас `Person` із деякою функціональністю. І щоб отримати його тип, використовується вираз `Type myType = typeof(Person);`.

Отримання типу за допомогою методу `GetType`, успадкованого від класу `Object`:

```csharp
Person tom = new Person("Tom");
Type myType = tom.GetType();
```

На відміну від попереднього прикладу, тут, щоб отримати тип, треба створювати об'єкт класу.

І третій спосіб отримання типу - статичний метод `Type.GetType()`:

```csharp
Type? myType = Type.GetType("Person", false, true);
```

Перший параметр вказує на повне ім'я класу із простором імен. Другий параметр вказує, чи генеруватиметься виняток, якщо клас не вдасться знайти. У цьому випадку значення `false` означає, що виняток не генеруватиметься. І третій параметр вказує, чи потрібно враховувати регістр символів у першому параметрі. Значення `true` означає, що регістр ігнорується. Оскільки зазначений тип може бути відсутнім, то метод повертає об'єкт nullable-типу.

У цьому випадку клас основної програми та клас `Person` знаходяться у глобальному просторі імен. Однак якщо тип розташовується в іншому просторі імен, його також треба вказати:

```csharp
Type? myType = Type.GetType("PeopleTypes.Person", false, true);

Console.WriteLine(myType); // PeopleTypes.Person

namespace PeopleTypes
{
    public class Person
    {
        public string Name { get; }
        public Person(string name) => Name = name;
    }
}
```

Як альтернативу можна застосовувати оператор `typeof`, передаючи в нього ім'я типу із зазначенням простору імен:

```csharp
Type myType = typeof(PeopleTypes.Person);
```

Якщо потрібний нам тип знаходиться в іншій збірці dll, то після повного імені класу через кому вказується ім'я збірки:

```csharp
Type myType = Type.GetType("PeopleTypes.Person, MyLibrary", false, true);
```

Тепер досліджуємо тип та отримаємо деяку інформацію про нього.

```csharp
Type myType = typeof(PeopleTypes.Person);

Console.WriteLine($"Name: {myType.Name}");
// Отримуємо коротке ім'я типу.
Console.WriteLine($"Full Name: {myType.FullName}");
// Отримуємо повне ім'я типу.
Console.WriteLine($"Namespace: {myType.Namespace}");
// Отримуємо простір імен типу.
Console.WriteLine($"Is struct: {myType.IsValueType}");
// Чи є тип структурою.
Console.WriteLine($"Is class: {myType.IsClass}");
// Чи є тип класом.

namespace PeopleTypes
{
    class Person
    {
        public string Name { get; }
        public Person(string name) => Name = name;
    }
}
```

Консольний вивід:

```text
Name: Person
Full Name: PeopleTypes.Person
Namespace: PeopleTypes
Is struct: False
Is class: True
```

### Пошук реалізованих інтерфейсів

Щоб отримати всі реалізовані типом інтерфейси, треба використовувати метод `GetInterfaces()`, який повертає масив об'єктів `Type`:

```csharp
Type myType = typeof(Person);

Console.WriteLine("Реалізовані інтерфейси:");
foreach (Type i in myType.GetInterfaces())
{
    Console.WriteLine(i.Name);
}

public class Person : IEater, IMovable
{
    public string Name { get; }
    public Person(string name) => Name = name;
    public void Eat() => Console.WriteLine($"{Name} eats");

    public void Move() => Console.WriteLine($"{Name} moves");
}

interface IEater
{
    void Eat();
}

interface IMovable
{
    void Move();
}
```

Так як кожен інтерфейс представляє об'єкт `Type`, то для кожного отриманого інтерфейсу можна також застосувати вище розглянуті методи для отримання інформації про властивості та методи.

Але поки що всі приклади вище ніяк не використовували рефлексію. У наступних темах розглянемо, як можна за допомогою рефлексії отримувати компоненти типу та звертатися до них, наприклад, змінювати значення приватних полів класу.
