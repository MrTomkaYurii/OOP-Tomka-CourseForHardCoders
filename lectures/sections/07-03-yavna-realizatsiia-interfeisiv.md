---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 3
number: "7.3"
title: "Явна реалізація інтерфейсів"
source: "../_combined/41-yavna-realizatsiia-interfeisiv.md"
---

## 7.3. Явна реалізація інтерфейсів

Окрім звичайної (неявної) реалізації інтерфейсу, де метод просто оголошується у класі з модифікатором `public`, існує **явна реалізація** — коли перед ім'ям методу або властивості вказується назва конкретного інтерфейсу. При явній реалізації модифікатор доступу не вказується взагалі — метод автоматично є закритим для прямого доступу через змінну класу і доступний виключно через змінну типу інтерфейсу.

Явна реалізація вирішує дві головні проблеми: по-перше, вона дозволяє розмежувати методи з однаковими підписами, якщо клас реалізує кілька інтерфейсів, що мають однойменні члени. По-друге, вона потрібна, коли члени інтерфейсу мають модифікатор доступу, відмінний від `public` — такі члени неможливо реалізувати неявно.

Синтаксис явної реалізації виглядає так: замість `public void RunDiagnostics()` пишемо `void IDiagnosable.RunDiagnostics()` — без `public`, з префіксом інтерфейсу:

```csharp run
using System;

class Patient : IDiagnosable
{
    public string Name { get; }
    public Patient(string name) => Name = name;

    // явна реалізація — без public, з префіксом інтерфейсу
    void IDiagnosable.RunDiagnostics()
        => Console.WriteLine($"[IDiagnosable] Діагностика пацієнта {Name}");
}

// доступ ТІЛЬКИ через змінну інтерфейсу
IDiagnosable p = new Patient("Марія Коваль");
p.RunDiagnostics();

interface IDiagnosable
{
    void RunDiagnostics();
}
```

## Доступ до явно реалізованих членів

Принципова особливість явної реалізації — явно реалізований член є частиною інтерфейсу класу, а не самого класу. Тому звернутися до нього безпосередньо через об'єкт класу неможливо: компілятор не знайде такого методу. Метод доступний лише через змінну типу відповідного інтерфейсу.

Це обмеження відіграє роль захисту інкапсуляції: зовнішній код може викликати `RunDiagnostics` лише у тому контексті, де він знає що об'єкт є `IDiagnosable`, — тобто свідомо, через контракт. Це запобігає випадковому виклику методу через «неправильний» контекст.

Для доступу до явно реалізованого члена через об'єкт класу потрібне явне приведення — безпечне через `is` або небезпечне через `(IInterface)`:

```csharp run
using System;

Patient p = new Patient("Іван Петренко");

// p.RunDiagnostics(); // ! Помилка — клас Patient не має публічного методу RunDiagnostics

// варіант 1: небезпечне приведення (кине виняток якщо тип не збігається)
((IDiagnosable)p).RunDiagnostics();

// варіант 2: безпечне приведення через is (рекомендовано)
if (p is IDiagnosable diag) diag.RunDiagnostics();

// варіант 3: змінна типу інтерфейсу одразу
IDiagnosable d = new Patient("Олена Сидоренко");
d.RunDiagnostics();

class Patient : IDiagnosable
{
    public string Name { get; }
    public Patient(string name) => Name = name;
    void IDiagnosable.RunDiagnostics()
        => Console.WriteLine($"Діагностика: {Name}");
}

interface IDiagnosable
{
    void RunDiagnostics();
}
```

![Явна vs неявна реалізація: диспетчеризація через тип змінної](_assets/07-03/explicit-vs-implicit.png)

## Конфлікт імен при множинній реалізації

Найбільш поширена ситуація, коли без явної реалізації не обійтись, — клас реалізує кілька інтерфейсів, які мають методи з однаковою сигнатурою, але різним змістом. У клінічній системі такий конфлікт виникає природно: наприклад, `IDiagnosable` і `ITreatment` обидва можуть мати метод `RunProcedure()` — але перший запускає діагностичну процедуру, а другий — лікувальну.

Якщо клас визначає один метод `RunProcedure()` без явної реалізації, він стає спільним для обох інтерфейсів — і виклик через `IDiagnosable`, і виклик через `ITreatment` дасть той самий результат. Це може бути прийнятним, але частіше потрібна різна поведінка для різних ролей:

```csharp run
using System;

// без явної реалізації — один спільний метод
class Patient : IDiagnosable, ITreatment
{
    public string Name { get; }
    public Patient(string name) => Name = name;

    public void RunProcedure()
        => Console.WriteLine($"{Name}: загальна процедура (однакова для обох інтерфейсів)");
}

Patient p = new Patient("Василь Мороз");
((IDiagnosable)p).RunProcedure();  // загальна процедура
((ITreatment)p).RunProcedure();    // загальна процедура — той самий метод

interface IDiagnosable { void RunProcedure(); }
interface ITreatment   { void RunProcedure(); }
```

Щоб розмежувати реалізацію — застосовуємо явну реалізацію для кожного інтерфейсу окремо. Тоді кожен інтерфейс отримує власну незалежну логіку:

```csharp run
using System;

class Patient : IDiagnosable, ITreatment
{
    public string Name { get; }
    public Patient(string name) => Name = name;

    void IDiagnosable.RunProcedure()
        => Console.WriteLine($"{Name}: діагностична процедура — МРТ, аналізи");

    void ITreatment.RunProcedure()
        => Console.WriteLine($"{Name}: лікувальна процедура — ін'єкція, крапельниця");
}

Patient p = new Patient("Тетяна Руденко");
((IDiagnosable)p).RunProcedure();
((ITreatment)p).RunProcedure();

interface IDiagnosable { void RunProcedure(); }
interface ITreatment   { void RunProcedure(); }
```

## Модифікатори доступу та явна реалізація

Члени інтерфейсу можуть мати різні модифікатори доступу — починаючи з C# 8.0. Якщо член інтерфейсу оголошений не як `public`, а, наприклад, як `protected internal`, — реалізувати його неявно (через звичайний публічний метод класу) неможливо. Саме тоді єдиним способом є явна реалізація.

Це пов'язано з логікою мови: неявна реалізація означає, що метод одночасно є членом і класу, і інтерфейсу. Але якщо інтерфейс вимагає `protected internal`, а клас хотів би зробити метод `public` — виникає суперечність. Явна реалізація розриває цей зв'язок: метод належить виключно інтерфейсу і доступний лише через нього.

Особливо це стосується подій і властивостей з нестандартними модифікаторами — їх явна реалізація вимагає повного запису аксесорів:

```csharp run
using System;

IMonitorable mon = new Patient("Надія Литвин");
mon.StatusChanged += () => Console.WriteLine($"[ALERT] Статус пацієнта змінився");
mon.UpdateStatus("Критичний стан");

interface IMonitorable
{
    protected internal void UpdateStatus(string status);
    protected internal string CurrentStatus { get; }
    delegate void StatusHandler();
    protected internal event StatusHandler StatusChanged;
}

class Patient : IMonitorable
{
    string _status = "Норма";
    IMonitorable.StatusHandler? _statusChanged;

    // явна реалізація події з аксесорами
    event IMonitorable.StatusHandler IMonitorable.StatusChanged
    {
        add    => _statusChanged += value;
        remove => _statusChanged -= value;
    }

    // явна реалізація властивості
    string IMonitorable.CurrentStatus => _status;

    public string Name { get; }
    public Patient(string name) => Name = name;

    // явна реалізація методу
    void IMonitorable.UpdateStatus(string status)
    {
        _status = status;
        Console.WriteLine($"{Name}: статус оновлено → {_status}");
        _statusChanged?.Invoke();
    }
}
```

Важливо: до явно реалізованих методів, властивостей і подій можна звертатися виключно через змінну інтерфейсу, але не через змінну класу. Це означає, що `Patient p = new Patient(...)` не дасть доступу до `UpdateStatus`, `CurrentStatus` чи `StatusChanged` — лише `IMonitorable m = new Patient(...)` відкриє ці члени.

## Реалізація інтерфейсів у базових та похідних класах

Якщо клас реалізує інтерфейс, він зобов'язаний реалізувати всі методи і властивості, що не мають реалізації за замовчуванням. Однак є виняток: клас може оголосити такі методи **абстрактними**, делегуючи відповідальність за реалізацію своїм похідним класам. У цьому випадку сам клас має бути абстрактним:

```csharp run
using System;

interface IDiagnosable
{
    void RunDiagnostics();
}

// абстрактний клас реалізує інтерфейс, але відкладає реалізацію
abstract class MedicalRecord : IDiagnosable
{
    public string PatientName { get; }
    protected MedicalRecord(string name) => PatientName = name;

    public abstract void RunDiagnostics(); // нехай похідні класи вирішують
}

class ClinicalRecord : MedicalRecord
{
    public ClinicalRecord(string name) : base(name) { }
    public override void RunDiagnostics()
        => Console.WriteLine($"{PatientName}: клінічний огляд — анамнез, симптоми");
}

class LabRecord : MedicalRecord
{
    public LabRecord(string name) : base(name) { }
    public override void RunDiagnostics()
        => Console.WriteLine($"{PatientName}: лабораторна діагностика — кров, сеча, біопсія");
}

IDiagnosable r1 = new ClinicalRecord("Олег Бойко");
IDiagnosable r2 = new LabRecord("Марина Шевченко");
r1.RunDiagnostics();
r2.RunDiagnostics();
```

Інша важлива ситуація: похідний клас може «успадкувати» реалізацію інтерфейсу від базового класу, навіть якщо сам базовий клас не оголошував реалізацію інтерфейсу явно. Якщо у базовому класі є публічний метод з відповідною сигнатурою, і похідний клас оголошує реалізацію інтерфейсу — компілятор автоматично прив'яже існуючий метод:

```csharp run
using System;

interface IDiagnosable
{
    void RunDiagnostics();
}

class BaseRecord
{
    // публічний метод — компілятор підхопить його як реалізацію IDiagnosable
    public void RunDiagnostics()
        => Console.WriteLine("BaseRecord: стандартна діагностика");
}

// HeroRecord успадковує метод і реалізує IDiagnosable через нього
class SpecialRecord : BaseRecord, IDiagnosable { }

IDiagnosable sr = new SpecialRecord();
sr.RunDiagnostics(); // викликається метод з BaseRecord

```

Якщо клас одночасно успадковує клас і реалізує інтерфейс, ім'я базового класу завжди вказується першим, а інтерфейси — після нього:

```csharp
class SpecialRecord : BaseRecord, IDiagnosable, ITreatment { }
```

## Зміна реалізації інтерфейсів у похідних класах

Може скластися ситуація, що базовий клас вже реалізував інтерфейс, але в похідному класі потрібно змінити цю реалізацію. Для цього існують чотири підходи, які відрізняються за механікою диспетчеризації (тобто якій саме реалізації відповідає виклик через різні типи змінних).

### Варіант 1 — перевизначення через `override`

Найправильніший і найпередбачуваніший варіант. Базовий клас оголошує метод як `virtual` (або `abstract`), а похідний — перевизначає через `override`. При цьому поліморфізм працює повністю: незалежно від того, чи тримаємо ми об'єкт у змінній базового класу, чи інтерфейсу, — завжди викликається реалізація з фактичного типу об'єкта:

```csharp run
using System;

interface IDiagnosable { void RunDiagnostics(); }

class BaseRecord : IDiagnosable
{
    public virtual void RunDiagnostics()
        => Console.WriteLine("BaseRecord: стандартна діагностика");
}

class SpecialRecord : BaseRecord
{
    public override void RunDiagnostics()
        => Console.WriteLine("SpecialRecord: розширена діагностика");
}

BaseRecord  r1 = new SpecialRecord();
IDiagnosable r2 = new SpecialRecord();
SpecialRecord r3 = new SpecialRecord();

r1.RunDiagnostics(); // SpecialRecord — поліморфізм
r2.RunDiagnostics(); // SpecialRecord — поліморфізм
r3.RunDiagnostics(); // SpecialRecord
```

### Варіант 2 — приховування через `new`

Похідний клас визначає метод із `new`, не перевизначаючи базовий. Такий метод «приховує» базовий, але лише для тих змінних, тип яких є похідним класом. Через змінну базового класу або інтерфейсу буде видно реалізацію з **базового** класу — адже саме там інтерфейс і був реалізований:

```csharp run
using System;

interface IDiagnosable { void RunDiagnostics(); }

class BaseRecord : IDiagnosable
{
    public void RunDiagnostics()
        => Console.WriteLine("BaseRecord: стандартна діагностика");
}

class SpecialRecord : BaseRecord
{
    public new void RunDiagnostics()
        => Console.WriteLine("SpecialRecord: спеціальна діагностика");
}

BaseRecord   r1 = new SpecialRecord();
IDiagnosable r2 = new SpecialRecord();
SpecialRecord r3 = new SpecialRecord();

r1.RunDiagnostics(); // BaseRecord — раннє зв'язування
r2.RunDiagnostics(); // BaseRecord — інтерфейс реалізований у BaseRecord
r3.RunDiagnostics(); // SpecialRecord — прямий тип
```

### Варіант 3 — повторна реалізація інтерфейсу разом із `new`

Якщо похідний клас явно вказує інтерфейс у своєму оголошенні (`: BaseRecord, IDiagnosable`), це означає **повторну реалізацію** інтерфейсу. Тепер компілятор прив'яже інтерфейс до нового методу `new` у похідному класі, а не до базового. Через змінну інтерфейсу буде видно реалізацію з **похідного** класу, але через змінну базового — як і раніше базова:

```csharp run
using System;

interface IDiagnosable { void RunDiagnostics(); }

class BaseRecord : IDiagnosable
{
    public void RunDiagnostics()
        => Console.WriteLine("BaseRecord: стандартна діагностика");
}

// повторна реалізація — IDiagnosable вказаний явно у SpecialRecord
class SpecialRecord : BaseRecord, IDiagnosable
{
    public new void RunDiagnostics()
        => Console.WriteLine("SpecialRecord: спеціальна діагностика");
}

BaseRecord   r1 = new SpecialRecord();
IDiagnosable r2 = new SpecialRecord();
SpecialRecord r3 = new SpecialRecord();

r1.RunDiagnostics(); // BaseRecord — раннє зв'язування за типом змінної
r2.RunDiagnostics(); // SpecialRecord — інтерфейс тепер прив'язаний до SpecialRecord
r3.RunDiagnostics(); // SpecialRecord
```

### Варіант 4 — явна реалізація інтерфейсу в похідному класі

Найбільш гнучкий варіант: похідний клас одночасно має `new`-метод (для доступу через власний тип) і явну реалізацію інтерфейсу (для доступу через змінну інтерфейсу). Це дає три різних результати залежно від типу змінної:

```csharp run
using System;

interface IDiagnosable { void RunDiagnostics(); }

class BaseRecord : IDiagnosable
{
    public void RunDiagnostics()
        => Console.WriteLine("BaseRecord: стандартна діагностика");
}

class SpecialRecord : BaseRecord, IDiagnosable
{
    public new void RunDiagnostics()
        => Console.WriteLine("SpecialRecord: спеціальна діагностика");

    // явна реалізація — виключно для змінної типу IDiagnosable
    void IDiagnosable.RunDiagnostics()
        => Console.WriteLine("SpecialRecord (явна IDiagnosable): протокол діагностики");
}

BaseRecord   r1 = new SpecialRecord();
IDiagnosable r2 = new SpecialRecord();
SpecialRecord r3 = new SpecialRecord();

r1.RunDiagnostics(); // BaseRecord — раннє зв'язування
r2.RunDiagnostics(); // явна IDiagnosable — найвищий пріоритет
r3.RunDiagnostics(); // SpecialRecord — новий public метод
```

![4 варіанти зміни реалізації інтерфейсу у похідному класі](_assets/07-03/override-variants.png)

Вибір між варіантами залежить від задачі: якщо потрібен повноцінний поліморфізм — `override`. Якщо потрібно лише «перекрити» метод для прямого використання — `new`. Якщо потрібно перезв'язати інтерфейс із новою реалізацією — повторна реалізація (`new` + інтерфейс у заголовку). Якщо потрібна абсолютно незалежна логіка для інтерфейсного контексту — явна реалізація.
