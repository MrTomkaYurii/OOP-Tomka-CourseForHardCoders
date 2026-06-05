---
chapter: 9
chapterTitle: "Розділ 9. Pattern matching"
section: 2
number: "9.2"
title: "Патерн властивостей"
source: "../_combined/57-patern-vlastyvostei.md"
---

## 9.2. Патерн властивостей

Патерн типів (9.1) перевіряє, **чим є** об'єкт. Але часто нас цікавить не тільки тип, а й **конкретні значення** його властивостей: «чи є це пацієнт з активним статусом і пріоритетом вище 2?». Для цього існує **патерн властивостей** (property pattern) — він дозволяє перевіряти відповідність значень полів об'єкта прямо у виразі `is` або `switch`.

## Синтаксис і анатомія

Патерн властивостей записується у фігурних дужках: `{ Властивість: значення }`. Двокрапка тут не присвоєння, а **порівняння**: «властивість має це значення». Значенням може бути константа, null, інший патерн (у тому числі реляційний `> 2`) або `var` для захоплення.

![Патерн властивостей: анатомія та варіанти](_assets/09-02/property-pattern-anatomy.png)

Патерн властивостей може стояти окремо або бути частиною складнішого патерну, де зліва вказано тип:

```csharp
// Тільки властивості (без перевірки типу)
if (patient is { Status: "Active" })

// Тип + властивості разом
if (patient is Patient { Status: "Active", Priority: > 2 })
```

У другій формі спочатку перевіряється тип (`Patient`), і якщо він збігається — перевіряються властивості.

## Базовий приклад у клінічному контексті

```csharp run
using System;

// Виконуваний код
var patients = new[]
{
    new Patient("Іван Петренко",  "Active",   priority: 3, "Кардіологія"),
    new Patient("Марія Коваль",   "Active",   priority: 1, "Неврологія"),
    new Patient("Олег Сидоренко", "Discharge",priority: 2, "Хірургія"),
    new Patient("Ганна Мельник",  "Active",   priority: 5, "Реанімація"),
};

foreach (var p in patients)
    Console.WriteLine($"{p.Name}: {GetPriority(p)}");

string GetPriority(Patient p) => p switch
{
    { Status: "Active", Priority: > 3 }  => "ТЕРМІНОВО — негайна увага",
    { Status: "Active", Priority: > 1 }  => "Активний — плановий огляд",
    { Status: "Active" }                 => "Активний — рутинний",
    { Status: "Discharge" }              => "Виписка оформляється",
    _                                    => "Невизначено",
};

// Клас
class Patient
{
    public string Name       { get; }
    public string Status     { get; }
    public int    Priority   { get; }
    public string Department { get; }

    public Patient(string name, string status, int priority, string dept)
    {
        Name = name; Status = status; Priority = priority; Department = dept;
    }
}
```

Зверніть увагу: `Priority: > 3` — це поєднання патерну властивостей з реляційним патерном. Значення `Priority` перевіряється не на рівність, а на виконання умови `> 3`. Патерни в C# **вкладаються** один в одного.

## Захоплення значення через var

Іноді нам потрібно не лише перевірити значення властивості, а й **зберегти** його у змінну для подальшого використання у виразі результату. Для цього замість конкретного значення пишуть `var ім'я`:

```csharp
string GetWelcome(Patient? p) => p switch
{
    { Status: "Active", Department: var dept } => $"Пацієнт активний, відділення: {dept}",
    { Status: var s }                          => $"Статус: {s}",
    null                                       => "Пацієнт не знайдений"
};
```

`Department: var dept` означає: «захопити значення властивості `Department` у змінну `dept`» — і тоді використати `dept` у рядку результату. Перевірка типу при цьому не виконується: `var` завжди успішно збігається з будь-яким значенням (у тому числі `null`).

## Вкладені об'єкти (C# 10+)

Якщо об'єкт містить вкладені об'єкти, патерн властивостей може заглиблюватись у них. До C# 10 для цього потрібен був вкладений патерн:

```csharp
// До C# 10 — явне вкладення
if (patient is { Department: { Name: "Кардіологія" } })

// C# 10+ — скорочений точковий запис
if (patient is { Department.Name: "Кардіологія" })
```

Обидва варіанти еквівалентні, але точковий синтаксис C# 10 значно компактніший.

```csharp run
using System;

// Виконуваний код
var patients = new[]
{
    new Patient("Іван Петренко",  new Department("Кардіологія", isIntensive: false)),
    new Patient("Марія Коваль",   new Department("Реанімація",  isIntensive: true)),
    new Patient("Олег Сидоренко", new Department("Хірургія",    isIntensive: false)),
};

foreach (var p in patients)
    Console.WriteLine($"{p.Name}: {GetAlert(p)}");

string GetAlert(Patient p) => p switch
{
    // Вкладений патерн — перевірка властивості вкладеного об'єкта
    { Department.IsIntensive: true }             => "РЕАНІМАЦІЯ — постійний моніторинг",
    { Department.Name: "Кардіологія" }           => "Кардіо-відділення — ЕКГ щодня",
    { Department: { Name: var name } }           => $"Відділення {name} — стандартний режим",
    _                                            => "Невідомо",
};

// Класи
class Department
{
    public string Name        { get; }
    public bool   IsIntensive { get; }
    public Department(string name, bool isIntensive)
    { Name = name; IsIntensive = isIntensive; }
}
class Patient
{
    public string     Name       { get; }
    public Department Department { get; }
    public Patient(string name, Department dept) { Name = name; Department = dept; }
}
```

## Порожній патерн властивостей {}

Фігурні дужки без вмісту `{}` — це особливий випадок: він **збігається з будь-яким non-null об'єктом**:

```csharp
string Describe(Patient? p) => p switch
{
    { Status: "Active" } => "Активний пацієнт",
    { }                  => "Пацієнт (не активний)", // будь-який не-null
    null                 => "Null"
};
```

`{}` часто стоїть передостанньою гілкою в switch як «запасний варіант для не-null» перед явною перевіркою на `null`.

## Поєднання типового та властивісного патернів

Обидва патерни можна поєднувати: спочатку перевірка типу, потім — властивостей. Це особливо зручно в ієрархіях:

```csharp
string GetInfo(MedicalStaff s) => s switch
{
    Doctor { IsOnLeave: false, Specialty: var spec } => $"Лікар на зміні: {spec}",
    Doctor { IsOnLeave: true }                       => "Лікар у відпустці",
    Nurse  { Ward: var ward }                        => $"Медсестра: палата {ward}",
    _                                                => "Персонал"
};
```

Тут `Doctor { IsOnLeave: false, Specialty: var spec }` — патерн типу `Doctor` (type pattern), що одночасно перевіряє властивість `IsOnLeave` (property pattern) і захоплює `Specialty` у змінну `spec` (var capture).

Такі поєднання роблять `switch expression` потужним інструментом для опису складної бізнес-логіки у компактній, декларативній формі — без глибоких вкладених `if-else`.
