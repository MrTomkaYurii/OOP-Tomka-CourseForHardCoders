---
chapter: 12
chapterTitle: "Розділ 12. Робота з датами та часом"
section: 5
number: "12.5"
title: "DateTimeOffset та часові пояси"
source: "../_combined/79-datetimeoffset-ta-chasovi-poiasy.md"
---

## 12.5. DateTimeOffset та часові пояси

Медичні інформаційні системи дедалі частіше є розподіленими: сервери можуть знаходитися в різних часових поясах, пацієнти проходять лікування в різних країнах, телемедичні консультації перетинають кордони. У такому середовищі `DateTime` вже недостатньо — він не містить інформацію про те, до якого поясу прив'язаний час. Для цього призначені `DateTimeOffset` і `TimeZoneInfo`.

![Парсинг DateTime та DateTimeOffset — безпечне перетворення рядків](_assets/12-05/parsing-and-datetimeoffset.png)

## Типи парсингу DateTime

Перетворення рядка у `DateTime` — одна з найчастіших операцій при читанні даних з форм, файлів, API. Є чотири основних методи, що відрізняються гнучкістю і безпекою:

### DateTime.Parse — гнучко, але небезпечно

`Parse` розпізнає багато поширених форматів, але залежить від поточної культури і кидає `FormatException` якщо рядок некоректний. Підходить для контрольованих внутрішніх сценаріїв, але **не для вводу від користувача**:

```csharp
DateTime dt = DateTime.Parse("11.06.2026 14:45"); // OK для uk-UA
// DateTime.Parse("abc") → FormatException !!!
```

### DateTime.TryParse — безпечний варіант

`TryParse` ніколи не кидає виняток — при невдачі повертає `false`, а `out`-параметр отримує `DateTime.MinValue`. Рекомендований для обробки будь-якого введення від користувача:

```csharp
string input = "11.06.2026";
if (DateTime.TryParse(input, out DateTime result))
    Console.WriteLine($"OK: {result:dd.MM.yyyy}");
else
    Console.WriteLine("Некоректна дата");
```

### DateTime.ParseExact — точний формат

`ParseExact` вимагає точного відповідного формату. Якщо рядок не відповідає — `FormatException`. Використовується коли формат гарантований (дані з відомої зовнішньої системи):

```csharp
using System.Globalization;

// Дата з HL7-повідомлення: формат YYYYMMDD
DateTime dt = DateTime.ParseExact("20260611", "yyyyMMdd", CultureInfo.InvariantCulture);
Console.WriteLine(dt); // 11.06.2026 0:00:00
```

Важливо: другий параметр може бути **масивом форматів** — тоді метод перебирає їх по черзі:

```csharp
string[] formats = { "dd.MM.yyyy", "yyyy-MM-dd", "dd/MM/yyyy" };
DateTime dt = DateTime.ParseExact("2026-06-11", formats, CultureInfo.InvariantCulture,
                                   DateTimeStyles.None);
```

### DateTime.TryParseExact — найбезпечніший

Поєднує точний формат з безпечним поверненням `bool`. Найрекомендованіший для медичних систем:

```csharp
using System.Globalization;

bool ok = DateTime.TryParseExact(
    "11.06.2026 14:30",
    "dd.MM.yyyy HH:mm",
    CultureInfo.InvariantCulture,
    DateTimeStyles.None,
    out DateTime admission);

if (ok)
    Console.WriteLine($"Прийом: {admission:F}");
else
    Console.WriteLine("Некоректний формат дати/часу");
```

## DateTimeOffset — час із зсувом від UTC

`DateTimeOffset` — це структура, яка зберігає **`DateTime` разом із зсувом від UTC** (`TimeSpan offset`). Це дозволяє точно представляти момент часу незалежно від часового поясу сервера, де виконується код.

Порівняння з `DateTime`:

| | `DateTime` | `DateTimeOffset` |
|--|------------|-----------------|
| Зберігає | Дата + час | Дата + час + offset від UTC |
| Kind | Unspecified / Local / Utc | Завжди несе offset |
| Рівність `==` | Порівнює значення (без offset) | Порівнює UTC-еквіваленти |
| Для UI | Зручно | Зручно |
| Для БД / API | Ризик помилок часового поясу | Рекомендовано |

### Створення DateTimeOffset

```csharp
using System;

// Поточний час зі зсувом Local
DateTimeOffset now = DateTimeOffset.Now;        // Kind=Local + offset
DateTimeOffset utc = DateTimeOffset.UtcNow;     // UTC, offset = +00:00

// Явно задати: час 14:30 з зсувом +02:00 (Київ, зима)
DateTimeOffset appointment = new DateTimeOffset(
    2026, 6, 11, 14, 30, 0,
    TimeSpan.FromHours(3)); // літній час UTC+3

// Із DateTime + offset
DateTime dt  = new DateTime(2026, 6, 11, 14, 30, 0);
TimeSpan off = TimeSpan.FromHours(3);
DateTimeOffset dto = new DateTimeOffset(dt, off);

Console.WriteLine(appointment); // 11.06.2026 14:30:00 +03:00
```

### Властивості DateTimeOffset

| Властивість | Опис |
|-------------|------|
| `Offset` | Зсув від UTC як `TimeSpan` |
| `UtcDateTime` | Відповідний `DateTime` в UTC |
| `LocalDateTime` | Відповідний `DateTime` в локальному часі |
| `DateTime` | `DateTime` без offset-мітки (Kind=Unspecified) |
| `UtcTicks` | Тіки в UTC |

```csharp
DateTimeOffset dto = new DateTimeOffset(2026, 6, 11, 14, 30, 0, TimeSpan.FromHours(3));

Console.WriteLine(dto.Offset);        // +03:00
Console.WriteLine(dto.UtcDateTime);   // 11.06.2026 11:30:00
Console.WriteLine(dto.LocalDateTime); // залежить від ОС
```

### DateTimeOffset та рівність

Ключова відмінність від `DateTime`: два `DateTimeOffset` **рівні**, якщо вони представляють один і той самий момент у UTC, навіть якщо зберігають різні зсуви:

```csharp
DateTimeOffset kyiv   = new DateTimeOffset(2026, 6, 11, 14, 30, 0, TimeSpan.FromHours(3));
DateTimeOffset london = new DateTimeOffset(2026, 6, 11, 11, 30, 0, TimeSpan.FromHours(0));

Console.WriteLine(kyiv == london); // true — той самий момент у UTC
```

Саме це робить `DateTimeOffset` надійним для зберігання в базі даних: порівняння дат між записами з різних серверів дає коректний результат.

## TimeZoneInfo — робота з часовими поясами

Клас `TimeZoneInfo` дозволяє знаходити часові пояси і конвертувати між ними. Він розташований у `System` і не потребує додаткових просторів імен.

```csharp
// Поточний часовий пояс ОС
TimeZoneInfo local = TimeZoneInfo.Local;
Console.WriteLine(local.DisplayName); // (UTC+02:00) Helsinkі, Kyiv, Riga, Sofia...

// UTC
TimeZoneInfo utcZone = TimeZoneInfo.Utc;

// Конкретний пояс за ID (крос-платформений ID IANA або Windows ID)
TimeZoneInfo kyivTz = TimeZoneInfo.FindSystemTimeZoneById("FLE Standard Time"); // Windows
// або "Europe/Kiev" на Linux/macOS
```

### Конвертація між поясами

```csharp
DateTime utcTime = new DateTime(2026, 6, 11, 11, 30, 0, DateTimeKind.Utc);

TimeZoneInfo kyivTz   = TimeZoneInfo.FindSystemTimeZoneById("FLE Standard Time");
TimeZoneInfo berlinTz = TimeZoneInfo.FindSystemTimeZoneById("W. Europe Standard Time");

DateTime kyivTime   = TimeZoneInfo.ConvertTimeFromUtc(utcTime, kyivTz);
DateTime berlinTime = TimeZoneInfo.ConvertTimeFromUtc(utcTime, berlinTz);

Console.WriteLine($"UTC:    {utcTime:HH:mm}");   // 11:30
Console.WriteLine($"Київ:   {kyivTime:HH:mm}");  // 14:30 (UTC+3)
Console.WriteLine($"Берлін: {berlinTime:HH:mm}"); // 13:30 (UTC+2)
```

### Перехід на літній/зимовий час

`TimeZoneInfo` автоматично враховує перехід на літній і зимовий час (DST — Daylight Saving Time). Метод `IsDaylightSavingTime(dt)` дозволяє перевірити, чи діє в даний момент літній час:

```csharp
TimeZoneInfo kyivTz = TimeZoneInfo.FindSystemTimeZoneById("FLE Standard Time");

DateTime summer = new DateTime(2026, 7, 1);   // літо — UTC+3
DateTime winter = new DateTime(2026, 12, 1);  // зима — UTC+2

Console.WriteLine($"Літо DST:  {kyivTz.IsDaylightSavingTime(summer)}"); // True
Console.WriteLine($"Зима DST:  {kyivTz.IsDaylightSavingTime(winter)}"); // False
Console.WriteLine($"Літо offset: {kyivTz.GetUtcOffset(summer)}"); // +03:00
Console.WriteLine($"Зима offset: {kyivTz.GetUtcOffset(winter)}"); // +02:00
```

## Рекомендації для медичних систем

Для медичних інформаційних систем, де точність і відтворюваність часових відміток критичні, рекомендуються такі практики:

1. **Зберігати у БД UTC або DateTimeOffset.UtcNow** — ніколи `DateTime.Now`, оскільки локальний час залежить від сервера і може дати неправильний порядок подій при міграції або масштабуванні.

2. **Для аудит-журналів** (коли пацієнт надійшов, коли прийнятий лікар) — `DateTimeOffset.UtcNow`, оскільки він зберігає і UTC-значення і локальний offset.

3. **Для парсингу вводу від користувача** — завжди `TryParseExact` з явно вказаним форматом і `CultureInfo.InvariantCulture`.

4. **Для відображення в UI** — конвертувати UTC у локальний час `TimeZoneInfo.ConvertTimeFromUtc` безпосередньо перед відображенням.

## Парсинг медичних форм — runnable приклад

```csharp run
using System;
using System.Globalization;

Console.WriteLine("=== Парсинг дат із різних джерел ===");

// 1. Форма введення пацієнта
string[] userInputs = { "15.04.1958", "abc", "32.13.2026", "2026-06-11" };
Console.WriteLine("Введення з форми (TryParseExact, dd.MM.yyyy):");
foreach (var s in userInputs)
{
    bool ok = DateTime.TryParseExact(s, "dd.MM.yyyy",
        CultureInfo.InvariantCulture, DateTimeStyles.None, out DateTime dt);
    Console.WriteLine($"  '{s}' -> {(ok ? dt.ToString("dd.MM.yyyy") : "ПОМИЛКА")}");
}

// 2. HL7 FHIR формат: YYYYMMDD або YYYY-MM-DD
string[] fhirDates = { "20260611", "2026-06-11" };
string[] fhirFormats = { "yyyyMMdd", "yyyy-MM-dd" };
Console.WriteLine("\nFHIR формати (ParseExact із масивом):");
foreach (var s in fhirDates)
{
    DateTime dt = DateTime.ParseExact(s, fhirFormats,
        CultureInfo.InvariantCulture, DateTimeStyles.None);
    Console.WriteLine($"  '{s}' -> {dt:dd.MM.yyyy}");
}

// 3. ISO 8601 з часовим поясом
string iso = "2026-06-11T14:30:00+03:00";
DateTimeOffset dto = DateTimeOffset.Parse(iso, CultureInfo.InvariantCulture);
Console.WriteLine($"\nISO 8601: {iso}");
Console.WriteLine($"  UTC:   {dto.UtcDateTime:dd.MM.yyyy HH:mm}");
Console.WriteLine($"  Local: {dto.LocalDateTime:dd.MM.yyyy HH:mm}");
Console.WriteLine($"  Offset: {dto.Offset}");
```

## DateTimeOffset і UTC для аудит-журналу — runnable приклад

```csharp run
using System;

Console.WriteLine("=== Аудит-журнал медичних подій (DateTimeOffset UTC) ===");

var kyivOffset   = TimeSpan.FromHours(3); // Київ, літній час
var berlinOffset = TimeSpan.FromHours(2); // Берлін, літній час

string[] eventLabels = { "Прийом пацієнта", "Забір аналізу", "Теле-консультація" };
DateTimeOffset[] eventTimes = {
    new DateTimeOffset(2026, 6, 11, 9,  0,  0, kyivOffset),   // Київ
    new DateTimeOffset(2026, 6, 11, 10, 30, 0, kyivOffset),   // Київ
    new DateTimeOffset(2026, 6, 11, 9,  45, 0, berlinOffset), // Берлін
};

Console.WriteLine($"{"Подія",-22} {"Місцевий",10} {"UTC",8}  Offset");
Console.WriteLine(new string('-', 55));
for (int i = 0; i < eventTimes.Length; i++)
{
    DateTimeOffset ev = eventTimes[i];
    Console.WriteLine($"{eventLabels[i],-22} {ev.DateTime:HH:mm,10} {ev.UtcDateTime:HH:mm,8}  {ev.Offset:hh\\:mm}");
}

Console.WriteLine("\n=== UTC-момент: порівняння між поясами ===");
// Хто прийшов раніше: Київ 09:00+03 чи Берлін 09:45+02?
DateTimeOffset kyivEvent   = eventTimes[0]; // 09:00 Київ = 06:00 UTC
DateTimeOffset berlinEvent = eventTimes[2]; // 09:45 Берлін = 07:45 UTC
bool kyivFirst = kyivEvent < berlinEvent;
Console.WriteLine($"Київ    09:00+03 → UTC {kyivEvent.UtcDateTime:HH:mm}");
Console.WriteLine($"Берлін  09:45+02 → UTC {berlinEvent.UtcDateTime:HH:mm}");
Console.WriteLine($"Київ раніше: {kyivFirst}");

Console.WriteLine("\n=== DateTimeOffset.UtcNow (рекомендовано для БД) ===");
DateTimeOffset stamp = DateTimeOffset.UtcNow;
Console.WriteLine($"Timestamp UTC: {stamp:yyyy-MM-ddTHH:mm:ssZ}");
Console.WriteLine($"Offset:        {stamp.Offset}");
```
