---
chapter: 19
chapterTitle: "Розділ 19. Серіалізація та десеріалізація. JSON та XML"
section: 6
number: "19.6"
title: "XPath та вибір між JSON і XML"
source: ""
---

## 19.6. XPath та вибір між JSON і XML

XPath (XML Path Language) — мова запитів до XML-документа. Вона дозволяє точно адресувати будь-який вузол або атрибут через вирази-шляхи: `/root/child`, `//descendant`, `@attribute`, `[predicat]`. XPath вбудований у `XmlDocument` через `SelectSingleNode`/`SelectNodes`, а для `XDocument` доступний через розширення `System.Xml.XPath`.

Після опанування всього інструментарію розділу — природне запитання: **коли обирати JSON, а коли XML?** Відповідь залежить від домену, вимог до схеми, набору інструментів і команди. Розглянемо обидва аспекти.

![XPath — синтаксис виразів та осі](_assets/19-06/xpath-syntax.png)

## Синтаксис XPath

XPath-вираз описує шлях по дереву вузлів. Основні конструкції:

| Вираз | Значення |
|---|---|
| `/clinic` | Кореневий елемент `<clinic>` |
| `/clinic/patient` | Прямі нащадки `<patient>` |
| `//diagnosis` | Всі `<diagnosis>` на будь-якій глибині |
| `@id` | Атрибут `id` поточного вузла |
| `patient[1]` | Перший елемент `<patient>` |
| `patient[last()]` | Останній `<patient>` |
| `patient[@ward='Терапія']` | `<patient>` з атрибутом ward="Терапія" |
| `*` | Будь-який елемент |
| `node()` | Будь-який вузол (включно з текстом) |
| `..` | Батьківський вузол |
| `.` | Поточний вузол |

### XPath-осі

Осі дозволяють переміщатися по дереву у будь-якому напрямку:

| Вісь | Вирізка |
|---|---|
| `child::` | Прямі дочірні (за замовчуванням) |
| `descendant::` | Всі нащадки (рекурсивно) |
| `parent::` | Батьківський вузол |
| `ancestor::` | Всі батьки вгору до кореня |
| `following-sibling::` | Сусіди після поточного вузла |
| `preceding-sibling::` | Сусіди перед поточним вузлом |
| `attribute::` | Атрибути (скорочення: `@`) |
| `self::` | Сам вузол |

### XPath-функції

```
count(nodes)          — кількість вузлів у наборі
normalize-space(str)  — прибрати зайві пробіли
contains(str, sub)    — перевірка входження підрядка
starts-with(str, pre) — перевірка початку рядка
string-length(str)    — довжина рядка
not(expr)             — логічне заперечення
position()            — позиція вузла в батьківському наборі
last()                — кількість вузлів в поточному наборі
```

## XPath у XmlDocument

```csharp run
using System;
using System.Xml;

string xml = """
<?xml version="1.0" encoding="utf-8"?>
<clinic date="2024-03-15">
    <patient id="PT-1001" ward="Терапія" status="active">
        <name>Петренко Іван Олексійович</name>
        <age>45</age>
        <diagnosis code="J06.9" severity="mild">ГРВІ</diagnosis>
        <diagnosis code="I10"   severity="moderate">Гіпертонія</diagnosis>
    </patient>
    <patient id="PT-1002" ward="Кардіологія" status="active">
        <name>Бойко Оксана Петрівна</name>
        <age>62</age>
        <diagnosis code="I21.0" severity="critical">Інфаркт міокарда</diagnosis>
    </patient>
    <patient id="PT-1003" ward="Терапія" status="discharged">
        <name>Мороз Василь Іванович</name>
        <age>38</age>
        <diagnosis code="E11.9" severity="moderate">Діабет 2 типу</diagnosis>
    </patient>
</clinic>
""";

XmlDocument doc = new XmlDocument();
doc.LoadXml(xml);

// 1. Точний шлях — перший пацієнт
XmlNode? first = doc.SelectSingleNode("/clinic/patient[1]/name");
Console.WriteLine($"Перший: {first?.InnerText}");

// 2. За значенням атрибуту
XmlNode? byId = doc.SelectSingleNode("/clinic/patient[@id='PT-1002']/name");
Console.WriteLine($"PT-1002: {byId?.InnerText}");

// 3. Фільтр за відділенням
XmlNodeList? therapy = doc.SelectNodes("/clinic/patient[@ward='Терапія']");
Console.WriteLine($"\nТерапія ({therapy?.Count.ToString()}):");
foreach (XmlNode p in therapy!)
    Console.WriteLine($"  {p["name"]?.InnerText} [{p.Attributes?["status"]?.Value}]");

// 4. contains() — часткове співпадіння
XmlNodeList? ivan = doc.SelectNodes("//patient[contains(name, 'Іван')]");
Console.WriteLine($"\nПацієнти з 'Іван' ({ivan?.Count.ToString()}):");
foreach (XmlNode p in ivan!)
    Console.WriteLine($"  {p["name"]?.InnerText}");

// 5. Комбінований OR у предикаті
XmlNodeList? cardioOrCrit = doc.SelectNodes(
    "//diagnosis[@severity='critical' or @severity='moderate']");
Console.WriteLine($"\nCritical/moderate діагнози ({cardioOrCrit?.Count.ToString()}):");
foreach (XmlNode d in cardioOrCrit!)
    Console.WriteLine($"  [{d.Attributes?["code"]?.Value}] {d.InnerText} — {d.Attributes?["severity"]?.Value}");

// 6. not() — активні пацієнти
XmlNodeList? active = doc.SelectNodes("/clinic/patient[not(@status='discharged')]");
Console.WriteLine($"\nАктивні пацієнти: {active?.Count.ToString()}");

// 7. count() і last()
XmlNode? lastPatient = doc.SelectSingleNode("/clinic/patient[last()]");
Console.WriteLine($"Останній пацієнт: {lastPatient?["name"]?.InnerText}");

int? total = (int?)doc.CreateNavigator()?.Evaluate("count(/clinic/patient)");
Console.WriteLine($"Всього пацієнтів: {total?.ToString()}");
```

## XPath у XDocument (System.Xml.XPath)

```csharp run
using System;
using System.Linq;
using System.Xml.Linq;
using System.Xml.XPath;

XDocument doc = XDocument.Parse("""
<clinic date="2024-03-15">
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
""");

// XPathSelectElement — перший вузол
XElement? pt = doc.XPathSelectElement("/clinic/patient[@ward='Кардіологія']");
Console.WriteLine($"Кардіологія: {pt?.Element("name")?.Value}");

// XPathSelectElements — колекція, повертає IEnumerable<XElement>
var all = doc.XPathSelectElements("//patient");
Console.WriteLine($"Всього пацієнтів: {all.Count().ToString()}");

// XPathEvaluate — арифметичні функції XPath
double count = (double)doc.XPathEvaluate("count(//patient)");
Console.WriteLine($"count(): {count.ToString()}");

// Пошук з contains
var withIvan = doc.XPathSelectElements("//patient[contains(name, 'Іван')]");
foreach (XElement p in withIvan)
    Console.WriteLine($"  {p.Element("name")?.Value}");

// XPathNavigator — позиційна навігація
System.Xml.XPath.XPathNavigator? nav = doc.CreateNavigator();
nav?.MoveToRoot();
Console.WriteLine($"\nNavigator root: {nav?.Name}");
```

## XPathNavigator для складної навігації

```csharp run
using System;
using System.Xml;
using System.Xml.XPath;

string xml = """
<clinic>
    <department name="Терапія">
        <patient id="PT-1001"><name>Петренко</name><age>45</age></patient>
        <patient id="PT-1002"><name>Мороз</name><age>38</age></patient>
    </department>
    <department name="Кардіологія">
        <patient id="PT-1003"><name>Бойко</name><age>62</age></patient>
    </department>
</clinic>
""";

XmlDocument doc = new XmlDocument();
doc.LoadXml(xml);

XPathNavigator nav = doc.CreateNavigator()!;

// Скомпілювати вираз для повторного використання
XPathExpression expr = nav.Compile("//patient[age > 40]");

XPathNodeIterator it = nav.Select(expr);
Console.WriteLine($"Пацієнти старші 40 ({it.Count.ToString()}):");
while (it.MoveNext())
{
    XPathNavigator cur = it.Current!;
    string id   = cur.GetAttribute("id", "");
    string name = cur.SelectSingleNode("name")?.Value ?? "";
    string age  = cur.SelectSingleNode("age")?.Value  ?? "";
    Console.WriteLine($"  [{id}] {name}, {age} р.");
}

// Навігація через батьківський вузол
XPathNavigator? firstPatient = nav.SelectSingleNode("//patient[@id='PT-1001']");
firstPatient?.MoveToParent();
Console.WriteLine($"\nВідділення PT-1001: {firstPatient?.GetAttribute("name", "")}");

// Агрегація через XPath 1.0
double avgAge = (double)nav.Evaluate("sum(//age) div count(//age)");
Console.WriteLine($"Середній вік: {avgAge.ToString("F1")} р.");
```

`XPathExpression` дозволяє скомпілювати XPath один раз і виконувати багаторазово без повторного парсингу — важливо при роботі з великими документами або частими запитами.

## JSON vs XML — порівняльний аналіз

```csharp run
using System;

// Один і той же об'єкт — в JSON та XML:

string json = """
{
  "id": "PT-1001",
  "name": "Петренко І.О.",
  "age": 45,
  "ward": "Терапія",
  "diagnoses": [
    { "code": "J06.9", "text": "ГРВІ" },
    { "code": "I10",   "text": "Гіпертонія" }
  ]
}
""";

string xml = """
<?xml version="1.0"?>
<patient id="PT-1001">
  <name>Петренко І.О.</name>
  <age>45</age>
  <ward>Терапія</ward>
  <diagnoses>
    <diagnosis code="J06.9">ГРВІ</diagnosis>
    <diagnosis code="I10">Гіпертонія</diagnosis>
  </diagnoses>
</patient>
""";

Console.WriteLine($"JSON: {json.Length.ToString()} символів");
Console.WriteLine($"XML:  {xml.Length.ToString()} символів");
Console.WriteLine($"XML більший на: {((xml.Length - json.Length) * 100.0 / json.Length).ToString("F0")}%");
Console.WriteLine();

// Порівняння за критеріями
Console.WriteLine("Критерій              JSON         XML");
Console.WriteLine(new string('-', 55));
Console.WriteLine($"{"Розмір",-22}{"менший",-13}{"більший"}");
Console.WriteLine($"{"Читаність",-22}{"висока",-13}{"висока"}");
Console.WriteLine($"{"Атрибути",-22}{"немає",-13}{"є"}");
Console.WriteLine($"{"Коментарі",-22}{"немає",-13}{"є"}");
Console.WriteLine($"{"Схема",-22}{"JSON Schema",-13}{"XSD/DTD"}");
Console.WriteLine($"{"Простори імен",-22}{"немає",-13}{"є (xmlns)"}");
Console.WriteLine($"{"LINQ у .NET",-22}{"JsonDocument",-13}{"XDocument+LINQ"}");
Console.WriteLine($"{"Серіалізатор .NET",-22}{"JsonSerializer",-13}{"XmlSerializer"}");
Console.WriteLine($"{"Потокове читання",-22}{"Utf8JsonReader",-13}{"XmlReader"}");
Console.WriteLine($"{"REST API",-22}{"стандарт",-13}{"застарілий"}");
Console.WriteLine($"{"HL7 / FHIR",-22}{"FHIR R4 JSON",-13}{"HL7 v2/v3 XML"}");
Console.WriteLine($"{"SOAP веб-сервіси",-22}{"не підходить",-13}{"стандарт"}");
Console.WriteLine($"{"Office (.docx)",-22}{"ні",-13}{"так"}");
Console.WriteLine($"{"Config .NET",-22}{"appsettings.json",-13}{"app.config"}");
```

![JSON vs XML — коли що обирати](_assets/19-06/json-vs-xml.png)

## Правила вибору формату

**Обирайте JSON, якщо:**
- Ви будуєте REST API або SPA-клієнт — JSON є індустріальним стандартом HTTP
- Дані — масиви, вкладені об'єкти без метаданих-атрибутів
- Потрібна максимальна стислість і простота парсингу у браузері
- Команда використовує JavaScript/TypeScript або мобільних клієнтів

**Обирайте XML, якщо:**
- Обмін з медичними системами: HL7 v2, HL7 v3, CDA, FHIR R2/R3 — там XML
- Потрібні атрибути як першокласний синтаксис (не поле-обгортка)
- SOAP-сервіси або WCF (корпоративний legacy)
- Документи з коментарями та просторами імен (XML схема обов'язкова)
- Office Open XML (.docx, .xlsx, .pptx) — це ZIP з XML всередині
- Конфіг .NET Framework: `Web.config`, `App.config`

**Обидва прийнятні, коли:**
- FHIR R4 підтримує і JSON, і XML — обирайте за можливостями клієнта
- Для зберігання у БД: JSON підтримується у PostgreSQL, MySQL, SQL Server нативно; XML — через XML-тип або nvarchar

## Підсумок розділу 19

```csharp run
using System;

Console.WriteLine("=== Розділ 19: Серіалізація та десеріалізація ===\n");

Console.WriteLine("19.1 System.Text.Json advanced:");
Console.WriteLine("  JsonDocument / JsonElement     — DOM без прив'язки до класу");
Console.WriteLine("  Utf8JsonWriter                 — найшвидший запис JSON");
Console.WriteLine("  JsonConverter<T>               — кастомна логіка серіалізації");
Console.WriteLine("  [JsonPolymorphic]              — поліморфний JSON");
Console.WriteLine("  SerializeAsync / DeserializeAsync — асинхронний I/O\n");

Console.WriteLine("19.2 XML + XmlDocument:");
Console.WriteLine("  XmlDocument.LoadXml / Load     — DOM у пам'яті");
Console.WriteLine("  SelectSingleNode / SelectNodes  — XPath-запити");
Console.WriteLine("  CreateElement / AppendChild     — побудова XML програмно\n");

Console.WriteLine("19.3 XDocument + LINQ to XML:");
Console.WriteLine("  new XElement(new XElement(...))  — декларативна побудова");
Console.WriteLine("  Elements() / Descendants()       — IEnumerable<XElement>");
Console.WriteLine("  Where / Select / GroupBy / OrderBy — нативний LINQ\n");

Console.WriteLine("19.4 XmlReader + XmlWriter:");
Console.WriteLine("  XmlReader.Create(stream)         — потокове читання O(1) RAM");
Console.WriteLine("  NodeType: Element/Text/EndElement — автомат станів");
Console.WriteLine("  XmlWriter.Create(stream, settings)— послідовний запис\n");

Console.WriteLine("19.5 XmlSerializer:");
Console.WriteLine("  [XmlRoot] [XmlElement] [XmlAttribute] [XmlIgnore]");
Console.WriteLine("  [XmlArray] [XmlArrayItem]        — колекції");
Console.WriteLine("  [XmlInclude]                     — поліморфізм\n");

Console.WriteLine("19.6 XPath + JSON vs XML:");
Console.WriteLine("  /path, //any, @attr, [predicate] — XPath-адресація");
Console.WriteLine("  XPathNavigator, XPathExpression  — скомпільовані запити");
Console.WriteLine("  JSON: REST API, браузер, стислість");
Console.WriteLine("  XML: HL7, SOAP, Office, схема, простори імен");
```
