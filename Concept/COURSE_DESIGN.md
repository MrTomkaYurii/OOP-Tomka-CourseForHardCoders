# Проєкт: OOP C# Курс — Медична Клініка (еталонний домен)

## Загальна ідея

Студент будує **одну живу систему** весь курс. Кожна лаба = гілка = нова функціональність.
Еталонний домен: **Медична Клініка**.
Інструкції для студентів пишуться в **абстрактному вигляді** (Сутність A, Операція, Користувач).
Студент підставляє свій домен (готель, ресторан, аптека тощо).

---

## Домени для студентів (Лаба 00)

| Варіант | Домен | Сутність A | Сутність B | Користувач | Операція |
|---------|-------|-----------|-----------|------------|---------|
| А | Клініка | Patient | Doctor | Receptionist | Appointment |
| Б | Готель | Room | Service | Guest | Booking |
| В | Університет | Course | Subject | Student | Enrollment |
| Г | Прокат авто | Car | Brand | Client | Rental |
| Д | Ресторан | Dish | Ingredient | Waiter | Order |
| Є | Аптека | Medicine | Supplier | Customer | Sale |
| Ж | Кінотеатр | Movie | Director | Viewer | Ticket |
| З | Бібліотека | Book | Author | Member | Loan |

---

## Структура репозиторію

```
project-root/
├── sandbox/
│   ├── intro/              ← Lab 01: базовий C#, без домену
│   │   ├── Task1.cs        (консоль, змінні, типи)
│   │   ├── Task2.cs        (умови, switch)
│   │   ├── Task3.cs        (цикли, математика)
│   │   └── Task4.cs        (методи, рефакторинг)
│   └── arrays/             ← Lab 02: масиви
│       ├── Task1.cs        (базові операції)
│       ├── Task2.cs        (пошук, сортування)
│       ├── Task3.cs        (складні алгоритми)
│       └── Task4.cs        (2D масиви або матриці)
├── src/
│   ├── Core/               ← з'являється на Lab 04
│   │   ├── Entities/       (BaseEntity, BaseAudit)
│   │   ├── Interfaces/     (IRepository, ISchedulable, IPayable)
│   │   └── Events/         (EventBus — Lab 12)
│   ├── Modules/
│   │   ├── Patients/       ← Lab 03
│   │   ├── Doctors/        ← Lab 06
│   │   ├── Appointments/   ← Lab 07-08
│   │   ├── Waiting/        ← Lab 09 (Generic queue)
│   │   ├── Validation/     ← Lab 11 (Reflection)
│   │   ├── Notifications/  ← Lab 12 (Events)
│   │   ├── Reports/        ← Lab 13-14 (LINQ + Functional)
│   │   ├── Storage/        ← Lab 15-16 (Files + JSON)
│   │   └── Database/       ← Lab 17-20 (EF Core)
│   └── ConsoleApp/
│       └── Program.cs      ← єдина точка входу, росте весь курс
├── labs/
│   ├── lab-00-choose-domain/
│   ├── lab-01-intro/
│   ├── lab-02-arrays/
│   └── ... (кожна лаба = папка з instructions.md)
└── docs/
    └── COURSE_DESIGN.md    ← цей файл
```

---

## Git стратегія

### Гілки
```
main                        ← завжди робочий стан
sandbox/intro               ← Lab 01 (НЕ зливається в main)
sandbox/arrays              ← Lab 02 (НЕ зливається в main)
feature/[lab-name]          ← нова функціональність
refactor/[name]             ← покращення архітектури
hotfix/[name]               ← виправлення багів
```

### Правила комітів
```
Lab01 Task1: Add basic console I/O and variables
Lab03 Task2: Add Patient class with constructor and properties
```

### Злиття в main
- ✅ Зливається: якщо в консолі з'являється нова команда або поведінка
- ⏳ Чекає: якщо зміна тільки внутрішня (рефакторинг, валідація)
- ⏳ → зливається разом з наступною лабою

---

## Таблиця лаб

| # | Гілка | Merge | Модуль | Що з'являється в консолі |
|---|-------|-------|--------|--------------------------|
| 00 | — | — | — | Вибір домену, setup |
| 01 | `sandbox/intro` | ❌ | — | Синтаксис C#, без проекту |
| 02 | `sandbox/arrays` | ❌ | — | Масиви доменних даних |
| 03 | `feature/catalog` | ✅ | Patients | Menu: список, додати, знайти |
| 04 | `feature/abstraction` | ✅ | Core | Нові типи в меню (лікарі за спеціальністю) |
| 05 | `feature/encapsulation` | ⏳ | Patients+ | Внутрішня валідація |
| 06 | `feature/inheritance` | ✅ | Doctors | Меню: реєстрація з типом (загальний/спеціаліст) |
| 07 | `feature/interfaces` | ✅ | Appointments | Меню: записатись, скасувати, переглянути |
| 08 | `feature/polymorphism` | ⏳ | Appointments+ | Внутрішнє покращення |
| 09 | `feature/generics` | ✅ | Waiting | Меню: черга очікування |
| 10 | `feature/iterators` | ✅ | всі | Меню: сортування списків (foreach, comparators) |
| 11 | `feature/reflection` | ⏳ | Validation | Авто-валідатор через рефлексію |
| 12 | `feature/events` | ✅ | Notifications | Меню: сповіщення про прийом |
| 13 | `feature/linq` | ✅ | Reports | Меню: звіти (топ лікарі, активні пацієнти) |
| 14 | `feature/functional` | ⏳ | Reports+ | Внутрішнє покращення (чисті функції) |
| 15 | `feature/storage` | ✅ | Storage | Меню: зберегти/завантажити стан |
| 16 | `feature/console-ui` | ✅ | ConsoleApp | Структуроване меню, розділи, навігація |
| 17 | `feature/ef-basic` | ✅ | Database | БД замінила in-memory дані |
| 18 | `feature/ef-relations` | ✅ | Database+ | Зв'язані запити в меню |
| 19 | `feature/ef-advanced` | ✅ | Database+ | Складні зв'язки many-to-many |
| 20 | `feature/ef-querying` | ✅ | Database+ | Фільтрація, пагінація через IQueryable |
| 21 | `refactor/solid` | ✅ | всі | Зовні нічого, внутрішньо — SOLID рефакторинг |

---

## Деталі кожної лаби

### Lab 01 — sandbox/intro (C# Basics)
**Джерело:** Old Lab 01 (Introduction)
**Гілка:** `sandbox/intro` → НЕ зливається
**Що робить студент:** окремий проект поза src/, процедурний код
**Завдання клініки:**
- Task1: Змінні та типи. Вивести інформацію про пацієнта (ім'я string, вік int, вага double, кров'яний тиск double). Базові Console.Write/ReadLine.
- Task2: Умови. Розрахунок ІМТ (BMI). Визначити категорію (if/switch): недостатня вага/норма/зайва вага/ожиріння.
- Task3: Цикли. Розрахувати суму коштів за N візитів. Знайти найдорожчий та найдешевший прийом у масиві.
- Task4: Методи. Винести логіку Task2-3 у методи. GetBMICategory(double bmi), FormatAppointmentCost(decimal cost). Це буде основою для класів у Lab 03.

### Lab 02 — sandbox/arrays (Arrays)
**Джерело:** Old Lab 02 (Arrays)
**Гілка:** `sandbox/arrays` → НЕ зливається
**Що робить студент:** масиви рядків і чисел домену
**Завдання клініки:**
- Task1: Масив імен пацієнтів. FindByName(), CountByBloodType(), PrintAll().
- Task2: Масив візитів (дати як рядки). SortByDate(), FindOverdue(), CountByDoctor().
- Task3: Решето Ератосфена → аналог: знайти лікарів без записів (алгоритм маркування).
- Task4: 2D масив розкладу. Рядки = лікарі, стовпці = часові слоти. Знайти вільний слот.

### Lab 03 — feature/catalog (Defining Classes)
**Джерело:** Old Lab 03 (Defining Classes)
**Гілка:** `feature/catalog` → ✅ зливається
**Що з'являється:** Меню з 4 пунктами: показати всіх пацієнтів, додати, знайти за ім'ям, вийти
**Завдання клініки:**
- Task1: Клас Patient (Id, Name, Age, BloodType string, Phone). Конструктори. ToString(). Список пацієнтів в пам'яті.
- Task2: Клас Doctor (Id, Name, Speciality, Phone, WorkingHours). Список лікарів. Знайти лікаря за спеціальністю.
- Task3 (проблема): "Клініка хоче зберігати не тільки пацієнтів, але і записи на прийом. Як зв'язати пацієнта з лікарем і датою так, щоб можна було переглянути всі записи лікаря або всі записи пацієнта?" → Клас Appointment (PatientId, DoctorId, DateTime, Status).
- Task4 (відкрите): "Список пацієнтів росте. Як знайти пацієнта швидко? Що якщо є 1000 пацієнтів?" → Студент досліджує Dictionary vs List.

### Lab 04 — feature/abstraction (Abstraction)
**Джерело:** Old Lab 04 (Abstraction)
**Гілка:** `feature/abstraction` → ✅ зливається
**Що з'являється:** В меню нові типи лікарів, можна фільтрувати за спеціальністю
**Завдання клініки:**
- Task1: Enum Speciality (General, Cardiology, Neurology, Pediatrics). Enum BloodType (A, B, AB, O). Клас PriceCalculator з enum VisitType (Regular, Urgent, Specialist) та DiscountType.
- Task2: Abstract клас MedicalEntity (Id, Name, CreatedAt). Patient і Doctor успадковують від нього.
- Task3 (проблема): "Клініка хоче приймати різні типи пацієнтів: застраховані і незастраховані. Розрахунок вартості відрізняється. Як зробити так, щоб система рахувала вартість автоматично без if?" → Abstract метод CalculateCost().
- Task4: "Що якщо в клініці є не тільки прийоми, але і процедури, операції? Як структурувати це без дублювання?" → Студент відкриває ієрархію класів.

### Lab 05 — feature/encapsulation (Encapsulation)
**Джерело:** Old Lab 05 (Encapsulation)
**Гілка:** `feature/encapsulation` → ⏳ зливається з Lab 06
**Завдання клініки:**
- Task1: Зробити всі поля Patient приватними. Додати валідацію в сеттери: Name не пустий, Age в [0..150], Phone формат. Exceptions з повідомленнями.
- Task2: Валідація Doctor. Speciality тільки з enum. WorkingHours в [6..12].
- Task3 (проблема): "Призначення (Appointment) має статус. Хтось може змінити статус на будь-який. Як захистити так, щоб переходи були лише дозволені: Scheduled→Completed або Scheduled→Cancelled?" → State machine через приватний сеттер + метод.
- Task4: "Як гарантувати що у кожного Patient є унікальний Id, і ніхто не може його змінити зовні?" → readonly, фабричний метод.

### Lab 06 — feature/inheritance (Inheritance)
**Джерело:** Old Lab 06 (Inheritance)
**Гілка:** `feature/inheritance` → ✅ зливається
**Що з'являється:** Меню: реєстрація пацієнта з типом (загальний/VIP), реєстрація лікаря з спеціальністю
**Завдання клініки:**
- Task1: InsuredPatient : Patient, PrivatePatient : Patient. Різна логіка CalculateCost(). Override ToString().
- Task2: GeneralPractitioner : Doctor, Specialist : Doctor (з полем Speciality). Specialist може бути тільки Cardiology/Neurology/etc.
- Task3 (проблема): "Клініка додала VIP-відділення. VIP пацієнт має всі права звичайного + пріоритетну чергу + знижку. Як зробити без копіювання коду InsuredPatient?" → Ланцюжок успадкування або композиція.
- Task4: "Студент бачить дублювання ToString() у всіх підкласах. Як уникнути?" → Студент відкриває шаблонний метод (Template Method pattern).

### Lab 07 — feature/interfaces (Interfaces & Abstraction)
**Джерело:** Old Lab 07 (Interfaces)
**Гілка:** `feature/interfaces` → ✅ зливається
**Що з'являється:** Меню: записатись на прийом, скасувати, переглянути мої записи
**Завдання клініки:**
- Task1: ISchedulable (CanSchedule(), GetAvailableSlots()). IPayable (CalculateCost(), Pay()). Реалізувати в Appointment.
- Task2: ICancellable (Cancel(), CancellationReason). INotifiable (Notify(string message)). Реалізувати.
- Task3 (проблема): "Деякі операції потрібні скрізь: і для пацієнтів, і для лікарів, і для прийомів. Як уникнути дублювання коду для загальних операцій (наприклад, пошук за Id)?" → Студент відкриває generic interface IRepository<T>.
- Task4: "Що якщо завтра додається нова сутність — медична карта? Чи треба змінювати IRepository?" → Студент перевіряє open/closed principle.

### Lab 08 — feature/polymorphism (Polymorphism)
**Джерело:** Old Lab 08 (Polymorphism)
**Гілка:** `feature/polymorphism` → ⏳ зливається з Lab 09
**Завдання клініки:**
- Task1: Різні типи прийомів: RegularAppointment, UrgentAppointment, SpecialistAppointment — всі успадковують від Appointment. Override методу CalculateCost() і GetDescription().
- Task2: Список Appointment (поліморфний). foreach — кожен виводить свій опис і вартість.
- Task3 (проблема): "VIP клієнти мають різні правила для кожного типу прийому. Тобто VIPPatient + UrgentAppointment = 50% знижка. Як передати «правило» у розрахунок без if?" → Студент відкриває Strategy pattern.
- Task4: "Що станеться якщо додати новий тип прийому? Скільки місць треба змінити?" → Студент аналізує і знаходить Open/Closed проблему.

### Lab 09 — feature/generics (Generics)
**Джерело:** Old Lab 09 (Generics)
**Гілка:** `feature/generics` → ✅ зливається
**Що з'являється:** Меню: черга очікування в клініці
**Завдання клініки:**
- Task1: Generic клас Repository<T> where T : MedicalEntity. Методи Add, GetById, GetAll, Remove.
- Task2: Generic клас WaitingQueue<T> (обгортка над Queue<T>). Enqueue, Dequeue, Peek, Count.
- Task3 (проблема): "Потрібна черга, де пріоритет залежить від терміновості. Urgent пацієнти мають йти першими. Як зробити без дублювання WaitingQueue?" → Generic з IComparer або Constraint: where T : IComparable<T>.
- Task4: "Repository<T> не може фільтрувати. GetAll() повертає все. Як додати Find(Predicate<T>)?" → Студент відкриває делегати/функції.

### Lab 10 — feature/iterators (Iterators & Comparators)
**Джерело:** Old Lab 10 (Iterators & Comparators)
**Гілка:** `feature/iterators` → ✅ зливається
**Що з'являється:** Меню: сортування списку пацієнтів, лікарів, прийомів за різними критеріями
**Завдання клініки:**
- Task1: IEnumerable<T> на PatientCollection. Реалізувати GetEnumerator() з yield return. Foreach по колекції.
- Task2: IComparable<Patient> (за ім'ям). IComparable<Appointment> (за датою).
- Task3: IComparer — PatientByAgeComparer, DoctorByRatingComparer. SortedSet<Doctor>.
- Task4 (проблема): "Список прийомів повинен автоматично залишатися відсортованим при додаванні нового. Але SortedSet не дозволяє дублікати. Як вирішити?" → Студент досліджує і знаходить SortedList або власну структуру.

### Lab 11 — feature/reflection (Reflection & Attributes)
**Джерело:** Old Lab 11 (Reflection & Attributes)
**Гілка:** `feature/reflection` → ⏳ зливається з Lab 12
**Завдання клініки:**
- Task1: Кастомний атрибут [Required], [MaxLength(n)], [Range(min, max)]. Застосувати до властивостей Patient і Doctor.
- Task2: Клас MedicalValidator. Метод Validate<T>(T entity) — через рефлексію знаходить всі властивості з атрибутами і перевіряє. Повертає список помилок.
- Task3 (проблема): "Валідатор треба підключити до Repository<T> щоб перевіряти перед Add(). Але Repository не знає про конкретні типи атрибутів. Як підключити?" → Validator через інтерфейс або делегат.
- Task4: "Вивести поля класу Patient через рефлексію у вигляді таблиці (назва — значення). Як зробити це для будь-якого об'єкта?" → Generic Display<T> метод.

### Lab 12 — feature/events (Events & Communication)
**Джерело:** Old Lab 12 (Communication & Events)
**Гілка:** `feature/events` → ✅ зливається
**Що з'являється:** Меню: налаштувати сповіщення. Автоматичні сповіщення при подіях (запис/скасування).
**Завдання клініки:**
- Task1: Event OnAppointmentScheduled в Appointment. EventArgs з інформацією. Підписатись (ConsoleNotifier) і вивести повідомлення.
- Task2: Event OnAppointmentCancelled. Multiple subscribers (ConsoleNotifier + Logger).
- Task3 (проблема): "Різні модулі хочуть знати про різні події. NotificationModule хоче знати про нові записи, ReportModule — про всі завершені. Як підключити без прямих залежностей між модулями?" → Студент відкриває EventBus/Mediator.
- Task4: "Що якщо сповіщень стає багато і консоль переповнена? Як зробити фільтрацію: кожен підписник отримує тільки ті події що йому потрібні?" → Предикати на підписку.

### Lab 13 — feature/linq (LINQ)
**Джерело:** Old Lab 13 (LINQ)
**Гілка:** `feature/linq` → ✅ зливається
**Що з'являється:** Меню: звіти — топ лікарі, завантаженість, статистика
**Завдання клініки:**
- Task1: LINQ запити на List<Patient>: фільтр за BloodType, вік від-до, є/немає запису.
- Task2: LINQ на Appointments: group by Doctor, OrderBy Date, Join Patient+Doctor.
- Task3: Агрегати: середній час очікування, найпопулярніша спеціальність, лікарі без пацієнтів цього місяця.
- Task4 (проблема): "Звіт займає довго бо перебирає всі записи. Як зробити щоб не завантажувати в пам'ять зайве?" → Студент відкриває IQueryable vs IEnumerable, lazy evaluation.

### Lab 14 — feature/functional (Functional Programming)
**Джерело:** Old Lab 14 (Functional Programming)
**Гілка:** `feature/functional` → ⏳ зливається з Lab 15
**Завдання клініки:**
- Task1: Action<Patient> для виводу інформації. Func<Appointment, decimal> для розрахунку вартості.
- Task2: Predicate<Patient> для фільтрів в Repository.Find(). Higher-order функція ApplyDiscount(Func<decimal, decimal> discountFn).
- Task3: Метод розширення ToClinicReport(this IEnumerable<Appointment>). Ланцюжок .Where().GroupBy().Select().
- Task4 (проблема): "Функції фільтрації часто комбінуються: пацієнти старше 60 І з серцевими хворобами І без страховки. Як скласти складний фільтр з простих без довгих if?" → Студент відкриває Predicate composition (AND, OR, NOT).

### Lab 15 — feature/storage (Streams & Files)
**Джерело:** Old Lab 15 (Streams, Files, Directories)
**Гілка:** `feature/storage` → ✅ зливається
**Що з'являється:** Меню: зберегти стан, завантажити при старті
**Завдання клініки:**
- Task1: Зберегти список пацієнтів у текстовий файл (StreamWriter). Завантажити (StreamReader). Формат CSV.
- Task2: Серіалізація/десеріалізація через System.Text.Json. Зберігати і завантажувати всі дані (пацієнти, лікарі, прийоми).
- Task3 (проблема): "При збереженні великих даних файл може бути пошкоджений якщо програма впаде. Як зробити безпечне збереження?" → Atomic write (спочатку в temp файл, потім переіменувати).
- Task4: "Треба зберігати логи дій (хто що зробив і коли). Лог не повинен видалятися при перезапуску." → Append mode, RotatingLog.

### Lab 16 — feature/console-ui (Advanced Console UI)
**Джерело:** Old Lab 16 PDFs (не зчитались — тема: розширений консольний інтерфейс)
**Гілка:** `feature/console-ui` → ✅ зливається
**Що з'являється:** Структуроване меню з розділами, кольори, форматовані таблиці
**Завдання клініки:**
- Task1: Розбити меню на секції: Patients / Doctors / Appointments / Reports. Навігація між секціями.
- Task2: Форматований вивід таблицею (Console, padding, borders). Кольорове виділення статусів.
- Task3: Пагінація при виводі великих списків (10 рядків на сторінку, ←→ для навігації).
- Task4 (проблема): "Меню стає великим. Кожен раз треба вписувати новий пункт в Program.cs. Як зробити щоб новий модуль реєстрував себе автоматично?" → Студент відкриває Command pattern або Plugin system.

### Lab 17 — feature/ef-basic (EF Code First)
**Джерело:** Old Lab 17 (EF Code First)
**Гілка:** `feature/ef-basic` → ✅ зливається
**Що з'являється:** Поведінка консолі та сама, але дані зберігаються в реальній БД
**Завдання клініки:**
- Task1: ClinicDbContext. Entities: Patient, Doctor, Appointment, Department. Migrations. DbContext замінює in-memory списки.
- Task2: Seed data. CRUD операції через EF замість файлів.
- Task3: Додати Doctor.Department зв'язок (один Department = багато Doctors). Нова міграція без втрати даних.
- Task4 (проблема): "Треба зберігати медичну картку пацієнта (MedicalRecord) — це великий текст. Чи варто зберігати в окремій таблиці? Як вплине на продуктивність?" → Студент досліджує table splitting та lazy loading.

### Lab 18 — feature/ef-relations (EF Entity Relations)
**Джерело:** Old Lab 18 (EF Entity Relations)
**Гілка:** `feature/ef-relations` → ✅ зливається
**Що з'являється:** Меню: перегляд прийомів лікаря, всіх пацієнтів відділення
**Завдання клініки:**
- Task1: One-to-Many: Department → Doctors, Doctor → Appointments, Patient → Appointments.
- Task2: Many-to-Many: Patient може мати багато Doctors (спостереження), Doctor — багато Patients. PatientDoctor junction table.
- Task3: Self-referencing: Doctor може мати "куратора" (старший лікар). Завантажити ієрархію.
- Task4 (проблема): "Appointment має і Patient, і Doctor, і Treatment. Як зробити щоб видалення Doctor не видаляло всі його Appointments? Cascade delete або soft delete?" → Студент налаштовує OnDelete behavior.

### Lab 19 — feature/ef-advanced (EF Advanced Relations)
**Джерело:** Old Lab 19 (EF Advanced Relations)
**Гілка:** `feature/ef-advanced` → ✅ зливається
**Завдання клініки:**
- Task1: Table-per-Hierarchy (TPH) для Patient: InsuredPatient, PrivatePatient в одній таблиці з Discriminator.
- Task2: Owned Entity: Address як value object всередині Patient.
- Task3: Concurrency token на Appointment (не дати двом лікарям взяти одного пацієнта одночасно).
- Task4 (проблема): "Потрібен audit log — хто і коли змінив запис. Як зробити це автоматично без коду в кожному репозиторії?" → Override SaveChanges() в DbContext.

### Lab 20 — feature/ef-querying (EF Advanced Querying)
**Джерело:** Old Lab 20 (EF Advanced Querying)
**Гілка:** `feature/ef-querying` → ✅ зливається
**Що з'являється:** Меню: складні звіти з фільтрами, пагінацією, сортуванням
**Завдання клініки:**
- Task1: IQueryable<T> фільтрація: пацієнти за BloodType, Appointments за DateRange + DoctorId.
- Task2: Projection: вивести тільки Name + NextAppointmentDate (не завантажувати весь об'єкт).
- Task3: Grouping + Aggregation: скільки прийомів на день, середня тривалість, завантаженість лікаря по днях тижня.
- Task4 (проблема): "Пагінація через Skip().Take() повільна на великих таблицях. Як зробити cursor-based pagination?" → Студент досліджує keyset pagination.

### Lab 21 — refactor/solid (SOLID Principles)
**Джерело:** Old Lab 21 (SOLID)
**Гілка:** `refactor/solid` → ✅ зливається
**Що з'являється:** Зовні нічого не змінилось. Внутрішньо — чиста архітектура.
**Завдання клініки:**
- Task1 (SRP): Виявити класи що роблять надто багато. Розділити AppointmentService на: SchedulingService, BillingService, NotificationService.
- Task2 (OCP/LSP): Перевірити ієрархію Doctor і Patient. Чи можна підставити будь-який підклас? Виправити порушення.
- Task3 (ISP): Великий інтерфейс IClinicService розбити на маленькі: IPatientService, IDoctorService, IAppointmentService.
- Task4 (DIP): CourseService залежить від конкретних класів. Ввести DI через конструктор. Налаштувати DI контейнер в Program.cs.

---

## Структура instructions.md (шаблон)

```markdown
# Лаба NN — [Назва теми]

## Мета
Одне речення: що студент навчиться робити.

## Контекст
Що вже є в системі. Яку нову проблему вирішує ця лаба.

## Гілка
git checkout main && git pull && git checkout -b feature/[назва]

## Завдання 1 — [назва] (обов'язкове) ⭐
[Конкретний опис. Без підказки рішення.]
**Коміт:** "LabNN Task1: [опис]"

## Завдання 2 — [назва] (обов'язкове) ⭐⭐
[Розширення Task1. Взаємодія з існуючим кодом.]
**Коміт:** "LabNN Task2: [опис]"

## Завдання 3 — [назва] (бажане) ⭐⭐⭐
[Формулюється як проблема! НЕ вказує рішення.]
**Коміт:** "LabNN Task3: [опис]"

## Завдання 4 — [назва] (бонус) ⭐⭐⭐⭐
[Відкрите питання. Студент знаходить підхід сам.]
**Коміт:** "LabNN Task4: [опис]"

## Злиття (якщо ✅)
git checkout main && git merge feature/[назва] && git push

## Що з'явиться в консолі
[Конкретний опис нової поведінки.]

## Питання для самоперевірки
- Питання 1
- Питання 2
- Питання 3
```

---

## Абстрактна термінологія для інструкцій

| Клініка | Загальний вигляд |
|---------|-----------------|
| Patient | Сутність A |
| Doctor | Сутність B |
| Receptionist | Користувач |
| Appointment | Операція |
| Department | Категорія |
| Treatment | Деталь операції |
| MedicalRecord | Документ |
| ClinicDbContext | DbContext / Контекст даних |

---

## Поточний стан

**Написано:** тільки цей файл дизайну.
**Наступний крок:** Lab 00 (вибір домену) → Lab 01 (sandbox/intro).
**Порядок роботи Claude Code:**
1. Написати еталонний код на C# (домен: Клініка)
2. Написати instructions.md в абстрактному вигляді
3. Перевірити Task 3-4 на складність
4. Зберегти файли в `labs/lab-NN-назва/`
