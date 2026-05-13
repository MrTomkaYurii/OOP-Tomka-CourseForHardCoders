---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 8
number: "7.8"
title: "Коваріантність та контраваріантність узагальнених інтерфейсів"
source: "../_combined/45-kovariantnist-ta-kontravariantnist-uzahalnenykh-interfeisiv.md"
---

## 7.8. Коваріантність та контраваріантність узагальнених інтерфейсів

Поняття коваріантності та контраваріантності пов'язані з можливістю використовувати в додатку замість деякого типу інший тип, який знаходиться нижче або вище в ієрархії спадкування.

Є три можливі варіанти поведінки:

Коваріантність: дозволяє використовувати більш конкретний тип, ніж заданий спочатку

Контраваріантність: дозволяє використовувати більш універсальний тип, ніж заданий спочатку

Інваріантність: дозволяє використовувати тільки заданий тип

C# дозволяє створювати коваріантні та контраваріантні узагальнені інтерфейси. Ця функціональність підвищує гнучкість під час використання узагальнених інтерфейсів у програмі. За умовчанням усі узагальнені інтерфейси є інваріантними.

Для розгляду коваріантних та контраваріантних інтерфейсів візьмемо такі класи:

```csharp
class Message
{
    public string Text { get; set; }
    public Message(string text) => Text = text;
}
class EmailMessage : Message
{
    public EmailMessage(string text): base(text) { }
}
```
Тут визначено клас повідомлення Message, який отримує через конструктор текст і зберігає його як Text. А клас EmailMessage представляє умовне email-повідомлення та просто викликає конструктор базового класу, передаючи йому текст повідомлення.

### Коваріантні інтерфейси

Узагальнені інтерфейси можуть бути коваріантними, якщо до універсального параметра застосовується ключове слово out. Такий параметр повинен представляти тип об'єкта, який повертається методом. Наприклад:

```csharp
interface IMessenger<out T>
{
    T WriteMessage(string text);
}
class EmailMessenger : IMessenger<EmailMessage>
{
    public EmailMessage WriteMessage(string text)
    {
        return new EmailMessage($"Email: {text}");
    }
}
```
Тут узагальнений інтерфейс IMessenger представляє інтерфейс месенджера та визначає метод WriteMessage() створення повідомлення. При цьому на момент визначення інтерфейсу ми не знаємо, об'єкт якого типу повертатиметься у цьому методі. Ключове слово out у визначенні інтерфейсу показує, що цей інтерфейс буде коваріантним.

Клас EmailMessenger, який представляє умовну програму для відправки email-повідомлень, реалізує цей інтерфейс та повертає з методу WriteMessage() об'єкт EmailMessage.

Застосуємо ці типи в програмі:

```csharp
IMessenger<Message> outlook = new EmailMessenger();
Message message = outlook.WriteMessage("Hello World");
Console.WriteLine(message.Text); // Email: Hello World
IMessenger<EmailMessage> emailClient = new EmailMessenger();
IMessenger<Message> messenger = emailClient;
Message emailMessage = messenger.WriteMessage("Hi!");
Console.WriteLine(emailMessage.Text); // Email: Hi!
```
Тобто ми можемо надати більш загальному типу IMessenger<Message> об'єкт більш конкретного типу EmailMessenger або IMessenger<EmailMessage>.

У той же час, якби ми не використовували ключове слово out:

```csharp
interface IMessenger<T>
```
то ми зіткнулися б з помилкою у рядку

```csharp
IMessenger<Message> outlook = new EmailMessenger(); // ! помилка
IMessenger<EmailMessage> emailClient = new EmailMessenger();
IMessenger<Message> messenger = emailClient; // ! помилка
```
Оскільки в цьому випадку неможливо було б привести об'єкт IMessenger<EmailMessage> до типу IMessenger<Message>.

При створенні коваріантного інтерфейсу треба враховувати, що універсальний параметр може використовуватися тільки як тип значення, що повертається методами інтерфейсу. Але не може використовуватися як тип аргументів методу або обмеження методів інтерфейсу.

### Контраваріантні інтерфейси

Для створення контраваріантного інтерфейсу слід використовувати ключове слово in. Наприклад, візьмемо ті самі класи Message та EmailMessage та визначимо такі типи:

```csharp
interface IMessenger<in T>
{
    void SendMessage(T message);
}
class SimpleMessenger : IMessenger<Message>
{
    public void SendMessage(Message message)
    {
        Console.WriteLine($"Відправляється повідомлення: {message.Text}");
    }
}
```
Тут знову ж таки інтерфейс IMessenger представляє інтерфейс месенджера і визначає метод SendMessage() для відправки умовного повідомлення. Ключове слово in у визначенні інтерфейсу показує, що цей інтерфейс є контраваріантним.

Клас SimpleMessenger представляє умовну програму надсилання повідомлень та реалізує цей інтерфейс. Причому як тип використовуваного цей клас використовує тип Message. Тобто SimpleMessenger фактично представляє тип IMessenger<Message>.

Застосуємо ці типи у програмі:

```csharp
IMessenger<EmailMessage> outlook = new SimpleMessenger();
outlook.SendMessage(new EmailMessage("Hi!"));
IMessenger<Message> telegram = new SimpleMessenger();
IMessenger<EmailMessage> emailClient = telegram;
emailClient.SendMessage(new EmailMessage("Hello"));
```
Оскільки інтерфейс IMessenger використовує універсальний параметр із ключовим словом in, він є контраваріантним, у коді ми можемо змінній типу IMessenger<EmailMessage> передати об'єкт IMessenger<Message> чи SimpleMessenger.

Якби ключове слово in не використовувалося б, ми не змогли б це зробити. Тобто об'єкт інтерфейсу з універсальним типом наводиться до об'єкта інтерфейсу з більш конкретним типом.

При створенні контраваріантного інтерфейсу треба враховувати, що універсальний параметр контраваріантного типу може застосовуватися тільки до аргументів методу, але не може застосовуватися до результату методу, що повертається.

### Поєднання коваріантності та контраваріантності

Також ми можемо поєднати коваріантність та контраваріантність в одному інтерфейсі. Наприклад:

```csharp
interface IMessenger<in T, out K>
{
    void SendMessage(T message);
    K WriteMessage(string text);
}
class SimpleMessenger : IMessenger<Message, EmailMessage>
{
    public void SendMessage(Message message)
    {
        Console.WriteLine($"Відправляється повідомлення: {message.Text}");
    }
    public EmailMessage WriteMessage(string text)
    {
        return new EmailMessage($"Email: {text}");
    }
}
```
Фактично тут об'єднано два попередні приклади. Завдяки коваріантності/контраваріантності об'єкт класу SimpleMessenger може представляти типи

```csharp
IMessenger<EmailMessage, Message>,
IMessenger<Message, EmailMessage>,
IMessenger<Message, Message>,
IMessenger<EmailMessage, EmailMessage>.
```
Застосування класів:

```csharp
IMessenger<EmailMessage, Message> messenger = new SimpleMessenger();
Message message = messenger.WriteMessage("Hello World");
Console.WriteLine(message.Text);
messenger.SendMessage(new EmailMessage("Test"));
IMessenger<EmailMessage, EmailMessage> outlook = new SimpleMessenger();
EmailMessage emailMessage = outlook.WriteMessage("Message from Outlook");
outlook.SendMessage(emailMessage);
IMessenger<Message, Message> telegram = new SimpleMessenger();
Message simpleMessage = telegram.WriteMessage("Message from Telegram");
telegram.SendMessage(simpleMessage);
```
