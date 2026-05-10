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

## Lab 11–21 — (детальніше після реалізації попередніх)

Дивись COURSE_DESIGN.md для опису завдань.

---

## Правила для нових лаб

1. **Перевір CONCEPTS_BY_LAB.md** — чи всі конструкції вже введені
2. **Оновлюй цей файл** — додай новий рядок після завершення лаби
3. **Меню росте** — кожна ✅ лаба показує щось нове в консолі
4. **⏳ лаби** — внутрішнє покращення, меню НЕ змінюється
