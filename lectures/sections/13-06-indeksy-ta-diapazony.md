---
chapter: 13
chapterTitle: "Розділ 13. Додаткові класи та структури .NET"
section: 6
number: "13.6"
title: "Індекси та діапазони (Index та Range)"
source: "../_combined/83-indeksy-ta-diapazony.md"
---

## 13.6. Індекси та діапазони (`Index` та `Range`)

До C# 8 отримати останній елемент масиву виглядало так: `arr[arr.Length - 1]`. Передостанній — `arr[arr.Length - 2]`. Взяти підмасив від 2-го до 5-го: `arr.Skip(2).Take(3).ToArray()` або ручний цикл. Ці операції прості концептуально, але громіздкі в записі і схильні до помилок «на одиницю».

C# 8 (.NET Core 3.0+) ввів два нових типи — `System.Index` і `System.Range` — та відповідний синтаксис: оператор `^` для індексування від кінця і оператор `..` для діапазонів. Разом вони роблять роботу з послідовностями значно лаконічнішою.

![Index та Range — індексування від кінця та діапазони](_assets/13-06/index-range-overview.png)

## Тип Index та оператор `^`

`System.Index` — структура, що представляє позицію в послідовності. Вона може бути **прямою** (від початку, як звичайний `int`) або **зворотньою** (від кінця, через оператор `^`):

```csharp
Index i0 = 2;    // третій елемент (звичайний індекс)
Index i1 = ^1;   // останній елемент
Index i2 = ^2;   // передостанній
```

Оператор `^n` означає «n-й від кінця», де **`^1` — останній**, `^2` — передостанній і т. д. `^0` рівний `.Length` — це позиція **за межею масиву**, тому `arr[^0]` дасть `IndexOutOfRangeException`:

```csharp
string[] names = { "Петренко", "Коваль", "Бойко", "Сидоренко" };

Console.WriteLine(names[^1]); // "Сидоренко" — останній
Console.WriteLine(names[^2]); // "Бойко"     — передостанній
Console.WriteLine(names[0]);  // "Петренко"  — перший (прямий індекс)
```

`Index` можна зберігати у змінній і передавати у методи:

```csharp
Index last = ^1;
Console.WriteLine(names[last]); // "Сидоренко"
```

`Index.GetOffset(length)` перетворює `^`-індекс у числовий: `^1.GetOffset(4) == 3`.

## Тип Range та оператор `..`

`System.Range` — структура, що представляє діапазон індексів. Синтаксис `a..b` означає «від `a` включно до `b` **виключно**». Обидві межі можуть бути звичайними індексами або `^`-індексами:

```csharp
double[] pressures = { 120, 135, 128, 142, 118, 155, 130 };

double[] first3 = pressures[0..3];    // { 120, 135, 128 } — індекси 0,1,2
double[] mid    = pressures[2..5];    // { 128, 142, 118 } — індекси 2,3,4
double[] last3  = pressures[^3..];    // { 155, 130, ? } — від ^3 до кінця
double[] all    = pressures[..];      // весь масив
```

Межі `..` є необов'язковими: `arr[..n]` — перші `n` елементів (від 0), `arr[n..]` — від `n` до кінця, `arr[..]` — весь масив.

Поєднання `^` і `..` робить типові операції дуже виразними:

```csharp
double[] withoutFirst  = pressures[1..];    // відкинути перший
double[] withoutLast   = pressures[..^1];   // відкинути останній
double[] inner         = pressures[1..^1];  // без першого і останнього
double[] lastFive      = pressures[^5..];   // останні 5
```

## Range можна зберігати у змінній

`Range` — це значущий тип (struct), його можна зберігати і передавати:

```csharp
Range recent = ^5..;       // останні 5
Range inner  = 1..^1;      // без крайніх

double[] recentReadings = pressures[recent];
double[] innerReadings  = pressures[inner];
```

`Range.GetOffsetAndLength(length)` повертає кортеж `(offset, length)` — числові значення для ручного використання, якщо API не підтримує `Range` безпосередньо:

```csharp
Range r = 1..^1;
var (offset, length) = r.GetOffsetAndLength(pressures.Length);
// offset=1, length=5 (для масиву з 7 елементів)
```

## Застосування до рядків

Оператор `[..]` працює зі `string` так само, як `Substring`, але значно лаконічніше:

```csharp
string icd = "I10.9";

char   first  = icd[0];       // 'I'
char   last   = icd[^1];      // '9'
string code   = icd[1..];     // "10.9" — без першого символу
string digits = icd[1..^2];   // "10"   — код без літери і дрібниці
string ext    = icd[^3..];    // ".9" — три символи з кінця
```

Результат `str[a..b]` — це **новий рядок** (heap-копія), тобто семантично еквівалентний `str.Substring(a, b - a)`. Для безкопійного варіанту — `str.AsSpan()[a..b]`, що повертає `ReadOnlySpan<char>`.

## Range та масиви: завжди нова копія

На відміну від `Span`, при застосуванні `Range` до масиву (`T[]`) завжди створюється **новий масив**:

```csharp
int[] src  = { 1, 2, 3, 4, 5 };
int[] copy = src[1..4]; // новий масив { 2, 3, 4 }

copy[0] = 99;
Console.WriteLine(src[1]); // 2 — src не змінився
```

Якщо потрібна безкопійна вибірка — використовуйте `Span<T>` або `ReadOnlySpan<T>`:

```csharp
Span<int> slice = src.AsSpan()[1..4]; // вказівник, не копія
slice[0] = 99;
Console.WriteLine(src[1]); // 99 — оригінал змінився
```

Вибір між `arr[a..b]` (нова копія) і `span[a..b]` (без копії) залежить від сценарію: якщо результат зберігається надовго або передається куди-небудь — копія доречна; якщо обробляється тут-і-зараз у межах методу — `Span` ефективніший.

## `List<T>` та інші колекції

`Index` і `Range` підтримуються **не всіма** колекціями. `T[]` і `string` підтримують повністю. `Span<T>` і `ReadOnlySpan<T>` — повністю. `List<T>` підтримує `Index` (`list[^1]`), але **не підтримує `Range`** (`list[1..3]` — помилка компіляції). Для зрізів `List<T>` використовується метод `.GetRange(index, count)`.

## Вимірювання тиску: Index та Range — runnable приклад

```csharp run
using System;

Console.WriteLine("=== Вимірювання артеріального тиску ===");
double[] systolic = { 145, 138, 152, 130, 147, 135, 128, 142, 155, 133 };

Console.WriteLine("Всі вимірювання:");
Console.WriteLine("  " + string.Join(", ", systolic));

Console.WriteLine($"\nПерше:        {systolic[0]}");
Console.WriteLine($"Останнє:      {systolic[^1]}");
Console.WriteLine($"Передостаннє: {systolic[^2]}");

Console.WriteLine("\nОстанні 3 вимірювання (^3..):");
double[] last3 = systolic[^3..];
Console.WriteLine("  " + string.Join(", ", last3));

Console.WriteLine("\nБез крайніх (1..^1) — прибираємо першу і останню точку:");
double[] inner = systolic[1..^1];
Console.WriteLine("  " + string.Join(", ", inner));

double sum = 0;
for (int i = 0; i < inner.Length; i++) sum += inner[i];
Console.WriteLine($"  Середнє (без крайніх): {sum / inner.Length:F1}");

Console.WriteLine("\n=== Рядки: ICD-10 ===");
string[] icds = { "I10.9", "J45.0", "E11.9", "K21.0" };
foreach (string icd in icds)
{
    char   letter = icd[0];
    string num    = icd[1..^2];
    string sub    = icd[^1..];
    Console.WriteLine($"  {icd}  → клас={letter}  код={num}  підкласс={sub}");
}

Console.WriteLine("\n=== Range у змінній ===");
Range recentRange = ^5..;
double[] recent5 = systolic[recentRange];
Console.WriteLine($"recent5 = [{string.Join(", ", recent5)}]");

var (offset, length) = recentRange.GetOffsetAndLength(systolic.Length);
Console.WriteLine($"GetOffsetAndLength: offset={offset}, length={length}");
```

## Range зі Span та GetOffsetAndLength — runnable приклад

```csharp run
using System;

Console.WriteLine("=== Span<double> з Range — без копіювання ===");
double[] glucose = { 5.1, 6.3, 7.8, 5.9, 6.1, 8.2, 5.4, 6.7 };

Console.WriteLine("Всі вимірювання глюкози:");
Console.WriteLine("  " + string.Join(", ", glucose));

// Span-зріз без копії
Span<double> spanAll   = glucose.AsSpan();
Span<double> spanInner = spanAll[1..^1]; // без першого і останнього

Console.WriteLine($"\nSpan[1..^1] (без крайніх), довжина = {spanInner.Length}:");
Console.Write("  ");
for (int i = 0; i < spanInner.Length; i++)
    Console.Write($"{spanInner[i]}{(i < spanInner.Length - 1 ? ", " : "\n")}");

// Зміна через Span змінює оригінальний масив
spanInner[0] = 6.0;
Console.WriteLine($"Після spanInner[0]=6.0: glucose[1] = {glucose[1]}");

Console.WriteLine("\n=== Масив vs Span: копія чи вказівник ===");
int[] data = { 10, 20, 30, 40, 50 };

int[] arrSlice  = data[1..4];      // нова копія
Span<int> spanSlice = data.AsSpan()[1..4]; // вказівник

arrSlice[0]  = 99;
spanSlice[1] = 88;

Console.WriteLine($"data після arrSlice[0]=99:   [{string.Join(", ", data)}]");
Console.WriteLine($"  data[1] = {data[1]} (не змінився — копія)");
Console.WriteLine($"data після spanSlice[1]=88:  [{string.Join(", ", data)}]");
Console.WriteLine($"  data[2] = {data[2]} (змінився — вказівник)");

Console.WriteLine("\n=== Index: GetOffset ===");
Index last  = ^1;
Index third = ^3;
Console.WriteLine($"^1 у масиві з 5 елементів → індекс {last.GetOffset(5)}");
Console.WriteLine($"^3 у масиві з 5 елементів → індекс {third.GetOffset(5)}");

Console.WriteLine("\n=== Range: GetOffsetAndLength ===");
Range[] ranges = { .., 1..^1, ^3.., 2..4 };
string[] labels = { "..", "1..^1", "^3..", "2..4" };
for (int i = 0; i < ranges.Length; i++)
{
    var (off, len) = ranges[i].GetOffsetAndLength(data.Length);
    Console.WriteLine($"  {labels[i],-8} → offset={off}, length={len}");
}
```
