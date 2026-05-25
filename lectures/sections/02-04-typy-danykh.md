---
chapter: 2
chapterTitle: "Розділ 2. Основи програмування на C#"
section: 4
number: "2.4"
title: "Типи даних"
source: "../_migration/source-chunks/03-literaly-ta-typy-danykh.md"
---

## 2.4. Типи даних

Як і в багатьох мовах програмування, у C# є власна система типів даних, яка використовується для створення змінних. **Тип даних** визначає внутрішнє представлення даних у пам'яті, діапазон значень, які може приймати змінна, і допустимі операції, які можна застосовувати над змінною. Саме тому, оголошуючи змінну, ми зобов'язані вказати її тип — компілятор використовує цю інформацію для перевірки коректності всіх операцій із цією змінною.

![Базові типи даних C#](_assets/02-04/data-types.png)

У мові C# є такі вбудовані базові типи даних:

### bool

Тип `bool` зберігає логічне значення — `true` (істина) або `false` (хибність). Представлений системним типом `System.Boolean`.

```csharp run
using System;

bool isAdmitted  = true;
bool hasAllergies = false;

Console.WriteLine(isAdmitted.ToString());
Console.WriteLine(hasAllergies.ToString());
```

### byte

Тип `byte` зберігає ціле беззнакове число від **0 до 255** і займає **1 байт**. Представлений системним типом `System.Byte`. Зручний для зберігання малих невід'ємних чисел — наприклад, значень компонентів кольору, відсотків, флагів.

```csharp run
using System;

byte age    = 45;
byte volume = 255;
byte zero   = 0;

Console.WriteLine(age.ToString());
Console.WriteLine(volume.ToString());
```

### sbyte

Тип `sbyte` (signed byte) зберігає ціле число зі знаком від **-128 до 127** і займає **1 байт**. Представлений системним типом `System.SByte`. Відрізняється від `byte` тим, що може зберігати від'ємні значення.

```csharp run
using System;

sbyte positive = 102;
sbyte negative = -101;

Console.WriteLine(positive.ToString());
Console.WriteLine(negative.ToString());
```

### short

Тип `short` зберігає ціле число зі знаком від **-32 768 до 32 767** і займає **2 байти**. Представлений системним типом `System.Int16`.

```csharp run
using System;

short systolic  = 120;
short diastolic = 80;

Console.WriteLine($"Тиск: {systolic.ToString()}/{diastolic.ToString()} мм рт.ст.");
```

### ushort

Тип `ushort` (unsigned short) зберігає ціле беззнакове число від **0 до 65 535** і займає **2 байти**. Представлений системним типом `System.UInt16`.

```csharp run
using System;

ushort heartRate = 72;
ushort maxValue  = 65535;

Console.WriteLine(heartRate.ToString());
Console.WriteLine(maxValue.ToString());
```

### int

Тип `int` зберігає ціле число зі знаком від **-2 147 483 648 до 2 147 483 647** і займає **4 байти**. Представлений системним типом `System.Int32`. Це **найпоширеніший цілочисленний тип** у C# — за замовчуванням усі цілі літерали (наприклад, `42`) мають саме тип `int`.

```csharp run
using System;

int a = 10;
int b = 0b101; // двійкова форма, b = 5
int c = 0xFF;  // шістнадцяткова форма, c = 255

Console.WriteLine(a.ToString());
Console.WriteLine(b.ToString());
Console.WriteLine(c.ToString());
```

### uint

Тип `uint` (unsigned int) зберігає ціле беззнакове число від **0 до 4 294 967 295** і займає **4 байти**. Представлений системним типом `System.UInt32`. Для явного позначення `uint`-літерала використовується суфікс `u` або `U`.

```csharp run
using System;

uint a = 10U;
uint b = 0b101;
uint c = 0xFF;

Console.WriteLine(a.ToString());
Console.WriteLine(b.ToString());
Console.WriteLine(c.ToString());
```

### long

Тип `long` зберігає ціле число зі знаком від **-9 223 372 036 854 775 808 до 9 223 372 036 854 775 807** і займає **8 байт**. Представлений системним типом `System.Int64`. Використовується тоді, коли діапазон `int` недостатній. Для явного позначення `long`-літерала — суфікс `l` або `L`.

```csharp run
using System;

long recordsCount = 9_000_000_000L;
long negative     = -10L;

Console.WriteLine(recordsCount.ToString());
Console.WriteLine(negative.ToString());
```

### ulong

Тип `ulong` (unsigned long) зберігає ціле беззнакове число від **0 до 18 446 744 073 709 551 615** і займає **8 байт**. Представлений системним типом `System.UInt64`. Суфікс — `ul` або `UL`.

```csharp run
using System;

ulong a = 10UL;
ulong b = 0b101;
ulong c = 0xFF;

Console.WriteLine(a.ToString());
Console.WriteLine(b.ToString());
Console.WriteLine(c.ToString());
```

### float

Тип `float` зберігає число з плаваючою точкою приблизно від **-3.4 × 10³⁸ до 3.4 × 10³⁸** і займає **4 байти**. Представлений системним типом `System.Single`. Забезпечує приблизно 7 значущих цифр. Для позначення `float`-літерала обов'язковий суфікс `f` або `F`.

```csharp run
using System;

float weight      = 72.5f;
float temperature = 36.6F;

Console.WriteLine(weight.ToString());
Console.WriteLine(temperature.ToString());
```

### double

Тип `double` зберігає число з плаваючою точкою приблизно від **±5.0 × 10⁻³²⁴ до ±1.7 × 10³⁰⁸** і займає **8 байт**. Представлений системним типом `System.Double`. Забезпечує приблизно 15–16 значущих цифр. Це **найпоширеніший тип для дробових чисел** — за замовчуванням усі речові літерали (наприклад, `3.14`) мають тип `double`.

```csharp run
using System;

double pi          = 3.14159265358979;
double temperature = 36.6;
double bmi         = 22.5;

Console.WriteLine(pi.ToString());
Console.WriteLine(temperature.ToString());
Console.WriteLine(bmi.ToString());
```

### decimal

Тип `decimal` зберігає десяткове дробове число з дуже високою точністю — 28–29 значущих цифр — і займає **16 байт**. Представлений системним типом `System.Decimal`. Діапазон від **±1.0 × 10⁻²⁸ до ±7.9 × 10²⁸**. Для позначення `decimal`-літерала обов'язковий суфікс `m` або `M`.

На відміну від `float` і `double`, тип `decimal` не має похибок округлення при роботі з десятковими дробами, тому він **незамінний у фінансових розрахунках**, де точність кожного знаку критична.

```csharp run
using System;

decimal price     = 1005.80m;
decimal discount  = 100.50M;
decimal total     = price - discount;

Console.WriteLine(price.ToString());
Console.WriteLine(discount.ToString());
Console.WriteLine(total.ToString());
```

### char

Тип `char` зберігає **одиночний символ** у кодуванні Unicode і займає **2 байти**. Представлений системним типом `System.Char`. Символьні літерали беруться в одинарні лапки.

```csharp run
using System;

char a = 'A';
char b = '\x5A'; // Z через шістнадцятковий ASCII-код
char c = 'І';    // кириличний символ

Console.WriteLine(a.ToString());
Console.WriteLine(b.ToString());
Console.WriteLine(c.ToString());
```

### string

Тип `string` зберігає **послідовність символів Unicode** довільної довжини. Представлений системним типом `System.String`. Рядкові літерали беруться в подвійні лапки. На відміну від усіх попередніх типів, `string` є **reference-типом** — змінна зберігає не саме значення, а посилання на об'єкт у купі.

```csharp run
using System;

string firstName = "Іван";
string lastName  = "Петренко";
string fullName  = firstName + " " + lastName;

Console.WriteLine(fullName);
Console.WriteLine($"Довжина: {fullName.Length.ToString()} символів");
```

### object

Тип `object` може зберігати значення **будь-якого типу даних** — як value-типів, так і reference-типів. Представлений системним типом `System.Object`, який є **базовим класом для всіх типів і класів .NET**. Займає 4 байти на 32-розрядній платформі та 8 байт — на 64-розрядній.

```csharp run
using System;

object a = 22;
object b = 3.14;
object c = "hello code";
object d = true;

Console.WriteLine(a.ToString());
Console.WriteLine(b.ToString());
Console.WriteLine(c.ToString());
Console.WriteLine(d.ToString());
```

Хоча `object` здається зручним — «приймає все» — на практиці він використовується обережно, бо втрачається типобезпека і можливі накладні витрати при boxing/unboxing (про це детально у темі узагальнень).

## Комплексний приклад

Визначимо кілька змінних різних типів і виведемо їх значення на консоль:

```csharp run
using System;

string name       = "Іван Петренко";
int    age        = 45;
bool   isAdmitted = false;
double weight     = 78.65;
decimal bill      = 1250.50m;

Console.WriteLine($"Ім'я: {name}");
Console.WriteLine($"Вік: {age.ToString()}");
Console.WriteLine($"Вага: {weight.ToString()}");
Console.WriteLine($"Госпіталізований: {isAdmitted.ToString()}");
Console.WriteLine($"Рахунок: {bill.ToString()} грн");
```

## Використання суфіксів

При присвоєнні значень слід пам'ятати: всі речові літерали за замовчуванням мають тип `double`, а всі цілочисленні — тип `int`. Щоб явно вказати інший тип, використовуються суфікси:

```csharp run
using System;

float   f = 3.14F;
decimal d = 1005.8M;
uint    u = 10U;
long    l = 20L;
ulong  ul = 30UL;

Console.WriteLine(f.ToString());
Console.WriteLine(d.ToString());
Console.WriteLine(u.ToString());
Console.WriteLine(l.ToString());
Console.WriteLine(ul.ToString());
```

## Системні типи

Назва вбудованого типу — це скорочення відповідного системного типу .NET. Наприклад, `int` і `System.Int32` є повністю еквівалентними:

```csharp run
using System;

int           a = 4;
System.Int32  b = 4;

Console.WriteLine(a.ToString());
Console.WriteLine(b.ToString());
Console.WriteLine((a == b).ToString()); // true
```

Обидва записи абсолютно рівнозначні — компілятор сприймає їх однаково. На практиці зазвичай вживають скорочені псевдоніми (`int`, `string`, `bool`), оскільки вони стисліші і звичніші.

## Неявна типізація

У C# можна не вказувати тип змінної явно, якщо компілятор може визначити його самостійно з виразу праворуч. Для цього замість назви типу вказується ключове слово `var`:

```csharp run
using System;

var hello = "Hello to World";
var c     = 20;
var d     = 3.14;
var flag  = true;

Console.WriteLine(hello.GetType().Name); // String
Console.WriteLine(c.GetType().Name);     // Int32
Console.WriteLine(d.GetType().Name);     // Double
Console.WriteLine(flag.GetType().Name);  // Boolean
```

Оскільки за замовчуванням цілочисленні значення розглядаються як `int`, а речові — як `double`, то `c` отримає тип `int`, а `d` — тип `double`. Тип виводиться **один раз** при оголошенні і фіксується — надалі змінна поводиться точно так само, як якби тип був вказаний явно.

Неявно типізована змінна має кілька обмежень. По-перше, не можна спочатку оголосити змінну, а потім ініціалізувати — компілятор не знатиме, який тип вивести:

```csharp
// Цей код працює:
int a;
a = 20;

// Цей код не працює — помилка компіляції:
var c;
c = 20;
```

По-друге, не можна ініціалізувати `var` значенням `null`, оскільки `null` сам по собі не несе інформації про тип:

```csharp
// Цей код не працює — помилка компіляції:
var c = null;
```
