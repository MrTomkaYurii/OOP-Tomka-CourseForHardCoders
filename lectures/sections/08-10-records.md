---
chapter: 8
chapterTitle: "Розділ 8. Додаткові можливості ООП у C#"
section: 10
number: "8.10"
title: "Records"
source: "../_combined/55-records.md"
---

## 8.10. Records

У більшості програм існують об'єкти двох принципово різних призначень. Одні — **сутності з ідентичністю**: конкретний пацієнт, конкретний лікар. Їх ідентифікують не за значеннями полів, а за посиланням на конкретний об'єкт у пам'яті. Два різні пацієнти з однаковим іменем — це різні люди. Для таких об'єктів добре підходить звичайний клас з посилальною рівністю.

Інші — **контейнери значень** (value objects): діагноз, дата прийому, результат аналізу, адреса, медичний запис. Тут два об'єкти з однаковим вмістом семантично рівні. «Діагноз "гіпертонія"» і ще один «діагноз "гіпертонія"» — це одне й те саме. Для таких об'єктів ми хочемо **структурну рівність** (як у `string`) і незмінність після створення. Раніше для цього доводилось вручну перевизначати `Equals`, `GetHashCode`, `ToString` та реалізовувати operator `==`. **Records** (C# 9) вирішують цю задачу: компілятор генерує весь цей код автоматично.

## Що компілятор генерує автоматично

Один рядок позиційного record:

```csharp
public record Patient(string Name, int Age);
```

замінює близько 50 рядків класу з усіма необхідними членами.

![Record: один рядок коду → що генерує компілятор](_assets/08-10/record-generated-members.png)

**Конструктор** — приймає всі параметри позиційного запису.

**init-властивості** — автоматично генеруються з readonly-семантикою: `public string Name { get; init; }`. Встановити можна тільки при конструюванні або в ініціалізаторі об'єкта — після цього значення зафіксоване.

**Структурна рівність** — `Equals`, `==`, `!=` порівнюють за значеннями всіх властивостей, а не за посиланням.

**`GetHashCode`** — генерується на основі значень властивостей, узгоджений з `Equals`.

**`ToString`** — виводить `Patient { Name = Іван, Age = 45 }` — зручно для логування та діагностики.

**`Deconstruct`** — дозволяє декомпозицію `var (name, age) = patient;`.

**`<Clone>()`** — внутрішній метод для підтримки оператора `with`.

## Модифікатор init

`init` — це особливий тип сеттера, введений у C# 9. Властивість з `init` можна встановити **тільки** в двох місцях:
- у конструкторі;
- в ініціалізаторі об'єкта (`new Patient { Name = "Іван" }`).

Після виходу з конструктора або ініціалізатора значення «замерзає» — будь-яка подальша спроба присвоєння спричиняє помилку компіляції. Це принципово відрізняється від `set` (можна змінити будь-коли) і від `readonly`-поля (можна встановити тільки в конструкторі, але не в ініціалізаторі).

```csharp
public record Patient
{
    public string Name { get; init; } = "";
    public int Age    { get; init; }
}

var p = new Patient { Name = "Іван", Age = 45 }; // OK — ініціалізатор
p.Name = "Марія"; // помилка компіляції — init вже завершено
```

## Синтаксис: повний та позиційний

**Повний синтаксис** — схожий на клас, але з ключовим словом `record`:

```csharp
public record Patient
{
    public string Name { get; init; }
    public int Age     { get; init; }

    public Patient(string name, int age)
    {
        Name = name;
        Age = age;
    }
}
```

**Позиційний синтаксис** — вся інформація в одному рядку:

```csharp
public record Patient(string Name, int Age);
```

Компілятор сам створює конструктор, `init`-властивості та `Deconstruct`. Позиційний синтаксис — це не скорочення повного, це повноцінна альтернатива. Якщо потрібні додаткові члени — їх можна дописати у тілі:

```csharp
public record Patient(string Name, int Age)
{
    public bool IsAdult => Age >= 18;
    public string Diagnosis { get; set; } = ""; // звичайна мутабельна властивість
}
```

## Оператор with

`with` — оператор немутабельного оновлення. Він створює **копію** record зі зміненими вказаними властивостями:

```csharp
var original = new Patient("Іван Петренко", 45);
var updated  = original with { Age = 46 }; // новий об'єкт; Name = "Іван Петренко"
```

`original` при цьому не змінюється. Це ключова особливість: замість того, щоб мутувати об'єкт, ми отримуємо новий з оновленими даними. Такий підхід — «незмінні дані + нові версії» — є основою функціонального програмування і безпечний при роботі з кількома потоками.

Внутрішньо `with` викликає `<Clone>()` і потім встановлює `init`-властивості через ініціалізатор. Оператор `with` працює тільки з `record` — для звичайних класів він недоступний.

## Структурна рівність

Для `record` компілятор генерує рівність за значеннями, а не за посиланням. Два різні об'єкти з однаковими даними рівні:

```csharp run
using System;

// Виконуваний код
var p1 = new Patient("Іван Петренко", 45);
var p2 = new Patient("Іван Петренко", 45); // різні об'єкти, однакові дані
var p3 = new Patient("Марія Коваль",  32);

Console.WriteLine($"p1 == p2: {p1 == p2}");      // true
Console.WriteLine($"p1 == p3: {p1 == p3}");      // false
Console.WriteLine($"Equals:   {p1.Equals(p2)}"); // true

// with — незмінне оновлення
var updated = p1 with { Age = 46 };
Console.WriteLine($"p1:      {p1}");     // вихідний не змінився
Console.WriteLine($"updated: {updated}"); // новий з Age=46

// Deconstruct
var (name, age) = p1;
Console.WriteLine($"Декомпозиція: {name}, {age}");

// record
public record Patient(string Name, int Age);
```

Порівняємо з класом:

```csharp run
using System;

// Виконуваний код
// record — структурна рівність
var r1 = new MedicalRecord("Гіпертонія II ст.", "2026-06-10");
var r2 = new MedicalRecord("Гіпертонія II ст.", "2026-06-10");
Console.WriteLine($"record r1 == r2: {r1 == r2}");  // true

// class — посилальна рівність (різні об'єкти — не рівні)
var c1 = new AppointmentClass("Гіпертонія II ст.", "2026-06-10");
var c2 = new AppointmentClass("Гіпертонія II ст.", "2026-06-10");
Console.WriteLine($"class  c1 == c2: {c1 == c2}");  // false

// ToString: record виводить вміст автоматично
Console.WriteLine(r1.ToString()); // MedicalRecord { Diagnosis = ..., Date = ... }

// record
public record MedicalRecord(string Diagnosis, string Date);

// class — без перевизначення Equals
public class AppointmentClass
{
    public string Diagnosis { get; }
    public string Date { get; }
    public AppointmentClass(string d, string date) { Diagnosis = d; Date = date; }
}
```

## Успадкування records

Record-класи можна успадковувати так само, як звичайні класи. Але є важлива деталь: при рівності враховується **фактичний тип** об'єкта. Компілятор генерує захищену властивість `EqualityContract`, яка повертає `typeof(Patient)`, `typeof(Doctor)` тощо. При порівнянні типи повинні збігатися.

```csharp run
using System;

// Виконуваний код
var person    = new MedicalPerson("Іван Петренко", 45);
var patient   = new ClinicPatient("Іван Петренко", 45, "Гіпертонія");
var patient2  = new ClinicPatient("Іван Петренко", 45, "Гіпертонія");

// Рівність record враховує тип!
Console.WriteLine($"person == patient:  {person.Equals(patient)}");   // false — різні типи
Console.WriteLine($"patient == patient2: {patient.Equals(patient2)}"); // true — однаковий тип і дані

Console.WriteLine(person);  // MedicalPerson { Name = Іван Петренко, Age = 45 }
Console.WriteLine(patient); // ClinicPatient { Name = ..., Age = ..., Diagnosis = ... }

// with працює і для похідних
var updated = patient with { Diagnosis = "Гіпертонія I ст." };
Console.WriteLine(updated);

// Records
public record MedicalPerson(string Name, int Age);
public record ClinicPatient(string Name, int Age, string Diagnosis) : MedicalPerson(Name, Age);
```

`EqualityContract` — це зв'язуюча ланка, яка гарантує: `Person { Name="Tom", Age=37 }` та `Employee { Name="Tom", Age=37 }` не рівні навіть при однакових значеннях полів. Це правильна поведінка: різні типи — різна ідентичність.

## record struct vs record class

Починаючи з C# 10, кортежний тип `record` можна визначити і як структуру:

```csharp
public record struct BloodPressure(int Systolic, int Diastolic);
```

Ключова відмінність від `record class`:

| Характеристика | `record class` | `record struct` | `readonly record struct` |
|---|---|---|---|
| Тип даних | reference (heap) | value (stack) | value (stack) |
| Null | може бути null | ні | ні |
| Mутабельність (позиційні) | init — immutable | set — **mutable** | init — immutable |
| Успадкування | так | ні | ні |
| `with` | так | так | так |
| Структурна рівність | так | так | так |

Важлива різниця: для **позиційного** `record struct` компілятор генерує звичайні `set`-сеттери (мутабельні), а для `record class` — `init`-сеттери (immutable). Щоб зробити `record struct` незмінним, потрібне `readonly`:

```csharp
public readonly record struct BloodPressure(int Systolic, int Diastolic);
```

`record struct` доречний для невеликих value objects, які часто копіюються: точки, координати, вимірювання — там де value type дає виграш у продуктивності.

## Підсумкова таблиця: record vs інші підходи

| | `record` | Анонімний тип | Кортеж | Клас |
|---|---|---|---|---|
| Іменований тип | ✓ | ✗ | ✓ (частково) | ✓ |
| Передача між методами | ✓ | ✗ (тільки object) | ✓ | ✓ |
| Структурна рівність | ✓ (авто) | ✓ (авто) | ✓ (авто) | ✗ (потрібно визначити) |
| Immutable | ✓ (init) | ✓ | ✗ (мутабельні) | ✓ (потрібно визначити) |
| `with` | ✓ | ✗ | ✗ | ✗ |
| Успадкування | ✓ (class) | ✗ | ✗ | ✓ |
| ToString (стан) | ✓ (авто) | ✓ (авто) | ✓ (авто) | ✗ (потрібно визначити) |
| Boilerplate | мінімальний | немає | немає | максимальний |

Records — ідеальний інструмент для **DTO** (Data Transfer Objects), **value objects** у доменній моделі, **результатів запитів**, **конфігураційних об'єктів**: скрізь, де об'єкт несе дані і ідентифікується за своїм вмістом, а не за посиланням на конкретний екземпляр.
