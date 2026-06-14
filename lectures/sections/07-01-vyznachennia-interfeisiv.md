---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 1
number: "7.1"
title: "Визначення інтерфейсів"
source: "../_combined/39-vyznachennia-interfeisiv.md"
---

## 7.1. Визначення інтерфейсів

Інтерфейс — це посилальний тип, який задає контракт: перелік методів, властивостей, подій та індексаторів, які зобов'язаний реалізувати будь-який клас або структура, що приймає цей інтерфейс. Сам інтерфейс не містить стану об'єкта і, як правило, не містить реалізації — він лише описує, що клас повинен вміти робити, але не як саме. Завдяки цьому один інтерфейс можуть реалізовувати абсолютно різні класи: і `Patient`, і `Doctor`, і `MedicalDevice` — якщо кожен із них відповідає заданому контракту. Саме це робить інтерфейси головним інструментом поліморфізму та слабкого зв'язування в об'єктно-орієнтованому програмуванні.

Важливо розуміти принципову відмінність від успадкування: клас може успадковувати лише один базовий клас, проте реалізовувати будь-яку кількість інтерфейсів. Це дає можливість описувати різні ролі одного об'єкта: пацієнт може водночас реалізовувати `IDiagnosable` (піддається діагностиці), `IBillable` (підлягає оплаті) та `INotifiable` (отримує сповіщення). Інтерфейси не замінюють успадкування — вони доповнюють його там, де потрібно виразити поведінку, а не походження.

## Визначення інтерфейсу

Для визначення інтерфейсу використовується ключове слово `interface`. За угодою іменування в C# назви інтерфейсів починаються з великої літери `I` — наприклад, `IComparable`, `IEnumerable`, `IDiagnosable`. Це так звана «угорська нотація» для інтерфейсів: вона не є обов'язковою вимогою мови, але є загальноприйнятим стилем у всій екосистемі .NET, якого слід дотримуватись для читабельності коду.

Інтерфейс може визначати такі сутності:

- **Методи** — підписи без реалізації (або з реалізацією за замовчуванням починаючи з C# 8.0)
- **Властивості** — оголошення з аксесорами `get` та/або `set`, без реалізації
- **Індексатори** — доступ до об'єкта за індексом
- **Події** — оголошення подій через `event`
- **Статичні поля та константи** — починаючи з C# 8.0

Проте інтерфейси **не можуть** визначати нестатичні змінні (поля екземпляра), конструктори та деструктори. Заборона на нестатичні поля зумовлена природою інтерфейсу: він описує поведінку, а не стан. Зберігати стан — обов'язок класу, який реалізує інтерфейс. Розглянемо клінічний інтерфейс, що охоплює всі дозволені категорії членів:

```csharp
interface IDiagnosable
{
    // константа
    const int MaxSeverityLevel = 5;
    // статична змінна (C# 8.0+)
    static int DiagnosisCount = 0;
    // метод без реалізації
    void RunDiagnostics();
    // властивість без реалізації
    string DiagnosisCode { get; set; }
    // делегат для події
    delegate void DiagnosisHandler(string message);
    // подія
    event DiagnosisHandler OnDiagnosed;
}
```

У цьому прикладі інтерфейс `IDiagnosable` описує об'єкт медичної системи, який піддається діагностиці. Він не знає, чи це пацієнт, чи лабораторний зразок, чи медичний прилад — він лише фіксує, що будь-який такий об'єкт повинен мати метод запуску діагностики, властивість з кодом діагнозу і подію про завершення діагностики. Конкретна логіка залишається за реалізацією.

Методи та властивості інтерфейсу не мають реалізації — у цьому вони зближуються з абстрактними методами та властивостями абстрактних класів. Метод `RunDiagnostics` не приймає параметрів, нічого не повертає і не має тіла. Те саме стосується властивості `DiagnosisCode`: на перший погляд вона схожа на автоматичну властивість, але насправді це лише декларація в інтерфейсі — реалізація буде в класі.

![Анатомія інтерфейсу: що може і що не може містити](_assets/07-01/interface-anatomy.png)

## Модифікатори доступу

Якщо члени інтерфейсу — методи та властивості — не мають явних модифікаторів доступу, то фактично за замовчуванням вони мають доступ `public`. Це принципово відрізняється від класів і структур, де члени за замовчуванням мають `private`. Таке рішення закономірне: мета інтерфейсу — визначити відкритий контракт для зовнішнього світу, тому всі оголошені в ньому методи та властивості апріорі публічні. Клас, який реалізує інтерфейс, не може зменшити рівень доступу реалізованого члена — він зобов'язаний залишити його `public`.

Це правило стосується також констант і статичних змінних. Якщо в класах і структурах вони за замовчуванням мають `private`, то в інтерфейсах — `public`. Тому до них можна звертатися безпосередньо через ім'я інтерфейсу:

```csharp run
using System;

Console.WriteLine($"Максимальний рівень тяжкості: {IDiagnosable.MaxSeverityLevel.ToString()}");
Console.WriteLine($"Кількість діагнозів: {IDiagnosable.DiagnosisCount.ToString()}");

interface IDiagnosable
{
    const int MaxSeverityLevel = 5;
    static int DiagnosisCount = 0;
    void RunDiagnostics();
    string DiagnosisCode { get; set; }
}
```

Починаючи з C# 8.0, у членів інтерфейсу можна явно вказувати модифікатори доступу. Це дає більш точний контроль над видимістю окремих членів. Наприклад, приватний статичний член може бути допоміжним для реалізації default-методів, тоді як публічні члени формують зовнішній контракт:

```csharp
interface IDiagnosable
{
    public const int MaxSeverityLevel = 5;
    private static int _internalCounter = 0;
    public void RunDiagnostics();
    protected internal string DiagnosisCode { get; set; }
    public delegate void DiagnosisHandler(string message);
    public event DiagnosisHandler OnDiagnosed;
}
```

Як і класи, інтерфейси за замовчуванням мають рівень доступу `internal` — тобто такий інтерфейс доступний лише в межах поточного проекту (збірки). Щоб зробити інтерфейс доступним із зовнішніх збірок, наприклад якщо він є частиною бібліотеки, використовується модифікатор `public`:

```csharp
public interface IDiagnosable
{
    void RunDiagnostics();
}
```

У реальних проектах публічні інтерфейси розміщують в окремій збірці-контракті, яку підключають і клієнтський код, і реалізація. Це дозволяє змінювати реалізацію, не змінюючи публічний контракт.

## Антипатерн: «Бог-інтерфейс» — надмірно широкий контракт

Найпоширеніша помилка при проектуванні інтерфейсів — об'єднати в одному інтерфейсі надто багато непов'язаних між собою обов'язків. Такий інтерфейс називають **«Бог-інтерфейс»** (God Interface): він «знає все» і «вміє все», але саме через це стає антипатерном.

Розглянемо типовий приклад. Розробник вирішив описати всі можливі дії над пацієнтом в одному інтерфейсі:

```csharp
// АНТИПАТЕРН: надто широкий контракт в одному інтерфейсі
interface IPatient
{
    // діагностика
    void RunDiagnostics();
    string GetDiagnosisCode();
    // лікування
    void PrescribeMedication(string med);
    void AssignToWard(string ward);
    // адміністрування
    void Register();
    void Discharge();
    void GenerateBill();
    // сповіщення
    void SendReminder(string message);
    void NotifyEmergencyContact();
}
```

Проблема виникає, коли цей інтерфейс намагаються реалізувати різні класи. Амбулаторний пацієнт не госпіталізується і не потребує `AssignToWard`, але **зобов'язаний** реалізувати цей метод — адже він є частиною контракту. Єдине, що може зробити розробник, — кинути виняток, перетворюючи помилку проектування на помилку часу виконання:

```csharp
class OutpatientRecord : IPatient
{
    public void RunDiagnostics() { /* ... */ }
    public string GetDiagnosisCode() => "J00";
    public void PrescribeMedication(string med) { /* ... */ }

    // Змушені реалізовувати методи, що не стосуються амбулаторного пацієнта:
    public void AssignToWard(string ward)
        => throw new NotSupportedException("Амбулаторний пацієнт не госпіталізується!");
    public void NotifyEmergencyContact()
        => throw new NotSupportedException("Не реалізовано для амбулаторних!");

    public void Register() { /* ... */ }
    public void Discharge() { /* ... */ }
    public void GenerateBill() { /* ... */ }
    public void SendReminder(string message) { /* ... */ }
}
```

`NotSupportedException` у реалізації інтерфейсного методу — чіткий сигнал порушення **принципу розділення інтерфейсів** (ISP — Interface Segregation Principle, детально у розділі 20): клієнти не повинні залежати від методів, які вони не використовують. Компілятор C# не може захистити від помилки, яку можна виявити лише у runtime.

**Рішення** — розбити «Бог-інтерфейс» на вузькоспеціалізовані інтерфейси. Техніка успадкування інтерфейсів (розділ 7.4) дозволяє зібрати потрібний набір обов'язків без дублювання:

```csharp run
using System;

// Кожен інтерфейс — одна відповідальність
interface IDiagnosable
{
    void RunDiagnostics();
    string GetDiagnosisCode();
}

interface ITreatable
{
    void PrescribeMedication(string med);
    void AssignToWard(string ward);
}

interface IAdministrable
{
    void Register();
    void Discharge();
    void GenerateBill();
}

interface INotifiable
{
    void SendReminder(string message);
    void NotifyEmergencyContact();
}

// Стаціонарний пацієнт потребує всіх ролей
class InpatientRecord : IDiagnosable, ITreatable, IAdministrable, INotifiable
{
    public string Name { get; }
    public InpatientRecord(string name) => Name = name;

    public void RunDiagnostics()          => Console.WriteLine($"{Name}: МРТ, ЕКГ");
    public string GetDiagnosisCode()      => "I10.9";
    public void PrescribeMedication(string med) => Console.WriteLine($"{Name}: призначено {med}");
    public void AssignToWard(string ward) => Console.WriteLine($"{Name}: переведено → {ward}");
    public void Register()                => Console.WriteLine($"{Name}: госпіталізовано");
    public void Discharge()               => Console.WriteLine($"{Name}: виписано");
    public void GenerateBill()            => Console.WriteLine($"{Name}: рахунок сформовано");
    public void SendReminder(string msg)  => Console.WriteLine($"{Name}: нагадування — {msg}");
    public void NotifyEmergencyContact()  => Console.WriteLine($"{Name}: повідомлено родичів");
}

// Амбулаторний пацієнт — тільки потрібні ролі; компілятор не дасть викликати AssignToWard
class OutpatientRecord : IDiagnosable, IAdministrable
{
    public string Name { get; }
    public OutpatientRecord(string name) => Name = name;

    public void RunDiagnostics()     => Console.WriteLine($"{Name}: аналізи крові");
    public string GetDiagnosisCode() => "J00";
    public void Register()           => Console.WriteLine($"{Name}: записано на прийом");
    public void Discharge()          => Console.WriteLine($"{Name}: консультацію завершено");
    public void GenerateBill()       => Console.WriteLine($"{Name}: рахунок — 350 грн");
}

var inpatient  = new InpatientRecord("Петренко Іван");
var outpatient = new OutpatientRecord("Коваль Марія");

Console.WriteLine("=== Стаціонар ===");
inpatient.RunDiagnostics();
inpatient.AssignToWard("кардіологія");
inpatient.GenerateBill();
inpatient.NotifyEmergencyContact();

Console.WriteLine("\n=== Амбулаторія ===");
outpatient.RunDiagnostics();
outpatient.GenerateBill();
// outpatient.AssignToWard(...) — помилка компіляції: OutpatientRecord не реалізує ITreatable
```

Тепер `OutpatientRecord` реалізує лише ті інтерфейси, що дійсно стосуються амбулаторного пацієнта. Помилка виявляється на **етапі компіляції**, а не у runtime. Кожен інтерфейс можна підмінити окремим тест-заглушенням (mock), не зачіпаючи інших.

| | Бог-інтерфейс | Вузькі інтерфейси |
|---|---|---|
| Відповідальність | Один клас знає і вміє все | Кожен інтерфейс — одна здібність |
| Непотрібні методи | Клас реалізує методи, що не стосуються його | Клас реалізує лише релевантні інтерфейси |
| Де виявляється помилка | `NotSupportedException` у runtime | Помилка компіляції |
| Тестування | Великий mock із багатьма методами | Мінімальний mock із потрібними методами |
| Вплив змін | Зміна будь-якого методу зачіпає всіх реалізаторів | Зміна вузького інтерфейсу зачіпає лише залежних від нього |

## Реалізація за замовчуванням

Починаючи з C# 8.0, інтерфейси підтримують реалізацію методів і властивостей за замовчуванням. Це означає, що в інтерфейсі можна визначити повноцінний метод із тілом, як у звичайному класі. Такий метод буде автоматично доступний усім класам, що реалізують інтерфейс, — якщо клас не перевизначить його, буде використана реалізація інтерфейсу. Це зручно для поступового розширення вже опублікованих інтерфейсів без порушення зворотної сумісності: новий метод можна додати з реалізацією за замовчуванням, і всі вже існуючі реалізатори продовжать компілюватись без змін.

```csharp run
using System;

IDiagnosable p = new Patient("Марія Коваль");
p.RunDiagnostics();
p.LogDiagnostics();

interface IDiagnosable
{
    void RunDiagnostics();
    // реалізація методу за замовчуванням
    void LogDiagnostics()
    {
        Console.WriteLine("[LOG] Діагностика завершена — результат записано");
    }
}

class Patient : IDiagnosable
{
    public string Name { get; }
    public Patient(string name) => Name = name;
    public void RunDiagnostics() =>
        Console.WriteLine($"Діагностика пацієнта {Name}");
    // LogDiagnostics не перевизначаємо — використовується default
}
```

З реалізацією властивостей за замовчуванням в інтерфейсах ситуація складніша: оскільки інтерфейси не можуть визначати нестатичні змінні, властивість інтерфейсу не може маніпулювати станом екземпляра. Тим не менш реалізацію за замовчуванням для властивості визначити можна — наприклад, для властивості тільки для читання, що повертає фіксоване значення:

```csharp run
using System;

IDiagnosable sample = new LabSample("LAB-2024-001");
sample.RunDiagnostics();
Console.WriteLine($"Рівень тяжкості за замовчуванням: {sample.DefaultSeverity.ToString()}");

interface IDiagnosable
{
    void RunDiagnostics() => Console.WriteLine("Стандартна діагностика");
    // властивість тільки для читання з реалізацією за замовчуванням
    int DefaultSeverity { get { return 1; } }
}

class LabSample : IDiagnosable
{
    public string SampleId { get; }
    public LabSample(string id) => SampleId = id;
    // RunDiagnostics і DefaultSeverity — використовуємо default
}
```

Варто зазначити: якщо інтерфейс має приватні методи або властивості (з модифікатором `private`), вони обов'язково повинні мати реалізацію за замовчуванням — адже до них не може звернутися реалізуючий клас. Те саме стосується статичних методів, які теж мають бути реалізовані в самому інтерфейсі:

```csharp run
using System;

Console.WriteLine($"Максимум: {IDiagnosable.MaxSeverityLevel.ToString()}");
IDiagnosable.MaxSeverityLevel = 7;
Console.WriteLine($"Оновлено: {IDiagnosable.MaxSeverityLevel.ToString()}");
double score = IDiagnosable.CalcRiskScore(145, 98);
Console.WriteLine($"Ризик-скор: {score.ToString("F2")}");

interface IDiagnosable
{
    public const int MinSeverityLevel = 0;
    private static int _maxSeverity = 5;

    static int MaxSeverityLevel
    {
        get => _maxSeverity;
        set { if (value > 0) _maxSeverity = value; }
    }

    // статичний допоміжний метод із реалізацією в інтерфейсі
    static double CalcRiskScore(int systolic, int diastolic)
        => systolic * 0.6 + diastolic * 0.4;
}
```

Статичний метод `CalcRiskScore` визначений і реалізований прямо в інтерфейсі. Він не належить жодному конкретному об'єкту і не успадковується класами-реалізаторами — це суто утилітарний метод інтерфейсу, доступний через ім'я інтерфейсу.

## Інтерфейс vs Абстрактний клас

Студенти часто запитують: коли варто використовувати інтерфейс, а коли абстрактний клас? Обидва інструменти дозволяють описати «незавершений» тип, який конкретизується у нащадках, але їх призначення принципово різне.

**Абстрактний клас** — це неповна реалізація: він може містити поля, конструктори, реалізовані методи та абстрактні методи. Він описує спільну базу для споріднених класів і передає їм стан та частину поведінки. Наприклад, `AbstractMedicalRecord` може зберігати `PatientId`, дату створення і реалізовувати метод `Format()`, лишивши абстрактним метод `Validate()`.

**Інтерфейс** — це чистий контракт поведінки: він не зберігає стану і не нав'язує реалізацію (крім default-методів). Він описує, що об'єкт вміє робити, незалежно від того, що він є. Клас може реалізовувати кілька інтерфейсів одночасно, чого не можна зробити з абстрактними класами. Наприклад, `Patient` може одночасно реалізовувати `IDiagnosable`, `IBillable` та `INotifiable`.

Практичне правило: якщо різні, не споріднені класи мають розділяти одну поведінку — використовуй інтерфейс. Якщо класи є різновидами одного типу і мають спільний стан або базову реалізацію — використовуй абстрактний клас.

![Інтерфейс vs Абстрактний клас](_assets/07-01/interface-vs-abstract.png)

## Визначення інтерфейсу у проекті

У Visual Studio є спеціальний шаблон для швидкого додавання нового інтерфейсу в окремому файлі. Для цього можна натиснути праву кнопку миші на проекті в Solution Explorer і у контекстному меню вибрати **Додати → Новий елемент**, а потім у діалоговому вікні — пункт **Інтерфейс**. Visual Studio автоматично створить файл із заготовкою `interface IMyInterface { }` і відповідним namespace.

Водночас можна додати звичайний файл класу (`.cs`) і вручну написати ключове слово `interface` замість `class` — компілятор не робить різниці, в якому файлі визначено інтерфейс. За угодою, кожен інтерфейс розміщують в окремому файлі, назва якого збігається з іменем інтерфейсу, наприклад `IDiagnosable.cs`. Це полегшує навігацію в проекті та є стандартом у більшості C# кодових баз.
