---
chapter: 9
chapterTitle: "Розділ 9. Pattern matching"
section: 4
number: "9.4"
title: "Позиційний патерн"
source: "../_combined/59-pozytsiinyi-patern.md"
---

## 9.4. Позиційний патерн

У секції 9.3 ми передавали у `switch` явно створений кортеж: `(specialty, shift) switch`. Але що якщо дані вже зібрані в об'єкт? Розбирати об'єкт на окремі змінні перед `switch` — зайва церемонія. **Позиційний патерн** вирішує це: він автоматично «розкладає» об'єкт через метод `Deconstruct` і потім зіставляє позиції — так само, як кортежний патерн.

## Механізм: Deconstruct як міст

Щоб об'єкт підтримував позиційний патерн, він повинен мати метод `Deconstruct` з `out`-параметрами. Компілятор виконує три кроки:

1. Викликає `obj.Deconstruct(out var p1, out var p2, ...)` — отримує набір `out`-значень.
2. Формує з цих значень тимчасовий кортеж позицій `[0]`, `[1]`, `[2]`...
3. Зіставляє кожну позицію з відповідним патерном у дужках `(pat1, pat2, ...)`.

Таким чином, позиційний патерн — це **кортежний патерн над об'єктом, що вміє себе деконструювати**. Зв'язок між 9.3 (кортежний) і 9.4 (позиційний) прямий: вони використовують один і той самий механізм зіставлення по позиції.

![Позиційний патерн: Deconstruct → кортеж → зіставлення](_assets/09-04/positional-pattern-flow.png)

## Зв'язок з record (8.10)

У розділі 8.10 ми дізнались, що позиційний `record` автоматично генерує `Deconstruct`. Це означає: **будь-який позиційний record вже підтримує позиційний патерн** без жодного додаткового коду:

```csharp
public record VitalSigns(double Temperature, int Pulse, int OxygenSat);

// Позиційний патерн одразу доступний:
vitals switch
{
    (> 38.5, > 100, _)        => "Жар і тахікардія",
    (_, _, < 90)              => "Гіпоксія",
    (>= 36.0 and <= 37.0, ..) => "Норма",
    _                         => "Потрібен огляд"
}
```

`record` і позиційний патерн — природна пара: record компактно описує структуру, позиційний патерн компактно описує умови на цю структуру.

## Приклад: record з позиційним патерном

```csharp run
using System;

// Виконуваний код
var measurements = new VitalSigns[]
{
    new(37.2, 72,  98),
    new(38.8, 105, 96),
    new(36.9, 68,  85),
    new(39.5, 95,  99),
};

foreach (var v in measurements)
    Console.WriteLine($"t={v.Temperature} p={v.Pulse} O2={v.OxygenSat}% → {Assess(v)}");

string Assess(VitalSigns v) => v switch
{
    // Позиційний патерн: [Temperature, Pulse, OxygenSat]
    (>= 39.0, > 90, _)             => "КРИТИЧНО: висока t° + тахікардія",
    (>= 38.5, _, _)                => "Жар — призначити жарознижуюче",
    (_, _, < 90)                   => "УВАГА: гіпоксія — кисень",
    (>= 36.0 and <= 37.0, < 100, >= 95) => "Норма — спостереження",
    (var t, var p, var o2)         => $"Стан: t={t:F1} p={p} O2={o2}%"
};

// record з автоматичним Deconstruct
public record VitalSigns(double Temperature, int Pulse, int OxygenSat);
```

У передостанньому arm `(>= 36.0 and <= 37.0, < 100, >= 95)` кожна позиція містить реляційний або логічний патерн. В останньому arm `(var t, var p, var o2)` — захоплення всіх позицій у змінні.

## Кастомний Deconstruct

Якщо клас не є record, `Deconstruct` визначається вручну — метод без типу результату (`void`) з параметрами `out`:

```csharp run
using System;

// Виконуваний код
var appointments = new Appointment[]
{
    new("Олег Петренко",   "Плановий",    "Кардіологія"),
    new("Марія Коваль",    "Ургентний",   "Хірургія"),
    new("Іван Сидоренко",  "Плановий",    "Неврологія"),
    new("Ганна Мельник",   "Ургентний",   "Реанімація"),
};

foreach (var a in appointments)
    Console.WriteLine($"{a.PatientName}: {GetPriority(a)}");

string GetPriority(Appointment a) => a switch
{
    // Позиційний патерн: [type, department]
    ("Ургентний", "Реанімація") => "НЕГАЙНО — реанімація",
    ("Ургентний", var dept)     => $"Терміново — {dept}",
    ("Плановий",  "Кардіологія")=> "Плановий + ЕКГ",
    ("Плановий",  var dept)     => $"Плановий — {dept}",
    _                           => "Невизначено"
};

// Клас з кастомним Deconstruct
class Appointment
{
    public string PatientName  { get; }
    public string Type         { get; }
    public string Department   { get; }

    public Appointment(string name, string type, string dept)
    { PatientName = name; Type = type; Department = dept; }

    // Deconstruct — розкладає на Type та Department
    public void Deconstruct(out string type, out string department)
    { type = Type; department = Department; }
}
```

Зверніть: `Deconstruct` розкриває лише `Type` і `Department` — не `PatientName`. Ми самі вирішуємо, які поля «виставити» позиційному патерну. Решту полів можна перевіряти через property pattern окремо або через `var` з подальшою умовою.

## Порівняння: кортежний vs позиційний патерн

| Аспект | Кортежний (9.3) | Позиційний (9.4) |
|--------|-----------------|-----------------|
| Вхід | явний кортеж `(a, b)` | об'єкт з `Deconstruct` |
| Вимога | будь-які два значення | `Deconstruct` в класі/record |
| Зв'язок | кортеж з 8.9 | record з 8.10 |
| Коли краще | незалежні зовнішні значення | вже є об'єкт з даними |

Якщо дані вже «живуть» в об'єкті — позиційний патерн. Якщо дані приходять як окремі змінні — кортежний.
