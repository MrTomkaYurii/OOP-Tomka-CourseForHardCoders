---
chapter: 15
chapterTitle: "Розділ 15. Багатопоточність"
section: 3
number: "15.3"
title: "Синхронізація потоків. Оператор lock та клас Lock"
source: ""
---

## 15.3. Синхронізація потоків. Оператор lock та клас Lock

Коли кілька потоків одночасно звертаються до спільних даних — читають, модифікують, записують — виникає фундаментальна проблема: **стан перегонів** (race condition). Це ситуація, коли результат виконання програми залежить від непередбачуваного порядку, у якому потоки отримують процесорний час. Стан перегонів є однією з найнебезпечніших помилок у паралельному програмуванні: він не відтворюється стабільно, рідко з'являється на стадії тестування і може призвести до пошкодження даних у виробничій системі.

## Демонстрація стану перегонів

Розглянемо класичну проблему: кілька потоків одночасно оновлюють лічильник пацієнтів у черзі:

```csharp run
using System;
using System.Threading;

int queueCount = 0; // спільний лічильник

Thread[] threads = new Thread[5];
for (int i = 0; i < 5; i++)
{
    threads[i] = new Thread(() =>
    {
        for (int j = 0; j < 1000; j++)
        {
            queueCount++; // НЕ є атомарною операцією!
        }
    });
}

foreach (Thread t in threads) t.Start();
foreach (Thread t in threads) t.Join();

// Очікуємо 5000, але отримуємо менше через стан перегонів
Console.WriteLine($"Очікувано: 5000");
Console.WriteLine($"Фактично:  {queueCount.ToString()}");
Console.WriteLine($"Різниця:   {(5000 - queueCount).ToString()} — це втрачені оновлення!");
```

Результат виявиться меншим за 5000. Чому? Операція `queueCount++` виглядає як одна операція, але на рівні процесора це три кроки: **читання** поточного значення, **збільшення** на 1, **запис** нового значення. Якщо два потоки виконують ці кроки одночасно — вони обидва можуть прочитати однакове значення, обидва збільшать його і запишуть однаковий результат. У підсумку два приросту перетворюються на один — оновлення «загублено».

## Оператор lock

Найпростіший і найпоширеніший інструмент синхронізації в C# — оператор `lock`. Він гарантує, що в певний момент часу лише **один** потік може виконувати блок коду, що знаходиться під замком. Решта потоків, що намагаються увійти в цей блок, блокуються і очікують, поки замок не звільниться.

Синтаксис `lock`:

```csharp
lock (об'єкт-замок)
{
    // код, що захищається від паралельного доступу
}
```

Об'єктом-замком (`lockObject`) може бути будь-який **посилальний тип** (reference type) — будь-який клас або `object`. Важливо: це **не** `string` (рядкові літерали можуть інтернуватись і бути несподівано спільними) і не значущий тип (`int`, `struct`). Стандартна практика — окремий об'єкт-замок, оголошений як приватне статичне або поле екземпляра:

```csharp
private readonly object _lock = new object();
```

Виправимо приклад зі стані перегонів за допомогою `lock`:

```csharp run
using System;
using System.Threading;

int queueCount = 0;
object lockObj = new object(); // об'єкт-замок

Thread[] threads = new Thread[5];
for (int i = 0; i < 5; i++)
{
    threads[i] = new Thread(() =>
    {
        for (int j = 0; j < 1000; j++)
        {
            lock (lockObj) // лише один потік одночасно
            {
                queueCount++; // тепер безпечно
            }
        }
    });
}

foreach (Thread t in threads) t.Start();
foreach (Thread t in threads) t.Join();

Console.WriteLine($"Очікувано: 5000");
Console.WriteLine($"Фактично:  {queueCount.ToString()}");
Console.WriteLine($"Різниця:   {(5000 - queueCount).ToString()} — результат коректний!");
```

Тепер результат завжди точно 5000. `lock` є **взаємним виключенням** (mutual exclusion, mutex): поки один потік виконує захищений блок, всі інші чекають у черзі перед вхідними дверима. Коли потік виходить із `lock`-блоку, замок знімається і один з тих, що чекають, може увійти.

## Клінічний приклад: реєстратура

Розглянемо реалістичний клінічний сценарій: реєстратура з кількома операторами, що одночасно записують пацієнтів на прийом.

```csharp run
using System;
using System.Threading;

AppointmentScheduler scheduler = new AppointmentScheduler();

// Три оператори паралельно намагаються записати пацієнтів
string[][] operatorPatients =
{
    new[] { "Коваль М.", "Петренко І.", "Бойко О.", "Мороз В.", "Сидоренко Т.",
            "Руденко Н.", "Кравченко Р.", "Гриценко Л.", "Ткаченко А.", "Савченко Д." },
    new[] { "Бондаренко Є.", "Шевченко І.", "Яковенко В.", "Романенко О.", "Захаренко М.",
            "Лисенко Ю.", "Павленко С.", "Олійник В.", "Кириленко Т.", "Денисенко Н." },
    new[] { "Іваненко А.", "Сергієнко К.", "Тимошенко Б.", "Чорновіл Г.", "Гнатенко В." }
};

Thread[] operators = new Thread[3];
for (int i = 0; i < 3; i++)
{
    int idx = i; // копія для замикання
    operators[i] = new Thread(() =>
    {
        string opName = $"Реєстратор-{(idx + 1).ToString()}";
        foreach (string patient in operatorPatients[idx])
        {
            scheduler.TryBook(opName, patient);
            Thread.Sleep(20); // невелика затримка між записами
        }
    });
    operators[i].Name = $"Operator-{(i + 1).ToString()}";
}

foreach (Thread t in operators) t.Start();
foreach (Thread t in operators) t.Join();

Console.WriteLine($"\nПідсумок: записано {scheduler.Total.ToString()} пацієнтів із 20 доступних");

// Розклад лікаря — спільний ресурс для кількох операторів
class AppointmentScheduler
{
    private int _appointmentsToday = 0;
    private readonly int _maxPerDay = 20;
    private readonly object _lock = new object();

    // Повертає true, якщо запис вдався
    public bool TryBook(string operatorName, string patientName)
    {
        lock (_lock) // тільки один оператор одночасно може модифікувати розклад
        {
            if (_appointmentsToday >= _maxPerDay)
            {
                Console.WriteLine($"[{operatorName}] Відмова: {patientName} — розклад повний ({_maxPerDay.ToString()}/{_maxPerDay.ToString()})");
                return false;
            }

            _appointmentsToday++;
            Console.WriteLine($"[{operatorName}] Записано: {patientName} — прийом #{_appointmentsToday.ToString()}");
            return true;
        }
    }

    public int Total => _appointmentsToday;
}
```

Завдяки `lock` лічильник `_appointmentsToday` ніколи не перевищить `_maxPerDay`, і не виникне ситуації, коли два оператори «одночасно» запишуть 21-го пацієнта. Кожна перевірка-та-запис відбувається атомарно — без можливості втручання іншого потоку між читанням і записом.

## Клас Lock (.NET 9)

У .NET 9 з'явився новий клас `System.Threading.Lock` — спеціалізований тип замку, що замінює `lock (object)` і забезпечує кращу продуктивність та зручніший API. На відміну від загального `object`, `Lock` є явним інструментом синхронізації і не може бути випадково використаний не за призначенням.

Синтаксис залишається майже ідентичним:

```csharp
Lock lockObj = new Lock(); // спеціалізований тип

lock (lockObj) // працює так само
{
    // захищений код
}
```

Клас `Lock` також підтримує явний `Enter`/`Exit` через `using`-патерн:

```csharp run
using System;
using System.Threading;

Lock _lock = new Lock();
int _totalBeds = 50;
int _occupiedBeds = 0;

Thread admissions = new Thread(RunAdmissions);
Thread discharges  = new Thread(RunDischarges);

admissions.Name = "Admissions";
discharges.Name  = "Discharges";

admissions.Start();
discharges.Start();

admissions.Join();
discharges.Join();

Console.WriteLine($"Вільних ліжок: {(_totalBeds - _occupiedBeds).ToString()} з {_totalBeds.ToString()}");

void RunAdmissions()
{
    for (int i = 0; i < 10; i++)
    {
        using (_lock.EnterScope()) // Enter + Exit через using
        {
            if (_occupiedBeds < _totalBeds)
            {
                _occupiedBeds++;
                Console.WriteLine($"[{Thread.CurrentThread.Name}] Пацієнт госпіталізований. Зайнято: {_occupiedBeds.ToString()}");
            }
        }
        Thread.Sleep(30);
    }
}

void RunDischarges()
{
    Thread.Sleep(50); // небагато затримки, щоб були ліжка для виписки
    for (int i = 0; i < 5; i++)
    {
        using (_lock.EnterScope())
        {
            if (_occupiedBeds > 0)
            {
                _occupiedBeds--;
                Console.WriteLine($"[{Thread.CurrentThread.Name}] Пацієнта виписано. Зайнято: {_occupiedBeds.ToString()}");
            }
        }
        Thread.Sleep(60);
    }
}
```

`EnterScope()` повертає об'єкт, який при виклику `Dispose()` (що відбувається автоматично при виході з `using`-блоку) знімає замок. Це унеможливлює «забутий» `Exit()` і гарантує коректне звільнення навіть при виникненні винятку.

## Що НЕ варто робити з lock

**Не використовуйте `this` як об'єкт-замок.** Якщо зовнішній код також намагається заблокувати той самий об'єкт, це може призвести до непередбачуваної взаємодії:

```csharp
// Погано — this є публічно доступним:
lock (this) { ... }
```

**Не використовуйте `string` як об'єкт-замок.** Рядкові літерали в C# можуть інтернуватись — два різних `"lockKey"` у різних місцях коду можуть посилатись на той самий об'єкт. Це призведе до несподіваної конкуренції між непов'язаними блоками коду.

**Не виконуйте довгих операцій усередині `lock`.** Поки один потік виконує довгу операцію під замком (наприклад, запит до бази даних або зчитування файлу), всі інші потоки стоять і чекають. Розміщуйте під замком лише мінімально необхідний код — зазвичай це лише читання-модифікація-запис спільної змінної.

```csharp
// Погано: запит до бази всередині lock тримає замок на весь час запиту
lock (_lock)
{
    var result = database.Query("SELECT ...");
    _count = result.Count;
}

// Добре: запит виконується поза lock, під замком лише оновлення змінної
var result = database.Query("SELECT ...");
lock (_lock)
{
    _count = result.Count;
}
```

## Взаємне блокування (Deadlock)

Одна з найнебезпечніших пасток при роботі із замками — **взаємне блокування** (deadlock). Воно виникає, коли два або більше потоки блокують один одного: потік A тримає замок X і чекає на замок Y; потік B тримає замок Y і чекає на замок X. Жоден не може продовжити виконання — система «зависла».

```csharp
object lockA = new object();
object lockB = new object();

// Потік 1: блокує A, потім намагається заблокувати B
lock (lockA) { lock (lockB) { /* ... */ } }

// Потік 2: блокує B, потім намагається заблокувати A
lock (lockB) { lock (lockA) { /* ... */ } } // ← DEADLOCK
```

Основне правило запобігання дедлоку: **завжди захоплюйте кілька замків в одному й тому самому порядку** у всіх потоках. Якщо усі потоки завжди блокують A перед B — дедлок неможливий. Проектування системи синхронізації так, щоб замки захоплювались в єдиному передбаченому порядку, є важливим аспектом архітектури паралельних систем.

## Клас Interlocked — атомарні операції без lock

Для простих операцій над числами (збільшення, зменшення, додавання, обмін) використання `lock` є надмірним — воно дорожче через захоплення та звільнення монітора. Клас `System.Threading.Interlocked` надає **атомарні** методи, що виконуються процесором як одна неподільна операція без захоплення замку:

| Метод | Опис |
|-------|------|
| `Interlocked.Increment(ref n)` | Атомарний `n++` |
| `Interlocked.Decrement(ref n)` | Атомарний `n--` |
| `Interlocked.Add(ref n, value)` | Атомарний `n += value` |
| `Interlocked.Exchange(ref n, value)` | Атомарний `n = value`, повертає старе |
| `Interlocked.CompareExchange(ref n, value, comparand)` | Якщо `n == comparand`, то `n = value` |

```csharp run
using System;
using System.Threading;

// Лічильник записів пацієнтів — атомарні операції без lock
int appointmentCount = 0;
int cancelledCount   = 0;

Thread[] receptionists = new Thread[4];
for (int i = 0; i < 4; i++)
{
    receptionists[i] = new Thread(() =>
    {
        for (int j = 0; j < 250; j++)
        {
            Interlocked.Increment(ref appointmentCount); // атомарний ++
            
            if (j % 10 == 0) // кожен десятий скасовуємо
                Interlocked.Increment(ref cancelledCount);
        }
    });
}

foreach (Thread t in receptionists) t.Start();
foreach (Thread t in receptionists) t.Join();

int active = appointmentCount - cancelledCount;
Console.WriteLine($"Всього записів:    {appointmentCount}");   // завжди 1000
Console.WriteLine($"Скасовано:         {cancelledCount}");     // завжди 100
Console.WriteLine($"Активних записів:  {active}");             // завжди 900
```

`Interlocked.CompareExchange` — атомарна операція «порівняй і встанови» (CAS, Compare-And-Swap). Вона встановлює нове значення тільки якщо поточне дорівнює очікуваному. Це основа для lock-free алгоритмів:

```csharp run
using System;
using System.Threading;

int _status = 0; // 0 = вільно, 1 = зайнято

bool TryAcquire()
{
    // Атомарно: якщо _status == 0, встановити 1, повернути старе значення
    int previous = Interlocked.CompareExchange(ref _status, 1, 0);
    return previous == 0; // true якщо вдалось захопити (було 0)
}

void Release()
{
    Interlocked.Exchange(ref _status, 0); // атомарно скинути в 0
}

// Симуляція захоплення ресурсу (наприклад, апарату УЗД)
Thread[] technicians = new Thread[3];
for (int i = 0; i < 3; i++)
{
    int num = i + 1;
    technicians[i] = new Thread(() =>
    {
        if (TryAcquire())
        {
            Console.WriteLine($"Технік-{num}: УЗД-апарат захоплено, обстежую...");
            Thread.Sleep(100);
            Release();
            Console.WriteLine($"Технік-{num}: звільнив апарат");
        }
        else
        {
            Console.WriteLine($"Технік-{num}: апарат зайнятий, спробую пізніше");
        }
    });
}

foreach (Thread t in technicians) t.Start();
foreach (Thread t in technicians) t.Join();
```

Використовуйте `Interlocked` замість `lock` для **одиночних операцій над числовими змінними** — це швидше і не може призвести до дедлоку. Для складніших операцій (перевірка + зміна кількох змінних) все одно потрібен `lock`.

## volatile — видимість змін між потоками

Сучасні процесори та компілятори можуть **кешувати** значення змінних у регістрах або переставляти порядок операцій для оптимізації. Для однопоточного коду це безпечно, але в багатопоточному може призвести до того, що один потік не бачить зміни, зроблені іншим.

Ключове слово `volatile` повідомляє компілятору і JIT: **завжди читати/писати цю змінну безпосередньо з/до пам'яті**, без кешування у регістрах. Це гарантує **видимість** змін між потоками:

```csharp run
using System;
using System.Threading;

volatile bool _isRunning = true; // volatile гарантує видимість між потоками

Thread monitor = new Thread(() =>
{
    Console.WriteLine("[Monitor] Старт моніторингу пацієнта...");
    int ticks = 0;
    while (_isRunning) // без volatile: компілятор міг би кешувати _isRunning = true назавжди
    {
        ticks++;
        Thread.Sleep(50);
    }
    Console.WriteLine($"[Monitor] Зупинено після {ticks} тіків моніторингу");
});

monitor.Start();
Thread.Sleep(300);

Console.WriteLine("[Main] Зупиняємо моніторинг...");
_isRunning = false; // volatile гарантує, що Monitor-потік побачить зміну
monitor.Join();
Console.WriteLine("[Main] Моніторинг завершено");
```

`volatile` гарантує лише **видимість** — що зміна, зроблена одним потоком, буде прочитана іншим. Але не гарантує **атомарності**: `volatile int x; x++;` все ще є небезпечним, бо `++` — три кроки (читання, збільшення, запис). Для атомарних операцій над числами використовуйте `Interlocked`.

| Засіб | Гарантує | Вартість | Підходить для |
|-------|----------|----------|---------------|
| `volatile` | Видимість | Мінімальна | Прапорці `bool`, статуси — прості поля |
| `Interlocked` | Атомарність + видимість | Низька | Лічильники, стани — одиночні числові операції |
| `lock` | Атомарність + видимість + взаємне виключення | Помірна | Складні операції над кількома полями |
