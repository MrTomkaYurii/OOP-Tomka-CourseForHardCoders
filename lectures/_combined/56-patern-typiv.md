## 9.1. Патерн типів

Pattern matching фактично виконує зіставлення деякого значення з деяким шаблоном. І якщо зіставлення пройшло успішно, виконуються певні дії. Мова C# дозволяє виконувати різні типи зіставлень.

Патерн типів або type pattern дозволяє перевірити деяке значення на відповідність деякому типу:

```text
значення is тип змінна_типу
```

Наприклад, у нас є такі класи:

```csharp
class Employee
{
    public virtual void Work() => Console.WriteLine("Employee works");
}

class Manager : Employee
{
    public override void Work() => Console.WriteLine("Manager works");
    public bool IsOnVacation { get; set; }
}
```

Клас Employee представляє працівника, а клас Manager - менеджера. Обидва класи реалізують метод Work. Крім того, клас Manager визначає властивість IsOnVacation.

За допомогою патерна типів перевіримо, чи представляє об'єкт Employee клас Manager:

```csharp
Employee tom = new Manager();
UseEmployee(tom);   // Manager works

void UseEmployee(Employee emp)
{
    if (emp is Manager manager && manager.IsOnVacation == false)
    {
        manager.Work();
    }
    else
    {
        Console.WriteLine("Перетворення не припустимо");
    }
}
```

Тут у методі UseEmployee значення emp зіставляється з типом Manager. Тобто в даному випадку як шаблон виступає тип Manager. Якщо зіставлення пройшло успішно (тобто значення emp представляє тип Manager), у змінній manager виявляється об'єкт emp. І далі ми можемо викликати в нього методи та властивості.

Також ми можемо використовувати constant pattern - зіставлення з деякою константою:

```csharp
var message = "hello";

// перевіряємо, чи відповідає значення message рядку "hello"
if (message is "hello")
{
    Console.WriteLine("hello");
}
```

Подібним чином, наприклад, можна перевірити значення на null:

```csharp
Employee? bob = new Employee();
Employee? tom = null;

UseEmployee(bob);
UseEmployee(tom);

void UseEmployee(Employee? emp)
{
    if (emp is not null)
        emp.Work();
}
```

Крім конструкції if зіставлення патернів може застосовуватися в конструкції switch:

```csharp
Employee bob = new Employee();
Employee tom = new Manager();
UseEmployee(tom);   // Manager works
UseEmployee(bob);   // Object is not manager

void UseEmployee(Employee? emp)
{
    switch (emp)
    {
        case Manager manager:
            manager.Work();
            break;
        case null:
            Console.WriteLine("Object is null");
            break;
        default:
            Console.WriteLine("Object is not manager");
            break;
    }
}
```

За допомогою виразу when можна вводити додаткові умови в конструкцію case:

```csharp
Employee bob = new Manager() { IsOnVacation = true };
Employee tom = new Manager() { IsOnVacation = false };
UseEmployee(tom);   // Manager works
UseEmployee(bob);   // Employee does not work

void UseEmployee(Employee? emp)
{
    switch (emp)
    {
        case Manager manager when !manager.IsOnVacation:
            manager.Work();
            break;
        case null:
            Console.WriteLine("Employee is null");
            break;
        default:
            Console.WriteLine("Employee does not work");
            break;
    }
}
```

У цьому випадку знову ж таки перетворимо об'єкт emp на об'єкт типу Manager і в разі вдалого перетворення дивимося на значення властивості IsOnVacation: якщо воно дорівнює false, то виконується даний блок case.
