---
chapter: 16
chapterTitle: "Розділ 16. Паралельне програмування та TPL"
section: 2
number: "16.2"
title: "Вкладені завдання та масиви завдань. Task<T>"
source: ""
---

## 16.2. Вкладені завдання та масиви завдань. Task\<T\>

Розглянемо можливості TPL, що дозволяють будувати складніші структури завдань: вкладені завдання, масиви завдань з колективним очікуванням і типізовані завдання, що повертають значення.

## Вкладені завдання

Завдання може запускати інше завдання зсередини свого тіла — таке завдання називається **вкладеним** (nested task). За замовчуванням вкладене завдання є **незалежним** від батьківського: батьківське завдання може завершитись раніше, ніж вкладене. Це може здивувати — інтуїтивно здається, що завдання повинно чекати на всі запущені ним задачі. Але TPL так не поводиться без явної вказівки.

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task outer = Task.Factory.StartNew(() =>
{
    Console.WriteLine($"[Outer {Task.CurrentId}] Початок: відкриваю прийом пацієнта");

    // вкладене завдання — незалежне за замовчуванням
    Task inner = Task.Factory.StartNew(() =>
    {
        Console.WriteLine($"[Inner {Task.CurrentId}] Запит до лабораторії відправлено");
        Thread.Sleep(500); // лабораторія довго обробляє
        Console.WriteLine($"[Inner {Task.CurrentId}] Лабораторія відповіла");
    });

    Console.WriteLine($"[Outer {Task.CurrentId}] Огляд лікаря завершено (не чекає лабораторії)");
    // Outer завершується — Inner ще виконується!
});

outer.Wait(); // чекаємо тільки outer
Console.WriteLine("[Main] Outer завершено. Inner може ще працювати!");
Thread.Sleep(600); // дамо inner доробити для демонстрації
Console.WriteLine("[Main] Програма завершується");
```

Поведінка «не чекати вкладеного» є навмисним рішенням дизайну: в більшості сценаріїв завдання запускають допоміжні підзавдання, за якими не потрібно стежити. Але якщо потрібно прив'язати вкладене завдання до батьківського, використовується `TaskCreationOptions.AttachedToParent`.

## AttachedToParent: дочірнє завдання

`TaskCreationOptions.AttachedToParent` перетворює вкладене завдання на **дочірнє** (child task). Батьківське завдання не може завершитись, доки не завершаться всі його дочірні завдання. Якщо дочірнє завдання кине виняток, він буде перекинутий через батьківське при виклику `Wait()`.

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task parent = Task.Factory.StartNew(() =>
{
    Console.WriteLine($"[Parent {Task.CurrentId}] Відкриваю комплексне обстеження");

    // дочірнє завдання — прив'язане до батька
    Task child1 = Task.Factory.StartNew(() =>
    {
        Console.WriteLine($"[Child {Task.CurrentId}] Аналіз крові...");
        Thread.Sleep(400);
        Console.WriteLine($"[Child {Task.CurrentId}] Аналіз крові готовий");
    }, TaskCreationOptions.AttachedToParent);

    Task child2 = Task.Factory.StartNew(() =>
    {
        Console.WriteLine($"[Child {Task.CurrentId}] ЕКГ-запис...");
        Thread.Sleep(300);
        Console.WriteLine($"[Child {Task.CurrentId}] ЕКГ готово");
    }, TaskCreationOptions.AttachedToParent);

    Console.WriteLine($"[Parent {Task.CurrentId}] Дочірні завдання запущені, чекаю їх завершення...");
    // Parent автоматично чекає child1 і child2
});

parent.Wait(); // чекає і parent, і всі його дочірні завдання
Console.WriteLine("[Main] Комплексне обстеження завершено — всі аналізи готові");
```

![Вкладені завдання: незалежні vs AttachedToParent](_assets/16-02/nested-tasks.png)

Практичне правило: якщо вкладені завдання є логічною частиною батьківської операції і їх результат потрібен для підтвердження завершення батька — використовуйте `AttachedToParent`. Якщо вкладені завдання є допоміжними, їх стан не має значення для батька — залишайте їх незалежними.

## Масиви завдань

Коли потрібно запустити кілька завдань і відстежити їх стан, зручно зібрати їх у масив або список. Це дозволяє застосовувати `Task.WaitAll` і `Task.WaitAny` до довільної кількості завдань без перерахування кожного вручну.

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

string[] examinations = { "Загальний аналіз крові", "Аналіз сечі", "ЕКГ", "УЗД черевної порожнини" };

// Спосіб 1: створення масиву через ініціалізатор
Task[] tasks = new Task[examinations.Length];
for (int i = 0; i < examinations.Length; i++)
{
    string exam = examinations[i]; // копія для замикання
    tasks[i] = Task.Run(() =>
    {
        int duration = 100 + exam.Length * 10; // різний час для різних обстежень
        Console.WriteLine($"[Task {Task.CurrentId}] Початок: {exam}");
        Thread.Sleep(duration);
        Console.WriteLine($"[Task {Task.CurrentId}] Готово: {exam}");
    });
}

Console.WriteLine("Всі обстеження запущені паралельно...");
Task.WaitAll(tasks); // чекаємо завершення всіх
Console.WriteLine("Всі обстеження завершено — готую зведений звіт лікарю");
```

### WaitAll vs WaitAny: коли що обирати

`Task.WaitAll` — для сценарію «потрібні всі результати, щоб рухатись далі». Наприклад, перш ніж видати загальний висновок, лікар чекає на всі аналізи.

`Task.WaitAny` — для сценарію «реагуй на перший готовий результат». Наприклад, система моніторингу обробляє показники від першого датчика, що надіслав дані, не чекаючи решти:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task[] monitors = new Task[]
{
    Task.Run(() => { Thread.Sleep(400); Console.WriteLine("Датчик пульсу: 88 уд/хв"); }),
    Task.Run(() => { Thread.Sleep(150); Console.WriteLine("Датчик SpO2: 97%"); }),
    Task.Run(() => { Thread.Sleep(280); Console.WriteLine("Датчик тиску: 122/78"); }),
};

Console.WriteLine("Система моніторингу: очікую перший сигнал...");
int first = Task.WaitAny(monitors);
Console.WriteLine($"Перший сигнал отримано від датчика #{first.ToString()} — фіксую в карті");
Task.WaitAll(monitors); // дочекаємо решту
Console.WriteLine("Всі показники зафіксовано");
```

## Task\<T\>: завдання з результатом

До цього моменту ми розглядали завдання, що нічого не повертають (`Task` — аналог `void`). Але часто завдання обчислює щось і результат потрібен у головному потоці. Для цього існує типізована версія — `Task<T>`, де `T` — тип значення, що повертається.

Результат отримується через властивість `Result`. Звернення до `Result` **блокує поточний потік** до завершення завдання — аналогічно `Wait()`. Тому `Result` є одночасно і очікуванням, і отриманням результату.

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

// Завдання, що повертає числовий результат
Task<double> bmiTask = Task.Run(() =>
{
    double weight = 72.5; // кг
    double height = 1.78; // м
    Thread.Sleep(100); // імітуємо розрахунок
    return weight / (height * height); // формула ІМТ
});

Console.WriteLine("ІМТ розраховується...");
double bmi = bmiTask.Result; // блокується тут до отримання результату
Console.WriteLine($"ІМТ пацієнта: {bmi.ToString("F1")} кг/м²");
Console.WriteLine($"Категорія: {(bmi < 18.5 ? "Недостатня вага" : bmi < 25 ? "Норма" : bmi < 30 ? "Зайва вага" : "Ожиріння")}");
```

### Task\<T\> з класом результату

У реальних клінічних задачах результат — це, як правило, не просте число, а об'єкт із кількома полями:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

class LabResult
{
    public string PatientName { get; }
    public double Glucose     { get; }
    public double Hemoglobin  { get; }
    public string Status      { get; }

    public LabResult(string name, double glucose, double hemoglobin)
    {
        PatientName = name;
        Glucose     = glucose;
        Hemoglobin  = hemoglobin;
        Status      = glucose > 6.1 ? "Глюкоза підвищена" : hemoglobin < 120 ? "Гемоглобін знижений" : "Норма";
    }
}

Task<LabResult> labTask = Task.Run(() =>
{
    Console.WriteLine("[Лабораторія] Виконую аналіз крові Коваль М.В...");
    Thread.Sleep(400);
    return new LabResult("Коваль М.В.", glucose: 5.8, hemoglobin: 138.0);
});

LabResult result = labTask.Result; // блокуємось до завершення

Console.WriteLine($"\n=== Результат аналізу ===");
Console.WriteLine($"Пацієнт:    {result.PatientName}");
Console.WriteLine($"Глюкоза:    {result.Glucose.ToString("F1")} ммоль/л");
Console.WriteLine($"Гемоглобін: {result.Hemoglobin.ToString("F0")} г/л");
Console.WriteLine($"Висновок:   {result.Status}");
```

### Кілька Task\<T\> з WaitAll

`Task.WaitAll` коректно працює і з масивами `Task<T>`. Після `WaitAll` до всіх результатів можна звертатись через `Result` без додаткового блокування — результати вже готові:

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Task<string>[] diagnostics = new Task<string>[]
{
    Task.Run(() => { Thread.Sleep(300); return "Кров: норма"; }),
    Task.Run(() => { Thread.Sleep(200); return "Сеча: норма"; }),
    Task.Run(() => { Thread.Sleep(400); return "Рентген: без патологій"; }),
};

Console.WriteLine("Паралельна діагностика запущена...");
Task.WaitAll(diagnostics);

Console.WriteLine("\n=== Зведений протокол обстеження ===");
for (int i = 0; i < diagnostics.Length; i++)
    Console.WriteLine($"  {(i + 1).ToString()}. {diagnostics[i].Result}");

Console.WriteLine("Протокол сформовано. Направляю до лікаря.");
```

Важливий момент: звернення до `Result` після `WaitAll` не блокує — всі завдання вже завершились. Але якщо завдання завершилось з винятком, `Result` кине `AggregateException` при зверненні. Завжди обробляйте можливі винятки через `try/catch`, якщо завдання може завершитись з помилкою.
