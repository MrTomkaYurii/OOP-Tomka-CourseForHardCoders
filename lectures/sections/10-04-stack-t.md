---
chapter: 10
chapterTitle: "Розділ 10. Колекції"
section: 4
number: "10.4"
title: "Stack<T>"
source: "../_combined/65-stack-t.md"
---

## 10.4. Stack<T>

Стек — одна з фундаментальних структур даних у програмуванні. Він реалізує принцип **LIFO** (Last In — First Out): останній доданий елемент вилучається першим. Уявіть стопку тарілок: нову тарілку кладуть зверху, і знімають теж зверху. Або одяг у зимовий день — одягаєш шарами (майка → сорочка → светр → куртка), а знімаєш у зворотному порядку.

У медичному контексті стек природно описує **журнал процедур у зворотному порядку**: скасувати потрібно останню введену процедуру, а не першу. Або стек навігації в медичній системі — кнопка «назад» завжди повертає на попередній екран, тобто на вершину стека переходів.

Клас `Stack<T>` з простору імен `System.Collections.Generic` реалізує цей принцип ефективно: і `Push`, і `Pop` виконуються за **O(1)**.

## Внутрішня структура

Всередині `Stack<T>` зберігає елементи у звичайному масиві. **Top** — індекс вершини стека, що вказує на останній доданий елемент. При `Push` індекс збільшується і туди записується елемент; при `Pop` зчитується значення і індекс зменшується. Жодного зсуву даних — лише зміна одного числа. Звідси O(1) для обох операцій.

При заповненні буфера відбувається стандартне подвоєння — аналогічно `List<T>`.

![Stack<T> — принцип LIFO](_assets/10-04/stack-lifo-structure.png)

## Створення стека

`Stack<T>` підтримує ті ж способи ініціалізації, що й `Queue<T>`:

```csharp
// Порожній стек
Stack<string> procedureLog = new Stack<string>();

// З початковою ємністю (без елементів)
Stack<string> withCapacity = new Stack<string>(32);

// З іншої колекції — елементи потрапляють у стек у порядку ітерації,
// тобто останній елемент колекції стане вершиною стека
var meds = new List<string> { "Аспірин", "Ібупрофен", "Лізиноприл" };
Stack<string> fromList = new Stack<string>(meds);
// Вершина: Лізиноприл (останній у List — перший у Pop)
```

Властивість `Count` повертає кількість елементів у стеку.

**Важливо:** `foreach` по `Stack<T>` повертає елементи у порядку **LIFO** — спочатку вершина, потім вниз. Це відрізняється від `Queue<T>`, де `foreach` іде від голови до хвоста.

## Методи Stack<T>

### Push та Pop

`Push(T item)` кладе елемент на вершину стека, `Pop()` знімає і повертає вершину:

```csharp
var stack = new Stack<string>();
stack.Push("А");   // стек: { А }
stack.Push("Б");   // стек: { Б, А }   ← Б на вершині
stack.Push("В");   // стек: { В, Б, А } ← В на вершині

var top = stack.Pop();   // повертає "В", стек стає { Б, А }
```

Виклик `Pop()` або `Peek()` на **порожньому** стеку кидає `InvalidOperationException`. Перевіряйте `Count > 0` або використовуйте `Try`-варіанти.

### Peek — підглянути без видалення

`Peek()` повертає вершину стека, але не видаляє її. Корисно, наприклад, щоб перевірити що саме буде знято, перш ніж приймати рішення про `Pop`:

```csharp
if (stack.Count > 0)
{
    var top = stack.Peek();    // прочитали вершину
    // ... перевірка ...
    stack.Pop();               // тепер знімаємо
}
```

### TryPop і TryPeek

Безпечні варіанти без ризику виключення:

- `bool TryPop(out T result)` — знімає вершину, якщо стек не порожній; `false` якщо порожній.
- `bool TryPeek(out T result)` — читає вершину без видалення; `false` якщо порожній.

### Повний перелік методів

| Метод | Що робить | Складність |
|-------|-----------|-----------|
| `Push(item)` | Кладе елемент на вершину | O(1)* |
| `Pop()` | Знімає і повертає вершину | O(1) |
| `Peek()` | Повертає вершину без видалення | O(1) |
| `TryPop(out T)` | Безпечний Pop; `false` якщо порожній | O(1) |
| `TryPeek(out T)` | Безпечний Peek; `false` якщо порожній | O(1) |
| `Contains(item)` | Чи є елемент у стеку | O(n) |
| `Clear()` | Очищає стек | O(n) |
| `ToArray()` | Масив у порядку LIFO (вершина першою) | O(n) |

## Покрокова зміна стану

![Stack<T> — покрокова зміна стану при Push та Pop](_assets/10-04/stack-state-steps.png)

## Журнал призначень — runnable приклад

Стек ідеально підходить для журналу, де важливо обробляти записи у зворотному порядку — наприклад, переглянути або скасувати останнє призначення:

```csharp run
using System;
using System.Collections.Generic;

var prescriptionLog = new Stack<string>();

// Лікар вносить призначення протягом дня
prescriptionLog.Push("08:15 — Аспірин 100мг (Петренко І.)");
prescriptionLog.Push("09:40 — Ібупрофен 400мг (Коваль М.)");
prescriptionLog.Push("11:00 — Лізиноприл 10мг (Сидоренко О.)");
prescriptionLog.Push("13:30 — Метформін 850мг (Мельник Г.)");

Console.WriteLine($"Призначень у журналі: {prescriptionLog.Count}");
Console.WriteLine($"Останнє призначення: {prescriptionLog.Peek()}");
Console.WriteLine();

// Перегляд усіх призначень у зворотному порядку (LIFO)
Console.WriteLine("=== Журнал призначень (від останнього) ===");
foreach (var entry in prescriptionLog)
    Console.WriteLine($"  {entry}");

Console.WriteLine();

// Скасування останнього призначення — помилка лікаря
var cancelled = prescriptionLog.Pop();
Console.WriteLine($"Скасовано: {cancelled}");
Console.WriteLine($"Поточне останнє: {prescriptionLog.Peek()}");
Console.WriteLine($"Залишилось у журналі: {prescriptionLog.Count}");

// Безпечне зняття всіх записів
Console.WriteLine("\n=== Обробка всіх призначень ===");
while (prescriptionLog.TryPop(out var record))
    Console.WriteLine($"  Оброблено: {record}");

Console.WriteLine($"Стек порожній: {prescriptionLog.Count == 0}");
```

## Навігація в медичній карті — runnable приклад

Класичний патерн «undo / назад» — стек переходів між розділами. Кожне відкриття нового розділу кладе поточний на стек; кнопка «назад» знімає зі стеку і повертає до попереднього:

```csharp run
using System;
using System.Collections.Generic;

// Виконуваний код
var navigator = new CardNavigator();
navigator.Open("Головна сторінка");
navigator.Open("Пацієнт: Петренко І.");
navigator.Open("Вкладка: Аналізи");
navigator.Open("Аналіз крові від 2026-01-15");

Console.WriteLine($"Поточний розділ: {navigator.Current}");
Console.WriteLine($"Глибина навігації: {navigator.Depth}");
Console.WriteLine();

navigator.GoBack();
Console.WriteLine($"Після 'назад': {navigator.Current}");

navigator.GoBack();
Console.WriteLine($"Після 'назад': {navigator.Current}");

navigator.GoBack();
Console.WriteLine($"Після 'назад': {navigator.Current}");

navigator.GoBack(); // спроба з першої сторінки
Console.WriteLine($"Спроба 'назад' з початку: {navigator.Current}");

// Клас — після виконуваного коду
class CardNavigator
{
    private Stack<string> _history = new Stack<string>();
    private string _current = "—";

    public string Current => _current;
    public int Depth => _history.Count;

    public void Open(string section)
    {
        if (_current != "—")
            _history.Push(_current);
        _current = section;
        Console.WriteLine($"  Відкрито: {section}  (history depth: {_history.Count})");
    }

    public void GoBack()
    {
        if (_history.TryPop(out var previous))
            _current = previous;
        else
            Console.WriteLine("  Вже на початковій сторінці — нікуди повертатись.");
    }
}
```

## Коли Stack<T>?

`Stack<T>` — правильний вибір коли:

- Потрібен **зворотний порядок обробки**: останній доданий — перший оброблений (undo, backtrack, відкат).
- Реалізується **рекурсія ітеративно**: стек замінює системний стек викликів.
- Потрібно **відстежувати вкладені стани**: навігація, відкриті теги, баланс дужок.

| Питання | Відповідь |
|---------|-----------|
| Порядок LIFO (скасування, «назад»)? | **Stack** |
| Порядок FIFO (черга обробки)? | **Queue** |
| Довільний доступ за індексом? | **List** |
| Вставка/видалення в середині? | **LinkedList** |
