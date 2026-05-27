---
chapter: 18
chapterTitle: "Розділ 18. Робота з файловою системою"
section: 2
number: "18.2"
title: "Класи FileInfo та DirectoryInfo"
source: ""
---

## 18.2. Класи FileInfo та DirectoryInfo

У розділі 18.1 ми розглянули статичні класи `Path`, `File` та `Directory`, кожен з яких виконує операцію атомарно: відкрив → зробив → закрив. Це зручно для разових дій, але неефективно, коли потрібно виконати кілька операцій над одним і тим самим ресурсом. Саме для таких сценаріїв C# надає **об'єктні аналоги** — класи `FileInfo` та `DirectoryInfo`.

На відміну від статичних класів, `FileInfo` і `DirectoryInfo` — **екземплярні класи**: ви створюєте об'єкт, що представляє конкретний файл або директорію, і далі вся робота відбувається через цей об'єкт. Ключова перевага — **безпека і одноразова авторизація**: при першому зверненні операційна система перевіряє права доступу один раз, результат кешується в об'єкті, і всі подальші операції не повторюють цю перевірку.

![Статичні vs екземплярні класи файлової системи](_assets/18-02/static-vs-instance.png)

## Клас FileInfo — об'єктне представлення файлу

`FileInfo` надає той самий набір операцій, що і статичний `File`, але через інтерфейс об'єкта: метадані файлу зберігаються у властивостях, а операції викликаються як методи екземпляра.

### Створення об'єкта та властивості

```csharp run
using System;
using System.IO;

// Визначаємо шлях до файлу
string path = Path.Combine(Path.GetTempPath(), "patient_card_001.txt");

// Записуємо тестовий файл
File.WriteAllText(path,
    "Пацієнт: Петренко Іван Олексійович\n" +
    "Дата народження: 15.03.1978\n" +
    "Діагноз: J06.9 — ГРВІ\n" +
    "Лікар: Коваленко О.П.");

// Створюємо FileInfo — об'єкт ще не звертається до диску при конструюванні
FileInfo fi = new FileInfo(path);

// Властивості — більшість звертаються до диску при першому зверненні
Console.WriteLine($"Існує:           {fi.Exists.ToString()}");
Console.WriteLine($"Ім'я:            {fi.Name}");
Console.WriteLine($"Ім'я без розш.:  {fi.Directory?.Name}");
Console.WriteLine($"Повний шлях:     {fi.FullName}");
Console.WriteLine($"Розширення:      {fi.Extension}");
Console.WriteLine($"Розмір (байт):   {fi.Length.ToString()}");
Console.WriteLine($"Тека:            {fi.DirectoryName}");
Console.WriteLine($"Тільки читання:  {fi.IsReadOnly.ToString()}");
Console.WriteLine($"Створено:        {fi.CreationTime:yyyy-MM-dd HH:mm:ss}");
Console.WriteLine($"Змінено:         {fi.LastWriteTime:yyyy-MM-dd HH:mm:ss}");
Console.WriteLine($"Відкрито:        {fi.LastAccessTime:yyyy-MM-dd HH:mm:ss}");

File.Delete(path);
```

### Методи FileInfo — операції над файлом

```csharp run
using System;
using System.IO;
using System.Text;

string srcPath  = Path.Combine(Path.GetTempPath(), "med_record.txt");
string copyPath = Path.Combine(Path.GetTempPath(), "med_record_backup.txt");
string movePath = Path.Combine(Path.GetTempPath(), "archive", "med_record_final.txt");

File.WriteAllText(srcPath, "Медична картка #007: Бойко Оксана Петрівна", Encoding.UTF8);
Directory.CreateDirectory(Path.GetDirectoryName(movePath)!);

FileInfo fi = new FileInfo(srcPath);

// Читання через OpenText — повертає StreamReader
using (StreamReader reader = fi.OpenText())
{
    Console.WriteLine($"Вміст: {reader.ReadToEnd()}");
}

// Копіювання — повертає FileInfo копії
FileInfo copyFi = fi.CopyTo(copyPath, overwrite: true);
Console.WriteLine($"Копія: {copyFi.FullName} ({copyFi.Length.ToString()} байт)");

// Переміщення
fi.MoveTo(movePath, overwrite: true);
Console.WriteLine($"Переміщено: {fi.FullName}"); // fi.FullName тепер вказує на нове місце

// Перейменування — це MoveTo у тій самій теці
FileInfo movedFi = new FileInfo(movePath);
movedFi.MoveTo(Path.Combine(Path.GetDirectoryName(movePath)!, "med_record_renamed.txt"));
Console.WriteLine($"Перейменовано: {movedFi.Name}");

// Видалення
movedFi.Delete();
copyFi.Delete();
Directory.Delete(Path.GetDirectoryName(movePath)!, recursive: true);
Console.WriteLine("Тимчасові файли прибрано");
```

`fi.MoveTo(...)` оновлює внутрішній стан об'єкта — після виклику `fi.FullName` і `fi.Name` відображають нове розташування файлу. Це суттєва відмінність від статичного `File.Move`, після якого ви маєте будувати новий шлях вручну.

### Відкриття потоків через FileInfo

`FileInfo` надає методи для відкриття різних видів потоків — це зручно, коли потрібен потоковий доступ замість атомарного читання/запису:

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "stream_test.txt");
File.WriteAllText(path, "Рядок 1\nРядок 2\nРядок 3", Encoding.UTF8);

FileInfo fi = new FileInfo(path);

// OpenRead — відкриває FileStream тільки для читання
using (FileStream fs = fi.OpenRead())
{
    Console.WriteLine($"FileStream: {fs.CanRead} / CanWrite: {fs.CanWrite.ToString()}");
    Console.WriteLine($"Розмір потоку: {fs.Length.ToString()} байт");
}

// OpenText — відкриває StreamReader (текстовий)
using (StreamReader sr = fi.OpenText())
{
    string? line;
    int lineNum = 1;
    while ((line = sr.ReadLine()) != null)
        Console.WriteLine($"  [{lineNum++.ToString()}] {line}");
}

// AppendText — відкриває StreamWriter у режимі дозапису
using (StreamWriter sw = fi.AppendText())
{
    sw.WriteLine($"Рядок додано: {DateTime.Now:HH:mm:ss}");
}

// Перевіряємо
Console.WriteLine($"Після дозапису: {fi.Length.ToString()} байт"); 
// Увага: fi.Length кешовано — потрібен Refresh()
fi.Refresh(); // оновлюємо кешовані метадані
Console.WriteLine($"Після Refresh(): {fi.Length.ToString()} байт");

fi.Delete();
```

`fi.Refresh()` — важливий метод: `FileInfo` кешує метадані (розмір, час змін) при першому зверненні. Якщо файл змінився після створення об'єкта, кешовані дані застаріють. Виклик `Refresh()` примусово перечитує метадані з диску.

## Клас DirectoryInfo — об'єктне представлення директорії

`DirectoryInfo` — об'єктний аналог статичного `Directory`. Представляє конкретну директорію і надає методи для роботи з нею та її вмістом через інтерфейс об'єкта.

### Властивості та методи

```csharp run
using System;
using System.IO;

string dirPath = Path.Combine(Path.GetTempPath(), "MedClinic_2024");
Directory.CreateDirectory(Path.Combine(dirPath, "Cardiology"));
Directory.CreateDirectory(Path.Combine(dirPath, "Neurology"));
File.WriteAllText(Path.Combine(dirPath, "index.txt"), "Клінічний архів 2024");
File.WriteAllText(Path.Combine(dirPath, "Cardiology", "pt001.txt"), "Петренко І.О.");
File.WriteAllText(Path.Combine(dirPath, "Cardiology", "pt002.txt"), "Коваль М.А.");

DirectoryInfo di = new DirectoryInfo(dirPath);

// Властивості
Console.WriteLine($"Існує:         {di.Exists.ToString()}");
Console.WriteLine($"Ім'я:          {di.Name}");
Console.WriteLine($"Повний шлях:   {di.FullName}");
Console.WriteLine($"Батьківська:   {di.Parent?.Name}");
Console.WriteLine($"Корінь:        {di.Root.FullName}");
Console.WriteLine($"Створено:      {di.CreationTime:yyyy-MM-dd HH:mm:ss}");

// Підтеки — GetDirectories() повертає DirectoryInfo[]
DirectoryInfo[] subdirs = di.GetDirectories();
Console.WriteLine($"\nПідтеки ({subdirs.Length.ToString()}):");
foreach (DirectoryInfo sub in subdirs)
    Console.WriteLine($"  [DIR]  {sub.Name}  ({sub.CreationTime:HH:mm:ss})");

// Файли — GetFiles() повертає FileInfo[]
FileInfo[] files = di.GetFiles("*.txt");
Console.WriteLine($"\nФайли .txt ({files.Length.ToString()}):");
foreach (FileInfo f in files)
    Console.WriteLine($"  [FILE] {f.Name}  {f.Length.ToString()} байт");

// Рекурсивний пошук
FileInfo[] allFiles = di.GetFiles("*.txt", SearchOption.AllDirectories);
Console.WriteLine($"\nВсі .txt рекурсивно ({allFiles.Length.ToString()}):");
foreach (FileInfo f in allFiles)
    Console.WriteLine($"  {f.FullName}");

di.Delete(recursive: true);
```

Ключова відмінність `DirectoryInfo.GetFiles()` від `Directory.GetFiles()`: перший повертає `FileInfo[]` — повноцінні об'єкти з метаданими (розмір, час, атрибути). Другий повертає лише `string[]` — масив рядків-шляхів. Якщо вам потрібні метадані файлів після переліку, `DirectoryInfo` економить один додатковий виклик на кожен файл.

### Створення ієрархії та навігація

```csharp run
using System;
using System.IO;

string root = Path.Combine(Path.GetTempPath(), "MedArchive");

// Створення ієрархії через DirectoryInfo
DirectoryInfo rootDi = new DirectoryInfo(root);
rootDi.Create(); // безпечно — не кидає при повторному викл.

DirectoryInfo year   = rootDi.CreateSubdirectory("2024");
DirectoryInfo cardio = year.CreateSubdirectory("Cardiology");
DirectoryInfo neuro  = year.CreateSubdirectory("Neurology");

// Додаємо файли через FileInfo від DirectoryInfo
string cardioFile = Path.Combine(cardio.FullName, "pt_reports.txt");
File.WriteAllText(cardioFile, "Звіти кардіологічного відділення");

// Навігація вверх по ієрархії через Parent
Console.WriteLine("Ієрархія від cardio вгору:");
DirectoryInfo? current = cardio;
while (current != null)
{
    Console.WriteLine($"  {current.FullName}");
    current = current.Parent;
}

// GetDirectories з SearchOption
Console.WriteLine($"\nВсі підтеки rootDi рекурсивно:");
foreach (DirectoryInfo d in rootDi.GetDirectories("*", SearchOption.AllDirectories))
    Console.WriteLine($"  {d.Name}");

rootDi.Delete(recursive: true);
```

`CreateSubdirectory` — метод, що повертає `DirectoryInfo` для щойно створеної підтеки. Це дозволяє будувати ієрархії тек у fluent-стилі, не будуючи шляхи вручну. Властивість `Parent` забезпечує навігацію вгору, `Root` — одразу до кореня.

## FileSystemInfo — спільний базовий клас

`FileInfo` і `DirectoryInfo` успадковують від абстрактного класу `FileSystemInfo`. Це дозволяє писати поліморфний код, що працює як з файлами, так і з директоріями:

```csharp run
using System;
using System.IO;

string root = Path.Combine(Path.GetTempPath(), "MedScan");
Directory.CreateDirectory(Path.Combine(root, "Reports"));
File.WriteAllText(Path.Combine(root, "index.txt"), "Індекс сканування");
File.WriteAllText(Path.Combine(root, "log.txt"), "Журнал операцій");

DirectoryInfo di = new DirectoryInfo(root);

// GetFileSystemInfos() повертає FileSystemInfo[] — суміш файлів і теок
FileSystemInfo[] entries = di.GetFileSystemInfos();
Console.WriteLine($"Всього записів: {entries.Length.ToString()}");

foreach (FileSystemInfo entry in entries)
{
    // Поліморфна обробка через is-перевірку
    if (entry is FileInfo fi)
    {
        Console.WriteLine($"  [FILE] {fi.Name}  {fi.Length.ToString()} байт  змінено: {fi.LastWriteTime:HH:mm:ss}");
    }
    else if (entry is DirectoryInfo subDir)
    {
        int fileCount = subDir.GetFiles().Length;
        Console.WriteLine($"  [DIR]  {subDir.Name}  ({fileCount.ToString()} файлів)  створено: {subDir.CreationTime:HH:mm:ss}");
    }
}

// Спільні властивості FileSystemInfo
Console.WriteLine("\nАтрибути через FileSystemInfo:");
foreach (FileSystemInfo entry in entries)
{
    Console.WriteLine($"  {entry.Name}: {entry.Attributes}");
}

di.Delete(recursive: true);
```

`FileSystemInfo` містить спільні властивості: `Name`, `FullName`, `Exists`, `CreationTime`, `LastWriteTime`, `LastAccessTime`, `Attributes`. Метод `GetFileSystemInfos()` повертає суміш `FileInfo` і `DirectoryInfo` об'єктів для всіх записів у теці.

## FileInfo vs File — порівняння підходів

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "compare_test.txt");
File.WriteAllText(path, "Тестовий вміст медичної картки пацієнта", Encoding.UTF8);

// --- Статичний File: зручно для разових операцій ---
// Кожен виклик: відкрити → дія → закрити → перевірити права
bool ex1  = File.Exists(path);
long len1 = new FileInfo(path).Length; // потрібен FileInfo для розміру
File.Copy(path, path + ".bak", overwrite: true);
File.Delete(path + ".bak");

// --- Екземплярний FileInfo: зручно для кількох операцій над тим самим файлом ---
// Права перевіряються один раз при першому зверненні
FileInfo fi = new FileInfo(path);
bool   ex2     = fi.Exists;      // перевірка прав і метадані — один раз
long   size    = fi.Length;      // вже кешовано
string ext     = fi.Extension;
DateTime mod   = fi.LastWriteTime;
FileInfo bakFi = fi.CopyTo(path + ".bak2", overwrite: true); // через об'єкт
bakFi.Delete();

Console.WriteLine($"Статичний: exists={ex1.ToString()}, size={len1.ToString()}");
Console.WriteLine($"Екземпляр: exists={ex2.ToString()}, size={size.ToString()}, ext={ext}, mod={mod:HH:mm:ss}");

fi.Delete();
```

**Правило вибору:**
- `File` / `Directory` — одна операція, результат не потрібен відразу, метадані не важливі
- `FileInfo` / `DirectoryInfo` — кілька операцій над тим самим ресурсом, або потрібні метадані файлу (розмір, час, атрибути)

## Практичний сценарій: аналіз архіву медичних записів

Об'єднаємо можливості `FileInfo` та `DirectoryInfo` у реальному сценарії — побудова зведеного звіту по архіву медичних записів:

```csharp run
using System;
using System.IO;
using System.Linq;
using System.Text;

// Створюємо тестову структуру архіву
string archive = Path.Combine(Path.GetTempPath(), "ClinicArchive");
Directory.CreateDirectory(Path.Combine(archive, "2023", "Cardiology"));
Directory.CreateDirectory(Path.Combine(archive, "2023", "Neurology"));
Directory.CreateDirectory(Path.Combine(archive, "2024", "Cardiology"));

// Генеруємо тестові файли
string[] files2023 = {
    Path.Combine(archive, "2023", "Cardiology", "pt001_report.pdf.txt"),
    Path.Combine(archive, "2023", "Cardiology", "pt002_ecg.pdf.txt"),
    Path.Combine(archive, "2023", "Neurology",  "pt003_mri.pdf.txt"),
};
string[] files2024 = {
    Path.Combine(archive, "2024", "Cardiology", "pt004_report.pdf.txt"),
    Path.Combine(archive, "2024", "Cardiology", "pt005_echo.pdf.txt"),
};

foreach (string f in files2023)
    File.WriteAllText(f, new string('X', 1024 + f.GetHashCode() % 512), Encoding.UTF8);
foreach (string f in files2024)
    File.WriteAllText(f, new string('X', 2048 + f.GetHashCode() % 1024), Encoding.UTF8);

// Аналіз через DirectoryInfo / FileInfo
DirectoryInfo archiveDi = new DirectoryInfo(archive);

Console.WriteLine($"=== Звіт архіву: {archiveDi.Name} ===\n");

foreach (DirectoryInfo yearDir in archiveDi.GetDirectories().OrderBy(d => d.Name))
{
    FileInfo[] yearFiles = yearDir.GetFiles("*.txt", SearchOption.AllDirectories);
    long totalSize = yearFiles.Sum(f => f.Length);
    
    Console.WriteLine($"Рік: {yearDir.Name}");
    Console.WriteLine($"  Файлів:      {yearFiles.Length.ToString()}");
    Console.WriteLine($"  Загальний розмір: {totalSize.ToString()} байт");
    
    // Топ-файл за розміром
    FileInfo? largest = yearFiles.OrderByDescending(f => f.Length).FirstOrDefault();
    if (largest != null)
        Console.WriteLine($"  Найбільший:  {largest.Name} ({largest.Length.ToString()} байт)");
    
    // Файли за підтеками
    foreach (DirectoryInfo deptDir in yearDir.GetDirectories())
    {
        FileInfo[] deptFiles = deptDir.GetFiles("*.txt");
        Console.WriteLine($"  [{deptDir.Name}] {deptFiles.Length.ToString()} файлів");
    }
    Console.WriteLine();
}

archiveDi.Delete(recursive: true);
```

![Властивості FileInfo та структура ієрархії](_assets/18-02/fileinfo-properties.png)
