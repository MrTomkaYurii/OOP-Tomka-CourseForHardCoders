---
chapter: 18
chapterTitle: "Розділ 18. Робота з файловою системою"
section: 5
number: "18.5"
title: "BinaryReader та BinaryWriter. Бінарні потоки"
source: ""
---

## 18.5. BinaryReader та BinaryWriter. Бінарні потоки

`StreamReader`/`StreamWriter` чудово підходять для текстових даних. Але медичні системи часто мають справу з даними зовсім іншої природи: показники датчиків — послідовності чисел з плаваючою комою, архіви кардіограм — тисячі 16-бітних відліків, медичні зображення — мільйони байтів з пікселями. Зберігати такі дані у текстовому форматі неефективно: рядок `"98.6"` займає 4 байти (символи), тоді як значення `float 98.6f` у бінарному форматі займає рівно 4 байти **і зчитується без конвертації**. Для роботи з типізованими бінарними даними C# надає `BinaryWriter` та `BinaryReader`.

`BinaryWriter` і `BinaryReader` — теж **декоратори над Stream** (як `StreamWriter`/`StreamReader`), але вони оперують не рядками, а C#-типами безпосередньо: `int`, `double`, `bool`, `string`, `byte[]`. Дані записуються у внутрішньому представленні .NET (little-endian для чисел) без будь-якого текстового кодування.

![Бінарний vs текстовий формат зберігання](_assets/18-05/binary-vs-text-storage.png)

## BinaryWriter — запис типізованих даних

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "patient_vitals.bin");

// BinaryWriter обгортає будь-який Stream
using (BinaryWriter bw = new BinaryWriter(File.Create(path), Encoding.UTF8))
{
    // Write() перевантажений для кожного примітивного типу
    bw.Write((int)1001);           // 4 байти — id пацієнта
    bw.Write("Петренко І.О.");     // string: довжина + UTF-8 байти
    bw.Write((byte)45);            // 1 байт — вік
    bw.Write(true);                // 1 байт — чи госпіталізований
    bw.Write(98.6f);               // 4 байти — температура (float)
    bw.Write(120.0 / 80.0);        // 8 байт — індекс АТ (double)
    bw.Write((short)72);           // 2 байти — пульс (short)
    
    // byte[] — записується з довжиною вперед
    byte[] ecgSample = { 0x12, 0x34, 0x56, 0x78, 0x9A };
    bw.Write(ecgSample.Length); // спочатку довжина
    bw.Write(ecgSample);         // потім дані
}

FileInfo fi = new FileInfo(path);
Console.WriteLine($"Бінарний файл: {fi.Length.ToString()} байт");

// Для порівняння: той самий пацієнт у текстовому CSV
string csv = "1001,Петренко І.О.,45,true,98.6,1.5,72,12345678A";
Console.WriteLine($"CSV рядок:     {Encoding.UTF8.GetByteCount(csv).ToString()} байт");

File.Delete(path);
```

Метод `Write` у `BinaryWriter` перевантажений для всіх примітивних типів C#: `bool`, `byte`, `sbyte`, `char`, `short`, `ushort`, `int`, `uint`, `long`, `ulong`, `float`, `double`, `decimal`, `string`, а також `byte[]` і `char[]`. Кожен тип записується у точній кількості байт свого розміру.

## BinaryReader — читання типізованих даних

```csharp run
using System;
using System.IO;
using System.Text;

string path = Path.Combine(Path.GetTempPath(), "vitals_demo.bin");

// Спочатку запишемо дані
using (BinaryWriter bw = new BinaryWriter(File.Create(path), Encoding.UTF8))
{
    bw.Write(1001);
    bw.Write("Петренко І.О.");
    bw.Write((byte)45);
    bw.Write(true);
    bw.Write(98.6f);
    bw.Write(120.0 / 80.0);
    bw.Write((short)72);
    byte[] ecg = { 0x12, 0x34, 0x56, 0x78, 0x9A };
    bw.Write(ecg.Length);
    bw.Write(ecg);
}

// Читаємо — ПОРЯДОК ЧИТАННЯ ПОВИНЕН ЗБІГАТИСЯ З ПОРЯДКОМ ЗАПИСУ
using (BinaryReader br = new BinaryReader(File.OpenRead(path), Encoding.UTF8))
{
    int    patientId  = br.ReadInt32();
    string name       = br.ReadString();
    byte   age        = br.ReadByte();
    bool   hospitalized = br.ReadBoolean();
    float  temp       = br.ReadSingle();    // float = Single
    double bpIndex    = br.ReadDouble();
    short  pulse      = br.ReadInt16();     // short = Int16
    int    ecgLength  = br.ReadInt32();
    byte[] ecgSample  = br.ReadBytes(ecgLength);
    
    Console.WriteLine($"ID:            {patientId.ToString()}");
    Console.WriteLine($"Ім'я:          {name}");
    Console.WriteLine($"Вік:           {age.ToString()}");
    Console.WriteLine($"Госпіт.:       {hospitalized.ToString()}");
    Console.WriteLine($"Температура:   {temp.ToString("F1")} °C");
    Console.WriteLine($"Індекс АТ:     {bpIndex.ToString("F3")}");
    Console.WriteLine($"Пульс:         {pulse.ToString()} уд/хв");
    Console.Write($"ЕКГ ({ecgLength.ToString()} байт): ");
    foreach (byte b in ecgSample) Console.Write($"{b.ToString("X2")} ");
    Console.WriteLine();
    
    // Перевірка: CanRead після кінця файлу
    Console.WriteLine($"\nПрочитано до кінця: {(br.BaseStream.Position == br.BaseStream.Length).ToString()}");
}

File.Delete(path);
```

**Критично важливо**: порядок читання методами (`ReadInt32`, `ReadString` тощо) повинен **точно відповідати** порядку запису методами `Write`. Якщо порядок порушений — прочитаємо «сміття» або отримаємо виняток. Бінарний формат — це неявна схема даних, яку потрібно явно документувати.

## BinaryReader — методи читання

```csharp run
using System;
using System.IO;

string path = Path.Combine(Path.GetTempPath(), "all_types.bin");

// Запис усіх основних типів
using (BinaryWriter bw = new BinaryWriter(File.Create(path)))
{
    bw.Write(true);         // bool   — 1 байт
    bw.Write((byte)255);    // byte   — 1 байт
    bw.Write((short)1000);  // short  — 2 байти
    bw.Write(42);           // int    — 4 байти
    bw.Write(100L);         // long   — 8 байт
    bw.Write(3.14f);        // float  — 4 байти
    bw.Write(2.718281828);  // double — 8 байт
    bw.Write('A');          // char   — 2 байти (Unicode)
    bw.Write("Hello");      // string — 1(len) + 5 байт
}

long fileSize = new FileInfo(path).Length;
Console.WriteLine($"Файл: {fileSize.ToString()} байт");

// Читання з відповідними методами
using (BinaryReader br = new BinaryReader(File.OpenRead(path)))
{
    Console.WriteLine($"bool:   {br.ReadBoolean().ToString()}  (1 байт)");
    Console.WriteLine($"byte:   {br.ReadByte().ToString()}  (1 байт)");
    Console.WriteLine($"short:  {br.ReadInt16().ToString()}  (2 байти)");
    Console.WriteLine($"int:    {br.ReadInt32().ToString()}  (4 байти)");
    Console.WriteLine($"long:   {br.ReadInt64().ToString()}  (8 байт)");
    Console.WriteLine($"float:  {br.ReadSingle().ToString("F5")}  (4 байти)");
    Console.WriteLine($"double: {br.ReadDouble().ToString("F9")}  (8 байт)");
    Console.WriteLine($"char:   {br.ReadChar().ToString()}  (2 байти)");
    Console.WriteLine($"string: {br.ReadString()}  (1+5 байт)");
}

File.Delete(path);
```

| Тип C# | Метод BinaryReader | Розмір |
|---|---|---|
| `bool` | `ReadBoolean()` | 1 байт |
| `byte` | `ReadByte()` | 1 байт |
| `sbyte` | `ReadSByte()` | 1 байт |
| `char` | `ReadChar()` | 2 байти (Unicode) |
| `short` | `ReadInt16()` | 2 байти |
| `ushort` | `ReadUInt16()` | 2 байти |
| `int` | `ReadInt32()` | 4 байти |
| `uint` | `ReadUInt32()` | 4 байти |
| `long` | `ReadInt64()` | 8 байт |
| `float` | `ReadSingle()` | 4 байти |
| `double` | `ReadDouble()` | 8 байт |
| `string` | `ReadString()` | 7-бітна довжина + байти |
| `byte[]` | `ReadBytes(count)` | `count` байт |

## Файл з фіксованими записами — індексований доступ

Бінарні файли з фіксованим розміром запису забезпечують O(1) доступ до будь-якого елемента через `Seek`:

```csharp run
using System;
using System.IO;
using System.Text;

// Структура: id(4) + name(20) + glucose(8) + pulse(2) = 34 байти на запис
const int RECORD_SIZE = 34;
const int NAME_SIZE   = 20;

string path = Path.Combine(Path.GetTempPath(), "vitals_index.bin");

// Записуємо кілька пацієнтів
var records = new (int id, string name, double glucose, short pulse)[]
{
    (1001, "Коваль М.А.",     5.1, 72),
    (1002, "Бойко О.П.",      8.7, 145),
    (1003, "Мороз В.І.",      4.8, 68),
    (1004, "Петренко І.О.",  12.4, 110),
    (1005, "Руденко С.В.",    5.5, 78),
};

using (BinaryWriter bw = new BinaryWriter(File.Create(path), Encoding.UTF8))
{
    foreach (var (id, name, glucose, pulse) in records)
    {
        bw.Write(id);
        
        // Ім'я фіксованої ширини — доповнення пробілами або обрізання
        byte[] nameBytes = new byte[NAME_SIZE];
        byte[] encoded   = Encoding.UTF8.GetBytes(name.PadRight(NAME_SIZE));
        Array.Copy(encoded, nameBytes, Math.Min(encoded.Length, NAME_SIZE));
        bw.Write(nameBytes);
        
        bw.Write(glucose);
        bw.Write(pulse);
    }
}

// Читання конкретного запису по індексу — O(1)
int targetIndex = 3; // 4-й пацієнт (0-based)

using (BinaryReader br = new BinaryReader(File.OpenRead(path), Encoding.UTF8))
{
    long offset = (long)targetIndex * RECORD_SIZE;
    br.BaseStream.Seek(offset, SeekOrigin.Begin);
    
    int    id      = br.ReadInt32();
    string name    = Encoding.UTF8.GetString(br.ReadBytes(NAME_SIZE)).Trim();
    double glucose = br.ReadDouble();
    short  pulse   = br.ReadInt16();
    
    Console.WriteLine($"Запис [{targetIndex.ToString()}]:");
    Console.WriteLine($"  ID:      {id.ToString()}");
    Console.WriteLine($"  Ім'я:    {name}");
    Console.WriteLine($"  Глюкоза: {glucose.ToString("F1")} ммоль/л");
    Console.WriteLine($"  Пульс:   {pulse.ToString()} уд/хв");
    
    // Читаємо всі записи
    Console.WriteLine("\nВсі пацієнти:");
    br.BaseStream.Seek(0, SeekOrigin.Begin);
    int count = (int)(br.BaseStream.Length / RECORD_SIZE);
    for (int i = 0; i < count; i++)
    {
        int    rid    = br.ReadInt32();
        string rname  = Encoding.UTF8.GetString(br.ReadBytes(NAME_SIZE)).Trim();
        double rglu   = br.ReadDouble();
        short  rpulse = br.ReadInt16();
        string alert  = (rglu > 7.0 || rpulse > 100) ? " [!]" : "";
        Console.WriteLine($"  {rid.ToString()} | {rname,-18} | глюк.={rglu.ToString("F1")} | пульс={rpulse.ToString()}{alert}");
    }
}

File.Delete(path);
```

## Практичний сценарій: бінарний архів ЕКГ

Реальний приклад застосування `BinaryWriter`/`BinaryReader` — зберігання даних електрокардіограми:

```csharp run
using System;
using System.IO;
using System.Text;

string ecgPath = Path.Combine(Path.GetTempPath(), "ecg_archive.ecg");

// Структура файлу ЕКГ:
// Заголовок: версія(4) + patientId(4) + sampleRate(4) + channelCount(4) + timestamp(8) = 24 байти
// Потім: samples_count(4) + float[] samples

void WriteEcgFile(string path, int patientId, int sampleRate, float[] samples)
{
    using BinaryWriter bw = new BinaryWriter(File.Create(path));
    
    // Заголовок
    bw.Write(1);                                    // версія формату
    bw.Write(patientId);                            // id пацієнта
    bw.Write(sampleRate);                           // частота дискретизації (Гц)
    bw.Write(1);                                    // кількість каналів
    bw.Write(DateTimeOffset.UtcNow.ToUnixTimeSeconds()); // timestamp
    
    // Дані
    bw.Write(samples.Length);
    foreach (float s in samples)
        bw.Write(s);
}

(int patientId, float[] samples, string label)[] ReadEcgFile(string path)
{
    using BinaryReader br = new BinaryReader(File.OpenRead(path));
    
    int version     = br.ReadInt32();
    int patientId   = br.ReadInt32();
    int sampleRate  = br.ReadInt32();
    int channels    = br.ReadInt32();
    long timestamp  = br.ReadInt64();
    int  sampleCount = br.ReadInt32();
    
    float[] samples = new float[sampleCount];
    for (int i = 0; i < sampleCount; i++)
        samples[i] = br.ReadSingle();
    
    return new[] { (patientId, samples, $"v{version.ToString()} sr={sampleRate.ToString()}Hz ch={channels.ToString()}") };
}

// Генеруємо симульований ЕКГ-сигнал (250 Гц, 1 секунда = 250 відліків)
const int SAMPLE_RATE = 250;
float[] ecgData = new float[SAMPLE_RATE];
for (int i = 0; i < SAMPLE_RATE; i++)
{
    double t = (double)i / SAMPLE_RATE;
    ecgData[i] = (float)(Math.Sin(2 * Math.PI * 1.2 * t) + 0.3 * Math.Sin(2 * Math.PI * 6 * t));
}

WriteEcgFile(ecgPath, 1007, SAMPLE_RATE, ecgData);

FileInfo ecgFi = new FileInfo(ecgPath);
int headerSize   = 24;
int samplesBytes = 4 * SAMPLE_RATE + 4; // 4 байт/float + 4 байти для count
Console.WriteLine($"ЕКГ файл: {ecgFi.Length.ToString()} байт");
Console.WriteLine($"  Заголовок: {headerSize.ToString()} байт");
Console.WriteLine($"  Дані:      {samplesBytes.ToString()} байт ({SAMPLE_RATE.ToString()} відліків x 4 байти)");

// Порівняємо з текстовим форматом
string csvLine = string.Join(",", Array.ConvertAll(ecgData, x => x.ToString("F6")));
Console.WriteLine($"\nТе саме у CSV: {Encoding.UTF8.GetByteCount(csvLine).ToString()} байт");
Console.WriteLine($"Стиснення: {((ecgFi.Length * 100.0) / Encoding.UTF8.GetByteCount(csvLine)).ToString("F0")}% від CSV-розміру");

var read = ReadEcgFile(ecgPath)[0];
Console.WriteLine($"\nЗчитано: patientId={read.patientId.ToString()}, {read.samples.Length.ToString()} відліків, {read.label}");
Console.WriteLine($"Перші 5 відліків: {string.Join(", ", Array.ConvertAll(read.samples[..5], x => x.ToString("F3")))}");

File.Delete(ecgPath);
```

![Структура бінарного запису фіксованого розміру](_assets/18-05/binary-record-layout.png)
