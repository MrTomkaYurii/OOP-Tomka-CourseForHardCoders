---
chapter: 8
chapterTitle: "Розділ 8. Додаткові можливості ООП у C#"
section: 6
number: "8.6"
title: "Методи розширення"
---

## 8.6. Методи розширення

Уявіть ситуацію: вам потрібно додати корисний метод до класу `string` або структури `DateTime` — але ви не маєте доступу до їх вихідного коду і не можете успадкуватися від них (`string` — `sealed`-клас, а від структур успадковуватися неможливо взагалі). Або ви хочете додати утиліти до типів зі сторонньої бібліотеки, не чіпаючи її код. Саме для цього існують **методи розширення** (extension methods) — механізм, який дозволяє «додавати» нові методи до будь-якого типу ззовні, без зміни його вихідного коду.

Методи розширення — це не магія. За лаштунками вони залишаються звичайними статичними методами. Але компілятор дозволяє викликати їх через крапку, як ніби вони є рідними методами типу:

```csharp
double temp = 38.5;
bool hasFever = temp.IsFever(); // виглядає як метод double
// компілятор транслює це в:
bool hasFever = TemperatureExtensions.IsFever(temp);
```

Це **синтаксичний цукор** — зручний запис, що приховує звичайний статичний виклик.

## Синтаксис методу розширення

Метод розширення визначається у `public static` класі як `public static` метод. Перший параметр — особливий: він позначається ключовим словом `this` і вказує, який тип цей метод розширює. При виклику цей параметр не передається явно — компілятор підставляє значення зліва від крапки.

![Методи розширення: синтаксис і механізм компіляції](_assets/08-06/extension-method-anatomy.png)

```csharp
public static class TemperatureExtensions
{
    public static bool IsFever(this double celsius) => celsius > 37.5;
    //                         ^^^^ — розширюємо тип double
}
```

## Розширення вбудованих типів: double

Додамо кілька корисних методів до `double` для роботи з температурними показниками — типовий сценарій у клінічних системах:

```csharp run
using System;

// Виконуваний код
double morning  = 36.6;
double evening  = 38.2;
double critical = 40.1;

Console.WriteLine($"Ранкова {morning}°C — жар: {(morning.IsFever() ? "так" : "ні")}");
Console.WriteLine($"Вечірня {evening}°C — жар: {(evening.IsFever() ? "так" : "ні")}");
Console.WriteLine($"Критична {critical}°C — небезпечна: {(critical.IsDangerous() ? "так" : "ні")}");
Console.WriteLine($"37.8°C у Фаренгейтах: {37.8.ToFahrenheit():F1}°F");

// Статичний клас з методами розширення для double
public static class TemperatureExtensions
{
    public static bool IsFever(this double celsius)
        => celsius > 37.5;

    public static bool IsDangerous(this double celsius)
        => celsius > 39.5;

    public static double ToFahrenheit(this double celsius)
        => celsius * 9.0 / 5.0 + 32.0;
}
```

## Розширення вбудованих типів: string

Методи розширення особливо корисні для `string` — дозволяють додавати специфічну бізнес-логіку без успадкування. Додамо методи для роботи з медичними рядками:

```csharp run
using System;

// Виконуваний код
string diagnosis = "   гіпертонія ii ст.   ";
string code = "ICD-10";
string emptyCode = "";

Console.WriteLine($"Нормалізований діагноз: '{diagnosis.NormalizeDiagnosis()}'");
Console.WriteLine($"Код '{code}' валідний: {(code.IsValidMedicalCode() ? "так" : "ні")}");
Console.WriteLine($"Код '{emptyCode}' валідний: {(emptyCode.IsValidMedicalCode() ? "так" : "ні")}");
Console.WriteLine($"Скорочено: '{("Гострий інфаркт міокарда, ускладнений серцевою недостатністю").Truncate(30)}'");

// Статичний клас з методами розширення для string
public static class StringMedicalExtensions
{
    // Trim + нормалізація регістру
    public static string NormalizeDiagnosis(this string s)
        => string.IsNullOrWhiteSpace(s) ? "" : s.Trim().ToLower();

    // Простий код: не порожній і довший за 3 символи
    public static bool IsValidMedicalCode(this string s)
        => !string.IsNullOrWhiteSpace(s) && s.Trim().Length >= 3;

    // Обрізати до maxLen символів, додати "..."
    public static string Truncate(this string s, int maxLen)
    {
        if (s == null || s.Length <= maxLen) return s;
        return s.Substring(0, maxLen) + "...";
    }
}
```

## Розширення DateTime

Методи розширення для `DateTime` зручні для бізнес-логіки, яка не належить до самого класу `DateTime`, але часто потрібна в конкретному домені:

```csharp run
using System;

// Виконуваний код
DateTime appointment1 = new DateTime(2027, 6, 8, 10, 30, 0);  // вівторок, 10:30
DateTime appointment2 = new DateTime(2027, 6, 12, 19, 0, 0);  // субота, 19:00
DateTime appointment3 = new DateTime(2027, 6, 13, 8, 0, 0);   // неділя, 8:00

Console.WriteLine($"{appointment1:ddd HH:mm} — робочий час: {(appointment1.IsWorkingHours() ? "так" : "ні")}");
Console.WriteLine($"{appointment2:ddd HH:mm} — робочий час: {(appointment2.IsWorkingHours() ? "так" : "ні")}");
Console.WriteLine($"{appointment3:ddd HH:mm} — робочий час: {(appointment3.IsWorkingHours() ? "так" : "ні")}");

Console.WriteLine($"Днів до прийому: {appointment1.DaysUntil()}");

// Статичний клас з методами розширення для DateTime
public static class DateTimeClinicExtensions
{
    // Пн-Пт, 8:00–18:00
    public static bool IsWorkingHours(this DateTime dt)
        => dt.DayOfWeek >= DayOfWeek.Monday
        && dt.DayOfWeek <= DayOfWeek.Friday
        && dt.Hour >= 8 && dt.Hour < 18;

    // Кількість днів від сьогодні
    public static int DaysUntil(this DateTime dt)
        => (int)(dt.Date - DateTime.Today).TotalDays;
}
```

## Правила та обмеження

**Простір імен.** Методи розширення діють у межах простору імен (`namespace`). Якщо статичний клас із методами розширення знаходиться в іншому `namespace`, його потрібно підключити через `using`:

```csharp
using ClinicApp.Extensions; // підключаємо простір імен зі статик-класом

string code = "ICD-10";
bool valid = code.IsValidMedicalCode(); // тепер доступний
```

**Пріоритет instance-методу.** Якщо тип вже має метод із тією самою сигнатурою, що й метод розширення, буде викликаний **рідний метод** — метод розширення ігнорується. Ця поведінка захищає від випадкового перевизначення поведінки існуючого типу.

**Де доцільно використовувати extension methods:**

- Додавання утилітарних методів до типів, яких ми не контролюємо (`string`, `DateTime`, типи з бібліотек).
- Розширення `sealed`-класів, від яких не можна успадкуватися.
- Організація допоміжної логіки окремо від основного класу (принцип єдиної відповідальності).
- Побудова fluent API: `patient.GetAge().IsAdult().HasInsurance()`.

Варто знати: весь механізм **LINQ** (`Where`, `Select`, `OrderBy`, `GroupBy` тощо) реалізований саме через методи розширення для `IEnumerable<T>`. Коли ви пишете `list.Where(p => p.Age > 18)`, ви викликаєте статичний метод `Enumerable.Where(list, p => p.Age > 18)` — і це саме метод розширення.

## Члени розширення в C# 14

Класичний синтаксис дозволяє додати до типу лише **методи**. C# 14 (.NET 10) вводить **блоки розширення** (`extension`), у яких можна оголошувати також **властивості** і **статичні члени** розширеного типу:

```csharp
public static class TemperatureExtensions
{
    extension(double celsius)            // «приймач» — як this-параметр
    {
        public bool IsFever() => celsius >= 37.5;            // метод
        public bool IsNormalRange => celsius is >= 36.0 and <= 37.0; // властивість!
    }
}

// Використання:
double t = 36.6;
bool fever  = t.IsFever();   // false
bool normal = t.IsNormalRange;   // true — властивість без дужок
```

Для коду, що викликає, нічого не змінюється: це ті самі статичні члени статичного класу, а класичні методи з `this` і нові блоки сумісні між собою. Перевірено на .NET 10.

Одна пастка, знайдена під час перевірки: властивість спершу хотілося назвати `IsNormal`, але в `double` вже є **статичний** метод `double.IsNormal(double)`. Правило пріоритету діє й тут — член самого типу перемагає розширення, тому `t.IsNormal` компілятор прив'язує до групи методів `double.IsNormal`, і рядок не компілюється (CS1503). Звідси ім'я `IsNormalRange`.
