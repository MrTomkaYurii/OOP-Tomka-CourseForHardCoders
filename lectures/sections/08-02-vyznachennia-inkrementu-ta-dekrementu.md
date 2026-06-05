---
chapter: 8
chapterTitle: "Розділ 8. Додаткові можливості ООП у C#"
section: 2
number: "8.2"
title: "Визначення інкременту та декременту"
source: "../_combined/47-vyznachennia-inkrementu-ta-dekrementu.md"
---

## 8.2. Визначення інкременту та декременту

Оператори `++` і `--` — унарні, тобто вони приймають один операнд і повертають змінений стан. Для користувацьких типів їх можна перевантажити так само, як і будь-який інший оператор. Однак у них є важлива особливість, яку необхідно враховувати при визначенні.

## Правило незмінності параметрів

Коли ми визначаємо оператор `++` або `--`, параметр методу представляє поточний об'єкт. Інтуїтивно здається, що потрібно просто змінити значення прямо у методі:

```csharp
// НЕПРАВИЛЬНО — мутуємо параметр
public static BodyTemperature operator ++(BodyTemperature t)
{
    t.Celsius += 0.1; // не можна: Celsius — readonly
    return t;
}
```

Це неправильний підхід з двох причин. По-перше, якщо властивість доступна лише для читання (що є стандартом для immutable-типів), такий код не скомпілюється. По-друге, і це головне: **оператор не повинен мутувати свої параметри**. Параметри — це входи, а не виходи. Правильне визначення — повернути **новий об'єкт** з оновленим значенням:

```csharp
// ПРАВИЛЬНО — повертаємо новий об'єкт
public static BodyTemperature operator ++(BodyTemperature t)
{
    return new BodyTemperature(t.Celsius + 0.1);
}
```

Цей підхід відомий як «immutable update pattern»: замість зміни існуючого об'єкта ми створюємо новий із потрібним значенням. Він запобігає побічним ефектам і є стандартом при визначенні операторів у C#.

## Синтаксис оператора інкременту та декременту

Оскільки `++` і `--` — унарні оператори, вони приймають один параметр. Одне визначення охоплює і префіксну (`++t`), і постфіксну (`t++`) форму — компілятор сам реалізує різницю:

```csharp run
using System;

class BodyTemperature
{
    public double Celsius { get; }

    public BodyTemperature(double celsius) => Celsius = celsius;

    // Один метод охоплює і ++t, і t++
    public static BodyTemperature operator ++(BodyTemperature t)
        => new BodyTemperature(Math.Round(t.Celsius + 0.1, 1));

    public static BodyTemperature operator --(BodyTemperature t)
        => new BodyTemperature(Math.Round(t.Celsius - 0.1, 1));

    public override string ToString() => $"{Celsius:F1}°C";
}

BodyTemperature t = new BodyTemperature(36.6);
Console.WriteLine($"Початкова: {t}");

t++;
Console.WriteLine($"Після t++: {t}");

++t;
Console.WriteLine($"Після ++t: {t}");

t--;
Console.WriteLine($"Після t--: {t}");
```

`Math.Round(..., 1)` тут необхідний через особливості арифметики чисел із плаваючою крапкою: `36.6 + 0.1` без округлення може дати `36.699999...` замість `36.7`.

## Префіксна та постфіксна форми: як компілятор розрізняє їх

Хоча ми визначаємо один метод, поведінка `t++` і `++t` — різна. Різниця не в тому, як змінюється об'єкт, а в тому, **яке значення повертається як результат виразу**. Компілятор реалізує це самостійно на основі одного нашого визначення.

![Постфіксний і префіксний ++: одне визначення, різна поведінка](_assets/08-02/increment-prefix-postfix.png)

Побачимо різницю в дії:

```csharp run
using System;

class BodyTemperature
{
    public double Celsius { get; }

    public BodyTemperature(double celsius) => Celsius = celsius;

    public static BodyTemperature operator ++(BodyTemperature t)
        => new BodyTemperature(Math.Round(t.Celsius + 0.1, 1));

    public override string ToString() => $"{Celsius:F1}°C";
}

BodyTemperature t1 = new BodyTemperature(36.6);

// Постфіксний: t2 отримує СТАРУ копію, потім t1 інкрементується
BodyTemperature t2 = t1++;
Console.WriteLine($"Постфіксний: t1={t1},  t2={t2}");
// t1 = 36.7, t2 = 36.6 — t2 зафіксувала стан ДО зміни

BodyTemperature t3 = new BodyTemperature(36.6);

// Префіксний: t3 спочатку інкрементується, потім t4 отримує НОВУ копію
BodyTemperature t4 = ++t3;
Console.WriteLine($"Префіксний:  t3={t3},  t4={t4}");
// t3 = 36.7, t4 = 36.7 — t4 отримала стан ПІСЛЯ зміни
```

При постфіксному `t1++` компілятор виконує три дії: зберігає поточний об'єкт у тимчасову змінну, замінює `t1` результатом `operator++(t1)`, а як результат виразу повертає тимчасову (стару) копію. При префіксному `++t3` — викликає `operator++(t3)`, присвоює результат `t3` і повертає його ж.

Ця різниця важлива лише тоді, коли результат виразу використовується: `t2 = t1++` та `t2 = ++t1` поводяться по-різному. Якщо ж ми пишемо просто `t++;` або `++t;` в окремому рядку — різниці немає.

## Оператори true та false

Окрема пара унарних операторів — `true` і `false`. Вони визначаються, коли ми хочемо використовувати об'єкт нашого класу **безпосередньо як умову** в `if`, `while` або тернарному операторі — без явного виклику методу чи порівняння з `bool`.

У клінічній системі природним кандидатом є клас `MedicalDevice`. Пристрій може бути активним або офлайн, і зручно писати `if (device)` замість `if (device.IsOnline)`:

```csharp run
using System;

class MedicalDevice
{
    public string Name { get; }
    public bool IsOnline { get; }

    public MedicalDevice(string name, bool isOnline)
    {
        Name = name;
        IsOnline = isOnline;
    }

    // Пристрій «true» — якщо активний
    public static bool operator true(MedicalDevice d)  => d.IsOnline;

    // Пристрій «false» — якщо офлайн
    public static bool operator false(MedicalDevice d) => !d.IsOnline;

    // Логічне заперечення: !device
    public static bool operator !(MedicalDevice d)     => !d.IsOnline;

    public override string ToString()
        => IsOnline ? $"{Name} [активний]" : $"{Name} [офлайн]";
}

MedicalDevice monitor = new MedicalDevice("Кардіомонітор", true);
MedicalDevice scanner = new MedicalDevice("МРТ-сканер", false);

// Використання в умові if — без явного .IsOnline
if (monitor)
    Console.WriteLine($"{monitor.Name}: готовий до роботи");

if (!scanner)
    Console.WriteLine($"{scanner.Name}: потрібне технічне обслуговування");

// Тернарний оператор
string status = monitor ? "підключений" : "відключений";
Console.WriteLine($"Статус монітора: {status}");
```

Оператори `true` і `false` завжди визначаються **парою** — компілятор вимагає наявності обох. Оператор `!` не є обов'язковим, але без нього конструкція `if (!device)` не компілюється. Семантично `!device` збігається з оператором `false` — обидва перевіряють, що пристрій «не true».

## Повний приклад: температурний моніторинг

Об'єднаємо `++`, `--` і `true`/`false` у реалістичному клінічному сценарії — автоматичному відстеженні температури пацієнта після лікування:

```csharp run
using System;

class BodyTemperature
{
    public double Celsius { get; }

    public bool IsNormal => Celsius >= 36.0 && Celsius <= 37.0;
    public bool IsFever  => Celsius > 37.5;

    public BodyTemperature(double celsius) => Celsius = celsius;

    public static BodyTemperature operator ++(BodyTemperature t)
        => new BodyTemperature(Math.Round(t.Celsius + 0.1, 1));

    public static BodyTemperature operator --(BodyTemperature t)
        => new BodyTemperature(Math.Round(t.Celsius - 0.1, 1));

    // true: температура в нормі
    public static bool operator true(BodyTemperature t)  => t.IsNormal;
    public static bool operator false(BodyTemperature t) => !t.IsNormal;
    public static bool operator !(BodyTemperature t)     => !t.IsNormal;

    public override string ToString() =>
        IsFever  ? $"{Celsius:F1}°C (жар)"   :
        IsNormal ? $"{Celsius:F1}°C (норма)" :
                   $"{Celsius:F1}°C";
}

BodyTemperature temp = new BodyTemperature(37.8);
Console.WriteLine($"Початкова температура: {temp}");

if (!temp)
    Console.WriteLine("Стан відхиляється від норми — призначено лікування");

Console.WriteLine("Динаміка після лікування:");
for (int i = 0; i < 10; i++)
{
    temp--;
    Console.WriteLine($"  вимірювання {i + 1}: {temp}");
    if (temp)
    {
        Console.WriteLine("Температура нормалізувалась. Лікування завершено.");
        break;
    }
}
```

У цьому прикладі `if (!temp)` перевіряє аномальний стан, а `if (temp)` у циклі фіксує повернення до норми. Код читається природно і не вимагає явного звертання до `IsNormal` або `IsFever` у кожній умові.
