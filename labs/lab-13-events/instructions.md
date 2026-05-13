# Лаба 13 — Events & Delegates (Події та делегати)

## Мета

Навчитись оголошувати власні `EventArgs`, підіймати події в менеджерах через `event EventHandler<T>`, підписувати кілька незалежних обробників на одну подію та спостерігати як система реагує автоматично — без явних викликів у меню.

## Контекст

Після Lab 12 система вміє писати у файли. Але всі виклики `Logger.LogInfo(...)` зроблені **вручну** — студент сам пише рядок після кожної дії. Ця лаба робить логування та інші реакції **автоматичними**: менеджер підіймає подію → всі підписники спрацьовують самі, не знаючи одне про одного.

## Гілка

```bash
git checkout main
git pull
git checkout -b feature/events
```

---

## Завдання 1 — Один event, один обробник ⭐⭐

### Умова

Зрозуміти механіку: оголосити власний `EventArgs`, додати `event` до менеджера, підписати простий метод-обробник і побачити що він спрацьовує автоматично.

### Що реалізувати

**`Events/AppointmentEventArgs.cs`** — новий файл:

```csharp
namespace YourApp.Events;

public class AppointmentEventArgs : EventArgs
{
    public int AppointmentId { get; }
    public int PatientId     { get; }
    public int DoctorId      { get; }
    public DateTime ScheduledAt { get; }
    public string Notes      { get; }

    public AppointmentEventArgs(int id, int patientId, int doctorId, DateTime at, string notes = "")
    {
        AppointmentId = id;
        PatientId     = patientId;
        DoctorId      = doctorId;
        ScheduledAt   = at;
        Notes         = notes;
    }
}
```

**`Managers/AppointmentManager.cs`** — додати поле події та підняти її в `Book()`:

```csharp
public event EventHandler<AppointmentEventArgs>? AppointmentBooked;

// у методі Book(), після успішного створення запису:
AppointmentBooked?.Invoke(this, new AppointmentEventArgs(
    appointment.Id, patientId, doctorId, scheduledAt));
```

**`Program.cs`** — підписати статичний метод:

```csharp
clinic.Appointments.AppointmentBooked += OnAppointmentBookedConsole;

// ...

static void OnAppointmentBookedConsole(object? sender, AppointmentEventArgs e)
{
    Console.WriteLine($"  [EVENT] Запис #{e.AppointmentId} створено — пацієнт {e.PatientId}, лікар {e.DoctorId}");
}
```

**Перевірка:** запишіть пацієнта через меню → рядок `[EVENT]` з'являється автоматично після підтвердження.

### Підказки

1. `EventArgs` — базовий клас для всіх аргументів події. Власний клас наслідує його і додає потрібні властивості.
2. `event EventHandler<T>?` — поле-подія. `?` означає що підписників може не бути. **Ніколи** не викликай подію без `?.Invoke` — `NullReferenceException` якщо підписників нема.
3. `?.Invoke(this, args)` — `this` є відправником (`sender`), `args` — дані події.
4. Обробник **зобов'язаний** мати сигнатуру `(object? sender, TEventArgs e)` — це вимога `EventHandler<T>`.
5. `+=` — підписка. Один метод можна підписати лише один раз на одну подію (якщо підписати двічі — спрацює двічі).
6. [EventHandler<T> — docs](https://learn.microsoft.com/en-us/dotnet/api/system.eventhandler-1)
7. [Events — C# docs](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/events/)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `AppointmentEventArgs` | `BookingEventArgs` | `ReservationEventArgs` | `EnrollmentEventArgs` | `RentalEventArgs` | `LoanEventArgs` | `SessionEventArgs` |
| `AppointmentBooked` | `BookingCreated` | `ReservationMade` | `StudentEnrolled` | `RentalStarted` | `BookLoaned` | `SessionBooked` |

### Коміт

```bash
git add src/Events/AppointmentEventArgs.cs src/Managers/AppointmentManager.cs src/Program.cs
git commit -m "Lab13 Task1: add AppointmentEventArgs, AppointmentBooked event, console handler"
```

---

## Завдання 2 — Всі події + ClinicLogger як підписник ⭐⭐

### Умова

Розширити систему подій: додати ще три `EventArgs`, ще чотири події в менеджерах, перенести обробку в `ClinicLogger` і прибрати ручні `LogInfo` виклики з меню. Тепер логування відбувається **автоматично** — без жодного рядка в меню.

### Що реалізувати

**`Events/PatientEventArgs.cs`**, **`Events/PaymentEventArgs.cs`**, **`Events/TreatmentPlanEventArgs.cs`** — аналогічно Task 1.

**`Managers/AppointmentManager.cs`** — додати три нові події:

```csharp
public event EventHandler<AppointmentEventArgs>? AppointmentCancelled;
public event EventHandler<AppointmentEventArgs>? AppointmentCompleted;
public event EventHandler<AppointmentEventArgs>? UrgentAppointmentBooked;
```

Підняти у відповідних методах (`Cancel`, `Complete`, `BookUrgent`). Для `BookUrgent` — підняти **обидві** події: `AppointmentBooked` і `UrgentAppointmentBooked` (одна дія — два сигнали).

**`Managers/PatientManager.cs`** — `PatientAdded` в `Add()`.

**`Managers/BillingManager.cs`** — `PaymentReceived` в `PayAppointment()`.

**`Managers/TreatmentPlanManager.cs`** — `PlanCompleted` + метод-обгортка:

```csharp
public event EventHandler<TreatmentPlanEventArgs>? PlanCompleted;

public bool Complete(int id)
{
    TreatmentPlan? plan = GetById(id);
    if (plan == null) return false;
    bool ok = plan.Complete();
    if (ok)
        PlanCompleted?.Invoke(this, new TreatmentPlanEventArgs(plan.Id, plan.PatientId, plan.Diagnosis));
    return ok;
}
```

**`Utils/ClinicLogger.cs`** — додати обробники-методи:

```csharp
public void OnPatientAdded(object? sender, PatientEventArgs e)
    => LogInfo($"Новий пацієнт #{e.PatientId}: {e.FullName}");

public void OnAppointmentBooked(object? sender, AppointmentEventArgs e)
    => LogInfo($"Запис #{e.AppointmentId}: пацієнт {e.PatientId} → лікар {e.DoctorId}");

// OnAppointmentCancelled, OnAppointmentCompleted, OnPaymentReceived, OnPlanCompleted — аналогічно

public void OnUrgentBooked(object? sender, AppointmentEventArgs e)
{
    LogWarning($"ТЕРМІНОВИЙ запис #{e.AppointmentId}: {e.Notes}");
    // Записати в окремий файл alerts/urgent_{дата}.txt
    string alertsDir = "alerts";
    Directory.CreateDirectory(alertsDir);
    string alertPath = Path.Combine(alertsDir, $"urgent_{DateTime.Today:yyyy-MM-dd}.txt");
    File.AppendAllText(alertPath, $"[{DateTime.Now:HH:mm:ss}] #{e.AppointmentId} | {e.Notes}\n", Encoding.UTF8);
}
```

**`Clinic.cs`** — підписати всі обробники в одному місці:

```csharp
private void SubscribeEvents()
{
    Patients.PatientAdded               += Logger.OnPatientAdded;
    Appointments.AppointmentBooked      += Logger.OnAppointmentBooked;
    Appointments.AppointmentCancelled   += Logger.OnAppointmentCancelled;
    Appointments.AppointmentCompleted   += Logger.OnAppointmentCompleted;
    Appointments.UrgentAppointmentBooked+= Logger.OnUrgentBooked;
    Billing.PaymentReceived             += Logger.OnPaymentReceived;
    TreatmentPlans.PlanCompleted        += Logger.OnPlanCompleted;
}
```

Викликати `SubscribeEvents()` в кінці конструктора.

**`Program.cs`** — прибрати ручні `LogInfo` виклики з меню де вони були. Обробник з Task 1 залишається (поки що два підписники на `AppointmentBooked`).

### Підказки

1. Два підписники на одну подію — обидва спрацюють. Перевір: при `BookUrgent` у `clinic.log` з'являється два рядки від `OnAppointmentBooked` і `OnUrgentBooked`, а також файл в `alerts/`.
2. `event` забороняє `=` ззовні класу — лише `+=` і `-=`. Спробуй написати `clinic.Appointments.AppointmentBooked = null` — отримаєш помилку компілятора. Саме для цього `event`, а не просто `delegate`.
3. `UrgentAppointmentBooked` і `AppointmentBooked` — різні поля. Підписник на одну не отримує сигнал від іншої. Але в `BookUrgent` ми самі підіймаємо обидві — це свідоме рішення.
4. [event keyword — C# docs](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/event)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `PatientAdded`, `PaymentReceived`, `PlanCompleted` | `GuestCheckedIn`, `PaymentReceived`, `ServiceCompleted` | `CustomerSeated`, `OrderPaid`, `SpecialOrderDone` | `StudentEnrolled`, `FeesPaid`, `ProjectSubmitted` | `ClientRegistered`, `PaymentReceived`, `CarReturned` | `ReaderRegistered`, `FinesPaid`, `BookRestored` | `MemberJoined`, `SessionPaid`, `ProgramCompleted` |

### Коміт

```bash
git add src/Events/ src/Managers/ src/Utils/ClinicLogger.cs src/Clinic.cs src/Program.cs
git commit -m "Lab13 Task2: add all EventArgs, wire events in all managers, ClinicLogger as subscriber"
```

---

## Завдання 3 — PatientPassportWriter ⭐⭐⭐

### Умова

Другий незалежний підписник на ті самі події. При реєстрації пацієнта та завершенні прийому або плану — автоматично генерується/оновлюється файл паспорту пацієнта.

### Структура паспорту `patients/passport_{id}.txt`

```
╔══════════════════════════════════════════════╗
║         МЕДИЧНА КАРТКА ПАЦІЄНТА             ║
╚══════════════════════════════════════════════╝
Згенеровано: 14.05.2026 10:30:15

── Особисті дані ─────────────────────────────
  ID:          1
  ПІБ:         Іван Петренко
  Дата нар.:   15.03.1985
  Вік:         41 р.
  Група крові: APositive
  Телефон:     0501234567

── Діагнози ──────────────────────────────────
  1. [10.04.2026] I10 — Гіпертонічна хвороба [хронічна]
  2. [09.04.2026] J06.9 — Гострий ринофарингіт

── Аналізи ───────────────────────────────────
  1. [07.04.2026] Гемоглобін: 145 г/л (норма: 120–160) ✓
  2. [07.04.2026] Холестерин: 6.2 ммоль/л (норма: < 5.2) ✗

── Рецепти ───────────────────────────────────
  1. [09.04.2026] Лізиноприл 10 мг × 30 дн. [активний]
       1 раз на добу вранці | до 09.05.2026

── Записи на прийом ──────────────────────────
  1. [15.05.2026 10:00] Лікар #1 | Звичайний прийом | Scheduled
  2. [15.05.2026 11:00] Лікар #2 | Терміновий | Completed

── Плани лікування ───────────────────────────
  1. #1 | Гіпертонічна хвороба | Active | 90 дн.

── Фінанси ───────────────────────────────────
  Заборгованість: 300,00 грн

══════════════════════════════════════════════
```

### Алгоритм `Write(int patientId)`

```
1. FindById(patientId) → якщо null, вийти
2. Відкрити StreamWriter(path, append: false) — завжди перезаписуємо
3. Записати заголовок + дату генерації
4. Секція "Особисті дані" — з Patient: Id, FullName, DateOfBirth, Age, BloodType, Phone
5. MedicalRecords.GetByPatient(patientId) → масив records
   5a. Цикл по records: if (records[i] is Diagnosis d) → секція "Діагнози"
   5b. Цикл по records: if (records[i] is LabResult lab) → секція "Аналізи", IsNormal → "✓"/"✗"
   5c. Цикл по records: if (records[i] is Prescription rx) → секція "Рецепти", IsActive() → "[активний]"
6. Appointments.GetByPatient(patientId) → секція "Записи на прийом"
   → GetDescription() для типу, Status для стану
7. TreatmentPlans.GetByPatient(patientId) → секція "Плани лікування"
8. Billing.GetPatientDebt(patientId) → секція "Фінанси"
9. Закрити (using — автоматично)
```

### Що реалізувати

**`Utils/PatientPassportWriter.cs`**:

```csharp
public class PatientPassportWriter
{
    private readonly Clinic _clinic;
    private readonly string _baseDir;

    public PatientPassportWriter(Clinic clinic, string baseDir = "patients")
    {
        _clinic = clinic;
        _baseDir = baseDir;
        Directory.CreateDirectory(baseDir);
    }

    public void OnPatientAdded(object? sender, PatientEventArgs e)    => Write(e.PatientId);
    public void OnAppointmentCompleted(object? sender, AppointmentEventArgs e) => Write(e.PatientId);
    public void OnPlanCompleted(object? sender, TreatmentPlanEventArgs e)      => Write(e.PatientId);

    private void Write(int patientId) { ... }
}
```

**`Clinic.cs`** — додати до `SubscribeEvents()`:

```csharp
Patients.PatientAdded              += Passport.OnPatientAdded;
Appointments.AppointmentCompleted  += Passport.OnAppointmentCompleted;
TreatmentPlans.PlanCompleted       += Passport.OnPlanCompleted;
```

**Перевірка:** зареєструй пацієнта → файл `patients/passport_N.txt` з'явився. Заверши прийом → файл оновився (дата генерації змінилась, прийом тепер Completed).

### Підказки

1. Три обробники → один приватний метод `Write(int patientId)`. Не дублюй логіку.
2. `is Diagnosis d` — патерн matching з оголошенням змінної. `records[i]` не є `Diagnosis` — ітерація продовжується.
3. `StreamWriter(path, append: false)` — **перезаписуємо** файл щоразу. Паспорт завжди актуальний.
4. Три незалежних цикли по одному масиві для трьох секцій — простіше ніж один складний.
5. `using StreamWriter w = new StreamWriter(...)` — без дужок блоку. Закриється при виході з методу.
6. Паспорт генерується при **кожному тригері** — навіть якщо змінилось одне поле. Це простіше ніж відстежувати що саме змінилось.

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `PatientPassportWriter` → `patients/passport_{id}.txt` | `GuestProfileWriter` → `guests/profile_{id}.txt` | `CustomerReceiptWriter` → `receipts/receipt_{id}.txt` | `StudentTranscriptWriter` → `students/transcript_{id}.txt` | `ClientContractWriter` → `clients/contract_{id}.txt` | `ReaderCardWriter` → `readers/card_{id}.txt` | `MemberCardWriter` → `members/card_{id}.txt` |

### Коміт

```bash
git add src/Utils/PatientPassportWriter.cs src/Clinic.cs
git commit -m "Lab13 Task3: add PatientPassportWriter, subscribe to PatientAdded/AppointmentCompleted/PlanCompleted"
```

---

## Завдання 4 — SessionEventTracker ⭐⭐⭐

### Умова

Третій незалежний підписник. Легковаговий клас в пам'яті, що рахує всі події за сесію, реагує на чергу при скасуванні і зберігає підсумок у файл при виході.

### Що реалізувати

**`Utils/SessionEventTracker.cs`**:

```csharp
public class SessionEventTracker
{
    private readonly Clinic _clinic;

    public int PatientsAdded         { get; private set; }
    public int AppointmentsBooked    { get; private set; }
    public int UrgentBooked          { get; private set; }
    public int AppointmentsCancelled { get; private set; }
    public int AppointmentsCompleted { get; private set; }
    public int PaymentsReceived      { get; private set; }
    public int PlansCompleted        { get; private set; }

    public void OnAppointmentCancelled(object? sender, AppointmentEventArgs e)
    {
        AppointmentsCancelled++;

        // Cross-domain реакція: скасовано слот → перевіряємо чергу
        if (!_clinic.WaitingRoom.IsEmpty)
        {
            var next = _clinic.WaitingRoom.Peek();
            Console.WriteLine($"  [!] Слот звільнився. Наступний у черзі: {next.FullName}");
        }
    }

    // решта обробників — просто збільшують лічильник

    public void PrintSummary() { ... }  // вивести в консоль при виході

    public void SaveSummary(string path = "session_summary.txt")
    {
        using StreamWriter writer = new StreamWriter(path, false, Encoding.UTF8);
        // записати всі лічильники у файл
    }
}
```

**`Clinic.cs`** — підписати всі обробники Tracker в `SubscribeEvents()`.

**`Program.cs`** — при виході (case "0") перед збереженням сесії:

```csharp
clinic.Tracker.PrintSummary();
clinic.Tracker.SaveSummary();
```

**Перевірка:**
- Додай 2 пацієнти, зроби 1 запис, скасуй його (а в черзі є пацієнт) → консоль: `[!] Слот звільнився. Наступний у черзі: ...`
- Вийди → `session_summary.txt` містить коректну статистику
- `clinic.log` містить всі ті ж події від Logger — обидва підписники спрацювали незалежно

### Підказки

1. `SessionEventTracker` підписаний **разом з Logger** на одні й ті ж події. Обидва спрацьовують — Logger пише у файл, Tracker інкрементує лічильник. Менеджери не знають про жодного з них.
2. `_clinic.WaitingRoom.IsEmpty` — Tracker має доступ до Clinic для cross-domain реакції. Це нормально — Tracker є частиною системи, просто не менеджером.
3. `-=` для відписки: `clinic.Appointments.AppointmentBooked -= OnAppointmentBookedConsole` — прибрати тимчасовий обробник з Task 1. Студент бачить що `event` підтримує як підписку так і відписку.
4. Спробуй ззовні написати `clinic.Appointments.AppointmentBooked = null` — компілятор забороняє. Тільки `+=` і `-=` доступні ззовні. Саме в цьому різниця між `event` і звичайним `delegate` полем.
5. [event vs delegate field — docs](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/events/how-to-implement-interface-events)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `SessionEventTracker` | `SessionEventTracker` | `SessionEventTracker` | `SessionEventTracker` | `SessionEventTracker` | `SessionEventTracker` | `SessionEventTracker` |
| WaitingRoom → наступний пацієнт | WaitingList → наступний гість | Waitlist → наступний столик | Waitlist → наступний студент | Queue → наступний клієнт | Queue → наступний читач | Queue → наступний член |
| `session_summary.txt` | однаково | однаково | однаково | однаково | однаково | однаково |

### Коміт

```bash
git add src/Utils/SessionEventTracker.cs src/Clinic.cs src/Program.cs
git commit -m "Lab13 Task4: add SessionEventTracker with queue reaction and session_summary.txt"
```

---

## Перевірка перед здачею

```bash
cd src
dotnet build
dotnet run
```

Переконайтесь, що:

- [ ] Зареєстрував пацієнта → `patients/passport_N.txt` з'явився з базовою інформацією
- [ ] Записав пацієнта через меню → `[EVENT]` рядок у консолі (Task 1) + рядок у `clinic.log` (Task 2) — два обробники одночасно
- [ ] Оформив терміновий запис → `clinic.log` має два рядки + файл `alerts/urgent_{дата}.txt` поповнився
- [ ] Завершив прийом → `patients/passport_N.txt` оновився: прийом тепер `Completed`, оновлено дату генерації
- [ ] Скасував запис (черга не порожня) → консоль: `[!] Слот звільнився. Наступний у черзі: ...`
- [ ] При виході → `session_summary.txt` містить коректну статистику сесії
- [ ] Спроба `clinic.Appointments.AppointmentBooked = null` → помилка компілятора (перевірити розуміння `event`)

---

## Питання для самоперевірки

1. Чому `?.Invoke(this, args)` а не просто `Invoke(this, args)`? Що станеться якщо підписників нема?
2. `event EventHandler<T>?` vs просто `EventHandler<T>?` як поле — яка різниця з точки зору доступу ззовні?
3. `AppointmentManager` не імпортує `ClinicLogger` і не знає про `PassportWriter`. Але обидва спрацьовують. Де відбувається зв'язок і чому це добре?
4. `BookUrgent` підіймає дві події: `AppointmentBooked` і `UrgentAppointmentBooked`. Logger підписаний на обидві. Скільки рядків у лозі після одного `BookUrgent`? Чому?
5. `SessionEventTracker.OnAppointmentCancelled` перевіряє `WaitingRoom`. Чи не порушує це принцип розділення відповідальності? Як можна було б зробити це через додаткову подію?
6. Що станеться якщо підписати один і той же метод двічі: `event += handler; event += handler`?

---

## Злиття

```bash
git checkout main
git merge --no-ff feature/events -m "Merge feature/events: Lab13 Events & Delegates"
git push
```

> Наступна лаба: `git checkout -b feature/linq` — LINQ: `Where`, `Select`, `OrderBy`, `GroupBy`, `First/FirstOrDefault`, `Sum/Average`, `Any/All`.
