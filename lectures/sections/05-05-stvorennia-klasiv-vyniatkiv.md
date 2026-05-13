---
chapter: 5
chapterTitle: "Розділ 5. Обробка винятків"
section: 5
number: "5.5"
title: "Створення класів винятків"
source: "../_combined/32-stvorennia-klasiv-vyniatkiv.md"
---

## 5.5. Створення класів винятків

Якщо нас не влаштовують вбудовані типи винятків, ми можемо створити свої типи. Базовим класом для всіх винятків є клас Exception, відповідно для створення своїх типів ми можемо успадкувати цей клас.

Допустимо, у нас у програмі буде обмеження за віком:

```csharp
try
{
    Person person = new Person { Name = "Tom", Age = 17 };
}
catch (Exception ex)
{
    Console.WriteLine($"Помилка: {ex.Message}");
}

class Person
{
    private int age;
    public string Name { get; set; } = "";
    public int Age
    {
        get => age;
        set
        {
            if (value < 18)
            throw new Exception("Особам до 18 реєстрація заборонена");
            else
            age = value;
        }
    }
}
```

У класі Person під час встановлення віку відбувається перевірка, і якщо вік менше 18, то викидається виняток. Клас Exception приймає в конструкторі як параметр рядок, який потім передається до його властивості Message.

Але іноді зручніше використовувати свої класи винятків. Наприклад, у якійсь ситуації ми хочемо обробити певним чином лише ті винятки, які належать до класу Person. Для цього ми можемо зробити спеціальний клас PersonException:

```csharp
class PersonException : Exception
{
    public PersonException(string message)
    : base(message) { }
}
```

Насправді клас крім порожнього конструктора нічого не має, і то в конструкторі ми просто звертаємося до конструктора базового класу Exception, передаючи в нього рядок message. Але тепер ми можемо змінити клас Person, щоб він викидав виняток саме цього типу і відповідно до основної програми обробляти цей виняток:

```csharp
try
{
    Person person = new Person { Name = "Tom", Age = 17 };
}
catch (PersonException ex)
{
    Console.WriteLine($"Помилка: {ex.Message}");
}

class Person
{
    private int age;
    public string Name { get; set; } = "";
    public int Age
    {
        get => age;
        set
        {
            if (value < 18)
            throw new PersonException("Особам до 18 реєстрація заборонена");
            else
            age = value;
        }
    }
}
```

Однак необов'язково успадкувати свій клас винятків саме від типу Exception, можна взяти якийсь інший похідний тип. Наприклад, в даному випадку ми можемо взяти тип ArgumentException, який представляє виняток, що генерується в результаті передачі аргументу методу некоректного значення:

```csharp
class PersonException : ArgumentException
{
    public PersonException(string message)
    : base(message)
    { }
}
```

Кожен тип винятків може визначати якісь свої властивості. Наприклад, в даному випадку ми можемо визначити в класі властивість для зберігання значення, що встановлюється:

```csharp
class PersonException : ArgumentException
{
    public int Value { get; }

    public PersonException(string message, int val)
    : base(message)
    {
        Value = val;
    }
}
```

У конструкторі класу ми встановлюємо цю властивість і при обробці винятку ми його можемо отримати:

```csharp
try
{
    Person person = new Person { Name = "Tom", Age = 17 };
}
catch (PersonException ex)
{
    Console.WriteLine($"Помилка: {ex.Message}");
    Console.WriteLine($"Некоректне значення: {ex.Value}");
}

class Person
{
    private int age;
    public string Name { get; set; } = "";
    public int Age
    {
        get => age;
        set
        {
            if (value < 18)
            throw new PersonException("Особам до 18 реєстрація заборонена", value);
            else
            age = value;
        }
    }
}
```

І в даному випадку ми отримаємо наступний консольний вивід:

![Консольний вивід власного класу винятку](../assets/docx/image94.png)
