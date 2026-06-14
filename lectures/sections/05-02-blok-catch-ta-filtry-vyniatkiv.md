---
chapter: 5
chapterTitle: "Розділ 5. Обробка винятків"
section: 2
number: "5.2"
title: "Блок catch та фільтри винятків"
source: "../_combined/29-blok-catch-ta-filtry-vyniatkiv.md"
---

## 5.2. Блок catch та фільтри винятків

Блок `catch` є серцем механізму обробки винятків. Він визначає, які саме винятки перехоплюються і яку інформацію про помилку надає розробнику. У C# є три форми блоку `catch`, а також можливість задати додатковий фільтр через `when`.

![Форми блоку catch та фільтр when](_assets/05-02/catch-forms.png)

## Форма 1: catch без параметрів

Найпростіший варіант — `catch` без вказання типу. Такий блок перехоплює **будь-який** виняток, незалежно від його типу:

```csharp
catch
{
    // виконується при будь-якому винятку
}
```

Це зручно на початку або коли тип помилки не важливий. Недолік: немає доступу до інформації про виняток — невідомо, що саме сталося.

```csharp run
using System;

string[] inputs = { "36.6", "abc", "37.2" };

foreach (string raw in inputs)
{
    try
    {
        double temp = double.Parse(raw);
        Console.WriteLine($"Температура: {temp.ToString()} °C");
    }
    catch
    {
        Console.WriteLine($"Помилка читання: «{raw}» — значення пропущено.");
    }
}
```

## Форма 2: catch з типом винятку

Якщо вказати тип у дужках, блок `catch` перехопить **лише** цей тип (або його похідні). Винятки інших типів через цей блок не пройдуть:

```csharp
catch (FormatException)
{
    // обробляє лише FormatException
}
```

```csharp run
using System;

string input = "не_число";

try
{
    int age = int.Parse(input);
    Console.WriteLine($"Вік: {age.ToString()} р.");
}
catch (FormatException)
{
    Console.WriteLine("Вік введено у некоректному форматі.");
}
catch (OverflowException)
{
    Console.WriteLine("Число виходить за допустимий діапазон.");
}
```

Тут два блоки `catch` — кожен обробляє свій тип. Якщо рядок некоректний — спрацьовує `FormatException`. Якщо число занадто велике — `OverflowException`. Якщо виникне інший тип помилки — жоден блок не перехопить його.

**Важливо:** блоки `catch` перевіряються **зверху вниз** у порядку оголошення. Спрацьовує перший відповідний.

## Форма 3: catch з типом і змінною

Найінформативніша форма: дає доступ до об'єкта винятку через іменовану змінну. Змінна містить усю доступну інформацію про помилку — передусім властивість `Message`:

```csharp
catch (FormatException ex)
{
    Console.WriteLine(ex.Message); // деталі помилки
}
```

```csharp run
using System;

RegisterPatient("Іван Петренко", "45");
RegisterPatient("Марія Сидоренко", "??");
RegisterPatient("Олег Бойко", "999999999999");

void RegisterPatient(string name, string ageInput)
{
    try
    {
        int age = int.Parse(ageInput);
        Console.WriteLine($"Зареєстровано: {name}, {age.ToString()} р.");
    }
    catch (FormatException ex)
    {
        Console.WriteLine($"[{name}] Некоректний формат віку: {ex.Message}");
    }
    catch (OverflowException ex)
    {
        Console.WriteLine($"[{name}] Вік поза допустимим діапазоном: {ex.Message}");
    }
}
```

Властивість `ex.Message` містить зрозумілий опис помилки від CLR. Це особливо корисно для логування: у виробничих системах повідомлення про помилку зазвичай записується у журнал, а не виводиться користувачу напряму.

## Фільтри винятків: when

Оператор `when` дозволяє додати **умову** до блоку `catch`. Блок спрацює лише якщо умова повертає `true`:

```csharp
catch (ExceptionType ex) when (умова)
{
    // виконується лише якщо умова == true
}
```

Якщо умова `false` — CLR продовжує шукати наступний відповідний `catch`, навіть якщо тип збігається.

Практичний приклад: в медичній системі ввід пульсу обробляється по-різному залежно від того, чи рядок порожній, чи містить некоректні символи:

```csharp run
using System;

ProcessPulse("");        // порожній рядок
ProcessPulse("abc");     // некоректні символи
ProcessPulse("72");      // коректне значення

void ProcessPulse(string input)
{
    try
    {
        if (string.IsNullOrEmpty(input))
            throw new FormatException("рядок порожній");

        int pulse = int.Parse(input);
        Console.WriteLine($"Пульс: {pulse.ToString()} уд/хв");
    }
    catch (FormatException ex) when (string.IsNullOrEmpty(input))
    {
        Console.WriteLine($"Пульс не введено (порожній рядок): {ex.Message}");
    }
    catch (FormatException ex)
    {
        Console.WriteLine($"Некоректне значення пульсу «{input}»: {ex.Message}");
    }
}
```

Обидва `catch` обробляють `FormatException`, але:
- перший — лише якщо `input` порожній (`when (string.IsNullOrEmpty(input))`)
- другий — у всіх інших випадках `FormatException`

Це дозволяє розрізнити різні смислові сценарії для одного типу винятку — без вкладених `if` у тілі `catch`.

## Антипатерн: «ковтання» винятків

Один із найпоширеніших і найнебезпечніших патернів — блок `catch`, що не робить нічого або просто виводить повідомлення, але не сигналізує про помилку далі:

```csharp
// ПОГАНО — помилка «ковтається», програма продовжує роботу з пошкодженим станом:
try
{
    int age = int.Parse(input);
    SaveToDatabase(age);
}
catch (Exception)
{
    // нічого не робимо
}
```

У медичній системі це особливо небезпечно: якщо `SaveToDatabase` кинула виняток (зв'язок з БД обірвався), а помилка «ковтнута» — дані пацієнта мовчки не зберігаються. Система вважає, що все добре, але картка так і не записана.

```csharp run
using System;

// Симуляція: критична помилка "ковтається"
string patientData = "P-1001";

Console.WriteLine("=== Антипатерн: ковтання помилки ===");
try
{
    SaveRecord(patientData); // кинуть Exception
}
catch (Exception)
{
    // нічого — помилка зникла
}
Console.WriteLine("Програма вважає, що дані збережено. Насправді — ні.");

Console.WriteLine("\n=== Правильно: логувати і перекидати або обробляти явно ===");
try
{
    SaveRecord(patientData);
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"[ПОМИЛКА ЗБЕРЕЖЕННЯ] {ex.Message}");
    // у реальному коді: logger.Error(ex), повернути false/Result, або throw
    throw; // перекидаємо, щоб вище знали про помилку
}
catch (Exception ex)
{
    Console.WriteLine($"[КРИТИЧНА ПОМИЛКА] {ex.GetType().Name}: {ex.Message}");
    throw;
}

void SaveRecord(string data) =>
    throw new InvalidOperationException($"З'єднання з БД втрачено під час запису {data}.");
```

Правила:
- **Ніколи не залишайте `catch` порожнім** у виробничому коді — принаймні логуйте виняток
- **`catch (Exception)`** — тільки на верхньому рівні (main loop, middleware), і лише якщо ви справді знаєте, що з ним робити
- Якщо не знаєте, як обробити виняток — використовуйте `throw;`, щоб він «спливав» вище

## Порядок блоків catch

Кілька блоків `catch` перевіряються у порядку оголошення. Є одне важливе правило: **загальніший тип має йти після конкретнішого**. Наприклад, `Exception` (базовий тип для всіх) повинен бути останнім, інакше він перехопить усе раніше:

```csharp run
using System;

string[] records = { "120", "abc", "0", "37" };

foreach (string r in records)
{
    try
    {
        int val = int.Parse(r);
        if (val == 0) throw new DivideByZeroException();
        Console.WriteLine($"Значення: {val.ToString()}");
    }
    catch (FormatException ex)
    {
        Console.WriteLine($"Формат: {ex.Message}");
    }
    catch (DivideByZeroException)
    {
        Console.WriteLine("Значення не може бути нулем.");
    }
    catch (Exception ex)
    {
        // загальний — завжди останнім
        Console.WriteLine($"Невідома помилка: {ex.Message}");
    }
}
```

Якщо поставити `catch (Exception ex)` першим — він перехопить усе, і специфічні блоки ніколи не виконаються. Компілятор попередить про недосяжний код.

## Підсумок

| Форма | Синтаксис | Що перехоплює |
|-------|-----------|---------------|
| Без параметрів | `catch { }` | Будь-який виняток |
| З типом | `catch (FormatException) { }` | Лише вказаний тип |
| З типом і змінною | `catch (FormatException ex) { }` | Лише вказаний тип + доступ до `ex.Message` |
| З фільтром | `catch (FormatException ex) when (умова) { }` | Тип збігається **і** умова `true` |

Блоки перевіряються зверху вниз. Загальніший тип (`Exception`) завжди ставте останнім.
