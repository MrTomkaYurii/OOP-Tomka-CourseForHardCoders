# Карта концепцій: що вводиться в кожній лабі

## Головне правило

Код в `src/` повинен **використовувати тільки конструкції з лаб ≤ поточної**.
Кожна лаба вводить нове. Якщо конструкція ще не введена — вона заборонена в еталонному коді.

---

## Таблиця: коли що вперше з'являється

| Конструкція / тип | Лаба | Примітка |
|-------------------|------|---------|
| `int`, `double`, `string`, `bool`, `decimal` | 01 | базові типи |
| `if / else if / else`, `switch expression` | 01 | |
| `for`, `foreach`, `while` | 01 | |
| `static` методи, параметри, повернення | 01 | |
| `Console.ReadLine()`, `Console.WriteLine()` | 01 | |
| `T[]` одновимірний масив | 02 | |
| `T[,]` прямокутний 2D масив | 02 | |
| `T[][]` рваний масив (jagged) | 02 | |
| `T[,,]` тривимірний масив | 02 | |
| `string.Join`, `string.Split` | 02 | |
| `class`, поля, `get; set;` авто-властивості | 03 | |
| Обчислювані властивості (`get` only) | 03 | |
| Конструктори, `:this()` ланцюжок | 03 | |
| Методи екземпляра (instance methods) | 03 | |
| `override ToString()` | 03 | |
| `static` поле (`_nextId`) | 03 | |
| `null`, `if (x == null)` | 03 | |
| Масив об'єктів `Patient[]` + ручний лічильник | 03 | замість List<T> |
| `const` поле | 03 | для MaxCapacity |
| `enum` | 04 | BloodType, Speciality, AppointmentStatus |
| `struct` | 04 | WorkSchedule (value type) |
| `static class` | 04 | ClinicFormatter — тільки static методи |
| Індексатор `this[int index]` | 04 | PatientManager, DoctorManager, AppointmentManager |
| Перевантаження методів (overloading) | 04 | FindBySpeciality(string) / (Speciality) |
| `out` параметр, TryXxx патерн | 04 | TryFindById(int, out T) |
| `?.` null-conditional, `??` null-coalescing | 04 | тепер дозволено |
| Явне приведення `(TypeName)value` | 04 | int → enum у меню |
| Підпростори імен (`ClinicApp.Models` тощо) + `using` директиви | 05 | організація файлів |
| `private` backing fields `_camelCase` | 05 | |
| Явні сеттери з валідацією | 05 | |
| `throw new ArgumentException(msg)` | 05 | |
| `throw new ArgumentOutOfRangeException(paramName, msg)` | 05 | |
| `string.IsNullOrWhiteSpace(value)` | 05 | |
| `nameof(Symbol)` | 05 | |
| `try / catch` (порядок блоків) | 05 | |
| `Regex.IsMatch()`, `static readonly Regex` | 05 | опційно |
| `abstract class`, `abstract` методи | 06 | |
| `virtual` методи | 06 | |
| `protected` конструктор | 06 | |
| `: BaseClass`, `base()` | 06 | успадкування |
| `override` переваги методів | 06 | |
| `is`, `as`, явне приведення | 06 | |
| `interface` | 07 | IPayable, ICancellable, ISchedulable |
| Кілька інтерфейсів на одному класі | 07 | |
| Поліморфізм (base ref → child type) | 08 | |
| `new` (приховування методу) | 08 | |
| `sealed` | 08 | |
| `List<T>` (Add, RemoveAt, Count, [], ToArray) | 09 | Generics лаба |
| Generic клас `class Foo<T>`, `where T : Interface` | 09 | |
| `Queue<T>`, `Stack<T>` | 09 | |
| `InvalidOperationException` | 09 | порожня черга |
| `default!` keyword | 09 | generic методи |
| `IComparable<T>`, `int CompareTo(T? other)` | 10 | |
| `IComparer<T>`, `int Compare(T? x, T? y)` | 10 | |
| `IEnumerable<T>` як тип повернення, `yield return` | 10 | ліниве обчислення |
| `Attribute` (кастомний), `Reflection` | 11 | |
| `File`, `StreamWriter`, `StreamReader`, `Path`, `Directory` | 12 | |
| `delegate`, `event`, `EventArgs`, `+=` | 13 | |
| LINQ (`.Where`, `.Select`, `.OrderBy`, `.GroupBy`, `.Join`, | 14 | |
|   `.FirstOrDefault`, `.Any`, `.Sum`, `.Average`, `.Min`, `.Max`, | | |
|   `.Count(predicate)`, `.ToList()`, `.ToArray()`) | | |
| `Func<T, TResult>`, `Action<T>` — lambda як змінна/поле | 15 | |
| Closure (замикання) — захоплення зовнішньої змінної | 15 | |
| `public static class` + `this T` — метод розширення | 15 | |
| Fluent interface — `return this` для ланцюга | 15 | |
| `Stream`, `StreamReader/Writer`, `File`, `Directory` | 16 | |
| `System.Text.Json` (серіалізація) | 15 | |
| NuGet-пакет: `dotnet add package`, `<PackageReference>` | 16 | |
| `using Spectre.Console;` — зовнішня бібліотека | 16 | |
| `AnsiConsole.MarkupLine("[color]...[/]")`, `Markup.Escape()` | 16 | |
| `new Rule(...)`, `new Table()`, `new Panel()`, `new Tree()` | 16 | |
| `new SelectionPrompt<string>()`, `new TextPrompt<T>()` | 16 | |
| `new BarChart()`, `AnsiConsole.Status()` (spinner) | 16 | |
| Фасад-патерн над бібліотекою: `ClinicRenderer` | 16 | |
| `DbContext`, `DbSet<T>`, `OnConfiguring`, `OnModelCreating` | 17 | EF Core ядро |
| `UseSqlServer(connectionString)` — LocalDB провайдер | 17 | |
| Fluent API: `HasKey`, `Property`, `HasMaxLength`, `IsRequired` | 17 | |
| `ValueGeneratedOnAdd()` — IDENTITY стовпець | 17 | |
| `HasConversion<string>()` — enum → рядок у БД | 17 | |
| `ValueConverter<TModel, TProvider>` — конвертер для struct | 17 | WorkSchedule → "8-17" |
| `HasIndex().IsUnique()` — унікальний індекс | 17 | |
| `dotnet ef migrations add`, `dotnet ef database update` | 17 | CLI міграцій |
| `context.SaveChanges()` — транзакція всіх змін | 17 | |
| `context.Set.Any()` — `SELECT TOP 1` без завантаження | 17 | |
| `Id { get; private set; }` — EF Core сумісність | 17 | патерн для Value Object |
| EF: One-to-Many, Many-to-Many, Navigation Properties | 18 | |
| EF: `.Include()`, зовнішні ключі, `.ThenInclude()` | 18 | |
| EF: TPH (Table Per Hierarchy) — ієрархія в одній таблиці | 19 | |
| EF: Owned Entity — вбудовані value objects | 19 | |
| EF: `IQueryable<T>` vs `IEnumerable<T>` | 20 | |
| EF: `.Skip().Take()` — пагінація | 20 | |
| EF: `.AsNoTracking()` — оптимізація для читання | 20 | |
| EF: проєкції `Select(new { ... })` — DTO без завантаження всіх полів | 20 | |
| DI контейнер, SOLID принципи | 21 | |

---

## Детально по лабах

### Lab 01 — Introduction (sandbox/intro, не зливається)

**Нові конструкції:**
- Типи: `int`, `double`, `string`, `bool`, `decimal`, `DateTime`
- Умови: `if / else if / else`, `switch expression` з `_` default
- Цикли: `for`, `foreach`, `while`
- Методи: `static`, параметри, повернення значень
- Форматування: `{val:F2}`, `{val:D2}`, `:D2`
- Консоль: `Console.ReadLine()`, `int.Parse()`, `double.Parse()`, `DateTime.Parse()`
- Оператори: `%` (остача), тернарний `?:`

**Заборонено (ще не введено):**
- Масиви, класи, колекції будь-які

---

### Lab 02 — Arrays (sandbox/arrays, не зливається)

**Нові конструкції:**
- `T[]` — одновимірний масив: оголошення, заповнення, перебір
- `T[,]` — прямокутний 2D
- `T[][]` — jagged (рваний)
- `T[,,]` — тривимірний
- `string.Join(" ", arr)`, `string.Split(' ')`
- `.Length` масиву
- Bubble sort (вкладені `for`)
- Паралельні масиви (синхронна заміна)

**Заборонено:**
- Класи, колекції (`List<T>`, `Dictionary` тощо)

---

### Lab 03 — Defining Classes (feature/catalog → зливається в main)

**Нові конструкції:**
- `class`, поля (`public`, `private`, `private static`)
- Авто-властивості: `public string Name { get; set; }`
- Обчислювані властивості: `public int Age => ...;` (лише `get`)
- Конструктори: без параметрів, з параметрами, ланцюжок `: this(...)`
- Методи екземпляра: `public string GetCategory() { ... }`
- `override ToString()`
- Ключове слово `new` для створення об'єктів
- `static` поле для авто-лічильника ID
- `null`, `if (x == null)`, `if (x != null)`
- `const` поле в класі
- Масив об'єктів: `Patient[] _patients = new Patient[100]` + `int _count`
- `T[]` як тимчасовий результат (two-pass search pattern)
- Рядкові методи: `.ToLower()`, `.Contains()`

**Колекції в Lab 03:**
- Основні: `T[]` з ручним лічильником (те що знають з Lab 02)
- Task 8 — дослідження: `List<T>` як бонус (не в основному коді)

**Заборонено:**
- `List<T>` в основному коді (тільки Task 8 дослідження)
- Будь-який LINQ (`.Where`, `.FirstOrDefault`, `.Average`, `.MinBy`, `.OrderBy` тощо)
- `Dictionary<K,V>` в основному коді
- `TimeOnly`, `DateOnly` (занадто специфічні)
- Nullable оператори `?.` та `??`
- `IEnumerable<T>` як тип параметра
- `is not null` pattern matching (використовувати `!= null`)
- `abstract`, `interface`, `enum`, `struct`, `static class`

---

### Lab 04 — Члени класу (feature/class-members → злито в main)

**Нові конструкції:**
- `enum` — BloodType, Speciality, AppointmentStatus; заміняє рядки-константи
- `struct` — WorkSchedule: value type, поля тільки `{ get; }`, конструктор
- `static class` — ClinicFormatter: клас без інстанцій, тільки `public static` методи
- Індексатор `this[int index]` — Manager-класи поводяться як масиви
- Перевантаження методів — одне ім'я, різні сигнатури (`FindBySpeciality(string)` / `(Speciality)`)
- `out` параметр — `bool TryFindById(int id, out Patient patient)` (TryXxx патерн)
- `?.` null-conditional та `??` null-coalescing — тепер дозволено
- Явне приведення `(TypeName)value` — int → enum для вводу з консолі

**Заборонено (ще не введено):**
- `List<T>`, `Dictionary<K,V>` (Lab 09 — Generics)
- `abstract class`, `virtual`, `override` (Lab 06 — Inheritance)
- `interface` (Lab 07)
- `try / catch`, `throw` (Lab 05)

---

### Lab 05 — Encapsulation (feature/encapsulation → злито в main)

**Нові конструкції:**
- Sub-namespaces: `ClinicApp.Models`, `ClinicApp.Enums`, `ClinicApp.Managers`, `ClinicApp.Utils`
- `using` директиви між підпросторами (залежності між підпапками)
- `private` backing fields: `private string _firstName = "";`
- Явні сеттери: `set { /* validate */ _firstName = value; }`
- `throw new ArgumentException(message)`
- `throw new ArgumentOutOfRangeException(paramName, message)`
- `string.IsNullOrWhiteSpace(value)` — перевірка порожнього/whitespace рядка
- `nameof(Property)` — ім'я символу як рядок (безпечно при рефакторингу)
- `try / catch` з правильним порядком: конкретніший тип (підклас) — першим
- `static class ClinicValidator` — правила валідації в одному місці (патерн)
- Опційно: `System.Text.RegularExpressions.Regex.IsMatch()`, `static readonly Regex`

**Заборонено (ще не введено):**
- `: BaseClass`, `base()`, `override`, `virtual`, `abstract` (Lab 06)
- `interface` (Lab 07)

---

### Lab 06 — Inheritance (feature/inheritance → злито в main)

**Нові конструкції:**
- `abstract class MedicalRecord` — базовий клас ієрархії медичних записів
- `abstract string GetSummary()` — підклас зобов'язаний реалізувати
- `virtual string GetRecordType()`, `virtual bool IsActive()` — підклас може перевизначити
- `: BaseClass`, `protected` конструктор, `base(...)` виклик
- `override` в підкласах (`Diagnosis`, `LabResult`, `Prescription`)
- `is` (перевірка типу), `is T variable` (pattern variable)
- `as` (безпечне приведення, повертає null)
- Явне приведення `(T)obj` — і коли воно кидає `InvalidCastException`
- Поліморфний масив `MedicalRecord[]` — різні підкласи в одному масиві

**Заборонено (ще не введено):**
- `interface` (Lab 07)
- `new` keyword (method hiding) (Lab 08)
- `sealed` (Lab 08)

---

### Lab 07 — Interfaces (feature/interfaces → зливається)

**Нові конструкції:**
- `interface IPayable { decimal GetCost(); bool IsPaid; void MarkPaid(); }`
- `interface ICancellable { bool Cancel(string reason = ""); bool IsCancelled; string CancellationReason; }`
- `interface ISchedulable { bool CanSchedule(DateTime); }`
- Реалізація кількох інтерфейсів: `class Appointment : IPayable, ICancellable`
- Метод що приймає інтерфейс як параметр: `void Process(IPayable[] items)`
- `is IPayable p` — перевірка реалізації інтерфейсу

**Що з'явиться в меню:** 5. Рахунки — борги пацієнта, оплата запису, загальна сума

**Заборонено (ще не введено):**
- `new` keyword (method hiding) (Lab 08)
- `sealed` (Lab 08)

---

### Lab 08 — Polymorphism (feature/polymorphism → злито в main)

**Нові конструкції:**
- Підкласи `Appointment`: `RegularAppointment`, `UrgentAppointment`, `SpecialistAppointment`
- `new` keyword — метод-приховування (відмінне від `override`)
- `sealed class` і `sealed override`
- Різна логіка `GetCost()` в кожному підкласі через `override`

---

### Lab 09 — Generics (feature/generics → злито в main)

**Нові конструкції:**
- `List<T>` — динамічний масив: `.Add()`, `.RemoveAt()`, `.Count`, `.ToArray()`, `[i]`
- Generic клас `public class WaitingQueue<T>` — параметр `T` без обмеження
- `Queue<T>` зі стандартної бібліотеки — `Enqueue`, `Dequeue`, `Peek`, `Count`
- Generic constraint `where T : IIdentifiable` — доступ до `item.Id` всередині generic класу
- `default!` — значення за замовчуванням для `T` (null для reference types)
- `InvalidOperationException` — кидається при операції на порожній черзі

**Що дозволяється вперше:**
- `List<T>` в основному коді (раніше — тільки Task 8 дослідження Lab 03)
- `Queue<T>` і `Stack<T>` (раніше заборонені)
- `Dictionary<K,V>` (офіційно дозволяється з Lab 09)

---

### Lab 10 — Iterators & Comparators (feature/iterators → злито в main)

**Нові конструкції:**
- `IComparable<T>` — `int CompareTo(T? other)`; реалізується в самому класі; `Array.Sort()` / `List.Sort()` без аргументу
- `IComparer<T>` — `int Compare(T? x, T? y)`; окремий клас-компаратор; `List.Sort(new MyComparer())`
- `IEnumerable<T>` як тип повернення методу
- `yield return` — ліниве обчислення (state machine), відновлення стану між ітераціями
- `foreach` по `IEnumerable<T>` для споживання ітератора

**Що дозволяється вперше:**
- `IEnumerable<T>` як тип повернення (раніше заборонено до Lab 10)
- `string.Compare(x, y, StringComparison.CurrentCulture)` — культурно-залежне порівняння рядків

---

### Lab 11 — Reflection & Attributes (feature/reflection → злито в main)

**Нові конструкції:**
- `[AttributeUsage(AttributeTargets.Property)] sealed class XxxAttribute : Attribute` — власний атрибут з нуля
- `typeof(T)` — статичний тип, відомий на час компіляції
- `obj.GetType()` — динамічний тип під час виконання
- `Type.GetProperties()` → `PropertyInfo[]`
- `prop.GetValue(obj)` — зчитати значення властивості через рефлексію
- `prop.SetValue(obj, value)` — записати значення через рефлексію
- `prop.GetCustomAttribute<T>()` — зчитати атрибут конкретного типу
- `prop.GetCustomAttributes()` — усі атрибути на властивості
- `where T : new()` — constraint: тип T повинен мати публічний конструктор без параметрів
- `Convert.ChangeType(value, targetType)` — конверсія значення до типу відомого тільки в рантаймі

**Нові файли:**
- `src/Attributes/RequiredAttribute.cs` — `[Required]`
- `src/Attributes/MaxLengthAttribute.cs` — `[MaxLength(n)]`
- `src/Attributes/MinValueAttribute.cs` — `[MinValue(n)]`
- `src/Enums/TreatmentStatus.cs` — `Planned / Active / Completed / Cancelled`
- `src/Models/TreatmentPlan.cs` — нова сутність з атрибутами
- `src/Utils/ValidationResult.cs` — контейнер помилок
- `src/Utils/ModelValidator.cs` — `static Validate(object)`, `PrintInfo(Type)`
- `src/Utils/FormBuilder.cs` — `static Build<T>() where T : new()`
- `src/Managers/TreatmentPlanManager.cs` — CRUD + валідація
- `src/Clinic.cs` оновлено — `public TreatmentPlanManager TreatmentPlans { get; }`
- `src/Program.cs` оновлено — пункт меню **9. Плани лікування**

**Що з'явиться в меню:** 9. Плани лікування — додавання через FormBuilder, зміна статусу, PrintInfo

**Заборонено (ще не введено):**
- `delegate`, `event` (Lab 12)
- LINQ (Lab 13)

---

### Lab 12 — File I/O (feature/files → злито в main)

**Нові конструкції:**
- `File.AppendAllText(path, text, Encoding.UTF8)` — дописати в кінець файлу
- `File.ReadAllLines(path, Encoding.UTF8)` → `string[]`
- `File.WriteAllText`, `File.Exists`, `File.Delete`
- `StreamWriter(path, append: false, Encoding.UTF8)` + `using` — потік із гарантованим закриттям (`IDisposable`)
- `Directory.CreateDirectory(path)` — рекурсивне створення, safe якщо існує
- `Path.Combine(part1, part2, ...)` — платформо-незалежні шляхи
- `Encoding.UTF8` — `using System.Text;`
- `Environment.NewLine` — правильний перенос рядка під поточну ОС
- `try/catch` per-iteration у CSV: помилка в рядку не зупиняє цикл
- Секційний формат файлу `[SECTION]` — розпізнавання секцій при читанні

---

### Lab 13 — Events & Delegates (feature/events → злито в main)

**Нові конструкції:**
- `class XxxEventArgs : EventArgs` — власні аргументи події з readonly властивостями
- `event EventHandler<T>?` — поле-подія в класі (заборонено `=` ззовні, тільки `+=`/`-=`)
- `?.Invoke(this, args)` — безпечне підняття: не падає якщо підписників нема
- `+=` / `-=` — підписка і відписка
- Обробник: `void Handler(object? sender, TEventArgs e)` — обов'язкова сигнатура
- Множинні підписники — всі спрацьовують при одному `Invoke`
- `event` vs поле `EventHandler<T>?` — різниця в доступі ззовні

**Нові файли:**
- `src/Events/AppointmentEventArgs.cs`, `PatientEventArgs.cs`, `PaymentEventArgs.cs`, `TreatmentPlanEventArgs.cs`
- `src/Utils/PatientPassportWriter.cs` — генерує `patients/passport_{id}.txt`
- `src/Utils/SessionEventTracker.cs` — лічильники + WaitingRoom реакція + `session_summary.txt`

**Що з'являється:** автоматичне логування, паспорти пацієнтів, алерти `alerts/`, підсумок сесії

**Заборонено (ще не введено):**
- LINQ (Lab 14)

---

### Lab 14 — LINQ (feature/linq → злито в main) ✅

**Нові конструкції:**
- `.Where(predicate)`, `.Select(selector)`, `.ToList()`, `.ToArray()`
- `.OrderBy(key)`, `.OrderByDescending(key)`, `.ThenBy(key)`
- `.GroupBy(key)`, `.Join(...)`, `.FirstOrDefault()`
- `.Any(pred)`, `.Count(pred)`, `.Sum()`, `.Max()`
- `.Take(n)`, `.Distinct()`
- Анонімний тип у `GroupBy`: `new { a.Year, a.Month }`
- Value tuple як тип повернення: `(int Year, int Month, decimal Total)`

**Що змінилось:** `AnalyticsManager` — рефакторинг з `yield return` + `for` → LINQ-ланцюги.  
**Що додалось:** `SpecialityReport` (DTO), `ReportManager` (7 звітів), пункт меню 11.

---

### Lab 15 — Functional C# (feature/functional → злито в main) ✅

**Нові концепції:**
- `Func<T, TResult>` — лямбда що повертає значення; зберігається як поле/змінна
- `Action<T>` — лямбда без повернення; зберігається у `List<Action<T>>`
- Замикання (closure) — лямбда захоплює змінну зовнішнього контексту
- `var prev = field` — фіксація стану поля для безпечного замикання
- `public static class` + `this T source` — метод розширення
- Fluent interface — метод повертає `this` для ланцюга
- Higher-order методи — `Func<>` та `Action<>` як параметри одного методу

**Нові файли:** `Extensions/` (3 файли), `AppointmentFilter`, `AppointmentProcessor`, `AppointmentPipeline`

---

### Lab 16 — Console UI — Spectre.Console (feature/console-ui → злито в main) ✅

**Нові концепції:**
- NuGet-пакет: `dotnet add package`, `<PackageReference>` у `.csproj`
- `using Spectre.Console;` — підключення зовнішньої бібліотеки
- `AnsiConsole.MarkupLine("[color]...[/]")` — ANSI-розмітка
- `Markup.Escape(text)` — захист від markup injection
- `new Rule(...)` — горизонтальний роздільник із заголовком
- `new Table().Border(...).AddColumn(...).AddRow(...)` — таблиця з рамкою
- `new TableColumn(...).Centered()/.RightAligned()` — вирівнювання колонок
- `new SelectionPrompt<string>().Title(...).AddChoices(...)` — меню зі стрілками
- `new TextPrompt<T>().ValidationErrorMessage(...)` — типізоване введення з авто-валідацією
- `new ConfirmationPrompt(...)` — запит yes/no
- `new Panel(content) { Header, Border, Padding }` — рамка навколо контенту
- `new Tree(root).AddNode(branch).AddNode(leaf)` — ієрархічне відображення
- `new BarChart().AddItem(label, value, color)` — стовпчаста діаграма
- `AnsiConsole.Status().Spinner(Known.Dots).Start(msg, ctx => {...})` — спіннер
- Фасад-патерн: `ClinicRenderer` ховає Spectre.Console від `Program.cs`
- SRP: `Program.cs` вирішує "що показати"; `ClinicRenderer` вирішує "як"

**Нова папка:** `src/UI/ClinicRenderer.cs`
**Зміни:** `Program.cs` повністю переписано на `ClinicRenderer.*`

---

## Заборонені практики (загальні)

| Практика | Чому заборонена |
|----------|----------------|
| LINQ в Labs 01–12 | Не введений до Lab 13 |
| `List<T>` в Labs 01–08 основному коді | Не введений до Lab 09 (Generics) |
| `TimeOnly`, `DateOnly` в Labs 01–05 | Надто специфічні типи, вводяться при потребі |
| `?.` і `??` в Labs 01–03 | Не введені до Lab 04 |
| `Dictionary<K,V>` в Labs 01–08 | Офіційно в Lab 09+ |
| `IEnumerable<T>` як тип параметра в Labs 01–09 | Не введений до Lab 10 |
