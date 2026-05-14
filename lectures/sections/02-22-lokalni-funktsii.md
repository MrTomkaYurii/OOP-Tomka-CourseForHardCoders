---
chapter: 2
chapterTitle: "Розділ 2. Основи програмування на C#"
section: 22
number: "2.22"
title: "Локальні функції"
source: "../_migration/source-chunks/11-rekursiia-ta-lokalni-funktsii.md"
---

## 2.22. Локальні функції

Локальні функції є функціями, визначеними всередині інших методів. Локальна функція, як правило, містить дії, що застосовуються лише у межах її методу.

Наприклад, визначимо метод, який порівнює суму чисел двох масивів:

```csharp
void Compare(int[] numbers1, int[] numbers2)
{
    int numbers1Sum = 0;
    int numbers2Sum = 0;

    foreach (int number in numbers1)
    numbers1Sum += number;

    foreach (int number in numbers2)
    numbers2Sum += number;

    if (numbers1Sum > numbers2Sum)
    Console.WriteLine("сума чисел з масиву numbers1 більше");
    else if (numbers1Sum < numbers2Sum)
    Console.WriteLine("сума чисел з масиву numbers2 більше");
    else
    Console.WriteLine("суми чисел обох масивів рівні");
}

int[] numbers1 = { 1, 2, 3 };
int[] numbers2 = { 3, 4, 5, 6, 7 };

Compare(numbers1, numbers2);
```

Тут метод `Compare` приймає два масиви і послідовно обчислює суму їх елементів, щоб дізнатися, у якому масиві сума чисел більше. Незважаючи на те, що все працює, тут є один недолік: тут повторюються дії, які обчислюють суму масиву:

```csharp
int numbers1Sum = 0;

foreach (int number in numbers1)
numbers1Sum += number;
```

До того ж що, якщо ми захочемо порівнювати суму лише позитивних чи парних чисел чи інакше змінити логіку порівняння? У цьому краще винести дії, що повторюються, в окремий метод. Однак, якщо ці дії ніде більше в програмі не будуть викликатися і будуть використовуватися тільки в одному методі, то доцільно визначити ці дії у вигляді локальної функції. Для цього змінимо метод `Compare` таким чином:

```csharp
void Compare(int[] numbers1, int[] numbers2)
{
    int numbers1Sum = Sum(numbers1);
    int numbers2Sum = Sum(numbers2);

    if (numbers1Sum > numbers2Sum)
    Console.WriteLine("сума чисел з масиву numbers1 більше");
    else if (numbers1Sum < numbers2Sum)
    Console.WriteLine("сума чисел з масиву numbers2 більше");
    else
    Console.WriteLine("суми чисел обох масивів рівні");

    int Sum(int[] numbers)
    {
        int result = 0;
        foreach (int number in numbers)
        result += number;
        return result;
    }
}

int[] numbers1 = { 1, 2, 3 };
int[] numbers2 = { 3, 4, 5, 6, 7 };

Compare(numbers1, numbers2);
```

Тут підрахунок суми винесений у локальну функцію `Sum`, яка приймає масив і повертає його суму. І далі в рамках методу `Compare` ми зможемо використовувати її для обчислення суми масиву. При цьому неважливо, чи визначена локальна функція до або після використання. Але поза її методом локальна функція не може використовуватись.

## Статичні локальні функції

Локальні функції можуть бути статичними. Такі функції визначаються за допомогою ключового слова `static`. Їх особливістю є те, що вони не можуть звертатися до змінних оточення, тобто методу, у якому статична функція визначена.

Спочатку визначимо локальну функцію, яка має оточення:

```csharp
int Sum(int[] numbers)
{
    int limit = 0;
    int result = 0;
    foreach (int number in numbers)
    {
        if (IsPassed(number)) result += number;
    }
    return result;

    bool IsPassed(int number)
    {
        return number > limit;
    }
}

int[] numbers1 = { -3, -2, -1, 0, 1, 2, 3 };
int[] numbers2 = { 3, -4, 5, -6, 7 };

Console.WriteLine(Sum(numbers1));
Console.WriteLine(Sum(numbers2));
```

Тут функція `Sum` обчислює суму чисел масиву, які відповідають умові локальної функції `IsPassed()`. Ця локальна функція перевіряє, чи більше передане число, ніж значення змінної `limit`, визначеної методом `Sum`. Тобто локальна функція `IsPassed` може звертатися до даних, визначених у навколишній функції `Sum`.

Тепер зробимо функцію `IsPassed` статичною:

```csharp
int Sum(int[] numbers)
{
    int result = 0;
    int limit = 0;
    foreach (int number in numbers)
    {
        if (IsPassed(number, limit)) result += number;
    }
    return result;

    static bool IsPassed(int number, int lim)
    {
        // return number > limit;
        // Помилка: метод IsPassed не має доступу до змінної limit
        return number > lim;
    }
}
```

Модифікатор `static` вказується перед типом локальної функції. Тепер функція `IsPassed` не може звертатися до змінної `limit`, і в цьому випадку нам треба або передати це значення у вигляді параметра, або визначити змінну `limit` безпосередньо в локальній функції.
