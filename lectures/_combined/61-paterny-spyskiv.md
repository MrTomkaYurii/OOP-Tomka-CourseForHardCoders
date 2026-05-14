
## 9.6. Патерни списків

Патерни списків (list pattern) дозволяють зіставляти вирази зі списками та масивами. Цей патерн поки що доступний в Preview-версії C# 11.

Повний збіг з масивом/списком:

```csharp
Console.WriteLine(GetNumber(new[] { 1, 2, 3, 4, 5 }));  // 1
Console.WriteLine(GetNumber(new[] { 1, 2 }));           // 3
Console.WriteLine(GetNumber(new int[] { }));            // 4
Console.WriteLine(GetNumber(new[] { 1, 2, 5 }));        // 5

int GetNumber(int[] values) => values switch
{
    [1, 2, 3, 4, 5] => 1,
    [1, 2, 3] => 2,
    [1, 2] => 3,
    [] => 4,
    _ => 5
};
```

Аналогічно замість масивів можна використовувати списки:

```csharp
List<int> numbers = new List<int> { 1, 2, 3 };

Console.WriteLine(GetNumber(numbers));  // 2

int GetNumber(List<int> values) => values switch
{
    [1, 2, 3, 4, 5] => 1,
    [1, 2, 3] => 2,
    [1, 2] => 3,
    [] => 4,
    _ => 5
};
```

Аналогічно патерни списків можна використовувати в конструкції if:

```csharp
int[] numbers = { 1, 2, 3, 4, 5 };
if (numbers is [1, 2, 3, 4, 5])
{
    Console.WriteLine("[1, 2, 3, 4, 5]");
}
```

### Підстановка _

За допомогою патерну можна позначити одиночний елемент, який має будь-яке значення. Наприклад, патерн [2, _, 5] відповідає будь-якому масиву з трьох елементів, в якому між 2 і 5 розташовується довільне значення. А масив [_, _] відповідає будь-якому масиву із двох довільних елементів

Декілька прикладів:

```csharp
Console.WriteLine(GetNumber(new[] { 2, 3, 5 }));      // 1
Console.WriteLine(GetNumber(new[] { 2, 4, 6 }));      // 2
Console.WriteLine(GetNumber(new[] { 1, 2, 5 }));      // 3
Console.WriteLine(GetNumber(new[] { 1, 2, 3 }));      // 4
Console.WriteLine(GetNumber(new int[] { }));          // 5

int GetNumber(int[] values) => values switch
{
    [2, _, 5] => 1,
    [2, _, _] => 2,
    [_, _, 5] => 3,
    [_, _, _] => 4,
    _ => 5
};
```

### Slice-патерн

Для передачі довільної кількості елементів масиву/списку застосовується slice-патерн `..`. Наприклад, патерн [1, 2, .., 5] відповідає масиву, який починається на 1, за яким йде 2. А останній елемент в масиві - 5. При цьому між 2 і 5 може розташовуватися довільна кількість довільних цілих чисел. Тобто патерн [1, 2, .., 5] буде відповідати таким масивам як

```csharp
int[] arr1 = { 1, 2, 3, 4, 5 };
int[] arr2 = { 1, 2, 5 };
int[] arr3 = { 1, 2, 66, 77, 88, 5 };
```

За допомогою патерна `..` можна задавати довільну кількість елементів як на початку, так і наприкінці масиву/списку. Наприклад, патерн [2, ..] представляє масив, який починається на 2. А патерн [.., 5] представляє масив, який закінчується елементом 5. Патерн [..] представляє масив, який містить довільну кількість елементів. Наприклад:

```csharp
int[] arr1 = { 1, 2, 3, 4, 5 };
Console.WriteLine(GetNumber(new[] { 2, 5 }));       // 1
Console.WriteLine(GetNumber(new[] { 2, 3, 4, 5 })); // 1

Console.WriteLine(GetNumber(new[] { 2 }));          // 2
Console.WriteLine(GetNumber(new[] { 2, 3, 4 }));    // 2

Console.WriteLine(GetNumber(new[] { 3, 4, 5 }));    // 3
Console.WriteLine(GetNumber(new[] { 5 }));          // 3

Console.WriteLine(GetNumber(new int[] { }));        // 4
Console.WriteLine(GetNumber(new[] { 1 }));          // 4
Console.WriteLine(GetNumber(new[] { 1, 2, 3 }));    // 4

int GetNumber(int[] values) => values switch
{
    [2, .., 5] => 1, // якщо перший елемент - 2, а останній - 5
    [2, ..] => 2,   // якщо перший елемент - 2
    [.., 5] => 3,   // якщо останній елемент - 5
    [..] => 4       // довільна кількість елементів
};
```

Slice-патерн можна поєднувати з символом підстановки _, наприклад:

```csharp
int GetNumber(int[] values) => values switch
{
    [_, .., _] => 1,
    [..] => 2
};
```

В даному випадку патерн [_, .., _] передбачає масив, який складається як мінімум з двох довільних елементів, і між першим і останнім елементом може бути довільна кількість інших елементів:

```csharp
Console.WriteLine(GetNumber(new[] { 1, 2, 3, 4 })); // 1
Console.WriteLine(GetNumber(new[] { 1, 2, 3 }));    // 1
Console.WriteLine(GetNumber(new[] { 1, 2 }));       // 1
Console.WriteLine(GetNumber(new[] { 1 }));          // 2
Console.WriteLine(GetNumber(new int[] { }));        // 2

int GetNumber(int[] values) => values switch
{
    [_, .., _] => 1,
    [..] => 2
};
```

### Отримання елементів у змінні

Окремі значення масиву/списку можна отримати у змінні, наприклад:

```csharp
int[] numbers = { 2, 3, 5 };
if (numbers is [var first, var second, .., var last])
{
    Console.WriteLine($"first: {first}, second: {second}  last: {last}");
}
```

В даному випадку отримуємо перший елемент масиву у змінну first, другий елемент - у змінну second, а останній елемент - у змінну last.

Приклад із різними масивами:

```csharp
Console.WriteLine(GetData(new[] { 1, 2, 3 }));      // First: 1  Second: 2  Last: 3
Console.WriteLine(GetData(new[] { 2, 4, 6, 8 }));   // First: 2  Second: 4  Last: 8
Console.WriteLine(GetData(new[] { 1, 2 }));         // Array has less than 3 elements

string GetData(int[] values) => values switch
{
    [var first, var second, .., var last] => $"First: {first}  Second: {second}  Last: {last}",
    [..] => "Array has less than 3 elements"
};
```

В даному випадку отримуємо перший елемент масиву у змінну first, другий елемент - у змінну second, а останній елемент - у змінну last.

При цьому значення, які проектуються на патерн `..`, також можна отримати у змінну. Наприклад, у патерні [2, .. var middle, 5] елементи, які проектуються на `..`, передаються у змінну middle. Декілька прикладів:

```csharp
Console.WriteLine(GetSlice(new[] { 2, 3, 4, 5 }));  // Middle: 3, 4
Console.WriteLine(GetSlice(new[] { 2, 4, 6, 8 }));  // End: 4, 6, 8
Console.WriteLine(GetSlice(new[] { 1, 2, 3, 5 }));  // Start: 1, 2, 3
Console.WriteLine(GetSlice(new[] { 1, 2, 3, 4 }));  // All: 1, 2, 3, 4
Console.WriteLine(GetSlice(new int[] { }));         // All:

string GetSlice(int[] values) => values switch
{
    [2, .. var middle, 5] => $"Middle: {string.Join(", ", middle)}",
    [2, .. var end] => $"End: {string.Join(", ", end)}",
    [.. var start, 5] => $"Start: {string.Join(", ", start)}",
    [.. var all] => $"All: {string.Join(", ", all)}"
};
```

### Властивості колекцій

Варто зазначити, що оскільки масиви та списки - звичайні класи C#, які мають властивості, то для них ми також можемо застосовувати патерн властивостей. Поєднання патерну властивостей і патерну списків дозволяє спростити вирішення деяких завдань. Наприклад, у нас є завдання: якщо масив має три елементи, то розкласти його на три змінні:

```csharp
int[] numbers = { 2, 3, 5 };
if (numbers is { Length: 3 } and [var first, var second, var third])
{
    Console.WriteLine($"first: {first}, second: {second}  third: {third}");
}
```
