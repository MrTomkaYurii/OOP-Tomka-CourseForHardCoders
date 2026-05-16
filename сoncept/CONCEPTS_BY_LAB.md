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
| EF: Navigation Properties — `ICollection<T>` (колекція) і `T?` (посилання) | 18 | |
| EF: Eager Loading `.Include(lambda)` → SQL JOIN (вирішення N+1) | 18 | |
| EF: `HasOne/WithMany/HasForeignKey/OnDelete` — One-to-Many Fluent API | 18 | |
| EF: `DeleteBehavior.Cascade` vs `.Restrict` — і чому не два Cascade | 18 | |
| EF: `HasDiscriminator<string>().HasValue<T>()` — TPH дискримінатор | 18 | |
| EF: Repository pattern — `ClinicRepository` з `.Include()` запитами | 18 | |
| EF: TPH для abstract класу — nullable стовпці підтипів | 19 | MedicalRecord ієрархія |
| EF: `OwnsOne(p => p.Contact, ec => {...})` — Owned Entity | 19 | EmergencyContact |
| EF: `IsRowVersion()` — Optimistic Concurrency Token | 19 | |
| EF: `DbUpdateConcurrencyException` — конкурентне редагування | 19 | |
| `record` — immutable тип, автогенеровані Equals/ToString | 20 | DTO патерн |
| EF: `IQueryable<T>` — відкладене виконання, Expression Tree | 20 | |
| EF: `.ToList()` в середині chain → LINQ to Objects (антипатерн) | 20 | |
| EF: `.Skip(n).Take(m)` → SQL OFFSET/FETCH NEXT (пагінація) | 20 | |
| EF: `Select(p => new DTO(...))` — проєкція конкретних стовпців | 20 | |
| EF: `HasQueryFilter(expr)` — Global Query Filter (автоматичний WHERE) | 20 | |
| EF: `.IgnoreQueryFilters()` — скасування глобального фільтра | 20 | |
| Soft Delete патерн: `IsDeleted` bool + `SoftDelete()` метод | 20 | |
| `async Task`, `async Task<T>` — правильні типи async методів | 21 | |
| `async void` — заборонений патерн (тільки event handlers) | 21 | |
| `await` — звільнення потоку під час очікування I/O | 21 | |
| `CancellationToken`, `CancellationTokenSource` — скасування | 21 | |
| `CancellationTokenSource(TimeSpan)` — автоматичний таймаут | 21 | |
| `ct.ThrowIfCancellationRequested()` — явна перевірка токену | 21 | |
| `Task.WhenAll(t1, t2, ...)` — паралельне виконання, чекати всіх | 21 | |
| `Task.WhenAny(t1, t2)` — race, перемагає перший завершений | 21 | |
| `Parallel.ForEachAsync(col, options, async (item,ct) => {})` | 21 | .NET 6+ |
| `ParallelOptions { MaxDegreeOfParallelism, CancellationToken }` | 21 | |
| `Interlocked.Increment(ref count)` — атомарний thread-safe інкремент | 21 | |
| `AggregateException`, `.InnerExceptions` — помилки паралельних задач | 21 | |
| `ContinueWith(t => ..., TaskContinuationOptions.OnlyOnFaulted)` | 21 | |
| `task.IsCompletedSuccessfully`, `task.IsFaulted`, `task.IsCanceled` | 21 | |
| `IProgress<T>`, `Progress<T>` — звітування про прогрес | 21 | |
| `progress?.Report(value)` — null-safe виклик прогресу | 21 | |
| `ConfigureAwait(false)` — у бібліотечному/DAL-коді | 21 | |
| `HttpClient` (singleton), `BaseAddress`, `Timeout` | 21 | |
| `GetFromJsonAsync<T>(url, ct)` — GET + JSON десеріалізація | 21 | System.Net.Http.Json |
| `[JsonPropertyName("snake_case")]` — маппінг JSON → C# | 21 | System.Text.Json |
| `HttpRequestException` — мережева помилка | 21 | |
| `TaskCanceledException when (!ct.IsCancellationRequested)` — таймаут HttpClient | 21 | |
| `Uri.EscapeDataString(s)` — кодування URL-параметрів | 21 | |
| EF async: `ToListAsync`, `FirstOrDefaultAsync`, `CountAsync`, `AnyAsync`, `SumAsync`, `SaveChangesAsync` | 21 | |
| S: Single Responsibility Principle — одна причина для зміни | 22 | |
| O: Open/Closed Principle — відкритий для розширення, закритий для змін | 22 | |
| L: Liskov Substitution Principle — підтипи замінні для базових типів | 22 | (аналіз) |
| I: Interface Segregation Principle — маленькі інтерфейси | 22 | |
| D: Dependency Inversion Principle — залежність від абстракцій | 22 | |
| Strategy pattern: `ICostStrategy`, реалізації | 22 | OCP |
| Decorator pattern: `LoggingPatientService(IPatientService inner)` | 22 | ISP+DIP |
| Primary constructor (C# 12): `class Foo(BarDep dep)` | 22 | |
| `IServiceCollection`, `ServiceCollection` | 22 | Microsoft.Extensions.DI |
| `services.AddSingleton<T>()`, `AddScoped<T>()`, `AddTransient<T>()` | 22 | |
| `services.AddScoped<IFoo, FooImpl>()` — interface → implementation | 22 | |
| `services.AddScoped<IFoo>(sp => new Decorator(sp.GetRequired<Impl>()))` | 22 | DI Decorator |
| `services.BuildServiceProvider()` → `IServiceProvider` | 22 | |
| `provider.GetRequiredService<T>()` — кидає якщо не зареєстровано | 22 | |
| `provider.GetService<T>()` — null якщо не зареєстровано | 22 | |
| `provider.CreateScope()` → `IServiceScope` | 22 | |
| `ReferenceEquals(a, b)` — перевірка ідентичності об'єктів | 22 | lifetime demo |
| `services.AddDbContext<T>()` — EF Core реєстрація у DI | 22 | |
| `record ClinicConfig(...)` — конфігурація як immutable record | 22 | SRP |

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

### Lab 17-20 — EF Core (feature/ef-core → злито в main) ✅

Детально — у `CODEBASE_STATE.md` секції Lab 17-20.

---

### Lab 21 — Async / Await (feature/async → злито в main) ✅

**Нові концепції:**

**Task 1 — async Task Main + SeedAsync:**
- `async Task` — правильний тип для async void-методів
- `await` у top-level statements → компілятор генерує `async Task Main`
- `AnyAsync(ct)`, `SaveChangesAsync(ct)` — async EF методи в DbSeeder
- `CancellationToken ct = default` — опціональний параметр (CancellationToken.None якщо не передано)

**Task 2 — AsyncClinicService базові методи:**
- `ToListAsync(ct)`, `FirstOrDefaultAsync(p => ..., ct)` — EF Core async методи
- `SaveChangesAsync(ct)` — async INSERT/UPDATE без блокування потоку
- `ConfigureAwait(false)` — в ClinicRepository (DAL): не захоплювати SynchronizationContext
- Конвенція: `GetPatients()` → `GetPatientsAsync(CancellationToken ct = default)`

**Task 3 — WhenAll, WhenAny, Parallel.ForEachAsync:**
- `Task.WhenAll(t1, t2, t3)` — запускає всі паралельно, чекає поки всі завершать
- Результати через `.Result` після `WhenAll` — безпечно, бо Task вже завершений
- `Task.WhenAny(apiTask, timeoutTask)` — перемагає перший; решту скасовуємо через `CancellationTokenSource`
- `Parallel.ForEachAsync` з `MaxDegreeOfParallelism` — обмеження паралелізму
- `Interlocked.Increment(ref count)` — thread-safe лічильник замість `count++`
- DbContext антипатерн: не викликати `FindAsync` всередині `Parallel.ForEachAsync` на одному контексті
- Правильний патерн: завантажити → обробити в пам'яті → зберегти одним SaveChangesAsync
- `CancellationTokenSource(TimeSpan)` — автоматичний таймаут
- `OperationCanceledException` — окремий catch від загального `Exception`

**Task 4 — AggregateException:**
- `AggregateException.InnerExceptions` — всі помилки, не тільки перша
- `await Task.WhenAll(...)` → розгортає до першого `InnerException`
- `ContinueWith(t => ..., TaskContinuationOptions.OnlyOnFaulted)` — обробник тільки для помилок
- `TaskContinuationOptions`: `OnlyOnFaulted`, `OnlyOnCanceled`, `OnlyOnRanToCompletion`
- `task.IsCompletedSuccessfully` — перевірка без виключення

**Task 5 — IProgress\<T\>:**
- `IProgress<T>` — абстракція: метод не знає про UI, тільки викликає `Report(value)`
- `Progress<T>(callback)` — маршалює `Report()` на UI-потік (SynchronizationContext)
- `progress?.Report(...)` — null-safe: якщо caller не передав progress — нічого не відбувається
- `ct.ThrowIfCancellationRequested()` — явна перевірка на кожній ітерації циклу

**Task 6 — HttpClient:**
- `HttpClient` як singleton: один статичний екземпляр замість `using var http = new HttpClient()`
- `HttpClient.BaseAddress`, `HttpClient.Timeout` — конфігурація
- `GetFromJsonAsync<T>(url, ct)` — GET + JSON → T в один виклик
- `[JsonPropertyName("...")]` на `record` властивостях — маппінг snake_case JSON
- `HttpRequestException` — мережева помилка (немає з'єднання, HTTP error)
- `TaskCanceledException when (!ct.IsCancellationRequested)` — таймаут HttpClient (не скасування)
- `Uri.EscapeDataString(s)` — кодування спецсимволів у URL
- `response.IsSuccessStatusCode` — перевірка HTTP 2xx
- FDA Open API: публічний API без реєстрації (`api.fda.gov/drug/label.json`)

---

### Lab 22 — SOLID + Dependency Injection (feature/solid-di → злито в main) ✅

**Task 1 — S: SRP:**
- `ClinicConfig` record — конфігурація виділена з `Clinic`
- `public Clinic(ClinicConfig config)` + `Clinic(string name) : this(new ClinicConfig(name))`
- `public string Name => Config.Name` — делегат замість поля
- Документація порушень SRP що залишились

**Task 2 — O: OCP (Strategy pattern):**
- `ICostStrategy` — інтерфейс з `Description` і `Calculate(Appointment)`
- `RegularCostStrategy`, `UrgentCostStrategy(multiplier)`, `DiscountCostStrategy(percent)`
- `AppointmentProcessor.WithCostStrategy()` — fluent розширення без зміни існуючої логіки
- `CalculateCost(a)` — `_costStrategy?.Calculate(a) ?? a.GetCost()`
- Тест OCP: `NightShiftCostStrategy` без зміни жодного існуючого файлу

**Tasks 3+4 — I+D: ISP + DIP:**
- `IPatientService`, `IDoctorService`, `IAppointmentService` — маленькі інтерфейси (ISP)
- `PatientService(ClinicDbContext context)` — primary constructor C# 12 (DIP)
- `DoctorService`, `AppointmentService` — аналогічно

**Task 5 — IServiceCollection + Decorator:**
- `ServiceContainer.Build()` — `ServiceCollection` + `BuildServiceProvider()`
- `AddSingleton<ClinicLogger>()`, `AddScoped<ClinicDbContext>()`, `AddScoped<I, Impl>()`
- `LoggingPatientService(IPatientService inner, ClinicLogger logger)` — Decorator
- DI реєстрація Decorator через фабричну лямбду `sp => new LoggingPatientService(...)`
- Перевірка Singleton: `ReferenceEquals(a, b) == true`
- Перевірка Scoped: різні scope → різні екземпляри

**Task 6 — GetRequiredService + LSP аналіз:**
- `GetRequiredService<T>()` — InvalidOperationException якщо незареєстровано
- `GetService<T>()` — null якщо незареєстровано
- `provider.CreateScope()` — scope для Scoped-сервісів в консольному застосунку
- LSP аналіз: `Appointment` ієрархія замінна (демонстрація)

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
