---
chapter: 11
chapterTitle: "Розділ 11. Робота з рядками"
section: 2
number: "11.2"
title: "Операції з рядками"
source: "../_combined/71-operatsii-z-riadkamy.md"
---

## 11.2. Операції з рядками

Клас `String` надає широкий набір методів для пошуку, поділу, об'єднання, зміни та аналізу рядків. Усі вони дотримуються принципу незмінності (immutability) з розділу 11.1: жоден метод не модифікує оригінальний рядок — кожен повертає **новий об'єкт** у heap. Розуміння цього факту критично важливе для оцінки продуктивності коду, особливо у циклах.

![Операції з рядками — групи методів класу String](_assets/11-02/string-operations-overview.png)

## Об'єднання рядків

Конкатенація виконується оператором `+` або статичним методом `Concat`:

```csharp
string firstName = "Іван";
string lastName  = "Петренко";

string fullName  = lastName + " " + firstName;              // оператор +
string fullName2 = string.Concat(lastName, " ", firstName); // метод Concat
```

Оператор `+` для рядків — це синтаксичний цукор над `string.Concat`. Компілятор Roslyn оптимізує кількість алокацій: якщо всі операнди є рядковими **літералами**, компілятор об'єднує їх ще на етапі компіляції — у IL потрапляє вже один готовий рядок, без жодного виклику `Concat`. Але якщо хоч один операнд є змінною або виразом, відбувається виклик `string.Concat` з відповідною кількістю аргументів.

`string.Concat` має перевантаження до 4 аргументів, де він може уникнути проміжних алокацій. При більшій кількості частин або у циклі — продуктивнішим є `StringBuilder` (розд. 11.4).

Для з'єднання **масиву або колекції** рядків через роздільник використовується `Join`:

```csharp
string[] parts = { "Петренко", "Іван", "67", "кардіологія", "I10.9" };
string record  = string.Join(";", parts); // "Петренко;Іван;67;кардіологія;I10.9"
```

`Join` є статичним методом і приймає також `IEnumerable<T>` (де T може бути будь-яким типом — кожен елемент перетворюється через `ToString()`). Це дуже зручно при формуванні CSV-рядків або протоколів зі списків об'єктів. `Join` внутрішньо виділяє пам'ять лише один раз (попередньо обчислюючи сумарну довжину), тому є ефективнішим за ручну конкатенацію у циклі.

## Пошук у рядку

**`Contains`** перевіряє наявність підрядка. За замовчуванням пошук чутливий до регістру; для нечутливого пошуку передається `StringComparison`:

```csharp
string diagnosis = "Гіпертензія артеріальна";

bool found1 = diagnosis.Contains("артеріальна");                                    // true
bool found2 = diagnosis.Contains("АРТЕРІАЛЬНА");                                    // false
bool found3 = diagnosis.Contains("АРТЕРІАЛЬНА", StringComparison.OrdinalIgnoreCase); // true
```

Порівняння через `StringComparison.OrdinalIgnoreCase` є **надійнішим і швидшим** за `diagnosis.ToLower().Contains(...)`, бо не виділяє проміжний рядок у heap. Крім того, `ToLower()` залежить від поточної культури операційної системи — в деяких локалях перетворення регістру відрізняється від очікуваного для ASCII-символів. `OrdinalIgnoreCase` виконує байтове порівняння кодових точок і є **незалежним від культури**.

**`IndexOf` та `LastIndexOf`** повертають позицію першого / останнього входження (0-based). Якщо підрядок не знайдено, повертається `-1`. Перевірка на `-1` є стандартним патерном:

```csharp
string text = "Діагноз: I10.9. Примітка: I10.9 підтверджено.";

int idx = text.IndexOf("I10.9");
if (idx >= 0)
    Console.WriteLine($"Знайдено на позиції {idx}");
```

`IndexOf` також приймає `startIndex` — початок пошуку, що дозволяє знаходити **наступні** входження у тексті за допомогою циклу:

```csharp
string notes = "Прийом: 09:00. Виписка: 14:00. Повторний прийом: 17:00";

int pos = 0;
while (true)
{
    int found = notes.IndexOf("прийом", pos, StringComparison.OrdinalIgnoreCase);
    if (found < 0) break;
    Console.WriteLine($"  знайдено на [{found}]: '{notes.Substring(found, 6)}'");
    pos = found + 1; // пересуваємося на 1 символ вперед від поточного збігу
}
```

Метод `LastIndexOf` виконує пошук з кінця рядка — корисний, наприклад, для знаходження останньої крапки в іменах файлів або останнього роздільника в шляху.

**`StartsWith` та `EndsWith`** перевіряють початок і кінець рядка — зручно для перевірки форматів:

```csharp
string icdCode = "I10.9";
bool isCardio = icdCode.StartsWith("I");  // true — серцево-судинні хвороби
bool hasSpec  = icdCode.EndsWith(".9");   // true — неуточнена форма
```

Обидва методи також приймають `StringComparison` для нечутливого до регістру пошуку.

## Поділ та витягування підрядків

**`Split`** розбиває рядок на масив підрядків за роздільником. Це один із найбільш завантажених роботою методів класу `String` — він має численні перевантаження:

```csharp
string record = "Петренко;Іван;;67;кардіологія";

// 1) Роздільник — один символ
string[] fields1 = record.Split(';');
// ["Петренко", "Іван", "", "67", "кардіологія"] — порожній елемент присутній

// 2) Видалити порожні елементи
string[] fields2 = record.Split(';', StringSplitOptions.RemoveEmptyEntries);
// ["Петренко", "Іван", "67", "кардіологія"]

// 3) Обмежити кількість частин
string[] parts = record.Split(';', 3);
// ["Петренко", "Іван", ";67;кардіологія"] — від 3-ї частини — весь залишок

// 4) Масив символів-роздільників (ділимо за кількома)
string notes = "АТ: 140/90\nЧСС: 78\rSpO2: 97%";
string[] lines = notes.Split(new char[] { '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
```

Параметр `StringSplitOptions.RemoveEmptyEntries` — дуже важлива опція: без неї подвійні роздільники (наприклад, `"a;;b"`) дають порожній рядок у масиві результату. Починаючи з .NET 5, є також `StringSplitOptions.TrimEntries` — він автоматично прибирає пробіли з кожної отриманої частини. Обидва значення можна комбінувати через побітове АБО: `StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries`.

**`Substring`** витягує підрядок за позицією. Є два перевантаження:

```csharp
string icd  = "I10.9 — Гіпертензія артеріальна";

string code = icd.Substring(0, 5);  // від 0, 5 символів: "I10.9"
string desc = icd.Substring(8);     // від 8 до кінця: "Гіпертензія артеріальна"
```

У C# 8+ з'явився синтаксис **Range** через оператор `..` та тип `Range`:

```csharp
string code = icd[0..5]; // те саме що Substring(0, 5)
string desc = icd[8..];  // те саме що Substring(8)
string last = icd[^3..]; // 3 символи з кінця
```

Оператор `^` (hat) позначає індекс відносно кінця рядка: `^1` — останній символ, `^3..` — три останніх. Це суттєво скорочує код при роботі з суфіксами та закінченнями.

## Зміна рядка

**`Replace`** замінює **всі** входження підрядка або символу на інший. Оскільки метод повертає новий рядок, виклики можна **ланцюгувати** — це зручний патерн для заповнення шаблонів:

```csharp
string template = "Пацієнт {NAME} прийнятий {DATE}";
string filled   = template
    .Replace("{NAME}", "Петренко І.С.")
    .Replace("{DATE}", "10.06.2026");
// "Пацієнт Петренко І.С. прийнятий 10.06.2026"
```

Ланцюгування стає можливим саме завдяки незмінності: кожен `Replace` повертає новий рядок, на якому можна одразу викликати наступний метод. Кількість ланцюгових викликів обмежена лише читабельністю коду.

`Replace` також має перевантаження для заміни одного символу: `"code".Replace('I', 'J')`. Символьна версія є швидшою, ніж рядкова, оскільки порівнює одне значення, а не підрядок.

**`Insert(index, value)`** вставляє підрядок на вказану позицію:

```csharp
string name    = "Петренко Іван";
string updated = name.Insert(9, "Степанович ");
// "Петренко Степанович Іван"
```

Важливо: `index` не може перевищувати `Length` рядка. При `index == Length` — вставка відбувається в кінець, що еквівалентно `Append`.

**`Remove`** має два перевантаження:
- `Remove(startIndex)` — видаляє всі символи від `startIndex` до кінця рядка.
- `Remove(startIndex, count)` — видаляє рівно `count` символів, починаючи з `startIndex`:

```csharp
string record = "ID:00042 Петренко";
string name   = record.Remove(0, 9);  // видалити перші 9 символів → "Петренко"
string prefix = record.Remove(7);     // залишити перші 7 символів → "ID:0004"
```

## Обрізка рядка

**`Trim()`** видаляє пробільні символи (пробіл, табуляція, `\r`, `\n`) на початку та в кінці рядка. `TrimStart()` і `TrimEnd()` обрізають тільки один бік відповідно:

```csharp
string raw     = "  Петренко Іван  \t";
string cleaned = raw.Trim();      // "Петренко Іван"
string left    = raw.TrimStart(); // "Петренко Іван  \t"
string right   = raw.TrimEnd();   // "  Петренко Іван"
```

Якщо відомо, що зайві символи можуть бути лише з одного боку (наприклад, читаємо рядок з файлу, де пробіли завжди є в кінці) — `TrimEnd()` є ефективнішим за `Trim()`, оскільки аналізує менше символів.

Можна також задати **довільні символи** для обрізання замість пробілу:

```csharp
string code  = "###I10.9###";
string clean = code.Trim('#'); // "I10.9"

// Або масив символів:
string messy = "--**I10.9**--";
string result = messy.Trim('-', '*', ' '); // "I10.9"
```

**`PadLeft(totalWidth)`** та **`PadRight(totalWidth)`** доповнюють рядок пробілами зліва або справа до заданої загальної ширини. Якщо рядок вже довший за `totalWidth` — він не обрізається, повертається без змін. Другий параметр дозволяє замінити пробіл на довільний символ:

```csharp
Console.WriteLine("Петренко".PadRight(20) + "| I10.9");
Console.WriteLine("Коваль".PadRight(20)   + "| J45.0");
// Петренко            | I10.9
// Коваль              | J45.0

// PadLeft з '0' для ідентифікаторів:
Console.WriteLine(42.ToString().PadLeft(6, '0')); // "000042"
```

`PadLeft` і `PadRight` є особливо цінними при формуванні текстових звітів з фіксованою шириною колонок, де необхідно вирівнювати дані по лівому або правому краю.

## Зміна регістру та порівняння

`ToUpper()` і `ToLower()` нормалізують регістр. Але для **порівняння** без урахування регістру краще передавати `StringComparison` напряму — без проміжної алокації:

```csharp
string input = "кардіологія";

// НЕ оптимально: виділяє новий рядок у heap перед порівнянням
bool match1 = input.ToLower() == "кардіологія";

// Краще: без зайвої алокації, незалежно від культури
bool match2 = string.Equals(input, "Кардіологія", StringComparison.OrdinalIgnoreCase);
```

Статичний метод `string.Compare(s1, s2)` повертає від'ємне число якщо `s1 < s2` лексикографічно, нуль якщо рядки рівні, додатне якщо `s1 > s2`. Лексикографічне порівняння — це посимвольне порівняння кодових точок Unicode зліва направо. Перший рядок вважається «меншим», якщо на найпершій позиції розбіжності його символ має менший Unicode-код:

```csharp
int cmp1 = string.Compare("Іваненко", "Петренко"); // < 0 — 'І' < 'П' за Unicode
int cmp2 = string.Compare("Коваль", "Коваль");     // == 0
int cmp3 = string.Compare("Петренко", "Іваненко"); // > 0
```

`string.Compare` також приймає `StringComparison` для культурно-незалежного порівняння. Метод екземпляра `s.CompareTo(other)` є аналогом `string.Compare(s, other)` без можливості вказати `StringComparison` — тому для точного контролю над режимом порівняння перевага надається статичному `Compare`.

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
