---
chapter: 2
chapterTitle: "Розділ 2. Основи програмування на C#"
section: 3
number: "2.3"
title: "Літерали"
source: "../_migration/source-chunks/03-literaly-ta-typy-danykh.md"
---

## 2.3. Літерали

**Літерали** — це фіксовані значення, записані безпосередньо у вихідному коді програми. Коли ми пишемо `42`, `3.14`, `"Привіт"` або `true` — все це літерали. На відміну від змінних, значення якої може змінюватись під час виконання, літерал завжди означає одне й те саме конкретне значення, відоме ще на етапі компіляції.

Літерали можна передавати змінним як значення, передавати як аргументи методів або використовувати безпосередньо у виразах. У C# є кілька видів літералів: **логічні**, **цілочисленні**, **речові**, **символьні**, **рядкові** та спеціальний літерал `null`.

## Логічні літерали

Є лише два логічних літерали — `true` (істина) і `false` (хибність). Вони відповідають типу `bool` і є єдиними допустимими значеннями для логічних змінних:

```csharp run
using System;

bool isAdmitted   = true;
bool hasAllergies = false;

Console.WriteLine(isAdmitted.ToString());
Console.WriteLine(hasAllergies.ToString());
Console.WriteLine(true.ToString());
Console.WriteLine(false.ToString());
```

## Цілочисленні літерали

Цілочисленні літерали представляють цілі числа — позитивні та негативні. Вони можуть бути виражені у трьох системах числення: **десятковій**, **двійковій** та **шістнадцятковій**.

З числами у десятковій формі все звично — вони використовуються в повсякденному житті:

```csharp run
using System;

Console.WriteLine(-11);
Console.WriteLine(5);
Console.WriteLine(505);
```

Числа у **двійковій** формі передуються символами `0b`, після яких іде набір з нулів та одиниць:

```csharp run
using System;

Console.WriteLine(0b11);     // 3
Console.WriteLine(0b1011);   // 11
Console.WriteLine(0b100001); // 33
```

Для запису числа у **шістнадцятковій** формі використовуються символи `0x`, після яких іде набір символів від `0` до `9` і від `A` до `F`:

```csharp run
using System;

Console.WriteLine(0x0A); // 10
Console.WriteLine(0xFF); // 255
Console.WriteLine(0xA1); // 161
```

Починаючи з C# 7, у цілочисленних літералах можна використовувати символ підкреслення `_` як розділювач розрядів для покращення читабельності. Компілятор його повністю ігнорує:

```csharp run
using System;

int million   = 1_000_000;
int cardNumber = 1234_5678;

Console.WriteLine(million.ToString());
Console.WriteLine(cardNumber.ToString());
```

## Речові літерали

Речові літерали представляють дробові числа. Перша форма — числа з фіксованою крапкою, де дробову частину відокремлено від цілої крапкою:

```csharp run
using System;

Console.WriteLine(3.14.ToString());
Console.WriteLine(100.001.ToString());
Console.WriteLine((-0.38).ToString());
```

Також речові літерали можуть задаватися в **експоненційній формі** `MEp`, де `M` — мантиса, `E` — ознака степеня, `p` — порядок (степінь десяти). Наприклад, `3.2e3` означає `3.2 × 10³ = 3200`:

```csharp run
using System;

Console.WriteLine(3.2e3.ToString());   // 3200
Console.WriteLine(1.2e-1.ToString());  // 0.12
Console.WriteLine(5.0e6.ToString());   // 5000000
```

За замовчуванням всі речові літерали є значеннями типу `double`. Якщо потрібно явно вказати тип `float` або `decimal`, використовуються суфікси: `f` або `F` для `float`, `m` або `M` для `decimal`:

```csharp run
using System;

double d = 3.14;       // double за замовчуванням
float  f = 3.14f;      // суфікс f → float
decimal m = 3.14m;     // суфікс m → decimal

Console.WriteLine(d.ToString());
Console.WriteLine(f.ToString());
Console.WriteLine(m.ToString());
```

Тип `decimal` особливо важливий для фінансових розрахунків, оскільки він не має похибок округлення, характерних для `float` і `double` при роботі з десятковими дробами.

## Символьні літерали

Символьні літерали представляють одиночний символ. Символ береться в **одинарні** лапки і відповідає типу `char`. Кожен символ кодується у Unicode і займає 2 байти.

Найпростіший вид — звичайні символи:

```csharp run
using System;

char letter = 'A';
char digit  = '2';
char ukr    = 'І';

Console.WriteLine(letter.ToString());
Console.WriteLine(digit.ToString());
Console.WriteLine(ukr.ToString());
```

Окрему групу складають **керуючі послідовності** — спеціальні комбінації символів, що починаються зі зворотного слішу `\`. Вони інтерпретуються компілятором не як два символи, а як один спеціальний:

```csharp run
using System;

char newline = '\n'; // переклад рядка
char tab     = '\t'; // горизонтальна табуляція
char bslash  = '\\'; // зворотний сліш
char squote  = '\''; // одинарна лапка

Console.Write("Перший рядок");
Console.Write(newline);
Console.Write("Другий рядок");
Console.Write(newline);
Console.WriteLine("Рядок з\tтабуляцією");
```

Символи також можна визначати через шістнадцяткові коди ASCII, вказуючи після `\x` шістнадцятковий код символу:

```csharp run
using System;

Console.WriteLine('\x78'.ToString()); // x
Console.WriteLine('\x5A'.ToString()); // Z
```

Ще один спосіб — визначення через **коди Unicode**. Після `\u` вказується чотиризначний шістнадцятковий код символу з таблиці Unicode:

```csharp run
using System;

Console.WriteLine('Р'.ToString()); // Р (кирилиця)
Console.WriteLine('С'.ToString()); // С (кирилиця)
Console.WriteLine('I'.ToString()); // I (латиниця)
```

## Рядкові літерали

Рядкові літерали представляють рядки — послідовності символів. Рядок береться в **подвійні** лапки і відповідає типу `string`:

```csharp run
using System;

Console.WriteLine("hello");
Console.WriteLine("Привіт, світ!");
Console.WriteLine("hello world");
```

Якщо всередині рядка необхідно використати подвійну лапку, вона екранується зворотним слішем `\"`:

```csharp run
using System;

Console.WriteLine("Клініка \"Надія\" — міський медичний центр.");
```

У рядках також можна використовувати керуючі послідовності. Зокрема, `\n` здійснює перехід на новий рядок:

```csharp run
using System;

Console.WriteLine("Пацієнт: Іван Петренко\nВік: 45 р.\nДіагноз: Гіпертонія");
```

Якщо рядок містить багато зворотних слішів (наприклад, шляхи до файлів), зручно використовувати **verbatim-рядок** з префіксом `@`. У такому рядку зворотний сліш не є спеціальним символом і не потребує екранування:

```csharp run
using System;

string path1 = "C:\\Users\\Doctor\\Patients\\record.txt";  // звичайний рядок
string path2 = @"C:\Users\Doctor\Patients\record.txt";   // verbatim — те саме

Console.WriteLine(path1);
Console.WriteLine(path2);
```

Verbatim-рядок також може бути багаторядковим — переноси рядка всередині `@"..."` включаються у значення як є:

```csharp run
using System;

string record = @"Пацієнт: Марія Сидоренко
Вік: 38 р.
Діагноз: Бронхіт
Лікар: Коваль О.В.";

Console.WriteLine(record);
```

## null

Окремий літерал `null` представляє **відсутність посилання** — тобто посилання, яке не вказує на жодний об'єкт. По суті, `null` означає «немає значення» або «значення невідоме».

Значення `null` може бути присвоєне будь-якій змінній **reference-типу** — рядкам, масивам, об'єктам класів:

```csharp run
using System;

string middleName = null; // по батькові не вказано

if (middleName == null)
    Console.WriteLine("По батькові не вказано.");
else
    Console.WriteLine($"По батькові: {middleName}");
```

Спроба звернутися до члена або методу змінної, що містить `null`, спричинить виняток `NullReferenceException` під час виконання — одну з найпоширеніших помилок у програмуванні. Саме тому перевірка на `null` перед використанням є важливою звичкою.
