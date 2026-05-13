---
chapter: 4
chapterTitle: "Розділ 4. Об'єктно-орієнтоване програмування"
section: 9
number: "4.9"
title: "Обмеження узагальнень"
source: "../_combined/26-obmezhennia-uzahalnen.md"
---

## 4.9. Обмеження узагальнень

За допомогою універсальних параметрів ми можемо типувати узагальнені класи будь-яким типом. Однак іноді виникає потреба конкретизувати тип. Наприклад, у нас є наступний клас `Message`, який представляє деяке повідомлення:

```csharp
class Message
{
    public string Text { get; } // текст повідомлення

    public Message(string text)
    {
        Text = text;
    }
}
```

І, припустимо, ми хочемо визначити метод для надсилання повідомлень у вигляді об'єктів `Message`. На перший погляд ми можемо визначити та використовувати наступний метод:

```csharp
SendMessage(new Message("Hello World"));

void SendMessage(Message message)
{
    Console.WriteLine($"Надсилається повідомлення: {message.Text}");
}
```

Метод `SendMessage` як параметр `message` приймає об'єкт `Message` та емулює його відправлення. Начебто все нормально і щось краще навряд чи можна придумати. Але у класу `Message` можуть бути класи-спадкоємці. Наприклад, клас `EmailMessage` для email-повідомлень, `SmsMessage` - для sms-повідомлень і так далі:

```csharp
class EmailMessage : Message
{
    public EmailMessage(string text) : base(text) { }
}

class SmsMessage : Message
{
    public SmsMessage(string text) : base(text) { }
}
```

Що якщо ми хочемо також надсилати повідомлення, які представляють ці класи? Проблеми начебто немає, оскільки метод `SendMessage` приймає об'єкт `Message` і відповідно також об'єкти похідних класів:

```csharp
SendMessage(new EmailMessage("Hello World"));

void SendMessage(Message message)
{
    Console.WriteLine($"Надсилається повідомлення: {message.Text}");
}
```

Але тут ми стикаємося із перетворенням типів: від `EmailMessage` до `Message`. Крім того, знову ж таки можлива проблема типобезпеки, якщо ми захочемо перетворити об'єкт `message` в об'єкт похідних класів. І в цьому випадку, щоб уникнути перетворень, ми можемо застосувати узагальнення:

```csharp
void SendMessage<T>(T message)
{
    Console.WriteLine($"Надсилається повідомлення: {message.Text}"); //! Помилка - властивість Text
}
```

Узагальнення дозволяють уникнути перетворень, але тепер ми стикаємося з іншою проблемою - універсальний параметр `T` має на увазі будь-який тип. Не будь-який тип має властивість `Text`. Відповідно властивість `Text` для об'єкта типу `T` не визначено і ми не можемо використовувати цю властивість. Більше того, для об'єкта `T` за умовчанням нам доступні лише методи типу `object`.

Таким чином виникає проблема: треба уникнути перетворень типів і відповідно використовувати узагальнення, а з іншого боку, необхідно звертатися всередині методу до функціоналу класу `Message`. І обмеження узагальнень дозволяють вирішити цю проблему.

## Обмеження методів

Обмеження методів вказуються після списку параметрів після оператора `where`:

```text
ім'я_методу<T>(параметри) where T: тип_обмеження
```

Після оператора `where` вказується універсальний параметр, для якого застосовується обмеження. І через двокрапку вказується тип обмеження - зазвичай як обмеження виступає конкретний тип.

Наприклад, застосуємо обмеження до методу `SendMessage`, який надсилає об'єкти `Message`:

```csharp
SendMessage(new Message("Hello World"));
SendMessage(new EmailMessage("Bye World"));

void SendMessage<T>(T message) where T : Message
{
    Console.WriteLine($"Надсилається повідомлення: {message.Text}");
}

class Message
{
    public string Text { get; } // Текст повідомлення

    public Message(string text)
    {
        Text = text;
    }
}

class EmailMessage : Message
{
    public EmailMessage(string text) : base(text) { }
}
```

Вираз `where T: Message` у визначенні методу `SendMessage` говорить, що через універсальний параметр `T` будуть передаватися об'єкти класу `Message` та похідних класів. Завдяки цьому компілятор знатиме, що `T` матиме функціонал класу `Message`, і ми зможемо звернутися до методів і властивостей класу `Message` всередині методу без проблем.

При виклику методу нам необов'язково вказувати тип у кутових дужках - компілятор на підставі переданого значення сам визначить, яким типом типізується метод:

```csharp
SendMessage(new EmailMessage("Bye World"));
```

Однак це можна зробити і явно:

```csharp
SendMessage<EmailMessage>(new EmailMessage("Bye World"));
```

## Обмеження узагальнень у типах

Подібним чином можна визначати обмеження узагальнених типів. Наприклад, обмеження узагальнених класів:

```text
class ім'я_класу<T> where T: тип_обмеження
```

Як приклад визначимо клас месенджера, який надсилатиме повідомлення у вигляді об'єктів `Message`:

```csharp
class Messenger<T> where T : Message
{
    public void SendMessage(T message)
    {
        Console.WriteLine($"Надсилається повідомлення: {message.Text}");
    }
}

class Message
{
    public string Text { get; } // Текст повідомлення

    public Message(string text)
    {
        Text = text;
    }
}

class EmailMessage : Message
{
    public EmailMessage(string text) : base(text) { }
}
```

Тут для класу `Messenger` знову ж таки встановлено обмеження `where T : Message`. Тобто, всередині класу `Messenger` всі об'єкти типу `T` можна використовувати як об'єкти `Message`. І в даному випадку в класі `Messenger` у методі `SendMessage` знову емулюється відправка повідомлення.

Застосуємо клас для надсилання повідомлень:

```csharp
Messenger<Message> telegram = new Messenger<Message>();
telegram.SendMessage(new Message("Hello World"));

Messenger<EmailMessage> outlook = new Messenger<EmailMessage>();
outlook.SendMessage(new EmailMessage("Bye World"));
```

## Типи обмежень та стандартні обмеження

Як обмеження ми можемо використовувати такі типи:

- Класи
- Інтерфейси
- `class` - універсальний параметр має представляти клас
- `struct` - універсальний параметр має представляти структуру
- `new()` - універсальний параметр повинен представляти тип, який має загальнодоступний конструктор без параметрів

Є низка стандартних обмежень, які ми можемо використати. Зокрема, можна вказати обмеження, щоб використовувалися лише структури чи інші типи значень:

```csharp
class Messenger<T> where T : struct
{
}
```

При цьому використовувати як обмеження конкретні структури на відміну класів не можна.

Також можна задати як обмеження типи посилань:

```csharp
class Messenger<T> where T : class
{
}
```

А також можна задати за допомогою слова `new` як обмеження клас або структуру, які мають загальнодоступний конструктор без параметрів:

```csharp
class Messenger<T> where T : new()
{
}
```

Якщо для універсального параметра встановлено кілька обмежень, то вони повинні йти в певному порядку:

- Назва класу, `class`, `struct`. Причому ми можемо одночасно визначити лише одне з цих обмежень
- Назва інтерфейсу
- `new()`

```csharp
class Smartphone<T> where T : Messenger, new()
{

}
```

## Використання кількох універсальних параметрів

Якщо клас використовує кілька універсальних параметрів, то послідовно можна встановити обмеження до кожного з них:

```csharp
class Messenger<T, P>
where T : Message
where P : Person
{
    public void SendMessage(P sender, P receiver, T message)
    {
        Console.WriteLine($"Відправник: {sender.Name}");
        Console.WriteLine($"Отримувач: {receiver.Name}");
        Console.WriteLine($"Повідомлення: {message.Text}");
    }
}

class Person
{
    public string Name { get; }

    public Person(string name) => Name = name;
}

class Message
{
    public string Text { get; } // Текст повідомлення

    public Message(string text) => Text = text;
}
```

В даному випадку для параметра `P` будуть передаватися об'єкти типу `Person`, а для параметра `T` - об'єкти `Message`.

Застосуємо класи:

```csharp
Messenger<Message, Person> telegram = new Messenger<Message, Person>();
Person tom = new Person("Tom");
Person bob = new Person("Bob");
Message hello = new Message("Hello, Bob!");
telegram.SendMessage(tom, bob, hello);
```

Консольний вивід:

![Консольний вивід надсилання повідомлення через узагальнений Messenger](assets/docx/image90.png)
