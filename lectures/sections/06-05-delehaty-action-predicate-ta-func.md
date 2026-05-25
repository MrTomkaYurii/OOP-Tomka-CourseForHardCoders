---
chapter: 6
chapterTitle: "Розділ 6. Делегати, події та лямбди"
section: 5
number: "6.5"
title: "Делегати Action, Predicate та Func"
source: "../_migration/source-chunks/38-delehaty-action-predicate-ta-func.md"
---

## 6.5. Делегати Action, Predicate та Func

У .NET є кілька вбудованих узагальнених делегатів, які покривають переважну більшість сценаріїв використання делегатів без потреби оголошувати власні типи. Найбільш вживані з них — `Action`, `Predicate` та `Func`. Їх наявність у стандартній бібліотеці дозволяє писати компактний код: замість `delegate void AlertHandler(string msg)` достатньо написати `Action<string>`, і компілятор розуміє те ж саме.

## Action

Делегат `Action` представляє дію, яка нічого **не повертає** (`void`). Він має кілька перевантажених версій залежно від кількості параметрів: від `Action` (без параметрів) до `Action<T1, T2, …, T16>` (до 16 параметрів):

```csharp
public delegate void Action()
public delegate void Action<in T>(T obj)
public delegate void Action<in T1, in T2>(T1 arg1, T2 arg2)
// ... до Action<T1..T16>
```

`Action` зазвичай передається як параметр методу і описує реакцію на якусь подію. Наприклад, метод обробки показника пацієнта може приймати `Action` як параметр і виконати потрібну дію залежно від контексту:

```csharp run
using System;

ProcessVitals("Іван Петренко", 145, LogAlert);
ProcessVitals("Марія Коваль",  72,  LogNormal);

void ProcessVitals(string patient, int pulse, Action<string, int> report)
    => report(patient, pulse);

void LogAlert(string name, int pulse)
    => Console.WriteLine($"[УВАГА] {name}: пульс {pulse.ToString()} уд/хв — критично!");

void LogNormal(string name, int pulse)
    => Console.WriteLine($"[OK] {name}: пульс {pulse.ToString()} уд/хв — норма");
```

Метод `ProcessVitals` не містить жодної логіки виведення — він лише викликає дію `report`, яку передає зовнішній код. Це дає гнучкість: в одному місці передаємо `LogAlert`, в іншому — `LogNormal`, або будь-яку лямбду.

`Action` без параметрів зручний для реєстрації простих зворотних викликів:

```csharp run
using System;

RunProcedure("Забір крові",   () => Console.WriteLine("  → Зразок взято, відправлено до лабораторії"));
RunProcedure("ЕКГ",           () => Console.WriteLine("  → ЕКГ записано, роздруковано"));
RunProcedure("МРТ",           () => Console.WriteLine("  → МРТ виконано, знімки збережено"));

void RunProcedure(string name, Action onComplete)
{
    Console.WriteLine($"Процедура: {name}");
    onComplete();
}
```

## Predicate

Делегат `Predicate<T>` приймає один параметр типу `T` і повертає `bool`. Він описує умову — відповідає або не відповідає об'єкт певному критерію:

```csharp
delegate bool Predicate<in T>(T obj);
```

`Predicate` використовується для фільтрації, перевірки, пошуку. Наприклад, перевіримо кілька показників пацієнта на відповідність нормі:

```csharp run
using System;

Predicate<double> isGlucoseNormal    = g => g >= 3.9 && g <= 6.1;
Predicate<int>    isPulseNormal      = p => p >= 60  && p <= 100;
Predicate<double> isCholesterolHigh  = c => c > 5.2;

Console.WriteLine($"Глюкоза 5.4: {(isGlucoseNormal(5.4) ? "норма" : "відхилення")}");
Console.WriteLine($"Глюкоза 7.8: {(isGlucoseNormal(7.8) ? "норма" : "відхилення")}");
Console.WriteLine($"Пульс 88: {(isPulseNormal(88) ? "норма" : "відхилення")}");
Console.WriteLine($"Холестерин 6.1: {(isCholesterolHigh(6.1) ? "підвищений" : "норма")}");
```

`Predicate<T>` можна передавати у методи як параметр фільтрації:

```csharp run
using System;

double[] glucoseTests = { 3.5, 5.1, 7.2, 4.8, 8.9, 3.1, 6.5 };

int aboveNorm = CountIf(glucoseTests, g => g > 6.1);
int belowNorm = CountIf(glucoseTests, g => g < 3.9);

Console.WriteLine($"Вище норми: {aboveNorm.ToString()} результатів");
Console.WriteLine($"Нижче норми: {belowNorm.ToString()} результатів");

int CountIf(double[] values, Predicate<double> condition)
{
    int count = 0;
    foreach (var v in values)
        if (condition(v)) count++;
    return count;
}
```

## Func

Делегат `Func` повертає значення і може приймати параметри. Останній параметр типу завжди є **типом повернення** (позначається `TResult`):

```csharp
Func<TResult>                          // без параметрів, повертає TResult
Func<T, TResult>                       // один параметр T, повертає TResult
Func<T1, T2, TResult>                  // два параметри, повертає TResult
// ... до Func<T1..T16, TResult>
```

`Func` часто використовується для обчислень і перетворень. Наприклад, набір функцій обробки медичних показників:

```csharp run
using System;

Func<double, double, double> calcBMI  = (weight, height) => weight / (height * height);
Func<int, string>            classify = pulse => pulse > 100 ? "Тахікардія" : pulse < 60 ? "Брадикардія" : "Норма";
Func<double, double>         kgToLb   = kg => kg * 2.20462;

Console.WriteLine($"ІМТ 70 кг / 1.75 м: {calcBMI(70, 1.75).ToString("F1")}");
Console.WriteLine($"Пульс 110: {classify(110)}");
Console.WriteLine($"70 кг у фунтах: {kgToLb(70).ToString("F1")}");
```

`Func` зручний також як параметр методу — для стратегій обчислення:

```csharp run
using System;

double dose1 = CalcDose("Аспірін",    70.0, weight => weight * 10.0);
double dose2 = CalcDose("Ібупрофен",  60.0, weight => weight * 5.0);
double dose3 = CalcDose("Парацетамол",80.0, weight => weight * 15.0);

Console.WriteLine($"Аспірін:     {dose1.ToString("F0")} мг");
Console.WriteLine($"Ібупрофен:   {dose2.ToString("F0")} мг");
Console.WriteLine($"Парацетамол: {dose3.ToString("F0")} мг");

double CalcDose(string drug, double weightKg, Func<double, double> formula)
{
    double dose = formula(weightKg);
    return dose;
}
```

![Вбудовані делегати: Action, Predicate, Func](_assets/06-05/action-predicate-func.png)

## Замикання

Замикання (closure) — це функція, яка «запам'ятовує» своє лексичне оточення навіть тоді, коли виконується поза областю видимості, де вона була створена. Якщо звичайна функція звертається лише до своїх параметрів і локальних змінних, то замикання також має доступ до змінних зовнішньої функції, у якій воно визначене.

Технічно замикання складається з трьох компонентів:

- **зовнішня функція** — визначає область видимості і змінні (лексичне оточення)
- **лексичне оточення** — змінні та параметри зовнішньої функції
- **вкладена функція** — захоплює і використовує лексичне оточення

У C# замикання реалізуються через локальні функції та лямбда-вирази.

### Замикання через локальні функції

```csharp run
using System;

var counter = CreateAlertCounter("ICU");
counter(); // ICU: сповіщення #1
counter(); // ICU: сповіщення #2
counter(); // ICU: сповіщення #3

Action CreateAlertCounter(string ward)
{
    int count = 0;                          // лексичне оточення
    void Increment()                        // локальна функція
    {
        count++;                            // захоплює count із зовнішньої функції
        Console.WriteLine($"{ward}: сповіщення #{count.ToString()}");
    }
    return Increment;                       // повертаємо функцію разом з оточенням
}
```

Тут `CreateAlertCounter` повертає локальну функцію `Increment`. Після виходу з `CreateAlertCounter` змінна `count` більше не існує «звичайним чином» на стеку — але замикання зберігає її в купі (heap). Кожен виклик `counter()` читає і змінює саме цю захоплену змінну, тому лічильник зростає між викликами.

### Замикання через лямбда-вирази

За допомогою лямбд можна скоротити визначення замикання:

```csharp run
using System;

var createCounter = (string ward) =>
{
    int count = 0;
    Action increment = () =>
    {
        count++;
        Console.WriteLine($"{ward}: сповіщення #{count.ToString()}");
    };
    return increment;
};

var icuCounter  = createCounter("ICU");
var cardCounter = createCounter("Кардіологія");

icuCounter();   // ICU: сповіщення #1
icuCounter();   // ICU: сповіщення #2
cardCounter();  // Кардіологія: сповіщення #1
icuCounter();   // ICU: сповіщення #3
```

Кожен виклик `createCounter` створює **нове** замикання з власним незалежним `count`. `icuCounter` і `cardCounter` — два окремих замикання, кожне з яких зберігає свій власний лічильник.

### Застосування параметрів у замиканнях

До лексичного оточення замикання належать не лише локальні змінні, а й **параметри зовнішньої функції**. Це дозволяє створювати «фабрики функцій» — методи, що повертають налаштовані дії:

```csharp run
using System;

var glucoseCheck  = CreateRangeCheck(3.9, 6.1);
var cholesterolCheck = CreateRangeCheck(3.0, 5.2);

Console.WriteLine($"Глюкоза 5.4: {glucoseCheck(5.4)}");
Console.WriteLine($"Глюкоза 7.8: {glucoseCheck(7.8)}");
Console.WriteLine($"Холестерин 4.1: {cholesterolCheck(4.1)}");
Console.WriteLine($"Холестерин 6.0: {cholesterolCheck(6.0)}");

Func<double, string> CreateRangeCheck(double low, double high)
{
    // параметри low і high захоплюються замиканням
    return value =>
        value < low  ? $"Нижче норми (норма {low.ToString("F1")}–{high.ToString("F1")})" :
        value > high ? $"Вище норми (норма {low.ToString("F1")}–{high.ToString("F1")})" :
                       "Норма";
}
```

Метод `CreateRangeCheck` приймає два порогові значення і повертає лямбду, яка їх «запам'ятовує». `glucoseCheck` і `cholesterolCheck` — це два різних замикання, кожне з яких містить свої пороги. Замість передавати `low` і `high` при кожному виклику — вони «вбудовані» у функцію один раз при її створенні.

![Механізм замикання: захоплення лексичного оточення](_assets/06-05/closure-lifecycle.png)

Скорочений запис через каррінг (ланцюг лямбд):

```csharp run
using System;

var check = (double low, double high) => (double value) =>
    value < low ? "Нижче" : value > high ? "Вище" : "Норма";

var hemoglobin = check(120, 170);
Console.WriteLine($"Гемоглобін 105: {hemoglobin(105)}");
Console.WriteLine($"Гемоглобін 145: {hemoglobin(145)}");
Console.WriteLine($"Гемоглобін 185: {hemoglobin(185)}");
```

Замикання — потужний механізм, але він несе відповідальність: захоплена змінна живе у пам'яті доти, доки живе замикання. Якщо замикання зберігається довго (наприклад, підписане на подію, що ніколи не відписується), захоплені великі об'єкти не звільняться збирачем сміття. При роботі з замиканнями слід усвідомлювати, які саме змінні захоплюються і який час вони мають жити.
