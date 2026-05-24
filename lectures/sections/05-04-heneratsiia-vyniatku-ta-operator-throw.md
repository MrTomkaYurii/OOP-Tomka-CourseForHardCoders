---
chapter: 5
chapterTitle: "Розділ 5. Обробка винятків"
section: 4
number: "5.4"
title: "Генерація винятку та оператор throw"
source: "../_combined/31-heneratsiia-vyniatku-ta-operator-throw.md"
---

## 5.4. Генерація винятку та оператор throw

До цього моменту ми розглядали лише **перехоплення** винятків, які генерує сама система. Але в C# будь-який метод може **генерувати виняток вручну** — оператором `throw`. Це ключовий інструмент для впровадження бізнес-правил і валідації даних.

## Навіщо генерувати виняток вручну

Іноді дані технічно коректні (рядок не порожній, число у діапазоні), але порушують бізнес-правило. Наприклад:

- вік пацієнта не може бути від'ємним
- діагноз не може бути порожнім рядком
- ідентифікатор картки повинен починатися з певного префікса

У таких випадках система не знає, що дані некоректні — це знаємо лише ми. Оператор `throw` дозволяє сигналізувати про помилку стандартним механізмом винятків.

![Дві форми оператора throw та ланцюжок винятків](_assets/05-04/throw-forms.png)

## Форма 1: throw new — генерація нового винятку

```csharp
throw new ExceptionType("повідомлення про помилку");
```

Після `throw` вказується **новий об'єкт** будь-якого класу винятку. Рядок у конструкторі стає значенням властивості `Message`.

```csharp run
using System;

RegisterPatient("Іван Петренко", 45);
RegisterPatient("", 30);
RegisterPatient("Марія Сидоренко", -5);

void RegisterPatient(string name, int age)
{
    if (string.IsNullOrWhiteSpace(name))
        throw new ArgumentException("Ім'я пацієнта не може бути порожнім.");

    if (age < 0 || age > 150)
        throw new ArgumentOutOfRangeException(nameof(age),
            $"Вік {age.ToString()} є неприпустимим значенням.");

    Console.WriteLine($"Зареєстровано: {name}, {age.ToString()} р.");
}
```

Цей код не компілюється у повноцінний runnable без try/catch навколо. Загорнемо виклики:

```csharp run
using System;

TryRegister("Іван Петренко", 45);
TryRegister("", 30);
TryRegister("Марія Сидоренко", -5);

void TryRegister(string name, int age)
{
    try
    {
        RegisterPatient(name, age);
    }
    catch (ArgumentException ex)
    {
        Console.WriteLine($"Помилка реєстрації: {ex.Message}");
    }
}

void RegisterPatient(string name, int age)
{
    if (string.IsNullOrWhiteSpace(name))
        throw new ArgumentException("Ім'я пацієнта не може бути порожнім.");

    if (age < 0 || age > 150)
        throw new ArgumentOutOfRangeException(nameof(age),
            $"Вік {age.ToString()} є неприпустимим значенням.");

    Console.WriteLine($"Зареєстровано: {name}, {age.ToString()} р.");
}
```

Зверніть увагу: `throw` у методі `RegisterPatient` не потребує `try...catch` всередині нього. Виняток «спливає» вгору до місця виклику, де і перехоплюється.

## Throw у методах: валідація аргументів

Найпоширеніший патерн — перевіряти аргументи на початку методу і кидати `ArgumentException` або `ArgumentNullException` при порушенні:

```csharp run
using System;

SetBloodPressure("П-001", 120, 80);
SetBloodPressure("П-002", 300, 80);   // некоректний тиск
SetBloodPressure("П-003", 120, -10);  // некоректне значення

void SetBloodPressure(string patientId, int systolic, int diastolic)
{
    try
    {
        ValidatePressure(systolic, diastolic);
        Console.WriteLine($"[{patientId}] Тиск: {systolic.ToString()}/{diastolic.ToString()} мм рт.ст.");
    }
    catch (ArgumentOutOfRangeException ex)
    {
        Console.WriteLine($"[{patientId}] {ex.Message}");
    }
}

void ValidatePressure(int systolic, int diastolic)
{
    if (systolic < 60 || systolic > 250)
        throw new ArgumentOutOfRangeException(nameof(systolic),
            $"Систолічний тиск {systolic.ToString()} поза нормою (60–250).");
    if (diastolic < 40 || diastolic > 150)
        throw new ArgumentOutOfRangeException(nameof(diastolic),
            $"Діастолічний тиск {diastolic.ToString()} поза нормою (40–150).");
}
```

## Форма 2: throw без аргументів — перекидання винятку

Оператор `throw` без об'єкта можна використовувати **лише всередині блоку `catch`**. Він повторно кидає той самий виняток, що перехоплено — без змін і зі збереженням оригінального стека викликів:

```csharp run
using System;

try
{
    ProcessMedicalRecord("P-001", "not-a-number");
}
catch (Exception ex)
{
    Console.WriteLine($"[Зовнішній catch] {ex.GetType().Name}: {ex.Message}");
}

void ProcessMedicalRecord(string id, string ageInput)
{
    try
    {
        int age = int.Parse(ageInput);
        Console.WriteLine($"[{id}] Вік: {age.ToString()} р.");
    }
    catch (FormatException ex)
    {
        Console.WriteLine($"[{id}] Логування помилки: {ex.Message}");
        throw;   // перекидаємо далі — зовнішній catch отримає той самий об'єкт
    }
}
```

Внутрішній `catch` логує помилку, але не пригнічує її — `throw;` передає виняток зовнішньому блоку. **Стек викликів залишається незмінним**: зовнішній обробник бачить оригінальне місце виникнення помилки.

## throw; vs throw ex; — важлива різниця

```csharp
// Правильно — зберігає оригінальний StackTrace:
catch (Exception ex)
{
    Log(ex);
    throw;
}

// Небезпечно — скидає StackTrace до цього рядка:
catch (Exception ex)
{
    Log(ex);
    throw ex;   // StackTrace тепер вказує на цей рядок, а не на першопричину
}
```

`throw ex;` замінює стек викликів на поточне місце, що ускладнює діагностику — у логах не буде видно, де насправді сталася помилка. Завжди використовуйте `throw;` для перекидання.

## Ланцюжок винятків через InnerException

Іноді доцільно «загорнути» низькорівневий виняток у вищорівневий — зі збереженням оригіналу як `InnerException`. Це дозволяє надати більш змістовний контекст, не втрачаючи першопричину:

```csharp run
using System;

LoadPatientRecord("P-001", "45");
LoadPatientRecord("P-002", "??");

void LoadPatientRecord(string id, string rawAge)
{
    try
    {
        int age = ParseAge(rawAge);
        Console.WriteLine($"[{id}] Вік: {age.ToString()} р. — завантажено.");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"[{id}] Помилка: {ex.Message}");
        if (ex.InnerException != null)
            Console.WriteLine($"       Причина: {ex.InnerException.Message}");
    }
}

int ParseAge(string raw)
{
    try
    {
        return int.Parse(raw);
    }
    catch (FormatException ex)
    {
        // загортаємо у більш змістовний виняток, зберігаючи оригінал
        throw new InvalidOperationException(
            $"Не вдалося розпізнати вік зі значення «{raw}».", ex);
    }
}
```

Конструктор більшості класів винятків приймає другим параметром `innerException`. Завдяки цьому зовнішній код може перевірити `ex.InnerException` і отримати повний ланцюжок причин.

## Підсумок

| Форма | Де використовується | Що робить |
|-------|-------------------|-----------|
| `throw new Ex("msg")` | Будь-де | Генерує новий виняток |
| `throw new Ex("msg", innerEx)` | Будь-де | Генерує виняток із збереженням причини |
| `throw;` | Лише у `catch` | Перекидає поточний виняток, зберігаючи StackTrace |
| `throw ex;` | Лише у `catch` | Перекидає з **новим** StackTrace — уникайте |

`throw` у методі — це не помилка, а норма. Метод має «кидати» виняток, якщо не може виконати свою роботу коректно. Обробку помилки слід залишати тому рівню, який знає, що з нею робити.
