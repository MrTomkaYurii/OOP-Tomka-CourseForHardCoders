---
chapter: 15
chapterTitle: "Розділ 15. Багатопоточність"
section: 7
number: "15.7"
title: "Клас Semaphore та SemaphoreSlim"
source: ""
---

## 15.7. Клас Semaphore та SemaphoreSlim

`Mutex` і `lock` реалізують принцип «один доступ одночасно»: лише один потік може захопити ресурс. Але що, якщо ресурс допускає **обмежений паралелізм**? Наприклад, в лікарні є 3 кабінети УЗД — одночасно можуть прийматися 3 пацієнти, але не 4 і не 10. Або апаратура може одночасно обслуговувати не більше 5 запитів.

Для таких сценаріїв призначений **семафор** (semaphore). Семафор — це лічильник доступів: він ініціалізується максимальним числом одночасних дозволів і видає їх потокам на вимогу. Потік, що хоче отримати доступ, «забирає» один дозвіл; якщо всі дозволи вичерпані — потік блокується до тих пір, поки якийсь інший потік не «поверне» свій дозвіл. Коли `Mutex` — це двері з одним місцем, семафор — це стоянка з N місцями.

## Semaphore і SemaphoreSlim

У .NET є два варіанти:

- **`Semaphore`** — об'єкт ядра ОС, як і `Mutex`. Може бути іменованим і доступним між процесами. Повільніший.
- **`SemaphoreSlim`** — легковаговий внутрішньопроцесний семафор. Набагато швидший, підтримує `async/await`. Є кращим вибором для переважної більшості задач.

| Характеристика | `Semaphore` | `SemaphoreSlim` |
|---------------|-------------|-----------------|
| Область дії | Процеси + міжпроцесна | Лише один процес |
| Продуктивність | Нижча (ОС-виклики) | Висока |
| `async`/`await` | Ні | Так (`WaitAsync`) |
| Іменований | Так | Ні |
| Типовий вибір | Міжпроцесне обмеження | Внутрішньопроцесний ліміт |

## API: SemaphoreSlim

| Метод / конструктор | Опис |
|---------------------|------|
| `new SemaphoreSlim(initialCount)` | Ліміт = `initialCount` = `initialCount` доступних дозволів |
| `new SemaphoreSlim(initialCount, maxCount)` | Початкова кількість і максимальна |
| `Wait()` | Забирає один дозвіл. Блокує, якщо лічильник = 0 |
| `Wait(int ms)` | З таймаутом. Повертає `bool` |
| `Release()` | Повертає один дозвіл (лічильник++) |
| `Release(int count)` | Повертає `count` дозволів відразу |
| `CurrentCount` | Кількість доступних дозволів |

## Клінічний приклад: кабінети УЗД

У медичному центрі є 3 апарати УЗД. Одночасно можуть проходити дослідження не більше трьох пацієнтів. Якщо всі три апарати зайняті — пацієнти чекають у черзі:

```csharp run
using System;
using System.Threading;

// 3 кабінети УЗД — не більше 3 одночасних досліджень
SemaphoreSlim usdRooms = new SemaphoreSlim(3, 3);

string[] patients =
{
    "Коваль М.",  "Петренко І.", "Бойко О.",
    "Мороз В.",   "Сидоренко Т.", "Руденко Н.",
    "Кравченко Р.", "Гриценко Л."
};

Thread[] threads = new Thread[patients.Length];

for (int i = 0; i < patients.Length; i++)
{
    string patient = patients[i];
    threads[i] = new Thread(() =>
    {
        Console.WriteLine($"[{patient}] Чекаю на вільний кабінет (доступно: {usdRooms.CurrentCount.ToString()})");

        usdRooms.Wait(); // займаємо один кабінет (або чекаємо)
        try
        {
            Console.WriteLine($"[{patient}] Займаю кабінет. Зайнято: {(3 - usdRooms.CurrentCount).ToString()}/3");
            Thread.Sleep(300); // УЗД-дослідження
            Console.WriteLine($"[{patient}] УЗД завершено, звільняю кабінет");
        }
        finally
        {
            usdRooms.Release(); // повертаємо дозвіл (звільняємо кабінет)
        }
    });
    threads[i].Name = $"Patient-{patient}";
}

foreach (Thread t in threads) t.Start();
foreach (Thread t in threads) t.Join();

Console.WriteLine($"\nВсіх пацієнтів обстежено. Вільних кабінетів: {usdRooms.CurrentCount.ToString()}/3");
```

Перші три пацієнти займуть кабінети і розпочнуть дослідження. Четвертий і наступні будуть чекати — `Wait()` заблокує їх до звільнення місця. Як тільки перший пацієнт викличе `Release()`, семафор підвищить лічильник і наступний очікуючий потік продовжить виконання.

`Release()` завжди розміщується у блоці `finally` — це гарантує звільнення дозволу навіть якщо у тілі потоку виник виняток.

## Контроль темпу: обмеження паралельних запитів

Семафор — природний інструмент обмеження навантаження (rate limiting). Наприклад, система відправки SMS-нагадувань не може надсилати більше 5 повідомлень одночасно через обмеження SMS-шлюзу:

```csharp run
using System;
using System.Threading;

// SMS-шлюз дозволяє не більше 5 паралельних запитів
SemaphoreSlim smsGateway = new SemaphoreSlim(5, 5);

string[] recipients =
{
    "+380501234001", "+380501234002", "+380501234003",
    "+380501234004", "+380501234005", "+380501234006",
    "+380501234007", "+380501234008", "+380501234009",
    "+380501234010", "+380501234011", "+380501234012"
};

Thread[] senders = new Thread[recipients.Length];

for (int i = 0; i < recipients.Length; i++)
{
    string phone = recipients[i];
    int msgNum = i + 1;
    senders[i] = new Thread(() =>
    {
        smsGateway.Wait(); // чекаємо вільного слота шлюзу
        try
        {
            Console.WriteLine($"[SMS #{msgNum.ToString()}] Відправляю на {phone}... (активних: {(5 - smsGateway.CurrentCount).ToString()}/5)");
            Thread.Sleep(200); // час відправки через шлюз
            Console.WriteLine($"[SMS #{msgNum.ToString()}] Доставлено → {phone}");
        }
        finally
        {
            smsGateway.Release(); // звільняємо слот
        }
    });
}

Console.WriteLine($"Розсилка нагадувань: {recipients.Length.ToString()} повідомлень через шлюз (ліміт 5)");
foreach (Thread t in senders) t.Start();
foreach (Thread t in senders) t.Join();
Console.WriteLine("Розсилку завершено");
```

## Клас Semaphore — іменований, міжпроцесний

`Semaphore` аналогічний `Mutex` у контексті міжпроцесного доступу. Його іменована версія дозволяє різним програмам обмежувати спільне використання системного ресурсу:

```csharp run
using System;
using System.Threading;

// Максимум 2 одночасних записи до журналу (між процесами)
const string SemName = "ClinicalAuditLog";

// У реальному сценарії: різні процеси або сервіси читають цю семафору
using Semaphore sem = new Semaphore(2, 2, SemName);

Thread[] writers = new Thread[5];
for (int i = 0; i < 5; i++)
{
    int id = i + 1;
    writers[i] = new Thread(() =>
    {
        Console.WriteLine($"[Writer-{id.ToString()}] Чекаю дозволу на запис...");
        sem.WaitOne();
        try
        {
            Console.WriteLine($"[Writer-{id.ToString()}] Пишу до журналу аудиту...");
            Thread.Sleep(200);
            Console.WriteLine($"[Writer-{id.ToString()}] Запис завершено");
        }
        finally
        {
            sem.Release();
        }
    });
}

foreach (Thread t in writers) t.Start();
foreach (Thread t in writers) t.Join();
```

## Release з кількома дозволами

`SemaphoreSlim.Release(int count)` дозволяє повернути кілька дозволів за раз. Це корисно, коли один «виробник» генерує пакет завдань і хоче одразу дозволити кільком споживачам почати роботу:

```csharp run
using System;
using System.Threading;

SemaphoreSlim batchSem = new SemaphoreSlim(0, 10); // 0 початково — ніхто не пройде

Thread[] workers = new Thread[5];
for (int i = 0; i < 5; i++)
{
    int id = i + 1;
    workers[i] = new Thread(() =>
    {
        Console.WriteLine($"[Лаборант-{id.ToString()}] Очікую партію зразків...");
        batchSem.Wait(); // чекаємо надходження зразків
        Console.WriteLine($"[Лаборант-{id.ToString()}] Отримав зразок, починаю аналіз");
        Thread.Sleep(150);
        Console.WriteLine($"[Лаборант-{id.ToString()}] Аналіз завершено");
    });
    workers[i].Name = $"Lab-{id}";
}

foreach (Thread t in workers) t.Start();

Thread.Sleep(200); // готуємо партію

Console.WriteLine("[Прийом] Надійшла партія з 5 зразків — дозволяю всім лаборантам");
batchSem.Release(5); // одночасно розблокуємо 5 потоків

foreach (Thread t in workers) t.Join();
Console.WriteLine("Партію оброблено");
```

Ініціалізація `SemaphoreSlim(0, 10)` означає: початково 0 дозволів (всі потоки зупиняться на `Wait`), максимум 10. Після `Release(5)` лічильник стає 5, і всі 5 очікуючих потоків одночасно пробуджуються.

## Загальна картина: коли який примітив обирати

Завершимо розділ зведеною таблицею всіх вивчених примітивів синхронізації:

| Примітив | Максимум потоків | Між процесами | Основний сценарій |
|----------|-----------------|---------------|-------------------|
| `lock` | 1 | Ні | Захист критичної секції (найчастіший вибір) |
| `Lock` (.NET 9) | 1 | Ні | Як `lock`, з кращою продуктивністю |
| `Monitor` | 1 | Ні | `Wait`/`Pulse` для координації виробника і споживача |
| `AutoResetEvent` | 1 (по черзі) | Ні | Сигналізація одному потоку про готовність даних |
| `Mutex` | 1 | **Так** | Singleton-процес, захист системного файлу |
| `Semaphore` | N | **Так** | Обмеження доступу до N ресурсів між процесами |
| `SemaphoreSlim` | N | Ні | Обмеження паралелізму всередині програми |

Вибір примітива визначається трьома запитаннями:
1. **Скільки потоків** одночасно мають доступ до ресурсу — один або N?
2. **Потрібна міжпроцесна** синхронізація чи лише внутрішньопроцесна?
3. **Потрібна сигналізація** (один потік чекає на подію від іншого) чи лише взаємне виключення?

Для переважної більшості задач — `lock` і `SemaphoreSlim` покривають 90% потреб. `Monitor` — коли потрібна тонка координація через `Wait/Pulse`. `AutoResetEvent` — для явного сигналювання між потоками. `Mutex` і `Semaphore` — лише коли є реальна потреба у міжпроцесній синхронізації.
