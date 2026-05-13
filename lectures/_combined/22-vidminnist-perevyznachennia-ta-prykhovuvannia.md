
## 4.5. Відмінність перевизначення та приховування методів

Раніше було розглянуто два способи зміни функціональності методів, успадкованих від базового класу - приховування та перевизначення. У чому різниця між цими двома способами?

## Перевизначення

Візьмемо приклад із перевизначенням методів:

```csharp
class Person
{
    public string Name { get; set; }

    public Person(string name)
    {
        Name = name;
    }

    public virtual void Print()
    {
        Console.WriteLine(Name);
    }
}

class Employee : Person
{
    public string Company { get; set; }

    public Employee(string name, string company)
    : base(name)
    {
        Company = company;
    }

    public override void Print()
    {
        Console.WriteLine($"{Name} працює в {Company}");
    }
}
```

Використовуємо класи у програмі:

```csharp
Person tom = new Employee("Tom", "Microsoft");
tom.Print();        // Tom працює в Microsoft
```

При виклику `tom.Print()` виконується реалізація методу `Print` із класу `Employee`, незважаючи на те, що змінна `tom` - змінна типу `Person`.

Для роботи з віртуальними методами компілятор формує таблицю віртуальних методів (Virtual Method Table або VMT). До неї записуються адреси віртуальних методів. До кожного класу створюється своя таблиця.

Коли створюється об'єкт класу, компілятор передає в конструктор об'єкта спеціальний код, який пов'язує об'єкт і таблицю VMT.

А за виклику віртуального методу з об'єкта береться адреса його таблиці VMT. Потім з VMT витягується адреса методу і передається управління. Тобто процес вибору реалізації методу провадиться під час виконання програми. Власне, так і виконується віртуальний метод. Слід враховувати, що оскільки середовищу виконання спочатку необхідно отримати з таблиці VMT адресу потрібного методу, це трохи уповільнює виконання програми.

## Приховування

Тепер візьмемо ті ж класи `Person` та `Employee`, але замість перевизначення використовуємо приховування:

```csharp
class Person
{
    public string Name { get; set; }

    public Person(string name)
    {
        Name = name;
    }

    public void Print()
    {
        Console.WriteLine(Name);
    }
}

class Employee : Person
{
    public string Company { get; set; }

    public Employee(string name, string company)
    : base(name)
    {
        Company = company;
    }

    public new void Print()
    {
        Console.WriteLine($"{Name} працює в {Company}");
    }
}
```

І подивимося, що буде у наступному випадку:

```csharp
Person tom = new Employee("Tom", "Microsoft");
tom.Print();        // Tom
```

Змінна `tom` являє собою тип `Person`, але зберігає посилання на об'єкт `Employee`. Однак під час виклику методу `Print` буде виконуватися та версія методу, яка визначена саме у класі `Person`, а не у класі `Employee`. Чому? Клас `Employee` не перевизначає метод `Print`, успадкований від базового класу, а фактично визначає новий метод. Тому під час виклику `tom.Print()` викликається метод `Print` із класу `Person`.

