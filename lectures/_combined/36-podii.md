
## 6.3. Події

Події сигналізують системі про те, що сталася певна дія. І якщо нам треба відстежити ці дії, то ми можемо застосовувати події.

Наприклад, візьмемо наступний клас, який описує банківський рахунок:

```csharp
class Account
{
    // сума на рахунку
    public int Sum { get; private set; }
    // у конструкторі встановлюємо початкову суму на рахунку
    public Account(int sum) => Sum = sum;
    // додавання коштів на рахунок
    public void Put(int sum) => Sum += sum;
    // списання коштів з рахунку
    public void Take(int sum)
    {
        if (Sum >= sum)
        {
            Sum -= sum;
        }
    }
}
```

У конструкторі встановлюємо початкову суму, що зберігається як Sum. За допомогою методу Put ми можемо додати кошти на рахунок, а за допомогою методу Take навпаки зняти гроші з рахунку. Спробуємо використовувати клас у програмі – створити рахунок, покласти та зняти з нього гроші:

```csharp
Account account = new Account(100);
account.Put(20); // додаємо на рахунок 20
Console.WriteLine($"Сума на рахунку: {account.Sum}");
account.Take(70); // намагаємося зняти з рахунку 70
Console.WriteLine($"Сума на рахунку: {account.Sum}");
account.Take(180); // намагаємося зняти з рахунку 180
Console.WriteLine($"Сума на рахунку: {account.Sum}");
```

Усі операції працюють як і належить. Але якщо ми хочемо повідомляти користувача про результати його операцій. Ми могли б, наприклад, змінити метод Put таким чином:

```csharp
public void Put(int sum)
{
    Sum += sum;
    Console.WriteLine($"На рахунок надійшло: {sum}");
}
```

Здавалося, тепер ми будемо сповіщені про операцію, побачивши відповідне повідомлення на консолі. Але тут є низка зауважень. На момент визначення класу ми можемо точно не знати, яку дію ми хочемо зробити у методі Put у відповідь на додавання грошей. Це може бути виведення на консоль, а можливо ми захочемо повідомити користувача по email або sms. Більше того, ми можемо створити окрему бібліотеку класів, яка міститиме цей клас, і додаватиме її до інших проектів. І вже із цих проектів вирішувати, яка дія має виконуватися. Можливо, ми захочемо використовувати клас Account у графічній програмі та виводити при додаванні на рахунок у графічному повідомленні, а не консоль. Або нашу бібліотеку класів буде використовувати інший розробник, який має свою думку, що саме робити при додаванні на рахунок. І ці питання ми можемо вирішити, використовуючи події.

### Визначення та виклик подій

Події оголошуються в класі за допомогою ключового слова event, після якого вказується тип делегата, який представляє подію:

```csharp
delegate void AccountHandler(string message);
event AccountHandler Notify;
```

У разі спочатку визначається делегат AccountHandler, який приймає один параметр типу string. Потім за допомогою ключового слова event визначається подія з ім'ям Notify, яку представляє делегат AccountHandler. Назва для події може бути довільною, але в будь-якому випадку вона має представляти певний делегат.

Визначивши подію, ми можемо її викликати у програмі як метод, використовуючи ім'я події:

```csharp
Notify("Сталася дія");
```

Оскільки подію Notify представляє делегат AccountHandler, який приймає один параметр типу string - рядок, то при виклику події нам треба передати в нього рядок.

Однак при виклику подій ми можемо зіткнутися з тим, що подія дорівнює null у випадку, якщо для неї не визначено обробника. Тому при виклику події краще його завжди перевіряти на null. Наприклад, так:

```csharp
if (Notify !=null) Notify("Сталася дія");
```

Або так:

```csharp
Notify?.Invoke("Сталася дія");
```

У цьому випадку оскільки подія представляє делегат, ми можемо його викликати за допомогою методу Invoke(), передавши в нього необхідні значення для параметрів.

Об'єднаємо всі разом і створимо та викликаємо подію:

```csharp
class Account
{
    public delegate void AccountHandler(string message);
    public event AccountHandler? Notify; // 1.Визначення події
    public Account(int sum) => Sum = sum;
    public int Sum { get; private set; }
    public void Put(int sum)
    {
        Sum += sum;
        Notify?.Invoke($"На рахунок надійшло: {sum}"); // 2.Виклик події
    }
    public void Take(int sum)
    {
        if (Sum >= sum)
        {
            Sum -= sum;
            Notify?.Invoke($"З рахунку знято: {sum}"); // 3.Виклик події
        }
        else
        {
            Notify?.Invoke($"Недостатньо грошей на рахунку. Поточний баланс: {Sum}"); ;
        }
    }
}
```

Тепер за допомогою події Notify ми повідомляємо систему про те, що були додані кошти та про те, що кошти знято з рахунку або на рахунку недостатньо коштів.

### Додавання обробника події

З подією може бути пов'язаний один або кілька обробників. Обробники подій - це саме те, що виконується під час виклику подій. Нерідко як обробники подій застосовуються методи. Кожен обробник подій за списком параметрів і типу, що повертається, повинен відповідати делегату, який представляє подію. Для додавання обробника події застосовується операція +=:

```csharp
Notify += обробник події;
```

Визначимо обробники для події Notify, щоб отримати у програмі потрібні повідомлення:

```csharp
Account account = new Account(100);
account.Notify += DisplayMessage; // Додаємо обробник для події
account.Put(20); // додаємо на рахунок 20
Console.WriteLine($"Сума на рахунку: {account.Sum}");
account.Take(70); // намагаємося зняти з рахунку 70
Console.WriteLine($"Сума на рахунку: {account.Sum}");
account.Take(180); // намагаємося зняти з рахунку 180
Console.WriteLine($"Сума на рахунку: {account.Sum}");
void DisplayMessage(string message) => Console.WriteLine(message);
```

В даному випадку як обробник використовується метод DisplayMessage, який відповідає за списком параметрів і типу делегату AccountHandler, що повертається. У результаті при виклику події Notify?.Invoke() буде викликатися метод DisplayMessage, якому для параметра message буде передаватися рядок, який передається в Notify.Invoke(). У DisplayMessage просто виводимо отримане від події повідомлення, але можна визначити будь-яку логіку.

Якби в даному випадку обробник не був би встановлений, то при виклику події Notify?.Invoke() нічого не відбувалося, оскільки подія Notify була б null.

Тепер ми можемо виділити клас Account в окрему бібліотеку класів та додавати до будь-якого проекту.

### Додавання та видалення обробників

Для однієї події можна встановити кілька обробників і потім у будь-який момент їх видалити. Для видалення обробників використовується операція -=. Наприклад:

```csharp
Account account = new Account(100);
account.Notify += DisplayMessage; // додаємо обробник DisplayMessage
account.Notify += DisplayRedMessage; // додаємо обробник DisplayRedMessage
account.Put(20); // додаємо на рахунок 20
account.Notify -= DisplayRedMessage; // видаляємо обробник DisplayRedMessage
account.Put(50); // додаємо на рахунок 50
void DisplayMessage(string message) => Console.WriteLine(message);
void DisplayRedMessage(string message)
{
    // Встановлюємо червоний колір символів
    Console.ForegroundColor = ConsoleColor.Red;
    Console.WriteLine(message);
    // Скидаємо налаштування кольору
    Console.ResetColor();
}
```

Як обробників можуть використовуватися не тільки звичайні методи, але також делегати, анонімні методи та лямбда-вирази. Використання делегатів та методів:

```csharp
Account acc = new Account(100);
// встановлення делегата, який вказує на метод DisplayMessage
acc.Notify += new Account.AccountHandler(DisplayMessage);
// установка як обробник методу DisplayMessage
acc.Notify += DisplayMessage; // додаємо обробник DisplayMessag
acc.Put(20); // додаємо на рахунок 20
void DisplayMessage(string message) => Console.WriteLine(message);
```

У цьому випадку різниці між двома обробниками ніякої не буде.

Встановлення як обробника анонімного методу:

```csharp
Account acc = new Account(100);
acc.Notify += delegate (string mes)
{
    Console.WriteLine(mes);
};
acc.Put(20);
```

Встановлення як обробника лямбда-виразу:

```csharp
Account account = new Account(100);
account.Notify += message => Console.WriteLine(message);
account.Put(20);
```

### Управління обробниками

За допомогою спеціальних аксесорів add/remove ми можемо керувати додаванням та видаленням обробників. Як правило, подібна функціональність рідко потрібна, проте ми її можемо використовувати. Наприклад:

```csharp
class Account
{
    public delegate void AccountHandler(string message);
    AccountHandler? notify;
    public event AccountHandler Notify
    {
        add
        {
            notify += value;
            Console.WriteLine($"{value.Method.Name} доданий");
        }
        remove
        {
            notify -= value;
            Console.WriteLine($"{value.Method.Name} видалено");
        }
    }

    public Account(int sum) => Sum = sum;
    public int Sum { get; private set; }

    public void Put(int sum)
    {
        Sum += sum;
        notify?.Invoke($"На рахунок надійшло: {sum}"); // 2. Виклик події
    }

    public void Take(int sum)
    {
        if (Sum >= sum)
        {
            Sum -= sum;
            notify?.Invoke($"З рахунку знято: {sum}"); // 2. Виклик події
        }
        else
        {
            notify?.Invoke($"Недостатньо грошей на рахунку. Поточний баланс: {Sum}");
        }
    }
}
```

Тепер визначення події розбивається на дві частини. Спочатку просто визначається змінна делегата, якою ми можемо викликати пов'язані обробники:

```csharp
AccountHandler notify;
```

У другій частині визначаємо аксесуари add і remove. Аксесор add викликається при додаванні обробника, тобто під час операції +=. Обробник, що додається, доступний через ключове слово value. Тут ми можемо отримати інформацію про обробника (наприклад, ім'я методу через value.Method.Name) та визначити деяку логіку. В даному випадку для простоти просто виводиться повідомлення на консоль:

```csharp
add
{
    notify += value;
    Console.WriteLine($"{value.Method.Name} доданий");
}
```

Блок remove викликається при видаленні обробника. Аналогічно тут можна задати деяку додаткову логіку:

```csharp
remove
{
    notify -= value;
    Console.WriteLine($"{value.Method.Name} видалено");
}
```

Всередині класу подія викликається також через змінну notify. Але для додавання та видалення обробників у програмі використовується якраз Notify:

```csharp
Account acc = new Account(100);
acc.Notify += DisplayMessage; // додаємо обробник DisplayMessage
acc.Put(20); // додаємо на рахунок 20
acc.Notify -= DisplayMessage; // видаляємо обробник DisplayMessage
acc.Put(20); // додаємо на рахунок 20
void DisplayMessage(string message) => Console.WriteLine(message);
```

### Передача даних події

Нерідко при події обробнику події потрібно передати деяку інформацію про подію. Наприклад, додамо і до нашої програми новий клас AccountEventArgs з наступним кодом:

```csharp
class AccountEventArgs
{
    // Повідомлення
    public string Message{get;}
    // Сума, на яку змінився рахунок
    public int Sum {get;}
    public AccountEventArgs(string message, int sum)
    {
        Message = message;
        Sum = sum;
    }
}
```

Даний клас має дві властивості: Message - для зберігання повідомлення, що виводиться, і Sum - для зберігання суми, на яку змінився рахунок.

Тепер застосуємо клас AccoutEventArgs, змінивши клас Account таким чином:

```csharp
class Account
{
    public delegate void AccountHandler(Account sender, AccountEventArgs e);
    public event AccountHandler? Notify;
    public int Sum { get; private set; }
    public Account(int sum) => Sum = sum;
    public void Put(int sum)
    {
        Sum += sum;
        Notify?.Invoke(this, new AccountEventArgs($"На рахунок надійшло {sum}", sum));
    }
    public void Take(int sum)
    {
        if (Sum >= sum)
        {
            Sum -= sum;
            Notify?.Invoke(this, new AccountEventArgs($"Суму {sum} знято з рахунку", sum));
        }
        else
        {
            Notify?.Invoke(this, new AccountEventArgs("Недостатньо грошей на рахунку", sum));
        }
    }
}
```

Порівняно з попередньою версією класу Account тут змінилася лише кількість параметрів у делегата і кількість параметрів під час виклику події. Тепер делегат AccountHandler як перший параметр приймає об'єкт, який викликав подію, тобто поточний об'єкт Account. А як другий параметр приймає об'єкт AccountEventArgs, який зберігає інформацію про подію, що отримується через конструктор.

Тепер змінимо основну програму:

```csharp
Account acc = new Account(100);
acc.Notify += DisplayMessage;
acc.Put(20);
acc.Take(70);
acc.Take(150);
void DisplayMessage(Account sender, AccountEventArgs e)
{
    Console.WriteLine($"Сума транзакції: {e.Sum}");
    Console.WriteLine(e.Message);
    Console.WriteLine($"Поточна сума на рахунку: {sender.Sum}");
}
```

Порівняно з попереднім варіантом, тут ми тільки змінюємо кількість параметрів та їх використання в обробнику DisplayMessage. Завдяки першому параметру в методі можна отримати інформацію про відправника події - рахунок, з яким здійснюється операція. А через другий параметр можна отримати інформацію про стан операції.

