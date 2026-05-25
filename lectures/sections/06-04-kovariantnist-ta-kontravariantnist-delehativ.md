---
chapter: 6
chapterTitle: "Розділ 6. Делегати, події та лямбди"
section: 4
number: "6.4"
title: "Коваріантність та контраваріантність делегатів"
source: "../_migration/source-chunks/37-kovariantnist-ta-kontravariantnist-delehativ.md"
---

## 6.4. Коваріантність та контраваріантність делегатів

Коваріантність і контраваріантність описують, як делегати взаємодіють зі спадкуванням типів. Вони дозволяють присвоювати делегату метод, сигнатура якого не збігається з делегатом точно, але є сумісною через ієрархію класів. Це підвищує гнучкість коду: замість того щоб оголошувати окремий делегат для кожного типу ієрархії, можна використати один делегат для роботи з базовим або похідним типом.

- **Коваріантність** стосується типу, що **повертається**: метод може повертати більш похідний (конкретніший) тип, ніж оголошено в делегаті.
- **Контраваріантність** стосується **параметрів**: метод може приймати більш загальний (базовий) тип, ніж оголошено в делегаті.

Розглянемо ці поняття на прикладі ієрархії класів медичних сповіщень:

```csharp run
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}

class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}

class SmsNotification : Notification
{
    public SmsNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"SMS: {Text}");
}

// просто перевіряємо ієрархію
Notification n = new EmailNotification("Результати аналізів готові");
n.Print();
n = new SmsNotification("Прийом завтра о 10:00");
n.Print();
```

Клас `Notification` — базовий для всіх типів сповіщень. `EmailNotification` і `SmsNotification` — похідні класи, кожен з яких перевизначає метод `Print`.

## Коваріантність

Коваріантність дозволяє передати делегату метод, тип якого, що **повертається**, є **похідним** від типу, що повертається делегатом. Якщо делегат оголошує повернення `Notification`, то метод може повертати `EmailNotification`:

```csharp run
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}
class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}

// делегат повертає базовий тип Notification
delegate Notification NotificationBuilder(string text);

// метод повертає похідний тип EmailNotification — коваріантність
NotificationBuilder builder = CreateEmail;

Notification result = builder("Аналізи пацієнта Петренка готові");
result.Print(); // Email: ...

EmailNotification CreateEmail(string text) => new EmailNotification(text);
```

Компілятор дозволяє це, бо будь-який об'єкт `EmailNotification` є водночас об'єктом `Notification` — відносини «є» (is-a). Якщо делегат очікує `Notification`, метод, що повертає `EmailNotification`, завжди задовольняє цю вимогу.

## Контраваріантність

Контраваріантність дозволяє передати делегату метод, тип **параметра** якого є **базовим** по відношенню до типу параметра делегата. Якщо делегат оголошує параметр `EmailNotification`, то метод може приймати `Notification`:

```csharp run
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}
class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}

// делегат приймає похідний тип EmailNotification
delegate void EmailReceiver(EmailNotification notification);

// метод приймає базовий тип Notification — контраваріантність
EmailReceiver receiver = ProcessNotification;
receiver(new EmailNotification("Прийом лікаря підтверджено"));

void ProcessNotification(Notification n) => n.Print();
```

На перший погляд це може здатися суперечливим: делегат оголошує `EmailNotification`, а метод приймає `Notification`. Але логіка правильна: при виклику `receiver(...)` ми завжди передаємо `EmailNotification`. Будь-який `EmailNotification` є `Notification`, тому метод `ProcessNotification(Notification n)` коректно обробить його. Метод з ширшим типом параметра — більш гнучкий, і все, що він може зробити з `Notification`, він зможе зробити і з `EmailNotification`.

![Коваріантність і контраваріантність делегатів](_assets/06-04/covariance-contravariance.png)

## Коваріантність та контраваріантність в узагальнених делегатах

Узагальнені делегати також підтримують коваріантність і контраваріантність — через ключові слова `out` і `in` у параметрах типу.

### Коваріантний узагальнений делегат (out)

Ключове слово `out` у параметрі типу означає, що цей тип використовується лише як **тип, що повертається**. Завдяки цьому делегат із більш конкретним типом можна присвоїти змінній делегата з більш загальним типом:

```csharp run
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}
class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}

delegate T NotificationBuilder<out T>(string text);

// повертає EmailNotification — більш конкретний тип
NotificationBuilder<EmailNotification> emailBuilder = text => new EmailNotification(text);

// завдяки out — можна присвоїти делегату з базовим типом
NotificationBuilder<Notification> generalBuilder = emailBuilder; // коваріантність

Notification n = generalBuilder("Результати МРТ");
n.Print(); // Email: Результати МРТ
```

Без `out` компілятор заборонив би таке присвоєння, навіть попри те, що `EmailNotification` є `Notification`.

### Контраваріантний узагальнений делегат (in)

Ключове слово `in` означає, що параметр типу використовується лише як **тип параметра** делегата. Завдяки цьому делегат із більш загальним типом можна присвоїти змінній делегата з більш конкретним типом:

```csharp run
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}
class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}

delegate void NotificationReceiver<in T>(T notification);

// приймає базовий тип Notification
NotificationReceiver<Notification> generalReceiver = n => n.Print();

// завдяки in — можна присвоїти делегату з похідним типом
NotificationReceiver<EmailNotification> emailReceiver = generalReceiver; // контраваріантність

generalReceiver(new Notification("Загальне повідомлення"));     // Сповіщення: ...
generalReceiver(new EmailNotification("Результати аналізів"));  // Email: ...
emailReceiver(new EmailNotification("Прийом підтверджено"));    // Email: ...
```

Як і у випадку з узагальненими інтерфейсами: параметр коваріантного типу (`out`) застосовується лише до типу, що повертається, а параметр контраваріантного типу (`in`) — лише до параметрів делегата.

## Поєднання коваріантності та контраваріантності

Один узагальнений делегат може одночасно використовувати обидва оператори — `in` для параметра і `out` для типу, що повертається:

```csharp run
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}
class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}
class SmsNotification : Notification
{
    public SmsNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"SMS: {Text}");
}

// конвертер: приймає тип M, повертає тип E
delegate E NotificationConverter<in M, out E>(M source);

// конвертер: з будь-якого Notification створює EmailNotification
NotificationConverter<Notification, EmailNotification> toEmail =
    n => new EmailNotification($"[Email] {n.Text}");

// контраваріантність по M: SmsNotification → Notification (ширший тип)
// коваріантність по E:     EmailNotification → Notification (ширший тип)
NotificationConverter<SmsNotification, Notification> converter = toEmail;

Notification result = converter(new SmsNotification("Аналіз крові"));
result.Print(); // Email: [Email] Аналіз крові
```

Тут делегат `converter` очікує: взяти `SmsNotification` і повернути `Notification`. Ми присвоїли йому `toEmail`, який бере будь-який `Notification` і повертає `EmailNotification`. Контраваріантність по `M` означає: `SmsNotification` → `Notification` (параметр стає ширшим). Коваріантність по `E` означає: `EmailNotification` → `Notification` (тип повернення стає ширшим). Обидві заміни безпечні, і компілятор це перевіряє статично.

Якщо узагальнити: **коваріантність** — від більш похідного до більш загального типу (`EmailNotification → Notification`), **контраваріантність** — від більш загального до більш похідного (`Notification → EmailNotification`).

![Коваріантність та контраваріантність: напрямки заміни типів](_assets/06-04/variance-directions.png)
