---
chapter: 6
chapterTitle: "Розділ 6. Делегати, події та лямбди"
section: 2
number: "6.2"
title: "Лямбди"
source: "../_combined/35-liambdy.md"
---

## 6.2. Лямбди

Лямбда-вираження представляють спрощений запис анонімних методів. Лямбда-вираження дозволяють створити ємні лаконічні методи, які можуть повертати деяке значення і які можна передати як параметри в інші методи.

Ламбда-вирази мають наступний синтаксис: ліворуч від лямбда-оператора => визначається список параметрів, а праворуч блок виразів, який використовує ці параметри:

```csharp
(список_параметрів) => вираз
```

З погляду типу даних лямбда-вираз представляє делегат. Наприклад, визначимо найпростіше лямбда-вираз:

```csharp
Message hello = () => Console.WriteLine("Hello");
hello(); // Hello
hello(); // Hello
hello(); // Hello
delegate void Message();
```

В даному випадку змінна hello представляє делегат Message - тобто деяка дія, яка нічого не повертає і не приймає жодних параметрів. Як значення цієї змінної надається лямбда-вираз. Цей лямбда-вираз має відповідати делегату Message – воно теж не приймає жодних параметрів, тому ліворуч від лямбда-оператора йдуть порожні дужки. А праворуч від лямбда-оператора йде вираз, що виконується - Console.WriteLine("Hello")

Потім у програмі можна викликати цю змінну як метод.

Якщо лямбда-вираз містить кілька дій, то вони поміщаються у фігурні дужки:

```csharp
Message hello = () =>
{
    Console.Write("Hello ");
    Console.WriteLine("World");
};
hello(); // Hello World
```

Вище ми визначили змінну hello, яка представляє делегат Message. Але починаючи з версії C# 10 ми можемо застосовувати неявну типізацію (визначення змінної за допомогою оператора var) щодо лямбда-виразу:

```csharp
var hello = () => Console.WriteLine("Hello");
hello(); // Hello
hello(); // Hello
hello(); // Hello
```

Але який тип у разі представляє змінна hello? При неявній типізації компілятор сам намагається зіставити лямбда-вираз з урахуванням його визначення з яким-небудь делегатом. Наприклад, вище визначений лямбда-вираз hello за замовчуванням компілятор буде розглядати як змінну вбудованого делегата Action, який не приймає жодних параметрів і нічого не повертає.

### Параметри лямбди

При визначенні списку параметрів ми можемо не вказувати їм тип даних:

```csharp
Operation sum = (x, y) => Console.WriteLine($"{x} + {y} = {x + y}");
sum(1, 2); // 1 + 2 = 3
sum(22, 14); // 22 + 14 = 36
delegate void Operation(int x, int y);
```

У даному випадку компілятор бачить, що лямбда-вираз sum є типом Operation, а значить обидва параметри лямбди представляють тип int. Тому жодних проблем не виникне.

Однак якщо ми застосовуємо неявну типізацію, то компілятор може мати труднощі, щоб вивести тип делегата для лямбда-вираження, наприклад, у наступному випадку

```csharp
var sum = (x, y) => Console.WriteLine($"{x} + {y} = {x + y}"); // ! Помилка
```

У цьому випадку можна вказати тип параметрів

```csharp
var sum = (int x, int y) => Console.WriteLine($"{x} + {y} = {x + y}");
sum(1, 2); // 1 + 2 = 3
sum(22, 14); // 22 + 14 = 36
```

Якщо лямбда має один параметр, для якого не потрібно вказувати тип даних, дужки можна опустити:

```csharp
PrintHandler print = message => Console.WriteLine(message);
print("Hello"); // Hello
print("Welcome"); // Welcome
delegate void PrintHandler(string message);
```

### Повернення результату

Лямбда-вираз може повертати результат. Результат, що повертається, можна вказати після лямбда-оператора:

```csharp
var sum = (int x, int y) => x + y;
int sumResult = sum(4, 5); // 9
Console.WriteLine(sumResult); // 9
Operation multiply = (x, y) => x * y;
int multiplyResult = multiply(4, 5); // 20
Console.WriteLine(multiplyResult); // 20
delegate int Operation(int x, int y);
```

Якщо лямбда-вираз містить кілька виразів, тоді потрібно використовувати оператор return, як у звичайних методах:

```csharp
var subtract = (int x, int y) =>
{
    if (x > y) return x - y;
    else return y - x;
};
int result1 = subtract(10, 6); // 4
Console.WriteLine(result1); // 4
int result2 = subtract(-10, 6); // 16
Console.WriteLine(result2); // 16
```

### Додавання та видалення дій у лямбда-виразі

Оскільки лямбда-вираз представляє делегат, той як і в делегат, змінну, яка представляє лямбда-вираз можна додавати методи та інші лямбди:

```csharp
var hello = () => Console.WriteLine("METANIT.COM");
var message = () => Console.Write("Hello ");
message += () => Console.WriteLine("World"); // додаємо анонімне лямбда-вираз
message += hello; // добавляем лямбда-выражение из переменной hello
message += Print; // додаємо метод
message();
Console.WriteLine("--------------"); // для поділу висновку
message -= Print; // видаляємо метод
message -= hello; // видаляємо лямбда-вираз зі змінної hello
message?.Invoke(); // на випадок, якщо у message більше немає дій
void Print() => Console.WriteLine("Welcome to C#");
```

### Лямбда-вираз як аргумент методу

Як і делегати, лямбда-вирази можна передавати параметрам методу, які представляють делегат:

```csharp
int[] integers = { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
// знайдемо суму чисел більше 5
int result1 = Sum(integers, x => x > 5);
Console.WriteLine(result1); // 30
// знайдемо суму парних чисел
int result2 = Sum(integers, x => x % 2 == 0);
Console.WriteLine(result2); //20
int Sum(int[] numbers, IsEqual func)
{
    int result = 0;
    foreach (int i in numbers)
    {
        if (func(i))
            result += i;
    }
    return result;
}
delegate bool IsEqual(int x);
```

Метод Sum приймає як параметр масив чисел і делегат IsEqual і повертає суму чисел масиву як об'єкта int. У циклі проходимо по всіх числах та складаємо їх. Причому складаємо лише ті числа, для яких делегат IsEqual func повертає true. Тобто делегат IsEqual тут фактично задає умову, якій мають відповідати значення масиву. Але на момент написання методу Sum нам невідомо, що це за умова.

При виклику методу Sum йому передається масив та лямбда-вираз:

```csharp
int result1 = Sum(integers, x => x > 5);
```

Тобто параметр x тут представлятиме число, яке передається в делегат:

```csharp
if (func(i))
```

А вираз x > 5 є умовою, якій має відповідати число. Якщо число відповідає цій умові, то лямбда-вираз повертає true, а передане число складається з іншими числами.

Подібним чином працює другий виклик методу Sum, тільки тут уже йде перевірка числа на парність, тобто якщо залишок від поділу на 2 дорівнює нулю:

```csharp
int result2 = Sum(integers, x => x % 2 == 0);
```

### Лямбда-вираз як результат методу

Метод також може повертати лямбда-вираз. У цьому випадку типом методу, що повертається, виступає делегат, якому відповідає лямбда-вираз, що повертається. Наприклад:

```csharp
Operation operation = SelectOperation(OperationType.Add);
Console.WriteLine(operation(10, 4)); // 14
operation = SelectOperation(OperationType.Subtract);
Console.WriteLine(operation(10, 4)); // 6
operation = SelectOperation(OperationType.Multiply);
Console.WriteLine(operation(10, 4)); // 40
Operation SelectOperation(OperationType opType)
{
    switch (opType)
    {
        case OperationType.Add: return (x, y) => x + y;
        case OperationType.Subtract: return (x, y) => x - y;
        default: return (x, y) => x * y;
    }
}

enum OperationType
{
    Add,
    Subtract,
    Multiply
}
```

В даному випадку метод SelectOperation() як параметр приймає перерахування типу OperationType. Цей перелік зберігає три константи, кожна з яких відповідає певній арифметичній операції. І в самому методі в залежності від значення параметра повертаємо певний лямбда-вираз.
