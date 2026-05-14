
## 13.2. Математичні обчислення та клас Math

Для виконання різних математичних операцій у бібліотеці класів .NET призначено клас `Math`. Він є статичним, тому всі його методи також статичні.

Розглянемо основні методи класу `Math`:

- `Abs(double value)`: повертає абсолютне значення аргументу `value`

```csharp
double result = Math.Abs(-12.4); // 12.4
```

- `Acos(double value)`: повертає арккосинус `value`. Параметр `value` повинен мати значення від -1 до 1

```csharp
double result = Math.Acos(1); // 0
```

- `Asin(double value)`: повертає арксинус `value`. Параметр `value` повинен мати значення від -1 до 1
- `Atan(double value)`: повертає арктангенс `value`
- `BigMul(int x, int y)`: повертає добуток `x * y` як об'єкт `long`

```csharp
long result = Math.BigMul(100, 9340); // 934000
```

- `Ceiling(double value)`: повертає найменше ціле число з плаваючою точкою, яке не менше за `value`

```csharp
double result = Math.Ceiling(2.34); // 3
```

- `Cos(double d)`: повертає косинус кута `d`
- `Cosh(double d)`: повертає гіперболічний косинус кута `d`
- `DivRem(int a, int b, out int result)`: повертає результат від поділу `a / b`, а залишок міститься у параметрі `result`

```csharp
int result;
int div = Math.DivRem(14, 5, out result);
// result = 4
// div = 2
```

- `Exp(double d)`: повертає основу натурального логарифму, зведену до степеня `d`
- `Floor(decimal d)`: повертає найбільше ціле число, яке не більше `d`

```csharp
double result = Math.Floor(2.56); // 2
```

- `IEEERemainder(double a, double b)`: повертає залишок від поділу `a` на `b`

```csharp
double result = Math.IEEERemainder(26, 4); // 2 = 26 - 24
```

- `Log(double d)`: повертає натуральний логарифм числа `d`
- `Log(double a, double newBase)`: повертає логарифм числа `a` на основі `newBase`
- `Log10(double d)`: повертає десятковий логарифм числа `d`
- `Max(double a, double b)`: повертає максимальне число з `a` та `b`
- `Min(double a, double b)`: повертає мінімальне число з `a` та `b`
- `Pow(double a, double b)`: повертає число `a`, зведене до степеня `b`
- `Round(double d)`: повертає число `d`, заокруглене до найближчого цілого числа

```csharp
double result1 = Math.Round(20.56); // 21
double result2 = Math.Round(20.46); // 20
```

- `Round(double a, int b)`: повертає число `a`, округлене до певної кількості знаків після коми, представленої параметром `b`

```csharp
double result1 = Math.Round(20.567, 2); // 20,57
double result2 = Math.Round(20.463, 1); // 20,5
```

- `Sign(double value)`: повертає число 1, якщо число `value` позитивне, -1, якщо значення `value` негативне. Якщо значення дорівнює 0, то повертає 0

```csharp
int result1 = Math.Sign(15); // 1
int result2 = Math.Sign(-5); // -1
```

- `Sin(double value)`: повертає синус кута `value`
- `Sinh(double value)`: повертає гіперболічний синус кута `value`
- `Sqrt(double value)`: повертає квадратний корінь числа `value`
- `Tan(double value)`: повертає тангенс кута `value`
- `Tanh(double value)`: повертає гіперболічний тангенс кута `value`
- `Truncate(double value)`: відкидає дрібну частину числа `value`, повертаючи лише ціле значення

```csharp
double result = Math.Truncate(16.89); // 16
```

Також клас `Math` визначає дві константи: `Math.E` та `Math.PI`. Наприклад, обчислимо площу кола:

```csharp
double radius = 50;
double area = Math.PI * Math.Pow(radius, 2);
Console.WriteLine($"Площа кола з радіусом {radius} дорівнює {Math.Round(area, 2)}");
```

Консольний вивід:

```text
Площа кола з радіусом 50 дорівнює 7853,98
```
