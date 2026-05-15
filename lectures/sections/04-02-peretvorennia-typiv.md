---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 2
number: "4.2"
title: "Перетворення типів"
source: "../_combined/19-peretvorennia-typiv.md"
---

## 4.2. Перетворення типів

У попередньому розділі ми говорили про перетворення об'єктів найпростіших типів. Зараз торкнемося теми перетворення об'єктів класів. Допустимо, у нас є наступна ієрархія класів:

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
        Console.WriteLine($"Person {Name}");
    }
}

class Employee : Person
{
    public string Company { get; set; }

    public Employee(string name, string company) : base(name)
    {
        Company = company;
    }
}

class Client : Person
{
    public string Bank { get; set; }

    public Client(string name, string bank) : base(name)
    {
        Bank = bank;
    }
}
```

У цій ієрархії класів ми можемо простежити наступний ланцюг успадкування: `Object` (всі класи неявно успадковуються від типу `Object`) -> `Person` -> `Employee | Client`.

![Ієрархія класів Object, Person, Employee і Client](_assets/_docx/image85.png)

Причому у цій ієрархії класів базові типи перебувають угорі, а похідні типи - внизу.

## Висхідні перетворення. Upcasting

Об'єкти похідного типу (що знаходиться внизу ієрархії) у той же час є і базовим типом. Наприклад, об'єкт `Employee` в той же час є об'єктом класу `Person`. Що у принципі природно, оскільки кожен співробітник (`Employee`) є людиною (`Person`). І ми можемо написати, наприклад, так:

```csharp
Employee employee = new Employee("Tom", "Microsoft");
Person person = employee;   // перетворення від Employee до Person
Console.WriteLine(person.Name);
```

У разі змінної `person`, яка представляє тип `Person`, присвоюється посилання об'єкт `Employee`. Але щоб зберегти посилання на об'єкт одного класу змінну іншого класу, необхідно виконати перетворення типів - у разі від типу `Employee` до типу `Person`. І оскільки `Employee` успадковується від класу `Person`, то автоматично виконується неявне висхідне перетворення - перетворення до типу, що знаходиться вгорі ієрархії класів, тобто до базового класу.

У результаті змінні `employee` і `person` будуть вказувати на той самий об'єкт у пам'яті, але змінної `person` буде доступна тільки та частина, яка представляє функціонал типу `Person`.

![Висхідне перетворення від Employee до Person](_assets/_docx/image86.png)

Подібним чином робляться й інші висхідні перетворення:

```csharp
Person bob = new Client("Bob", "ContosoBank");
```

Тут змінна `bob`, яка представляє тип `Person`, зберігає посилання на об'єкт `Client`, тому також виконується неявне висхідне перетворення від похідного класу `Client` до базового типу `Person`.

Висхідне неявне перетворення відбуватиметься і в наступному випадку:

```csharp
object person1 = new Employee("Tom", "Microsoft");  // від Employee до object
object person2 = new Client("Bob", "ContosoBank");  // від Client до object
object person3 = new Person("Sam");                 // від Person до object
```

Оскільки тип `object` - базовий для всіх інших типів, то перетворення щодо нього буде здійснюватися автоматично.

## Спадні перетворення. Downcasting

Але крім висхідних перетворень від похідного до базового типу є низхідні перетворення чи downcasting - від базового типу до похідного. Наприклад, у наступному коді змінна `person` зберігає посилання на об'єкт `Employee`:

```csharp
Employee employee = new Employee("Tom", "Microsoft");
Person person = employee;   // перетворення від Employee до Person
```

І може виникнути питання, чи можна звернутися до функціонала типу `Employee` через змінну типу `Person`. Але автоматично такі перетворення не відбуваються, адже не кожна людина (об'єкт `Person`) є співробітником підприємства (об'єктом `Employee`). І для низхідного перетворення необхідно застосувати явне перетворення, вказавши в дужках тип, до якого потрібно виконати перетворення:

```csharp
Employee employee1 = new Employee("Tom", "Microsoft");
Person person = employee1;   // перетворення від Employee до Person

// Employee employee2 = person;    // так не можна, потрібне явне перетворення
Employee employee2 = (Employee)person;  // перетворення від Person до Employee
```

Розглянемо деякі приклади перетворень:

```csharp
// Об'єкт Employee також представляє тип object
object obj = new Employee("Bill", "Microsoft");

// щоб звернутися до можливостей типу Employee, наводимо об'єкт до типу Employee
Employee employee = (Employee)obj;

// об'єкт Client також представляє тип Person
Person person = new Client("Sam", "ContosoBank");

// Перетворення від типу Person до Client
Client client = (Client)person;
```

У першому випадку змінної `obj` присвоєно посилання на об'єкт `Employee`, тому ми можемо перетворити об'єкт `obj` до будь-якого типу, який знаходиться в ієрархії класів між типом `object` і `Employee`.

Якщо нам треба звернутися до якихось окремих властивостей чи методів об'єкта, то нам необов'язково надавати перетворений об'єкт змінній:

```csharp
// Об'єкт Employee також представляє тип object
object obj = new Employee("Bill", "Microsoft");

// Перетворення до типу Person для виклику методу Print
((Person)obj).Print();

// або так
// ((Employee)obj).Print();

// Перетворення до типу Employee, щоб отримати властивість Company
string company = ((Employee)obj).Company;
```

У той же час необхідно бути обережними при подібних перетвореннях. Наприклад, що буде в наступному випадку:

```csharp
// Об'єкт Employee також представляє тип object
object obj = new Employee("Bill", "Microsoft");

// Перетворення до типу Client, щоб отримати властивість Bank
string bank = ((Client)obj).Bank;
```

В даному випадку ми отримаємо помилку, оскільки змінна `obj` зберігає посилання на об'єкт `Employee`. Цей об'єкт також є об'єктом типів `object` і `Person`, тому ми можемо перетворити його до цих типів. Але до типу `Client` ми перетворити не можемо.

Інший приклад:

```csharp
Employee employee1 = new Person("Tom"); //! Помилка

Person person = new Person("Bob");
Employee employee2 = (Employee)person; //! Помилка
```

У цьому випадку ми намагаємося перетворити об'єкт типу `Person` на тип `Employee`, а об'єкт `Person` не є об'єктом `Employee`. Причому в останньому випадку Visual Studio не підкаже, що в даному рядку помилка, і цей рядок навіть нормально скомпілюється, проте в процесі виконання програми ми отримаємо помилку. У цьому числі й полягає підступність перетворень, тому у подібних ситуаціях треба виявляти обережність.

Існує низка способів, щоб уникнути подібних помилок перетворення.

## Способи перетворень

По-перше, можна використовувати ключове слово `as`. За допомогою нього програма намагається перетворити вираз до певного типу, причому не викидає виняток. У разі невдалого перетворення вираз міститиме значення `null`:

```csharp
Person person = new Person("Tom");
Employee? employee = person as Employee;

if (employee == null)
{
    Console.WriteLine("Перетворення пройшло невдало");
}
else
{
    Console.WriteLine(employee.Company);
}
```

Варто зазначити, що змінна `employee` визначається не просто як змінна `Employee`, а саме `Employee?` - після назви типу ставиться знак питання. Що вказує, що змінна може зберігати як значення `null`, так і значення `Employee`.

Другий спосіб полягає в перевірці допустимості перетворення за допомогою ключового слова `is`:

```text
значення is тип
```

Якщо значення ліворуч від оператора представляє тип, вказаний праворуч від оператора, то оператор `is` повертає `true`, інакше повертається `false`.

Причому оператор `is` дозволяє автоматично перетворити значення типу, якщо це значення представляє даний тип. Наприклад:

```csharp
Person person = new Person("Tom");

if (person is Employee employee)
{
    Console.WriteLine(employee.Company);
}
else
{
    Console.WriteLine("Перетворення не допустимо");
}
```

Вираз `if (person is Employee employee)` перевіряє, чи є змінна `person` об'єктом типу `Employee`. І якщо `person` є об'єктом `Employee`, то автоматично перетворює значення змінної `person` на тип `Employee` і перетворене значення зберігає змінну `employee`. Далі у блоці `if` ми можемо використовувати об'єкт `employee` як значення типу `Employee`.

Однак, якщо `person` не є об'єктом `Employee`, як у цьому випадку, то така перевірка поверне значення `false` і перетворення не спрацює.

Оператор `is` також можна застосовувати без перетворення, просто перевіряючи на відповідність типу:

```csharp
Person person = new Person("Tom");

if (person is Employee)
{
    Console.WriteLine("Представляє тип Employee");
}
else
{
    Console.WriteLine("НЕ є об'єктом типу Employee");
}
```
