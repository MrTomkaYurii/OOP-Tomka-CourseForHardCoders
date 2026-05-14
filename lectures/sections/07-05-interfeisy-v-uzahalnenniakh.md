---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 5
number: "7.5"
title: "Інтерфейси в узагальненнях"
source: "../_combined/43-interfeisy-v-uzahalnenniakh.md"
---

## 7.5. Інтерфейси в узагальненнях

### Інтерфейси як обмеження узагальнень

Інтерфейси можуть виступати як обмеження узагальнень. При цьому якщо як обмеження можна вказати лише один клас, то інтерфейсів можна вказати кілька.

Припустимо, у нас є такі інтерфейси та клас, який їх реалізує:

```csharp
interface IMessage
{
    string Text { get; } // текст повідомлення
}
interface IPrintable
{
    void Print();
}
class Message : IMessage, IPrintable
{
    public string Text { get; }
    public Message(string text) => Text = text;
    public void Print() => Console.WriteLine(Text);
}
```
Інтерфейс IMessage представляє інтерфейс повідомлення та визначає властивість Text для зберігання тексту повідомлення. Інтерфейс IPrintable визначає метод Print для умовного друку повідомлення. І безпосередньо клас повідомлення – клас Message реалізує ці інтерфейси.

Використовуємо перераховані вище інтерфейси як обмеження узагальненого класу:

```csharp
class Messenger<T> where T: IMessage, IPrintable
{
    public void Send(T message)
    {
        Console.WriteLine("Відправка повідомлення:");
        message.Print();
    }
}
```
В даному випадку клас умовного месенджера використовує параметр T - тип, який реалізує відразу два інтерфейси IMessage та IPrintable. Наприклад, вище визначено клас Message, який реалізує обидва інтерфейси, тому ми можемо типом Message типізувати об'єкти Messenger:

```csharp
// створюємо месенджер
var telegram = new Messenger<Message>();
// створюємо повідомлення
var message = new Message("Hello World!");
// надсилаємо повідомлення
telegram.Send(message);
```
Також параметр T може представляти інтерфейс, який успадковується від обох інтерфейсів:

```csharp
interface IPrintableMessage : IPrintable, IMessage { }
class PrintableMessage : IPrintableMessage
{
    public string Text { get; }
    public PrintableMessage(string text) => Text = text;
    public void Print() => Console.WriteLine(Text);
}
```
У цьому випадку об'єкти Messenger ми можемо типізувати типом IPrintableMessage:

```csharp
var telegram = new Messenger<IPrintableMessage>();
var message = new PrintableMessage("Hello World!");
telegram.Send(message);
```
### Узагальнені інтерфейси

Як і класи, інтерфейси можуть бути узагальненими:

```csharp
interface IUser<T>
{
    T Id { get; }
}
class User<T> : IUser<T>
{
    public T Id { get; }
    public User(T id) => Id = id;
}
```
Інтерфейс IUser типізований параметром T, який під час реалізації інтерфейсу використовується у класі User. Зокрема, змінна _id визначена як T, що дозволяє використовувати для id різні типи.

Визначимо дві реалізації: одна як параметр використовуватиме тип int, а інша - тип string:

```csharp
IUser<int> user1 = new User<int>(6789);
Console.WriteLine(user1.Id); // 6789
IUser<string> user2 = new User<string>("12345");
Console.WriteLine(user2.Id); // 12345
```
Також при реалізації інтерфейсу ми можемо явно вказати, який тип буде використовуватися для параметра T:

```csharp
class IntUser : IUser<int>
{
    public int Id { get; }
    public IntUser(int id) => Id = id;
}
```
Застосування:

```csharp
IUser<int> user1 = new IntUser(2345);
Console.WriteLine(user1.Id); // 2345
IntUser user2 = new IntUser(9840);
Console.WriteLine(user2.Id); // 9840
```
