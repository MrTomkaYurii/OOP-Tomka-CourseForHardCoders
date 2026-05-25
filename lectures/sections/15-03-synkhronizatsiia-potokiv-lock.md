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
