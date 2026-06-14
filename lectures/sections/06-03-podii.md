---
chapter: 6
chapterTitle: "Розділ 6. Делегати, події та лямбди"
section: 3
number: "6.3"
title: "Події"
source: "../_migration/source-chunks/36-podii.md"
---

## 6.3. Події

Події сигналізують системі про те, що сталася певна дія. Якщо делегат — це лише посилання на метод, то подія — це спеціальна конструкція, яка обгортає делегат і накладає обмеження на доступ до нього. Зовнішній код може лише підписатися на подію (`+=`) або відписатися від неї (`-=`), але не може викликати подію безпосередньо або замінити весь список обробників через звичайне присвоєння. Це важливе архітектурне рішення: клас контролює, коли і чому виникає подія, а зовнішній код лише реагує на неї.

## Навіщо потрібні події

Розглянемо клас `Patient`, який описує пацієнта медичної системи із страховим рахунком:

```csharp
class Patient
{
    public int Balance { get; private set; }
    public string Name { get; }
    public Patient(string name, int balance) { Name = name; Balance = balance; }

    public void AddFunds(int amount) => Balance += amount;

    public void Spend(int amount)
    {
        if (Balance >= amount) Balance -= amount;
    }
}
```

Якщо ми захочемо повідомляти про кожне списання страхових коштів, найпростіший варіант — додати `Console.WriteLine` прямо в метод `Spend`:

```csharp
public void Spend(int amount)
{
    if (Balance >= amount)
    {
        Balance -= amount;
        Console.WriteLine($"Списано {amount} грн. зі страхового рахунку пацієнта {Name}.");
    }
}
```

Але цей підхід має серйозні обмеження. На момент написання класу ми можемо точно не знати, яку саме дію потрібно виконати після списання. У консольному застосунку — це виведення рядка. У графічному WPF-додатку — спливне вікно. У веб-API — запис у лог або відправка HTTP-запиту. Якщо клас `Patient` планується як бібліотека для різних проектів — жорстко вшитий `Console.WriteLine` не підходить: інші розробники захочуть реагувати на списання по-своєму, і ми навіть не знаємо заздалегідь як саме. Саме для вирішення цієї проблеми існують події.

## Визначення та виклик події

Подія оголошується в класі за допомогою ключового слова `event`, після якого вказується тип делегата, що представляє подію:

```csharp
delegate void PatientHandler(string message);
event PatientHandler Notify;
```

Спочатку визначається делегат `PatientHandler`, що приймає один параметр `string`. Потім за допомогою `event` визначається подія `Notify`, представлена цим делегатом. Назва події може бути довільною, але вона завжди прив'язана до конкретного делегата.

Оголошену подію можна викликати всередині класу як метод:

```csharp
Notify("Сталося списання");
```

Оскільки `Notify` представляє делегат `PatientHandler`, що приймає рядок, — при виклику передається рядок. Якщо жоден обробник не зареєстрований, подія дорівнює `null`, тому при виклику краще завжди перевіряти:

```csharp
Notify?.Invoke("Сталося списання");
```

Метод `Invoke` із оператором умовного null `?.` не виконає виклик, якщо подія `null`, — виняток не виникне.

Поєднаємо все разом — визначимо подію і виклики у повному класі:

```csharp run
using System;

Patient p = new Patient("Іван Петренко", 500);
// обробник ще не встановлено — виклики події не дають ефекту
p.AddFunds(100);
p.Spend(200);
Console.WriteLine($"Баланс: {p.Balance.ToString()} грн.");

class Patient
{
    public delegate void PatientHandler(string message);
    public event PatientHandler? Notify;        // 1. Визначення події

    public string Name { get; }
    public int Balance { get; private set; }

    public Patient(string name, int balance) { Name = name; Balance = balance; }

    public void AddFunds(int amount)
    {
        Balance += amount;
        Notify?.Invoke($"На рахунок {Name} зараховано: {amount.ToString()} грн.");  // 2. Виклик
    }

    public void Spend(int amount)
    {
        if (Balance >= amount)
        {
            Balance -= amount;
            Notify?.Invoke($"З рахунку {Name} списано: {amount.ToString()} грн.");  // 3. Виклик
        }
        else
        {
            Notify?.Invoke($"Недостатньо коштів. Баланс {Name}: {Balance.ToString()} грн.");
        }
    }
}
```

Поки жоден обробник не зареєстрований, виклики `Notify?.Invoke(...)` нічого не роблять — подія `null`.

## Додавання обробника події

Обробник події — це метод, який виконується під час виклику події. Його список параметрів і тип повернення мають відповідати делегату події. Обробник додається через `+=`:

```csharp run
using System;

Patient p = new Patient("Марія Коваль", 500);
p.Notify += DisplayMessage;         // підписуємось на подію

p.AddFunds(200);
Console.WriteLine($"Баланс: {p.Balance.ToString()} грн.");
p.Spend(300);
Console.WriteLine($"Баланс: {p.Balance.ToString()} грн.");
p.Spend(600);
Console.WriteLine($"Баланс: {p.Balance.ToString()} грн.");

void DisplayMessage(string message) => Console.WriteLine(message);

class Patient
{
    public delegate void PatientHandler(string message);
    public event PatientHandler? Notify;
    public string Name { get; }
    public int Balance { get; private set; }
    public Patient(string name, int balance) { Name = name; Balance = balance; }
    public void AddFunds(int amount)
    {
        Balance += amount;
        Notify?.Invoke($"На рахунок {Name} зараховано: {amount.ToString()} грн.");
    }
    public void Spend(int amount)
    {
        if (Balance >= amount)
        {
            Balance -= amount;
            Notify?.Invoke($"З рахунку {Name} списано: {amount.ToString()} грн.");
        }
        else
        {
            Notify?.Invoke($"Недостатньо коштів. Баланс {Name}: {Balance.ToString()} грн.");
        }
    }
}
```

Метод `DisplayMessage` відповідає делегату `PatientHandler` — приймає `string`, нічого не повертає. При виклику `Notify?.Invoke(...)` тепер буде виконуватися цей метод. Клас `Patient` нічого не знає про `Console.WriteLine` — він лише надсилає повідомлення через подію. Зовнішній код вирішує, що з ним робити.

![Потік події: реєстрація обробника та виклик](_assets/06-03/event-flow.png)

## Додавання та видалення обробників

Для однієї події можна зареєструвати кілька обробників — і в будь-який момент видалити будь-який із них через `-=`:

```csharp run
using System;

Patient p = new Patient("Олег Бойко", 800);

p.Notify += DisplayMessage;         // реєструємо перший обробник
p.Notify += DisplayWarningMessage;  // реєструємо другий

p.AddFunds(100);                    // спрацюють обидва
Console.WriteLine("---");
p.Notify -= DisplayWarningMessage;  // видаляємо другий
p.Spend(300);                       // спрацює лише перший

void DisplayMessage(string message) => Console.WriteLine(message);
void DisplayWarningMessage(string message)
{
    Console.ForegroundColor = ConsoleColor.Yellow;
    Console.WriteLine($"[!] {message}");
    Console.ResetColor();
}

class Patient
{
    public delegate void PatientHandler(string message);
    public event PatientHandler? Notify;
    public string Name { get; }
    public int Balance { get; private set; }
    public Patient(string name, int balance) { Name = name; Balance = balance; }
    public void AddFunds(int amount)
    {
        Balance += amount;
        Notify?.Invoke($"На рахунок {Name} зараховано: {amount.ToString()} грн.");
    }
    public void Spend(int amount)
    {
        if (Balance >= amount)
        {
            Balance -= amount;
            Notify?.Invoke($"З рахунку {Name} списано: {amount.ToString()} грн.");
        }
        else
        {
            Notify?.Invoke($"Недостатньо коштів. Баланс: {Balance.ToString()} грн.");
        }
    }
}
```

Як обробники можна використовувати не лише іменовані методи, а й анонімні методи та лямбда-вирази:

```csharp run
using System;

Patient p = new Patient("Тетяна Руденко", 500);

// обробник через делегат
p.Notify += new Patient.PatientHandler(msg => Console.WriteLine($"[ДЕЛЕГАТ] {msg}"));
// обробник через анонімний метод
p.Notify += delegate(string msg) { Console.WriteLine($"[АНОНІМНИЙ] {msg}"); };
// обробник через лямбду
p.Notify += msg => Console.WriteLine($"[ЛЯМБДА] {msg}");

p.Spend(200);

class Patient
{
    public delegate void PatientHandler(string message);
    public event PatientHandler? Notify;
    public string Name { get; }
    public int Balance { get; private set; }
    public Patient(string name, int balance) { Name = name; Balance = balance; }
    public void Spend(int amount)
    {
        if (Balance >= amount) { Balance -= amount; Notify?.Invoke($"Списано: {amount.ToString()} грн."); }
        else Notify?.Invoke($"Недостатньо коштів. Баланс: {Balance.ToString()} грн.");
    }
}
```

## Управління обробниками (аксесори add/remove)

За допомогою спеціальних аксесорів `add` і `remove` можна керувати логікою підписки та відписки. Це корисно тоді, коли потрібно, наприклад, записати у лог хто підписався, або обмежити кількість обробників:

```csharp run
using System;

Patient p = new Patient("Василь Мороз", 600);

p.Notify += DisplayMessage;
p.Spend(100);
p.Notify -= DisplayMessage;
p.Spend(50);

void DisplayMessage(string message) => Console.WriteLine(message);

class Patient
{
    public delegate void PatientHandler(string message);

    PatientHandler? _notify;        // приватна змінна делегата

    public event PatientHandler Notify
    {
        add
        {
            _notify += value;
            Console.WriteLine($"[ПІДПИСКА] Обробник '{value.Method.Name}' зареєстровано");
        }
        remove
        {
            _notify -= value;
            Console.WriteLine($"[ВІДПИСКА] Обробник '{value.Method.Name}' видалено");
        }
    }

    public string Name { get; }
    public int Balance { get; private set; }
    public Patient(string name, int balance) { Name = name; Balance = balance; }

    public void Spend(int amount)
    {
        if (Balance >= amount)
        {
            Balance -= amount;
            _notify?.Invoke($"З рахунку {Name} списано: {amount.ToString()} грн.");
        }
        else
        {
            _notify?.Invoke($"Недостатньо коштів. Баланс: {Balance.ToString()} грн.");
        }
    }
}
```

Визначення події тепер розбивається на дві частини. Спочатку оголошується приватна змінна делегата `_notify`, якою клас викликає обробники зсередини. Потім визначаються аксесори: `add` виконується при операції `+=`, а `remove` — при `-=`. Усередині аксесора обробник, що додається або видаляється, доступний через ключове слово `value`. Зовнішній код працює з `Notify` (публічна подія), але реальний список обробників зберігається у `_notify`.

![Подія vs делегат: ключові відмінності](_assets/06-03/event-vs-delegate.png)

## Передача даних події

Нерідко обробнику події потрібно отримати детальну інформацію про те, що саме сталося — не просто рядок, а структурований об'єкт з кількома полями. Для цього визначається спеціальний клас аргументів події. Додамо клас `PatientEventArgs`:

```csharp run
using System;

Patient p = new Patient("Надія Литвин", 700);
p.Notify += DisplayTransactionInfo;

p.AddFunds(150);
p.Spend(400);
p.Spend(600);

void DisplayTransactionInfo(Patient sender, PatientEventArgs e)
{
    Console.WriteLine($"Пацієнт: {sender.Name}");
    Console.WriteLine($"Операція: {e.Message}");
    Console.WriteLine($"Сума: {e.Amount.ToString()} грн. | Поточний баланс: {sender.Balance.ToString()} грн.");
    Console.WriteLine("---");
}

class PatientEventArgs
{
    public string Message { get; }
    public int Amount { get; }
    public PatientEventArgs(string message, int amount)
    {
        Message = message;
        Amount  = amount;
    }
}

class Patient
{
    public delegate void PatientHandler(Patient sender, PatientEventArgs e);
    public event PatientHandler? Notify;

    public string Name { get; }
    public int Balance { get; private set; }

    public Patient(string name, int balance) { Name = name; Balance = balance; }

    public void AddFunds(int amount)
    {
        Balance += amount;
        Notify?.Invoke(this, new PatientEventArgs($"На рахунок зараховано {amount.ToString()} грн.", amount));
    }

    public void Spend(int amount)
    {
        if (Balance >= amount)
        {
            Balance -= amount;
            Notify?.Invoke(this, new PatientEventArgs($"Списано {amount.ToString()} грн. зі страхового рахунку", amount));
        }
        else
        {
            Notify?.Invoke(this, new PatientEventArgs("Недостатньо коштів на страховому рахунку", amount));
        }
    }
}
```

Делегат `PatientHandler` тепер приймає два параметри: перший — об'єкт `Patient`, що є джерелом події (відправник), другий — `PatientEventArgs` із деталями операції. Перший параметр `this` передає посилання на сам об'єкт `Patient`, тому обробник може звернутися до будь-якого стану пацієнта — наприклад, прочитати поточний баланс. Другий параметр містить повідомлення і суму операції.

Такий патерн — `(sender, eventArgs)` — є стандартним у .NET і використовується у бібліотечних подіях: `Button.Click`, `Timer.Elapsed`, `HttpClient` — усі вони слідують цій же конвенції. У реальних проектах `PatientEventArgs` зазвичай успадковують від `System.EventArgs`, а делегат замінюють вбудованим `EventHandler<T>`, що буде розглянуто пізніше.

## Антипатерн: витік пам'яті через незвільнені підписки

Підписка на подію через `+=` створює посилання від **видавця** (publisher) до **підписника** (subscriber). Якщо видавець — довготривалий об'єкт (наприклад, статичний клас або синглтон), а підписник — об'єкт із коротким циклом життя, сміттєзбирач (GC) **не зможе видалити** підписника, доки він залишається в списку обробників події.

Це — **витік пам'яті через події**: об'єкти, які мали б зібратися GC, залишаються живими через приховане посилання з події.

```csharp run
using System;

// Видавець — довгоживучий (симулюємо статичним полем)
var hospitalSystem = new HospitalMonitor();

Console.WriteLine("=== Реєструємо 3 монітори пацієнтів ===");
for (int i = 1; i <= 3; i++)
{
    var monitor = new PatientMonitor($"Monitor-{i}");
    monitor.Subscribe(hospitalSystem);
    // monitor виходить зі scope — але GC НЕ збере його!
}

GC.Collect();
GC.WaitForPendingFinalizers();

Console.WriteLine($"\nПісля GC.Collect() — живих підписників: {hospitalSystem.SubscriberCount}");
Console.WriteLine("(Очікували 0, але всі 3 залишились — витік пам'яті!)");

Console.WriteLine("\n=== Сигнал тривоги — усі підписники ще реагують ===");
hospitalSystem.RaiseAlert("Критичний показник у палаті 5");

// Клас без відписки — витік пам'яті
class PatientMonitor
{
    public string Name { get; }
    public PatientMonitor(string name) { Name = name; Console.WriteLine($"[{name}] Створено"); }
    
    public void Subscribe(HospitalMonitor monitor) =>
        monitor.AlertRaised += OnAlert; // підписуємось, але ніколи не відписуємось!
    
    void OnAlert(string message) =>
        Console.WriteLine($"  [{Name}] Отримав сигнал: {message}");
    
    ~PatientMonitor() => Console.WriteLine($"[{Name}] Фіналізовано (GC зібрав)");
}

class HospitalMonitor
{
    private event Action<string>? _alertRaised;
    
    public event Action<string> AlertRaised
    {
        add    { _alertRaised += value; }
        remove { _alertRaised -= value; }
    }
    
    public int SubscriberCount =>
        _alertRaised?.GetInvocationList().Length ?? 0;
    
    public void RaiseAlert(string message) => _alertRaised?.Invoke(message);
}
```

```csharp run
using System;

// Правильний патерн: завжди відписуватися або реалізовувати IDisposable
var hospitalSystem = new HospitalMonitor();

Console.WriteLine("=== Правильно: відписка через IDisposable ===");
var monitor1 = new PatientMonitorSafe("Monitor-1", hospitalSystem);
var monitor2 = new PatientMonitorSafe("Monitor-2", hospitalSystem);

Console.WriteLine($"Підписників: {hospitalSystem.SubscriberCount}"); // 2

hospitalSystem.RaiseAlert("Тест");

monitor1.Dispose(); // відписка
Console.WriteLine($"\nПісля monitor1.Dispose(): {hospitalSystem.SubscriberCount} підписник");

monitor2.Dispose();
Console.WriteLine($"Після monitor2.Dispose(): {hospitalSystem.SubscriberCount} підписників");

GC.Collect();
GC.WaitForPendingFinalizers();
Console.WriteLine("GC не має що збирати — об'єкти коректно звільнені");

// Правильний клас: реалізує IDisposable для відписки
class PatientMonitorSafe : IDisposable
{
    private readonly HospitalMonitor _source;
    public string Name { get; }
    
    public PatientMonitorSafe(string name, HospitalMonitor source)
    {
        Name = name;
        _source = source;
        _source.AlertRaised += OnAlert; // підписуємось
        Console.WriteLine($"[{name}] Підписано");
    }
    
    void OnAlert(string message) =>
        Console.WriteLine($"  [{Name}] Сигнал: {message}");
    
    public void Dispose()
    {
        _source.AlertRaised -= OnAlert; // ОБОВ'ЯЗКОВО відписуємось
        Console.WriteLine($"[{Name}] Відписано");
    }
    
    ~PatientMonitorSafe() => Console.WriteLine($"[{Name}] GC зібрав");
}

class HospitalMonitor
{
    private event Action<string>? _alertRaised;
    public event Action<string> AlertRaised
    {
        add    { _alertRaised += value; }
        remove { _alertRaised -= value; }
    }
    public int SubscriberCount => _alertRaised?.GetInvocationList().Length ?? 0;
    public void RaiseAlert(string message) => _alertRaised?.Invoke(message);
}
```

**Правила безпечної роботи з подіями:**

| Сценарій | Рекомендація |
|----------|-------------|
| Підписник живе стільки ж, скільки видавець | Відписка необов'язкова, але бажана для ясності |
| Підписник має коротший цикл життя | Реалізуйте `IDisposable`, відписуйтесь у `Dispose()` |
| Підписка через лямбду | Збережіть лямбду у поле, щоб можна було передати в `-=` |
| Відписатися від усіх одразу | У класі-видавці зробіть метод `ClearSubscriptions()` |

Правило просте: **кожному `+=` має відповідати `-=`** у відповідному місці (Dispose, Close, деструктор або явна очистка).
