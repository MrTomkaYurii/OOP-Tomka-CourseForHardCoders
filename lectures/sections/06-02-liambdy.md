---
chapter: 6
chapterTitle: "Розділ 6. Делегати, події та лямбди"
section: 2
number: "6.2"
title: "Лямбди"
source: "../_migration/source-chunks/35-liambdy.md"
---

## 6.2. Лямбди

Лямбда-вираз — це компактний синтаксис для визначення анонімних методів. Там, де раніше потрібно було писати ключове слово `delegate`, список параметрів у дужках і тіло у фігурних дужках, лямбда дозволяє записати все в один рядок. З погляду типів даних лямбда-вираз представляє делегат — тобто посилання на метод із певною сигнатурою. Лямбди особливо корисні, коли метод короткий, застосовується в одному місці і немає сенсу виносити його у самостійну функцію.

Лямбда-оператор `=>` розбиває вираз на дві частини: ліворуч — список параметрів, праворуч — тіло:

```text
(список_параметрів) => тіло
```

Якщо тіло є одним виразом — фігурні дужки не потрібні. Якщо тіло містить кілька інструкцій — воно оформляється як звичайний блок у фігурних дужках.

## Базовий синтаксис

Розглянемо найпростішу лямбду без параметрів, яка виводить повідомлення:

```csharp run
using System;

PatientHandler greet = () => Console.WriteLine("Пацієнт зареєстрований у системі");
greet();
greet();

delegate void PatientHandler();
```

Змінна `greet` представляє делегат `PatientHandler` — метод без параметрів і без повернення. Як значення надається лямбда-вираз: ліворуч від `=>` порожні дужки (немає параметрів), праворуч — єдиний вираз.

Якщо лямбда виконує кілька дій — вони поміщаються у фігурні дужки:

```csharp run
using System;

PatientHandler register = () =>
{
    Console.WriteLine("Пацієнт зареєстрований у системі");
    Console.WriteLine("Очікуйте виклику лікаря");
};
register();

delegate void PatientHandler();
```

![Синтаксис лямбда-виразу](_assets/06-02/lambda-syntax.png)

Починаючи з C# 10 можна застосовувати неявну типізацію через `var`. Компілятор сам виводить тип делегата з контексту:

```csharp run
using System;

var greet = () => Console.WriteLine("Пацієнт зареєстрований");
greet();
```

При неявній типізації компілятор зіставляє лямбда-вираз із вбудованим делегатом. У цьому прикладі `greet` буде типу `Action` — стандартного делегата без параметрів і без повернення.

## Параметри лямбди

При визначенні списку параметрів типи даних зазвичай можна не вказувати — компілятор виводить їх з типу делегата:

```csharp run
using System;

AlertHandler alert = (name, msg) => Console.WriteLine($"[{name}]: {msg}");
alert("Кардіологія", "Пацієнт Петренко: пульс 145");
alert("ICU", "Критичний стан — негайна допомога");

delegate void AlertHandler(string department, string message);
```

Компілятор бачить, що `alert` є типом `AlertHandler`, де обидва параметри — `string`, тому `name` і `msg` автоматично отримують тип `string`.

Якщо ж застосовується неявна типізація через `var`, компілятор не може вивести типи параметрів — тоді їх потрібно вказати явно:

```csharp run
using System;

var alert = (string department, string message) =>
    Console.WriteLine($"[{department}]: {message}");
alert("Неврологія", "Пацієнт Сидоренко: скарги на головний біль");
```

Якщо лямбда має рівно один параметр і його тип можна вивести — дужки навколо параметра можна опустити:

```csharp run
using System;

NotifyHandler notify = patientName => Console.WriteLine($"Виклик: {patientName}");
notify("Марія Коваль");
notify("Олег Бойко");

delegate void NotifyHandler(string patientName);
```

## Повернення результату

Лямбда-вираз може повертати результат. Якщо тіло є єдиним виразом — значення повертається автоматично, без `return`:

```csharp run
using System;

CalculateHandler bmi = (weight, height) => weight / (height * height);
double result = bmi(70.0, 1.75);
Console.WriteLine($"ІМТ: {result.ToString("F1")}");

ScoreHandler classify = score => score >= 60 ? "задовільно" : "критично";
Console.WriteLine($"Оцінка стану: {classify(72)}");
Console.WriteLine($"Оцінка стану: {classify(45)}");

delegate double CalculateHandler(double weight, double height);
delegate string ScoreHandler(int score);
```

Якщо лямбда містить кілька виразів — потрібен явний `return`, як у звичайному методі:

```csharp run
using System;

BloodPressureHandler classify = (systolic, diastolic) =>
{
    if (systolic > 140 || diastolic > 90) return "Гіпертонія";
    if (systolic < 90 || diastolic < 60) return "Гіпотонія";
    return "Норма";
};

Console.WriteLine($"150/95: {classify(150, 95)}");
Console.WriteLine($"85/55: {classify(85, 55)}");
Console.WriteLine($"120/80: {classify(120, 80)}");

delegate string BloodPressureHandler(int systolic, int diastolic);
```

## Додавання та видалення дій у лямбда-виразі

Оскільки лямбда-вираз представляє делегат, до змінної-лямбди можна додавати інші методи та лямбди через `+=`, а також видаляти через `-=`:

```csharp run
using System;

AlertChain logAlert = () => Console.WriteLine("[LOG] Сигнал тривоги");
AlertChain notifyDoc = () => Console.WriteLine("[DR] Виклик лікаря");
AlertChain sendSMS = () => Console.WriteLine("[SMS] Повідомлення відправлено");

AlertChain alert = logAlert;
alert += notifyDoc;
alert += sendSMS;
alert();

Console.WriteLine("--- видаляємо SMS ---");
alert -= sendSMS;
alert?.Invoke();

delegate void AlertChain();
```

При виклику `alert()` послідовно виконуються всі методи зі списку виклику. Після видалення `sendSMS` залишаються лише два перших.

## Лямбда-вираз як аргумент методу

Найпрактичніше застосування лямбд — передача їх як аргументи методам. Це дозволяє параметризувати поведінку: метод визначає загальну структуру, а конкретна дія передається ззовні:

```csharp run
using System;

double[] glucoseReadings = { 3.5, 7.2, 5.1, 8.8, 4.9, 6.3, 2.9 };

double highCount = CountMatching(glucoseReadings, x => x > 6.1);
double lowCount  = CountMatching(glucoseReadings, x => x < 3.9);

Console.WriteLine($"Вище норми (>6.1): {highCount.ToString("F0")} результатів");
Console.WriteLine($"Нижче норми (<3.9): {lowCount.ToString("F0")} результатів");

double CountMatching(double[] values, IsMatch condition)
{
    int count = 0;
    foreach (var v in values)
        if (condition(v)) count++;
    return count;
}

delegate bool IsMatch(double value);
```

Метод `CountMatching` не знає, яка конкретно умова застосовується — він лише викликає делегат `condition` для кожного елемента. Умова передається зовні через лямбду: `x => x > 6.1` або `x => x < 3.9`. Такий підхід дозволяє повторно використовувати метод для будь-яких критеріїв фільтрації без зміни самого методу.

## Лямбда-вираз як результат методу

Метод може повертати лямбда-вираз. Тип, що повертається, — делегат, якому відповідає лямбда:

```csharp run
using System;

BloodAnalysis analyze = SelectAnalysis(AnalysisType.Glucose);
Console.WriteLine($"Глюкоза 7.5: {analyze(7.5)}");

analyze = SelectAnalysis(AnalysisType.Hemoglobin);
Console.WriteLine($"Гемоглобін 105: {analyze(105.0)}");

analyze = SelectAnalysis(AnalysisType.Cholesterol);
Console.WriteLine($"Холестерин 6.2: {analyze(6.2)}");

BloodAnalysis SelectAnalysis(AnalysisType type)
{
    switch (type)
    {
        case AnalysisType.Glucose:
            return value => value < 3.9 ? "Низький" : value > 6.1 ? "Високий" : "Норма";
        case AnalysisType.Hemoglobin:
            return value => value < 120 ? "Низький" : value > 170 ? "Високий" : "Норма";
        default:
            return value => value < 3.0 ? "Низький" : value > 5.2 ? "Високий" : "Норма";
    }
}

enum AnalysisType { Glucose, Hemoglobin, Cholesterol }
delegate string BloodAnalysis(double value);
```

Метод `SelectAnalysis` отримує тип аналізу і повертає відповідну лямбду з потрібними порогами норми. Зовнішній код отримує готову функцію-класифікатор і може викликати її для будь-якого значення. Такий патерн часто називають «фабрикою функцій» — метод конструює і повертає поведінку, а не лише дані.

![Лямбда vs анонімний метод vs іменований метод](_assets/06-02/lambda-vs-methods.png)
