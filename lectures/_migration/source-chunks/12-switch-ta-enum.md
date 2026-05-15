# 2.23. Конструкція switch

Конструкція `switch/case` оцінює деякий вираз та порівнює його значення з набором значень. І при збігу значень виконує певний код.

Конструкція `switch` має таке формальне визначення:

```csharp
switch (вираз)
{
    case значення1:
        код, виконуваний якщо вираз має значення1
        break;
    case значення2:
        код, виконуваний якщо вираз має значення2
        break;
    //.............
    case значенняN:
        код, виконуваний якщо вираз має значення N
        break;
    default:
        код, який виконується, якщо вираз не має жодного з вищевказаних значень
        break;
}
```

Після ключового слова `switch` у дужках йде порівнюваний вираз. Значення цього виразу послідовно порівнюється зі значеннями, розміщеними після оператора `case`. І якщо збіг буде знайдено, виконуватиметься певний блок `case`.

Наприкінці кожного блоку `case` повинен ставитися один із операторів переходу: `break`, `goto case`, `return` або `throw`. Як правило, використовується оператор `break`. При його застосуванні інші блоки `case` не виконуватимуться.

Наприклад:

```csharp
string name = "Tom";

switch (name)
{
    case "Bob":
        Console.WriteLine("Ваше ім'я - Bob");
        break;
    case "Tom":
        Console.WriteLine("Ваше ім'я - Tom");
        break;
    case "Sam":
        Console.WriteLine("Ваше ім'я - Sam");
        break;
}
```

В даному випадку конструкція `switch` послідовно порівнює значення змінної `name` з набором значень, що вказані після операторів `case`. Оскільки тут значення змінної `name` - рядок `"Tom"`, то буде виконуватись блок

```csharp
case "Tom":
    Console.WriteLine("Ваше ім'я - Tom");
    break;
```

Відповідно ми побачимо на консолі

![Рисунок з оригінального документа](assets/docx/image39.png)

Якщо значення змінної `name` не збігається з жодним значенням після операторів `case`, то жоден з блоків `case` не виконується. Однак якщо навіть у цьому випадку нам все одно треба виконати якісь дії, то ми можемо додати в конструкцію `switch` необов'язковий блок `default`. Наприклад:

```csharp
string name = "Alex";

switch (name)
{
    case "Bob":
        Console.WriteLine("Ваше ім'я - Bob");
        break;
    case "Tom":
        Console.WriteLine("Ваше ім'я - Tom");
        break;
    case "Sam":
        Console.WriteLine("Ваше ім'я - Sam");
        break;
    default:
        Console.WriteLine("Невідоме ім'я");
        break;
}
```

В даному випадку жодне зі значень після операторів `case` не збігається зі значенням змінної `name`, тому буде виконуватися блок `default`:

```csharp
default:
    Console.WriteLine("Невідоме ім'я");
    break;
```

Однак якщо ми хочемо, щоб, навпаки, після виконання поточного блоку `case` виконувався інший блок `case`, то ми можемо використовувати замість `break` оператор `goto case`:

```csharp
int number = 1;
switch (number)
{
    case 1:
        Console.WriteLine("case 1");
        goto case 5; // Перехід до case 5
    case 3:
        Console.WriteLine("case 3");
        break;
    case 5:
        Console.WriteLine("case 5");
        break;
    default:
        Console.WriteLine("default");
        break;
}
```

## Повернення значення з switch

Конструкція `switch` дозволяє повертати деяке значення. Для повернення значення в блоках `case` може застосовуватись оператор `return`. Наприклад, визначимо наступний метод:

```csharp
int DoOperation(int op, int a, int b)
{
    switch (op)
    {
        case 1: return a + b;
        case 2: return a - b;
        case 3: return a * b;
        default: return 0;
    }
}
```

У метод `DoOperation()` передається числовий код операції та два операнди. Залежно від коду операції над операндами виконається певна операція та її результат повертається з методу. Для прикладу за умовчанням з методу повертається 0, якщо код операції не дорівнює 1, 2 або 3.

Потім ми можемо викликати цей метод:

```csharp
int DoOperation(int op, int a, int b)
{
    switch (op)
    {
        case 1: return a + b;
        case 2: return a - b;
        case 3: return a * b;
        default: return 0;
    }
}

int result1 = DoOperation(1, 10, 5); // 15
Console.WriteLine(result1);          // 15

int result2 = DoOperation(3, 10, 5); // 50
Console.WriteLine(result2);          // 50
```

## Отримання результату з switch

Хоча конструкція `switch` у прикладі вище чудово працює, проте ми її можемо скоротити і отримати результат безпосередньо з конструкції `switch`:

```csharp
int DoOperation(int op, int a, int b)
{
    int result = op switch
    {
        1 => a + b,
        2 => a - b,
        3 => a * b,
        _ => 0
    };
    return result;
}
```

Тепер не потрібен оператор `case`, а після порівнюваного значення ставиться оператор стрілка `=>`. Значення праворуч від стрілки виступає як значення, що повертається. Крім того, замість оператора `default` використовується підкреслення `_`. У результаті результат конструкції `switch` буде присвоюватися змінній `result`.

Природно, ми можемо відразу повернути з методу результат без надання змінної результату конструкції `switch`:

```csharp
int DoOperation(int op, int a, int b)
{
    return op switch
    {
        1 => a + b,
        2 => a - b,
        3 => a * b,
        _ => 0
    };
}
```

Або зробити метод ще коротшим:

```csharp
int DoOperation(int op, int a, int b) => op switch
{
    1 => a + b,
    2 => a - b,
    3 => a * b,
    _ => 0
};
```

Звертаю увагу, що це спрощення стосується лише таких конструкцій `switch`, які повертають деякі значення, як у прикладі вище.

Варто відзначити, що при поверненні значення методу, метод повинен у будь-якому випадку повертати значення. Наприклад, наступна версія методу не працюватиме:

```csharp
int DoOperation(int op, int a, int b)
{
    return op switch
    {
        1 => a + b,
        2 => a - b,
        3 => a * b
    };
}
```

Ця версія методу повертає значення, якщо код операції дорівнює 1, 2 або 3. Але що якщо буде передано значення 4 або якесь інше? Тому ця версія методу навіть не скомпілюється. Тому треба передбачити повернення значення з методу за всіх можливих варіантах. Тобто, ми можемо, як у прикладі вище, додати в конструкцію `switch` блок `default`, в якому повертатиметься значення при інших випадках.

# 2.24. Перерахування enum

Крім примітивних типів даних у мові програмування C# є такий тип як `enum` чи перерахування. Перерахування представляють набір логічно пов'язаних констант.

Оголошення перерахування відбувається за допомогою оператора `enum`:

```csharp
enum назва_перерахування
{
    // значення перерахування
    значення1,
    значення2,
    .......
    значенняN
}
```

Після оператора `enum` йде назва перерахування. І потім у фігурних дужках через кому перераховуються константи перерахування.

Визначимо найпростіше перерахування:

```csharp
enum DayTime
{
    Morning,
    Afternoon,
    Evening,
    Night
}
```

Тут визначено перелік `DayTime`, який має чотири значення: `Morning`, `Afternoon`, `Evening` і `Night`.

Кожне перерахування фактично визначає новий тип даних, за допомогою яких ми також, як і за допомогою іншого типу, можемо визначати змінні, константи, параметри методів і т.д. Як значення змінної, константи та параметра методу, які представляють перерахування, повинна виступати одна з констант цього перерахування, наприклад:

```csharp
const DayTime dayTime = DayTime.Morning;
```

Далі у програмі ми можемо використовувати подібні змінні/константи/параметри як і будь-які інші:

```csharp
DayTime dayTime = DayTime.Morning;

if (dayTime == DayTime.Morning)
    Console.WriteLine("Доброго ранку");
else
    Console.WriteLine("Привіт");

enum DayTime
{
    Morning,
    Afternoon,
    Evening,
    Night
}
```

## Зберігання стану

Найчастіше змінна перерахування виступає як сховище стану, залежно від якого виконуються деякі дії:

```csharp
DayTime now = DayTime.Evening;

PrintMessage(now); // Добрий вечір
PrintMessage(DayTime.Afternoon); // Добрий день
PrintMessage(DayTime.Night); // Доброї ночі

void PrintMessage(DayTime dayTime)
{
    switch (dayTime)
    {
        case DayTime.Morning:
            Console.WriteLine("Доброго ранку");
            break;
        case DayTime.Afternoon:
            Console.WriteLine("Доброго дня");
            break;
        case DayTime.Evening:
            Console.WriteLine("Добрий вечір");
            break;
        case DayTime.Night:
            Console.WriteLine("Добраніч");
            break;
    }
}

enum DayTime
{
    Morning,
    Afternoon,
    Evening,
    Night
}
```

Тут метод `PrintMessage()` як параметр приймає значення типу перерахування `DayTime` і залежно від цього значення виводить певне привітання.

Інший приклад:

```csharp
DoOperation(10, 5, Operation.Add);      // 15
DoOperation(10, 5, Operation.Subtract); // 5
DoOperation(10, 5, Operation.Multiply); // 50
DoOperation(10, 5, Operation.Divide);   // 2

void DoOperation(double x, double y, Operation op)
{
    double result = op switch
    {
        Operation.Add => x + y,
        Operation.Subtract => x - y,
        Operation.Multiply => x * y,
        Operation.Divide => x / y
    };
    Console.WriteLine(result);
}

enum Operation
{
    Add,
    Subtract,
    Multiply,
    Divide
}
```

Тут визначено перелік `Operation`, який представляє арифметичні операції. Кожен тип операцій визначено як одну з констант перерахування. І також визначено метод `DoOperation()`, який як параметри приймає два числа і тип операції у вигляді константи перерахування і в залежності від цього типу повертає з конструкції `switch` результат певної операції.

## Тип та значення констант перерахування

Константи переліку можуть мати тип. Тип вказується після назви перерахування через двокрапку:

```csharp
enum Time : byte
{
    Morning,
    Afternoon,
    Evening,
    Night
}
```

Тип перерахування обов'язково повинен представляти цілий тип (`byte`, `sbyte`, `short`, `ushort`, `int`, `uint`, `long`, `ulong`). Якщо тип явно не вказано, то за замовчуванням використовується тип `int`.

Тип впливає значення, які можуть мати константи. За замовчуванням кожному елементу перерахування надається ціле значення, причому перший елемент матиме значення 0, другий - 1 і так далі. Наприклад, візьмемо вище певне `DayTime`:

```csharp
DayTime now = DayTime.Morning;

Console.WriteLine((int)now); // 0
Console.WriteLine((int)DayTime.Night); // 3

enum DayTime
{
    Morning,
    Afternoon,
    Evening,
    Night
}
```

Ми можемо використовувати операцію приведення, щоб отримати ціле значення константи перерахування:

```csharp
(int)DayTime.Night // 3
```

У той же час, незважаючи на те, що кожна константа зіставляється з певним числом, ми не можемо надати їй числове значення:

```csharp
DayTime now = 2; // ! Помилка
```

Можна також явно вказати значення елементів, або вказавши значення першого елемента:

```csharp
enum DayTime
{
    Morning = 3, // кожен наступний елемент збільшується на 1
    Afternoon,  // цей елемент дорівнює 4
    Evening,    // 5
    Night       // 6
}
```

Але можна і для всіх елементів явно вказати значення:

```csharp
enum DayTime
{
    Morning = 2,
    Afternoon = 4,
    Evening = 8,
    Night = 16
}
```

При цьому константи перерахування можуть мати однакові значення, або навіть можна надавати одній константі значення іншої константи:

```csharp
enum DayTime
{
    Morning = 1,
    Afternoon = Morning,
    Evening = 2,
    Night = 2
}
```

