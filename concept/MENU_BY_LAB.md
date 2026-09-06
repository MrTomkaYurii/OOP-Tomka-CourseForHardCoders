# Функціональність по лабах — що де є в меню

> Показує **що і коли** з'являється в `src/Program.cs`.  
> Лаби 01–02 — ізольований sandbox, не входять у `src/`.

---

## Головне меню — еволюція

| Пункт меню                    | Lab 03 | Lab 04 | Lab 05 | Lab 06 | Lab 07 | Lab 08 | Lab 09 | Lab 10 | Lab 11 | Lab 12 | Lab 13 | Lab 14 | Lab 15 | Lab 16 | Lab 17 |
|-------------------------------|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| 1. Пацієнти                   | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅ UPD | ✅ DB  |
| 2. Лікарі                     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅ UPD | ✅ DB  |
| 3. Записи                     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅ UPD | ✅     |
| 4. Медична картка             | —      | —      | —      | ✅ NEW | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅ UPD | ✅     |
| 5. Рахунки                    | —      | —      | —      | —      | ✅ NEW | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅ UPD | ✅     |
| 6. Черга — очікування, прийом | —      | —      | —      | —      | —      | —      | ✅ NEW | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅ UPD | ✅     |
| 7. Звіт                       | ✅ (6) | ✅ (6) | ✅ (6) | ✅ (6) | ✅ (6) | ✅ (6) | ✅ (7) | ✅ (7) | ✅ (7) | ✅ (7) | ✅ (7) | ✅ (7) | ✅ (7) | ✅ (7) | ✅ (7) |
| 8. Аналітика                  | —      | —      | —      | —      | —      | —      | —      | ✅ NEW | ✅     | ✅     | ✅     | ✅     | ✅     | ✅ UPD | ✅     |
| 9. Плани лікування            | —      | —      | —      | —      | —      | —      | —      | —      | ✅ NEW | ✅     | ✅     | ✅     | ✅     | ✅ UPD | ✅     |
| 10. Файли                     | —      | —      | —      | —      | —      | —      | —      | —      | —      | ✅ NEW | ✅     | ✅     | ✅     | ✅ UPD | ✅     |
| 11. Звіти (LINQ)              | —      | —      | —      | —      | —      | —      | —      | —      | —      | —      | —      | ✅ NEW | ✅     | ✅ UPD | ✅     |
| 12. Фільтри (Functional)      | —      | —      | —      | —      | —      | —      | —      | —      | —      | —      | —      | —      | ✅ NEW | ✅ UPD | ✅     |
| ← Вийти (зберегти сесію)     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅     | ✅ UPD | ✅ UPD | ✅     | ✅     | ✅ UPD | ✅     |

> Lab 07: головне меню отримало **описи через дефіс** (напр. "1. Пацієнти — реєстрація, пошук").  
> Lab 08: меню **не змінюється** — внутрішні зміни (підкласи Appointment).  
> Lab 09: доданий пункт **6. Черга**; колишній "6. Звіт" переміщено на **7. Звіт**.  
> Lab 10: доданий пункт **8. Аналітика** — новий модуль статистики.  
> Lab 11: доданий пункт **9. Плани лікування** — рефлексія та атрибути.  
> Lab 12: доданий пункт **10. Файли**; вихід тепер пропонує зберегти сесію.  
> Lab 13: меню **не змінюється** — авто-поведінка: лог у файл, паспорт пацієнта, алерти, трекер сесії.  
> Lab 14: доданий пункт **11. Звіти** — LINQ-аналітика по спеціальностях, топ, місячна виручка.  
> Lab 15: доданий пункт **12. Фільтри** — Func/Action/замикання/пайплайн.  
> Lab 16: меню без нових пунктів — **переробка UI**: SelectionPrompt замість цифр, Table для списків, Panel для карток, Tree для медкартки, BarChart для виручки.  
> Lab 17: меню **не змінюється** — внутрішні зміни: Patients і Doctors тепер зберігаються в LocalDB через EF Core. ✅ DB = дані зберігаються між сесіями.

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

## 6. Черга — очікування, прийом *(додано в Lab 09)*

| Підпункт                  | Що робить                                                                    |
|---------------------------|------------------------------------------------------------------------------|
| 1. Додати пацієнта до черги | вибрати пацієнта за ID → `clinic.WaitingRoom.Enqueue(patient)`             |
| 2. Прийняти першого        | `WaitingRoom.Dequeue()` — виводить ім'я та скільки залишилось; `try/catch`  |
| 3. Хто перший?             | `WaitingRoom.Peek()` — показати без видалення; `try/catch`                  |
| 4. Переглянути всю чергу   | `WaitingRoom.ToArray()` — нумерований список черги                          |

**`WaitingQueue<T>`** — новий generic клас в Lab 09:

| Член                  | Опис                                                                |
|-----------------------|---------------------------------------------------------------------|
| `int Count`           | кількість у черзі (тільки читання)                                  |
| `bool IsEmpty`        | чи порожня черга                                                    |
| `void Enqueue(T item)`| додати в кінець                                                     |
| `T Dequeue()`         | взяти першого (видаляє); кидає `InvalidOperationException` якщо порожня |
| `T Peek()`            | подивитись на першого (не видаляє); кидає `InvalidOperationException` якщо порожня |
| `T[] ToArray()`       | поточний стан черги у масиві (FIFO порядок)                         |

---

## 7. Звіт

| Підпункт   | Додано  | Що робить                                                             |
|------------|---------|------------------------------------------------------------------------|
| (без меню) | Lab 03  | `clinic.GenerateReport()` — загальна кількість пацієнтів/лікарів/записів |

---

## 10. Файли *(додано в Lab 12)*

| Підпункт                        | Що робить                                                                                |
|---------------------------------|------------------------------------------------------------------------------------------|
| 1. Експортувати всі звіти       | `Exporter.ExportAll()` → 4 файли в `reports/yyyy-MM-dd/`                                |
| 2. Експортувати пацієнтів       | `Exporter.ExportPatients()` → `patients.txt` з заголовком і підсумком                   |
| 3. Експортувати записи          | `Exporter.ExportAppointments()` → `appointments.txt`                                     |
| 4. Імпортувати пацієнтів з CSV  | `Importer.ImportPatients(path)` → `ImportResult.Print()` — скільки ОК, скільки помилок  |
| 5. Переглянути останні рядки логу | `Logger.GetLastLines(n)` → вивести в консоль                                           |
| 6. Очистити лог                 | `Logger.Clear()` → видаляє `clinic.log`                                                  |
| 0→ вихід                        | Lab 12: пропонує зберегти сесію через `Session.Save(clinic)`                             |

---

## Авто-поведінка *(додано в Lab 13 — Events)*

> Lab 13 **не додає нових пунктів меню** — тільки авто-реакції на вже існуючі дії.

### Що відбувається автоматично після Lab 13

| Дія користувача               | Хто підписаний          | Що відбувається                                                           |
|-------------------------------|-------------------------|---------------------------------------------------------------------------|
| Додати пацієнта               | Logger, Passport        | Рядок у `clinic.log`; генерується `patients/passport_{id}.txt`           |
| Записати на прийом            | Logger, Tracker         | Рядок у `clinic.log`; `AppointmentsBooked++`                              |
| Терміновий запис              | Logger, Tracker         | WARN у `clinic.log`; дозапис у `alerts/urgent_{date}.txt`                |
| Скасувати запис               | Logger, Tracker         | WARN у `clinic.log`; виводить наступного в черзі (якщо є)                |
| Завершити прийом              | Logger, Tracker, Passport | Рядок у `clinic.log`; оновлює `passport_{id}.txt`; `AppointmentsCompleted++` |
| Прийняти оплату               | Logger, Tracker         | Рядок у `clinic.log`; `PaymentsReceived++`                                |
| Завершити план лікування      | Logger, Tracker, Passport | Рядок у `clinic.log`; оновлює `passport_{id}.txt`; `PlansCompleted++`   |

### Файли, що генеруються авто

| Файл                            | Генерується коли                   | Вміст                                                      |
|---------------------------------|------------------------------------|------------------------------------------------------------|
| `clinic.log`                    | будь-яка подія                     | `[рівень]` + час + опис події                              |
| `patients/passport_{id}.txt`    | додавання пацієнта / завершення прийому або плану | 6 розділів: дані, діагнози, аналізи, рецепти, записи, фінанси |
| `alerts/urgent_{date}.txt`      | терміновий запис                   | час + номер запису + нотатка                               |
| `session_summary.txt`           | при виході з програми              | лічильники всіх подій за сесію                             |

### Нові класи в Lab 13

| Клас / файл                       | Простір імен           | Призначення                                                              |
|-----------------------------------|------------------------|--------------------------------------------------------------------------|
| `AppointmentEventArgs`            | `ClinicApp.Events`     | `AppointmentId, PatientId, DoctorId, ScheduledAt, Notes`                 |
| `PatientEventArgs`                | `ClinicApp.Events`     | `PatientId, FullName`                                                    |
| `PaymentEventArgs`                | `ClinicApp.Events`     | `AppointmentId, Amount`                                                  |
| `TreatmentPlanEventArgs`          | `ClinicApp.Events`     | `PlanId, PatientId, Diagnosis`                                           |
| `PatientPassportWriter`           | `ClinicApp.Utils`      | підписується на 3 події → генерує `patients/passport_{id}.txt`           |
| `SessionEventTracker`             | `ClinicApp.Utils`      | рахує всі події; реагує на скасування → черга; `PrintSummary/SaveSummary` |

### Події в менеджерах (Lab 13)

| Менеджер               | Подія                       | Піднімається коли                  |
|------------------------|-----------------------------|------------------------------------|
| `PatientManager`       | `PatientAdded`              | `Add()` успішний                   |
| `AppointmentManager`   | `AppointmentBooked`         | `Book()` успішний                  |
| `AppointmentManager`   | `UrgentAppointmentBooked`   | `BookUrgent()` успішний            |
| `AppointmentManager`   | `AppointmentCancelled`      | `Cancel()` успішний                |
| `AppointmentManager`   | `AppointmentCompleted`      | `Complete()` успішний              |
| `BillingManager`       | `PaymentReceived`           | `PayAppointment()` успішний        |
| `TreatmentPlanManager` | `PlanCompleted`             | `Complete(id)` успішний            |

---

## 9. Плани лікування *(додано в Lab 11)*

| Підпункт                        | Що робить                                                                                     |
|---------------------------------|-----------------------------------------------------------------------------------------------|
| 1. Показати всі плани           | `TreatmentPlans.GetAll()` → вивести список                                                    |
| 2. Додати план лікування        | `FormBuilder.Build<TreatmentPlan>()` → `TreatmentPlans.Add(plan)` (з валідацією атрибутами)  |
| 3. Плани пацієнта               | `TreatmentPlans.GetByPatient(patientId)` → список                                             |
| 4. Активувати план              | `plan.Activate()` — `Planned → Active`                                                        |
| 5. Завершити план               | `plan.Complete()` — `Active → Completed`                                                      |
| 6. Скасувати план               | `plan.Cancel()` — якщо не `Completed/Cancelled`                                               |
| 7. Інформація про тип           | `ModelValidator.PrintInfo(typeof(TreatmentPlan))` — список властивостей та атрибутів          |

**Нові класи в Lab 11:**

| Клас / файл                   | Простір імен           | Призначення                                                        |
|-------------------------------|------------------------|--------------------------------------------------------------------|
| `RequiredAttribute`           | `ClinicApp.Attributes` | власний атрибут: поле є обов'язковим                               |
| `MaxLengthAttribute`          | `ClinicApp.Attributes` | власний атрибут: макс. довжина рядка                               |
| `MinValueAttribute`           | `ClinicApp.Attributes` | власний атрибут: мін. числове значення                             |
| `TreatmentStatus`             | `ClinicApp.Enums`      | enum: Planned / Active / Completed / Cancelled                     |
| `TreatmentPlan`               | `ClinicApp.Models`     | модель із атрибутами на властивостях                               |
| `ValidationResult`            | `ClinicApp.Utils`      | контейнер помилок валідації                                        |
| `ModelValidator`              | `ClinicApp.Utils`      | static: `Validate(object)`, `PrintInfo(Type)` — через рефлексію   |
| `FormBuilder`                 | `ClinicApp.Utils`      | static: `Build<T>() where T : new()` — через рефлексію            |
| `TreatmentPlanManager`        | `ClinicApp.Managers`   | CRUD + валідація при `Add`                                         |

---

## 8. Аналітика *(додано в Lab 10)*

| Підпункт                          | Що робить                                                                                  |
|-----------------------------------|--------------------------------------------------------------------------------------------|
| 1. Лікарі — за навантаженням      | `ComputeDoctorStats()` → зібрати в List → `.Sort()` (IComparable) → вивести               |
| 2. Лікарі — за виручкою           | `.Sort(new DoctorStatsByRevenue())`                                                        |
| 3. Лікарі — за іменем             | `.Sort(new DoctorStatsByName())`                                                           |
| 4. Пацієнти — за кількістю візитів| `ComputePatientStats()` → зібрати в List → `.Sort()` (IComparable) → вивести              |
| 5. Пацієнти — за витратами        | `.Sort(new PatientStatsBySpent())`                                                         |

**Нові класи в Lab 10:**

| Клас | Інтерфейс | Поля |
|------|-----------|------|
| `DoctorStats` | `IComparable<DoctorStats>` | DoctorId, FullName, AppointmentCount, TotalRevenue, LastAppointmentDate |
| `PatientStats` | `IComparable<PatientStats>` | PatientId, FullName, VisitCount, TotalSpent, LastVisitDate |
| `DoctorStatsByRevenue` | `IComparer<DoctorStats>` | сортує за TotalRevenue (desc) |
| `DoctorStatsByName` | `IComparer<DoctorStats>` | сортує за FullName (asc) |
| `PatientStatsBySpent` | `IComparer<PatientStats>` | сортує за TotalSpent (desc) |
| `PatientStatsByLastVisit` | `IComparer<PatientStats>` | сортує за LastVisitDate (desc) |

**`AnalyticsManager`** — ключовий клас Lab 10:

| Метод | Повертає | Як реалізовано |
|-------|----------|----------------|
| `ComputeDoctorStats()` | `IEnumerable<DoctorStats>` | `yield return` по кожному лікарю |
| `ComputePatientStats()` | `IEnumerable<PatientStats>` | `yield return` по кожному пацієнту |

---

## 11. Звіти — LINQ-аналітика *(додано в Lab 14)*

| Підпункт                          | Метод                              | LINQ-оператори                          |
|-----------------------------------|------------------------------------|-----------------------------------------|
| 1. Статистика по спеціальностях   | `Reports.GetSpecialityStats()`     | `GroupBy` + `Select` + `OrderByDescending` |
| 2. Найзайнятіший лікар            | `Reports.FindBusiestDoctorName()`  | `OrderByDescending` + `FirstOrDefault`  |
| 3. Пацієнти з кількома візитами   | `Reports.GetPatientsWithMultipleVisits(n)` | `GroupBy` + `Where` + `Join`   |
| 4. Топ-3 лікарів за виручкою      | `Reports.GetTopEarners(3)`         | `Select` + `OrderByDescending` + `Take` |
| 5. Чи є термінові записи?         | `Reports.HasAnyUrgentAppointments()` | `Any` + `is`                          |
| 6. Активні спеціальності          | `Reports.GetActiveSpecialities()`  | `Select` + `Distinct` + `OrderBy`      |
| 7. Виручка по місяцях             | `Reports.GetMonthlyRevenue()`      | `GroupBy` (анонімний тип) + `ThenBy`   |

**Нові класи в Lab 14:**

| Клас / файл          | Простір імен           | Призначення                                            |
|----------------------|------------------------|--------------------------------------------------------|
| `SpecialityReport`   | `ClinicApp.Models`     | DTO: Speciality, DoctorCount, AppointmentCount, TotalRevenue |
| `ReportManager`      | `ClinicApp.Managers`   | 7 LINQ-звітів; залежить від Appointment/Doctor/Patient |

**`AnalyticsManager` — рефакторинг в Lab 14:**

| Метод | До (Lab 10) | Після (Lab 14) |
|-------|-------------|----------------|
| `ComputeDoctorStats()` | `yield return` з вкладеними `for` | `.Select()` + `.Where()` + `.Count()` + `.Sum()` + `.Max()` + `.Any()` |
| `ComputePatientStats()` | `yield return` з вкладеними `for` | те саме — без `yield return` |

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
├── Clinic.cs                    — Lab 03+ оркестратор; Lab 12: Logger/Exporter/Importer/Session; Lab 13: Passport/Tracker + SubscribeEvents()
├── Program.cs                   — Lab 03+ меню; Lab 12: FilesMenu, session load/save; Lab 13: Tracker.PrintSummary/SaveSummary при виході
│
├── Attributes/                  — Lab 11
│   ├── RequiredAttribute.cs     — Lab 11 ([Required])
│   ├── MaxLengthAttribute.cs    — Lab 11 ([MaxLength(n)])
│   └── MinValueAttribute.cs     — Lab 11 ([MinValue(n)])
│
├── Events/                      — Lab 13
│   ├── AppointmentEventArgs.cs  — Lab 13
│   ├── PatientEventArgs.cs      — Lab 13
│   ├── PaymentEventArgs.cs      — Lab 13
│   └── TreatmentPlanEventArgs.cs— Lab 13
│
├── Enums/
│   ├── BloodType.cs             — Lab 04
│   ├── Speciality.cs            — Lab 04
│   ├── AppointmentStatus.cs     — Lab 04
│   └── TreatmentStatus.cs       — Lab 11 (Planned/Active/Completed/Cancelled)
│
├── Interfaces/
│   ├── IPayable.cs              — Lab 07
│   ├── ICancellable.cs          — Lab 07
│   ├── ISchedulable.cs          — Lab 07
│   └── IIdentifiable.cs         — Lab 09 (int Id { get; })
│
├── Models/
│   ├── Patient.cs               — Lab 03 → Lab 05 (валідація) → Lab 09 (IIdentifiable)
│   ├── Doctor.cs                — Lab 03 → Lab 05 → Lab 07 (ISchedulable) → Lab 09 (IIdentifiable)
│   ├── Appointment.cs           — Lab 03 → Lab 05 → Lab 07 (IPayable, ICancellable) → Lab 08 (virtual) → Lab 09 (IIdentifiable)
│   ├── RegularAppointment.cs    — Lab 08 (override GetDescription)
│   ├── UrgentAppointment.cs     — Lab 08 (override GetCost *1.5, sealed GetDescription, new GetPriority)
│   ├── SpecialistAppointment.cs — Lab 08 (sealed class, override GetCost *1.3)
│   ├── WaitingQueue.cs          — Lab 09 (generic WaitingQueue<T> над Queue<T>)
│   ├── DoctorStats.cs           — Lab 10 (IComparable<DoctorStats>)
│   ├── PatientStats.cs          — Lab 10 (IComparable<PatientStats>)
│   ├── SpecialityReport.cs      — Lab 14 (DTO: Speciality, DoctorCount, AppointmentCount, TotalRevenue)
│   ├── WorkSchedule.cs          — Lab 04 (struct)
│
├── Extensions/                  — Lab 15
│   ├── AppointmentExtensions.cs — Lab 15 (.Unpaid .Upcoming .ByDoctor .Overdue .CostAbove .TotalCost)
│   ├── PatientExtensions.cs     — Lab 15 (.Adults .ByBloodType .WithAppointments)
│   └── DoctorExtensions.cs      — Lab 15 (.BySpeciality .Available .WithAppointments)
│   ├── MedicalRecord.cs         — Lab 06 (abstract)
│   ├── Diagnosis.cs             — Lab 06
│   ├── LabResult.cs             — Lab 06
│   ├── Prescription.cs          — Lab 06
│   └── TreatmentPlan.cs         — Lab 11 (атрибути [Required][MaxLength][MinValue])
│
├── Comparators/                 — Lab 10
│   ├── DoctorStatsByRevenue.cs  — Lab 10 (IComparer<DoctorStats>)
│   ├── DoctorStatsByName.cs     — Lab 10 (IComparer<DoctorStats>)
│   ├── PatientStatsBySpent.cs   — Lab 10 (IComparer<PatientStats>)
│   └── PatientStatsByLastVisit.cs— Lab 10 (IComparer<PatientStats>)
│
├── GrowablePatientManager.cs    — Lab 05 (зростаючий масив — концептуальний)
│
├── Managers/
│   ├── PatientManager.cs        — Lab 03 → Lab 04 → Lab 09 (List<Patient>) → Lab 13 (event PatientAdded)
│   ├── DoctorManager.cs         — Lab 03 → Lab 04
│   ├── AppointmentManager.cs    — Lab 03 → Lab 04 → Lab 07 → Lab 08 → Lab 13 (4 events: Booked/Urgent/Cancelled/Completed)
│   ├── MedicalRecordManager.cs  — Lab 06
│   ├── BillingManager.cs        — Lab 07 → Lab 13 (event PaymentReceived)
│   ├── Repository.cs            — Lab 09 (generic Repository<T> where T : IIdentifiable)
│   ├── AnalyticsManager.cs      — Lab 10 (yield return) → Lab 14 (LINQ rewrite)
│   ├── ReportManager.cs         — Lab 14 (7 LINQ-звітів: GroupBy, Join, OrderBy+Take, Any, Distinct)
│   ├── AppointmentFilter.cs     — Lab 15 (Func<Appointment,bool>: Add/And/Or/Negate/Apply)
│   ├── AppointmentProcessor.cs  — Lab 15 (Action<Appointment>: Run/RunIf/Combine/Execute)
│   ├── AppointmentPipeline.cs   — Lab 15 (фасад: Filter().Then().Execute())
│   └── TreatmentPlanManager.cs  — Lab 11 → Lab 13 (event PlanCompleted; методи Activate/Complete/Cancel)
│
└── Utils/
    ├── ClinicFormatter.cs       — Lab 04 (static: форматування)
    ├── ClinicValidator.cs       — Lab 05 (static: валідація)
    ├── ValidationResult.cs      — Lab 11 (контейнер помилок)
    ├── ModelValidator.cs        — Lab 11 (static: рефлексія → валідація та PrintInfo)
    ├── FormBuilder.cs           — Lab 11 (static: Build<T>() where T : new())
    ├── ClinicLogger.cs          — Lab 12 (AppendAllText, GetLastLines); Lab 13 (7 обробників подій)
    ├── ClinicExporter.cs        — Lab 12 (StreamWriter → reports/yyyy-MM-dd/)
    ├── CsvImporter.cs           — Lab 12 (ReadAllLines, CSV-парсинг, ImportResult)
    ├── ImportResult.cs          — Lab 12 (Imported/Skipped/Errors лічильники)
    ├── SessionManager.cs        — Lab 12 (Save/Load session.dat з [PATIENTS][DOCTORS] секціями)
    ├── PatientPassportWriter.cs — Lab 13 (підписник 3 подій → patients/passport_{id}.txt)
    └── SessionEventTracker.cs   — Lab 13 (рахує події; WaitingRoom реакція; session_summary.txt)
```
