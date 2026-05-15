
## 13.3. Перетворення типів та клас Convert

### Методи Parse та TryParse

Усі примітивні типи мають два методи, які дозволяють перетворити рядок на цей тип. Це методи `Parse()` та `TryParse()`.

Метод `Parse()` як параметр приймає рядок та повертає об'єкт поточного типу. Наприклад:

```csharp
int a = int.Parse("10");
double b = double.Parse("23,56");
decimal c = decimal.Parse("12,45");
byte d = byte.Parse("4");
Console.WriteLine($"a={a}  b={b}  c={c}  d={d}");
```

Варто зазначити, що парсинг дробових чисел залежить від налаштувань поточної культури. Зокрема, для отримання числа `double` я передаю рядок `"23,56"` з комою як роздільник. Якби я передав крапку замість коми, то програма видала помилку виконання. На комп'ютерах з іншою локаллю, навпаки, використання коми замість крапки видало б помилку.

Щоб не залежати від культурних відмінностей, ми можемо встановити чіткий формат за допомогою класу `NumberFormatInfo` та його властивості `NumberDecimalSeparator`:

```csharp
using System.Globalization;

IFormatProvider formatter = new NumberFormatInfo { NumberDecimalSeparator = "." };
double number = double.Parse("23.56", formatter);
Console.WriteLine(number); // 23,56
```

У даному випадку як роздільник встановлюється точка. Однак, потенційно при використанні методу `Parse` ми можемо зіткнутися з помилкою, наприклад, при передачі алфавітних символів замість числових. І в цьому випадку вдалим вибором буде застосування методу `TryParse()`. Він намагається перетворити рядок до типу і якщо перетворення пройшло успішно, то повертає `true`. Інакше повертається `false`:

```csharp
Console.WriteLine("Введіть рядок:");
string? input = Console.ReadLine();

bool result = int.TryParse(input, out var number);
if (result == true)
    Console.WriteLine($"Перетворення пройшло успішно. Число: {number}");
else
    Console.WriteLine("Перетворення завершилося невдало");
```

Якщо перетворення пройде невдало, то виняток ніякого не буде викинуто, просто метод `TryParse` поверне `false`, а змінна `number` міститиме значення за замовчуванням.

### Convert

Клас `Convert` є ще одним способом для перетворення значень. Для цього в ньому визначено такі статичні методи:

- `ToBoolean(value)`
- `ToByte(value)`
- `ToChar(value)`
- `ToDateTime(value)`
- `ToDecimal(value)`
- `ToDouble(value)`
- `ToInt16(value)`
- `ToInt32(value)`
- `ToInt64(value)`
- `ToSByte(value)`
- `ToSingle(value)`
- `ToUInt16(value)`
- `ToUInt32(value)`
- `ToUInt64(value)`

Як параметр у ці методи може передаватися значення різних примітивних типів, необов'язково рядки:

```csharp
int n = Convert.ToInt32("23");
bool b = true;
double d = Convert.ToDouble(b);
Console.WriteLine($"n={n}  d={d}");
```

Однак знову ж таки, як і у випадку з методом `Parse`, якщо методу не вдасться перетворити значення до потрібного типу, він викидає виняток `FormatException`.
