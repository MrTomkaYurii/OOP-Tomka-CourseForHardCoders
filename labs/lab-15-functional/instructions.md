# Лаба 15 — Функціональне програмування у C#

## Мета

Зрозуміти, як у C# методи можна передавати як значення — зберігати у змінних, передавати в параметри, комбінувати між собою. Навчитися будувати гнучкий код через `Func<>`, `Action<>`, замикання та методи розширення.

## Контекст

Відкрийте будь-який менеджер у проєкті — `AppointmentManager`, `AnalyticsManager` — і знайдіть місця, де фільтруються прийоми: умови написані безпосередньо всередині методу. Потрібна нова умова — треба змінити метод або написати новий.

Проблема: **логіка, що змінюється, захардкоджена всередині логіки, що не змінюється**. Рішення — зробити умову **параметром**: замість умови всередині методу передати `Func<Appointment, bool> predicate` ззовні. Саме так влаштований `.Where()` у LINQ: він не знає вашу умову заздалегідь — він отримує її як параметр.

### Структура проєкту на початку лаби

Це результат Лаби 14 — стан `main` після її злиття:

```text
oop-course/                           ← гілка main (після злиття Лаби 14)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/  (16 файлів)
    ├── Managers/  (10 файлів)
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    └── Events/  (4 файли)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### `Func<>`, `Action<>`, замикання, методи розширення

**`Func<T, TResult>`** — тип для «методу, що приймає `T` і повертає `TResult`». `Func<Appointment, bool>` — функція, що перевіряє прийом і повертає `true`/`false` (предикат).

**`Action<T>`** — тип для «методу, що приймає `T` і нічого не повертає». `Action<Appointment>` — дія над прийомом: вивести, позначити оплаченим, надіслати сповіщення.

```csharp
Func<Appointment, bool> isUrgent = a => a is UrgentAppointment;
Action<Appointment> print = a => Console.WriteLine(a);
```

**Замикання** — лямбда «захоплює» змінну з навколишнього коду і зберігає **посилання на неї**, а не копію значення:

```csharp
decimal threshold = 300;
Func<Appointment, bool> expensive = a => a.GetCost() > threshold;
```

Якщо пізніше `threshold` зміниться — зміниться і результат лямбди. У Задачі 3 ви побачите, як замикання на неправильну змінну ламає логіку.

**Метод розширення** — статичний метод у статичному класі, перший параметр якого позначено `this`. Після цього метод викликається так, ніби завжди існував у типі: `appointments.Unpaid()`. Саме так влаштовані всі LINQ-методи.

### Що нового дозволено (і тільки воно)

- змінні й параметри типів `Func<...>` і `Action<...>`;
- лямбди, що зберігаються у змінних і полях, замикання;
- власні методи розширення (`static` клас, параметр `this`);
- методи, що повертають `this` (fluent-ланцюг).

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-15
```

Коміт — на кожне завдання (`Lab15 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. Методи розширення для записів ⭐

### Умова

Щоб отримати «неоплачені майбутні прийоми», зараз щоразу пишуть LINQ-умову вручну. Потрібна в п'яти місцях — повторюється п'ять разів, змінилась — правити всюди. Назвіть кожну умову одним словом і напишіть її один раз — методом розширення.

**Що реалізувати:**

1. Створити теку `ClinicApp/Extensions/` і статичний клас `AppointmentExtensions` (простір імен `ClinicApp.Extensions`).
2. Реалізувати сім методів розширення на `IEnumerable<Appointment>` зі специфікації.

### Специфікація

| Метод | Повертає | Умова / результат |
|-------|----------|-------------------|
| `Unpaid()` | `IEnumerable<Appointment>` | не оплачено і не скасовано |
| `Upcoming()` | `IEnumerable<Appointment>` | `IsUpcoming == true` |
| `ByDoctor(int doctorId)` | `IEnumerable<Appointment>` | `DoctorId` збігається |
| `ByPatient(int patientId)` | `IEnumerable<Appointment>` | `PatientId` збігається |
| `Overdue()` | `IEnumerable<Appointment>` | дата в минулому, не скасовано, не оплачено |
| `CostAbove(decimal minCost)` | `IEnumerable<Appointment>` | `GetCost() > minCost` |
| `TotalCost()` | `decimal` | сума `GetCost()` |

### Приклад

```csharp
decimal debt = clinic.Appointments.GetAll().Unpaid().TotalCost();
var big = clinic.Appointments.GetAll().Upcoming().CostAbove(500);
```

### Підказки

1. Клас і методи — `static`; перший параметр кожного методу — `this IEnumerable<Appointment> source`.
2. Усередині — звичайний LINQ (`Where`, `Sum`) над `source`.
3. `TotalCost()` — «термінальний» метод: повертає число, а не продовження ланцюга.
4. У `CostAbove` параметр `minCost` потрапляє всередину лямбди — це замикання: лямбда пам'ятає `minCost` і після завершення методу.

📖 Документація:
- [Методи розширення](https://learn.microsoft.com/dotnet/csharp/programming-guide/classes-and-structs/extension-methods)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `AppointmentExtensions` | `BookingExtensions` | `ReservationExtensions` | `EnrollmentExtensions` | `RentalExtensions` | `LoanExtensions` | `SessionExtensions` |
| `Unpaid`, `Overdue`, `CostAbove` | `Unpaid`, `Overdue`, `CostAbove` | `Unpaid`, `Overdue`, `CostAbove` | `Unpaid`, `Overdue`, `FeeAbove` | `Unpaid`, `Overdue`, `CostAbove` | `Overdue`, `FineAbove` | `Unpaid`, `Overdue`, `CostAbove` |

### Коміт

```bash
git add ClinicApp/Extensions/AppointmentExtensions.cs
git commit -m "Lab15 Task01"
```

---

## Задача 2. Методи розширення для пацієнтів і лікарів ⭐

### Умова

Фільтрація пацієнтів за групою крові чи лікарів за спеціальністю розкидана по коду або відсутня. Винесіть ці умови в методи розширення так само, як у Задачі 1.

**Що реалізувати:**

1. Статичний клас `PatientExtensions` у `ClinicApp/Extensions/` з трьома методами на `IEnumerable<Patient>`.
2. Статичний клас `DoctorExtensions` у `ClinicApp/Extensions/` з трьома методами на `IEnumerable<Doctor>`.

### Специфікація

| Клас | Метод | Умова |
|------|-------|-------|
| `PatientExtensions` | `Adults()` | вік 18 і більше |
| `PatientExtensions` | `ByBloodType(BloodType bloodType)` | збіг групи крові |
| `PatientExtensions` | `WithAppointments(IEnumerable<Appointment> appointments)` | у пацієнта є хоч один запис |
| `DoctorExtensions` | `BySpeciality(Speciality speciality)` | збіг спеціальності |
| `DoctorExtensions` | `Available()` | `IsAvailableNow == true` |
| `DoctorExtensions` | `WithAppointments(IEnumerable<Appointment> appointments)` | у лікаря є хоч один запис |

### Приклад

```csharp
var adults = clinic.Patients.GetAll().Adults();
var busy = clinic.Doctors.GetAll().WithAppointments(clinic.Appointments.GetAll());
```

### Підказки

1. `WithAppointments` перевіряє для кожного пацієнта (лікаря), чи є серед прийомів хоч один його — `Any`.
2. Колекція прийомів передається параметром, а не береться з клініки напряму: метод розширення не повинен знати, звідки беруться дані.

📖 Документація:
- [Методи розширення](https://learn.microsoft.com/dotnet/csharp/programming-guide/classes-and-structs/extension-methods)
- [`Enumerable.Any`](https://learn.microsoft.com/dotnet/api/system.linq.enumerable.any)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `Adults()`, `ByBloodType()` | `Adults()`, `ByRoomType()` | `Adults()`, `ByCategory()` | `ByFaculty()` | `ByCarClass()` | `ByGenre()` | `ByFitnessLevel()` |
| `BySpeciality()`, `Available()` | `ByDepartment()`, `OnDuty()` | `ByCuisine()`, `OnShift()` | `BySubject()`, `Available()` | `ByBrand()`, `Available()` | `BySection()`, `OnDuty()` | `ByTrainingType()`, `Available()` |

### Коміт

```bash
git add ClinicApp/Extensions/PatientExtensions.cs ClinicApp/Extensions/DoctorExtensions.cs
git commit -m "Lab15 Task02"
```

---

## Задача 3. `AppointmentFilter` — складання умов з частин ⭐⭐

### Умова

Користувач хоче відфільтрувати прийоми за кількома умовами одразу — наприклад, «термінові і не оплачені». Зараз умови зліплені в одну лямбду, їх не можна скласти з окремих частин. Напишіть клас, що збирає предикати по одному і комбінує їх через «і», «або», «не».

**Що реалізувати:**

1. Клас `AppointmentFilter` у `ClinicApp/Managers/`. Зберігає одне поле — поточний комбінований предикат `Func<Appointment, bool>?`; спочатку `null` (порожній фільтр пропускає все).
2. Методи зі специфікації. `Add`, `And`, `Or`, `Negate` повертають `this` (fluent-ланцюг).

### Специфікація

| Метод | Дія |
|-------|-----|
| `Add(Func<Appointment, bool> predicate)` | додає умову через «і»; якщо фільтр порожній — умова стає першою |
| `And(Func<Appointment, bool> predicate)` | те саме, що `Add` (для читабельності ланцюга) |
| `Or(Func<Appointment, bool> predicate)` | додає умову через «або» |
| `Negate()` | заперечує поточну комбіновану умову |
| `Apply(IEnumerable<Appointment> source)` | порожній фільтр — уся колекція; інакше — відібрані записи |
| `Reset()` | очищає фільтр |

### Приклад

```csharp
var filter = new AppointmentFilter();
var result = filter
    .Add(a => a is UrgentAppointment)
    .And(a => !a.IsPaid)
    .Apply(clinic.Appointments.GetAll());
```

### Підказки

1. **Критична пастка — замикання на поле.** Якщо в новій лямбді звернутися до поля з поточним предикатом, лямбда захопить саме **поле**, а не його поточне значення. Коли вона виконається, поле вже міститиме цю саму нову лямбду — і вона викличе сама себе: нескінченна рекурсія.
2. Правильно: перед створенням нової лямбди скопіюйте поточний предикат у **локальну змінну** і використовуйте в лямбді її — локальна змінна після створення вже не змінюється.
3. `Or` і `Negate` будуються так само, лише з `||` та `!`.
4. `return this` дозволяє писати виклики ланцюгом — так само, як `WithCostStrategy` чи LINQ.

📖 Документація:
- [`Func<T, TResult>`](https://learn.microsoft.com/dotnet/api/system.func-2)
- [Лямбди і захоплені змінні](https://learn.microsoft.com/dotnet/csharp/language-reference/operators/lambda-expressions#capture-of-outer-variables-and-variable-scope-in-lambda-expressions)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `AppointmentFilter` | `BookingFilter` | `ReservationFilter` | `EnrollmentFilter` | `RentalFilter` | `LoanFilter` | `SessionFilter` |

### Коміт

```bash
git add ClinicApp/Managers/AppointmentFilter.cs
git commit -m "Lab15 Task03"
```

---

## Задача 4. `AppointmentProcessor` — набір дій над записами ⭐⭐

### Умова

Щоб «для кожного запису зробити X», пишуть `foreach` із дією всередині. А якщо дій кілька і вони визначаються під час роботи програми? Напишіть клас, що накопичує дії і виконує їх усі разом.

**Що реалізувати:**

1. Клас `AppointmentProcessor` у `ClinicApp/Managers/`: зберігає список дій `List<Action<Appointment>>`.
2. Методи зі специфікації. `Run`, `RunIf`, `Combine` повертають `this`.

### Специфікація

| Метод | Дія |
|-------|-----|
| `Run(Action<Appointment> action)` | додає дію в список |
| `RunIf(Func<Appointment, bool> predicate, Action<Appointment> action)` | додає **одну** дію, що виконує `action` лише для записів, які задовольняють `predicate` |
| `Combine(Action<Appointment> first, Action<Appointment> second)` | додає **одну** дію, що викликає `first`, потім `second` |
| `Execute(IEnumerable<Appointment> source)` | для кожного запису виконує всі дії зі списку |
| `Clear()` | очищає список дій |

### Приклад

```csharp
var processor = new AppointmentProcessor()
    .Run(a => Console.WriteLine(a))
    .RunIf(a => a is UrgentAppointment, a => Console.WriteLine("  ⚠ терміновий"));
processor.Execute(clinic.Appointments.GetAll());
```

### Підказки

1. `RunIf` і `Combine` не виконують нічого одразу — вони **створюють нову лямбду** і кладуть її у список. Перевірка умови відбувається пізніше, під час `Execute`.
2. `Execute` — два вкладені цикли: зовнішній по записах, внутрішній по діях.
3. Повторний `Execute` виконає дії ще раз: список не очищається сам. Для цього є `Clear()`.

📖 Документація:
- [`Action<T>`](https://learn.microsoft.com/dotnet/api/system.action-1)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `AppointmentProcessor` | `BookingProcessor` | `ReservationProcessor` | `EnrollmentProcessor` | `RentalProcessor` | `LoanProcessor` | `SessionProcessor` |

### Коміт

```bash
git add ClinicApp/Managers/AppointmentProcessor.cs
git commit -m "Lab15 Task04"
```

---

## Задача 5. `AppointmentPipeline` — фасад «фільтр → дія» ⭐

### Умова

`AppointmentFilter` знає, як фільтрувати, `AppointmentProcessor` — як обробляти, але вони не пов'язані: порядок «спершу фільтр, потім дії» кожен складає сам. Напишіть **фасад** — один клас, що ховає обидва і дає простий інтерфейс «опиши умови, опиши дії, запусти».

**Що реалізувати:**

1. Клас `AppointmentPipeline` у `ClinicApp/Managers/` з двома полями — `AppointmentFilter` і `AppointmentProcessor`, обидва створюються в конструкторі.
2. Методи зі специфікації.

### Специфікація

| Метод | Дія | Повертає |
|-------|-----|----------|
| `Filter(Func<Appointment, bool> predicate)` | додає умову у фільтр | `this` |
| `Then(Action<Appointment> action)` | додає дію в процесор | `this` |
| `Execute(IEnumerable<Appointment> source)` | фільтрує, **один раз** матеріалізує результат у масив, запускає процесор на ньому | `int` — кількість оброблених |
| `Reset()` | очищає і фільтр, і процесор | |

### Приклад

```csharp
int count = pipeline
    .Filter(a => !a.IsPaid)
    .Filter(a => a.IsUpcoming)
    .Then(a => Console.WriteLine(a))
    .Execute(allAppointments);
Console.WriteLine($"Оброблено: {count} записів.");
```

### Підказки

1. Без матеріалізації (`ToArray()`) фільтр виконувався б двічі: раз для обробки, раз для підрахунку.
2. Фасад нічого не вміє сам — він лише делегує своїм двом полям.

📖 Документація:
- [Патерн «Фасад»](https://refactoring.guru/uk/design-patterns/facade)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `AppointmentPipeline` | `BookingPipeline` | `ReservationPipeline` | `EnrollmentPipeline` | `RentalPipeline` | `LoanPipeline` | `SessionPipeline` |

### Коміт

```bash
git add ClinicApp/Managers/AppointmentPipeline.cs
git commit -m "Lab15 Task05"
```

---

## Задача 6. Меню «Фільтри» ⭐

### Умова

Підключіть усе до клініки і меню.

**Що реалізувати:**

1. У `Clinic.cs` додати властивість `Pipeline` типу `AppointmentPipeline` і створити її в конструкторі.
2. На початку `Program.cs` додати `using ClinicApp.Extensions;`.
3. У головному меню додати пункт `12` — «Фільтри — Func, Action, Pipeline».
4. У `Program.cs` додати функцію `FunctionalMenu(Clinic clinic)` з вісьмома пунктами зі специфікації.

### Специфікація

| Пункт | Що показує | Що використовує |
|-------|------------|-----------------|
| `1` | Неоплачені прийоми і їх загальна сума | `Unpaid()` + `TotalCost()` |
| `2` | Майбутні записи дорожчі за N грн (N питає програма) | `Upcoming().CostAbove(n)` |
| `3` | Повнолітні пацієнти | `Adults()` |
| `4` | Лікарі з хоч одним записом | `WithAppointments(...)` |
| `5` | Термінові **і** майбутні | `AppointmentFilter`: `Add(...).And(...)` |
| `6` | Термінові **або** прострочені | `AppointmentFilter`: `Add(...).Or(...)` |
| `7` | Дві дії над кожним записом | `AppointmentProcessor.Combine(вивід, запис у лог)` |
| `8` | Повний пайплайн: фільтр → дія | `clinic.Pipeline.Filter(...).Then(...).Execute(...)`, далі `Оброблено: N записів.` |
| `0` | Назад | |

### Приклад

```
── Фільтри ─────────────────────
Оберіть: 2
Поріг, грн: 300
[9]  Терміновий (біль у грудях) | … | 450.00 грн
[10] Консультація спеціаліста: кардіологія | … | 780.00 грн
```

### Підказки

1. `clinic.Pipeline` зберігає умови між викликами — перед кожним запуском пункту 8 викликайте `Reset()`.
2. Для пункту 7 дію «запис у лог» зберіть із `clinic.Logger.LogInfo(...)`.

📖 Документація:
- [Директива `using`](https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/using-directive)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `12. Фільтри` | `12. Фільтри` | `12. Фільтри` | `12. Фільтри` | `12. Фільтри` | `12. Фільтри` | `12. Фільтри` |

### Коміт

```bash
git add ClinicApp/Clinic.cs ClinicApp/Program.cs
git commit -m "Lab15 Task06"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                            ← гілка Lab-15 (після злиття — main)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs                     ✏ Т6
    ├── Clinic.cs                      ✏ Т6
    ├── Enums/  (4 файли)
    ├── Models/  (16 файлів)
    ├── Managers/
    │   ├── AppointmentFilter.cs       🆕 Т3
    │   ├── AppointmentProcessor.cs    🆕 Т4
    │   ├── AppointmentPipeline.cs     🆕 Т5
    │   └── … ще 10 файлів без змін
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    ├── Events/  (4 файли)
    └── Extensions/
        ├── AppointmentExtensions.cs   🆕 Т1
        ├── DoctorExtensions.cs        🆕 Т2
        └── PatientExtensions.cs       🆕 Т2
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 14.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] `12. Фільтри` → `1`: неоплачені прийоми і загальна сума
- [ ] `2` з порогом `300`: тільки майбутні записи дорожчі за 300 грн
- [ ] `5` показує записи, що одночасно термінові і майбутні; `6` — більше записів (об'єднання умов)
- [ ] `8` виводить кількість оброблених записів; повторний запуск дає той самий результат
- [ ] Комбінований фільтр із 3+ умов не падає з `StackOverflowException`
- [ ] `8. Аналітика` і `11. Звіти` працюють, як раніше

---

## Питання для самоперевірки

1. Чим `Func<Appointment, bool>` відрізняється від методу `bool Check(Appointment a)`? Що в них спільного?
2. Яка різниця між `Action<Appointment>` і `Func<Appointment, bool>`? Коли використовується кожен?
3. Що станеться в `AppointmentFilter.Add`, якщо лямбда звертатиметься до поля напряму, без локальної копії?
4. Метод розширення можна викликати і як звичайний статичний: `AppointmentExtensions.Unpaid(source)`. Чому краще писати `source.Unpaid()`?
5. Навіщо `Combine`, якщо можна двічі викликати `Run`?
6. Що означає патерн «фасад»? Що `AppointmentPipeline` ховає від зовнішнього коду?

---

## Статус гілки

Після всіх 6 завдань (кожне — окремий коміт `Lab15 TaskNN` на гілці `Lab-15`):

```bash
git push -u origin Lab-15
git checkout main
git merge --no-ff Lab-15 -m "Merge Lab-15: Functional C#"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-16`.
