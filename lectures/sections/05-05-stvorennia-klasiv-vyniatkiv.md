---
chapter: 5
chapterTitle: "Розділ 5. Обробка винятків"
section: 5
number: "5.5"
title: "Створення класів винятків"
source: "../_combined/32-stvorennia-klasiv-vyniatkiv.md"
---

## 5.5. Створення класів винятків

Вбудованих типів винятків (.NET надає їх понад 200) часто достатньо для технічних помилок. Але для **доменних помилок** — тих, що описують порушення бізнес-правил конкретної системи, — краще створювати власні класи винятків. Це дозволяє:

- точно вказувати `catch` на потрібну категорію помилок
- передавати у виняток додаткову доменну інформацію (ID пацієнта, некоректне значення)
- будувати ієрархії винятків під свою предметну область

## Мінімальний власний клас винятку

Будь-який клас, що успадковується від `Exception`, є повноцінним типом винятку. Мінімальна реалізація — конструктор із рядком повідомлення:

```csharp run
using System;

try
{
    RegisterPatient("Tom", 17);
}
catch (PatientException ex)
{
    Console.WriteLine($"Помилка пацієнта: {ex.Message}");
}

void RegisterPatient(string name, int age)
{
    if (age < 0 || age > 150)
        throw new PatientException($"Вік {age.ToString()} є неприпустимим для пацієнта.");
    Console.WriteLine($"Зареєстровано: {name}, {age.ToString()} р.");
}

class PatientException : Exception
{
    public PatientException(string message) : base(message) { }
}
```

Конструктор передає рядок у базовий `Exception` через `base(message)`. Тепер у `catch` можна точно вказати `PatientException` — і він не перехопить `FormatException` чи `NullReferenceException`.

## Власні властивості у класі винятку

Справжня сила власних винятків — можливість зберігати доменні дані прямо в об'єкті помилки. Наприклад, некоректне значення, ID пацієнта, назву поля:

```csharp run
using System;

try
{
    RegisterPatient("Марія Сидоренко", -5);
}
catch (PatientAgeException ex)
{
    Console.WriteLine($"Помилка: {ex.Message}");
    Console.WriteLine($"Некоректний вік: {ex.InvalidAge.ToString()} р.");
}

void RegisterPatient(string name, int age)
{
    if (age < 0 || age > 150)
        throw new PatientAgeException(
            $"Вік {age.ToString()} виходить за допустимий діапазон (0–150).", age);
    Console.WriteLine($"Зареєстровано: {name}, {age.ToString()} р.");
}

class PatientAgeException : Exception
{
    public int InvalidAge { get; }

    public PatientAgeException(string message, int invalidAge) : base(message)
    {
        InvalidAge = invalidAge;
    }
}
```

Властивість `InvalidAge` дозволяє обробнику отримати конкретне значення, що спричинило помилку — без парсингу рядка `Message`. Це зручно для логування та відображення деталей у UI.

## Вибір базового класу

Власний виняток не обов'язково успадковувати від кореневого `Exception`. Якщо є більш підходящий вбудований тип — краще успадкувати від нього. Тоді `catch (ArgumentException)` також перехопить ваш клас:

```csharp run
using System;

// catch (ArgumentException) перехопить PatientValidationException теж
try
{
    SetDiagnosis("П-001", "");
}
catch (PatientValidationException ex)
{
    Console.WriteLine($"Валідація: {ex.Message} (поле: {ex.FieldName})");
}
catch (ArgumentException ex)
{
    Console.WriteLine($"Аргумент: {ex.Message}");
}

void SetDiagnosis(string patientId, string diagnosis)
{
    if (string.IsNullOrWhiteSpace(diagnosis))
        throw new PatientValidationException(
            "Діагноз не може бути порожнім.", nameof(diagnosis));
}

// Успадковуємо від ArgumentException — семантично коректно:
// це помилка некоректного аргументу в доменному контексті
class PatientValidationException : ArgumentException
{
    public string FieldName { get; }

    public PatientValidationException(string message, string fieldName)
        : base(message)
    {
        FieldName = fieldName;
    }
}
```

## Ієрархія власних винятків

Для складніших систем будують цілі ієрархії. Базовий доменний виняток об'єднує всі помилки предметної області, а конкретні типи уточнюють причину:

![Ієрархія власних класів винятків клінічної системи](_assets/05-05/custom-exception-hierarchy.png)

```csharp run
using System;

ProcessRecord("П-001", "Іван Петренко", 45, "J18.9");
ProcessRecord("П-002", "", 30, "J18.9");
ProcessRecord("П-003", "Олег Бойко", -3, "J18.9");
ProcessRecord("П-004", "Марія Коваль", 28, "");

void ProcessRecord(string id, string name, int age, string diagnosisCode)
{
    try
    {
        ValidateRecord(id, name, age, diagnosisCode);
        Console.WriteLine($"[{id}] {name}, {age.ToString()} р., діагноз: {diagnosisCode} — збережено.");
    }
    catch (PatientAgeException ex)
    {
        Console.WriteLine($"[{id}] Вік: {ex.Message} (значення: {ex.InvalidAge.ToString()})");
    }
    catch (DiagnosisException ex)
    {
        Console.WriteLine($"[{id}] Діагноз: {ex.Message} (код: {ex.DiagnosisCode})");
    }
    catch (MedicalException ex)
    {
        // перехоплює будь-який MedicalException, що не потрапив вище
        Console.WriteLine($"[{id}] Медична помилка: {ex.Message}");
    }
}

void ValidateRecord(string id, string name, int age, string diagnosisCode)
{
    if (string.IsNullOrWhiteSpace(name))
        throw new MedicalException("Ім'я пацієнта не може бути порожнім.", id);

    if (age < 0 || age > 150)
        throw new PatientAgeException(
            $"Неприпустимий вік для пацієнта.", id, age);

    if (string.IsNullOrWhiteSpace(diagnosisCode))
        throw new DiagnosisException(
            "Код діагнозу не може бути порожнім.", id, diagnosisCode ?? "");
}

// Базовий доменний виняток
class MedicalException : Exception
{
    public string PatientId { get; }

    public MedicalException(string message, string patientId) : base(message)
    {
        PatientId = patientId;
    }
}

// Конкретний: помилка віку
class PatientAgeException : MedicalException
{
    public int InvalidAge { get; }

    public PatientAgeException(string message, string patientId, int invalidAge)
        : base(message, patientId)
    {
        InvalidAge = invalidAge;
    }
}

// Конкретний: помилка діагнозу
class DiagnosisException : MedicalException
{
    public string DiagnosisCode { get; }

    public DiagnosisException(string message, string patientId, string diagnosisCode)
        : base(message, patientId)
    {
        DiagnosisCode = diagnosisCode;
    }
}
```

Ієрархія дає гнучкість: можна перехопити конкретний тип або всі помилки предметної області через базовий `MedicalException`.

## Де оголошувати власні класи винятків

Кілька практичних правил:

- Ім'я завжди завершується словом `Exception`: `PatientAgeException`, `DiagnosisException`
- Клас розташовують поруч із тим, де він використовується (або в окремому файлі для великих проєктів)
- Якщо виняток вказує на некоректний аргумент — успадковуйте від `ArgumentException`
- Якщо виняток описує стан об'єкта, що не дозволяє операцію — від `InvalidOperationException`
- Якщо помилка специфічна для вашої предметної області — від `Exception` або власного базового

## Підсумок

- Власний клас винятку — це звичайний клас, що успадковує `Exception` (або його похідний)
- Мінімальна реалізація: конструктор з `string message`, що передає його в `base(message)`
- Додаткові властивості зберігають доменний контекст: ID, некоректне значення, назву поля
- Ієрархії дозволяють перехоплювати як конкретні типи, так і всю категорію помилок
- Ім'я класу завжди закінчується на `Exception`
