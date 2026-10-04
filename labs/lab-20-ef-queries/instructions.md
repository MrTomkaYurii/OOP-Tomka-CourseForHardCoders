# Лаба 20 — EF Core: IQueryable, пагінація, проєкції

## Мета

Навчитися будувати запити EF Core так, щоб фільтрація, сортування і вибір полів виконувались у SQL, а не в пам'яті: розуміти відкладене виконання `IQueryable<T>`, робити пагінацію, проєкції в DTO і глобальні фільтри (м'яке видалення).

## Контекст

Клініка зростає: 10 000 пацієнтів, 50 000 записів. `context.Patients.ToList()` завантажує **всі** рядки в пам'ять — секунди очікування і десятки мегабайт. Три типові помилки продуктивності:

1. Завантажити все і відфільтрувати в C# — замість `WHERE` у SQL.
2. Показати список із 1000 елементів — замість сторінок по 20.
3. Завантажити повний об'єкт (15 полів), коли потрібні 3, — `SELECT *` замість `SELECT Id, Name, Phone`.

Усі три вирішуються одним принципом: **EF будує SQL-запит поступово і виконує його лише в момент матеріалізації**.

### Структура проєкту на початку лаби

Це результат Лаби 19 — стан `main` після її злиття:

```text
oop-course/                                    ← гілка main (після злиття Лаби 19)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/
    │   ├── Patient.cs
    │   └── … ще 16 файлів без змін
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
    │   ├── DbSeeder.cs
    │   └── ClinicRepository.cs
    └── Migrations/  (7 файлів — генерує EF)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Ключові поняття

**`IQueryable<T>` — опис запиту, а не колекція.** SQL виконується лише при матеріалізації:

| Операція | Виконує SQL? |
|----------|--------------|
| `context.Patients`, `.Where(...)`, `.OrderBy(...)`, `.Skip(...)`, `.Take(...)` | ні — лише нарощують запит |
| `.ToList()`, `.Count()`, `.FirstOrDefault()`, `foreach` | **так** |

`ToList()` посеред ланцюжка — решта операцій виконується вже в C#, над усіма завантаженими рядками.

**Пагінація** — `Skip((page - 1) * pageSize).Take(pageSize)`; EF генерує `OFFSET … FETCH NEXT …`. Без `OrderBy` порядок рядків у БД не гарантований — сторінки будуть непередбачуваними. Загальну кількість для «Показано 1–20 з 347» дає окремий `Count()` до `Skip`/`Take`.

**Проєкція** — `Select(p => new Dto(...))`: EF вибирає з БД лише потрібні стовпці, а кількість записів пацієнта рахує підзапитом `COUNT(*)`. **DTO** (Data Transfer Object) — простий тип лише з даними, без логіки; зручно оголошувати як `record`.

**Глобальний фільтр** — `HasQueryFilter(p => !p.IsDeleted)` у `OnModelCreating`: EF додає `WHERE IsDeleted = 0` до **кожного** запиту до таблиці, включно з `Include`. Обійти фільтр (для адміністративних запитів) — `IgnoreQueryFilters()`.

### Що нового дозволено (і тільки воно)

- `IQueryable<T>` як тип результату методу;
- `Skip` / `Take` для пагінації;
- `record` для DTO, проєкції через `Select`;
- `HasQueryFilter`, `IgnoreQueryFilters`;
- логування SQL через `LogTo` (тимчасово, для спостереження).

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-20
```

Коміт — на кожне завдання (`Lab20 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. `ClinicQueryService`: відкладене виконання ⭐⭐

### Умова

Покажіть різницю між фільтром, що виконується в SQL, і фільтром, що виконується в пам'яті, і дайте викликаючому коду змогу самому дописувати умови до запиту.

**Що реалізувати:**

1. Клас `ClinicQueryService` у `ClinicApp/Data/` з конструктором `(ClinicDbContext context)`.
2. Метод `DemoQueryableVsEnumerable(string filter)`: той самий пошук за прізвищем двома способами — умова **до** `ToList()` і умова **після** `ToList()`; повертає обидва результати.
3. Метод `QueryPatients()`: повертає `IQueryable<Patient>` (лише читання), до якого викликаючий код може додати `Where`/`OrderBy` до виконання.
4. Тимчасово увімкнути в `OnConfiguring` логування SQL (`LogTo`) і порівняти, які запити генерують два способи. Перед комітом логування прибрати.

### Специфікація

| Метод | Повертає |
|-------|----------|
| `DemoQueryableVsEnumerable(string filter)` | `(List<Patient> InSql, List<Patient> InMemory)` |
| `QueryPatients()` | `IQueryable<Patient>` без відстеження змін |

### Приклад

```csharp
var seniors = queryService.QueryPatients()
    .Where(p => p.DateOfBirth.Year < 1960)   // додається до того самого SQL-запиту
    .OrderBy(p => p.LastName)
    .ToList();
```

У лозі SQL перший спосіб `DemoQueryableVsEnumerable` містить `WHERE … LIKE …`, другий — `SELECT` без умови.

### Підказки

1. `IQueryable` «стає даними» на першій матеріалізації — `ToList()`, `Count()`, `foreach`.
2. Для запитів лише на читання — `AsNoTracking()` (Лаба 18).
3. `LogTo(Console.WriteLine, LogLevel.Information)` показує кожен SQL-запит, який EF відправляє в БД.

📖 Документація:
- [Як працюють запити EF](https://learn.microsoft.com/ef/core/querying/how-query-works)
- [Простий журнал SQL](https://learn.microsoft.com/ef/core/logging-events-diagnostics/simple-logging)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `QueryPatients()` | `QueryGuests()` | `QueryCustomers()` | `QueryStudents()` | `QueryClients()` | `QueryReaders()` | `QueryMembers()` |

### Коміт

```bash
git add ClinicApp/Data/ClinicQueryService.cs
git commit -m "Lab20 Task01"
```

---

## Задача 2. Пагінація ⭐⭐

### Умова

Замість повного списку віддавайте дані сторінками разом із загальною кількістю — для інтерфейсу виду «Показано 1–20 з 347».

**Що реалізувати:**

1. У `ClinicQueryService` метод `GetPatientsPaged`: необов'язковий пошук за прізвищем, сортування, сторінка.
2. Метод `GetAppointmentsPaged` з необов'язковими фільтрами за статусом і пацієнтом.
3. В обох — загальна кількість рахується **до** `Skip`/`Take`, а сортування застосовується **перед** ними.

### Специфікація

| Метод | Параметри | Повертає |
|-------|-----------|----------|
| `GetPatientsPaged` | `int page, int pageSize, string? search = null` | `(List<Patient> Items, int TotalCount)`, сортування за прізвищем |
| `GetAppointmentsPaged` | `int page, int pageSize, AppointmentStatus? status = null, int? patientId = null` | `(List<Appointment> Items, int TotalCount)`, сортування за датою |

Необов'язковий фільтр додається до запиту, лише якщо його задано.

### Приклад

```csharp
var (items, total) = queryService.GetPatientsPaged(page: 2, pageSize: 20);
Console.WriteLine($"Показано {items.Count} з {total}");
```

### Підказки

1. Нарощуйте запит у змінній: `query = query.Where(...)` — це не виконує SQL, лише додає умову.
2. `query.Count()` — окремий `SELECT COUNT(*)` у БД; `query.ToList().Count` — завантаження всіх рядків заради одного числа.
3. Номер сторінки рахується з 1: пропустити треба `(page - 1) * pageSize` рядків.

📖 Документація:
- [Пагінація](https://learn.microsoft.com/ef/core/querying/pagination)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `GetPatientsPaged` / `GetAppointmentsPaged` | `GetGuestsPaged` / `GetBookingsPaged` | `GetCustomersPaged` / `GetReservationsPaged` | `GetStudentsPaged` / `GetEnrollmentsPaged` | `GetClientsPaged` / `GetRentalsPaged` | `GetReadersPaged` / `GetLoansPaged` | `GetMembersPaged` / `GetSessionsPaged` |

### Коміт

```bash
git add ClinicApp/Data/ClinicQueryService.cs
git commit -m "Lab20 Task02"
```

---

## Задача 3. Проєкції в DTO ⭐⭐

### Умова

Замість повних об'єктів вибирайте з БД лише потрібні поля — через проєкцію `Select` у DTO.

**Що реалізувати:**

1. Створити в `ClinicApp/Models/` два `record`-и зі специфікації.
2. У `ClinicQueryService` метод `GetPatientSummaries()` — проєкція пацієнтів у `PatientSummaryDto`, кількість записів — через `p.Appointments.Count`.
3. Метод `GetAppointmentSummaries()` — проєкція записів у `AppointmentSummaryDto` з іменами пацієнта й лікаря.

### Специфікація

| DTO | Поля |
|-----|------|
| `PatientSummaryDto` | `Id`, `FullName`, `Age`, `Phone`, `BloodType` (рядок), `AppointmentCount` |
| `AppointmentSummaryDto` | `Id`, `PatientName`, `DoctorName`, `Speciality`, `Date`, `Status`, `Cost` |

| Метод | Повертає |
|-------|----------|
| `GetPatientSummaries()` | `List<PatientSummaryDto>` |
| `GetAppointmentSummaries()` | `List<AppointmentSummaryDto>` |

### Приклад

```sql
-- що генерує EF для GetPatientSummaries
SELECT p.Id, p.FirstName + N' ' + p.LastName, …,
       (SELECT COUNT(*) FROM Appointments AS a WHERE p.Id = a.PatientId)
FROM Patients AS p
```

### Підказки

1. `record` з позиційними параметрами — коротке оголошення незмінного типу даних: `public record PatientSummaryDto(int Id, string FullName, …);`.
2. Вік у проєкції достатньо порахувати як різницю років — EF перекладе це в SQL.
3. Імена пацієнта й лікаря беруться через навігаційні властивості прямо в `Select` — `Include` не потрібен.
4. Не все перекладається в SQL. Що EF не може перекласти в останньому `Select` (наприклад, `GetCost()`), він обчислює на клієнті вже після завантаження — перевірте це в лозі SQL.

📖 Документація:
- [Записи (`record`)](https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/record)
- [Обчислення на клієнті](https://learn.microsoft.com/ef/core/querying/client-eval)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `PatientSummaryDto` / `AppointmentSummaryDto` | `GuestSummaryDto` / `BookingSummaryDto` | `CustomerSummaryDto` / `ReservationSummaryDto` | `StudentSummaryDto` / `EnrollmentSummaryDto` | `ClientSummaryDto` / `RentalSummaryDto` | `ReaderSummaryDto` / `LoanSummaryDto` | `MemberSummaryDto` / `SessionSummaryDto` |

### Коміт

```bash
git add ClinicApp/Models/PatientSummaryDto.cs ClinicApp/Models/AppointmentSummaryDto.cs ClinicApp/Data/ClinicQueryService.cs
git commit -m "Lab20 Task03"
```

---

## Задача 4. М'яке видалення і глобальний фільтр ⭐⭐⭐

### Умова

Замість фізичного видалення пацієнта (`Remove`) позначайте його видаленим, а запити хай автоматично не бачать таких пацієнтів.

**Що реалізувати:**

1. У `Patient` додати властивість `IsDeleted` (`private set`) і метод `SoftDelete()`.
2. У `OnModelCreating` додати для `Patient` глобальний фільтр «не видалений».
3. У `ClinicQueryService` додати методи `SoftDeletePatient(int id)` і `GetDeletedPatients()`.
4. Створити і застосувати міграцію `AddPatientSoftDelete`.

### Специфікація

```bash
dotnet ef migrations add AddPatientSoftDelete --project ClinicApp
dotnet ef database update --project ClinicApp
```

| Член | Опис |
|------|------|
| `Patient.IsDeleted` | `bool`, `private set` |
| `Patient.SoftDelete()` | позначає пацієнта видаленим |
| `ClinicQueryService.SoftDeletePatient(int id)` | знаходить пацієнта, `SoftDelete()`, `SaveChanges()`; `bool` — чи знайдено |
| `ClinicQueryService.GetDeletedPatients()` | `List<Patient>` — лише видалені, в обхід фільтра |

### Приклад

```
SoftDeletePatient(3)                 → True
context.Patients.Count()             → 4   (пацієнт #3 не видно)
IgnoreQueryFilters().Count()         → 5
GetDeletedPatients()                 → [3] Максим Бойко
```

### Підказки

1. Після фільтра **кожен** запит до `Patients` (і `Include` пацієнта) додає `WHERE IsDeleted = 0` — писати умову вручну більше не треба.
2. Видаленого пацієнта не знайде звичайний пошук — у `SoftDeletePatient` шукайте з `IgnoreQueryFilters()`, щоб коректно обробити повторне видалення.
3. Під час міграції EF попередить, що `Patient` з фільтром — обов'язковий кінець зв'язку з `Appointment`: записи видаленого пацієнта при `Include(a => a.Patient)` матимуть `Patient == null`. Варіанти — такий самий фільтр для `Appointment`, необов'язковий зв'язок або задокументоване обмеження. Оберіть і поясніть коментарем.

📖 Документація:
- [Глобальні фільтри запитів](https://learn.microsoft.com/ef/core/querying/filters)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `Patient.IsDeleted` | `Guest.IsDeleted` | `Customer.IsDeleted` | `Student.IsDeleted` | `Client.IsDeleted` | `Reader.IsDeleted` | `Member.IsDeleted` |

### Коміт

```bash
git add ClinicApp/Models/Patient.cs ClinicApp/Data/ClinicDbContext.cs ClinicApp/Data/ClinicQueryService.cs ClinicApp/Migrations/
git commit -m "Lab20 Task04"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                                    ← гілка Lab-20 (після злиття — main)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/
    │   ├── Patient.cs                         ✏ Т4
    │   ├── AppointmentSummaryDto.cs           🆕 Т3
    │   ├── PatientSummaryDto.cs               🆕 Т3
    │   └── … ще 16 файлів без змін
    ├── Managers/  (13 файлів)
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    ├── Events/  (4 файли)
    ├── Extensions/  (3 файли)
    ├── UI/  (1 файл)
    ├── Data/
    │   ├── ClinicDbContext.cs                 ✏ Т4
    │   ├── DbSeeder.cs
    │   ├── ClinicRepository.cs
    │   └── ClinicQueryService.cs              🆕 Т1  ✏ Т2 Т3 Т4
    └── Migrations/  (9 файлів — генерує EF)   ✏ Т4
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 19.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] `DemoQueryableVsEnumerable` повертає однакові списки, але в лозі SQL лише перший спосіб містить `WHERE … LIKE`
- [ ] `GetPatientsPaged(2, 2)` повертає третього й четвертого пацієнтів за прізвищем і правильну загальну кількість
- [ ] `GetPatientSummaries()` у лозі SQL не вибирає непотрібних стовпців (`Email`, `RowVersion`)
- [ ] Після `SoftDeletePatient` пацієнт зникає зі звичайних запитів і з'являється в `GetDeletedPatients()`
- [ ] У `OnConfiguring` не лишилось `LogTo`

---

## Питання для самоперевірки

1. **Дерево виразів чи делегат.** `IQueryable` працює з деревами виразів, `IEnumerable` — з делегатами `Func<T, bool>`. Чому EF не може перекласти в SQL будь-який `Func`?
2. **Keyset-пагінація.** `Skip`/`Take` при сотнях тисяч рядків дорогий. Альтернатива — `WHERE Id > @lastId ORDER BY Id`. Коли варто на неї переходити?
3. **DTO чи ViewModel.** DTO — для передачі даних між шарами, ViewModel — для відображення. Чи є між ними різниця у вашому проєкті?
4. **`record` чи `class` для DTO.** `record` сам генерує `Equals`, `GetHashCode`, `ToString`. Чи потрібні вони DTO? Коли краще `class`?
5. **М'яке видалення й унікальність.** Якби номер ліцензії лікаря мав унікальний індекс, а лікаря видалили м'яко — новий лікар з тим самим номером не додався б. Як це вирішити?
6. **Матеріалізація посеред ланцюжка.** Чому цей код компілюється, але є проблемою продуктивності?
   ```csharp
   var result = context.Patients
       .AsNoTracking()
       .ToList()
       .GroupBy(p => p.BloodType)
       .Select(g => new { g.Key, Count = g.Count() })
       .ToList();
   ```

---

## Статус гілки

Після всіх 4 завдань (кожне — окремий коміт `Lab20 TaskNN` на гілці `Lab-20`):

```bash
git push -u origin Lab-20
git checkout main
git merge --no-ff Lab-20 -m "Merge Lab-20: EF Core Queries"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-21`.
