---
chapter: 5
chapterTitle: "Розділ 5. Обробка винятків"
section: 6
number: "5.6"
title: "Пошук блоку catch при обробці винятків"
source: "../_combined/33-poshuk-bloku-catch-pry-obrobtsi-vyniatkiv.md"
---

## 5.6. Пошук блоку catch при обробці винятків

Виняток, що виник у методі, не зобов'язаний оброблятися там само. Якщо у поточному методі немає відповідного `catch`, CLR **піднімається вгору по стеку викликів** — до того методу, який викликав поточний, і так далі. Це дозволяє централізувати обробку помилок на потрібному рівні, не захаращуючи кожен метод блоками `try...catch`.

## Як CLR шукає обробник: дві фази

Коли виникає виняток, CLR виконує **дві окремі фази**:

**Фаза 1 — пошук:** CLR рухається вгору по стеку від місця винятку, перевіряючи кожен рівень на наявність відповідного `catch`. Поки обробник не знайдено — жодний `catch` і жодний `finally` **не виконується**.

**Фаза 2 — розкрутка стека:** Щойно відповідний `catch` знайдено, CLR повертається від місця помилки **назад донизу**, виконуючи по дорозі всі блоки `finally`. Потім виконується знайдений `catch`.

![Пошук catch у стеку викликів та порядок виконання finally](_assets/05-06/call-stack-search.png)

## Покроковий приклад

Розглянемо ланцюжок методів клінічної системи: `ProcessAdmission` → `SaveRecord` → `ParseAge`. Виняток виникає у найглибшому методі:

```csharp run
using System;

ProcessAdmission("П-001", "Іван Петренко", "abc");

void ProcessAdmission(string id, string name, string ageInput)
{
    try
    {
        SaveRecord(id, name, ageInput);
        Console.WriteLine($"[{id}] Госпіталізацію завершено.");
    }
    catch (FormatException ex)
    {
        // CLR знайшов catch тут — на 3-му рівні
        Console.WriteLine($"[{id}] Помилка даних: {ex.Message}");
    }
    finally
    {
        Console.WriteLine($"[{id}] finally у ProcessAdmission — виконується 3-м");
    }
    Console.WriteLine($"[{id}] Після try у ProcessAdmission.");
}

void SaveRecord(string id, string name, string ageInput)
{
    try
    {
        int age = ParseAge(ageInput);   // виняток виникне тут
        Console.WriteLine($"[{id}] {name}, {age.ToString()} р. — збережено.");
    }
    catch (NullReferenceException ex)
    {
        // не підходить для FormatException — пропускається
        Console.WriteLine($"[{id}] NullRef: {ex.Message}");
    }
    finally
    {
        Console.WriteLine($"[{id}] finally у SaveRecord — виконується 2-м");
    }
    Console.WriteLine($"[{id}] Після try у SaveRecord."); // НЕ виконається
}

int ParseAge(string raw)
{
    // try без catch — finally є, але catch немає
    try
    {
        return int.Parse(raw);   // FormatException тут
    }
    finally
    {
        Console.WriteLine("finally у ParseAge — виконується 1-м");
    }
    // сюди не дійде — НЕ виконається
}
```

Порядок виведення показує обидві фази чітко:
1. `finally у ParseAge` — перший на шляху розкрутки
2. `finally у SaveRecord` — другий
3. `catch` у `ProcessAdmission` — виконується після всіх finally
4. `finally у ProcessAdmission` — останній
5. `"Після try у ProcessAdmission."` — виконується, бо виняток перехоплено

## Що не виконується

Коли виняток не перехоплено на певному рівні, **увесь код після блоку `try...catch` на цьому рівні пропускається**. У прикладі вище:

- `"Після try у SaveRecord."` — не виводиться, хоча `SaveRecord` має `finally`
- Код у `ParseAge` після `int.Parse(raw)` — не досягається взагалі

Це принципово важливо: виняток негайно перериває нормальне виконання і передає керування механізму пошуку обробника.

## Якщо catch не знайдено ніде

Якщо CLR пройде весь стек і не знайде жодного відповідного `catch` — програма аварійно завершується. При цьому блоки `finally` **можуть не виконатися** (залежить від середовища та типу завершення). Саме тому завжди варто мати «страхувальний» `catch (Exception ex)` на верхньому рівні програми:

```csharp run
using System;

// Верхній рівень — перехоплює все непередбачене
try
{
    RunClinicSystem();
}
catch (Exception ex)
{
    Console.WriteLine($"Критична помилка системи: {ex.GetType().Name}");
    Console.WriteLine(ex.Message);
}

void RunClinicSystem()
{
    // Симулюємо необроблений виняток у глибині системи
    ProcessPatient("П-999", null!);
}

void ProcessPatient(string id, string name)
{
    // NullReferenceException — не перехоплюється ніде нижче
    Console.WriteLine($"Довжина імені: {name.Length.ToString()}");
}
```

## Практичний патерн: логування + перекидання

Поширений підхід — логувати помилку на проміжному рівні через `finally` або `catch + throw`, а фактично обробляти її вище:

```csharp run
using System;

try
{
    AdmitPatient("П-101", "Олена Коваль", "сорок п'ять");
}
catch (Exception ex)
{
    Console.WriteLine($"[UI] Не вдалося прийняти пацієнта: {ex.Message}");
}

void AdmitPatient(string id, string name, string ageInput)
{
    try
    {
        int age = int.Parse(ageInput);
        Console.WriteLine($"[{id}] {name}, {age.ToString()} р. прийнято.");
    }
    catch (FormatException ex)
    {
        // логуємо деталь на цьому рівні
        Console.WriteLine($"[Лог] ParseError у AdmitPatient: «{ageInput}» → {ex.Message}");
        throw; // перекидаємо вище — без зміни StackTrace
    }
}
```

`throw;` (без аргументу) зберігає оригінальний об'єкт і стек — верхній рівень отримає точне місце першопричини. Якщо написати `throw ex;` — стек скинеться до місця перекидання, що ускладнює діагностику.

## Підсумок: алгоритм CLR при винятку

1. Виняток виникає у методі N
2. **Фаза пошуку:** CLR перевіряє рівні стека знизу вгору: N → N-1 → ... → точка входу
3. На кожному рівні перевіряє: чи є `catch`, чий тип відповідає винятку і чий `when`-фільтр (якщо є) дає `true`
4. Якщо знайдено → **фаза розкрутки:** виконує `finally` від рівня N до рівня знахідки, потім сам `catch`
5. Якщо не знайдено ніде → аварійне завершення програми
6. Код після `try...catch` на рівнях без обробника **не виконується**; код після `try...catch` на рівні з обробником — виконується нормально
