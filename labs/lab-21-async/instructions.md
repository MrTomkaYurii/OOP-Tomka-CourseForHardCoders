# Лаба 21 — Async / Await

## Мета

Навчитися писати асинхронний код: `async`/`await` з EF Core, скасування через `CancellationToken`, паралельне виконання задач (`Task.WhenAll`, `Task.WhenAny`, `Parallel.ForEachAsync`), обробку помилок паралельних задач, звітування про прогрес (`IProgress<T>`) і асинхронні HTTP-запити.

## Контекст

У Лабах 17–20 код був синхронним навмисно — щоб було видно, що відбувається:

```csharp
var patients = context.Patients.ToList();   // потік ЗАБЛОКОВАНИЙ ~50 мс
var doctors  = context.Doctors.ToList();    // потік ЗАБЛОКОВАНИЙ ~50 мс
```

Тепер уявіть 100 одночасних запитів у вебзастосунку: кожен блокує потік, пул потоків вичерпується, нові запити стають у чергу — застосунок «провисає». **Рішення — `async`/`await`:** не блокувати потік, а звільняти його на час очікування введення-виведення.

```csharp
var patients = await context.Patients.ToListAsync();   // потік ВІЛЬНИЙ під час очікування
```

### Структура проєкту на початку лаби

Це результат Лаби 20 — стан `main` після її злиття:

```text
oop-course/                                    ← гілка main (після злиття Лаби 20)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/  (19 файлів)
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
    │   ├── ClinicRepository.cs
    │   └── ClinicQueryService.cs
    └── Migrations/  (9 файлів — генерує EF)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Ключові поняття

- **`async` / `await`.** `async` — «метод може містити `await`»; `await` — «призупини метод, звільни потік, продовж, коли задача завершиться». Типи результату: `void` → `async Task`, `T` → `async Task<T>`. `async void` допустимий лише для обробників подій: його виняток неможливо перехопити ззовні, і на нього неможливо чекати.
- **`CancellationToken`** — сигнал ззовні «скасуй операцію». При скасуванні кидається `OperationCanceledException` — його ловлять окремо від інших винятків.
- **`Task.WhenAll`** — запустити кілька задач одночасно і дочекатися всіх: час ≈ найдовша, а не сума. **`Task.WhenAny`** — дочекатися першої (гонка, таймаут).
- **`Parallel.ForEachAsync`** — паралельна обробка колекції з обмеженням кількості одночасних задач.
- **`DbContext` не потокобезпечний.** Два одночасні запити через **один** контекст кидають `InvalidOperationException`. Паралельні запити до БД — кожен через **свій** контекст; паралельна обробка в пам'яті — лише над уже завантаженими об'єктами.
- **`AggregateException`.** `await Task.WhenAll(...)` при кількох помилках кидає лише **першу**; усі доступні через `Exception.InnerExceptions` самої задачі.
- **`IProgress<T>`** — спосіб повідомляти про прогрес, не знаючи, хто і як його показує.

### Що нового дозволено (і тільки воно)

- `async` / `await`, `Task`, `Task<T>`, async-методи EF Core (`ToListAsync`, `CountAsync`, `SaveChangesAsync` …);
- `CancellationToken`, `CancellationTokenSource`;
- `Task.WhenAll`, `Task.WhenAny`, `Task.Delay`, `Parallel.ForEachAsync`, `Interlocked`;
- `ContinueWith`;
- `IProgress<T>` / `Progress<T>`;
- `HttpClient`, `System.Net.Http.Json`, `[JsonPropertyName]`.

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-21
```

Коміт — на кожне завдання (`Lab21 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. Асинхронний сідер ⭐

### Умова

Побачте, як `async`/`await` поширюється від точки входу вниз по стеку викликів: переведіть сідер на асинхронні методи EF.

**Що реалізувати:**

1. У `DbSeeder` додати `SeedAsync(ClinicDbContext context, CancellationToken ct = default)`.
2. Кожен приватний крок перевести на асинхронний (`SeedPatients` → `SeedPatientsAsync` тощо): `Any()` → `AnyAsync(ct)`, `SaveChanges()` → `SaveChangesAsync(ct)`.
3. У `Program.cs` викликати `await DbSeeder.SeedAsync(...)`.

### Специфікація

| Було | Стало |
|------|-------|
| `static void Seed(ClinicDbContext context)` | `static async Task SeedAsync(ClinicDbContext context, CancellationToken ct = default)` |
| `context.Patients.Any()` | `await context.Patients.AnyAsync(ct)` |
| `context.SaveChanges()` | `await context.SaveChangesAsync(ct)` |

### Приклад

```csharp
await DbSeeder.SeedAsync(context);   // у Program.cs, прямо на верхньому рівні
```

### Підказки

1. `Program.cs` з top-level statements: щойно в ньому з'являється `await`, компілятор сам створює `async Task Main`.
2. `CancellationToken ct = default` — «токен, який ніколи не скасовується»: викликати можна і без нього.

📖 Документація:
- [Асинхронне програмування](https://learn.microsoft.com/dotnet/csharp/asynchronous-programming/)
- [Асинхронні запити EF Core](https://learn.microsoft.com/ef/core/miscellaneous/async)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `SeedPatientsAsync`, `SeedDoctorsAsync` … | `SeedGuestsAsync` … | `SeedCustomersAsync` … | `SeedStudentsAsync` … | `SeedClientsAsync` … | `SeedReadersAsync` … | `SeedMembersAsync` … |

### Коміт

```bash
git add ClinicApp/Data/DbSeeder.cs ClinicApp/Program.cs
git commit -m "Lab21 Task01"
```

---

## Задача 2. `AsyncClinicService`: асинхронні операції EF ⭐⭐

### Умова

Створіть сервіс з асинхронними версіями типових операцій і додайте асинхронні варіанти в репозиторій.

**Що реалізувати:**

1. Клас `AsyncClinicService` у `ClinicApp/Data/` з конструктором `(ClinicDbContext context)` і чотирма методами зі специфікації — кожен `await`-ить асинхронний метод EF.
2. У `ClinicRepository` додати `GetPatientWithAppointmentsAsync` і `GetUpcomingAppointmentsAsync`.
3. У методах репозиторію використати `ConfigureAwait(false)` і пояснити в коментарі, навіщо.

### Специфікація

| Клас | Метод | Повертає |
|------|-------|----------|
| `AsyncClinicService` | `GetAllPatientsAsync(CancellationToken ct = default)` | `Task<List<Patient>>` |
| `AsyncClinicService` | `GetPatientByIdAsync(int id, CancellationToken ct = default)` | `Task<Patient?>` |
| `AsyncClinicService` | `GetUpcomingAppointmentsAsync(CancellationToken ct = default)` | `Task<List<Appointment>>` |
| `AsyncClinicService` | `SaveAppointmentAsync(Appointment a, CancellationToken ct = default)` | `Task<int>` — кількість збережених рядків |
| `ClinicRepository` | `GetPatientWithAppointmentsAsync(int id, CancellationToken ct = default)` | `Task<Patient?>` |
| `ClinicRepository` | `GetUpcomingAppointmentsAsync(CancellationToken ct = default)` | `Task<List<Appointment>>` |

### Приклад

```csharp
var service = new AsyncClinicService(context);
Patient? p = await service.GetPatientByIdAsync(1);
```

### Підказки

1. Токен передавайте далі в кожен асинхронний метод EF — інакше скасування до БД не дійде.
2. `async`-метод без жодного `await` компілюється з попередженням і виконується синхронно.
3. `.Result` замість `await` блокує потік і в застосунках із `SynchronizationContext` може призвести до взаємоблокування.

📖 Документація:
- [`ConfigureAwait` FAQ](https://devblogs.microsoft.com/dotnet/configureawait-faq/)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `AsyncClinicService` | `AsyncHotelService` | `AsyncRestaurantService` | `AsyncUniversityService` | `AsyncRentalService` | `AsyncLibraryService` | `AsyncGymService` |

### Коміт

```bash
git add ClinicApp/Data/AsyncClinicService.cs ClinicApp/Data/ClinicRepository.cs
git commit -m "Lab21 Task02"
```

---

## Задача 3. Паралельні задачі і скасування ⭐⭐⭐

### Умова

Додайте в `AsyncClinicService` чотири методи, кожен демонструє окремий інструмент: паралельні запити, таймаут, паралельну обробку колекції і скасування. Покажіть їх роботу в `Program.cs`.

**Що реалізувати:**

1. `record ClinicDashboard` у `ClinicApp/Models/` (поля нижче).
2. `GetDashboardAsync()` — п'ять значень дашборда **одночасно** через `Task.WhenAll`; **кожен** запит — через **окремий** `ClinicDbContext`.
3. `GetDashboardWithTimeoutAsync(int timeoutMs)` — гонка дашборда з `Task.Delay(timeoutMs)` через `Task.WhenAny`; при таймауті — `null`.
4. `MarkAppointmentsAsPaidAsync(IEnumerable<int> ids, CancellationToken ct)` — завантажити записи одним запитом, позначити оплаченими паралельно в пам'яті (`Parallel.ForEachAsync`, лічильник через `Interlocked.Increment`), зберегти **одним** `SaveChangesAsync` після циклу.
5. `SearchPatientsAsync(string query, CancellationToken ct)` — пошук за прізвищем із штучною затримкою `Task.Delay(200, ct)`.
6. У `Program.cs` показати: дашборд, таймаут, оплату списку записів і скасування пошуку токеном зі строком 100 мс з перехопленням `OperationCanceledException`.

### Специфікація

| `ClinicDashboard` | Як рахується |
|-------------------|--------------|
| `PatientCount` | `CountAsync` пацієнтів |
| `DoctorCount` | `CountAsync` лікарів |
| `TotalRevenue` | сума `GetCost()` оплачених записів — у пам'яті, після завантаження |
| `UpcomingCount` | записи в майбутньому зі статусом `Scheduled` |
| `TodayCount` | записи на сьогодні |

### Приклад

```
Дашборд: пацієнтів 5, лікарів 5, виручка 1230.00 грн, майбутніх 2, сьогодні 1
Дашборд з таймаутом 1 мс: таймаут
Оплачено записів: 3
Пошук скасовано (таймаут токена).
```

### Підказки

1. **Один контекст — одна операція за раз.** Запустивши п'ять запитів через спільний контекст, отримаєте `InvalidOperationException` («A second operation was started on this context»). Для `GetDashboardAsync` створюйте окремий контекст у кожній з п'яти задач (у `using`).
2. **`GetCost()` не перекладається в SQL** (Лаба 18): `TotalRevenue` — це окрема асинхронна функція, що завантажує оплачені записи і рахує суму в пам'яті.
3. Після `Task.WhenAll` результати задач читайте через `await` або `.Result` — задачі вже завершені.
4. Програвша в `WhenAny` задача **не зупиняється сама** — вона продовжує працювати у фоні.
5. У `Parallel.ForEachAsync` не звертайтесь до `DbContext` — лише до вже завантажених об'єктів. `count++` з кількох потоків губить збільшення — тому `Interlocked.Increment`.

📖 Документація:
- [`Task.WhenAll`](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task.whenall)
- [`Task.WhenAny`](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task.whenany)
- [`Parallel.ForEachAsync`](https://learn.microsoft.com/dotnet/api/system.threading.tasks.parallel.foreachasync)
- [Скасування задач](https://learn.microsoft.com/dotnet/standard/parallel-programming/task-cancellation)
- [Час життя `DbContext` і потоки](https://learn.microsoft.com/ef/core/dbcontext-configuration/#avoiding-dbcontext-threading-issues)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `ClinicDashboard` | `HotelDashboard` | `RestaurantDashboard` | `UniversityDashboard` | `RentalDashboard` | `LibraryDashboard` | `GymDashboard` |

### Коміт

```bash
git add ClinicApp/Models/ClinicDashboard.cs ClinicApp/Data/AsyncClinicService.cs ClinicApp/Program.cs
git commit -m "Lab21 Task03"
```

---

## Задача 4. Помилки паралельних задач ⭐⭐⭐

### Умова

Зберіть звіт про пацієнта з чотирьох паралельних задач і обробіть їхні помилки двома способами — побачте різницю між «першою помилкою» і «всіма помилками».

**Що реалізувати:**

1. У `AsyncClinicService.cs` оголосити `record PatientReport` (поля нижче).
2. Метод `BuildPatientReportAsync(int patientId)` — чотири задачі паралельно, кожна через **власний** контекст.
3. Обробити помилки двома способами: продовження `ContinueWith` з `OnlyOnFaulted`, що виводить **усі** `InnerExceptions`, і `try/catch` навколо `await`, що отримує лише **першу** помилку.
4. Після завершення вивести стан кожної задачі (`IsCompletedSuccessfully`, `IsFaulted`, `IsCanceled`).
5. У `Program.cs` викликати звіт для існуючого і для неіснуючого `patientId`.

### Специфікація

| `PatientReport` | Задача |
|-----------------|--------|
| `Patient` | пацієнт за `Id` (немає — виняток) |
| `RecentAppointments` | останні 5 записів пацієнта |
| `MedicalRecords` | медичні записи пацієнта |
| `Dashboard` | `GetDashboardAsync()` |

### Приклад

```
Звіт для пацієнта #99:
  [усі помилки] Пацієнта #99 не знайдено.
  [перша помилка] Пацієнта #99 не знайдено.
  Задача пацієнта: Faulted; записів: RanToCompletion; медкартки: RanToCompletion; дашборда: RanToCompletion
```

### Підказки

1. `await Task.WhenAll(...)` розгортає `AggregateException` і кидає лише першу з помилок — так зручніше в типовому коді.
2. Щоб побачити всі помилки, потрібна сама задача `Task.WhenAll(...)` (не `await`), а її `Exception.InnerExceptions` — у продовженні.
3. Скасована задача має стан `IsCanceled`, а не `IsFaulted`.

📖 Документація:
- [Обробка винятків задач](https://learn.microsoft.com/dotnet/standard/parallel-programming/exception-handling-task-parallel-library)
- [`TaskContinuationOptions`](https://learn.microsoft.com/dotnet/api/system.threading.tasks.taskcontinuationoptions)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `PatientReport` | `GuestReport` | `CustomerReport` | `StudentReport` | `ClientReport` | `ReaderReport` | `MemberReport` |

### Коміт

```bash
git add ClinicApp/Data/AsyncClinicService.cs ClinicApp/Program.cs
git commit -m "Lab21 Task04"
```

---

## Задача 5. Прогрес через `IProgress<T>` ⭐⭐

### Умова

Масова зміна статусу записів триває довго. Нехай метод повідомляє про прогрес, не знаючи, де і як його покажуть, і підтримує скасування.

**Що реалізувати:**

1. У `AsyncClinicService` метод `BulkProcessAppointmentsAsync` (сигнатура нижче): для кожного запису змінює статус, звітує про прогрес, перевіряє скасування, імітує обробку затримкою 80 мс; повертає кількість оброблених.
2. У `Program.cs` викликати його з `Progress<T>`, що виводить `[i/N] повідомлення`.
3. *(За бажанням)* показати той самий прогрес через `AnsiConsole.Progress()` зі Spectre.Console (Лаба 16).

### Специфікація

```
Task<int> BulkProcessAppointmentsAsync(
    AppointmentStatus newStatus,
    IProgress<(int Current, int Total, string Message)>? progress = null,
    CancellationToken ct = default)
```

| На кожній ітерації | |
|--------------------|--|
| `ct.ThrowIfCancellationRequested()` | явна перевірка скасування |
| `await Task.Delay(80, ct)` | імітація обробки |
| `progress?.Report((i + 1, total, опис запису))` | звіт про прогрес; без `progress` — нічого |

### Приклад

```
[1/4] Запис #1 → Completed
[2/4] Запис #2 → Completed
[3/4] Запис #3 → Completed
[4/4] Запис #4 → Completed
Оброблено: 4
```

### Підказки

1. `progress?.Report(...)` — безпечний виклик: метод працює і без того, хто стежить за прогресом.
2. `Progress<T>` викликає обробник через `SynchronizationContext`. У консолі його немає — обробник виконується в пулі потоків, тож рядки можуть з'явитися з невеликою затримкою.
3. Зміни статусу збережіть одним `SaveChangesAsync` після циклу.

📖 Документація:
- [`IProgress<T>`](https://learn.microsoft.com/dotnet/api/system.iprogress-1)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `BulkProcessAppointmentsAsync` | `BulkProcessBookingsAsync` | `BulkProcessReservationsAsync` | `BulkProcessEnrollmentsAsync` | `BulkProcessRentalsAsync` | `BulkProcessLoansAsync` | `BulkProcessSessionsAsync` |

### Коміт

```bash
git add ClinicApp/Data/AsyncClinicService.cs ClinicApp/Program.cs
git commit -m "Lab21 Task05"
```

---

## Задача 6. `ClinicHttpClient`: асинхронні HTTP-запити і JSON ⭐⭐⭐

### Умова

Отримайте довідку про препарат із публічного FDA Open API (реєстрація не потрібна) — асинхронно, з десеріалізацією JSON і коректною обробкою мережевих помилок і таймаутів.

**Що реалізувати:**

1. Клас `ClinicHttpClient` у `ClinicApp/Data/` з одним **статичним** `HttpClient` (таймаут 10 с).
2. У тому самому файлі — публічний `record DrugInfo` і приватні `record`-и для відповіді API з `[JsonPropertyName]`.
3. Три методи зі специфікації.
4. Обробка помилок: мережеву помилку і таймаут `HttpClient` — перехопити (повернути `null`); скасування через переданий токен — **не** перехоплювати.
5. У `Program.cs` запитати довідку про `Aspirin`, `Ibuprofen`, `Omeprazole`.

### Специфікація

Запит: `GET https://api.fda.gov/drug/label.json?search=openfda.brand_name:{назва}&limit=1`

| Метод | Повертає |
|-------|----------|
| `GetDrugInfoAsync(string drugName, CancellationToken ct = default)` | `Task<DrugInfo?>` — `null`, якщо не знайдено або помилка мережі/таймаут |
| `IsApiAvailableAsync(CancellationToken ct = default)` | `Task<bool>` |
| `GetDrugInfoWithRaceAsync(string drugName, int timeoutMs)` | `Task<DrugInfo?>` — гонка запиту з `Task.Delay(timeoutMs)`; програв запит — `null` |

| `DrugInfo` | З поля відповіді |
|------------|------------------|
| `Name` | `openfda.brand_name[0]` |
| `Purpose` | `purpose[0]` |
| `Warnings` | `warnings[0]` |
| `Dosage` | `dosage_and_administration[0]` |

| Виняток | Що робити |
|---------|-----------|
| `HttpRequestException` | мережева помилка — повернути `null` |
| `TaskCanceledException`, коли `ct` **не** скасовано | таймаут `HttpClient` — повернути `null` |
| `OperationCanceledException` від `ct` | не перехоплювати |

### Приклад

```
Aspirin: Pain reliever/fever reducer
  Warnings: Reye's syndrome: Children and teenagers who have or are recovering…
```

### Підказки

1. **Один `HttpClient` на застосунок.** Створення й знищення `HttpClient` на кожен запит вичерпує сокети ОС — тому поле `static readonly`, хоч `HttpClient` і реалізує `IDisposable`.
2. `GetFromJsonAsync<T>` = GET + десеріалізація JSON одним викликом (`using System.Net.Http.Json;`).
3. Назву препарату в URL екрануйте `Uri.EscapeDataString`.
4. Розрізнити таймаут `HttpClient` і скасування токеном допомагає фільтр винятку `when (!ct.IsCancellationRequested)`.

📖 Документація:
- [`HttpClient`: рекомендації](https://learn.microsoft.com/dotnet/fundamentals/networking/http/httpclient-guidelines)
- [`GetFromJsonAsync`](https://learn.microsoft.com/dotnet/api/system.net.http.json.httpclientjsonextensions.getfromjsonasync)
- [openFDA: drug label API](https://open.fda.gov/apis/drug/label/)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| FDA: препарати | API курсу валют | API рецептів | API розкладу | API довідника авто | Open Library API | API вправ |

### Коміт

```bash
git add ClinicApp/Data/ClinicHttpClient.cs ClinicApp/Program.cs
git commit -m "Lab21 Task06"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                                    ← гілка Lab-21 (після злиття — main)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs                             ✏ Т1 Т3 Т4 Т5 Т6
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/
    │   ├── ClinicDashboard.cs                 🆕 Т3
    │   └── … ще 19 файлів без змін
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
    │   ├── DbSeeder.cs                        ✏ Т1
    │   ├── ClinicRepository.cs                ✏ Т2
    │   ├── ClinicQueryService.cs
    │   ├── AsyncClinicService.cs              🆕 Т2  ✏ Т3 Т4 Т5
    │   └── ClinicHttpClient.cs                🆕 Т6
    └── Migrations/  (9 файлів — генерує EF)
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 20.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] Сідер працює асинхронно; у `Program.cs` — `await DbSeeder.SeedAsync(...)`
- [ ] `GetDashboardAsync` повертає всі п'ять значень без `InvalidOperationException` про паралельні операції
- [ ] Дашборд із таймаутом 1 мс повертає `null`
- [ ] Пошук із токеном на 100 мс завершується `OperationCanceledException`, програма не падає
- [ ] Звіт для неіснуючого пацієнта виводить помилку обома способами і стани задач
- [ ] Прогрес виводиться рядками `[i/N] …`
- [ ] Довідка FDA для трьох препаратів (без мережі — `null` без падіння)
- [ ] У коді немає `async void` (окрім обробників подій) і `.Result` на незавершених задачах

---

## Питання для самоперевірки

1. **Deadlock через `.Result`.** Чому `GetPatientsAsync().Result` у WinForms або старому ASP.NET може «зависнути»? Яку роль тут грають `SynchronizationContext` і `ConfigureAwait(false)`? Чому в ASP.NET Core цього немає?
2. **«Async всю дорогу».** Чому не можна зробити один метод асинхронним, а його виклик лишити синхронним через `.Result`?
3. **`DbContext` і потоки.** Чому паралельні запити через один контекст небезпечні? Як це вирішують у реальних застосунках (`IDbContextFactory<T>`)?
4. **`Task.WhenAll` чи `Parallel.ForEachAsync`.** Що буде з `Task.WhenAll(items.Select(ProcessAsync))` для 10 000 елементів? Навіщо `MaxDegreeOfParallelism`?
5. **`IProgress<T>` чи подія.** У чому перевага `IProgress<T>` перед подією для прогресу?
6. **Вичерпання сокетів.** Що відбувається на рівні ОС, якщо 1000 разів за секунду створювати і знищувати `HttpClient`? Як це вирішує `IHttpClientFactory`?

---

## Статус гілки

Після всіх 6 завдань (кожне — окремий коміт `Lab21 TaskNN` на гілці `Lab-21`):

```bash
git push -u origin Lab-21
git checkout main
git merge --no-ff Lab-21 -m "Merge Lab-21: Async/Await"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-22`.
