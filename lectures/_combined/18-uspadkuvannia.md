
## 4.1. Успадкування

Успадкування (inheritance) є одним із ключових моментів ООП. Завдяки успадкуванню один клас може успадкувати функціональність іншого класу.

Нехай у нас є наступний клас `Person`, який описує окрему людину:

```csharp
class Person
{
    private string _name = "";

    public string Name
    {
        get { return _name; }
        set { _name = value; }
    }

    public void Print()
    {
        Console.WriteLine(Name);
    }
}
```

Але раптом нам знадобився клас, який описує співробітника підприємства - клас `Employee`. Оскільки цей клас реалізовуватиме той самий функціонал, як і клас `Person`, оскільки співробітник - це і людина, було б раціонально зробити клас `Employee` похідним (чи спадкоємцем, чи підкласом) від класу `Person`, який, своєю чергою, називається базовим класом або батьком (або суперкласом):

```csharp
class Employee : Person
{

}
```

Після двокрапки ми вказуємо базовий клас для даного класу. Для класу `Employee` базовим є `Person`, і тому клас `Employee` успадковує ті самі властивості, методи, поля, які є у класі `Person`. Єдине, що не передається під час наслідування, це конструктори базового класу з параметрами.

Таким чином, успадкування реалізує відношення is-a (є), об'єкт класу `Employee` також є об'єктом класу `Person`:

```csharp
Person person = new Person { Name = "Tom" };
person.Print();   // Tom

person = new Employee { Name = "Sam" };
person.Print();   // Sam
```

І оскільки об'єкт `Employee` є і об'єктом `Person`, ми можемо визначити змінну: `Person p = new Employee()`.

За умовчанням усі класи успадковуються від базового класу `Object`, навіть якщо ми явно не встановлюємо спадкування. Тому вище визначені класи `Person` і `Employee` крім своїх методів, також матимуть і методи класу `Object`: `ToString()`, `Equals()`, `GetHashCode()` і `GetType()`.

Усі класи за умовчанням можуть успадковуватись. Однак тут є низка обмежень:

- Не підтримується множинне спадкування, клас може успадковуватися тільки від одного класу.
- При створенні похідного класу треба враховувати тип доступу до базового класу - тип доступу до похідного класу має бути таким самим, як і у базового класу, або більш суворим. Тобто, якщо базовий клас має тип доступу `internal`, то похідний клас може мати тип доступу `internal` чи `private`, але не `public`.
- Проте слід враховувати, що якщо базовий і похідний клас перебувають у різних складаннях (проектах), то в цьому випадку похідний клас може успадковувати лише від класу, що має модифікатор `public`.
- Якщо клас оголошений з модифікатором `sealed`, то від цього класу не можна успадковувати і створювати похідні класи. Наприклад, наступний клас не допускає створення спадкоємців:

```csharp
sealed class Admin
{
}
```

- Не можна успадкувати клас від статичного класу.

## Доступ до членів базового класу із класу-спадкоємця

Повернемося до наших класів `Person` та `Employee`. Хоча `Employee` успадковує весь функціонал від класу `Person`, подивимося, що буде в наступному випадку:

```csharp
class Employee : Person
{
    public void PrintName()
    {
        Console.WriteLine(_name);
    }
}
```

Цей код не спрацює і видасть помилку, тому що змінна `_name` оголошена з модифікатором `private` і тому доступ до неї має тільки клас `Person`. Але в класі `Person` визначено загальнодоступну властивість `Name`, яку ми можемо використовувати, тому наступний код у нас працюватиме нормально:

```csharp
class Employee : Person
{
    public void PrintName()
    {
        Console.WriteLine(Name);
    }
}
```

Таким чином, похідний клас може мати доступ тільки до тих членів базового класу, які визначені з модифікаторами `private protected` (якщо базовий і похідний клас знаходяться в одній збірці), `public`, `internal` (якщо базовий та похідний клас знаходяться в одній збірці), `protected` і `protected internal`.

## Ключове слово base

Тепер додамо до наших класів конструктори:

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
}
```

Клас `Person` має конструктор, який встановлює властивість `Name`. Оскільки клас `Employee` успадковує і встановлює ту саму властивість `Name`, то логічно було б не писати по сто разів код установки, а викликати відповідний код класу `Person`. До того ж властивостей, які треба встановити в конструкторі базового класу, параметрів може бути набагато більше.

За допомогою ключового слова `base` ми можемо звернутися до базового класу. У нашому випадку у конструкторі класу `Employee` нам треба встановити ім'я та компанію. Але ім'я ми передаємо на встановлення в конструктор базового класу, тобто конструктор класу `Person`, за допомогою виразу `base(name)`.

```csharp
Person person = new Person("Bob");
person.Print();     // Bob

Employee employee = new Employee("Tom", "Microsoft");
employee.Print();   // Tom
```

## Конструктори у похідних класах

Конструктори не передаються похідному класу під час успадкування. І якщо в базовому класі не визначено конструктора за замовчуванням без параметрів, а лише конструктори з параметрами (як у випадку з базовим класом `Person`), то у похідному класі ми обов'язково повинні викликати один з цих конструкторів через ключове слово `base`. Наприклад, з класу `Employee` приберемо визначення конструктора:

```csharp
class Employee : Person
{
    public string Company { get; set; } = "";
}
```

У разі ми отримаємо помилку, оскільки клас `Employee` успадковує клас `Person`, але не викликає конструктор базового класу. Навіть якби ми додали якийсь конструктор, який би встановлював ті самі властивості, то ми все одно б отримали помилку:

```csharp
class Employee : Person
{
    public string Company { get; set; } = "";

    public Employee(string name, string company)    // ! Помилка
    {
        Name = name;
        Company = company;
    }
}
```

Тобто в класі `Employee` через ключове слово `base` треба явно викликати конструктор класу `Person`:

```csharp
class Employee : Person
{
    public string Company { get; set; } = "";

    public Employee(string name, string company)
    : base(name)
    {
        Company = company;
    }
}
```

Або як альтернативу ми могли б визначити в базовому класі конструктор без параметрів:

```csharp
class Person
{
    public string Name { get; set; }

    // конструктор без параметрів
    public Person()
    {
        Name = "Tom";
        Console.WriteLine("Виклик конструктора без параметрів");
    }

    public Person(string name)
    {
        Name = name;
    }

    public void Print()
    {
        Console.WriteLine(Name);
    }
}
```

Тоді в будь-якому конструкторі похідного класу, де немає звернення до конструктора базового класу, все одно неявно викликався б цей конструктор за умовчанням. Наприклад, наступний конструктор

```csharp
public Employee(string company)
{
    Company = company;
}
```

фактично був би еквівалентний наступному конструктору:

```csharp
public Employee(string company)
: base()
{
    Company = company;
}
```

## Порядок виклику конструкторів

При виклику конструктора класу спочатку відпрацьовують конструктори базових класів і потім конструктори похідних. Наприклад, візьмемо такі класи:

```csharp
class Person
{
    string name;
    int age;

    public Person(string name)
    {
        this.name = name;
        Console.WriteLine("Person(string name)");
    }

    public Person(string name, int age) : this(name)
    {
        this.age = age;
        Console.WriteLine("Person(string name, int age)");
    }
}

class Employee : Person
{
    string company;

    public Employee(string name, int age, string company) : base(name, age)
    {
        this.company = company;
        Console.WriteLine("Employee(string name, int age, string company)");
    }
}
```

Під час створення об'єкта `Employee`:

```csharp
Employee tom = new Employee("Tom", 22, "Microsoft");
```

Ми отримаємо наступний консольний вивід:

![Консольний вивід порядку виклику конструкторів](assets/docx/image84.png)

У результаті ми отримуємо наступний ланцюг виконань.

Спочатку викликається конструктор `Employee(string name, int age, string company)`. Він делегує виконання конструктору `Person(string name, int age)`.

Викликається конструктор `Person(string name, int age)`, який сам поки що не виконується і передає виконання конструктору `Person(string name)`.

Викликається конструктор `Person(string name)`, який передає виконання конструктору класу `System.Object`, оскільки це базовий за промовчанням клас для `Person`.

Виконується конструктор `System.Object.Object()`, потім виконання повертається конструктору `Person(string name)`.

Виконується тіло конструктора `Person(string name)`, потім виконання повертається конструктору `Person(string name, int age)`.

Виконується тіло конструктора `Person(string name, int age)`, потім виконання повертається конструктору `Employee(string name, int age, string company)`.

Виконується тіло конструктора `Employee(string name, int age, string company)`. У результаті створюється об'єкт `Employee`.

