---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 8
number: "4.8"
title: "Узагальнення"
source: "../_combined/25-uzahalnennia.md"
---

## 4.8. Узагальнення

Крім звичайних типів, фреймворк .NET підтримує **узагальнені типи** (generics) — класи, структури, інтерфейси та методи, які параметризуються типом. Generics є одним із найважливіших механізмів C# і широко використовуються у стандартній бібліотеці: `List<T>`, `Dictionary<TKey, TValue>`, `Queue<T>` та багато інших.

## Проблема без узагальнень

Щоб зрозуміти навіщо потрібні generics, розглянемо задачу. У клінічній системі медична картка пацієнта може мати ідентифікатор різного типу: в одній системі це `int`, в іншій — `string` типу `"P-001"`, у третій — `Guid`. Як написати один клас, що підтримує всі варіанти?

Перше рішення — використати `object`, оскільки це базовий тип для всіх:

```csharp run
using System;

MedicalRecord r1 = new MedicalRecord(1001, "Гіпертонія");
MedicalRecord r2 = new MedicalRecord("P-001", "Бронхіт");

int id1 = (int)r1.Id;         // розпакування — додаткові витрати
string id2 = (string)r2.Id;

Console.WriteLine($"Картка #{id1.ToString()}: {r1.Description}");
Console.WriteLine($"Картка {id2}: {r2.Description}");

// Небезпечно: компілятор не зловить помилку — лише runtime!
try
{
    string wrongId = (string)r1.Id; // InvalidCastException
}
catch (InvalidCastException)
{
    Console.WriteLine("Помилка: невірне приведення типу");
}

class MedicalRecord
{
    public object Id { get; }
    public string Description { get; }

    public MedicalRecord(object id, string description)
    {
        Id = id;
        Description = description;
    }
}
```

Два суттєві недоліки цього підходу:

1. **Boxing/unboxing** — при передачі `int` у `object` відбувається упаковка (boxing): значення зі стека копіюється у купу, де для нього виділяється об'єкт-обгортка. Зворотна операція (розпакування) — теж копіювання. У гарячих ділянках коду це помітно знижує продуктивність.

2. **Відсутність типобезпеки** — компілятор не знає реального типу `Id`, тому не може попередити про неправильне приведення. Помилка виникне лише під час виконання як `InvalidCastException`.

## Узагальнений клас

Generics вирішують обидві проблеми. Замість `object` використовується **параметр типу** `T` — своєрідний «слот», який заповнюється конкретним типом при використанні класу:

```csharp run
using System;

MedicalRecord<int>    r1 = new MedicalRecord<int>(1001, "Гіпертонія");
MedicalRecord<string> r2 = new MedicalRecord<string>("P-001", "Бронхіт");

int    id1 = r1.Id; // без розпакування
string id2 = r2.Id; // без приведення типів

Console.WriteLine($"Картка #{id1.ToString()}: {r1.Description}");
Console.WriteLine($"Картка {id2}: {r2.Description}");

// MedicalRecord<int> r3 = new MedicalRecord<int>("abc", "..."); // помилка компіляції!

class MedicalRecord<T>
{
    public T Id { get; }
    public string Description { get; }

    public MedicalRecord(T id, string description)
    {
        Id = id;
        Description = description;
    }

    public override string ToString() => $"[{Id}] {Description}";
}
```

![Узагальнений клас: один шаблон — різні типи](_assets/04-08/generics-overview.png)

Кутові дужки `<T>` в оголошенні `class MedicalRecord<T>` вказують, що клас є узагальненим. Буква `T` — умовна назва параметра типу; замість неї може бути будь-який ідентифікатор. При створенні об'єкта конкретний тип вказується у кутових дужках: `new MedicalRecord<int>(...)`. Компілятор замінює `T` на `int` і перевіряє всі операції з `Id` відповідно до цього типу — помилки типів виловлюються на етапі компіляції, а не виконання.

## Конвенції іменування параметрів типу

У C# прийнято такі угоди щодо назв параметрів типу:

- `T` — загальний параметр типу (скорочення від *Type*)
- `TKey`, `TValue` — для пар ключ/значення (як у `Dictionary<TKey, TValue>`)
- `TResult` — для типу результату (як у `Func<T, TResult>`)
- `TEntity`, `TModel` — описові назви для конкретного контексту

## Кілька параметрів типу

Клас може мати кілька параметрів типу одночасно. Наприклад, клас призначення `Assignment` пов'язує пацієнта та лікаря, причому обидва можуть мати свої типи ідентифікаторів:

```csharp run
using System;

Assignment<int, string> a1 = new Assignment<int, string>(
    1001, "P-001", "Первинний огляд");

Console.WriteLine(a1.ToString());

class Assignment<TPatientId, TDoctorId>
{
    public TPatientId PatientId { get; }
    public TDoctorId  DoctorId  { get; }
    public string     Purpose   { get; }

    public Assignment(TPatientId patientId, TDoctorId doctorId, string purpose)
    {
        PatientId = patientId;
        DoctorId  = doctorId;
        Purpose   = purpose;
    }

    public override string ToString() =>
        $"Призначення: пацієнт #{PatientId} → лікар {DoctorId} | {Purpose}";
}
```

Кожен параметр типу замінюється незалежно: `TPatientId` → `int`, `TDoctorId` → `string`.

## Статичні поля узагальнених класів

Важливий нюанс: при типізації узагальненого класу різними типами для кожної комбінації типів створюється **окремий набір статичних членів**. Тобто `MedicalRecord<int>` і `MedicalRecord<string>` — це фактично два різних класи з власними статичними полями:

```csharp run
using System;

MedicalRecord<int>.Prefix    = "INT";
MedicalRecord<string>.Prefix = "STR";

Console.WriteLine(MedicalRecord<int>.Prefix);    // INT
Console.WriteLine(MedicalRecord<string>.Prefix); // STR — незалежне поле

class MedicalRecord<T>
{
    public static string Prefix = "DEFAULT";
    public T Id { get; }
    public MedicalRecord(T id) { Id = id; }
}
```

## Узагальнений клас як тип поля

Параметр типу може сам бути узагальненим класом. Наприклад, клас `Clinic` зберігає головного лікаря як `MedicalRecord<T>`:

```csharp run
using System;

MedicalRecord<int> chiefRecord = new MedicalRecord<int>(42, "Головний лікар");
Clinic<MedicalRecord<int>> clinic = new Clinic<MedicalRecord<int>>("Клініка №1", chiefRecord);

Console.WriteLine(clinic.ToString());

class MedicalRecord<T>
{
    public T Id { get; }
    public string Description { get; }
    public MedicalRecord(T id, string desc) { Id = id; Description = desc; }
    public override string ToString() => $"[{Id}] {Description}";
}

class Clinic<TChief>
{
    public string Name  { get; }
    public TChief Chief { get; }
    public Clinic(string name, TChief chief) { Name = name; Chief = chief; }
    public override string ToString() => $"{Name}, керівник: {Chief}";
}
```

## Узагальнені методи

Generics застосовуються не лише до класів, але й до окремих методів. Узагальнений метод оголошує власний параметр типу і може бути визначений у будь-якому класі — в тому числі у звичайному (не generic):

```csharp run
using System;

int a = 10, b = 20;
Swap<int>(ref a, ref b);
Console.WriteLine($"a={a.ToString()} b={b.ToString()}"); // a=20 b=10

string s1 = "Кардіологія", s2 = "Неврологія";
Swap(ref s1, ref s2); // тип виводиться автоматично
Console.WriteLine($"s1={s1} s2={s2}");

MedicalRecord<int> r1 = new MedicalRecord<int>(1, "Гіпертонія");
MedicalRecord<int> r2 = new MedicalRecord<int>(2, "Бронхіт");
Swap(ref r1, ref r2);
Console.WriteLine($"r1={r1} r2={r2}");

void Swap<T>(ref T x, ref T y)
{
    T temp = x;
    x = y;
    y = temp;
}

class MedicalRecord<T>
{
    public T Id { get; }
    public string Description { get; }
    public MedicalRecord(T id, string desc) { Id = id; Description = desc; }
    public override string ToString() => $"[{Id}] {Description}";
}
```

Зверніть увагу на виклик `Swap(ref s1, ref s2)` без явного вказання типу — компілятор сам визначає `T = string` з типів переданих аргументів. Це називається **виведення типу** (type inference) і робить код лаконічнішим.

## Generics у стандартній бібліотеці

Generics є основою колекцій .NET. Завдяки ним колекції зберігають елементи без boxing і з повною типобезпекою:

```csharp run
using System;
using System.Collections.Generic;

List<string> diagnoses = new List<string>();
diagnoses.Add("Гіпертонія");
diagnoses.Add("Бронхіт");
diagnoses.Add("Діабет");

foreach (string d in diagnoses)
    Console.WriteLine(d);

Dictionary<int, string> patients = new Dictionary<int, string>();
patients[1001] = "Іван Петренко";
patients[1002] = "Марія Сидоренко";

Console.WriteLine(patients[1001]);
Console.WriteLine(patients[1002]);
```

`List<string>` зберігає рядки безпосередньо, без упаковки в `object` — на відміну від старого `ArrayList`. `Dictionary<int, string>` типізує і ключ, і значення, тому жодних явних приведень не потрібно. Детально колекції розглядаються у наступних розділах курсу.
