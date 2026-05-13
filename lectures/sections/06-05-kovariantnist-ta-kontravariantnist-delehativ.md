---
chapter: 6
chapterTitle: "Розділ 6. Делегати, події та лямбди"
section: 5
number: "6.5"
title: "Коваріантність та контраваріантність делегатів"
source: "../_combined/37-kovariantnist-ta-kontravariantnist-delehativ.md"
---

## 6.5. Коваріантність та контраваріантність делегатів

Делегати можуть бути коваріантними та контраваріантними. Коваріантність делегата передбачає, що типом, що повертається, може бути похідний тип. Контраваріантність делегата передбачає, що тип параметра може бути більш універсальний тип.

Розглянемо коваріантність та контраваріантність на прикладі наступних класів:

```csharp
class Message
{
    public string Text { get; }
    public Message(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Message: {Text}");
}
class EmailMessage : Message
{
    public EmailMessage(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}
class SmsMessage : Message
{
    public SmsMessage(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Sms: {Text}");
}
```

В даному випадку клас Message представляє деяке повідомлення та визначає властивість Text для зберігання тексту повідомлення, що встановлюється через конструктор. А в методі Print повідомлення виводиться на консоль. Клас EmailMessage представляє email-повідомлення, а SmsMessage - смс-повідомлення, і обидва класи є похідними від Message.

### Коваріантність

Коваріантність дозволяє передати делегату метод, тип якого є похідним від типу, що повертається делегатом. Тобто якщо тип делегата, що повертається, Message, то метод може мати як повертаний тип клас EmailMessage:

```csharp
// делегату з базовим типом передаємо метод із похідним типом
MessageBuilder messageBuilder = WriteEmailMessage; // коваріантність
Message message = messageBuilder("Hello");
message.Print(); // Email: Hello
EmailMessage WriteEmailMessage(string text) => new EmailMessage(text);
delegate Message MessageBuilder(string text);
```

Тут делегат MessageBuilder повертає об'єкт Message. Однак завдяки коваріантності цей делегат може вказувати на метод, який повертає об'єкт похідного типу, наприклад, на метод WriteEmailMessage.

### Контраваріантність

Контраваріантність дозволяє надати делегату метод, тип параметра якого є більш універсальним по відношенню до типу параметра делегата. Наприклад, візьмемо вище визначені класи Message та EmailMessage та використовуємо їх у наступному прикладі:

```csharp
// делегату з похідним типом передаємо метод із базовим типом
EmailReceiver emailBox = ReceiveMessage; // контраваріантність
emailBox(new EmailMessage("Welcome")); // Email: Welcome
void ReceiveMessage(Message message) => message.Print();
delegate void EmailReceiver(EmailMessage message);
```

Незважаючи на те, що делегат як параметр приймає об'єкт EmailMessage, йому можна надати метод, у якого параметр представляє базовий тип Message. Може здатися на перший погляд, що тут є певна суперечність, тобто використання більш універсального типу замість більш похідного. Однак насправді в делегат при його виклику ми все одно можемо передати лише об'єкти типу EmailMessage, а будь-який об'єкт типу EmailMessage є об'єктом типу Message, який використовується у методі.

### Коваріантність та контраваріантність в узагальнених делегатах

Узагальнені делегати також можуть бути коваріантними та контраваріантними, що дає нам більше гнучкості в їх використанні.

Коваріантність

Наприклад, оголосимо та використовуємо коваріантний узагальнений делегат:

```csharp
// повертає EmailMessage – більш конкретний тип
MessageBuilder<EmailMessage> EmailMessageWriter = (string text) => new EmailMessage(text);
//повертає загальний тип Message
MessageBuilder<Message> messageBuilder = EmailMessageWriter; // коварiантнiсть
Message message = messageBuilder("hello Tom"); //виклик делегата
message.Print(); // Email: hello Tom
delegate T MessageBuilder<out T>(string text);
```

Завдяки використанню out ми можемо привласнити делегату типу MessageBuilder<Message> (загальний тип) делегат типу MessageBuilder<EmailMessage> (конкретніший тип).

Контраваріантність

Розглянемо контраваріантний узагальнений делегат:

```csharp
// приймає об'єкт більш загального типу
MessageReceiver<Message> messageReceiver = (Message message) => message.Print();
// приймає об'єкт більш конкретного типу
MessageReceiver<EmailMessage> emailMessageReceiver = messageReceiver;
// контраваріантність
messageReceiver(new Message("Hello World!"));
// Message: Hello World!
messageReceiver(new EmailMessage("Hello World!"));
// Email: Hello World!
delegate void MessageReceiver<in T>(T message);
```

Використання ключового слова in дозволяє присвоїти делегату з похідним типом (MessageReceiver<EmailMessage>) делегат із базовим типом (MessageReceiver<Message>).

Як і у випадку з узагальненими інтерфейсами, параметр коваріантного типу застосовується тільки до типу значення, що повертається делегатом. А параметр контраваріантного типу застосовується лише до параметрів делегату.

Тобто, якщо грубо узагальнити, коваріантність - це від більш похідного до більш загального типу (EmailMessage -> Message), а контраваріантність - від більш загального до більш похідного типу (Message -> EmailMessage).

### Поєднання коваріантності та контраваріантності

Причому делегат може однозначно використовувати обидва оператори: in і out. Наприклад:

```csharp
MessageConverter<Message, EmailMessage> toEmailConverter = (Message message) => new EmailMessage(message.Text);
MessageConverter<SmsMessage, Message> converter = toEmailConverter;
Message message = converter(new SmsMessage("Hello work"));
message.Print(); // Email: Hello work
delegate E MessageConverter<in M, out E>(M message);
```

Тут делегат MessageConverter представляє умовну дію, що конвертує об'єкт типу M у тип E.

У програмі визначена змінна converter, яка представляє тип MessageConverter <SmsMessage, Message> - тобто конвертер з типу SmsMessage у будь-який тип Message, грубо кажучи перетворює смс на будь-який інший тип повідомлення.

Цією змінною можна передати дію - на EmailConverter, яке з повідомлень будь-якого типу створює об'єкт Email-повідомлення. Тут застосовується контраваріантність: для параметра замість похідного типу SmsMessage використовується базовий тип Message. І також є коваріантність: замість типу Message, що повертається, використовується похідний тип EmailMessage.
