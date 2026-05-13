---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 10
number: "4.10"
title: "Наслідування узагальнених типів"
source: "../_combined/27-nasliduvannia-uzahalnenykh-typiv.md"
---

## 4.10. Наслідування узагальнених типів

Один узагальнений клас може бути успадкований від іншого узагальненого. При цьому можна використовувати різні варіанти спадкування.

Допустимо, у нас є наступний базовий клас `Person`:

```csharp
class Person<T>
{
    public T Id { get; }

    public Person(T id)
    {
        Id = id;
    }
}
```

Перший варіант полягає у створенні класу-спадкоємця, який типізований тим же типом, що і базовий:

```csharp
class UniversalPerson<T> : Person<T>
{
    public UniversalPerson(T id) : base(id) { }
}
```

Застосування класу:

```csharp
Person<string> person1 = new Person<string>("34");
Person<int> person3 = new UniversalPerson<int>(45);
UniversalPerson<int> person2 = new UniversalPerson<int>(33);
Console.WriteLine(person1.Id);
Console.WriteLine(person2.Id);
Console.WriteLine(person3.Id);
```

Другий варіант є створення звичайного неузагальненого класу-спадкоємця. У цьому випадку при успадкуванні у базового класу треба явно визначити тип, що використовується:

```csharp
class StringPerson : Person<string>
{
    public StringPerson(string id) : base(id) { }
}
```

Тепер у похідному класі як тип використовуватиметься тип `string`. Застосування класу:

```csharp
StringPerson person4 = new StringPerson("438767");
Person<string> person5 = new StringPerson("43875");

// Так не можна написати
// Person<int> person6 = new StringPerson("45545");

Console.WriteLine(person4.Id);
Console.WriteLine(person5.Id);
```

Третій варіант представляє типізацію похідного класу параметром зовсім іншого типу, відмінного від універсального параметра в базовому класі. У цьому випадку для базового класу також треба вказати тип, що використовується:

```csharp
class IntPerson<T> : Person<int>
{
    public T Code { get; set; }

    public IntPerson(int id, T code) : base(id)
    {
        Code = code;
    }
}
```

Тут тип `IntPerson` типізовано ще одним типом, який може не збігатися з типом, який використовується базовим класом. Застосування класу:

```csharp
IntPerson<string> person7 = new IntPerson<string>(5, "r4556");
Person<int> person8 = new IntPerson<long>(7, 4587);
Console.WriteLine(person7.Id);
Console.WriteLine(person8.Id);
```

І також у класах-спадкоємцях можна поєднувати використання універсального параметра з базового класу із застосуванням своїх параметрів:

```csharp
class MixedPerson<T, K> : Person<T>
where K : struct
{
    public K Code { get; set; }

    public MixedPerson(T id, K code) : base(id)
    {
        Code = code;
    }
}
```

Тут на додаток до успадкованого від базового класу параметра `T` додається новий параметр `K`. Також якщо необхідно встановити обмеження, ми їх можемо вказати після назви базового класу. Застосування класу:

```csharp
MixedPerson<string, int> person9 = new MixedPerson<string, int>("456", 356);
Person<string> person10 = new MixedPerson<string, int>("9867", 35678);
Console.WriteLine(person9.Id);
Console.WriteLine(person10.Id);
```

При цьому варто враховувати, що якщо на рівні базового класу для універсального параметра встановлено обмеження, то подібне обмеження має бути визначене і у похідних класах, які також використовують цей параметр:

```csharp
class Person<T> where T : class
{
    public T Id { get; }
    public Person(T id) => Id = id;
}

class UniversalPerson<T> : Person<T> where T : class
{
    public UniversalPerson(T id) : base(id) { }
}
```

Тобто якщо в базовому класі як обмеження зазначено `class`, тобто будь-який клас, то у похідному класі також треба вказати як обмеження `class`, або ж якийсь конкретний клас.
