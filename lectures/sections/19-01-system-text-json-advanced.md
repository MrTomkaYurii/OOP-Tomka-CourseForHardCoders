---
chapter: 19
chapterTitle: "Розділ 19. Серіалізація та десеріалізація. JSON та XML"
section: 1
number: "19.1"
title: "System.Text.Json — поглиблено"
source: ""
---

## 19.1. System.Text.Json — поглиблено

У розділі 18.6 ми розглянули базові операції `JsonSerializer.Serialize` / `Deserialize` — достатньо для більшості задач. Але реальні системи стикаються з ситуаціями, де базового API не вистачає: схема JSON невідома заздалегідь, потрібна власна логіка серіалізації для специфічного типу, дані надходять як потік з HTTP і не варто буферизувати їх у рядок, або ієрархія класів потребує поліморфної серіалізації.

`System.Text.Json` надає **три рівні API**: від зручного `JsonSerializer` до низькорівневих `JsonDocument`/`Utf8JsonReader`. Чим нижчий рівень — тим більший контроль і вища продуктивність, але й більше коду.

![Три рівні API System.Text.Json](_assets/19-01/json-api-levels.png)

## JsonDocument та JsonElement — DOM без десеріалізації

`JsonDocument` — це легка DOM-модель для JSON, яка дозволяє читати та навігувати по JSON-документу **без прив'язки до конкретного C#-класу**. Корисно, коли схема документа невідома або змінюється — наприклад, відповідь зовнішнього API, налаштування плагінів, гетерогенні медичні записи.

```csharp run
using System;
using System.Text.Json;

// Сценарій: відповідь зовнішнього API лабораторії — схема невідома заздалегідь
string labApiResponse = """
{
    "requestId": "LAB-2024-0315",
    "patient": {
        "id": 1001,
        "name": "Петренко Іван Олексійович",
        "ward": "Терапія"
    },
    "results": [
        { "test": "Гемоглобін",  "value": 135.0, "unit": "г/л",     "status": "норма" },
        { "test": "Глюкоза",     "value": 7.8,   "unit": "ммоль/л", "status": "вище норми" },
        { "test": "Лейкоцити",   "value": 6.2,   "unit": "10^9/л",  "status": "норма" }
    ],
    "processedAt": "2024-03-15T14:30:00Z"
}
""";

// JsonDocument.Parse — парсимо без прив'язки до класу
using JsonDocument doc = JsonDocument.Parse(labApiResponse);
JsonElement root = doc.RootElement;

// Читання скалярних значень
string requestId = root.GetProperty("requestId").GetString()!;
Console.WriteLine($"Запит: {requestId}");

// Навігація по вкладених об'єктах
JsonElement patient = root.GetProperty("patient");
int    patientId   = patient.GetProperty("id").GetInt32();
string patientName = patient.GetProperty("name").GetString()!;
Console.WriteLine($"Пацієнт: [{patientId.ToString()}] {patientName}");

// Перебір масиву
JsonElement results = root.GetProperty("results");
Console.WriteLine($"\nРезультати ({results.GetArrayLength().ToString()} аналізів):");
foreach (JsonElement result in results.EnumerateArray())
{
    string test   = result.GetProperty("test").GetString()!;
    double value  = result.GetProperty("value").GetDouble();
    string unit   = result.GetProperty("unit").GetString()!;
    string status = result.GetProperty("status").GetString()!;
    string icon   = status == "норма" ? "[OK]" : "[!!]";
    Console.WriteLine($"  {icon} {test}: {value.ToString()} {unit} — {status}");
}

// Перевірка існування поля
if (root.TryGetProperty("processedAt", out JsonElement ts))
    Console.WriteLine($"\nОброблено: {ts.GetDateTimeOffset():yyyy-MM-dd HH:mm}");
```

`JsonDocument` реалізує `IDisposable` — завжди використовуйте `using`. Внутрішньо він рентить пам'ять з пулу (`ArrayPool<byte>`), і `Dispose` повертає її назад. Без `Dispose` пам'ять буде затримана до наступного GC.

### TryGetProperty та перевірка типів

```csharp run
using System;
using System.Text.Json;

string json = """
{
    "patientId": 1002,
    "temperature": 37.2,
    "hospitalized": true,
    "notes": null,
    "tags": ["ГРВІ", "сезонний"]
}
""";

using JsonDocument doc = JsonDocument.Parse(json);
JsonElement root = doc.RootElement;

// TryGetProperty — безпечне читання (не кидає при відсутності поля)
if (root.TryGetProperty("temperature", out JsonElement temp))
    Console.WriteLine($"Температура: {temp.GetDouble().ToString("F1")} °C");

// Перевірка типу через ValueKind
foreach (JsonProperty prop in root.EnumerateObject())
{
    string typeName = prop.Value.ValueKind switch
    {
        JsonValueKind.Number  => $"number = {prop.Value.GetDouble().ToString()}",
        JsonValueKind.String  => $"string = \"{prop.Value.GetString()}\"",
        JsonValueKind.True    => "bool = true",
        JsonValueKind.False   => "bool = false",
        JsonValueKind.Null    => "null",
        JsonValueKind.Array   => $"array[{prop.Value.GetArrayLength().ToString()}]",
        JsonValueKind.Object  => "object {...}",
        _                     => prop.Value.ValueKind.ToString()
    };
    Console.WriteLine($"  {prop.Name}: {typeName}");
}
```

`JsonValueKind` — перелік, що описує JSON-тип вузла: `Object`, `Array`, `String`, `Number`, `True`, `False`, `Null`, `Undefined`. Перевіряйте `ValueKind` перед читанням, якщо схема документа не гарантована.

## Utf8JsonWriter — швидкісний запис JSON

`Utf8JsonWriter` — найнижчий рівень запису JSON. Він записує безпосередньо в UTF-8 байти без проміжного рядкового представлення — це найшвидший можливий спосіб генерації JSON у .NET:

```csharp run
using System;
using System.IO;
using System.Text;
using System.Text.Json;

using MemoryStream ms = new MemoryStream();
var writerOptions = new JsonWriterOptions { Indented = true };

using (Utf8JsonWriter writer = new Utf8JsonWriter(ms, writerOptions))
{
    writer.WriteStartObject();                          // {

    writer.WriteString("requestId", "MED-2024-0315");
    writer.WriteNumber("version", 2);

    writer.WriteStartObject("patient");                 // "patient": {
    writer.WriteNumber("id", 1001);
    writer.WriteString("name", "Петренко І.О.");
    writer.WriteBoolean("hospitalized", false);
    writer.WriteEndObject();                            // }

    writer.WriteStartArray("diagnoses");                // "diagnoses": [
    writer.WriteStringValue("J06.9");
    writer.WriteStringValue("I10");
    writer.WriteEndArray();                             // ]

    writer.WriteNull("notes");                          // "notes": null
    writer.WriteString("createdAt", DateTime.UtcNow);

    writer.WriteEndObject();                            // }
}

string json = Encoding.UTF8.GetString(ms.ToArray());
Console.WriteLine(json);
Console.WriteLine($"\nРозмір: {ms.Length.ToString()} байт");
```

`Utf8JsonWriter` застосовується у бібліотеках і фреймворках, де продуктивність критична — наприклад, ASP.NET Core використовує його внутрішньо для серіалізації HTTP-відповідей. Для звичайного застосунку достатньо `JsonSerializer`.

## Кастомні конвертери: JsonConverter\<T\>

Стандартна серіалізація не завжди підходить для специфічних типів. `JsonConverter<T>` дозволяє повністю контролювати, як конкретний тип читається з JSON і записується в JSON:

```csharp run
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

// Кастомний тип — діапазон нормальних значень показника
struct NormalRange
{
    public double Min { get; }
    public double Max { get; }
    public NormalRange(double min, double max) { Min = min; Max = max; }
    public override string ToString() => $"{Min.ToString()}-{Max.ToString()}";
}

// За замовчуванням NormalRange серіалізується як об'єкт {"Min":...,"Max":...}
// Хочемо: рядок "4.0-6.5" для компактності

class NormalRangeConverter : JsonConverter<NormalRange>
{
    // Читання: "4.0-6.5" -> NormalRange(4.0, 6.5)
    public override NormalRange Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        string? s = reader.GetString() ?? throw new JsonException("Expected string for NormalRange");
        string[] parts = s.Split('-');
        if (parts.Length != 2) throw new JsonException($"Invalid NormalRange format: {s}");
        return new NormalRange(double.Parse(parts[0]), double.Parse(parts[1]));
    }

    // Запис: NormalRange(4.0, 6.5) -> "4.0-6.5"
    public override void Write(Utf8JsonWriter writer, NormalRange value, JsonSerializerOptions options)
    {
        writer.WriteStringValue($"{value.Min.ToString()}-{value.Max.ToString()}");
    }
}

class LabTest
{
    public string      Name    { get; set; } = "";
    public double      Value   { get; set; }
    public string      Unit    { get; set; } = "";
    [JsonConverter(typeof(NormalRangeConverter))]   // атрибут на конкретному полі
    public NormalRange Normal  { get; set; }
}

var test = new LabTest
{
    Name   = "Глюкоза",
    Value  = 5.4,
    Unit   = "ммоль/л",
    Normal = new NormalRange(3.9, 6.1)
};

var opts = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(test, opts);
Console.WriteLine("JSON з кастомним конвертером:");
Console.WriteLine(json);

// Десеріалізація — конвертер відпрацьовує автоматично
LabTest? loaded = JsonSerializer.Deserialize<LabTest>(json, opts);
Console.WriteLine($"\nВідновлено: {loaded?.Name} = {loaded?.Value.ToString()} {loaded?.Unit}");
Console.WriteLine($"Норма: {loaded?.Normal}");
Console.WriteLine($"Статус: {(loaded?.Value >= loaded?.Normal.Min && loaded?.Value <= loaded?.Normal.Max ? "норма" : "відхилення")}");
```

Конвертер можна зареєструвати **глобально** через `options.Converters.Add(new NormalRangeConverter())` замість атрибута на кожному полі — тоді він спрацює для всіх властивостей цього типу в усій програмі.

## Поліморфна серіалізація: JsonDerivedType

Коли в полі може бути один з кількох підтипів, `JsonSerializer` за замовчуванням серіалізує лише властивості базового типу і при десеріалізації не знає, який підтип відновити. Атрибути `[JsonPolymorphic]` і `[JsonDerivedType]` вирішують це:

```csharp run
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

[JsonPolymorphic(TypeDiscriminatorPropertyName = "$type")]
[JsonDerivedType(typeof(BloodTest),   typeDiscriminator: "blood")]
[JsonDerivedType(typeof(EcgRecord),   typeDiscriminator: "ecg")]
[JsonDerivedType(typeof(ImagingData), typeDiscriminator: "imaging")]
abstract class MedicalResult
{
    public int    PatientId  { get; set; }
    public DateTime RecordedAt { get; set; } = DateTime.Now;
}

class BloodTest : MedicalResult
{
    public double Glucose    { get; set; }
    public double Hemoglobin { get; set; }
}

class EcgRecord : MedicalResult
{
    public int    HeartRate  { get; set; }
    public string Rhythm     { get; set; } = "";
}

class ImagingData : MedicalResult
{
    public string Modality   { get; set; } = ""; // МРТ, КТ, УЗД
    public string BodyPart   { get; set; } = "";
}

// Список різних підтипів
var results = new List<MedicalResult>
{
    new BloodTest   { PatientId=1001, Glucose=5.1, Hemoglobin=135.0 },
    new EcgRecord   { PatientId=1001, HeartRate=72, Rhythm="синусовий" },
    new ImagingData { PatientId=1002, Modality="УЗД", BodyPart="черевна порожнина" },
};

var opts = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(results, opts);
Console.WriteLine("Поліморфний JSON:");
Console.WriteLine(json);

// Десеріалізація відновлює правильний підтип
var loaded = JsonSerializer.Deserialize<List<MedicalResult>>(json, opts)!;
foreach (MedicalResult r in loaded)
{
    string info = r switch
    {
        BloodTest   b => $"Кров: глюкоза={b.Glucose.ToString()}",
        EcgRecord   e => $"ЕКГ: пульс={e.HeartRate.ToString()}, ритм={e.Rhythm}",
        ImagingData i => $"Знімок: {i.Modality} ({i.BodyPart})",
        _             => "невідомий тип"
    };
    Console.WriteLine($"  [{r.GetType().Name}] пацієнт {r.PatientId.ToString()}: {info}");
}
```

`$type` — дискримінатор типу, який `JsonSerializer` автоматично додає при записі і читає при десеріалізації. Ім'я поля (`TypeDiscriminatorPropertyName`) можна задати довільним — часто використовують `"type"`, `"kind"`, `"$type"`.

## Async серіалізація: SerializeAsync та DeserializeAsync

Для роботи з HTTP-потоками та великими файлами є async-версії, що не блокують потік:

```csharp run
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

class PatientRecord
{
    public int      Id        { get; set; }
    public string   Name      { get; set; } = "";
    public string   Diagnosis { get; set; } = "";
    public DateTime AdmittedAt { get; set; }
}

string filePath = Path.Combine(Path.GetTempPath(), "patients_async.json");

var patients = new List<PatientRecord>
{
    new() { Id=1001, Name="Петренко І.О.", Diagnosis="J06.9", AdmittedAt=DateTime.Now.AddDays(-3) },
    new() { Id=1002, Name="Бойко О.П.",    Diagnosis="I10",   AdmittedAt=DateTime.Now.AddDays(-1) },
    new() { Id=1003, Name="Мороз В.І.",    Diagnosis="E11.9", AdmittedAt=DateTime.Now },
};

var opts = new JsonSerializerOptions { WriteIndented = true };

// Async запис у файл — не блокує потік під час I/O
await using (FileStream fs = File.Create(filePath))
    await JsonSerializer.SerializeAsync(fs, patients, opts);

Console.WriteLine($"Async запис: {new FileInfo(filePath).Length.ToString()} байт");

// Async читання з файлу
await using (FileStream fs = File.OpenRead(filePath))
{
    List<PatientRecord>? loaded = await JsonSerializer.DeserializeAsync<List<PatientRecord>>(fs, opts);
    Console.WriteLine($"Async читання: {loaded?.Count.ToString()} записів");
    foreach (var p in loaded ?? new())
        Console.WriteLine($"  [{p.Id.ToString()}] {p.Name} — {p.Diagnosis}");
}

File.Delete(filePath);
```

`SerializeAsync` / `DeserializeAsync` — особливо важливі у ASP.NET Core: при відповіді на HTTP-запит серіалізація відбувається напряму у `HttpResponse.Body`-потік без буферизації всього JSON у пам'яті. Для консольних застосунків або Desktop різниця мінімальна, але для веб-сервісів під навантаженням — суттєва.

## Практичний сценарій: агрегація гетерогенних JSON-відповідей

```csharp run
using System;
using System.Collections.Generic;
using System.Text.Json;

// Симуляція: кілька API повертають різні JSON-схеми
// Потрібно агрегувати дані без фіксованих класів

string[] apiResponses = {
    """{"source":"lab",     "patientId":1001, "test":"Глюкоза",    "value":5.1,  "unit":"ммоль/л"}""",
    """{"source":"vitals",  "patientId":1001, "pulse":72,           "temp":36.8,  "bp":"120/80"}""",
    """{"source":"pharmacy","patientId":1001, "drug":"Амоксицилін", "dose":"500mg","days":7}""",
};

var summary = new Dictionary<string, List<string>>();

foreach (string response in apiResponses)
{
    using JsonDocument doc = JsonDocument.Parse(response);
    JsonElement root = doc.RootElement;

    string source    = root.GetProperty("source").GetString()!;
    int    patientId = root.GetProperty("patientId").GetInt32();

    if (!summary.ContainsKey(source))
        summary[source] = new List<string>();

    // Агрегуємо поля, залежно від джерела
    switch (source)
    {
        case "lab":
            string test  = root.GetProperty("test").GetString()!;
            double value = root.GetProperty("value").GetDouble();
            string unit  = root.GetProperty("unit").GetString()!;
            summary[source].Add($"{test}: {value.ToString()} {unit}");
            break;

        case "vitals":
            int    pulse = root.GetProperty("pulse").GetInt32();
            double temp  = root.GetProperty("temp").GetDouble();
            string bp    = root.GetProperty("bp").GetString()!;
            summary[source].Add($"пульс={pulse.ToString()}, t={temp.ToString("F1")}, АТ={bp}");
            break;

        case "pharmacy":
            string drug = root.GetProperty("drug").GetString()!;
            string dose = root.GetProperty("dose").GetString()!;
            int    days = root.GetProperty("days").GetInt32();
            summary[source].Add($"{drug} {dose} x {days.ToString()} днів");
            break;
    }
}

Console.WriteLine("=== Зведення по пацієнту 1001 ===");
foreach (var (source, items) in summary)
{
    Console.WriteLine($"\n[{source.ToUpper()}]");
    foreach (string item in items)
        Console.WriteLine($"  • {item}");
}
```

![Кастомний JsonConverter\<T\> — схема роботи](_assets/19-01/custom-converter.png)
