---
chapter: 15
chapterTitle: "Розділ 15. Багатопоточність"
section: 6
number: "15.6"
title: "Клас Mutex"
source: ""
---

## 15.6. Клас Mutex

`Mutex` (від англ. *mutual exclusion* — взаємне виключення) — примітив синхронізації, що схожий на `lock`, але має ключову відмінність: `Mutex` може працювати **між процесами**, а не лише між потоками одного процесу. Це робить його незамінним інструментом у ситуаціях, коли потрібно координувати доступ до ресурсу між кількома запущеними програмами.

Крім міжпроцесного режиму, `Mutex` підтримує і внутрішньопроцесну синхронізацію. Однак він суттєво повільніший за `lock`: внутрішньопроцесний `lock` — це операція на рівні CLR без звернень до ядра ОС; `Mutex` — це об'єкт операційної системи, і кожне захоплення/звільнення вимагає системного виклику. Тому для синхронізації потоків усередині одного процесу зазвичай краще обирати `lock`. `Mutex` обирають тоді, коли міжпроцесна синхронізація є вимогою.

## API класу Mutex

| Метод / конструктор | Опис |
|---------------------|------|
| `new Mutex()` | Локальний (внутрішньопроцесний) mutex, починає у вільному стані |
| `new Mutex(bool initiallyOwned)` | `true` — поточний потік одразу стає власником |
| `new Mutex(bool initiallyOwned, string name)` | Іменований (міжпроцесний) mutex. `name` — глобальна системна назва |
| `WaitOne()` | Захоплює mutex. Блокує, якщо зайнятий |
| `WaitOne(int ms)` | Захоплення з таймаутом. Повертає `bool` |
| `ReleaseMutex()` | Звільняє mutex. Лише потік-власник може це зробити |
| `Dispose()` | Звільняє системний ресурс |

Важлива особливість: mutex є **реентерабельним** (recursive). Якщо потік, що вже тримає mutex, знову викликає `WaitOne()`, він пройде без блокування. Але він зобов'язаний викликати `ReleaseMutex()` рівно стільки разів, скільки викликав `WaitOne()` — інакше mutex залишиться захопленим.

## Базовий приклад: захист спільного ресурсу

Спочатку розглянемо `Mutex` у ролі звичайного внутрішньопроцесного замку — для розуміння API:

```csharp run
using System;
using System.Threading;

Mutex mutex = new Mutex();
int _sharedLog = 0; // спільний лічильник записів у журналі

Thread[] nurses = new Thread[3];
for (int i = 0; i < 3; i++)
{
    int nurseId = i + 1;
    nurses[i] = new Thread(() =>
    {
        for (int j = 0; j < 5; j++)
        {
            mutex.WaitOne(); // захоплюємо mutex
            try
            {
                _sharedLog++;
                Console.WriteLine($"[Медсестра-{nurseId.ToString()}] Запис #{_sharedLog.ToString()} у журналі");
                Thread.Sleep(50);
            }
            finally
            {
                mutex.ReleaseMutex(); // завжди звільняємо у finally
            }

            Thread.Sleep(30);
        }
    });
    nurses[i].Name = $"Nurse-{nurseId}";
}

foreach (Thread t in nurses) t.Start();
foreach (Thread t in nurses) t.Join();

mutex.Dispose();
Console.WriteLine($"\nЗагалом записів у журналі: {_sharedLog.ToString()}");
```

Зверніть на паттерн `try/finally`: `ReleaseMutex()` розміщується у блоці `finally`, щоб гарантувати звільнення навіть при виникненні винятку. Якщо mutex не буде звільнений, всі інші потоки заблокуються назавжди.

## Іменований Mutex — захист між процесами

Головна сила `Mutex` — іменований варіант, що є спільним об'єктом ОС. Два процеси, що створюють `Mutex` з однаковим іменем, отримують посилання на той самий системний об'єкт:

```csharp run
using System;
using System.Threading;

// Один примірник програми захоплює mutex, другий — чекатиме або отримає відмову
const string MutexName = "Global\\ClinicalSystem_ReportGenerator";

bool createdNew;
using Mutex mutex = new Mutex(true, MutexName, out createdNew);

if (!createdNew)
{
    Console.WriteLine("Генератор звітів вже запущено в іншому процесі.");
    Console.WriteLine("Для безпеки даних дозволено лише один екземпляр.");
    return;
}

try
{
    // Лише один процес може дійти до цього місця
    Console.WriteLine("Генератор звітів запущено. Генерую місячний звіт...");
    Thread.Sleep(500);
    Console.WriteLine("Місячний звіт сформовано і збережено.");
}
finally
{
    mutex.ReleaseMutex(); // звільняємо при завершенні
}
```

Параметр `out createdNew` повертає `true`, якщо цей процес **створив** mutex (тобто є першим), або `false`, якщо mutex вже існував (інший процес вже запущений). Префікс `Global\\` означає, що mutex видимий для всіх сесій ОС; `Local\\` (або без префікса) — лише для поточної сесії.

Практичний сценарій: клінічна інформаційна система, де лише один запущений екземпляр може здійснювати запис до бази даних. Спроба запустити другий екземпляр завершиться повідомленням, а не пошкодженням даних.

## Тайм-аут очікування

`Mutex.WaitOne(ms)` дозволяє не блокуватись вічно:

```csharp run
using System;
using System.Threading;

Mutex equipmentMutex = new Mutex();

// Перший лікар захоплює апарат УЗД надовго
Thread doctor1 = new Thread(() =>
{
    equipmentMutex.WaitOne();
    try
    {
        Console.WriteLine("[Лікар-1] Використовую апарат УЗД (600 мс)...");
        Thread.Sleep(600);
        Console.WriteLine("[Лікар-1] Процедуру завершено, звільняю апарат");
    }
    finally
    {
        equipmentMutex.ReleaseMutex();
    }
});

// Другий лікар — намагається отримати апарат, але не готовий чекати більше 200 мс
Thread doctor2 = new Thread(() =>
{
    Thread.Sleep(50); // дати першому захопити mutex
    Console.WriteLine("[Лікар-2] Намагаюсь отримати апарат УЗД (чекаю до 200 мс)...");

    bool acquired = equipmentMutex.WaitOne(200);
    if (acquired)
    {
        try
        {
            Console.WriteLine("[Лікар-2] Апарат отримано! Проводжу діагностику.");
            Thread.Sleep(200);
        }
        finally
        {
            equipmentMutex.ReleaseMutex();
        }
    }
    else
    {
        Console.WriteLine("[Лікар-2] Апарат зайнятий. Записую пацієнта на завтра.");
    }
});

doctor1.Start();
doctor2.Start();

doctor1.Join();
doctor2.Join();
equipmentMutex.Dispose();
```

## AbandonedMutexException

Коли потік завершується, не звільнивши mutex, інші потоки, що чекають, отримають виняток `AbandonedMutexException`. Це захисний механізм: наступний потік-власник отримає сигнал, що попередній «впав» без коректного завершення, і може прийняти рішення щодо стану спільного ресурсу.

```csharp run
using System;
using System.Threading;

Mutex mutex = new Mutex();

// Потік, що «аварійно завершується» без звільнення mutex
Thread crashingThread = new Thread(() =>
{
    mutex.WaitOne();
    Console.WriteLine("[Аварійний потік] Захопив mutex і впав без звільнення!");
    // mutex.ReleaseMutex() не викликається — mutex залишиться «покинутим»
    throw new Exception("Симуляція аварійного завершення");
});

crashingThread.Start();
crashingThread.Join(); // ігноруємо виняток у потоці

// Наступний потік спробує отримати mutex
Thread nextThread = new Thread(() =>
{
    try
    {
        mutex.WaitOne(); // отримаємо AbandonedMutexException
        Console.WriteLine("[Наступний потік] Отримав mutex (попередній власник впав)");
        // Тут треба перевірити стан ресурсу — він може бути пошкоджений
        mutex.ReleaseMutex();
    }
    catch (AbandonedMutexException)
    {
        Console.WriteLine("[Наступний потік] Попередній власник mutex завершився аварійно!");
        Console.WriteLine("[Наступний потік] Перевіряю цілісність даних...");
        mutex.ReleaseMutex();
    }
});

nextThread.Start();
nextThread.Join();
mutex.Dispose();
```

## Mutex vs lock: підсумок

| Характеристика | `lock` | `Mutex` |
|---------------|--------|---------|
| Область дії | Потоки одного процесу | Потоки та **різні процеси** |
| Продуктивність | Дуже висока (без ОС-викликів) | Нижча (об'єкт ядра ОС) |
| Реентерабельність | Ні (нова спроба — дедлок) | Так (рекурсивне захоплення) |
| Таймаут очікування | Ні | `WaitOne(ms)` |
| `AbandonedMutexException` | Ні | Так |
| Типовий сценарій | Захист даних усередині програми | Singleton-процес, спільний файл |

Правило вибору: для синхронізації потоків усередині одного додатку — `lock`; якщо потрібна координація між кількома запущеними програмами або захист системного ресурсу — `Mutex`.
