---
chapter: 15
chapterTitle: "Розділ 15. Багатопоточність"
section: 1
number: "15.1"
title: "Введення у багатопоточність. Клас Thread"
source: ""
---

## 15.1. Введення у багатопоточність. Клас Thread

Сучасні програми рідко виконуються суворо послідовно: одна задача за одною. У реальних системах паралельно відбуваються десятки операцій — обробляються запити, зчитуються файли, надсилаються повідомлення, виконуються обчислення. Для ефективного управління такими сценаріями в .NET існує механізм **багатопоточності** — можливість виконувати кілька незалежних послідовностей інструкцій одночасно в межах одного процесу.

Щоб зрозуміти потоки, спочатку варто зрозуміти **процес**. Процес — це екземпляр запущеної програми: він отримує від операційної системи власну ізольовану область пам'яті, набір ресурсів і щонайменше один потік виконання. Потік (thread) — це найменша одиниця виконання всередині процесу. Кілька потоків одного процесу поділяють спільну пам'ять і ресурси процесу, але мають власні стек виклику і лічильник команд. Саме через спільну пам'ять потоки можуть ефективно обмінюватись даними, але саме через неї ж виникають проблеми синхронізації, з якими ми познайомимось у наступних розділах.

## Навіщо потрібна багатопоточність: клінічний сценарій

Уявіть реєстратуру медичного центру. При однопотоковій архітектурі все відбувалось би строго по черзі: спочатку зареєструвати пацієнта — потім роздрукувати направлення — потім надіслати SMS — потім завантажити медичну картку з бази даних. Поки база даних відповідає (це може зайняти сотні мілісекунд), програма стоїть і нічого не робить.

Реальна клінічна інформаційна система функціонує паралельно: реєстратура приймає нових пацієнтів, лабораторія обробляє зразки, черговий лікар опитує пацієнтів, система розсилає нагадування — все це одночасно. Саме таку модель і реалізує багатопоточність: замість одного виконавця з довгою чергою задач — кілька паралельних виконавців, кожен зі своїм потоком відповідальності.

Окрім відгуку та паралелізму, багатопоточність дає ще одну перевагу: **ефективне використання процесора**. Поки один потік чекає на відповідь від мережі або диску, інший може виконувати корисну роботу. На багатоядерних процесорах потоки можуть виконуватись дійсно одночасно на різних ядрах, а не лише чергуватись.

## Простір імен System.Threading

Усі класи для роботи з потоками у .NET зосереджені у просторі імен `System.Threading`. Перед тим як використовувати будь-який клас потоків, необхідно підключити цей простір імен:

```csharp
using System.Threading;
```

Основні типи, з якими ми працюватимемо у цьому розділі:

| Тип | Призначення |
|-----|-------------|
| `Thread` | Основний клас для створення та управління потоком |
| `ThreadStart` | Делегат — точка входу потоку без параметрів |
| `ParameterizedThreadStart` | Делегат — точка входу потоку з параметром `object?` |
| `ThreadPriority` | Перерахування пріоритетів потоку |
| `ThreadState` | Перерахування станів потоку |

## Клас Thread: властивості

Клас `Thread` — це центральний інструмент для роботи з потоками у .NET. Кожен запущений потік є об'єктом типу `Thread`. Щоб отримати посилання на поточний потік (той, у якому виконується код), використовується статична властивість `Thread.CurrentThread`:

```csharp run
using System;
using System.Threading;

// отримати інформацію про головний потік програми
Thread main = Thread.CurrentThread;
main.Name = "MainThread";

Console.WriteLine($"Назва потоку:       {main.Name}");
Console.WriteLine($"ID потоку:          {main.ManagedThreadId.ToString()}");
Console.WriteLine($"Стан потоку:        {main.ThreadState.ToString()}");
Console.WriteLine($"Фоновий потік:      {main.IsBackground.ToString()}");
Console.WriteLine($"Пріоритет:          {main.Priority.ToString()}");
Console.WriteLine($"Активний (живий):   {main.IsAlive.ToString()}");
```

Розглянемо ключові властивості класу `Thread`:

**`Name`** — текстова назва потоку. Може бути задана довільно, але лише один раз: після першого присвоєння змінити її неможливо (повторне присвоєння викличе виняток `InvalidOperationException`). Назва потоку незамінна при налагодженні: у стектрейсах і профайлерах вона дозволяє миттєво розпізнати, який потік що виконував.

**`ManagedThreadId`** — унікальний ціло­чисельний ідентифікатор потоку, що присвоюється середовищем виконання (CLR). На відміну від `Name`, він гарантовано унікальний і незмінний протягом усього часу життя потоку. Корисний для логування і діагностики.

**`IsAlive`** — повертає `true`, якщо потік ще виконується (не завершений і не відмінений). Дозволяє перевіряти, чи потік ще активний, не блокуючись у очікуванні.

**`IsBackground`** — вказує, чи є потік фоновим. Це ключова властивість, що визначає поведінку при завершенні програми — детально розглянемо нижче.

**`Priority`** — задає відносний пріоритет потоку через перерахування `ThreadPriority`. Детально розглянемо нижче.

**`ThreadState`** — поточний стан потоку з перерахування `ThreadState`. Відображає, чи потік запущений, чи очікує, чи завершений.

## Стани потоку

Протягом свого існування потік проходить через кілька станів, описаних у перерахуванні `ThreadState`. Розуміння цих станів необхідне для правильного управління потоками:

- **`Unstarted`** — потік створений об'єктом `new Thread(...)`, але метод `Start()` ще не викликаний. Потік існує як об'єкт, але ще не виконується.
- **`Running`** — потік виконується або готовий до виконання (чекає виділення процесорного часу планувальником ОС).
- **`WaitSleepJoin`** — потік призупинений: або через `Thread.Sleep()` (чекає певний час), або через `Monitor.Wait()` / `Join()` (чекає на інший потік чи подію).
- **`Stopped`** — потік завершив виконання або був відмінений. Повторний запуск неможливий.
- **`Background`** — прапорець, що вказує на фоновий режим потоку. Може поєднуватись з іншими станами.

![Стани потоку та переходи між ними](_assets/15-01/thread-lifecycle.png)

## Методи класу Thread

### Start — запуск потоку

Метод `Start()` переводить потік зі стану `Unstarted` у стан `Running`. Після виклику `Start()` планувальник операційної системи вирішує, коли саме виділити процесорний час цьому потоку — не обов'язково миттєво. Порядок виконання потоків не гарантується: кожен запуск програми може давати різну послідовність.

```csharp run
using System;
using System.Threading;

// Створення і запуск потоку для фонової реєстрації пацієнта
Thread registrationThread = new Thread(RegisterPatient);
registrationThread.Name = "RegistrationWorker";
registrationThread.Start();

// Головний потік продовжує роботу паралельно
Console.WriteLine($"[{Thread.CurrentThread.Name ?? "Main"}] Головний потік: система готова до роботи");

void RegisterPatient()
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Початок реєстрації пацієнта...");
    Thread.Sleep(100); // імітуємо роботу з базою даних
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Пацієнта зареєстровано успішно");
}
```

### Sleep — призупинення потоку

Метод `Thread.Sleep(milliseconds)` призупиняє поточний потік на вказану кількість мілісекунд, переводячи його у стан `WaitSleepJoin`. Поки потік «спить», планувальник ОС може виділяти процесорний час іншим потокам. `Thread.Sleep(0)` — особливий випадок: він не зупиняє потік, а лише повідомляє планувальнику, що поточний потік готовий поступитись своїм квантом часу.

`Sleep` широко використовується для:
- Імітації тривалих операцій у прикладах та тестах
- Реалізації простих таймерів і повторних спроб (retry logic)
- Зменшення навантаження від активного очікування (busy-wait)

```csharp run
using System;
using System.Threading;

Console.WriteLine("Система моніторингу запущена");

// Потік, що імітує циклічний моніторинг показників
Thread monitorThread = new Thread(MonitorVitals);
monitorThread.Name = "VitalsMonitor";
monitorThread.IsBackground = true; // фоновий — завершиться разом з програмою
monitorThread.Start();

Thread.Sleep(350); // дати монітору попрацювати 350 мс
Console.WriteLine("Сеанс моніторингу завершено");

void MonitorVitals()
{
    for (int i = 1; i <= 5; i++)
    {
        Console.WriteLine($"[{Thread.CurrentThread.Name}] Цикл {i.ToString()}: пульс 72 уд/хв, тиск 120/80");
        Thread.Sleep(100); // перевірка кожні 100 мс
    }
}
```

### Join — очікування завершення потоку

Метод `Join()` блокує викликаючий потік до завершення того потоку, на якому він викликаний. Це основний механізм синхронізації: головний потік може запустити кілька робочих потоків і потім зачекати на завершення всіх через `Join()`.

Існує перевантаження `Join(int milliseconds)`, яке очікує не довше зазначеної кількості мілісекунд і повертає `true`, якщо потік завершився, або `false`, якщо час вичерпано.

```csharp run
using System;
using System.Threading;

// Клінічний сценарій: паралельний збір аналізів, потім загальний звіт
Thread bloodTest  = new Thread(() => RunTest("Загальний аналіз крові",  400));
Thread urineTest  = new Thread(() => RunTest("Аналіз сечі",             250));
Thread ecgTest    = new Thread(() => RunTest("ЕКГ",                     300));

bloodTest.Name  = "BloodTest";
urineTest.Name  = "UrineTest";
ecgTest.Name    = "ECG";

Console.WriteLine("Відправка пацієнта на обстеження...");

bloodTest.Start();
urineTest.Start();
ecgTest.Start();

// Чекаємо завершення всіх трьох потоків
bloodTest.Join();
urineTest.Join();
ecgTest.Join();

// Цей рядок виконується лише після завершення всіх трьох
Console.WriteLine("Всі аналізи отримано. Формую загальний звіт...");
Console.WriteLine("Звіт готовий — направляю до лікаря.");

void RunTest(string testName, int durationMs)
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] → Початок: {testName}");
    Thread.Sleep(durationMs);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] ✓ Готово:  {testName}");
}
```

Якби не було `Join()`, рядок «Всі аналізи отримано» міг би вивестись ще до того, як всі потоки закінчили роботу. `Join()` гарантує правильну послідовність: спочатку всі аналізи, потім звіт.

### Interrupt — переривання очікування

Метод `Interrupt()` викидає виняток `ThreadInterruptedException` у потоці, що знаходиться в стані `WaitSleepJoin`. Якщо потік не перебуває в цьому стані, виняток буде кинуто, як тільки потік у нього перейде. Це дозволяє «розбудити» заблокований потік і попросити його завершити роботу.

```csharp run
using System;
using System.Threading;

Thread monitorThread = new Thread(LongMonitoringSession);
monitorThread.Name = "LongMonitor";
monitorThread.IsBackground = true;
monitorThread.Start();

Thread.Sleep(250); // даємо поопрацювати 250 мс
Console.WriteLine("[Main] Надзвичайна ситуація — переривання моніторингу");
monitorThread.Interrupt(); // надсилаємо переривання
monitorThread.Join();       // чекаємо коректного завершення
Console.WriteLine("[Main] Моніторинг зупинено коректно");

void LongMonitoringSession()
{
    try
    {
        for (int i = 1; i <= 20; i++)
        {
            Console.WriteLine($"[{Thread.CurrentThread.Name}] Цикл моніторингу {i.ToString()}");
            Thread.Sleep(100); // тут може прилетіти ThreadInterruptedException
        }
    }
    catch (ThreadInterruptedException)
    {
        // Коректна реакція на переривання: зберегти стан, звільнити ресурси
        Console.WriteLine($"[{Thread.CurrentThread.Name}] Отримано сигнал переривання — завершую сеанс");
    }
}
```

## Передній та фоновий потоки

Один із найважливіших концептів управління потоками — розмежування між **переднім** (foreground) і **фоновим** (background) потоком. Ця відмінність визначає, як поведеться програма при завершенні.

Правило просте і критично важливе:

> **Процес .NET завершується, коли завершуються всі передні потоки.** Фонові потоки при цьому примусово зупиняються, незалежно від того, що вони виконують.

За замовчуванням кожен новий потік є **переднім** (`IsBackground = false`). Головний потік програми завжди є переднім і не може стати фоновим.

Щоб зробити потік фоновим, необхідно встановити `IsBackground = true` **до** виклику `Start()`:

```csharp run
using System;
using System.Threading;

// Передній потік — програма чекатиме його завершення
Thread foregroundWorker = new Thread(SendReports);
foregroundWorker.Name = "ReportSender";
foregroundWorker.IsBackground = false; // значення за замовчуванням

// Фоновий потік — буде зупинений при завершенні головного потоку
Thread backgroundMonitor = new Thread(ContinuousMonitor);
backgroundMonitor.Name = "BackgroundMonitor";
backgroundMonitor.IsBackground = true; // фоновий!

foregroundWorker.Start();
backgroundMonitor.Start();

Console.WriteLine("[Main] Головний потік завершує роботу");
// Програма НЕ завершиться, поки foregroundWorker не закінчить
// backgroundMonitor буде зупинений примусово після foregroundWorker

void SendReports()
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Надсилаю звіти... (передній потік)");
    Thread.Sleep(300);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Звіти надіслано — передній потік завершено");
}

void ContinuousMonitor()
{
    int cycle = 0;
    while (true) // нескінченний цикл — зупиниться тільки примусово
    {
        cycle++;
        Console.WriteLine($"[{Thread.CurrentThread.Name}] Моніторинг, цикл {cycle.ToString()}");
        Thread.Sleep(80);
    }
}
```

![Передні та фонові потоки: порівняння поведінки](_assets/15-01/foreground-vs-background.png)

Практичне правило вибору типу потоку:

- **Передній потік** — для критично важливих операцій, які обов'язково мають завершитися: збереження даних, відправлення транзакцій, закриття з'єднань з базою даних. Якщо ця операція не завершиться — цілісність даних буде порушена.
- **Фоновий потік** — для сервісних операцій, які можна безпечно перервати: логування, кешування, моніторинг, виявлення нових файлів. Їх незавершення не призведе до втрати важливих даних.

## Пріоритет потоків

Пріоритет потоку (`Priority`) визначає, яку частину процесорного часу планувальник ОС виділяє потоку відносно інших. Задається через перерахування `ThreadPriority`:

| Значення | Числовий рівень | Клінічне застосування |
|----------|-----------------|----------------------|
| `Lowest` | 0 | Архівація старих записів, генерація звітів |
| `BelowNormal` | 1 | Фонова синхронізація даних |
| `Normal` | 2 | Стандартна обробка запитів *(за замовчуванням)* |
| `AboveNormal` | 3 | Реєстрація пацієнтів в режимі реального часу |
| `Highest` | 4 | Критичні сповіщення: аритмія, зупинка серця |

Пріоритет необхідно встановлювати **до** виклику `Start()`. Після запуску потоку змінити пріоритет технічно можливо, але це рідко доцільно.

```csharp run
using System;
using System.Threading;

// Потік критичних сповіщень — найвищий пріоритет
Thread alertThread = new Thread(SendCriticalAlert);
alertThread.Name = "CriticalAlert";
alertThread.Priority = ThreadPriority.Highest;

// Потік планових звітів — найнижчий пріоритет
Thread reportThread = new Thread(GenerateReport);
reportThread.Name = "ReportGenerator";
reportThread.Priority = ThreadPriority.Lowest;
reportThread.IsBackground = true;

// Звичайний потік реєстрації — стандартний пріоритет
Thread registrationThread = new Thread(ProcessRegistration);
registrationThread.Name = "Registration";
// Priority.Normal — значення за замовчуванням

alertThread.Start();
reportThread.Start();
registrationThread.Start();

alertThread.Join();
registrationThread.Join();

void SendCriticalAlert()
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] *** КРИТИЧНО: зупинка серця — бригада до палати 7! ***");
    Thread.Sleep(50);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Сповіщення доставлено всьому персоналу");
}

void ProcessRegistration()
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Реєстрація пацієнта Петренко О.В.");
    Thread.Sleep(200);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Пацієнта зареєстровано");
}

void GenerateReport()
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Генерація місячного звіту (фоновий, низький пріоритет)");
    Thread.Sleep(500);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Звіт сформовано");
}
```

Важливо розуміти: пріоритет потоку — це лише **підказка** операційній системі, а не жорстка гарантія. ОС може ігнорувати пріоритет або коригувати його динамічно для запобігання «голодуванню» (starvation) — ситуації, коли низькопріоритетний потік ніколи не отримує процесорного часу через постійно активні високопріоритетні потоки. На сучасних багатоядерних системах з невеликим навантаженням різниця між пріоритетами може бути непомітною — потоків вистачить на всіх.

## Повний клінічний приклад

Підсумкуємо все вивчене у комплексному прикладі: система первинного прийому пацієнта, де паралельно відбуваються кілька незалежних процесів.

```csharp run
using System;
using System.Threading;

// --- Запускаємо всі паралельні процеси ---
Thread vitalsThread    = CreateThread("VitalsCheck",    MeasureVitals,    ThreadPriority.AboveNormal, false);
Thread historyThread   = CreateThread("HistoryLoad",    LoadMedHistory,   ThreadPriority.Normal,      false);
Thread notifyThread    = CreateThread("NotifySender",   SendNotification, ThreadPriority.Normal,      false);
Thread archiveThread   = CreateThread("ArchiveWorker",  ArchiveOldData,   ThreadPriority.Lowest,      true); // фоновий

Console.WriteLine("[Прийом] Пацієнт Коваленко Н.В. — починаємо первинний прийом");
Console.WriteLine($"[Прийом] Головний потік ID: {Thread.CurrentThread.ManagedThreadId.ToString()}");
Console.WriteLine();

vitalsThread.Start();
historyThread.Start();
notifyThread.Start();
archiveThread.Start();

// Чекаємо обов'язкових процесів (передні потоки)
vitalsThread.Join();
historyThread.Join();
notifyThread.Join();

Console.WriteLine();
Console.WriteLine("[Прийом] Первинний прийом завершено. Перенаправляємо до лікаря.");
// archiveThread (фоновий) зупиниться автоматично

Thread CreateThread(string name, ThreadStart action, ThreadPriority priority, bool isBackground)
{
    Thread t = new Thread(action);
    t.Name         = name;
    t.Priority     = priority;
    t.IsBackground = isBackground;
    return t;
}

void MeasureVitals()
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Вимірювання показників...");
    Thread.Sleep(300);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Пульс: 78, АТ: 118/76, SpO2: 98% — норма");
}

void LoadMedHistory()
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Завантаження медичної карти...");
    Thread.Sleep(400);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Медична карта завантажена (3 попередніх звернення)");
}

void SendNotification()
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Надсилання SMS-підтвердження...");
    Thread.Sleep(150);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] SMS надіслано: 'Ви в черзі, орієнтовне очікування 15 хв'");
}

void ArchiveOldData()
{
    // Фоновий потік — може бути перерваний у будь-який момент
    for (int i = 1; i <= 10; i++)
    {
        Console.WriteLine($"[{Thread.CurrentThread.Name}] Архівація запису {i.ToString()}/10...");
        Thread.Sleep(200);
    }
}
```

У цьому прикладі три передні потоки (VitalsCheck, HistoryLoad, NotifySender) виконуються паралельно та незалежно. Головний потік чекає на всі три через `Join()`. Фоновий потік ArchiveWorker запущений одночасно, але програма не буде чекати його завершення — він зупиниться, коли завершаться всі передні потоки.
