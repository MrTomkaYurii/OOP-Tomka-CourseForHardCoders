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
| `delegate`, `event`, `EventArgs`, `+=` | 12 | |
| LINQ (`.Where`, `.Select`, `.OrderBy`, `.GroupBy`, `.Join`, | 13 | |
|   `.FirstOrDefault`, `.Any`, `.Sum`, `.Average`, `.Min`, `.Max`, | | |
|   `.Count(predicate)`, `.ToList()`, `.ToArray()`) | | |
| `Func<>`, `Action<>`, `Predicate<>`, lambda як змінна | 14 | |
| `Stream`, `StreamReader/Writer`, `File`, `Directory` | 15 | |
| `System.Text.Json` (серіалізація) | 15 | |
| `Console.Clear()`, `ConsoleColor`, `SetCursorPosition` | 16 | |
| EF Core: `DbContext`, `DbSet<T>`, міграції | 17 | |
| EF: One-to-Many, Many-to-Many, зовнішні ключі | 18 | |
| EF: TPH, Owned Entity, Concurrency | 19 | |
| EF: `IQueryable<T>`, `.Skip/.Take`, проєкції | 20 | |
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
- `interface ICancellable { void Cancel(string reason); bool IsCancelled; }`
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

### Lab 11 — Reflection & Attributes (feature/reflection → чекає Lab12)

**Нові конструкції:**
- `[AttributeUsage(...)] class RequiredAttribute : Attribute`
- `typeof(T)`, `obj.GetType()`
- `PropertyInfo[]` через `Type.GetProperties()`
- `GetCustomAttribute<T>()`

---

### Lab 12 — Events (feature/events → зливається)

**Нові конструкції:**
- `delegate void Handler(object? sender, EventArgs e)`
- `event EventHandler<T> OnSomething`
- `+=`, `-=` підписка/відписка
- Власний `EventArgs`: `class AppointmentEventArgs : EventArgs`

---

### Lab 13 — LINQ (feature/linq → зливається)

**Нові конструкції (увесь LINQ!):**
- `.Where(predicate)`, `.Select(selector)`, `.ToList()`, `.ToArray()`
- `.OrderBy(key)`, `.OrderByDescending(key)`, `.ThenBy(key)`
- `.GroupBy(key)`, `.Join(...)`, `.First/FirstOrDefault()`
- `.Any(pred)`, `.All(pred)`, `.Count(pred)`
- `.Sum()`, `.Average()`, `.Min()`, `.Max()`, `.MinBy()`, `.MaxBy()`
- Query syntax: `from x in source where ... select ...`

**Перехід:** Усі Manager-методи з Lab 03-12 що використовували ручні цикли для пошуку/фільтрації можна спростити через LINQ

---

### Lab 14 — Functional (feature/functional → чекає Lab15)

**Нові конструкції:**
- `Func<T, TResult>`, `Action<T>`, `Predicate<T>`
- Lambda як змінна: `Func<Patient, bool> isAdult = p => p.Age >= 18;`
- Higher-order методи: `ApplyTo(IEnumerable<T> items, Func<T,bool> filter)`
- Замикання (closures)
- Методи розширення: `static T MyMethod(this IEnumerable<T> source)`

---

### Lab 15 — Streams & Files (feature/storage → зливається)

**Нові конструкції:**
- `StreamWriter`, `StreamReader`
- `File.WriteAllText()`, `File.ReadAllText()`
- `FileInfo`, `DirectoryInfo`, `Path`
- `JsonSerializer.Serialize/Deserialize<T>()`
- `using` statement для IDisposable

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
