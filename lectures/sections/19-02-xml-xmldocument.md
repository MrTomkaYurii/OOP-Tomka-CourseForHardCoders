---
chapter: 19
chapterTitle: "Розділ 19. Серіалізація та десеріалізація. JSON та XML"
section: 2
number: "19.2"
title: "XML-формат та XmlDocument. DOM-модель"
source: ""
---

## 19.2. XML-формат та XmlDocument. DOM-модель

XML (eXtensible Markup Language) — мова розмітки, що описує структуровані дані у вигляді ієрархії тегів. На відміну від JSON, XML підтримує атрибути як першокласний синтаксис, простори імен (`xmlns`) та валідацію через схеми (XSD). У медичній галузі XML — стандартний формат: **HL7 v2/v3** і **FHIR** для обміну клінічними даними, **DICOM** заголовки, **CDA** (Clinical Document Architecture). Конфігурація .NET-застосунків (`.config`-файли), SOAP-сервіси, Office Open XML (.docx, .xlsx) — теж XML.

`System.Xml` — простір імен, що надає повний набір інструментів для роботи з XML. Клас `XmlDocument` реалізує **DOM** (Document Object Model) — модель, де весь XML-документ завантажується у пам'ять як дерево вузлів (`XmlNode`). Кожен елемент, атрибут, текстовий вузол, коментар — окремий об'єкт у цьому дереві.

![Структура XML-документа та DOM-дерево](_assets/19-02/xml-dom-tree.png)

## Структура XML-документа

```csharp run
using System;

// Повна структура XML з усіма можливими вузлами:
string xmlExample = """
<?xml version="1.0" encoding="utf-8"?>
<!-- Медична картка пацієнта: CDA-подібний формат -->
<patientRecord xmlns:med="http://clinic.ua/medical/2024">
    <patient id="PT-1001" status="active">
        <name>Петренко Іван Олексійович</name>
        <birthDate>1978-03-15</birthDate>
        <ward>Терапія</ward>
    </patient>
    <diagnoses>
        <diagnosis code="J06.9" system="ICD-10">ГРВІ</diagnosis>
        <diagnosis code="I10"   system="ICD-10">Гіпертонічна хвороба</diagnosis>
    </diagnoses>
    <vitals recordedAt="2024-03-15T14:30:00">
        <temperature unit="C">37.2</temperature>
        <pulse unit="bpm">82</pulse>
        <bloodPressure>
            <systolic>135</systolic>
            <diastolic>85</diastolic>
        </bloodPressure>
    </vitals>
</patientRecord>
""";

// Ключові компоненти XML:
Console.WriteLine("Компоненти XML-документа:");
Console.WriteLine("  <?xml ...?>          — декларація (версія, кодування)");
Console.WriteLine("  <!-- ... -->         — коментар");
Console.WriteLine("  <patientRecord>      — кореневий елемент (root element)");
Console.WriteLine("  xmlns:med=\"...\"   — простір імен (namespace)");
Console.WriteLine("  id=\"PT-1001\"      — атрибут елемента");
Console.WriteLine("  <name>Петр...</name> — дочірній елемент з текстовим вмістом");
Console.WriteLine("  <diagnosis code=...> — елемент з атрибутами і текстом");
```

## XmlDocument — завантаження та навігація

```csharp run
using System;
using System.Xml;
using System.IO;

string xml = """
<?xml version="1.0" encoding="utf-8"?>
<patientRecord>
    <patient id="PT-1001" status="active">
        <name>Петренко Іван Олексійович</name>
        <birthDate>1978-03-15</birthDate>
        <ward>Терапія</ward>
    </patient>
    <diagnoses>
        <diagnosis code="J06.9">ГРВІ</diagnosis>
        <diagnosis code="I10">Гіпертонічна хвороба</diagnosis>
    </diagnoses>
    <vitals>
        <temperature unit="C">37.2</temperature>
        <pulse unit="bpm">82</pulse>
    </vitals>
</patientRecord>
""";

XmlDocument doc = new XmlDocument();

// Завантаження з рядка
doc.LoadXml(xml);

// Альтернатива — з файлу:
// doc.Load("patient.xml");
// або зі Stream:
// doc.Load(stream);

// DocumentElement — кореневий елемент
XmlElement root = doc.DocumentElement!;
Console.WriteLine($"Корінь: <{root.Name}>");
Console.WriteLine($"Дочірніх вузлів: {root.ChildNodes.Count.ToString()}");

// Доступ до дочірніх елементів
XmlNode? patientNode = root["patient"];  // перший <patient>
if (patientNode != null)
{
    // Читання атрибутів
    string id     = patientNode.Attributes?["id"]?.Value ?? "";
    string status = patientNode.Attributes?["status"]?.Value ?? "";
    Console.WriteLine($"\nПацієнт: id={id}, status={status}");

    // Читання текстового вмісту дочірніх елементів
    string name  = patientNode["name"]?.InnerText  ?? "";
    string bdate = patientNode["birthDate"]?.InnerText ?? "";
    string ward  = patientNode["ward"]?.InnerText  ?? "";
    Console.WriteLine($"  Ім'я: {name}");
    Console.WriteLine($"  Дата народження: {bdate}");
    Console.WriteLine($"  Відділення: {ward}");
}

// Перебір дочірніх вузлів колекції
XmlNode? diagsNode = root["diagnoses"];
if (diagsNode != null)
{
    Console.WriteLine($"\nДіагнози ({diagsNode.ChildNodes.Count.ToString()}):");
    foreach (XmlNode diag in diagsNode.ChildNodes)
    {
        string code = diag.Attributes?["code"]?.Value ?? "";
        string text = diag.InnerText;
        Console.WriteLine($"  [{code}] {text}");
    }
}
```

`XmlNode` — базовий клас для всіх вузлів DOM. `XmlElement` — конкретний тип для елементів (тегів). Властивість `InnerText` повертає весь текстовий вміст вузла (включно з вкладеними тегами), `InnerXml` — весь XML-вміст як рядок.

## SelectSingleNode та SelectNodes — XPath у XmlDocument

```csharp run
using System;
using System.Xml;

string xml = """
<?xml version="1.0" encoding="utf-8"?>
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
        <diagnosis code="E11.9">Цукровий діабет 2 типу</diagnosis>
    </patient>
</clinic>
""";

XmlDocument doc = new XmlDocument();
doc.LoadXml(xml);

// SelectSingleNode — перший вузол за XPath
XmlNode? first = doc.SelectSingleNode("/clinic/patient[1]/name");
Console.WriteLine($"Перший пацієнт: {first?.InnerText}");

// Пошук за значенням атрибуту
XmlNode? byId = doc.SelectSingleNode("/clinic/patient[@id='PT-1002']");
Console.WriteLine($"Пацієнт PT-1002: {byId?["name"]?.InnerText}");

// SelectNodes — всі вузли за XPath
XmlNodeList? therapyPatients = doc.SelectNodes("/clinic/patient[@ward='Терапія']");
Console.WriteLine($"\nПацієнти у Терапії ({therapyPatients?.Count.ToString()}):");
if (therapyPatients != null)
    foreach (XmlNode p in therapyPatients)
        Console.WriteLine($"  {p.Attributes?["id"]?.Value}: {p["name"]?.InnerText}");

// Пошук по всьому документу: // = будь-який рівень вкладеності
XmlNodeList? allDiags = doc.SelectNodes("//diagnosis[@code='I10' or @code='I21.0']");
Console.WriteLine($"\nКардіологічні діагнози ({allDiags?.Count.ToString()}):");
if (allDiags != null)
    foreach (XmlNode diag in allDiags)
        Console.WriteLine($"  [{diag.Attributes?["code"]?.Value}] {diag.InnerText}");
```

XPath-вирази у `SelectSingleNode`/`SelectNodes` — потужний засіб вибірки: `/root/child` (точний шлях), `//element` (будь-яка глибина), `[@attr='val']` (фільтр за атрибутом), `[position()]` (за позицією).

## Створення XML-документа програмно

```csharp run
using System;
using System.IO;
using System.Xml;

XmlDocument doc = new XmlDocument();

// XML-декларація
XmlDeclaration decl = doc.CreateXmlDeclaration("1.0", "utf-8", null);
doc.AppendChild(decl);

// Кореневий елемент
XmlElement root = doc.CreateElement("medicalReport");
root.SetAttribute("version", "1.0");
root.SetAttribute("generatedAt", DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss"));
doc.AppendChild(root);

// Коментар
XmlComment comment = doc.CreateComment("Автоматично згенеровано медичною системою");
root.AppendChild(comment);

// Елемент пацієнта з атрибутами
XmlElement patient = doc.CreateElement("patient");
patient.SetAttribute("id", "PT-1001");
patient.SetAttribute("status", "active");
root.AppendChild(patient);

// Дочірні елементи з текстовим вмістом
void AddElement(XmlElement parent, string tagName, string text)
{
    XmlElement el = doc.CreateElement(tagName);
    el.InnerText = text;
    parent.AppendChild(el);
}

AddElement(patient, "name",      "Петренко Іван Олексійович");
AddElement(patient, "birthDate", "1978-03-15");
AddElement(patient, "ward",      "Терапія");

// Вкладена структура: diagnoses -> diagnosis[]
XmlElement diagnoses = doc.CreateElement("diagnoses");
root.AppendChild(diagnoses);

var diagData = new[] {
    ("J06.9", "ICD-10", "ГРВІ"),
    ("I10",   "ICD-10", "Гіпертонічна хвороба"),
};
foreach (var (code, system, text) in diagData)
{
    XmlElement diag = doc.CreateElement("diagnosis");
    diag.SetAttribute("code",   code);
    diag.SetAttribute("system", system);
    diag.InnerText = text;
    diagnoses.AppendChild(diag);
}

// Збереження у рядок
using StringWriter sw = new StringWriter();
using XmlTextWriter xw = new XmlTextWriter(sw) { Formatting = Formatting.Indented, Indentation = 2 };
doc.WriteTo(xw);
Console.WriteLine(sw.ToString());

// Збереження у файл
string path = Path.Combine(Path.GetTempPath(), "patient_report.xml");
doc.Save(path);
Console.WriteLine($"\nЗбережено: {path}");
File.Delete(path);
```

### Зміна існуючого XML

```csharp run
using System;
using System.Xml;

string xml = """
<?xml version="1.0" encoding="utf-8"?>
<patients>
    <patient id="PT-1001">
        <name>Петренко І.О.</name>
        <ward>Терапія</ward>
    </patient>
</patients>
""";

XmlDocument doc = new XmlDocument();
doc.LoadXml(xml);

XmlElement root = doc.DocumentElement!;

// Зміна атрибуту існуючого вузла
XmlNode? p1 = doc.SelectSingleNode("/patients/patient[@id='PT-1001']");
p1?.Attributes?["id"]?.OwnerElement?.SetAttribute("status", "discharged");

// Зміна текстового вмісту
if (p1?["ward"] != null)
    p1["ward"]!.InnerText = "Виписаний";

// Додавання нового пацієнта
XmlElement newPatient = doc.CreateElement("patient");
newPatient.SetAttribute("id", "PT-1002");
newPatient.SetAttribute("status", "active");

XmlElement nameEl = doc.CreateElement("name");
nameEl.InnerText = "Бойко О.П.";
newPatient.AppendChild(nameEl);

XmlElement wardEl = doc.CreateElement("ward");
wardEl.InnerText = "Кардіологія";
newPatient.AppendChild(wardEl);

root.AppendChild(newPatient);

// Видалення вузла
XmlNode? toRemove = doc.SelectSingleNode("/patients/patient[@id='PT-1001']/ward");
toRemove?.ParentNode?.RemoveChild(toRemove);

// Результат
using System.IO.StringWriter sw = new System.IO.StringWriter();
using XmlTextWriter xw = new XmlTextWriter(sw) { Formatting = Formatting.Indented };
doc.WriteTo(xw);
Console.WriteLine(sw.ToString());
```

## Практичний сценарій: збереження результатів обстеження у XML

```csharp run
using System;
using System.Collections.Generic;
using System.IO;
using System.Xml;

string BuildExamXml(PatientExam exam)
{
    XmlDocument doc = new XmlDocument();
    doc.AppendChild(doc.CreateXmlDeclaration("1.0", "utf-8", null));

    XmlElement root = doc.CreateElement("examination");
    root.SetAttribute("version",  "2.0");
    root.SetAttribute("exportedAt", DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ"));
    doc.AppendChild(root);

    // Пацієнт
    XmlElement pt = doc.CreateElement("patient");
    pt.SetAttribute("id", exam.PatientId.ToString());
    pt.InnerText = exam.PatientName;
    root.AppendChild(pt);

    // Дата обстеження
    XmlElement dateEl = doc.CreateElement("examDate");
    dateEl.InnerText = exam.ExamDate.ToString("yyyy-MM-dd");
    root.AppendChild(dateEl);

    // Результати
    XmlElement resultsEl = doc.CreateElement("labResults");
    resultsEl.SetAttribute("count", exam.Results.Count.ToString());
    root.AppendChild(resultsEl);

    foreach (ExamResult r in exam.Results)
    {
        XmlElement res = doc.CreateElement("result");
        res.SetAttribute("status", r.Status);
        res.SetAttribute("ref",    r.ReferenceRange);

        XmlElement testEl = doc.CreateElement("test");  testEl.InnerText = r.TestName;
        XmlElement valEl  = doc.CreateElement("value"); valEl.InnerText = r.Value.ToString("F2");
        valEl.SetAttribute("unit", r.Unit);

        res.AppendChild(testEl);
        res.AppendChild(valEl);
        resultsEl.AppendChild(res);
    }

    using StringWriter sw = new StringWriter();
    using XmlTextWriter xw = new XmlTextWriter(sw) { Formatting = Formatting.Indented, Indentation = 4 };
    doc.WriteTo(xw);
    return sw.ToString();
}

// Тест
var exam = new PatientExam(1001, "Петренко Іван Олексійович", DateTime.Now, new List<ExamResult>
{
    new("Гемоглобін",   135.0, "г/л",     "норма",       "120-160"),
    new("Глюкоза",      7.8,   "ммоль/л", "вище норми",  "3.9-6.1"),
    new("Лейкоцити",    6.2,   "10^9/л",  "норма",       "4.0-9.0"),
    new("Холестерин",   5.1,   "ммоль/л", "норма",       "<5.2"),
});

string resultXml = BuildExamXml(exam);
Console.WriteLine(resultXml);

// Збереження
string path = Path.Combine(Path.GetTempPath(), "exam_result.xml");
File.WriteAllText(path, resultXml, System.Text.Encoding.UTF8);
Console.WriteLine($"\nФайл: {new FileInfo(path).Length.ToString()} байт");
File.Delete(path);

record ExamResult(string TestName, double Value, string Unit, string Status, string ReferenceRange);
record PatientExam(int PatientId, string PatientName, DateTime ExamDate, List<ExamResult> Results);
```

![Методи XmlDocument по категоріях](_assets/19-02/xmldocument-api.png)
