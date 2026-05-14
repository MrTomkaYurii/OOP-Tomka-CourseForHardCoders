---
chapter: 9
chapterTitle: "Розділ 9. Pattern matching"
section: 4
number: "9.4"
title: "Позиційний патерн"
source: "../_combined/59-pozytsiinyi-patern.md"
---

## 9.4. Позиційний патерн

Позиційний патерн застосовується до типу, який має метод деконструктора. Наприклад, визначимо наступний клас:

```csharp
class MessageDetails
{
    public string Language { get; set; } = "";    // мова користувача
    public string DateTime { get; set; } = "";    // час доби
    public string Status { get; set; } = "";      // статус користувача

    public void Deconstruct(out string lang, out string datetime, out string status)
    {
        lang = Language;
        datetime = DateTime;
        status = Status;
    }
}
```

Тепер використовуємо позиційний патерн і в залежності від значень об'єкта MessageDetails повернемо певне повідомлення:

```csharp
string GetWelcome(MessageDetails details) => details switch
{
    ("english", "morning", _) => "Good morning",
    ("english", "evening", _) => "Good evening",
    ("german", "morning", _) => "Guten Morgen",
    ("german", "evening", _) => "Guten Abend",
    (_, _, "admin") => "Hello, Admin",
    _ => "Вітання"
};
```

Фактично цей патерн схожий на приклад із кортежами вище, тільки тепер замість кортежу в конструкцію switch передається об'єкт MessageDetails. Через метод деконструктора ми можемо отримати набір вихідних параметрів у вигляді кортежу і знову ж таки по позиції порівнювати їх з деякими значеннями в конструкції switch.

Застосування:

```csharp
MessageDetails details1 = new MessageDetails
{
    Language = "english",
    DateTime = "evening",
    Status = "user"
};

string message = GetWelcome(details1);
Console.WriteLine(message);  // Good evening

MessageDetails details2 = new MessageDetails
{
    Language = "french",
    DateTime = "morning",
    Status = "admin"
};

message = GetWelcome(details2);
Console.WriteLine(message);  // Hello, Admin
```

Також ми можемо взяти значення об'єкта MessageDetails та використовувати їх при створенні результату методу:

```csharp
string GetWelcome(MessageDetails details) => details switch
{
    ("english", "morning", _) => "Good morning",
    ("english", "evening", _) => "Good evening",
    ("german", "morning", _) => "Guten Morgen",
    ("german", "evening", _) => "Guten Abend",
    (_, _, "admin") => "Hello, Admin",
    (var lang, var datetime, var status) => $"{lang} not found, {datetime} unknown, {status} undefined",
    _ => "Вітання"
};
```

У передостанній інструкції в конструкції switch отримуємо за позицією значення з MessageDetails в змінні lang, datetime і status і використовуємо їх для створення повідомлення:

```csharp
MessageDetails details1 = new MessageDetails
{
    Language = "chinese",
    DateTime = "night",
    Status = "moderator"
};
string message = GetWelcome(details1);
Console.WriteLine(message);
// chinese not found, night unknown, moderator undefined
```
