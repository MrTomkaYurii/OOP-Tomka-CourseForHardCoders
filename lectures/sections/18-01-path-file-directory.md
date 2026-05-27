---
chapter: 18
chapterTitle: "Розділ 18. Робота з файловою системою"
section: 1
number: "18.1"
title: "Класи Path, File та Directory"
source: ""
---

## 18.1. Класи Path, File та Directory

Файлова система — один із найважливіших механізмів збереження даних у будь-якому застосунку. Медична інформаційна система зберігає картки пацієнтів, результати аналізів, знімки, архіви журналів — усе це файли та теки на диску. C# надає потужний і зручний інструментарій для роботи з файловою системою через простір імен `System.IO`. Три основні статичні класи — `Path`, `File` та `Directory` — покривають переважну більшість сценаріїв: від складання шляхів і перевірки існування ресурсів до читання, запису та переміщення файлів.

## Клас Path — маніпуляції з рядками шляхів

`Path` — статичний клас, що надає методи для роботи з рядковим поданням шляхів файлової системи. Важлива особливість: `Path` **не звертається до диску взагалі** — він виключно обробляє рядки. Це робить його операції миттєвими і безпечними щодо винятків файлової системи.

```csharp run
using System;
using System.IO;

string filePath = @"C:\MedSystem\Patients\PT-2024\card_001.txt";

// Розбирання шляху на складові
Console.WriteLine($"Тека:              {Path.GetDirectoryName(filePath)}");
Console.WriteLine($"Ім'я файлу:        {Path.GetFileName(filePath)}");
Console.WriteLine($"Ім'я без розширення: {Path.GetFileNameWithoutExtension(filePath)}");
Console.WriteLine($"Розширення:        {Path.GetExtension(filePath)}");
Console.WriteLine($"Корінь шляху:      {Path.GetPathRoot(filePath)}");
```

Метод `Path.Combine` дозволяє об'єднувати частини шляху незалежно від операційної системи. Використання рядкової конкатенації (`dir + "\\" + file`) — поширена помилка: вона ламається на Linux/macOS, де роздільник — `/`. `Path.Combine` завжди підставляє правильний роздільник:

```csharp run
using System;
using System.IO;

string baseDir  = @"C:\MedSystem\Patients";
string patientId = "PT-2024-007";
string fileName  = "card.json";

// Правильно: Path.Combine
string fullPath = Path.Combine(baseDir, patientId, fileName);
Console.WriteLine($"Шлях: {fullPath}");

// Платформонезалежний роздільник
Console.WriteLine($"Роздільник:      {Path.DirectorySeparatorChar}");
Console.WriteLine($"Роздільник Alt:  {Path.AltDirectorySeparatorChar}");

// Тимчасова тека системи
Console.WriteLine($"Temp:            {Path.GetTempPath()}");

// Унікальне тимчасове ім'я файлу
Console.WriteLine($"Temp file:       {Path.GetTempFileName()}");
```

`Path.GetFullPath` перетворює відносний шлях на абсолютний — корисно при роботі з конфігурацією:

```csharp run
using System;
using System.IO;

// Відносний шлях → абсолютний (відносно поточної теки)
string relative = Path.Combine("data", "patients", "archive.json");
string absolute = Path.GetFullPath(relative);
Console.WriteLine($"Відносний: {relative}");
Console.WriteLine($"Абсолютний: {absolute}");

// Перевірка шляху на правильність
bool hasExtension = Path.HasExtension("report.pdf");
Console.WriteLine($"Має розширення: {hasExtension.ToString()}");
```

![Статичні класи файлової системи та анатомія шляху](_assets/18-01/static-classes-overview.png)

## Клас Directory — робота з теками

`Directory` — статичний клас для операцій над директоріями файлової системи: перевірки існування, створення, видалення, перебирання вмісту.

### Перевірка існування та створення

```csharp run
using System;
using System.IO;

string archiveDir = Path.Combine(Path.GetTempPath(), "MedArchive", "2024");

// Перевіряємо існування
if (!Directory.Exists(archiveDir))
{
    // CreateDirectory створює всі проміжні теки (аналог mkdir -p)
    Directory.CreateDirectory(archiveDir);
    Console.WriteLine($"Створено: {archiveDir}");
}
else
{
    Console.WriteLine($"Вже існує: {archiveDir}");
}

// Поточна тека
Console.WriteLine($"Поточна тека: {Directory.GetCurrentDirectory()}");
```

`Directory.CreateDirectory` безпечно ігнорує виклик, якщо тека вже існує — не кидає виняток при повторному створенні. Це дозволяє гарантувати існування потрібної структури теок перед записом файлів.

### Перебирання вмісту теки

```csharp run
using System;
using System.IO;

// Ство рюємо тестову структуру у temp
string root = Path.Combine(Path.GetTempPath(), "MedTest");
Directory.CreateDirectory(Path.Combine(root, "Cardiology"));
Directory.CreateDirectory(Path.Combine(root, "Neurology"));
File.WriteAllText(Path.Combine(root, "index.txt"), "Медичний архів 2024");
File.WriteAllText(Path.Combine(root, "Cardiology", "pt001.txt"), "Петренко І.О.");
File.WriteAllText(Path.Combine(root, "Cardiology", "pt002.txt"), "Коваль М.А.");

// Отримати всі теки
string[] dirs = Directory.GetDirectories(root);
Console.WriteLine($"Підтеки ({dirs.Length.ToString()}):");
foreach (string d in dirs)
    Console.WriteLine($"  [DIR] {Path.GetFileName(d)}");

// Отримати всі файли
string[] files = Directory.GetFiles(root, "*.txt");
Console.WriteLine($"\nФайли .txt ({files.Length.ToString()}):");
foreach (string f in files)
    Console.WriteLine($"  [FILE] {Path.GetFileName(f)}");

// Рекурсивний пошук по всій ієрархії
string[] allFiles = Directory.GetFiles(root, "pt*.txt", SearchOption.AllDirectories);
Console.WriteLine($"\nВсі файли пацієнтів ({allFiles.Length.ToString()}):");
foreach (string f in allFiles)
    Console.WriteLine($"  {f}");
```

### GetFiles vs EnumerateFiles

`GetFiles` повертає весь масив одразу — усі шляхи зчитуються у пам'ять перед поверненням. `EnumerateFiles` повертає `IEnumerable<string>` з ліниво обчисленим результатом — елементи надходять по одному в міру обходу. Для великих теок з тисячами файлів `EnumerateFiles` ефективніший — перший файл доступний без очікування завершення всього обходу:

```csharp run
using System;
using System.IO;
using System.Linq;

string root = Path.Combine(Path.GetTempPath(), "MedTest");
Directory.CreateDirectory(root);

// EnumerateFiles — лінивий обхід, зупиняємось на першому знайденому
string? firstPatient = Directory.EnumerateFiles(root, "pt*.txt", SearchOption.AllDirectories)
    .FirstOrDefault();

Console.WriteLine(firstPatient != null
    ? $"Перший файл пацієнта: {firstPatient}"
    : "Файлів не знайдено");
```

### Переміщення та видалення теки

```csharp run
using System;
using System.IO;

string src = Path.Combine(Path.GetTempPath(), "OldArchive");
string dst = Path.Combine(Path.GetTempPath(), "NewArchive");
Directory.CreateDirectory(src);
File.WriteAllText(Path.Combine(src, "log.txt"), "тест");

// Переміщення (перейменування) теки
Directory.Move(src, dst);
Console.WriteLine($"Переміщено: {src} → {dst}");

// Видалення: другий параметр true — рекурсивне видалення разом з вмістом
Directory.Delete(dst, recursive: true);
Console.WriteLine("Видалено разом з вмістом");
```

Без параметра `recursive: true` виклик `Delete` на непорожній теці кине `IOException`.

## Клас File — робота з файлами

`File` — статичний клас для атомарних операцій над файлами. «Атомарних» означає: кожен метод сам відкриває файл, виконує операцію і закриває. Це зручно для простих сценаріїв, де не потрібен потоковий доступ.

### Запис та читання тексту

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "patient_card.txt");

// Запис: створює файл або повністю перезаписує існуючий
string content = "Пацієнт: Петренко Іван Олексійович\n" +
                 "Дата народження: 15.03.1978\n" +
                 "Діагноз: J06.9 — ГРВІ\n" +
                 "Лікар: Коваленко О.П.";

File.WriteAllText(path, content, Encoding.UTF8);
Console.WriteLine($"Записано: {path}");

// Читання всього вмісту
string loaded = File.ReadAllText(path, Encoding.UTF8);
Console.WriteLine($"\n--- Вміст файлу ---\n{loaded}");

// Рядки — масив рядків (кожен рядок як окремий елемент)
string[] lines = File.ReadAllLines(path, Encoding.UTF8);
Console.WriteLine($"\nРядків: {lines.Length.ToString()}");
Console.WriteLine($"Перший рядок: {lines[0]}");
```

### Дозапис у кінець файлу

```csharp run
using System;
using System.IO;

string logPath = Path.Combine(Path.GetTempPath(), "clinic_log.txt");

// AppendAllText — дописує в кінець, не стирає існуючий вміст
File.AppendAllText(logPath, $"[{DateTime.Now:yyyy-MM-dd HH:mm}] Прийом: Бойко О.П.\n");
File.AppendAllText(logPath, $"[{DateTime.Now:yyyy-MM-dd HH:mm}] Прийом: Мороз В.І.\n");
File.AppendAllText(logPath, $"[{DateTime.Now:yyyy-MM-dd HH:mm}] Прийом: Сидоренко Т.К.\n");

string log = File.ReadAllText(logPath);
Console.WriteLine("Журнал прийомів:");
Console.WriteLine(log);
```

### Перевірка існування, копіювання, переміщення, видалення

```csharp run
using System;
using System.IO;

string src  = Path.Combine(Path.GetTempPath(), "original.txt");
string copy = Path.Combine(Path.GetTempPath(), "backup.txt");

File.WriteAllText(src, "Медична картка #001");

// Перевірка існування
Console.WriteLine($"Існує: {File.Exists(src).ToString()}");

// Копіювання: третій параметр overwrite
File.Copy(src, copy, overwrite: true);
Console.WriteLine($"Скопійовано до: {copy}");

// Інформація про файл
DateTime created  = File.GetCreationTime(src);
DateTime modified = File.GetLastWriteTime(src);
Console.WriteLine($"Створено:  {created:yyyy-MM-dd HH:mm:ss}");
Console.WriteLine($"Змінено:   {modified:yyyy-MM-dd HH:mm:ss}");

// Переміщення
string moved = Path.Combine(Path.GetTempPath(), "archive_001.txt");
File.Move(copy, moved, overwrite: true);
Console.WriteLine($"Переміщено: {moved}");

// Видалення
File.Delete(src);
File.Delete(moved);
Console.WriteLine("Тимчасові файли видалено");
```

### Читання/запис масиву байтів

Для бінарних даних `File.ReadAllBytes` і `File.WriteAllBytes` зчитують та записують весь файл як `byte[]`:

```csharp run
using System;
using System.IO;

string path = Path.Combine(Path.GetTempPath(), "binary_data.bin");

// Запис байтів (наприклад, результати вимірювань)
byte[] measurements = { 0x48, 0xB4, 0x00, 0x50, 0x00, 0x46 }; // hex-кодовані дані
File.WriteAllBytes(path, measurements);

// Читання назад
byte[] loaded = File.ReadAllBytes(path);
Console.WriteLine($"Прочитано {loaded.Length.ToString()} байт");
Console.Write("Байти: ");
foreach (byte b in loaded)
    Console.Write($"{b.ToString("X2")} ");
Console.WriteLine();

File.Delete(path);
```

## Path, File та Directory разом: реальний сценарій

Об'єднаємо всі три класи у типовому сценарії медичної системи — організація архіву результатів аналізів:

```csharp run
using System;
using System.IO;

// Структура архіву: MedArchive/{рік}/{місяць}/{пацієнт}.txt
string archiveRoot = Path.Combine(Path.GetTempPath(), "MedArchive");

void SaveLabResult(string patientId, string result)
{
    string year  = DateTime.Now.Year.ToString();
    string month = DateTime.Now.Month.ToString("D2");
    string dir   = Path.Combine(archiveRoot, year, month);

    // Гарантуємо існування ієрархії теок
    Directory.CreateDirectory(dir);

    string fileName = $"{patientId}_{DateTime.Now:yyyyMMdd_HHmmss}.txt";
    string filePath = Path.Combine(dir, fileName);

    File.WriteAllText(filePath, result);
    Console.WriteLine($"Збережено: {filePath}");
}

string LoadLatestResult(string patientId)
{
    string year  = DateTime.Now.Year.ToString();
    string month = DateTime.Now.Month.ToString("D2");
    string dir   = Path.Combine(archiveRoot, year, month);

    if (!Directory.Exists(dir)) return "Архів порожній";

    // Знаходимо всі файли цього пацієнта і беремо найновіший
    string pattern = $"{patientId}_*.txt";
    string? latest = Directory.EnumerateFiles(dir, pattern)
        .OrderByDescending(f => f)
        .FirstOrDefault();

    return latest != null ? File.ReadAllText(latest) : "Результатів не знайдено";
}

// Зберігаємо кілька результатів
SaveLabResult("PT001", "Гемоглобін: 135 г/л — норма\nЛейкоцити: 6.2 — норма");
SaveLabResult("PT002", "Глюкоза: 7.8 ммоль/л — вище норми\nХолестерин: 5.1 — норма");
SaveLabResult("PT001", "Глюкоза: 4.9 ммоль/л — норма");

// Читаємо останній результат
Console.WriteLine($"\nОстанній результат PT001:\n{LoadLatestResult("PT001")}");

// Прибираємо тестові дані
if (Directory.Exists(archiveRoot))
    Directory.Delete(archiveRoot, recursive: true);
```

![Анатомія шляху файлової системи](_assets/18-01/path-anatomy.png)
