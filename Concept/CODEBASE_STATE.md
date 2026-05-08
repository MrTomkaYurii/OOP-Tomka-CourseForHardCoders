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
- Немає типів пацієнтів (застрахований/приватний) → Lab06 Inheritance

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

**Статус:** 📋 ЗАПЛАНОВАНО
**Гілка:** `feature/interfaces` — ✅ зливається
**Що з'явиться:**
- `ISchedulable`, `IPayable`, `ICancellable`, `INotifiable`
- В меню: записатись / скасувати / переглянути записи
- Перший погляд на `IRepository<T>`

**Нові файли:** `Interfaces/ISchedulable.cs`, `Interfaces/IPayable.cs` тощо

---

## Lab 08 — Polymorphism (feature/polymorphism)

**Статус:** 📋 ЗАПЛАНОВАНО
**Гілка:** `feature/polymorphism` — ⏳ чекає Lab09
**Що зміниться:**
- `RegularAppointment`, `UrgentAppointment`, `SpecialistAppointment`
- Поліморфний список `Appointment[]` або `List<Appointment>`
- Внутрішнє покращення, меню не змінюється

---

## Lab 09 — Generics (feature/generics)

**Статус:** 📋 ЗАПЛАНОВАНО
**Гілка:** `feature/generics` — ✅ зливається
**Що з'явиться:**
- `Repository<T>` замінює PatientManager, DoctorManager
- `WaitingQueue<T>` (черга очікування)
- В меню: черга очікування

---

## Lab 10 — Iterators & Comparators (feature/iterators)

**Статус:** 📋 ЗАПЛАНОВАНО
**Гілка:** `feature/iterators` — ✅ зливається
**Що з'явиться:**
- `IEnumerable<T>` на колекціях
- Сортування пацієнтів, лікарів, записів за різними критеріями
- В меню: вибір критерію сортування

---

## Lab 11–21 — (детальніше після реалізації попередніх)

Дивись COURSE_DESIGN.md для опису завдань.

---

## Правила для нових лаб

1. **Перевір CONCEPTS_BY_LAB.md** — чи всі конструкції вже введені
2. **Оновлюй цей файл** — додай новий рядок після завершення лаби
3. **Меню росте** — кожна ✅ лаба показує щось нове в консолі
4. **⏳ лаби** — внутрішнє покращення, меню НЕ змінюється
