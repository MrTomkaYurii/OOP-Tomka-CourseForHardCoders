---
chapter: 13
chapterTitle: "Розділ 13. Додаткові класи та структури .NET"
section: 4
number: "13.4"
title: "Клас Array"
source: "../_combined/81-klas-array.md"
---

## 13.4. Клас `Array`

Масив — одна з фундаментальних структур даних у C#. Кожен масив, оголошений як `int[]`, `string[]` або `PatientRecord[]`, насправді є об'єктом класу `System.Array` — абстрактного базового класу для всіх масивів у .NET. Саме тому масиви мають властивості `.Length`, `.Rank` і підтримують інтерфейси `IEnumerable<T>`, `IList<T>`, `ICloneable`.

Поряд із самими масивами, .NET надає **статичний клас `Array`** із набором методів для пошуку, сортування, копіювання, заповнення та перевірки. Ці методи доповнюють вбудовані можливості масивів і дозволяють виконувати типові операції без написання ручних циклів.

![Клас Array — пошук, сортування, копіювання](_assets/13-04/array-overview.png)

## Властивості масивів

Будь-який масив як екземпляр `System.Array` має такі властивості:

```csharp
int[] ages = { 67, 45, 52, 71, 38 };

Console.WriteLine(ages.Length);    // 5 — загальна кількість елементів
Console.WriteLine(ages.Rank);      // 1 — одновимірний масив

int[,] matrix = new int[3, 4];
Console.WriteLine(matrix.Length);         // 12 — 3 × 4
Console.WriteLine(matrix.Rank);           // 2
Console.WriteLine(matrix.GetLength(0));   // 3 — рядки
Console.WriteLine(matrix.GetLength(1));   // 4 — стовпці
```

`Rank` завжди `1` для звичайних одновимірних масивів. Для двовимірних (матриць) `GetLength(dimension)` повертає розмір відповідного виміру.

## Сортування: Array.Sort

`Array.Sort(arr)` виконує сортування **in-place** — змінює сам переданий масив, нічого не повертаючи. Використовує алгоритм introsort (O(n log n)), вимагає, щоб тип `T` реалізовував `IComparable<T>`:

```csharp
int[] ages = { 67, 45, 52, 71, 38 };
Array.Sort(ages);
// ages: { 38, 45, 52, 67, 71 }
```

Для сортування масиву об'єктів за конкретним полем передається **лямбда-вираз порівняння**:

```csharp
string[] names = { "Сидоренко", "Петренко", "Коваль", "Бойко" };
Array.Sort(names, (a, b) => string.Compare(a, b, StringComparison.OrdinalIgnoreCase));
// names: { "Бойко", "Коваль", "Петренко", "Сидоренко" }
```

`Array.Sort(keys, values)` дозволяє **паралельно сортувати два масиви**, зберігаючи відповідність між ними. Після сортування елементи `values` слідують за переміщеними елементами `keys`:

```csharp
string[] ids   = { "P003", "P001", "P002" };
int[]    ages  = { 52, 38, 67 };

Array.Sort(ids, ages); // сортуємо за id, ages рухаються разом
// ids:  { "P001", "P002", "P003" }
// ages: { 38, 67, 52 }
```

`Array.Reverse(arr)` перевертає порядок елементів in-place. Зручно після сортування, якщо потрібний спадний порядок:

```csharp
Array.Sort(ages);
Array.Reverse(ages); // від більшого до меншого
```

## Пошук: IndexOf, BinarySearch, Find

`Array.IndexOf(arr, value)` виконує **лінійний пошук** (O(n)) і повертає індекс першого знайденого елемента або `-1`:

```csharp
string[] ids = { "P001", "P002", "P003", "P004" };
int idx = Array.IndexOf(ids, "P003"); // 2
int bad = Array.IndexOf(ids, "P999"); // -1
```

`Array.BinarySearch(arr, value)` — **бінарний пошук** (O(log n)), але **вимагає відсортованого масиву**. Якщо елемент знайдено, повертає його індекс. Якщо ні — повертає від'ємне число (побітове доповнення позиції вставки):

```csharp
int[] sorted = { 38, 45, 52, 67, 71 };
int pos  = Array.BinarySearch(sorted, 52);  //  2 — знайдено
int miss = Array.BinarySearch(sorted, 50);  // -3 — не знайдено (~позиції 2)
```

Якщо результат від'ємний — елемент відсутній. Щоб отримати позицію, куди можна вставити елемент: `~miss`.

`Array.Find(arr, predicate)` шукає **перший елемент, що задовольняє умову**. Якщо нічого не знайдено — повертає значення за замовчуванням (`null` для посилальних типів, `0` для `int`):

```csharp
int[] ages = { 67, 45, 52, 71, 38 };
int senior = Array.Find(ages, a => a >= 65); // 67
```

`Array.FindAll(arr, predicate)` повертає **новий масив** з усіма елементами, що відповідають умові:

```csharp
int[] seniors = Array.FindAll(ages, a => a >= 65); // { 67, 71 }
```

`Array.FindIndex(arr, predicate)` — як `Find`, але повертає **індекс**, а не значення:

```csharp
int idx = Array.FindIndex(ages, a => a >= 65); // 0 (перший елемент)
```

## Перевірки: Exists та TrueForAll

`Array.Exists(arr, predicate)` — повертає `true`, якщо **хоча б один** елемент задовольняє умову:

```csharp
bool hasSenior = Array.Exists(ages, a => a >= 65); // true
```

`Array.TrueForAll(arr, predicate)` — повертає `true`, якщо **всі** елементи задовольняють умову:

```csharp
bool allAdults = Array.TrueForAll(ages, a => a >= 18); // true
bool allYoung  = Array.TrueForAll(ages, a => a < 50);  // false
```

## Копіювання: Array.Copy та Clone

`Array.Copy(sourceArray, destinationArray, length)` копіює перші `length` елементів:

```csharp
int[] src = { 1, 2, 3, 4, 5 };
int[] dst = new int[5];
Array.Copy(src, dst, 3); // dst: { 1, 2, 3, 0, 0 }
```

З вказанням початкових позицій:

```csharp
// Array.Copy(src, srcIndex, dst, dstIndex, length)
Array.Copy(src, 1, dst, 2, 3); // копіювати src[1..3] у dst[2..4]
// src: { 1, 2, 3, 4, 5 }
// dst: { 0, 0, 2, 3, 4 }
```

`.Clone()` повертає **поверхневу копію** (shallow copy) масиву як `object`. Для масивів значущих типів (`int[]`, `double[]`) це повна незалежна копія. Для масивів посилальних типів (`PatientRecord[]`) копіюються **посилання**, не самі об'єкти — зміна поля через `dst[0].Name = "..."` вплине на обидва масиви:

```csharp
int[] a = { 1, 2, 3 };
int[] b = (int[])a.Clone();
b[0] = 99;
Console.WriteLine(a[0]); // 1 — незалежні копії для int[]
```

## Array.Resize — новий масив під капотом

`Array.Resize(ref arr, newSize)` змінює розмір масиву. Але під капотом це **не розширення існуючого масиву** — .NET виділяє нову ділянку пам'яті, копіює дані і оновлює посилання `arr` через `ref`:

```csharp
int[] arr = { 1, 2, 3 };
Array.Resize(ref arr, 6);
// arr: { 1, 2, 3, 0, 0, 0 }
```

Якщо `newSize < arr.Length` — масив обрізається, зайві елементи губляться.

Важливе наслідство: якщо є інша змінна, що вказувала на старий масив, вона **залишається вказувати на стару ділянку** пам'яті після `Resize`. Саме тому параметр `ref` — обов'язковий, щоб оновити хоча б оригінальну змінну. Якщо потрібна динамічна колекція без цих обмежень — краще використовувати `List<T>`.

## Заповнення та очищення

`Array.Fill(arr, value)` (.NET Core 2.1+) заповнює весь масив заданим значенням:

```csharp
int[] slots = new int[5];
Array.Fill(slots, -1); // { -1, -1, -1, -1, -1 }
```

З вказанням діапазону:

```csharp
Array.Fill(slots, 0, 2, 3); // заповнити 3 елементи починаючи з індексу 2
// slots: { -1, -1, 0, 0, 0 }
```

`Array.Clear(arr, index, length)` заповнює елементи **значенням за замовчуванням**: `0` для числових, `false` для `bool`, `null` для посилальних типів:

```csharp
int[] data = { 10, 20, 30, 40, 50 };
Array.Clear(data, 1, 3);
// data: { 10, 0, 0, 0, 50 }
```

В .NET 6+ з'явився `Array.Clear(arr)` без параметрів — очищення всього масиву.

## Сортування та пошук пацієнтів — runnable приклад

```csharp run
using System;

var patients = new Patient[]
{
    new Patient { Id="P001", Name="Петренко Іван",   Age=67, Bmi=27.3, Icd="I10.9" },
    new Patient { Id="P002", Name="Коваль Марія",    Age=45, Bmi=23.1, Icd="J45.0" },
    new Patient { Id="P003", Name="Сидоренко Олег",  Age=52, Bmi=31.8, Icd="E11.9" },
    new Patient { Id="P004", Name="Бойко Тетяна",    Age=71, Bmi=19.4, Icd="I10.9" },
    new Patient { Id="P005", Name="Мороз Василь",    Age=38, Bmi=25.6, Icd="J45.0" },
};

Console.WriteLine("=== Сортування за віком (спадно) ===");
Array.Sort(patients, (a, b) => b.Age.CompareTo(a.Age));
Console.WriteLine($"{"ID",-6} {"Пацієнт",-22} {"Вік",4} {"ІМТ",6}  ICD");
Console.WriteLine(new string('-', 48));
foreach (var p in patients)
    Console.WriteLine($"{p.Id,-6} {p.Name,-22} {p.Age,4} {p.Bmi,6:F1}  {p.Icd}");

Console.WriteLine("\n=== Сортування за ІМТ (зростаючи) ===");
Array.Sort(patients, (a, b) => a.Bmi.CompareTo(b.Bmi));
foreach (var p in patients)
    Console.WriteLine($"{p.Id,-6} {p.Name,-22} ІМТ={p.Bmi:F1}");

Console.WriteLine("\n=== Пошук: FindAll за діагнозом I10.9 ===");
var hypertensive = Array.FindAll(patients, p => p.Icd == "I10.9");
Console.WriteLine($"Гіпертонія (I10.9): {hypertensive.Length} пацієнтів");
foreach (var p in hypertensive)
    Console.WriteLine($"  {p.Name}, {p.Age} р.");

Console.WriteLine("\n=== Exists / TrueForAll ===");
bool hasObesity  = Array.Exists(patients, p => p.Bmi >= 30);
bool allAdults   = Array.TrueForAll(patients, p => p.Age >= 18);
Console.WriteLine($"Є ожиріння (ІМТ≥30): {hasObesity}");
Console.WriteLine($"Усі повнолітні:       {allAdults}");

Console.WriteLine("\n=== Find + FindIndex ===");
var firstSenior = Array.Find(patients, p => p.Age >= 65);
int seniorIdx   = Array.FindIndex(patients, p => p.Age >= 65);
Console.WriteLine($"Перший пацієнт 65+: {firstSenior.Name} (індекс {seniorIdx})");

struct Patient
{
    public string Id;
    public string Name;
    public int    Age;
    public double Bmi;
    public string Icd;
}
```

## Копіювання, Fill та IndexOf — runnable приклад

```csharp run
using System;

Console.WriteLine("=== Array.Copy ===");
string[] source = { "P001", "P002", "P003", "P004", "P005" };
string[] backup = new string[5];

Array.Copy(source, backup, 3);
Console.WriteLine("Source: " + string.Join(", ", source));
Console.WriteLine("Backup: " + string.Join(", ", backup));

Console.WriteLine("\n=== Array.IndexOf ===");
int idx = Array.IndexOf(source, "P003");
int bad = Array.IndexOf(source, "P999");
Console.WriteLine($"IndexOf(\"P003\") = {idx}");
Console.WriteLine($"IndexOf(\"P999\") = {bad}  // не знайдено");

Console.WriteLine("\n=== Array.BinarySearch (потрібен відсортований масив) ===");
int[] ages = { 38, 45, 52, 67, 71 }; // вже відсортований
int found   = Array.BinarySearch(ages, 52);
int missing = Array.BinarySearch(ages, 50);
Console.WriteLine($"BinarySearch(52) = {found}   // знайдено на індексі {found}");
Console.WriteLine($"BinarySearch(50) = {missing}  // не знайдено, позиція вставки = {~missing}");

Console.WriteLine("\n=== Array.Fill ===");
int[] slots = new int[6];
Array.Fill(slots, -1);
Console.WriteLine("Fill(-1):   " + string.Join(", ", slots));
Array.Fill(slots, 0, 2, 3);
Console.WriteLine("Fill(0,2,3):" + string.Join(", ", slots));

Console.WriteLine("\n=== Array.Clear ===");
int[] data = { 10, 20, 30, 40, 50 };
Console.WriteLine("До Clear:   " + string.Join(", ", data));
Array.Clear(data, 1, 3);
Console.WriteLine("Після Clear:" + string.Join(", ", data));

Console.WriteLine("\n=== Array.Resize ===");
string[] ids = { "P001", "P002", "P003" };
Console.WriteLine($"До Resize:   Length={ids.Length}, дані={string.Join(", ", ids)}");
Array.Resize(ref ids, 5);
Console.WriteLine($"Після Resize:Length={ids.Length}, дані={string.Join(", ", ids ?? new string[0])}");
ids[3] = "P004"; ids[4] = "P005";
Console.WriteLine($"Після заповн:дані={string.Join(", ", ids)}");
