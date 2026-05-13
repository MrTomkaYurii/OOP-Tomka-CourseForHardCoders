---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 7
number: "4.7"
title: "Клас System.Object та його методи"
source: "../_combined/24-system-object-ta-ioho-metody.md"
---

## 4.7. Клас System.Object та його методи

Всі класи в .NET, навіть ті, які ми самі створюємо, а також базові типи, такі як `System.Int32`, є похідними від класу `Object`. Навіть якщо ми не вказуємо клас `Object` як базовий, за умовчанням неявно клас `Object` все одно стоїть на вершині ієрархії спадкування. Тому всі типи та класи можуть реалізувати ті методи, які визначені у класі `System.Object`. Розглянемо ці методи.

## ToString

Метод `ToString` служить для отримання строкового представлення даного об'єкта. Для базових типів просто виводитиметься їх рядкове значення:

```csharp
int i = 5;
Console.WriteLine(i.ToString()); // виведе число 5

double d = 3.5;
Console.WriteLine(d.ToString()); // виведе число 3,5
```

Для класів цей метод виводить повну назву класу із зазначенням простору імен, у якому визначено цей клас. І ми можемо перевизначити цей метод. Подивимося на прикладі:

```csharp
Person person = new Person { Name = "Tom" };
Console.WriteLine(person.ToString()); // виведе назву класу Person

Clock clock = new Clock { Hours = 15, Minutes = 34, Seconds = 53 };
Console.WriteLine(clock.ToString()); // виведе 15:34:53

class Clock
{
    public int Hours { get; set; }
    public int Minutes { get; set; }
    public int Seconds { get; set; }

    public override string ToString()
    {
        return $"{Hours}:{Minutes}:{Seconds}";
    }
}

class Person
{
    public string Name { get; set; } = "";
}
```

Для перевизначення методу `ToString()` в класі `Clock`, який представляє годинник, використовується ключове слово `override` (як і за звичайного перевизначення віртуальних або абстрактних методів). У разі метод `ToString()` виводить у рядку значення властивостей `Hours`, `Minutes`, `Seconds`.

Клас `Person` не перевизначає метод `ToString`, тому для цього класу спрацьовує стандартна реалізація цього методу, яка виводить просто назву класу.

До речі, у цьому випадку ми могли задіяти обидві реалізації:

```csharp
Person tom = new Person { Name = "Tom" };
Console.WriteLine(tom.ToString()); // Tom

Person undefined = new Person();
Console.WriteLine(undefined.ToString()); // Person

class Person
{
    public string Name { get; set; } = "";

    public override string? ToString()
    {
        if (string.IsNullOrEmpty(Name))
        return base.ToString();

        return Name;
    }
}
```

Тобто якщо ім'я - властивість `Name` не має значення, воно є порожнім рядком, то повертається базова реалізація - назва класу. Варто зазначити, що базова реалізація повертає не просто рядок, а об'єкт `string?` - тобто це може бути рядок `string` або значення `null`, яке вказує на відсутність значення. І насправді як тип, що повертається для методу, ми можемо використовувати як `string`, так і `string?`.

Якщо ім'я об'єкта `Person` встановлено, то повертається значення властивості `Name`. Для перевірки рядка на наявність значення застосовується метод `String.IsNullOrEmpty()`.

Варто зазначити, що різні технології на платформі .NET активно використовують метод `ToString` для різних цілей. Зокрема, той самий метод `Console.WriteLine()` за умовчанням виводить саме рядкове уявлення об'єкта. Тому, якщо нам треба вивести рядкове подання об'єкта на консоль, то при передачі об'єкта методу `Console.WriteLine` необов'язково використовувати метод `ToString()` - він викликається неявно:

```csharp
Person person = new Person { Name = "Tom" };
Console.WriteLine(person); // Tom

Clock clock = new Clock { Hours = 15, Minutes = 34, Seconds = 53 };
Console.WriteLine(clock); // виведе 15:34:53
```

## Метод GetHashCode

Метод `GetHashCode` дозволяє повернути деяке числове значення, яке буде відповідати даному об'єкту або його хеш-коду. За цим числом, наприклад, можна порівнювати об'єкти. Можна визначати різні алгоритми генерації подібного числа або взяти реалізацію базового типу:

```csharp
class Person
{
    public string Name { get; set; } = "";

    public override int GetHashCode()
    {
        return Name.GetHashCode();
    }
}
```

В даному випадку метод `GetHashCode` повертає хеш-код значення властивості `Name`. Тобто два об'єкти `Person`, які мають те саме ім'я, повертатимуть один і той же хеш-код. Проте насправді алгоритм може бути різним.

## Отримання типу об'єкта та метод GetType

Метод `GetType` дозволяє отримати тип об'єкта:

```csharp
Person person = new Person { Name = "Tom" };
Console.WriteLine(person.GetType());    // Person
```

Цей метод повертає об'єкт `Type`, тобто тип об'єкта.

За допомогою ключового слова `typeof` ми отримуємо тип класу і порівнюємо його з типом об'єкта. І якщо цей об'єкт є типом `Person`, то виконуємо певні дії.

```csharp
object person = new Person { Name = "Tom" };

if (person.GetType() == typeof(Person))
Console.WriteLine("Це реально клас Person");
```

Причому оскільки клас `Object` є базовим типом всім класів, ми можемо змінній типу `object` присвоїти об'єкт будь-якого типу. Однак для цієї змінної метод `GetType` все одно поверне той тип, на який посилається змінна. Тобто в цьому випадку об'єкт типу `Person`.

Варто зазначити, що перевірку типу можна скоротити за допомогою оператора `is`:

```csharp
object person = new Person { Name = "Tom" };

if (person is Person)
Console.WriteLine("Це реально клас Person");
```

На відміну від методів `ToString`, `Equals`, `GetHashCode`, метод `GetType()` не перевизначається.

## Метод Equals

Метод `Equals` дозволяє порівняти два об'єкти на рівність. Як параметр він приймає об'єкт для порівняння у вигляді типу `object` і повертає `true`, якщо обидва об'єкти рівні:

```csharp
public override bool Equals(object? obj) { ...... }
```

Наприклад, реалізуємо цей метод у класі `Person`:

```csharp
class Person
{
    public string Name { get; set; } = "";

    public override bool Equals(object? obj)
    {
        // якщо параметр методу представляє тип Person
        // то повертаємо true, якщо імена збігаються
        if (obj is Person person) return Name == person.Name;

        return false;
    }

    // разом із методом Equals слід реалізувати метод GetHashCode
    public override int GetHashCode() => Name.GetHashCode();
}
```

Метод `Equals` приймає як параметр об'єкт будь-якого типу, який потім приводиться до поточного класу - класу `Person`.

Якщо переданий об'єкт є типом `Person`, то повертаємо результат порівняння імен двох об'єктів `Person`. Якщо об'єкт представляє інший тип, то повертається `false`.

В даному випадку для прикладу застосовується досить простий алгоритм порівняння, проте при необхідності реалізацію методу можна зробити складнішою, наприклад, порівнювати за декількома властивостями за їх наявності.

Слід зазначити, що з методом `Equals` слід реалізувати метод `GetHashCode`.

Застосування методу:

```csharp
var person1 = new Person { Name = "Tom" };
var person2 = new Person { Name = "Bob" };
var person3 = new Person { Name = "Tom" };

bool person1EqualsPerson2 = person1.Equals(person2);   // false
bool person1EqualsPerson3 = person1.Equals(person3);   // true

Console.WriteLine(person1EqualsPerson2);   // false
Console.WriteLine(person1EqualsPerson3);   // true
```

І якщо слід порівнювати два складні об'єкти, як у цьому випадку, то краще використовувати метод `Equals`, а не стандартну операцію `==`.
