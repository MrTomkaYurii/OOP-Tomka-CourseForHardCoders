# Лаба 09 — Generics (Узагальнені типи)

## Мета

Навчитись використовувати `List<T>` замість масивів з ручним лічильником, і самостійно писати generic класи з параметром типу `<T>`. Побачити, як один клас може працювати з різними типами без дублювання коду.

## Контекст

Після восьми лаб система працює, але з обмеженнями: `PatientManager` має фіксований масив `Patient[100]` і вручну керує лічильником. `Remove()` вимагає зсуву всіх елементів. Це ті самі «навмисні обмеження», що були в Лабі 03. Настав час замінити їх на `List<T>`.

Крім того, клініка потребує нову функціональність — **чергу очікування**: пацієнти приходять, стають у чергу і приймаються по порядку. Це окрема функція, яка природно виражається через `Queue<T>`.

### Структура проєкту на початку лаби

Це результат Лаби 08 — стан `main` після її злиття:

```text
oop-course/                             ← гілка main (після злиття Лаби 08)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/  (3 файли)
    ├── Models/
    │   ├── Patient.cs
    │   ├── Doctor.cs
    │   ├── Appointment.cs
    │   └── … ще 8 файлів без змін
    ├── Managers/
    │   ├── PatientManager.cs
    │   ├── DoctorManager.cs
    │   ├── AppointmentManager.cs
    │   ├── GrowablePatientManager.cs
    │   ├── MedicalRecordManager.cs
    │   └── BillingManager.cs
    ├── Utils/  (2 файли)
    └── Interfaces/
        ├── ICancellable.cs
        ├── IPayable.cs
        └── ISchedulable.cs
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Що нового дозволено (і тільки воно)

- `List<T>` і `Queue<T>` зі стандартної бібліотеки;
- власні generic класи з параметром типу `<T>`;
- обмеження параметра типу `where T : ...`;
- `default` для параметра типу.

Досі заборонено: LINQ (Лаба 14), делегати й лямбди (Лаби 13–15).

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-09
```

Коміт — на кожне завдання (`Lab09 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. `List<T>` замість масиву з лічильником ⭐

### Умова

`PatientManager` зберігає пацієнтів у `Patient[] _patients` з ручним `int _count`. Через це є штучне обмеження (`MaxPatients = 100`), `Remove()` потребує ручного зсуву елементів, а `GetAll()`, `FindByName()`, `FindByBloodType()` використовують двопрохідний патерн.

Замініть внутрішнє сховище на `List<Patient>`. Зовнішній API (`Add`, `FindById`, `DisplayAll`, `Remove` тощо) **не змінюється** — тільки внутрішня реалізація.

**Що реалізувати:**

1. Поле `_patients` змінити з `Patient[]` на `List<Patient>`; прибрати поле `_count` і константу `MaxPatients`.
2. `Count` — повертати кількість елементів списку.
3. `Add()` — додавати в список без перевірки ліміту.
4. `Remove()` — видаляти зі списку замість ручного зсуву.
5. `FindByName()`, `FindByBloodType()` — замість двопрохідного патерну наповнювати проміжний `List<Patient>` і в кінці повертати масив.
6. `GetAll()` — повертати масив однією операцією замість циклу.
7. Перевірити, що меню `1. Пацієнти` працює так само, як раніше, але без обмеження на 100 пацієнтів.

### Специфікація

| Член `PatientManager` | Було | Стало |
|-----------------------|------|-------|
| `_patients` | `Patient[]` + `_count` + `MaxPatients` | `List<Patient>` |
| `Count` | `_count` | кількість елементів списку |
| `Add` | перевірка ліміту, запис у масив | додавання в список |
| `Remove` | ручний зсув | видалення зі списку |
| `FindByName`, `FindByBloodType` | два проходи | проміжний список → масив |
| `GetAll` | цикл копіювання | одна операція |

Сигнатури публічних методів не змінюються.

### Підказки

1. `List<T>` — це динамічний масив зі стандартної бібліотеки. Розмір зростає автоматично при додаванні.
2. `.Add(item)` — додає в кінець. `.RemoveAt(index)` — видаляє за індексом і зсуває решту автоматично.
3. `.Count` — кількість елементів (аналог `_count`). `[i]` — доступ за індексом (як у масиві).
4. `.ToArray()` — повертає звичайний масив `T[]` з усіх елементів `List<T>`.
5. Конструктор без параметрів `new List<Patient>()` — порожній список.

📖 Документація:
- [`List<T>`](https://learn.microsoft.com/dotnet/api/system.collections.generic.list-1)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `PatientManager` | `GuestManager` | `CustomerManager` | `StudentManager` | `ClientManager` | `ReaderManager` | `MemberManager` |
| `Patient[]` → `List<Patient>` | `Guest[]` → `List<Guest>` | `Customer[]` → `List<Customer>` | `Student[]` → `List<Student>` | `Client[]` → `List<Client>` | `Reader[]` → `List<Reader>` | `Member[]` → `List<Member>` |
| `_count` → `_patients.Count` | `_count` → `_guests.Count` | `_count` → `_customers.Count` | `_count` → `_students.Count` | `_count` → `_clients.Count` | `_count` → `_readers.Count` | `_count` → `_members.Count` |

### Коміт

```bash
git add ClinicApp/Managers/PatientManager.cs
git commit -m "Lab09 Task01"
```

---

## Задача 2. Власний generic клас `WaitingQueue<T>` ⭐⭐

### Умова

Клініці потрібна черга очікування. Пацієнти приходять і стають у чергу (FIFO: перший прийшов — перший приймається). Це класична структура `Queue<T>`, але нам потрібна обгортка зі зрозумілим API і захистом від помилок.

**Що реалізувати:**

1. Створити generic клас `WaitingQueue<T>` у `ClinicApp/Models/WaitingQueue.cs` — обгортку над `Queue<T>`.
2. Додати члени зі специфікації нижче.
3. `Dequeue()` і `Peek()` на порожній черзі мають кидати `InvalidOperationException` зі зрозумілим повідомленням.

### Специфікація

| Член | Тип | Опис |
|------|-----|------|
| `Count` | `int` (лише читання) | Кількість у черзі |
| `IsEmpty` | `bool` | Чи порожня черга |
| `Enqueue(T item)` | `void` | Додати в кінець |
| `Dequeue()` | `T` | Прийняти першого (видаляє з черги); порожня — `InvalidOperationException` |
| `Peek()` | `T` | Подивитись, хто перший (не видаляє); порожня — `InvalidOperationException` |
| `ToArray()` | `T[]` | Поточний стан черги у вигляді масиву (для виводу) |

### Приклад

```csharp
WaitingQueue<string> q = new WaitingQueue<string>();
q.Enqueue("A"); q.Enqueue("B"); q.Enqueue("C");
Console.WriteLine(q.Count);      // 3
Console.WriteLine(q.Peek());     // A
Console.WriteLine(q.Dequeue());  // A
Console.WriteLine(q.Count);      // 2
```

`Dequeue()` на порожній черзі кидає `InvalidOperationException`.

### Підказки

1. Generic клас оголошується як `public class WaitingQueue<T>`. Використовуйте `T` скрізь, де раніше писали б конкретний тип.
2. `Queue<T>` — стандартна колекція FIFO. `Enqueue` — додати, `Dequeue` — взяти перший, `Peek` — подивитись на перший.
3. `Queue<T>` сама кидає `InvalidOperationException` при `Dequeue`/`Peek` на порожній черзі — але явна перевірка через `IsEmpty` дає зрозуміліше повідомлення.
4. Параметр `<T>` не накладає жодних обмежень — `WaitingQueue<Patient>`, `WaitingQueue<Doctor>`, `WaitingQueue<string>` — усе компілюється.
5. Перевірити клас можна тимчасовим кодом у `Program.cs`, як у прикладі вище; перед комітом його приберіть.

📖 Документація:
- [`Queue<T>`](https://learn.microsoft.com/dotnet/api/system.collections.generic.queue-1)
- [Generic класи](https://learn.microsoft.com/dotnet/csharp/programming-guide/generics/generic-classes)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `WaitingQueue<Patient>` | `WaitingQueue<Guest>` | `WaitingQueue<Customer>` | `WaitingQueue<Student>` | `WaitingQueue<Client>` | `WaitingQueue<Reader>` | `WaitingQueue<Member>` |
| черга на прийом | черга на заїзд | черга на столик | черга на зарахування | черга на авто | черга на книгу | черга до тренера |

### Коміт

```bash
git add ClinicApp/Models/WaitingQueue.cs
git commit -m "Lab09 Task02"
```

---

## Задача 3. Черга в системі: нове меню ⭐⭐⭐

### Умова

`WaitingQueue<T>` готова — тепер підключіть її до клініки: додайте чергу пацієнтів у `Clinic` і новий пункт головного меню «Черга».

**Що реалізувати:**

1. У `Clinic.cs` додати властивість `WaitingRoom` типу `WaitingQueue<Patient>` і створити чергу в конструкторі.
2. У головному меню додати пункт `6` — «Черга — очікування, прийом»; «Звіт» переїжджає на `7`.
3. У `Program.cs` додати функцію `WaitingRoomMenu(Clinic clinic)` з чотирма діями (див. специфікацію).
4. Дії «Прийняти першого» і «Хто перший?» обгорнути в `try/catch` на `InvalidOperationException` — на порожній черзі показати повідомлення, а не падати.

### Специфікація

| Пункт | Дія | Що виводить |
|-------|-----|-------------|
| `1` — Додати пацієнта до черги | запитує ID, знаходить пацієнта, ставить у чергу | підтвердження або «Пацієнта не знайдено» |
| `2` — Прийняти першого | `Dequeue` | ім'я прийнятого і скільки лишилось у черзі |
| `3` — Хто перший? | `Peek` | ім'я першого, без видалення |
| `4` — Переглянути всю чергу | `ToArray` | список із нумерацією |
| `0` — Назад | | |

### Приклад

```
── Черга ───────────────────────
  1. Додати пацієнта до черги
  2. Прийняти першого
  3. Хто перший?
  4. Переглянути всю чергу
  0. Назад
Оберіть: 2
Прийнято: Іван Петренко. У черзі лишилось: 1
```

### Підказки

1. `WaitingRoom` зберігає об'єкти `Patient` — тому можна одразу виводити `patient.FullName`.
2. `clinic.WaitingRoom.ToArray()` — отримати масив для виводу переліку черги.
3. `Queue<T>` гарантує порядок FIFO — порядок у `ToArray()` відповідає порядку додавання.

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `Clinic.WaitingRoom` | `Hotel.CheckInQueue` | `Restaurant.DiningQueue` | `University.EnrollmentQueue` | `CarRental.RentalQueue` | `Library.BorrowQueue` | `GymCenter.TrainingQueue` |
| `6. Черга — очікування, прийом` | `6. Черга — реєстрація` | `6. Черга — на столик` | `6. Черга — зарахування` | `6. Черга — на авто` | `6. Черга — на книгу` | `6. Черга — до тренера` |

### Коміт

```bash
git add ClinicApp/Clinic.cs ClinicApp/Program.cs
git commit -m "Lab09 Task03"
```

---

## Задача 4. `Repository<T>`: generic CRUD з обмеженням типу ⭐⭐⭐⭐

### Умова

`WaitingQueue<T>` не має обмежень — до неї можна додати будь-який тип. Іноді generic клас повинен **гарантувати**, що `T` має певні властивості. Наприклад, `Repository<T>` потрібен метод `GetById(int id)` — але для цього він повинен знати, що у `T` є властивість `Id`. Рішення — **обмеження** `where T : IIdentifiable`.

**Що реалізувати:**

1. Створити інтерфейс `IIdentifiable` у `ClinicApp/Interfaces/` з властивістю `int Id { get; }`.
2. Додати `: IIdentifiable` до оголошення `Patient`, `Doctor` і `Appointment` (властивість `Id` у них уже є).
3. Створити generic клас `Repository<T> where T : IIdentifiable` у `ClinicApp/Managers/Repository.cs` з методами зі специфікації. Усередині — `List<T>`.

### Специфікація

| Член `Repository<T>` | Опис |
|----------------------|------|
| `Add(T item)` | Додати |
| `GetById(int id)` | Знайти за `Id`; якщо немає — `default` |
| `GetAll()` | Усі елементи як `T[]` |
| `Remove(int id)` | Видалити за `Id`; `bool` — чи було що видаляти |
| `Count` | Кількість |

### Приклад

```csharp
Repository<Patient> repo = new Repository<Patient>();
repo.Add(p1);
repo.Add(p2);
Console.WriteLine(repo.GetById(p2.Id)?.FullName);  // ім'я p2
Console.WriteLine(repo.Remove(p1.Id));             // True
Console.WriteLine(repo.Count);                     // 1
```

### Підказки

1. `where T : IIdentifiable` — компілятор дозволяє звертатись до `item.Id` всередині класу, бо гарантовано, що у `T` є цей член.
2. `default!` — повертає `null` для reference-типів і підходить як «не знайдено», аналогічно до `null!` в існуючому коді.
3. `Repository<T>` не замінює `PatientManager`. Це окремий generic інструмент: `PatientManager` містить специфічну логіку (пошук за ім'ям, статистика), якої `Repository` не знає.
4. Перевірити клас можна тимчасовим кодом у `Program.cs`, як у прикладі; перед комітом його приберіть.

📖 Документація:
- [Обмеження параметрів типу](https://learn.microsoft.com/dotnet/csharp/programming-guide/generics/constraints-on-type-parameters)
- [`default`](https://learn.microsoft.com/dotnet/csharp/language-reference/operators/default)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `Repository<Patient>` | `Repository<Guest>` | `Repository<Customer>` | `Repository<Student>` | `Repository<Client>` | `Repository<Reader>` | `Repository<Member>` |
| `Patient`, `Doctor`, `Appointment` : `IIdentifiable` | `Guest`, `Staff`, `Booking` | `Customer`, `Waiter`, `TableReservation` | `Student`, `Lecturer`, `Enrollment` | `Client`, `Manager`, `Rental` | `Reader`, `Librarian`, `BookLoan` | `Member`, `Trainer`, `Session` |

### Коміт

```bash
git add ClinicApp/Interfaces/IIdentifiable.cs ClinicApp/Managers/Repository.cs
git add ClinicApp/Models/Patient.cs ClinicApp/Models/Doctor.cs ClinicApp/Models/Appointment.cs
git commit -m "Lab09 Task04"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                             ← гілка Lab-09 (після злиття — main)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs                      ✏ Т3
    ├── Clinic.cs                       ✏ Т3
    ├── Enums/  (3 файли)
    ├── Models/
    │   ├── Patient.cs                  ✏ Т4
    │   ├── Doctor.cs                   ✏ Т4
    │   ├── Appointment.cs              ✏ Т4
    │   ├── WaitingQueue.cs             🆕 Т2
    │   └── … ще 8 файлів без змін
    ├── Managers/
    │   ├── PatientManager.cs           ✏ Т1
    │   ├── DoctorManager.cs
    │   ├── AppointmentManager.cs
    │   ├── GrowablePatientManager.cs
    │   ├── MedicalRecordManager.cs
    │   ├── BillingManager.cs
    │   └── Repository.cs               🆕 Т4
    ├── Utils/  (2 файли)
    └── Interfaces/
        ├── ICancellable.cs
        ├── IPayable.cs
        ├── ISchedulable.cs
        └── IIdentifiable.cs            🆕 Т4
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 08.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] `1. Пацієнти` — поведінка не змінилась, але немає ліміту на кількість
- [ ] `6. Черга` — новий пункт у головному меню, «Звіт» — на `7`
- [ ] Додати 3 пацієнтів у чергу → прийняти двох → у черзі 1
- [ ] «Прийняти» з порожньої черги → повідомлення про помилку, програма не падає
- [ ] *(Експеримент, не для коміту)* `Repository<Patient>` компілюється; `Repository<string>` — ні
- [ ] *(Експеримент, не для коміту)* `WaitingQueue<string>` і `WaitingQueue<int>` компілюються (без обмеження)

---

## Питання для самоперевірки

1. В чому різниця між `List<T>` і `T[]`? Коли перевага у масиву, коли у `List<T>`?
2. Що означає `<T>` в оголошенні класу? Хто вказує конкретний тип — і коли?
3. Навіщо `where T : IIdentifiable`? Що буде, якщо прибрати обмеження і звернутись до `item.Id`?
4. Чому `WaitingQueue<T>` не має обмеження, а `Repository<T>` має? В чому принципова різниця між ними?
5. FIFO чи LIFO: `Queue<T>` або `Stack<T>` — що підходить для черги очікування і чому?
6. `PatientManager` тепер використовує `List<Patient>`. Чи є сенс замінити весь `PatientManager` на `Repository<Patient>`? Що б втратилось?

---

## Статус гілки

Після всіх 4 завдань (кожне — окремий коміт `Lab09 TaskNN` на гілці `Lab-09`):

```bash
git push -u origin Lab-09
git checkout main
git merge --no-ff Lab-09 -m "Merge Lab-09: Generics"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-10`.
