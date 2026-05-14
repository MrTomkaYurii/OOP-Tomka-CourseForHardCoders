---
chapter: 12
chapterTitle: "Розділ 12. Робота з датами та часом"
section: 2
number: "12.2"
title: "Налаштування формату часу та дати"
source: "../_combined/76-nalashtuvannia-formatu-chasu-ta-daty.md"
---

## 12.2. Налаштування формату часу та дати

Не завжди зручне використання вбудованих форматів дати та часу. Іноді буває необхідно встановити власну форму відображення об'єкта `DateTime`. У цьому випадку ми можемо скласти свій формат з описувачів:

Створимо пару своїх форматів:

```csharp
DateTime now = DateTime.Now;
Console.WriteLine(now.ToString("hh:mm:ss"));
Console.WriteLine(now.ToString("dd.MM.yyyy"));
```

Консольний вивід:

```text
02:46:38
06.01.2022
```
