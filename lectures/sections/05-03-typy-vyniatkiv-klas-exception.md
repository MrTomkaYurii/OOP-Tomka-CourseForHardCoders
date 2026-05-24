---
chapter: 5
chapterTitle: "Розділ 5. Обробка винятків"
section: 3
number: "5.3"
title: "Типи винятків. Клас Exception"
source: "../_combined/30-typy-vyniatkiv-klas-exception.md"
---

## 5.3. Типи винятків. Клас Exception

Кожен виняток у C# — це об'єкт. Усі класи винятків успадковуються від базового класу `System.Exception`. Це означає, що кожен виняток гарантовано містить набір стандартних властивостей з інформацією про помилку, а `catch (Exception ex)` здатен перехопити будь-який виняток у системі.

## Клас Exception та його властивості

`System.Exception` визначає кілька ключових властивостей:

| Властивість | Тип | Що містить |
|-------------|-----|-----------|
| `Message` | `string` | Текстовий опис помилки |
| `StackTrace` | `string` | Стек викликів на момент винятку |
| `InnerException` | `Exception?` | Виняток, що спричинив поточний (якщо є) |
| `TargetSite` | `MethodBase?` | Метод, у якому виник виняток |
| `Source` | `string?` | Назва збірки або об'єкта-джерела |

```csharp run
using System;

try
{
    string input = "не_число";
    int age = int.Parse(input);
    Console.WriteLine($"Вік: {age.ToString()} р.");
}
catch (Exception ex)
{
    Console.WriteLine($"Тип:      {ex.GetType().Name}");
    Console.WriteLine($"Повідомлення: {ex.Message}");
    Console.WriteLine($"Метод:    {ex.TargetSite}");
}
```

Властивість `ex.GetType().Name` показує реальний тип винятку — тут це буде `FormatException`, хоча перехоплюємо через базовий `Exception`. Це корисно для логування: ми отримуємо і конкретний тип, і загальні властивості.

## Ієрархія типів винятків

![Ієрархія класу Exception та поширені похідні типи](_assets/05-03/exception-hierarchy.png)

У .NET існує багато спеціалізованих класів винятків. Кожен відповідає за конкретну категорію помилок. Найпоширеніші:

| Тип | Коли виникає |
|-----|-------------|
| `FormatException` | Некоректний формат рядка при `Parse` |
| `OverflowException` | Переповнення числового типу |
| `DivideByZeroException` | Ділення цілого числа на нуль |
| `IndexOutOfRangeException` | Вихід за межі масиву або рядка |
| `NullReferenceException` | Звернення до `null`-посилання |
| `InvalidCastException` | Неприпустиме явне перетворення типів |
| `ArgumentException` | Некоректний аргумент методу |
| `ArgumentOutOfRangeException` | Аргумент поза допустимим діапазоном |

Усі вони є похідними від `Exception`, тому `catch (Exception ex)` перехопить кожен із них.

## Кілька блоків catch для різних типів

Якщо у блоці `try` можуть виникнути різні типи помилок, варто обробляти їх окремо — це дозволяє давати більш точні повідомлення та вживати відповідних заходів:

```csharp run
using System;

ProcessRecord("P-001", "45");    // коректно
ProcessRecord("P-002", "abc");   // FormatException
ProcessRecord("P-003", "");      // FormatException (порожній рядок)

void ProcessRecord(string id, string ageInput)
{
    try
    {
        int age = int.Parse(ageInput);

        string[] allowedIds = { "P-001", "P-003" };
        int idx = Array.IndexOf(allowedIds, id);

        if (allowedIds[idx] != id)   // IndexOutOfRangeException якщо idx == -1
            throw new ArgumentException($"ID {id} не знайдено");

        Console.WriteLine($"[{id}] Вік: {age.ToString()} р. — запис збережено.");
    }
    catch (FormatException ex)
    {
        Console.WriteLine($"[{id}] Некоректний вік: {ex.Message}");
    }
    catch (IndexOutOfRangeException)
    {
        Console.WriteLine($"[{id}] Запис не знайдено у системі.");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"[{id}] Непередбачена помилка: {ex.Message}");
    }
}
```

CLR перевіряє блоки `catch` зверху вниз і виконує **перший**, тип якого відповідає типу винятку. Після цього решта блоків ігнорується.

## Один виняток зупиняє виконання try

Важливо розуміти: як тільки в `try` виникає виняток, всі рядки після нього **не виконуються**. CLR негайно передає керування відповідному `catch`:

```csharp run
using System;

string[] names   = { "Іван Петренко", "Марія Сидоренко" };
string[] ageStrs = { "45", "abc" };

try
{
    for (int i = 0; i < names.Length; i++)
    {
        int age = int.Parse(ageStrs[i]);         // FormatException на i==1
        Console.WriteLine($"{names[i]}: {age.ToString()} р.");
        // рядок нижче не виконається після винятку
    }
    Console.WriteLine("Всі записи оброблено.");  // пропускається
}
catch (FormatException ex)
{
    Console.WriteLine($"Помилка: {ex.Message}");
}

Console.WriteLine("Програма завершила роботу.");
```

Рядок `"Всі записи оброблено."` ніколи не виведеться, якщо виняток виник до кінця циклу. Рядок після всього блоку `try...catch` — `"Програма завершила роботу."` — виведеться завжди, оскільки виняток було перехоплено.

## Необроблений виняток аварійно завершує програму

Якщо тип винятку не відповідає жодному `catch` — виняток не перехоплюється. CLR пробуджує обробники вище по стеку, і якщо ніхто не перехопив — програма завершується аварійно:

```csharp run
using System;

try
{
    object obj = "P-001";
    int id = (int)obj;           // InvalidCastException
    Console.WriteLine(id.ToString());
}
catch (FormatException)
{
    Console.WriteLine("FormatException — не перехоплено InvalidCastException");
}
catch (DivideByZeroException)
{
    Console.WriteLine("DivideByZeroException — також не підходить");
}
catch (Exception ex)
{
    // Exception — базовий тип, перехопить усе що не піймали вище
    Console.WriteLine($"Перехоплено базовим Exception: {ex.GetType().Name}");
    Console.WriteLine(ex.Message);
}
```

Блок `catch (Exception ex)` тут виступає «страхувальним мережем» — він обробляє будь-який виняток, якого не перехопили конкретніші блоки.

## Правила порядку блоків catch

1. **Конкретніший тип — раніше**: `FormatException` перед `Exception`
2. **Загальний `Exception` — завжди останнім**: інакше він перехопить усе, і специфічні блоки стануть недосяжним кодом — компілятор видасть помилку
3. **Похідний клас — перед базовим**: якщо `ArgumentOutOfRangeException` (похідний від `ArgumentException`) стоїть після `ArgumentException` — він ніколи не спрацює

```csharp run
using System;

string input = "9999999999999";

try
{
    int age = int.Parse(input);
    Console.WriteLine($"Вік: {age.ToString()} р.");
}
catch (OverflowException ex)
{
    // конкретніший — перший
    Console.WriteLine($"Переповнення: {ex.Message}");
}
catch (FormatException ex)
{
    Console.WriteLine($"Формат: {ex.Message}");
}
catch (Exception ex)
{
    // загальний — останній
    Console.WriteLine($"Інша помилка: {ex.Message}");
}
```

## Підсумок

- `System.Exception` — базовий клас для всіх винятків, містить `Message`, `StackTrace`, `InnerException`, `TargetSite`
- Кожен виняток — це об'єкт конкретного класу в ієрархії `Exception`
- Блоки `catch` перевіряються зверху вниз; спрацьовує перший відповідний
- Загальний `catch (Exception ex)` — страхувальний мережа, завжди останній
- Виняток зупиняє виконання `try` одразу; код після місця помилки не виконується
