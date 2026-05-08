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
| `abstract class`, `abstract` методи | 06 | разом з успадкуванням |
| `virtual` методи | 06 | |
| `List<T>` (базово: Add, Count, [], foreach) | 09 | Generics лаба |
| Підпростори імен (`ClinicApp.Models` тощо) + `using` директиви | 05 | організація файлів |
| `private` backing fields `_camelCase` | 05 | |
| Явні сеттери з валідацією | 05 | |
| `throw new ArgumentException(msg)` | 05 | |
| `throw new ArgumentOutOfRangeException(paramName, msg)` | 05 | |
| `string.IsNullOrWhiteSpace(value)` | 05 | |
| `nameof(Symbol)` | 05 | |
| `try / catch` (порядок блоків) | 05 | |
| `Regex.IsMatch()`, `static readonly Regex` | 05 | опційно |
| `: BaseClass`, `base()` | 06 | успадкування |
| `override` переваги методів | 06 | |
| `is`, `as`, явне приведення | 06 | |
| `interface` | 07 | |
| Кілька інтерфейсів на одному класі | 07 | |
| Поліморфізм (base ref → child type) | 08 | |
| `new` (приховування методу) | 08 | |
| Генерики `<T>`, `where T :` | 09 | |
| `Queue<T>`, `Stack<T>` | 09 | |
| `IEnumerable<T>`, `yield return` | 10 | |
| `IComparable<T>`, `IComparer<T>` | 10 | |
| `SortedSet<T>`, `SortedList<K,V>` | 10 | |
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

### Lab 06 — Inheritance (feature/inheritance → зливається)

**Нові конструкції:**
- Успадкування: `class InsuredPatient : Patient`
- `base(...)` в конструкторі
- `override` методу батьківського класу
- `is` (перевірка типу), `as` (безпечне приведення)
- `(ChildType)parent` явне приведення

---

### Lab 07 — Interfaces (feature/interfaces → зливається)

**Нові конструкції:**
- `interface ISchedulable { ... }`
- Реалізація кількох інтерфейсів: `class X : Base, IFoo, IBar`
- Явна реалізація: `void IFoo.Method() { ... }`
- Generic interface: перший погляд на `IRepository<T>`

---

### Lab 08 — Polymorphism (feature/polymorphism → чекає Lab09)

**Нові конструкції:**
- Поліморфний список: `Patient[] patients` зберігає `InsuredPatient`, `PrivatePatient`
- `new` (метод-приховування, відмінне від `override`)
- Виклик через базовий тип

---

### Lab 09 — Generics (feature/generics → зливається)

**Нові конструкції:**
- `class Repository<T> where T : ...`
- `class WaitingQueue<T>`
- `Queue<T>`, `Stack<T>` зі стандартної бібліотеки
- Типові параметри: `where T : class`, `where T : new()`, `where T : IInterface`
- Пояснення: чому `List<T>` — це generics (retroactively)

---

### Lab 10 — Iterators & Comparators (feature/iterators → зливається)

**Нові конструкції:**
- `IEnumerable<T>`: реалізація `GetEnumerator()`, `yield return`
- `IComparable<T>`: `CompareTo()` для сортування
- `IComparer<T>`: окремий клас-компаратор
- `SortedSet<T>`, `SortedList<K,V>`
- Власний `foreach` через `IEnumerable`

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
| `List<T>` в Labs 01–03 основному коді | Не введений до Lab 04 |
| `TimeOnly`, `DateOnly` в Labs 01–05 | Надто специфічні типи, вводяться при потребі |
| `?.` і `??` в Labs 01–03 | Не введені до Lab 04 |
| `Dictionary<K,V>` в Labs 01–08 | Офіційно в Lab 09+ |
| `IEnumerable<T>` як тип параметра в Labs 01–09 | Не введений до Lab 10 |
