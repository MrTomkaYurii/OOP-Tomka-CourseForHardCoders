---
chapter: 2
chapterTitle: "Розділ 2. Основи програмування на C#"
section: 23
number: "2.23"
title: "Конструкція switch"
source: "../_migration/source-chunks/12-switch-ta-enum.md"
---

## 2.23. Конструкція switch

Конструкція `switch` призначена для порівняння одного виразу з набором фіксованих значень і виконання різних дій залежно від результату. Вона є структурованою альтернативою ланцюжку `if / else if / else` у тих ситуаціях, де потрібно обробити кілька конкретних варіантів одного значення. `switch` не лише читабельніший у таких сценаріях — він явно сигналізує читачу, що всі гілки обробляють одну змінну, а не довільні незалежні умови.

## Синтаксис switch/case

Формальна структура конструкції `switch`:

```text
switch (вираз)
{
    case значення1:
        код для значення1
        break;
    case значення2:
        код для значення2
        break;
    // ...
    default:
        код для всіх інших значень
        break;
}
```

Вираз у дужках після `switch` обчислюється один раз. Його значення послідовно порівнюється з кожним `case`. При збігу виконується відповідний блок коду. Наприкінці кожного `case` обов'язково стоїть оператор переходу — найчастіше `break`, який зупиняє виконання та виходить із `switch`.

![Потік виконання конструкції switch/case](_assets/02-23/switch-flow.png)

## Базовий приклад: тип відділення

```csharp run
using System;

string wardType = "Cardio";

switch (wardType)
{
    case "ICU":
        Console.WriteLine("Відділення: Інтенсивна терапія");
        break;
    case "Surgery":
        Console.WriteLine("Відділення: Хірургія");
        break;
    case "Cardio":
        Console.WriteLine("Відділення: Кардіологія");
        break;
    default:
        Console.WriteLine("Відділення: Загальна палата");
        break;
}
```

Значення `"Cardio"` збігається з третім `case`, виводиться відповідне повідомлення, `break` завершує конструкцію. Якщо `wardType` не збігається з жодним `case` — виконується блок `default`. Блок `default` необов'язковий, але його рекомендується додавати завжди як захисну гілку для непередбачених значень.

## Кілька значень для одного блоку

Якщо кілька значень мають обробляти однаковий код, їх `case`-мітки можна розміщувати поспіль без `break` між ними:

```csharp run
using System;

string diagnosis = "Bronchitis";

switch (diagnosis)
{
    case "Pneumonia":
    case "Bronchitis":
    case "Pleuritis":
        Console.WriteLine("Профіль: Пульмонологія");
        break;
    case "Infarction":
    case "Arrhythmia":
        Console.WriteLine("Профіль: Кардіологія");
        break;
    default:
        Console.WriteLine("Профіль: Терапія (загальний)");
        break;
}
```

Три `case`-мітки підряд (`Pneumonia`, `Bronchitis`, `Pleuritis`) без `break` між ними означають: якщо значення збігається з будь-яким із них — виконується один і той самий блок. Це єдиний дозволений в C# спосіб «провалитися» між `case`.

## Оператор goto case

Якщо після виконання одного `case` потрібно явно перейти до іншого (не наступного за списком), використовується `goto case`:

```csharp run
using System;

int priority = 1;

switch (priority)
{
    case 1:
        Console.WriteLine("КРИТИЧНИЙ пріоритет — негайна госпіталізація");
        goto case 2;
    case 2:
        Console.WriteLine("Виклик чергового лікаря");
        break;
    case 3:
        Console.WriteLine("Запис на прийом");
        break;
    default:
        Console.WriteLine("Стандартна черга");
        break;
}
```

При `priority == 1` спочатку виводиться повідомлення про критичний пріоритет, потім `goto case 2` перекидає виконання до блоку `case 2`. Використовувати `goto case` слід обережно — надмірне застосування ускладнює читання.

## switch у методах з return

Конструкцію `switch` зручно використовувати всередині методів для повернення різних значень. Оператор `return` у блоці `case` одночасно виходить із `switch` і з методу, тому `break` у таких блоках не потрібен:

```csharp run
using System;

string GetWardName(string code)
{
    switch (code)
    {
        case "ICU":     return "Інтенсивна терапія";
        case "SRG":     return "Хірургія";
        case "CARD":    return "Кардіологія";
        case "NEURO":   return "Неврологія";
        default:        return "Загальне відділення";
    }
}

Console.WriteLine(GetWardName("ICU"));
Console.WriteLine(GetWardName("CARD"));
Console.WriteLine(GetWardName("ORTHO"));
```

Компілятор перевіряє, що метод повертає значення при всіх можливих варіантах. Якщо відсутній `default` і жоден `case` не покриває всі можливі значення — виникне помилка компіляції.

## switch-вираз (switch expression)

C# надає компактний синтаксис для `switch`, що повертає значення — **switch-вираз**. Замість ключового слова `case` і `break` використовується оператор `=>`, а замість `default` — символ підкреслення `_`:

```csharp run
using System;

string GetWardName(string code) => code switch
{
    "ICU"   => "Інтенсивна терапія",
    "SRG"   => "Хірургія",
    "CARD"  => "Кардіологія",
    "NEURO" => "Неврологія",
    _       => "Загальне відділення"
};

Console.WriteLine(GetWardName("ICU"));
Console.WriteLine(GetWardName("CARD"));
Console.WriteLine(GetWardName("ORTHO"));
```

Switch-вираз є виразом, а не оператором — він обчислюється і повертає значення. Його можна використати безпосередньо в присвоєнні або у `return`. Результат кожної гілки — значення після `=>`, гілки розділяються комами, а не `break`.

![switch-оператор vs switch-вираз](_assets/02-23/switch-expr-vs-stmt.png)

Switch-вираз вимагає **вичерпності**: компілятор перевіряє, що покриті всі можливі значення. Якщо гілка `_` відсутня і вхідне значення не збігається з жодним `case` — під час виконання буде кинуто `SwitchExpressionException`. Тому для рядкових і числових типів гілка `_` практично завжди обов'язкова.

Ще приклад з обчисленням: switch-вираз може повертати не лише рядки, а будь-який тип:

```csharp run
using System;

double CalculateDrugDose(string drug, double weightKg)
{
    double dosePerKg = drug switch
    {
        "Aspirin"    => 10.0,
        "Ibuprofen"  => 5.0,
        "Paracetamol"=> 15.0,
        _            => 0.0
    };
    return weightKg * dosePerKg;
}

Console.WriteLine($"Аспірин 70 кг: {CalculateDrugDose("Aspirin", 70.0).ToString("F1")} мг");
Console.WriteLine($"Ібупрофен 60 кг: {CalculateDrugDose("Ibuprofen", 60.0).ToString("F1")} мг");
Console.WriteLine($"Невідомий: {CalculateDrugDose("Unknown", 70.0).ToString("F1")} мг");
```

Switch-вираз оцінює назву препарату і повертає дозу на кілограм, після чого обчислюється повна доза. Для невідомого препарату `_`-гілка повертає `0.0`, і результат коректно дорівнює нулю.
