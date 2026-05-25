---
chapter: 6
chapterTitle: "Розділ 6. Делегати, події та лямбди"
section: 1
number: "6.1"
title: "Делегати"
source: "../_combined/34-delehaty.md"
---

## 6.1. Делегати

Делегати — один із фундаментальних механізмів C#, який дозволяє зберігати посилання на методи і передавати методи як значення. Якщо змінна типу `int` зберігає число, а змінна типу `string` — рядок, то змінна-делегат зберігає посилання на метод. Через цю змінну метод можна викликати, передати в інший метод як аргумент або зберегти для виклику пізніше.

Делегати є основою для подій, лямбда-виразів, функцій вищого порядку та патерну зворотного виклику (callback). Розуміння делегатів — це розуміння того, як у C# методи стають об'єктами першого класу.

## Визначення делегата

Для оголошення делегата використовується ключове слово `delegate`, після якого вказується тип значення, що повертається, ім'я делегата та список параметрів. По суті, це оголошення типу, що описує сигнатуру методів, на які делегат може вказувати:

```csharp
delegate void Notify(string message);
```

Делегат `Notify` відповідає будь-якому методу, який приймає один параметр `string` і нічого не повертає (`void`). Жоден інший набір параметрів або тип, що повертається, не підійде.

## Використання делегата: чотири кроки

Робота з делегатом завжди складається з одних і тих самих кроків:

```csharp run
using System;

delegate void Notify(string message); // 1. Оголошуємо тип делегата

void AlertDoctor(string msg) =>
    Console.WriteLine($"[ЛІКАР] {msg}");

Notify handler;          // 2. Оголошуємо змінну делегата
handler = AlertDoctor;   // 3. Присвоюємо посилання на метод
handler("Критичний пульс пацієнта Петренка!"); // 4. Викликаємо
```

![Делегат як посилання на метод](_assets/06-01/delegate-concept.png)

Змінну делегата можна перепризначити на інший метод тієї ж сигнатури — і виклик делегата почне виконувати вже інший код. Саме ця здатність змінювати поведінку під час виконання є ключовою перевагою делегатів.

## Делегати, що вказують на методи інших класів

Делегат може вказувати на методи будь-яких класів — статичні та екземплярні:

```csharp run
using System;

delegate void Notify(string message);

class ConsoleLogger
{
    public static void Log(string msg) =>
        Console.WriteLine($"[LOG] {msg}");
}

class DoctorNotifier
{
    public void Alert(string msg) =>
        Console.WriteLine($"[DR] {msg}");
}

Notify n1 = ConsoleLogger.Log;
Notify n2 = new DoctorNotifier().Alert;

n1("Аналізи готові");
n2("Пацієнт потребує огляду");
```

Статичний метод призначається через ім'я класу, екземплярний — через екземпляр об'єкта. З точки зору делегата різниці немає: обидва виклики виглядають однаково.

## Місце визначення делегата

У програмах верхнього рівня (top-level statements, файл `Program.cs`), які є стандартом починаючи з C# 10, делегат визначається після всього виконуваного коду — так само як класи та інші типи. Він може також бути визначений всередині класу або поза ним у традиційному стилі.

## Параметри та повернення значення

Делегат повністю успадковує сигнатуру методу: параметри, їх типи і тип значення, що повертається. Делегат можна перепризначати між методами, що мають однакову сигнатуру:

```csharp run
using System;

delegate double Calculate(double a, double b);

double Add(double x, double y)      => x + y;
double Subtract(double x, double y) => x - y;
double Multiply(double x, double y) => x * y;

Calculate calc = Add;
Console.WriteLine($"Сума:   {calc(10.5, 4.5).ToString("F1")}");

calc = Subtract;
Console.WriteLine($"Різниця: {calc(10.5, 4.5).ToString("F1")}");

calc = Multiply;
Console.WriteLine($"Добуток: {calc(10.5, 4.5).ToString("F1")}");
```

Альтернативний синтаксис ініціалізації через конструктор делегата дає той самий результат:

```csharp
Calculate calc1 = Add;
Calculate calc2 = new Calculate(Add); // рівноцінно
```

## Відповідність методів делегату

Метод відповідає делегату, якщо він має **той самий тип, що повертається**, і **той самий набір параметрів**, включно з модифікаторами `ref`, `in`, `out`. Наприклад, для делегата:

```csharp
delegate void AlertHandler(string message);
```

Відповідає:
```csharp
void SendToNurse(string msg) { }          // OK
```

Не відповідає:
```csharp
string GetMessage(string msg)  { return msg; }  // інший тип повернення
void Log(string msg, int code) { }              // інший набір параметрів
void Handle(ref string msg)    { }              // модифікатор ref
```

## Додавання методів у делегат (multicast)

Делегат у C# може вказувати не на один, а на **кілька методів** одночасно. Внутрішньо він підтримує список виклику (invocation list). Додавання методу виконується оператором `+=`:

```csharp run
using System;

delegate void AlertHandler(string message);

void LogToConsole(string msg) =>
    Console.WriteLine($"[КОНСОЛЬ] {msg}");

void LogToFile(string msg) =>
    Console.WriteLine($"[ФАЙЛ] Записано: {msg}");

void NotifyDoctor(string msg) =>
    Console.WriteLine($"[ЛІКАР] Увага: {msg}");

AlertHandler alert = LogToConsole;
alert += LogToFile;
alert += NotifyDoctor;

alert("Критичні показники пацієнта Бойка!");
```

![Список виклику multicast-делегата](_assets/06-01/invocation-list.png)

При виклику делегата всі методи зі списку викликаються **послідовно у порядку додавання**. Якщо один і той самий метод додати кілька разів — він викликатиметься стільки разів, скільки був доданий.

## Видалення методів із делегата

Методи видаляються зі списку виклику оператором `-=`. Якщо після видалення список стає порожнім — делегат набуває значення `null`:

```csharp run
using System;

delegate void AlertHandler(string message);

void LogToConsole(string msg) => Console.WriteLine($"[LOG] {msg}");
void NotifyDoctor(string msg) => Console.WriteLine($"[DR]  {msg}");

AlertHandler? alert = LogToConsole;
alert += NotifyDoctor;

Console.WriteLine("=== Обидва обробники ===");
alert("Температура 39.5°C");

alert -= NotifyDoctor;

Console.WriteLine("=== Тільки логування ===");
alert?.Invoke("Температура 38.0°C");
```

Змінна оголошена як `AlertHandler?` (nullable), бо після видалення всіх методів вона може стати `null`. Перед викликом обов'язково перевіряємо — через `?.Invoke()` або явну перевірку на `null`.

## Об'єднання делегатів

Два делегати можна об'єднати оператором `+` — отримаємо новий делегат, чий список виклику містить методи обох:

```csharp run
using System;

delegate void AlertHandler(string message);

void LogToConsole(string msg) => Console.WriteLine($"[LOG]  {msg}");
void NotifyDoctor(string msg) => Console.WriteLine($"[DR]   {msg}");
void SendSMS(string msg)      => Console.WriteLine($"[SMS]  {msg}");

AlertHandler group1 = LogToConsole;
group1 += NotifyDoctor;

AlertHandler group2 = SendSMS;

AlertHandler all = group1 + group2;
all("Пацієнт Сидоренко: пульс 145 уд/хв");
```

## Виклик делегата: прямий та через Invoke

Делегат можна викликати двома еквівалентними способами:

```csharp run
using System;

delegate int Score(int base_, int bonus);

int CalcScore(int b, int bonus) => b + bonus;

Score score = CalcScore;

// Прямий виклик
int r1 = score(80, 15);
Console.WriteLine($"Результат 1: {r1.ToString()}");

// Через Invoke
int r2 = score.Invoke(80, 20);
Console.WriteLine($"Результат 2: {r2.ToString()}");
```

Метод `Invoke` особливо корисний у поєднанні з оператором умовного null `?.`, що дозволяє безпечно викликати делегат, який може бути `null`:

```csharp run
using System;

delegate void AlertHandler(string message);

AlertHandler? alert = null;

// Без перевірки — впаде з NullReferenceException
// alert("Помилка!");

// Безпечний виклик через ?. — нічого не станеться якщо null
alert?.Invoke("Безпечний виклик");

Console.WriteLine("Програма продовжує виконання");
```

## Повернення значення з multicast-делегата

Якщо делегат містить кілька методів і повертає значення — повертається результат **останнього методу** зі списку виклику. Результати проміжних методів відкидаються:

```csharp run
using System;

delegate int ScoreCalc(int base_, int coeff);

int Method1(int b, int c) { Console.WriteLine($"Method1: {(b*c).ToString()}"); return b * c; }
int Method2(int b, int c) { Console.WriteLine($"Method2: {(b+c).ToString()}"); return b + c; }
int Method3(int b, int c) { Console.WriteLine($"Method3: {(b-c).ToString()}"); return b - c; }

ScoreCalc calc = Method1;
calc += Method2;
calc += Method3;

int result = calc(10, 3);
Console.WriteLine($"Повернуто (останній): {result.ToString()}");
```

З цієї причини multicast-делегати з типом повернення, відмінним від `void`, застосовуються рідко — зазвичай саме для `void`-методів, де кожен метод виконує свою дію незалежно.

## Узагальнені делегати

Делегати, як і класи, можуть мати параметри типів. Це дозволяє описати делегат, що відповідає методам із різними типами параметрів і повернення:

```csharp run
using System;

delegate TResult Transform<TInput, TResult>(TInput value);

double KgToLb(double kg) => kg * 2.20462;
int CelsiusToFahrenheit(int celsius) => celsius * 9 / 5 + 32;
string FormatPulse(int pulse) => $"{pulse.ToString()} уд/хв";

Transform<double, double> weightConv  = KgToLb;
Transform<int, int>       tempConv    = CelsiusToFahrenheit;
Transform<int, string>    pulseFormat = FormatPulse;

Console.WriteLine($"70 кг = {weightConv(70.0).ToString("F1")} фунтів");
Console.WriteLine($"37°C = {tempConv(37).ToString()}°F");
Console.WriteLine($"Пульс: {pulseFormat(72)}");
```

Узагальнені делегати — основа стандартних делегатів `Func<>` та `Action<>`, які вбудовані в .NET і розглядатимуться далі.

## Делегати як параметри методів

Найпотужніша можливість делегатів — передача методів як аргументів іншим методам. Це дозволяє будувати гнучкі алгоритми, поведінка яких визначається ззовні:

```csharp run
using System;

delegate bool Filter(double value);
delegate string Format(double value);

void PrintReadings(double[] readings, Filter filter, Format format)
{
    foreach (var r in readings)
    {
        if (filter(r))
            Console.WriteLine($"  {format(r)}");
    }
}

double[] pulseData = { 72, 145, 68, 130, 55, 88, 165 };

Console.WriteLine("Критичні показники пульсу:");
PrintReadings(
    pulseData,
    v => v > 120 || v < 60,
    v => $"Пульс {v.ToString("F0")} уд/хв [!]"
);

Console.WriteLine("Норма:");
PrintReadings(
    pulseData,
    v => v >= 60 && v <= 120,
    v => $"Пульс {v.ToString("F0")} уд/хв"
);
```

Метод `PrintReadings` не знає заздалегідь ні логіки фільтрації, ні способу форматування — їх визначає викликаючий код. Це і є функції вищого порядку.

## Повернення делегатів із методів

Метод може повертати делегат — тобто повертати певну поведінку як об'єкт:

```csharp run
using System;

delegate string DiagnoseFunc(double value);

enum MeasurementType { Pulse, Temperature, BloodPressureSys }

DiagnoseFunc GetDiagnoser(MeasurementType type) => type switch
{
    MeasurementType.Pulse =>
        v => v < 60 ? "Брадикардія" : v > 100 ? "Тахікардія" : "Норма",
    MeasurementType.Temperature =>
        v => v < 36.0 ? "Гіпотермія" : v > 37.5 ? "Гіпертермія" : "Норма",
    MeasurementType.BloodPressureSys =>
        v => v < 90 ? "Гіпотонія" : v > 140 ? "Гіпертонія" : "Норма",
    _ => v => "Невідомий показник"
};

var diagnosePulse = GetDiagnoser(MeasurementType.Pulse);
var diagnoseTemp  = GetDiagnoser(MeasurementType.Temperature);

Console.WriteLine($"Пульс 145: {diagnosePulse(145)}");
Console.WriteLine($"Пульс 72: {diagnosePulse(72)}");
Console.WriteLine($"Темп 38.2: {diagnoseTemp(38.2)}");
```

## Практичний приклад: патерн зворотного виклику

Найважливіше застосування делегатів — **callback-патерн**: клас визначає делегат для сповіщення про події, а зовнішній код реєструє власні обробники. Клас не знає що саме відбудеться — він просто викликає делегат.

Розглянемо монітор вітальних показників пацієнта. Клас повинен реагувати на критичні значення, але не повинен знати як саме — через консоль, лог, SMS або GUI:

![Патерн зворотного виклику через делегат](_assets/06-01/callback-pattern.png)

```csharp run
using System;

public delegate void AlertHandler(string message);

public class VitalSignsMonitor
{
    private string _patientName;
    private AlertHandler? _onAlert;

    public VitalSignsMonitor(string patientName)
    {
        _patientName = patientName;
    }

    public void RegisterAlert(AlertHandler handler)  => _onAlert += handler;
    public void UnregisterAlert(AlertHandler handler) => _onAlert -= handler;

    public void CheckPulse(int pulse)
    {
        if (pulse > 120)
            _onAlert?.Invoke($"{_patientName}: тахікардія, пульс {pulse.ToString()} уд/хв");
        else if (pulse < 50)
            _onAlert?.Invoke($"{_patientName}: брадикардія, пульс {pulse.ToString()} уд/хв");
    }

    public void CheckTemperature(double temp)
    {
        if (temp > 38.5)
            _onAlert?.Invoke($"{_patientName}: гіпертермія, температура {temp.ToString("F1")}°C");
    }
}

void LogToConsole(string msg) =>
    Console.WriteLine($"[LOG]  {msg}");

void AlertNurse(string msg) =>
    Console.WriteLine($"[МЕДСЕСТРА] Терміново! {msg}");

var monitor = new VitalSignsMonitor("Іван Петренко");

monitor.RegisterAlert(LogToConsole);
monitor.RegisterAlert(AlertNurse);

monitor.CheckPulse(145);
monitor.CheckTemperature(39.1);

Console.WriteLine("--- Прибрали сповіщення медсестри ---");
monitor.UnregisterAlert(AlertNurse);

monitor.CheckPulse(42);
```

Клас `VitalSignsMonitor` абсолютно не залежить від того, що відбувається при спрацюванні сповіщення. Він просто викликає делегат і передає повідомлення. Конкретні дії — вивід у консоль, запис у лог, відправка SMS, показ у GUI — реєструються ззовні. Якщо завтра з'явиться нова вимога «надсилати push-сповіщення» — достатньо зареєструвати ще один обробник, не змінюючи клас монітора.

## Анонімні методи

Замість оголошення окремого іменованого методу, делегату можна присвоїти **анонімний метод** — метод без імені, визначений прямо у місці присвоєння за допомогою ключового слова `delegate`:

```csharp run
using System;

delegate void AlertHandler(string message);

AlertHandler handler = delegate(string msg)
{
    Console.WriteLine($"[АНОНІМНИЙ] {msg}");
};

handler("Пацієнт Коваль: критичний стан");
```

Анонімний метод не може існувати сам по собі — він одразу прив'язується до змінної делегата або передається як аргумент. Анонімні методи часто використовують для одноразових обробників, коли немає сенсу оголошувати окремий метод:

```csharp run
using System;

delegate void AlertHandler(string message);

void RegisterAndTest(string patientName, AlertHandler handler)
{
    Console.WriteLine($"Моніторинг: {patientName}");
    handler($"Перевірка {patientName}: пульс в нормі");
}

RegisterAndTest("Марія Сидоренко", delegate(string msg)
{
    Console.WriteLine($"  >> {msg}");
});
```

Якщо делегат не використовує параметри (навіть якщо вони є у сигнатурі), дужки з параметрами можна опустити:

```csharp run
using System;

delegate void AlertHandler(string message);

AlertHandler handler = delegate
{
    Console.WriteLine("Отримано сповіщення (параметри проігноровано)");
};

handler("будь-яке повідомлення");
```

Анонімні методи, як і локальні функції, мають доступ до змінних зовнішнього контексту (замикання):

```csharp run
using System;

delegate void AlertHandler(string message);

string wardName = "Кардіологія";
int alertCount  = 0;

AlertHandler handler = delegate(string msg)
{
    alertCount++;
    Console.WriteLine($"[{wardName}] #{alertCount.ToString()}: {msg}");
};

handler("Пульс 145");
handler("Тиск 180/100");
handler("Температура 39.2");
Console.WriteLine($"Всього сповіщень: {alertCount.ToString()}");
```

Анонімний метод захоплює змінні `wardName` і `alertCount` із зовнішнього контексту. Зміна `alertCount` всередині анонімного методу відображається у зовнішньому коді — це замикання (closure). Анонімні методи є попередниками лямбда-виразів, які розглядатимуться у наступних розділах і є більш компактним сучасним способом запису того самого.
