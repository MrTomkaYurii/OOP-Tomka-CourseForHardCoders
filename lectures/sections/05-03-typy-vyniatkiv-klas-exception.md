---
chapter: 5
chapterTitle: "Розділ 5. Обробка винятків"
section: 3
number: "5.3"
title: "Типи винятків. Клас Exception"
source: "../_combined/30-typy-vyniatkiv-klas-exception.md"
---

## 5.3. Типи винятків. Клас Exception

Базовим для всіх типів винятків є тип Exception. Цей тип визначає ряд властивостей, за допомогою яких можна отримати інформацію про виняток.

- `InnerException`: зберігає інформацію про виняток, що спричинило поточний виняток
- `Message`: зберігає повідомлення про виняток, текст помилки
- `Source`: зберігає ім'я об'єкта або складання, яке викликало виняток
- `StackTrace`: повертає рядкове представлення стека викликів, які призвели до винятку
- `TargetSite`: повертає метод, у якому було викликано виняток

Наприклад, обробимо винятки типу Exception:

```csharp
try
{
    int x = 5;
    int y = x / 0;
    Console.WriteLine($"Результат: {y}");
}
catch (Exception ex)
{
    Console.WriteLine($"Виняток: {ex.Message}");
    Console.WriteLine($"Метод: {ex.TargetSite}");
    Console.WriteLine($"Трасування стека: {ex.StackTrace}");
}
```

![Виведення властивостей винятку Exception](_assets/_docx/image93.png)

Однак так як тип Exception є базовим типом для всіх винятків, вираз `catch (Exception ex)` буде обробляти всі винятки, які можуть виникнути.

Але також є більш спеціалізовані типи винятків, які призначені для обробки певних видів винятків. Їх досить багато, я наведу лише деякі:

- `DivideByZeroException`: представляє виняток, що генерується при діленні на нуль
- `ArgumentOutOfRangeException`: генерується, якщо значення аргументу знаходиться поза діапазоном допустимих значень
- `ArgumentException`: генерується, якщо методу для параметра передається некоректне значення
- `IndexOutOfRangeException`: генерується, якщо індекс елемента масиву або колекції знаходиться поза діапазоном допустимих значень
- `InvalidCastException`: генерується при спробі зробити неприпустимі перетворення типів
- `NullReferenceException`: генерується при спробі звернення до об'єкта, який дорівнює null (тобто, по суті, невизначений)

І за потреби ми можемо розмежувати обробку різних типів винятків, увімкнувши додаткові блоки catch:

```csharp
static void Main(string[] args)
{
    try
    {
        int[] numbers = new int[4];
        numbers[7] = 9; // IndexOutOfRangeException

        int x = 5;
        int y = x / 0; // DivideByZeroException
        Console.WriteLine($"Результат: {y}");
    }
    catch (DivideByZeroException)
    {
        Console.WriteLine("Виник виняток DivideByZeroException");
    }
    catch (IndexOutOfRangeException ex)
    {
        Console.WriteLine(ex.Message);
    }

    Console.Read();
}
```

У цьому випадку блоки catch обробляють винятки типів IndexOutOfRangeException та DivideByZeroException. Коли у блоці try виникне виняток, то CLR шукатиме потрібний блок catch для обробки винятку. Так, у цьому випадку на рядку

```csharp
numbers[7] = 9;
```

відбувається звернення до 7 елементу масиву. Однак оскільки в масиві лише 4 елементи, ми отримаємо виняток типу IndexOutOfRangeException. CLR знайде блок catch, який обробляє цей виняток, і передасть йому керування.

Слід зазначити, що в даному випадку в блоці try є ситуація для генерації другого винятку - поділ на нуль. Однак оскільки після генерації IndexOutOfRangeException керування переходить у відповідний блок catch, то поділ на нуль `int y = x / 0` в принципі не виконуватиметься, тому виняток типу DivideByZeroException ніколи не буде згенеровано.

Однак розглянемо іншу ситуацію:

```csharp
try
{
    object obj = "you";
    int num = (int)obj; // System.InvalidCastException
    Console.WriteLine($"Результат: {num}");
}
catch (DivideByZeroException)
{
    Console.WriteLine("Виник виняток DivideByZeroException");
}
catch (IndexOutOfRangeException)
{
    Console.WriteLine("Виник виняток IndexOutOfRangeException");
}
```

В даному випадку в блоці try генерується виняток типу InvalidCastException, проте відповідного блоку catch для обробки цього винятку немає. Тому програма аварійно завершить виконання.

Ми також можемо визначити для InvalidCastException свій блок catch, проте суть у тому, що теоретично в коді можуть бути згенеровані різні типи винятків. А визначати для всіх типів винятків блоки catch, якщо обробка винятків однотипна, немає сенсу. І в цьому випадку ми можемо визначити блок catch для базового типу Exception:

```csharp
try
{
    object obj = "you";
    int num = (int)obj; // System.InvalidCastException
    Console.WriteLine($"Результат: {num}");
}
catch (DivideByZeroException)
{
    Console.WriteLine("Виник виняток DivideByZeroException");
}
catch (IndexOutOfRangeException)
{
    Console.WriteLine("Виник виняток IndexOutOfRangeException");
}
catch (Exception ex)
{
    Console.WriteLine($"Виняток: {ex.Message}");
}
```

І в даному випадку блок `catch (Exception ex) {}` буде обробляти всі винятки крім DivideByZeroException та IndexOutOfRangeException. При цьому блоки catch для більш загальних, базових винятків слід поміщати в кінці - після блоків catch для більш конкретних, спеціалізованих типів. Так як CLR вибирає для обробки виняток перший блок catch, який відповідає типу згенерованого винятку. Тому в даному випадку спочатку обробляється виняток DivideByZeroException та IndexOutOfRangeException, і тільки потім Exception (оскільки DivideByZeroException і IndexOutOfRangeException успадковуються від класу Exception).
