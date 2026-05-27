---
chapter: 18
chapterTitle: "Розділ 18. Робота з файловою системою"
section: 4
number: "18.4"
title: "StreamReader та StreamWriter. Текстові потоки"
source: ""
---

## 18.4. StreamReader та StreamWriter. Текстові потоки

`FileStream` із розділу 18.3 оперує **байтами** — він не знає нічого про текст, рядки, символи чи кодування. Якщо потрібно читати чи записувати текстові дані, щоразу виконувати ручне кодування/декодування байтів незручно і ненадійно. Саме для цього .NET надає `StreamReader` і `StreamWriter` — **текстові обгортки над потоком**, що прозоро обробляють кодування символів і надають зручний рядковий API.

Ключовий принцип: `StreamReader` / `StreamWriter` не є самостійними — вони **декорують** інший `Stream` (найчастіше `FileStream`). Це класичний патерн **Decorator**: обгортка додає нову поведінку (роботу з текстом), не змінюючи базову абстракцію потоку.

![Потік текстових даних: StreamReader та StreamWriter](_assets/18-04/text-stream-flow.png)

## StreamWriter — запис тексту у потік

`StreamWriter` перетворює рядки на байти з урахуванням кодування і записує їх у базовий потік.

### Базовий запис

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "patient_log.txt");

// Варіант 1: конструктор з рядком шляху (автоматично створює FileStream)
// Encoding.UTF8 — без BOM (Byte Order Mark). Для UTF-8 з BOM: new UTF8Encoding(encoderShouldEmitUTF8Identifier: true)
using (StreamWriter sw = new StreamWriter(path, append: false, encoding: Encoding.UTF8))
{
    sw.WriteLine("=== Журнал прийомів пацієнтів ===");
    sw.WriteLine($"Дата: {DateTime.Now:yyyy-MM-dd}");
    sw.WriteLine();
    sw.Write("Пацієнт: ");       // Write без переносу рядка
    sw.WriteLine("Петренко І.О."); // WriteLine додає Environment.NewLine
    sw.WriteLine($"Час: {DateTime.Now:HH:mm}");
}

// Варіант 2: обгортка над FileStream (більший контроль над потоком)
using (FileStream fs = new FileStream(path, FileMode.Append, FileAccess.Write))
using (StreamWriter sw = new StreamWriter(fs, Encoding.UTF8))
{
    sw.WriteLine();
    sw.WriteLine("--- Другий прийом ---");
    sw.WriteLine("Пацієнт: Бойко О.П.");
    sw.Flush(); // примусово скинути буфер на базовий потік
}

string result = File.ReadAllText(path, Encoding.UTF8);
Console.WriteLine(result);
File.Delete(path);
```

Другий параметр конструктора `append: false` — якщо `true`, файл відкривається у режимі дозапису. Фактично це визначає `FileMode`: `false` → `FileMode.Create`, `true` → `FileMode.Append`.

### AutoFlush та буферизація

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "clinic_events.log");

using StreamWriter sw = new StreamWriter(path, append: false, Encoding.UTF8);

// AutoFlush = true: кожен Write/WriteLine одразу передається у базовий потік
// Корисно для журналів, де важлива надійність запису
sw.AutoFlush = true;

for (int i = 1; i <= 4; i++)
{
    sw.WriteLine($"[{DateTime.Now:HH:mm:ss}] Подія #{i.ToString()}: {GetEventDescription(i)}");
    // З AutoFlush=true кожен рядок одразу на диску — не втратимо при краші
}

string GetEventDescription(int code) => code switch
{
    1 => "пацієнт зареєстрований",
    2 => "аналізи взяті",
    3 => "лікар призначений",
    _ => "виписка"
};

sw.Close(); // явний Close — аналог Dispose
Console.WriteLine(File.ReadAllText(path, Encoding.UTF8));
File.Delete(path);
```

За замовчуванням `AutoFlush = false` — дані накопичуються у внутрішньому буфері (зазвичай 4 KB) і записуються на диск при заповненні буфера або при `Flush()`/`Dispose()`. Для журналів подій де критична надійність встановлюйте `AutoFlush = true`.

### Кодування — як StreamWriter обробляє символи

```csharp run
using System;
using System.IO;
using System.Text;

string text = "Пацієнт: Петренко І.О. Діагноз: J06.9 — ГРВІ";

// Запишемо у різних кодуваннях
string utf8Path    = Path.Combine(Path.GetTempPath(), "enc_utf8.txt");
string utf16Path   = Path.Combine(Path.GetTempPath(), "enc_utf16.txt");
string asciiPath   = Path.Combine(Path.GetTempPath(), "enc_ascii.txt");

using (var sw = new StreamWriter(utf8Path,  false, Encoding.UTF8))    sw.WriteLine(text);
using (var sw = new StreamWriter(utf16Path, false, Encoding.Unicode)) sw.WriteLine(text);
using (var sw = new StreamWriter(asciiPath, false, Encoding.ASCII))   sw.WriteLine(text);

long utf8Size  = new FileInfo(utf8Path).Length;
long utf16Size = new FileInfo(utf16Path).Length;
long asciiSize = new FileInfo(asciiPath).Length;

Console.WriteLine($"UTF-8:   {utf8Size.ToString()} байт  (1-4 байти/символ, кирилиця = 2 байти)");
Console.WriteLine($"UTF-16:  {utf16Size.ToString()} байт  (2 байти/символ + 2-байтний BOM)");
Console.WriteLine($"ASCII:   {asciiSize.ToString()} байт  (кирилиця = '?' — не підтримується)");

// Читання ASCII-файлу покаже знаки питання для кирилиці
string asciiRead = File.ReadAllText(asciiPath, Encoding.ASCII);
Console.WriteLine($"ASCII читання: {asciiRead}");

foreach (string p in new[] { utf8Path, utf16Path, asciiPath })
    File.Delete(p);
```

**Рекомендація для нових застосунків**: завжди використовуйте `Encoding.UTF8` — це стандарт де-факто для текстових файлів у сучасних системах. `Encoding.UTF8` у .NET 5+ не додає BOM (Byte Order Mark) за замовчуванням, що сумісно з усіма платформами.

## StreamReader — читання тексту з потоку

`StreamReader` декодує байти з базового потоку у символи рядків. Надає методи для читання рядок за рядком, символ за символом або весь вміст одразу.

### Базове читання

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "medical_records.txt");
File.WriteAllText(path,
    "ID001|Петренко І.О.|J06.9|2024-03-15\n" +
    "ID002|Бойко О.П.|I10|2024-03-16\n" +
    "ID003|Коваль М.А.|E11.9|2024-03-17\n",
    Encoding.UTF8);

// Варіант 1: з рядком шляху
using (StreamReader sr = new StreamReader(path, Encoding.UTF8))
{
    // Метадані потоку
    Console.WriteLine($"CurrentEncoding: {sr.CurrentEncoding.EncodingName}");
    Console.WriteLine($"EndOfStream: {sr.EndOfStream.ToString()}");
    
    // Читання рядок за рядком
    string? line;
    int lineNum = 0;
    while ((line = sr.ReadLine()) != null)
    {
        lineNum++;
        string[] parts = line.Split('|');
        Console.WriteLine($"  [{lineNum.ToString()}] id={parts[0]}, пацієнт={parts[1]}, діагноз={parts[2]}");
    }
    
    Console.WriteLine($"EndOfStream після читання: {sr.EndOfStream.ToString()}");
}

File.Delete(path);
```

### Методи читання: ReadLine, Read, ReadToEnd, Peek

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "read_methods_test.txt");
File.WriteAllText(path, "ABCDE\nFGHIJ\nKLMNO", Encoding.UTF8);

// Показуємо всі 4 методи читання
using (StreamReader sr = new StreamReader(path, Encoding.UTF8))
{
    // Peek: дивиться на наступний символ БЕЗ просування позиції
    int nextChar = sr.Peek();
    Console.WriteLine($"Peek(): '{(char)nextChar}' (позиція не змінилась)");
    
    // Read(): читає один символ і просуває позицію
    char c = (char)sr.Read();
    Console.WriteLine($"Read(): '{c.ToString()}' (позиція +1)");
    
    // Read(buffer, index, count): читає N символів у масив
    char[] buf = new char[3];
    int read = sr.Read(buf, 0, buf.Length);
    Console.WriteLine($"Read(buf, 0, 3): '{new string(buf, 0, read)}' ({read.ToString()} символів)");
    
    // ReadLine(): читає до кінця рядка (без '\n')
    string? line = sr.ReadLine(); // пропуск залишку 1-го рядка
    Console.WriteLine($"ReadLine(): '{line}'");  // "E" (залишок після "ABCD")
    
    string? line2 = sr.ReadLine();
    Console.WriteLine($"ReadLine(): '{line2}'"); // "FGHIJ"
    
    // ReadToEnd(): читає все від поточної позиції до кінця
    string rest = sr.ReadToEnd();
    Console.WriteLine($"ReadToEnd(): '{rest}'"); // "KLMNO"
    
    Console.WriteLine($"EndOfStream: {sr.EndOfStream.ToString()}");
}

File.Delete(path);
```

`Peek()` — без споживання символу. Це дозволяє перевірити, чи є ще дані, перш ніж читати: `while (sr.Peek() != -1) { ... }`. Повертає `-1` на кінці потоку.

### Обробка великих файлів рядок за рядком

```csharp run
using System;
using System.IO;
using System.Text;

// Генеруємо великий тестовий файл — журнал пацієнтів
string logPath = Path.Combine(Path.GetTempPath(), "patients_log_large.txt");
using (StreamWriter gen = new StreamWriter(logPath, false, Encoding.UTF8))
{
    string[] diagnoses = { "J06.9", "I10", "E11.9", "K29.5", "M54.5" };
    for (int i = 1; i <= 1000; i++)
    {
        string date = DateTime.Now.AddMinutes(-i).ToString("yyyy-MM-dd HH:mm");
        string diag = diagnoses[i % diagnoses.Length];
        gen.WriteLine($"{date}|PT{i.ToString("D4")}|{diag}|Лікар #{(i % 10 + 1).ToString()}");
    }
}

FileInfo logFi = new FileInfo(logPath);
Console.WriteLine($"Файл: {logFi.Length.ToString()} байт, ~1000 записів");

// Агрегація без завантаження всього файлу у пам'ять
int total = 0, j069Count = 0, i10Count = 0;

using (StreamReader sr = new StreamReader(logPath, Encoding.UTF8))
{
    string? line;
    while ((line = sr.ReadLine()) != null)
    {
        total++;
        string[] parts = line.Split('|');
        if (parts.Length > 2)
        {
            if (parts[2] == "J06.9") j069Count++;
            if (parts[2] == "I10")   i10Count++;
        }
    }
}

Console.WriteLine($"Всього записів: {total.ToString()}");
Console.WriteLine($"J06.9 (ГРВІ): {j069Count.ToString()}");
Console.WriteLine($"I10 (гіпертонія): {i10Count.ToString()}");
Console.WriteLine("Файл оброблено рядок за рядком — пам'яті лише один рядок одночасно");

File.Delete(logPath);
```

`ReadLine()` — ідеальний вибір для обробки великих текстових файлів: тримає у пам'яті лише один рядок, обробляє гігабайтні файли без `OutOfMemoryException`.

## StringReader та StringWriter — потоки над рядком

`StringReader` і `StringWriter` реалізують той самий текстовий інтерфейс, що `StreamReader`/`StreamWriter`, але над `string` або `StringBuilder` у пам'яті. Корисні для тестування та обробки рядкових даних без файлів:

```csharp run
using System;
using System.IO;
using System.Text;

// StringWriter — запис у StringBuilder
var sb = new StringBuilder();
using (StringWriter sw = new StringWriter(sb))
{
    sw.WriteLine("Пацієнт: Бойко О.П.");
    sw.WriteLine("Вік: 45");
    sw.WriteLine($"Дата: {DateTime.Now:yyyy-MM-dd}");
}
Console.WriteLine("StringWriter результат:");
Console.WriteLine(sb.ToString());

// StringReader — читання з рядка рядок за рядком
string input = "ID001|Петренко|J06.9\nID002|Бойко|I10\nID003|Коваль|E11.9";
int count = 0;
using (StringReader sr = new StringReader(input))
{
    string? line;
    while ((line = sr.ReadLine()) != null)
    {
        count++;
        string[] parts = line.Split('|');
        Console.WriteLine($"  [{count.ToString()}] {parts[1]} — {parts[2]}");
    }
}

// Корисний патерн: той самий метод обробляє і файл, і рядок
void ProcessLines(TextReader reader)
{
    string? line;
    int n = 0;
    while ((line = reader.ReadLine()) != null)
        Console.WriteLine($"    обробка рядка {++n}: {line.Split('|')[0]}");
}

Console.WriteLine("\nОдин метод — різні джерела:");
using (StringReader sr = new StringReader(input)) ProcessLines(sr);  // рядок у пам'яті
// ProcessLines(new StreamReader(path));                               // файл на диску
```

`TextReader` і `TextWriter` — абстрактні базові класи для `StreamReader`/`StringReader` та `StreamWriter`/`StringWriter` відповідно. Код, написаний проти `TextReader`, однаково працює з файлом, рядком або будь-яким іншим текстовим джерелом.

## Практичний сценарій: CSV-парсинг медичних записів

```csharp run
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

// Структура запису лабораторного аналізу
record LabResult(string PatientId, string TestName, double Value, string Unit, string Status);

// CSV-файл з результатами аналізів
string csvPath = Path.Combine(Path.GetTempPath(), "lab_results.csv");
using (StreamWriter sw = new StreamWriter(csvPath, false, Encoding.UTF8))
{
    sw.WriteLine("patient_id,test_name,value,unit,status");
    sw.WriteLine("PT001,Гемоглобін,135.0,г/л,норма");
    sw.WriteLine("PT001,Лейкоцити,6.2,10^9/л,норма");
    sw.WriteLine("PT002,Глюкоза,7.8,ммоль/л,вище норми");
    sw.WriteLine("PT002,Холестерин,5.1,ммоль/л,норма");
    sw.WriteLine("PT003,Гемоглобін,98.0,г/л,нижче норми");
}

// Парсинг CSV
List<LabResult> ParseLabCsv(string path)
{
    var results = new List<LabResult>();
    using StreamReader sr = new StreamReader(path, Encoding.UTF8);
    
    string? header = sr.ReadLine(); // пропускаємо заголовок
    Console.WriteLine($"Заголовок: {header}");
    
    string? line;
    while ((line = sr.ReadLine()) != null)
    {
        if (string.IsNullOrWhiteSpace(line)) continue;
        
        string[] parts = line.Split(',');
        if (parts.Length < 5) continue;
        
        if (!double.TryParse(parts[2], System.Globalization.NumberStyles.Float,
            System.Globalization.CultureInfo.InvariantCulture, out double val))
            continue;
        
        results.Add(new LabResult(parts[0], parts[1], val, parts[3], parts[4]));
    }
    return results;
}

List<LabResult> results = ParseLabCsv(csvPath);
Console.WriteLine($"\nЗчитано {results.Count.ToString()} записів:");
foreach (LabResult r in results)
{
    string icon = r.Status == "норма" ? "[OK]" : "[!!]";
    Console.WriteLine($"  {icon} {r.PatientId} | {r.TestName}: {r.Value.ToString()} {r.Unit} — {r.Status}");
}

// Формуємо звіт — відхилення від норми
Console.WriteLine("\n--- Відхилення від норми ---");
foreach (LabResult r in results)
    if (r.Status != "норма")
        Console.WriteLine($"  {r.PatientId}: {r.TestName} = {r.Value.ToString()} {r.Unit} [{r.Status}]");

File.Delete(csvPath);
```

![Кодування символів у текстових потоках](_assets/18-04/encoding-comparison.png)
