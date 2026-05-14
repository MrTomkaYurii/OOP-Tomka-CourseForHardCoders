---
chapter: 10
chapterTitle: "Розділ 10. Колекції"
section: 7
number: "10.7"
title: "Інтерфейси IEnumerable та IEnumerator"
source: "../_combined/68-interfeisy-ienumerable-ta-ienumerator.md"
---

## 10.7. Інтерфейси IEnumerable та IEnumerator

Як ми побачили, основою для більшості колекцій є реалізація інтерфейсів `IEnumerable` та `IEnumerator`. Завдяки такій реалізації ми можемо перебирати об'єкти в циклі `foreach`:

```csharp
foreach (var item in перерахований_об'єкт)
{
}
```

Колекція, що перебирається, повинна реалізувати інтерфейс `IEnumerable`.

Інтерфейс `IEnumerable` має метод, що повертає посилання на інший інтерфейс.

```csharp
public interface IEnumerable
{
    IEnumerator GetEnumerator();
}
```

А інтерфейс `IEnumerator` визначає функціонал для перебору внутрішніх об'єктів у контейнері:

```csharp
public interface IEnumerator
{
    bool MoveNext(); // переміщення на одну позицію вперед у контейнері елементів
    object Current { get; } // поточний елемент у контейнері
    void Reset(); // переміщення на початок контейнера
}
```

Метод `MoveNext()` переміщує покажчик на поточний елемент на наступну позицію в послідовності. Якщо послідовність ще не закінчилася, то повертає `true`. Якщо послідовність закінчилася, то повертається `false`.

Властивість `Current` повертає об'єкт у послідовності, на який вказує покажчик.

Метод `Reset()` скидає покажчик позиції в початкове положення.

Яким чином буде здійснюватися переміщення покажчика та отримання елементів залежить від реалізації інтерфейсу. У різних реалізаціях логіка може бути побудована по-різному.

Наприклад, без використання циклу `foreach` переберемо масив за допомогою інтерфейсу `IEnumerator`:

```csharp
using System.Collections;

string[] people = { "Tom", "Sam", "Bob" };

IEnumerator peopleEnumerator = people.GetEnumerator(); // отримуємо IEnumerator
while (peopleEnumerator.MoveNext()) // доки не буде повернуто false
{
    string item = (string)peopleEnumerator.Current; // отримуємо елемент на поточній позиції
    Console.WriteLine(item);
}

peopleEnumerator.Reset(); // скидаємо покажчик на початок масиву
```

### Реалізація IEnumerable та IEnumerator

Розглянемо просту реалізацію `IEnumerable` на прикладі:

```csharp
using System.Collections;

Week week = new Week();
foreach (var day in week)
{
    Console.WriteLine(day);
}

class Week : IEnumerable
{
    string[] days =
    {
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    };

    public IEnumerator GetEnumerator() => days.GetEnumerator();
}
```

У цьому випадку клас `Week`, який представляє тиждень і зберігає всі дні тижня, реалізує інтерфейс `IEnumerable`. Однак у цьому випадку ми вчинили дуже просто - замість реалізації `IEnumerator` ми просто повертаємо в методі `GetEnumerator` об'єкт `IEnumerator` для масиву.

```csharp
public IEnumerator GetEnumerator() => days.GetEnumerator();
```

Завдяки цьому ми можемо перебрати всі дні тижня у циклі `foreach`.

У той самий час слід зазначити, що для перебору колекції через `foreach` у принципі необов'язково реалізувати інтерфейс `IEnumerable`. Досить у класі визначити публічний метод `GetEnumerator`, який би повертав об'єкт `IEnumerator`. Наприклад:

```csharp
class Week
{
    string[] days =
    {
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    };

    public IEnumerator GetEnumerator() => days.GetEnumerator();
}
```

Однак це було досить просто - ми просто використовуємо вже готовий перелічувач масиву. Однак, можливо, потрібно буде задати свою власну логіку перебору об'єктів. Для цього реалізуємо інтерфейс `IEnumerator`:

```csharp
using System.Collections;

class WeekEnumerator : IEnumerator
{
    string[] days;
    int position = -1;

    public WeekEnumerator(string[] days) => this.days = days;

    public object Current
    {
        get
        {
            if (position == -1 || position >= days.Length)
            {
                throw new ArgumentException();
            }

            return days[position];
        }
    }

    public bool MoveNext()
    {
        if (position < days.Length - 1)
        {
            position++;
            return true;
        }
        else
        {
            return false;
        }
    }

    public void Reset() => position = -1;
}

class Week
{
    string[] days =
    {
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    };

    public IEnumerator GetEnumerator() => new WeekEnumerator(days);
}
```

Тут тепер клас `Week` використовує не вбудований перелічувач, а `WeekEnumerator`, який реалізує `IEnumerator`.

Ключовий момент при реалізації перелічувача - переміщення покажчика на елемент. У класі `WeekEnumerator` для зберігання поточної позиції визначено змінну `position`. Слід враховувати, що на самому початку (у вихідному стані) покажчик повинен вказувати на позицію перед першим елементом. Коли буде проводитися цикл `foreach`, цей цикл спочатку викликає метод `MoveNext` і фактично переміщає покажчик однією позицією вперед і лише потім звертається до властивості `Current`, щоб одержати елемент у поточній позиції.

Потім у програмі ми можемо аналогічно перебирати об'єкт `Week` за допомогою циклу `foreach`:

```csharp
Week week = new Week();
foreach (var day in week)
{
    Console.WriteLine(day);
}
```

### Узагальнена версія IEnumerator

У прикладах вище використовувалися неузагальнені версії інтерфейсів, проте ми також можемо використовувати їх узагальнені двійники:

```csharp
using System.Collections;

class WeekEnumerator : IEnumerator<string>
{
    string[] days;
    int position = -1;

    public WeekEnumerator(string[] days) => this.days = days;

    public string Current
    {
        get
        {
            if (position == -1 || position >= days.Length)
            {
                throw new ArgumentException();
            }

            return days[position];
        }
    }

    object IEnumerator.Current => Current;

    public bool MoveNext()
    {
        if (position < days.Length - 1)
        {
            position++;
            return true;
        }
        else
        {
            return false;
        }
    }

    public void Reset() => position = -1;

    public void Dispose() { }
}

class Week
{
    string[] days =
    {
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    };

    public IEnumerator<string> GetEnumerator() => new WeekEnumerator(days);
}
```

У цьому разі реалізуємо інтерфейс `IEnumerator<string>`, відповідно у властивості `Current` нам треба повернути об'єкт `string`. У цьому випадку при переборі в циклі `foreach` об'єкти, що перебираються, будуть автоматично представляти тип `string`:

```csharp
Week week = new Week();
foreach (string day in week)
{
    Console.WriteLine(day);
}
```
