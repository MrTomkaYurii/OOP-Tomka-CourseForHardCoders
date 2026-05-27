---
chapter: 18
chapterTitle: "Розділ 18. Робота з файловою системою"
section: 3
number: "18.3"
title: "Stream та FileStream. Потоковий доступ до файлів"
source: ""
---

## 18.3. Stream та FileStream. Потоковий доступ до файлів

Усі класи `File.WriteAllText`, `File.ReadAllBytes` — це зручні обгортки над нижчим рівнем абстракції: **потоками (streams)**. Потік — це абстракція послідовного доступу до даних, де читання або запис відбуваються **по шматках (chunk by chunk)**, а не завантаженням усього ресурсу у пам'ять одразу. Розуміння потоків є фундаментом для роботи не лише з файлами, а й з мережевими з'єднаннями, ZIP-архівами, HTTP-відповідями, шифруванням — будь-яким I/O у .NET.

Абстрактний клас `Stream` визначає єдиний контракт для всіх видів потоків. `FileStream` — одна з конкретних реалізацій, що забезпечує потоковий доступ до файлів на диску.

![Ієрархія класів Stream у .NET](_assets/18-03/stream-class-hierarchy.png)

## Абстрактний клас Stream

`Stream` (простір імен `System.IO`) визначає мінімальний набір можливостей, якими може володіти або не володіти потік:

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "stream_demo.bin");

// Запишемо щось через FileStream, щоб мати що читати
File.WriteAllText(path, "MED-DATA-2024", Encoding.ASCII);

// Відкриваємо через абстрактний тип Stream
using Stream stream = File.OpenRead(path);

// Три фундаментальні властивості потоку
Console.WriteLine($"CanRead:   {stream.CanRead.ToString()}");    // чи можна читати
Console.WriteLine($"CanWrite:  {stream.CanWrite.ToString()}");   // чи можна записувати
Console.WriteLine($"CanSeek:   {stream.CanSeek.ToString()}");    // чи підтримує позиціонування

// Позиціонування — доступне лише якщо CanSeek == true
Console.WriteLine($"Length:    {stream.Length.ToString()} байт");
Console.WriteLine($"Position:  {stream.Position.ToString()} (початок)");

// Читання у буфер
byte[] buffer = new byte[4];
int read = stream.Read(buffer, 0, buffer.Length);
Console.WriteLine($"Прочитано: {read.ToString()} байт: {Encoding.ASCII.GetString(buffer, 0, read)}");
Console.WriteLine($"Position після Read: {stream.Position.ToString()}");

// Seek — переміщення позиції
stream.Seek(4, SeekOrigin.Begin);   // з початку на 4
Console.WriteLine($"Після Seek(4, Begin): Position={stream.Position.ToString()}");

stream.Seek(-2, SeekOrigin.End);    // від кінця на -2
Console.WriteLine($"Після Seek(-2, End):  Position={stream.Position.ToString()}");

stream.Seek(2, SeekOrigin.Current); // від поточної позиції
Console.WriteLine($"Після Seek(2, Current): Position={stream.Position.ToString()}");

File.Delete(path);
```

`Stream` визначає три типи операцій: **читання** (`Read`, `ReadByte`), **запис** (`Write`, `WriteByte`, `Flush`) і **позиціонування** (`Seek`, `Position`). Не всі потоки підтримують усі операції — мережевий потік `NetworkStream` не підтримує `Seek` (`CanSeek == false`), потік лише для читання не підтримує `Write`. Перевіряйте `CanRead`/`CanWrite`/`CanSeek` перед використанням.

## Клас FileStream

`FileStream` — реалізація `Stream` для файлів на диску. Він підтримує всі три операції: читання, запис і позиціонування (`CanSeek == true`).

### Відкриття файлу: FileMode та FileAccess

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "filestream_test.bin");

// Варіант 1: через конструктор FileStream
// FileMode: Create, CreateNew, Open, OpenOrCreate, Append, Truncate
// FileAccess: Read, Write, ReadWrite
using (FileStream fs = new FileStream(path, FileMode.Create, FileAccess.Write))
{
    Console.WriteLine($"Відкрито для запису. CanWrite: {fs.CanWrite.ToString()}");
    byte[] data = Encoding.UTF8.GetBytes("PATIENT-DATA-001");
    fs.Write(data, 0, data.Length);
    Console.WriteLine($"Записано {data.Length.ToString()} байт");
} // using закриває потік і звільняє ресурс

// Варіант 2: через статичний File (зручніший синтаксис)
using (FileStream fs = File.Open(path, FileMode.Open, FileAccess.Read))
{
    byte[] buf = new byte[fs.Length];
    int n = fs.Read(buf, 0, buf.Length);
    Console.WriteLine($"Прочитано {n.ToString()} байт: {Encoding.UTF8.GetString(buf)}");
}

// Варіант 3: через FileInfo
FileInfo fi = new FileInfo(path);
using (FileStream fs = fi.Open(FileMode.Open, FileAccess.ReadWrite))
{
    fs.Seek(8, SeekOrigin.Begin); // переходимо до "001"
    byte[] patch = Encoding.ASCII.GetBytes("007");
    fs.Write(patch, 0, patch.Length);
    
    fs.Seek(0, SeekOrigin.Begin);
    byte[] result = new byte[fs.Length];
    fs.Read(result, 0, result.Length);
    Console.WriteLine($"Після патчу: {Encoding.UTF8.GetString(result)}");
}

File.Delete(path);
```

**FileMode** визначає, що відбувається при відкритті:

| FileMode | Якщо файл існує | Якщо файл не існує |
|---|---|---|
| `Create` | Обрізає до нуля | Створює новий |
| `CreateNew` | Кидає IOException | Створює новий |
| `Open` | Відкриває | Кидає FileNotFoundException |
| `OpenOrCreate` | Відкриває | Створює новий |
| `Append` | Відкриває, позиція в кінці | Створює новий |
| `Truncate` | Обрізає до нуля | Кидає FileNotFoundException |

### Буферизований запис та Flush

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "buffered_write.txt");

// Варіант 4: з явним розміром буфера
// FileStream внутрішньо буферизує запис — дані спочатку потрапляють у буфер
using (FileStream fs = new FileStream(path, FileMode.Create, FileAccess.Write, FileShare.None, bufferSize: 4096))
{
    string header = "=== Медичний журнал 2024 ===\n";
    byte[] headerBytes = Encoding.UTF8.GetBytes(header);
    fs.Write(headerBytes, 0, headerBytes.Length);
    Console.WriteLine($"Після Write: Position={fs.Position.ToString()}");
    
    // Flush — примусово скидає буфер на диск
    // Без Flush дані можуть ще бути у буфері при краші
    fs.Flush();
    Console.WriteLine("Flush виконано — дані гарантовано на диску");
    
    string entry = $"[{DateTime.Now:HH:mm:ss}] Прийом: Петренко І.О.\n";
    byte[] entryBytes = Encoding.UTF8.GetBytes(entry);
    fs.Write(entryBytes, 0, entryBytes.Length);
}
// При виході з using: Dispose() → Flush() → Close() — автоматично

string content = File.ReadAllText(path, Encoding.UTF8);
Console.WriteLine($"Вміст файлу:\n{content}");
File.Delete(path);
```

`Flush()` гарантує, що буферизовані дані записані на фізичний диск. Для критичних даних (медичні журнали, транзакції) — викликайте `Flush()` після кожного запису. При звичайних ситуаціях `using` / `Dispose` автоматично виконає `Flush` і `Close`.

### Паралельний доступ: FileShare

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "shared_log.txt");
File.WriteAllText(path, "Початковий вміст\n", Encoding.UTF8);

// FileShare.Read — дозволяє іншим процесам читати, поки ми пишемо
using FileStream fs1 = new FileStream(path, FileMode.Append, FileAccess.Write, FileShare.Read);
fs1.Write(Encoding.UTF8.GetBytes("Запис 1 від процесу A\n"));

// FileShare.ReadWrite — дозволяє і читання, і запис
using FileStream fs2 = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
byte[] buf = new byte[fs2.Length];
fs2.Read(buf, 0, buf.Length);
Console.WriteLine($"Паралельне читання:\n{Encoding.UTF8.GetString(buf)}");

// Важливо: FileShare.None = виключний доступ (іншим забороняється відкривати файл)
Console.WriteLine("FileShare.None = монопольний доступ (інші отримають IOException)");

File.Delete(path);
```

`FileShare` визначає, що дозволяється іншим процесам (або потокам) робити з файлом, поки він відкритий у вас:

| FileShare | Опис |
|---|---|
| `None` | Виключний доступ — ніхто інший не може відкрити файл |
| `Read` | Інші можуть відкривати для читання |
| `Write` | Інші можуть відкривати для запису |
| `ReadWrite` | Інші можуть відкривати для читання і запису |
| `Delete` | Інші можуть видаляти файл |

### Читання та запис по шматках — ефективна обробка великих файлів

Ключова перевага потокового доступу — обробка файлів будь-якого розміру при константному використанні пам'яті:

```csharp run
using System;
using System.IO;
using System.Text;

string srcPath  = Path.Combine(Path.GetTempPath(), "large_medical_data.bin");
string dstPath  = Path.Combine(Path.GetTempPath(), "large_medical_copy.bin");

// Генеруємо тестовий файл ~50 KB
using (FileStream gen = new FileStream(srcPath, FileMode.Create))
{
    byte[] chunk = new byte[1024];
    for (int i = 0; i < 50; i++)
    {
        // Заповнюємо імітаційними медичними даними
        for (int j = 0; j < chunk.Length; j++)
            chunk[j] = (byte)((i * 7 + j * 3) % 256);
        gen.Write(chunk, 0, chunk.Length);
    }
}

FileInfo srcFi = new FileInfo(srcPath);
Console.WriteLine($"Джерело: {srcFi.Length.ToString()} байт");

// Копіювання по шматках — використовує лише 4 KB пам'яті незалежно від розміру файлу
const int BUFFER_SIZE = 4096;
byte[] buffer = new byte[BUFFER_SIZE];
int totalCopied = 0;

using FileStream src = File.OpenRead(srcPath);
using FileStream dst = File.Create(dstPath);

int bytesRead;
while ((bytesRead = src.Read(buffer, 0, buffer.Length)) > 0)
{
    dst.Write(buffer, 0, bytesRead);
    totalCopied += bytesRead;
}

Console.WriteLine($"Скопійовано: {totalCopied.ToString()} байт");
Console.WriteLine($"Файли ідентичні: {(new FileInfo(dstPath).Length == srcFi.Length).ToString()}");

// Альтернатива: Stream.CopyTo — вбудований метод копіювання між потоками
using FileStream src2 = File.OpenRead(srcPath);
using FileStream dst2 = File.Create(dstPath);
src2.CopyTo(dst2, bufferSize: 4096);
Console.WriteLine("CopyTo: теж по шматках, теж ефективно");

File.Delete(srcPath);
File.Delete(dstPath);
```

`Stream.CopyTo(Stream destination, int bufferSize)` — вбудований метод для копіювання між будь-якими потоками: з файлу у файл, з файлу у мережу, з HTTP-відповіді у файл. Внутрішньо він теж читає по шматках вказаного розміру.

### Seekable потік: довільний доступ до даних

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "indexed_records.bin");

// Запишемо 5 «записів» фіксованого розміру (32 байти кожен)
const int RECORD_SIZE = 32;
string[] patients = { "Коваль М.А.    ", "Бойко О.П.     ", "Мороз В.І.     ",
                       "Петренко І.О.  ", "Руденко С.В.   " };

using (FileStream fs = new FileStream(path, FileMode.Create))
{
    foreach (string p in patients)
    {
        byte[] record = new byte[RECORD_SIZE];
        byte[] nameBytes = Encoding.UTF8.GetBytes(p.PadRight(RECORD_SIZE));
        Array.Copy(nameBytes, record, Math.Min(nameBytes.Length, RECORD_SIZE));
        fs.Write(record, 0, RECORD_SIZE);
    }
}

// Довільне читання: записи 4-й (індекс 3)
using (FileStream fs = new FileStream(path, FileMode.Open, FileAccess.Read))
{
    int targetIndex = 3;
    long offset = (long)targetIndex * RECORD_SIZE;
    
    fs.Seek(offset, SeekOrigin.Begin);
    byte[] buf = new byte[RECORD_SIZE];
    fs.Read(buf, 0, RECORD_SIZE);
    
    Console.WriteLine($"Запис #{targetIndex.ToString()}: {Encoding.UTF8.GetString(buf).Trim()}");
    Console.WriteLine($"Прочитано без перебору {targetIndex.ToString()} попередніх записів — O(1) доступ");
}

File.Delete(path);
```

Файлові потоки (`CanSeek == true`) підтримують **довільний доступ** — стрибок до будь-якої позиції за O(1). Це основа для баз даних фіксованих записів, індексних структур і форматів з заголовками.

## MemoryStream — потік у пам'яті

`MemoryStream` реалізує `Stream` над масивом байтів у пам'яті. Не звертається до диску, але реалізує той самий інтерфейс. Корисний для тестування (замість реальних файлів), серіалізації у пам'яті та конвеєрів обробки:

```csharp run
using System;
using System.IO;
using System.Text;

// MemoryStream — Stream у RAM
using MemoryStream ms = new MemoryStream();

// Записуємо у пам'ять через StreamWriter (текстовий запис у потік)
using (StreamWriter sw = new StreamWriter(ms, Encoding.UTF8, leaveOpen: true))
{
    sw.WriteLine("Пацієнт: Петренко І.О.");
    sw.WriteLine("Діагноз: J06.9");
    sw.Flush();
}

Console.WriteLine($"MemoryStream.Length = {ms.Length.ToString()} байт");

// Читаємо назад
ms.Seek(0, SeekOrigin.Begin);
using (StreamReader sr = new StreamReader(ms, Encoding.UTF8))
{
    Console.WriteLine("Вміст MemoryStream:");
    Console.WriteLine(sr.ReadToEnd());
}

// Отримати весь масив байтів
byte[] bytes = ms.ToArray();
Console.WriteLine($"ToArray(): {bytes.Length.ToString()} байт");

// Корисний паттерн: обробити у пам'яті, потім зберегти на диск
string outputPath = Path.Combine(Path.GetTempPath(), "from_memory.txt");
File.WriteAllBytes(outputPath, bytes);
Console.WriteLine($"Збережено на диск: {outputPath}");
File.Delete(outputPath);
```

`leaveOpen: true` у конструкторі `StreamWriter` — важливий параметр: без нього `StreamWriter.Dispose()` закриє і `MemoryStream`, і ми не зможемо прочитати дані після `using`-блоку.

## Практичний сценарій: журнал медичних подій з FileStream

```csharp run
using System;
using System.IO;
using System.Text;

// Бінарний журнал: кожен запис — фіксованого розміру
// Формат: [timestamp:8 байт][patientId:16 байт][eventCode:4 байт][checksum:4 байт] = 32 байти

string logPath = Path.Combine(Path.GetTempPath(), "medical_events.log");
const int ENTRY_SIZE = 32;

// Запис події
void LogEvent(FileStream log, long patientId, int eventCode)
{
    byte[] entry = new byte[ENTRY_SIZE];
    long ts = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
    
    BitConverter.TryWriteBytes(entry.AsSpan(0,  8), ts);
    BitConverter.TryWriteBytes(entry.AsSpan(8,  8), patientId);
    BitConverter.TryWriteBytes(entry.AsSpan(16, 4), eventCode);
    
    int checksum = 0;
    for (int i = 0; i < 20; i++) checksum += entry[i];
    BitConverter.TryWriteBytes(entry.AsSpan(20, 4), checksum);
    
    log.Write(entry, 0, ENTRY_SIZE);
    log.Flush(); // Кожна подія одразу на диску
}

// Зберігаємо кілька подій
using (FileStream log = new FileStream(logPath, FileMode.Create, FileAccess.Write, FileShare.Read))
{
    LogEvent(log, 1001L, 0x01); // пацієнт 1001, подія "прийом"
    LogEvent(log, 1002L, 0x01);
    LogEvent(log, 1001L, 0x02); // пацієнт 1001, подія "виписка"
    LogEvent(log, 1003L, 0x01);
}

// Читання журналу
FileInfo logFi = new FileInfo(logPath);
int entryCount = (int)(logFi.Length / ENTRY_SIZE);
Console.WriteLine($"Журнал: {entryCount.ToString()} записів, {logFi.Length.ToString()} байт");

using (FileStream log = File.OpenRead(logPath))
{
    byte[] entry = new byte[ENTRY_SIZE];
    for (int i = 0; i < entryCount; i++)
    {
        log.Read(entry, 0, ENTRY_SIZE);
        long ts        = BitConverter.ToInt64(entry, 0);
        long patientId = BitConverter.ToInt64(entry, 8);
        int  eventCode = BitConverter.ToInt32(entry, 16);
        int  checksum  = BitConverter.ToInt32(entry, 20);
        
        string evtName = eventCode == 1 ? "прийом" : "виписка";
        Console.WriteLine($"  [{i.ToString()}] pid={patientId.ToString()}, подія={evtName}, ts={ts.ToString()}");
    }
}

File.Delete(logPath);
```

![FileMode та FileAccess — параметри відкриття файлу](_assets/18-03/filemode-fileaccess.png)
