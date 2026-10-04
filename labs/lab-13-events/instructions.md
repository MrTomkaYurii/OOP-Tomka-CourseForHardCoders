# Лаба 13 — Events & Delegates (Події та делегати)

## Мета

Зрозуміти проблему жорсткого зв'язування між класами та навчитись її вирішувати через механізм подій. Опанувати `delegate`, `EventArgs`, `event EventHandler<T>`, підписку через `+=` і побудову системи, де компоненти реагують на зміни, **не знаючи один про одного**.

## Контекст

Відкрийте `ClinicApp/Program.cs` і подивіться на будь-який пункт меню. Після кожної дії ви побачите щось подібне:

```csharp
clinic.Appointments.Book(patientId, doctorId, scheduledAt);
clinic.Logger.LogInfo($"Запис створено: пацієнт {patientId}...");
```

Тобто **кожна дія в меню вручну повідомляє `Logger`**. Зараз слухач один — але що, якщо потрібно ще й оновити паспорт пацієнта чи вести статистику? Тоді після кожної дії буде три рядки, потім чотири, потім п'ять. Це **жорстке зв'язування**: `Program.cs` знає про всіх слухачів і мусить викликати кожного вручну.

**Правильно**, щоб менеджер просто **повідомляв**: «запис створено». А всі зацікавлені слухачі реагують самі — незалежно, не знаючи одне про одного. Це **патерн Publisher–Subscriber**, реалізований через механізм подій у C#.

### Структура проєкту на початку лаби

Це результат Лаби 12 — стан `main` після її злиття:

```text
oop-course/                             ← гілка main (після злиття Лаби 12)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/  (15 файлів)
    ├── Managers/
    │   ├── PatientManager.cs
    │   ├── DoctorManager.cs
    │   ├── AppointmentManager.cs
    │   ├── GrowablePatientManager.cs
    │   ├── MedicalRecordManager.cs
    │   ├── BillingManager.cs
    │   ├── Repository.cs
    │   ├── AnalyticsManager.cs
    │   └── TreatmentPlanManager.cs
    ├── Utils/
    │   ├── ClinicLogger.cs
    │   └── … ще 9 файлів без змін
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    └── Attributes/  (3 файли)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Що таке делегат, подія і `EventArgs`

**Делегат** — тип, що описує сигнатуру методу. Думайте про нього як про «контракт обробника»: «я очікую метод, що приймає `object? sender` і `AppointmentEventArgs e` і нічого не повертає». `EventHandler<T>` — вбудований у .NET делегат саме з такою сигнатурою: оголошувати власний не потрібно.

**Подія (`event`)** — поле типу делегата з обмеженнями: ззовні класу дозволено лише `+=` і `-=`. Не можна присвоїти `= null` чи викликати подію напряму — це захищає від випадкового знищення всіх підписників.

**`EventArgs`** — базовий клас для «посилки з даними про подію». Повідомляючи про створення запису, менеджер передає `AppointmentEventArgs` з усіма деталями; підписник отримує цю посилку і робить з нею що потрібно.

### Що нового дозволено (і тільки воно)

- `event EventHandler<T>`, підписка `+=` / відписка `-=`;
- власні класи-нащадки `EventArgs`;
- безпечний виклик події `?.Invoke(...)`;
- методи з тілом-виразом `=>` для коротких обробників.

Досі заборонено: LINQ (Лаба 14), лямбди й `Func`/`Action` (Лаба 15).

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-13
```

Коміт — на кожне завдання (`Lab13 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. Перша подія: `AppointmentBooked` ⭐⭐

### Умова

`AppointmentManager.Book()` створює запис, але нікому про це не повідомляє — `Program.cs` мусить сам писати в лог після кожного виклику. Додайте першу подію і першого підписника, щоб побачити механіку.

**Що реалізувати:**

1. Створити теку `ClinicApp/Events/` і клас `AppointmentEventArgs : EventArgs` з даними про запис (специфікація нижче). Усі властивості лише для читання, заповнюються в конструкторі.
2. У `AppointmentManager` оголосити подію `AppointmentBooked` типу `EventHandler<AppointmentEventArgs>`.
3. Піднімати `AppointmentBooked` після **кожного** успішного створення запису — у `Book`, `BookUrgent` і `BookSpecialist`.
4. У `Program.cs` оголосити статичний обробник `OnAppointmentBookedConsole`, що виводить рядок `[EVENT] Запис #N створено…`, і підписати його **до** створення початкових даних.

### Специфікація

| Властивість `AppointmentEventArgs` | Тип |
|------------------------------------|-----|
| `AppointmentId` | `int` |
| `PatientId` | `int` |
| `DoctorId` | `int` |
| `ScheduledAt` | `DateTime` |
| `Notes` | `string` (за замовчуванням `""`) |

| Член `AppointmentManager` | Опис |
|---------------------------|------|
| `event EventHandler<AppointmentEventArgs>? AppointmentBooked` | піднімається після успішного запису будь-якого типу |

### Приклад

```
  [EVENT] Запис #1 створено: пацієнт #1 → лікар #1, 16.10.2026 10:00
  [EVENT] Запис #2 створено: пацієнт #2 → лікар #2, 16.10.2026 11:00
```

Рядки з'являються автоматично — у коді меню немає жодного виклику обробника.

### Підказки

1. Знак `?` у типі події означає, що підписників може не бути, і це нормально.
2. Піднімайте подію безпечним викликом `?.Invoke(this, args)`: якщо підписників немає — нічого не відбувається. Без `?.` порожня подія кине `NullReferenceException`.
3. Якщо в Лабі 08 ви винесли спільну частину `Book`/`BookUrgent`/`BookSpecialist` у приватний метод — підніміть подію там, і вона спрацює для всіх трьох.
4. `sender` — об'єкт, що підняв подію (тут — менеджер). Передавайте `this`.
5. `Notes` має значення за замовчуванням `""` — запис може бути без приміток.

📖 Документація:
- [Події (посібник)](https://learn.microsoft.com/dotnet/csharp/programming-guide/events/)
- [`EventHandler<TEventArgs>`](https://learn.microsoft.com/dotnet/api/system.eventhandler-1)
- [Як підняти й обробити подію](https://learn.microsoft.com/dotnet/standard/events/how-to-raise-and-consume-events)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `AppointmentEventArgs` | `BookingEventArgs` | `ReservationEventArgs` | `EnrollmentEventArgs` | `RentalEventArgs` | `LoanEventArgs` | `SessionEventArgs` |
| `AppointmentBooked` | `BookingCreated` | `ReservationCreated` | `StudentEnrolled` | `RentalCreated` | `BookLoaned` | `SessionBooked` |

### Коміт

```bash
git add ClinicApp/Events/AppointmentEventArgs.cs ClinicApp/Managers/AppointmentManager.cs ClinicApp/Program.cs
git commit -m "Lab13 Task01"
```

---

## Задача 2. Усі події системи і `ClinicLogger` як підписник ⭐⭐

### Умова

Зараз `Program.cs` **знає** про `Logger` і **пам'ятає** викликати його після кожної дії. Новий пункт меню без такого виклику — і дія не потрапить у лог. Нехай натомість менеджери піднімають події, а `Logger` як підписник реагує сам — автоматично і завжди.

**Що реалізувати:**

1. У `ClinicApp/Events/` створити `PatientEventArgs`, `PaymentEventArgs`, `TreatmentPlanEventArgs` (специфікація нижче).
2. Додати події в менеджери і піднімати їх у відповідних методах (таблиця подій нижче).
3. У `TreatmentPlanManager` додати метод `Complete(int planId)`: знаходить план, завершує його і піднімає `PlanCompleted`. Пункт меню «Завершити план» (Лаба 11) тепер викликає цей метод.
4. У `ClinicLogger` додати обробник для кожної події. Терміновий запис — `LogWarning` і додатковий рядок у файлі `alerts/urgent_{yyyy-MM-dd}.txt`.
5. У `Clinic.cs` додати приватний метод `SubscribeEvents()`, що підписує `Logger` на всі події, і викликати його в кінці конструктора.
6. Прибрати з `Program.cs` ручні виклики `clinic.Logger.LogInfo(...)` для дій, які тепер покриті подіями.

### Специфікація

| `EventArgs` | Властивості |
|-------------|-------------|
| `PatientEventArgs` | `PatientId`, `FullName` |
| `PaymentEventArgs` | `AppointmentId`, `Amount` (`decimal`) |
| `TreatmentPlanEventArgs` | `PlanId`, `PatientId`, `Diagnosis` |

| Менеджер | Подія | Де піднімається |
|----------|-------|-----------------|
| `AppointmentManager` | `AppointmentCancelled` | `Cancel()`; у `CancelAll()` — для кожного скасованого запису |
| `AppointmentManager` | `AppointmentCompleted` | `Complete()` |
| `AppointmentManager` | `UrgentAppointmentBooked` | `BookUrgent()` — **разом** з `AppointmentBooked` |
| `PatientManager` | `PatientAdded` | `Add()` |
| `BillingManager` | `PaymentReceived` | `PayAppointment()`; сума — `GetCost()` |
| `TreatmentPlanManager` | `PlanCompleted` | новий `Complete(int planId)` |

Кожна подія піднімається лише після **успішної** дії.

### Приклад

```
[2026-10-15 11:00:02] [INFO ] Новий пацієнт #6: Марія Ткач
[2026-10-15 11:01:15] [INFO ] Запис #9 створено: пацієнт #6 → лікар #2
[2026-10-15 11:01:15] [WARN ] ТЕРМІНОВИЙ запис #9: біль у грудях
[2026-10-15 11:03:40] [INFO ] Оплата запису #9: 450.00 грн
```

### Підказки

1. Нові `EventArgs` — за тим самим зразком, що `AppointmentEventArgs`: лише ті поля, що описують «що сталося».
2. Терміновий запис — теж запис, тож `BookUrgent()` піднімає **обидві** події. Logger підписаний на обидві й залогує обидві — це задумано.
3. Обробник у `ClinicLogger` — звичайний публічний метод із сигнатурою `(object? sender, XxxEventArgs e)`; короткий можна записати з тілом-виразом `=>`.
4. Підписка — у `Clinic`, а не в `Program.cs`: `Clinic` — оркестратор, він знає всі менеджери й вирішує, хто на що підписаний.
5. Підписка можлива лише після створення і менеджерів, і `Logger` — тому `SubscribeEvents()` викликається **в кінці** конструктора.
6. Теку `alerts/` створіть через `Directory.CreateDirectory` перед записом.

📖 Документація:
- [Події (посібник)](https://learn.microsoft.com/dotnet/csharp/programming-guide/events/)
- [`File.AppendAllText`](https://learn.microsoft.com/dotnet/api/system.io.file.appendalltext)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `PatientAdded` | `GuestRegistered` | `CustomerAdded` | `StudentAdded` | `ClientAdded` | `ReaderAdded` | `MemberAdded` |
| `PaymentReceived` | `InvoicePaid` | `BillPaid` | `FeePaid` | `RentalPaid` | `FinePaid` | `MembershipPaid` |
| `UrgentAppointmentBooked` | `SuiteBooked` | `PrivateRoomReserved` | `IntensiveEnrolled` | `PremiumRented` | `ResearchLoaned` | `PersonalTrainingBooked` |

### Коміт

```bash
git add ClinicApp/Events/ ClinicApp/Managers/ ClinicApp/Utils/ClinicLogger.cs ClinicApp/Clinic.cs ClinicApp/Program.cs
git commit -m "Lab13 Task02"
```

---

## Задача 3. `PatientPassportWriter` — другий незалежний підписник ⭐⭐⭐

### Умова

Замовник просить: «при реєстрації пацієнта, після кожного завершеного прийому і завершеного плану лікування — генеруйте файл паспорта пацієнта». З подіями це **один новий клас**: менеджери вже піднімають потрібні події, достатньо підписати нового слухача. `PatientManager`, `AppointmentManager`, `Program.cs` не змінюються.

**Що реалізувати:**

1. Клас `PatientPassportWriter` у `ClinicApp/Utils/`: отримує `Clinic` і теку для паспортів (за замовчуванням `patients`) через конструктор; теку створює в конструкторі.
2. Три публічні обробники — на `PatientAdded`, `AppointmentCompleted`, `PlanCompleted`; усі викликають **один** приватний метод запису паспорта.
3. Метод запису перезаписує файл `patients/passport_{id}.txt` повністю; якщо пацієнта не знайдено — нічого не пише.
4. У `Clinic.cs` додати властивість `Passport` і підписати три обробники в `SubscribeEvents()`.

### Специфікація

Секції паспорта (у такому порядку):

| Секція | Джерело |
|--------|---------|
| Особисті дані: ім'я, дата народження, вік, група крові, телефон | `Patients` |
| Медичні записи: окремо діагнози, аналізи, рецепти | `MedicalRecords` |
| Записи на прийом | `Appointments` |
| Плани лікування | `TreatmentPlans` |
| Заборгованість | `Billing` |
| Дата генерації паспорта | `DateTime.Now` |

### Приклад

```
=== Паспорт пацієнта #1 ===
Згенеровано: 15.10.2026 11:20

Ім'я: Іван Петренко
Дата народження: 15.03.1985 (41 рік)
Група крові: A+   Телефон: (050) 123-4567

-- Діагнози --
I10: Гіпертонічна хвороба [хронічне]
-- Аналізи --
Холестерин: 6.2 ммоль/л (норма: < 5.2) ⚠ поза нормою
-- Рецепти --
Лізиноприл 10 мг × 30 днів (вранці)

-- Записи --
[1] Звичайний прийом | 16.10.2026 10:00 | Completed | 300.00 грн

-- Плани лікування --
[1] Гіпертонія | 30 днів | Active

Заборгованість: 0.00 грн
```

### Підказки

1. Логіка генерації однакова для всіх трьох тригерів — не дублюйте її: обробники лише передають `PatientId` у спільний метод.
2. Перезапис (`StreamWriter` з `append: false`), а не дописування: паспорт — це знімок поточного стану, а не журнал.
3. Для розбиття медичних записів на типи — `is` з оголошенням змінної (Лаба 06). Три окремі проходи для трьох секцій простіші за один прохід із кількома `if`.
4. Ранній вихід `return`, якщо пацієнта не знайдено, — щоб не створити порожній файл.

📖 Документація:
- [`StreamWriter`](https://learn.microsoft.com/dotnet/api/system.io.streamwriter)
- [Зіставлення з шаблоном `is`](https://learn.microsoft.com/dotnet/csharp/language-reference/operators/is)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `PatientPassportWriter` → `passport_{id}.txt` | картка гостя | картка клієнта | залікова книжка | картка клієнта | формуляр читача | картка учасника |

### Коміт

```bash
git add ClinicApp/Utils/PatientPassportWriter.cs ClinicApp/Clinic.cs
git commit -m "Lab13 Task03"
```

---

## Задача 4. `SessionEventTracker` — реакція на події з іншої підсистеми ⭐⭐⭐

### Умова

Досі кожен підписник реагував у своїй зоні: `Logger` пише у файл, `PassportWriter` генерує документ. Але інколи реакція на подію зачіпає іншу підсистему: скасовано прийом → звільнився слот → варто перевірити чергу очікування (Лаба 09). Скасування — подія `AppointmentManager`, черга — у `Clinic`. Зв'яжіть їх без прямої залежності між менеджерами.

**Що реалізувати:**

1. Клас `SessionEventTracker` у `ClinicApp/Utils/`: отримує `Clinic` через конструктор і рахує події за сесію (лічильники нижче — `public` з `private set`).
2. Обробник на кожну подію збільшує свій лічильник. Обробник скасування додатково перевіряє чергу: якщо вона не порожня — виводить `[ЧЕРГА] Слот звільнився. Наступний: …` (без видалення з черги).
3. Метод `PrintSummary()` — підсумок сесії в консоль; метод `SaveSummary(string path = "session_summary.txt")` — той самий підсумок у файл, з датою й часом формування.
4. У `Clinic.cs` додати властивість `Tracker` і підписати всі його обробники в `SubscribeEvents()`.
5. У `Program.cs` при виході (пункт `0`) перед збереженням сесії викликати `PrintSummary()` і `SaveSummary()`.

### Специфікація

| Лічильник | Подія |
|-----------|-------|
| `PatientsAdded` | `PatientAdded` |
| `AppointmentsBooked` | `AppointmentBooked` |
| `UrgentBooked` | `UrgentAppointmentBooked` |
| `AppointmentsCancelled` | `AppointmentCancelled` |
| `AppointmentsCompleted` | `AppointmentCompleted` |
| `PaymentsReceived` | `PaymentReceived` |
| `PlansCompleted` | `PlanCompleted` |

### Приклад

```
  [ЧЕРГА] Слот звільнився. Наступний: Олена Коваль
…
=== Підсумок сесії ===
Пацієнтів додано:    1
Записів створено:    4 (термінових: 1)
Скасовано:           1
Завершено:           2
Оплат:               2
Планів завершено:    1
```

### Підказки

1. Наступного в черзі дивіться через `Peek()`, а не `Dequeue()`: трекер лише повідомляє, а прийом — дія користувача.
2. `PrintSummary()` викликається явно в `Program.cs`, а не через подію: це не реакція на зміну в системі, а дія користувача «підсумок перед виходом».
3. `Logger` і `Tracker` підписані на ті самі події. Обробники викликаються в порядку підписки — подумайте, чи важливий цей порядок тут.

📖 Документація:
- [Події (посібник)](https://learn.microsoft.com/dotnet/csharp/programming-guide/events/)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| скасування → черга очікування | скасування броні → лист очікування | звільнився столик → черга | звільнилось місце → черга на курс | авто повернули → черга | книгу повернули → черга | звільнився тренер → черга |

### Коміт

```bash
git add ClinicApp/Utils/SessionEventTracker.cs ClinicApp/Clinic.cs ClinicApp/Program.cs
git commit -m "Lab13 Task04"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                             ← гілка Lab-13 (після злиття — main)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs                      ✏ Т1 Т2 Т4
    ├── Clinic.cs                       ✏ Т2 Т3 Т4
    ├── Enums/  (4 файли)
    ├── Models/  (15 файлів)
    ├── Managers/
    │   ├── PatientManager.cs           ✏ Т2
    │   ├── DoctorManager.cs
    │   ├── AppointmentManager.cs       ✏ Т1 Т2
    │   ├── GrowablePatientManager.cs
    │   ├── MedicalRecordManager.cs
    │   ├── BillingManager.cs           ✏ Т2
    │   ├── Repository.cs
    │   ├── AnalyticsManager.cs
    │   └── TreatmentPlanManager.cs     ✏ Т2
    ├── Utils/
    │   ├── ClinicLogger.cs             ✏ Т2
    │   ├── PatientPassportWriter.cs    🆕 Т3
    │   ├── SessionEventTracker.cs      🆕 Т4
    │   └── … ще 9 файлів без змін
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    └── Events/
        ├── AppointmentEventArgs.cs     🆕 Т1
        ├── PatientEventArgs.cs         🆕 Т2
        ├── PaymentEventArgs.cs         🆕 Т2
        └── TreatmentPlanEventArgs.cs   🆕 Т2
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 12.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] Записали пацієнта → рядок `[EVENT]` у консолі **і** рядок у `clinic.log` (два підписники)
- [ ] Терміновий запис → у `clinic.log` два рядки + рядок у `alerts/urgent_{дата}.txt`
- [ ] Зареєстрували пацієнта → з'явився `patients/passport_N.txt`
- [ ] Завершили прийом → `passport_N.txt` оновився (нова дата генерації, прийом `Completed`)
- [ ] Скасували запис при непорожній черзі → `[ЧЕРГА] Слот звільнився…`
- [ ] Вихід → `session_summary.txt` з коректними лічильниками
- [ ] У `Program.cs` не лишилось ручних `Logger.LogInfo` для дій, покритих подіями
- [ ] *(Експеримент, не для коміту)* `clinic.Appointments.AppointmentBooked = null` — помилка компіляції

---

## Питання для самоперевірки

1. У чому різниця між полем-делегатом і `event`? Що саме забороняє `event` ззовні класу?
2. Чому обробник має сигнатуру `(object? sender, T e)`? Що передається в `sender`?
3. `AppointmentManager` не знає ні про `ClinicLogger`, ні про `PatientPassportWriter`. Де відбувається їхній зв'язок? Чому це добре?
4. `BookUrgent` піднімає дві події, `Logger` підписаний на обидві. Скільки рядків у лозі після одного `BookUrgent`?
5. Якщо підписати той самий метод двічі (`event += handler; event += handler`), скільки разів він спрацює?
6. Чому паспорт перезаписується, а не дописується?
7. Яку ще автоматичну реакцію можна додати до системи, не змінюючи жодного менеджера? Які файли для цього знадобиться змінити?

---

## Статус гілки

Після всіх 4 завдань (кожне — окремий коміт `Lab13 TaskNN` на гілці `Lab-13`):

```bash
git push -u origin Lab-13
git checkout main
git merge --no-ff Lab-13 -m "Merge Lab-13: Events & Delegates"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-14`.
