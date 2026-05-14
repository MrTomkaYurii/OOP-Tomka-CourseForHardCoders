---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
section: 6
number: "14.6"
title: "Атрибути у .NET"
source: "../_combined/89-atrybuty-u-dotnet.md"
---

## 14.6. Атрибути у .NET

Атрибути в .NET представляють спеціальні інструменти, які дозволяють вбудовувати до збірки додаткові метадані. Атрибути можуть застосовуватися як до всього типу (класу, інтерфейсу тощо), так і до окремих його частин (методу, властивості тощо). Основу атрибутів становить клас `System.Attribute`, від якого утворені й інші класи атрибутів. У .NET є багато вбудованих класів атрибутів. І також ми можемо створювати власні класи атрибутів, які будуть визначати метадані інших типів.

Допустимо, нам треба перевіряти користувача на відповідність деяким віковим обмеженням. Створимо свій атрибут, який зберігатиме граничне значення віку, з якого дозволені деякі дії:

```csharp
class AgeValidationAttribute : Attribute
{
    public int Age { get; }
    public AgeValidationAttribute() { }
    public AgeValidationAttribute(int age) => Age = age;
}
```

По суті, це звичайний клас, успадкований від `System.Attribute`. У ньому визначено два конструктори: з параметром та без. Як параметр другий конструктор атрибута приймає якийсь пороговий вік і зберігає його як властивість.

Тепер застосуємо його до деякого класу:

```csharp
[AgeValidation(18)]
public class Person
{
    public string Name { get; }
    public int Age { get; set; }
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
}
```

Цей клас `Person` застосовує атрибут. І тому ім'я атрибута вказується у квадратних дужках безпосередньо перед визначенням класу. Причому суфікс `Attribute` вказувати необов'язково. Обидва записи `[AgeValidation(18)]` та `[AgeValidationAttribute(18)]` будуть рівноправними.

Якщо конструктор атрибута передбачає використання параметрів (`public AgeValidationAttribute(int age)`), після імені атрибута ми можемо вказати значення для параметрів конструктора. У разі передається значення для параметра `age`. Тобто фактично ми говоримо, що в `AgeValidationAttribute` властивість `Age` матиме значення 18.

Як альтернативу можна використовувати іменовані параметри для всіх властивостей атрибуту, якщо клас атрибута має конструктор без параметрів:

```csharp
[AgeValidation(Age = 18)]
```

Тепер отримаємо атрибут класу `Person` та використовуємо його для перевірки об'єктів даного класу:

```csharp
Person tom = new Person("Tom", 35);
Person bob = new Person("Bob", 16);
bool tomIsValid = ValidateUser(tom); // true
bool bobIsValid = ValidateUser(bob); // false

Console.WriteLine($"Результат валідації Тома: {tomIsValid}");
Console.WriteLine($"Результат валідації Боба: {bobIsValid}");

bool ValidateUser(Person person)
{
    Type type = typeof(Person);
    // Отримуємо всі атрибути класу Person.
    object[] attributes = type.GetCustomAttributes(false);

    // Проходимо по всім атрибутам.
    foreach (Attribute attr in attributes)
    {
        // Якщо атрибут представляє тип AgeValidationAttribute.
        if (attr is AgeValidationAttribute ageAttribute)
            // Повертаємо результат перевірки за віком.
            return person.Age >= ageAttribute.Age;
    }
    return true;
}

class AgeValidationAttribute : Attribute
{
    public int Age { get; }
    public AgeValidationAttribute() { }
    public AgeValidationAttribute(int age) => Age = age;
}

[AgeValidation(18)]
public class Person
{
    public string Name { get; }
    public int Age { get; set; }
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
}
```

В даному випадку в методі `ValidateUser` через параметр отримуємо деякий об'єкт `Person` і за допомогою методу `GetCustomAttributes` витягуємо з типу `Person` усі атрибути. Далі беремо з атрибутів атрибут `AgeValidationAttribute` за його наявності (адже ми можемо його і не застосовувати до класу) та перевіримо допустимість віку користувача. Якщо користувач пройшов перевірку віком, то повертаємо `true`, інакше повертаємо `false`. Якщо атрибут не застосовується, то повертаємо `true`.

### Обмеження застосування атрибуту

За допомогою атрибуту `AttributeUsage` можна обмежити типи, до яких застосовуватиметься атрибут. Наприклад, ми хочемо, щоб вище визначений атрибут міг застосовуватися лише до класів:

```csharp
[AttributeUsage(AttributeTargets.Class)]
class AgeValidationAttribute : Attribute
{
    // ...
}
```

Обмеження задає перерахування `AttributeTargets`, яке може набувати ще ряду значень:

- `All`: використовується всіма типами
- `Assembly`: атрибут застосовується до збірки
- `Constructor`: атрибут застосовується до конструктора
- `Delegate`: атрибут застосовується до делегату
- `Enum`: застосовується до перерахування
- `Event`: атрибут застосовується до події
- `Field`: застосовується до поля типу
- `Interface`: атрибут застосовується до інтерфейсу
- `Method`: застосовується до методу
- `Property`: застосовується до властивості
- `Struct`: застосовується до структури

За допомогою логічної операції АБО можна комбінувати ці значення. Наприклад, нехай атрибут може застосовуватися до класів та структур:

```csharp
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct)]
```
