---
chapter: 11
chapterTitle: "Розділ 11. Робота з рядками"
section: 4
number: "11.4"
title: "Клас StringBuilder"
source: "../_combined/73-klas-stringbuilder.md"
---

## 11.4. Клас StringBuilder

З розділу 11.1 відомо: рядок `string` є незмінним — кожна операція створює новий об'єкт у heap. При одиничних операціях це не проблема. Але якщо потрібно побудувати рядок із 50 фрагментів (наприклад, виписку пацієнта по рядку за рядком), конкатенація через `+` виконає **50 алокацій**, де кожен новий об'єкт копіює весь попередній вміст. Складність такого підходу — O(N²).

Клас `StringBuilder` з простору імен `System.Text` вирішує цю задачу: він зберігає **мутабельний буфер** символів і додає нові символи на місці, без копіювання попереднього вмісту. Алокація відбувається лише тоді, коли буфер переповнюється — і тоді він **подвоюється**.

![StringBuilder vs string — алокація пам'яті при побудові рядка у циклі](_assets/11-04/stringbuilder-vs-string-memory.png)

## Алгоритм подвоєння ємності

`StringBuilder` виділяє початковий буфер на 16 символів (якщо рядок у конструкторі не перевищує 16 символів). При переповненні буфер **подвоюється**: 16 → 32 → 64 → 128 і т.д. Це амортизована O(1) вставка — в середньому кожен символ вимагає постійної кількості операцій незалежно від поточного розміру.

```csharp
using System.Text;

var sb = new StringBuilder("Виписка:");
Console.WriteLine($"Length={sb.Length}, Capacity={sb.Capacity}"); // Length=8, Capacity=16

sb.Append(" Петренко");
Console.WriteLine($"Length={sb.Length}, Capacity={sb.Capacity}"); // Length=17, Capacity=32  <-- подвоєно
```

Якщо кінцевий розмір рядка відомий наперед, ємність можна задати явно в конструкторі — тоді реалокацій буде нуль:

```csharp
var sb = new StringBuilder(capacity: 512); // одразу виділяємо 512 символів
```

## Створення StringBuilder

```csharp
using System.Text;

// Порожній буфер (Capacity=16)
var sb1 = new StringBuilder();

// З початковим рядком
var sb2 = new StringBuilder("Виписка пацієнта:");

// З заданою ємністю (уникаємо реалокацій)
var sb3 = new StringBuilder(256);

// З початковим рядком і ємністю
var sb4 = new StringBuilder("Виписка пацієнта:", 256);
```

## Основні методи

| Метод | Що робить |
|-------|-----------|
| `Append(value)` | Додати значення в кінець |
| `AppendLine(value)` | Додати значення і `\n` |
| `AppendLine()` | Додати порожній рядок |
| `AppendFormat(format, args)` | Додати форматований рядок |
| `Insert(index, value)` | Вставити за індексом |
| `Remove(start, count)` | Видалити символи |
| `Replace(old, new)` | Замінити всі входження |
| `Clear()` | Очистити буфер (зберігає Capacity) |
| `ToString()` | Отримати рядок із буфера |

## Fluent API — method chaining

Усі методи `StringBuilder` повертають **`this`** — посилання на сам об'єкт. Це дозволяє ланцюгувати виклики (fluent API):

```csharp
string result = new StringBuilder()
    .Append("Пацієнт: ")
    .AppendLine("Петренко І.С.")
    .Append("Діагноз: ")
    .AppendLine("I10.9 — Гіпертензія")
    .Append("Відділення: кардіологія")
    .ToString();

Console.WriteLine(result);
```

## AppendLine та AppendFormat

**`AppendLine`** — найзручніший метод для побудови багаторядкових текстів:

```csharp
var sb = new StringBuilder();
sb.AppendLine("Виписка з лікарні");
sb.AppendLine("==================");
sb.AppendLine("Пацієнт: Петренко Іван Степанович");
sb.AppendLine("Дата: 10.06.2026");
```

**`AppendFormat`** — форматоване додавання з підтримкою специфікаторів (розд. 11.3):

```csharp
sb.AppendFormat("АТ: {0:F0}/{1:F0} мм рт.ст.\n", 140.5, 90.0);
sb.AppendFormat("Вартість: {0:C2}\n", 1250.50);
```

## Clear() для повторного використання

`Clear()` обнуляє `Length` до нуля, але **зберігає виділений буфер**. Це дозволяє повторно використовувати `StringBuilder` без повторного виділення пам'яті:

```csharp
var sb = new StringBuilder(256);

for (int i = 1; i <= 3; i++)
{
    sb.Clear();                          // скидаємо вміст, буфер лишається
    sb.AppendLine($"Звіт #{i}");
    sb.AppendLine($"Пацієнт: Петренко");
    Console.WriteLine(sb.ToString());
}
```

## Коли string, а коли StringBuilder?

| Ситуація | Рекомендація |
|----------|-------------|
| До ~10 операцій конкатенації | `string` — компілятор може оптимізувати |
| Цикл з невідомою кількістю ітерацій | `StringBuilder` — O(N) vs O(N²) |
| Побудова багаторядкового звіту | `StringBuilder.AppendLine` |
| Шаблонне форматування | `string.Format` або `$"..."` |
| Пошук (`IndexOf`, `Contains`) | `string` — у `StringBuilder` їх немає |

`StringBuilder` не має методів `IndexOf`, `Contains`, `StartsWith`. Якщо потрібен пошук під час побудови — зберігайте проміжні `string`, або завершіть побудову через `ToString()` і шукайте вже у звичайному рядку.

## Побудова виписки — runnable приклад

Демонстрація Capacity, AppendLine, AppendFormat, Clear:

```csharp run
using System;
using System.Text;

var sb = new StringBuilder(128);
Console.WriteLine($"Початок: Length={sb.Length}, Capacity={sb.Capacity}");

sb.AppendLine("================================");
sb.AppendLine("     ВИПИСКА З ЛІКАРНІ");
sb.AppendLine("================================");
sb.AppendFormat("Пацієнт:    {0}\n", "Петренко Іван Степанович");
sb.AppendFormat("Вік:        {0} р.\n", 67);
sb.AppendFormat("Відділення: {0}\n", "кардіологія");
sb.AppendFormat("МКХ-10:     {0}\n", "I10.9");
sb.AppendLine("--------------------------------");
sb.AppendFormat("АТ при вступі:   {0:F0}/{1:F0} мм рт.ст.\n", 158.0, 100.0);
sb.AppendFormat("АТ при виписці:  {0:F0}/{1:F0} мм рт.ст.\n", 130.0, 85.0);
sb.AppendLine("--------------------------------");
sb.AppendFormat("Вартість:   {0:N2} грн.\n", 4350.75);
sb.AppendLine("================================");

Console.WriteLine($"Після заповнення: Length={sb.Length}, Capacity={sb.Capacity}");
Console.WriteLine();
Console.WriteLine(sb.ToString());
```

## Fluent chaining та повторне використання — runnable приклад

Ланцюг викликів та `Clear()` між ітераціями:

```csharp run
using System;
using System.Text;

string[] names = { "Петренко Іван", "Коваль Марія", "Сидоренко Олег" };
string[] icds  = { "I10.9", "J45.0", "K25.3" };

var sb = new StringBuilder(256);

for (int i = 0; i < names.Length; i++)
{
    sb.Clear();

    string card = sb
        .Append($"[{i+1}] ")
        .Append(names[i].PadRight(20))
        .Append(" | ")
        .Append(icds[i])
        .ToString();

    Console.WriteLine(card);
}

Console.WriteLine();
Console.WriteLine($"Capacity буфера: {sb.Capacity} (без реалокацій після Clear)");

// Replace у StringBuilder
sb.Clear();
sb.Append("Шановний {NAME}, ваш прийом {DATE} підтверджено.");
sb.Replace("{NAME}", "Петренко І.С.");
sb.Replace("{DATE}", "12.06.2026 о 10:00");
Console.WriteLine(sb.ToString());
```
