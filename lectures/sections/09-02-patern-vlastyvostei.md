---
chapter: 9
chapterTitle: "Розділ 9. Pattern matching"
section: 2
number: "9.2"
title: "Патерн властивостей"
source: "../_combined/57-patern-vlastyvostei.md"
---

## 9.2. Патерн властивостей

Патерн властивостей дозволяє порівнювати із значеннями певних властивостей об'єкта. Наприклад, нехай у нас буде наступний клас:

```csharp
class Person
{
    public string Name { get; set; } = "";        // Ім'я користувача
    public string Status { get; set; } = "";      // статус користувача
    public string Language { get; set; } = "";    // мова користувача
}
```

Наприклад, залежно від мови користувача виведемо йому певне повідомлення, застосувавши патерн властивостей:

```csharp
Person tom = new Person { Language = "english", Status = "user", Name = "Tom" };
Person pierre = new Person
{
    Language = "french",
    Status = "user",
    Name = "Pierre"
};

SayHello(tom);      // Hello
SayHello(pierre);   // Salut

void SayHello(Person person)
{
    if (person is Person { Language: "french" })
    {
        Console.WriteLine("Salut");
    }
    else
    {
        Console.WriteLine("Hello");
    }
}
```

Тут метод SayHello як параметр приймає об'єкт Person і зіставляє його з деяким патерном. Як патерн виступає вираз Person { Language: "french" }. Тобто параметр person повинен представляти об'єкт Person, у якого значення властивості Language дорівнює "french".

При цьому можна використовувати набір властивостей. Наприклад, додамо перевірку за властивістю Status:

```csharp
Person admin = new Person { Language = "english", Status = "admin", Name = "Admin" };
Person tom = new Person { Language = "english", Status = "user", Name = "Tom" };
Person pierre = new Person
{
    Language = "french",
    Status = "user",
    Name = "Pierre"
};

SayHello(admin);    // Hello, admin
SayHello(tom);      // Hello
SayHello(pierre);   // Salut

void SayHello(Person person)
{
    if (person is Person { Language: "english", Status: "admin" })
    {
        Console.WriteLine("Hello, admin");
    }
    else if (person is Person { Language: "french" })
    {
        Console.WriteLine("Salut");
    }
    else
    {
        Console.WriteLine("Hello");
    }
}
```

Тепер вираз if перевіряє, чи параметр person є об'єктом Person, у якого властивості Language і Status мають певні значення.

Подібним чином можна застосовувати патерн властивостей у конструкції switch:

```csharp
string GetMessage(Person? p) => p switch
{
    { Language: "english" } => "Hello!",
    { Language: "german", Status: "admin" } => "Hallo, admin!",
    { Language: "french" } => "Salut!",
    { } => "undefined",
    null => "null"       // якщо Person p = null
};
```

Патерни властивостей припускають використання фігурних дужок, усередині яких вказуються властивості і через двокрапку їх значення `{ властивість: значення }`. І зі значенням властивості у фігурних дужках порівнюється властивість об'єкта, що передається. При цьому у фігурних дужках ми можемо вказати кілька властивостей та їх значень `{ Language: "german", Status: "admin" }` - тоді властивості об'єкта, що передається, повинні відповідати всім цим значенням.

Можна залишити порожні фігурні дужки, як в останньому випадку `{ } => "undefined!"` - об'єкт, що передається, буде відповідати порожнім фігурним дужкам, якщо він не відповідає всім попереднім значенням, або наприклад, якщо його властивості не вказані або мають значення null.

Тобто в даному випадку, якщо об'єкт Person p виконує рівність Language = "english", повертатиметься рядок "Hello!".

Якщо об'єкт Person p одночасно виконує дві рівності Language = "german" і Status = "admin", буде повертатися рядок "Hallo, admin!".

Якщо об'єкт Person p виконує рівність Language = "french", повертатиметься рядок "Salut!".

Якщо об'єкт Person буде зіставлятися з порожніми фігурними дужками {} і повертатиметься рядок "undefined".

Остання перевірка перевіряє значення null.

Застосування:

```csharp
Person pierre = new Person
{
    Language = "french",
    Status = "user",
    Name = "Pierre"
};
string message = GetMessage(pierre);
Console.WriteLine(message);          // Salut!

Person tomas = new Person
{
    Language = "german",
    Status = "admin",
    Name = "Tomas"
};
Console.WriteLine(GetMessage(tomas));     // Hallo, admin!

Person pablo = new Person
{
    Language = "spanish",
    Status = "user",
    Name = "Pablo"
};
Console.WriteLine(GetMessage(pablo));     // undefined

Console.WriteLine(GetMessage(null));      // null
```

Крім того, ми можемо визначати в патернах властивостей змінні, передавати цим змінним значення об'єкта та використовувати при поверненні значення:

```csharp
string GetMessage(Person? p) => p switch
{
    { Language: "german", Status: "admin" } => "Hallo, admin!",
    { Language: "french", Name: var name } => $"Salut, {name}!",
    { Language: var lang } => $"Unknown language: {lang}",
    null => "null"
};
```

Так, підвираз Name: var name говорить, що треба передати змінній name значення властивості Name. Потім її можна застосувати при генерації вихідного значення: `=> $"Salut, {name}!"`

Застосування:

```csharp
Person pierre = new Person
{
    Language = "french",
    Status = "user",
    Name = "Pierre"
};
string message = GetMessage(pierre);
Console.WriteLine(message);             // Salut, Pierre!

Person tomas = new Person
{
    Language = "german",
    Status = "admin",
    Name = "Tomas"
};
Console.WriteLine(GetMessage(tomas));     // Hallo, admin!

Person pablo = new Person
{
    Language = "spanish",
    Status = "user",
    Name = "Pablo"
};
Console.WriteLine(GetMessage(pablo));     // Unknown language: spanish

Person? bob = null;
Console.WriteLine(GetMessage(bob));       // null
```

Починаючи з версії C# 10 було спрощено зіставлення з властивостями вкладених об'єктів. Припустимо, у нас є такі класи:

```csharp
class Employee
{
    public string Name { get; }
    public Company Company { get; set; }
    public Employee(string name, Company company)
    {
        Name = name;
        Company = company;
    }
}

class Company
{
    public string Title { get; }
    public Company(string title) => Title = title;
}
```

Клас Company визначає властивість Title, що зберігає назву компанії. Клас Employee визначає співробітника фірми і як Company зберігає компанію. Застосуємо патерн властивостей з урахуванням властивостей вкладеного об'єкта Company:

```csharp
var microsoft = new Company("Microsoft");
var google = new Company("Google");
var tom = new Employee("Tom", microsoft);
var bob = new Employee("Bob", google);

PrintCompany(tom);    // Tom works in Microsoft
PrintCompany(bob);    // Bob works somewhere

void PrintCompany(Employee employee)
{
    if (employee is Employee { Company: { Title: "Microsoft" } })
    {
        Console.WriteLine($"{employee.Name} works in Microsoft");
    }
    else
    {
        Console.WriteLine($"{employee.Name} works somewhere");
    }
}
```

У методі PrintCompany об'єкт employee зіставляється з патерном Employee { Company:{Title: "Microsoft" } }. Тобто співробітник компанії повинен представляти об'єкт Employee, у якого назва компанії рівна "Microsoft"

Однак ми також можемо скоротити цей патерн таким чином:

```csharp
void PrintCompany(Employee employee)
{
    if (employee is Employee { Company.Title: "Microsoft" })
    {
        Console.WriteLine($"{employee.Name} works in Microsoft");
    }
    else
    {
        Console.WriteLine($"{employee.Name} works somewhere");
    }
}
```
