---
chapter: 6
chapterTitle: "Розділ 6. Делегати, події та лямбди"
section: 1
number: "6.1"
title: "Делегати"
source: "../_combined/34-delehaty.md"
---

## 6.1. Делегати

Делегати репрезентують такі об'єкти, які вказують на методи. Тобто делегати – це покажчики на методи і за допомогою делегатів ми можемо викликати ці методи.

### Визначення делегатів

Для оголошення делегата використовується ключове слово delegate, після якого йде тип, назва і параметри, що повертається. Наприклад:

```csharp
delegate void Message();
```

Делегат Message як тип, що повертається, має тип void (тобто нічого не повертає) і не приймає жодних параметрів. Це означає, що цей делегат може вказувати на будь-який метод, який не приймає жодних параметрів та нічого не повертає.

Розглянемо застосування цього делегата:

```csharp
Message mes; // 2. Створюємо змінну делегата
mes = Hello; // 3. Присвоюємо цій змінній адресу методу
mes(); // 4. Викликаємо метод
void Hello() => Console.WriteLine("Hello METANIT.COM");
delegate void Message(); // 1. Оголошуємо делегат
```

Насамперед спочатку необхідно визначити сам делегат:

```csharp
delegate void Message(); // 1. Оголошуємо делегат
```

Для використання делегата оголошується змінна цього делегата:

```csharp
Message mes; // 2. Створюємо змінну делегата
```

Далі делегат передається адресу певного методу (у нашому випадку методу Hello). Зверніть увагу, що даний метод має той же тип, що повертається, і той же набір параметрів (в даному випадку відсутність параметрів), що і делегат.

```csharp
mes = Hello; // 3. Присвоюємо цій змінній адресу методу
```

Потім через делегат викликаємо метод, який посилається даний делегат:

```csharp
mes(); // 4. Викликаємо метод
```

Виклик делегата здійснюється подібно до виклику методу.

При цьому делегати необов'язково можуть вказувати лише на методи, які визначені в тому класі, де визначена змінна делегата. Це можуть бути також методи інших класів і структур.

```csharp
Message message1 = Welcome.Print;
Message message2 = new Hello().Display;
message1(); // Welcome
message2(); // Привіт
delegate void Message();
class Welcome
{
    public static void Print() => Console.WriteLine("Welcome");
}
class Hello
{
    public void Display() => Console.WriteLine("Привіт");
}
```

### Місце визначення делегата

Якщо ми визначаємо делегат у програмах верхнього рівня (top-level program), яку за умовчанням представляє файл Program.cs, починаючи з версії C# 10, як у прикладі вище, то, як і інші типи, делегат визначається наприкінці коду. Але в принципі делегат можна визначати всередині класу:

```csharp
class Program
{
    delegate void Message(); // 1. Оголошуємо делегат
    static void Main()
    {
        Message mes; // 2. Створюємо змінну делегата
        mes = Hello; // 3. Присвоюємо цій змінній адресу методу
        mes(); // 4. Викликаємо метод
        void Hello() => Console.WriteLine("Hello METANIT.COM");
    }
}
```

Або поза класом:

```csharp
delegate void Message(); // 1. Оголошуємо делегат
class Program
{
    static void Main()
    {
        Message mes; // 2. Створюємо змінну делегата
        mes = Hello; // 3. Присвоюємо цій змінній адресу методу
        mes(); // 4. Викликаємо метод
        void Hello() => Console.WriteLine("Hello METANIT.COM");
    }
}
```

### Параметри та результат делегата

Розглянемо визначення та застосування делегата, який приймає параметри та повертає результат:

```csharp
Operation operation = Add; // делегат вказує на метод Add
int result = operation(4, 5); // фактично Add(4, 5)
Console.WriteLine(result); // 9
operation = Multiply; // тепер делегат вказує на метод Multiply
result = operation(4, 5); // фактично Multiply(4, 5)
Console.WriteLine(result); // 20
int Add(int x, int y) => x + y;
int Multiply(int x, int y) => x * y;
delegate int Operation(int x, int y);
```

У даному випадку делегат Operation повертає значення типу int і має два параметри типу int. Тому цьому делегату відповідає будь-який метод, який повертає значення типу int та приймає два параметри типу int. У нашому випадку це методи Add і Multiply. Тобто ми можемо присвоїти змінній делегату будь-який із цих методів і викликати.

Оскільки делегат приймає два параметри типу int, при його виклику необхідно передати значення цих параметрів: operation(4,5).

```csharp
Operation operation1 = Add;
Operation operation2 = new Operation(Add);
int Add(int x, int y) => x + y;
delegate int Operation(int x, int y);
```

Обидва способи рівноцінні.

### Відповідність методів делегату

Як було написано вище, методи відповідають делегату, якщо вони мають один і той же тип, що повертається, і той самий набір параметрів. Але треба враховувати, що до уваги також беруться модифікатори ref, in та out. Наприклад, нехай у нас є делегат:

```csharp
delegate void SomeDel(int a, double b);
```

Цьому делегату відповідає, наприклад, наступний метод:

```csharp
void SomeMethod1(int g, double n) { }
```

А такі методи не відповідають:

```csharp
double SomeMethod2(int g, double n) { return g + n; }
void SomeMethod3(double n, int g) { }
void SomeMethod4(ref int g, double n) { }
void SomeMethod5(out int g, double n) { g = 6; }
```

Тут метод SomeMethod2 має інший тип, що повертається, відмінний від типу делегата. SomeMethod3 має інший набір параметрів. Параметри SomeMethod4 та SomeMethod5 також відрізняються від параметрів делегата, оскільки мають модифікатори ref та out.

### Додавання методів у делегат

У прикладах вище змінна делегата вказувала на один метод. Насправді делегат може вказувати на безліч методів, які мають ту ж сигнатуру і тип, що повертається. Усі методи у делегаті потрапляють у спеціальний список - список виклику або invocation list. І при виклику делегата всі методи цього списку послідовно викликаються. І ми можемо додавати до цього списку не один, а кілька методів. Для додавання методів до делегата застосовується операція +=:

```csharp
Message message = Hello;
message += HowAreYou; // тепер message вказує на два методи
message(); // викликаються обидва методи - Hello і HowAreYou
void Hello() => Console.WriteLine("Hello");
void HowAreYou() => Console.WriteLine("How are you?");
delegate void Message();
```

У цьому випадку до списку виклику делегата message додаються два методи - Hello і HowAreYou. І при виклику message викликаються відразу обидва ці методи.

Однак варто зазначити, що в реальності відбуватиметься створення нового об'єкта делегата, який отримає методи старої копії делегата і новий метод, і новий об'єкт делегата буде присвоєний змінній message.

При додаванні делегатів слід враховувати, що ми можемо додати посилання на той самий метод кілька разів, і в списку виклику делегата тоді буде кілька посилань на той самий метод. Відповідно при виклику делегата доданий метод буде викликатися стільки разів, скільки він був доданий:

```csharp
Message message = Hello;
message += HowAreYou;
message += Hello;
message += Hello;
message();
```

Консольний вивід:

![Консольний вивід доданих методів делегата](../assets/docx/image97.png)

Подібним чином ми можемо видаляти методи з делегата за допомогою операції -=:

```csharp
Message? message = Hello;
message += HowAreYou;
message(); // викликаються всі методи з message
message -= HowAreYou; // видаляємо метод HowAreYou
if (message != null) message(); // викликається метод Hello
```

При видаленні методів з делегата фактично буде створюватись новий делегат, який у списку виклику методів міститиме на один метод менше.

Варто відзначити, що при видаленні методу може скластися ситуація, що в делегаті не буде методів, і тоді змінна матиме значення null. Тому в даному випадку змінна не просто визначена як змінна типу Message, а саме Message?, тобто типу, який може представляти як делегат Message, так і значення null.

Крім того, перед другим викликом ми перевіряємо змінну значення null.

При видаленні слід враховувати, що й делегат містить кілька посилань однією і той самий метод, то операція -= починає пошук із кінця списку виклику делегата і видаляє лише перше знайдене входження. Якщо такого методу у списку виклику делегата немає, то операція -= не має жодного ефекту.

### Об'єднання делегатів

Делегати можна поєднувати в інші делегати. Наприклад:

```csharp
Message mes1 = Hello;
Message mes2 = HowAreYou;
Message mes3 = mes1 + mes2; // об'єднуємо делегати
mes3(); // викликаються всі методи з mes1 та mes2
void Hello() => Console.WriteLine("Hello");
void HowAreYou() => Console.WriteLine("How are you?");
delegate void Message();
```

У разі об'єкт mes3 представляє об'єднання делегатів mes1 і mes2. Об'єднання делегатів означає, що до списку виклику делегата mes3 потраплять усі методи із делегатів mes1 та mes2. І за виклику делегата mes3 всі ці методи одночасно будуть викликані.

Виклик делегата

У прикладах вище делегат викликався як стандартний спосіб. Якщо делегат приймав параметри, то його виклику для параметрів передавалися необхідні значення:

```csharp
Message mes = Hello;
mes();
Operation op = Add;
int n = op(3, 4);
Console.WriteLine(n);
void Hello() => Console.WriteLine("Hello");
int Add(int x, int y) => x + y;
delegate int Operation(int x, int y);
delegate void Message();
```

Інший спосіб виклику делегата представляє метод Invoke():

```csharp
Message mes = Hello;
mes.Invoke(); // Hello
Operation op = Add;
int n = op.Invoke(3, 4);
Console.WriteLine(n); // 7
void Hello() => Console.WriteLine("Hello");
int Add(int x, int y) => x + y;
delegate int Operation(int x, int y);
delegate void Message();
```

Якщо делегат приймає параметри, то метод Invoke передаються значення цих параметрів.

Слід враховувати, що й делегат порожній, тобто у його списку виклику немає посилань на жодну з методів (тобто делегат дорівнює Null), то за виклику такого делегата ми отримаємо виняток, як, наприклад, у наступному випадку:

```csharp
Message? mes;
//mes(); // ! Помилка: делегат дорівнює null
Operation? op = Add;
op -= Add; // делегат op порожній
int n = op(3, 4); // !Помилка: делегат дорівнює null
```

Тому при виклику делегата завжди краще перевіряти, чи він не дорівнює null. Або можна використовувати метод Invoke та оператор умовного null:

```csharp
Message? mes = null;
mes?.Invoke(); // помилки немає, делегат просто не викликається
Operation? op = Add;
op -= Add; // делегат op порожній
int? n = op?.Invoke(3, 4); // помилки немає, делегат просто не викликається, а n = null
```

Якщо делегат повертає деяке значення, то повертається значення останнього методу зі списку виклику (якщо у списку виклику кілька методів). Наприклад:

```csharp
Operation op = Subtract;
op += Multiply;
op += Add;
Console.WriteLine(op(7, 2)); // Add(7,2) = 9
int Add(int x, int y) => x + y;
int Subtract(int x, int y) => x - y;
int Multiply(int x, int y) => x * y;
delegate int Operation(int x, int y);
```

### Узагальнені делегати

Делегати, як та інші типи, можуть бути узагальненими, наприклад:

```csharp
Operation<decimal, int> squareOperation = Square;
decimal result1 = squareOperation(5);
Console.WriteLine(result1); // 25
Operation<int, int> doubleOperation = Double;
int result2 = doubleOperation(5);
Console.WriteLine(result2); // 10
decimal Square(int n) => n * n;
int Double(int n) => n + n;
delegate T Operation<T, K>(K val);
```

Тут делегат Operation типизується двома параметрами типів. Параметр T представляє тип значення, що повертається. А параметр K представляє тип переданого делегат параметра. Таким чином, цьому делегату відповідає метод, який приймає параметр будь-якого типу та повертає значення будь-якого типу.

У прогамі ми можемо визначити змінні делегата під певний метод. Наприклад, делегату Operation<decimal, int> відповідає метод, який приймає число int та повертає число типу decimal. А делегату Operation<int, int> відповідає метод, який приймає та повертає число типу int.

### Делегати як параметри методів

Також делегати може бути параметрами методів. Завдяки цьому один метод як параметри може отримувати дії - інші методи. Наприклад:

```csharp
DoOperation(5, 4, Add); // 9
DoOperation(5, 4, Subtract); // 1
DoOperation(5, 4, Multiply); // 20
void DoOperation(int a, int b, Operation op)
{
    Console.WriteLine(op(a,b));
}
int Add(int x, int y) => x + y;
int Subtract(int x, int y) => x - y;
int Multiply(int x, int y) => x * y;
delegate int Operation(int x, int y);
```

Тут метод DoOperation як параметри приймає два числа і деяку дію у вигляді делегата Operation. Всередині методу викликаємо делегат Operation, передаючи йому числа з перших двох параметрів.

При виклику методу DoOperation ми можемо передати до нього як третій параметр метод, який відповідає делегату Operation.

### Повернення делегатів із методу

Також делегати можна повертати із методів. Тобто ми можемо повертати із методу якусь дію у вигляді іншого методу. Наприклад:

```csharp
Operation operation = SelectOperation(OperationType.Add);
Console.WriteLine(operation(10, 4)); // 14
operation = SelectOperation(OperationType.Subtract);
Console.WriteLine(operation(10, 4)); // 6
operation = SelectOperation(OperationType.Multiply);
Console.WriteLine(operation(10, 4)); // 40
Operation SelectOperation(OperationType opType)
{
    switch (opType)
    {
        case OperationType.Add: return Add;
        case OperationType.Subtract: return Subtract;
        default: return Multiply;
    }
}
int Add(int x, int y) => x + y;
int Subtract(int x, int y) => x - y;
int Multiply(int x, int y) => x * y;
enum OperationType
{
    Add, Subtract, Multiply
}
delegate int Operation(int x, int y);
```

В даному випадку метод SelectOperation() як параметр приймає перерахування типу OperationType. Цей перелік зберігає три константи, кожна з яких відповідає певній арифметичній операції. І в самому методі, залежно від значення параметра, повертаємо певний метод. Причому оскільки тип методу, що повертається - делегат Operation, то метод повинен повернути метод, який відповідає цьому делегату - у нашому випадку це методи Add, Subtract, Multiply. Тобто якщо параметр методу SelectOperation дорівнює OperationType.Add, то повертається метод Add, який виконує додавання двох чисел:

```csharp
case OperationType.Add: return Add;
```

При виклику методу SelectOperation ми можемо отримати з нього необхідну дію в змінну operation:

```csharp
Operation operation = SelectOperation(OperationType.Add);
```

І за виклику змінної operation фактично буде викликатися отриманий з SelectOperation метод:

```csharp
Operation operation = SelectOperation(OperationType.Add); // тут operation = Add
Console.WriteLine(operation(10, 4)); // 14
```

### Застосування делегатів

Минулої теми докладно було розглянуто делегати. Проте ці приклади, можливо, не показують справжньої сили делегатів, оскільки потрібні нам методи у разі ми можемо викликати і без будь-яких делегатів. Однак найбільш сильна сторона делегатів полягає в тому, що вони дозволяють делегувати виконання певного коду ззовні. І на момент написання програми ми можемо не знати, що за код виконуватиметься. Ми просто викликаємо делегат. А який метод безпосередньо виконуватиметься при виклику делегата, вирішуватиметься потім.

Розглянемо докладний приклад. Нехай у нас є клас, який описує рахунок у банку:

```csharp
public class Account
{
    int sum; // Змінна для зберігання суми
    // через конструктор встановлюється початкова сума на рахунку
    public Account(int sum) => this.sum = sum;
    // додати кошти на рахунок
    public void Add(int sum) => this.sum += sum;
    // взяти гроші з рахунку
    public void Take(int sum)
    {
        // беремо гроші, якщо на рахунку достатньо коштів
        if (this.sum >=sum) this.sum -= sum;
    }
}
```

У змінній sum зберігається сума на рахунку. За допомогою конструктора встановлюється початкова сума на рахунку. Метод Add() служить для додавання коштів на рахунок, а метод Take - для зняття грошей з рахунку.

Припустимо, у разі виведення грошей за допомогою методу Take нам треба якось повідомляти про це самого власника рахунку та, можливо, інші об'єкти. Якщо йдеться про консольну програму, і клас застосовуватиметься у тому ж проекті, де він створений, то ми можемо написати просто:

```csharp
public class Account
{
    int sum;
    public Account(int sum) => this.sum = sum;
    public void Add(int sum) => this.sum += sum;
    public void Take(int sum)
    {
        if (this.sum >= sum)
        {
            this.sum -= sum;
            Console.WriteLine($"З рахунку списано {sum} у.е.");
        }
    }
}
```

Але якщо наш клас планується використовувати в інших проектах, наприклад, у графічному додатку на Windows Forms або WPF, у мобільному додатку, у веб-додатку. Там рядок повідомлення

```csharp
Console.WriteLine($"З рахунку списано {sum} у.е.");
```

не матиме великого сенсу.

Більш того, наш клас Account використовуватиметься іншими розробниками у вигляді окремої бібліотеки класів. І ці розробники захочуть повідомляти про зняття коштів якимось іншим чином, про які ми можемо навіть не здогадуватися на момент написання класу. Тому примітивне повідомлення у вигляді рядка коду

```csharp
Console.WriteLine($"З рахунку списано {sum} у.е.");
```

не найкраще рішення у цьому випадку. І делегати дозволяють делегувати визначення дії із класу у зовнішній код, який використовуватиме цей клас.

Змінимо клас, застосувавши делегати:

```csharp
// Оголошуємо делегат
public delegate void AccountHandler(string message);
public class Account
{
    int sum;
    // Створюємо змінну делегата
    AccountHandler? taken;
    public Account(int sum) => this.sum = sum;
    // Реєструємо делегат
    public void RegisterHandler(AccountHandler del)
    {
        taken = del;
    }
    public void Add(int sum) => this.sum += sum;
    public void Take(int sum)
    {
        if (this.sum >= sum)
        {
            this.sum -= sum;
            // викликаємо делегат, передаючи йому повідомлення
            taken?.Invoke($"З рахунку списано {sum} у.е.");
        }
        else
        {
            taken?.Invoke($"Недостатньо коштів. Баланс: {this.sum} у.е.");
        }
    }
}
```

Для делегування дії тут визначено делегата AccountHandler. Цей делегат відповідає будь-яким методам, які мають тип void та приймають параметр типу string.

```csharp
public delegate void AccountHandler(string message);
```

У класі Account визначаємо змінну taken, яка представляє цей делегат:

```csharp
AccountHandler? taken;
```

Тепер треба пов'язати цю змінну з конкретною дією, яка виконуватиметься. Ми можемо використовувати різні способи передачі делегата в клас. У даному випадку визначається спеціальний метод RegisterHandler, який передається в змінну такої реальної дії:

```csharp
public void RegisterHandler(AccountHandler del)
{
    taken = del;
}
```

Таким чином, делегат встановлений і тепер його можна викликати. Виклик делегата здійснюється у методі Take:

```csharp
public void Take(int sum)
{
    if (this.sum >= sum)
    {
        this.sum -= sum;
        // викликаємо делегат, передаючи йому повідомлення
        taken?.Invoke($"З рахунку списано {sum} у.е.");
    }
    else
    {
        taken?.Invoke($"Недостатньо коштів. Баланс: {this.sum} у.е.");
    }
}
```

Оскільки делегат AccountHandler як параметр приймає рядок, при виклику змінної taken() ми можемо передати у цей виклик конкретне повідомлення. Залежно від того, чи відбулося зняття грошей, чи ні, у виклик делегата передаються різні повідомлення.

Тобто фактично замість делегата виконуватимуться дії, які передані делегату у методі RegisterHandler. Причому знову ж таки підкреслю, при виклику делегата ми не знаємо, що це будуть дії. Тут ми тільки передаємо в ці дії повідомлення про успішне або невдале зняття.

Тепер протестуємо клас в основній програмі:

```csharp
// створюємо банківський рахунок
Account account = new Account(200);
// Додаємо в делегат посилання на метод PrintSimpleMessage
account.RegisterHandler(PrintSimpleMessage);
// Двічі поспіль намагаємось зняти гроші
account.Take(100);
account.Take(150);
void PrintSimpleMessage(string message) => Console.WriteLine(message);
```

Тут через метод RegisterHandler змінної taken у класі Account передається посилання на метод PrintSimpleMessage. Цей метод відповідає делегату AccountHandler. Відповідно там, де викликається делегат taken у методі Account, насправді буде виконуватися метод PrintSimpleMessage.

Таким чином ми створили механізм зворотного виклику для класу Account, який спрацьовує у разі зняття грошей. Тут ми виводимо повідомлення на консоль. Так, ми могли просто виводити повідомлення на консоль і без делегатів. Проте з делегатом для класу Account не має значення, як це повідомлення виводиться. Класу Account навіть не відомо, що взагалі робитиметься внаслідок списання грошей. Він просто надсилає повідомлення про це через делегат.

В результаті, якщо ми створюємо консольну програму, ми можемо через делегат виводити повідомлення на консоль. Якщо ми створюємо графічну програму Windows Forms або WPF, можна виводити повідомлення у вигляді графічного вікна. А можна не просто виводити повідомлення. А, наприклад, записати при списанні інформацію про цю дію у файл або надіслати повідомлення на електронну пошту. Загалом у будь-який спосіб обробити виклик делегата. І спосіб обробки не залежатиме від класу Account.

### Додавання та видалення методів у делегаті

Хоча у прикладі наш делегат приймав адресу одного методу, насправді він може вказувати відразу на кілька методів. Крім того, за потреби ми можемо видалити посилання на адреси певних методів, щоб вони не викликалися під час виклику делегата. Отже, змінимо в класі Account метод RegisterHandler і додамо новий метод UnregisterHandler, який видалятиме методи зі списку методів делегата:

```csharp
public delegate void AccountHandler(string message);
public class Account
{
    int sum;
    AccountHandler? taken;
    public Account(int sum) => this.sum = sum;
    // Реєструємо делегат
    public void RegisterHandler(AccountHandler del)
    {
        taken += del;
    }
    // Скасування реєстрації делегата
    public void UnregisterHandler(AccountHandler del)
    {
        taken -= del; // видаляємо делегат
    }
    public void Add(int sum) => this.sum += sum;
    public void Take(int sum)
    {
        if (this.sum >= sum)
        {
            this.sum -= sum;
            taken?.Invoke($"З рахунку списано{sum} у.е.");
        }
        else
        taken?.Invoke($"Недостатньо коштів. Баланс: {this.sum} у.е.");
    }
}
```

У першому методі об'єднуються делегати taken і del в один, який потім присвоюється змінній taken. У другому методі зі змінної taken видаляється делегат del.

Застосуємо нові методи:

```csharp
Account account = new Account(200);
// Додаємо в делегат посилання на методи
account.RegisterHandler(PrintSimpleMessage);
account.RegisterHandler(PrintColorMessage);
// Двічі поспіль намагаємось зняти гроші
account.Take(100);
account.Take(150);
// Видаляємо делегат
account.UnregisterHandler(PrintColorMessage);
// знову намагаємось зняти гроші
account.Take(50);
void PrintSimpleMessage(string message) => Console.WriteLine(message);
void PrintColorMessage(string message)
{
    // Встановлюємо червоний колір символів
    Console.ForegroundColor = ConsoleColor.Red;
    Console.WriteLine(message);
    // Скидаємо налаштування кольору
    Console.ResetColor();
}
```

З метою тестування ми створили ще один метод - PrintColorMessage, який виводить те саме повідомлення тільки червоним кольором. Посилання на цей метод також передається в метод RegisterHandler, і таким чином його отримає змінна taken.

У рядку account.UnregisterHandler(PrintColorMessage); цей метод видаляється зі списку виклику делегата, тому цей метод більше не спрацьовуватиме.

### Анонімні методи

Із делегатами тісно пов'язані анонімні методи. Анонімні методи використовують для створення екземплярів делегатів.

Визначення анонімних методів починається з ключового слова delegate, після якого йде у дужках список параметрів та тіло методу у фігурних дужках:

```csharp
delegate(параметри)
{
    // інструкції
}
```

Наприклад:

```csharp
MessageHandler handler = delegate (string mes)
{
    Console.WriteLine(mes);
};
handler("hello world!");
delegate void MessageHandler(string message);
```

Анонімний метод не може існувати сам по собі, він використовується для ініціалізації екземпляра делегата, як у даному випадку змінна handler є анонімним методом. І через цю змінну делегата можна викликати цей анонімний метод.

Інший приклад анонімних методів - передача як аргумент для параметра, який представляє делегат:

```csharp
ShowMessage("hello!", delegate (string mes)
{
    Console.WriteLine(mes);
});
static void ShowMessage(string message, MessageHandler handler)
{
    handler(message);
}
delegate void MessageHandler(string message);
```

Якщо анонімний метод використовує параметри, вони повинні відповідати параметрам делегата. Якщо для анонімного методу не потрібні параметри, то дужки з параметрами опускаються. При цьому навіть якщо делегат приймає кілька параметрів, то в анонімному методі можна опустити параметри:

```csharp
MessageHandler handler = delegate
{
    Console.WriteLine("анонімний метод");
};
handler("hello world!"); // анонімний метод
delegate void MessageHandler(string message);
```

Тобто, якщо анонімний метод містить параметри, вони обов'язково повинні відповідати параметрам делегата. Або анонімний метод взагалі може не містити жодних параметрів, тоді він відповідає будь-якому делегату, який має той же тип значення, що повертається.

При цьому параметри анонімного методу не можуть бути опущені, якщо один або декілька параметрів визначено модифікатором out.

Так само, як і звичайні методи, анонімні можуть повертати результат:

```csharp
Operation operation = delegate (int x, int y)
{
    return x + y;
};
int result = operation(4, 5);
Console.WriteLine(result); // 9
delegate int Operation(int x, int y);
```

При цьому анонімний метод має доступ до всіх змінних, визначених у зовнішньому коді:

```csharp
int z = 8;
Operation operation = delegate (int x, int y)
{
    return x + y + z;
};
int result = operation(4, 5);
Console.WriteLine(result); // 17
delegate int Operation(int x, int y);
```

У яких ситуаціях використовують анонімні методи? Коли нам треба визначити одноразову дію, яка не має багато інструкцій та ніде більше не використовується. Зокрема їх можна використовувати для обробки подій, які будуть розглянуті далі.
