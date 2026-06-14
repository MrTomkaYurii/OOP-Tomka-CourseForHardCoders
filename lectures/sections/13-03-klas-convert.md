---
chapter: 13
chapterTitle: "Розділ 13. Додаткові класи та структури .NET"
section: 3
number: "13.3"
title: "Клас Convert"
source: "../_combined/80-klas-convert.md"
---

## 13.3. Клас `Convert`

У реальних застосунках дані постійно змінюють форму: рядок із форми стає числом, ціле число перетворюється на рядок для JSON, булеве значення записується як 1 або 0 у базу даних, бінарний вміст файлу кодується у Base64 для передачі через API. Для всіх цих потреб .NET надає статичний клас `Convert` із простору імен `System`.

На відміну від оператора явного приведення `(int)`, `Convert` розроблений для сценаріїв, де тип вхідного значення може бути невідомий на етапі компіляції, де рядок потрібно розпарсити у число, або де важлива семантика заокруглення. Клас реалізує перетворення через інтерфейс `IConvertible`, який реалізують усі базові типи .NET.

![Клас Convert — перетворення типів](_assets/13-03/convert-overview.png)

## Parse та TryParse

Найпростіший шлях перетворити рядок на примітивний тип — методи `Parse()` та `TryParse()`, які визначені безпосередньо на кожному числовому типі.

`Parse()` приймає рядок і повертає значення потрібного типу. Якщо рядок не відповідає очікуваному формату, кидається `FormatException`:

```csharp run
using System;

int    age    = int.Parse("67");
double weight = double.Parse("82.5");
bool   active = bool.Parse("True");

Console.WriteLine($"Вік: {age}, Вага: {weight}, Активний: {active}");
```

Важливий нюанс: парсинг дробових чисел залежить від поточної культури. На машинах з українською/польською локаллю `double.Parse("82.5")` може кинути виняток, бо очікується кома. Щоб гарантувати крапку як роздільник — використовуйте `CultureInfo.InvariantCulture`:

```csharp run
using System;
using System.Globalization;

double weight1 = double.Parse("82.5", CultureInfo.InvariantCulture); // завжди крапка
double weight2 = double.Parse("82,5", new NumberFormatInfo { NumberDecimalSeparator = "," });

Console.WriteLine($"{weight1}  {weight2}");
```

`TryParse()` — безпечна альтернатива, що не кидає виняток: повертає `true` якщо перетворення пройшло успішно, `false` інакше. Значення записується в `out`-параметр:

```csharp run
using System;

string[] inputs = { "67", "abc", "3.14", "" };

foreach (string s in inputs)
{
    if (int.TryParse(s, out int value))
        Console.WriteLine($"'{s}' -> {value}");
    else
        Console.WriteLine($"'{s}' -> не вдалось розпарсити");
}
```

Правило вибору: якщо рядок надходить від користувача або з ненадійного джерела — використовуйте `TryParse`. Якщо рядок гарантовано правильного формату (з власної БД, відомого API) — `Parse`. `Convert.ToXxx` підходить для перетворень між числовими типами та булевими значеннями, а не тільки для рядків.

## Cast vs Convert: в чому різниця

Щоб зрозуміти призначення `Convert`, важливо спочатку побачити, чим він відрізняється від оператора явного приведення типу `(T)`.

Оператор `(int)` виконує **усічення** (truncation): він просто відкидає дробову частину, не округлюючи:

```csharp
double d = 3.9;
int a = (int)d;                 // 3  — дробова частина відкинута
int b = Convert.ToInt32(d);     // 4  — банківське заокруглення
```

`Convert.ToInt32` застосовує **банківське заокруглення** (як `Math.Round` з MidpointRounding.ToEven), тому `3.5 → 4` і `2.5 → 2`. Це важливо для медичних розрахунків, де джерелом числа може бути `double`, але результат потрібен у цілочисельній формі.

Ще одна принципова відмінність: `(int)` можна застосувати тільки до сумісних числових типів — компілятор не дозволить `(int)"42"` або `(int)true`. `Convert` же здатен перетворити рядок у число, `bool` у `int` і навпаки:

```csharp
// Це не компілюється:
// int x = (int)"42";   // CS0030

// Це працює:
int x = Convert.ToInt32("42"); // 42
int y = Convert.ToInt32(true); // 1
int z = Convert.ToInt32(false);// 0
```

## Числові перетворення

Методи `Convert.ToInt32`, `Convert.ToInt64`, `Convert.ToDouble`, `Convert.ToDecimal` тощо приймають `object` або будь-який тип, що реалізує `IConvertible`. Якщо передати `null` — повертається нуль або значення за замовчуванням:

```csharp
int fromNull    = Convert.ToInt32(null);   // 0
double fromNull = Convert.ToDouble(null);  // 0.0
```

Якщо передати рядок, що не є числом, — кидається `FormatException`:

```csharp
int bad = Convert.ToInt32("abc"); // FormatException!
```

Тому для ненадійних вхідних рядків слід використовувати `int.TryParse` або `double.TryParse` — вони повертають `bool` замість викидання виняткового стану. `Convert` підходить тоді, коли формат даних гарантований (наприклад, дані з власної бази або відомого API).

При переповненні (overflow) `Convert.ToInt32` кидає `OverflowException`:

```csharp
Convert.ToInt32(3_000_000_000L); // OverflowException — не вміщується в int
```

Це **безпечніша** поведінка, ніж `(int)3_000_000_000L`, який мовчки дасть некоректний результат через переповнення.

## Перетворення рядків: Convert.ToString та Convert.ToXxx

`Convert.ToString(object value)` перетворює будь-яке значення в рядок. Принципова відмінність від виклику `.ToString()` безпосередньо — коректна обробка `null`:

```csharp
string s1 = Convert.ToString(null);   // "" — порожній рядок, не виняток
string s2 = null?.ToString();         // null — не рядок
```

Якщо поле пацієнта необов'язкове і може бути `null`, `Convert.ToString` дозволяє отримати рядок для відображення без додаткової перевірки `if (x != null)`.

`Convert.ToDateTime(string)` перетворює рядок у `DateTime`, орієнтуючись на поточну культуру. Для надійного парсингу з явним форматом краще використовувати `DateTime.ParseExact` або `DateTime.TryParseExact` (розд. 12.2).

## Булеві перетворення

`Convert.ToBoolean` розпізнає числові та рядкові представлення булевих значень:

```csharp
bool b1 = Convert.ToBoolean(1);       // true
bool b2 = Convert.ToBoolean(0);       // false
bool b3 = Convert.ToBoolean("True");  // true  (регістронезалежно)
bool b4 = Convert.ToBoolean("False"); // false
bool b5 = Convert.ToBoolean("yes");   // FormatException! (тільки True/False)
```

Зворотньо — `Convert.ToInt32(bool)` дає `1` або `0`, що зручно при запису в бази даних, де `bool` зберігається як `BIT` або `TINYINT`.

## Base64 — кодування бінарних даних

`Convert.ToBase64String(byte[])` і `Convert.FromBase64String(string)` — два методи для кодування бінарних даних у текстовий формат Base64 і назад.

Base64 перетворює довільні байти у рядок із символів ASCII (64 символи: A-Z, a-z, 0-9, +, /). Це стандарт передачі бінарних даних у текстових протоколах:

```csharp
byte[] data = { 72, 101, 108, 108, 111 }; // "Hello" у ASCII

string encoded = Convert.ToBase64String(data);
Console.WriteLine(encoded); // "SGVsbG8="

byte[] decoded = Convert.FromBase64String(encoded);
Console.WriteLine(System.Text.Encoding.ASCII.GetString(decoded)); // "Hello"
```

У медичній інформатиці Base64 з'являється у стандарті **HL7 FHIR**: зображення (рентген, УЗД), PDF-документи і файли аналізів передаються у JSON-відповідях API у форматі Base64. При отриманні такого поля `Convert.FromBase64String` повертає масив байтів, який потім зберігається або відображається.

```csharp
// Приклад поля у FHIR-документі:
// { "data": "SGVsbG8=" }

string fhirData = "SGVsbG8=";
byte[] documentBytes = Convert.FromBase64String(fhirData);
// далі: File.WriteAllBytes("document.pdf", documentBytes)
```

## Convert.ChangeType — динамічне перетворення

`Convert.ChangeType(object value, Type conversionType)` — найгнучкіший метод класу. Він приймає значення і тип як `Type`, виконуючи перетворення у рантаймі:

```csharp
object result = Convert.ChangeType("42", typeof(int));
int number = (int)result; // 42

object d = Convert.ChangeType("3.14", typeof(double));
```

Це корисно в узагальненому (generic) коді, де тип перетворення стає відомим лише під час виконання: наприклад, при заповненні властивостей об'єкта з рядкового словника (десеріалізація, читання CSV із заголовками, відображення форм).

`ChangeType` також кидає `FormatException` якщо рядок некоректний, та `OverflowException` при переповненні — ті самі виняткові стани, що й конкретні методи `ToInt32`, `ToDouble` тощо.

## Парсинг даних пацієнта — runnable приклад

Читання клінічних даних пацієнта з рядкового представлення (наприклад, CSV або API-відповідь):

```csharp run
using System;

Console.WriteLine("=== Зчитування даних пацієнта з рядків ===");

// Симуляція даних, що прийшли з форми або CSV
string nameRaw     = "Петренко Іван";
string ageRaw      = "67";
string weightRaw   = "82.5";
string heightRaw   = "1.76";
string activeRaw   = "1";
string diagnosisRaw = null; // необов'язкове поле

// Convert для гарантовано коректних рядків
int    age     = Convert.ToInt32(ageRaw);
double weight  = Convert.ToDouble(weightRaw);
double height  = Convert.ToDouble(heightRaw);
bool   active  = Convert.ToBoolean(activeRaw == "1" ? "True" : "False");
string diag    = Convert.ToString(diagnosisRaw); // "" якщо null

double bmi = weight / (height * height);

Console.WriteLine($"Пацієнт:   {nameRaw}");
Console.WriteLine($"Вік:       {age} р.");
Console.WriteLine($"Вага/зріст:{weight} кг / {height} м");
Console.WriteLine($"ІМТ:       {Math.Round(bmi, 1)}");
Console.WriteLine($"Активний:  {active}");
Console.WriteLine($"Діагноз:   '{diag}' (пустий рядок, не null)");

Console.WriteLine("\n=== Різниця: cast vs Convert ===");
double d = 3.7;
Console.WriteLine($"(int)3.7              = {(int)d}      // Truncate");
Console.WriteLine($"Convert.ToInt32(3.7)  = {Convert.ToInt32(d)}      // Round");

double half = 2.5;
Console.WriteLine($"(int)2.5              = {(int)half}      // Truncate");
Console.WriteLine($"Convert.ToInt32(2.5)  = {Convert.ToInt32(half)}      // ToEven = 2");

Console.WriteLine("\n=== Захист від FormatException ===");
string[] inputs = { "45", "abc", "22.5", "" };
foreach (var s in inputs)
{
    try
    {
        int val = Convert.ToInt32(s);
        Console.WriteLine($"  '{s}' -> {val}");
    }
    catch (FormatException)
    {
        Console.WriteLine($"  '{s}' -> FormatException (використовуй TryParse!)");
    }
    catch (OverflowException)
    {
        Console.WriteLine($"  '{s}' -> OverflowException");
    }
}
```

## Base64 і ChangeType — runnable приклад

```csharp run
using System;
using System.Text;

Console.WriteLine("=== Base64: медичний ідентифікатор ===");

// Унікальний ідентифікатор пацієнта для передачі через API
string patientId = "UA-2026-PETRO-I10";
byte[] idBytes   = Encoding.UTF8.GetBytes(patientId);

string encoded = Convert.ToBase64String(idBytes);
Console.WriteLine($"Оригінал:  {patientId}");
Console.WriteLine($"Base64:    {encoded}");

byte[] decoded  = Convert.FromBase64String(encoded);
string restored = Encoding.UTF8.GetString(decoded);
Console.WriteLine($"Відновлено:{restored}");
Console.WriteLine($"Ідентично: {patientId == restored}");

Console.WriteLine("\n=== Base64: бінарні дані ===");
byte[] fakeDicom = { 0x44, 0x49, 0x43, 0x4D }; // "DICM" — початок DICOM-файлу
string b64 = Convert.ToBase64String(fakeDicom);
Console.WriteLine($"DICOM header bytes: {string.Join(", ", fakeDicom)}");
Console.WriteLine($"Base64: {b64}");
byte[] backBytes = Convert.FromBase64String(b64);
Console.WriteLine($"Відновлено байти:   {string.Join(", ", backBytes)}");

Console.WriteLine("\n=== Convert.ChangeType: динамічне перетворення ===");

// Словник даних — тип значення невідомий заздалегідь
string[] keys   = { "age", "weight", "active", "name" };
string[] values = { "67",  "82.5",   "True",   "Петренко Іван" };
Type[]   types  = { typeof(int), typeof(double), typeof(bool), typeof(string) };

for (int i = 0; i < keys.Length; i++)
{
    object result = Convert.ChangeType(values[i], types[i]);
    Console.WriteLine($"  {keys[i],-8}: \"{values[i],-14}\" -> {result,-16} ({result.GetType().Name})");
}
```
