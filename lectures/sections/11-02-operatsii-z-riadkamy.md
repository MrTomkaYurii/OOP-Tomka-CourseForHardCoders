---
chapter: 11
chapterTitle: "Розділ 11. Робота з рядками"
section: 2
number: "11.2"
title: "Операції з рядками"
source: "../_combined/71-operatsii-z-riadkamy.md"
---

## 11.2. Операції з рядками

Клас `String` надає широкий набір методів для пошуку, поділу, об'єднання, зміни та аналізу рядків. Усі вони дотримуються принципу незмінності (immutability) з розділу 11.1: жоден метод не модифікує оригінальний рядок — кожен повертає **новий об'єкт** у heap.

![Операції з рядками — групи методів класу String](_assets/11-02/string-operations-overview.png)

## Об'єднання рядків

Конкатенація виконується оператором `+` або статичним методом `Concat`:

```csharp
string firstName = "Іван";
string lastName  = "Петренко";

string fullName  = lastName + " " + firstName;              // оператор +
string fullName2 = string.Concat(lastName, " ", firstName); // метод Concat
```

Для з'єднання масиву рядків через роздільник використовується `Join`:

```csharp
string[] parts = { "Петренко", "Іван", "67", "кардіологія", "I10.9" };
string record  = string.Join(";", parts); // "Петренко;Іван;67;кардіологія;I10.9"
```

`Join` є статичним методом і приймає також `IEnumerable<string>`, що дозволяє передавати будь-які колекції напряму.

## Пошук у рядку

**`Contains`** перевіряє наявність підрядка. За замовчуванням пошук чутливий до регістру; для нечутливого пошуку передається `StringComparison`:

```csharp
string diagnosis = "Гіпертензія артеріальна";

bool found1 = diagnosis.Contains("артеріальна");                                    // true
bool found2 = diagnosis.Contains("АРТЕРІАЛЬНА");                                    // false
bool found3 = diagnosis.Contains("АРТЕРІАЛЬНА", StringComparison.OrdinalIgnoreCase); // true
```

Порівняння через `StringComparison.OrdinalIgnoreCase` є **надійнішим і швидшим** за `diagnosis.ToLower().Contains(...)`, бо не виділяє проміжний рядок у heap.

**`IndexOf` та `LastIndexOf`** повертають позицію першого / останнього входження (`-1` якщо не знайдено). `IndexOf` також приймає `startIndex` — початок пошуку, що дозволяє знаходити **наступні** входження у тексті:

```csharp
string notes = "Прийом: 09:00. Виписка: 14:00. Повторний прийом: 17:00";

int first = notes.IndexOf("прийом", StringComparison.OrdinalIgnoreCase);       // 0
int next  = notes.IndexOf("прийом", first + 1, StringComparison.OrdinalIgnoreCase); // 42
```

**`StartsWith` та `EndsWith`** перевіряють початок і кінець рядка — зручно для перевірки форматів:

```csharp
string icdCode = "I10.9";
bool isCardio = icdCode.StartsWith("I");  // true — серцево-судинні хвороби
bool hasSpec  = icdCode.EndsWith(".9");   // true — неуточнена форма
```

## Поділ та витягування підрядків

**`Split`** розбиває рядок на масив підрядків за роздільником. Параметр `StringSplitOptions.RemoveEmptyEntries` видаляє порожні елементи (на випадок подвійних роздільників):

```csharp
string record = "Петренко;Іван;;67;кардіологія";
string[] fields = record.Split(';', StringSplitOptions.RemoveEmptyEntries);
// ["Петренко", "Іван", "67", "кардіологія"]
```

`Split` також приймає масив символів-роздільників:

```csharp
string notes = "АТ: 140/90\nЧСС: 78\nSpO2: 97%";
string[] lines = notes.Split(new char[] { '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
```

**`Substring(startIndex)`** — витягти підрядок від позиції до кінця.  
**`Substring(startIndex, length)`** — витягти підрядок заданої довжини:

```csharp
string icd  = "I10.9 — Гіпертензія";
string code = icd.Substring(0, 5);  // "I10.9"
string desc = icd.Substring(8);     // "Гіпертензія"
```

## Зміна рядка

**`Replace`** замінює **всі** входження підрядка або символу на інший. Оскільки метод повертає новий рядок, виклики можна **ланцюгувати**:

```csharp
string template = "Пацієнт {NAME} прийнятий {DATE}";
string filled   = template
    .Replace("{NAME}", "Петренко І.С.")
    .Replace("{DATE}", "10.06.2026");
// "Пацієнт Петренко І.С. прийнятий 10.06.2026"
```

**`Insert(index, value)`** вставляє підрядок на вказану позицію:

```csharp
string name    = "Петренко Іван";
string updated = name.Insert(9, "Степанович ");
// "Петренко Степанович Іван"
```

**`Remove(startIndex)`** видаляє всі символи з позиції до кінця.  
**`Remove(startIndex, count)`** видаляє рівно `count` символів:

```csharp
string record = "ID:00042 Петренко";
string name   = record.Remove(0, 9); // "Петренко"
```

## Обрізка рядка

**`Trim()`** видаляє пробільні символи на початку та в кінці:

```csharp
string raw     = "  Петренко Іван  \t";
string cleaned = raw.Trim(); // "Петренко Іван"
```

**`TrimStart()`** і **`TrimEnd()`** обрізають тільки один бік. Можна передати символи для видалення:

```csharp
string code  = "###I10.9###";
string clean = code.Trim('#'); // "I10.9"
```

**`PadLeft(totalWidth)`** та **`PadRight(totalWidth)`** доповнюють рядок пробілами до заданої ширини. Корисно для вирівнювання колонок у текстових звітах:

```csharp
Console.WriteLine("Петренко".PadRight(20) + "| I10.9");
Console.WriteLine("Коваль".PadRight(20)   + "| J45.0");
// Петренко            | I10.9
// Коваль              | J45.0
```

## Зміна регістру та порівняння

`ToUpper()` і `ToLower()` нормалізують регістр. Але для **порівняння** без урахування регістру краще передавати `StringComparison` напряму — без проміжної алокації:

```csharp
string input = "кардіологія";

// НЕ оптимально: виділяє новий рядок у heap
bool match1 = input.ToLower() == "кардіологія";

// Краще: без зайвої алокації
bool match2 = string.Equals(input, "Кардіологія", StringComparison.OrdinalIgnoreCase);
```

Статичний метод `string.Compare(s1, s2)` повертає від'ємне число якщо `s1 < s2`, нуль якщо рівні, додатне якщо `s1 > s2` — використовується для лексикографічного сортування:

```csharp
int cmp = string.Compare("Іваненко", "Петренко"); // < 0 — Іваненко стоїть вище за алфавітом
```

## Парсинг медичної картки — runnable приклад

Розбираємо рядок медичного запису на поля, перевіряємо формат і формуємо листа:

```csharp run
using System;

string record = "Петренко;Іван;67;кардіологія;I10.9";

string[] fields  = record.Split(';');
string lastName  = fields[0];
string firstName = fields[1];
int    age       = int.Parse(fields[2]);
string dept      = fields[3];
string icd       = fields[4];

Console.WriteLine("=== Картка пацієнта ===");
Console.WriteLine($"ПІБ:        {lastName} {firstName}");
Console.WriteLine($"Вік:        {age} р.");
Console.WriteLine($"Відділення: {dept}");
Console.WriteLine($"МКХ-10:     {icd}");

bool isCardio = dept.Contains("кардіо", StringComparison.OrdinalIgnoreCase);
bool isHypert = icd.StartsWith("I10");
Console.WriteLine($"\nКардіологія: {isCardio}");
Console.WriteLine($"Гіпертензія: {isHypert}");

string letter = "Шановний пацієнте {NAME}, ваш код діагнозу: {ICD}."
    .Replace("{NAME}", $"{firstName} {lastName}")
    .Replace("{ICD}",  icd);
Console.WriteLine($"\n{letter}");

string rebuilt = string.Join(" | ", lastName, firstName, icd);
Console.WriteLine($"\nЗапис: {rebuilt}");
```

## Форматування звіту відділення — runnable приклад

Вирівнювання колонок через `PadRight`, аналіз кодів МКХ через `StartsWith`:

```csharp run
using System;

string[] patients = {
    "Петренко Іван;I10.9;кардіологія",
    "Коваль Марія;J45.0;пульмонологія",
    "Сидоренко Олег;K25.3;гастроентерологія",
    "Мельник Ганна;M54.5;неврологія",
};

Console.WriteLine("=== Список пацієнтів ===");
Console.WriteLine("Ім'я".PadRight(22) + "МКХ".PadRight(8) + "Відділення");
Console.WriteLine(new string('-', 55));

foreach (var row in patients)
{
    string[] f   = row.Split(';');
    string name  = f[0];
    string icd   = f[1];
    string dept  = f[2];

    char system = icd[0];
    string flag = system == 'I' ? "[серце]"  :
                  system == 'J' ? "[легені]" :
                  system == 'K' ? "[ШКТ]"   : "[інше]";

    Console.WriteLine($"{name.PadRight(22)}{icd.PadRight(8)}{dept}  {flag}");
}

Console.WriteLine(new string('-', 55));

int cardioCount = 0;
foreach (var row in patients)
    if (row.Contains("кардіологія", StringComparison.OrdinalIgnoreCase))
        cardioCount++;

Console.WriteLine($"Кардіологія: {cardioCount} з {patients.Length} пацієнтів");
```
