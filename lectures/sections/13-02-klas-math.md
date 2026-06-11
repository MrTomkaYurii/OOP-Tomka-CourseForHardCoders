---
chapter: 13
chapterTitle: "Розділ 13. Додаткові класи та структури .NET"
section: 2
number: "13.2"
title: "Клас Math"
source: "../_combined/79-klas-math.md"
---

## 13.2. Клас `Math`

Обчислення в медичних інформаційних системах пронизують усі рівні застосунку: розрахунок ІМТ пацієнта, дозування препаратів, перетворення одиниць вимірювання, побудова статистичних показників. Для всіх цих потреб .NET надає статичний клас `Math` із простору імен `System` — набір математичних функцій і констант, готових до використання без будь-яких додаткових просторів імен.

`Math` є **запечатаним статичним класом** (`static sealed class`): неможливо ані успадкувати від нього, ані створити екземпляр — усі члени викликаються безпосередньо через ім'я класу: `Math.Round(...)`, `Math.Sqrt(...)`. Це проектне рішення .NET: математичні операції не потребують стану, тому клас-бібліотека з набором чистих функцій є найпростішим і найефективнішим підходом.

![Клас Math — огляд методів](_assets/13-02/math-overview.png)

## Константи Math.PI та Math.E

Клас `Math` надає дві фундаментальні математичні константи як `public const double`:

```csharp
Console.WriteLine(Math.PI);  // 3.141592653589793
Console.WriteLine(Math.E);   // 2.718281828459045
Console.WriteLine(Math.Tau); // 6.283185307179586 = 2 * PI  (.NET 5+)
```

`Math.PI` — відношення довжини кола до діаметра, використовується в задачах геометрії і тригонометрії. `Math.E` — основа натурального логарифму, з'являється в формулах неперервного нарахування відсотків, нормального розподілу, ентропії. `Math.Tau = 2π` — конвенція, що з'явилась у .NET 5: в багатьох формулах зручніше оперувати одним повним обертом τ замість «2π».

## Округлення: чотири різні методи

Округлення — одна з найбільш пастяних операцій у C#. Стандарт IEEE 754 для `double` і стандарт ISO банківської математики дають різні результати на межових значеннях (x.5), тому `Math` надає кілька різних методів.

### Math.Floor та Math.Ceiling

`Math.Floor(x)` — **округлення вниз** до найближчого цілого, не більшого за `x`. Математично: ⌊x⌋. Для від'ємних чисел «вниз» означає далі від нуля:

```csharp
Console.WriteLine(Math.Floor(2.7));  // 2
Console.WriteLine(Math.Floor(2.1));  // 2
Console.WriteLine(Math.Floor(-2.7)); // -3  (до -∞, не до 0!)
```

`Math.Ceiling(x)` — **округлення вгору** до найближчого цілого, не меншого за `x`. Математично: ⌈x⌉:

```csharp
Console.WriteLine(Math.Ceiling(2.1));  // 3
Console.WriteLine(Math.Ceiling(2.0));  // 2
Console.WriteLine(Math.Ceiling(-2.1)); // -2  (до +∞)
```

У медичних розрахунках `Floor` і `Ceiling` з'являються, коли потрібно визначити кількість повних одиниць: «скільки повних днів пройшло», «скільки повних таблеток в упаковці по N мг».

### Math.Truncate

`Math.Truncate(x)` відкидає дробову частину, завжди **до нуля**. На відміну від `Floor`, для від'ємних чисел вони різняться:

```csharp
Console.WriteLine(Math.Truncate(2.9));  // 2
Console.WriteLine(Math.Truncate(-2.9)); // -2  (не -3 як Floor!)
```

### Math.Round — банківське заокруглення за замовчуванням

`Math.Round(x)` за замовчуванням застосовує **банківське заокруглення** (MidpointRounding.ToEven): на межовому значенні x.5 округлюється до **найближчого парного**:

```csharp
Console.WriteLine(Math.Round(2.5)); // 2  — до парного
Console.WriteLine(Math.Round(3.5)); // 4  — до парного
Console.WriteLine(Math.Round(4.5)); // 4  — до парного
Console.WriteLine(Math.Round(5.5)); // 6  — до парного
```

Це стандарт IEEE 754 і банківської математики: при великих вибірках сума помилок округлення прямує до нуля. Але «шкільне» правило «.5 завжди вгору» виглядає інакше:

```csharp
Console.WriteLine(Math.Round(2.5, MidpointRounding.AwayFromZero)); // 3
Console.WriteLine(Math.Round(3.5, MidpointRounding.AwayFromZero)); // 4
```

Другий параметр `Math.Round(x, n)` задає кількість знаків після коми:

```csharp
Console.WriteLine(Math.Round(3.14159, 2));  // 3.14
Console.WriteLine(Math.Round(3.14159, 4));  // 3.1416
```

Для медичних доз важливо знати, яке саме заокруглення застосовується: помилка заокруглення, що накопичується через сотні пацієнтів, може призводити до систематичних відхилень у статистиці.

## Абсолютне значення та знак

`Math.Abs(x)` повертає модуль числа: `Math.Abs(-7.5) == 7.5`. Перевантажений для всіх числових типів: `int`, `long`, `double`, `decimal` тощо.

`Math.Sign(x)` повертає `-1`, `0` або `1` залежно від знаку аргументу:

```csharp
Console.WriteLine(Math.Sign(-15));  // -1
Console.WriteLine(Math.Sign(0));    //  0
Console.WriteLine(Math.Sign(3.7));  //  1
```

Це корисно, коли потрібно визначити **напрям відхилення** від норми без знання абсолютної величини. Наприклад: `Math.Sign(actual - norm)` повертає `+1` якщо показник вище норми, `-1` якщо нижче, `0` якщо рівний.

`Math.CopySign(magnitude, sign)` (.NET 6+) повертає число з абсолютним значенням `magnitude` і знаком `sign`:

```csharp
Console.WriteLine(Math.CopySign(5.0, -1.0)); // -5
Console.WriteLine(Math.CopySign(5.0, 1.0));  // 5
```

## Min, Max та Clamp

`Math.Min(a, b)` і `Math.Max(a, b)` — найпростіші операції порівняння, перевантажені для всіх числових типів:

```csharp
int age   = Math.Max(0, inputAge);  // негативний вік неможливий
double bmi = Math.Min(calculatedBmi, 99.9); // обмеження відображення
```

`Math.Clamp(value, min, max)` (.NET Core 2.0+) — **обмеження значення в діапазон**: якщо `value < min`, повертає `min`; якщо `value > max`, повертає `max`; інакше повертає `value`:

```csharp
int percent = Math.Clamp(rawValue, 0, 100);
double dose = Math.Clamp(calculatedDose, minDose, maxDose);
```

Це надзвичайно корисна операція в медичних системах: кожен показник має допустимий діапазон, і `Clamp` дозволяє безпечно обмежити значення без громіздкого `if`:

```csharp
// Без Clamp:
if (dose < 0.5) dose = 0.5;
else if (dose > 10.0) dose = 10.0;

// З Clamp:
dose = Math.Clamp(dose, 0.5, 10.0);
```

## Степені та корені

`Math.Pow(base, exp)` — піднесення до степеня. Обидва аргументи і результат — `double`:

```csharp
Console.WriteLine(Math.Pow(2, 10));   // 1024
Console.WriteLine(Math.Pow(9, 0.5));  // 3.0  (= Math.Sqrt(9))
Console.WriteLine(Math.Pow(10, -2));  // 0.01
```

`Math.Sqrt(x)` — квадратний корінь (square root). Швидший спеціалізований варіант, ніж `Math.Pow(x, 0.5)`:

```csharp
double bmi = weight / Math.Pow(heightMeters, 2); // зріст у квадраті
```

`Math.Cbrt(x)` (.NET 5+) — кубічний корінь. На відміну від `Math.Pow(x, 1.0/3.0)`, коректно обробляє від'ємні числа:

```csharp
Console.WriteLine(Math.Cbrt(27));  // 3
Console.WriteLine(Math.Cbrt(-8)); // -2  (Pow(-8, 1.0/3.0) → NaN!)
```

Логарифми:

```csharp
Console.WriteLine(Math.Log(Math.E));   // 1.0   — натуральний ln
Console.WriteLine(Math.Log(100, 10));  // 2.0   — log₁₀(100)
Console.WriteLine(Math.Log2(8));       // 3.0   — log₂(8)
Console.WriteLine(Math.Log10(1000));   // 3.0
```

## Тригонометрія та радіани

Усі тригонометричні функції `Math` приймають аргумент **у радіанах**, а не градусах. Перетворення: `radians = degrees * Math.PI / 180`:

```csharp
double degrees = 90;
double radians = degrees * Math.PI / 180;

Console.WriteLine(Math.Sin(radians)); // 1.0
Console.WriteLine(Math.Cos(radians)); // 6.12e-17 ≈ 0 (похибка floating-point)
Console.WriteLine(Math.Tan(Math.PI / 4)); // 1.0  (tan(45°))
```

Обернені функції повертають радіани:

```csharp
double angle = Math.Asin(1.0);  // π/2 ≈ 1.5707...
Console.WriteLine(angle * 180 / Math.PI); // 90 градусів
```

## Перевірка особливих значень double

При математичних обчисленнях можуть виникати спеціальні значення `double`:
- `0.0 / 0.0 → double.NaN` (Not a Number)
- `1.0 / 0.0 → double.PositiveInfinity`
- `-1.0 / 0.0 → double.NegativeInfinity`

Ці значення не кидають виняток — вони **поширюються**: `NaN + 5 == NaN`, `Infinity * 2 == Infinity`. Тому перед використанням результату обчислення слід перевіряти:

```csharp
double result = weight / (height * height);

if (!double.IsFinite(result))
{
    Console.WriteLine("Некоректні вхідні дані");
    return;
}
```

```csharp
double.IsNaN(x)       // true якщо NaN
double.IsInfinity(x)  // true якщо +∞ або -∞
double.IsFinite(x)    // true якщо звичайне скінченне число (не NaN, не Inf)
```

`double.IsFinite` — найзручніша перевірка «чи придатне це значення для подальших розрахунків».

## Розрахунок ІМТ — runnable приклад

Обчислення ІМТ (Індекс маси тіла) за формулою ВООЗ: BMI = вага (кг) / зріст² (м):

```csharp run
using System;

static string BmiCategory(double bmi)
{
    if (bmi < 18.5) return "Недостатня маса";
    if (bmi < 25.0) return "Норма";
    if (bmi < 30.0) return "Надмірна вага";
    if (bmi < 35.0) return "Ожиріння I ст.";
    return "Ожиріння II+ ст.";
}

var patients = new[]
{
    ("Петренко Іван",  72.0, 1.78),
    ("Коваль Марія",   55.0, 1.62),
    ("Сидоренко Олег", 105.0, 1.75),
    ("Бойко Тетяна",   48.0, 1.68),
};

Console.WriteLine($"{"Пацієнт",-22} {"Вага",6} {"Зріст",6} {"ІМТ",6}  Категорія");
Console.WriteLine(new string('-', 65));

double totalBmi = 0;
foreach (var (name, weight, height) in patients)
{
    double bmi = weight / Math.Pow(height, 2);
    double bmiRounded = Math.Round(bmi, 1);
    totalBmi += bmi;

    // Clamp для відображення: візуальний індикатор обмежений 0-100
    int bar = Math.Clamp((int)bmi, 0, 50);
    string category = BmiCategory(bmi);

    Console.WriteLine($"{name,-22} {weight,6:F1} {height,6:F2} {bmiRounded,6:F1}  {category}");
}

double avg = totalBmi / patients.Length;
Console.WriteLine(new string('-', 65));
Console.WriteLine($"Середній ІМТ по групі: {Math.Round(avg, 1):F1}");

// Демонстрація IsFinite: захист від нульового зросту
Console.WriteLine("\n=== Перевірка некоректних даних ===");
double badHeight = 0.0;
double badBmi = 70.0 / Math.Pow(badHeight, 2);
Console.WriteLine($"70кг / 0м² = {badBmi}");
Console.WriteLine($"IsFinite: {double.IsFinite(badBmi)}");
Console.WriteLine($"IsInfinity: {double.IsInfinity(badBmi)}");
```

## Округлення та математичні функції — runnable приклад

Демонстрація всіх режимів округлення та функцій степеня/кореня:

```csharp run
using System;

Console.WriteLine("=== Порівняння методів округлення ===");
double[] values = { 2.5, 3.5, -2.5, 2.4, 2.6 };

Console.WriteLine($"{"Значення",10} {"Floor",8} {"Ceiling",9} {"Truncate",10} {"Round(ToEven)",15} {"Round(Away0)",13}");
Console.WriteLine(new string('-', 68));

foreach (double v in values)
{
    Console.WriteLine(
        $"{v,10:F1}" +
        $"{Math.Floor(v),8:F0}" +
        $"{Math.Ceiling(v),9:F0}" +
        $"{Math.Truncate(v),10:F0}" +
        $"{Math.Round(v),15:F0}" +
        $"{Math.Round(v, MidpointRounding.AwayFromZero),13:F0}"
    );
}

Console.WriteLine("\n=== Степінь, корінь, логарифм ===");
Console.WriteLine($"Math.Pow(2, 10)  = {Math.Pow(2, 10)}");
Console.WriteLine($"Math.Sqrt(144)   = {Math.Sqrt(144)}");
Console.WriteLine($"Math.Cbrt(125)   = {Math.Cbrt(125)}");
Console.WriteLine($"Math.Log10(1000) = {Math.Log10(1000)}");
Console.WriteLine($"Math.Log2(64)    = {Math.Log2(64)}");

Console.WriteLine("\n=== Abs, Sign, Min, Max, Clamp ===");
int heartRate = 210; // некоректне значення
int clamped = Math.Clamp(heartRate, 40, 200);
Console.WriteLine($"ЧСС отримано: {heartRate} уд/хв");
Console.WriteLine($"Math.Clamp(210, 40, 200) = {clamped} уд/хв");

double deviation = -4.7;
Console.WriteLine($"\nВідхилення від норми: {deviation}");
Console.WriteLine($"Math.Abs:  {Math.Abs(deviation):F1}");
Console.WriteLine($"Math.Sign: {Math.Sign(deviation)}  (−1 = нижче норми)");

Console.WriteLine("\n=== Тригонометрія: 30, 60, 90 градусів ===");
int[] degrees = { 30, 60, 90 };
foreach (int deg in degrees)
{
    double rad = deg * Math.PI / 180;
    Console.WriteLine($"sin({deg}°) = {Math.Round(Math.Sin(rad), 4),8}   cos({deg}°) = {Math.Round(Math.Cos(rad), 4),8}");
}
```
