---
chapter: 11
chapterTitle: "Розділ 11. Робота з рядками"
section: 1
number: "11.1"
title: "Рядки та клас String"
source: "../_combined/70-riadky-ta-klas-string.md"
---

## 11.1. Рядки та клас String

Значна частина завдань у розробці медичних застосунків пов'язана з обробкою текстових даних: парсинг діагнозів за МКХ-10, перевірка формату номера телефону пацієнта, побудова звітів, пошук у клінічних нотатках. У мові C# рядкові значення представляє тип `string`, а вся функціональність роботи з ним зосереджена в класі `System.String`. Власне `string` — це псевдонім (alias) класу `String`; обидва записи еквівалентні.

Об'єкти `String` зберігають текст як послідовність символів Unicode (UTF-16). Максимальний розмір об'єкта `String` у пам'яті — близько 2 ГБ або приблизно 1 мільярд символів.

## Незмінність рядків (immutability)

Найважливіша властивість `string` у C# — **незмінність**. Після створення об'єкт рядка **не може бути змінений**. Кожен метод класу `String`, який «змінює» рядок, насправді створює **новий об'єкт у heap** і повертає посилання на нього.

```csharp
string diagnosis = "Гіпертензія артеріальна";
string step1 = diagnosis.ToLower();      // новий об'єкт у heap
string step2 = step1 + " есенціальна";  // ще один новий об'єкт
string step3 = step2.ToUpper();          // ще один

Console.WriteLine(diagnosis); // "Гіпертензія артеріальна" — не змінився!
```

На діаграмі нижче видно: змінні на стеку зберігають **посилання** на різні об'єкти в heap. Оригінал залишається незачепленим.

![string — незмінний тип: кожна операція створює новий об'єкт у heap](_assets/11-01/string-immutability.png)

Практичний наслідок: якщо у циклі багато разів змінювати рядок через конкатенацію, кожна ітерація виділяє нову пам'ять. Для таких сценаріїв існує `StringBuilder` (розд. 11.4).

## String interning

Компілятор C# застосовує **string interning**: однакові рядкові літерали в коді компілюються в один спільний об'єкт у пулі рядків. Тому оператор `==` для рядків порівнює **значення**, а не посилання — і дає очікуваний результат:

```csharp
string a = "I10";
string b = "I10";

Console.WriteLine(a == b);                // true  — порівняння значень
Console.WriteLine(ReferenceEquals(a, b)); // true  — один об'єкт у пулі (literal interning)

string c = new string(new char[] { 'I', '1', '0' });
Console.WriteLine(a == c);                // true  — значення однакові
Console.WriteLine(ReferenceEquals(a, c)); // false — c створено через new, поза пулом
```

Метод `string.Intern(s)` дозволяє вручну помістити рядок у пул, щоб наступні порівняння через `ReferenceEquals` давали `true`. Але на практиці для перевірки рівності завжди достатньо `==`.

## Тип char

Кожен символ рядка — це значення типу `char` (16-бітний Unicode, займає 2 байти). `char` — **значущий тип** (struct), тоді як `string` — **посилальний тип** (class).

```csharp
char letter = 'А';           // одинарні лапки
string word  = "Артеріальна"; // подвійні лапки
```

Клас `char` містить корисні статичні методи для аналізу символів:

| Метод | Що перевіряє |
|-------|-------------|
| `char.IsLetter(c)` | Чи є символ літерою |
| `char.IsDigit(c)` | Чи є символ цифрою |
| `char.IsWhiteSpace(c)` | Чи є символ пробільним |
| `char.IsUpper(c)` | Чи є символ у верхньому регістрі |
| `char.IsLower(c)` | Чи є символ у нижньому регістрі |
| `char.ToUpper(c)` | Перетворити на верхній регістр |
| `char.ToLower(c)` | Перетворити на нижній регістр |

## Створення рядків

Рядок можна створити кількома способами:

```csharp
// Рядковий літерал — найпоширеніший спосіб
string diagnosis = "Гіпертензія артеріальна";

// Конструктор: повторити символ N разів
string separator = new string('-', 40);  // "----------------------------------------"

// Конструктор: із масиву символів
string code = new string(new char[] { 'I', '1', '0' });  // "I10"

// Конструктор: частина масиву (startIndex, count)
string sub = new string(new char[] { 'I', '1', '0', '.', '9' }, 0, 3);  // "I10"

// Порожній рядок — два еквівалентні способи
string empty1 = "";
string empty2 = string.Empty;
```

## Рядок як масив символів

Клас `String` реалізує інтерфейс `IEnumerable<char>`, тому рядок можна перебирати як послідовність символів. Крім того, визначено **індексатор** тільки для читання:

```csharp
string icd = "I10.9";

char first = icd[0];            // 'I'
int length  = icd.Length;       // 5

// Перебір через for
for (int i = 0; i < icd.Length; i++)
    Console.Write(icd[i] + " "); // I 1 0 . 9

// Перебір через foreach
foreach (char c in icd)
    Console.Write(c + " ");      // I 1 0 . 9
```

Індексатор доступний **тільки для читання** — `icd[0] = 'X'` призведе до помилки компіляції. Це знову підкреслює незмінність рядка.

## Перевірка на порожній рядок

Наявність значення у рядку перевіряють двома статичними методами:

```csharp
string.IsNullOrEmpty(s)      // true якщо s == null або s == ""
string.IsNullOrWhiteSpace(s) // true якщо s == null, "" або "   "
```

`IsNullOrWhiteSpace` є кращим у більшості випадків: він захищає від рядків із самими пробілами, що часто зустрічається при обробці введення користувача або імпортованих даних.

```csharp
void PrintDiagnosis(string? text)
{
    if (string.IsNullOrWhiteSpace(text))
    {
        Console.WriteLine("Діагноз не вказано");
        return;
    }
    Console.WriteLine($"Діагноз: {text.Trim()}");
}
```

## Порівняння рядків

На відміну від більшості класів, `==` для рядків порівнює **значення**, а не посилання. Але для порівняння без урахування регістру краще використовувати `string.Equals` з параметром `StringComparison`:

```csharp
string d1 = "Гіпертензія";
string d2 = "гіпертензія";

Console.WriteLine(d1 == d2);  // false — різний регістр
Console.WriteLine(string.Equals(d1, d2, StringComparison.OrdinalIgnoreCase)); // true
```

`StringComparison.OrdinalIgnoreCase` — порівняння за байтовими значеннями символів без урахування регістру і культури. Для медичних ідентифікаторів (коди МКХ, індентифікатори пацієнтів тощо) це надійний і швидкий варіант, оскільки не залежить від локалі системи.

## Перелік основних методів

| Метод | Що робить |
|-------|-----------|
| `Contains(s)` | Чи містить рядок підрядок |
| `StartsWith(s)` / `EndsWith(s)` | Чи починається / закінчується підрядком |
| `IndexOf(s)` / `LastIndexOf(s)` | Індекс першого / останнього входження |
| `Replace(old, new)` | Замінити всі входження |
| `Split(separator)` | Розбити на масив підрядків |
| `Substring(start, length)` | Витягти підрядок |
| `Trim()` / `TrimStart()` / `TrimEnd()` | Видалити пробіли |
| `ToUpper()` / `ToLower()` | Зміна регістру |
| `Insert(index, value)` | Вставити підрядок |
| `Remove(start, count)` | Видалити символи |
| `PadLeft(n)` / `PadRight(n)` | Доповнити пробілами до ширини n |

Кожен з цих методів розглядається детально в розділі 11.2.

## Рядки у клінічному контексті — runnable приклад

Базові операції зі рядками на прикладі даних медичної картки:

```csharp run
using System;

string rawName   = "  Петренко Іван Степанович  ";
string diagnosis = "Гіпертензія артеріальна";
string icdCode   = "I10";

Console.WriteLine("=== Дані пацієнта ===");
Console.WriteLine($"Ім'я (raw):  '{rawName}'");
Console.WriteLine($"Ім'я (trim): '{rawName.Trim()}'");
Console.WriteLine($"Довжина (trim): {rawName.Trim().Length}");

Console.WriteLine("\n=== Аналіз діагнозу ===");
Console.WriteLine($"Містить 'артеріальна': {diagnosis.Contains("артеріальна")}");
Console.WriteLine($"Код МКХ починається з 'I': {icdCode.StartsWith("I")}");
Console.WriteLine($"Позиція 'артеріальна': {diagnosis.IndexOf("артеріальна")}");

Console.WriteLine("\n=== Immutability: кожна операція — новий об'єкт ===");
string d1 = diagnosis.ToUpper();
string d2 = diagnosis.Replace("артеріальна", "есенціальна");
Console.WriteLine($"Original : {diagnosis}");
Console.WriteLine($"ToUpper(): {d1}");
Console.WriteLine($"Replace(): {d2}");
Console.WriteLine($"Original не змінився: {diagnosis == "Гіпертензія артеріальна"}");
```

## Символьний аналіз рядка — runnable приклад

Перевірка формату коду МКХ-10 через `char`-методи та `IsNullOrWhiteSpace`:

```csharp run
using System;

Console.WriteLine("=== Символи коду МКХ-10 ===");
string code = "I10.9";
for (int i = 0; i < code.Length; i++)
{
    char c = code[i];
    Console.WriteLine($"  [{i}] '{c}'  Letter={char.IsLetter(c)}  Digit={char.IsDigit(c)}");
}

Console.WriteLine("\n=== IsNullOrWhiteSpace ===");
string[] inputs = { "I10", "", "   ", "J45.0" };
foreach (var s in inputs)
    Console.WriteLine($"  '{s}' -> порожній: {string.IsNullOrWhiteSpace(s)}");

Console.WriteLine("\n=== Конструктори String ===");
string separator = new string('-', 30);
string fromChars = new string(new char[] { 'I', '1', '0' });
Console.WriteLine(separator);
Console.WriteLine($"Із масиву символів: {fromChars}");
Console.WriteLine($"OrdinalIgnoreCase: {string.Equals("i10", "I10", StringComparison.OrdinalIgnoreCase)}");
```
