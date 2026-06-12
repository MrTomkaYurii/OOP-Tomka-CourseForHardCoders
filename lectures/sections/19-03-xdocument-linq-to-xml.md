---
chapter: 19
chapterTitle: "Розділ 19. Серіалізація та десеріалізація. JSON та XML"
section: 3
number: "19.3"
title: "XDocument та LINQ to XML"
source: ""
---

## 19.3. XDocument та LINQ to XML

`XmlDocument` з'явився у .NET 1.0 і повністю реалізує стандарт DOM рівня 1. Але його API проектувався за зразком Java DOM і є досить багатослівним: щоб додати один елемент, потрібно викликати `CreateElement`, `SetAttribute`, `AppendChild` — три окремих виклики. Навігація потребує явного приведення типів. А LINQ-запити до `XmlNodeList` — неможливі без ручного перебору.

.NET 3.5 разом із LINQ представив принципово інший підхід: `System.Xml.Linq`. Класи `XDocument`, `XElement`, `XAttribute` проектувалися **з нуля** під функціональний стиль і LINQ. Результат — код у 2–4 рази коротший, XML будується декларативно (через вкладені конструктори), а LINQ-запити працюють нативно на будь-якій колекції вузлів.

![XDocument vs XmlDocument — порівняння API](_assets/19-03/xdocument-vs-xmldocument.png)

## Декларативне створення XML через XElement

Ключова перевага `XDocument`/`XElement` — **вкладений конструктор**. XML будується в точності так, як він виглядає: вкладені теги = вкладені об'єкти:

```csharp run
using System;
using System.Xml.Linq;

// Один виклик — весь документ
XDocument doc = new XDocument(
    new XDeclaration("1.0", "utf-8", null),
    new XComment("Медична картка пацієнта"),
    new XElement("patientRecord",
        new XAttribute("version", "2.0"),
        new XAttribute("generatedAt", DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss")),

        new XElement("patient",
            new XAttribute("id", "PT-1001"),
            new XAttribute("status", "active"),
            new XElement("name",      "Петренко Іван Олексійович"),
            new XElement("birthDate", "1978-03-15"),
            new XElement("ward",      "Терапія")
        ),

        new XElement("diagnoses",
            new XElement("diagnosis",
                new XAttribute("code",   "J06.9"),
                new XAttribute("system", "ICD-10"),
                "ГРВІ"),
            new XElement("diagnosis",
                new XAttribute("code",   "I10"),
                new XAttribute("system", "ICD-10"),
                "Гіпертонічна хвороба")
        ),

        new XElement("vitals",
            new XAttribute("recordedAt", "2024-03-15T14:30:00"),
            new XElement("temperature", new XAttribute("unit", "C"),   37.2),
            new XElement("pulse",       new XAttribute("unit", "bpm"), 82),
            new XElement("bloodPressure",
                new XElement("systolic",  135),
                new XElement("diastolic",  85))
        )
    )
);

// Виведення з відступами
Console.WriteLine(doc.ToString());
```

Порівняйте: у `XmlDocument` той самий документ потребував би близько 40 рядків з явними `CreateElement`/`AppendChild`. Тут вся структура видна одним поглядом.

## Збереження та завантаження

```csharp run
using System;
using System.IO;
using System.Linq;
using System.Xml.Linq;

string path = Path.Combine(Path.GetTempPath(), "clinic_xdoc.xml");

XDocument doc = new XDocument(
    new XElement("clinic",
        new XElement("patient", new XAttribute("id","PT-1001"),
            new XElement("name","Петренко І.О."),
            new XElement("ward","Терапія")),
        new XElement("patient", new XAttribute("id","PT-1002"),
            new XElement("name","Бойко О.П."),
            new XElement("ward","Кардіологія"))
    )
);

// Save — з автоматичними відступами
doc.Save(path);
Console.WriteLine($"Збережено: {new FileInfo(path).Length.ToString()} байт");
Console.WriteLine(File.ReadAllText(path));

// Load — завантаження з файлу
XDocument loaded = XDocument.Load(path);
Console.WriteLine($"Кореневий елемент: {loaded.Root?.Name}");
Console.WriteLine($"Пацієнтів: {loaded.Root?.Elements("patient").Count().ToString()}");

// Parse — завантаження з рядка
string xmlStr = "<root><item>A</item><item>B</item></root>";
XDocument parsed = XDocument.Parse(xmlStr);
Console.WriteLine($"Parse: {parsed.Root?.Elements().Count().ToString()} елементів");

File.Delete(path);
```

## Навігація по документу

```csharp run
using System;
using System.Linq;
using System.Xml.Linq;

XDocument doc = XDocument.Parse("""
<clinic>
    <patient id="PT-1001" ward="Терапія">
        <name>Петренко Іван Олексійович</name>
        <diagnosis code="J06.9">ГРВІ</diagnosis>
        <diagnosis code="I10">Гіпертонія</diagnosis>
    </patient>
    <patient id="PT-1002" ward="Кардіологія">
        <name>Бойко Оксана Петрівна</name>
        <diagnosis code="I21.0">Інфаркт міокарда</diagnosis>
    </patient>
    <patient id="PT-1003" ward="Терапія">
        <name>Мороз Василь Іванович</name>
        <diagnosis code="E11.9">Діабет 2 типу</diagnosis>
    </patient>
</clinic>
""");

XElement root = doc.Root!;

// Element(name) — перший прямий дочірній елемент з такою назвою
XElement? first = root.Element("patient");
Console.WriteLine($"Перший: {first?.Attribute("id")?.Value}");

// Elements(name) — всі прямі дочірні з такою назвою
Console.WriteLine($"\nВсі пацієнти ({root.Elements("patient").Count().ToString()}):");
foreach (XElement p in root.Elements("patient"))
{
    string id   = p.Attribute("id")?.Value ?? "";
    string ward = p.Attribute("ward")?.Value ?? "";
    string name = p.Element("name")?.Value ?? "";
    Console.WriteLine($"  [{id}] {name} — {ward}");
}

// Descendants(name) — всі нащадки з назвою на будь-якій глибині
Console.WriteLine($"\nВсі діагнози ({root.Descendants("diagnosis").Count().ToString()}):");
foreach (XElement diag in root.Descendants("diagnosis"))
{
    string code = diag.Attribute("code")?.Value ?? "";
    Console.WriteLine($"  [{code}] {diag.Value}");
}

// Ancestors — навігація вгору
XElement? oneDiag = root.Descendants("diagnosis").FirstOrDefault();
Console.WriteLine($"\nБатьківський пацієнт діагнозу: {oneDiag?.Parent?.Element("name")?.Value}");
```

| Метод | Що повертає |
|---|---|
| `Element("name")` | Перший прямий дочірній XElement з такою назвою |
| `Elements("name")` | Всі прямі дочірні XElement з такою назвою |
| `Elements()` | Всі прямі дочірні XElement |
| `Descendants("name")` | Всі нащадки з назвою (будь-яка глибина) |
| `Descendants()` | Всі нащадки |
| `Ancestors("name")` | Всі батьківські вузли з назвою (вгору) |
| `Attribute("name")` | XAttribute або null |
| `Attributes()` | Всі атрибути |

## LINQ-запити до XML

Найсильніша сторона `XDocument` — нативна інтеграція з LINQ. Будь-який метод, що повертає `IEnumerable<XElement>`, можна фільтрувати, трансформувати, групувати через `Where`, `Select`, `GroupBy`, `OrderBy`:

```csharp run
using System;
using System.Collections.Generic;
using System.Linq;
using System.Xml.Linq;

XDocument doc = XDocument.Parse("""
<clinic date="2024-03-15">
    <patient id="PT-1001" ward="Терапія">
        <name>Петренко І.О.</name>
        <age>45</age>
        <diagnosis code="J06.9" severity="mild">ГРВІ</diagnosis>
    </patient>
    <patient id="PT-1002" ward="Кардіологія">
        <name>Бойко О.П.</name>
        <age>62</age>
        <diagnosis code="I21.0" severity="critical">Інфаркт міокарда</diagnosis>
    </patient>
    <patient id="PT-1003" ward="Терапія">
        <name>Мороз В.І.</name>
        <age>38</age>
        <diagnosis code="E11.9" severity="moderate">Діабет 2 типу</diagnosis>
    </patient>
    <patient id="PT-1004" ward="Кардіологія">
        <name>Руденко С.В.</name>
        <age>55</age>
        <diagnosis code="I10" severity="moderate">Гіпертонія</diagnosis>
    </patient>
</clinic>
""");

// 1. Фільтрація: пацієнти з відділення Кардіологія
var cardio = doc.Root!
    .Elements("patient")
    .Where(p => p.Attribute("ward")?.Value == "Кардіологія")
    .Select(p => p.Element("name")?.Value)
    .ToList();
Console.WriteLine($"Кардіологія ({cardio.Count.ToString()}): {string.Join(", ", cardio)}");

// 2. Сортування за віком
var byAge = doc.Root
    .Elements("patient")
    .OrderBy(p => int.Parse(p.Element("age")?.Value ?? "0"))
    .Select(p => $"{p.Element("name")?.Value} ({p.Element("age")?.Value} р.)");
Console.WriteLine($"\nЗа віком: {string.Join(" | ", byAge)}");

// 3. Критичні пацієнти
var critical = doc.Root
    .Descendants("diagnosis")
    .Where(d => d.Attribute("severity")?.Value == "critical")
    .Select(d => new {
        Patient = d.Parent?.Element("name")?.Value,
        Diag    = d.Value,
        Code    = d.Attribute("code")?.Value
    });
Console.WriteLine("\nКритичні стани:");
foreach (var c in critical)
    Console.WriteLine($"  [{c.Code}] {c.Patient}: {c.Diag}");

// 4. Групування за відділенням
var byWard = doc.Root
    .Elements("patient")
    .GroupBy(p => p.Attribute("ward")?.Value)
    .Select(g => new { Ward = g.Key, Count = g.Count(), AvgAge = g.Average(p => int.Parse(p.Element("age")?.Value ?? "0")) });
Console.WriteLine("\nПо відділеннях:");
foreach (var w in byWard)
    Console.WriteLine($"  {w.Ward}: {w.Count.ToString()} пацієнтів, сер. вік {w.AvgAge.ToString("F0")} р.");
```

## Зміна документа

```csharp run
using System;
using System.Linq;
using System.Xml.Linq;

XDocument doc = XDocument.Parse("""
<patients>
    <patient id="PT-1001" status="active">
        <name>Петренко І.О.</name>
        <ward>Терапія</ward>
    </patient>
</patients>
""");

XElement root = doc.Root!;

// 1. Зміна значення атрибута
XElement? p1 = root.Elements("patient").FirstOrDefault(p => p.Attribute("id")?.Value == "PT-1001");
p1?.SetAttributeValue("status", "discharged");

// 2. Зміна тексту елемента
p1?.Element("ward")?.SetValue("Виписаний");

// 3. Додавання нового атрибута
p1?.SetAttributeValue("dischargedAt", DateTime.Now.ToString("yyyy-MM-dd"));

// 4. Додавання нового дочірнього елемента
p1?.Add(new XElement("note", "Виписаний за покращення стану"));

// 5. Видалення елемента
p1?.Element("ward")?.Remove();

// 6. Додавання нового пацієнта
root.Add(new XElement("patient",
    new XAttribute("id", "PT-1002"),
    new XAttribute("status", "active"),
    new XElement("name", "Бойко О.П."),
    new XElement("ward", "Кардіологія")
));

Console.WriteLine("Після змін:");
Console.WriteLine(doc.ToString());
```

`SetAttributeValue` — зручний метод: якщо атрибут існує — оновлює значення, не існує — додає. При значенні `null` — видаляє атрибут. `SetValue` — аналогічно для текстового вмісту елемента.

## Генерація XML з колекцій C#

Особливо зручно використовувати конструктор `XElement` з `IEnumerable<XElement>` — можна передавати LINQ-вираз як аргумент:

```csharp run
using System;
using System.Collections.Generic;
using System.Linq;
using System.Xml.Linq;

var results = new List<LabResult>
{
    new(1001, "Петренко І.О.", "Гемоглобін",  135.0, "г/л",     "норма"),
    new(1001, "Петренко І.О.", "Глюкоза",     5.1,   "ммоль/л", "норма"),
    new(1002, "Бойко О.П.",    "Глюкоза",     8.7,   "ммоль/л", "вище норми"),
    new(1002, "Бойко О.П.",    "Холестерин",  5.8,   "ммоль/л", "вище норми"),
    new(1003, "Мороз В.І.",    "Гемоглобін",  98.0,  "г/л",     "нижче норми"),
};

// Генерація XML з групуванням по пацієнту
XDocument report = new XDocument(
    new XDeclaration("1.0", "utf-8", null),
    new XElement("labReport",
        new XAttribute("generatedAt", DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss")),
        new XAttribute("totalResults", results.Count.ToString()),

        // LINQ прямо у конструкторі XElement
        from g in results.GroupBy(r => r.PatientId)
        select new XElement("patient",
            new XAttribute("id",   g.Key.ToString()),
            new XAttribute("name", g.First().Name),
            new XAttribute("resultsCount", g.Count().ToString()),
            from r in g
            select new XElement("result",
                new XAttribute("status", r.Status),
                new XElement("test",  r.Test),
                new XElement("value", new XAttribute("unit", r.Unit), r.Value.ToString("F2"))
            )
        )
    )
);

Console.WriteLine(report.ToString());

// Підрахунок відхилень
int abnormal = report.Descendants("result")
    .Count(r => r.Attribute("status")?.Value != "норма");
Console.WriteLine($"\nВідхилень від норми: {abnormal.ToString()} з {results.Count.ToString()}");

record LabResult(int PatientId, string Name, string Test, double Value, string Unit, string Status);
```

![LINQ to XML — схема запитів через Descendants та Elements](_assets/19-03/linq-to-xml-queries.png)
