---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
section: 2
number: "14.2"
title: "Застосування рефлексії та дослідження типів"
source: "../_combined/85-zastosuvannia-refleksii-ta-doslidzhennia-typiv.md"
---

## 14.2. Застосування рефлексії та дослідження типів

### Отримання всіх компонентів типу

Метод `GetMembers()` повертає всі доступні компоненти типу як об'єкт `MemberInfo`. Цей об'єкт дозволяє отримати інформацію про компонент типу. Зокрема, деякі його властивості:

- `DeclaringType`: повертає повну назву типу
- `MemberType`: повертає значення з переліку `MemberTypes`:
- `MemberTypes.Constructor`
- `MemberTypes.Method`
- `MemberTypes.Field`
- `MemberTypes.Event`
- `MemberTypes.Property`
- `MemberTypes.NestedType`
- `Name`: повертає назву компонента

Застосуємо метод `GetMembers` і виведемо всі доступні елементи типу:

```csharp
using System.Reflection; // Підключаємо функціонал рефлексії.

Type myType = typeof(Person);

foreach (MemberInfo member in myType.GetMembers())
{
    Console.WriteLine($"{member.DeclaringType} {member.MemberType} {member.Name}");
}

public class Person
{
    string name;
    public int Age { get; set; }
    public Person(string name, int age)
    {
        this.name = name;
        this.Age = age;
    }
    public void Print() => Console.WriteLine($"Name: {name} Age: {Age}");
}
```

В даному випадку ми отримаємо всі доступні члени класу `Person`.

```text
Person Method get_Age
Person Method set_Age
Person Method Print

System.Object Method GetType
System.Object Method ToString
System.Object Method Equals
System.Object Method GetHashCode
Person Constructor .ctor
Person Property Age
```

Зверніть увагу, що в даному випадку ми отримуємо тільки всі публічні компоненти класу, і нам не виводиться інформація про приватну змінну `name`.

З іншого боку, властивості виводяться методи доступу - геттер (тут `get_Age`) і сеттер (тут `set_Age`).

Третій момент, який слід зазначити, що за умовчанням ми отримуємо весь функціонал, у тому числі успадкований від базових класів (у цьому випадку функціонал базового класу `Object`).

### BindingFlags

У прикладі вище використовувалася проста форма методу `GetMembers()`, яка витягує всі загальнодоступні публічні методи. Але ми можемо використовувати й іншу форму методу: `MemberInfo[] GetMembers(BindingFlags)`. Перелік `BindingFlags` може набувати різних значень:

- `DeclaredOnly`: отримує тільки методи безпосередньо даного класу, успадковані методи не вилучаються
- `Instance`: отримує тільки методи екземпляра
- `NonPublic`: витягує непублічні методи
- `Public`: отримує лише публічні методи
- `Static`: отримує лише статичні методи

Поєднуючи дані значення за допомогою побітової операції АБО можна комбінувати вивід. Наприклад, отримаємо лише компоненти безпосередньо самого класу без успадкованих, як публічні, і всі інші:

```csharp
using System.Reflection; // Підключаємо функціонал рефлексії.

Type myType = typeof(Person);

foreach (MemberInfo member in myType.GetMembers(
             BindingFlags.DeclaredOnly |
             BindingFlags.Instance |
             BindingFlags.NonPublic |
             BindingFlags.Public))
{
    Console.WriteLine($"{member.DeclaringType} {member.MemberType} {member.Name}");
}

public class Person
{
    string name;
    public int Age { get; set; }
    public Person(string name, int age)
    {
        this.name = name;
        this.Age = age;
    }
    public void Print() => Console.WriteLine($"Name: {name} Age: {Age}");
}
```

І в даному випадку ми отримаємо дещо інший вивід:

```text
Person Method get_Age
Person Method set_Age
Person Method Print
Person Constructor .ctor
Person Property Age
Person Field name
Person Field <Age>k__BackingField
```

### Отримання одного компонента на ім'я

Для отримання одного компонента можна використовувати метод `GetMember()`, який передає ім'я компонента. І опціонально можна передати прапори `BindingFlags`.

```csharp
Type myType = typeof(Person);

// Отримуємо метод Print.
MemberInfo[] print = myType.GetMember("Print", BindingFlags.Instance | BindingFlags.Public);
foreach (MemberInfo member in print)
{
    Console.WriteLine($"{member.MemberType} {member.Name}");
}
```

Варто зазначити, що при отриманні одного члена типу знову ж таки повертається масив `MemberInfo[]`, оскільки в класі може бути кілька елементів з одним ім'ям, наприклад, кілька перевантажених версій методу `Print`.
