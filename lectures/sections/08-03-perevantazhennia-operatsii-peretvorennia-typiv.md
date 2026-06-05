---
chapter: 8
chapterTitle: "Розділ 8. Додаткові можливості ООП у C#"
section: 3
number: "8.3"
title: "Перевантаження операцій перетворення типів"
source: "../_combined/48-perevantazhennia-operatsii-peretvorennia-typiv.md"
---

## 8.3. Перевантаження операцій перетворення типів

У розділі 2 ми розглядали неявні та явні перетворення між примітивними типами: `int` → `long` відбувається автоматично (implicit), а `double` → `int` потребує явного cast-у (explicit). Той самий механізм можна визначити і для власних класів — це **перевантаження операторів перетворення типів**.

Завдяки цьому ми можемо навчити компілятор, як перетворювати об'єкт нашого типу на інший тип (і навпаки), і контролювати — чи це відбуватиметься автоматично, чи лише при явному приведенні. Наприклад, у клінічній системі зручно присвоювати числове значення температури безпосередньо об'єкту `BodyTemperature`:

```csharp
BodyTemperature t = 36.6;  // implicit: double → BodyTemperature
double c = (double)t;      // explicit: BodyTemperature → double
```

## Синтаксис оператора перетворення

Оператор перетворення визначається як статичний метод у класі або структурі:

```csharp
public static implicit|explicit operator ТипРезультату(ВхіднийТип param)
{
    // логіка перетворення
}
```

- `public static` — обов'язкові модифікатори.
- `implicit` або `explicit` — визначає, чи потрібен явний cast.
- `operator` — ключове слово.
- `ТипРезультату` — тип, **до** якого перетворюємо.
- `ВхіднийТип param` — тип і параметр, **з** якого перетворюємо.

![Оператор перетворення типів: implicit vs explicit](_assets/08-03/conversion-implicit-explicit.png)

**Обмеження:** оператор перетворення повинен або приймати параметром об'єкт свого типу, або повертати об'єкт свого типу. Тобто оператор визначений у класі `BodyTemperature` може перетворювати `double` → `BodyTemperature` (повертає свій тип) або `BodyTemperature` → `double` (приймає свій тип). Визначити оператор між двома чужими типами в середині третього класу — неможливо.

## implicit: неявне перетворення

Неявне перетворення відбувається автоматично — без жодного синтаксису з боку програміста. Використовується тоді, коли перетворення безпечне, без втрати даних і семантично очевидне.

Визначимо implicit-перетворення з `double` у `BodyTemperature` — створення температури з числового значення:

```csharp run
using System;

// Виконуваний код
// Неявне перетворення: double → BodyTemperature (без cast)
BodyTemperature morning = 36.6;
BodyTemperature fever   = 38.5;

Console.WriteLine($"Ранкова температура: {morning}");
Console.WriteLine($"Температура при жарі: {fever}");
Console.WriteLine($"Є жар: {(fever.IsFever ? "так" : "ні")}");

// Клас
class BodyTemperature
{
    public double Celsius { get; }
    public bool IsFever => Celsius > 37.5;

    public BodyTemperature(double celsius) => Celsius = celsius;

    // implicit: double → BodyTemperature (безпечно, без втрат)
    public static implicit operator BodyTemperature(double celsius)
        => new BodyTemperature(celsius);

    public override string ToString() => $"{Celsius:F1}°C";
}
```

Завдяки `implicit` ми можемо писати `BodyTemperature t = 36.6` — компілятор сам викличе оператор перетворення. Це зручно і читабельно, адже семантика очевидна: число 36.6 — це температура в градусах Цельсія.

## explicit: явне перетворення

Явне перетворення вимагає від програміста написати cast явно: `(ТипРезультату)`. Це сигнал: «я свідомо роблю це перетворення і розумію наслідки».

Визначимо explicit-перетворення з `BodyTemperature` у `double` — вилучення числового значення температури:

```csharp run
using System;

// Виконуваний код
BodyTemperature t = new BodyTemperature(38.2);

// Явне перетворення: BodyTemperature → double (потрібен cast)
double celsius = (double)t;
Console.WriteLine($"Температура як число: {celsius}");

// Якщо написати просто: double c = t; — буде помилка компіляції
// (немає implicit оператора в цьому напрямку)

// Клас
class BodyTemperature
{
    public double Celsius { get; }

    public BodyTemperature(double celsius) => Celsius = celsius;

    // explicit: BodyTemperature → double (явно — бо "просто число" без контексту)
    public static explicit operator double(BodyTemperature t)
        => t.Celsius;

    public override string ToString() => $"{Celsius:F1}°C";
}
```

Чому тут `explicit`, а не `implicit`? Коли ми витягуємо `double` з `BodyTemperature`, результат втрачає семантичний контекст — це вже «просто число», а не температура. Програміст має явно підтвердити, що він хоче саме це. Якщо б перетворення було неявним, можна було б випадково отримати число там, де очікувався об'єкт `BodyTemperature`, і не помітити помилки.

## Перетворення між двома власними типами

Оператори перетворення можна визначити і між двома складовими типами. Розглянемо конвертацію між `BodyTemperature` (градуси Цельсія) і `FahrenheitTemperature` (градуси Фаренгейта) — типова задача в міжнародних клінічних системах:

```csharp run
using System;

// Виконуваний код
BodyTemperature celsius = new BodyTemperature(38.5);

// explicit: BodyTemperature → FahrenheitTemperature (формульне перетворення)
FahrenheitTemperature fahrenheit = (FahrenheitTemperature)celsius;
Console.WriteLine($"Цельсій:    {celsius}");
Console.WriteLine($"Фаренгейт:  {fahrenheit}");

// explicit: FahrenheitTemperature → BodyTemperature (назад)
BodyTemperature backToCelsius = (BodyTemperature)fahrenheit;
Console.WriteLine($"Назад:      {backToCelsius}");

// Клас температури в Цельсіях
class BodyTemperature
{
    public double Celsius { get; }

    public BodyTemperature(double celsius) => Celsius = celsius;

    // explicit → FahrenheitTemperature (формула: F = C * 9/5 + 32)
    public static explicit operator FahrenheitTemperature(BodyTemperature t)
        => new FahrenheitTemperature(t.Celsius * 9.0 / 5.0 + 32.0);

    public override string ToString() => $"{Celsius:F1}°C";
}

// Клас температури у Фаренгейтах
class FahrenheitTemperature
{
    public double Fahrenheit { get; }

    public FahrenheitTemperature(double fahrenheit) => Fahrenheit = fahrenheit;

    // explicit → BodyTemperature (формула: C = (F - 32) * 5/9)
    public static explicit operator BodyTemperature(FahrenheitTemperature f)
        => new BodyTemperature((f.Fahrenheit - 32.0) * 5.0 / 9.0);

    public override string ToString() => $"{Fahrenheit:F1}°F";
}
```

Обидва перетворення тут `explicit`, бо вони нетривіальні: задіяна формула, є заокруглення, і читач коду повинен бачити, що відбувається перетворення між системами вимірювання. Неявне перетворення тут приховало б важливий факт.

## Коли обирати implicit, а коли explicit

| Критерій | implicit | explicit |
|----------|----------|----------|
| Можлива втрата даних? | Ні | Так (або невідомо) |
| Семантика очевидна? | Так | Неочевидна або потребує уваги |
| Задіяна нетривіальна формула? | Ні | Так |
| Перетворення між різними одиницями вимірювання? | Ні | Так |
| Приклад у клінічному домені | `double` → `BodyTemperature` | `BodyTemperature` → `FahrenheitTemperature` |

Загальне правило: **якщо є хоч найменший сумнів — робіть explicit**. Явний cast у коді — це документація: він повідомляє читачеві, що тут відбувається свідоме перетворення типів.
