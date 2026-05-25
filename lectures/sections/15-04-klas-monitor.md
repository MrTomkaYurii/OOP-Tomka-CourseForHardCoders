---
chapter: 15
chapterTitle: "Розділ 15. Багатопоточність"
section: 4
number: "15.4"
title: "Клас Monitor"
source: ""
---

## 15.4. Клас Monitor

Оператор `lock` — це зручна синтаксична обгортка над класом `System.Threading.Monitor`. Кожен `lock`-блок компілятор перетворює на виклики `Monitor.Enter()` і `Monitor.Exit()` у блоці `try/finally`. Тобто коли ви пишете:

```csharp
lock (lockObj)
{
    // код
}
```

Компілятор генерує приблизно таке:

```csharp
bool lockTaken = false;
try
{
    Monitor.Enter(lockObj, ref lockTaken);
    // код
}
finally
{
    if (lockTaken) Monitor.Exit(lockObj);
}
```

`Monitor` надає більш низькорівневий і гнучкий API, ніж `lock`. Його ключова перевага — можливість **очікування та сигналізації**: потік може добровільно звільнити замок і перейти в режим очікування, а інший потік може «розбудити» його, коли настане відповідний момент. Саме ця можливість дозволяє реалізовувати складні патерни координації між потоками — наприклад, «виробник — споживач».

## Методи Monitor

Ключові методи класу `Monitor`:

| Метод | Опис |
|-------|------|
| `Monitor.Enter(obj)` | Захоплює замок на об'єкті `obj`. Блокує потік, якщо замок зайнятий |
| `Monitor.Exit(obj)` | Звільняє замок. Викликати лише у потоці, що тримає замок |
| `Monitor.TryEnter(obj)` | Спроба захопити замок без блокування. Повертає `bool` |
| `Monitor.TryEnter(obj, ms)` | Спроба захопити замок із таймаутом `ms` мілісекунд |
| `Monitor.Wait(obj)` | Звільняє замок і блокує поточний потік до сигналу `Pulse/PulseAll`. Замок автоматично повертається при пробудженні |
| `Monitor.Pulse(obj)` | Сповіщає один потік, що очікує через `Wait`, про можливість продовження |
| `Monitor.PulseAll(obj)` | Сповіщає **всі** потоки, що очікують через `Wait` |

Методи `Wait`, `Pulse` і `PulseAll` можуть викликатись **лише у потоці, що тримає замок** — тобто всередині `lock`-блоку або між `Enter()` і `Exit()`. Порушення цієї умови призведе до `SynchronizationLockException`.

## Monitor.Wait і Monitor.Pulse: механізм координації

`Monitor.Wait(obj)` виконує три дії атомарно:
1. Звільняє замок на `obj`
2. Переводить поточний потік у список очікування для `obj`
3. Блокує поточний потік

Коли інший потік викликає `Monitor.Pulse(obj)`, один потік з цього списку отримує сигнал і може відновити виконання — але спочатку він зобов'язаний знову захопити замок (що відбувається автоматично при виході з `Wait`).

Ця схема є основою класичного патерну «виробник — споживач»: виробник додає дані до черги і сповіщає споживача через `Pulse`; споживач чекає через `Wait`, доки черга не буде заповнена.

## Клінічний приклад: черга лабораторних зразків

У клінічній лабораторії зразки надходять від медсестер (виробники) і обробляються лаборантами (споживачі). Черга зразків — це спільний ресурс, доступ до якого потрібно синхронізувати.

```csharp run
using System;
using System.Collections.Generic;
using System.Threading;

// Черга лабораторних зразків — спільний ресурс
class LabQueue
{
    private readonly Queue<string> _samples = new Queue<string>();
    private readonly object _lock = new object();
    private bool _accepting = true; // false = нові зразки більше не надходять

    // Медсестра додає зразок до черги
    public void AddSample(string sample)
    {
        lock (_lock)
        {
            _samples.Enqueue(sample);
            Console.WriteLine($"[Надходження] Зразок '{sample}' додано до черги (черга: {_samples.Count.ToString()})");
            Monitor.Pulse(_lock); // сповіщаємо лаборанта, що є новий зразок
        }
    }

    // Оголошуємо, що нових зразків більше не буде
    public void StopAccepting()
    {
        lock (_lock)
        {
            _accepting = false;
            Monitor.PulseAll(_lock); // розбуджуємо всіх, хто чекає — вони перевірять умову
        }
    }

    // Лаборант бере наступний зразок для обробки
    // Повертає null, якщо черга закрита і порожня
    public string? TakeSample()
    {
        lock (_lock)
        {
            // Очікуємо, поки черга стане непорожньою або прийом не зупинять
            while (_samples.Count == 0 && _accepting)
            {
                Monitor.Wait(_lock); // звільняємо замок і чекаємо
            }

            if (_samples.Count > 0)
                return _samples.Dequeue();

            return null; // черга порожня і прийом зупинено
        }
    }
}

LabQueue queue = new LabQueue();

// Лаборант — споживач (запускаємо першим, він чекатиме на зразки)
Thread labWorker = new Thread(() =>
{
    Console.WriteLine("[Лаборант] Готовий до роботи, очікую зразки...");
    while (true)
    {
        string? sample = queue.TakeSample();
        if (sample == null) break; // черга закрита і порожня — виходимо

        Console.WriteLine($"[Лаборант] Обробляю: '{sample}'");
        Thread.Sleep(150); // час аналізу
        Console.WriteLine($"[Лаборант] Аналіз '{sample}' завершено");
    }
    Console.WriteLine("[Лаборант] Робочий день завершено — всі зразки оброблено");
});
labWorker.Name = "LabWorker";
labWorker.Start();

// Медсестра — виробник
Thread nurse = new Thread(() =>
{
    string[] samples = { "Кров-Коваль", "Сеча-Петренко", "Кров-Бойко", "Мокрота-Мороз", "Кров-Сидоренко" };
    foreach (string sample in samples)
    {
        Thread.Sleep(100); // час між надходженнями зразків
        queue.AddSample(sample);
    }
    Console.WriteLine("[Медсестра] Всі зразки здано до лабораторії");
    queue.StopAccepting(); // сигналізуємо, що нових зразків не буде
});
nurse.Name = "Nurse";
nurse.Start();

nurse.Join();
labWorker.Join();
Console.WriteLine("\n=== Лабораторія закрита ===");
```

Зверніть на конструкцію `while (_samples.Count == 0 && _accepting) { Monitor.Wait(_lock); }`. Умова перевіряється у **циклі**, а не в `if` — це критично важливо. `Pulse` не гарантує, що після пробудження умова дійсно виконана: можливе так зване «хибне пробудження» (spurious wakeup), або інший потік міг встигнути забрати зразок до того, як поточний захопив замок. Тому завжди перевіряємо умову заново після `Wait`.

## Кілька споживачів з PulseAll

`Monitor.Pulse` сповіщає лише один потік; `Monitor.PulseAll` — всі. Якщо є кілька лаборантів, при додаванні партії зразків доцільно розбудити всіх одразу — хай кожен забере по одному:

```csharp run
using System;
using System.Collections.Generic;
using System.Threading;

class MultiWorkerQueue
{
    private readonly Queue<string> _items = new Queue<string>();
    private readonly object _lock = new object();
    private bool _running = true;

    public void Produce(string item)
    {
        lock (_lock)
        {
            _items.Enqueue(item);
            Monitor.PulseAll(_lock); // розбуджуємо всіх лаборантів
        }
    }

    public void Stop()
    {
        lock (_lock)
        {
            _running = false;
            Monitor.PulseAll(_lock);
        }
    }

    public string? Consume(string workerName)
    {
        lock (_lock)
        {
            while (_items.Count == 0 && _running)
                Monitor.Wait(_lock);

            if (_items.Count > 0)
            {
                string item = _items.Dequeue();
                Console.WriteLine($"[{workerName}] Взяв зразок: {item}");
                return item;
            }
            return null;
        }
    }
}

MultiWorkerQueue queue = new MultiWorkerQueue();

// Два лаборанти-споживачі
void RunWorker(string name)
{
    while (true)
    {
        string? item = queue.Consume(name);
        if (item == null) break;
        Thread.Sleep(200);
        Console.WriteLine($"[{name}] Аналіз '{item}' завершено");
    }
    Console.WriteLine($"[{name}] Зміна завершена");
}

Thread w1 = new Thread(() => RunWorker("Лаборант-1")) { Name = "Worker1" };
Thread w2 = new Thread(() => RunWorker("Лаборант-2")) { Name = "Worker2" };

w1.Start();
w2.Start();

// Виробник
Thread.Sleep(50);
string[] batch = { "Зразок-А", "Зразок-Б", "Зразок-В", "Зразок-Г", "Зразок-Д", "Зразок-Е" };
foreach (string s in batch)
{
    queue.Produce(s);
    Thread.Sleep(80);
}
queue.Stop();

w1.Join();
w2.Join();
Console.WriteLine("Всі аналізи завершено");
```

## Monitor.TryEnter — спроба без блокування

`Monitor.TryEnter(obj)` намагається захопити замок і повертає `true` або `false` негайно, без очікування. Це корисно, коли потік має корисну альтернативну роботу, якщо замок зайнятий:

```csharp run
using System;
using System.Threading;

object equipmentLock = new object();

// Потік-1: тривала діагностика апарату
Thread diagnosticThread = new Thread(() =>
{
    lock (equipmentLock)
    {
        Console.WriteLine("[Діагностика] Починаю діагностику МРТ (довга операція)...");
        Thread.Sleep(400);
        Console.WriteLine("[Діагностика] Діагностику завершено");
    }
});

// Потік-2: технік, що намагається отримати доступ
Thread techThread = new Thread(() =>
{
    Thread.Sleep(50); // даємо потоку-1 захопити замок

    bool acquired = Monitor.TryEnter(equipmentLock, 100); // чекаємо не більше 100 мс
    if (acquired)
    {
        try
        {
            Console.WriteLine("[Технік] Доступ отримано — проводжу технічне обслуговування");
            Thread.Sleep(100);
        }
        finally
        {
            Monitor.Exit(equipmentLock);
        }
    }
    else
    {
        // Замок зайнятий — виконуємо альтернативну задачу
        Console.WriteLine("[Технік] МРТ зайнятий. Займусь обслуговуванням рентгену");
    }
});

diagnosticThread.Start();
techThread.Start();

diagnosticThread.Join();
techThread.Join();
```

`TryEnter` є важливим інструментом для уникнення дедлоків: якщо ресурс недоступний, потік не «зависає» у вічному очікуванні, а може спробувати іншу стратегію.

## Monitor vs lock: коли що обирати

`lock` підходить для переважної більшості задач: захист критичної секції, яка виконується коротко і не потребує координації між потоками. `Monitor` обирають у таких ситуаціях:

- Потрібні `Wait`/`Pulse`/`PulseAll` для координації «виробник — споживач» або подібних патернів
- Потрібен `TryEnter` для спроби захоплення без блокування, зокрема з таймаутом
- Потрібен більш гранульований контроль над захопленням/звільненням замку

У всіх інших сценаріях — `lock` зрозуміліший, компактніший і менш схильний до помилок (наприклад, забутого `Monitor.Exit()`).
