---
chapter: 10
chapterTitle: "Розділ 10. Колекції"
section: 5
number: "10.5"
title: "Словник Dictionary<K, V>"
source: "../_combined/66-slovnyk-dictionary-k-v.md"
---

## 10.5. Словник Dictionary\<K, V\>

Уявіть задачу: є список пацієнтів, і потрібно швидко знайти пацієнта за його ідентифікатором `"P001"`. При використанні `List<T>` доведеться перебирати весь список поелементно — O(n). При 10 000 пацієнтів це 10 000 порівнянь у гіршому випадку.

`Dictionary<K, V>` вирішує цю задачу за **O(1)** в середньому. Це колекція пар **ключ → значення**, де ключ унікальний і забезпечує миттєвий доступ до відповідного значення. `Dictionary<K, V>` — правильний вибір щоразу, коли потрібен швидкий пошук за ідентифікатором, кодом або будь-яким унікальним атрибутом.

## Внутрішня структура: хеш-таблиця

Всередині `Dictionary<K, V>` зберігає дані у **хеш-таблиці**. Принцип роботи:

1. При додаванні пари `key → value` обчислюється хеш ключа: `key.GetHashCode()`.
2. За хешем визначається **індекс бакету** (bucket): `index = hash % bucketCount`.
3. Пара зберігається у відповідному бакеті.
4. При пошуку за ключем ті самі два кроки дають індекс — і значення знаходиться без перебору.

![Dictionary<K,V> — внутрішня структура (хеш-таблиця)](_assets/10-05/dictionary-hash-structure.png)

Якщо два різних ключі дають однаковий індекс бакету (**колізія**), елементи зберігаються разом у тому ж бакеті у вигляді ланцюжка. Добре реалізований `GetHashCode()` мінімізує колізії, тому на практиці пошук майже завжди O(1).

Тип ключа `K` повинен коректно реалізувати `GetHashCode()` і `Equals()`. Для вбудованих типів (`string`, `int`, `Guid` тощо) це вже зроблено. Для власних класів — потрібно явно перевизначити ці методи або використовувати незмінні типи-значення.

## Створення та ініціалізація

`Dictionary<K, V>` типізується двома параметрами: тип ключа `K` і тип значення `V`:

```csharp
// Порожній словник: int-ключ → рядкове значення
Dictionary<int, string> rooms = new Dictionary<int, string>();

// Ключ — рядок (код пацієнта), значення — рядок (ПІБ)
var patientIndex = new Dictionary<string, string>();

// Ініціалізатор з фігурними дужками — синтаксис { ключ, значення }
var diagnoses = new Dictionary<string, string>()
{
    { "P001", "Гіпертонія" },
    { "P002", "Діабет" },
    { "P003", "Аритмія" }
};

// Альтернативний синтаксис з індексатором [ключ] = значення
var medications = new Dictionary<string, string>()
{
    ["ASP100"] = "Аспірин 100мг",
    ["IBU400"] = "Ібупрофен 400мг",
    ["MET850"] = "Метформін 850мг"
};
```

Обидва синтаксиси рівноцінні — використовуйте той, що читається краще для конкретної задачі.

## KeyValuePair\<TKey, TValue\>

Кожен елемент словника внутрішньо представляється структурою `KeyValuePair<TKey, TValue>`. Ця структура має дві властивості: `Key` — ключ елемента і `Value` — його значення. Вона з'являється при ітерації словника через `foreach`, при ініціалізації через конструктор, і при роботі з колекцією `Keys`/`Values`.

```csharp
// Створення через KeyValuePair (рідкісний сценарій — для ініціалізації з колекції)
var pair = new KeyValuePair<string, string>("P001", "Петренко Іван");
var pairs = new List<KeyValuePair<string, string>> { pair };
var dict = new Dictionary<string, string>(pairs);
```

## Отримання та зміна елементів

Доступ до елемента відбувається через індексатор `dict[key]`:

```csharp
var patientNames = new Dictionary<string, string>()
{
    ["P001"] = "Петренко Іван",
    ["P002"] = "Коваль Марія",
};

// Читання
string name = patientNames["P001"];   // "Петренко Іван"

// Оновлення існуючого ключа
patientNames["P002"] = "Коваль Марія Степанівна";

// Додавання нового ключа — якщо ключ відсутній
patientNames["P003"] = "Сидоренко Олег";
```

Якщо звернутися за **неіснуючим ключем** через `dict[key]` — буде кинуто `KeyNotFoundException`. Для безпечного доступу використовуйте `TryGetValue`.

## Властивості Dictionary\<K, V\>

- `Count` — кількість пар у словнику.
- `Keys` — колекція всіх ключів типу `ICollection<K>`. Ітерується через `foreach`.
- `Values` — колекція всіх значень типу `ICollection<V>`.

```csharp
var rooms = new Dictionary<int, string>()
{
    [101] = "Кардіологія",
    [102] = "Неврологія",
    [201] = "Хірургія"
};

Console.WriteLine($"Палат: {rooms.Count}");

foreach (var roomNum in rooms.Keys)
    Console.WriteLine($"Палата {roomNum}");

foreach (var dept in rooms.Values)
    Console.WriteLine($"Відділення: {dept}");
```

## Перебір словника

При `foreach` кожен елемент словника — це `KeyValuePair<K, V>`:

```csharp
var patientNames = new Dictionary<string, string>()
{
    ["P001"] = "Петренко Іван",
    ["P002"] = "Коваль Марія",
    ["P003"] = "Сидоренко Олег"
};

foreach (var entry in patientNames)
{
    Console.WriteLine($"ID: {entry.Key}  Пацієнт: {entry.Value}");
}
```

З C# 7+ можна одразу деструктурувати пару:

```csharp
foreach (var (id, name) in patientNames)
{
    Console.WriteLine($"{id} → {name}");
}
```

## Методи Dictionary\<K, V\>

| Метод | Що робить | Складність |
|-------|-----------|-----------|
| `Add(key, value)` | Додає пару; виняток якщо ключ вже є | O(1)* |
| `TryAdd(key, value)` | Додає якщо ключ відсутній; повертає `bool` | O(1)* |
| `Remove(key)` | Видаляє пару за ключем; повертає `bool` | O(1)* |
| `Remove(key, out V)` | Видаляє і повертає значення через `out` | O(1)* |
| `ContainsKey(key)` | Чи є ключ у словнику | O(1)* |
| `ContainsValue(value)` | Чи є значення у словнику | O(n) |
| `TryGetValue(key, out V)` | Безпечне читання; `false` якщо ключ відсутній | O(1)* |
| `Clear()` | Очищає словник | O(n) |

### TryGetValue — найважливіший метод безпечного доступу

`TryGetValue` — рекомендований спосіб читання зі словника в production-коді. Він не кидає виняток на відсутньому ключі і повертає `false`:

```csharp
if (patientNames.TryGetValue("P999", out var name))
    Console.WriteLine($"Знайдено: {name}");
else
    Console.WriteLine("Пацієнт P999 не знайдений.");
```

Порівняйте з небезпечним варіантом:

```csharp
// НЕБЕЗПЕЧНО — кидає KeyNotFoundException якщо ключ відсутній:
var name = patientNames["P999"];
```

## Каталог медикаментів — runnable приклад

Медичний каталог: пошук препарату за кодом, оновлення, видалення:

```csharp run
using System;
using System.Collections.Generic;

// Каталог: код препарату → назва
var catalog = new Dictionary<string, string>()
{
    ["ASP100"] = "Аспірин 100мг",
    ["IBU400"] = "Ібупрофен 400мг",
    ["MET850"] = "Метформін 850мг",
    ["LIS10"]  = "Лізиноприл 10мг"
};

Console.WriteLine($"Препаратів у каталозі: {catalog.Count}");

// Перебір усіх записів
Console.WriteLine("\n=== Каталог медикаментів ===");
foreach (var (code, name) in catalog)
    Console.WriteLine($"  [{code}]  {name}");

// Пошук за кодом — O(1)
Console.WriteLine();
string[] lookupCodes = { "IBU400", "PARA500", "LIS10" };
foreach (var code in lookupCodes)
{
    if (catalog.TryGetValue(code, out var med))
        Console.WriteLine($"Знайдено [{code}]: {med}");
    else
        Console.WriteLine($"Не знайдено: [{code}]");
}

// Оновлення назви та додавання нового
catalog["MET850"] = "Метформін 850мг (пролонгований)";
catalog.TryAdd("PARA500", "Парацетамол 500мг");
Console.WriteLine($"\nПісля оновлення: {catalog["MET850"]}");
Console.WriteLine($"Новий препарат: {catalog["PARA500"]}");

// Видалення
bool removed = catalog.Remove("ASP100", out var removedName);
Console.WriteLine($"\nВидалено ASP100 ({removedName}): {removed}");
Console.WriteLine($"Препаратів у каталозі: {catalog.Count}");

// Ключі відділень
Console.WriteLine("\nДоступні коди:");
foreach (var key in catalog.Keys)
    Console.Write($"{key}  ");
Console.WriteLine();
```

## Реєстратура пацієнтів — runnable приклад

Реалістичний приклад з класом: реєстр пацієнтів за ідентифікатором:

```csharp run
using System;
using System.Collections.Generic;

// Виконуваний код
var registry = new PatientRegistry();

registry.Register("P001", new Patient("Петренко Іван",  42, "Гіпертонія"));
registry.Register("P002", new Patient("Коваль Марія",   35, "Діабет 2 типу"));
registry.Register("P003", new Patient("Сидоренко Олег", 58, "Аритмія"));
registry.Register("P004", new Patient("Мельник Ганна",  29, "Мігрень"));

Console.WriteLine($"Пацієнтів у реєстрі: {registry.Count}\n");

registry.PrintAll();

Console.WriteLine();
registry.Lookup("P002");
registry.Lookup("P999");

registry.Discharge("P003");
Console.WriteLine($"\nПісля виписки: {registry.Count} пацієнтів");

// Класи — після виконуваного коду
class Patient
{
    public string Name { get; }
    public int Age { get; }
    public string Diagnosis { get; }

    public Patient(string name, int age, string diagnosis)
    {
        Name = name;
        Age = age;
        Diagnosis = diagnosis;
    }

    public override string ToString() =>
        $"{Name}, {Age} р. — {Diagnosis}";
}

class PatientRegistry
{
    private Dictionary<string, Patient> _data = new Dictionary<string, Patient>();

    public int Count => _data.Count;

    public void Register(string id, Patient patient)
    {
        if (_data.TryAdd(id, patient))
            Console.WriteLine($"  Зареєстровано [{id}]: {patient.Name}");
        else
            Console.WriteLine($"  Помилка: ID {id} вже існує.");
    }

    public void Lookup(string id)
    {
        if (_data.TryGetValue(id, out var p))
            Console.WriteLine($"Пацієнт [{id}]: {p}");
        else
            Console.WriteLine($"Пацієнт [{id}] не знайдений.");
    }

    public void Discharge(string id)
    {
        if (_data.Remove(id, out var p))
            Console.WriteLine($"Виписано [{id}]: {p.Name}");
        else
            Console.WriteLine($"Пацієнт [{id}] не знайдений.");
    }

    public void PrintAll()
    {
        Console.WriteLine("=== Поточний реєстр ===");
        foreach (var (id, p) in _data)
            Console.WriteLine($"  [{id}]  {p}");
    }
}
```

## Складність операцій

![Dictionary<K,V> — складність операцій vs List<T>](_assets/10-05/dictionary-complexity.png)

## Коли Dictionary\<K, V\>?

`Dictionary<K, V>` — правильний вибір коли:

- Потрібен **швидкий пошук за ключем**: O(1) vs O(n) у `List<T>`.
- Дані мають природну структуру **ключ → значення**: ID пацієнта → пацієнт, код препарату → препарат.
- Потрібно перевіряти **наявність** елемента за ідентифікатором.
- Потрібен **підрахунок** (ключ → кількість) або **групування** (ключ → список).

`List<T>` залишається кращим вибором, коли:

- Порядок елементів важливий і ключова операція — перебір.
- Немає унікального ідентифікатора для елементів.
- Колекція мала (< ~20 елементів) — різниця O(1) vs O(n) несуттєва.

## HashSet\<T\> — множина унікальних елементів

`HashSet<T>` — «словник без значень». Він зберігає **лише унікальні елементи**, гарантує O(1) для додавання, видалення і пошуку, але на відміну від `Dictionary` не зберігає пар ключ-значення — тільки самі елементи.

Ключові властивості `HashSet<T>`:
- **Не допускає дублікатів**: повторне `Add(element)` ігнорується (повертає `false`)
- **Немає гарантій порядку**: елементи перебираються у довільному порядку
- **О(1) для Contains**: значно швидший за `List<T>.Contains` для великих колекцій
- **Операції теорії множин**: `UnionWith`, `IntersectWith`, `ExceptWith`

```csharp run
using System;
using System.Collections.Generic;

// Реєстр унікальних діагностичних кодів (ICD-10) у відділенні
var diagnosisCodes = new HashSet<string>();

// Додавання — дублікати ігноруються
bool added1 = diagnosisCodes.Add("I10.9");   // Гіпертонія — додано
bool added2 = diagnosisCodes.Add("J45.0");   // Астма — додано
bool added3 = diagnosisCodes.Add("E11.9");   // Діабет — додано
bool added4 = diagnosisCodes.Add("I10.9");   // Гіпертонія — ВЖЕ Є, повертає false

Console.WriteLine($"Унікальних кодів: {diagnosisCodes.Count}"); // 3, не 4
Console.WriteLine($"Додано 4-й (дублікат): {added4}"); // False

// О(1) пошук
bool hasHypertension = diagnosisCodes.Contains("I10.9"); // true
bool hasCancer       = diagnosisCodes.Contains("C34.1"); // false
Console.WriteLine($"Є гіпертонія (I10.9): {hasHypertension}");
Console.WriteLine($"Є рак легень (C34.1): {hasCancer}");

// Видалення
diagnosisCodes.Remove("J45.0");
Console.WriteLine($"Після видалення астми: {diagnosisCodes.Count} кодів");
```

```csharp run
using System;
using System.Collections.Generic;

// Операції теорії множин — корисні для порівняння груп пацієнтів
var cardioPatients   = new HashSet<string> { "P001", "P002", "P003", "P004" };
var diabeticPatients = new HashSet<string> { "P003", "P004", "P005", "P006" };

// Перетин: пацієнти з обома захворюваннями
var both = new HashSet<string>(cardioPatients);
both.IntersectWith(diabeticPatients);
Console.WriteLine("Кардіо + Діабет: " + string.Join(", ", both)); // P003, P004

// Об'єднання: всі пацієнти хоча б з одним захворюванням
var either = new HashSet<string>(cardioPatients);
either.UnionWith(diabeticPatients);
Console.WriteLine("Кардіо або Діабет: " + string.Join(", ", either)); // P001-P006

// Різниця: тільки кардіо пацієнти (без діабетиків)
var onlyCardio = new HashSet<string>(cardioPatients);
onlyCardio.ExceptWith(diabeticPatients);
Console.WriteLine("Тільки кардіо: " + string.Join(", ", onlyCardio)); // P001, P002

// IsSubsetOf: чи всі кардіо-пацієнти входять до загальної групи?
bool isSubset = cardioPatients.IsSubsetOf(either);
Console.WriteLine($"Кардіо ⊆ Об'єднання: {isSubset}"); // True

// Видалення дублікатів зі списку
var rawList = new List<string> { "I10.9", "J45.0", "I10.9", "E11.9", "J45.0" };
var uniqueCodes = new HashSet<string>(rawList); // автоматично лише унікальні
Console.WriteLine($"\nRaw: {rawList.Count} кодів → Unique: {uniqueCodes.Count} кодів");
Console.WriteLine(string.Join(", ", uniqueCodes));
```

| Операція | `List<T>` | `HashSet<T>` |
|----------|-----------|--------------|
| `Add` | O(1) (amortized) | O(1) — дублікати ігноруються |
| `Contains` | O(n) | **O(1)** |
| `Remove` | O(n) | O(1) |
| Порядок | Зберігається | Не гарантується |
| Дублікати | Дозволені | Заборонені |
| Теорія множин | Ні | `UnionWith`, `IntersectWith`, `ExceptWith` |

**Використовуйте `HashSet<T>` коли:** потрібна колекція без дублікатів, або потрібна швидка перевірка `Contains` для великих наборів даних, або потрібні операції над множинами. **Використовуйте `List<T>` коли:** важливий порядок або допустимі дублікати.
