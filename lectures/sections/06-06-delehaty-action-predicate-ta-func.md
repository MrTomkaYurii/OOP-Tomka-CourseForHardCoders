---
chapter: 6
chapterTitle: "Розділ 6. Делегати, події та лямбди"
section: 6
number: "6.6"
title: "Делегати Action, Predicate та Func"
source: "../_combined/38-delehaty-action-predicate-ta-func.md"
---

## 6.6. Делегати Action, Predicate та Func

У .NET є кілька вбудованих делегатів, які використовуються у різних ситуаціях. І найбільш використовуваними, з якими часто доводиться стикатися, є Action, Predicate та Func.

### Action

Делегат Action представляє деяку дію, яка нічого не повертає, тобто як тип, що повертається, має тип void:

```csharp
public delegate void Action()
public delegate void Action<in T>(T obj)
```

Цей делегат має ряд перевантажених версій. Кожна версія приймає різну кількість параметрів: від Action<in T1> до Action<in T1, in T2,....in T16>. Таким чином можна передати до 16 значень метод.

Як правило, цей делегат передається як параметр методу і передбачає виклик певних дій у відповідь на дії, що відбулися. Наприклад:

```csharp
DoOperation(10, 6, Add); // 10 + 6 = 16
DoOperation(10, 6, Multiply); // 10 * 6 = 60
void DoOperation(int a, int b, Action<int, int> op) => op(a, b);
void Add(int x, int y) => Console.WriteLine($"{x} + {y} = {x + y}");
void Multiply(int x, int y) => Console.WriteLine($"{x}*{y} = {x * y}");
```

### Predicate

Делегат Predicate приймає один параметр і повертає значення типу bool:

```csharp
delegate bool Predicate<in T>(T obj);
```

Як правило, використовується для порівняння, зіставлення деякого об'єкта T певною умовою. Як вихідний результат повертається значення true, якщо умова дотримана, і false, якщо не дотримано:

```csharp
Predicate<int> isPositive = (int x) => x > 0;
Console.WriteLine(isPositive(20));
Console.WriteLine(isPositive(-20));
```

У разі повертається true чи false залежно від цього, більше нуля число чи ні.

### Func

Ще одним поширеним делегатом є Func. Він повертає результат дії та може приймати параметри. Він також має різні форми: від Func<out T>(), де T - тип значення, що повертається, до Func<in T1, in T2,...in T16, out TResult>(), тобто може приймати до 16 параметрів .

```csharp
TResult Func<out TResult>()
TResult Func<in T, out TResult>(T arg)
TResult Func<in T1, in T2, out TResult>(T1 arg1, T2 arg2)
TResult Func<in T1, in T2, in T3, out TResult>(T1 arg1, T2 arg2, T3 arg3)
TResult Func<in T1, in T2, in T3, in T4, out TResult>(T1 arg1, T2 arg2, T3 arg3, T4 arg4)
```

Цей делегат також часто використовується як параметр у методах:

```csharp
int result1 = DoOperation(6, DoubleNumber); // 12
Console.WriteLine(result1);
int result2 = DoOperation(6, SquareNumber); // 36
Console.WriteLine(result2);
int DoOperation(int n, Func<int, int> operation) => operation(n);
int DoubleNumber(int n) => 2 * n;
int SquareNumber(int n) => n * n;
```

Метод DoOperation() як параметр приймає делегат Func<int, int>, тобто посилання на метод, який приймає число int і повертає значення int.

При першому виклику методу DoOperation() йому передається посилання метод DoubleNumber, який збільшує число вдвічі. У другому випадку передається метод SquareNumber - знову ж таки метод, який приймає параметр типу int і повертає результат у вигляді значення int.

Інший приклад:

```csharp
Func<int, int, string> createString = (a, b) => $"{a}{b}";
Console.WriteLine(createString(1, 5)); // 15
Console.WriteLine(createString(3, 5)); // 35
```

Тут змінна createString представляє лямбда-вираз, який приймає два числа int і повертає рядок, тобто представляє делегат Func<int, int, string>.

### Замикання

Замикання (closure) представляє об'єкт функції, який запам'ятовує своє лексичне оточення навіть у тому випадку, коли вона виконується поза своєю областю видимості.

Технічно замикання включає три компоненти:

- зовнішня функція, яка визначає деяку область видимості та в якій визначені деякі змінні та параметри - лексичне оточення
- змінні та параметри (лексичне оточення), які визначені у зовнішній функції
- вкладена функція, яка використовує змінні та параметри зовнішньої функції

У мові C# реалізувати замикання можна у різний спосіб - з допомогою локальних функцій і лямбда-виразів.

Розглянемо створення замикань через локальні функції:

```csharp
var fn = Outer(); // fn = Inner, оскільки метод Outer повертає функцію Inner
// викликаємо внутрішню функцію Inner
fn(); // 6
fn(); // 7
fn(); // 8
Action Outer() // метод або зовнішня функція
{
    int x = 5; // лексичне оточення - локальна змінна
    void Inner() // локальна функція
    {
        x++; // операції з лексичним оточенням
        Console.WriteLine(x);
    }
    return Inner; // повертаємо локальну функцію
}
```

Тут метод Outer як тип, що повертається, має тип Action, тобто метод повертає функцію, яка не приймає параметрів і має тип void.

```csharp
Action Outer()
```

Усередині методу Outer визначено змінну x - це і є лексичне оточення для внутрішньої функції:

```csharp
int x = 5;
```

Також усередині методу Outer визначено внутрішню функцію - локальну функцію Inner, яка звертається до свого лексичного оточення - змінної x - збільшує її значення на одиницю і виводить на консоль:

```csharp
void Inner()
{
    x++;
    Console.WriteLine(x);
}
```

Ця локальна функція повертається методом Outer:

```csharp
return Inner;
```

У програмі викликаємо метод Outer і отримуємо змінну fn локальну функцію Inner:

```csharp
var fn = Outer();
```

Змінна fn і є замиканням, тобто об'єднує дві речі: функцію і оточення, в якому функція була створена. І незважаючи на те, що ми отримали локальну функцію і можемо її викликати поза її методом, у якому вона визначена, проте вона запам'ятала своє лексичне оточення і може до нього звертатися та змінювати, що ми побачимо з консольного виводу:

```csharp
fn(); // 6
fn(); // 7
fn(); // 8
```

### Реалізація за допомогою лямбда-виразів

За допомогою лямбд можна скоротити визначення замикання:

```csharp
var outerFn = () =>
{
    int x = 10;
    var innerFn = () => Console.WriteLine(++x);
    return innerFn;
};
var fn = outerFn(); // fn = innerFn, тому що outerFn повертає innerFn
// викликаємо innerFn
fn(); // 11
fn(); // 12
fn(); // 13
```

### Застосування параметрів

Крім зовнішніх змінних до лексичного оточення також належать параметри навколишнього методу. Розглянемо використання параметрів:

```csharp
var fn = Multiply(5);
Console.WriteLine(fn(5)); // 25
Console.WriteLine(fn(6)); // 30
Console.WriteLine(fn(7)); // 35
```

```csharp
Operation Multiply(int n)
{
    int Inner(int m)
    {
        return n * m;
    }
    return Inner;
}
delegate int Operation(int n);
```

Тут зовнішня функція – метод Multiply повертає функцію, яка приймає число int та повертає число int. Для цього визначено делегат Operation, який представлятиме тип, що повертається:

```csharp
delegate int Operation(int n);
```

Хоча можна було б використовувати вбудований делегат Func<int, int>.

Виклик методу Multiply() повертає локальну функцію, яка відповідає сигнатурі делегата Operation:

```csharp
int Inner(int m)
{
    return n * m;
}
```

Ця функція запам'ятовує оточення, де вона була створена, зокрема, значення параметра n. Крім того, сама приймає параметр і повертає добуток параметрів n та m.

У результаті виклику методу Multiply визначається змінна fn, яка отримує локальну функцію Inner та її лексичне оточення - значення параметра n:

```csharp
var fn = Multiply(5);
```

У цьому разі параметр n дорівнює 5.

При виклику локальної функції, наприклад, у разі:

```csharp
Console.WriteLine(fn(6)); // 30
```

Число 6 передається для параметра m локальної функції, яка повертає добуток n та m, тобто 5*6 = 30.

Також можна було б скоротити весь цей код за допомогою лямбд:

```csharp
var multiply = (int n) => (int m) => n * m;
var fn = multiply(5);
Console.WriteLine(fn(5)); // 25
Console.WriteLine(fn(6)); // 30
Console.WriteLine(fn(7)); // 35
```
