# Лаба 10 — Iterators & Comparators (Ітератори і компаратори)

## Мета

Навчитись реалізовувати `IComparable<T>` і `IComparer<T>` для управління порядком сортування об'єктів, а також `IEnumerable<T>` з `yield return` для лінивої генерації послідовностей. Побудувати аналітичний модуль клініки, де ці концепції мають природний практичний сенс.

## Контекст

Система вже накопичує дані: пацієнти, лікарі, записи на прийом. Але відповісти на питання «хто з лікарів прийняв найбільше пацієнтів?» або «хто з пацієнтів витратив найбільше?» неможливо. Це задача аналітики: обчислити статистику по кожному об'єкту і відсортувати за різними критеріями.

Порівняння і сортування в C# будуються на двох інтерфейсах:
- `IComparable<T>` — **природний порядок**: клас сам знає, як порівнювати себе з іншим. Один порядок, вбудований у тип.
- `IComparer<T>` — **зовнішній компаратор**: окремий клас реалізує один критерій сортування. Таких компараторів можна мати скільки завгодно.

Генерація даних для аналітики природно виражається через `IEnumerable<T>` з `yield return` — ліниве обчислення статистики для кожного об'єкта по черзі, замість того щоб спочатку побудувати весь масив у пам'яті.

### Структура проєкту на початку лаби

Це результат Лаби 09 — стан `main` після її злиття:

```text
oop-course/                           ← гілка main (після злиття Лаби 09)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (3 файли)
    ├── Models/  (12 файлів)
    ├── Managers/  (7 файлів)
    ├── Utils/  (2 файли)
    └── Interfaces/  (4 файли)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Що нового дозволено (і тільки воно)

- інтерфейси `IComparable<T>` і `IComparer<T>`;
- `Array.Sort()` і `List<T>.Sort()` — без аргументу і з компаратором;
- `IEnumerable<T>` і `yield return`.

Досі заборонено: LINQ (Лаба 14), делегати й лямбди (Лаби 13–15).

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-10
```

Коміт — на кожне завдання (`Lab10 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. `DoctorStats` і природний порядок через `IComparable<T>` ⭐⭐

### Умова

Клініці потрібен об'єкт — аналітичний знімок по лікарю: скільки прийомів провів, яка загальна виручка, коли був останній прийом. Цей об'єкт має вміти порівнювати себе з іншим таким об'єктом, щоб масив `DoctorStats[]` можна було відсортувати одним викликом `Array.Sort()`.

**Що реалізувати:**

1. Створити клас `DoctorStats` у `ClinicApp/Models/DoctorStats.cs` з властивостями зі специфікації (лише для читання).
2. Конструктор отримує всі п'ять значень і присвоює їх властивостям.
3. Реалізувати `IComparable<DoctorStats>`: лікар із більшою кількістю прийомів стоїть **першим** після `Array.Sort()`.
4. Перевизначити `ToString()`: один рядок — ID, ім'я, кількість прийомів, виручка, дата останнього прийому.

### Специфікація

| Властивість | Тип | Опис |
|-------------|-----|------|
| `DoctorId` | `int` | ID лікаря |
| `FullName` | `string` | Повне ім'я |
| `AppointmentCount` | `int` | Загальна кількість прийомів |
| `TotalRevenue` | `decimal` | Сума `GetCost()` по всіх прийомах |
| `LastAppointmentDate` | `DateTime` | Дата останнього прийому; `DateTime.MinValue`, якщо прийомів немає |

### Приклад

```csharp
DoctorStats[] arr =
{
    new DoctorStats(1, "Олег Сидоренко", 2, 600m, DateTime.Today),
    new DoctorStats(2, "Наталія Мороз",  5, 1500m, DateTime.Today),
};
Array.Sort(arr);
Console.WriteLine(arr[0].FullName);   // Наталія Мороз — 5 прийомів
```

### Підказки

1. `IComparable<T>` вимагає один метод: `int CompareTo(T? other)`. Він повертає від'ємне число, якщо `this` йде перед `other`, нуль — якщо рівні, додатне — якщо `this` йде після.
2. Щоб більша кількість прийомів опинилась першою, порівнюйте навпаки — `other` з `this`, а не `this` з `other`. Перевірте на папері: лікар А = 5 прийомів, лікар Б = 2 — після `Sort()` А має бути першим.
3. `DateTime.MinValue` — константа «найраніша можлива дата». Зручна як маркер «прийомів не було».
4. Конструктор `DoctorStats` не рахує статистику сам — лише зберігає готові значення. Підрахунок буде в `AnalyticsManager` (Задача 4).
5. Перевірити сортування можна тимчасовим кодом у `Program.cs`, як у прикладі; перед комітом його приберіть.

📖 Документація:
- [`IComparable<T>`](https://learn.microsoft.com/dotnet/api/system.icomparable-1)
- [`Array.Sort`](https://learn.microsoft.com/dotnet/api/system.array.sort)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `DoctorStats` | `StaffStats` | `WaiterStats` | `LecturerStats` | `ManagerStats` | `LibrarianStats` | `TrainerStats` |
| `AppointmentCount` | к-сть check-in | к-сть столів | к-сть курсів | к-сть оренд | к-сть видач | к-сть сесій |
| `TotalRevenue` | загальна виручка | загальна виручка | к-сть студентів | загальна виручка | к-сть повернень | загальна виручка |
| більше прийомів = вище | більше обслугованих = вище | більше столів = вище | більше курсів = вище | більше оренд = вище | більше видач = вище | більше сесій = вище |

### Коміт

```bash
git add ClinicApp/Models/DoctorStats.cs
git commit -m "Lab10 Task01"
```

---

## Задача 2. `PatientStats` і `IComparable<PatientStats>` ⭐⭐

### Умова

За аналогією з `DoctorStats` створіть статистичний об'єкт для пацієнта: скільки візитів, скільки витрачено, дата останнього візиту. Природний порядок — за кількістю візитів (найактивніший пацієнт — перший).

**Що реалізувати:**

1. Створити клас `PatientStats` у `ClinicApp/Models/PatientStats.cs` з властивостями зі специфікації.
2. Реалізувати `IComparable<PatientStats>`: більша кількість візитів — вища позиція.
3. Перевизначити `ToString()`: один рядок з усіма даними; якщо візитів не було, замість `01.01.0001` вивести `—`.

### Специфікація

| Властивість | Тип | Опис |
|-------------|-----|------|
| `PatientId` | `int` | ID пацієнта |
| `FullName` | `string` | Повне ім'я |
| `VisitCount` | `int` | Кількість візитів |
| `TotalSpent` | `decimal` | Сума `GetCost()` по всіх візитах |
| `LastVisitDate` | `DateTime` | Дата останнього візиту; `DateTime.MinValue`, якщо візитів не було |

### Приклад

```
[3] Максим Бойко | Візитів: 0 | Витрачено: 0.00 грн | Останній візит: —
```

### Підказки

1. Структура ідентична `DoctorStats` — той самий патерн, інші поля. Мета задачі — закріпити патерн на другому прикладі.
2. Порівняння з `DateTime.MinValue` у `ToString()` дає змогу показати «—» замість безглуздої дати.

📖 Документація:
- [`IComparable<T>`](https://learn.microsoft.com/dotnet/api/system.icomparable-1)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `PatientStats` | `GuestStats` | `CustomerStats` | `StudentStats` | `ClientStats` | `ReaderStats` | `MemberStats` |
| `VisitCount` | к-сть ночей | к-сть відвідин | к-сть курсів | к-сть оренд | к-сть видач | к-сть тренувань |
| `TotalSpent` | загальна сума | загальна сума | середній бал | загальна сума | штрафи сплачені | загальна сума |
| більше візитів = вище | більше ночей = вище | більше відвідин = вище | більше курсів = вище | більше оренд = вище | більше видач = вище | більше тренувань = вище |

### Коміт

```bash
git add ClinicApp/Models/PatientStats.cs
git commit -m "Lab10 Task02"
```

---

## Задача 3. Кілька критеріїв сортування через `IComparer<T>` ⭐⭐⭐

### Умова

`IComparable<T>` дає один фіксований порядок. Але аналітичному модулю потрібно кілька: лікарів можна ранжувати за навантаженням, за виручкою, за алфавітом. Для цього є `IComparer<T>` — окремий клас, що реалізує один критерій і передається в `List<T>.Sort(comparer)`.

**Що реалізувати:**

1. Створити папку `ClinicApp/Comparators/` (простір імен `ClinicApp.Comparators`).
2. Створити в ній чотири компаратори зі специфікації.

### Специфікація

| Клас | Реалізує | Сортує за | Порядок |
|------|----------|-----------|---------|
| `DoctorStatsByRevenue` | `IComparer<DoctorStats>` | `TotalRevenue` | спадання (більша виручка вище) |
| `DoctorStatsByName` | `IComparer<DoctorStats>` | `FullName` | зростання (А → Я), `string.Compare(x, y, StringComparison.CurrentCulture)` |
| `PatientStatsBySpent` | `IComparer<PatientStats>` | `TotalSpent` | спадання |
| `PatientStatsByLastVisit` | `IComparer<PatientStats>` | `LastVisitDate` | спадання (найновіший візит вище) |

### Приклад

```csharp
List<DoctorStats> list = new List<DoctorStats> { a, b, c };
list.Sort();                              // за кількістю прийомів (IComparable)
list.Sort(new DoctorStatsByRevenue());    // за виручкою
list.Sort(new DoctorStatsByName());       // за ім'ям
```

### Підказки

1. `IComparer<T>` вимагає один метод: `int Compare(T? x, T? y)`. Та сама семантика, що й `CompareTo`: від'ємне — `x` перед `y`, нуль — рівні, додатне — `x` після `y`.
2. Обробляйте `null` явно: обидва `null` → `0`; лише `x == null` → `-1`; лише `y == null` → `1`. Тип параметрів nullable, тож компілятор попередить, якщо цього не зробити.
3. Щоб отримати спадний порядок, міняйте місцями `x` і `y` у порівнянні.
4. `DateTime` теж реалізує `IComparable` — дати порівнюються так само, як числа.
5. Перевірити компаратори можна тимчасовим кодом у `Program.cs`, як у прикладі; перед комітом його приберіть.

📖 Документація:
- [`IComparer<T>`](https://learn.microsoft.com/dotnet/api/system.collections.generic.icomparer-1)
- [`List<T>.Sort`](https://learn.microsoft.com/dotnet/api/system.collections.generic.list-1.sort)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `DoctorStatsByRevenue` | `StaffStatsByRevenue` | `WaiterStatsByRevenue` | `LecturerStatsByStudents` | `ManagerStatsByRevenue` | `LibrarianStatsByIssues` | `TrainerStatsByRevenue` |
| `DoctorStatsByName` | `StaffStatsByName` | `WaiterStatsByName` | `LecturerStatsByName` | `ManagerStatsByName` | `LibrarianStatsByName` | `TrainerStatsByName` |
| `PatientStatsBySpent` | `GuestStatsBySpent` | `CustomerStatsBySpent` | `StudentStatsByGrade` | `ClientStatsBySpent` | `ReaderStatsByIssues` | `MemberStatsBySpent` |
| `PatientStatsByLastVisit` | `GuestStatsByLastStay` | `CustomerStatsByLastVisit` | `StudentStatsByLastCourse` | `ClientStatsByLastRental` | `ReaderStatsByLastLoan` | `MemberStatsByLastSession` |

### Коміт

```bash
git add ClinicApp/Comparators/
git commit -m "Lab10 Task03"
```

---

## Задача 4. `AnalyticsManager` і ліниве обчислення через `yield return` ⭐⭐⭐

### Умова

Статистику можна обчислити методом, що будує весь масив `DoctorStats[]` одразу. Кращий підхід — `IEnumerable<T>` з `yield return`: метод обчислює статистику для кожного лікаря по черзі і **одразу віддає** результат, не накопичуючи весь масив. Коли лікарів тисячі, можна зупинитись після першого десятка — решта не обчислюватиметься взагалі.

**Що реалізувати:**

1. Створити клас `AnalyticsManager` у `ClinicApp/Managers/AnalyticsManager.cs`, який отримує `AppointmentManager`, `DoctorManager` і `PatientManager` через конструктор.
2. Метод `ComputeDoctorStats()`: для кожного лікаря порахувати кількість його прийомів, суму `GetCost()` і найпізнішу дату — і віддати `DoctorStats` через `yield return`.
3. Метод `ComputePatientStats()` — те саме для пацієнтів.
4. У `Clinic.cs` додати властивість `Analytics` і створити `AnalyticsManager` у конструкторі.

### Специфікація

| Член `AnalyticsManager` | Повертає | Опис |
|-------------------------|----------|------|
| конструктор `(AppointmentManager appointments, DoctorManager doctors, PatientManager patients)` | | зберігає залежності |
| `ComputeDoctorStats()` | `IEnumerable<DoctorStats>` | по одному `DoctorStats` на кожного лікаря, через `yield return` |
| `ComputePatientStats()` | `IEnumerable<PatientStats>` | по одному `PatientStats` на кожного пацієнта, через `yield return` |

Для лікаря чи пацієнта без прийомів: кількість `0`, сума `0`, дата `DateTime.MinValue`.

### Приклад

```csharp
foreach (DoctorStats s in clinic.Analytics.ComputeDoctorStats())
    Console.WriteLine(s);
// [1] Олег Сидоренко | Прийомів: 2 | Виручка: 600.00 грн | Останній: 15.10.2026
// [2] Наталія Мороз  | Прийомів: 0 | Виручка: 0.00 грн | Останній: —
```

### Підказки

1. Отримайте всіх лікарів через `_doctors.GetAll()` і всі прийоми через `_appointments.GetAll()`; для кожного лікаря — цикл по прийомах з умовою на `DoctorId`.
2. `yield return` у методі з типом `IEnumerable<T>` перетворює метод на **ітератор**. Після кожного `yield return` виконання «призупиняється» і відновлюється, коли запитують наступний елемент.
3. Щоб побачити лінивість: тимчасово виведіть рядок «обчислюю …» перед `yield return`. При `foreach` рядки з'являтимуться по одному під час ітерації, а не всі на початку.
4. Найпізніша дата: почніть з `DateTime.MinValue` і оновлюйте, коли дата прийому пізніша.

📖 Документація:
- [`yield`](https://learn.microsoft.com/dotnet/csharp/language-reference/statements/yield)
- [`IEnumerable<T>`](https://learn.microsoft.com/dotnet/api/system.collections.generic.ienumerable-1)
- [Ітератори](https://learn.microsoft.com/dotnet/csharp/iterators)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `ComputeDoctorStats()` | `ComputeStaffStats()` | `ComputeWaiterStats()` | `ComputeLecturerStats()` | `ComputeManagerStats()` | `ComputeLibrarianStats()` | `ComputeTrainerStats()` |
| `ComputePatientStats()` | `ComputeGuestStats()` | `ComputeCustomerStats()` | `ComputeStudentStats()` | `ComputeClientStats()` | `ComputeReaderStats()` | `ComputeMemberStats()` |

### Коміт

```bash
git add ClinicApp/Managers/AnalyticsManager.cs ClinicApp/Clinic.cs
git commit -m "Lab10 Task04"
```

---

## Задача 5. Меню «Аналітика» ⭐⭐⭐

### Умова

`DoctorStats`, `PatientStats`, компаратори і `AnalyticsManager` готові. Підключіть їх до меню: новий пункт головного меню `8` — «Аналітика» з п'ятьма звітами.

**Що реалізувати:**

1. У головному меню додати пункт `8` — «Аналітика».
2. У `Program.cs` додати функцію `AnalyticsMenu(Clinic clinic)` з п'ятьма звітами зі специфікації.
3. Додати дві допоміжні функції: `CollectDoctorStats(Clinic clinic)` і `CollectPatientStats(Clinic clinic)` — збирають результат ітератора в `List<...>` через `foreach`.

### Специфікація

| Пункт | Звіт | Як сортувати |
|-------|------|--------------|
| `1` | Лікарі за навантаженням | `Sort()` без аргументу (`IComparable`) |
| `2` | Лікарі за виручкою | `Sort(new DoctorStatsByRevenue())` |
| `3` | Лікарі за іменем | `Sort(new DoctorStatsByName())` |
| `4` | Пацієнти за кількістю візитів | `Sort()` без аргументу (`IComparable`) |
| `5` | Пацієнти за витратами | `Sort(new PatientStatsBySpent())` |
| `0` | Назад | |

### Приклад

```
── Аналітика ───────────────────
  1. Лікарі за навантаженням
  2. Лікарі за виручкою
  3. Лікарі за іменем
  4. Пацієнти за кількістю візитів
  5. Пацієнти за витратами
  0. Назад
Оберіть: 2
[2] Наталія Мороз  | Прийомів: 1 | Виручка: 780.00 грн | Останній: 16.10.2026
[1] Олег Сидоренко | Прийомів: 2 | Виручка: 600.00 грн | Останній: 15.10.2026
```

### Підказки

1. `clinic.Analytics.ComputeDoctorStats()` повертає ітератор, а не список. Щоб сортувати, потрібен `List<DoctorStats>` — збирайте через `foreach` і `.Add()`.
2. Одну й ту саму `CollectDoctorStats()` можна викликати для кожного пункту меню — ітератор щоразу починає обчислення заново.
3. `.Sort()` без аргументу вимагає, щоб тип реалізовував `IComparable<T>`. `.Sort(comparer)` використовує переданий компаратор.
4. Не забудьте `using ClinicApp.Comparators;` на початку `Program.cs`.

📖 Документація:
- [`List<T>.Sort`](https://learn.microsoft.com/dotnet/api/system.collections.generic.list-1.sort)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| Лікарі за навантаженням | Персонал за check-in | Офіціанти за столами | Викладачі за курсами | Менеджери за орендами | Бібліотекарі за видачами | Тренери за сесіями |
| Лікарі за виручкою | Персонал за виручкою | Офіціанти за виручкою | Викладачі за студентами | Менеджери за виручкою | Бібліотекарі за відділами | Тренери за виручкою |
| Пацієнти за кількістю візитів | Гості за ночами | Клієнти за відвідинами | Студенти за курсами | Клієнти за орендами | Читачі за видачами | Учасники за тренуваннями |
| Пацієнти за витратами | Гості за витратами | Клієнти за витратами | Студенти за балом | Клієнти за витратами | Читачі за штрафами | Учасники за витратами |

### Коміт

```bash
git add ClinicApp/Program.cs
git commit -m "Lab10 Task05"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                              ← гілка Lab-10 (після злиття — main)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs                       ✏ Т5
    ├── Clinic.cs                        ✏ Т4
    ├── Enums/  (3 файли)
    ├── Models/
    │   ├── DoctorStats.cs               🆕 Т1
    │   ├── PatientStats.cs              🆕 Т2
    │   └── … ще 12 файлів без змін
    ├── Managers/
    │   ├── AnalyticsManager.cs          🆕 Т4
    │   └── … ще 7 файлів без змін
    ├── Utils/  (2 файли)
    ├── Interfaces/  (4 файли)
    └── Comparators/
        ├── DoctorStatsByName.cs         🆕 Т3
        ├── DoctorStatsByRevenue.cs      🆕 Т3
        ├── PatientStatsByLastVisit.cs   🆕 Т3
        └── PatientStatsBySpent.cs       🆕 Т3
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 09.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] `8. Аналітика` з'явилась у головному меню
- [ ] «Лікарі за навантаженням» і «Лікарі за виручкою» дають **різний** порядок (якщо тестові дані різноманітні)
- [ ] «Лікарі за іменем» дає алфавітний порядок
- [ ] Пацієнт без записів показує `Візитів: 0` і дату `—`
- [ ] *(Експеримент, не для коміту)* якщо прибрати `IComparable` з `DoctorStats`, проєкт збирається, але `.Sort()` без аргументу кидає `InvalidOperationException` під час виконання

---

## Питання для самоперевірки

1. Чим `IComparable<T>` відрізняється від `IComparer<T>`? Коли використовувати перше, коли друге?
2. Що повертає `CompareTo` при рівних значеннях? Що станеться, якщо завжди повертати `0`?
3. Чому `yield return` у `ComputeDoctorStats()` дає «ліниве» обчислення? Коли саме виконується тіло циклу?
4. Як отримати з `IEnumerable<T>` лише перші N елементів без LINQ? (підказка: `foreach` + лічильник)
5. Що станеться, якщо викликати `.Sort()` на `List<DoctorStats>` після того, як прибрати `IComparable<DoctorStats>` з класу? Чому це помилка часу виконання, а не компіляції?
6. Порівняйте: `ComputeDoctorStats()` з `yield return` і метод, що будує й повертає `DoctorStats[]`. В чому різниця у поведінці при великій кількості лікарів?

---

## Статус гілки

Після всіх 5 завдань (кожне — окремий коміт `Lab10 TaskNN` на гілці `Lab-10`):

```bash
git push -u origin Lab-10
git checkout main
git merge --no-ff Lab-10 -m "Merge Lab-10: Iterators & Comparators"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-11`.
