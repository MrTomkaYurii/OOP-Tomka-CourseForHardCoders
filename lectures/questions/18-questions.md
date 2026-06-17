---
chapter: 18
chapterTitle: "Розділ 18. Файлова система та потоки"
type: self-assessment
---

# Питання для самоконтролю — Розділ 18. Файлова система та потоки

## 18.1. Path, File, Directory

1. Чим відрізняється `Path.Combine("C:\\data", "logs", "app.log")` від простої конкатенації рядків через `+`? Чому `Path.Combine` є кращим вибором у кросплатформних застосунках?

2. Розгляньте код:
   ```csharp
   string path = @"C:\projects\app\bin\Debug\app.exe";
   Console.WriteLine(Path.GetDirectoryName(path));
   Console.WriteLine(Path.GetFileNameWithoutExtension(path));
   Console.WriteLine(Path.GetExtension(path));
   ```
   Що виведе кожен рядок? Поясніть різницю між `GetFileName` і `GetFileNameWithoutExtension`.

3. Знайдіть помилку в наступному коді:
   ```csharp
   string dir = @"C:\reports\2024\january";
   if (!Directory.Exists(dir))
       Directory.CreateDirectory(dir);
   File.WriteAllText(dir + "report.txt", "data");
   ```
   Виправте її та поясніть, яка функція `Path` вирішує цю проблему.

4. Порівняйте `Directory.GetFiles()` і `Directory.EnumerateFiles()`. У якому сценарії `EnumerateFiles` матиме суттєву перевагу в продуктивності? Наведіть приклад такого сценарію.

5. Напишіть метод `CleanOldLogs(string folder, int daysOld)`, який видаляє з папки всі `.log` файли, що не змінювались більше `daysOld` днів. Використовуйте `File.GetLastWriteTime` і `Directory.EnumerateFiles`.

6. Що відбудеться при виклику `Directory.Delete(@"C:\mydir")`? Коли потрібен параметр `recursive: true`? Яка небезпека рекурсивного видалення?

7. Напишіть метод `EnsureBackupExists(string sourceFile)`, який копіює файл поряд з оригіналом з суфіксом `.bak`, але тільки якщо `.bak` ще не існує або старіший за оригінал.

## 18.2. FileInfo та DirectoryInfo

1. Яка принципова різниця між статичним класом `File` і класом `FileInfo`? Коли виправдано використовувати `FileInfo` замість `File.GetXxx()` методів?

2. Розгляньте код:
   ```csharp
   var fi = new FileInfo(@"C:\data\report.csv");
   Console.WriteLine(fi.Length);
   // ... зовнішній процес змінює файл ...
   Console.WriteLine(fi.Length);
   ```
   Чому другий `Console.WriteLine` може вивести хибне значення? Що треба зробити, щоб отримати актуальний розмір?

3. Поясніть концепцію кешування метаданих у `FileInfo`. Як це допомагає при роботі з багатьма операціями над одним файлом? Наведіть приклад коду, де `FileInfo` ефективніший за `File`.

4. Що таке `FileSystemInfo`? Яку роль він відіграє в ієрархії класів? Напишіть метод, що приймає `FileSystemInfo` і виводить ім'я та дату створення незалежно від того, файл це чи директорія.

5. Напишіть метод `GetLargestFiles(string directory, int count)`, що повертає `count` найбільших файлів у директорії (включно з вкладеними) у вигляді колекції `FileInfo`, відсортованих за спаданням розміру.

6. `DirectoryInfo.GetFileSystemInfos()` повертає `FileSystemInfo[]`. Чому це корисно? Напишіть код, що обходить директорію рекурсивно та виводить дерево файлів і папок з відступами відповідно до рівня вкладеності.

7. Порівняйте підходи: `new FileInfo(path).Exists` проти `File.Exists(path)`. Чи є між ними різниця в поведінці? Який з них кращий у циклі з 1000 перевірок одного й того самого файлу?

## 18.3. Stream та FileStream

1. Що таке абстрактний клас `Stream`? Назвіть три найважливіших властивості Stream та поясніть їх значення. Чому Stream є абстрактним, а не інтерфейсом?

2. Розгляньте код:
   ```csharp
   using var fs = new FileStream("data.bin", FileMode.Create);
   byte[] data = Encoding.UTF8.GetBytes("Hello");
   fs.Write(data, 0, data.Length);
   // програма завершується
   ```
   Що станеться з даними без явного `Flush()`? У яких умовах `using` гарантує збереження даних?

3. Поясніть різницю між `FileMode.Create`, `FileMode.CreateNew` і `FileMode.OpenOrCreate`. Наведіть конкретний сценарій, де помилковий вибір режиму призведе до втрати даних.

4. Навіщо потрібен параметр `FileShare`? Напишіть код, що відкриває файл журналу так, щоб кілька процесів могли читати його одночасно, але жоден не міг писати під час читання.

5. Реалізуйте метод `CopyStream(Stream source, Stream destination, int bufferSize)`, що копіює дані чанками вказаного розміру. Поясніть, чому порційне копіювання краще за `source.CopyTo(destination)` у деяких випадках.

6. Напишіть код, що використовує `Seek(offset, SeekOrigin)` для читання останніх 100 байт файлу без завантаження всього файлу в пам'ять. Поясніть значення `SeekOrigin.End`.

7. Що таке `MemoryStream`? Чим він відрізняється від `FileStream`? Поясніть параметр `leaveOpen` у контексті передачі `MemoryStream` в інший об'єкт.

8. Розгляньте сценарій: потрібно прочитати великий файл (2 ГБ), обробити дані та записати результат. Чому не варто використовувати `File.ReadAllBytes()`? Як правильно організувати обробку за допомогою `FileStream`?

## 18.4. StreamReader та StreamWriter

1. Чому `StreamReader` і `StreamWriter` називають "декораторами"? Який паттерн проєктування тут реалізовано? Намалюйте (текстово) ланцюжок об'єктів при читанні UTF-8 файлу.

2. Розгляньте код:
   ```csharp
   var writer = new StreamWriter("log.txt", append: true);
   writer.WriteLine("Entry 1");
   writer.WriteLine("Entry 2");
   // writer.Dispose() не викликається
   ```
   Що може статися з даними? Як `AutoFlush = true` змінює поведінку? Які його переваги та недоліки?

3. Напишіть метод `CountLinesInFile(string path)`, що підраховує кількість рядків у великому текстовому файлі (сотні мегабайт) без завантаження всього файлу в пам'ять. Чому `ReadLine()` кращий за `ReadToEnd()` у цьому випадку?

4. Що таке `StringReader` і `StringWriter`? Навіщо вони потрібні, якщо є `string`? Напишіть приклад використання `StringWriter` для тестування методу, що пише до `TextWriter`.

5. Поясніть різницю між `TextReader` і `StreamReader`. Де в реальному коді корисно приймати `TextReader` замість `StreamReader` як параметр методу?

6. Розгляньте код:
   ```csharp
   using var reader = new StreamReader("data.csv");
   while (!reader.EndOfStream)
   {
       string line = reader.ReadLine();
       ProcessLine(line);
   }
   ```
   Що поверне `reader.Peek()` на останньому рядку? Як `EndOfStream` пов'язаний з `Peek()`?

7. Напишіть метод `MergeCsvFiles(string[] inputPaths, string outputPath)`, що об'єднує кілька CSV файлів в один, зберігаючи заголовок тільки з першого файлу. Використовуйте `StreamReader` і `StreamWriter`.

## 18.5. BinaryReader та BinaryWriter

1. Чим принципово відрізняється двійковий формат від текстового при збереженні числа `3.14159265358979`? Скільки байт займає `double` у бінарному форматі проти текстового?

2. Розгляньте код запису:
   ```csharp
   using var bw = new BinaryWriter(File.Create("data.bin"));
   bw.Write(42);
   bw.Write("Hello");
   bw.Write(3.14f);
   bw.Write(true);
   ```
   Напишіть відповідний код читання. Що станеться, якщо читати у іншому порядку (спочатку `float`, потім `int`)?

3. Поясніть концепцію записів фіксованого розміру у бінарних файлах. Напишіть структуру `PatientRecord` (ID: int, вік: byte, вага: float) та методи для запису й читання масиву таких записів.

4. Як використати `Seek` у `FileStream` разом з `BinaryReader` для читання запису за індексом без перебору всього файлу? Обчисліть зміщення для читання запису з індексом `i`, якщо кожен запис займає 9 байт.

5. Порівняйте розмір файлу при збереженні 1000 чисел типу `double` у текстовому форматі (через `StreamWriter`) та бінарному (через `BinaryWriter`). Зробіть розрахунок та поясніть різницю.

6. Напишіть метод `UpdateRecord(string filePath, int index, float newWeight)`, що відкриває бінарний файл записів `PatientRecord` (ID: int, вік: byte, вага: float), знаходить запис за індексом та оновлює тільки поле ваги без переписування всього файлу.

7. Де бінарний формат є очевидним вибором, а де текстовий? Перелічіть 3 сценарії для кожного формату. Що таке ендіанність і чому вона важлива при обміні бінарними файлами між різними системами?

## 18.6. System.Text.Json

1. Що робить `JsonSerializer.Serialize(obj, new JsonSerializerOptions { WriteIndented = true })`? Коли доцільно використовувати `WriteIndented = false` у продуктивному середовищі?

2. Розгляньте клас:
   ```csharp
   public class Doctor
   {
       public string Name { get; set; }
       public string PasswordHash { get; set; }
       public DateTime CreatedAt { get; set; }
       public List<string> Roles { get; set; }
   }
   ```
   Як серіалізувати об'єкт так, щоб: поле `PasswordHash` не потрапило в JSON, `CreatedAt` стало `created_at` у camelCase, а `Roles` стало `permissions`? Використайте JSON атрибути.

3. Поясніть різницю між `JsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase` та атрибутом `[JsonPropertyName("name")]`. Який з них має пріоритет?

4. Що означає `DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull`? Напишіть код та покажіть вихідний JSON для об'єкта, де частина полів `null`.

5. Перерахуйте всі JSON атрибути, що вивчались у розділі (`[JsonPropertyName]`, `[JsonIgnore]` тощо). Для кожного наведіть короткий приклад використання та поясніть ефект.

6. Напишіть метод `SaveConfig<T>(T config, string path)` і `T LoadConfig<T>(string path)`, що зберігають і відновлюють конфігурацію з JSON файлу. Обробіть випадки, коли файл не існує або містить невалідний JSON.

7. Порівняйте `JsonSerializer.Serialize(obj)` (рядок) і `JsonSerializer.Serialize(stream, obj)` (в потік). Коли потокова версія є кращим вибором? Яка різниця в використанні пам'яті?

8. Що таке `JsonStringEnumConverter`? Без нього як серіалізується enum за замовчуванням? Напишіть приклад, де `JsonStringEnumConverter` зареєстрований глобально через `JsonSerializerOptions`.
