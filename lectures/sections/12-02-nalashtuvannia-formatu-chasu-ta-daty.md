---
chapter: 12
chapterTitle: "Розділ 12. Робота з датами та часом"
section: 2
number: "12.2"
title: "Налаштування формату часу та дати"
source: "../_combined/76-nalashtuvannia-formatu-chasu-ta-daty.md"
---

## 12.2. Налаштування формату часу та дати

Об'єкт `DateTime` зберігає дату і час як точне числове значення — але виводити його на екран потрібно в людиночитному форматі. Проблема: у різних країнах ці формати різні. У США пишуть `06/11/2026`, в Україні — `11.06.2026`, у міжнародних стандартах — `2026-06-11`. Медичні системи мають підтримувати чітко визначені формати для обміну даними між установами, для друку документів та для зберігання в базах даних.

Клас `DateTime` вирішує це через метод `ToString(format)`, де `format` — рядок із специфікаторами форматування.

![Форматування DateTime — стандартні та кастомні специфікатори](_assets/12-02/datetime-formatting.png)

## Стандартні специфікатори форматування

Стандартні специфікатори — це однолітерні коди, що дають готові локалізовані формати. Їхній вивід залежить від поточної культури (`CultureInfo`) операційної системи — тому `"d"` в Україні дає `11.06.2026`, а в США — `6/11/2026`:

```csharp
DateTime now = new DateTime(2026, 6, 11, 14, 45, 20);

Console.WriteLine(now.ToString("d")); // 11.06.2026       — коротка дата
Console.WriteLine(now.ToString("D")); // 11 червня 2026 р.— довга дата
Console.WriteLine(now.ToString("t")); // 14:45            — короткий час
Console.WriteLine(now.ToString("T")); // 14:45:20         — довгий час
Console.WriteLine(now.ToString("f")); // 11 червня 2026 р. 14:45
Console.WriteLine(now.ToString("F")); // 11 червня 2026 р. 14:45:20
Console.WriteLine(now.ToString("g")); // 11.06.2026 14:45
Console.WriteLine(now.ToString("G")); // 11.06.2026 14:45:20
```

Важливо розуміти різницю між великою і малою літерою: `"d"` — коротка дата, `"D"` — довга; `"t"` — короткий час, `"T"` — довгий. Аналогічно для `f/F` і `g/G`.

Повна таблиця стандартних специфікаторів:

| Специфікатор | Приклад | Опис |
|---|---|---|
| `d` | `11.06.2026` | Коротка дата |
| `D` | `11 червня 2026 р.` | Довга дата |
| `t` | `14:45` | Короткий час |
| `T` | `14:45:20` | Довгий час |
| `f` | `11 червня 2026 р. 14:45` | Довга дата + короткий час |
| `F` | `11 червня 2026 р. 14:45:20` | Довга дата + довгий час |
| `g` | `11.06.2026 14:45` | Коротка дата + короткий час |
| `G` | `11.06.2026 14:45:20` | Коротка дата + довгий час (за замовчуванням) |
| `M` або `m` | `11 червня` | Місяць і день |
| `Y` або `y` | `червень 2026 р.` | Рік і місяць |
| `s` | `2026-06-11T14:45:20` | ISO 8601 (без часового поясу) |
| `O` або `o` | `2026-06-11T14:45:20.000+02:00` | ISO 8601 з часовим поясом |
| `R` або `r` | `Thu, 11 Jun 2026 12:45:20 GMT` | RFC 1123 (HTTP-заголовки) |
| `u` | `2026-06-11 14:45:20Z` | UTC sortable |

Специфікатор `"s"` (ISO 8601) є особливо важливим у медичній інформатиці: стандарт HL7 FHIR, що використовується для обміну медичними даними між системами, вимагає саме ISO 8601 для дат. Специфікатор `"O"` дає повний ISO 8601 з offset часового поясу.

## Кастомні специфікатори форматування

Кастомні специфікатори дають повний контроль над форматом. Вони комбінуються довільно в рядку формату:

```csharp
DateTime now = new DateTime(2026, 6, 11, 14, 45, 20, 123);

Console.WriteLine(now.ToString("dd.MM.yyyy"));          // 11.06.2026
Console.WriteLine(now.ToString("dd/MM/yyyy HH:mm:ss")); // 11/06/2026 14:45:20
Console.WriteLine(now.ToString("yyyy-MM-dd"));          // 2026-06-11 (ISO дата)
Console.WriteLine(now.ToString("d MMMM yyyy р."));      // 11 червня 2026 р.
Console.WriteLine(now.ToString("dddd, d MMMM"));        // четвер, 11 червня
Console.WriteLine(now.ToString("HH:mm:ss.fff"));        // 14:45:20.123
```

Повна таблиця кастомних специфікаторів:

| Специфікатор | Опис | Приклад |
|---|---|---|
| `yyyy` | Рік 4 цифри | `2026` |
| `yy` | Рік 2 цифри | `26` |
| `MM` | Місяць 2 цифри | `06` |
| `MMM` | Місяць коротко | `чер` |
| `MMMM` | Місяць повністю | `червень` |
| `dd` | День 2 цифри | `11` |
| `d` | День без нуля | `11` або `1` |
| `ddd` | День тижня коротко | `Чт` |
| `dddd` | День тижня повністю | `четвер` |
| `HH` | Година 24h (00-23) | `14` |
| `hh` | Година 12h (01-12) | `02` |
| `mm` | Хвилина (00-59) | `45` |
| `ss` | Секунда (00-59) | `20` |
| `fff` | Мілісекунди | `123` |
| `tt` | AM/PM | `PM` |
| `zzz` | Зсув часового поясу | `+02:00` |

Якщо рядок формату містить лише один символ — він може бути інтерпретований як **стандартний** специфікатор. Щоб рядок з одним кастомним символом розпізнався правильно, ставте перед ним `%`: `now.ToString("%d")` → `11`, а не `"D"` (довга дата).

## Культура та CultureInfo

За замовчуванням `ToString(format)` використовує культуру поточного потоку (`Thread.CurrentThread.CurrentCulture`). Щоб форматувати незалежно від регіональних налаштувань, передається другий параметр `IFormatProvider`:

```csharp
using System.Globalization;

DateTime dt = new DateTime(2026, 6, 11, 14, 45, 20);

// Явна культура — незалежна від ОС
string ua  = dt.ToString("dd.MM.yyyy", CultureInfo.GetCultureInfo("uk-UA")); // 11.06.2026
string us  = dt.ToString("MM/dd/yyyy", CultureInfo.GetCultureInfo("en-US")); // 06/11/2026
string iso = dt.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture);        // 2026-06-11

Console.WriteLine(ua);
Console.WriteLine(us);
Console.WriteLine(iso);
```

`CultureInfo.InvariantCulture` — культура, що не прив'язана до жодної конкретної мови чи регіону. Її використовують для **зберігання і передачі** дат між системами (файли, API, бази даних), де однакове форматування є критичним. Для **відображення** в UI — краще використовувати культуру користувача.

## Парсинг: перетворення рядка у DateTime

Зворотна операція — перетворення рядка у `DateTime` — не менш важлива. Наприклад, читаємо дату народження пацієнта з поля форми або з CSV-файлу.

**`DateTime.Parse(s)`** — найпростіший варіант. Розпізнає багато поширених форматів автоматично, але залежить від культури і кидає `FormatException` при невдачі:

```csharp
DateTime dt = DateTime.Parse("11.06.2026 14:45"); // OK для uk-UA культури
```

**`DateTime.TryParse(s, out DateTime result)`** — безпечний варіант: не кидає виняток, а повертає `false` при невдачі. Рекомендований для обробки введення від користувача:

```csharp
string input = "11.06.2026";
if (DateTime.TryParse(input, out DateTime result))
    Console.WriteLine($"Розпізнано: {result:dd.MM.yyyy}");
else
    Console.WriteLine("Некоректна дата");
```

**`DateTime.ParseExact(s, format, provider)`** — парсинг з точно вказаним форматом. Якщо формат відомий наперед (наприклад, дані приходять із зовнішньої системи у фіксованому вигляді), цей метод є найнадійнішим:

```csharp
using System.Globalization;

// Формат з медичної інформаційної системи: "рр/ММ/дд"
DateTime dt = DateTime.ParseExact(
    "26/06/11",
    "yy/MM/dd",
    CultureInfo.InvariantCulture);
Console.WriteLine(dt); // 11.06.2026 0:00:00
```

**`DateTime.TryParseExact(s, format, provider, style, out result)`** — комбінація точного формату і безпечного повернення bool. Найбільш рекомендований варіант для парсингу в медичних системах:

```csharp
using System.Globalization;

string raw = "11.06.2026 14:30";
bool ok = DateTime.TryParseExact(
    raw,
    "dd.MM.yyyy HH:mm",
    CultureInfo.InvariantCulture,
    DateTimeStyles.None,
    out DateTime admission);

if (ok)
    Console.WriteLine($"Прийом: {admission:F}");
```

## Форматування дат у медичних документах — runnable приклад

Використання стандартних і кастомних специфікаторів для різних форматів виводу:

```csharp run
using System;

DateTime admission = new DateTime(2026, 6, 11, 9, 30, 0);
DateTime discharge = new DateTime(2026, 6, 18, 14, 0, 0);
DateTime birth     = new DateTime(1958, 4, 15);

Console.WriteLine("=== Виписний епікриз ===");
Console.WriteLine($"Дата народження:  {birth:dd MMMM yyyy р.}");
Console.WriteLine($"Дата вступу:      {admission:dd.MM.yyyy HH:mm}");
Console.WriteLine($"Дата виписки:     {discharge:dd.MM.yyyy HH:mm}");
Console.WriteLine($"День тижня вступу: {admission:dddd}");

Console.WriteLine("\n=== Формати для різних цілей ===");
Console.WriteLine($"Для звіту (UA):   {discharge:D}");
Console.WriteLine($"Для бази даних:   {discharge:yyyy-MM-ddTHH:mm:ss}");
Console.WriteLine($"ISO 8601:         {discharge:s}");
Console.WriteLine($"Тільки час:       {admission:HH:mm:ss}");
Console.WriteLine($"Місяць і день:    {admission:d MMMM}");

Console.WriteLine("\n=== Розрахунки ===");
TimeSpan stay = discharge - admission;
Console.WriteLine($"Тривалість: {stay.Days} днів {stay.Hours} годин");

int age = DateTime.Today.Year - birth.Year;
if (birth > DateTime.Today.AddYears(-age)) age--;
Console.WriteLine($"Вік пацієнта: {age} р.");
```

## Парсинг та валідація введення — runnable приклад

Безпечний парсинг дат із різними форматами введення:

```csharp run
using System;
using System.Globalization;

Console.WriteLine("=== TryParse: гнучкий парсинг ===");
string[] inputs = { "11.06.2026", "2026-06-11", "11/06/2026", "abc", "32.13.2026" };

foreach (var s in inputs)
{
    if (DateTime.TryParse(s, out DateTime dt))
        Console.WriteLine($"  '{s}' -> OK: {dt:dd.MM.yyyy}");
    else
        Console.WriteLine($"  '{s}' -> ПОМИЛКА: некоректна дата");
}

Console.WriteLine("\n=== TryParseExact: точний формат ===");
string[] records = {
    "15.04.1958",
    "11.06.2026",
    "1958/04/15",   // неправильний формат
    "29.02.2026",   // 2026 не високосний
};

foreach (var s in records)
{
    bool ok = DateTime.TryParseExact(
        s, "dd.MM.yyyy",
        CultureInfo.InvariantCulture,
        DateTimeStyles.None,
        out DateTime dt);

    Console.WriteLine(ok
        ? $"  '{s}' -> {dt:D}"
        : $"  '{s}' -> ПОМИЛКА формату або дата не існує");
}

Console.WriteLine("\n=== ParseExact: ISO 8601 з зовнішньої системи ===");
string isoDate = "2026-06-11T09:30:00";
DateTime parsed = DateTime.ParseExact(isoDate, "yyyy-MM-ddTHH:mm:ss", CultureInfo.InvariantCulture);
Console.WriteLine($"ISO вхід:  {isoDate}");
Console.WriteLine($"Результат: {parsed:F}");
```
