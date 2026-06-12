---
chapter: 19
chapterTitle: "Розділ 19. Серіалізація та десеріалізація. JSON та XML"
section: 4
number: "19.4"
title: "XmlReader та XmlWriter. Потоковий XML"
source: ""
---

## 19.4. XmlReader та XmlWriter. Потоковий XML

`XmlDocument` і `XDocument` зручні, але мають спільний недолік: вони завантажують **весь XML-документ у пам'ять** як дерево об'єктів. Для файлу в 10 MB це прийнятно. Для XML-експорту з 500 000 лабораторних результатів, XML-архіву DICOM-даних або потоку HL7-повідомлень — DOM-підхід призведе до `OutOfMemoryException` або неприйнятного часу завантаження.

`XmlReader` і `XmlWriter` реалізують **потоковий (streaming)** підхід: читання і запис відбуваються **послідовно, вузол за вузлом**, без побудови повного дерева в пам'яті. Використання пам'яті константне незалежно від розміру файлу — тільки один поточний вузол.

![XmlReader — forward-only потокове читання XML](_assets/19-04/xmlreader-flow.png)

## XmlReader — forward-only читання

`XmlReader` рухається по XML **в одному напрямку** — вперед. Не можна повернутися до попереднього вузла (на відміну від DOM). Кожен виклик `Read()` просуває позицію на наступний вузол і встановлює `NodeType`.

### Базове читання

```csharp run
using System;
using System.IO;
using System.Xml;

string xml = """
<?xml version="1.0" encoding="utf-8"?>
<clinic>
    <patient id="PT-1001" ward="Терапія">
        <name>Петренко Іван Олексійович</name>
        <age>45</age>
        <diagnosis code="J06.9">ГРВІ</diagnosis>
    </patient>
    <patient id="PT-1002" ward="Кардіологія">
        <name>Бойко Оксана Петрівна</name>
        <age>62</age>
        <diagnosis code="I21.0">Інфаркт міокарда</diagnosis>
    </patient>
</clinic>
""";

var settings = new XmlReaderSettings
{
    IgnoreWhitespace = true,   // пропускати текстові вузли з пробілами
    IgnoreComments   = true,   // пропускати коментарі
};

using XmlReader reader = XmlReader.Create(new StringReader(xml), settings);

Console.WriteLine("Всі вузли (тип | назва | значення):");
while (reader.Read())
{
    string indent = new string(' ', reader.Depth * 2);
    switch (reader.NodeType)
    {
        case XmlNodeType.XmlDeclaration:
            Console.WriteLine($"{indent}[Decl] <?xml {reader.Value}?>");
            break;
        case XmlNodeType.Element:
            Console.Write($"{indent}[Elem] <{reader.Name}");
            if (reader.HasAttributes)
            {
                // Зберігаємо атрибути поточного елемента
                for (int i = 0; i < reader.AttributeCount; i++)
                {
                    reader.MoveToAttribute(i);
                    Console.Write($" {reader.Name}=\"{reader.Value}\"");
                }
                reader.MoveToElement(); // повернутись до елемента після атрибутів
            }
            Console.WriteLine(reader.IsEmptyElement ? "/>" : ">");
            break;
        case XmlNodeType.Text:
            Console.WriteLine($"{indent}[Text] \"{reader.Value}\"");
            break;
        case XmlNodeType.EndElement:
            Console.WriteLine($"{indent}[End]  </{reader.Name}>");
            break;
    }
}
```

`reader.Depth` показує рівень вкладеності поточного вузла — зручно для відступів. `reader.IsEmptyElement` — `true` для `<tag/>` без вмісту.

### ReadToFollowing, ReadElementContentAsString та GetAttribute

```csharp run
using System;
using System.IO;
using System.Xml;
using System.Collections.Generic;

string xml = """
<?xml version="1.0"?>
<clinic>
    <patient id="PT-1001" ward="Терапія">
        <name>Петренко Іван Олексійович</name>
        <age>45</age>
        <diagnosis code="J06.9">ГРВІ</diagnosis>
        <diagnosis code="I10">Гіпертонія</diagnosis>
    </patient>
    <patient id="PT-1002" ward="Кардіологія">
        <name>Бойко Оксана Петрівна</name>
        <age>62</age>
        <diagnosis code="I21.0">Інфаркт міокарда</diagnosis>
    </patient>
</clinic>
""";

var settings = new XmlReaderSettings { IgnoreWhitespace = true };
using XmlReader reader = XmlReader.Create(new StringReader(xml), settings);

int patientCount = 0;
var allDiagnoses = new List<string>();

// ReadToFollowing — переходить до наступного елемента з такою назвою
while (reader.ReadToFollowing("patient"))
{
    patientCount++;
    // GetAttribute — читання атрибуту поточного елемента
    string id   = reader.GetAttribute("id") ?? "";
    string ward = reader.GetAttribute("ward") ?? "";

    // ReadToDescendant — переходить до першого дочірнього з такою назвою
    reader.ReadToDescendant("name");
    // ReadElementContentAsString — читає текст і просуває позицію за EndElement
    string name = reader.ReadElementContentAsString();

    reader.ReadToNextSibling("age");
    int age = reader.ReadElementContentAsInt();

    Console.WriteLine($"  [{id}] {name}, {age.ToString()} р. ({ward})");

    // Читаємо всі diagnosis для цього пацієнта
    while (reader.ReadToNextSibling("diagnosis"))
    {
        string code = reader.GetAttribute("code") ?? "";
        string text = reader.ReadElementContentAsString();
        allDiagnoses.Add($"[{code}] {text}");
    }
}

Console.WriteLine($"\nПацієнтів: {patientCount.ToString()}");
Console.WriteLine($"Всі діагнози ({allDiagnoses.Count.ToString()}):");
foreach (string diag in allDiagnoses)
    Console.WriteLine($"  {diag}");
```

| Метод | Опис |
|---|---|
| `Read()` | Наступний вузол; `false` = кінець |
| `ReadToFollowing("name")` | Перемотати до наступного елемента з назвою |
| `ReadToDescendant("name")` | Перемотати до першого дочірнього |
| `ReadToNextSibling("name")` | Перемотати до сусіднього на тому ж рівні |
| `ReadElementContentAsString()` | Прочитати текст і перейти за `</tag>` |
| `ReadElementContentAsInt()` | Те саме для `int` |
| `ReadElementContentAsDouble()` | Те саме для `double` |
| `GetAttribute("name")` | Атрибут поточного Element-вузла |
| `Skip()` | Пропустити поточний елемент з усіма дочірніми |

### Обробка великого XML-файлу потоково

```csharp run
using System;
using System.IO;
using System.Xml;
using System.Collections.Generic;

// Генеруємо великий тестовий XML
string xmlPath = Path.Combine(Path.GetTempPath(), "large_clinic.xml");
using (XmlWriter gen = XmlWriter.Create(xmlPath, new XmlWriterSettings { Indent = true }))
{
    gen.WriteStartDocument();
    gen.WriteStartElement("clinicExport");
    gen.WriteAttributeString("date", DateTime.Now.ToString("yyyy-MM-dd"));

    string[] diagnoses = { "J06.9", "I10", "E11.9", "K29.5", "M54.5" };
    string[] wards     = { "Терапія", "Кардіологія", "Неврологія" };

    for (int i = 1; i <= 500; i++)
    {
        gen.WriteStartElement("patient");
        gen.WriteAttributeString("id",   $"PT-{i.ToString("D4")}");
        gen.WriteAttributeString("ward", wards[i % wards.Length]);
        gen.WriteElementString("name",   $"Пацієнт #{i.ToString()}");
        gen.WriteElementString("age",    (20 + i % 60).ToString());
        gen.WriteElementString("diagnosis", diagnoses[i % diagnoses.Length]);
        gen.WriteEndElement();
    }

    gen.WriteEndElement();
    gen.WriteEndDocument();
}

var fileInfo = new FileInfo(xmlPath);
Console.WriteLine($"XML: {fileInfo.Length.ToString()} байт, ~500 пацієнтів");

// Потокова обробка — пам'яті потрібно лише для одного пацієнта
int total = 0, cardioCount = 0;
var settings = new XmlReaderSettings { IgnoreWhitespace = true };

using (XmlReader reader = XmlReader.Create(xmlPath, settings))
{
    while (reader.ReadToFollowing("patient"))
    {
        total++;
        string ward = reader.GetAttribute("ward") ?? "";
        if (ward == "Кардіологія") cardioCount++;

        // Skip() — пропускаємо вміст пацієнта без читання
        reader.Skip();
    }
}

Console.WriteLine($"Оброблено: {total.ToString()} пацієнтів");
Console.WriteLine($"Кардіологія: {cardioCount.ToString()}");
Console.WriteLine("Витрачено пам'яті: ~константна (лише один вузол одночасно)");

File.Delete(xmlPath);
```

## XmlWriter — потоковий запис XML

`XmlWriter` записує XML **послідовно** — елемент за елементом. Він гарантує синтаксичну коректність: відкритий тег без `WriteEndElement` призведе до помилки при `Dispose`.

### Базовий запис

```csharp run
using System;
using System.IO;
using System.Text;
using System.Xml;

var settings = new XmlWriterSettings
{
    Indent            = true,          // відступи
    IndentChars       = "    ",        // 4 пробіли
    Encoding          = Encoding.UTF8,
    OmitXmlDeclaration = false,        // включати <?xml ...?>
    NewLineChars      = "\n",          // Unix-стиль переносів
};

using MemoryStream ms = new MemoryStream();
using (XmlWriter writer = XmlWriter.Create(ms, settings))
{
    writer.WriteStartDocument();

    // Коментар
    writer.WriteComment("Медична звітність 2024");

    writer.WriteStartElement("medReport");
    writer.WriteAttributeString("version",     "1.0");
    writer.WriteAttributeString("generatedAt", DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss"));

    // Пацієнт 1
    writer.WriteStartElement("patient");
    writer.WriteAttributeString("id",     "PT-1001");
    writer.WriteAttributeString("status", "active");

    writer.WriteElementString("name",      "Петренко Іван Олексійович");
    writer.WriteElementString("birthDate", "1978-03-15");
    writer.WriteElementString("ward",      "Терапія");

    // Вкладений елемент з атрибутом і текстом
    writer.WriteStartElement("diagnosis");
    writer.WriteAttributeString("code",   "J06.9");
    writer.WriteAttributeString("system", "ICD-10");
    writer.WriteString("ГРВІ");          // текстовий вміст
    writer.WriteEndElement();            // </diagnosis>

    writer.WriteEndElement(); // </patient>

    // WriteRaw — записує XML-рядок без escaping
    writer.WriteRaw("\n    <!-- кінець звіту -->");

    writer.WriteEndElement(); // </medReport>
    writer.WriteEndDocument();
}

string result = Encoding.UTF8.GetString(ms.ToArray());
Console.WriteLine(result);
```

### Серіалізація колекції у XML через XmlWriter

```csharp run
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Xml;

var patients = new List<Patient>
{
    new(1001, "Петренко І.О.", "Терапія",     new[]{"J06.9","I10"},    5.1, 72),
    new(1002, "Бойко О.П.",   "Кардіологія", new[]{"I21.0"},          8.7, 145),
    new(1003, "Мороз В.І.",   "Неврологія",  new[]{"G43.9","G40.9"},  4.8, 68),
};

string path = Path.Combine(Path.GetTempPath(), "patients_export.xml");

var settings = new XmlWriterSettings { Indent = true, Encoding = Encoding.UTF8 };
using (XmlWriter w = XmlWriter.Create(path, settings))
{
    w.WriteStartDocument();
    w.WriteStartElement("clinicExport");
    w.WriteAttributeString("exportedAt", DateTime.Now.ToString("O"));
    w.WriteAttributeString("count",      patients.Count.ToString());

    foreach (Patient p in patients)
    {
        w.WriteStartElement("patient");
        w.WriteAttributeString("id",   p.Id.ToString());
        w.WriteAttributeString("ward", p.Ward);

        w.WriteElementString("name", p.Name);

        // Числові значення
        w.WriteStartElement("vitals");
        w.WriteElementString("glucose", p.Glucose.ToString("F1"));
        w.WriteElementString("pulse",   p.Pulse.ToString());
        w.WriteEndElement(); // </vitals>

        // Масив діагнозів
        w.WriteStartElement("diagnoses");
        foreach (string code in p.Diagnoses)
            w.WriteElementString("code", code);
        w.WriteEndElement(); // </diagnoses>

        // Умовний елемент — тільки якщо критичний стан
        bool critical = p.Glucose > 7.0 || p.Pulse > 120;
        if (critical)
        {
            w.WriteStartElement("alert");
            w.WriteAttributeString("level", "high");
            w.WriteString(p.Glucose > 7.0 ? $"Глюкоза: {p.Glucose.ToString("F1")}" : $"Пульс: {p.Pulse.ToString()}");
            w.WriteEndElement();
        }

        w.WriteEndElement(); // </patient>
    }

    w.WriteEndElement(); // </clinicExport>
    w.WriteEndDocument();
}

Console.WriteLine(File.ReadAllText(path, Encoding.UTF8));
Console.WriteLine($"Файл: {new FileInfo(path).Length.ToString()} байт");
File.Delete(path);

record Patient(int Id, string Name, string Ward, string[] Diagnoses, double Glucose, int Pulse);
```

## XmlReader + XmlWriter: трансформація великих файлів

Найпотужніший патерн — читати через `XmlReader` і одночасно писати через `XmlWriter`. Це дозволяє трансформувати XML будь-якого розміру при константному використанні пам'яті:

```csharp run
using System;
using System.IO;
using System.Xml;

// Генеруємо вхідний файл
string inputPath  = Path.Combine(Path.GetTempPath(), "input_clinic.xml");
string outputPath = Path.Combine(Path.GetTempPath(), "output_critical.xml");

// Вхідний XML з пацієнтами
using (XmlWriter gen = XmlWriter.Create(inputPath, new XmlWriterSettings { Indent = true }))
{
    gen.WriteStartDocument();
    gen.WriteStartElement("patients");
    var data = new[] {
        ("PT-1001","Петренко І.О.", 5.1,  72,  "Терапія"),
        ("PT-1002","Бойко О.П.",    8.7,  145, "Кардіологія"),
        ("PT-1003","Мороз В.І.",    4.8,  68,  "Терапія"),
        ("PT-1004","Руденко С.В.", 12.4,  110, "Кардіологія"),
    };
    foreach (var (id,name,gluc,pulse,ward) in data)
    {
        gen.WriteStartElement("patient");
        gen.WriteAttributeString("id", id);
        gen.WriteAttributeString("ward", ward);
        gen.WriteElementString("name", name);
        gen.WriteElementString("glucose", gluc.ToString("F1"));
        gen.WriteElementString("pulse", pulse.ToString());
        gen.WriteEndElement();
    }
    gen.WriteEndElement();
    gen.WriteEndDocument();
}

// Трансформація: копіюємо лише критичних пацієнтів
int processed = 0, written = 0;
var rSettings = new XmlReaderSettings { IgnoreWhitespace = true };
var wSettings = new XmlWriterSettings { Indent = true };

using (XmlReader reader = XmlReader.Create(inputPath, rSettings))
using (XmlWriter writer = XmlWriter.Create(outputPath, wSettings))
{
    writer.WriteStartDocument();
    writer.WriteStartElement("criticalPatients");
    writer.WriteAttributeString("filter", "glucose>7 OR pulse>120");

    while (reader.ReadToFollowing("patient"))
    {
        processed++;
        string id   = reader.GetAttribute("id") ?? "";
        string ward = reader.GetAttribute("ward") ?? "";

        // Читаємо дані пацієнта у змінні
        reader.ReadToDescendant("name");
        string name   = reader.ReadElementContentAsString();
        double gluc   = reader.ReadElementContentAsDouble();
        int    pulse  = reader.ReadElementContentAsInt();

        bool critical = gluc > 7.0 || pulse > 120;
        if (!critical) continue;

        // Пишемо у вихідний файл
        written++;
        writer.WriteStartElement("patient");
        writer.WriteAttributeString("id",   id);
        writer.WriteAttributeString("ward", ward);
        writer.WriteElementString("name",   name);
        writer.WriteElementString("glucose", gluc.ToString("F1"));
        writer.WriteElementString("pulse",   pulse.ToString());

        string reason = gluc > 7.0
            ? $"глюкоза {gluc.ToString("F1")} ммоль/л"
            : $"пульс {pulse.ToString()} уд/хв";
        writer.WriteElementString("alertReason", reason);

        writer.WriteEndElement();
    }

    writer.WriteEndElement();
    writer.WriteEndDocument();
}

Console.WriteLine($"Оброблено: {processed.ToString()} пацієнтів");
Console.WriteLine($"Критичних: {written.ToString()}");
Console.WriteLine($"\nРезультат:");
Console.WriteLine(File.ReadAllText(outputPath));

File.Delete(inputPath);
File.Delete(outputPath);
```

![XmlWriter — послідовний запис елементів і атрибутів](_assets/19-04/xmlwriter-flow.png)
