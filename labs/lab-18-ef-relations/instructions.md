# Лаба 18 — EF Core: зв'язки та Navigation Properties

## Мета

Описати зв'язки між таблицями через зовнішні ключі та navigation properties, зберегти ієрархію записів в одній таблиці (TPH), завантажувати пов'язані дані одним запитом (`Include`) і робити запити лише для читання без відстеження змін (`AsNoTracking`).

## Контекст

Після Лаби 17 у БД є дві незалежні таблиці — `Patients` і `Doctors`. Але запис на прийом пов'язаний з конкретним пацієнтом і лікарем. Якщо завантажувати таблиці окремо і зіставляти вручну, це: багато коду; **проблема N+1** — для 100 записів 101 запит до БД, щоб показати імена; жодної гарантії узгодженості даних.

Реляційні БД вирішують це **зовнішніми ключами** (Foreign Keys). EF Core додає до них **navigation properties** — C#-властивості, що описують зв'язки між класами.

### Структура проєкту на початку лаби

Це результат Лаби 17 — стан `main` після її злиття:

```text
oop-course/                                   ← гілка main (після злиття Лаби 17)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/
    │   ├── Patient.cs
    │   ├── Doctor.cs
    │   ├── Appointment.cs
    │   ├── RegularAppointment.cs
    │   ├── SpecialistAppointment.cs
    │   ├── UrgentAppointment.cs
    │   └── … ще 10 файлів без змін
    ├── Managers/  (13 файлів)
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    ├── Events/  (4 файли)
    ├── Extensions/  (3 файли)
    ├── UI/  (1 файл)
    ├── Data/
    │   ├── ClinicDbContext.cs
    │   └── DbSeeder.cs
    └── Migrations/  (3 файли — генерує EF)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Ключові поняття

- **Navigation property** — властивість, що посилається на інший об'єкт або колекцію: у `Patient` — колекція його записів, у `Appointment` — його пацієнт. EF заповнює її даними з БД за відповідного запиту.
- **Eager loading** — `.Include(...)`: EF виконує один SQL-`JOIN` і повертає пов'язані дані разом, замість N+1 окремих запитів.
- **One-to-Many** — «один пацієнт — багато записів». Описується з боку `Appointment`, де живе стовпець зовнішнього ключа: `HasOne(...).WithMany(...).HasForeignKey(...)`.
- **TPH (Table Per Hierarchy)** — усі підтипи `Appointment` в **одній таблиці** зі стовпцем-дискримінатором `AppointmentType`; поля підтипів (`UrgencyNote`, `ConsultationTopic`) у рядках інших типів — `NULL`. Перевага — без `JOIN`; недолік — порожні стовпці.
- **`AsNoTracking()`** — EF за замовчуванням зберігає копію кожного завантаженого об'єкта, щоб помітити зміни. Для запитів лише на читання це зайва робота — `AsNoTracking()` її вимикає.

### Що нового дозволено (і тільки воно)

- navigation properties (`ICollection<T>`, посилання на об'єкт);
- `HasOne` / `WithMany` / `HasForeignKey`, `OnDelete`;
- TPH: `HasDiscriminator`;
- `Include`, `AsNoTracking`.

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-18
```

Коміт — на кожне завдання (`Lab18 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. Navigation properties і підготовка моделей до EF ⭐⭐

### Умова

Додайте до моделей зв'язки і підготуйте ієрархію записів до роботи з EF: завантажуючи об'єкт, EF викликає конструктор без параметрів, а потім заповнює властивості через сеттери.

**Що реалізувати:**

1. У `Patient` і `Doctor` додати колекцію записів `Appointments` (специфікація нижче).
2. У `Appointment` додати навігаційні властивості `Patient` і `Doctor`.
3. У `Appointment` додати `protected` конструктор без параметрів із безпечними значеннями за замовчуванням.
4. У `UrgentAppointment` змінити `UrgencyNote` на `{ get; private set; }` і додати `protected` конструктор без параметрів.
5. У `SpecialistAppointment` змінити `ConsultationTopic` на `{ get; private set; }` і додати **`private`** конструктор без параметрів (клас `sealed` — `protected` у ньому безглуздий).

### Специфікація

| Клас | Додати |
|------|--------|
| `Patient` | `public ICollection<Appointment> Appointments { get; private set; } = new List<Appointment>();` |
| `Doctor` | те саме |
| `Appointment` | `public Patient? Patient { get; set; }`, `public Doctor? Doctor { get; set; }`, `protected Appointment()` |
| `UrgentAppointment` | `UrgencyNote { get; private set; }`, `protected UrgentAppointment()` |
| `SpecialistAppointment` | `ConsultationTopic { get; private set; }`, `private SpecialistAppointment()` |

### Приклад

```csharp
Patient p = context.Patients.Include(p => p.Appointments).First();
Console.WriteLine(p.Appointments.Count);   // кількість записів пацієнта з БД
```

### Підказки

1. `ICollection<T>` — інтерфейс, який EF уміє заповнювати; ініціалізація порожнім списком захищає від `null` у нового об'єкта.
2. `private set` EF встановлює через рефлексію — ззовні властивість і далі лише для читання.
3. EF може викликати й `private` конструктор (теж через рефлексію) — тому для `sealed` класу достатньо `private`.

📖 Документація:
- [Зв'язки: огляд](https://learn.microsoft.com/ef/core/modeling/relationships)
- [Конструктори сутностей](https://learn.microsoft.com/ef/core/modeling/constructors)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `Patient.Appointments` | `Guest.Bookings` | `Customer.Reservations` | `Student.Enrollments` | `Client.Rentals` | `Reader.Loans` | `Member.Sessions` |

### Коміт

```bash
git add ClinicApp/Models/
git commit -m "Lab18 Task01"
```

---

## Задача 2. Зв'язки One-to-Many і TPH у Fluent API ⭐⭐⭐

### Умова

Опишіть таблицю `Appointments`: два зовнішні ключі, ієрархію підтипів в одній таблиці і збереження стану запису.

**Що реалізувати:**

1. Додати в `ClinicDbContext` таблицю `DbSet<Appointment> Appointments`.
2. Налаштувати `Appointment` у `OnModelCreating` за специфікацією: ключ, зв'язки з пацієнтом і лікарем, дискримінатор.
3. Налаштувати поля підтипів `UrgentAppointment` і `SpecialistAppointment`.
4. Відобразити стан оплати: `IsPaid` обчислюється з приватного поля `_isPaid`, тому зберігати треба саме поле.

### Специфікація

| Що | Налаштування |
|----|--------------|
| Таблиця | `Appointments` |
| Ключ | `Id`, IDENTITY; значення з `_nextId` ігнорується (як у Лабі 17) |
| `PatientId` | FK → `Patients(Id)`, видалення **каскадне** (видалили пацієнта — видалились записи) |
| `DoctorId` | FK → `Doctors(Id)`, видалення **заборонене** (`Restrict`), поки в лікаря є записи |
| Дискримінатор | стовпець `AppointmentType` (рядок): `Base`, `Regular`, `Urgent`, `Specialist` |
| `Status` | рядком |
| Стан оплати | приватне поле `_isPaid` → стовпець `IsPaid` |
| `UrgencyNote` | до 200 символів, за замовчуванням `""` |
| `ConsultationTopic` | до 200 символів, за замовчуванням `""` |

### Приклад

```
Appointments
Id | PatientId | DoctorId | AppointmentType | Status    | IsPaid | UrgencyNote   | ConsultationTopic
 1 |     1     |    1     | Regular         | Completed |   1    | NULL          | NULL
 2 |     2     |    2     | Urgent          | Scheduled |   0    | біль у грудях | NULL
```

### Підказки

1. **Два каскади — помилка.** SQL Server не дозволяє двох каскадних шляхів до однієї таблиці: якщо обидва FK каскадні, міграція впаде. Тому один каскадний, другий — `Restrict`.
2. Поля підтипів налаштовуються окремо — `modelBuilder.Entity<UrgentAppointment>()`.
3. **Приватне поле як стовпець:** властивість, якої немає в класі, але яку EF має зберігати, оголошується через `Property<bool>("_isPaid")` з потрібною назвою стовпця.
4. Значення дискримінатора задаються для кожного типу ієрархії через `HasValue<…>("…")`.

📖 Документація:
- [Зв'язки один-до-багатьох](https://learn.microsoft.com/ef/core/modeling/relationships/one-to-many)
- [Каскадне видалення](https://learn.microsoft.com/ef/core/saving/cascade-delete)
- [Успадкування (TPH)](https://learn.microsoft.com/ef/core/modeling/inheritance)
- [Поля-резерви (backing fields)](https://learn.microsoft.com/ef/core/modeling/backing-field)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `Appointments`: Regular / Urgent / Specialist | `Bookings`: Standard / Suite / Corporate | `Reservations`: Regular / PrivateRoom / Event | `Enrollments`: Regular / Online / Intensive | `Rentals`: Basic / Premium / LongTerm | `Loans`: Regular / Digital / Research | `Sessions`: Regular / Personal / Group |

### Коміт

```bash
git add ClinicApp/Data/ClinicDbContext.cs
git commit -m "Lab18 Task02"
```

---

## Задача 3. Міграція і записи в `DbSeeder` ⭐⭐

### Умова

Застосуйте нову схему і додайте в сідер записи на прийом. Записи потребують справжніх `Id` пацієнтів і лікарів, які видає БД, — тому записи додаються **після** збереження пацієнтів і лікарів.

**Що реалізувати:**

1. Розділити `DbSeeder.Seed` на кроки `SeedPatients`, `SeedDoctors`, `SeedAppointments`, кожен зі своїм `SaveChanges()`.
2. `SeedAppointments` завантажує пацієнтів і лікарів із БД і створює 4 записи різних типів (звичайний, терміновий, спеціаліста), частина — завершені й оплачені.
3. `SeedAppointments` ідемпотентний: якщо записи вже є — нічого не додає.
4. Створити і застосувати міграцію `AddAppointmentsWithRelations`; у згенерованому класі знайти стовпець `AppointmentType`, FK з `ON DELETE CASCADE` і FK з `ON DELETE NO ACTION`.

### Специфікація

```bash
dotnet ef migrations add AddAppointmentsWithRelations --project ClinicApp
dotnet ef database update --project ClinicApp
```

| Крок сідера | Що робить |
|-------------|-----------|
| `SeedPatients` | 5 пацієнтів (якщо таблиця порожня) |
| `SeedDoctors` | 5 лікарів (якщо таблиця порожня) |
| `SeedAppointments` | 4 записи трьох типів на реальні `Id`, частина `Completed` і оплачені (якщо таблиця порожня) |

### Приклад

```csharp
var patients = context.Patients.ToList();   // справжні Id з БД
var doctors  = context.Doctors.ToList();
```

### Підказки

1. Порядок важливий: записи посилаються на пацієнтів і лікарів через FK — без них у БД запис не збережеться.
2. Після `SaveChanges()` EF записує в об'єкти `Id`, видані БД; повторне завантаження (`ToList()`) дає їх надійно.
3. Завершення й оплата — тими самими методами, що й раніше (`Complete()`, `MarkPaid()`), перед збереженням.

📖 Документація:
- [Міграції: огляд](https://learn.microsoft.com/ef/core/managing-schemas/migrations/)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `SeedAppointments` | `SeedBookings` | `SeedReservations` | `SeedEnrollments` | `SeedRentals` | `SeedLoans` | `SeedSessions` |

### Коміт

```bash
git add ClinicApp/Data/DbSeeder.cs ClinicApp/Migrations/
git commit -m "Lab18 Task03"
```

---

## Задача 4. `ClinicRepository`: запити з `Include` ⭐⭐⭐

### Умова

Зберіть складні запити до БД в одному класі. Репозиторій отримує `ClinicDbContext` через конструктор (ін'єкція залежності — тема Лаби 22, але патерн правильний уже зараз).

**Що реалізувати:**

1. Клас `ClinicRepository` у `ClinicApp/Data/` з конструктором `(ClinicDbContext context)`.
2. Чотири методи зі специфікації.

### Специфікація

| Метод | Повертає | Що робить |
|-------|----------|-----------|
| `GetPatientWithAppointments(int patientId)` | `Patient?` | пацієнт із заповненою колекцією `Appointments` |
| `GetUpcomingAppointments()` | `List<Appointment>` | заплановані майбутні записи з пацієнтом і лікарем |
| `GetAppointmentsByPatient(int patientId)` | `List<Appointment>` | усі записи пацієнта з лікарем, від найновіших |
| `GetDoctorStats()` | `List<(string Name, int Count, decimal Revenue)>` | для кожного лікаря — кількість записів і виручка; запит лише для читання |

### Приклад

```
GetDoctorStats():
Олег Сидоренко  | записів: 2 | 600.00 грн
Наталія Мороз   | записів: 1 | 450.00 грн
```

### Підказки

1. Пацієнта й лікаря для запису — двома `Include`.
2. **Виручку не можна порахувати в SQL**: `GetCost()` — C#-метод, EF не перекладе його в SQL. Завантажте лікарів разом із записами (`AsNoTracking` + `Include`), матеріалізуйте (`ToList()`), а суму порахуйте вже в пам'яті.
3. `Include` разом із проєкцією `Select` у запиті ігнорується — завантажуйте зв'язані дані або через `Include`, або через `Select`, а не обома одразу.
4. Без `Include` навігаційна властивість лишиться `null` — і звернення до `appointment.Patient.FullName` кине `NullReferenceException`.

📖 Документація:
- [Завантаження пов'язаних даних](https://learn.microsoft.com/ef/core/querying/related-data/)
- [Запити без відстеження](https://learn.microsoft.com/ef/core/querying/tracking)
- [Обчислення на клієнті](https://learn.microsoft.com/ef/core/querying/client-eval)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `GetPatientWithAppointments` | `GetGuestWithBookings` | `GetCustomerWithReservations` | `GetStudentWithEnrollments` | `GetClientWithRentals` | `GetReaderWithLoans` | `GetMemberWithSessions` |

### Коміт

```bash
git add ClinicApp/Data/ClinicRepository.cs
git commit -m "Lab18 Task04"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                                    ← гілка Lab-18 (після злиття — main)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/
    │   ├── Patient.cs                         ✏ Т1
    │   ├── Doctor.cs                          ✏ Т1
    │   ├── Appointment.cs                     ✏ Т1
    │   ├── RegularAppointment.cs              ✏ Т1
    │   ├── SpecialistAppointment.cs           ✏ Т1
    │   ├── UrgentAppointment.cs               ✏ Т1
    │   └── … ще 10 файлів без змін
    ├── Managers/  (13 файлів)
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    ├── Events/  (4 файли)
    ├── Extensions/  (3 файли)
    ├── UI/  (1 файл)
    ├── Data/
    │   ├── ClinicDbContext.cs                 ✏ Т2
    │   ├── DbSeeder.cs                        ✏ Т3
    │   └── ClinicRepository.cs                🆕 Т4
    └── Migrations/  (5 файлів — генерує EF)   ✏ Т3
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 17.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] У таблиці `Appointments` є стовпці `AppointmentType`, `IsPaid`, `UrgencyNote`, `ConsultationTopic`
- [ ] FK `PatientId` — `ON DELETE CASCADE`, `DoctorId` — `ON DELETE NO ACTION`
- [ ] Після сідера в БД 4 записи трьох типів, оплачені мають `IsPaid = 1`
- [ ] `GetPatientWithAppointments` повертає пацієнта із записами; `GetDoctorStats` — кількість і виручку кожного лікаря
- [ ] Повторний запуск не дублює дані

---

## Питання для самоперевірки

1. **Navigation чи Id.** В `Appointment` є і `PatientId` (FK), і `Patient` (навігація). Навіщо зберігати FK окремо?
2. **Cascade чи Restrict.** Видалення пацієнта видаляє його записи, а видалення лікаря заборонене. Чи правильно це з погляду бізнесу? Яка альтернатива?
3. **TPH чи TPT.** Один рядок з nullable-стовпцями чи окремі таблиці для підтипів із `JOIN` — коли що краще?
4. **Lazy loading.** EF може завантажувати навігацію автоматично при першому зверненні. Чому ми його не вмикаємо?
5. **Глибина `Include`.** Що дасть `.Include(p => p.Appointments).ThenInclude(a => a.Doctor)`? Чи є небезпека?
6. **Чому `GetCost()` не працює в SQL-запиті** і де проходить межа між тим, що виконує БД, і тим, що виконує C#?

---

## Статус гілки

Після всіх 4 завдань (кожне — окремий коміт `Lab18 TaskNN` на гілці `Lab-18`):

```bash
git push -u origin Lab-18
git checkout main
git merge --no-ff Lab-18 -m "Merge Lab-18: EF Core Relations"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-19`.
