---
chapter: 3
chapterTitle: "Розділ 3. Класи, структури та простір імен"
section: 4
number: "3.4"
title: "Структури"
source: "../_combined/16-struktury.md"
---

## 3.4. Структури

Поряд із класами структури представляють ще один спосіб створення власних типів даних у C#. Більше того, багато примітивних типів — `int`, `double`, `bool` та інші — по суті є структурами, визначеними в стандартній бібліотеці .NET. Це не випадково: структури оптимізовані для зберігання невеликих, семантично цілісних наборів даних, які логічно утворюють одне значення. Наприклад, показник артеріального тиску складається з двох чисел — систолічного і діастолічного — і не має сенсу розглядати їх окремо. Саме такі дані найкраще представляти структурою.

Ключова відмінність структури від класу полягає в тому, що **структура є типом значення** (value type), а клас — **типом посилання** (reference type). Детально про цю різницю йтиметься у розділі 3.5, але вже зараз важливо розуміти: при копіюванні структури створюється повністю незалежна копія, тоді як при копіюванні посилання на клас обидві змінні вказують на один і той самий об'єкт у пам'яті.

## Визначення структури

Для визначення структури застосовується ключове слово `struct`:

```csharp
struct ім'я_структури
{
    // Елементи структури
}
```

Після слова `struct` йде назва структури і далі у фігурних дужках розміщуються елементи структури — поля, методи тощо. Як і класи, структури можуть зберігати стан як поля (змінні) і визначати поведінку як методи. Наприклад, визначимо структуру `BloodPressure`, яка представляє показник артеріального тиску пацієнта:

```csharp
struct BloodPressure
{
    public int systolic;   // систолічний тиск (верхній)
    public int diastolic;  // діастолічний тиск (нижній)

    public void Print()
    {
        Console.WriteLine($"Тиск: {systolic}/{diastolic} мм рт. ст.");
    }
}
```

Тут визначено два поля для зберігання показників тиску та метод `Print` для виведення результату на консоль. Для звернення до полів і методів структури застосовується точкова нотація — так само, як і для класів:

```csharp
об'єкт.поле_структури
об'єкт.метод_структури(параметри)
```

## Створення об'єкта структури

### Ініціалізація за допомогою конструктора

Для використання структури її необхідно ініціалізувати. Як і у випадку класів, для створення об'єктів структури застосовується виклик конструктора з оператором `new`. Навіть якщо в коді структури не визначено жодного конструктора, вона має щонайменше один — **конструктор за замовчуванням**, який генерується компілятором. Він не приймає параметрів і створює об'єкт зі значеннями за замовчуванням: `0` для числових полів і `null` для рядків.

```csharp run
using System;

BloodPressure bp = new BloodPressure(); // виклик конструктора за замовчуванням
// або: BloodPressure bp = new();

bp.systolic  = 120; // встановлюємо значення після створення
bp.diastolic = 80;

bp.Print(); // Тиск: 120/80 мм рт. ст.

struct BloodPressure
{
    public int systolic;
    public int diastolic;

    public void Print()
    {
        Console.WriteLine($"Тиск: {systolic}/{diastolic} мм рт. ст.");
    }
}
```

### Безпосередня ініціалізація полів

Якщо всі поля структури мають модифікатор `public`, структуру можна ініціалізувати без виклику конструктора — просто оголосивши змінну і надавши значення всім полям вручну перед першим використанням. Компілятор вимагає, щоб **усі поля були заповнені** до звернення до будь-якого з них або до методів структури. Якщо хоч одне поле залишиться неініціалізованим, компілятор видасть помилку.

```csharp run
using System;

BloodPressure bp; // конструктор не викликається
bp.systolic  = 130;
bp.diastolic = 85;

bp.Print(); // Тиск: 130/85 мм рт. ст.

struct BloodPressure
{
    public int systolic;
    public int diastolic;

    public void Print()
    {
        Console.WriteLine($"Тиск: {systolic}/{diastolic} мм рт. ст.");
    }
}
```

### Ініціалізація полів за замовчуванням

Починаючи з C# 10, поля структури можна ініціалізувати безпосередньо при їх визначенні — так само, як у класі. До C# 10 це було заборонено. Якщо ви використовуєте такі значення за замовчуванням, необхідно явно визначити й викликати конструктор без параметрів:

```csharp run
using System;

BloodPressure bp = new BloodPressure();
bp.Print(); // Тиск: 120/80 мм рт. ст.

struct BloodPressure
{
    public int systolic  = 120; // значення за замовчуванням, C# 10+
    public int diastolic = 80;

    public BloodPressure() { } // явний конструктор без параметрів обов'язковий

    public void Print() => Console.WriteLine($"Тиск: {systolic}/{diastolic} мм рт. ст.");
}
```

## Конструктори структури

Як і клас, структура може визначати власні конструктори з параметрами. Це дозволяє ініціалізувати об'єкт у момент створення, не заповнюючи поля вручну після `new`. Починаючи з C# 10, дозволено також визначати конструктор без параметрів явно:

```csharp run
using System;

BloodPressure bp1 = new BloodPressure();
BloodPressure bp2 = new BloodPressure(130, 85);

bp1.Print(); // Тиск: 120/80 мм рт. ст.
bp2.Print(); // Тиск: 130/85 мм рт. ст.

struct BloodPressure
{
    public int systolic;
    public int diastolic;

    public BloodPressure() // C# 10+: власний конструктор без параметрів
    {
        systolic  = 120;
        diastolic = 80;
    }

    public BloodPressure(int systolic, int diastolic)
    {
        this.systolic  = systolic;
        this.diastolic = diastolic;
    }

    public void Print() => Console.WriteLine($"Тиск: {systolic}/{diastolic} мм рт. ст.");
}
```

Варто зазначити: якщо в структурі є конструктор із параметрами, але немає явного конструктора без параметрів, то при виклику `new()` (без аргументів) все одно використовується автоматичний конструктор за замовчуванням — він встановлює всі поля в `0`/`null`, ігноруючи будь-які значення за замовчуванням, визначені в полях.

Конструктори структури можна також будувати в ланцюжок через `this(...)` — за тими самими правилами, що й для класів. Починаючи з C# 11, конструктор структури не зобов'язаний ініціалізувати всі поля явно, якщо ланцюжок гарантує їх заповнення:

```csharp run
using System;

BloodPressure bp1 = new BloodPressure();
BloodPressure bp2 = new BloodPressure(130);
BloodPressure bp3 = new BloodPressure(140, 90);

bp1.Print(); // Тиск: 120/80 мм рт. ст.
bp2.Print(); // Тиск: 130/80 мм рт. ст.
bp3.Print(); // Тиск: 140/90 мм рт. ст.

struct BloodPressure
{
    public int systolic;
    public int diastolic;

    public BloodPressure() : this(120, 80) {}
    public BloodPressure(int systolic) : this(systolic, 80) {}
    public BloodPressure(int systolic, int diastolic)
    {
        this.systolic  = systolic;
        this.diastolic = diastolic;
    }

    public void Print() => Console.WriteLine($"Тиск: {systolic}/{diastolic} мм рт. ст.");
}
```

## Ініціалізатор структури

Так само, як і для класу, можна використовувати синтаксис ініціалізатора для створення об'єкта структури. При цьому спочатку викликається конструктор без параметрів (явний або автоматичний), а потім вказаним полям надаються задані значення:

```csharp run
using System;

BloodPressure bp = new BloodPressure { systolic = 118, diastolic = 76 };
bp.Print(); // Тиск: 118/76 мм рт. ст.

struct BloodPressure
{
    public int systolic;
    public int diastolic;

    public void Print() => Console.WriteLine($"Тиск: {systolic}/{diastolic} мм рт. ст.");
}
```

## Копіювання структури за допомогою `with`

Коли потрібно створити новий об'єкт структури на основі існуючого, змінивши лише окремі поля, зручно використовувати оператор `with`. Він створює **копію** структури і застосовує до неї вказані зміни, не торкаючись оригіналу:

```csharp run
using System;

BloodPressure initial   = new BloodPressure { systolic = 120, diastolic = 80 };
BloodPressure elevated  = initial with { systolic = 145 };
BloodPressure crisis    = initial with { systolic = 180, diastolic = 110 };

initial.Print();  // Тиск: 120/80 мм рт. ст.
elevated.Print(); // Тиск: 145/80 мм рт. ст.
crisis.Print();   // Тиск: 180/110 мм рт. ст.

struct BloodPressure
{
    public int systolic;
    public int diastolic;

    public void Print() => Console.WriteLine($"Тиск: {systolic}/{diastolic} мм рт. ст.");
}
```

Тут об'єкт `elevated` отримує всі значення від `initial`, але з іншим систолічним тиском. Об'єкт `crisis` також базується на `initial`, але змінені обидва поля. При цьому `initial` лишається незмінним — оператор `with` ніколи не модифікує оригінал.

## Struct як тип значення: copy semantics

Саме тут проявляється принципова відмінність структури від класу. Коли ми присвоюємо одну структуру іншій, C# **копіює всі поля** — виникає два повністю незалежних об'єкти. Зміна одного не впливає на інший:

```csharp run
using System;

BloodPressure bp1 = new BloodPressure { systolic = 120, diastolic = 80 };
BloodPressure bp2 = bp1; // повна копія значень

bp2.systolic = 145; // змінюємо лише bp2

bp1.Print(); // Тиск: 120/80 мм рт. ст. — bp1 не змінився
bp2.Print(); // Тиск: 145/80 мм рт. ст.

struct BloodPressure
{
    public int systolic;
    public int diastolic;

    public void Print() => Console.WriteLine($"Тиск: {systolic}/{diastolic} мм рт. ст.");
}
```

Якби `BloodPressure` було класом, обидві змінні вказували б на один і той самий об'єкт у пам'яті — зміна `bp2.systolic` змінила б і `bp1.systolic`. Зі структурою цього не відбувається.

![Struct — тип значення: копіювання створює незалежний об'єкт](_assets/03-04/struct-copy-semantics.png)
