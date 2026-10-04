# Лаба 12 — File I/O (Робота з файлами)

## Мета

Навчитись читати та писати файли в C#: від простих `File.AppendAllText` до `StreamWriter` з форматуванням, CSV-парсингу з обробкою помилок та збереження стану між запусками програми.

## Контекст

Після Лаби 11 система вміє валідувати дані через рефлексію. Але все, що ввів користувач, зникає при закритті програми. Ця лаба додає **персистентність**: логування дій у файл, експорт звітів, імпорт даних з CSV та збереження сесії між запусками.

### Структура проєкту на початку лаби

Це результат Лаби 11 — стан `main` після її злиття:

```text
oop-course/                           ← гілка main (після злиття Лаби 11)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/  (15 файлів)
    ├── Managers/  (9 файлів)
    ├── Utils/
    │   ├── ClinicFormatter.cs
    │   ├── ClinicValidator.cs
    │   ├── FormBuilder.cs
    │   ├── ModelValidator.cs
    │   └── ValidationResult.cs
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    └── Attributes/  (3 файли)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Що нового дозволено (і тільки воно)

- клас `File`: `AppendAllText`, `ReadAllLines`, `Exists`, `Delete`;
- `StreamWriter` у блоці `using`;
- `Path.Combine` і `Directory.CreateDirectory`;
- `Encoding.UTF8`, `DateTime.ParseExact`, `Enum.Parse`.

Досі заборонено: LINQ (Лаба 14), делегати й лямбди (Лаби 13–15).

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-12
```

Коміт — на кожне завдання (`Lab12 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. `ClinicLogger`: журнал дій у файлі ⭐⭐

### Умова

Клініці потрібен журнал подій — файл `clinic.log`, куди записуються дії системи з часовою міткою. Треба також мати змогу переглянути останні N рядків, не відкриваючи файл вручну.

**Що реалізувати:**

1. Клас `ClinicLogger` у `ClinicApp/Utils/` з методами зі специфікації. Кожен запис дописується в кінець файлу.
2. У `Clinic.cs` додати властивість `Logger` і створити `ClinicLogger` у конструкторі.
3. У `Program.cs` записувати в лог ключові дії: додавання пацієнта й лікаря, запис на прийом, скасування й завершення запису, оплату (`LogInfo`); помилки введення в `catch` (`LogWarning`).
4. У головному меню додати пункт `10` — «Файли» з двома пунктами: «Останні рядки лога» (запитує N) і «Очистити лог».

### Специфікація

| Член `ClinicLogger` | Опис |
|---------------------|------|
| конструктор `(string logPath = "clinic.log")` | шлях до файлу лога |
| `LogInfo(string message)` | запис рівня `INFO` |
| `LogWarning(string message)` | запис рівня `WARN` |
| `LogError(string message)` | запис рівня `ERROR` |
| `GetLastLines(int n)` | `string[]` — останні `n` рядків; порожній масив, якщо файлу немає |
| `Clear()` | очистити лог |
| `Exists()` | `bool` — чи існує файл |

Формат рядка: `[yyyy-MM-dd HH:mm:ss] [LEVEL] message`.

### Приклад

```
[2026-10-15 10:02:11] [INFO ] Додано пацієнта #6: Марія Ткач
[2026-10-15 10:03:40] [INFO ] Запис #9 створено: пацієнт #6 → лікар #2
[2026-10-15 10:04:05] [WARN ] Помилка введення: Телефон має містити рівно 10 цифр.
```

### Підказки

1. `File.AppendAllText(path, text, encoding)` — дописує в кінець файлу, не перезаписує. Якщо файл не існує — створює автоматично.
2. `File.ReadAllLines(path, encoding)` — зчитує **всі** рядки у масив `string[]`. Для великих файлів це дорого, але для лога прийнятно.
3. `Encoding.UTF8` — обов'язково для кирилиці (`using System.Text;`).
4. `Environment.NewLine` — правильний перенос рядка для поточної ОС.
5. Останні N рядків: визначте, скільки рядків пропустити з початку (не менше нуля), і скопіюйте решту в новий масив.
6. Один приватний метод запису, який викликають `LogInfo`/`LogWarning`/`LogError`, — щоб формат рядка був в одному місці.

📖 Документація:
- [`File.AppendAllText`](https://learn.microsoft.com/dotnet/api/system.io.file.appendalltext)
- [`File.ReadAllLines`](https://learn.microsoft.com/dotnet/api/system.io.file.readalllines)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `ClinicLogger` → `clinic.log` | `HotelLogger` → `hotel.log` | `RestaurantLogger` → `restaurant.log` | `UniversityLogger` → `uni.log` | `RentalLogger` → `rental.log` | `LibraryLogger` → `library.log` | `GymLogger` → `gym.log` |

### Коміт

```bash
git add ClinicApp/Utils/ClinicLogger.cs ClinicApp/Clinic.cs ClinicApp/Program.cs
git commit -m "Lab12 Task01"
```

---

## Задача 2. `ClinicExporter`: звіти у файли через `StreamWriter` ⭐⭐

### Умова

Адміністратор хоче отримувати готові текстові звіти у файлах — із заголовком, датою генерації і підсумком. Файли зберігаються в теці з датою: `reports/2026-10-15/`.

**Що реалізувати:**

1. Клас `ClinicExporter` у `ClinicApp/Utils/`: отримує `Clinic` і базову теку через конструктор.
2. Чотири методи експорту зі специфікації; кожен пише окремий файл і повертає шлях до нього.
3. Метод `ExportAll()` — викликає всі чотири експорти.
4. У `Clinic.cs` додати властивість `Exporter`; у меню «Файли» додати пункт `3` — «Експортувати всі звіти» (виводить шляхи створених файлів).

### Специфікація

| Член `ClinicExporter` | Файл | Вміст |
|-----------------------|------|-------|
| конструктор `(Clinic clinic, string baseDir = "reports")` | | |
| `ExportPatients()` | `patients.txt` | усі пацієнти |
| `ExportAppointments()` | `appointments.txt` | усі записи |
| `ExportBilling()` | `billing.txt` | неоплачені записи і загальний борг |
| `ExportTreatmentPlans()` | `treatment_plans.txt` | усі плани лікування |
| `ExportAll()` | | викликає всі чотири, повертає `string[]` шляхів |

Кожен файл: заголовок з назвою звіту і датою генерації, роздільник, нумеровані рядки даних, підсумок (кількість). Тека — `reports/yyyy-MM-dd/`, створюється автоматично.

### Приклад

```
=== Пацієнти — звіт ===
Згенеровано: 15.10.2026 10:20
----------------------------------------
  1. [1] Іван Петренко | 41 рік | A+ | (050) 123-4567
  2. [2] Олена Коваль  | 33 роки | B- | (067) 234-5678
----------------------------------------
Всього: 2
```

### Підказки

1. `StreamWriter(path, false, encoding)` — `false` означає перезаписати файл, якщо він існує.
2. `using StreamWriter writer = new StreamWriter(...)` автоматично закриває файл при виході з блоку. Без `using` файл може лишитись відкритим.
3. `Directory.CreateDirectory(dir)` створює теку і всі батьківські теки; **не кидає виняток**, якщо тека вже існує.
4. `Path.Combine("reports", "2026-10-15", "patients.txt")` склеює шлях правильно для будь-якої ОС — не збирайте шлях конкатенацією з `/`.
5. Створення теки з датою винесіть в один приватний метод — його використовують усі чотири експорти.
6. `{i + 1,3}` у рядку з інтерполяцією вирівнює номер по правому краю в 3 символи.

📖 Документація:
- [`StreamWriter`](https://learn.microsoft.com/dotnet/api/system.io.streamwriter)
- [`Path.Combine`](https://learn.microsoft.com/dotnet/api/system.io.path.combine)
- [`Directory.CreateDirectory`](https://learn.microsoft.com/dotnet/api/system.io.directory.createdirectory)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `ClinicExporter` | `HotelExporter` | `RestaurantExporter` | `UniversityExporter` | `RentalExporter` | `LibraryExporter` | `GymExporter` |
| `ExportPatients/Appointments/Billing` | `ExportGuests/Bookings/Invoices` | `ExportCustomers/Reservations/Orders` | `ExportStudents/Courses/Grades` | `ExportClients/Rentals/Invoices` | `ExportReaders/Loans/Fines` | `ExportMembers/Sessions/Payments` |

### Коміт

```bash
git add ClinicApp/Utils/ClinicExporter.cs ClinicApp/Clinic.cs ClinicApp/Program.cs
git commit -m "Lab12 Task02"
```

---

## Задача 3. `CsvImporter`: імпорт пацієнтів з помилковими рядками ⭐⭐⭐

### Умова

Адміністратор отримав список нових пацієнтів у форматі CSV і хоче завантажити їх одним файлом. CSV може містити помилкові рядки — їх треба пропустити і повідомити про кожен окремо, не зупиняючи імпорт.

**Що реалізувати:**

1. Клас `ImportResult` у `ClinicApp/Utils/` — підсумок імпорту (специфікація нижче).
2. Клас `CsvImporter` у `ClinicApp/Utils/` з методом `ImportPatients(Clinic clinic, string filePath)`: читає файл, створює пацієнтів і додає їх у `clinic.Patients`.
3. Перший рядок (заголовок) і порожні рядки пропускати; помилковий рядок записувати в `ImportResult` з номером і причиною, імпорт продовжувати.
4. У меню «Файли» додати пункт `4` — «Імпорт пацієнтів з CSV»: запитує шлях до файлу і виводить підсумок.

### Специфікація

Формат CSV:

```
FirstName,LastName,DateOfBirth,BloodType,Phone
Іван,Петренко,15.03.1985,APositive,0501234567
Олена,Коваль,22.07.1992,BNegative,0672345678
НеПравильний рядок
,Ткач,01.01.2000,,
```

| Член `ImportResult` | Опис |
|---------------------|------|
| `Imported` | кількість імпортованих (`private set`) |
| `Skipped` | кількість пропущених (`private set`) |
| `Errors` | список помилок лише для читання |
| `AddSuccess()` | +1 до `Imported` |
| `AddError(int lineNumber, string reason)` | +1 до `Skipped`, помилка `"Рядок N: причина"` |
| `Print()` | підсумок і всі помилки |

Якщо файлу немає — одна помилка з номером рядка `0`.

### Приклад

```
Імпортовано: 2 | Пропущено: 2
  Рядок 4: Рядок має 1 поле замість 5.
  Рядок 5: Ім'я не може бути порожнім.
```

### Підказки

1. `try/catch` — **навколо обробки одного рядка**, а не навколо всього циклу: помилка в рядку 3 не повинна зупинити рядки 4, 5, 6.
2. `line.Split(',')` повертає `string[]`. Перевірте кількість полів перед зверненням до `parts[2]` — рядок може мати менше полів.
3. `DateTime.ParseExact(str, "dd.MM.yyyy", CultureInfo.InvariantCulture)` — суворий парсинг дати (`using System.Globalization;`).
4. `Enum.Parse(typeof(BloodType), str)` кидає виняток, якщо рядок не відповідає жодному значенню enum — `catch` його перехопить.
5. Валідація пацієнта з Лаби 05 спрацює сама: некоректне ім'я чи телефон кине виняток у конструкторі.
6. Номер рядка для людини — індекс у масиві плюс один.

📖 Документація:
- [`String.Split`](https://learn.microsoft.com/dotnet/api/system.string.split)
- [`DateTime.ParseExact`](https://learn.microsoft.com/dotnet/api/system.datetime.parseexact)
- [`Enum.Parse`](https://learn.microsoft.com/dotnet/api/system.enum.parse)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `ImportPatients` | `ImportGuests` | `ImportCustomers` | `ImportStudents` | `ImportClients` | `ImportReaders` | `ImportMembers` |

### Коміт

```bash
git add ClinicApp/Utils/ImportResult.cs ClinicApp/Utils/CsvImporter.cs ClinicApp/Program.cs
git commit -m "Lab12 Task03"
```

---

## Задача 4. `SessionManager`: збереження пацієнтів між запусками ⭐⭐⭐

### Умова

Зараз при кожному запуску програми дані починаються з нуля — пацієнти, яких додав користувач, зникають. Збережіть список пацієнтів у файл `session.dat` при виході і відновіть його при наступному старті.

**Що реалізувати:**

1. Клас `SessionManager` у `ClinicApp/Utils/` з методами зі специфікації.
2. У `Clinic.cs` додати властивість `Session`.
3. У `Program.cs` на старті (після початкових даних): якщо сесія існує — запитати «Завантажити? (y/n)» і завантажити.
4. У `Program.cs` при виході (пункт `0`): запитати «Зберегти сесію? (y/n)» і зберегти.

### Специфікація

Формат файлу:

```
[PATIENTS]
Іван,Петренко,15.03.1985,APositive,0501234567
Олена,Коваль,22.07.1992,BNegative,0672345678
[END]
```

| Член `SessionManager` | Опис |
|-----------------------|------|
| конструктор `(string sessionPath = "session.dat")` | шлях до файлу сесії |
| `Exists()` | `bool` — чи є збережена сесія |
| `Save(Clinic clinic)` | перезаписує файл: секція `[PATIENTS]`, рядок на пацієнта, `[END]` |
| `Load(Clinic clinic)` | `int` — скільки пацієнтів додано; `0`, якщо файлу немає |

Правила `Load`: рядки до першої секції і порожні — ігнорувати; пошкоджений рядок — пропустити; пацієнта, який уже є в системі (те саме ім'я, прізвище і дата народження), — не додавати вдруге.

### Приклад

```
Знайдено збережену сесію. Завантажити? (y/n): y
Завантажено 2 пацієнтів.
…
Зберегти сесію? (y/n): y
Сесію збережено.
```

### Підказки

1. Рядок, що починається з `[`, — заголовок секції. Запам'ятайте поточну секцію і обробляйте наступні рядки відповідно до неї — так у майбутньому легко додати `[APPOINTMENTS]`.
2. Сесія зберігає **всіх** пацієнтів, включно з початковими. Тому без перевірки «вже є» кожен запуск дублюватиме початкових пацієнтів.
3. Пошкоджений рядок пропускайте в `catch` — краще завантажити 9 з 10 пацієнтів, ніж впасти.
4. `_nextId` у `Patient` — статичний: завантажені пацієнти отримають **нові** `Id`. Для цієї лаби це нормально.
5. `{p.DateOfBirth:dd.MM.yyyy}` — форматування дати в рядку з інтерполяцією.

📖 Документація:
- [`StreamWriter`](https://learn.microsoft.com/dotnet/api/system.io.streamwriter)
- [`String.StartsWith`](https://learn.microsoft.com/dotnet/api/system.string.startswith)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `[PATIENTS]` | `[GUESTS]` | `[CUSTOMERS]` | `[STUDENTS]` | `[CLIENTS]` | `[READERS]` | `[MEMBERS]` |

### Коміт

```bash
git add ClinicApp/Utils/SessionManager.cs ClinicApp/Clinic.cs ClinicApp/Program.cs
git commit -m "Lab12 Task04"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                           ← гілка Lab-12 (після злиття — main)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs                    ✏ Т1 Т2 Т3 Т4
    ├── Clinic.cs                     ✏ Т1 Т2 Т4
    ├── Enums/  (4 файли)
    ├── Models/  (15 файлів)
    ├── Managers/  (9 файлів)
    ├── Utils/
    │   ├── ClinicFormatter.cs
    │   ├── ClinicValidator.cs
    │   ├── FormBuilder.cs
    │   ├── ModelValidator.cs
    │   ├── ValidationResult.cs
    │   ├── ClinicLogger.cs           🆕 Т1
    │   ├── ClinicExporter.cs         🆕 Т2
    │   ├── ImportResult.cs           🆕 Т3
    │   ├── CsvImporter.cs            🆕 Т3
    │   └── SessionManager.cs         🆕 Т4
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    └── Attributes/  (3 файли)
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 11.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] Після додавання пацієнта в `clinic.log` з'являється рядок `[yyyy-MM-dd HH:mm:ss] [INFO ] …`
- [ ] «Файли» → «Останні рядки лога» показує N останніх записів
- [ ] Папка `reports/yyyy-MM-dd/` створюється автоматично; у кожному звіті — заголовок, дата генерації, підсумок
- [ ] CSV з 1 помилковим рядком із 5: `Імпортовано: 4 | Пропущено: 1` + деталі
- [ ] Після збереження сесії, перезапуску і «y» — додані раніше пацієнти знову в системі, початкові не дублюються
- [ ] Пошкоджений рядок у `session.dat` не зупиняє завантаження решти

---

## Питання для самоперевірки

1. Чим `File.WriteAllText` відрізняється від `File.AppendAllText`? Коли кожен з них доречний?
2. Чому `using StreamWriter writer = ...` важливіший за просто `StreamWriter writer = new ...`? Що станеться, якщо не закрити потік?
3. Чому `Path.Combine` краще за конкатенацію рядків `"reports/" + date + "/file.txt"`?
4. У `CsvImporter` `try/catch` обгортає обробку одного рядка, а не весь цикл. Яка різниця з точки зору поведінки?
5. `SessionManager.Load` повертає `int`, а не `bool`. Чому це краще?
6. `File.ReadAllLines` завантажує весь файл у пам'ять. Коли це стає проблемою і що використовувати натомість?

---

## Статус гілки

Після всіх 4 завдань (кожне — окремий коміт `Lab12 TaskNN` на гілці `Lab-12`):

```bash
git push -u origin Lab-12
git checkout main
git merge --no-ff Lab-12 -m "Merge Lab-12: File I/O"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-13`.
