# Лаба 14 — LINQ

## Мета

Зрозуміти різницю між імперативним і декларативним стилем роботи з колекціями. Навчитись виражати запити до даних через LINQ-оператори `.Where`, `.Select`, `.GroupBy`, `.Join`, `.OrderBy`, `.Any`, `.Sum`, `.Count`, `.Max`, `.Take`, `.Distinct` — і розуміти, коли і чому кожен з них доречний.

## Контекст

Відкрийте `ClinicApp/Managers/AnalyticsManager.cs` і знайдіть метод `ComputeDoctorStats`. Він рахує статистику по кожному лікарю: скільки прийомів, яка виручка, коли останній прийом. Скільки рядків займає ця логіка?

Тепер прочитайте той самий алгоритм словами:
> *«Для кожного лікаря — знайди всі його прийоми, порахуй їх кількість, склади вартість, знайди найпізнішу дату.»*

Одне речення. А в коді — десятки рядків із вкладеними циклами і тимчасовими змінними.

**LINQ** (Language Integrated Query) — набір методів, що дозволяє писати запити до колекцій так само лаконічно, як ви їх описуєте словами. Це не нова мова, а бібліотека методів розширення над `IEnumerable<T>`, який ви вже знаєте з Лаби 10.

| Цикл (імперативно) | LINQ (декларативно) |
|--------------------|---------------------|
| Описує **як** перебирати | Описує **що** отримати |
| Тимчасові змінні-лічильники | Результат — вираз |
| Важко читати з першого погляду | Читається майже як речення |

### Структура проєкту на початку лаби

Це результат Лаби 13 — стан `main` після її злиття:

```text
oop-course/                           ← гілка main (після злиття Лаби 13)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (4 файли)
    ├── Models/  (15 файлів)
    ├── Managers/
    │   ├── AnalyticsManager.cs
    │   └── … ще 8 файлів без змін
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    └── Events/  (4 файли)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Що нового дозволено (і тільки воно)

- LINQ-оператори (`using System.Linq;`) над масивами і списками;
- лямбда-вирази як аргументи LINQ-операторів (`a => a.DoctorId == d.Id`);
- анонімні типи (`new { ... }`) і кортежі (`(int Year, int Month, decimal Total)`).

Досі заборонено: змінні типів `Func<>` / `Action<>` і методи розширення власного написання (Лаба 15).

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-14
```

Коміт — на кожне завдання (`Lab14 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. Рефакторинг `AnalyticsManager` на LINQ ⭐⭐

### Умова

Кожен цикл по прийомах усередині циклу по лікарях — це по суті **фільтрація** (`Where`) і **агрегація** (`Count`, `Sum`, `Max`). Перепишіть обидва методи `AnalyticsManager` через LINQ.

**Що реалізувати:**

1. Переписати `ComputeDoctorStats()`: прийоми лікаря відібрати через `Where`, кількість — `Count()`, виручку — `Sum(...)`, останню дату — `Max(...)`; усіх лікарів перетворити на `DoctorStats` через `Select`.
2. Переписати `ComputePatientStats()` так само.
3. Сигнатури методів і тип результату не змінювати.
4. Перевірити, що пункт `8. Аналітика` дає ті самі результати, що й до рефакторингу.

### Специфікація

| Що рахуємо | Оператор |
|------------|----------|
| прийоми лікаря | `.Where(a => a.DoctorId == d.Id)` |
| кількість | `.Count()` |
| виручка | `.Sum(a => a.GetCost())` |
| останній прийом | `.Max(a => a.ScheduledAt)`, якщо прийоми є; інакше `DateTime.MinValue` |
| статистика для всіх | `.Select(d => new DoctorStats(...))` |

### Приклад

Вивід пункту `8. Аналітика` → «Лікарі за навантаженням» не змінився:

```
[2] Наталія Мороз  | Прийомів: 3 | Виручка: 1230.00 грн | Останній: 16.10.2026
[1] Олег Сидоренко | Прийомів: 2 | Виручка: 600.00 грн | Останній: 15.10.2026
```

### Підказки

1. **Порожня послідовність.** `.Max()` кидає виняток, якщо елементів немає. Перед ним перевірте `.Any()` і для лікаря без прийомів поверніть `DateTime.MinValue`.
2. Масив прийомів отримайте **один раз** перед `Select`, а не всередині: інакше `GetAll()` викликатиметься для кожного лікаря.
3. Якщо в `Select` потрібна проміжна змінна (прийоми одного лікаря), використайте лямбду з тілом у фігурних дужках і `return`.
4. `Select` повертає `IEnumerable<DoctorStats>` — тип результату методу лишається тим самим.

📖 Документація:
- [LINQ (огляд)](https://learn.microsoft.com/dotnet/csharp/linq/)
- [`Enumerable.Where`](https://learn.microsoft.com/dotnet/api/system.linq.enumerable.where) / [`Select`](https://learn.microsoft.com/dotnet/api/system.linq.enumerable.select)
- [Лямбда-вирази](https://learn.microsoft.com/dotnet/csharp/language-reference/operators/lambda-expressions)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `ComputeDoctorStats` на LINQ | `ComputeStaffStats` | `ComputeWaiterStats` | `ComputeLecturerStats` | `ComputeManagerStats` | `ComputeLibrarianStats` | `ComputeTrainerStats` |

### Коміт

```bash
git add ClinicApp/Managers/AnalyticsManager.cs
git commit -m "Lab14 Task01"
```

---

## Задача 2. Клас звіту `SpecialityReport` ⭐

### Умова

Звіт по спеціальностях повертатиме для кожної спеціальності кілька чисел одночасно: кількість лікарів, кількість прийомів, загальну виручку. Можна було б повертати кортеж, але іменований клас читається краще і дозволяє додати `ToString()`.

**Що реалізувати:**

1. Створити клас `SpecialityReport` у `ClinicApp/Models/` з чотирма властивостями лише для читання (специфікація нижче), заповненими через конструктор.
2. Перевизначити `ToString()`: один рядок з усіма чотирма значеннями, за зразком `DoctorStats.ToString()`.

### Специфікація

| Властивість | Тип |
|-------------|-----|
| `Speciality` | `Speciality` (enum) |
| `DoctorCount` | `int` |
| `AppointmentCount` | `int` |
| `TotalRevenue` | `decimal` |

### Приклад

```
Кардіологія | Лікарів: 2 | Прийомів: 5 | Виручка: 1830.00 грн
```

### Підказки

1. Українську назву спеціальності дає `ClinicFormatter.FormatSpeciality` (Лаба 04).

📖 Документація:
- [Властивості лише для читання](https://learn.microsoft.com/dotnet/csharp/programming-guide/classes-and-structs/properties#read-only)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `SpecialityReport` | `DepartmentReport` | `CuisineReport` | `FacultyReport` | `CarClassReport` | `SectionReport` | `TrainingTypeReport` |

### Коміт

```bash
git add ClinicApp/Models/SpecialityReport.cs
git commit -m "Lab14 Task02"
```

---

## Задача 3. `ReportManager`: сім звітів через LINQ ⭐⭐⭐

### Умова

`AnalyticsManager` уже має чітку відповідальність — статистика по лікарях і пацієнтах для сортування. Нові звіти мають іншу природу (групування, топ-N, місячна виручка), тож для них — окремий клас.

**Що реалізувати:**

1. Створити клас `ReportManager` у `ClinicApp/Managers/`, конструктор приймає ті самі три менеджери, що й `AnalyticsManager`.
2. Реалізувати сім методів зі специфікації — кожен через вказані LINQ-оператори, без циклів.

### Специфікація

| Метод | Повертає | Що рахує | Оператори |
|-------|----------|----------|-----------|
| `GetSpecialityStats()` | `IEnumerable<SpecialityReport>` | для кожної спеціальності: кількість лікарів, їхніх прийомів і виручку; за виручкою спадно | `GroupBy`, `Contains`, `OrderByDescending` |
| `FindBusiestDoctorName()` | `string?` | ім'я лікаря з найбільшою кількістю прийомів; `null`, якщо лікарів немає | `OrderByDescending`, `FirstOrDefault` |
| `GetPatientsWithMultipleVisits(int minVisits)` | `IEnumerable<string>` | імена пацієнтів, у яких щонайменше `minVisits` прийомів | `GroupBy`, `Where`, `Join` |
| `GetTopEarners(int n)` | `IEnumerable<DoctorStats>` | `n` лікарів з найбільшою виручкою | `OrderByDescending`, `Take` |
| `HasAnyUrgentAppointments()` | `bool` | чи є хоч один терміновий прийом | `Any` + `is UrgentAppointment` |
| `GetActiveSpecialities()` | `IEnumerable<Speciality>` | унікальні спеціальності лікарів, упорядковані | `Select`, `Distinct`, `OrderBy` |
| `GetMonthlyRevenue()` | `IEnumerable<(int Year, int Month, decimal Total)>` | виручка по кожному місяцю; за роком, потім місяцем | `GroupBy` з анонімним ключем, `OrderBy`, `ThenBy` |

### Приклад

```
GetMonthlyRevenue():
2026/09 — 1350.00 грн
2026/10 — 2280.00 грн
```

### Підказки

1. **`GroupBy`** розкладає елементи у «стопки» за ключем: кожна група має `Key` і елементи. Для спеціальностей ключ — `d.Speciality`.
2. **Прийоми групи лікарів:** зберіть ID лікарів групи в масив і відберіть прийоми, чий `DoctorId` міститься в цьому масиві (`Contains`).
3. **`Join`** з'єднує дві колекції за спільним ключем, як `JOIN` у SQL: ключ групи прийомів — `PatientId`, ключ пацієнта — `Id`.
4. **`Take(n)`** ставиться **після** сортування — інакше ви візьмете випадкові `n`.
5. **`Any(умова)`** зупиняється на першому збігу — це ефективніше, ніж `Count(...) > 0`.
6. **Анонімний ключ** `new { a.ScheduledAt.Year, a.ScheduledAt.Month }` групує одночасно за роком і місяцем; далі — `g.Key.Year`, `g.Key.Month`.
7. **`GetTopEarners`** потребує тієї самої статистики, що й `AnalyticsManager.ComputeDoctorStats()`. Не дублюйте логіку — подумайте, як її перевикористати.

📖 Документація:
- [`GroupBy`](https://learn.microsoft.com/dotnet/api/system.linq.enumerable.groupby)
- [`Join`](https://learn.microsoft.com/dotnet/api/system.linq.enumerable.join)
- [`OrderBy` / `ThenBy`](https://learn.microsoft.com/dotnet/api/system.linq.enumerable.orderby)
- [Анонімні типи](https://learn.microsoft.com/dotnet/csharp/fundamentals/types/anonymous-types)
- [Кортежі](https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/value-tuples)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `GetSpecialityStats` | `GetDepartmentStats` | `GetCuisineStats` | `GetFacultyStats` | `GetCarClassStats` | `GetSectionStats` | `GetTrainingTypeStats` |
| `HasAnyUrgentAppointments` | `HasAnySuiteBookings` | `HasAnyPrivateRooms` | `HasAnyIntensiveCourses` | `HasAnyPremiumRentals` | `HasAnyResearchLoans` | `HasAnyPersonalTrainings` |

### Коміт

```bash
git add ClinicApp/Managers/ReportManager.cs
git commit -m "Lab14 Task03"
```

---

## Задача 4. Меню «Звіти» ⭐

### Умова

Підключіть `ReportManager` до клініки і меню.

**Що реалізувати:**

1. У `Clinic.cs` додати властивість `Reports` і створити `ReportManager` у конструкторі з `Appointments`, `Doctors`, `Patients`.
2. У головному меню додати пункт `11` — «Звіти».
3. У `Program.cs` додати функцію `ReportsMenu(Clinic clinic)` — сім пунктів, по одному на кожен метод `ReportManager` (специфікація нижче).

### Специфікація

| Пункт | Метод | Особливості |
|-------|-------|-------------|
| `1` — Спеціальності | `GetSpecialityStats()` | |
| `2` — Найзавантаженіший лікар | `FindBusiestDoctorName()` | якщо `null` — «немає лікарів» |
| `3` — Пацієнти з кількома візитами | `GetPatientsWithMultipleVisits(n)` | спершу запитує мінімальну кількість візитів |
| `4` — Топ-3 лікарів за виручкою | `GetTopEarners(3)` | вивід з нумерацією |
| `5` — Чи є термінові записи | `HasAnyUrgentAppointments()` | «Так» / «Ні» |
| `6` — Активні спеціальності | `GetActiveSpecialities()` | |
| `7` — Виручка по місяцях | `GetMonthlyRevenue()` | формат `2026/05 — 1350.00 грн` |
| `0` — Назад | | |

### Приклад

```
── Звіти ───────────────────────
Оберіть: 4
  1. Наталія Мороз  — 1230.00 грн
  2. Олег Сидоренко — 600.00 грн
  3. Андрій Власенко — 300.00 грн
```

### Підказки

1. Місяць у форматі з двох цифр: `Month.ToString("D2")`.

📖 Документація:
- [Рядки стандартного числового формату](https://learn.microsoft.com/dotnet/standard/base-types/standard-numeric-format-strings)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `11. Звіти` | `11. Звіти` | `11. Звіти` | `11. Звіти` | `11. Звіти` | `11. Звіти` | `11. Звіти` |

### Коміт

```bash
git add ClinicApp/Clinic.cs ClinicApp/Program.cs
git commit -m "Lab14 Task04"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                           ← гілка Lab-14 (після злиття — main)
├── .gitignore
├── oop-course.sln
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs                    ✏ Т4
    ├── Clinic.cs                     ✏ Т4
    ├── Enums/  (4 файли)
    ├── Models/
    │   ├── SpecialityReport.cs       🆕 Т2
    │   └── … ще 15 файлів без змін
    ├── Managers/
    │   ├── AnalyticsManager.cs       ✏ Т1
    │   ├── ReportManager.cs          🆕 Т3
    │   └── … ще 8 файлів без змін
    ├── Utils/  (12 файлів)
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    ├── Attributes/  (3 файли)
    └── Events/  (4 файли)
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 13.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] `8. Аналітика` після рефакторингу дає ті самі результати, що й раніше
- [ ] `11. Звіти` → `1`: спеціальності з кількістю лікарів і виручкою, за виручкою спадно
- [ ] `2`: ім'я лікаря з найбільшою кількістю записів
- [ ] `3` при введенні `1`: усі пацієнти, що мають хоч один запис
- [ ] `4`: три лікарі за виручкою спадно
- [ ] `5`: повідомлення про наявність або відсутність термінових записів
- [ ] `7`: рядки виду `2026/05 — 1350.00 грн`
- [ ] У `ReportManager` і переписаному `AnalyticsManager` немає циклів `for` / `foreach`

---

## Питання для самоперевірки

1. Чим `.Where()` відрізняється від `.Select()`? Що кожен з них повертає?
2. Чому `.Max()` на порожній послідовності кидає виняток, а `.FirstOrDefault()` — ні?
3. Що таке `g.Key` у `.GroupBy()`? Якого він типу в `GetSpecialityStats` і в `GetMonthlyRevenue`?
4. `.Any()` і `.Count() > 0` дають однаковий результат. В чому різниця з точки зору продуктивності?
5. `.Take(n)` стоїть **після** `.OrderByDescending()`. Що станеться, якщо поміняти їх місцями?
6. У `GetMonthlyRevenue` ключ `GroupBy` — анонімний тип `new { Year, Month }`. Як C# порівнює два такі об'єкти на рівність?
7. Чому погано викликати `_appointments.GetAll()` усередині `Select` для кожного лікаря?

---

## Статус гілки

Після всіх 4 завдань (кожне — окремий коміт `Lab14 TaskNN` на гілці `Lab-14`):

```bash
git push -u origin Lab-14
git checkout main
git merge --no-ff Lab-14 -m "Merge Lab-14: LINQ"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-15`.
