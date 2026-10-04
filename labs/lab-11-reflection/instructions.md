# Лаба 11 — Reflection & Attributes (Рефлексія та атрибути)

## Мета

Навчитись створювати власні атрибути через спадкування від `System.Attribute`, зчитувати метадані типів та властивостей через рефлексію і будувати узагальнені утиліти (валідатор, конструктор форм), що працюють з **будь-яким класом** без явного знання про його поля.

## Контекст

Після Лаби 10 система має повний аналітичний модуль. Ця лаба додає **плани лікування** (`TreatmentPlan`) як новий тип даних та інструментарій рефлексії, що перевіряє валідність об'єктів і генерує форми введення **автоматично** — зчитуючи атрибути з властивостей класу під час виконання.

### Структура проєкту на початку лаби

Це результат Лаби 10 — стан `main` після її злиття:

```text
oop-course/                           ← гілка main (після злиття Лаби 10)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs
    ├── Clinic.cs
    ├── Enums/
    │   ├── AppointmentStatus.cs
    │   ├── BloodType.cs
    │   └── Speciality.cs
    ├── Models/  (14 файлів)
    ├── Managers/  (8 файлів)
    ├── Utils/
    │   ├── ClinicFormatter.cs
    │   └── ClinicValidator.cs
    ├── Interfaces/  (4 файли)
    └── Comparators/  (4 файли)
```

Структуру **наприкінці** лаби (з позначками, що створюється і змінюється в кожній задачі) наведено в розділі «Структура проєкту наприкінці лаби» перед перевіркою.

### Що нового дозволено (і тільки воно)

- власні атрибути (`: Attribute`) і `[AttributeUsage]`;
- рефлексія: `GetType()`, `typeof(...)`, `PropertyInfo` (`GetProperties`, `GetValue`, `SetValue`, `GetCustomAttribute`);
- обмеження `where T : new()`;
- `Convert.ChangeType`.

Досі заборонено: LINQ (Лаба 14), делегати й лямбди (Лаби 13–15).

---

## Крок 1. Гілка

> **Робочий процес** (повністю — [Git Воркшоп](https://tomka.space/git-workshop/)):
> лаба = гілка `Lab-XX` від `main`, коміт на кожне завдання (`LabXX TaskYY`), у кінці — злиття в `main`.

Проєкт `ClinicApp/` уже існує. Тут лише нова гілка від `main`:

```bash
git checkout main
git checkout -b Lab-11
```

Коміт — на кожне завдання (`Lab11 TaskNN`).

### Ваш домен

За замовчуванням виконуйте завдання **як написано** (домен «клініка»). Для власного домену дивіться таблицю **«Адаптація до вашого домену»** в кінці кожного завдання.

### Як користуватися підказками

Підказки — **напрям думки, не готовий код**. «Що реалізувати» і «Специфікація» кажуть *що*; підказки — *як міркувати*; блок **📖 Документація** — де прочитати синтаксис. Спершу документація і власна спроба.

---

## Задача 1. Власні атрибути ⭐

### Умова

Правила валідації можна описати безпосередньо в класі — атрибутом над кожною властивістю. Замість готових атрибутів із `System.ComponentModel.DataAnnotations` напишіть власні **з нуля**.

**Що реалізувати:**

1. Створити теку `ClinicApp/Attributes/` (простір імен `ClinicApp.Attributes`).
2. Створити три атрибути зі специфікації. Кожен — `sealed` клас, що успадковує `Attribute`, і може стояти **лише на властивостях**, не більше одного разу.

### Специфікація

| Клас | Властивості (лише читання) | Конструктор |
|------|----------------------------|-------------|
| `RequiredAttribute` | `ErrorMessage` | `(string errorMessage = "Field is required.")` |
| `MaxLengthAttribute` | `Length`, `ErrorMessage` | `(int length, string errorMessage = "")` |
| `MinValueAttribute` | `Min` (`double`), `ErrorMessage` | `(double min, string errorMessage = "")` |

Над кожним класом: `[AttributeUsage(AttributeTargets.Property, AllowMultiple = false)]`.

### Приклад

```csharp
public class Sample
{
    [Required("Назва обов'язкова.")]
    [MaxLength(50, "Назва — не довше 50 символів.")]
    public string Title { get; set; } = "";

    [MinValue(1, "Кількість — щонайменше 1.")]
    public int Quantity { get; set; }
}
```

### Підказки

1. Атрибут — це клас, що успадковує `System.Attribute`. При застосуванні суфікс `Attribute` можна опускати: `[MaxLength(200)]` замість `[MaxLengthAttribute(200)]`.
2. `[AttributeUsage]` обмежує, де атрибут можна поставити. `AttributeTargets.Property` — тільки на властивостях.
3. `AllowMultiple = false` означає: один атрибут одного типу на одну властивість.
4. `sealed` — атрибут не підлягає подальшому спадкуванню (хороша практика).

📖 Документація:
- [Створення власних атрибутів](https://learn.microsoft.com/dotnet/csharp/advanced-topics/reflection-and-attributes/creating-custom-attributes)
- [`AttributeUsage`](https://learn.microsoft.com/dotnet/api/system.attributeusageattribute)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `MaxLength` на `Diagnosis` | `MaxLength` на `GuestNote` | `MaxLength` на `DishNote` | `MaxLength` на `CourseName` | `MaxLength` на `VehicleModel` | `MaxLength` на `BookTitle` | `MaxLength` на `ExercisePlan` |
| `MinValue` на `DurationDays` | `MinValue` на `StayNights` | `MinValue` на `GuestCount` | `MinValue` на `Credits` | `MinValue` на `RentalDays` | `MinValue` на `OverdueDays` | `MinValue` на `DurationMinutes` |

### Коміт

```bash
git add ClinicApp/Attributes/
git commit -m "Lab11 Task01"
```

---

## Задача 2. Модель `TreatmentPlan` з атрибутами ⭐⭐

### Умова

Додайте нову сутність — план лікування. Правила її полів опишіть атрибутами із Задачі 1, а стан плану змінюйте лише через методи.

**Що реалізувати:**

1. Створити `enum TreatmentStatus` у `ClinicApp/Enums/` зі значеннями `Planned`, `Active`, `Completed`, `Cancelled`.
2. Створити клас `TreatmentPlan` у `ClinicApp/Models/` з властивостями й атрибутами зі специфікації.
3. Додати конструктор без параметрів: присвоює `Id` з лічильника.
4. Додати методи переходу стану `Activate()`, `Complete()`, `Cancel()` — кожен повертає `bool` (чи відбувся перехід).

### Специфікація

| Властивість | Тип | Атрибути | Доступ |
|-------------|-----|----------|--------|
| `Id` | `int` | — | лише `get`, з лічильника |
| `PatientId` | `int` | `[MinValue(1, "Patient ID is required.")]` | `get; set;` |
| `Diagnosis` | `string` | `[Required("Diagnosis cannot be empty.")]`, `[MaxLength(200, "Diagnosis must not exceed 200 characters.")]` | `get; set;` |
| `DurationDays` | `int` | `[MinValue(1, "Duration must be at least 1 day.")]` | `get; set;` |
| `Status` | `TreatmentStatus` | — | `get; private set;`, початково `Planned` |

| Метод | Перехід | Інакше |
|-------|---------|--------|
| `Activate()` | `Planned` → `Active` | `false` |
| `Complete()` | `Active` → `Completed` | `false` |
| `Cancel()` | будь-який, крім `Completed` і `Cancelled` → `Cancelled` | `false` |

### Приклад

```csharp
TreatmentPlan plan = new TreatmentPlan { PatientId = 1, Diagnosis = "Гіпертонія", DurationDays = 30 };
Console.WriteLine(plan.Activate());  // True
Console.WriteLine(plan.Activate());  // False — уже Active
Console.WriteLine(plan.Complete());  // True
```

### Підказки

1. Атрибути — це лише метадані. Самі по собі вони нічого не перевіряють — перевірку виконає `ModelValidator` у Задачі 3.
2. На одну властивість можна поставити **кілька різних** атрибутів: `[Required]` і `[MaxLength(200)]` обидва будуть прочитані рефлексією.
3. `[Required]` має сенс для рядків і посилальних типів: у `int` не буває `null`, тому для числових ID використано `[MinValue(1)]`.
4. `private set` для `Status` — стан змінюється тільки через методи, що зберігає правила переходів.
5. Ініціалізатор `new TreatmentPlan { ... }` можливий, бо є конструктор без параметрів і публічні сеттери; він же знадобиться `FormBuilder` у Задачі 4.

📖 Документація:
- [Типи параметрів атрибутів](https://learn.microsoft.com/dotnet/csharp/advanced-topics/reflection-and-attributes/attribute-parameter-types)
- [Ініціалізатори об'єктів](https://learn.microsoft.com/dotnet/csharp/programming-guide/classes-and-structs/object-and-collection-initializers)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `TreatmentPlan` | `ServiceRequest` | `SpecialOrder` | `CourseProject` | `ServiceOrder` | `RestorationRequest` | `TrainingProgram` |
| `TreatmentStatus` | `ServiceStatus` | `OrderStatus` | `ProjectStatus` | `ServiceStatus` | `RestorationStatus` | `ProgramStatus` |
| `Activate/Complete/Cancel` | `Start/Finish/Cancel` | `Confirm/Serve/Cancel` | `Start/Submit/Withdraw` | `Start/Return/Cancel` | `Begin/Finish/Cancel` | `Begin/Complete/Cancel` |

### Коміт

```bash
git add ClinicApp/Enums/TreatmentStatus.cs ClinicApp/Models/TreatmentPlan.cs
git commit -m "Lab11 Task02"
```

---

## Задача 3. `ModelValidator` через рефлексію ⭐⭐⭐

### Умова

Напишіть статичний валідатор, що **автоматично** перевіряє будь-який об'єкт: читає атрибути з його властивостей через рефлексію. У коді валідатора не має бути жодної перевірки конкретного поля на кшталт `if (plan.Diagnosis == "")`.

**Що реалізувати:**

1. Клас `ValidationResult` у `ClinicApp/Utils/` — контейнер помилок (специфікація нижче).
2. Статичний клас `ModelValidator` у `ClinicApp/Utils/` з методом `Validate(object obj)`: для кожної властивості об'єкта перевірити `Required`, `MaxLength`, `MinValue` і зібрати помилки у `ValidationResult`.
3. Метод `ModelValidator.PrintInfo(Type type)`: вивести назву типу і список його властивостей з атрибутами.

### Специфікація

| Член `ValidationResult` | Опис |
|-------------------------|------|
| `IsValid` | `true`, якщо помилок немає |
| `Errors` | список помилок лише для читання (`IReadOnlyList<string>`) |
| `AddError(string error)` | додати помилку |
| `Print()` | вивести кожну помилку окремим рядком з позначкою `[!]` |

| Атрибут | Помилка, якщо… | Текст помилки |
|---------|----------------|---------------|
| `Required` | значення `null` або рядок з пробілів | `"Назва: ErrorMessage"` |
| `MaxLength` | рядок довший за `Length` | `"Назва: ErrorMessage"` |
| `MinValue` | число менше за `Min` | `"Назва: ErrorMessage"` |

### Приклад

```
ModelValidator.Validate(new TreatmentPlan()).Print();
  [!] PatientId: Patient ID is required.
  [!] Diagnosis: Diagnosis cannot be empty.
  [!] DurationDays: Duration must be at least 1 day.
```

### Підказки

1. `obj.GetType()` — тип конкретного об'єкта під час виконання. Відрізняється від `typeof(T)` — типу, відомого на час компіляції.
2. `type.GetProperties()` — масив `PropertyInfo[]`. Кожен `PropertyInfo` описує одну властивість: ім'я, тип, атрибути.
3. `prop.GetValue(obj)` — зчитує значення властивості з конкретного об'єкта; повертає `object?`.
4. `prop.GetCustomAttribute<RequiredAttribute>()` — шукає атрибут цього типу; якщо не знайдено — `null`.
5. Для `MinValue` значення треба перетворити на число: `Convert.ToDouble(value)`.
6. `prop.GetCustomAttributes()` — усі атрибути на властивості (для `PrintInfo`).

📖 Документація:
- [Рефлексія й атрибути](https://learn.microsoft.com/dotnet/csharp/advanced-topics/reflection-and-attributes/)
- [`PropertyInfo.GetValue`](https://learn.microsoft.com/dotnet/api/system.reflection.propertyinfo.getvalue)
- [`GetCustomAttribute`](https://learn.microsoft.com/dotnet/api/system.reflection.customattributeextensions.getcustomattribute)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| Валідує `TreatmentPlan` | Валідує `ServiceRequest` | Валідує `SpecialOrder` | Валідує `CourseProject` | Валідує `ServiceOrder` | Валідує `RestorationRequest` | Валідує `TrainingProgram` |

### Коміт

```bash
git add ClinicApp/Utils/ValidationResult.cs ClinicApp/Utils/ModelValidator.cs
git commit -m "Lab11 Task03"
```

---

## Задача 4. `TreatmentPlanManager` і `FormBuilder` ⭐⭐⭐

### Умова

Підключіть валідацію до менеджера планів і напишіть generic утиліту, що будує консольну форму введення автоматично — за атрибутами на властивостях.

**Що реалізувати:**

1. Клас `TreatmentPlanManager` у `ClinicApp/Managers/`: зберігає плани в `List<TreatmentPlan>`; `Add` спершу перевіряє план через `ModelValidator` і не додає невалідний.
2. Статичний клас `FormBuilder` у `ClinicApp/Utils/` з методом `Build<T>() where T : new()`: створює об'єкт і для кожної властивості з **публічним** сеттером питає значення в консолі.

### Специфікація

| Член `TreatmentPlanManager` | Опис |
|-----------------------------|------|
| `Add(TreatmentPlan plan)` | Валідує; невалідний — виводить помилки, повертає `false`; інакше додає, `true` |
| `GetById(int id)` | `TreatmentPlan?` |
| `GetByPatient(int patientId)` | `TreatmentPlan[]` |
| `GetByStatus(TreatmentStatus status)` | `TreatmentPlan[]` |
| `GetAll()` | `TreatmentPlan[]` |

| `FormBuilder.Build<T>()` | |
|--------------------------|--|
| Які властивості питає | лише з публічним сеттером (`Id` і `Status` пропускаються) |
| Підказка до поля | з атрибутів: обов'язкове, максимальна довжина, мінімум |
| Некоректне введення | повідомлення і повторний запит цього ж поля |
| Результат | заповнений об'єкт `T` |

### Приклад

```
  PatientId (мін. 1): 1
  Diagnosis (обов'язкове, макс. 200): Гіпертонія
  DurationDays (мін. 1): abc
  Некоректне значення, спробуйте ще раз.
  DurationDays (мін. 1): 30
```

### Підказки

1. `where T : new()` — тип `T` повинен мати конструктор без параметрів. Без цього `new T()` не компілюється.
2. `typeof(T)` і `obj.GetType()` дають `Type`, але `typeof(T)` — статичний (час компіляції), `GetType()` — динамічний. У `FormBuilder` результат однаковий, бо `T` відомий.
3. **Пастка `CanWrite`.** `prop.CanWrite` повертає `true` і для **приватного** сеттера (як у `Status`). Публічний сеттер перевіряйте через `prop.GetSetMethod()` — для непублічного він повертає `null`.
4. `Convert.ChangeType(input, prop.PropertyType)` перетворює рядок у потрібний тип і кидає виняток, якщо не вийшло — обгорніть у `try/catch` і повторіть запит.
5. `prop.SetValue(obj, converted)` записує значення у властивість через рефлексію.
6. Перебирайте властивості звичайним циклом із перевіркою всередині — LINQ і лямбди в цій лабі ще заборонені.

📖 Документація:
- [`PropertyInfo.SetValue`](https://learn.microsoft.com/dotnet/api/system.reflection.propertyinfo.setvalue)
- [`PropertyInfo.GetSetMethod`](https://learn.microsoft.com/dotnet/api/system.reflection.propertyinfo.getsetmethod)
- [`Convert.ChangeType`](https://learn.microsoft.com/dotnet/api/system.convert.changetype)
- [Обмеження `new()`](https://learn.microsoft.com/dotnet/csharp/language-reference/constraints/new-constraint)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `TreatmentPlanManager` | `ServiceRequestManager` | `SpecialOrderManager` | `CourseProjectManager` | `ServiceOrderManager` | `RestorationManager` | `TrainingProgramManager` |
| `FormBuilder.Build<TreatmentPlan>()` | `FormBuilder.Build<ServiceRequest>()` | `FormBuilder.Build<SpecialOrder>()` | `FormBuilder.Build<CourseProject>()` | `FormBuilder.Build<ServiceOrder>()` | `FormBuilder.Build<RestorationRequest>()` | `FormBuilder.Build<TrainingProgram>()` |

### Коміт

```bash
git add ClinicApp/Managers/TreatmentPlanManager.cs ClinicApp/Utils/FormBuilder.cs
git commit -m "Lab11 Task04"
```

---

## Задача 5. Меню «Плани лікування» ⭐⭐

### Умова

Підключіть `TreatmentPlanManager` до клініки і додайте меню, що показує роботу рефлексії.

**Що реалізувати:**

1. У `Clinic.cs` додати властивість `TreatmentPlans` і створити `TreatmentPlanManager` у конструкторі.
2. У головному меню додати пункт `9` — «Плани лікування — рефлексія, атрибути».
3. У `Program.cs` додати підменю «Плани лікування» з пунктами зі специфікації.

### Специфікація

| Пункт | Дія |
|-------|-----|
| `1` — Показати всі плани | `GetAll()` |
| `2` — Додати план лікування | форма через `FormBuilder.Build<TreatmentPlan>()`, далі `Add` |
| `3` — Плани пацієнта | запитує ID пацієнта, `GetByPatient` |
| `4` — Активувати план | запитує ID плану, `Activate()` |
| `5` — Завершити план | запитує ID плану, `Complete()` |
| `6` — Скасувати план | запитує ID плану, `Cancel()` |
| `7` — Інформація про тип `TreatmentPlan` | `ModelValidator.PrintInfo(typeof(TreatmentPlan))` |
| `0` — Назад | |

Для пунктів 4–6: якщо плану немає — «План не знайдено»; якщо перехід неможливий — повідомлення про це.

### Приклад

```
── Плани лікування ────────────────────
  1. Показати всі плани
  2. Додати план лікування
  3. Плани пацієнта
  4. Активувати план
  5. Завершити план
  6. Скасувати план
  7. Інформація про тип TreatmentPlan
  0. Назад
Оберіть: 7
TreatmentPlan
  Id
  PatientId     [MinValue]
  Diagnosis     [Required] [MaxLength]
  DurationDays  [MinValue]
  Status
```

### Підказки

1. Пункт 7 отримує `Type`, а не об'єкт: рефлексія працює і без екземпляра.
2. Невалідний план із форми `Add` не прийме — у меню просто покажіть його помилки й поверніться в підменю.

📖 Документація:
- [Оператор `typeof`](https://learn.microsoft.com/dotnet/csharp/language-reference/operators/type-testing-and-cast#typeof-operator)

### Адаптація до вашого домену

| Клініка | Готель | Ресторан | Університет | Прокат авто | Бібліотека | Спортзал |
|---------|--------|----------|-------------|-------------|------------|---------|
| `9. Плани лікування` | `9. Запити на сервіс` | `9. Спецзамовлення` | `9. Курсові проєкти` | `9. Сервісні замовлення` | `9. Реставрація` | `9. Програми тренувань` |

### Коміт

```bash
git add ClinicApp/Clinic.cs ClinicApp/Program.cs
git commit -m "Lab11 Task05"
```

---

## Структура проєкту наприкінці лаби

Так має виглядати `ClinicApp/`, коли всі завдання виконано:

```text
oop-course/                           ← гілка Lab-11 (після злиття — main)
├── .gitignore
├── oop-course.slnx
└── ClinicApp/
    ├── ClinicApp.csproj
    ├── Program.cs                    ✏ Т5
    ├── Clinic.cs                     ✏ Т5
    ├── Enums/
    │   ├── AppointmentStatus.cs
    │   ├── BloodType.cs
    │   ├── Speciality.cs
    │   └── TreatmentStatus.cs        🆕 Т2
    ├── Models/
    │   ├── TreatmentPlan.cs          🆕 Т2
    │   └── … ще 14 файлів без змін
    ├── Managers/
    │   ├── TreatmentPlanManager.cs   🆕 Т4
    │   └── … ще 8 файлів без змін
    ├── Utils/
    │   ├── ClinicFormatter.cs
    │   ├── ClinicValidator.cs
    │   ├── FormBuilder.cs            🆕 Т4
    │   ├── ModelValidator.cs         🆕 Т3
    │   └── ValidationResult.cs       🆕 Т3
    ├── Interfaces/  (4 файли)
    ├── Comparators/  (4 файли)
    └── Attributes/
        ├── MaxLengthAttribute.cs     🆕 Т1
        ├── MinValueAttribute.cs      🆕 Т1
        └── RequiredAttribute.cs      🆕 Т1
```

**Легенда:** 🆕 — новий файл · ✏ — змінено вміст · Т*n* — номер задачі, у якій ви працюєте з файлом. Файли без позначки лишились такими, як були після Лаби 10.

Назви файлів наведено для домену «клініка»; у власному домені назви ваші — важливо, що саме створюється й змінюється.

---

## Перевірка перед здачею

```bash
dotnet build ClinicApp
dotnet run --project ClinicApp
```

Переконайтесь, що:

- [ ] Структура проєкту збігається зі схемою вище
- [ ] Три атрибути — власні класи, що успадковують `Attribute`, з `[AttributeUsage(AttributeTargets.Property ...)]`
- [ ] `ModelValidator.Validate(new TreatmentPlan())` повертає три помилки, а в коді валідатора немає звернень до полів `TreatmentPlan`
- [ ] Форма `FormBuilder.Build<TreatmentPlan>()` не питає `Id` і `Status`, підказки беруться з атрибутів
- [ ] Некоректне число у формі — повторний запит, програма не падає
- [ ] Пункт «Інформація про тип» виводить властивості й атрибути через `typeof(TreatmentPlan)`
- [ ] Спроба додати план без обов'язкових полів — повідомлення про помилки, план не додано
- [ ] У коді немає LINQ і лямбд

---

## Питання для самоперевірки

1. Чим відрізняється `obj.GetType()` від `typeof(T)`? Коли кожен з них корисний?
2. Що б змінилось у `FormBuilder` без `where T : new()`?
3. `ModelValidator.Validate()` приймає `object`, а не `TreatmentPlan`. Що це дає? Які ще об'єкти можна провалідувати без змін у коді валідатора?
4. Чому `[Required]` на `int` нічого не перевіряє? Як правильно позначити обов'язковий числовий ID?
5. Чому `CanWrite` недостатньо, щоб відрізнити публічний сеттер від приватного?
6. `Convert.ChangeType(input, prop.PropertyType)` кидає виняток, якщо `PropertyType` — enum або nullable. Як це виправити?

---

## Статус гілки

Після всіх 5 завдань (кожне — окремий коміт `Lab11 TaskNN` на гілці `Lab-11`):

```bash
git push -u origin Lab-11
git checkout main
git merge --no-ff Lab-11 -m "Merge Lab-11: Reflection & Attributes"
git push
```

> Наступна лаба: `git checkout main` → `git checkout -b Lab-12`.
