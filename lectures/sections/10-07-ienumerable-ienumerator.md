---
chapter: 10
chapterTitle: "Розділ 10. Колекції"
section: 7
number: "10.7"
title: "Інтерфейси IEnumerable<T> та IEnumerator<T>"
source: "../_combined/68-ienumerable-ienumerator.md"
---

## 10.7. Інтерфейси IEnumerable\<T\> та IEnumerator\<T\>

Щоразу, коли ви пишете `foreach (var p in ward)`, C# виконує певний контракт — звертається до колекції через стандартизовані інтерфейси. Цей контракт описується двома інтерфейсами: `IEnumerable<T>` і `IEnumerator<T>`.

Розуміння цих інтерфейсів пояснює, чому `foreach` однаково працює з масивом, `List<T>`, `Queue<T>`, `Dictionary<K,V>`, власним класом пацієнтів або лінивим генератором. Усі вони реалізують один і той самий контракт.

## Що компілятор робить з foreach

Конструкція `foreach` — синтаксичний цукор. Компілятор розгортає її у явний виклик методів перелічувача:

```csharp
// Що ви пишете:
foreach (var p in ward)
    Console.WriteLine(p);

// Що компілятор генерує:
var e = ward.GetEnumerator();
try
{
    while (e.MoveNext())
    {
        var p = e.Current;
        Console.WriteLine(p);
    }
}
finally
{
    e.Dispose();
}
```

Ці методи `GetEnumerator()`, `MoveNext()`, `Current`, `Dispose()` — і є контрактом двох інтерфейсів.

![IEnumerable<T> та IEnumerator<T> — як працює foreach](_assets/10-07/ienumerable-foreach-decomposition.png)

## Інтерфейс IEnumerable\<T\>

```csharp
public interface IEnumerable<out T> : IEnumerable
{
    IEnumerator<T> GetEnumerator();
}
```

`IEnumerable<T>` відповідає на одне питання: «дай мені перелічувач». Саме цей інтерфейс перевіряє компілятор, коли ви пишете `foreach`. Якщо об'єкт реалізує `IEnumerable<T>` — він допускається до `foreach`.

Реалізують: `List<T>`, `T[]`, `Queue<T>`, `Stack<T>`, `Dictionary<K,V>`, `ObservableCollection<T>`, `LinkedList<T>` та будь-який власний клас, якому ви додасте цей інтерфейс.

## Інтерфейс IEnumerator\<T\>

```csharp
public interface IEnumerator<out T> : IDisposable, IEnumerator
{
    bool MoveNext();    // перейти до наступного елемента
    T    Current { get; } // повернути поточний елемент
    void Reset();       // повернутись на початок (рідко використовується)
    void Dispose();     // звільнити ресурси
}
```

`IEnumerator<T>` — сам перелічувач. Він зберігає **поточну позицію** всередині колекції. Кожен виклик `MoveNext()` зсуває позицію на один крок і повертає `true`, поки є елементи; коли елементи вичерпані — повертає `false` і цикл `while` завершується.

## Власний IEnumerable\<T\> — runnable приклад

Щоб власний клас підтримував `foreach`, достатньо реалізувати `IEnumerable<T>`. Нижче — клас `Ward` (відділення), який перебирає тільки критичних пацієнтів:

```csharp run
using System;
using System.Collections;
using System.Collections.Generic;

var ward = new Ward("Кардіологія");
ward.AddPatient(new Patient("Петренко І.", severity: 1));
ward.AddPatient(new Patient("Коваль М.",  severity: 3));
ward.AddPatient(new Patient("Сидоренко О.", severity: 2));
ward.AddPatient(new Patient("Мельник Г.", severity: 3));

Console.WriteLine("=== Критичні пацієнти відділення ===");
foreach (var p in ward)
    Console.WriteLine($"  {p.Name} (рівень {p.Severity})");

class Patient
{
    public string Name { get; }
    public int Severity { get; }
    public Patient(string name, int severity) { Name = name; Severity = severity; }
}

class Ward : IEnumerable<Patient>
{
    private readonly List<Patient> _patients = new();
    public string Name { get; }

    public Ward(string name) { Name = name; }

    public void AddPatient(Patient p) => _patients.Add(p);

    // IEnumerable<Patient>: повертаємо тільки критичних (severity >= 2)
    public IEnumerator<Patient> GetEnumerator()
    {
        foreach (var p in _patients)
            if (p.Severity >= 2)
                yield return p;
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}
```

Зверніть увагу: всередині `GetEnumerator()` використовується `yield return` (детально — розділ 10.8). Це найпростіший спосіб реалізувати власний перелічувач без написання окремого класу.

## Явна реалізація IEnumerator\<T\> — runnable приклад

Для повного розуміння механізму — клас `RangeEnumerator`, який перебирає числа від `from` до `to` без зберігання їх у пам'яті:

```csharp run
using System;
using System.Collections;
using System.Collections.Generic;

// Перебираємо ліжко-місця відділення: 101..105
var beds = new BedRange(101, 105);
Console.WriteLine("Ліжко-місця кардіологічного відділення:");
foreach (var num in beds)
    Console.WriteLine($"  Палата {num}");

// Клас діапазону
class BedRange : IEnumerable<int>
{
    private readonly int _from;
    private readonly int _to;
    public BedRange(int from, int to) { _from = from; _to = to; }

    public IEnumerator<int> GetEnumerator() => new RangeEnumerator(_from, _to);
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}

// Перелічувач: стан зберігається у полі _current
class RangeEnumerator : IEnumerator<int>
{
    private readonly int _from;
    private readonly int _to;
    private int _current;

    public RangeEnumerator(int from, int to)
    {
        _from = from;
        _to = to;
        _current = from - 1; // до першого MoveNext()
    }

    public int  Current    => _current;
    object? IEnumerator.Current => _current;

    public bool MoveNext()
    {
        _current++;
        return _current <= _to;
    }

    public void Reset()   => _current = _from - 1;
    public void Dispose() { }
}
```

Цей приклад показує, що `IEnumerator<T>` — звичайний клас зі станом (`_current`). `MoveNext()` зсуває стан; `Current` повертає поточне значення. `foreach` просто викликає їх у потрібному порядку.

## Коли реалізувати IEnumerable\<T\>?

| Сценарій | Рішення |
|----------|---------|
| Власний клас-колекція | Реалізуйте `IEnumerable<T>` |
| Метод повертає послідовність | Використовуйте `yield return` (10.8) |
| Тільки читати чужу колекцію | Оголошуйте параметр як `IEnumerable<T>` |
| Потрібні індексація та `Count` | Використовуйте `IList<T>` або `List<T>` |

Параметр методу типу `IEnumerable<T>` замість `List<T>` — хороша практика: метод прийматиме масив, `List<T>`, `Queue<T>` та будь-яку іншу послідовність без змін.
