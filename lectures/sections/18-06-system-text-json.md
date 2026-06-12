---
chapter: 18
chapterTitle: "Розділ 18. Робота з файловою системою"
section: 6
number: "18.6"
title: "System.Text.Json. Серіалізація та десеріалізація"
source: ""
---

## 18.6. System.Text.Json. Серіалізація та десеріалізація

Текстові та бінарні потоки з попередніх розділів вирішують питання *як* зберегти байти. Але сучасний застосунок рідко оперує сирими байтами — він оперує **об'єктами**: пацієнтами, аналізами, рецептами, планами лікування. Зберегти об'єкт C# у файл або передати через мережу означає його **серіалізувати** — перетворити граф об'єктів у послідовність байтів. Зворотний процес — **десеріалізація**: відновити об'єкти зі збереженого представлення.

Найпоширеніший формат для серіалізації у сучасних застосунках — **JSON** (JavaScript Object Notation). Він людиночитабельний, підтримується всіма мовами і платформами, і є стандартом де-факто для REST API, конфігурацій та обміну даними між сервісами.

.NET 5+ включає `System.Text.Json` — **вбудовану бібліотеку серіалізації JSON**, оптимізовану для продуктивності. Вона замінила сторонній `Newtonsoft.Json` (Json.NET) як основний інструмент для більшості задач.

![Потік JSON-серіалізації в System.Text.Json](_assets/18-06/json-serialization-flow.png)

## JsonSerializer — базова серіалізація та десеріалізація

Центральний клас бібліотеки — `JsonSerializer`. Два основних методи: `Serialize` (об'єкт → рядок JSON) і `Deserialize` (рядок JSON → об'єкт).

```csharp run
using System;
using System.Text.Json;

// Серіалізація: об'єкт → JSON рядок
var card = new PatientCard
{
    Id           = 1001,
    FullName     = "Петренко Іван Олексійович",
    Age          = 45,
    Diagnosis    = "J06.9",
    Hospitalized = false,
    Glucose      = 5.1
};

string json = JsonSerializer.Serialize(card);
Console.WriteLine("JSON (compact):");
Console.WriteLine(json);

// Відформатований JSON з відступами
var options = new JsonSerializerOptions { WriteIndented = true };
string prettyJson = JsonSerializer.Serialize(card, options);
Console.WriteLine("\nJSON (indented):");
Console.WriteLine(prettyJson);

// Десеріалізація: JSON рядок → об'єкт
PatientCard? restored = JsonSerializer.Deserialize<PatientCard>(json);
Console.WriteLine($"\nВідновлено: {restored?.FullName}, діагноз={restored?.Diagnosis}, вік={restored?.Age.ToString()}");

// Моделі даних медичної картки
class PatientCard
{
    public int    Id          { get; set; }
    public string FullName    { get; set; } = "";
    public int    Age         { get; set; }
    public string Diagnosis   { get; set; } = "";
    public bool   Hospitalized { get; set; }
    public double Glucose     { get; set; }
}
```

`JsonSerializer.Serialize` без опцій генерує компактний JSON без пробілів — це оптимально для мережевої передачі. `WriteIndented = true` додає відступи для читабельності — зручно для конфігурацій і логів.

## Серіалізація до файлу та з файлу

Найчастіший сценарій — збереження об'єктів у файл і завантаження з файлу. `JsonSerializer` інтегрується зі `Stream`:

```csharp run
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

string filePath = Path.Combine(Path.GetTempPath(), "med_records.json");

var records = new List<MedRecord>
{
    new() { PatientId=1001, PatientName="Петренко І.О.", TestName="Гемоглобін", Value=135.0, Unit="г/л",     Status="норма",       RecordedAt=DateTime.Now.AddHours(-2) },
    new() { PatientId=1001, PatientName="Петренко І.О.", TestName="Глюкоза",    Value=5.1,   Unit="ммоль/л", Status="норма",       RecordedAt=DateTime.Now.AddHours(-2) },
    new() { PatientId=1002, PatientName="Бойко О.П.",    TestName="Глюкоза",    Value=8.7,   Unit="ммоль/л", Status="вище норми",  RecordedAt=DateTime.Now.AddHours(-1) },
    new() { PatientId=1003, PatientName="Мороз В.І.",    TestName="Гемоглобін", Value=98.0,  Unit="г/л",     Status="нижче норми", RecordedAt=DateTime.Now },
};

var options = new JsonSerializerOptions
{
    WriteIndented = true,
    // Серіалізація DateTime у ISO 8601
};

// Запис у файл через Stream — ефективніше ніж Serialize → string → WriteAllText
using (FileStream fs = File.Create(filePath))
{
    JsonSerializer.Serialize(fs, records, options);
}

FileInfo fi = new FileInfo(filePath);
Console.WriteLine($"Записано: {fi.Length.ToString()} байт");

// Читання з файлу
List<MedRecord>? loaded;
using (FileStream fs = File.OpenRead(filePath))
{
    loaded = JsonSerializer.Deserialize<List<MedRecord>>(fs);
}

Console.WriteLine($"Завантажено: {loaded?.Count.ToString()} записів");
if (loaded != null)
{
    foreach (MedRecord r in loaded)
    {
        string icon = r.Status == "норма" ? "[OK]" : "[!!]";
        Console.WriteLine($"  {icon} {r.PatientName} | {r.TestName}: {r.Value.ToString()} {r.Unit} ({r.Status})");
    }
}

File.Delete(filePath);

class MedRecord
{
    public int      PatientId  { get; set; }
    public string   PatientName { get; set; } = "";
    public string   TestName   { get; set; } = "";
    public double   Value      { get; set; }
    public string   Unit       { get; set; } = "";
    public string   Status     { get; set; } = "";
    public DateTime RecordedAt { get; set; }
}
```

Передача `Stream` у `JsonSerializer.Serialize/Deserialize` ефективніша за `string`-варіант: бібліотека пише напряму у потік без проміжного рядкового буфера — важливо для великих об'єктів.

## JsonSerializerOptions — налаштування серіалізації

`JsonSerializerOptions` — центральний об'єкт конфігурації, що контролює практично всі аспекти серіалізації:

```csharp run
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

var vitals = new PatientVitals
{
    PatientId     = 1001,
    fullName      = "Петренко І.О.",
    BloodPressure = 120.0 / 80.0,
    HeartRate     = 72,
    Notes         = null
};

// За замовчуванням: PascalCase, null включається
Console.WriteLine("=== Стандартні опції ===");
Console.WriteLine(JsonSerializer.Serialize(vitals, new JsonSerializerOptions { WriteIndented = true }));

// camelCase назви полів (стандарт JavaScript/REST)
Console.WriteLine("\n=== camelCase ===");
var camelOptions = new JsonSerializerOptions
{
    WriteIndented      = true,
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
};
Console.WriteLine(JsonSerializer.Serialize(vitals, camelOptions));

// Ігнорування null-значень
Console.WriteLine("\n=== Без null полів ===");
var noNullOptions = new JsonSerializerOptions
{
    WriteIndented      = true,
    DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
};
Console.WriteLine(JsonSerializer.Serialize(vitals, noNullOptions));

// Десеріалізація нечутлива до регістру
string json = """{"patientid":1002,"fullname":"Бойко О.П.","bloodpressure":1.6,"heartrate":145,"notes":null}""";
var relaxedOptions = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
PatientVitals? loaded = JsonSerializer.Deserialize<PatientVitals>(json, relaxedOptions);
Console.WriteLine($"\nНечутливо до регістру: {loaded?.fullName}, пульс={loaded?.HeartRate.ToString()}");

class PatientVitals
{
    public int    PatientId    { get; set; }
    public string fullName     { get; set; } = "";  // camelCase назва
    public double BloodPressure { get; set; }
    public int    HeartRate    { get; set; }
    public string? Notes       { get; set; }        // null-able
}
```

### Типові JsonSerializerOptions для медичного застосунку

```csharp run
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

// Рекомендований набір опцій для REST API / зберігання
var standardOptions = new JsonSerializerOptions
{
    WriteIndented              = false,               // компактний для API/файлів
    PropertyNamingPolicy       = JsonNamingPolicy.CamelCase, // camelCase для JS
    PropertyNameCaseInsensitive = true,               // гнучке читання
    DefaultIgnoreCondition     = JsonIgnoreCondition.WhenWritingNull, // без null
    // Enum як рядки замість чисел
    Converters = { new JsonStringEnumConverter() }
};

var apt = new Appointment { Id = 5, Doctor = "Коваленко О.П.", Status = PatientStatus.InTreatment, Room = null };
string json = JsonSerializer.Serialize(apt, standardOptions);
Console.WriteLine("Стандартний API JSON:");
Console.WriteLine(json);

// Десеріалізація
Appointment? loaded = JsonSerializer.Deserialize<Appointment>(json, standardOptions);
Console.WriteLine($"\nПовернуто: id={loaded?.Id.ToString()}, лікар={loaded?.Doctor}, статус={loaded?.Status}");

// Використовуємо enum
enum PatientStatus { Active, Discharged, InTreatment }

class Appointment
{
    public int           Id     { get; set; }
    public string        Doctor { get; set; } = "";
    public PatientStatus Status { get; set; }
    public string?       Room   { get; set; }
}
```

## Атрибути керування серіалізацією

`System.Text.Json` надає атрибути для тонкого контролю над кожним полем і класом:

```csharp run
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

var record = new DiagnosisRecord
{
    PatientId     = 1001,
    DiagnosisCode = "J06.9",
    InternalNotes = "ці дані НЕ збережуться у JSON",
    PatientName   = "Петренко І.О.",
    RecordedAt    = DateTime.Now,
    Ward          = "Терапія",
    OptionalValue = null
};

string json = JsonSerializer.Serialize(record, new JsonSerializerOptions { WriteIndented = true });
Console.WriteLine("JSON з атрибутами:");
Console.WriteLine(json);

// Перевіряємо: InternalNotes відсутній у JSON
Console.WriteLine($"\nПоле 'InternalNotes' у JSON: {json.Contains("InternalNotes").ToString()} (має бути False)");
Console.WriteLine($"Поле 'patient_id' у JSON: {json.Contains("patient_id").ToString()} (має бути True)");

class DiagnosisRecord
{
    [JsonPropertyName("patient_id")]   // Перейменування поля у JSON
    public int PatientId { get; set; }
    
    [JsonPropertyName("diagnosis_code")]
    public string DiagnosisCode { get; set; } = "";
    
    [JsonIgnore]                        // Поле не включається у JSON
    public string InternalNotes { get; set; } = "внутрішні примітки";
    
    [JsonPropertyOrder(1)]              // Порядок полів у JSON
    public string PatientName { get; set; } = "";
    
    [JsonPropertyOrder(2)]
    public DateTime RecordedAt { get; set; }
    
    [JsonInclude]                       // Включає публічне поле (не тільки property)
    public string Ward = "";
    
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingDefault)]
    public double? OptionalValue { get; set; } // null або 0 — не записується
}
```

| Атрибут | Призначення |
|---|---|
| `[JsonPropertyName("name")]` | Задає ім'я поля у JSON |
| `[JsonIgnore]` | Виключає поле з серіалізації |
| `[JsonIgnore(Condition = ...)]` | Умовне виключення (null, default) |
| `[JsonPropertyOrder(n)]` | Порядок полів у виводі |
| `[JsonInclude]` | Включає публічне поле (field, не property) |
| `[JsonRequired]` | Поле обов'язкове при десеріалізації |
| `[JsonConverter(typeof(...))]` | Кастомний конвертер для типу |

## Робота з вкладеними структурами та колекціями

```csharp run
using System;
using System.Collections.Generic;
using System.Text.Json;

var patient = new Patient
{
    Id      = 1001,
    Name    = "Петренко І.О.",
    Address = new Address { City = "Київ", Street = "вул. Хрещатик, 1" },
    Diagnoses = new List<string> { "J06.9", "I10" },
    LabResults = new Dictionary<string, double>
    {
        ["Гемоглобін"] = 135.0,
        ["Глюкоза"]    = 5.1,
        ["Холестерин"] = 4.8
    }
};

var opts = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(patient, opts);
Console.WriteLine("Вкладений JSON:");
Console.WriteLine(json);

// Десеріалізація — вкладені об'єкти відновлюються автоматично
Patient? loaded = JsonSerializer.Deserialize<Patient>(json, opts);
Console.WriteLine($"\nВідновлено:");
Console.WriteLine($"  {loaded?.Name}, м.{loaded?.Address?.City}");
Console.WriteLine($"  Діагнози: {string.Join(", ", loaded?.Diagnoses ?? new())}");
foreach (var (test, val) in loaded?.LabResults ?? new())
    Console.WriteLine($"  {test}: {val.ToString()}");

// Вкладені класи
class Address
{
    public string City   { get; set; } = "";
    public string Street { get; set; } = "";
}

class Patient
{
    public int             Id         { get; set; }
    public string          Name       { get; set; } = "";
    public Address?        Address    { get; set; }
    public List<string>    Diagnoses  { get; set; } = new();
    public Dictionary<string, double> LabResults { get; set; } = new();
}
```

## Практичний сценарій: JSON-конфігурація медичного застосунку

```csharp run
using System;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Collections.Generic;

string configPath = Path.Combine(Path.GetTempPath(), "clinic_config.json");

// Запис конфігурації
var config = new ClinicConfig
{
    ClinicName         = "Міська клінічна лікарня №1",
    Departments        = new List<string> { "Терапія", "Кардіологія", "Неврологія", "Хірургія" },
    MaxPatientsPerDay  = 200,
    Thresholds         = new LabThresholds { GlucoseMax=7.0, PulseMin=60, PulseMax=100, HemoglobinMin=110.0 },
    LastUpdated        = DateTime.Now
};

var opts = new JsonSerializerOptions { WriteIndented = true };
using (FileStream fs = File.Create(configPath))
    JsonSerializer.Serialize(fs, config, opts);

Console.WriteLine($"Конфіг збережено: {new FileInfo(configPath).Length.ToString()} байт");

// Завантаження та використання
ClinicConfig? loaded;
using (FileStream fs = File.OpenRead(configPath))
    loaded = JsonSerializer.Deserialize<ClinicConfig>(fs, opts);

Console.WriteLine($"\nКлініка: {loaded?.ClinicName}");
Console.WriteLine($"Відділення: {string.Join(", ", loaded?.Departments ?? new())}");
Console.WriteLine($"Ліміт пацієнтів/день: {loaded?.MaxPatientsPerDay.ToString()}");
Console.WriteLine($"Порогові значення:");
Console.WriteLine($"  Глюкоза: <= {loaded?.Thresholds.GlucoseMax.ToString()} ммоль/л");
Console.WriteLine($"  Пульс: {loaded?.Thresholds.PulseMin.ToString()} - {loaded?.Thresholds.PulseMax.ToString()} уд/хв");

// Перевірка пацієнта по конфігу
double patientGlucose = 8.5;
bool criticalGlucose = loaded != null && patientGlucose > loaded.Thresholds.GlucoseMax;
Console.WriteLine($"\nГлюкоза {patientGlucose.ToString()} ммоль/л — {(criticalGlucose ? "КРИТИЧНО" : "норма")}");

File.Delete(configPath);

// Конфігурація клініки — типовий сценарій для JSON
class ClinicConfig
{
    [JsonPropertyName("clinic_name")]
    public string ClinicName { get; set; } = "";
    
    [JsonPropertyName("departments")]
    public List<string> Departments { get; set; } = new();
    
    [JsonPropertyName("max_patients_per_day")]
    public int MaxPatientsPerDay { get; set; }
    
    [JsonPropertyName("lab_thresholds")]
    public LabThresholds Thresholds { get; set; } = new();
    
    [JsonPropertyName("last_updated")]
    public DateTime LastUpdated { get; set; }
}

class LabThresholds
{
    [JsonPropertyName("glucose_max")]    public double GlucoseMax    { get; set; }
    [JsonPropertyName("pulse_min")]      public int    PulseMin      { get; set; }
    [JsonPropertyName("pulse_max")]      public int    PulseMax      { get; set; }
    [JsonPropertyName("hemoglobin_min")] public double HemoglobinMin { get; set; }
}
```

![Атрибути JSON та JsonSerializerOptions](_assets/18-06/json-attributes.png)
