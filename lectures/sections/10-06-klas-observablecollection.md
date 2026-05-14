---
chapter: 10
chapterTitle: "Розділ 10. Колекції"
section: 6
number: "10.6"
title: "Клас ObservableCollection"
source: "../_combined/67-klas-observablecollection.md"
---

## 10.6. Клас ObservableCollection

Окрім стандартних класів колекцій типу списків, черг, словників, стеків .NET також надає спеціальний клас `ObservableCollection<T>`. На відміну від раніше розглянутих колекцій цей клас визначений у просторі імен `System.Collections.ObjectModel`. За функціональністю колекція `ObservableCollection` схожа на список `List` за винятком, що дозволяє сповістити зовнішні об'єкти про те, що колекція була змінена.

### Створення та ініціалізація ObservableCollection

Для створення об'єкта клас `ObservableCollection` надає низку конструкторів. Насамперед ми можемо створити порожню колекцію:

```csharp
using System.Collections.ObjectModel;

ObservableCollection<string> people = new ObservableCollection<string>();
```

У цьому випадку колекція людей типізується типом `string`, тому може зберігати лише рядки.

Інша версія конструктора дозволяє передати в `ObservableCollection` об'єкти з іншої колекції або масиву:

```csharp
var people = new ObservableCollection<string>(new string[] { "Tom", "Bob", "Sam" });
```

Для ініціалізації можна через ініціалізатор у фігурних дужках передати значення

```csharp
var people = new ObservableCollection<string>
{
    "Tom", "Bob", "Sam"
};
```

Також можна поєднувати попередні два способи:

```csharp
var people = new ObservableCollection<string>(new string[] { "Mike", "Alice", "Kate" })
{
    "Tom", "Bob", "Sam"
};
```

### Звернення до елементів колекції

Для звернення до елементів `ObservableCollection` можна застосовувати індекси на зразок масивів або списків `List`:

```csharp
var people = new ObservableCollection<string>
{
    "Tom", "Bob", "Sam"
};

// отримуємо перший елемент
Console.WriteLine(people[0]); // Tom

// змінюємо перший елемент
people[0] = "Tomas";
Console.WriteLine(people[0]); // Tomas
```

### Перебір колекції

Для перебору колекції можна використовувати стандартні цикли:

```csharp
using System.Collections.ObjectModel;

var people = new ObservableCollection<string>
{
    "Tom", "Bob", "Sam"
};

foreach (var person in people)
{
    Console.WriteLine(person);
}

for (int i = 0; i < people.Count; i++)
{
    Console.WriteLine(people[i]);
}
```

За допомогою властивості `Count` можна отримати кількість елементів колекції.

### Методи ObservableCollection

Серед методів класу `ObservableCollection` можна назвати такі:

- `void Add(T item)`: додавання нового елемента до колекції
- `CopyTo(T[] array, int index)`: копіює в масив `array` елементи з колекції починаючи з індексу `index`
- `bool Contains(T item)`: повертає `true`, якщо елемент `item` є в колекції
- `Clear()`: видаляє з колекції всі елементи
- `int IndexOf(T item)`: повертає індекс першого входження елемента в колекції
- `void Insert(int index, T item)`: вставляє елемент `item` в колекцію за індексом `index`. Якщо такого індексу у колекції немає, то генерується виняток
- `bool Remove(T item)`: видаляє елемент `item` із колекції, і якщо видалення пройшло успішно, то повертає `true`. Якщо в колекції кілька однакових елементів, то видаляється лише перший з них
- `void RemoveAt(int index)`: видалення елемента за вказаним індексом `index`. Якщо такого індексу у колекції немає, то генерується виняток
- `void Move(int oldIndex, int newIndex)`: переміщає елемент з індексу `oldIndex` на позицію за індексом `newIndex`

Застосування методів:

```csharp
using System.Collections.ObjectModel;

var people = new ObservableCollection<string>();

// додаємо елемент
people.Add("Bob");

// вставляємо елемент за індексом 0
people.Insert(0, "Tom");

// перевірка наявності елемента
bool bobExists = people.Contains("Bob");
// true
Console.WriteLine($"Bob exists: {bobExists}");

bool mikeExists = people.Contains("Mike");
// false
Console.WriteLine($"Mike exists: {mikeExists}");

// видаляємо елемент
people.Remove("Tom");

// видаляємо елемент за індексом 0
people.RemoveAt(0);
```

### Повідомлення про зміну колекції

Клас `ObservableCollection` визначає подію `CollectionChanged`, підписавшись на яку ми можемо обробити будь-які зміни колекції. Ця подія представляє делегат `NotifyCollectionChangedEventHandler`:

```csharp
void NotifyCollectionChangedEventHandler(object? sender, NotifyCollectionChangedEventArgs e);
```

Другий параметр делегата - об'єкт `NotifyCollectionChangedEventArgs` зберігає всю інформацію про подію. Зокрема, його властивість `Action` дозволяє дізнатися про характер змін. Воно зберігає одне із значень з переліку `NotifyCollectionChangedAction`:

- `NotifyCollectionChangedAction.Add`: додавання
- `NotifyCollectionChangedAction.Remove`: видалення
- `NotifyCollectionChangedAction.Replace`: заміна
- `NotifyCollectionChangedAction.Move`: переміщення об'єкта всередині колекції на нову позицію
- `NotifyCollectionChangedAction.Reset`: скидання вмісту колекції (наприклад, під час її очищення за допомогою методу `Clear()`)

Крім того, властивості `NewItems` і `OldItems` дозволяють отримати відповідно додані та видалені об'єкти. Таким чином, ми отримуємо повний контроль над обробкою додавання, видалення та заміни об'єктів у колекції.

Допустимо, у нас буде наступний клас `Person`, який представляє користувача:

```csharp
class Person
{
    public string Name { get; }
    public Person(string name) => Name = name;
}
```

Для керування колекцією об'єктів `Person` визначимо таку програму:

```csharp
using System.Collections.ObjectModel;
using System.Collections.Specialized;

var people = new ObservableCollection<Person>()
{
    new Person("Tom"),
    new Person("Sam")
};

// підписуємось на подію зміни колекції
people.CollectionChanged += People_CollectionChanged;

people.Add(new Person("Bob"));
// додаємо новий елемент

people.RemoveAt(1);
// видаляємо елемент

people[0] = new Person("Eugene");
// замінюємо елемент

Console.WriteLine("\nСписок користувачів:");
foreach (var person in people)
{
    Console.WriteLine(person.Name);
}

// обробник зміни колекції
void People_CollectionChanged(object? sender, NotifyCollectionChangedEventArgs e)
{
    switch (e.Action)
    {
        case NotifyCollectionChangedAction.Add:
            // якщо додавання
            if (e.NewItems?[0] is Person newPerson)
            {
                Console.WriteLine($"Додано новий об'єкт: {newPerson.Name}");
            }
            break;

        case NotifyCollectionChangedAction.Remove:
            // якщо видалення
            if (e.OldItems?[0] is Person oldPerson)
            {
                Console.WriteLine($"Вилучений об'єкт: {oldPerson.Name}");
            }
            break;

        case NotifyCollectionChangedAction.Replace:
            // якщо заміна
            if (e.NewItems?[0] is Person replacingPerson &&
                e.OldItems?[0] is Person replacedPerson)
            {
                Console.WriteLine($"Об'єкт {replacedPerson.Name} замінено на об'єкт {replacingPerson.Name}.");
            }
            break;
    }
}
```

Тут як обробник змін колекції виступає метод `People_CollectionChanged`, в якому за допомогою параметра `NotifyCollectionChangedEventArgs` отримуємо інформацію про зміну. Консольний вивід програми:

![Рисунок з оригінального документа](assets/docx/image102.png)

```text
Додано новий об'єкт: Bob
Вилучений об'єкт: Sam
Об'єкт Tom замінено на об'єкт Eugene.

Список користувачів:
Eugene
Bob
```
