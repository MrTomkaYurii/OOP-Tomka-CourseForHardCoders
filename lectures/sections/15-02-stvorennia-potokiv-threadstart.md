---
chapter: 15
chapterTitle: "Розділ 15. Багатопоточність"
section: 2
number: "15.2"
title: "Створення потоків. ThreadStart та ParameterizedThreadStart"
source: ""
---

## 15.2. Створення потоків. ThreadStart та ParameterizedThreadStart

Будь-який потік у .NET починається з делегата — посилання на метод, який потік виконуватиме. Конструктор класу `Thread` приймає делегат однієї з двох форм: `ThreadStart` або `ParameterizedThreadStart`. Розуміння відмінностей між ними та вміння обрати правильний підхід — основа грамотного використання багатопоточності.

## Делегат ThreadStart — потік без параметрів

`ThreadStart` — найпростіша форма: делегат без параметрів і без значення, що повертається:

```csharp
public delegate void ThreadStart();
```

Він описує метод, який отримує все необхідне зі свого лексичного оточення (замикання, поля класу, константи) або взагалі не потребує зовнішніх даних. Саме цей делегат підходить для ізольованих завдань, де потік є самодостатнім.

Є три способи передати метод у конструктор `Thread`: іменований метод, анонімний метод та лямбда-вираз.

### Іменований метод

```csharp run
using System;
using System.Threading;

// Класичний спосіб: передаємо ім'я методу
Thread t = new Thread(RunMorningRound);
t.Name = "MorningRound";
t.Start();
t.Join();

void RunMorningRound()
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Починаю ранковий обхід палат...");
    Thread.Sleep(200);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Обхід завершено: 12 пацієнтів, стан стабільний");
}
```

Іменований метод — найзрозуміліший варіант: логіку видно у декларації методу, а не в місці створення потоку. Підходить для складних, об'ємних задач.

### Анонімний метод

```csharp run
using System;
using System.Threading;

string ward = "Кардіологія";
int patientCount = 8;

// Анонімний метод захоплює ward і patientCount із зовнішньої області
Thread t = new Thread(delegate()
{
    Console.WriteLine($"[Обхід] Починаю обхід відділення '{ward}'");
    Thread.Sleep(150);
    Console.WriteLine($"[Обхід] Оглянуто {patientCount.ToString()} пацієнтів у '{ward}'");
});
t.Start();
t.Join();
```

Анонімний метод зручний, коли логіка проста і тісно пов'язана з контекстом. Він автоматично захоплює змінні зовнішньої функції (замикання).

### Лямбда-вираз

```csharp run
using System;
using System.Threading;

string ward = "Неврологія";

// Лямбда — найкомпактніший спосіб
Thread t = new Thread(() =>
{
    Console.WriteLine($"[Лямбда] Потік '{Thread.CurrentThread.Name}' обслуговує '{ward}'");
    Thread.Sleep(100);
    Console.WriteLine($"[Лямбда] Роботу завершено");
});
t.Name = "NeurologyWorker";
t.Start();
t.Join();
```

Лямбда-вираз є найпоширенішим сучасним підходом: компактна, читабельна, підтримує замикання. Для простих задач — оптимальний вибір.

## Делегат ParameterizedThreadStart — потік з параметром

`ParameterizedThreadStart` відрізняється від `ThreadStart` одним параметром типу `object?`:

```csharp
public delegate void ParameterizedThreadStart(object? obj);
```

Відповідно, метод `Thread.Start(object? parameter)` приймає значення, яке буде передане у тіло потоку. Це дозволяє передавати дані у потік у момент його запуску, не вдаючись до замикань чи спільних полів:

```csharp run
using System;
using System.Threading;

// Передаємо ім'я пацієнта як параметр
Thread t1 = new Thread(RegisterPatient);
Thread t2 = new Thread(RegisterPatient);

t1.Name = "RegWorker-1";
t2.Name = "RegWorker-2";

t1.Start("Олена Коваль");
t2.Start("Іван Петренко");

t1.Join();
t2.Join();

void RegisterPatient(object? param)
{
    // Обов'язково перевіряємо та приводимо тип
    string name = param as string ?? "Невідомий";
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Реєстрація: {name}");
    Thread.Sleep(200);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Пацієнта '{name}' зареєстровано");
}
```

Параметр завжди має тип `object?`, тому в тілі потоку його необхідно привести до потрібного типу. Якщо тип не збігається — `as` поверне `null`, що можна перевірити і обробити. Явне приведення через `(T)` кине `InvalidCastException` при невідповідності.

## Передача кількох значень через клас-обгортку

Найсуттєве обмеження `ParameterizedThreadStart` — лише один параметр типу `object?`. Якщо потоку потрібно передати кілька значень, їх пакують у клас або структуру:

```csharp run
using System;
using System.Threading;

Thread t1 = new Thread(ProcessAdmission);
Thread t2 = new Thread(ProcessAdmission);

t1.Name = "Admissions-1";
t2.Name = "Admissions-2";

t1.Start(new PatientTask("Марія Шевченко", "Терапія",    1));
t2.Start(new PatientTask("Олег Бондаренко", "Хірургія",  2));

t1.Join();
t2.Join();

void ProcessAdmission(object? param)
{
    if (param is not PatientTask task) return; // pattern matching — безпечне приведення

    Console.WriteLine($"[{Thread.CurrentThread.Name}] Прийом: {task.Name} → {task.Ward} (пріоритет {task.Priority.ToString()})");
    Thread.Sleep(200);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Завершено: {task.Name} оформлено до відділення '{task.Ward}'");
}

// Клас-обгортка для передачі кількох значень у потік
class PatientTask
{
    public string Name     { get; }
    public string Ward     { get; }
    public int    Priority { get; }

    public PatientTask(string name, string ward, int priority)
    {
        Name     = name;
        Ward     = ward;
        Priority = priority;
    }
}
```

Використання `is not PatientTask task` — це патерн-матчинг: якщо `param` не є `PatientTask`, умова спрацьовує і метод завершується. Це безпечніше і лаконічніше за явне приведення та перевірку на `null`.

## Замикання як альтернатива ParameterizedThreadStart

Коли потрібно передати дані в потік, замикання через лямбда-вираз часто зручніше за `ParameterizedThreadStart`. Лямбда захоплює змінні безпосередньо, без необхідності приведення типів:

```csharp run
using System;
using System.Threading;

string[] patients = { "Василь Мороз", "Тетяна Руденко", "Олена Сидоренко" };

Thread[] threads = new Thread[patients.Length];

for (int i = 0; i < patients.Length; i++)
{
    string patient = patients[i]; // важливо: копія для замикання, не сам i
    threads[i] = new Thread(() =>
    {
        Console.WriteLine($"[Worker] Обробка пацієнта: {patient}");
        Thread.Sleep(150);
        Console.WriteLine($"[Worker] Завершено: {patient}");
    });
    threads[i].Name = $"Worker-{(i + 1).ToString()}";
}

foreach (Thread t in threads) t.Start();
foreach (Thread t in threads) t.Join();

Console.WriteLine("Всіх пацієнтів оброблено");
```

Зверніть увагу на рядок `string patient = patients[i]`: ми копіюємо значення в окрему змінну перед тим, як лямбда її захопить. Це критично важливо. Якщо б лямбда захопила змінну `i` безпосередньо, всі потоки читали б одне й те саме значення `i` — те, яке воно буде в момент виконання лямбди, а не в момент її створення. Оскільки цикл завершується швидко, всі потоки могли б прочитати `i == 3` і звернутись до одного й того ж елемента масиву (або вийти за межі). Копія виправляє цю проблему.

## Порівняння підходів

Усі три підходи — іменований метод, `ParameterizedThreadStart` і лямбда з замиканням — вирішують одну задачу: зв'язати потік із кодом та даними. Вибір залежить від обсягу логіки та кількості параметрів:

| Підхід | Коли обирати |
|--------|-------------|
| Іменований метод + `ThreadStart` | Велика, самодостатня логіка потоку, що варта окремого методу |
| `ParameterizedThreadStart` | Один або кілька параметрів, що передаються у момент `Start()` |
| Лямбда з замиканням | Коротка логіка, що використовує змінні навколишнього контексту |

## Повний клінічний приклад: паралельна обробка черги

```csharp run
using System;
using System.Threading;

LabOrder[] orders =
{
    new LabOrder(1, "Коваль М.В.",    "Загальний аналіз крові",   300),
    new LabOrder(2, "Петренко І.О.",  "Біохімія крові",            450),
    new LabOrder(3, "Бойко О.П.",     "Аналіз сечі",              200),
    new LabOrder(4, "Мороз В.К.",     "Коагулограма",             380),
};

Thread[] workers = new Thread[orders.Length];

for (int i = 0; i < orders.Length; i++)
{
    LabOrder order = orders[i]; // захоплюємо копію для замикання
    workers[i] = new Thread(() => ProcessLabOrder(order));
    workers[i].Name = $"Lab-{order.OrderId.ToString()}";
}

Console.WriteLine("=== Лабораторія: запуск паралельної обробки ===");

foreach (Thread w in workers) w.Start();
foreach (Thread w in workers) w.Join();

Console.WriteLine("=== Всі аналізи оброблено. Результати готові до видачі. ===");

void ProcessLabOrder(LabOrder order)
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Початок: {order.PatientName} — {order.TestType}");
    Thread.Sleep(order.ProcessMs);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Готово:  {order.PatientName} — {order.TestType} ({order.ProcessMs.ToString()} мс)");
}

// Завдання для обробки в окремому потоці
class LabOrder
{
    public int    OrderId    { get; }
    public string PatientName { get; }
    public string TestType   { get; }
    public int    ProcessMs  { get; } // час обробки у мс

    public LabOrder(int id, string name, string test, int ms)
    {
        OrderId     = id;
        PatientName = name;
        TestType    = test;
        ProcessMs   = ms;
    }
}
```

Цей приклад демонструє реальну паралельну обробку: чотири лабораторні замовлення виконуються одночасно у чотирьох незалежних потоках. Без багатопоточності загальний час склав би суму всіх затримок (1330 мс); з багатопоточністю — лише час найдовшої операції (450 мс). Метод `Join()` у фінальному циклі гарантує, що рядок «Всі аналізи оброблено» з'явиться тільки після завершення всіх чотирьох потоків.
