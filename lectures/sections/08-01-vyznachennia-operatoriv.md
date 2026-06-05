---
chapter: 8
chapterTitle: "Розділ 8. Додаткові можливості ООП у C#"
section: 1
number: "8.1"
title: "Визначення операторів"
source: "../_combined/46-vyznachennia-operatoriv.md"
---

## 8.1. Визначення операторів

Оператори `+`, `-`, `>`, `<`, `==` добре знайомі у контексті примітивних типів: `int`, `double`, `bool`. Але коли ми створюємо власний клас, компілятор не знає, що означає «скласти» або «порівняти» два об'єкти — адже у кожного класу своя семантика. **Перевантаження операторів** (operator overloading) — це механізм, який дозволяє визначити власну логіку для стандартних операторів стосовно об'єктів нашого типу.

Уявіть клінічну систему, де потрібно порівнювати температуру тіла двох пацієнтів або відстежувати її зміну після прийому жарознижуючого. Без перевантаження код виглядає громіздко і прив'язаний до деталей реалізації:

```csharp
if (patient1.Temperature.Celsius > patient2.Temperature.Celsius) { ... }
double change = afterMed.Temperature.Celsius - beforeMed.Temperature.Celsius;
```

З перевантаженням — читабельно і природно, як у математиці:

```csharp
if (tempAfter > tempBefore) { ... }
double change = tempAfter - tempBefore;
```

Перевантаження операторів не змінює їх пріоритет, не додає нових символів і не змінює правил мови — воно лише визначає, що відбувається, коли стандартний символ застосовується до об'єктів нашого типу.

## Механізм: як компілятор знаходить оператор

Коли компілятор зустрічає вираз `t1 + delta`, де `t1` має тип `BodyTemperature`, він шукає у цьому класі статичний метод із підходящою сигнатурою:

```csharp
public static BodyTemperature operator+(BodyTemperature t, double delta)
```

Якщо такий метод є — вираз `t1 + delta` автоматично перетворюється на виклик `BodyTemperature.operator+(t1, delta)`. Якщо немає — помилка компіляції. Це і є «синтаксичний цукор»: зручний запис оператором, за яким приховується звичайний виклик статичного методу.

![Перевантаження оператора: від виразу до виклику методу](_assets/08-01/operator-mechanism.png)

## Синтаксис визначення оператора

Оператор визначається як спеціальний метод у тілі класу або структури:

```csharp
public static ТипРезультату operator СИМВОЛ(параметр1[, параметр2])
{
    // логіка
}
```

**Обов'язкові вимоги:**

- Модифікатори `public static` — оператор є методом типу, а не конкретного екземпляра.
- Ключове слово `operator` перед символом оператора.
- Принаймні один параметр повинен мати тип класу або структури, де визначається оператор.
- Бінарні оператори (два операнди) — приймають два параметри.
- Унарні оператори (один операнд) — приймають один параметр.
- Тип результату може бути будь-яким: тим самим класом, `bool`, `double`, будь-яким іншим.

## Клінічний приклад: клас BodyTemperature

Розглянемо клас `BodyTemperature`, що представляє температуру тіла пацієнта. Цей клас — наочний приклад для перевантаження: температури порівнюють (чи є жар?), обчислюють різницю (наскільки знизилась?), застосовують зсув (зросла на 0.5°C).

### Арифметичні оператори

Визначимо два оператори: `+` для зсуву температури на задану величину і `-` для обчислення різниці між двома вимірами. Зверніть увагу, що вони повертають різні типи — `BodyTemperature` і `double` відповідно, адже семантика операцій різна:

```csharp run
using System;

class BodyTemperature
{
    public double Celsius { get; }

    public BodyTemperature(double celsius) => Celsius = celsius;

    // Зсув температури: 36.6 + 0.5 → нова температура 37.1
    public static BodyTemperature operator +(BodyTemperature t, double delta)
    {
        return new BodyTemperature(t.Celsius + delta);
    }

    // Різниця між двома вимірами: повертає double, не BodyTemperature
    public static double operator -(BodyTemperature t1, BodyTemperature t2)
    {
        return t1.Celsius - t2.Celsius;
    }

    public override string ToString() => $"{Celsius:F1}°C";
}

BodyTemperature morning = new BodyTemperature(36.6);
BodyTemperature evening = new BodyTemperature(37.8);

// Зсув — наприклад, після фізичного навантаження
BodyTemperature afterExercise = morning + 0.8;
Console.WriteLine($"Після навантаження: {afterExercise}");

// Різниця між вечірнім і ранковим вимірами
double delta = evening - morning;
Console.WriteLine($"Приріст за день: {delta:+0.0;-0.0}°C");
```

Тип результату оператора — не обов'язково той самий клас. Оператор `-` між двома `BodyTemperature` повертає `double`, бо різниця температур — числова величина, а не нова температура. Тип результату визначається семантикою операції.

Оскільки в операторі `+` перший параметр — `BodyTemperature`, а другий — `double`, вираз `morning + 0.8` коректний. Але `0.8 + morning` вже не компілюється — параметри не збігаються в потрібному порядку. Якщо потрібно, можна визначити ще один перевантажений варіант із переставленими параметрами.

### Оператори порівняння

Порівняння — найчастіший сценарій у клінічних системах: «чи є у пацієнта жар?», «яка температура вища?». Визначимо чотири оператори порівняння:

```csharp run
using System;

class BodyTemperature
{
    public double Celsius { get; }
    public bool IsFever => Celsius > 37.5;

    public BodyTemperature(double celsius) => Celsius = celsius;

    public static bool operator >(BodyTemperature t1, BodyTemperature t2)
        => t1.Celsius > t2.Celsius;

    public static bool operator <(BodyTemperature t1, BodyTemperature t2)
        => t1.Celsius < t2.Celsius;

    public static bool operator ==(BodyTemperature t1, BodyTemperature t2)
        => Math.Abs(t1.Celsius - t2.Celsius) < 0.05;

    public static bool operator !=(BodyTemperature t1, BodyTemperature t2)
        => !(t1 == t2);

    public override string ToString() => $"{Celsius:F1}°C";
    public override bool Equals(object obj) => obj is BodyTemperature t && this == t;
    public override int GetHashCode() => Math.Round(Celsius, 1).GetHashCode();
}

BodyTemperature t1 = new BodyTemperature(38.2);
BodyTemperature t2 = new BodyTemperature(36.9);
BodyTemperature t3 = new BodyTemperature(38.2);

Console.WriteLine($"{t1} > {t2}: {(t1 > t2 ? "так" : "ні")}");
Console.WriteLine($"{t1} < {t2}: {(t1 < t2 ? "так" : "ні")}");
Console.WriteLine($"{t1} == {t3}: {(t1 == t3 ? "так" : "ні")}");
Console.WriteLine($"Пацієнт має жар: {(t1.IsFever ? "так" : "ні")}");
```

Зверніть увагу на оператор `==`: замість строгого `t1.Celsius == t2.Celsius` використовується допуск `0.05`. Це важливо для чисел із плаваючою крапкою — через особливості їх бінарного представлення два «однакові» значення після арифметичних операцій можуть трохи відрізнятись.

### Повний клас у клінічному сценарії

Об'єднаємо всі оператори в повному класі і побачимо, як природно вони виглядають у реальному коді:

```csharp run
using System;

class BodyTemperature
{
    public double Celsius { get; }

    public bool IsNormal    => Celsius >= 36.0 && Celsius <= 37.0;
    public bool IsFever     => Celsius > 37.5;
    public bool IsHighFever => Celsius > 39.0;

    public BodyTemperature(double celsius)
    {
        if (celsius < 30.0 || celsius > 45.0)
            throw new ArgumentOutOfRangeException(nameof(celsius));
        Celsius = celsius;
    }

    public static BodyTemperature operator +(BodyTemperature t, double delta)
        => new BodyTemperature(t.Celsius + delta);

    public static BodyTemperature operator -(BodyTemperature t, double delta)
        => new BodyTemperature(t.Celsius - delta);

    public static double operator -(BodyTemperature t1, BodyTemperature t2)
        => t1.Celsius - t2.Celsius;

    public static bool operator >(BodyTemperature t1, BodyTemperature t2)
        => t1.Celsius > t2.Celsius;

    public static bool operator <(BodyTemperature t1, BodyTemperature t2)
        => t1.Celsius < t2.Celsius;

    public static bool operator ==(BodyTemperature t1, BodyTemperature t2)
        => Math.Abs(t1.Celsius - t2.Celsius) < 0.05;

    public static bool operator !=(BodyTemperature t1, BodyTemperature t2)
        => !(t1 == t2);

    public override string ToString() =>
        IsHighFever ? $"{Celsius:F1}°C (висока!)" :
        IsFever     ? $"{Celsius:F1}°C (жар)"     :
        IsNormal    ? $"{Celsius:F1}°C (норма)"   :
                      $"{Celsius:F1}°C";

    public override bool Equals(object obj) => obj is BodyTemperature t && this == t;
    public override int GetHashCode() => Math.Round(Celsius, 1).GetHashCode();
}

// Клінічний сценарій: вимірювання до і після прийому жарознижуючого
BodyTemperature before = new BodyTemperature(39.4);
BodyTemperature after  = new BodyTemperature(37.1);

Console.WriteLine($"До прийому:    {before}");
Console.WriteLine($"Після прийому: {after}");

double drop = before - after;
Console.WriteLine($"Зниження: {drop:F1}°C");

Console.WriteLine($"Температура нормалізувалась: {(after.IsNormal ? "так" : "ні")}");

// Через 2 години температура трохи підвищилась
BodyTemperature twoHoursLater = after + 0.4;
Console.WriteLine($"Через 2 год: {twoHoursLater}");
Console.WriteLine($"Потрібен повторний прийом: {(twoHoursLater > after ? "так" : "ні")}");
```

## Парні оператори

Деякі оператори компілятор вимагає визначати **парами**. Якщо ви визначаєте один — необхідно визначити і другий:

| Пара | Причина |
|------|---------|
| `>` і `<` | Логічна симетрія: якщо `a > b`, то `b < a` |
| `>=` і `<=` | Аналогічно |
| `==` і `!=` | Якщо об'єкти рівні, то вони не нерівні |

Ця вимога вбудована в компілятор — він не дозволить визначити `>` без `<`. Мета обмеження — запобігти логічним суперечностям: ситуації, коли `a > b` і `a < b` обидва повертають `false`, або коли `a == b` і `a != b` обидва повертають `true`.

При перевантаженні `==` компілятор також рекомендує перевизначити `Equals(object)` і `GetHashCode()`. Причина: за замовчуванням ці методи порівнюють посилання, а не значення. Якщо залишити їх без змін, поведінка стає непослідовною — `==` порівнює значення, а `Equals()` — посилання на об'єкт у пам'яті.

## Таблиця операторів, що підтримують перевантаження

| Категорія | Оператори | Примітка |
|-----------|-----------|----------|
| Унарні | `+x`, `-x`, `!`, `~`, `++`, `--`, `true`, `false` | `true`/`false` — для умовних виразів |
| Арифметичні | `+`, `-`, `*`, `/`, `%` | — |
| Порівняння | `==`, `!=`, `<`, `>`, `<=`, `>=` | Тільки парами |
| Порозрядні | `&`, `\|`, `^`, `<<`, `>>`, `>>>` | — |
| Логічні | `&&`, `\|\|` | Визначаються через `&`, `\|`, `true`, `false` |

Оператори присвоєння (`=`, `+=`, `-=` тощо), тернарний `?:`, оператор доступу `.` та `?.` перевантажити **неможливо**. При цьому `+=` та `-=` автоматично використовують перевантажений `+` і `-` — визначати їх окремо не потрібно.

## Коли варто, а коли не варто перевантажувати оператори

**Варто**, якщо:
- Тип моделює математичне або фізичне поняття: температура, відстань, маса, координата, інтервал часу.
- Оператор має очевидну і однозначну інтерпретацію для цього типу.
- Код з оператором читається так само природно, як математичний вираз.

**Не варто**, якщо:
- Семантика оператора неочевидна або може трактуватись по-різному.
- Ви перевантажуєте оператор виключно заради стислості — без виграшу в читабельності.
- Тип не є «значеннєвим» поняттям. Для сутностей-ідентичностей — пацієнт, лікар, прийом — оператор `+` між двома об'єктами не має природного змісту.

Перевантаження операторів — інструмент виразності, а не синтаксичний трюк. Добре спроектований оператор робить код читабельнішим; поганий вносить плутанину і ускладнює підтримку.
