# Лаба 22 — SOLID + Dependency Injection

## Мета

Застосувати п'ять принципів SOLID до наявного проєкту і зробити залежності між класами керованими через Dependency Injection: виділити конфігурацію, додати стратегії ціноутворення, розбити сервіси на вузькі інтерфейси, зареєструвати їх у DI-контейнері з декоратором і перевірити принцип підстановки Лісков.

## Контекст

Після Лаб 03–21 у нас тисячі рядків робочого коду, але з прихованою проблемою — **жорсткими залежностями**:

```csharp
// Clinic.cs — усі залежності створюються прямо в конструкторі
public Clinic(string name)
{
    Patients = new PatientManager();      // ← жорстко
    Logger   = new ClinicLogger();        // ← жорстко
    Exporter = new ClinicExporter(this);  // ← жорстко
    // … ще десяток рядків
}
```

Наслідки: `ClinicLogger` неможливо підмінити тестовим; новий тип ціноутворення вимагає змінювати `AppointmentProcessor`; `Clinic` знає про десятки конкретних класів і змінюється разом із кожним. **SOLID** — п'ять принципів проти цих проблем; **Dependency Injection** — механізм, що робить залежності керованими.

### Структура проєкту на початку лаби

Це результат Лаби 21 — стан `main` після її злиття:

```text
oop-course/                                    ← гілка main (після злиття Лаби 21)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/  (20 файлів)
    ├── Managers/
    │   ├── AppointmentProcessor.cs
    │   └── … ще 12 файлів без змін
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    ├── Events/  (4 файли)
    ├── Extensions/  (3 файли)
    ├── UI/  (1 файл)
    ├── Data/  (6 файлів)
    └── Migrations/  (9 файлів — генерує EF)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### SOLID коротко

| Принцип | Формулювання | Де в цій лабі |
|---------|--------------|---------------|
| **S** — Single Responsibility | у класу одна причина для зміни | `ClinicConfig` (Задача 1) |
| **O** — Open/Closed | відкритий для розширення, закритий для змін | стратегії ціни (Задача 2) |
| **L** — Liskov Substitution | підтип замінює базовий тип без сюрпризів | ієрархія `Appointment` (Задача 5) |
| **I** — Interface Segregation | клієнт не залежить від методів, яких не використовує | вузькі сервісні інтерфейси (Задача 3) |
| **D** — Dependency Inversion | залежати від абстракцій, а не від конкретних класів | сервіси через конструктор (Задачі 3–4) |

### Dependency Injection

**DI-контейнер** (`ServiceCollection`) зберігає правила «який тип створювати для якої залежності» і сам будує об'єкти з усіма їхніми залежностями. **Час життя** реєстрації:

| Lifetime | Новий екземпляр | Підходить для |
|----------|-----------------|---------------|
| `Singleton` | один на весь застосунок | логер, `HttpClient`, конфігурація |
| `Scoped` | один на кожен scope (`CreateScope()`) | `DbContext`, репозиторії, сервіси |
| `Transient` | при кожному запиті | легкі об'єкти без стану |

Singleton **не може** залежати від Scoped: інакше він «захопить» перший `DbContext` назавжди.

**Декоратор** реалізує той самий інтерфейс, що й «справжній» об'єкт, і делегує йому виклики, додаючи свою поведінку (наприклад, логування) — без зміни самого об'єкта.

### Що нового дозволено (і тільки воно)

- `record` з обчислюваними властивостями;
- primary constructor (C# 12): `class PatientService(ClinicDbContext context)`;
- пакет `Microsoft.Extensions.DependencyInjection`: `ServiceCollection`, `AddSingleton` / `AddScoped`, `AddDbContext`, `GetRequiredService` / `GetService`, `CreateScope`.

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-22
```

Коміт — на кожне завдання (`Lab22 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. S — конфігурація клініки в `ClinicConfig` ⭐

### Умова

У `Clinic` кілька причин змінитись: конфігурація, нові менеджери, події, формат звітів… Почніть зі SRP: винесіть конфігурацію клініки в окремий незмінний `record`.

**Що реалізувати:**

1. Створити `record ClinicConfig` у `ClinicApp/Models/` (специфікація нижче).
2. У `Clinic` додати властивість `Config` і конструктор `Clinic(ClinicConfig config)`.
3. Залишити конструктор `Clinic(string name)` для зворотної сумісності — він передає роботу новому конструктору.
4. `Name` у `Clinic` тепер береться з `Config`.
5. Коментарем у `Clinic.cs` перелічити, які відповідальності в класі ще лишились.

### Специфікація

| `ClinicConfig` | |
|----------------|--|
| `Name` | `string` |
| `Address` | `string`, за замовчуванням `""` |
| `Founded` | `DateTime?`, за замовчуванням `null` |
| `FoundedYear` | обчислювана: рік заснування або `"невідомо"` |

| `Clinic` | |
|----------|--|
| `Config` | `ClinicConfig`, лише читання |
| `Clinic(ClinicConfig config)` | новий основний конструктор |
| `Clinic(string name)` | `: this(new ClinicConfig(name))` |
| `Name` | повертає `Config.Name` |

### Приклад

```csharp
var clinic = new Clinic(new ClinicConfig("Медична клініка", "вул. Медична 1", new DateTime(2010, 3, 1)));
Console.WriteLine(clinic.Config.FoundedYear);   // 2010
var old = new Clinic("Клініка");                 // старий код і далі працює
```

### Підказки

1. `record` з позиційними параметрами — незмінний тип: конфігурацію не можна «випадково» змінити з будь-якого місця програми.
2. Обчислювана властивість у `record` оголошується в тілі після параметрів.
3. Межа «одна відповідальність» — це одна **причина для зміни**, а не один метод.

📖 Документація:
- [Записи (`record`)](https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/record)
- [Принцип єдиної відповідальності](https://learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/architectural-principles#single-responsibility)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `ClinicConfig` | `HotelConfig` | `RestaurantConfig` | `UniversityConfig` | `RentalConfig` | `LibraryConfig` | `GymConfig` |

### Коміт

```bash
git add ClinicApp/Models/ClinicConfig.cs ClinicApp/Clinic.cs
git commit -m "Lab22 Task01"
```

---

## Задача 2. O — стратегії ціноутворення ⭐⭐

### Умова

Щоб додати нову ставку, зараз треба дописувати `if` в існуючий код — і ризикувати зламати те, що працювало. Застосуйте патерн **Strategy**: кожна ставка — окремий клас, а `AppointmentProcessor` лише використовує передану стратегію.

**Що реалізувати:**

1. Створити теку `ClinicApp/Strategies/` з інтерфейсом `ICostStrategy` і трьома стратегіями (специфікація нижче).
2. **Розширити** (не переписати) `AppointmentProcessor` (Лаба 15): необов'язкова стратегія, метод її встановлення, розрахунок ціни і статичне порівняння.
3. Перевірити OCP: додати `NightShiftCostStrategy` (×1.2 для прийомів, що починаються о 18:00 і пізніше) — **без жодних змін** у `AppointmentProcessor`, `Appointment` і наявних стратегіях.

### Специфікація

| Тип | Опис |
|-----|------|
| `ICostStrategy` | `string Description { get; }`, `decimal Calculate(Appointment appointment)` |
| `RegularCostStrategy` | `DurationMinutes × 10` грн |
| `UrgentCostStrategy` | базова × множник (за замовчуванням `1.5`, задається конструктором) |
| `DiscountCostStrategy` | базова × (1 − знижка), знижка задається конструктором |
| `NightShiftCostStrategy` | базова × 1.2, якщо прийом о 18:00 і пізніше; інакше базова |

| Нове в `AppointmentProcessor` | Опис |
|-------------------------------|------|
| поле `ICostStrategy?` | стратегія, спочатку не задана |
| `WithCostStrategy(ICostStrategy strategy)` | встановлює стратегію, повертає `this` |
| `CalculateCost(Appointment a)` | ціна за стратегією; якщо стратегії немає — `a.GetCost()` |
| `static CompareCost(Appointment a, ICostStrategy s)` | `(decimal Regular, decimal WithStrategy)` |

### Приклад

```csharp
var (regular, night) = AppointmentProcessor.CompareCost(appt, new NightShiftCostStrategy());
Console.WriteLine($"{regular:F2} → {night:F2}");   // 300.00 → 360.00 для прийому о 19:00
```

### Підказки

1. Стратегія необов'язкова: без неї процесор поводиться, як раніше, — тому не параметр конструктора, а метод `WithCostStrategy`.
2. `?.` і `??` разом дають «ціна за стратегією або звичайна ціна» одним виразом.
3. Перевірка OCP — це саме те, що змінилось у `git diff` Задачі 2 після додавання `NightShiftCostStrategy`: лише новий файл.

📖 Документація:
- [Патерн «Стратегія»](https://refactoring.guru/uk/design-patterns/strategy)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `NightShiftCostStrategy` | `WeekendRateStrategy` | `LateDinnerStrategy` | `EveningCourseStrategy` | `HolidayRateStrategy` | `OverdueFineStrategy` | `PeakHoursStrategy` |

### Коміт

```bash
git add ClinicApp/Strategies/ ClinicApp/Managers/AppointmentProcessor.cs
git commit -m "Lab22 Task02"
```

---

## Задача 3. I + D — вузькі інтерфейси сервісів і їх реалізації ⭐⭐⭐

### Умова

Замість одного великого «сервісу клініки» опишіть три вузькі інтерфейси (ISP) і реалізуйте їх поверх EF Core так, щоб реалізації отримували `ClinicDbContext` ззовні, через конструктор (DIP).

**Що реалізувати:**

1. Створити теку `ClinicApp/Services/` з трьома інтерфейсами (специфікація нижче); усі методи асинхронні з `CancellationToken ct = default`.
2. Реалізувати `PatientService`, `DoctorService`, `AppointmentService` з **primary constructor**, що приймає `ClinicDbContext`.
3. У `Program.cs` додати функцію `PrintPatientCount(IPatientService service)` — вона приймає **інтерфейс**, а не клас.

### Специфікація

| Інтерфейс | Методи |
|-----------|--------|
| `IPatientService` | `GetAllAsync`, `GetByIdAsync(int id)`, `SearchAsync(string query)`, `AddAsync(Patient p)`, `SoftDeleteAsync(int id)`, `CountAsync` |
| `IDoctorService` | `GetAllAsync`, `GetByIdAsync(int id)`, `GetBySpecialityAsync(Speciality s)`, `CountAsync` |
| `IAppointmentService` | `GetUpcomingAsync`, `GetByPatientAsync(int patientId)`, `BookAsync(Appointment a)`, `CancelAsync(int id)`, `CompleteAsync(int id)`, `GetTotalRevenueAsync` |

### Приклад

```csharp
public class PatientService(ClinicDbContext context) : IPatientService
{
    // context доступний у всіх методах без явного поля
}
```

```
Пацієнтів: 5
```

### Підказки

1. **Primary constructor** — параметри конструктора в оголошенні класу; вони доступні всім методам без явного поля.
2. Для читання — `AsNoTracking()`; для змін — звичайне відстеження і `SaveChangesAsync`.
3. `GetTotalRevenueAsync`: `GetCost()` не перекладається в SQL (Лаба 18) — завантажте записи і порахуйте суму в пам'яті.
4. `PrintPatientCount` працюватиме з будь-якою реалізацією `IPatientService` — `PatientService`, декоратором із Задачі 4 чи тестовою заглушкою.

📖 Документація:
- [Primary constructors](https://learn.microsoft.com/dotnet/csharp/whats-new/tutorials/primary-constructors)
- [Принцип інверсії залежностей](https://learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/architectural-principles#dependency-inversion)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `IPatientService` / `IDoctorService` / `IAppointmentService` | `IGuestService` / `IStaffService` / `IBookingService` | `ICustomerService` / `IWaiterService` / `IReservationService` | `IStudentService` / `ILecturerService` / `IEnrollmentService` | `IClientService` / `IManagerService` / `IRentalService` | `IReaderService` / `ILibrarianService` / `ILoanService` | `IMemberService` / `ITrainerService` / `ISessionService` |

### Коміт

```bash
git add ClinicApp/Services/ ClinicApp/Program.cs
git commit -m "Lab22 Task03"
```

---

## Задача 4. DI-контейнер і декоратор логування ⭐⭐⭐

### Умова

Перестаньте створювати сервіси вручну: зареєструйте їх у DI-контейнері, а логування додайте декоратором — без змін у `PatientService`.

**Що реалізувати:**

1. Додати пакет `Microsoft.Extensions.DependencyInjection` (команда нижче).
2. Створити `static class ServiceContainer` у `ClinicApp/Infrastructure/` з методом `Build()`, що реєструє сервіси за специфікацією і повертає `IServiceProvider`.
3. Створити декоратор `LoggingPatientService` у `ClinicApp/Services/`: реалізує `IPatientService`, отримує «справжній» `IPatientService` і `ClinicLogger`, логує виклик і результат, делегує роботу.
4. Зареєструвати `IPatientService` фабрикою, що обгортає `PatientService` у `LoggingPatientService`.
5. У `Program.cs` побудувати контейнер, отримати сервіси в scope і перевірити час життя (див. приклад).

### Специфікація

```bash
dotnet add ClinicApp package Microsoft.Extensions.DependencyInjection --version 8.0.0
```

| Реєстрація | Lifetime |
|------------|----------|
| `ClinicDbContext` | Scoped (`AddDbContext`) |
| `ClinicLogger` | Singleton |
| `IDoctorService` → `DoctorService` | Scoped |
| `IAppointmentService` → `AppointmentService` | Scoped |
| `IPatientService` → `LoggingPatientService`(`PatientService`) | Scoped, фабрика `sp => …` |

### Приклад

```csharp
var a = provider.GetRequiredService<ClinicLogger>();
var b = provider.GetRequiredService<ClinicLogger>();
Console.WriteLine(ReferenceEquals(a, b));      // True — Singleton

using var s1 = provider.CreateScope();
using var s2 = provider.CreateScope();
var x = s1.ServiceProvider.GetRequiredService<IAppointmentService>();
var y = s2.ServiceProvider.GetRequiredService<IAppointmentService>();
Console.WriteLine(ReferenceEquals(x, y));      // False — Scoped, різні scope
```

### Підказки

1. У фабриці залежності беріть із `sp.GetRequiredService<T>()` — контейнер сам віддасть потрібний екземпляр із правильним часом життя.
2. Декоратор — композиція: він **містить** `IPatientService`, а не успадковує `PatientService`.
3. Методи без логування декоратор просто передає далі — `inner.Метод(...)`.
4. У консольному застосунку scope створюється явно — `CreateScope()`, один scope ≈ одна «операція».

📖 Документація:
- [Dependency injection у .NET](https://learn.microsoft.com/dotnet/core/extensions/dependency-injection)
- [Час життя сервісів](https://learn.microsoft.com/dotnet/core/extensions/dependency-injection#service-lifetimes)
- [Патерн «Декоратор»](https://refactoring.guru/uk/design-patterns/decorator)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `LoggingPatientService` | `LoggingGuestService` | `LoggingCustomerService` | `LoggingStudentService` | `LoggingClientService` | `LoggingReaderService` | `LoggingMemberService` |

### Коміт

```bash
git add ClinicApp/ClinicApp.csproj ClinicApp/Infrastructure/ServiceContainer.cs ClinicApp/Services/LoggingPatientService.cs ClinicApp/Program.cs
git commit -m "Lab22 Task04"
```

---

## Задача 5. `GetRequiredService` чи `GetService`; L — підстановка Лісков ⭐⭐

### Умова

Покажіть різницю між обов'язковим і необов'язковим отриманням сервісу з контейнера і перевірте, що ієрархія записів дотримується принципу підстановки Лісков.

**Що реалізувати:**

1. У `Program.cs` продемонструвати: `GetRequiredService` для зареєстрованого сервісу; `GetService` для зареєстрованого (не `null`) і для незареєстрованого `SessionManager` (`null`).
2. Додати функцію `ProcessAppointment(Appointment a)`, що виводить опис і вартість, і викликати її з об'єктами всіх трьох підтипів — без `is`/`as`.
3. Коментарем описати місце в проєкті, де LSP **могло б** бути порушено (наприклад, якби `UrgentAppointment.Cancel()` кидав виняток замість повернення `false`).

### Специфікація

| Метод | Сервіс не зареєстровано |
|-------|-------------------------|
| `GetRequiredService<T>()` | `InvalidOperationException` — для обов'язкових залежностей |
| `GetService<T>()` | `null` — для необов'язкових |

### Приклад

```
GetService<ClinicLogger>:   знайдено
GetService<SessionManager>: null
Звичайний прийом | 300.00 грн
Терміновий (біль у грудях) | 450.00 грн
Консультація спеціаліста: кардіологія | 780.00 грн
```

### Підказки

1. LSP — не про синтаксис, а про поведінку: підтип не має кидати винятків чи посилювати вимоги там, де базовий тип цього не робить.
2. Підстановку декоратора замість `PatientService` (Задача 4) теж можна розглядати як LSP: код, що працює з `IPatientService`, не помічає різниці.

📖 Документація:
- [`ServiceProviderServiceExtensions`](https://learn.microsoft.com/dotnet/api/microsoft.extensions.dependencyinjection.serviceproviderserviceextensions)
- [Принцип підстановки Лісков](https://learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/architectural-principles#liskov-substitution)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `ProcessAppointment(Appointment)` | `ProcessBooking(Booking)` | `ProcessReservation(TableReservation)` | `ProcessEnrollment(Enrollment)` | `ProcessRental(Rental)` | `ProcessLoan(BookLoan)` | `ProcessSession(Session)` |

### Коміт

```bash
git add ClinicApp/Program.cs
git commit -m "Lab22 Task05"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                                    ← гілка Lab-22 (після злиття — main)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj                       ✏ Т4
    ├── Program.cs                             ✏ Т3 Т4 Т5
    ├── Clinic.cs                              ✏ Т1
    ├── Enums/  (4 файли)
    ├── Models/
    │   ├── ClinicConfig.cs                    🆕 Т1
    │   └── … ще 20 файлів без змін
    ├── Managers/
    │   ├── AppointmentProcessor.cs            ✏ Т2
    │   └── … ще 12 файлів без змін
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    ├── Events/  (4 файли)
    ├── Extensions/  (3 файли)
    ├── UI/  (1 файл)
    ├── Data/  (6 файлів)
    ├── Migrations/  (9 файлів — генерує EF)
    ├── Infrastructure/
    │   └── ServiceContainer.cs                🆕 Т4
    ├── Services/
    │   ├── IPatientService.cs                 🆕 Т3
    │   ├── IDoctorService.cs                  🆕 Т3
    │   ├── IAppointmentService.cs             🆕 Т3
    │   ├── PatientService.cs                  🆕 Т3
    │   ├── DoctorService.cs                   🆕 Т3
    │   ├── AppointmentService.cs              🆕 Т3
    │   └── LoggingPatientService.cs           🆕 Т4
    └── Strategies/
        ├── ICostStrategy.cs                   🆕 Т2
        ├── RegularCostStrategy.cs             🆕 Т2
        ├── UrgentCostStrategy.cs              🆕 Т2
        ├── DiscountCostStrategy.cs            🆕 Т2
        └── NightShiftCostStrategy.cs          🆕 Т2
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 21.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] `new Clinic("…")` і `new Clinic(new ClinicConfig(…))` — обидва працюють
- [ ] Додавання `NightShiftCostStrategy` не змінило жодного існуючого файлу
- [ ] `PrintPatientCount` приймає `IPatientService` і виводить кількість пацієнтів
- [ ] Виклики `IPatientService` з'являються в лозі (працює декоратор)
- [ ] Перевірка часу життя: Singleton — `True`, Scoped у різних scope — `False`
- [ ] `GetService<SessionManager>()` повертає `null`
- [ ] `ProcessAppointment` працює з усіма трьома підтипами без `is`/`as`

---

## Питання для самоперевірки

1. **SOLID як ціле.** Як порушення одного принципу тягне за собою інші? Чи складніше дотриматись DIP, якщо `Clinic` порушує SRP?
2. **Декоратор чи успадкування.** Чому `LoggingPatientService` — декоратор (композиція), а не `class LoggingPatientService : PatientService`? Коли успадкування було б кращим?
3. **Singleton `DbContext`.** `DbContext` тримає в пам'яті стан змінених об'єктів. Що станеться при одночасних запитах, якщо він Singleton?
4. **Primary constructor.** На що компілятор перетворює `class PatientService(ClinicDbContext context)`? Які обмеження порівняно зі звичайним конструктором?
5. **OCP і кількість файлів.** Стратегії зменшують ризик регресій, але множать файли. Коли варто залишити простий `switch`?
6. **ISP у .NET.** `ILogger<T>` — великий чи маленький інтерфейс? Чи порушує він ISP? Порівняйте з `IPatientService`.

---

## Статус гілки

Після всіх 5 завдань (кожне — окремий коміт `Lab22 TaskNN` на гілці `Lab-22`):

```bash
git push -u origin Lab-22
git checkout main
git merge --no-ff Lab-22 -m "Merge Lab-22: SOLID and Dependency Injection"
git push
```

> Це остання лаба курсу. Вітаємо!
