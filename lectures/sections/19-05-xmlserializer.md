---
chapter: 19
chapterTitle: "Розділ 19. Серіалізація та десеріалізація. JSON та XML"
section: 5
number: "19.5"
title: "XmlSerializer — атрибутна серіалізація"
source: ""
---

## 19.5. XmlSerializer — атрибутна серіалізація

`XmlSerializer` із простору імен `System.Xml.Serialization` перетворює .NET-об'єкти у XML і назад за допомогою **атрибутів-анотацій** прямо на класах та властивостях. Це класичний підхід «contract-first»: ви описуєте структуру XML декораторами, а серіалізатор будує і читає документ автоматично.

На відміну від `JsonSerializer`, `XmlSerializer` потребує **публічного конструктора без параметрів** і **публічних властивостей або полів** — це жорстка вимога, пов'язана із генерацією коду серіалізатора під час першого виклику.

![XmlSerializer — атрибути та схема потоку](_assets/19-05/xmlserializer-attributes.png)

## Базова серіалізація та десеріалізація

```csharp run
using System;
using System.IO;
using System.Xml.Serialization;

public class Patient
{
    public int    Id       { get; set; }
    public string Name     { get; set; } = "";
    public string Ward     { get; set; } = "";
    public int    Age      { get; set; }
}

// Серіалізація
Patient patient = new Patient { Id = 1001, Name = "Петренко Іван", Ward = "Терапія", Age = 45 };

XmlSerializer serializer = new XmlSerializer(typeof(Patient));

// У рядок через StringWriter
using StringWriter sw = new StringWriter();
serializer.Serialize(sw, patient);
string xml = sw.ToString();
Console.WriteLine(xml);

// Десеріалізація
using StringReader sr = new StringReader(xml);
Patient? loaded = (Patient?)serializer.Deserialize(sr);
Console.WriteLine($"\nЗавантажено: {loaded?.Name}, відділення: {loaded?.Ward}");
```

За замовчуванням ім'я кореневого елемента збігається з ім'ям класу, а кожна властивість стає дочірнім елементом. Атрибути-анотації дозволяють повністю змінити цю поведінку.

## Атрибути XmlSerializer

### [XmlRoot] — кореневий елемент

```csharp run
using System;
using System.IO;
using System.Xml.Serialization;

[XmlRoot("patient", Namespace = "http://clinic.ua/2024")]
public class PatientRecord
{
    // Властивість → XML-атрибут (не елемент)
    [XmlAttribute("id")]
    public string PatientId { get; set; } = "";

    // Властивість → елемент з іншою назвою
    [XmlElement("fullName")]
    public string Name { get; set; } = "";

    // Властивість → елемент у просторі імен
    [XmlElement("ward", Namespace = "http://clinic.ua/2024")]
    public string Ward { get; set; } = "";

    // Властивість повністю ігнорується
    [XmlIgnore]
    public DateTime LastAccessed { get; set; }

    // Числова властивість без зміни імені
    public int Age { get; set; }
}

PatientRecord rec = new PatientRecord
{
    PatientId    = "PT-1001",
    Name         = "Петренко Іван Олексійович",
    Ward         = "Терапія",
    Age          = 45,
    LastAccessed = DateTime.Now   // буде проігноровано
};

XmlSerializer xs = new XmlSerializer(typeof(PatientRecord));
using StringWriter sw = new StringWriter();
xs.Serialize(sw, rec);
Console.WriteLine(sw.ToString());
```

| Атрибут | Що робить |
|---|---|
| `[XmlRoot("tag")]` | Перейменовує кореневий елемент |
| `[XmlElement("tag")]` | Серіалізує властивість як XML-елемент з даним ім'ям |
| `[XmlAttribute("attr")]` | Серіалізує властивість як XML-атрибут |
| `[XmlIgnore]` | Виключає властивість з серіалізації |
| `[XmlText]` | Серіалізує властивість як текстовий вміст елемента |
| `[XmlArray("list")]` | Перейменовує обгортковий елемент колекції |
| `[XmlArrayItem("item")]` | Перейменовує елементи всередині колекції |

### [XmlArray] та [XmlArrayItem] — серіалізація колекцій

```csharp run
using System;
using System.Collections.Generic;
using System.IO;
using System.Xml.Serialization;

public class DiagnosisEntry
{
    [XmlAttribute("code")]
    public string Code { get; set; } = "";

    [XmlAttribute("system")]
    public string System { get; set; } = "ICD-10";

    [XmlText]
    public string Description { get; set; } = "";
}

public class VitalSign
{
    [XmlAttribute("type")]
    public string Type  { get; set; } = "";

    [XmlAttribute("unit")]
    public string Unit  { get; set; } = "";

    [XmlText]
    public string Value { get; set; } = "";
}

[XmlRoot("patientRecord")]
public class FullPatientRecord
{
    [XmlAttribute("id")]
    public string Id { get; set; } = "";

    [XmlElement("name")]
    public string Name { get; set; } = "";

    // List → <diagnoses><diagnosis ...>
    [XmlArray("diagnoses")]
    [XmlArrayItem("diagnosis")]
    public List<DiagnosisEntry> Diagnoses { get; set; } = new();

    // List → <vitals><sign ...>
    [XmlArray("vitals")]
    [XmlArrayItem("sign")]
    public List<VitalSign> Vitals { get; set; } = new();
}

FullPatientRecord record = new FullPatientRecord
{
    Id   = "PT-1001",
    Name = "Петренко Іван Олексійович",
    Diagnoses = new List<DiagnosisEntry>
    {
        new() { Code = "J06.9", Description = "ГРВІ" },
        new() { Code = "I10",   Description = "Гіпертонія" }
    },
    Vitals = new List<VitalSign>
    {
        new() { Type = "temperature", Unit = "C",   Value = "37.2" },
        new() { Type = "pulse",       Unit = "bpm", Value = "82"   }
    }
};

XmlSerializer xs = new XmlSerializer(typeof(FullPatientRecord));
using StringWriter sw = new StringWriter();
xs.Serialize(sw, record);
Console.WriteLine(sw.ToString());
```

## Серіалізація з простором імен

```csharp run
using System;
using System.IO;
using System.Xml;
using System.Xml.Serialization;

[XmlRoot("clinic", Namespace = "http://clinic.ua/schema/2024")]
public class ClinicDocument
{
    [XmlElement("name")]
    public string ClinicName { get; set; } = "";

    [XmlElement("registrationDate")]
    public string RegDate { get; set; } = "";
}

ClinicDocument doc = new ClinicDocument
{
    ClinicName = "Міська клінічна лікарня №5",
    RegDate    = "2024-01-01"
};

XmlSerializer xs   = new XmlSerializer(typeof(ClinicDocument));
XmlSerializerNamespaces ns = new XmlSerializerNamespaces();
ns.Add("clinic", "http://clinic.ua/schema/2024");
ns.Add("",       "");   // прибирає зайвий xsi/xsd

using StringWriter sw = new StringWriter();
xs.Serialize(sw, doc, ns);
Console.WriteLine(sw.ToString());
```

`XmlSerializerNamespaces` дозволяє додавати або прибирати простори імен з вихідного XML. Якщо передати `ns.Add("", "")` — серіалізатор не додає зайвих `xmlns:xsi` та `xmlns:xsd`.

## Десеріалізація з файлу та валідація

```csharp run
using System;
using System.IO;
using System.Xml.Serialization;

[XmlRoot("examination")]
public class ExamRecord
{
    [XmlAttribute("patientId")]
    public string PatientId { get; set; } = "";

    [XmlElement("examDate")]
    public string ExamDate { get; set; } = "";

    [XmlElement("conclusion")]
    public string Conclusion { get; set; } = "";

    [XmlArray("tests")]
    [XmlArrayItem("test")]
    public List<TestResult> Tests { get; set; } = new();
}

public class TestResult
{
    [XmlAttribute("name")]
    public string Name { get; set; } = "";

    [XmlAttribute("status")]
    public string Status { get; set; } = "";

    [XmlText]
    public string Value { get; set; } = "";
}

string xmlData = """
<?xml version="1.0" encoding="utf-16"?>
<examination patientId="PT-1002">
  <examDate>2024-03-15</examDate>
  <conclusion>Стан задовільний</conclusion>
  <tests>
    <test name="Гемоглобін" status="норма">135</test>
    <test name="Глюкоза" status="вище норми">8.7</test>
    <test name="Холестерин" status="норма">4.9</test>
  </tests>
</examination>
""";

XmlSerializer xs = new XmlSerializer(typeof(ExamRecord));

// Десеріалізація
using StringReader sr = new StringReader(xmlData);
ExamRecord? exam = (ExamRecord?)xs.Deserialize(sr);

if (exam != null)
{
    Console.WriteLine($"Пацієнт: {exam.PatientId}");
    Console.WriteLine($"Дата: {exam.ExamDate}");
    Console.WriteLine($"Висновок: {exam.Conclusion}");
    Console.WriteLine($"Тестів: {exam.Tests.Count.ToString()}");
    foreach (TestResult t in exam.Tests)
        Console.WriteLine($"  {t.Name}: {t.Value} [{t.Status}]");
}
```

## Наслідування та [XmlInclude]

```csharp run
using System;
using System.IO;
using System.Xml.Serialization;

// Базовий клас — треба оголосити всі похідні типи
[XmlInclude(typeof(BloodTest))]
[XmlInclude(typeof(EcgRecord))]
public abstract class MedicalTest
{
    [XmlAttribute("id")]
    public string TestId { get; set; } = "";

    [XmlElement("date")]
    public string Date { get; set; } = "";
}

public class BloodTest : MedicalTest
{
    [XmlElement("hemoglobin")]
    public double Hemoglobin { get; set; }

    [XmlElement("glucose")]
    public double Glucose { get; set; }
}

public class EcgRecord : MedicalTest
{
    [XmlElement("heartRate")]
    public int HeartRate { get; set; }

    [XmlElement("rhythm")]
    public string Rhythm { get; set; } = "";
}

[XmlRoot("lab")]
public class LabContainer
{
    // XmlSerializer серіалізує через [XmlInclude] типи з xsi:type
    [XmlElement("test")]
    public List<MedicalTest> Tests { get; set; } = new();
}

LabContainer lab = new LabContainer
{
    Tests = new List<MedicalTest>
    {
        new BloodTest { TestId = "BT-001", Date = "2024-03-15", Hemoglobin = 135.0, Glucose = 5.1 },
        new EcgRecord { TestId = "EC-001", Date = "2024-03-15", HeartRate = 72, Rhythm = "Синусовий" }
    }
};

XmlSerializer xs = new XmlSerializer(typeof(LabContainer));
using StringWriter sw = new StringWriter();
xs.Serialize(sw, lab);
string xml = sw.ToString();
Console.WriteLine(xml);

// Roundtrip — читаємо назад
using StringReader sr = new StringReader(xml);
LabContainer? loaded = (LabContainer?)xs.Deserialize(sr);
Console.WriteLine($"\nЗавантажено {loaded?.Tests.Count.ToString()} тестів:");
foreach (MedicalTest t in loaded?.Tests ?? new())
    Console.WriteLine($"  [{t.GetType().Name}] {t.TestId} — {t.Date}");
```

`[XmlInclude]` обов'язковий, якщо ви серіалізуєте колекцію базового типу і очікуєте отримати правильні похідні типи після десеріалізації. Серіалізатор додає `xsi:type="BloodTest"` у XML, і при зворотному читанні відновлює правильний тип.

## Практичний сценарій: збереження протоколу обходу

```csharp run
using System;
using System.Collections.Generic;
using System.IO;
using System.Xml.Serialization;

[XmlRoot("wardRound")]
public class WardRoundProtocol
{
    [XmlAttribute("date")]
    public string Date { get; set; } = "";

    [XmlAttribute("physician")]
    public string Physician { get; set; } = "";

    [XmlArray("patients")]
    [XmlArrayItem("patient")]
    public List<WardPatient> Patients { get; set; } = new();
}

public class WardPatient
{
    [XmlAttribute("id")]
    public string Id { get; set; } = "";

    [XmlElement("name")]
    public string Name { get; set; } = "";

    [XmlElement("ward")]
    public string Ward { get; set; } = "";

    [XmlElement("notes")]
    public string Notes { get; set; } = "";

    [XmlElement("status")]
    public string Status { get; set; } = "";

    // Порожній конструктор обов'язковий для XmlSerializer
    public WardPatient() {}

    public WardPatient(string id, string name, string ward, string notes, string status)
    {
        Id = id; Name = name; Ward = ward; Notes = notes; Status = status;
    }
}

WardRoundProtocol protocol = new WardRoundProtocol
{
    Date      = DateTime.Now.ToString("yyyy-MM-dd"),
    Physician = "Коваленко О.В.",
    Patients  = new List<WardPatient>
    {
        new("PT-1001", "Петренко І.О.", "Терапія",     "Стан покращився, t=36.8", "задовільний"),
        new("PT-1002", "Бойко О.П.",    "Кардіологія", "ЕКГ в нормі, АТ 125/80",  "стабільний"),
        new("PT-1003", "Мороз В.І.",    "Терапія",     "Скарги на слабкість",      "спостереження"),
    }
};

XmlSerializer xs = new XmlSerializer(typeof(WardRoundProtocol));
string path = Path.Combine(Path.GetTempPath(), "ward_round.xml");

// Серіалізація у файл
using (FileStream fs = File.Create(path))
    xs.Serialize(fs, protocol);

Console.WriteLine($"Збережено ({new FileInfo(path).Length.ToString()} байт):");
Console.WriteLine(File.ReadAllText(path));

// Десеріалізація з файлу
using FileStream fsr = File.OpenRead(path);
WardRoundProtocol? loaded = (WardRoundProtocol?)xs.Deserialize(fsr);

Console.WriteLine($"\nПротокол від {loaded?.Date}, лікар: {loaded?.Physician}");
Console.WriteLine($"Пацієнтів: {loaded?.Patients.Count.ToString()}");
foreach (WardPatient p in loaded?.Patients ?? new())
    Console.WriteLine($"  [{p.Id}] {p.Name} — {p.Status}");

File.Delete(path);
```

![XmlSerializer — порівняння з JsonSerializer за підходом](_assets/19-05/xmlserializer-vs-json.png)
