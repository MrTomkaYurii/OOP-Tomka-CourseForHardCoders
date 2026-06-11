---
chapter: 10
chapterTitle: "Розділ 10. Колекції"
section: 6
number: "10.6"
title: "Клас ObservableCollection<T>"
source: "../_combined/67-klas-observablecollection.md"
---

## 10.6. Клас ObservableCollection\<T\>

`List<T>`, `Queue<T>`, `Dictionary<K,V>` — всі ці колекції ефективно зберігають і організовують дані. Але жодна з них **не повідомляє** зовнішній код про те, що щось змінилось. Якщо хтось додав пацієнта до списку — UI-компонент, що відображає цей список, нічого про це не знатиме і не перемалює себе.

Клас `ObservableCollection<T>` з простору імен `System.Collections.ObjectModel` вирішує саме цю задачу. За своїми методами він ідентичний `List<T>` (індексований доступ, `Add`, `Remove`, `Insert`, `Move`), але кожна зміна колекції генерує **подію `CollectionChanged`**. Будь-який підписник може відреагувати: перемалювати UI, зберегти лог, синхронізувати стан.

`ObservableCollection<T>` є базою для прив'язки даних у WPF, MAUI, Xamarin. Якщо ви прив'язуєте колекцію до `ListView` чи `DataGrid` — майже завжди потрібна саме `ObservableCollection<T>`.

## Внутрішня структура: подія CollectionChanged

При кожній зміні `ObservableCollection<T>` генерує подію `CollectionChanged` і передає підписникам об'єкт `NotifyCollectionChangedEventArgs`, де зберігається:

- `Action` — тип зміни: `Add`, `Remove`, `Replace`, `Move`, `Reset`.
- `NewItems` — список доданих або нових елементів (для `Add`, `Replace`).
- `OldItems` — список видалених або замінених елементів (для `Remove`, `Replace`).

![ObservableCollection<T> — сповіщення про зміни](_assets/10-06/observablecollection-event-flow.png)

## Створення та ініціалізація

```csharp
using System.Collections.ObjectModel;

// Порожня колекція
ObservableCollection<string> ward = new ObservableCollection<string>();

// З масиву
var fromArray = new ObservableCollection<string>(new[] { "Петренко", "Коваль" });

// Через ініціалізатор
var fromInit = new ObservableCollection<string>
{
    "Петренко І.",
    "Коваль М.",
    "Сидоренко О."
};
```

## Доступ до елементів та методи

`ObservableCollection<T>` надає ті самі операції, що й `List<T>`:

```csharp
var patients = new ObservableCollection<string> { "Петренко І.", "Коваль М." };

// Доступ за індексом
Console.WriteLine($"Перший: {patients[0]}");

// Зміна елемента за індексом (генерує Replace)
patients[0] = "Петренко Іван Степанович";

// Перебір
foreach (var p in patients)
    Console.WriteLine(p);
```

**Повний перелік методів:**

| Метод | Що робить |
|-------|-----------|
| `Add(item)` | Додати в кінець |
| `Insert(index, item)` | Вставити за індексом |
| `Remove(item)` | Видалити перше входження |
| `RemoveAt(index)` | Видалити за індексом |
| `Move(oldIndex, newIndex)` | Перемістити елемент на нову позицію |
| `Clear()` | Очистити (генерує Reset) |
| `Contains(item)` | Перевірити наявність |
| `IndexOf(item)` | Індекс першого входження |
| `CopyTo(array, index)` | Скопіювати в масив |

Метод `Move` — унікальна особливість `ObservableCollection<T>`, якої немає в `List<T>`. Він переміщує елемент і генерує подію `Move`, що дозволяє UI-компонентам правильно анімувати переупорядкування.

## Підписка на CollectionChanged — runnable приклад

Базовий сценарій: відстежуємо всі зміни списку пацієнтів у відділенні:

```csharp run
using System;
using System.Collections.ObjectModel;
using System.Collections.Specialized;

var ward = new ObservableCollection<string>
{
    "Петренко І.",
    "Коваль М."
};

// Підписка на подію
ward.CollectionChanged += (sender, e) =>
{
    switch (e.Action)
    {
        case NotifyCollectionChangedAction.Add:
            Console.WriteLine($"  [+] Надійшов: {e.NewItems?[0]}");
            break;
        case NotifyCollectionChangedAction.Remove:
            Console.WriteLine($"  [-] Виписано: {e.OldItems?[0]}");
            break;
        case NotifyCollectionChangedAction.Replace:
            Console.WriteLine($"  [~] Замінено: {e.OldItems?[0]} -> {e.NewItems?[0]}");
            break;
        case NotifyCollectionChangedAction.Move:
            Console.WriteLine($"  [m] Переміщено: {e.OldItems?[0]}");
            break;
        case NotifyCollectionChangedAction.Reset:
            Console.WriteLine($"  [!] Список очищено");
            break;
    }
};

Console.WriteLine("=== Зміни у відділенні ===");
ward.Add("Сидоренко О.");
ward.Add("Мельник Г.");
ward.Remove("Коваль М.");
ward[0] = "Петренко Іван Степанович";
ward.Move(1, 0);
ward.Clear();

Console.WriteLine($"\nПалата: {ward.Count} пацієнтів");
```

## Відстеження з об'єктами Patient — runnable приклад

Розширений приклад з класом: журналюємо кожну зміну складу відділення:

```csharp run
using System;
using System.Collections.ObjectModel;
using System.Collections.Specialized;

// Виконуваний код
var patients = new ObservableCollection<Patient>();

patients.CollectionChanged += WardChanged;

patients.Add(new Patient("Петренко Іван",  "кардіологія"));
patients.Add(new Patient("Коваль Марія",   "неврологія"));
patients.Add(new Patient("Сидоренко Олег", "хірургія"));

patients.RemoveAt(1);

patients[0] = new Patient("Петренко Іван Степанович", "кардіологія");

Console.WriteLine("\n=== Поточний склад відділення ===");
for (int i = 0; i < patients.Count; i++)
    Console.WriteLine($"  {i+1}. {patients[i]}");

void WardChanged(object? sender, NotifyCollectionChangedEventArgs e)
{
    switch (e.Action)
    {
        case NotifyCollectionChangedAction.Add:
        {
            if (e.NewItems?[0] is Patient p)
                Console.WriteLine($"[Прийом]  {p.Name} ({p.Department})");
            break;
        }
        case NotifyCollectionChangedAction.Remove:
        {
            if (e.OldItems?[0] is Patient p)
                Console.WriteLine($"[Виписка] {p.Name}");
            break;
        }
        case NotifyCollectionChangedAction.Replace:
        {
            if (e.OldItems?[0] is Patient old && e.NewItems?[0] is Patient newPat)
                Console.WriteLine($"[Оновлення] {old.Name} -> {newPat.Name}");
            break;
        }
    }
}

class Patient
{
    public string Name { get; }
    public string Department { get; }
    public Patient(string name, string dept) { Name = name; Department = dept; }
    public override string ToString() => $"{Name} ({Department})";
}
```

## Коли ObservableCollection\<T\>?

| Ситуація | Рекомендація |
|----------|-------------|
| WPF / MAUI / Xamarin прив'язка до UI | **ObservableCollection** — обов'язково |
| Потрібно реагувати на зміни ззовні | **ObservableCollection** + `CollectionChanged` |
| Звичайне зберігання і перебір даних | **List\<T\>** — легший overhead |
| Великі батч-операції без UI | **List\<T\>** — немає зайвих подій |

`ObservableCollection<T>` генерує подію на **кожну** окрему зміну. Якщо потрібно додати 10 000 елементів — краще створити `List<T>`, наповнити його, а потім передати в конструктор `ObservableCollection<T>(list)`, щоб уникнути 10 000 подій.
