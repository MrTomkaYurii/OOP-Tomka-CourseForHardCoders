---
chapter: 9
chapterTitle: "Розділ 9. Pattern matching"
section: 1
number: "9.1"
title: "Патерн типів"
source: "../_combined/56-patern-typiv.md"
---

## 9.1. Патерн типів

## Що таке pattern matching

**Pattern matching** (зіставлення із зразком) — це механізм, який дозволяє перевірити значення на відповідність певному **зразку** (pattern) і, якщо перевірка успішна, виконати відповідну дію або отримати результат. Зразок може описувати тип, конкретне значення, структуру об'єкта, діапазон, логічну комбінацію умов тощо.

До появи pattern matching у C# 7 (і його розширень у 8, 9, 10, 11) програмісти виконували перевірки вручну через ланцюги `if-else`, оператори `as` і явні приведення типів. Ця система працювала, але була багатослівною, схильною до помилок і погано читалась. Pattern matching замінює її компактним, виразним і типобезпечним синтаксисом.

У розділі 9 ми розглянемо всі ключові типи зразків: типів, властивостей, кортежів, позиційних, реляційних, логічних і списків.

## Патерн типів (type pattern)

Найпростіший і найбільш використовуваний різновид — **патерн типів**. Він перевіряє, чи є значення екземпляром певного типу, і якщо так — одразу прив'язує його до нової змінної потрібного типу:

```text
значення  is  Тип  змінна
```

Три дії в одному виразі: перевірка, приведення і прив'язка. Якщо перевірка не проходить — змінна не створюється, виконання йде в гілку `else`.

## Стара форма vs pattern matching

До C# 7 перевірка типу з подальшим cast виглядала так:

```csharp
// Стара форма — два кроки, дублювання
if (staff is Doctor)
{
    Doctor doc = (Doctor)staff; // cast треба повторити явно
    doc.PrescribeMeds();
}

// Або через as + null-check
Doctor? doc = staff as Doctor;
if (doc != null)
    doc.PrescribeMeds();
```

З патерном типів:

```csharp
// Нова форма — одна операція
if (staff is Doctor doc)
{
    doc.PrescribeMeds(); // doc вже типу Doctor, не потрібен додатковий cast
}
```

![Патерн типів: стара форма vs pattern matching](_assets/09-01/type-pattern-old-vs-new.png)

Компілятор гарантує: якщо умова `is Doctor doc` виконалась, то `doc` не є `null` і гарантовано має тип `Doctor`. Ні зайвого cast-у, ні зайвої null-перевірки.

## Клінічний приклад: ієрархія медичного персоналу

Визначимо клінічну ієрархію і застосуємо патерн типів:

```csharp run
using System;

// Виконуваний код
MedicalStaff[] staff =
{
    new Doctor("Олег Петренко", "Кардіологія"),
    new Nurse("Марія Іванова", "Кардіологія"),
    new Doctor("Тетяна Мельник", "Неврологія"),
    new MedicalStaff("Адмін Сидоренко"),
};

foreach (var person in staff)
    ProcessStaff(person);

void ProcessStaff(MedicalStaff s)
{
    if (s is Doctor doc)
    {
        Console.WriteLine($"Лікар {doc.Name} ({doc.Specialty}) — може виписувати рецепти");
    }
    else if (s is Nurse nurse)
    {
        Console.WriteLine($"Медсестра {nurse.Name} — виконує призначення лікаря");
    }
    else
    {
        Console.WriteLine($"Персонал {s.Name} — адміністративна роль");
    }
}

// Ієрархія
class MedicalStaff
{
    public string Name { get; }
    public MedicalStaff(string name) => Name = name;
}
class Doctor : MedicalStaff
{
    public string Specialty { get; }
    public Doctor(string name, string specialty) : base(name) => Specialty = specialty;
}
class Nurse : MedicalStaff
{
    public string Ward { get; }
    public Nurse(string name, string ward) : base(name) => Ward = ward;
}
```

Змінні `doc` та `nurse` існують лише у відповідних блоках `if` — за межами блоку вони недоступні. Це scope binding: патерн не просто перевіряє тип, а прив'язує результат перевірки до іменованої змінної у вужчій області видимості.

## Патерн типів у switch

Патерни зручно застосовувати в конструкції `switch`. Починаючи з C# 8 є дві форми:

**switch statement** (традиційний) — більш детальний, дозволяє `break`/`return` в кожному case:

```csharp
switch (staff)
{
    case Doctor doc when !doc.IsOnLeave:
        doc.PrescribeMeds();
        break;
    case Nurse nurse:
        nurse.ExecuteOrders();
        break;
    case null:
        Console.WriteLine("Об'єкт null");
        break;
    default:
        Console.WriteLine("Невідома роль");
        break;
}
```

**switch expression** (C# 8+) — компактний, повертає значення:

```csharp
string role = staff switch
{
    Doctor doc   => $"Лікар: {doc.Specialty}",
    Nurse  nurse => $"Медсестра: {nurse.Ward}",
    null         => "null",
    _            => "Інший персонал"
};
```

Switch expression — це **вираз**, він повертає значення і може стояти в правій частині присвоєння. Switch statement — це **оператор**, він виконує дії. При pattern matching switch expression зазвичай компактніший і виразніший.

## Додаткові умови: when

У `switch statement` до кожного `case` можна додати умову через `when`:

```csharp run
using System;

// Виконуваний код
MedicalStaff[] staff =
{
    new Doctor("Олег Петренко",  isOnLeave: false),
    new Doctor("Тетяна Мельник", isOnLeave: true),
    new Nurse("Марія Іванова"),
};

foreach (var person in staff)
{
    string status = GetStatus(person);
    Console.WriteLine($"{person.Name}: {status}");
}

string GetStatus(MedicalStaff s) => s switch
{
    Doctor { IsOnLeave: false } doc => $"Лікар на зміні ({doc.Name})",
    Doctor { IsOnLeave: true }      => "Лікар у відпустці",
    Nurse nurse                     => $"Медсестра: {nurse.Name}",
    null                            => "порожньо",
    _                               => "інший персонал"
};

// Ієрархія
class MedicalStaff
{
    public string Name { get; }
    public MedicalStaff(string name) => Name = name;
}
class Doctor : MedicalStaff
{
    public bool IsOnLeave { get; }
    public Doctor(string name, bool isOnLeave) : base(name) => IsOnLeave = isOnLeave;
}
class Nurse : MedicalStaff
{
    public Nurse(string name) : base(name) { }
}
```

## Constant pattern і null-перевірка

Патерн може порівнювати значення з **константою**, включаючи `null`:

```csharp
// Перевірка конкретного рядка
if (diagnosis is "Гіпертонія II ст.")
    Console.WriteLine("Стандартний протокол лікування");

// null-перевірка через патерн
if (patient is not null)
    patient.PrintInfo();

// Або
if (patient is null)
    throw new ArgumentNullException(nameof(patient));
```

`is not null` — це не просто синтаксичний цукор. Компілятор трактує це як **null-check pattern** і може виконати його ефективніше, ніж `!= null` у деяких контекстах. Крім того, такий запис виразно показує намір: «переконатись, що об'єкт існує».

## Порядок case у switch: важливо

Switch обробляє варіанти **зверху вниз** і зупиняється на першому збігу. Якщо базовий тип іде першим — до похідних ніколи не дійде:

```csharp
// НЕПРАВИЛЬНО — Doctor ніколи не буде спіймано:
switch (staff)
{
    case MedicalStaff s:  // спрацює першим для будь-якого типу!
        // ...
    case Doctor doc:      // недосяжний код
        // ...
}

// ПРАВИЛЬНО — конкретніші типи першими:
switch (staff)
{
    case Doctor doc:      // спочатку — конкретний
    case Nurse nurse:
    case MedicalStaff s:  // потім — загальний
}
```

Компілятор попереджає про недосяжні case, але відповідальність за правильний порядок — на програмісті.

## Антипатерн: ланцюг if-else з is та явним cast

До появи pattern matching стандартним способом перевірки типу була комбінація `is` для перевірки і явного cast `(Тип)значення` для доступу до членів. Цей підхід досі зустрічається у старому коді та є антипатерном у сучасному C#:

```csharp
// АНТИПАТЕРН — стара форма: тип перевіряється двічі, потім cast вручну
void ProcessStaff(MedicalStaff s)
{
    if (s is Doctor)
    {
        Doctor doc = (Doctor)s;              // тип дублюється: is Doctor і (Doctor)
        Console.WriteLine(doc.Specialty);
    }
    else if (s is Nurse)
    {
        Nurse nurse = (Nurse)s;
        Console.WriteLine(nurse.Ward);
    }
    else if (s is Administrator)
    {
        Administrator admin = (Administrator)s;
        Console.WriteLine(admin.Department);
    }
}
```

Цей стиль має три проблеми. По-перше, **дублювання типу**: перевірка `is Doctor` і наступний `(Doctor)s` — це дві операції над одним і тим самим фактом. По-друге, **крихкість при рефакторингу**: якщо хтось змінить перевірку `is Doctor` на `is Surgeon`, але забуде оновити cast — отримає `InvalidCastException` у runtime. По-третє, **відсутність вичерпності**: якщо до ієрархії додати новий тип `Paramedic`, компілятор не попередить, що він не оброблений у жодній гілці — виконання мовчки пройде мимо.

Стара форма через `as + null-check` трохи краща (немає подвійного cast), але все одно потребує двох кроків і не дає binding у вужчій області видимості:

```csharp
// as + null-check: один cast, але binding поза блоком if
Doctor? doc = s as Doctor;
if (doc != null)
    Console.WriteLine(doc.Specialty);

// doc досі видимий тут — хоч може бути null
```

**Правильний підхід** — switch expression із type pattern. Одна операція перевіряє тип і прив'язує змінну; вираз повертає значення; exhaustiveness перевіряється компілятором через `_`:

```csharp run
using System;

MedicalStaff[] staff =
{
    new Doctor("Петренко О.", "Кардіологія"),
    new Doctor("Мельник Т.", "Неврологія") { IsOnLeave = true },
    new Nurse("Іванова М.", "Кардіологія"),
    new Administrator("Бойко Р.", "Реєстратура"),
};

foreach (var person in staff)
    Console.WriteLine(Describe(person));

// switch expression: тип + властивість в одному місці, повертає рядок
string Describe(MedicalStaff s) => s switch
{
    Doctor { IsOnLeave: true } doc
        => $"Лікар {doc.Name} ({doc.Specialty}) — у відпустці",
    Doctor doc
        => $"Лікар {doc.Name} ({doc.Specialty}) — на зміні",
    Nurse nurse
        => $"Медсестра {nurse.Name}, відділення {nurse.Ward}",
    Administrator admin
        => $"Адміністратор {admin.Name}, {admin.Department}",
    null
        => "(порожнє посилання)",
    _
        => $"Невідома роль: {s.GetType().Name}"
};

class MedicalStaff
{
    public string Name { get; }
    public MedicalStaff(string name) => Name = name;
}
class Doctor : MedicalStaff
{
    public string Specialty { get; }
    public bool IsOnLeave { get; init; }
    public Doctor(string name, string specialty) : base(name) => Specialty = specialty;
}
class Nurse : MedicalStaff
{
    public string Ward { get; }
    public Nurse(string name, string ward) : base(name) => Ward = ward;
}
class Administrator : MedicalStaff
{
    public string Department { get; }
    public Administrator(string name, string dept) : base(name) => Department = dept;
}
```

Switch expression перевіряє тип і прив'язує змінну **в одній операції** (`Doctor doc`) — жодного зайвого cast, жодного дублювання. Вбудований property pattern (`{ IsOnLeave: true }`) дозволяє уточнити умову без окремого `if`. Гілка `_` — запасний варіант для нових типів: IDE одразу підказує додати `case Paramedic`, щойно такий клас з'явиться у ієрархії.

| | Старий if-else + cast | Switch expression |
|---|---|---|
| Кількість операцій для перевірки типу | 2 (`is` + явний cast) | 1 (type pattern) |
| Ризик `InvalidCastException` | Є при неузгодженому рефакторингу | Відсутній |
| Прив'язка змінної | Окрема оголошення після блоку `if` | Вбудована (`Doctor doc`) |
| Перевірка властивостей | Окремий вкладений `if` | Вбудований property pattern |
| Повертає значення | Ні — лише виконує дії | Так — вираз, можна присвоїти |
| Контроль нових типів | Мовчазний пропуск | IDE пропонує додати case |
