
## 7.7. Копіювання об'єктів. Інтерфейс ICloneable

Оскільки класи представляють типи посилань, то це накладає деякі обмеження на їх використання. Зокрема, припустимо, ми маємо наступний клас:

```csharp
class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
}
```
Створимо один об'єкт Person і спробуємо скопіювати дані в інший об'єкт Person:

```csharp
var tom = new Person("Tom", 23);
var bob = tom;
bob.Name = "Bob";
Console.WriteLine(tom.Name); // Bob
```
В даному випадку об'єкти tom і bob будуть вказувати на той самий об'єкт у пам'яті, тому зміни властивостей для змінної bob торкнуться також і змінну tom.

Щоб змінна bob вказувала на новий об'єкт, але при цьому мала значення зі змінної tom, ми можемо застосувати клонування за допомогою реалізації ICloneable інтерфейсу:

```csharp
public interface ICloneable
{
    object Clone();
}
```
### Поверхневе копіювання

Реалізація інтерфейсу в класі Person могла б виглядати так:

```csharp
class Person : ICloneable
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
    public object Clone()
    {
        return new Person(Name, Age);
    }
}
```
Використання:

```csharp
var tom = new Person("Tom", 23);
var bob = (Person)tom.Clone();
bob.Name = "Bob";
Console.WriteLine(tom.Name); // Tom
```
Тепер все нормально копіюється, зміни у властивостях змінної bob не позначаються на властивостях із змінної tom.

Для скорочення коду копіювання ми можемо використовувати спеціальний метод MemberwiseClone(), який повертає копію об'єкта:

```csharp
class Person : ICloneable
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
    public object Clone()
    {
        return MemberwiseClone();
    }
}
```
Цей метод реалізує поверхневе (неглибоке) копіювання. Однак цього копіювання може бути недостатньо. Наприклад, нехай клас Person містить посилання на об'єкт класу Company:

```csharp
class Person : ICloneable
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Company Work { get; set; }
    public Person(string name, int age, Company company)
    {
        Name = name;
        Age = age;
        Work = company;
    }
    public object Clone() => MemberwiseClone();
}
class Company
{
    public string Name { get; set; }
    public Company(string name) => Name = name;
}
```
У цьому випадку при копіюванні нова копія вказуватиме на той самий об'єкт Company:

```csharp
var tom = new Person("Tom", 23, new Company("Microsoft"));
var bob = (Person)tom.Clone();
bob.Work.Name = "Google";
Console.WriteLine(tom.Work.Name); // Google - має бути Microsoft
```
### Глибоке копіювання

Поверхневе копіювання працює тільки для властивостей, що становлять примітивні типи, але не для складних об'єктів. І в цьому випадку треба застосовувати глибоке копіювання:

```csharp
class Person : ICloneable
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Company Work { get; set; }
    public Person(string name, int age, Company company)
    {
        Name = name;
        Age = age;
        Work = company;
    }
    public object Clone() => new Person(Name, Age, new Company(Work.Name));
}
class Company
{
    public string Name { get; set; }
    public Company(string name) => Name = name;
}
```
### Сортування об'єктів. Інтерфейс IComparable

Більшість вбудованих у .NET класів колекцій та масиви підтримують сортування. За допомогою одного методу, який, як правило, називається, Sort() можна відразу відсортувати за зростанням весь набір даних. Наприклад:

```csharp
int[] numbers = new int[] { 97, 45, 32, 65, 83, 23, 15 };
Array.Sort(numbers);
foreach (int n in numbers)
Console.WriteLine(n);
// 15 23 32 45 65 83 97
```
Однак метод Sort за промовчанням працює тільки для наборів примітивних типів, як int або string. Для сортування наборів складних об'єктів застосовується інтерфейс IComparable. Він має лише один метод:

```csharp
public interface IComparable
{
    int CompareTo(object? o);
}
```
Метод CompareTo призначений для порівняння поточного об'єкта з об'єктом, який передається як параметр object? o. На виході він повертає ціле число, яке може мати одне із трьох значень:

Менше нуля. Отже, поточний об'єкт повинен перебувати перед об'єктом, який передається як параметр

дорівнює нулю. Отже, обидва об'єкти рівні

Більше нуля. Отже, поточний об'єкт повинен перебувати після об'єкта, що передається як параметр

Наприклад, є клас Person:

```csharp
class Person : IComparable
{
    public string Name { get; }
    public int Age { get; set; }
    public Person(string name, int age)
    {
        Name = name; Age = age;
    }
    public int CompareTo(object? o)
    {
        if(o is Person person) return Name.CompareTo(person.Name);
        else throw new ArgumentException("некоректне значення параметрів");
    }
}
```
Тут як критерій порівняння вибрано властивість Name об'єкта Person. Тому при порівнянні тут фактично іде порівняння значення властивості Name поточного об'єкта та властивості Name об'єкта, переданого через параметр. Якщо раптом об'єкт не вдасться привести до типу Person, викидається виняток.

Застосування:

```csharp
var tom = new Person("Tom", 37);
var bob = new Person("Bob", 41);
var sam = new Person("Sam", 25);
Person[] people = { tom, bob, sam};
Array.Sort(people);
foreach (Person person in people)
{
    Console.WriteLine($"{person.Name} - {person.Age}");
}
```
І в даному випадку ми отримаємо наступний консольний вивід:

```csharp
Bob - 41
Sam - 25
Tom – 37
```

Інтерфейс IComparable має узагальнену версію, тому ми могли б скоротити та спростити його застосування у класі Person:

```csharp
class Person : IComparable<Person>
{
    public string Name { get; }
    public int Age { get; set; }
    public Person(string name, int age)
    {
        Name = name; Age = age;
    }
    public int CompareTo(Person? person)
    {
        if(person is null) throw new ArgumentException("некоректне значення параметра");
        return Name.CompareTo(person.Name);
    }
}
```
Аналогічним чином ми могли порівнювати за віком:

```csharp
class Person : IComparable<Person>
{
    public string Name { get; }
    public int Age { get; set; }
    public Person(string name, int age)
    {
        Name = name; Age = age;
    }
    public int CompareTo(Person? person)
    {
        if(person is null) throw new ArgumentException("Некоректне значення параметра");
        return Age - person.Age;
    }
}
```
### Застосування компаратора

Крім інтерфейсу IComparable, платформа .NET також надає інтерфейс IComparer:

```csharp
public interface IComparer<in T>
{
    int Compare(T? x, T? y);
}
```
Метод Compare призначений для порівняння двох об'єктів o1 та o2. Він також повертає три значення, залежно від результату порівняння: якщо перший об'єкт більший за другий, то повертається число більше 0, якщо менше - то число менше нуля; якщо обидва об'єкти дорівнюють, повертається нуль.

Створимо компаратор об'єктів Person. Нехай він порівнює об'єкти залежно від довжини рядка – значення властивості Name:

```csharp
class PeopleComparer : IComparer<Person>
{
    public int Compare(Person? p1, Person? p2)
    {
        if(p1 is null || p2 is null)
        throw new ArgumentException("Некоректне значення параметра");
        return p1.Name.Length - p2.Name.Length;
    }
}
class Person
{
    public string Name { get; }
    public int Age { get; set; }
    public Person(string name, int age)
    {
        Name = name; Age = age;
    }
}
```
У цьому випадку використовується узагальнена версія інтерфейсу IComparer, щоб не робити зайвих перетворень типів. Застосування компаратора:

```csharp
var alice = new Person("Alice", 41);
var tom = new Person("Tom", 37);
var kate = new Person("Kate", 25);
Person[] people = { alice, tom, kate};
Array.Sort(people, new PeopleComparer());
foreach (Person person in people)
{
    Console.WriteLine($"{person.Name} - {person.Age}");
}
```
Об'єкт компаратора вказується як другий параметр методу Array.Sort(). При цьому не важливо, чи реалізує клас Person інтерфейс IComparable чи ні. Правила сортування, встановлені компаратором, матимуть більший пріоритет. На початку будуть йти об'єкти Person, у яких імена менші, а в кінці - у яких імена довші:

```csharp
Tom - 37
Kate - 25
Alice – 41
```
