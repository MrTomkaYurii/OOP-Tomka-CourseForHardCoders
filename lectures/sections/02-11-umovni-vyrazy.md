---
chapter: 2
chapterTitle: "Розділ 2. Основи програмування на C#"
section: 11
number: "2.11"
title: "Умовні вирази"
source: "../_migration/source-chunks/07-umovni-vyrazy-ta-cykly.md"
---

## 2.11. Умовні вирази

Програми рідко виконуються лінійно від початку до кінця. Зазвичай потрібно приймати рішення: перевірити, чи вік пацієнта вписується в допустимий діапазон, чи є значення тиску критичним, чи не перевищено добову норму ліків. Для цього в C# існують **умовні вирази** — вирази, що повертають логічне значення типу `bool`: `true` (істина) або `false` (хибність). До умовних виразів належать оператори порівняння та логічні оператори.

![Умовні вирази C#: оператори порівняння та логічні оператори](_assets/02-11/conditional-ops.png)

## Оператори порівняння

Оператори порівняння порівнюють два операнди і повертають `bool`. Якщо твердження відповідає дійсності — результат `true`, інакше — `false`.

| Оператор | Значення              | Приклад           |
|----------|-----------------------|-------------------|
| `==`     | Рівність              | `age == 18`       |
| `!=`     | Нерівність            | `age != 0`        |
| `<`      | Менше ніж             | `age < 60`        |
| `>`      | Більше ніж            | `age > 18`        |
| `<=`     | Менше або рівно       | `age <= 110`      |
| `>=`     | Більше або рівно      | `age >= 0`        |

Оператори `<`, `>`, `<=`, `>=` мають вищий пріоритет ніж `==` і `!=`.

```csharp run
using System;

int age        = 45;
int criticalBp = 180;
int bpSystolic = 155;

Console.WriteLine($"Вік == 45: {(age == 45).ToString()}");
Console.WriteLine($"Вік != 18: {(age != 18).ToString()}");
Console.WriteLine($"Тиск < критичного: {(bpSystolic < criticalBp).ToString()}");
Console.WriteLine($"Вік >= 60 (пенсіонер): {(age >= 60).ToString()}");
```

## Логічні оператори

Логічні оператори об'єднують кілька умовних виразів в один. Усі вони приймають операнди типу `bool` і повертають `bool`.

### `&&` — логічне І (AND, кон'юнкція)

Повертає `true` лише тоді, коли **обидва** операнди дорівнюють `true`. Якщо хоч один — `false`, результат `false`.

```csharp run
using System;

int age        = 45;
int bpSystolic = 155;

bool isAdultNormalBp = age >= 18 && bpSystolic < 140;
bool isAdultHighBp   = age >= 18 && bpSystolic >= 140;

Console.WriteLine($"Дорослий і нормальний тиск: {isAdultNormalBp.ToString()}");
Console.WriteLine($"Дорослий і підвищений тиск: {isAdultHighBp.ToString()}");
```

### `||` — логічне АБО (OR, диз'юнкція)

Повертає `true`, якщо **хоча б один** операнд дорівнює `true`. `false` лише коли обидва — `false`.

```csharp run
using System;

int age = 8;

bool needsSpecialCare = age < 12 || age >= 70;
Console.WriteLine($"Потребує особливого догляду: {needsSpecialCare.ToString()}");
```

### `!` — логічне НЕ (NOT, заперечення)

Унарний оператор: інвертує значення. `!true` → `false`, `!false` → `true`.

```csharp run
using System;

bool isStableCondition = true;
bool isUnstable = !isStableCondition;
Console.WriteLine($"Нестабільний стан: {isUnstable.ToString()}");
```

### `^` — виключне АБО (XOR)

Повертає `true`, якщо операнди **різні**: один `true`, інший `false`. Якщо обидва однакові — повертає `false`.

```csharp run
using System;

bool hasFever    = true;
bool hasCough    = true;

bool onlyOneSym  = hasFever ^ hasCough;
Console.WriteLine($"Лише один симптом з двох: {onlyOneSym.ToString()}");
```

### `|` і `&` — операції без скорочення

C# також має пари `|` (логічне АБО) і `&` (логічне І), які на відміну від `||` і `&&` **завжди обчислюють обидва операнди**. Це принципова різниця.

У виразі `x || y`: якщо `x` вже є `true`, обчислення `y` пропускається — результат і так `true`. Аналогічно `x && y`: якщо `x` є `false`, обчислення `y` пропускається. Це називається **скороченим обчисленням** (short-circuit evaluation) і підвищує продуктивність.

```csharp run
using System;

int bpSystolic = 130;
int bpDiastolic = 85;

// && — якщо bpSystolic <= 140 вже false, bpDiastolic не перевіряється
bool isOptimal = bpSystolic <= 130 && bpDiastolic <= 80;
Console.WriteLine($"Оптимальний тиск: {isOptimal.ToString()}");

// & — обидва операнди завжди обчислюються
bool alsoOptimal = bpSystolic <= 130 & bpDiastolic <= 80;
Console.WriteLine($"Той самий результат: {alsoOptimal.ToString()}");
```

Оператори `|` і `&` зазвичай використовують для порозрядних операцій над цілими числами (що розглядалося в розділі 2.7). Для логічних перевірок умов застосовуйте `&&` і `||` — вони ефективніші.

## Комбінування умов

Умови можна поєднувати в складні вирази. Пріоритет: спочатку `!`, потім `<`, `>`, `<=`, `>=`, потім `==`, `!=`, потім `&`, потім `^`, потім `|`, потім `&&`, і нарешті `||`. Для ясності завжди використовуйте дужки:

```csharp run
using System;

int age        = 45;
int bpSystolic = 165;
bool hasDiabetes = true;

// Пацієнт у зоні ризику: або дуже високий тиск, або (старший 40 і діабет)
bool highRisk = bpSystolic >= 160 || (age > 40 && hasDiabetes);
Console.WriteLine($"Зона ризику: {highRisk.ToString()}");

// Допускається до операції: немає критичного тиску І не діабетик, або вік < 30
bool canOperate = (bpSystolic < 180 && !hasDiabetes) || age < 30;
Console.WriteLine($"Допуск до операції: {canOperate.ToString()}");
```

Результат умовного виразу — значення типу `bool`. Його можна зберігати у змінну, передавати в конструкції `if`, використовувати як аргумент методу або відразу виводити на екран.
