---
chapter: 8
chapterTitle: "Розділ 8. Додаткові можливості ООП у C#"
section: 4
number: "8.4"
title: "Індексатори"
source: "../_combined/49-indeksatory.md"
---

## 8.4. Індексатори

Масиви зручні тим, що до елементів можна звертатися за індексом: `arr[0]`, `arr[i]`. Але іноді ми хочемо, щоб і власний клас підтримував таку синтаксичну форму — наприклад, звертатися до пацієнтів відділення як `ward[0]`, `ward[i]`, або до атрибутів пацієнта як `patient["diagnosis"]`. Саме для цього у C# існують **індексатори** (indexers).

Індексатор — це спеціальний член класу, який дозволяє звертатися до об'єкта за допомогою квадратних дужок, як до масиву або словника. За своєю формою він нагадує властивість: також має блоки `get` і `set`, також має тип. Ключова відмінність — замість фіксованої назви використовується ключове слово `this` і параметр у квадратних дужках.

## Синтаксис індексатора

```csharp
тип_результату this[Тип параметр, ...]
{
    get { ... }
    set { ... }
}
```

- `this` — ключове слово замість назви. Означає «доступ до цього об'єкта за індексом».
- Тип у квадратних дужках — тип індексу (може бути `int`, `string` або будь-яким іншим).
- `get` — повертає значення за вказаним індексом.
- `set` — записує значення; переданий об'єкт доступний через неявний параметр `value`.
- Індексатор не може бути статичним — він завжди прив'язаний до екземпляра.

![Індексатор: синтаксис та порівняння з властивістю](_assets/08-04/indexer-anatomy.png)

## Числовий індексатор

Найпоширеніший варіант — індексатор з параметром `int`, який дозволяє звертатися до елементів внутрішньої колекції об'єкта. Визначимо клас `Ward` (відділення лікарні), що зберігає масив пацієнтів і надає доступ до них за позицією:

```csharp run
using System;

// Виконуваний код
Ward cardiology = new Ward("Кардіологія", new Patient[]
{
    new Patient("Іван Петренко"),
    new Patient("Марія Коваль"),
    new Patient("Олег Сидоренко"),
});

// Доступ через індексатор — як у масиві
Patient first = cardiology[0];
Console.WriteLine($"Перший пацієнт: {first.Name}");

// Заміна елемента через set
cardiology[0] = new Patient("Андрій Мельник");
Console.WriteLine($"Після виписки: {cardiology[0].Name}");

// Ітерація
for (int i = 0; i < 3; i++)
    Console.WriteLine($"  [{i}] {cardiology[i].Name}");

// Класи
class Patient
{
    public string Name { get; }
    public Patient(string name) => Name = name;
}

class Ward
{
    public string Name { get; }
    private Patient[] _patients;

    public Ward(string name, Patient[] patients)
    {
        Name = name;
        _patients = patients;
    }

    public Patient this[int index]
    {
        get
        {
            if (index < 0 || index >= _patients.Length)
                throw new ArgumentOutOfRangeException(nameof(index));
            return _patients[index];
        }
        set
        {
            if (index < 0 || index >= _patients.Length)
                throw new ArgumentOutOfRangeException(nameof(index));
            _patients[index] = value;
        }
    }
}
```

Блок `get` перевіряє межі масиву і генерує `ArgumentOutOfRangeException`, якщо індекс некоректний — так само, як поводиться звичайний масив при виході за межі. Блок `set` виконує ту саму перевірку перед записом.

## Рядковий індексатор

Індекс не обов'язково має бути цілим числом. Рядковий індекс зручний, коли об'єкт зберігає набір іменованих атрибутів. Визначимо `Patient` із доступом до клінічних даних за ключовим рядком:

```csharp run
using System;

// Виконуваний код
Patient patient = new Patient("Іван Петренко");
patient["diagnosis"] = "Гіпертонія II ст.";
patient["allergies"] = "Пеніцилін";
patient["notes"]     = "Контроль АТ двічі на день";

Console.WriteLine($"Пацієнт: {patient.Name}");
Console.WriteLine($"Діагноз:  {patient["diagnosis"]}");
Console.WriteLine($"Алергії:  {patient["allergies"]}");
Console.WriteLine($"Примітки: {patient["notes"]}");

// Клас
class Patient
{
    public string Name { get; }
    private string _diagnosis = "";
    private string _allergies = "";
    private string _notes = "";

    public Patient(string name) => Name = name;

    public string this[string attribute]
    {
        get
        {
            switch (attribute)
            {
                case "diagnosis": return _diagnosis;
                case "allergies": return _allergies;
                case "notes":     return _notes;
                default: throw new ArgumentException($"Невідомий атрибут: {attribute}");
            }
        }
        set
        {
            switch (attribute)
            {
                case "diagnosis": _diagnosis = value; break;
                case "allergies": _allergies = value; break;
                case "notes":     _notes = value;     break;
                default: throw new ArgumentException($"Невідомий атрибут: {attribute}");
            }
        }
    }
}
```

Рядковий індексатор дає інтерфейс, схожий на словник, але з чіткими дозволеними ключами і можливістю додати валідацію або логіку перетворення прямо в `get`/`set`.

## Індексатор із кількома параметрами

Індексатор може приймати більше одного параметра. Це корисно для двовимірних структур, наприклад, для розкладу прийомів лікаря, де день і час — це два незалежні виміри:

```csharp run
using System;

// Виконуваний код
AppointmentGrid schedule = new AppointmentGrid(5, 16);

schedule[0, 9]  = "Кардіологія — Петренко І.";
schedule[0, 11] = "Неврологія  — Коваль М.";
schedule[1, 10] = "Ортопедія   — Сидоренко О.";

Console.WriteLine($"Пн 09:00 — {schedule[0, 9]}");
Console.WriteLine($"Пн 11:00 — {schedule[0, 11]}");
Console.WriteLine($"Вт 10:00 — {schedule[1, 10]}");

string slot = schedule[0, 14];
Console.WriteLine($"Пн 14:00 — {(slot != null ? slot : "(вільно)")}");

// Клас
class AppointmentGrid
{
    private string[,] _slots;

    public AppointmentGrid(int days, int hours)
    {
        _slots = new string[days, hours];
    }

    // Два параметри: день (0=Пн..4=Пт) і година (8..17)
    public string this[int day, int hour]
    {
        get => _slots[day, hour];
        set => _slots[day, hour] = value;
    }
}
```

Синтаксис звернення `schedule[0, 9]` виглядає так само природно, як доступ до двовимірного масиву. Компілятор транслює це в виклик індексатора з двома аргументами.

## Модифікатори доступу та readonly-індексатор

Як і у властивостей, в індексаторах можна опустити блок `set` (тоді індексатор лише для читання) або обмежити його доступ модифікатором:

```csharp
// Тільки для читання — set відсутній
public Patient this[int index]
{
    get => _patients[index];
}

// set приватний — зовні не можна записати
public Patient this[int index]
{
    get => _patients[index];
    private set => _patients[index] = value;
}
```

Readonly-індексатор корисний для незмінних колекцій (наприклад, архівних записів), де зовнішній код має тільки читати дані, але не змінювати їх.

## Перевантаження індексаторів

Так само як і методи, індексатори можна **перевантажувати** — визначити кілька версій з різними типами або кількістю параметрів. Визначимо `Ward` одночасно з числовим доступом (за позицією) і рядковим (за ім'ям пацієнта):

```csharp run
using System;

// Виконуваний код
Ward ward = new Ward(new Patient[]
{
    new Patient("Іван Петренко"),
    new Patient("Марія Коваль"),
    new Patient("Олег Сидоренко"),
});

// Доступ за числовим індексом
Console.WriteLine($"Пацієнт [0]: {ward[0].Name}");
Console.WriteLine($"Пацієнт [2]: {ward[2].Name}");

// Доступ за ім'ям
Patient found = ward["Марія Коваль"];
Console.WriteLine($"Знайдено за ім'ям: {found.Name}");

// Класи
class Patient
{
    public string Name { get; }
    public Patient(string name) => Name = name;
}

class Ward
{
    private Patient[] _patients;

    public Ward(Patient[] patients) => _patients = patients;

    // Перший індексатор — доступ за позицією
    public Patient this[int index] => _patients[index];

    // Другий індексатор — пошук за ім'ям
    public Patient this[string name]
    {
        get
        {
            foreach (var p in _patients)
                if (p.Name == name) return p;
            throw new ArgumentException($"Пацієнт '{name}' не знайдений");
        }
    }
}
```

Компілятор розрізняє перевантажені варіанти за типом аргументу у дужках: `ward[0]` — це `int`, тому викликається перший індексатор; `ward["Марія Коваль"]` — це `string`, тому другий. Перевантаження за кількістю параметрів також дозволене.

Індексатори можуть бути **віртуальними** і **абстрактними** — їх можна перевизначати у похідних класах так само, як і методи, що дозволяє будувати гнучкі ієрархії класів із уніфікованим синтаксисом доступу.
