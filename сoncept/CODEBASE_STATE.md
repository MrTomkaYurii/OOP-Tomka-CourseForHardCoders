# Стан кодобази: що є після кожної лаби

Цей файл відстежує що конкретно живе в `src/` (і `sandbox/`) після кожної лаби.
Оновлюй після завершення кожної лаби.

---

## Lab 00 — Вибір домену

**Статус:** ✅ концептуально (не потребує коду)
**Гілка:** немає
**Файли:** тільки `.gitignore`, `COURSE_DESIGN.md`
**Меню:** немає

---

## Lab 01 — C# Basics (sandbox/intro)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `sandbox/intro` — НЕ зливається
**Файли:**
```
sandbox/intro/
├── ClinicIntro.csproj
├── Program.cs          ← Task1.Run() → Task2.Run() → ... → Task8.Run()
├── Task1.cs            ⭐   ІМТ пацієнта (double, формула, F2)
├── Task2.cs            ⭐   Вартість прийому зі знижкою
├── Task3.cs            ⭐   Вік та категорія пацієнта (if/else)
├── Task4.cs            ⭐⭐  Артеріальний тиск (складні умови, ||)
├── Task5.cs            ⭐⭐  Розклад клініки (switch expression)
├── Task6.cs            ⭐⭐  Аналіз номера картки (%, ?:)
├── Task7.cs            ⭐⭐⭐ Статистика прийомів (for/foreach/while, масив)
└── Task8.cs            ⭐⭐⭐ Методи (рефакторинг Task1-4 у static методи)
```

**Що є в системі:** нічого (лише ізольовані процедурні вправи)
**Методи з Task8, які стануть методами класів у Lab03:**
- `CalculateBMI()` → `Patient.GetBMI()`
- `GetBMICategory()` → `Patient.GetBMIStatus()`
- `CalculateCost()` → `Appointment.GetCost()`
- `GetAgeCategory()` → `Patient.GetAgeCategory()`

---

## Lab 02 — Arrays (sandbox/arrays)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `sandbox/arrays` — НЕ зливається
**Файли:**
```
sandbox/arrays/
├── SandboxArrays.csproj
├── Program.cs          ← Task1.Run() → ... → Task8.Run()
├── Task1.cs            ⭐   Ваги пацієнтів (1D array, статистика)
├── Task2.cs            ⭐   Bubble sort вартостей прийомів
├── Task3.cs            ⭐⭐  Тижневий графік (фіксований масив + назви)
├── Task4.cs            ⭐⭐  Матриця прийомів лікарів (2D int[,])
├── Task5.cs            ⭐⭐  Квадратна матриця — діагоналі
├── Task6.cs            ⭐⭐⭐ Рваний масив — прийоми лікарів (int[][])
├── Task7.cs            ⭐⭐⭐ Паралельні масиви — рейтинг ІМТ
└── Task8.cs            ⭐⭐⭐ 3D масив — відділення × тижні × зміни
```

**Що є в системі:** нічого (ізольовані вправи з масивами)
**Підготовлено для Lab03:** розуміння масивів об'єктів (`Patient[] patients`)

---

## Lab 03 — Defining Classes (feature/catalog)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/catalog` — ✅ **злито в main**
**Файли:**
```
src/
├── ClinicApp.csproj
├── Patient.cs              ← Task 1: клас Patient
├── Doctor.cs               ← Task 2: клас Doctor
├── PatientManager.cs       ← Task 3: CRUD + пошук (масив Patient[100])
├── DoctorManager.cs        ← Task 4: CRUD + пошук (масив Doctor[50])
├── Appointment.cs          ← Task 5: клас Appointment (статус-машина)
├── AppointmentManager.cs   ← Task 6: управління записами (масив)
├── Clinic.cs               ← Task 7: оркестратор + звіт
└── Program.cs              ← Task 7: консольне меню
```

**Що є в пам'яті:**
- `Patient[100]` з `_count` — лінійний пошук за ім'ям та ID
- `Doctor[50]` з `_count` — лінійний пошук за спеціальністю
- `Appointment[500]` з `_count` — лінійний пошук, фільтр за датою

**Можливості меню після Lab03:**
```
╔══════════════════════════════╗
║     МЕДИЧНА КЛІНІКА          ║
╠══════════════════════════════╣
║  1. Пацієнти                 ║   → показати / додати / знайти / видалити / статистика
║  2. Лікарі                   ║   → показати / додати / знайти за спец. / статистика
║  3. Записи на прийом         ║   → записати / скасувати / завершити
║  4. Звіт                     ║   → загальна кількість
║  0. Вийти                    ║
╚══════════════════════════════╝
```

**Навмисні обмеження (мотивують наступні лаби):**
- Фіксований розмір масивів → `List<T>` в Lab09 (Generics)
- Лінійний пошук O(n) → `Dictionary` в Lab09
- Немає валідації полів → Lab05 Encapsulation
- Медичні записи (MedicalRecord) відсутні → Lab06 Inheritance

**Концепції введені в Lab03:**
- `class`, `static int _nextId`, `const int MaxCapacity`
- `public`, `private` поля
- Авто-властивості `{ get; set; }`, `{ get; }`, `{ get; private set; }`
- Обчислювані властивості (`get only`)
- Конструктори, ланцюжок `: this(...)`
- `override ToString()`
- Методи екземпляра
- `null`, `if (x == null)`, `if (x != null)`
- Масив об'єктів з ручним лічильником

---

## Lab 04 — Члени класу (feature/class-members)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/class-members` — ✅ **злито в main**
**Файли:**
```
src/
├── BloodType.cs            ← enum BloodType (9 значень)
├── Speciality.cs           ← enum Speciality (8 значень)
├── AppointmentStatus.cs    ← enum AppointmentStatus (3 значення)
├── WorkSchedule.cs         ← struct WorkSchedule { Start, End, IsNow, Contains() }
├── ClinicFormatter.cs      ← static class — FormatBloodType, FormatSpeciality, FormatAge, FormatPhone
├── Patient.cs              ← використовує BloodType enum та ClinicFormatter
├── Doctor.cs               ← використовує Speciality + WorkSchedule, IsAvailableNow
├── Appointment.cs          ← використовує AppointmentStatus enum
├── PatientManager.cs       ← + indexer this[int], + TryFindById(out), + FindByBloodType
├── DoctorManager.cs        ← + indexer, + FindBySpeciality(Speciality) overload, + TryFindById(out)
├── AppointmentManager.cs   ← + indexer, + GetByDate(int,int,int) overload
└── Program.cs              ← cast (BloodType)num, (Speciality)num у меню
```

**Нові концепції в Lab 04:**
- `enum` — BloodType, Speciality, AppointmentStatus
- `struct` — WorkSchedule (value type, immutable fields)
- `static class` — ClinicFormatter (утиліти без інстанцій)
- Індексатор `this[int index]` в Manager-класах
- Перевантаження методів (`FindBySpeciality(string)` / `FindBySpeciality(Speciality)`)
- `out` параметр і TryXxx патерн (`TryFindById`)
- `?.` null-conditional та `??` null-coalescing (тепер дозволено)
- `(TypeName)value` — явне приведення int → enum

---

## Lab 05 — Encapsulation (feature/encapsulation)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/encapsulation` — ✅ **злито в main**
**Файли:**
```
src/
├── Clinic.cs                        ← without changes to API
├── GrowablePatientManager.cs        ← + using ClinicApp.Models
├── Program.cs                       ← + using ClinicApp.*; try/catch у меню
├── Enums/
│   ├── AppointmentStatus.cs         ← namespace ClinicApp.Enums (moved)
│   ├── BloodType.cs
│   └── Speciality.cs
├── Managers/
│   ├── AppointmentManager.cs        ← namespace ClinicApp.Managers (moved)
│   ├── DoctorManager.cs
│   └── PatientManager.cs
├── Models/
│   ├── Appointment.cs               ← namespace ClinicApp.Models; _durationMinutes + validate
│   ├── Doctor.cs                    ← private _firstName, _lastName, _licenseNumber, _phone
│   ├── Patient.cs                   ← private _firstName, _lastName, _dateOfBirth, _phone
│   └── WorkSchedule.cs              ← validates start/end in constructor
└── Utils/
    ├── ClinicFormatter.cs           ← namespace ClinicApp.Utils (moved)
    └── ClinicValidator.cs           ← NEW: static ValidateName/Phone/Date/Positive
```

**Нові концепції в Lab 05:**
- Sub-namespaces: `ClinicApp.Models`, `ClinicApp.Enums`, `ClinicApp.Managers`, `ClinicApp.Utils`
- `using` директиви для залежностей між підпросторами
- `private` backing fields: `_camelCase`
- Явні сеттери з валідацією
- `throw new ArgumentException(msg)`
- `throw new ArgumentOutOfRangeException(paramName, msg)`
- `string.IsNullOrWhiteSpace()`
- `nameof(Property)`
- `try / catch` (порядок: спочатку конкретніший тип)
- Опційно: `Regex.IsMatch()` для перевірки формату

**Що НЕ змінилось:** меню, API менеджерів, зовнішня поведінка

---

## Lab 06 — Inheritance (feature/inheritance)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/inheritance` — ✅ **злито в main**
**Файли:**
```
src/
├── Models/
│   ├── MedicalRecord.cs    ← abstract: Id, PatientId, DoctorId, Date, Notes
│   │                          abstract GetSummary(); virtual GetRecordType(); virtual IsActive()
│   ├── Diagnosis.cs        ← DiagnosisCode, Description, IsChronic
│   ├── LabResult.cs        ← TestName, Value, Unit, ReferenceRange, IsNormal
│   └── Prescription.cs     ← MedicationName, Dosage, DurationDays, ExpiresAt; override IsActive()
└── Managers/
    └── MedicalRecordManager.cs  ← MedicalRecord[1000] поліморфний масив
                                    GetDiagnoses/LabResults/Prescriptions/ChronicDiagnoses/ActivePrescriptions
                                    DisplayPatientSummary
```

**Нові концепції в Lab 06:**
- `abstract class` — не можна інстанціювати напряму
- `abstract` метод — підклас зобов'язаний реалізувати
- `virtual` метод — підклас може перевизначити
- `: BaseClass`, `base(...)` в конструкторі
- `override` в підкласах
- `protected` конструктор
- `is`, `as`, pattern variable `is T var`
- Поліморфний масив `MedicalRecord[]`

**Нове в меню:** пункт 4 "Медична картка" → зведення / всі записи / додати діагноз/аналіз/рецепт / записи лікаря

---

## Lab 07 — Interfaces (feature/interfaces)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/interfaces` — ✅ злито в main

**Нові файли:**
```
src/
├── Interfaces/
│   ├── IPayable.cs         ← decimal GetCost(); bool IsPaid; void MarkPaid()
│   ├── ICancellable.cs     ← bool IsCancelled; string CancellationReason; bool Cancel(string)
│   └── ISchedulable.cs     ← bool CanSchedule(DateTime); DateTime[] GetAvailableSlots(DateTime, int)
└── Managers/
    └── BillingManager.cs   ← GetAllUnpaid, GetUnpaidByPatient, GetTotalDebt, GetPatientDebt, PayAppointment, DisplayUnpaid
```

**Зміни в існуючих файлах:**
- `Models/Appointment.cs` — `class Appointment : IPayable, ICancellable`; додано `_isPaid`, `GetCost()`, `IsPaid`, `MarkPaid()`, `IsCancelled`, `CancellationReason`
- `Models/Doctor.cs` — `class Doctor : ISchedulable`; додано `CanSchedule(DateTime)`, `GetAvailableSlots(DateTime, int)`
- `Managers/AppointmentManager.cs` — додано `GetAll()`
- `Clinic.cs` — додано `public BillingManager Billing { get; }`
- `Program.cs` — головне меню з описами через дефіс; додано `BillingMenu` (пункт 5)

**Нові концепції:**
- `interface` із методами та властивостями
- Клас реалізує кілька інтерфейсів: `class Appointment : IPayable, ICancellable`
- Інтерфейс як тип параметра: `void DisplayUnpaid(IPayable[] items)`
- `is Appointment a` — перевірка на тип через базове посилання

**Нове в меню:** пункт 5 "Рахунки" → борги пацієнта, оплата запису, загальна сума боргів

---

## Lab 08 — Polymorphism (feature/polymorphism)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/polymorphism` — ✅ злито в main

**Нові файли:**
```
src/Models/
├── RegularAppointment.cs   ← override GetDescription() → "Звичайний прийом"
├── UrgentAppointment.cs    ← UrgencyNote; override GetCost() * 1.5m; sealed override GetDescription(); new GetPriority() => 1
└── SpecialistAppointment.cs← sealed class; ConsultationTopic; override GetCost() * 1.3m; override GetDescription()
```

**Зміни в існуючих файлах:**
- `Models/Appointment.cs` — `GetCost()` та `GetDescription()` стали `virtual`; додано `GetPriority() => 3` (не virtual — для демо `new`); оновлено `ToString()` через `GetDescription()` і `GetCost()`
- `Managers/AppointmentManager.cs` — `Book()` тепер створює `RegularAppointment`; додано `BookUrgent()` і `BookSpecialist()`
- `Program.cs` — seed data оновлено: `BookUrgent(2, 2, ...)`, `BookSpecialist(3, 3, ...)`; демо `new` vs `override` при старті

**Нові концепції:**
- `virtual` метод у базовому класі
- `override` у підкласах — справжній поліморфізм
- `new` — приховування методу (НЕ поліморфізм)
- `sealed class` — `SpecialistAppointment` не можна успадкувати
- `sealed override` — `UrgentAppointment.GetDescription()` не можна перевизначити далі
- `base.GetCost()` — виклик реалізації батька в override

**Меню не змінюється** — всі зміни внутрішні

---

## Lab 09 — Generics (feature/generics)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/generics` — ✅ злито в main
**Файли:**
```
src/
├── Models/
│   └── WaitingQueue.cs          ← NEW: generic WaitingQueue<T> над Queue<T>
├── Interfaces/
│   └── IIdentifiable.cs         ← NEW: interface IIdentifiable { int Id { get; } }
└── Managers/
    ├── PatientManager.cs        ← List<Patient> замість Patient[] + _count
    └── Repository.cs            ← NEW: Repository<T> where T : IIdentifiable
```

**Зміни в існуючих файлах:**
- `Models/Patient.cs` — `class Patient : IIdentifiable`
- `Models/Doctor.cs` — `class Doctor : ISchedulable, IIdentifiable`
- `Models/Appointment.cs` — `class Appointment : IPayable, ICancellable, IIdentifiable`
- `Clinic.cs` — `public WaitingQueue<Patient> WaitingRoom { get; }` + ініціалізація
- `Program.cs` — пункт "6. Черга — очікування, прийом" (Звіт переміщено з 6 на 7), `WaitingRoomMenu()`

**Нові концепції в Lab 09:**
- `List<T>` — динамічний список замість `T[]` + ручний лічильник
- Generic клас `class WaitingQueue<T>` — параметр типу без constraint
- `Queue<T>` — FIFO колекція зі стандартної бібліотеки
- Generic constraint `where T : IIdentifiable` — обмеження типу через інтерфейс
- `default!` — повернення default значення типу в generic методі
- `InvalidOperationException` — кидається при `Dequeue`/`Peek` на порожній черзі

**Нове в меню:** пункт 6 "Черга — очікування, прийом" → додати до черги, прийняти першого, хто перший, переглянути чергу

---

## Lab 10 — Iterators & Comparators (feature/iterators)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/iterators` — ✅ зливається
**Файли:**
```
src/
├── Models/
│   ├── DoctorStats.cs           ← NEW: IComparable<DoctorStats> (за AppointmentCount desc)
│   └── PatientStats.cs          ← NEW: IComparable<PatientStats> (за VisitCount desc)
├── Comparators/
│   ├── DoctorStatsByRevenue.cs  ← NEW: IComparer<DoctorStats> (за TotalRevenue desc)
│   ├── DoctorStatsByName.cs     ← NEW: IComparer<DoctorStats> (за FullName asc)
│   ├── PatientStatsBySpent.cs   ← NEW: IComparer<PatientStats> (за TotalSpent desc)
│   └── PatientStatsByLastVisit.cs← NEW: IComparer<PatientStats> (за LastVisitDate desc)
└── Managers/
    └── AnalyticsManager.cs      ← NEW: IEnumerable<DoctorStats/PatientStats> з yield return
```

**Зміни в існуючих файлах:**
- `Clinic.cs` — `public AnalyticsManager Analytics { get; }` + ініціалізація
- `Program.cs` — "8. Аналітика", `AnalyticsMenu()`, `CollectDoctorStats()`, `CollectPatientStats()`

**Нові концепції в Lab 10:**
- `IComparable<T>` — природній порядок, реалізується в самому класі; `Array.Sort()` / `List.Sort()`
- `IComparer<T>` — зовнішній компаратор, окремий клас для одного критерію; `List.Sort(comparer)`
- `IEnumerable<T>` як тип повернення методу
- `yield return` — ліниве обчислення: state machine, обчислення по запиту
- `foreach` по `IEnumerable<T>` для споживання ітератора

**Нове в меню:** пункт 8 "Аналітика" → 5 варіантів рейтингів (лікарі та пацієнти за різними критеріями)

---

## Lab 11 — Reflection & Attributes (feature/reflection)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/reflection` — ✅ зливається
**Файли:**
```
src/
├── Attributes/
│   ├── RequiredAttribute.cs     ← NEW: власний атрибут [Required]
│   ├── MaxLengthAttribute.cs    ← NEW: власний атрибут [MaxLength(n)]
│   └── MinValueAttribute.cs     ← NEW: власний атрибут [MinValue(n)]
├── Enums/
│   └── TreatmentStatus.cs       ← NEW: Planned/Active/Completed/Cancelled
├── Models/
│   └── TreatmentPlan.cs         ← NEW: модель із атрибутами на властивостях
├── Utils/
│   ├── ValidationResult.cs      ← NEW: контейнер помилок валідації
│   ├── ModelValidator.cs        ← NEW: static Validate(object), PrintInfo(Type)
│   └── FormBuilder.cs           ← NEW: static Build<T>() where T : new()
└── Managers/
    └── TreatmentPlanManager.cs  ← NEW: CRUD + валідація через ModelValidator
```

**Зміни в існуючих файлах:**
- `Clinic.cs` — `public TreatmentPlanManager TreatmentPlans { get; }` + ініціалізація
- `Program.cs` — "9. Плани лікування", `TreatmentPlansMenu()`

**Нові концепції в Lab 11:**
- `sealed class XxxAttribute : Attribute` — власний атрибут з нуля
- `[AttributeUsage(AttributeTargets.Property, AllowMultiple = false)]`
- `typeof(T)` vs `obj.GetType()` — статичний vs динамічний тип
- `Type.GetProperties()` → `PropertyInfo[]`
- `prop.GetValue(obj)` / `prop.SetValue(obj, value)` — читання/запис через рефлексію
- `prop.GetCustomAttribute<T>()` — атрибути конкретного типу
- `where T : new()` — constraint на наявність публічного конструктора без параметрів
- `Convert.ChangeType(value, targetType)` — конверсія без знання типу на час компіляції

**Нове в меню:** пункт 9 "Плани лікування" → 7 підпунктів (включно з PrintInfo через рефлексію)

---

## Lab 12 — File I/O (feature/files)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/files` — ✅ зливається
**Файли:**
```
src/
└── Utils/
    ├── ClinicLogger.cs      ← NEW: File.AppendAllText, ReadAllLines, GetLastLines(n)
    ├── ImportResult.cs      ← NEW: контейнер результатів імпорту (Imported/Skipped/Errors)
    ├── ClinicExporter.cs    ← NEW: StreamWriter, Path.Combine, Directory.CreateDirectory
    ├── CsvImporter.cs       ← NEW: CSV-парсинг з try/catch per-line, повертає ImportResult
    └── SessionManager.cs    ← NEW: Save/Load у session.dat, секційний формат [PATIENTS]
```

**Зміни в існуючих файлах:**
- `Clinic.cs` — `Logger`, `Exporter`, `Importer`, `Session` властивості
- `Program.cs` — завантаження сесії на старті, збереження при виході, `FilesMenu()`, пункт "10. Файли"

**Нові концепції в Lab 12:**
- `File.AppendAllText(path, text, encoding)` — дописати в кінець
- `File.ReadAllLines(path, encoding)` — зчитати у `string[]`
- `File.WriteAllText`, `File.Exists`, `File.Delete`
- `StreamWriter(path, append, encoding)` + `using` — потік з гарантованим закриттям
- `Directory.CreateDirectory(path)` — створює теки рекурсивно, не кидає якщо існує
- `Path.Combine(...)` — платформо-незалежне з'єднання частин шляху
- `Encoding.UTF8` — для кирилиці обов'язково
- `Environment.NewLine` — правильний перенос рядка
- `try/catch` per-line у CSV-парсингу — помилка в рядку не зупиняє решту
- Секційний текстовий формат `[SECTION]` — простий спосіб зберігати різнотипні дані

**Нове в меню:** пункт 10 "Файли", вихід з пропозицією збереження сесії

---

## Lab 13 — Events & Delegates (feature/events)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/events` — ✅ зливається
**Файли:**
```
src/
├── Events/
│   ├── AppointmentEventArgs.cs  ← NEW: Id, PatientId, DoctorId, ScheduledAt, Notes
│   ├── PatientEventArgs.cs      ← NEW: PatientId, FullName
│   ├── PaymentEventArgs.cs      ← NEW: AppointmentId, Amount
│   └── TreatmentPlanEventArgs.cs← NEW: PlanId, PatientId, Diagnosis
└── Utils/
    ├── PatientPassportWriter.cs ← NEW: генерує patients/passport_{id}.txt за подіями
    └── SessionEventTracker.cs   ← NEW: рахує події, реагує на чергу, session_summary.txt
```

**Зміни в існуючих файлах:**
- `AppointmentManager` — `AppointmentBooked`, `AppointmentCancelled`, `AppointmentCompleted`, `UrgentAppointmentBooked`
- `PatientManager` — `PatientAdded`
- `BillingManager` — `PaymentReceived`
- `TreatmentPlanManager` — `PlanCompleted` + методи `Activate(id)`, `Complete(id)`, `Cancel(id)`
- `ClinicLogger` — обробники `OnPatientAdded`, `OnAppointmentBooked/Cancelled/Completed`, `OnUrgentBooked` (+ alerts/), `OnPaymentReceived`, `OnPlanCompleted`
- `Clinic.cs` — `Passport`, `Tracker` властивості + `SubscribeEvents()`
- `Program.cs` — Task1 handler, `Tracker.PrintSummary/SaveSummary` при виході

**Нові концепції в Lab 13:**
- `class XxxEventArgs : EventArgs` — власні аргументи події
- `event EventHandler<T>?` — оголошення події в класі
- `?.Invoke(sender, args)` — безпечне підняття події
- `+=` / `-=` — підписка / відписка
- Множинні підписники на одну подію — спрацьовують всі незалежно
- `event` vs `delegate` поле — заборона `=` ззовні
- Cross-domain реакція через обробник (WaitingRoom в SessionEventTracker)

**Що з'являється:** Logger тепер пише автоматично; паспорти в `patients/`; алерти в `alerts/`; підсумок `session_summary.txt` при виході

---

## Lab 14 — LINQ (feature/linq)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/linq` — ✅ злито в main
**Файли:**
```
src/
├── Models/
│   └── SpecialityReport.cs      ← NEW: DTO — спеціальність, кількість лікарів, прийомів, виручка
└── Managers/
    ├── AnalyticsManager.cs      ← REWRITE: for-цикли → LINQ (.Select/.Where/.Count/.Sum/.Max/.Any)
    └── ReportManager.cs         ← NEW: 7 LINQ-звітів (GroupBy, Join, OrderBy+Take, Any, Distinct, місяць)
```

**Зміни в існуючих файлах:**
- `Clinic.cs` — `public ReportManager Reports { get; }` + ініціалізація
- `Program.cs` — пункт "11. Звіти — LINQ-аналітика", `ReportsMenu()`

**Нові концепції в Lab 14:**
- `.Where(predicate)`, `.Select(selector)` — фільтрація та проєкція
- `.Count()`, `.Sum()`, `.Max()`, `.Any()` — агрегати
- `.OrderBy()`, `.OrderByDescending()`, `.ThenBy()` — сортування
- `.GroupBy(key)` — групування за ключем
- `.Join(...)` — з'єднання двох колекцій
- `.FirstOrDefault()` — перший або null
- `.Take(n)` — взяти перші N елементів
- `.Distinct()` — унікальні значення
- Анонімний тип у `GroupBy`: `new { a.Year, a.Month }`
- Value tuple як тип повернення: `(int Year, int Month, decimal Total)`

**Нові методи ReportManager:**

| Метод | LINQ-оператори | Результат |
|-------|----------------|-----------|
| `GetSpecialityStats()` | `GroupBy` + `Select` + `Contains` + `OrderByDescending` | статистика по спеціальностях |
| `FindBusiestDoctorName()` | `OrderByDescending` + `Select` + `FirstOrDefault` | ім'я найзайнятішого лікаря |
| `GetPatientsWithMultipleVisits(n)` | `GroupBy` + `Where` + `Join` | імена пацієнтів з N+ візитами |
| `GetTopEarners(n)` | `Select` + `OrderByDescending` + `Take` | топ-N лікарів за виручкою |
| `HasAnyUrgentAppointments()` | `Any` + `is` | чи є термінові записи |
| `GetActiveSpecialities()` | `Select` + `Distinct` + `OrderBy` | унікальні спеціальності |
| `GetMonthlyRevenue()` | `GroupBy` (анонімний тип) + `Select` (tuple) + `OrderBy` + `ThenBy` | виручка по місяцях |

**Нове в меню:** пункт 11 "Звіти — LINQ-аналітика" → 7 підпунктів

---

## Lab 15 — Functional C# (feature/functional)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/functional` — ✅ злито в main
**Файли:**
```
src/
├── Extensions/                      ← НОВА ПАПКА
│   ├── AppointmentExtensions.cs     ← NEW: .Unpaid() .Upcoming() .ByDoctor() .Overdue() .CostAbove() .TotalCost()
│   ├── PatientExtensions.cs         ← NEW: .Adults() .ByBloodType() .WithAppointments()
│   └── DoctorExtensions.cs          ← NEW: .BySpeciality() .Available() .WithAppointments()
└── Managers/
    ├── AppointmentFilter.cs         ← NEW: Func<Appointment,bool> — Add/And/Or/Negate/Apply
    ├── AppointmentProcessor.cs      ← NEW: Action<Appointment> — Run/RunIf/Combine/Execute
    └── AppointmentPipeline.cs       ← NEW: фасад Filter+Processor, fluent Filter().Then().Execute()
```

**Зміни в існуючих файлах:**
- `Clinic.cs` — `public AppointmentPipeline Pipeline { get; }` + ініціалізація
- `Program.cs` — `using ClinicApp.Extensions;`, пункт "12. Фільтри", `FunctionalMenu()`

**Нові концепції в Lab 15:**
- `Func<T, TResult>` — тип для лямбди що повертає значення; зберігається у змінній/полі
- `Action<T>` — тип для лямбди без повернення; зберігається у `List<Action<T>>`
- Замикання (closure) — лямбда захоплює локальну змінну (`minCost`, `prev`)
- `var prev = _combined` — фіксація стану при комбінуванні предикатів
- Методи розширення — `static` метод з `this T source` → `source.MyMethod()`
- `public static class` — обов'язкова умова для extension methods
- Fluent interface — кожен метод повертає `this` для ланцюга викликів
- Higher-order методи — `RunIf(Func<> predicate, Action<> action)` — обидва як параметри

**Нове в меню:** пункт 12 "Фільтри — Func, Action, Pipeline" → 8 підпунктів

---

## Lab 16 — Console UI — Spectre.Console (feature/console-ui)

**Статус:** ✅ ЗАВЕРШЕНО
**Гілка:** `feature/console-ui` — ✅ злито в main
**Файли:**
```
src/
└── UI/
    └── ClinicRenderer.cs   ← NEW: статичний UI-фасад над Spectre.Console
```

**Зміни в існуючих файлах:**
- `ClinicApp.csproj` — `<PackageReference Include="Spectre.Console" Version="0.55.2"/>`
- `Program.cs` — всі меню через `SelectionPrompt`, списки через `Table`, введення через `TextPrompt`, картки через `Panel`, медкартка через `Tree`, повідомлення кольорові

**ClinicRenderer — публічне API:**

| Група | Методи |
|-------|--------|
| Текст | `PrintHeader`, `PrintSuccess`, `PrintError`, `PrintWarning`, `PrintInfo` |
| Меню | `SelectMenu(title, options[])` → SelectionPrompt |
| Введення | `PromptInt`, `PromptString`, `PromptDecimal`, `PromptConfirm`, `PromptDate`, `PromptDateTime` |
| Таблиці | `RenderPatients`, `RenderDoctors`, `RenderAppointments` |
| Картки | `RenderPatientCard`, `RenderDoctorCard` |
| Ієрархія | `RenderMedicalRecord` (Tree з гілками Діагнози/Аналізи/Рецепти) |
| Звіти | `RenderSpecialityStats` (Table), `RenderMonthlyRevenue` (BarChart) |
| Утиліти | `WithSpinner(msg, action)` — Status spinner |

**Нові концепції в Lab 16:**
- NuGet-пакети: `dotnet add package`, `<PackageReference>` у `.csproj`
- `using Spectre.Console;` — підключення зовнішньої бібліотеки
- `AnsiConsole.MarkupLine("[color]text[/]")` — ANSI-розмітка з кольорами
- `Markup.Escape(text)` — захист від markup injection
- `new Rule(...)` — горизонтальний роздільник
- `new Table().AddColumn().AddRow()` — таблиця з рамкою
- `new SelectionPrompt<string>().AddChoices(...)` — меню зі стрілками
- `new TextPrompt<T>()` з авто-валідацією і повторним запитом
- `new ConfirmationPrompt(...)` — запит так/ні
- `new Panel(content)` з `PanelHeader` і `BoxBorder` — рамка навколо тексту
- `new Tree(root).AddNode(branch).AddNode(leaf)` — ієрархічне відображення
- `new BarChart().AddItem(label, value, color)` — стовпчаста діаграма
- `AnsiConsole.Status().Spinner(Known.Dots).Start(msg, ctx => {...})` — спіннер
- Фасад-патерн: `ClinicRenderer` ховає Spectre.Console від `Program.cs`
- SRP: `Program.cs` = "що"; `ClinicRenderer` = "як"

**Нове в меню:** меню тепер навігуються стрілками (SelectionPrompt). Новий пункт "← Назад" замість "0. Вийти". Медична картка показується як Tree.

---

## Lab 17 — EF Core Basic (feature/ef-core)

**Статус:** 🔄 В РОБОТІ
**Гілка:** `feature/ef-core` — НЕ злито (зливається тільки після Lab 20)
**Файли:**
```
src/
├── Data/
│   ├── ClinicDbContext.cs   ← NEW: DbContext з DbSet<Patient>, DbSet<Doctor>
│   └── DbSeeder.cs          ← NEW: ідемпотентне наповнення 5 пацієнтів + 5 лікарів
├── Migrations/              ← NEW: auto-generated EF Core
│   ├── 20260515215137_InitialCreate.cs
│   ├── 20260515215137_InitialCreate.Designer.cs
│   └── ClinicDbContextModelSnapshot.cs
├── Models/
│   ├── Patient.cs           ← UPD: Id { get; private set; } для EF Core
│   └── Doctor.cs            ← UPD: Id { get; private set; } для EF Core
└── ClinicApp.csproj         ← UPD: EF Core 8.0.0 пакети
```

**Нові пакети:**
- `Microsoft.EntityFrameworkCore 8.0.0`
- `Microsoft.EntityFrameworkCore.SqlServer 8.0.0`
- `Microsoft.EntityFrameworkCore.Design 8.0.0`

**ClinicDbContext — API:**

| Частина | Код | Опис |
|---------|-----|------|
| `DbSet<Patient>` | `Set<Patient>()` | Таблиця Patients у вигляді C# |
| `DbSet<Doctor>` | `Set<Doctor>()` | Таблиця Doctors |
| `OnConfiguring` | `UseSqlServer(...)` | LocalDB, `(localdb)\mssqllocaldb` |
| `OnModelCreating` | Fluent API | Правила відображення |
| Patient конфіг | `HasKey`, `HasMaxLength`, `IsRequired` | Структура таблиці |
| Patient індекс | `HasIndex(p => p.LastName)` | `IX_Patients_LastName` |
| Doctor LicenseNumber | `.IsUnique()` | `UX_Doctors_License` |
| Enum → string | `HasConversion<string>()` | `BloodType`, `Speciality` як текст |
| WorkSchedule | `ValueConverter<WorkSchedule, string>` | `"8-17"` → `new WorkSchedule(8,17)` |

**Нові концепції в Lab 17:**
- `DbContext` — посередник між C#-об'єктами і БД; відстежує зміни (Unit of Work)
- `DbSet<T>` — "таблиця" в C#; LINQ-запити → SQL
- `OnConfiguring(DbContextOptionsBuilder)` — де і який провайдер
- `UseSqlServer(connectionString)` — підключення до SQL Server / LocalDB
- `OnModelCreating(ModelBuilder)` — Fluent API конфігурація
- `HasKey`, `Property`, `HasMaxLength`, `IsRequired`, `HasColumnName` — налаштування стовпців
- `ValueGeneratedOnAdd()` — IDENTITY стовпець у БД
- `HasConversion<string>()` — enum → текстовий рядок у БД
- `ValueConverter<TModel, TProvider>` — конвертер для struct (WorkSchedule)
- `HasIndex().IsUnique()` — унікальний індекс
- `dotnet ef migrations add <Name>` — генерація класу міграції
- `dotnet ef database update` — застосування міграції до БД
- `context.SaveChanges()` — фіксація всіх змін однією транзакцією
- `context.XxxSet.AddRange(items)` — додати колекцію
- `context.XxxSet.Any()` — `SELECT TOP 1` без завантаження всіх даних
- Ідемпотентний Seeder: `if (Any()) return`

**Що з'явилося в системі:**
- База даних `ClinicApp` в LocalDB з таблицями `Patients` і `Doctors`
- Початкові дані: 5 пацієнтів, 5 лікарів (DbSeeder)
- `Migrations/` — версійована схема БД

---

## Lab 18 — EF Core: Relations (feature/ef-core)

**Статус:** 🔄 В РОБОТІ
**Гілка:** `feature/ef-core` — НЕ злито
**Файли:**
```
src/
├── Data/
│   ├── ClinicDbContext.cs   ← UPD: DbSet<Appointment>, One-to-Many Fluent API, TPH
│   ├── DbSeeder.cs          ← UPD: SeedAppointments (Regular, Urgent, Specialist)
│   └── ClinicRepository.cs  ← NEW: .Include() queries з Eager Loading
├── Migrations/              ← NEW: AddAppointmentsWithRelations
├── Models/
│   ├── Appointment.cs       ← UPD: Id+PatientId+DoctorId private set, IsPaid private set
│   │                             + Patient? Doctor? navigation props + protected ctor
│   ├── RegularAppointment.cs← UPD: protected ctor
│   ├── UrgentAppointment.cs ← UPD: UrgencyNote private set + protected ctor
│   ├── SpecialistAppointment.cs ← UPD: ConsultationTopic private set + private ctor
│   ├── Patient.cs           ← UPD: ICollection<Appointment> Appointments
│   └── Doctor.cs            ← UPD: ICollection<Appointment> Appointments
```

**ClinicRepository — API:**

| Метод | Include | Примітка |
|-------|---------|---------|
| `GetPatientWithAppointments(id)` | `.Include(p => p.Appointments)` | Eager loading |
| `GetDoctorWithAppointments(id)` | `.Include(d => d.Appointments)` | |
| `GetUpcomingAppointments()` | `.Include(Patient) + .Include(Doctor)` | 2 JOIN |
| `GetAppointmentsByPatient(id)` | `.Include(a => a.Doctor)` | Ordered desc |
| `GetDoctorStats()` | `.AsNoTracking() + .Include` | Read-only projection |
| `GetPatientsWithActiveAppointments()` | `.Include + .Any()` | Subquery filter |

**Нові концепції в Lab 18:**
- Navigation Property — `ICollection<T>` (колекція) і `T?` (посилання) у зв'язаних класах
- Eager Loading — `.Include(lambda)` → один SQL JOIN замість N+1 запитів
- Проблема N+1 — що це, як виникає, як вирішити через `.Include()`
- `HasOne/WithMany/HasForeignKey/OnDelete` — Fluent API для One-to-Many
- `DeleteBehavior.Cascade` vs `DeleteBehavior.Restrict` — і чому не можна два Cascade до однієї таблиці
- TPH (Table Per Hierarchy) — `HasDiscriminator<string>("Col").HasValue<T>("val")`
- Підтипи в TPH: одна таблиця, nullable стовпці для специфічних полів
- `AsNoTracking()` — відключення Change Tracker для read-only запитів
- `ClinicRepository` — Repository pattern: інкапсуляція складних запитів

---

## Lab 19 — EF Core Advanced (feature/ef-core)

**Статус:** 🔄 В РОБОТІ
**Гілка:** `feature/ef-core` — НЕ злито
**Файли:**
```
src/
├── Data/
│   ├── ClinicDbContext.cs  ← UPD: DbSet<MedicalRecord>, TPH, OwnsOne, RowVersion
│   └── DbSeeder.cs         ← UPD: SeedMedicalRecords + EmergencyContact
├── Migrations/             ← NEW: AddMedicalRecordsAndOwnedEntities
├── Models/
│   ├── MedicalRecord.cs    ← UPD: private set на Id/PatientId/DoctorId/Date, protected ctor, Patient? nav prop
│   ├── Diagnosis.cs        ← UPD: protected ctor
│   ├── LabResult.cs        ← UPD: protected ctor
│   ├── Prescription.cs     ← UPD: protected ctor + Instructions default ""
│   ├── EmergencyContact.cs ← NEW: Owned Entity (Name, Phone, Relationship)
│   └── Patient.cs          ← UPD: ICollection<MedicalRecord>, EmergencyContact?, byte[] RowVersion
```

**Нові концепції в Lab 19:**
- TPH для abstract класу: `HasDiscriminator` на `MedicalRecord` → Diagnosis/LabResult/Prescription
- Nullable стовпці для підтипових полів: `IsRequired(false)` у Fluent API
- Owned Entity — `OwnsOne(p => p.EmergencyContact, ec => {...})` → стовпці EC_* у Patients
- Різниця OwnsOne vs ValueConverter: N стовпців (OwnsOne) vs 1 серіалізований рядок (ValueConverter)
- `IsRowVersion()` — Concurrency Token для Optimistic Concurrency
- `DbUpdateConcurrencyException` — виняток при конкурентному редагуванні
- Порядок Seeder: Patients → Doctors → Appointments → MedicalRecords (залежність від реальних Ids)

---

## Lab 20 — EF Core Queries (feature/ef-core)

**Статус:** 🔄 В РОБОТІ (остання лаба на цій гілці)
**Гілка:** `feature/ef-core` — НЕ злито (злиття після фіналу)
**Файли:**
```
src/
├── Data/
│   ├── ClinicDbContext.cs     ← UPD: HasQueryFilter(!IsDeleted), IsDeleted default false
│   └── ClinicQueryService.cs  ← NEW: IQueryable demo, Skip/Take, Select DTO, IgnoreQueryFilters
├── Migrations/                ← NEW: AddSoftDeleteAndQueryFilter (IsDeleted column)
├── Models/
│   ├── Patient.cs             ← UPD: bool IsDeleted + SoftDelete()
│   ├── PatientSummaryDto.cs   ← NEW: record DTO
│   └── AppointmentSummaryDto.cs ← NEW: record DTO
```

**ClinicQueryService — API:**

| Метод | Концепція | Опис |
|-------|-----------|------|
| `QueryPatients()` | IQueryable | Повертає невиконаний запит |
| `DemoQueryableVsEnumerable(filter)` | IQueryable vs IEnumerable | Демо різниці |
| `GetPatientsPaged(page, size, orderBy)` | Skip/Take | Пагінація + Count |
| `GetAppointmentsPaged(page, size, status?, patientId?)` | Dynamic filter | Nullable умови |
| `GetPatientSummaries(page, size)` | Projection | Select → PatientSummaryDto |
| `GetAppointmentSummaries(page, size, status?)` | Projection | Select → AppointmentSummaryDto |
| `SoftDeletePatient(id)` | Soft Delete | IsDeleted = true |
| `GetAllPatientsIncludingDeleted()` | IgnoreQueryFilters | Всі включно з видаленими |
| `GetDeletedPatients()` | IgnoreQueryFilters + filter | Тільки видалені |
| `GetDoctorRevenueSummary()` | Tuple projection | AsNoTracking + Sum |

**Нові концепції в Lab 20:**
- `IQueryable<T>` — відкладене виконання (Expression Tree → SQL при матеріалізації)
- Матеріалізація: `.ToList()`, `.Count()`, `.FirstOrDefault()`, `foreach` — виконують SQL
- `.ToList()` в середині ланцюга → решта LINQ в C#, не SQL (антипатерн)
- `.Skip(n).Take(m)` → SQL `OFFSET n ROWS FETCH NEXT m ROWS ONLY` (пагінація)
- Обов'язковість `.OrderBy()` перед `.Skip()/.Take()`
- `(List<T> Items, int TotalCount)` — результат пагінованого запиту
- `Select(p => new DTO(...))` — проєкція тільки потрібних стовпців
- `record` тип для DTO — immutable, автогенеровані Equals/GetHashCode
- `HasQueryFilter(expr)` — Global Query Filter (автоматичний WHERE у кожному запиті)
- `IsDeleted` + `SoftDelete()` — патерн м'якого видалення
- `.IgnoreQueryFilters()` — скасування Global Filter для конкретного запиту
- Nullable параметри як умовні фільтри: `if (x.HasValue) query = query.Where(...)`
- EF попередження про Global Filter + required end of relationship

---

## Lab 21 — Async / Await (feature/async)

**Статус:** ✅ ЗАВЕРШЕНО  
**Гілка:** `feature/async` → зливається в `main`

**Нові файли:**
```
src/Models/ClinicDashboard.cs       ← record з 5 полями (PatientCount, DoctorCount, TotalRevenue, UpcomingCount, TodayCount)
src/Data/AsyncClinicService.cs      ← Tasks 2-5: async EF методи, WhenAll, Parallel.ForEachAsync, AggregateException, IProgress<T>
src/Data/ClinicHttpClient.cs        ← Task 6: HttpClient, GetFromJsonAsync, Task.WhenAny race
```

**Змінені файли:**
```
src/Data/DbSeeder.cs          ← додано SeedAsync() + async private методи (Task 1)
src/Data/ClinicRepository.cs  ← додано async варіанти всіх методів з ConfigureAwait(false)
src/Program.cs                ← using ClinicApp.Data + using Microsoft.EntityFrameworkCore
                                 + меню "База даних (EF Core)" + "Async (Lab 21)"
                                 + EfCoreMenu() + AsyncMenu()
```

**API AsyncClinicService:**
| Метод | Task |
|-------|------|
| `GetAllPatientsAsync(ct)` | 2 |
| `GetPatientByIdAsync(id, ct)` | 2 |
| `GetDoctorByIdAsync(id, ct)` | 2 |
| `GetUpcomingAppointmentsAsync(ct)` | 2 |
| `SaveAppointmentAsync(a, ct)` | 2 |
| `GetDashboardAsync(ct)` | 3 — Task.WhenAll x5 |
| `GetDashboardWithTimeoutAsync(ms)` | 3 — Task.WhenAny race |
| `MarkAppointmentsAsPaidAsync(ids, ct)` | 3 — Parallel.ForEachAsync |
| `SearchPatientsAsync(query, ct)` | 3 — CancellationToken |
| `BuildPatientReportAsync(id, ct)` | 4 — AggregateException + ContinueWith |
| `BulkProcessAppointmentsAsync(status, progress, ct)` | 5 — IProgress<T> |
| `GoodFireAndForgetAsync(ct)` | 1 — async void vs async Task |

**API ClinicHttpClient:**
| Метод | Що демонструє |
|-------|--------------|
| `GetDrugInfoAsync(name, ct)` | GetFromJsonAsync, HttpRequestException, TaskCanceledException |
| `IsApiAvailableAsync(ct)` | async bool, fail-safe |
| `GetDrugInfoWithRaceAsync(name, ms)` | Task.WhenAny race з таймаутом |

**Нові концепції в Lab 21:**
- `async Task`, `async Task<T>` — правильні типи повернення
- `async void` — заборонений патерн (тільки event handlers)
- `await` — звільнення потоку під час очікування I/O
- `CancellationToken`, `CancellationTokenSource` — скасування операцій
- `Task.WhenAll(t1, t2, ...)` — паралельне виконання, чекати всіх
- `Task.WhenAny(t1, t2)` — race, перемагає перший
- `Parallel.ForEachAsync(collection, options, async (item, ct) => ...)` — паралельна обробка колекцій
- `Interlocked.Increment` — атомарний інкремент (thread-safe counter)
- `AggregateException`, `InnerExceptions` — помилки з паралельних задач
- `ContinueWith(TaskContinuationOptions.OnlyOnFaulted)` — обробник для помилкового стану
- `task.IsCompletedSuccessfully`, `task.IsFaulted` — перевірка статусу
- `IProgress<T>`, `Progress<T>` — звітування про прогрес
- `HttpClient` (singleton pattern), `GetFromJsonAsync<T>` — HTTP async запити
- `[JsonPropertyName("...")]` — маппінг JSON → C# властивість
- `ConfigureAwait(false)` — у бібліотечному коді
- `ct.ThrowIfCancellationRequested()` — явна перевірка токену
- `OperationCanceledException` vs `TaskCanceledException` vs `HttpRequestException` — різні типи помилок async

---

## Правила для нових лаб

1. **Перевір CONCEPTS_BY_LAB.md** — чи всі конструкції вже введені
2. **Оновлюй цей файл** — додай новий рядок після завершення лаби
3. **Меню росте** — кожна ✅ лаба показує щось нове в консолі
4. **⏳ лаби** — внутрішнє покращення, меню НЕ змінюється
