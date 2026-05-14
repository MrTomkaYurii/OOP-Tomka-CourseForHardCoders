---
chapter: 8
chapterTitle: "Розділ 8. Додаткові можливості ООП у C#"
section: 4
number: "8.4"
title: "Індексатори"
source: "../_combined/49-indeksatory.md"
---

## 8.4. Індексатори

Індексатори дозволяють індексувати об'єкти та звертатися до даних щодо індексу. Фактично, за допомогою індексаторів ми можемо працювати з об'єктами як з масивами. За формою вони нагадують властивості зі стандартними блоками get та set, які повертають та надають значення.

Формальне визначення індексатора:

```csharp
тип_що_повертається this [Тип параметр1, ...]
{
    get { ... }
    set { ... }
}
```
На відміну від властивостей, індексатор не має назви. Замість нього вказується ключове слово this, після якого у квадратних дужках йдуть параметри. Індексатор повинен мати щонайменше один параметр.

Подивимося на прикладі. Припустимо, у нас є клас Person, який представляє людину, і клас Company, який представляє деяку компанію, де працюють люди. Використовуємо індексатори для визначення класу Company:

```csharp
class Person
{
    public string Name { get; }
    public Person(string name) => Name = name;
}
class Company
{
    Person[] personal;
    public Company(Person[] people) => personal = people;
    // індексатор
    public Person this[int index]
    {
        get => personal[index];
        set => personal[index] = value;
    }
}
```
Для зберігання персоналу компанії у класі визначено масив personal, що складається з об'єктів Person. Для доступу до цих об'єктів визначено індексатор:

```csharp
public Person this[int index]
```
Індексатор у принципі подібний до стандартної властивості. По-перше, для індексатора визначається тип у разі тип Person. Тип індексатора визначає, які об'єкти отримуватиме і повертатиме індексатор.

По-друге, для індексатора визначено параметр int index, через який звертаємось до елементів усередині об'єкту Company.

Для повернення об'єкта в індексаторі визначено блок get:

```csharp
get => personal[index];
```
Оскільки індексатор має тип Person, то у блоці get нам треба повернути об'єкт цього типу за допомогою оператора return. Тут ми можемо визначити різноманітну логіку. В даному випадку просто повертаємо об'єкт із масиву personal.

У блоці set, як і в звичайній властивості, отримуємо через параметр value переданий об'єкт Person і зберігаємо його в масив за індексом.

```csharp
set => personal[index] = value;
```
Після цього ми можемо працювати з об'єктом Company як із набором об'єктів Person:

```csharp
var microsoft = new Company(new[]
{
    new Person("Tom"), new Person("Bob"), new Person("Sam"), new Person("Alice")
});
// отримуємо об'єкт із індексатора
Person firstPerson = microsoft[0];
Console.WriteLine(firstPerson.Name); // Tom
// перевстановлюємо об'єкт
microsoft[0] = new Person("Mike");
Console.WriteLine(microsoft[0].Name); // Mike
```
Варто зазначити, що якщо індексатору буде передано некоректний індекс, який відсутній у масиві person, ми отримаємо виняток, як і у разі звернення безпосередньо до елементів масиву. І тут можна передбачити якусь додаткову логіку. Наприклад, перевіряти переданий індекс:

```csharp
class Company
{
    Person[] personal;
    public Company(Person[] people) => personal = people;
    // індексатор
    public Person this[int index]
    {
        get
        {
            // якщо індекс є в масиві
            if (index >= 0 && index < personal.Length)
                return personal[index];
            // то повертаємо об'єкт Person за індексом
            else
                throw new ArgumentOutOfRangeException();
            // інакше генеруємо виняток
        }
        set
        {
            // якщо індекс є у масиві
            if (index >= 0 && index < personal.Length)
                personal[index] = value; // встановлюємо значення за індексом
        }
    }
}
```
Тут у блоці get якщо переданий індекс є у масиві, то повертаємо об'єкт за індексом. Якщо індексу немає у масиві, то генеруємо виняток. Аналогічно в блоці set встановлюємо значення індексу, якщо індекс є в масиві.

### Індекси

Індексатор отримує набір індексів як параметрів. Однак індекси необов'язково мають представляти тип int, що встановлюються/повертаються значення необов'язково зберігати в масиві. Наприклад, ми можемо розглядати об'єкт як сховище атрибутів/властивостей та передавати ім'я атрибута у вигляді рядка:

```csharp
User tom = new User();
// встановлюємо значення
tom["name"] = "Tom";
tom["email"] = "tom@gmail.ru";
tom["phone"] = "+1234556767";
// отримуємо значення
Console.WriteLine(tom["name"]); // Tom
class User
{
    string name = "";
    string email = "";
    string phone = "";
    public string this[string propname]
    {
        get
        {
            switch (propname)
            {
                case "name": return name;
                case "email": return email;
                case "phone": return phone;
                default: throw new Exception("Unknown property name");
            }
        }
        set
        {
            switch (propname)
            {
                case "name":
                    name = value;
                    break;
                case "email":
                    email = value;
                    break;
                case "phone":
                    phone = value;
                    break;
            }
        }
    }
}
```
У цьому випадку індексатор у класі User як індекс отримує рядок, який зберігає назву атрибута (в даному випадку назва поля класу).

У блоці get, залежно від значення рядкового індексу, повертається значення того чи іншого поля класу. Якщо передано невідому назву, то генерується виняток. У блоці set схожа логіка – за індексом дізнаємося, для якого поля треба встановити значення.

### Застосування кількох параметрів

Також індексатор може приймати кілька параметрів. Допустимо, у нас є клас, у якому сховище визначено у вигляді двомірного масиву або матриці:

```csharp
class Matrix
{
    int[,] numbers = new int[,] { { 1, 2, 4 }, { 2, 3, 6 }, { 3, 4, 8 } };
    public int this[int i, int j]
    {
        get => numbers[i, j];
        set => numbers[i, j] = value;
    }
}
```
Тепер у визначенні індексатора використовуються два індекси - i і j. І в програмі ми вже повинні звертатися до об'єкта, використовуючи два індекси:

```csharp
Matrix matrix = new Matrix();
Console.WriteLine(matrix[0, 0]);
matrix[0, 0] = 111;
Console.WriteLine(matrix[0, 0]);
```
Слід враховувати, що індексатор не може бути статичним і застосовується лише до екземпляру класу. Але при цьому індексатори можуть бути віртуальними та абстрактними та можуть перевизначатися у похідних класах.

### Блоки get та set

Як і у властивостях, в індексаторах можна опускати блок get чи set, якщо в них немає потреби. Наприклад, видалимо блок set і зробимо індексатор доступним тільки для читання:

```csharp
class Matrix
{
    int[,] numbers = new int[,] { { 1, 2, 4 }, { 2, 3, 6 }, { 3, 4, 8 } };
    public int this[int i, int j]
    {
        get => numbers[i, j];
    }
}
```
Також ми можемо обмежувати доступ до блоків get та set, використовуючи модифікатори доступу. Наприклад, зробимо блок set приватним:

```csharp
class Matrix
{
    int[,] numbers = new int[,] { { 1, 2, 4 }, { 2, 3, 6 }, { 3, 4, 8 } };
    public int this[int i, int j]
    {
        get => numbers[i, j];
        private set => numbers[i, j] = value;
    }
}
```
### Перевантаження індексаторів

Подібно до методів індексатори можна перевантажувати. У цьому випадку також індексатори повинні відрізнятися за кількістю, типом або порядком використовуваних параметрів. Наприклад:

```csharp
var microsoft = new Company(new Person[] { new("Tom"), new("Bob"), new("Sam") });
Console.WriteLine(microsoft[0].Name); // Tom
Console.WriteLine(microsoft["Bob"].Name); // Bob
class Person
{
    public string Name { get; }
    public Person(string name) => Name = name;
}
class Company
{
    Person[] personal;
    public Company(Person[] people) => personal = people;
    // індексатор
    public Person this[int index]
    {
        get => personal[index];
        set => personal[index] = value;
    }
    public Person this[string name]
    {
        get
        {
            foreach (var person in personal)
            {
                if (person.Name == name) return person;
            }
            throw new Exception("Unknown name");
        }
    }
}
```
У цьому випадку клас Company містить дві версії індексатора. Перша версія отримує та встановлює об'єкт Person за індексом, а друга - тільки отримує об'єкт Person на його ім'я.
