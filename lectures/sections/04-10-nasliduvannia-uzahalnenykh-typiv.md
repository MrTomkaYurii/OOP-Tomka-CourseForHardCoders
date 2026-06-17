---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 10
number: "4.10"
title: "Наслідування узагальнених типів"
source: "../_combined/27-nasliduvannia-uzahalnenykh-typiv.md"
---

## 4.10. Наслідування узагальнених типів

Узагальнені класи можуть успадковуватися один від одного — так само як і звичайні. При цьому є чотири принципово різних варіанти того, як похідний клас взаємодіє з параметром типу базового. Вибір між ними визначається тим, наскільки гнучким або конкретним має бути похідний клас.

Як базовий клас для всіх прикладів використаємо `MedicalRecord<T>`:

```csharp
abstract class MedicalRecord<T>
{
    public T Id { get; }
    public string Description { get; set; }

    public MedicalRecord(T id, string description)
    {
        Id          = id;
        Description = description;
    }

    public override string ToString() => $"[{Id}] {Description}";
}
```

![4 варіанти успадкування узагальнених класів](_assets/04-10/generic-inheritance-variants.png)

## Варіант 1: передача параметра далі — Child<T> : Base<T>

Похідний клас залишається узагальненим і передає свій параметр `T` у базовий клас. Це найбільш гнучкий варіант — конкретний тип визначається лише при створенні екземпляра:

```csharp run
using System;

FlexibleRecord<int>    r1 = new FlexibleRecord<int>(1001, "Гіпертонія", "Стаціонар");
FlexibleRecord<string> r2 = new FlexibleRecord<string>("P-002", "Бронхіт", "Амбулаторія");

Console.WriteLine(r1.ToString());
Console.WriteLine(r2.ToString());

abstract class MedicalRecord<T>
{
    public T Id { get; }
    public string Description { get; }
    public MedicalRecord(T id, string desc) { Id = id; Description = desc; }
    public override string ToString() => $"[{Id}] {Description}";
}

class FlexibleRecord<T> : MedicalRecord<T>   // T передається далі
{
    public string Ward { get; }

    public FlexibleRecord(T id, string desc, string ward) : base(id, desc)
    {
        Ward = ward;
    }

    public override string ToString() => $"{base.ToString()} | {Ward}";
}
```

`FlexibleRecord<int>` і `FlexibleRecord<string>` — це два різних класи, кожен зі своїм типом `Id`. Похідний клас просто «пробрасує» параметр у базовий.

## Варіант 2: фіксація типу — Child : Base<string>

Похідний клас є звичайним (неузагальненим) і фіксує конкретний тип для базового. Це доречно, коли для конкретної предметної ситуації тип ідентифікатора відомий заздалегідь:

```csharp run
using System;

InpatientRecord r1 = new InpatientRecord("IP-001", "Планова операція", 12);
InpatientRecord r2 = new InpatientRecord("IP-002", "Спостереження", 7);

Console.WriteLine(r1.ToString());
Console.WriteLine(r2.ToString());

// r1 — це також MedicalRecord<string>:
MedicalRecord<string> rec = r1;
Console.WriteLine(rec.Id);

abstract class MedicalRecord<T>
{
    public T Id { get; }
    public string Description { get; }
    public MedicalRecord(T id, string desc) { Id = id; Description = desc; }
    public override string ToString() => $"[{Id}] {Description}";
}

class InpatientRecord : MedicalRecord<string>   // T зафіксований як string
{
    public int RoomNumber { get; }

    public InpatientRecord(string id, string desc, int room) : base(id, desc)
    {
        RoomNumber = room;
    }

    public override string ToString() => $"{base.ToString()} | Палата {RoomNumber.ToString()}";
}
```

`InpatientRecord` — звичайний клас без власних параметрів типу. Він завжди має `Id` типу `string`, і його можна зберігати у змінній `MedicalRecord<string>`.

## Варіант 3: власний параметр при фіксованому базовому — Child<T> : Base<int>

Похідний клас є узагальненим з власним параметром `T`, але у базового клас тип зафіксований. Це дозволяє додавати нові generic-поля незалежно від базового:

```csharp run
using System;

TaggedRecord<string> r1 = new TaggedRecord<string>(1001, "Гіпертонія", "кардіологія");
TaggedRecord<string[]> r2 = new TaggedRecord<string[]>(1002, "Діабет",
    new[] { "ендокринологія", "дієтологія" });

Console.WriteLine(r1.ToString());
Console.WriteLine($"[{r2.Id}] {r2.Description} | Теги: {string.Join(", ", r2.Tag)}");

abstract class MedicalRecord<T>
{
    public T Id { get; }
    public string Description { get; }
    public MedicalRecord(T id, string desc) { Id = id; Description = desc; }
    public override string ToString() => $"[{Id}] {Description}";
}

class TaggedRecord<T> : MedicalRecord<int>  // int фіксовано у базовому, T — своє
{
    public T Tag { get; }

    public TaggedRecord(int id, string desc, T tag) : base(id, desc)
    {
        Tag = tag;
    }

    public override string ToString() => $"{base.ToString()} | Тег: {Tag}";
}
```

`TaggedRecord<T>` успадковує `MedicalRecord<int>` — тому `Id` завжди `int`. Але сам клас залишається параметричним за `T`, що використовується для поля `Tag`.

## Варіант 4: розширення базового параметра — Child<T, TExtra> : Base<T>

Похідний клас передає базовому параметр `T` і одночасно додає власний новий параметр. Це найбільш потужний варіант для побудови складних ієрархій:

```csharp run
using System;

AnnotatedRecord<int, string> r1 =
    new AnnotatedRecord<int, string>(1001, "Гіпертонія", "Лікар: Коваль О.В.");

AnnotatedRecord<string, int> r2 =
    new AnnotatedRecord<string, int>("P-002", "Бронхіт", 3);

Console.WriteLine(r1.ToString());
Console.WriteLine(r2.ToString());

abstract class MedicalRecord<T>
{
    public T Id { get; }
    public string Description { get; }
    public MedicalRecord(T id, string desc) { Id = id; Description = desc; }
    public override string ToString() => $"[{Id}] {Description}";
}

class AnnotatedRecord<T, TNote> : MedicalRecord<T>  // T передається, TNote — нове
{
    public TNote Note { get; }

    public AnnotatedRecord(T id, string desc, TNote note) : base(id, desc)
    {
        Note = note;
    }

    public override string ToString() => $"{base.ToString()} | Примітка: {Note}";
}
```

`AnnotatedRecord<T, TNote>` повністю гнучкий: `T` визначає тип Id (як у базовому), а `TNote` — тип додаткової анотації. Обидва параметри незалежні.

## Успадкування обмежень

Якщо базовий клас встановлює обмеження на параметр типу, похідний клас зобов'язаний підтримати або посилити це обмеження для того самого параметра:

```csharp run
using System;

FlexibleRecord<Patient> r = new FlexibleRecord<Patient>(
    new Patient("Іван Петренко"), "Огляд", "Терапія");
Console.WriteLine(r.ToString());

// FlexibleRecord<int> wrong = new(...);  // помилка: int — не клас

abstract class MedicalRecord<T> where T : class   // обмеження на рівні базового
{
    public T Id { get; }
    public string Description { get; }
    public MedicalRecord(T id, string desc) { Id = id; Description = desc; }
    public override string ToString() => $"[{Id}] {Description}";
}

class FlexibleRecord<T> : MedicalRecord<T> where T : class  // обмеження повторюється
{
    public string Ward { get; }
    public FlexibleRecord(T id, string desc, string ward) : base(id, desc)
    { Ward = ward; }
    public override string ToString() => $"{base.ToString()} | {Ward}";
}

class Patient
{
    public string Name { get; }
    public Patient(string name) { Name = name; }
    public override string ToString() => $"Пацієнт: {Name}";
}
```

Правило просте: якщо базовий клас має `where T : class`, то і похідний повинен вказати `where T : class` або конкретніше обмеження (наприклад, `where T : Patient`). Це гарантує, що компілятор зможе перевіряти обмеження на всіх рівнях ієрархії.

## Підсумок: коли що використовувати

| Варіант | Синтаксис | Коли застосовувати |
|---------|-----------|-------------------|
| Передача T | `Child<T> : Base<T>` | Похідний залишається гнучким |
| Фіксація типу | `Child : Base<string>` | Тип відомий — клас стає конкретним |
| Свій T, фіксований базовий | `Child<T> : Base<int>` | Додаємо гнучкість у нових полях |
| Розширення параметрів | `Child<T, K> : Base<T>` | Максимальна гнучкість |
