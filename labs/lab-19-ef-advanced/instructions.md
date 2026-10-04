# Лаба 19 — EF Core: TPH для абстрактної ієрархії, Owned Entity, Concurrency

## Мета

Зберегти в БД абстрактну ієрархію медичних записів (TPH з різними наборами полів), вбудувати в таблицю пацієнтів залежний об'єкт (Owned Entity) і захистити дані від одночасного редагування (concurrency token).

## Контекст

Після Лаби 18 таблиця `Appointments` зберігає ієрархію підтипів через TPH. Але медичні записи (діагноз, аналіз, рецепт) ще не в БД — і ця ієрархія складніша: `MedicalRecord` абстрактний, а підтипи мають зовсім різні набори полів.

Крім того, пацієнту потрібна контактна особа на випадок надзвичайної ситуації. Це не окрема сутність, а **частина** пацієнта (ім'я, телефон, ким доводиться) — окрема таблиця для неї надлишкова, досить кількох стовпців у `Patients`.

І ще: якщо два адміністратори одночасно редагують картку пацієнта, без захисту від **паралельного доступу** останній запис мовчки перезапише перший.

### Структура проєкту на початку лаби

Це результат Лаби 18 — стан `main` після її злиття:

```text
oop-course/                                    ← гілка main (після злиття Лаби 18)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/
    │   ├── Patient.cs
    │   ├── Diagnosis.cs
    │   ├── LabResult.cs
    │   ├── MedicalRecord.cs
    │   ├── Prescription.cs
    │   └── … ще 11 файлів без змін
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
    └── Migrations/  (5 файлів — генерує EF)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Ключові поняття

- **TPH для абстрактного класу.** `new MedicalRecord()` неможливий — EF створює лише конкретні підтипи. Дискримінатор описується для базового типу; поля підтипів у рядках інших підтипів — `NULL`, тому вони налаштовуються як необов'язкові.
- **Owned Entity (`OwnsOne`).** Залежний об'єкт без власного `Id` і таблиці: його поля стають стовпцями таблиці власника (`EC_Name`, `EC_Phone`, `EC_Relationship` у `Patients`). На відміну від `ValueConverter` (один рядок, як `WorkSchedule`), кожне поле — окремий стовпець рідного SQL-типу, по якому можна шукати.
- **Concurrency token (`RowVersion`).** SQL Server автоматично змінює стовпець `rowversion` при кожному `UPDATE`. EF додає до `UPDATE` умову `WHERE RowVersion = @старе_значення`: якщо запис устиг змінити хтось інший, рядок не знайдеться — і EF кине `DbUpdateConcurrencyException`.

### Що нового дозволено (і тільки воно)

- TPH для абстрактного базового класу;
- `OwnsOne` (Owned Entity);
- `IsRowVersion()` і `DbUpdateConcurrencyException`.

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-19
```

Коміт — на кожне завдання (`Lab19 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. Ієрархія `MedicalRecord`: підготовка до EF ⭐⭐

### Умова

Підготуйте абстрактну ієрархію медичних записів (Лаба 06) до роботи з EF: властивості мають отримувати значення з БД, а EF — створювати об'єкти підтипів.

**Що реалізувати:**

1. У `MedicalRecord` змінити `Id`, `PatientId`, `DoctorId`, `Date` на `{ get; private set; }`.
2. Додати в `MedicalRecord` `protected` конструктор без параметрів, що задає `Date = DateTime.Today`.
3. Додати в `MedicalRecord` навігаційну властивість `Patient`.
4. Додати `protected` конструктори без параметрів у `Diagnosis`, `LabResult`, `Prescription`.

### Специфікація

| Клас | Зміни |
|------|-------|
| `MedicalRecord` | `Id`, `PatientId`, `DoctorId`, `Date` — `private set`; `protected MedicalRecord()`; `public Patient? Patient { get; set; }` |
| `Diagnosis`, `LabResult`, `Prescription` | `protected` конструктор без параметрів |

### Приклад

```csharp
var records = context.MedicalRecords.Where(r => r.PatientId == 1).ToList();
// у списку — Diagnosis, LabResult, Prescription: EF створив об'єкти потрібних підтипів
```

### Підказки

1. `Date = DateTime.Today` у конструкторі без параметрів — безпечне значення до того, як EF запише справжнє.
2. EF викликає `protected` конструктор через рефлексію; конструктор без параметрів потрібен кожному конкретному підтипу.
3. Завантажуючи запис, EF заповнює властивості через сеттери — а сеттери підтипів валідують значення (Лаба 05). Подумайте, чи небезпечно це для даних, що вже лежать у БД.

📖 Документація:
- [Конструктори сутностей](https://learn.microsoft.com/ef/core/modeling/constructors)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `MedicalRecord` → `Diagnosis` / `LabResult` / `Prescription` | `ServiceRecord` → … | `OrderRecord` → … | `AcademicRecord` → … | `VehicleRecord` → … | `LoanRecord` → … | `FitnessRecord` → … |

### Коміт

```bash
git add ClinicApp/Models/MedicalRecord.cs ClinicApp/Models/Diagnosis.cs ClinicApp/Models/LabResult.cs ClinicApp/Models/Prescription.cs
git commit -m "Lab19 Task01"
```

---

## Задача 2. Таблиця `MedicalRecords` (TPH) у Fluent API ⭐⭐⭐

### Умова

Опишіть таблицю медичних записів: два зовнішні ключі, дискримінатор і необов'язкові поля підтипів.

**Що реалізувати:**

1. Додати в `ClinicDbContext` таблицю `DbSet<MedicalRecord> MedicalRecords`.
2. Налаштувати `MedicalRecord` у `OnModelCreating`: таблиця, ключ, зв'язки, дискримінатор (специфікація нижче).
3. Налаштувати поля кожного підтипу окремо — усі необов'язкові.

### Специфікація

| Стовпець | Налаштування |
|----------|--------------|
| `Id` | PK, IDENTITY; значення з `_nextId` ігнорується (як у Лабі 17) |
| `PatientId` | FK → `Patients`, каскадне видалення |
| `DoctorId` | FK → `Doctors`, `Restrict` |
| `Date` | дата |
| `Notes` | до 500 символів |
| `RecordType` | дискримінатор: `Diagnosis` / `LabResult` / `Prescription` |
| `DiagnosisCode` (до 20), `Description`, `IsChronic` | лише для `Diagnosis`, nullable |
| `TestName`, `Value`, `Unit`, `ReferenceRange`, `IsNormal` | лише для `LabResult`, nullable |
| `MedicationName`, `Dosage`, `DurationDays`, `Instructions` | лише для `Prescription`, nullable |

### Приклад

```
MedicalRecords
Id | PatientId | RecordType   | DiagnosisCode | TestName   | MedicationName
 1 |     1     | Diagnosis    | I10           | NULL       | NULL
 2 |     1     | LabResult    | NULL          | Холестерин | NULL
 3 |     1     | Prescription | NULL          | NULL       | Лізиноприл
```

### Підказки

1. Два каскади до однієї таблиці SQL Server не дозволяє — як і в Лабі 18: пацієнт — каскад, лікар — `Restrict`.
2. Абстрактний базовий тип не має власного значення дискримінатора — значення задаються лише для конкретних підтипів.
3. `IsRequired(false)` явно позначає стовпець як nullable: без нього EF може вимагати `NOT NULL` для полів, яких в інших підтипах просто немає.
4. Значення полів підтипів зберігаються в приватних полях (`_diagnosisCode`, `_testName` …) за властивостями — EF працює через властивості.

📖 Документація:
- [Успадкування (TPH)](https://learn.microsoft.com/ef/core/modeling/inheritance)
- [Обов'язкові й необов'язкові властивості](https://learn.microsoft.com/ef/core/modeling/entity-properties#required-and-optional-properties)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `MedicalRecords` (`RecordType`) | `ServiceRecords` | `OrderRecords` | `AcademicRecords` | `VehicleRecords` | `LoanRecords` | `FitnessRecords` |

### Коміт

```bash
git add ClinicApp/Data/ClinicDbContext.cs
git commit -m "Lab19 Task02"
```

---

## Задача 3. Контактна особа як Owned Entity ⭐⭐

### Умова

Додайте пацієнту контактну особу на випадок надзвичайної ситуації. Вона не має власного `Id` і таблиці — існує лише як частина пацієнта.

**Що реалізувати:**

1. Створити клас `EmergencyContact` у `ClinicApp/Models/` з трьома властивостями зі специфікації.
2. Додати в `Patient` необов'язкову властивість `EmergencyContact`.
3. Налаштувати її в `OnModelCreating` через `OwnsOne` — три стовпці в таблиці `Patients`.

### Специфікація

| Властивість `EmergencyContact` | Стовпець у `Patients` | Довжина |
|--------------------------------|-----------------------|---------|
| `Name` — ім'я контактної особи | `EC_Name` | 100 |
| `Phone` — телефон | `EC_Phone` | 20 |
| `Relationship` — ким доводиться (дружина, мати, брат…) | `EC_Relationship` | 50 |

| Член `Patient` | |
|----------------|--|
| `public EmergencyContact? EmergencyContact { get; set; }` | необов'язкова: без контакту стовпці `EC_*` — `NULL` |

### Приклад

```
Patients
Id | FirstName | … | EC_Name       | EC_Phone   | EC_Relationship
 1 | Іван      | … | Олена Петренко | 0671112233 | дружина
 2 | Олена     | … | NULL          | NULL       | NULL
```

### Підказки

1. `OwnsOne` вбудовує поля залежного об'єкта в таблицю власника: немає `JOIN`, FK чи окремої таблиці.
2. Назви стовпців задаються через `HasColumnName`.
3. Порівняйте з `WorkSchedule` (Лаба 17): один рядок проти трьох окремих стовпців — по яких зручніше шукати?

📖 Документація:
- [Owned Entity Types](https://learn.microsoft.com/ef/core/modeling/owned-entities)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `EmergencyContact` | `EmergencyContact` гостя | `ContactPerson` клієнта | `Guardian` студента | `EmergencyContact` клієнта | `ContactPerson` читача | `EmergencyContact` учасника |

### Коміт

```bash
git add ClinicApp/Models/EmergencyContact.cs ClinicApp/Models/Patient.cs ClinicApp/Data/ClinicDbContext.cs
git commit -m "Lab19 Task03"
```

---

## Задача 4. `RowVersion`, міграція і медичні записи в сідері ⭐⭐⭐

### Умова

Захистіть картку пацієнта від одночасного редагування, застосуйте всі зміни схеми цієї лаби однією міграцією і додайте медичні записи в сідер.

**Що реалізувати:**

1. Додати в `Patient` властивість `RowVersion` і налаштувати її як concurrency token (`IsRowVersion()`).
2. Створити і застосувати міграцію `AddMedicalRecordsAndOwnedEntities` (команди нижче).
3. Додати в `DbSeeder` крок `SeedMedicalRecords` (після `SeedAppointments`): хронічний і звичайний діагнози, аналіз у нормі й поза нормою, активний рецепт — на реальні `Id` з БД; ідемпотентно.
4. Додати в `Program.cs` статичну функцію `DemoConcurrencyConflict()` і викликати її один раз на старті: два окремі контексти завантажують того самого пацієнта, перший зберігає зміну, другий отримує `DbUpdateConcurrencyException`; виведіть, що сталося.

### Специфікація

```bash
dotnet ef migrations add AddMedicalRecordsAndOwnedEntities --project ClinicApp
dotnet ef database update --project ClinicApp
```

| Член `Patient` | Налаштування |
|----------------|--------------|
| `public byte[]? RowVersion { get; private set; }` | `IsRowVersion()` → тип `rowversion`, оновлюється SQL Server автоматично |

| Крок `DemoConcurrencyConflict()` | Очікувано |
|----------------------------------|-----------|
| контекст А і контекст Б завантажують пацієнта #1 | обидва бачать однаковий `RowVersion` |
| А змінює телефон і зберігає | успіх, `RowVersion` у БД змінився |
| Б змінює ім'я і зберігає | `DbUpdateConcurrencyException` |

### Приклад

```
== Конфлікт паралельного редагування ==
Сесія А: зміни збережено.
Сесія Б: DbUpdateConcurrencyException — запис уже змінено іншим користувачем.
```

### Підказки

1. `IsRowVersion()` поєднує три налаштування: тип `rowversion`, участь у `WHERE` при `UPDATE` і автоматичну генерацію значення сервером.
2. Два «користувачі» — це два **окремі** екземпляри `DbContext`: в одному контексті EF відстежує один об'єкт і конфлікту не буде.
3. Перехопіть виняток у `try/catch`; у реальній програмі тут або перезавантажують дані, або повідомляють користувача.
4. Порядок у сідері: пацієнти → лікарі → записи → медичні записи.

📖 Документація:
- [Конфлікти паралельного доступу](https://learn.microsoft.com/ef/core/saving/concurrency)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `Patient.RowVersion` | `Guest.RowVersion` | `Customer.RowVersion` | `Student.RowVersion` | `Client.RowVersion` | `Reader.RowVersion` | `Member.RowVersion` |

### Коміт

```bash
git add ClinicApp/Models/Patient.cs ClinicApp/Data/ClinicDbContext.cs ClinicApp/Data/DbSeeder.cs ClinicApp/Migrations/ ClinicApp/Program.cs
git commit -m "Lab19 Task04"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                                    ← гілка Lab-19 (після злиття — main)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs                             ✏ Т4
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/
    │   ├── Patient.cs                         ✏ Т3 Т4
    │   ├── Diagnosis.cs                       ✏ Т1
    │   ├── LabResult.cs                       ✏ Т1
    │   ├── MedicalRecord.cs                   ✏ Т1
    │   ├── Prescription.cs                    ✏ Т1
    │   ├── EmergencyContact.cs                🆕 Т3
    │   └── … ще 11 файлів без змін
    ├── Managers/  (13 файлів)
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    ├── Events/  (4 файли)
    ├── Extensions/  (3 файли)
    ├── UI/  (1 файл)
    ├── Data/
    │   ├── ClinicDbContext.cs                 ✏ Т2 Т3 Т4
    │   ├── DbSeeder.cs                        ✏ Т4
    │   └── ClinicRepository.cs
    └── Migrations/  (7 файлів — генерує EF)   ✏ Т4
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 18.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] У БД є таблиця `MedicalRecords` зі стовпцем `RecordType` і nullable-стовпцями підтипів
- [ ] У таблиці `Patients` є стовпці `EC_Name`, `EC_Phone`, `EC_Relationship` і `RowVersion`
- [ ] Після сідера в БД медичні записи всіх трьох типів
- [ ] На старті `DemoConcurrencyConflict()` показує успіх першої сесії і `DbUpdateConcurrencyException` другої
- [ ] Повторний запуск не дублює дані

---

## Питання для самоперевірки

1. **Nullable-стовпці TPH.** `DiagnosisCode`, `TestName`, `MedicationName` — nullable. Це порушення першої нормальної форми чи прийнятний компроміс?
2. **TPT як альтернатива.** Окремі таблиці для підтипів — без `NULL`, але з `JOIN` при завантаженні `MedicalRecord[]`. Де краще TPH, де TPT?
3. **Value Object.** `EmergencyContact` — value object у термінах DDD. Чим value object відрізняється від сутності (entity)?
4. **Оптимістичне чи песимістичне блокування.** Чим `RowVersion` відрізняється від блокування рядка на час редагування?
5. **Що робити в `catch (DbUpdateConcurrencyException)`** — перезавантажити дані чи повідомити користувача? Від чого залежить вибір?
6. **Валідація в сеттерах чи обмеження БД.** Сеттер `DiagnosisCode` не пропускає порожній рядок, а стовпець у БД — nullable. Хто відповідає за якість даних?

---

## Статус гілки

Після всіх 4 завдань (кожне — окремий коміт `Lab19 TaskNN` на гілці `Lab-19`):

```bash
git push -u origin Lab-19
git checkout main
git merge --no-ff Lab-19 -m "Merge Lab-19: EF Core Advanced"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-20`.
