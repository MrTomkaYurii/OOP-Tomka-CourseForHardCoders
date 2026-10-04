# Лаба 17 — Entity Framework Core: основи

## Мета

Підключити до проєкту реляційну базу даних через ORM Entity Framework Core: описати таблиці C#-класами, налаштувати відображення через Fluent API, перетворення складних типів (Value Conversion), створити схему БД міграцією і заповнити її початковими даними.

## Контекст

Досі клініка існує тільки в оперативній пам'яті: кожен запуск програми починається з нуля (сесія з Лаби 12 зберігає лише пацієнтів у текстовий файл). Реальна система потребує більшого: дані мають зберігатися між запусками, кілька користувачів мають бачити ті самі записи, пошук має масштабуватися до тисяч записів.

Найпоширеніше рішення — реляційна база даних. Працювати з нею напряму через SQL-рядки — це ручне формування запитів і ручне перетворення рядків таблиці в C#-об'єкти. **Object-Relational Mapper (ORM)** автоматизує цю роботу. **Entity Framework Core** — офіційний ORM від Microsoft: описує таблиці звичайними класами, сам генерує SQL, відстежує зміни об'єктів і керує схемою БД через **міграції**.

### Структура проєкту на початку лаби

Це результат Лаби 16 — стан `main` після її злиття:

```text
oop-course/                           ← гілка main (після злиття Лаби 16)
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
    │   └── … ще 14 файлів без змін
    ├── Managers/  (13 файлів)
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    ├── Events/  (4 файли)
    ├── Extensions/  (3 файли)
    └── UI/  (1 файл)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Ключові поняття EF Core

- **`DbContext`** — посередник між кодом і БД: підключається до бази (`OnConfiguring`), оголошує таблиці (`DbSet<T>`), описує правила відображення (`OnModelCreating`) і **відстежує зміни** — під час `SaveChanges()` сам формує `INSERT`, `UPDATE`, `DELETE`.
- **`DbSet<T>`** — «таблиця» в термінах C#. LINQ-запит до `DbSet` EF перетворює на SQL: `context.Patients.Where(p => p.LastName == "Коваль")` → `SELECT … WHERE LastName = 'Коваль'`.
- **Fluent API** — конфігурація відображення в `OnModelCreating` ланцюжком викликів. На відміну від атрибутів (`[Required]`), тримає налаштування БД **окремо від моделі**: модель лишається чистим доменним класом. У цій лабі використовуємо саме Fluent API.
- **Value Conversion** — правило, як зберегти C#-тип, що не має прямого відповідника в SQL: `enum BloodType` → рядок `"APositive"`, `struct WorkSchedule` → рядок `"8-17"`.
- **Міграція** — автоматично згенерований клас зі змінами схеми БД (методи `Up()` / `Down()`). Цикл роботи: змінили модель → `dotnet ef migrations add Назва` → `dotnet ef database update`.

### Що нового дозволено (і тільки воно)

- пакети EF Core і провайдер SQL Server (LocalDB);
- `DbContext`, `DbSet<T>`, Fluent API у `OnModelCreating`, `ValueConverter`;
- міграції (`dotnet ef`);
- `private set` і конструктор без параметрів для потреб EF.

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-17
```

Коміт — на кожне завдання (`Lab17 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. Пакети EF Core і `ClinicDbContext` ⭐⭐

### Умова

Підключіть EF Core до проєкту і налаштуйте з'єднання з локальною БД. Базовий пакет `Microsoft.EntityFrameworkCore` не знає ні про SQL Server, ні про SQLite — конкретний провайдер підключається окремим пакетом.

**Що реалізувати:**

1. Додати в `ClinicApp` три пакети версії `8.0.0` (під `net8.0`): `Microsoft.EntityFrameworkCore`, `Microsoft.EntityFrameworkCore.SqlServer`, `Microsoft.EntityFrameworkCore.Design`.
2. Один раз на комп'ютері встановити інструмент міграцій `dotnet-ef` (команда нижче).
3. Створити теку `ClinicApp/Data/` і клас `ClinicDbContext : DbContext` з таблицями `Patients` і `Doctors`.
4. У `OnConfiguring` підключитися до LocalDB рядком підключення зі специфікації.

### Специфікація

```bash
dotnet add ClinicApp package Microsoft.EntityFrameworkCore --version 8.0.0
dotnet add ClinicApp package Microsoft.EntityFrameworkCore.SqlServer --version 8.0.0
dotnet add ClinicApp package Microsoft.EntityFrameworkCore.Design --version 8.0.0
dotnet tool install --global dotnet-ef --version 8.0.0
```

| Член `ClinicDbContext` | Опис |
|------------------------|------|
| `DbSet<Patient> Patients` | таблиця пацієнтів |
| `DbSet<Doctor> Doctors` | таблиця лікарів |
| `OnConfiguring(...)` | `UseSqlServer(рядок підключення)` |

Рядок підключення до LocalDB:

```
Server=(localdb)\mssqllocaldb;Database=ClinicApp;Trusted_Connection=True;TrustServerCertificate=True;
```

### Приклад

```xml
<ItemGroup>
  <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.0" />
  <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />
  <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.0" />
</ItemGroup>
```

### Підказки

1. Версія EF Core має збігатися з версією .NET у `ClinicApp.csproj`: `net8.0` → `8.0.x`.
2. `dotnet-ef` — глобальний інструмент командного рядка, а не пакет проєкту: без нього команда `dotnet ef` не знайдеться. Перевірка: `dotnet ef --version`.
3. **LocalDB** — вбудований SQL Server для розробки (ставиться разом із Visual Studio); запускається автоматично при першому підключенні.
4. `UseSqlServer` — метод розширення з пакета провайдера: саме тому він з'являється лише після встановлення `…SqlServer`.

📖 Документація:
- [EF Core: початок роботи](https://learn.microsoft.com/ef/core/get-started/overview/first-app)
- [`DbContext`: налаштування](https://learn.microsoft.com/ef/core/dbcontext-configuration/)
- [Інструмент `dotnet ef`](https://learn.microsoft.com/ef/core/cli/dotnet)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `ClinicDbContext` | `HotelDbContext` | `RestaurantDbContext` | `UniversityDbContext` | `RentalDbContext` | `LibraryDbContext` | `GymDbContext` |
| `Patients`, `Doctors` | `Guests`, `Staff` | `Customers`, `Waiters` | `Students`, `Lecturers` | `Clients`, `Managers` | `Readers`, `Librarians` | `Members`, `Trainers` |

### Коміт

```bash
git add ClinicApp/ClinicApp.csproj ClinicApp/Data/ClinicDbContext.cs
git commit -m "Lab17 Task01"
```

---

## Задача 2. Відображення `Patient` через Fluent API ⭐⭐

### Умова

Опишіть, як клас `Patient` зберігається в таблиці `Patients`. Спершу підготуйте сам клас до роботи з EF, потім налаштуйте відображення в `OnModelCreating`.

**Що реалізувати:**

1. У `Patient` змінити `Id` на `{ get; private set; }`: EF має записати в нього значення з БД після `INSERT`, а ззовні змінити `Id` і далі неможливо.
2. Переконатися, що в `Patient` є конструктор без параметрів (з Лаби 03) — EF використовує його, завантажуючи об'єкт із БД.
3. У `ClinicDbContext.OnModelCreating` налаштувати `Patient` за специфікацією.

### Специфікація

| Що | Налаштування |
|----|--------------|
| Таблиця | `Patients` |
| Ключ | `Id`, значення генерує БД (IDENTITY); значення з лічильника `_nextId` при вставці ігнорується |
| `FirstName`, `LastName` | обов'язкові, до 100 символів |
| `Phone` | до 10 символів |
| `Email` | до 100 символів |
| `BloodType` | зберігається **рядком** (`"APositive"`), а не числом |
| Індекс | за `LastName`, ім'я `IX_Patients_LastName` |

### Приклад

```csharp
modelBuilder.Entity<Patient>(entity =>
{
    entity.ToTable("Patients");
    entity.HasKey(p => p.Id);
    entity.Property(p => p.FirstName).HasMaxLength(100).IsRequired();
    // … решта за специфікацією
});
```

### Підказки

1. `ValueGeneratedOnAdd()` означає «значення генерує БД під час `INSERT`» — це і є IDENTITY в SQL Server.
2. **Пастка з лічильником.** Конструктор `Patient` уже присвоює `Id` з `_nextId`. Побачивши ненульовий `Id`, EF спробує вставити його явно — і SQL Server відмовить (вставка в IDENTITY-стовпець вимкнена). Скажіть EF ігнорувати клієнтське значення при вставці: `Metadata.SetBeforeSaveBehavior(PropertySaveBehavior.Ignore)` для властивості `Id`.
3. Enum без перетворення зберігається числом (0, 1, 2…): змінили порядок значень — дані в БД стали некоректними. `HasConversion<string>()` зберігає назву.
4. `HasKey` можна не писати — EF знайде `Id` за іменем. Але явна конфігурація читається краще.

📖 Документація:
- [Fluent API: конфігурація моделі](https://learn.microsoft.com/ef/core/modeling/)
- [Згенеровані значення](https://learn.microsoft.com/ef/core/modeling/generated-properties)
- [Явні значення для згенерованих властивостей](https://learn.microsoft.com/ef/core/saving/explicit-values-generated-properties)
- [Перетворення значень](https://learn.microsoft.com/ef/core/modeling/value-conversions)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `Patient` → `Patients`, `BloodType` рядком | `Guest` → `Guests`, `RoomType` рядком | `Customer` → `Customers`, `DishCategory` рядком | `Student` → `Students`, `Faculty` рядком | `Client` → `Clients`, `CarClass` рядком | `Reader` → `Readers`, `BookGenre` рядком | `Member` → `Members`, `FitnessLevel` рядком |

### Коміт

```bash
git add ClinicApp/Data/ClinicDbContext.cs ClinicApp/Models/Patient.cs
git commit -m "Lab17 Task02"
```

---

## Задача 3. Відображення `Doctor` і перетворення `WorkSchedule` ⭐⭐⭐

### Умова

Опишіть відображення `Doctor`. Особлива частина — розклад `WorkSchedule`: зберігати двопольну структуру окремою таблицею надлишково, тому збережіть її **одним рядком** `"8-17"` і відновлюйте назад при читанні.

**Що реалізувати:**

1. Підготувати `Doctor` так само, як `Patient`: `Id { get; private set; }`, конструктор без параметрів.
2. Налаштувати `Doctor` у `OnModelCreating` за специфікацією.
3. Для `Schedule` створити `ValueConverter<WorkSchedule, string>`: розклад → `"Start-End"` і назад. Зворотний розбір винести в окремий статичний метод.

### Специфікація

| Що | Налаштування |
|----|--------------|
| Таблиця | `Doctors` |
| Ключ | `Id`, IDENTITY; значення з `_nextId` ігнорується (як у `Patient`) |
| `FirstName`, `LastName`, `LicenseNumber` | обов'язкові, до 100 символів |
| `Phone` | до 10 символів |
| `Speciality` | рядком |
| `Schedule` | один рядок `"8-17"` через `ValueConverter` |

### Приклад

```
Doctors
Id | FirstName | LastName  | Speciality | Schedule
 1 | Олег      | Сидоренко | Cardiology | 8-16
```

### Підказки

1. **Чому окремий метод для розбору.** Лямбди в `HasConversion` компілюються в **дерева виразів** — обмежену підмножину C#. Виклики з необов'язковими параметрами (як `int.Parse` з `IFormatProvider`) там можуть не компілюватися (помилка `CS0854`). Статичний метод розбору, викликаний із лямбди конвертера, цю проблему знімає.
2. `ValueConverter<TModel, TProvider>` — окремий об'єкт: перший аргумент перетворює модель у значення для БД, другий — назад. Передайте його в `HasConversion(converter)`.
3. Розбір: розділити рядок за `-`, перетворити дві частини на числа і створити `WorkSchedule` — валідація з Лаби 05 спрацює автоматично.

📖 Документація:
- [Перетворення значень](https://learn.microsoft.com/ef/core/modeling/value-conversions)
- [Дерева виразів](https://learn.microsoft.com/dotnet/csharp/advanced-topics/expression-trees/)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `WorkSchedule` → `"8-17"` | `BookingPeriod` → `"14-12"` | `ServiceHours` → `"10-23"` | `LectureSlot` → `"9-11"` | `RentalPeriod` → `"9-18"` | `ShiftSchedule` → `"9-18"` | `TrainingSlot` → `"7-9"` |

### Коміт

```bash
git add ClinicApp/Data/ClinicDbContext.cs ClinicApp/Models/Doctor.cs
git commit -m "Lab17 Task03"
```

---

## Задача 4. Міграція і `DbSeeder` ⭐⭐

### Умова

Створіть схему БД міграцією і заповніть її початковими даними. Початкові дані — окремий клас, а не `Program.cs`: `Program.cs` керує навігацією, а сідер відповідає за початковий стан БД.

**Що реалізувати:**

1. Створити першу міграцію `InitialCreate` і застосувати її до БД (команди нижче). Відкрити згенерований клас і переконатися, що `Up()` створює таблиці за вашою конфігурацією.
2. Створити статичний клас `DbSeeder` у `ClinicApp/Data/` з методом `Seed(ClinicDbContext context)`: додає 5 пацієнтів і 5 лікарів різних спеціальностей і зберігає зміни.
3. Сідер **ідемпотентний**: якщо пацієнти в БД уже є — нічого не додає.
4. У `Program.cs` на старті створити контекст і викликати `DbSeeder.Seed`.

### Специфікація

```bash
dotnet ef migrations add InitialCreate --project ClinicApp
dotnet ef database update --project ClinicApp
```

| Член `DbSeeder` | Опис |
|-----------------|------|
| `Seed(ClinicDbContext context)` | якщо таблиця `Patients` не порожня — вихід; інакше 5 пацієнтів + 5 лікарів, `SaveChanges()` |

### Приклад

```
SELECT Id, FirstName, LastName, BloodType FROM Patients;
1 | Іван   | Петренко | APositive
2 | Олена  | Коваль   | BNegative
…
```

### Підказки

1. Перевірку «чи є дані» робіть через `Any()` — він генерує `SELECT TOP 1`, а не завантажує всю таблицю.
2. Контекст створюйте з `using`: він тримає з'єднання з БД і має бути звільнений.
3. **Не використовуйте `Database.EnsureCreated()`** разом із міграціями: БД, створену так, наступна міграція спробує створити ще раз і впаде. Схему створює лише `dotnet ef database update`.
4. Дані перевірте через SQL Server Object Explorer у Visual Studio.

📖 Документація:
- [Міграції: огляд](https://learn.microsoft.com/ef/core/managing-schemas/migrations/)
- [Заповнення даними](https://learn.microsoft.com/ef/core/modeling/data-seeding)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| 5 пацієнтів + 5 лікарів | 5 гостей + 5 працівників | 5 клієнтів + 5 офіціантів | 5 студентів + 5 викладачів | 5 клієнтів + 5 менеджерів | 5 читачів + 5 бібліотекарів | 5 учасників + 5 тренерів |

### Коміт

```bash
git add ClinicApp/Data/DbSeeder.cs ClinicApp/Migrations/ ClinicApp/Program.cs
git commit -m "Lab17 Task04"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                                   ← гілка Lab-17 (після злиття — main)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj                      ✏ Т1
    ├── Program.cs                            ✏ Т4
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/
    │   ├── Patient.cs                        ✏ Т2
    │   ├── Doctor.cs                         ✏ Т3
    │   └── … ще 14 файлів без змін
    ├── Managers/  (13 файлів)
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    ├── Events/  (4 файли)
    ├── Extensions/  (3 файли)
    ├── UI/  (1 файл)
    ├── Data/
    │   ├── ClinicDbContext.cs                🆕 Т1  ✏ Т2 Т3
    │   └── DbSeeder.cs                       🆕 Т4
    └── Migrations/  (3 файли — генерує EF)   🆕 Т4
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 16.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] `dotnet ef --version` показує версію 8.0.x
- [ ] У БД `ClinicApp` є таблиці `Patients`, `Doctors` і `__EFMigrationsHistory`
- [ ] `BloodType` і `Speciality` збережені рядками, `Schedule` — рядком виду `8-17`
- [ ] Після першого запуску в БД 5 пацієнтів і 5 лікарів; після повторного — так само 5 (сідер ідемпотентний)
- [ ] У коді немає `EnsureCreated()`

---

## Питання для самоперевірки

1. **Unit of Work.** Усі зміни в одному `DbContext` зберігаються разом через `SaveChanges()`. Як це пов'язано з транзакціями в БД?
2. **Fluent API чи атрибути.** Атрибути (`[Required]`, `[MaxLength]`) простіші, але змішують модель із деталями БД. Коли ви обрали б атрибути?
3. **Пошкоджені дані.** Конструктор `WorkSchedule` перевіряє `start < end`. Що станеться, якщо в БД рядок `"17-8"`? Як від цього захиститись?
4. **Два лічильники.** `_nextId` у `Patient` і IDENTITY у БД рахують незалежно. Чому EF має ігнорувати значення з лічильника при вставці? Що було б без цього?
5. **Міграція як версія схеми.** Що буде, якщо один розробник застосував міграцію `AddAppointments`, а інший ні — і обидва запускають програму з однією БД?
6. **`using var context`.** Чому `DbContext` реалізує `IDisposable`? Чи зберігаються незбережені зміни під час `Dispose()`?

---

## Статус гілки

Після всіх 4 завдань (кожне — окремий коміт `Lab17 TaskNN` на гілці `Lab-17`):

```bash
git push -u origin Lab-17
git checkout main
git merge --no-ff Lab-17 -m "Merge Lab-17: EF Core Basics"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-18`.
