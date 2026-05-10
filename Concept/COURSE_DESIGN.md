# Проєкт: OOP C# Курс — Медична Клініка (еталонний домен)

## Загальна ідея

Студент будує **одну живу систему** весь курс. Кожна лаба = гілка = нова функціональність.
Еталонний домен: **Медична Клініка**.
Інструкції для студентів пишуться в **абстрактному вигляді** (Сутність A, Операція, Користувач).
Студент підставляє свій домен (готель, ресторан, аптека тощо).

---

## Домени для студентів (Лаба 00)

| Варіант | Домен | Сутність A | Сутність B | Користувач | Операція |
|---------|-------|-----------|-----------|------------|---------|
| А | Клініка | Patient | Doctor | Receptionist | Appointment |
| Б | Готель | Room | Service | Guest | Booking |
| В | Університет | Course | Subject | Student | Enrollment |
| Г | Прокат авто | Car | Brand | Client | Rental |
| Д | Ресторан | Dish | Ingredient | Waiter | Order |
| Є | Аптека | Medicine | Supplier | Customer | Sale |
| Ж | Кінотеатр | Movie | Director | Viewer | Ticket |
| З | Бібліотека | Book | Author | Member | Loan |

---

## Структура репозиторію

```
project-root/
├── sandbox/
│   ├── intro/              ← Lab 01: базовий C#, без домену
│   └── arrays/             ← Lab 02: масиви
├── src/                    ← головний проект, росте весь курс
│   ├── ClinicApp.csproj
│   ├── Clinic.cs           ← оркестратор (з'явився Lab 03)
│   ├── Program.cs          ← єдина точка входу, росте весь курс
│   ├── Enums/              ← Lab 04: BloodType, Speciality, AppointmentStatus
│   ├── Models/             ← Lab 03+: Patient, Doctor, Appointment, WorkSchedule
│   │                          Lab 06+: MedicalRecord, Diagnosis, LabResult, Prescription
│   ├── Managers/           ← Lab 03+: PatientManager, DoctorManager, AppointmentManager
│   │                          Lab 05: GrowablePatientManager
│   │                          Lab 06+: MedicalRecordManager
│   │                          Lab 07+: BillingManager (IPayable)
│   ├── Interfaces/         ← Lab 07+: IPayable, ISchedulable, ICancellable
│   ├── Utils/              ← Lab 04: ClinicFormatter; Lab 05: ClinicValidator
│   └── (майбутнє)
│       ├── Events/         ← Lab 12: EventBus
│       ├── Reports/        ← Lab 13–14: LINQ + Functional
│       └── Storage/        ← Lab 15–16: Files + JSON
├── labs/
│   ├── lab-00-choose-domain/
│   ├── lab-01-intro/
│   ├── lab-02-arrays/
│   └── ... (кожна лаба = папка з instructions.md)
└── Concept/
    ├── COURSE_DESIGN.md    ← цей файл
    ├── CODEBASE_STATE.md   ← стан src/ після кожної лаби
    ├── CONCEPTS_BY_LAB.md  ← які C# конструкції вводяться коли
    └── MENU_BY_LAB.md      ← що є в меню після кожної лаби
```

---

## Git стратегія

### Гілки
```
main                        ← завжди робочий стан
sandbox/intro               ← Lab 01 (НЕ зливається в main)
sandbox/arrays              ← Lab 02 (НЕ зливається в main)
feature/[lab-name]          ← нова функціональність
refactor/[name]             ← покращення архітектури
hotfix/[name]               ← виправлення багів
```

### Правила комітів
```
Lab01 Task1: Add basic console I/O and variables
Lab03 Task2: Add Patient class with constructor and properties
```

### Злиття в main
- ✅ Зливається: якщо в консолі з'являється нова команда або поведінка
- ⏳ Чекає: якщо зміна тільки внутрішня (рефакторинг, валідація)
- ⏳ → зливається разом з наступною лабою

---

## Таблиця лаб

| # | Гілка | Merge | Статус | Модуль | Що з'являється в консолі |
|---|-------|-------|--------|--------|--------------------------|
| 00 | — | — | ✅ | — | Вибір домену, setup |
| 01 | `sandbox/intro` | ❌ | ✅ | — | Синтаксис C#, sandbox (8 завдань) |
| 02 | `sandbox/arrays` | ❌ | ✅ | — | Масиви доменних даних, sandbox (8 завдань) |
| 03 | `feature/catalog` | ✅ | ✅ | Patients + Doctors + Appointments | Меню: 1.Пацієнти 2.Лікарі 3.Записи 4.Звіт |
| 04 | `feature/class-members` | ✅ | ✅ | Core types | Enum BloodType/Speciality у меню, статистика, розклад |
| 05 | `feature/encapsulation` | ✅ | ✅ | Patients+ | Внутрішня валідація + try/catch у меню |
| 06 | `feature/inheritance` | ✅ | ✅ | MedicalRecords | **Нове меню:** 4.Медична картка (діагнози, аналізи, рецепти) |
| 07 | `feature/interfaces` | ✅ | ✅ | Billing | **Нове меню:** 5.Рахунки (IPayable → вартість, борг, оплата) |
| 08 | `feature/polymorphism` | ⏳ | 📋 | Appointments+ | Внутрішнє покращення (типи прийомів) |
| 09 | `feature/generics` | ✅ | 📋 | Waiting | **Нове меню:** 6.Черга очікування |
| 10 | `feature/iterators` | ✅ | 📋 | всі | Меню: сортування списків (foreach, comparators) |
| 11 | `feature/reflection` | ⏳ | 📋 | Validation | Внутрішнє: авто-валідатор через рефлексію |
| 12 | `feature/events` | ✅ | 📋 | Notifications | **Нове меню:** сповіщення при записі/скасуванні |
| 13 | `feature/linq` | ✅ | 📋 | Reports | **Нове меню:** Звіти (топ лікарі, активні пацієнти) |
| 14 | `feature/functional` | ⏳ | 📋 | Reports+ | Внутрішнє покращення (чисті функції, делегати) |
| 15 | `feature/storage` | ✅ | 📋 | Storage | **Нове меню:** зберегти/завантажити стан |
| 16 | `feature/console-ui` | ✅ | 📋 | ConsoleApp | Структуроване меню, кольори, пагінація |
| 17 | `feature/ef-basic` | ✅ | 📋 | Database | БД замінила in-memory дані |
| 18 | `feature/ef-relations` | ✅ | 📋 | Database+ | Зв'язані запити в меню |
| 19 | `feature/ef-advanced` | ✅ | 📋 | Database+ | Складні зв'язки many-to-many |
| 20 | `feature/ef-querying` | ✅ | 📋 | Database+ | Фільтрація, пагінація через IQueryable |
| 21 | `refactor/solid` | ✅ | 📋 | всі | Зовні нічого, внутрішньо — SOLID рефакторинг |

---

## Деталі кожної лаби

### Lab 01 — sandbox/intro (C# Basics)
**Джерело:** Old Lab 01 (Introduction)
**Гілка:** `sandbox/intro` → НЕ зливається
**Що робить студент:** окремий проект поза src/, процедурний код
**Завдання клініки:**
- Task1: Змінні та типи. Вивести інформацію про пацієнта (ім'я string, вік int, вага double, кров'яний тиск double). Базові Console.Write/ReadLine.
- Task2: Умови. Розрахунок ІМТ (BMI). Визначити категорію (if/switch): недостатня вага/норма/зайва вага/ожиріння.
- Task3: Цикли. Розрахувати суму коштів за N візитів. Знайти найдорожчий та найдешевший прийом у масиві.
- Task4: Методи. Винести логіку Task2-3 у методи. GetBMICategory(double bmi), FormatAppointmentCost(decimal cost). Це буде основою для класів у Lab 03.

### Lab 02 — sandbox/arrays (Arrays)
**Джерело:** Old Lab 02 (Arrays)
**Гілка:** `sandbox/arrays` → НЕ зливається
**Що робить студент:** масиви рядків і чисел домену
**Завдання клініки:**
- Task1: Масив імен пацієнтів. FindByName(), CountByBloodType(), PrintAll().
- Task2: Масив візитів (дати як рядки). SortByDate(), FindOverdue(), CountByDoctor().
- Task3: Решето Ератосфена → аналог: знайти лікарів без записів (алгоритм маркування).
- Task4: 2D масив розкладу. Рядки = лікарі, стовпці = часові слоти. Знайти вільний слот.

### Lab 03 — feature/catalog (Defining Classes) ✅
**Гілка:** `feature/catalog` → ✅ злито
**Що з'явилось:** Головне меню: 1.Пацієнти 2.Лікарі 3.Записи на прийом 4.Звіт
**Нові файли:** `Patient.cs`, `Doctor.cs`, `Appointment.cs`, `PatientManager.cs`, `DoctorManager.cs`, `AppointmentManager.cs`, `Clinic.cs`, `Program.cs`
**Завдання клініки:**
- Task1: Клас `Patient` (Id, FirstName, LastName, DateOfBirth, BloodType string, Phone). Конструктори. ToString(). Масив `Patient[100]` з лічильником.
- Task2: Клас `Doctor` (Id, Name, Speciality string, LicenseNumber, Phone). `DoctorManager` з пошуком за спеціальністю.
- Task3: Клас `Appointment` (PatientId, DoctorId, ScheduledAt, Status string, Notes). `AppointmentManager`: Book, Cancel, Complete, GetByPatient, GetByDoctor.
- Task4: `Clinic` як оркестратор. `GenerateReport()`. Консольне меню з підменю для кожного розділу.

### Lab 04 — feature/class-members (Class Members) ✅
**Гілка:** `feature/class-members` → ✅ злито
**Що з'явилось:** BloodType у меню додавання пацієнта; фільтр за Speciality; статистика; розклад лікаря
**Нові файли:** `Enums/BloodType.cs`, `Enums/Speciality.cs`, `Enums/AppointmentStatus.cs`, `Models/WorkSchedule.cs`, `Utils/ClinicFormatter.cs`
**Завдання клініки:**
- Task1: `enum BloodType` (9 значень), `enum Speciality` (8 значень), `enum AppointmentStatus`. Замінити рядки в `Patient`, `Doctor`, `Appointment`.
- Task2: `struct WorkSchedule` (Start, End, IsNow, Contains()). Додати до `Doctor`. `static class ClinicFormatter` — FormatBloodType, FormatSpeciality, FormatAge.
- Task3: Індексатор `this[int]` в Manager-класах. Перевантаження методів: `FindBySpeciality(string)` і `FindBySpeciality(Speciality)`.
- Task4: `out` параметр і `TryFindById(int, out T)` патерн у PatientManager і DoctorManager.

### Lab 05 — feature/encapsulation (Encapsulation) ✅
**Гілка:** `feature/encapsulation` → ✅ злито
**Що з'явилось:** Зовні нічого — внутрішньо валідація; меню показує повідомлення про помилку замість краша
**Нові файли:** `Utils/ClinicValidator.cs`, `GrowablePatientManager.cs`; реорганізація в sub-namespaces
**Завдання клініки:**
- Task1: `private` backing fields в `Patient` (`_firstName`, `_lastName`, `_dateOfBirth`, `_phone`). Явні сеттери з `ClinicValidator.ValidateName/Phone/Date`. `throw new ArgumentException`.
- Task2: Аналогічно для `Doctor` і `WorkSchedule`. `throw new ArgumentOutOfRangeException` для числових меж.
- Task3: `Appointment.DurationMinutes` — приватне поле + `ValidatePositive`. State machine для `Status`: `Cancel()` і `Complete()` методи замість прямого присвоєння.
- Task4: `try/catch` у меню (порядок: спочатку `ArgumentOutOfRangeException`, потім `ArgumentException`). `GrowablePatientManager` — зростаючий масив через `Array.Resize`.

### Lab 06 — feature/inheritance (Inheritance) ✅
**Гілка:** `feature/inheritance` → ✅ злито
**Що з'явилось:** **Нове меню:** 4.Медична картка (зведення пацієнта, всі записи, додати діагноз/аналіз/рецепт, записи лікаря)
**Нові файли:** `Models/MedicalRecord.cs` (abstract), `Models/Diagnosis.cs`, `Models/LabResult.cs`, `Models/Prescription.cs`, `Managers/MedicalRecordManager.cs`
**Завдання клініки:**
- Task1: `abstract class MedicalRecord` (Id, PatientId, DoctorId, Date, Notes). `abstract GetSummary()`, `virtual GetRecordType()`, `virtual IsActive()`. Перший підклас `Diagnosis` (DiagnosisCode, Description, IsChronic). Валідація через `ClinicValidator`.
- Task2: `LabResult` (TestName, Value, Unit, ReferenceRange, IsNormal) і `Prescription` (MedicationName, Dosage, DurationDays, ExpiresAt). `Prescription` перевизначає `IsActive()`. `MedicalRecordManager` з `MedicalRecord[1000]`.
- Task3: Фільтрація через `is`/`as`/pattern variable: `GetDiagnoses()`, `GetLabResults()`, `GetPrescriptions()`, `GetChronicDiagnoses()`, `GetActivePrescriptions()`.
- Task4: Інтеграція в `Clinic.cs`. `MedicalRecordsMenu` в `Program.cs` з `try/catch`. `DisplayPatientSummary` — зведення по типах.

### Lab 07 — feature/interfaces (Interfaces) ✅
**Гілка:** `feature/interfaces` → ✅ зливається
**Що з'явиться:** **Нове меню:** 5.Рахунки — перегляд боргів, оплата прийому, підсумок по пацієнту
**Нові файли:** `Interfaces/IPayable.cs`, `Interfaces/ICancellable.cs`, `Interfaces/ISchedulable.cs`, `Managers/BillingManager.cs`
**Завдання клініки:**
- Task1: `interface IPayable` (decimal GetCost(), bool IsPaid, void MarkPaid()). Реалізувати в `Appointment`. `BillingManager` — збирає всі `IPayable`, рахує борг пацієнта.
- Task2: `interface ICancellable` (void Cancel(string reason), bool IsCancelled, string CancellationReason). Реалізувати в `Appointment`. Метод що приймає `ICancellable[]` — скасувати всі прострочені.
- Task3: `interface ISchedulable` (bool CanSchedule(DateTime), DateTime[] GetAvailableSlots()). Реалізувати в `Doctor`. `BillingManager.GetUnpaidByPatient(int)` — повертає `IPayable[]`.
- Task4: Меню "Рахунки": показати борги пацієнта, оплатити запис (за Id), загальна сума боргів по клініці. `try/catch`.

### Lab 08 — feature/polymorphism (Polymorphism)
**Джерело:** Old Lab 08 (Polymorphism)
**Гілка:** `feature/polymorphism` → ⏳ зливається з Lab 09
**Завдання клініки:**
- Task1: Різні типи прийомів: RegularAppointment, UrgentAppointment, SpecialistAppointment — всі успадковують від Appointment. Override методу CalculateCost() і GetDescription().
- Task2: Список Appointment (поліморфний). foreach — кожен виводить свій опис і вартість.
- Task3 (проблема): "VIP клієнти мають різні правила для кожного типу прийому. Тобто VIPPatient + UrgentAppointment = 50% знижка. Як передати «правило» у розрахунок без if?" → Студент відкриває Strategy pattern.
- Task4: "Що станеться якщо додати новий тип прийому? Скільки місць треба змінити?" → Студент аналізує і знаходить Open/Closed проблему.

### Lab 09 — feature/generics (Generics)
**Джерело:** Old Lab 09 (Generics)
**Гілка:** `feature/generics` → ✅ зливається
**Що з'являється:** Меню: черга очікування в клініці
**Завдання клініки:**
- Task1: Generic клас Repository<T> where T : MedicalEntity. Методи Add, GetById, GetAll, Remove.
- Task2: Generic клас WaitingQueue<T> (обгортка над Queue<T>). Enqueue, Dequeue, Peek, Count.
- Task3 (проблема): "Потрібна черга, де пріоритет залежить від терміновості. Urgent пацієнти мають йти першими. Як зробити без дублювання WaitingQueue?" → Generic з IComparer або Constraint: where T : IComparable<T>.
- Task4: "Repository<T> не може фільтрувати. GetAll() повертає все. Як додати Find(Predicate<T>)?" → Студент відкриває делегати/функції.

### Lab 10 — feature/iterators (Iterators & Comparators)
**Джерело:** Old Lab 10 (Iterators & Comparators)
**Гілка:** `feature/iterators` → ✅ зливається
**Що з'являється:** Меню: сортування списку пацієнтів, лікарів, прийомів за різними критеріями
**Завдання клініки:**
- Task1: IEnumerable<T> на PatientCollection. Реалізувати GetEnumerator() з yield return. Foreach по колекції.
- Task2: IComparable<Patient> (за ім'ям). IComparable<Appointment> (за датою).
- Task3: IComparer — PatientByAgeComparer, DoctorByRatingComparer. SortedSet<Doctor>.
- Task4 (проблема): "Список прийомів повинен автоматично залишатися відсортованим при додаванні нового. Але SortedSet не дозволяє дублікати. Як вирішити?" → Студент досліджує і знаходить SortedList або власну структуру.

### Lab 11 — feature/reflection (Reflection & Attributes)
**Джерело:** Old Lab 11 (Reflection & Attributes)
**Гілка:** `feature/reflection` → ⏳ зливається з Lab 12
**Завдання клініки:**
- Task1: Кастомний атрибут [Required], [MaxLength(n)], [Range(min, max)]. Застосувати до властивостей Patient і Doctor.
- Task2: Клас MedicalValidator. Метод Validate<T>(T entity) — через рефлексію знаходить всі властивості з атрибутами і перевіряє. Повертає список помилок.
- Task3 (проблема): "Валідатор треба підключити до Repository<T> щоб перевіряти перед Add(). Але Repository не знає про конкретні типи атрибутів. Як підключити?" → Validator через інтерфейс або делегат.
- Task4: "Вивести поля класу Patient через рефлексію у вигляді таблиці (назва — значення). Як зробити це для будь-якого об'єкта?" → Generic Display<T> метод.

### Lab 12 — feature/events (Events & Communication)
**Джерело:** Old Lab 12 (Communication & Events)
**Гілка:** `feature/events` → ✅ зливається
**Що з'являється:** Меню: налаштувати сповіщення. Автоматичні сповіщення при подіях (запис/скасування).
**Завдання клініки:**
- Task1: Event OnAppointmentScheduled в Appointment. EventArgs з інформацією. Підписатись (ConsoleNotifier) і вивести повідомлення.
- Task2: Event OnAppointmentCancelled. Multiple subscribers (ConsoleNotifier + Logger).
- Task3 (проблема): "Різні модулі хочуть знати про різні події. NotificationModule хоче знати про нові записи, ReportModule — про всі завершені. Як підключити без прямих залежностей між модулями?" → Студент відкриває EventBus/Mediator.
- Task4: "Що якщо сповіщень стає багато і консоль переповнена? Як зробити фільтрацію: кожен підписник отримує тільки ті події що йому потрібні?" → Предикати на підписку.

### Lab 13 — feature/linq (LINQ)
**Джерело:** Old Lab 13 (LINQ)
**Гілка:** `feature/linq` → ✅ зливається
**Що з'являється:** Меню: звіти — топ лікарі, завантаженість, статистика
**Завдання клініки:**
- Task1: LINQ запити на List<Patient>: фільтр за BloodType, вік від-до, є/немає запису.
- Task2: LINQ на Appointments: group by Doctor, OrderBy Date, Join Patient+Doctor.
- Task3: Агрегати: середній час очікування, найпопулярніша спеціальність, лікарі без пацієнтів цього місяця.
- Task4 (проблема): "Звіт займає довго бо перебирає всі записи. Як зробити щоб не завантажувати в пам'ять зайве?" → Студент відкриває IQueryable vs IEnumerable, lazy evaluation.

### Lab 14 — feature/functional (Functional Programming)
**Джерело:** Old Lab 14 (Functional Programming)
**Гілка:** `feature/functional` → ⏳ зливається з Lab 15
**Завдання клініки:**
- Task1: Action<Patient> для виводу інформації. Func<Appointment, decimal> для розрахунку вартості.
- Task2: Predicate<Patient> для фільтрів в Repository.Find(). Higher-order функція ApplyDiscount(Func<decimal, decimal> discountFn).
- Task3: Метод розширення ToClinicReport(this IEnumerable<Appointment>). Ланцюжок .Where().GroupBy().Select().
- Task4 (проблема): "Функції фільтрації часто комбінуються: пацієнти старше 60 І з серцевими хворобами І без страховки. Як скласти складний фільтр з простих без довгих if?" → Студент відкриває Predicate composition (AND, OR, NOT).

### Lab 15 — feature/storage (Streams & Files)
**Джерело:** Old Lab 15 (Streams, Files, Directories)
**Гілка:** `feature/storage` → ✅ зливається
**Що з'являється:** Меню: зберегти стан, завантажити при старті
**Завдання клініки:**
- Task1: Зберегти список пацієнтів у текстовий файл (StreamWriter). Завантажити (StreamReader). Формат CSV.
- Task2: Серіалізація/десеріалізація через System.Text.Json. Зберігати і завантажувати всі дані (пацієнти, лікарі, прийоми).
- Task3 (проблема): "При збереженні великих даних файл може бути пошкоджений якщо програма впаде. Як зробити безпечне збереження?" → Atomic write (спочатку в temp файл, потім переіменувати).
- Task4: "Треба зберігати логи дій (хто що зробив і коли). Лог не повинен видалятися при перезапуску." → Append mode, RotatingLog.

### Lab 16 — feature/console-ui (Advanced Console UI)
**Джерело:** Old Lab 16 PDFs (не зчитались — тема: розширений консольний інтерфейс)
**Гілка:** `feature/console-ui` → ✅ зливається
**Що з'являється:** Структуроване меню з розділами, кольори, форматовані таблиці
**Завдання клініки:**
- Task1: Розбити меню на секції: Patients / Doctors / Appointments / Reports. Навігація між секціями.
- Task2: Форматований вивід таблицею (Console, padding, borders). Кольорове виділення статусів.
- Task3: Пагінація при виводі великих списків (10 рядків на сторінку, ←→ для навігації).
- Task4 (проблема): "Меню стає великим. Кожен раз треба вписувати новий пункт в Program.cs. Як зробити щоб новий модуль реєстрував себе автоматично?" → Студент відкриває Command pattern або Plugin system.

### Lab 17 — feature/ef-basic (EF Code First)
**Джерело:** Old Lab 17 (EF Code First)
**Гілка:** `feature/ef-basic` → ✅ зливається
**Що з'являється:** Поведінка консолі та сама, але дані зберігаються в реальній БД
**Завдання клініки:**
- Task1: ClinicDbContext. Entities: Patient, Doctor, Appointment, Department. Migrations. DbContext замінює in-memory списки.
- Task2: Seed data. CRUD операції через EF замість файлів.
- Task3: Додати Doctor.Department зв'язок (один Department = багато Doctors). Нова міграція без втрати даних.
- Task4 (проблема): "Треба зберігати медичну картку пацієнта (MedicalRecord) — це великий текст. Чи варто зберігати в окремій таблиці? Як вплине на продуктивність?" → Студент досліджує table splitting та lazy loading.

### Lab 18 — feature/ef-relations (EF Entity Relations)
**Джерело:** Old Lab 18 (EF Entity Relations)
**Гілка:** `feature/ef-relations` → ✅ зливається
**Що з'являється:** Меню: перегляд прийомів лікаря, всіх пацієнтів відділення
**Завдання клініки:**
- Task1: One-to-Many: Department → Doctors, Doctor → Appointments, Patient → Appointments.
- Task2: Many-to-Many: Patient може мати багато Doctors (спостереження), Doctor — багато Patients. PatientDoctor junction table.
- Task3: Self-referencing: Doctor може мати "куратора" (старший лікар). Завантажити ієрархію.
- Task4 (проблема): "Appointment має і Patient, і Doctor, і Treatment. Як зробити щоб видалення Doctor не видаляло всі його Appointments? Cascade delete або soft delete?" → Студент налаштовує OnDelete behavior.

### Lab 19 — feature/ef-advanced (EF Advanced Relations)
**Джерело:** Old Lab 19 (EF Advanced Relations)
**Гілка:** `feature/ef-advanced` → ✅ зливається
**Завдання клініки:**
- Task1: Table-per-Hierarchy (TPH) для Patient: InsuredPatient, PrivatePatient в одній таблиці з Discriminator.
- Task2: Owned Entity: Address як value object всередині Patient.
- Task3: Concurrency token на Appointment (не дати двом лікарям взяти одного пацієнта одночасно).
- Task4 (проблема): "Потрібен audit log — хто і коли змінив запис. Як зробити це автоматично без коду в кожному репозиторії?" → Override SaveChanges() в DbContext.

### Lab 20 — feature/ef-querying (EF Advanced Querying)
**Джерело:** Old Lab 20 (EF Advanced Querying)
**Гілка:** `feature/ef-querying` → ✅ зливається
**Що з'являється:** Меню: складні звіти з фільтрами, пагінацією, сортуванням
**Завдання клініки:**
- Task1: IQueryable<T> фільтрація: пацієнти за BloodType, Appointments за DateRange + DoctorId.
- Task2: Projection: вивести тільки Name + NextAppointmentDate (не завантажувати весь об'єкт).
- Task3: Grouping + Aggregation: скільки прийомів на день, середня тривалість, завантаженість лікаря по днях тижня.
- Task4 (проблема): "Пагінація через Skip().Take() повільна на великих таблицях. Як зробити cursor-based pagination?" → Студент досліджує keyset pagination.

### Lab 21 — refactor/solid (SOLID Principles)
**Джерело:** Old Lab 21 (SOLID)
**Гілка:** `refactor/solid` → ✅ зливається
**Що з'являється:** Зовні нічого не змінилось. Внутрішньо — чиста архітектура.
**Завдання клініки:**
- Task1 (SRP): Виявити класи що роблять надто багато. Розділити AppointmentService на: SchedulingService, BillingService, NotificationService.
- Task2 (OCP/LSP): Перевірити ієрархію Doctor і Patient. Чи можна підставити будь-який підклас? Виправити порушення.
- Task3 (ISP): Великий інтерфейс IClinicService розбити на маленькі: IPatientService, IDoctorService, IAppointmentService.
- Task4 (DIP): CourseService залежить від конкретних класів. Ввести DI через конструктор. Налаштувати DI контейнер в Program.cs.

---

## Структура instructions.md (шаблон)

```markdown
# Лаба NN — [Назва теми]

## Мета
Одне речення: що студент навчиться робити.

## Контекст
Що вже є в системі. Яку нову проблему вирішує ця лаба.

## Гілка
git checkout main && git pull && git checkout -b feature/[назва]

## Завдання 1 — [назва] (обов'язкове) ⭐
[Конкретний опис. Без підказки рішення.]
**Коміт:** "LabNN Task1: [опис]"

## Завдання 2 — [назва] (обов'язкове) ⭐⭐
[Розширення Task1. Взаємодія з існуючим кодом.]
**Коміт:** "LabNN Task2: [опис]"

## Завдання 3 — [назва] (бажане) ⭐⭐⭐
[Формулюється як проблема! НЕ вказує рішення.]
**Коміт:** "LabNN Task3: [опис]"

## Завдання 4 — [назва] (бонус) ⭐⭐⭐⭐
[Відкрите питання. Студент знаходить підхід сам.]
**Коміт:** "LabNN Task4: [опис]"

## Злиття (якщо ✅)
git checkout main && git merge feature/[назва] && git push

## Що з'явиться в консолі
[Конкретний опис нової поведінки.]

## Питання для самоперевірки
- Питання 1
- Питання 2
- Питання 3
```

---

## Абстрактна термінологія для інструкцій

| Клініка | Загальний вигляд |
|---------|-----------------|
| Patient | Сутність A |
| Doctor | Сутність B |
| Receptionist | Користувач |
| Appointment | Операція |
| Department | Категорія |
| Treatment | Деталь операції |
| MedicalRecord | Документ |
| ClinicDbContext | DbContext / Контекст даних |

---

## Поточний стан

**Завершено:** Lab 00–07 ✅
**Наступний крок:** Lab 08 — `feature/polymorphism` — Polymorphism (⏳ чекає Lab 09)

**Порядок роботи:**
1. Реалізувати еталонний код на C# (домен: Клініка) на новій гілці
2. Написати `labs/lab-NN-назва/instructions.md` в абстрактному вигляді
3. Оновити `Concept/CODEBASE_STATE.md`, `Concept/CONCEPTS_BY_LAB.md`, `Concept/MENU_BY_LAB.md`
4. Злити в `main`, запушити

**Головне меню після Lab 07:**
```
1. Пацієнти       — реєстрація, пошук
2. Лікарі         — персонал, розклад
3. Записи         — прийоми, скасування
4. Медична картка — діагнози, рецепти
5. Рахунки        — оплата, борги
6. Звіт           — загальна статистика
```
