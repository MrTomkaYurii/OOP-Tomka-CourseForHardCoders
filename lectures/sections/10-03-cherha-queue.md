---
chapter: 10
chapterTitle: "Розділ 10. Колекції"
section: 3
number: "10.3"
title: "Черга Queue<T>"
source: "../_combined/64-cherha-queue.md"
---

## 10.3. Черга Queue<T>

У реальному житті черга — інтуїтивна структура: хто прийшов першим, той і обслуговується першим. У програмуванні цей принцип називається **FIFO** (First In — First Out): елемент, доданий до колекції раніше, вилучається з неї раніше.

Клас `Queue<T>` з простору імен `System.Collections.Generic` реалізує саме цей принцип. На відміну від `List<T>`, де є індексований доступ і вставка в будь-яку позицію, `Queue<T>` надає лише дві основні операції: **Enqueue** (додати в кінець) і **Dequeue** (забрати з початку). Такий обмежений, але чіткий контракт робить черги ідеальними там, де важливий порядок обробки: черга пацієнтів на прийом, задачі у виконавця, повідомлення в черзі обробки.

## Внутрішня структура

Всередині `Queue<T>` зберігає елементи у **кільцевому масиві** (circular buffer). На відміну від `List<T>`, де при видаленні з початку всі елементи зсуваються, черга використовує два індекси — **head** (вказівник на перший елемент) і **tail** (вказівник на наступну вільну позицію). При `Dequeue` лише head зсувається вперед — жодного копіювання. Тому обидві основні операції виконуються за **O(1)**.

![Queue<T> — принцип FIFO](_assets/10-03/queue-fifo-structure.png)

Якщо кільцевий масив заповнюється, `Queue<T>` виділяє новий масив більшого розміру і копіює дані — аналогічно до `List<T>`. Тому `Enqueue` — O(1) **амортизована**: більшість операцій O(1), але іноді виникає O(n) перевиділення.

## Створення черги

`Queue<T>` типізується елементом, що зберігається, і підтримує кілька способів ініціалізації:

```csharp
// Порожня черга
Queue<string> waitingRoom = new Queue<string>();

// З початковою ємністю (без елементів — лише буфер)
Queue<string> withCapacity = new Queue<string>(32);

// З іншої колекції або масиву
var names = new List<string> { "Петренко", "Коваль", "Мельник" };
Queue<string> fromList = new Queue<string>(names);
```

Властивість `Count` повертає поточну кількість елементів у черзі.

## Методи Queue<T>

### Enqueue та Dequeue

`Enqueue(T item)` додає елемент до хвоста черги, `Dequeue()` вилучає і повертає елемент з голови:

```csharp
var queue = new Queue<string>();
queue.Enqueue("А");  // { А }
queue.Enqueue("Б");  // { А, Б }
queue.Enqueue("В");  // { А, Б, В }

var first = queue.Dequeue();  // повертає "А", черга стає { Б, В }
```

Важливо: якщо викликати `Dequeue()` або `Peek()` на **порожній** черзі — програма кине `InvalidOperationException`. Завжди перевіряйте `Count > 0` або використовуйте `Try`-варіанти методів.

### Peek — підглянути без видалення

`Peek()` повертає перший елемент черги, але не видаляє його. Корисно, коли потрібно прийняти рішення на основі поточного елемента, не обробляючи його одразу:

```csharp
if (queue.Count > 0)
{
    var next = queue.Peek();   // прочитали, не видалили
    // ... перевірка ...
    var processed = queue.Dequeue();  // тепер забираємо
}
```

### TryDequeue і TryPeek

Безпечні варіанти, що не кидають виняток на порожній черзі. Повертають `true`, якщо операція успішна, і передають результат через `out`-параметр:

- `bool TryDequeue(out T result)` — вилучає перший елемент, якщо черга не порожня.
- `bool TryPeek(out T result)` — читає перший елемент без видалення, якщо черга не порожня.

### Повний перелік методів

| Метод | Що робить | Складність |
|-------|-----------|-----------|
| `Enqueue(item)` | Додає елемент до хвоста | O(1)* |
| `Dequeue()` | Вилучає і повертає елемент з голови | O(1) |
| `Peek()` | Повертає перший елемент без видалення | O(1) |
| `TryDequeue(out T)` | Безпечний Dequeue; повертає false якщо порожня | O(1) |
| `TryPeek(out T)` | Безпечний Peek; повертає false якщо порожня | O(1) |
| `Contains(item)` | Чи є елемент у черзі | O(n) |
| `Clear()` | Очищає чергу | O(n) |
| `CopyTo(arr, i)` | Копіює в масив починаючи з індексу i | O(n) |
| `ToArray()` | Повертає новий масив зі збереженням порядку | O(n) |

## Черга реєстратури — runnable приклад

Змоделюємо ранкову чергу пацієнтів у реєстратурі. Нові пацієнти займають чергу, реєстратор обслуговує по одному в порядку надходження:

```csharp run
using System;
using System.Collections.Generic;

var registrationDesk = new Queue<string>();

// Пацієнти записуються в чергу
registrationDesk.Enqueue("Петренко І. — прийом 08:00");
registrationDesk.Enqueue("Коваль М.   — аналізи");
registrationDesk.Enqueue("Сидоренко О. — кардіолог");
registrationDesk.Enqueue("Мельник Г.  — терапевт");

Console.WriteLine($"Черга на реєстрацію: {registrationDesk.Count} осіб");
Console.WriteLine($"Перший у черзі: {registrationDesk.Peek()}");
Console.WriteLine();

// Реєстратор обслуговує по одному
Console.WriteLine("=== Процес реєстрації ===");
while (registrationDesk.Count > 0)
{
    var patient = registrationDesk.Dequeue();
    Console.WriteLine($"✓ Зареєстровано: {patient}");
    Console.WriteLine($"  Залишилось у черзі: {registrationDesk.Count}");
}

Console.WriteLine("\nРеєстрацію завершено.");

// TryDequeue на порожній черзі — безпечний варіант
var success = registrationDesk.TryDequeue(out var next);
Console.WriteLine($"\nСпроба Dequeue з порожньої черги: {(success ? "успішно" : "черга порожня")}");
```

## Черга пацієнтів у лікаря — runnable приклад

Розширений приклад із класами: черга пацієнтів передається лікарю, який послідовно їх приймає:

```csharp run
using System;
using System.Collections.Generic;

// Виконуваний код
var patients = new Queue<Patient>();
patients.Enqueue(new Patient("Петренко Іван",    "гіпертонія"));
patients.Enqueue(new Patient("Коваль Марія",     "діабет"));
patients.Enqueue(new Patient("Сидоренко Олег",   "аритмія"));
patients.Enqueue(new Patient("Мельник Ганна",    "мігрень"));

Console.WriteLine($"Очікують прийому: {patients.Count} пацієнтів\n");

var doctor = new Doctor("Іванченко В.О.", "кардіолог");
doctor.ConductReception(patients);

Console.WriteLine($"\nЧерга після прийому: {patients.Count} осіб");

// Класи — після виконуваного коду
class Patient
{
    public string Name { get; }
    public string Diagnosis { get; }
    public Patient(string name, string diagnosis)
    {
        Name = name;
        Diagnosis = diagnosis;
    }
}

class Doctor
{
    private string _name;
    private string _speciality;

    public Doctor(string name, string speciality)
    {
        _name = name;
        _speciality = speciality;
    }

    public void ConductReception(Queue<Patient> queue)
    {
        Console.WriteLine($"Лікар {_name} ({_speciality}) розпочинає прийом:");
        int num = 1;
        while (queue.TryDequeue(out var patient))
        {
            Console.WriteLine($"  {num++}. {patient.Name} — скарга: {patient.Diagnosis}");
        }
        Console.WriteLine("Прийом завершено.");
    }
}
```

## Складність операцій

![Queue<T> — складність операцій та порівняння з List<T>](_assets/10-03/queue-complexity.png)

Ключова перевага `Queue<T>` над `List<T>` — **O(1) для Dequeue**. Якщо ви реалізуєте чергу через `List<T>` і видаляєте елемент з початку через `RemoveAt(0)` — кожна така операція зсуває весь список: O(n). При великих обсягах даних це критично.

## Коли Queue<T>?

`Queue<T>` — правильний вибір, коли:

- **Порядок обробки важливий**: потрібно зберегти FIFO-порядок (черга задач, повідомлень, запитів).
- **Операції тільки з кінцями**: ніколи не потрібен доступ до середини колекції.
- **Видалення з початку часте**: `List<T>` для цього невигідний — O(n) на кожне `RemoveAt(0)`.

Якщо ж потрібен доступ за індексом, пошук по середині, або порядок **LIFO** (останній прийшов — перший вийшов) — розгляньте відповідно `List<T>` або `Stack<T>`.
