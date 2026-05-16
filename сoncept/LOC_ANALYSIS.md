# LOC Analysis — Аналіз кодобази по лабах

> Підраховано після завершення Labs 03–20 (гілка `feature/ef-core` злита в `main`).  
> Враховуються тільки файли `src/` (без `bin/`, `obj/`, `Migrations/`).  
> LOC = кількість рядків включно з коментарями та порожніми рядками (загальний обсяг файлу).

---

## Зведена таблиця по лабах

| Лаба | Нові файли | LOC нових файлів | Ключові зміни в існуючих | Оцінка |
|------|-----------|-----------------|--------------------------|--------|
| Lab 03 | Patient, Doctor, Appointment, Clinic, 3 Managers, Program | ~806 | — (старт) | ⭐⭐⭐⭐ |
| Lab 04 | 3 Enums, WorkSchedule, ClinicFormatter | 108 | Patient+Doctor+Appointment: enum поля | ⭐⭐ |
| Lab 05 | GrowablePatientManager, ClinicValidator | 91 | Patient+Doctor+Appointment: валідація | ⭐⭐ |
| Lab 06 | MedicalRecord, Diagnosis, LabResult, Prescription, MedicalRecordManager | 304 | — | ⭐⭐⭐ |
| Lab 07 | 4 Interfaces, BillingManager | 103 | Appointment: IPayable+ICancellable; Doctor: ISchedulable | ⭐⭐ |
| Lab 08 | RegularAppointment, UrgentAppointment, SpecialistAppointment | 42 | AppointmentManager: підтипи | ⭐⭐ |
| Lab 09 | WaitingQueue | 19 | Всі Managers: Array → List<T>; новий пункт меню | ⭐⭐ |
| Lab 10 | 4 Comparators, DoctorStats, PatientStats, AnalyticsManager, Repository | 202 | DoctorManager+PatientManager: статистика | ⭐⭐⭐ |
| Lab 11 | 3 Attributes, ModelValidator, FormBuilder, ValidationResult, TreatmentPlan, TreatmentPlanManager | 256 | Clinic: TreatmentPlanManager | ⭐⭐⭐⭐ |
| Lab 12 | ClinicLogger, ClinicExporter, CsvImporter, SessionManager, ImportResult | 280 | Clinic: Logger+Exporter+Importer+Session | ⭐⭐⭐ |
| Lab 13 | 4 EventArgs, PatientPassportWriter, SessionEventTracker | 232 | 4 Managers: події; Clinic: SubscribeEvents() | ⭐⭐⭐ |
| Lab 14 | SpecialityReport, ReportManager | 117 | AnalyticsManager: LINQ рефакторинг | ⭐⭐ |
| Lab 15 | 3 Extensions, AppointmentFilter, AppointmentPipeline, AppointmentProcessor | 179 | Clinic: Pipeline; Program: FunctionalMenu | ⭐⭐⭐ |
| Lab 16 | ClinicRenderer | 349 | Program.cs: повний переврайт на Spectre.Console | ⭐⭐⭐⭐ |
| Lab 17 | ClinicDbContext, DbSeeder | 382 | Patient+Doctor: private set Id | ⭐⭐⭐ |
| Lab 18 | ClinicRepository | 91 | DbContext: Appointments+TPH; моделі: nav props | ⭐⭐⭐ |
| Lab 19 | EmergencyContact | 35 | DbContext: MedicalRecord TPH, OwnsOne, RowVersion | ⭐⭐ |
| Lab 20 | ClinicQueryService, PatientSummaryDto, AppointmentSummaryDto | 288 | DbContext: HasQueryFilter; Patient: IsDeleted | ⭐⭐⭐ |
| Lab 21 | AsyncClinicService, ClinicHttpClient, ClinicDashboard | ~420 | DbSeeder: SeedAsync; ClinicRepository: async variants; Program.cs: AsyncMenu+EfCoreMenu | ⭐⭐⭐⭐ |

**Разом нових файлів: 71**  
**Загальний LOC `src/` (без Migrations):** ~5 280 рядків

---

## Детально: нові файли по лабах

### Lab 03 — Classes & Objects
| Файл | LOC |
|------|-----|
| `Models/Patient.cs` | 96 |
| `Models/Doctor.cs` | 86 |
| `Models/Appointment.cs` | 74 |
| `Clinic.cs` | 95 |
| `Managers/PatientManager.cs` | 93 |
| `Managers/DoctorManager.cs` | 121 |
| `Managers/AppointmentManager.cs` | 241 |
| `Program.cs` *(росте протягом всього курсу)* | **876** |
| **Підсумок (без Program.cs)** | **806** |

---

### Lab 04 — Class Members
| Файл | LOC |
|------|-----|
| `Enums/BloodType.cs` | 13 |
| `Enums/Speciality.cs` | 12 |
| `Enums/AppointmentStatus.cs` | 7 |
| `Enums/TreatmentStatus.cs` | 8 |
| `Models/WorkSchedule.cs` | 22 |
| `Utils/ClinicFormatter.cs` | 46 |
| **Підсумок** | **108** |

---

### Lab 05 — Encapsulation
| Файл | LOC |
|------|-----|
| `GrowablePatientManager.cs` | 58 |
| `Utils/ClinicValidator.cs` | 33 |
| **Підсумок** | **91** |

---

### Lab 06 — Inheritance
| Файл | LOC |
|------|-----|
| `Models/MedicalRecord.cs` | 33 |
| `Models/Diagnosis.cs` | 31 |
| `Models/LabResult.cs` | 43 |
| `Models/Prescription.cs` | 42 |
| `Managers/MedicalRecordManager.cs` | 155 |
| **Підсумок** | **304** |

---

### Lab 07 — Interfaces
| Файл | LOC |
|------|-----|
| `Interfaces/IPayable.cs` | 7 |
| `Interfaces/ICancellable.cs` | 7 |
| `Interfaces/IIdentifiable.cs` | 5 |
| `Interfaces/ISchedulable.cs` | 6 |
| `Managers/BillingManager.cs` | 78 |
| **Підсумок** | **103** |

---

### Lab 08 — Polymorphism
| Файл | LOC |
|------|-----|
| `Models/RegularAppointment.cs` | 8 |
| `Models/UrgentAppointment.cs` | 17 |
| `Models/SpecialistAppointment.cs` | 17 |
| **Підсумок** | **42** |

---

### Lab 09 — Generics
| Файл | LOC |
|------|-----|
| `Models/WaitingQueue.cs` | 19 |
| **Підсумок** | **19** |
> + масштабний рефакторинг всіх Managers: Array → `List<T>`

---

### Lab 10 — Iterators & IComparable
| Файл | LOC |
|------|-----|
| `Comparators/DoctorStatsByRevenue.cs` | 12 |
| `Comparators/DoctorStatsByName.cs` | 12 |
| `Comparators/PatientStatsBySpent.cs` | 12 |
| `Comparators/PatientStatsByLastVisit.cs` | 12 |
| `Models/DoctorStats.cs` | 32 |
| `Models/PatientStats.cs` | 32 |
| `Managers/AnalyticsManager.cs` | 44 |
| `Managers/Repository.cs` | 23 |
| **Підсумок** | **179** |

---

### Lab 11 — Reflection & Attributes
| Файл | LOC |
|------|-----|
| `Attributes/RequiredAttribute.cs` | 10 |
| `Attributes/MaxLengthAttribute.cs` | 14 |
| `Attributes/MinValueAttribute.cs` | 14 |
| `Utils/ModelValidator.cs` | 56 |
| `Utils/FormBuilder.cs` | 40 |
| `Utils/ValidationResult.cs` | 13 |
| `Models/TreatmentPlan.cs` | 46 |
| `Managers/TreatmentPlanManager.cs` | 49 |
| **Підсумок** | **242** |

---

### Lab 12 — Files & Serialization
| Файл | LOC |
|------|-----|
| `Utils/ClinicLogger.cs` | 57 |
| `Utils/ClinicExporter.cs` | 91 |
| `Utils/CsvImporter.cs` | 56 |
| `Utils/SessionManager.cs` | 56 |
| `Utils/ImportResult.cs` | 20 |
| **Підсумок** | **280** |

---

### Lab 13 — Events & Delegates
| Файл | LOC |
|------|-----|
| `Events/AppointmentEventArgs.cs` | 17 |
| `Events/PatientEventArgs.cs` | 11 |
| `Events/PaymentEventArgs.cs` | 11 |
| `Events/TreatmentPlanEventArgs.cs` | 13 |
| `Utils/PatientPassportWriter.cs` | 117 |
| `Utils/SessionEventTracker.cs` | 63 |
| **Підсумок** | **232** |

---

### Lab 14 — LINQ
| Файл | LOC |
|------|-----|
| `Models/SpecialityReport.cs` | 20 |
| `Managers/ReportManager.cs` | 97 |
| **Підсумок** | **117** |
> + рефакторинг `AnalyticsManager.cs` (for → LINQ): поточний розмір 44 LOC (скорочення!)

---

### Lab 15 — Functional C#
| Файл | LOC |
|------|-----|
| `Extensions/AppointmentExtensions.cs` | 26 |
| `Extensions/DoctorExtensions.cs` | 17 |
| `Extensions/PatientExtensions.cs` | 17 |
| `Managers/AppointmentFilter.cs` | 54 |
| `Managers/AppointmentPipeline.cs` | 32 |
| `Managers/AppointmentProcessor.cs` | 33 |
| **Підсумок** | **179** |

---

### Lab 16 — Console UI (Spectre.Console)
| Файл | LOC |
|------|-----|
| `UI/ClinicRenderer.cs` | 349 |
| **Підсумок** | **349** |
> + повний переврайт `Program.cs`: вся навігація переведена на `SelectionPrompt`

---

### Lab 17 — EF Core Basic
| Файл | LOC |
|------|-----|
| `Data/ClinicDbContext.cs` | 257 |
| `Data/DbSeeder.cs` | 125 |
| **Підсумок** | **382** |
> + `Migrations/InitialCreate` (auto-generated, не рахується)

---

### Lab 18 — Navigation Properties & Relations
| Файл | LOC |
|------|-----|
| `Data/ClinicRepository.cs` | 91 |
| **Підсумок** | **91** |
> + DbContext +70 LOC (Appointments, TPH, FKs)
> + моделі: nav properties на Patient, Doctor, Appointment, підкласи (protected ctors)

---

### Lab 19 — Advanced EF Core
| Файл | LOC |
|------|-----|
| `Models/EmergencyContact.cs` | 35 |
| **Підсумок** | **35** |
> + DbContext +85 LOC (MedicalRecord TPH, OwnsOne, RowVersion)
> + Seeder +40 LOC (SeedMedicalRecords)

---

### Lab 20 — IQueryable, Pagination, Projections
| Файл | LOC |
|------|-----|
| `Data/ClinicQueryService.cs` | 249 |
| `Models/PatientSummaryDto.cs` | 22 |
| `Models/AppointmentSummaryDto.cs` | 17 |
| **Підсумок** | **288** |
> + DbContext: `HasQueryFilter` + `IsDeleted` на Patient

---

### Lab 21 — Async / Await
| Файл | LOC |
|------|-----|
| `Data/AsyncClinicService.cs` | ~230 |
| `Data/ClinicHttpClient.cs` | ~140 |
| `Models/ClinicDashboard.cs` | 25 |
| **Підсумок нових** | **~395** |
> + `DbSeeder.cs`: +80 LOC (SeedAsync + 4 async private методи)
> + `ClinicRepository.cs`: +55 LOC (5 async варіантів з ConfigureAwait)
> + `Program.cs`: +200 LOC (EfCoreMenu, AsyncMenu, using директиви)

---

## Загальна статистика

| Категорія | LOC |
|-----------|-----|
| `Models/` | 692 |
| `Managers/` | 1 020 |
| `Data/` (EF Core) | 722 |
| `Utils/` | 648 |
| `UI/` | 349 |
| `Extensions/` | 60 |
| `Events/` | 52 |
| `Comparators/` | 48 |
| `Interfaces/` | 25 |
| `Attributes/` | 38 |
| `Enums/` | 40 |
| `Clinic.cs` | 95 |
| `GrowablePatientManager.cs` | 58 |
| `Program.cs` | 876 |
| **Разом** | **~4 720** |

---

## Висновки по балансу

### Перевантажені лаби
| Лаба | LOC нових файлів | Причина |
|------|-----------------|---------|
| **Lab 16** | 349 + Program.cs переврайт | ClinicRenderer — великий фасад; Program.cs повністю переписаний |
| **Lab 17** | 382 | DbContext — великий через детальні коментарі; Seeder — всі чотири сутності |
| **Lab 20** | 288 | ClinicQueryService — багато методів-демонстрацій |

### Легкі лаби
| Лаба | LOC нових файлів | Причина |
|------|-----------------|---------|
| **Lab 08** | 42 | Тільки 3 підкласи Appointment |
| **Lab 09** | 19 | WaitingQueue — простий клас; основна робота — рефакторинг |
| **Lab 19** | 35 | EmergencyContact — малий клас; основна робота — в DbContext |

### Рекомендації для наступних курсів
1. **Lab 09** варто розширити: додати пріоритетну чергу або SortedList — щоб Generics-лаба мала більше самостійного коду
2. **Lab 16 (ClinicRenderer)** можна розбити: базовий UI (Table, Menu) в Lab 16, складний UI (Tree, BarChart) — в Lab 17 або окрема
3. **Lab 19** могла б включати більше — наприклад, повноцінну симуляцію конкурентного доступу (два DbContext)
4. **EF Core arc (17-20)** занадто великий для 4 лаб — розглянути розбивку на 5-6 лаб у наступній ітерації курсу
5. **Program.cs (876 LOC)** — єдиний монолітний файл; починаючи з Lab 10+ студентам важко орієнтуватися; варто ввести `MenuHandler`-клас раніше

---

## Графік росту `Program.cs`

| Лаба | Приблизний LOC |
|------|----------------|
| Lab 03 | ~120 |
| Lab 06 | ~200 |
| Lab 09 | ~300 |
| Lab 12 | ~450 |
| Lab 14 | ~600 |
| Lab 16 | 876 (після переврайту на Spectre.Console) |

> **Висновок:** Program.cs зростає нелінійно. Lab 16 — переломний момент: переврайт вдвічі зменшив LOC (було ~1200 до рефакторингу), але файл залишається найбільшим. Це типова ситуація для навчального проєкту де точка входу є одночасно і оркестратором і навчальним прикладом.
