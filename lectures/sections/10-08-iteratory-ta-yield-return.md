---
chapter: 10
chapterTitle: "Розділ 10. Колекції"
section: 8
number: "10.8"
title: "Ітератори та yield return"
source: "../_combined/69-iteratory-ta-yield-return.md"
---

## 10.8. Ітератори та yield return

У розділі 10.7 ми побачили, що для реалізації `IEnumerable<T>` необхідно або написати окремий клас-перелічувач (`IEnumerator<T>`), або скористатися `yield return` у тілі `GetEnumerator()`. Другий варіант — набагато простіший і значно поширеніший на практиці.

`yield return` — це ключове слово, яке перетворює звичайний метод на **ітераторний метод**. Компілятор сам генерує клас-перелічувач з усіма необхідними полями та методами. Ви описуєте логіку обходу; C# будує машину стану.

## Синтаксис і базовий принцип

Метод вважається ітераторним, якщо:

1. Тип повернення — `IEnumerable<T>`, `IEnumerator<T>` або їхні негенерик-варіанти.
2. Тіло містить хоча б один `yield return` або `yield break`.

```csharp
IEnumerable<int> Sequence()
{
    yield return 1;
    yield return 2;
    yield return 3;
}
```

Кожен виклик `yield return` повертає один елемент і **призупиняє виконання**. При наступному виклику `MoveNext()` виконання відновлюється з тієї ж точки. `yield break` завершує ітерацію достроково.

## Ліниве виконання

Ключова властивість ітераторних методів: тіло методу **не виконується в момент виклику**. Воно запускається лише тоді, коли `foreach` або інший споживач запросить перший елемент.

![yield return — ліниве виконання ітератора](_assets/10-08/yield-lazy-execution.png)

```csharp
IEnumerable<string> GetActivePatients(List<Patient> all)
{
    Console.WriteLine("Початок перебору");  // виконається при першому MoveNext()
    foreach (var p in all)
        if (p.IsActive)
            yield return p.Name;            // пауза до наступного MoveNext()
    Console.WriteLine("Перебір завершено");
}

// Тут метод ще НЕ виконується:
var seq = GetActivePatients(patients);

// Тут починається фактичне виконання:
foreach (var name in seq)
    Console.WriteLine(name);
```

## yield return у GetEnumerator — runnable приклад

Найпоширеніший патерн: реалізація `IEnumerable<T>` без окремого класу-перелічувача. Клас `Department` фільтрує пацієнтів за статусом прямо в `GetEnumerator()`:

```csharp run
using System;
using System.Collections;
using System.Collections.Generic;

var dept = new Department("Хірургія");
dept.Add(new Patient("Петренко І.", active: true));
dept.Add(new Patient("Коваль М.",  active: false));
dept.Add(new Patient("Сидоренко О.", active: true));
dept.Add(new Patient("Мельник Г.", active: false));
dept.Add(new Patient("Гонта В.",   active: true));

Console.WriteLine("=== Активні пацієнти ===");
int count = 0;
foreach (var p in dept)
{
    count++;
    Console.WriteLine($"  {count}. {p.Name}");
}
Console.WriteLine($"Всього активних: {count}");

class Patient
{
    public string Name   { get; }
    public bool   Active { get; }
    public Patient(string name, bool active) { Name = name; Active = active; }
}

class Department : IEnumerable<Patient>
{
    private readonly List<Patient> _all = new();
    public string Name { get; }

    public Department(string name) { Name = name; }

    public void Add(Patient p) => _all.Add(p);

    public IEnumerator<Patient> GetEnumerator()
    {
        foreach (var p in _all)
            if (p.Active)
                yield return p;
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}
```

## yield return як самостійний метод — runnable приклад

`yield return` може бути у будь-якому методі з типом повернення `IEnumerable<T>`, не лише в `GetEnumerator()`. Це дозволяє будувати ланцюжки фільтрів і генераторів:

```csharp run
using System;
using System.Collections.Generic;

var patients = new List<Patient>
{
    new Patient("Петренко І.", dept: "Кардіологія", age: 67),
    new Patient("Коваль М.",   dept: "Неврологія",  age: 45),
    new Patient("Сидоренко О.",dept: "Кардіологія", age: 71),
    new Patient("Мельник Г.", dept: "Хірургія",    age: 38),
    new Patient("Гонта В.",   dept: "Кардіологія", age: 58),
};

Console.WriteLine("=== Кардіологія, вік 60+ ===");
foreach (var p in FilterByDeptAndAge(patients, "Кардіологія", 60))
    Console.WriteLine($"  {p.Name}, {p.Age} р.");

Console.WriteLine("\n=== Перші 3 пацієнти (yield break) ===");
foreach (var p in TakeFirst(patients, 3))
    Console.WriteLine($"  {p.Name}");

IEnumerable<Patient> FilterByDeptAndAge(
    IEnumerable<Patient> source, string dept, int minAge)
{
    foreach (var p in source)
        if (p.Department == dept && p.Age >= minAge)
            yield return p;
}

IEnumerable<Patient> TakeFirst(IEnumerable<Patient> source, int count)
{
    int i = 0;
    foreach (var p in source)
    {
        if (i >= count) yield break;
        yield return p;
        i++;
    }
}

class Patient
{
    public string Name       { get; }
    public string Department { get; }
    public int    Age        { get; }
    public Patient(string name, string dept, int age)
    { Name = name; Department = dept; Age = age; }
}
```

## Що компілятор генерує з yield return

`yield return` — це синтаксичний цукор. Компілятор перетворює ітераторний метод на клас-машину стану з полями для всіх локальних змінних та покажчиком поточного кроку:

```
Ваш код:
  IEnumerable<T> MyMethod() { yield return a; yield return b; }

Генерований код (спрощено):
  class MyMethod_StateMachine : IEnumerator<T>
  {
      int _state = 0;
      T   _current;

      bool MoveNext() {
          switch (_state) {
              case 0: _current = a; _state = 1; return true;
              case 1: _current = b; _state = 2; return true;
              default: return false;
          }
      }
      T Current => _current;
  }
```

Саме тому між двома `yield return` зберігається стан усіх локальних змінних: вони стають полями класу.

## yield return vs явний IEnumerator\<T\>

| Критерій | yield return | Явний IEnumerator\<T\> |
|----------|-------------|----------------------|
| Обсяг коду | Мінімальний | Значний (клас зі станом) |
| Читабельність | Висока | Середня |
| Повний контроль | Частковий | Повний (Reset, Dispose) |
| Ліниве виконання | Автоматично | Вручну |
| Коли використовувати | 95% випадків | Складні нестандартні сценарії |

## yield return та IEnumerable\<T\> — підсумок розділу 10

Раздел 10 охоплює повний ланцюжок від конкретних колекцій до абстракцій:

```
List<T>               — індексована, динамічна
LinkedList<T>         — двозв'язний список, O(1) вставка
Queue<T>              — FIFO-черга
Stack<T>              — LIFO-стек
Dictionary<K,V>       — хеш-таблиця
ObservableCollection  — з подією CollectionChanged
IEnumerable<T>        — контракт «можна перебрати foreach»
yield return          — генерує IEnumerator<T> без зайвого коду
```

Кожен рівень дає додатковий рівень абстракції: `foreach` не знає, що за нею стоїть — список у пам'яті, черга у БД чи генератор з `yield return`. Вона просто викликає `MoveNext()`.
