## 8.6. Часткові класи та методи

Класи можуть бути частковими. Тобто ми можемо мати кілька файлів з визначенням того самого класу, і при компіляції всі ці визначення будуть скомпільовані в одне.

Наприклад, визначимо у проєкті два файли з кодом. Не так важливо, як ці файли будуть називатися. Наприклад, PersonBase.cs та PersonAdditional.cs. В одному з цих файлів (без різниці в якому саме) визначимо наступний клас:

```csharp
public partial class Person
{
    public void Move()
    {
        Console.WriteLine("I am moving");
    }
}
```

А в іншому файлі визначимо наступний клас:

```csharp
public partial class Person
{
    public void Eat()
    {
        Console.WriteLine("I am eating");
    }
}
```

Таким чином, два файли в проєкті містять визначення одного і того ж класу Person, які містять два різні методи. І обидва визначені тут класи є частковими. Для цього вони визначаються з ключовим словом partial.

Потім ми можемо використовувати всі методи класу Person:

```csharp
class Program
{
    static void Main(string[] args)
    {
        Person tom = new Person();
        tom.Move();
        tom.Eat();

        Console.ReadKey();
    }
}
```

### Часткові методи

Часткові класи можуть містити часткові методи. Такі методи також визначаються з ключовим словом partial. Причому визначення часткового методу без тіла методу перебуває в одному частковому класі, а реалізація цього методу - в іншому частковому класі.

Наприклад, змінимо вище визначені класи Person. Перший клас:

```csharp
public partial class Person
{
    partial void Read();
    public void DoSomething()
    {
        Read();
    }
}
```

Другий клас:

```csharp
public partial class Person
{
    partial void Read()
    {
        Console.WriteLine("I am reading a book");
    }
}
```

У першому класі визначено метод Read(). Причому на момент визначення першого класу невідомо, що робить цей метод, які дії він виконуватиме. Тим не менш, ми знаємо список його параметрів і можемо викликати його в першому класі.

Другий клас вже безпосередньо визначає тіло методу Read().

```csharp
class Program
{
    static void Main(string[] args)
    {
        Person tom = new Person();
        tom.DoSomething();
    }
}
```

Варто зазначити, що за умовчанням до часткових методів застосовується низка обмежень:

- Вони не можуть мати модифікаторів доступу
- Вони мають тип void
- Вони не можуть мати out-параметри
- Вони не можуть мати модифікатори virtual, override, sealed, new або extern

Якщо ж вони не відповідають якомусь із цих обмежень, то для них має бути надана реалізація. Як, наприклад, у наступному прикладі часткові методи застосовують модифікатор public:

```csharp
// перша реалізація класу та його методів
public partial class Person
{
    public partial void Read();
    public void DoSomething()
    {
        Read();
    }
}

// друга реалізація класу та його методів
public partial class Person
{
    public partial void Read()
    {
        Console.WriteLine("I am reading a book");
    }
}
```
