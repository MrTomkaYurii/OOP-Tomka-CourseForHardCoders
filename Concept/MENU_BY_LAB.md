# Функціональність по лабах — що де є в меню

> Показує **що і коли** з'являється в `src/Program.cs`.  
> Лаби 01–02 — ізольований sandbox, не входять у `src/`.

---

## Головне меню — еволюція

| Пункт меню          | Lab 03 | Lab 04 | Lab 05 | Lab 06 | Lab 07 | Lab 08 |
|---------------------|:------:|:------:|:------:|:------:|:------:|:------:|
| 1. Пацієнти         | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     |
| 2. Лікарі           | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     |
| 3. Записи           | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     |
| 4. Медична картка   | —      | —      | —      | ✅ NEW | ✅     | ✅     |
| 5. Рахунки          | —      | —      | —      | —      | ✅ NEW | ✅     |
| 6. Звіт             | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     |

> Lab 07: головне меню отримало **описи через дефіс** (напр. "1. Пацієнти — реєстрація, пошук").  
> Lab 08: меню **не змінюється** — внутрішні зміни (підкласи Appointment).

---

## 1. Пацієнти

| Підпункт                | Додано  | Що робить                                             |
|-------------------------|---------|-------------------------------------------------------|
| 1. Показати всіх        | Lab 03  | `Patients.DisplayAll()`                               |
| 2. Додати пацієнта      | Lab 03  | ім'я + дата народження                                |
| 2. Додати пацієнта      | +Lab 04 | + вибір `BloodType` (enum, cast `(BloodType)num`)     |
| 2. Додати пацієнта      | +Lab 05 | + `try/catch` → показує помилку при порожньому імені  |
| 3. Знайти за ім'ям      | Lab 03  | `Patients.FindByName(query)`                          |
| 4. Видалити пацієнта    | Lab 03  | `Patients.Remove(id)`                                 |
| 5. Статистика           | Lab 04  | `Patients.DisplayStats()` (розбивка по групах крові)  |

**Модель `Patient`** — що є в об'єкті:

| Поле / властивість     | Додано  | Примітка                                         |
|------------------------|---------|--------------------------------------------------|
| `Id`                   | Lab 03  | авто-лічильник `_nextId`                         |
| `FirstName`, `LastName`| Lab 03  | авто-властивості                                 |
| `DateOfBirth`, `Age`   | Lab 03  | `Age` — обчислювана                              |
| `GetBMI()`, `GetBMIStatus()` | Lab 03 | перенесено з Task8 sandbox             |
| `GetAgeCategory()`     | Lab 03  | перенесено з Task8 sandbox                       |
| `BloodType`            | Lab 04  | `enum BloodType` (9 значень)                     |
| `Phone`                | Lab 04  | рядок                                            |
| `FirstName`, `LastName`| Lab 05 ↑| тепер private backing fields + валідація        |
| `DateOfBirth`          | Lab 05 ↑| валідується (не майбутня, не >150 років)        |
| `Phone`                | Lab 05 ↑| валідується формат 10 цифр                      |

---

## 2. Лікарі

| Підпункт                    | Додано  | Що робить                                                  |
|-----------------------------|---------|-------------------------------------------------------------|
| 1. Показати всіх            | Lab 03  | `Doctors.DisplayAll()`                                      |
| 2. Додати лікаря            | Lab 03  | ім'я + спеціальність (рядок)                               |
| 2. Додати лікаря            | +Lab 04 | + enum `Speciality`, + `WorkSchedule` (початок/кінець)     |
| 2. Додати лікаря            | +Lab 05 | + `try/catch` → помилка при порожньому імені/ліцензії      |
| 3. Знайти за спеціальністю  | Lab 03  | `Doctors.FindBySpeciality(string)`                          |
| 3. Знайти за спеціальністю  | +Lab 04 | перевантаження `FindBySpeciality(Speciality)`               |
| 4. Статистика               | Lab 04  | `Doctors.DisplayStats()` (розбивка по спеціальностях)       |

**Модель `Doctor`** — що є в об'єкті:

| Поле / властивість      | Додано  | Примітка                                     |
|-------------------------|---------|----------------------------------------------|
| `Id`, `FirstName`, `LastName` | Lab 03 | авто-лічильник, авто-властивості        |
| `Speciality`            | Lab 03  | рядок → Lab 04: `enum Speciality`            |
| `LicenseNumber`, `Phone`| Lab 03  | рядки                                        |
| `Schedule`              | Lab 04  | `struct WorkSchedule` (Start, End, IsNow)    |
| `IsAvailableNow`        | Lab 04  | обчислювана → `Schedule.IsNow`               |
| `FirstName`, `LastName` | Lab 05 ↑| private backing fields + валідація           |
| `LicenseNumber`         | Lab 05 ↑| валідується (не порожній)                    |
| `Phone`                 | Lab 05 ↑| валідується формат                           |

---

## 3. Записи на прийом

| Підпункт                | Додано  | Що робить                                              |
|-------------------------|---------|--------------------------------------------------------|
| 1. Записати пацієнта    | Lab 03  | `Appointments.Book(patientId, doctorId, dateTime)`     |
| 1. Записати пацієнта    | +Lab 04 | + тривалість у хвилинах (int, перевантаження Book)     |
| 1. Записати пацієнта    | +Lab 05 | + `try/catch` для помилок тривалості                   |
| 2. Скасувати запис      | Lab 03  | `Appointments.Cancel(id, reason)`                      |
| 3. Позначити виконаним  | Lab 03  | `Appointments.Complete(id)`                            |
| 4. Записи пацієнта      | Lab 03  | `GetByPatient(id)` → `DisplayList()`                   |
| 5. Записи лікаря        | Lab 03  | `GetByDoctor(id)` → `DisplayList()`                    |
| 6. Розклад на дату      | Lab 03  | `clinic.DisplaySchedule(date)`                         |
| 7. Майбутні записи      | Lab 03  | `GetUpcoming()` → `DisplayList()`                      |

**Модель `Appointment`** — що є в об'єкті:

| Поле / властивість      | Додано  | Примітка                                           |
|-------------------------|---------|-----------------------------------------------------|
| `Id`, `PatientId`, `DoctorId` | Lab 03 | авто-ID                                     |
| `ScheduledAt`           | Lab 03  | `DateTime`                                         |
| `Status`                | Lab 03  | рядок → Lab 04: `enum AppointmentStatus`           |
| `Notes`                 | Lab 03  | рядок, необов'язковий                              |
| `DurationMinutes`       | Lab 04  | `int`, за замовчуванням 30                         |
| `DurationMinutes`       | Lab 05 ↑| private backing field + `ValidatePositive`         |
| `GetCost()`             | Lab 03  | обчислювана; Lab 07: реалізує `IPayable`; Lab 08: стає `virtual` |
| `IsPaid`, `MarkPaid()`  | Lab 07  | реалізує `IPayable`                                |
| `IsCancelled`, `CancellationReason` | Lab 07 | реалізує `ICancellable`               |
| `GetDescription()`      | Lab 08  | `virtual` → повертає рядок типу прийому            |
| `GetPriority()`         | Lab 08  | НЕ virtual — для демонстрації `new` vs `override`  |

**Ієрархія підкласів `Appointment`** — введена в Lab 08:

| Клас                      | Унікальні поля    | override / new / sealed                                    |
|---------------------------|-------------------|------------------------------------------------------------|
| `Appointment` (base)      | —                 | `virtual GetCost()`, `virtual GetDescription()`, `GetPriority()` |
| `RegularAppointment`      | —                 | `override GetDescription()` → "Звичайний прийом"          |
| `UrgentAppointment`       | `UrgencyNote`     | `override GetCost() * 1.5m`, `sealed override GetDescription()`, `new GetPriority() => 1` |
| `SpecialistAppointment` *(sealed)* | `ConsultationTopic` | `override GetCost() * 1.3m`, `override GetDescription()` |

---

## 4. Медична картка *(додано в Lab 06)*

| Підпункт                       | Що робить                                                         |
|-------------------------------|-------------------------------------------------------------------|
| 1. Картка пацієнта (зведення) | `MedicalRecords.DisplayPatientSummary(id)` — кількість по типах, хронічні, активні рецепти |
| 2. Всі записи пацієнта        | `GetByPatient(id)` → `DisplayList()`                             |
| 3. Додати діагноз             | `new Diagnosis(patId, docId, date, code, desc, isChronic)` + try/catch |
| 4. Додати аналіз              | `new LabResult(patId, docId, date, name, value, unit, range, isNormal)` + try/catch |
| 5. Додати рецепт              | `new Prescription(patId, docId, date, med, dosage, days, instr)` + try/catch |
| 6. Записи лікаря              | `GetByDoctor(id)` → `DisplayList()`                              |

**Ієрархія `MedicalRecord`** — введена в Lab 06:

| Клас                | Унікальні поля                                       | override          |
|---------------------|------------------------------------------------------|-------------------|
| `MedicalRecord` (abstract) | `Id`, `PatientId`, `DoctorId`, `Date`, `Notes` | `ToString()`      |
| `Diagnosis`         | `DiagnosisCode`, `Description`, `IsChronic`          | `GetSummary()`, `GetRecordType()` |
| `LabResult`         | `TestName`, `Value`, `Unit`, `ReferenceRange`, `IsNormal` | `GetSummary()`, `GetRecordType()` |
| `Prescription`      | `MedicationName`, `Dosage`, `DurationDays`, `ExpiresAt` | `GetSummary()`, `GetRecordType()`, `IsActive()` |

---

## 5. Рахунки *(додано в Lab 07)*

| Підпункт                        | Що робить                                                                         |
|---------------------------------|-----------------------------------------------------------------------------------|
| 1. Борги пацієнта               | `Billing.GetUnpaidByPatient(id)` → `DisplayUnpaid()` — список неоплачених записів |
| 2. Оплатити запис               | `Billing.PayAppointment(id)` — позначає запис як оплачений                        |
| 3. Загальна сума боргів         | `Billing.GetTotalDebt()` — сума всіх неоплачених записів по клініці               |
| 4. Борги пацієнта (з підсумком) | `GetPatientDebt(id)` — скільки конкретний пацієнт заборгував                      |

**Модель `Appointment` — зміни в Lab 07:**

| Нова властивість / метод | Інтерфейс        | Примітка                               |
|--------------------------|------------------|----------------------------------------|
| `bool IsPaid`            | `IPayable`       | `true` після `MarkPaid()`              |
| `decimal GetCost()`      | `IPayable`       | `DurationMinutes * 10m`                |
| `void MarkPaid()`        | `IPayable`       | не спрацьовує якщо запис скасовано     |
| `bool IsCancelled`       | `ICancellable`   | `Status == Cancelled`                  |
| `string CancellationReason` | `ICancellable` | Notes якщо скасовано, інакше ""       |

---

## 6. Звіт

| Підпункт   | Додано  | Що робить                                                             |
|------------|---------|------------------------------------------------------------------------|
| (без меню) | Lab 03  | `clinic.GenerateReport()` — загальна кількість пацієнтів/лікарів/записів |

---

## Тестові дані (seeded при старті)

| Що               | Кількість | Додано  | Примітка                                                  |
|------------------|-----------|---------|-----------------------------------------------------------|
| Пацієнти         | 4         | Lab 03  |                                                           |
| Лікарі           | 3         | Lab 03  |                                                           |
| Записи на прийом | 3         | Lab 03  | Lab 08: 1×RegularAppointment, 1×UrgentAppointment, 1×SpecialistAppointment |
| Медичні записи   | 8         | Lab 06  |                                                           |

---

## Де живуть класи в `src/`

```
src/
├── Clinic.cs                    — оркестратор (Patients, Doctors, Appointments, MedicalRecords, Billing)
├── Program.cs                   — меню (PatientsMenu / DoctorsMenu / AppointmentsMenu / MedicalRecordsMenu / BillingMenu)
│
├── Enums/
│   ├── BloodType.cs             — Lab 04
│   ├── Speciality.cs            — Lab 04
│   └── AppointmentStatus.cs     — Lab 04
│
├── Interfaces/                  — Lab 07
│   ├── IPayable.cs              — Lab 07
│   ├── ICancellable.cs          — Lab 07
│   └── ISchedulable.cs          — Lab 07
│
├── Models/
│   ├── Patient.cs               — Lab 03 → Lab 05 (валідація)
│   ├── Doctor.cs                — Lab 03 → Lab 05 → Lab 07 (ISchedulable)
│   ├── Appointment.cs           — Lab 03 → Lab 05 → Lab 07 (IPayable, ICancellable) → Lab 08 (virtual)
│   ├── RegularAppointment.cs    — Lab 08 (override GetDescription)
│   ├── UrgentAppointment.cs     — Lab 08 (override GetCost *1.5, sealed GetDescription, new GetPriority)
│   ├── SpecialistAppointment.cs — Lab 08 (sealed class, override GetCost *1.3)
│   ├── WorkSchedule.cs          — Lab 04 (struct)
│   ├── MedicalRecord.cs         — Lab 06 (abstract)
│   ├── Diagnosis.cs             — Lab 06
│   ├── LabResult.cs             — Lab 06
│   └── Prescription.cs          — Lab 06
│
├── Managers/
│   ├── PatientManager.cs        — Lab 03 → Lab 04 (indexer, out, overloads)
│   ├── DoctorManager.cs         — Lab 03 → Lab 04
│   ├── AppointmentManager.cs    — Lab 03 → Lab 04 → Lab 07 (GetAll) → Lab 08 (BookUrgent, BookSpecialist)
│   ├── GrowablePatientManager.cs— Lab 05 (зростаючий масив — концептуальний)
│   ├── MedicalRecordManager.cs  — Lab 06
│   └── BillingManager.cs        — Lab 07
│
└── Utils/
    ├── ClinicFormatter.cs       — Lab 04 (static: форматування)
    └── ClinicValidator.cs       — Lab 05 (static: валідація)
```
