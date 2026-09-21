# Лаба 05 — Інкапсуляція

## Мета

Навчитися захищати внутрішній стан об'єктів: ховати дані за `private`-полями та властивостями, гарантувати коректність через валідацію в сеттерах, виносити правила, що повторюються, в окремий клас, організовувати проєкт підпапками з підпросторами імен і обробляти виняткові ситуації через `try/catch`.

## Контекст

Після Лаби 04 система має хороші типи (`enum`, `struct`), але жодного захисту даних: будь-хто може написати `patient.FirstName = ""` або `new WorkSchedule(25, 3)` — і об'єкт мовчки збереже нісенітницю. Програма при цьому не падає, а показує пацієнта без імені й лікаря, що «працює з 25:00».

### Структура проєкту на початку лаби

Це результат Лаби 04 — стан `main` після її злиття. Усі 14 файлів лежать в одній теці:

```text
oop-course/                          ← гілка main (після злиття Лаби 04)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Patient.cs
    ├── Doctor.cs
    ├── PatientManager.cs
    ├── DoctorManager.cs
    ├── Appointment.cs
    ├── AppointmentManager.cs
    ├── Clinic.cs
    ├── GrowablePatientManager.cs
    ├── AppointmentStatus.cs
    ├── BloodType.cs
    ├── Speciality.cs
    ├── WorkSchedule.cs
    └── ClinicFormatter.cs
```

Структуру **наприкінці** лаби (з позначками, що переміщується, змінюється і створюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Що таке інкапсуляція

**Інкапсуляція** — це принцип, за яким об'єкт сам відповідає за власну коректність. Зовні видно лише те, що об'єкт дозволяє робити (публічний інтерфейс), а внутрішній стан змінюється тільки контрольованими шляхами.

Ключове поняття — **інваріант**: умова, яка *завжди* має бути істинною для коректного об'єкта («ім'я не порожнє», «початок роботи раніше за кінець», «тривалість більша за нуль»). Інкапсуляція гарантує інваріант так, що **некоректний об'єкт неможливо створити чи зіпсувати** — у програмі просто немає шляху, яким він міг би там опинитись.

Технічно це три кроки, і кожен — це окрема задача цієї лаби:

1. **Сховати** дані (`private`-поле).
2. **Відкрити контрольований доступ** (властивість з `get`/`set`).
3. **Перевірити** значення перед збереженням і відхилити некоректне (валідація + виняток).

Решта лаби — інженерна дисципліна навколо цих трьох кроків: спершу впорядковуємо проєкт (підпапки, простори імен), наприкінці виносимо повторювані правила в один клас і вчимо меню коректно реагувати на відхилені значення.

### Що нового дозволено (і тільки воно)

- підпростори імен (`ClinicApp.Models` тощо) та директиви `using`;
- `private`-поля з іменами `_camelCase` і властивості з власним тілом `get`/`set`;
- оператор `throw`, винятки `ArgumentException` і `ArgumentOutOfRangeException`;
- `nameof(...)` та `string.IsNullOrWhiteSpace(...)`;
- `try / catch` (порядок блоків `catch`), необов'язковий `finally`;
- `static class ClinicValidator` — правила валідації в одному місці;
- `Regex` — лише в опційній Задачі 5.

Досі заборонено: успадкування, `virtual` / `abstract` (Лаба 06), `interface` (Лаба 07), `List<T>` / `Dictionary` та інші generic-колекції (Лаба 09), LINQ (Лаба 14).

> **Примітка про слово «підклас».** У Задачі 4 ви побачите, що `ArgumentOutOfRangeException` — «дочірній» тип до `ArgumentException`. Що таке успадкування, розберемо в Лабі 06; зараз потрібне лише практичне правило порядку `catch`.

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** наприкінці кожного завдання — вона підказує, чим замінити сутності й правила. Структуру рішення зберігайте.

### Як користуватися підказками

Підказки — **напрям думки, а не готовий код**. «Специфікація» каже, *що* має вийти; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Приклади коду в цій лабі показують загальну схему на **вигаданому** класі (`Book`, `Thermometer`) — перенесення її на `Patient`, `Doctor`, `Appointment` і `WorkSchedule` робите самі.

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-05
```

---

## Задача 1. Підпапки та підпростори імен ⭐⭐

### Умова

Усі 14 `.cs` файлів зараз лежать у корені `ClinicApp/`. Коли проєкт зростає, орієнтуватись у плоскому списку стає складно. Стандартна практика .NET — групувати файли за відповідальністю в підпапки та відображати це у просторах імен.

Перенесіть файли в підпапки, оновіть у кожному `namespace` і додайте потрібні `using`. Поведінка програми **не змінюється** — це чистий рефакторинг.

### Специфікація

| Підпапка | Файли | Простір імен |
|----------|-------|--------------|
| `ClinicApp/Models/` | `Patient.cs`, `Doctor.cs`, `Appointment.cs`, `WorkSchedule.cs` | `ClinicApp.Models` |
| `ClinicApp/Enums/` | `BloodType.cs`, `Speciality.cs`, `AppointmentStatus.cs` | `ClinicApp.Enums` |
| `ClinicApp/Managers/` | `PatientManager.cs`, `DoctorManager.cs`, `AppointmentManager.cs`, `GrowablePatientManager.cs` | `ClinicApp.Managers` |
| `ClinicApp/Utils/` | `ClinicFormatter.cs` | `ClinicApp.Utils` |
| `ClinicApp/` (корінь) | `Clinic.cs` | `ClinicApp` |
| `ClinicApp/` (корінь) | `Program.cs` | без `namespace` (top-level statements) |

Правила:
- простір імен файлу **збігається з його папкою**;
- кожен файл має `using` для кожного простору імен, з якого він використовує типи;
- директиви `using` розташовуються на початку файлу, до оголошення `namespace`.

### Приклад — цільова структура

```
ClinicApp/
├── ClinicApp.csproj
├── Program.cs
├── Clinic.cs
├── Enums/      AppointmentStatus.cs  BloodType.cs  Speciality.cs
├── Models/     Appointment.cs  Doctor.cs  Patient.cs  WorkSchedule.cs
├── Managers/   AppointmentManager.cs  DoctorManager.cs  PatientManager.cs  GrowablePatientManager.cs
└── Utils/      ClinicFormatter.cs
```

Орієнтовні залежності між просторами імен (остаточно вирішує компілятор):

| Файли в… | зазвичай використовують… |
|----------|--------------------------|
| `Models/` | `Enums`, `Utils` |
| `Managers/` | `Models`, `Enums` |
| `Utils/` | `Enums` |
| `Clinic.cs` | `Managers`, `Models` |
| `Program.cs` | усі підпростори |

### Підказки

1. **Переносьте по одній папці, а не все одразу.** Почніть з `Enums/` — вона майже ні від чого не залежить. Перенесли, зібрали (`dotnet build`), виправили помилки — і лише тоді наступна папка (`Utils`, далі `Models`, `Managers`).
2. **Два окремі кроки на кожен файл:** фізично перемістити його та змінити рядок `namespace`. Зручно робити це засобами середовища (Visual Studio / Rider: «Move to folder» оновить `namespace` сам) або командою `git mv`, яка зберігає історію файлу.
3. **Простір імен із крапкою.** У file-scoped формі (`namespace ...;` без фігурних дужок — ви його вже використовували) до кореневого імені просто додається суфікс папки.
4. **Читайте помилки компілятора — вони підкажуть все.** `CS0246` («the type or namespace name … could not be found») означає, що файлу бракує `using` для якогось простору імен (або в самому файлі типу неправильний `namespace`). Виправляйте по одному повідомленню.
5. **Зайві `using` не додавайте.** Середовище підсвічує невикористані директиви сірим — приберіть їх.
6. **`Program.cs` і `Clinic.cs` лишаються в корені.** У `Program.cs` (top-level statements) просто з'являються `using` для тих просторів імен, з яких він бере типи.
7. **Файл проєкту `.csproj` змінювати не треба:** проєкт SDK-стилю сам підхоплює всі `.cs` у підпапках.
8. **Критерій успіху:** програма збирається, меню працює точно як раніше.

📖 Документація:
- [Простори імен (namespaces)](https://learn.microsoft.com/dotnet/csharp/fundamentals/types/namespaces)
- [Директива `using`](https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/using-directive)
- [Ключове слово `namespace`](https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/namespace)
- [`git mv`](https://git-scm.com/docs/git-mv)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `ClinicApp.Models` | `HotelApp.Models` | `RestaurantApp.Models` | `UniversityApp.Models` | `RentalApp.Models` | `LibraryApp.Models` | `GymApp.Models` |
| `ClinicApp.Enums` | `HotelApp.Enums` | `RestaurantApp.Enums` | `UniversityApp.Enums` | `RentalApp.Enums` | `LibraryApp.Enums` | `GymApp.Enums` |
| `ClinicApp.Managers` | `HotelApp.Managers` | `RestaurantApp.Managers` | `UniversityApp.Managers` | `RentalApp.Managers` | `LibraryApp.Managers` | `GymApp.Managers` |
| `ClinicApp.Utils` | `HotelApp.Utils` | `RestaurantApp.Utils` | `UniversityApp.Utils` | `RentalApp.Utils` | `LibraryApp.Utils` | `GymApp.Utils` |

Кореневе ім'я (`ClinicApp`, `HotelApp` …) — назва **вашого** проєкту; назви підпапок (`Models`, `Enums`, `Managers`, `Utils`) лишаються однаковими.

### Коміт

```bash
git add -A ClinicApp/          # -A підхоплює і нові, і видалені (перенесені) файли
git commit -m "Lab05 Task01"
```

---

## Задача 2. Private поля та властивості ⭐⭐⭐

### Умова

Зараз властивості в `Patient`, `Doctor`, `Appointment` — автовластивості (`{ get; set; }`). Будь-який код може записати в них будь-що без жодних перевірок.

Інкапсуляція починається з простого: **дані — `private`, доступ — через властивість**. Властивість зовні виглядає так само (`patient.FirstName`), але тепер ви контролюєте, що в неї записується. У цій задачі ви лише перебудовуєте структуру — самі перевірки з'являться в Задачах 3–4.

### Специфікація

| Клас | Перетворити на «приватне поле + властивість» | Залишити без змін |
|------|----------------------------------------------|-------------------|
| `Patient` | `FirstName`, `LastName`, `DateOfBirth`, `Phone` | `Id` (лише `get`), `BloodType` (enum), `Email` |
| `Doctor` | `FirstName`, `LastName`, `LicenseNumber`, `Phone` | `Id`, `Speciality` (enum), `Schedule` (struct) |
| `Appointment` | `DurationMinutes` | `Id`, `PatientId`, `DoctorId`, `ScheduledAt`, `Status` / `Notes` (`private set`) |

Правила:
- ім'я поля — `_camelCase` (підкреслення + перша літера маленька): `_firstName`;
- ім'я властивості — `PascalCase`, як і раніше;
- тип властивості й поля збігаються;
- рядкові поля ініціалізуйте порожнім рядком, щоб компілятор не скаржився на можливий `null`.

### Приклад

Схема перетворення — на вигаданому класі `Book` (у вашому проєкті такі перетворення робите самі):

```csharp
// До: автовластивість
public string Title { get; set; }

// Після: приватне поле + явна властивість
private string _title = "";

public string Title
{
    get => _title;
    set => _title = value;
}
```

Зовні поведінка **ідентична**: увесь наявний код на кшталт `book.Title = "..."` компілюється й працює без змін.

### Підказки

1. **Що таке backing field.** Приватне «резервне» поле — це справжнє сховище даних. Властивість — лише «вікно» до нього: `get` віддає значення поля, `set` кладе нове.
2. **Ключове слово `value` у сеттері** — це те значення, яке присвоюють (`patient.FirstName = "Іван"` → `value` дорівнює `"Іван"`).
3. **Дві форми запису.** Стрілка `=>` — скорочення для однорядкового тіла, фігурні дужки — для кількох рядків. У Задачі 3 в сеттері з'явиться кілька рядків, тож переходьте на форму з дужками вже тоді.
4. **Що лишаємо автовластивістю і чому.** `Id` — його присвоюють лише в конструкторі, окремий сеттер не потрібен. `Email` та `Schedule` — поки без правил. Enum-поля — див. наступну підказку.
5. **Enum не «захищений» від некоректних значень.** Значення enum — це число під капотом, а приведення `(BloodType)99` **компілюється й працює**. Меню з Лаби 04 робить саме `(BloodType)число` з рядка, який ввів користувач — тож некоректне число може потрапити в поле. Зараз залишаємо, як є; за бажанням перевірте число на межі вводу — див. `Enum.IsDefined` у документації (це теж інкапсуляція: не пускати сміття всередину).
6. **Критерій успіху цієї задачі — «нічого не змінилось».** Програма працює точно як раніше. Якщо після рефакторингу щось зламалось — ви змінили поведінку, а не структуру.

📖 Документація:
- [Властивості](https://learn.microsoft.com/dotnet/csharp/programming-guide/classes-and-structs/properties)
- [Модифікатори доступу](https://learn.microsoft.com/dotnet/csharp/programming-guide/classes-and-structs/access-modifiers)
- [`Enum.IsDefined`](https://learn.microsoft.com/dotnet/api/system.enum.isdefined)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `Patient` (`_firstName`, `_lastName`, `_dateOfBirth`, `_phone`) | `Guest` (`_firstName`, `_lastName`, `_phone`, `_birthDate`) | `Customer` (`_firstName`, `_lastName`, `_phone`) | `Student` (`_firstName`, `_lastName`, `_dateOfBirth`, `_phone`) | `Client` (`_firstName`, `_lastName`, `_phone`, `_licenseNumber`) | `Reader` (`_firstName`, `_lastName`, `_phone`) | `Member` (`_firstName`, `_lastName`, `_phone`) |
| `Doctor` (+ `_licenseNumber`) | `Staff` | `Waiter` | `Lecturer` | `Manager` | `Librarian` | `Trainer` |
| `Appointment` (`_durationMinutes`) | `Booking` (`_stayNights`) | `TableReservation` (`_durationMinutes`) | `Enrollment` (`_courseDays`) | `Rental` (`_rentalDays`) | `BookLoan` (`_loanDays`) | `Session` (`_durationMinutes`) |

### Коміт

```bash
git add ClinicApp/Models/Patient.cs ClinicApp/Models/Doctor.cs ClinicApp/Models/Appointment.cs
git commit -m "Lab05 Task02"
```

---

## Задача 3. Валідація в сеттерах — throw ⭐⭐⭐

### Умова

Приватні поля вже захищені від прямого доступу, але сеттери приймають будь-яке значення. Тепер вони мають **перевіряти значення перед збереженням** і відхиляти некоректне — кидаючи виняток. Тоді поле фізично не може отримати некоректне значення.

Дві вбудовані категорії винятків:
- `ArgumentException` — аргумент некоректний «за формою» (порожній рядок, не цифри);
- `ArgumentOutOfRangeException` — число або дата поза допустимими межами.

### Специфікація

| Поле | Правило (некоректно, якщо…) | Виняток |
|------|------------------------------|---------|
| `FirstName`, `LastName` у `Patient` та `Doctor` | порожнє або лише пробіли; довжина > 50 | `ArgumentException` |
| `LicenseNumber` у `Doctor` | порожнє або лише пробіли | `ArgumentException` |
| `Phone` у `Patient` та `Doctor` | довжина не 10; містить не лише цифри | `ArgumentException` |
| `DateOfBirth` у `Patient` | пізніше за сьогодні; раніше 1900 року | `ArgumentOutOfRangeException` |
| `DurationMinutes` у `Appointment` | ≤ 0 | `ArgumentOutOfRangeException` |
| `WorkSchedule(start, end)` | `start` < 0 або > 23; `end` < 1 або > 24 | `ArgumentOutOfRangeException` |
| `WorkSchedule(start, end)` | `start` ≥ `end` | `ArgumentException` |

Додатково:
- ім'я властивості, яка відхилила значення, передавайте у виняток через `nameof(...)`;
- створити об'єкт із некоректними даними має бути неможливо — тож конструктори теж мусять проходити через ці перевірки;
- **невдала спроба створення не повинна «з'їдати» номер `Id`** (див. підказку 8).

### Приклад

Схема — на вигаданому класі `Thermometer` (у вашому проєкті робите самі):

```csharp
private double _celsius;

public double Celsius
{
    get => _celsius;
    set
    {
        if (value < -273.15)
            throw new ArgumentOutOfRangeException(nameof(Celsius), "Температура нижча за абсолютний нуль.");
        _celsius = value;
    }
}
```

Спроба записати `-500` завершиться так:

```
System.ArgumentOutOfRangeException: Температура нижча за абсолютний нуль. (Parameter 'Celsius')
```

Для вашого проєкту очікувана поведінка така: `new Patient("", "Петренко", …)` кидає `ArgumentException`; пацієнт із датою народження «завтра» — `ArgumentOutOfRangeException`; `new WorkSchedule(20, 6)` — виняток.

### Підказки

1. **`throw` — оператор**, який негайно перериває виконання поточного методу й передає керування вгору по стеку викликів (як саме — у Задачі 4).
2. **Порядок у сеттері: спершу перевірка, потім присвоєння.** Якщо значення некоректне — до присвоєння справа не дійде, і поле лишиться зі старим значенням.
3. **Який виняток обрати.** Значення «не того вигляду» (порожній рядок, літери в телефоні) — `ArgumentException`. Значення «не в межах» (дата в майбутньому, тривалість ≤ 0) — `ArgumentOutOfRangeException`. Обидва приймають зрозуміле повідомлення; другий, крім того, — ім'я параметра.
4. **Порожній рядок:** `string.IsNullOrWhiteSpace` перевіряє одразу три випадки — `null`, `""` і рядок із самих пробілів. Довжину дає `.Length`.
5. **Телефон — два окремі правила.** Спершу довжина рівно 10, потім кожен символ має бути цифрою. Друге — цикл по символах: ту саму ідею ви вже реалізували у `FormatPhone` в Лабі 04.
6. **Дата народження.** Порівняйте зі «сьогодні» (`DateTime.Today`) і перевірте рік (`.Year`).
7. **`WorkSchedule` — перевірки в конструкторі.** Це `struct` з властивостями `Start` і `End` лише для читання: їх присвоюють у конструкторі, тож усі перевірки мають стояти **до** присвоєнь. Три правила — три окремі `if`.
8. **Конструктори й номер `Id`.** Конструктори з Лаби 03 вже присвоюють поля через властивості, тож перевірки спрацюють без додаткового коду. Але якщо рядок з `_nextId++` стоїть у конструкторі **першим**, то кожна невдала спроба створення об'єкта все одно збільшить лічильник. **Експеримент:** у `try/catch` двічі створіть пацієнта з порожнім іменем, а потім коректного — який `Id` він отримав? Виправлення: присвоєння `Id` — **останній** рядок конструктора, після всіх властивостей. Принцип: побічний ефект (лічильник) має відбутись лише тоді, коли все вдалось.
9. **Навіщо `nameof`.** `nameof(DateOfBirth)` дає рядок `"DateOfBirth"`, але перевіряється компілятором і змінюється разом із перейменуванням властивості — на відміну від «магічного» рядка.
10. **Про суфікс у повідомленні.** Для `ArgumentOutOfRangeException` з іменем параметра .NET дописує до `e.Message` хвіст `(Parameter '…')`. Це нормально й очікувано.

📖 Документація:
- [Оператор `throw`](https://learn.microsoft.com/dotnet/csharp/language-reference/statements/exception-handling-statements#the-throw-statement)
- [`ArgumentException`](https://learn.microsoft.com/dotnet/api/system.argumentexception)
- [`ArgumentOutOfRangeException`](https://learn.microsoft.com/dotnet/api/system.argumentoutofrangeexception)
- [`nameof`](https://learn.microsoft.com/dotnet/csharp/language-reference/operators/nameof)
- [`String.IsNullOrWhiteSpace`](https://learn.microsoft.com/dotnet/api/system.string.isnullorwhitespace)

### Адаптація до вашого домену

Уважно: правило для дати **може мати протилежний напрям**.

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `DateOfBirth` — **не в майбутньому** | `BirthDate` — не в майбутньому; `CheckIn` — не в минулому | `ReservationDate` — **не в минулому** | `EnrollmentDate` — в межах поточного року | `RentalStart` — **не в минулому** | `LoanDate` — не в майбутньому | `SessionDate` — **не в минулому** |
| `DurationMinutes` > 0 | `StayNights` > 0 | `Duration` > 0 | `CourseDays` > 0 | `RentalDays` > 0 | `LoanDays` > 0 | `DurationMinutes` > 0 |
| `WorkSchedule`: `start` < `end` | зміна: початок < кінець | зміна: початок < кінець | пара: початок < кінець | робочі години: початок < кінець | зміна: початок < кінець | години тренера: початок < кінець |

### Коміт

```bash
git add ClinicApp/Models/Patient.cs ClinicApp/Models/Doctor.cs ClinicApp/Models/Appointment.cs ClinicApp/Models/WorkSchedule.cs
git commit -m "Lab05 Task03"
```

---

## Задача 4. `ClinicValidator` та `try/catch` ⭐⭐⭐⭐

### Умова

**Частина 1 — не повторюватись.** Після Задачі 3 однакова перевірка імені лежить у чотирьох сеттерах (`FirstName` і `LastName` в двох класах), перевірка телефону — у двох. Змінилось правило (ліміт довжини стане 100) — правити треба скрізь. Рішення: винести **повторювані** правила в окремий статичний клас `ClinicValidator`; сеттери лише викликають його.

Правило, яке зустрічається один раз (`LicenseNumber`, перевірки в конструкторі `WorkSchedule`), виносити немає сенсу — воно **лишається на місці**. Централізуємо те, що повторюється.

**Частина 2 — не падати.** Дані з меню вводить користувач, тому виняток із валідатора — цілком очікувана ситуація. Якщо його не перехопити, програма завершиться зі стеком викликів. `try/catch` дозволяє перехопити виняток і показати зрозуміле повідомлення.

### Що реалізувати

1. `static class ClinicValidator` у `ClinicApp/Utils/` (простір імен `ClinicApp.Utils`) з чотирма методами зі специфікації нижче.
2. Переписати сеттери `Patient`, `Doctor` та `Appointment`: замість вбудованих перевірок — виклик валідатора **перед** присвоєнням. `LicenseNumber` і `WorkSchedule` лишаються з власними перевірками.
3. У `Program.cs` огорнути в `try/catch` **всі** операції меню, що можуть кинути виняток через введення користувача:
   - «Додати пацієнта»;
   - «Додати лікаря» — **разом** зі створенням `WorkSchedule` з введених годин;
   - «Записати на прийом» — тривалість може бути ≤ 0.

### Специфікація `ClinicValidator`

| Метод | Параметри | Перевіряє | Виняток |
|-------|-----------|-----------|---------|
| `ValidateName` | `string value`, `string fieldName` | не порожнє / не пробіли; довжина ≤ 50 | `ArgumentException` |
| `ValidatePhone` | `string phone` | не порожнє; рівно 10 символів; лише цифри | `ArgumentException` |
| `ValidateDate` | `DateTime value`, `string fieldName` | не пізніше за сьогодні; не раніше 1900 року | `ArgumentOutOfRangeException` |
| `ValidatePositive` | `int value`, `string fieldName` | значення > 0 | `ArgumentOutOfRangeException` |

Методи нічого не повертають: або тихо завершуються (значення коректне), або кидають виняток. Параметр `fieldName` — назва поля для повідомлення й для `paramName`; передавайте з сеттера `nameof(...)` тієї властивості.

Які сеттери яким методом користуються:

| Сеттер | Метод валідатора |
|--------|------------------|
| `Patient.FirstName`, `Patient.LastName`, `Doctor.FirstName`, `Doctor.LastName` | `ValidateName` |
| `Patient.Phone`, `Doctor.Phone` | `ValidatePhone` |
| `Patient.DateOfBirth` | `ValidateDate` |
| `Appointment.DurationMinutes` | `ValidatePositive` |

### Приклад

Схема `try/catch` — на вигаданому класі `Thermometer`:

```csharp
try
{
    Thermometer t = new Thermometer();
    t.Celsius = -500;                      // кине ArgumentOutOfRangeException
    Console.WriteLine("Цей рядок не виконається");
}
catch (ArgumentOutOfRangeException e)
{
    Console.WriteLine("Помилка: " + e.Message);
}

Console.WriteLine("Програма продовжує роботу");
```

Вивід:

```
Помилка: Температура нижча за абсолютний нуль. (Parameter 'Celsius')
Програма продовжує роботу
```

Для вашого проєкту очікувана поведінка: користувач вводить некоректні дані в меню → бачить рядок «Помилка: …» → повертається до меню; програма **не падає**.

### Підказки

1. **Як працює `try/catch`.** Код у `try` виконується як звичайно; щойно виникає виняток — решта `try` пропускається й керування переходить у відповідний `catch`. Після `catch` програма продовжує працювати.
2. **Що класти в `try`.** Усе, що може кинути виняток через введення користувача. Пастка: `try` лише навколо `new Doctor(...)` **не** захистить від рядка «початок 20, кінець 6», бо `WorkSchedule` створюється окремим виразом. Перевірте вручну: введіть у меню «Додати лікаря» години `20` і `6`.
3. **Порядок блоків `catch` — спершу конкретніший тип.** `ArgumentOutOfRangeException` є «дочірнім» до `ArgumentException` (докладніше — в Лабі 06), тому має стояти першим. Якщо поставити загальніший першим, компілятор видасть помилку `CS0160`.
4. **`catch (Exception)`** ловить усе, що завгодно. Це розумно як останній «страховий» рубіж, але для очікуваних помилок вводу краще конкретні типи — інакше можна замаскувати справжні помилки програмування.
5. **Не «ковтайте» виняток мовчки.** Порожній `catch` — найгірше з можливого: користувач не побачить, чому нічого не сталось. Завжди показуйте повідомлення.
6. **Що дає виняток.** `e.Message` — текст пояснення; `e.GetType().Name` — назва типу винятку (зручно для налагодження).
7. **`finally` (необов'язково)** виконується завжди — і після `try`, і після `catch`. Потрібен для звільнення ресурсів; у цій лабі майже не знадобиться.
8. **Виняток, не перехоплений ніде,** завершує програму зі стеком викликів. `try/catch` — це межа між внутрішньою логікою і «зовнішнім світом» (ввід користувача, файли, мережа).
9. **Чому `ClinicValidator` — `static class`.** Він не має власного стану — лише правила, так само як `ClinicFormatter` з Лаби 04. Екземпляри не потрібні.
10. **(За бажанням)** перевірте номер enum, який вводить користувач у меню (`Enum.IsDefined`) — інакше `(BloodType)99` пройде повз усі ваші правила.

📖 Документація:
- [`try-catch`](https://learn.microsoft.com/dotnet/csharp/language-reference/statements/exception-handling-statements)
- [Винятки (основи)](https://learn.microsoft.com/dotnet/csharp/fundamentals/exceptions/)
- [Найкращі практики роботи з винятками](https://learn.microsoft.com/dotnet/standard/exceptions/best-practices-for-exceptions)
- [Статичні класи](https://learn.microsoft.com/dotnet/csharp/programming-guide/classes-and-structs/static-classes-and-static-class-members)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `ClinicValidator` | `HotelValidator` | `RestaurantValidator` | `UnivValidator` | `RentalValidator` | `LibraryValidator` | `GymValidator` |
| `ValidateName` | `ValidateName` | `ValidateName` | `ValidateName` | `ValidateName` | `ValidateName` | `ValidateName` |
| `ValidatePhone` | `ValidatePhone` | `ValidatePhone` | `ValidatePhone` | `ValidatePhone` | `ValidatePhone` | `ValidatePhone` |
| `ValidateDate` (не в майбутньому) | `ValidateBirthDate` (не в майбутньому) | `ValidateReservationDate` (**не в минулому**) | `ValidateEnrollmentDate` | `ValidateRentalStart` (**не в минулому**) | `ValidateLoanDate` | `ValidateSessionDate` (**не в минулому**) |
| `ValidatePositive` | `ValidatePositive` | `ValidatePositive` | `ValidatePositive` | `ValidatePositive` | `ValidatePositive` | `ValidatePositive` |

Там, де правило дати обертається (бронювання, оренда, заняття — мають бути **в майбутньому**), не копіюйте перевірку з клініки: перегляньте рядок про дату в таблиці Задачі 3.

### Коміт

```bash
git add ClinicApp/Utils/ClinicValidator.cs
git add ClinicApp/Models/Patient.cs ClinicApp/Models/Doctor.cs ClinicApp/Models/Appointment.cs
git add ClinicApp/Program.cs
git commit -m "Lab05 Task04"
```

---

## Задача 5 (опційна). Regex для телефону та email ⭐⭐⭐

### Умова

Регулярний вираз (`Regex`) — компактний спосіб перевірити, чи рядок відповідає шаблону. Ви перепишете перевірку телефону з циклу на `Regex` і додасте перевірку email.

**Що реалізувати:**

1. У `ValidatePhone` замінити цикл по символах на `Regex.IsMatch` — з **тими самими** правилами (рівно 10 цифр).
2. Додати в `ClinicValidator` метод `ValidateEmail(string email)`.
3. Підключити його: перетворіть `Email` у `Patient` на властивість з приватним полем `_email` (за схемою Задачі 2). **Порожній рядок означає «email невідомий» і дозволений**; непорожній має пройти `ValidateEmail`.
4. *Виклик (ще складніше):* підтримка номера у форматі `+38` + 10 цифр (разом 12 цифр) — див. підказку 6.

### Специфікація

**Що має вважатись коректним:**

| Вхід | Результат |
|------|-----------|
| `0501234567` | ✔ коректний телефон |
| `050123456` (9 цифр) | ✘ |
| `05012345678` (11 цифр) | ✘ |
| `050abc4567` | ✘ |
| `٠٥٠١٢٣٤٥٦٧` (10 арабо-індійських цифр) | ✘ — не ASCII-цифри |
| `0501234567` + перенос рядка в кінці | ✘ |
| `ivan@mail.com` | ✔ коректний email |
| `ivan@mail` (без крапки в домені) | ✘ |
| `iv an@mail.com` (пробіл) | ✘ |
| `a@@b.com` (два `@`) | ✘ |
| порожній рядок | ✔ для `Email` — «невідомо» |

**Елементи шаблонів, з яких ви складаєте власні:**

| Елемент | Значення |
|---------|----------|
| `^` | початок рядка |
| `\z` | кінець рядка (суворо) |
| `$` | кінець рядка **або перед кінцевим переносом** |
| `[0-9]` | одна цифра `0`–`9` (лише ASCII) |
| `\d` | одна цифра **будь-якого** алфавіту (Unicode) |
| `{n}` | рівно `n` повторень попереднього елемента |
| `+` | один або більше повторень |
| `[^@\s]` | будь-який символ, окрім `@` і пробільного |
| `\.` | буквальна крапка |

### Підказки

1. **`Regex.IsMatch(input, pattern)`** — статичний метод, повертає `bool`. Шаблони зручно писати у «дослівних» рядках `@"..."`, де зворотний слеш не потрібно екранувати.
2. **Перевіряйте шаблон на таблиці вище, а не «на око».** Особливо — на рядках з арабо-індійськими цифрами та з переносом у кінці. Регулярний вираз, який «майже такий самий, але коротший», може ненавмисно пропускати те, що цикл відхиляв.
3. **Пастка `\d` і `$`.** `\d` приймає цифри з інших алфавітів, а `$` пропускає рядок із кінцевим `\n`. Строго-ASCII перевірка потребує `[0-9]` і `\z`. Спробуйте самі, який шаблон відхилить усі рядки з таблиці.
4. **Чому `static readonly` поле.** Шаблон розбирається й компілюється в момент створення об'єкта `Regex`. Якщо тримати його в статичному `readonly`-полі — це станеться один раз, а не при кожній перевірці.
5. **Email — навмисно спрощена перевірка.** «Ідеального» шаблону для email не існує (формат надзвичайно складний). На практиці так перевіряють лише «схоже на email», а справжність підтверджують листом із посиланням.
6. **Виклик з `+38`.** `ClinicFormatter.FormatPhone` (Лаба 04) розрахований рівно на 10 цифр — довший номер він виведе «як є». Вирішіть: зберігати номер як ввели чи нормалізувати до 10 цифр, — і узгодьте це з форматером.
7. **Задача необов'язкова** — для здачі лаби не потрібна, але тренує читання документації й акуратність із граничними випадками.

📖 Документація:
- [Регулярні вирази в .NET](https://learn.microsoft.com/dotnet/standard/base-types/regular-expressions)
- [Мова регулярних виразів — швидкий довідник](https://learn.microsoft.com/dotnet/standard/base-types/regular-expression-language-quick-reference)
- [`Regex.IsMatch`](https://learn.microsoft.com/dotnet/api/system.text.regularexpressions.regex.ismatch)
- [Ключове слово `readonly`](https://learn.microsoft.com/dotnet/csharp/language-reference/keywords/readonly)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| телефон, email пацієнта | телефон, email гостя | телефон, email клієнта | email студента | телефон клієнта, номерний знак | номер читацького квитка | номер абонемента |
| — | код бронювання (напр. `AB-1234`) | номер столу | код групи | VIN / держномер | інвентарний номер книги | код картки |

Замість (або додатково до) телефону й email придумайте один свій шаблон для «коду» з вашого домену й перевірте його на трьох коректних та трьох некоректних рядках.

### Коміт

```bash
git add ClinicApp/Utils/ClinicValidator.cs ClinicApp/Models/Patient.cs
git commit -m "Lab05 Task05"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли виконано Задачі 1–4 (Задача 5 — опційна, її позначки нижче):

```text
oop-course/                          ← гілка Lab-05 (після злиття — main)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs                      ✏ Т1 Т4
    ├── Clinic.cs                       ✏ Т1
    ├── Enums/
    │   ├── AppointmentStatus.cs        📦 Т1
    │   ├── BloodType.cs                📦 Т1
    │   └── Speciality.cs               📦 Т1
    ├── Models/
    │   ├── Patient.cs                  📦 Т1  ✏ Т2 Т3 Т4 Т5
    │   ├── Doctor.cs                   📦 Т1  ✏ Т2 Т3 Т4
    │   ├── Appointment.cs              📦 Т1  ✏ Т2 Т3 Т4
    │   └── WorkSchedule.cs             📦 Т1  ✏ Т3
    ├── Managers/
    │   ├── PatientManager.cs           📦 Т1
    │   ├── DoctorManager.cs            📦 Т1
    │   ├── AppointmentManager.cs       📦 Т1
    │   └── GrowablePatientManager.cs   📦 Т1
    └── Utils/
        ├── ClinicFormatter.cs          📦 Т1
        └── ClinicValidator.cs          🆕 Т4  ✏ Т5
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · 📦 — лише переміщено (змінились тільки `namespace` і `using`) · Т*n* — номер задачі, у якій ви працюєте з файлом. Файл може мати кілька позначок, наприклад `Patient.cs` спершу переїжджає (Т1), а далі змінюється в Т2–Т5.

Зверніть увагу: у корені `ClinicApp/` лишились лише `Program.cs` і `Clinic.cs`. Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важлива структура підпапок.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] Проєкт компілюється без помилок і без попереджень
- [ ] Файли лежать у підпапках `Models/`, `Enums/`, `Managers/`, `Utils/`; у корені лише `Program.cs` і `Clinic.cs`
- [ ] Простір імен кожного файлу збігається з його папкою; `using` стоять на початку файлу
- [ ] `Patient`, `Doctor`, `Appointment` мають приватні поля `_camelCase`
- [ ] `new Patient("", "Петренко", …)` кидає `ArgumentException`
- [ ] Пацієнт із датою народження «завтра» — `ArgumentOutOfRangeException`
- [ ] `new WorkSchedule(20, 6)` кидає виняток
- [ ] Після двох невдалих спроб створити пацієнта коректний пацієнт отримує **наступний за попереднім успішним** `Id` — без «дірок»
- [ ] Меню «Додати пацієнта» з некоректними даними — **програма не падає**, показує «Помилка: …»
- [ ] Меню «Додати лікаря» з годинами `20` і `6` — **програма не падає**
- [ ] Меню «Записати» з тривалістю `-5` — **програма не падає**
- [ ] У `ClinicValidator` жодного правила не продубльовано в сеттерах (`FirstName`/`LastName`/`Phone`/`DateOfBirth`/`DurationMinutes`)
- [ ] Увесь попередній функціонал (пошук, запис, звіт) працює як раніше
- [ ] У коді немає `List<T>`, `Dictionary<,>`, LINQ, успадкування (`: Базовий`), `interface`

---

## Питання для самоперевірки

1. Що таке **інкапсуляція** і що таке **інваріант**? Наведіть інваріант для `Appointment`.
2. Яка різниця між `private string _name` і `public string Name { get; set; }`? Що саме «захищає» перший варіант, а другий — ні?
3. Навіщо приватне поле, якщо автовластивість теж «ховає» деталі? Що змінилось, коли ви перейшли на явну властивість?
4. Чому в сеттері перевірка має стояти **до** присвоєння, а не після?
5. Що станеться з `Id`, якщо в конструкторі `_nextId++` стоїть першим рядком, а наступний рядок кидає виняток? Як це виправити і чому?
6. У якому порядку мають стояти блоки `catch` для `ArgumentOutOfRangeException` та `ArgumentException`? Що скаже компілятор, якщо переплутати?
7. Чому `try` навколо одного лише `new Doctor(...)` не захищає від годин `20` і `6`?
8. Чому `LicenseNumber` і `WorkSchedule` не винесли в `ClinicValidator`, а імена й телефон — винесли? За яким принципом обирають, що централізувати?
9. `(BloodType)99` компілюється. Що це говорить про «захищеність» enum і де правильно ставити перевірку такого значення?
10. *(Опційна Задача 5)* Чим `\d` відрізняється від `[0-9]` і чим `$` від `\z`? Як ви це перевірили?

---

## Статус гілки

Після всіх завдань (кожне — окремий коміт `Lab05 TaskNN` на гілці `Lab-05`):

```bash
git push -u origin Lab-05
git checkout main
git merge --no-ff Lab-05 -m "Merge Lab-05: Encapsulation"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-06`.
