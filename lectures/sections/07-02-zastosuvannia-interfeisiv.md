---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 2
number: "7.2"
title: "Застосування інтерфейсів"
source: "../_combined/40-zastosuvannia-interfeisiv.md"
---

## 7.2. Застосування інтерфейсів

Інтерфейс являє собою певний опис типу — набір компонентів, який повинен мати тип даних, що реалізує цей інтерфейс. Принципова відмінність від класу: ми не можемо створювати об'єкти інтерфейсу безпосередньо через конструктор. Інтерфейс — це не клас, у нього немає конструктора і немає тіла для розміщення стану:

```csharp
IDiagnosable d = new IDiagnosable(); // ! Помилка — інтерфейс не можна інстанціювати

interface IDiagnosable
{
    void RunDiagnostics();
}
```

Натомість інтерфейс призначений для реалізації у класах і структурах. Змінна типу інтерфейсу може зберігати посилання на будь-який об'єкт, клас якого реалізує цей інтерфейс. Саме це і є ключовою перевагою: код, що працює з `IDiagnosable`, не знає — і не повинен знати — чи це `Patient`, `LabSample`, чи `MedicalDevice`. Він знає лише, що об'єкт гарантовано має метод `RunDiagnostics()`.

## Реалізація інтерфейсу у класі та структурі

Для застосування інтерфейсу після імені класу або структури через двокрапку вказується ім'я інтерфейсу — так само, як при успадкуванні. Клас зобов'язаний реалізувати **всі** методи та властивості інтерфейсу, якщо вони не мають реалізації за замовчуванням. Невиконання цієї умови — помилка компіляції.

Якщо методи та властивості інтерфейсу оголошені без модифікатора доступу, вони вважаються `public`. При реалізації в класі або структурі до них можна застосовувати виключно модифікатор `public` — зменшити рівень доступу неможливо, адже інтерфейс є публічним контрактом.

Інтерфейс може реалізовувати не лише клас, а й структура. Для структури це особливо важливо: вона не може успадковувати клас, але може реалізовувати будь-яку кількість інтерфейсів:

```csharp run
using System;

// реалізація інтерфейсу в класі
class Patient : IDiagnosable
{
    public string Name { get; }
    public Patient(string name) => Name = name;

    public void RunDiagnostics()
        => Console.WriteLine($"Діагностика пацієнта {Name} розпочата");
}

// реалізація інтерфейсу в структурі
struct LabSample : IDiagnosable
{
    public string SampleId { get; }
    public LabSample(string id) => SampleId = id;

    public void RunDiagnostics()
        => Console.WriteLine($"Аналіз зразка {SampleId} виконано");
}

Patient p      = new Patient("Марія Коваль");
LabSample s    = new LabSample("LAB-2024-099");
p.RunDiagnostics();
s.RunDiagnostics();

interface IDiagnosable
{
    void RunDiagnostics();
}
```

## Інтерфейс як параметр методу — поліморфізм

Найпрактичніше застосування інтерфейсів — передача як параметра методу. Метод, що приймає `IDiagnosable`, може працювати з будь-яким об'єктом, що реалізує цей інтерфейс: класом, структурою, або будь-яким майбутнім типом, який ще не написаний. На момент написання такого методу достатньо знати лише контракт — що у переданого об'єкта є метод `RunDiagnostics()`.

Це і є поліморфізм через інтерфейс: один метод обробляє різні типи однаково, через спільний контракт:

```csharp run
using System;

Patient   p = new Patient("Іван Петренко");
LabSample s = new LabSample("LAB-2024-007");

ProcessDiagnostics(p);
ProcessDiagnostics(s);

void ProcessDiagnostics(IDiagnosable target)
{
    Console.WriteLine("--- Початок діагностики ---");
    target.RunDiagnostics();
    Console.WriteLine("--- Завершено ---");
}

interface IDiagnosable
{
    void RunDiagnostics();
}

class Patient : IDiagnosable
{
    public string Name { get; }
    public Patient(string name) => Name = name;
    public void RunDiagnostics()
        => Console.WriteLine($"Пацієнт {Name}: клінічний огляд");
}

struct LabSample : IDiagnosable
{
    public string SampleId { get; }
    public LabSample(string id) => SampleId = id;
    public void RunDiagnostics()
        => Console.WriteLine($"Зразок {SampleId}: хімічний аналіз");
}
```

Метод `ProcessDiagnostics` не має жодної залежності від `Patient` чи `LabSample`. Інтерфейс — це контракт, що певний тип обов'язково реалізує деякий функціонал. Якщо завтра з'явиться новий тип `MedicalDevice : IDiagnosable`, метод `ProcessDiagnostics` одразу зможе з ним працювати без жодних змін.

## Реалізація за замовчуванням

Починаючи з C# 8.0, інтерфейси підтримують реалізацію методів і властивостей за замовчуванням. Це вирішує важливу практичну проблему: якщо опублікований інтерфейс використовують десятки класів у різних бібліотеках, додавання нового абстрактного методу зламає всі ці класи — вони перестануть компілюватись. Замість цього новий метод можна додати з реалізацією за замовчуванням: усі наявні реалізатори продовжать працювати, а ті, кому потрібна специфічна поведінка, перевизначать метод самостійно.

```csharp run
using System;

IDiagnosable p1 = new Patient("Олег Бойко");
IDiagnosable p2 = new LabSample("LAB-2024-042");

p1.RunDiagnostics();
p1.LogResult();   // використовує default-реалізацію

p2.RunDiagnostics();
p2.LogResult();   // LabSample перевизначив LogResult

interface IDiagnosable
{
    void RunDiagnostics();
    // реалізація за замовчуванням — додана пізніше, не ламає наявні класи
    void LogResult()
        => Console.WriteLine("[LOG] Результат діагностики збережено в системі");
}

class Patient : IDiagnosable
{
    public string Name { get; }
    public Patient(string name) => Name = name;
    public void RunDiagnostics()
        => Console.WriteLine($"Пацієнт {Name}: огляд завершено");
    // LogResult не перевизначаємо — береться з інтерфейсу
}

class LabSample : IDiagnosable
{
    public string SampleId { get; }
    public LabSample(string id) => SampleId = id;
    public void RunDiagnostics()
        => Console.WriteLine($"Зразок {SampleId}: аналіз завершено");
    // власна реалізація LogResult
    public void LogResult()
        => Console.WriteLine($"[LAB-LOG] Зразок {SampleId} — результат відправлено до лабораторії");
}
```

Варто зазначити важливий нюанс: якщо змінна оголошена типом конкретного класу (а не інтерфейсу), виклик default-методу через неї неможливий, якщо клас його не перевизначив. Default-реалізація доступна лише через змінну типу інтерфейсу:

```csharp run
using System;

IDiagnosable asInterface = new Patient("Тетяна Руденко");
asInterface.LogResult(); // OK — default реалізація через інтерфейс

Patient asConcrete = new Patient("Тетяна Руденко");
// asConcrete.LogResult(); // ! Помилка — клас Patient не визначив LogResult

interface IDiagnosable
{
    void LogResult() => Console.WriteLine("[LOG] Збережено");
}

class Patient : IDiagnosable
{
    public string Name { get; }
    public Patient(string name) => Name = name;
}
```

## Множинна реалізація інтерфейсів

В C# клас може успадковувати лише один базовий клас, але реалізовувати будь-яку кількість інтерфейсів. Це дозволяє описати різні ролі одного об'єкта незалежно одна від одної. Реальний клінічний об'єкт — наприклад, пацієнт — одночасно підлягає діагностиці, виставленню рахунків і отриманню сповіщень. Кожна ця роль виражається своїм інтерфейсом, і клас `Patient` реалізує їх усі:

```csharp
class Patient : IDiagnosable, IBillable, INotifiable
{
    // ...
}
```

Усі реалізовані інтерфейси перераховуються через кому. Якщо клас одночасно успадковує базовий клас і реалізує інтерфейси, базовий клас вказується першим:

```csharp
class Patient : BaseRecord, IDiagnosable, IBillable, INotifiable
{
    // ...
}
```

Розглянемо повний клінічний приклад із трьома інтерфейсами:

```csharp run
using System;

Patient p = new Patient("Надія Литвин", "D-2024-077");

// через різні інтерфейси — різні ролі одного об'єкта
IDiagnosable  diag  = p;
IBillable     bill  = p;
INotifiable   note  = p;

diag.RunDiagnostics();
Console.WriteLine($"Рахунок: {bill.CalcBill().ToString()} грн.");
note.Notify("Результати готові — зверніться до лікаря");

interface IDiagnosable
{
    void RunDiagnostics();
}
interface IBillable
{
    decimal CalcBill();
}
interface INotifiable
{
    void Notify(string message);
}

class Patient : IDiagnosable, IBillable, INotifiable
{
    public string Name       { get; }
    public string DiagCode   { get; }

    public Patient(string name, string diagCode)
    {
        Name     = name;
        DiagCode = diagCode;
    }

    public void RunDiagnostics()
        => Console.WriteLine($"Пацієнт {Name}: діагностика за кодом {DiagCode}");

    public decimal CalcBill()
        => 850.00m;

    public void Notify(string message)
        => Console.WriteLine($"[SMS → {Name}]: {message}");
}
```

![Клас реалізує кілька інтерфейсів](_assets/07-02/multiple-interfaces.png)

## Інтерфейси у перетвореннях типів

Все сказане щодо перетворення типів між класами стосується і інтерфейсів. Оскільки клас `Patient` реалізує інтерфейс `IDiagnosable`, змінна типу `IDiagnosable` може зберігати посилання на об'єкт типу `Patient`. Таке перетворення від конкретного класу до інтерфейсу є **розширювальним** (widening) і відбувається автоматично — воно завжди безпечне, бо будь-який `Patient` гарантовано є `IDiagnosable`:

```csharp run
using System;

Patient p = new Patient("Василь Мороз", "D-001");

// автоматичне розширювальне перетворення — завжди OK
IDiagnosable diag = p;
diag.RunDiagnostics();

// через інтерфейс доступні тільки члени інтерфейсу
// diag.Name — ! Помилка: IDiagnosable не має властивості Name

interface IDiagnosable
{
    void RunDiagnostics();
}

class Patient : IDiagnosable
{
    public string Name    { get; }
    public string DiagCode { get; }
    public Patient(string name, string code) { Name = name; DiagCode = code; }
    public void RunDiagnostics()
        => Console.WriteLine($"Пацієнт {Name} [{DiagCode}]: діагностику розпочато");
}
```

Зворотне перетворення — від інтерфейсу до конкретного класу — є **звужувальним** (narrowing). Воно не відбувається автоматично, тому що не кожен `IDiagnosable` є `Patient`: інтерфейс можуть реалізовувати й інші класи. Для звужувального перетворення потрібне явне приведення або перевірка через `is`/`as`:

```csharp run
using System;

IDiagnosable diag = new Patient("Олена Сидоренко", "D-055");

// is — перевірка типу + безпечне приведення
if (diag is Patient pat)
{
    Console.WriteLine($"Ім'я: {pat.Name}");
    Console.WriteLine($"Код: {pat.DiagCode}");
}

// as — повертає null якщо тип не відповідає (не кидає виняток)
Patient? asPat = diag as Patient;
if (asPat != null)
    Console.WriteLine($"Через as: {asPat.Name}");

// явне приведення — кине InvalidCastException якщо тип не відповідає
Patient explicit = (Patient)diag;
Console.WriteLine($"Явне: {explicit.Name}");

interface IDiagnosable
{
    void RunDiagnostics();
}

class Patient : IDiagnosable
{
    public string Name    { get; }
    public string DiagCode { get; }
    public Patient(string name, string code) { Name = name; DiagCode = code; }
    public void RunDiagnostics()
        => Console.WriteLine($"Діагностика: {Name}");
}
```

На практиці перевага — за `is` із pattern matching: він одночасно перевіряє тип і виконує приведення в одному виразі, не кидаючи винятків. Оператор `as` зручний, коли потрібно лише перевірити і не виконувати тіло `if` одразу. Явне приведення через `(T)` застосовується лише тоді, коли тип відомий з абсолютною впевненістю.

![Перетворення типів через інтерфейс](_assets/07-02/interface-type-cast.png)
