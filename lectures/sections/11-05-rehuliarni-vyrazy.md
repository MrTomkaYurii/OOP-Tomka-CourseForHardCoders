---
chapter: 11
chapterTitle: "Розділ 11. Робота з рядками"
section: 5
number: "11.5"
title: "Регулярні вирази"
source: "../_combined/74-rehuliarni-vyrazy.md"
---

## 11.5. Регулярні вирази

Методи `Contains`, `IndexOf`, `Split` — ефективні для пошуку фіксованих підрядків. Але коли потрібно знайти рядок за **шаблоном** — наприклад, будь-який код МКХ-10 формату `[Літера][2 цифри][.цифра]?`, номер телефону або email — ці методи вимагають складного ручного коду. Для таких задач існують **регулярні вирази** (regular expressions, regex).

Основна функціональність у .NET зосереджена у просторі імен `System.Text.RegularExpressions`. Центральний клас — `Regex`.

![Регулярні вирази у C# — синтаксис та API класу Regex](_assets/11-05/regex-syntax-and-api.png)

## Синтаксис регулярних виразів

Регулярний вираз — це рядок-шаблон, де більшість символів означають себе, а спеціальні символи мають особливе значення:

| Елемент | Значення |
|---------|---------|
| `^` / `$` | Початок / кінець рядка |
| `.` | Будь-який один символ (крім `\n`) |
| `*` | Попередній елемент 0 або більше разів |
| `+` | Попередній елемент 1 або більше разів |
| `?` | Попередній елемент 0 або 1 раз |
| `{n}` | Рівно n разів |
| `{n,m}` | Від n до m разів |
| `\d` / `\D` | Цифра / не цифра |
| `\w` / `\W` | Словесний символ (літера, цифра, `_`) / решта |
| `\s` / `\S` | Пробільний / не пробільний символ |
| `[abc]` | Один із символів a, b або c |
| `[A-Z]` | Символ у діапазоні |
| `(...)` | Група збігу |
| `(?<name>...)` | **Іменована** група |
| `\|` | Альтернатива: `abc\|def` |
| `\.` | Екранування: літеральна крапка |

У C# шаблони зазвичай записують як **verbatim-рядки** `@"..."`, щоб уникнути подвійного екранування зворотних слешів: `@"\d+"` замість `"\\d+"`.

## Клас Regex та основні методи

```csharp
using System.Text.RegularExpressions;

var regex = new Regex(@"[A-Z]\d{2}(\.?\d)?");

// IsMatch — bool: чи є хоч один збіг
bool ok = regex.IsMatch("I10.9");   // true
bool no = regex.IsMatch("999");     // false

// Match — перший збіг
Match m = regex.Match("код: I10.9, примітка");
Console.WriteLine(m.Value);  // "I10.9"
Console.WriteLine(m.Index);  // 5 — позиція у рядку

// Matches — всі збіги
MatchCollection all = regex.Matches("I10.9 і J45.0");
foreach (Match match in all)
    Console.WriteLine(match.Value); // "I10.9", "J45.0"
```

## RegexOptions

Конструктор `Regex` приймає параметр `RegexOptions`, який змінює поведінку шаблону:

| Параметр | Ефект |
|---------|-------|
| `IgnoreCase` | Нечутливість до регістру |
| `Multiline` | `^` та `$` — початок/кінець кожного рядка |
| `Singleline` | `.` відповідає і `\n` |
| `Compiled` | Компіляція у IL для швидшого виконання при багаторазовому використанні |
| `CultureInvariant` | Ігнорувати регіональні відмінності |

```csharp
var re = new Regex(@"гіпертензія", RegexOptions.IgnoreCase | RegexOptions.Compiled);
```

## Іменовані групи

Групи `(...)` дозволяють витягати підчастини збігу. **Іменовані групи** `(?<name>...)` зручніші за числові: не потрібно пам'ятати порядок:

```csharp
var re = new Regex(
    @"(?<last>\w+);(?<first>\w+);(?<age>\d+);(?<icd>[A-Z]\d{2}\.?\d?)");

Match m = re.Match("Петренко;Іван;67;I10.9");
if (m.Success)
{
    Console.WriteLine(m.Groups["last"].Value);  // Петренко
    Console.WriteLine(m.Groups["age"].Value);   // 67
    Console.WriteLine(m.Groups["icd"].Value);   // I10.9
}
```

Якщо поля в рядку змінять порядок — треба змінити лише шаблон, а не весь код читання груп.

## Replace та Split

**`Replace`** замінює всі збіги шаблону на заданий рядок:

```csharp
// Видалити всі не-цифри з телефону
string phone  = "+38 (067) 123-45-67";
string digits = Regex.Replace(phone, @"\D", ""); // "380671234567"

// Нормалізувати множинні пробіли
string notes  = "пацієнт   прийнятий   10.06.2026";
string clean  = Regex.Replace(notes, @"\s{2,}", " "); // "пацієнт прийнятий 10.06.2026"
```

**`Regex.Split`** розбиває рядок по збігах шаблону — потужніший аналог `string.Split`:

```csharp
// Розбити по будь-якій кількості пробілів або крапок з комою
string[] parts = Regex.Split("Петренко ; Іван ;; 67", @"\s*;\s*");
// ["Петренко", "Іван", "", "67"]
```

## Статичні методи Regex

Клас `Regex` дозволяє викликати методи статично, без створення об'єкта. Зручно для разових перевірок:

```csharp
bool valid = Regex.IsMatch("I10.9", @"^[A-Z]\d{2}(\.?\d)?$");
string     = Regex.Replace("+380671234567", @"\D", "");
```

Але для повторного використання в циклі або гарячому шляху краще створити об'єкт `Regex` **один раз** і зберегти його у полі класу — об'єкт `Regex` є потокобезпечним (thread-safe) для читання.

## Валідація клінічних даних — runnable приклад

Перевірка формату коду МКХ-10 та телефону пацієнта:

```csharp run
using System;
using System.Text.RegularExpressions;

// Шаблони
var icdRe   = new Regex(@"^[A-Z]\d{2}(\.?\d)?$");
var phoneRe = new Regex(@"^\+?(\d[\s\-]?){10,13}$");

// Тестові дані
string[] icds = { "I10.9", "J45.0", "999", "i10", "K25", "Z00.0" };
Console.WriteLine("=== Валідація МКХ-10 ===");
foreach (var code in icds)
    Console.WriteLine($"  {code,-8} -> {(icdRe.IsMatch(code) ? "OK" : "INVALID")}");

string[] phones = {
    "+380671234567",
    "0671234567",
    "+38 067 123-45-67",
    "abc",
    "123"
};
Console.WriteLine("\n=== Валідація телефону ===");
foreach (var p in phones)
    Console.WriteLine($"  {p,-22} -> {(phoneRe.IsMatch(p) ? "OK" : "INVALID")}");

// Витягування всіх кодів МКХ з клінічної нотатки
string notes = "Основний: I10.9. Супутні: J45.0, E11.9. Перенесений: K25.";
var allCodes = new Regex(@"[A-Z]\d{2}\.?\d?").Matches(notes);
Console.WriteLine("\n=== Коди МКХ у нотатці ===");
foreach (Match m in allCodes)
    Console.WriteLine($"  {m.Value} (позиція {m.Index})");
```

## Парсинг медичного запису через іменовані групи — runnable приклад

```csharp run
using System;
using System.Text.RegularExpressions;

string[] records = {
    "Петренко;Іван;67;I10.9;кардіологія",
    "Коваль;Марія;45;J45.0;пульмонологія",
    "Сидоренко;Олег;71;K25.3;гастроентерологія",
};

var re = new Regex(
    @"(?<last>\w+);(?<first>\w+);(?<age>\d+);(?<icd>[A-Z]\d{2}\.?\d?);(?<dept>\w+)");

Console.WriteLine($"{"ПІБ",-22}{"Вік",5}{"МКХ",8}  Відділення");
Console.WriteLine(new string('-', 55));

foreach (var row in records)
{
    Match m = re.Match(row);
    if (!m.Success) { Console.WriteLine($"  Помилка: {row}"); continue; }

    string name = $"{m.Groups["last"].Value} {m.Groups["first"].Value}";
    int    age  = int.Parse(m.Groups["age"].Value);
    string icd  = m.Groups["icd"].Value;
    string dept = m.Groups["dept"].Value;

    Console.WriteLine($"{name,-22}{age,5}{icd,8}  {dept}");
}

Console.WriteLine(new string('-', 55));

// Replace: видалити все крім цифр з телефону
string rawPhone = "+38 (067) 123-45-67";
string digits   = Regex.Replace(rawPhone, @"\D", "");
Console.WriteLine($"\nТелефон: {rawPhone} -> {digits}");

// Нормалізація пробілів у нотатці
string note  = "пацієнт   Петренко   прийнятий   10.06.2026";
string clean = Regex.Replace(note, @"\s{2,}", " ");
Console.WriteLine($"Нотатка: {clean}");
```
