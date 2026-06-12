---
chapter: 6
chapterTitle: "Розділ 6. Делегати, події та лямбди"
section: 1
number: "6.1"
title: "Делегати"
source: "../_combined/34-delehaty.md"
---

## 6.1. Делегати

Делегати — один із фундаментальних механізмів C#, який дозволяє зберігати посилання на методи і передавати методи як значення. Якщо змінна типу `int` зберігає число, а змінна типу `string` — рядок, то змінна-делегат зберігає посилання на метод. Через цю змінну метод можна викликати, передати в інший метод як аргумент або зберегти для виклику пізніше. Делегати є основою для подій, лямбда-виразів, функцій вищого порядку та патерну зворотного виклику (callback). Розуміння делегатів — це розуміння того, як у C# методи стають об'єктами першого класу.

## Визначення делегата

Для оголошення делегата використовується ключове слово `delegate`, після якого вказується тип значення, що повертається, ім'я делегата та список параметрів. По суті, це оголошення нового типу, який описує сигнатуру методів, на які делегат може вказувати:

```csharp
delegate void Notify(string message);
```

Делегат `Notify` відповідає будь-якому методу, який приймає один параметр `string` і нічого не повертає (`void`). Жоден інший набір параметрів або тип, що повертається, не підійде — компілятор перевіряє це статично.

Розглянемо застосування цього делегата:

```csharp run
using System;

Notify handler;                  // 2. Створюємо змінну делегата
handler = AlertDoctor;           // 3. Присвоюємо адресу методу
handler("Критичний пульс!");     // 4. Викликаємо метод через делегат

void AlertDoctor(string msg) => Console.WriteLine($"[ЛІКАР] {msg}");
delegate void Notify(string message); // 1. Оголошуємо делегат
```

Насамперед необхідно визначити сам делегат — оголосити новий тип. Потім оголошується змінна цього типу. Далі делегату передається адреса певного методу — у нашому випадку методу `AlertDoctor`. Зверніть увагу: цей метод має той самий тип, що повертається, і той самий набір параметрів, що і делегат. Нарешті, через змінну делегата викликається метод. Виклик делегата виглядає так само, як звичайний виклик методу.

![Делегат як посилання на метод](_assets/06-01/delegate-concept.png)

При цьому делегати не обмежені методами того класу, де визначена змінна делегата. Це можуть бути також методи інших класів і структур:

```csharp run
using System;

Notify n1 = ClinicLogger.Print;
Notify n2 = new DoctorNotifier().Alert;

n1("Аналізи готові");   // виклик статичного методу
n2("Пацієнт Петренко потребує огляду"); // виклик екземплярного методу

delegate void Notify(string message);

class ClinicLogger
{
    public static void Print(string msg) =>
        Console.WriteLine($"[LOG] {msg}");
}

class DoctorNotifier
{
    public void Alert(string msg) =>
        Console.WriteLine($"[DR] {msg}");
}
```

## Місце визначення делегата

Якщо ми визначаємо делегат у програмах верхнього рівня (top-level program), яку за замовчуванням представляє файл `Program.cs`, починаючи з версії C# 10, то, як і інші типи, делегат визначається в кінці коду (як у прикладах вище). Але делегат можна визначати і всередині класу:

```csharp
class Program
{
    delegate void Notify(string message); // делегат всередині класу

    static void Main()
    {
        Notify handler;
        handler = AlertDoctor;
        handler("Критичний пульс!");

        void AlertDoctor(string msg) => Console.WriteLine($"[ЛІКАР] {msg}");
    }
}
```

Або поза класом:

```csharp
delegate void Notify(string message); // делегат поза класом

class Program
{
    static void Main()
    {
        Notify handler;
        handler = AlertDoctor;
        handler("Критичний пульс!");

        void AlertDoctor(string msg) => Console.WriteLine($"[ЛІКАР] {msg}");
    }
}
```

## Параметри та результат делегата

Делегат повністю успадковує сигнатуру методу: параметри, їх типи і тип значення, що повертається. Розглянемо визначення та застосування делегата, який приймає параметри і повертає результат. Делегат можна перепризначати між методами, що мають однакову сигнатуру:

```csharp run
using System;

Calculate calc = Add; // делегат вказує на метод Add
double r1 = calc(10.5, 4.5); // фактично Add(10.5, 4.5)
Console.WriteLine($"Сума: {r1.ToString("F1")}");

calc = Subtract; // тепер делегат вказує на Subtract
double r2 = calc(10.5, 4.5);
Console.WriteLine($"Різниця: {r2.ToString("F1")}");

calc = Multiply;
double r3 = calc(10.5, 4.5);
Console.WriteLine($"Добуток: {r3.ToString("F1")}");

double Add(double x, double y)      => x + y;
double Subtract(double x, double y) => x - y;
double Multiply(double x, double y) => x * y;

delegate double Calculate(double a, double b);
```

Делегат `Calculate` повертає `double` і приймає два параметри `double`. Тому йому відповідає будь-який метод з таким самим підписом — `Add`, `Subtract`, `Multiply`. Оскільки делегат приймає два параметри, при виклику необхідно передати їх значення.

Існує також альтернативний синтаксис ініціалізації через конструктор делегата — обидва варіанти рівноцінні:

```csharp
Calculate calc1 = Add;
Calculate calc2 = new Calculate(Add); // рівноцінно першому
```

## Відповідність методів делегату

Як зазначено вище, методи відповідають делегату, якщо вони мають **той самий тип, що повертається**, і **той самий набір параметрів**. При цьому до уваги також беруться модифікатори `ref`, `in` та `out`. Наприклад, нехай у нас є делегат:

```csharp
delegate void AlertHandler(string message, int code);
```

Цьому делегату відповідає такий метод:

```csharp
void LogAlert(string msg, int level) { } // OK — той самий підпис
```

А такі методи не відповідають:

```csharp
string GetAlert(string msg, int code) { return msg; } // інший тип повернення
void Handle(int code, string msg)     { }              // інший порядок параметрів
void Handle(ref string msg, int code) { }              // модифікатор ref
void Handle(out string msg, int code) { msg = ""; }    // модифікатор out
```

Метод з іншим типом повернення не підходить. Метод з іншим порядком параметрів — теж, навіть якщо типи самих параметрів збігаються. Наявність модифікаторів `ref` або `out` також робить метод несумісним із делегатом без цих модифікаторів.

## Додавання методів у делегат

У прикладах вище змінна делегата вказувала на один метод. Насправді делегат може вказувати на **безліч методів**, які мають ту ж сигнатуру і тип, що повертається. Усі методи у делегаті потрапляють у спеціальний список — **список виклику** (invocation list). При виклику делегата всі методи цього списку послідовно викликаються. Для додавання методів до делегата застосовується операція `+=`:

```csharp run
using System;

AlertHandler alert = LogToConsole;
alert += NotifyDoctor; // тепер alert вказує на два методи
alert("Критичні показники пацієнта Бойка!"); // викликаються обидва

void LogToConsole(string msg) => Console.WriteLine($"[КОНСОЛЬ] {msg}");
void NotifyDoctor(string msg) => Console.WriteLine($"[ЛІКАР] Увага: {msg}");
delegate void AlertHandler(string message);
```

У цьому випадку до списку виклику делегата `alert` додаються два методи. При виклику `alert` викликаються відразу обидва.

Однак варто зазначити, що в реальності відбувається створення нового об'єкта делегата, який отримує методи старої копії і новий метод, і цей новий об'єкт присвоюється змінній `alert`.

При додаванні делегатів слід враховувати, що один і той самий метод можна додати кілька разів. У цьому випадку у списку виклику делегата буде кілька посилань на той самий метод, і при виклику делегата цей метод буде викликатися стільки разів, скільки він був доданий:

```csharp run
using System;

AlertHandler alert = LogToConsole;
alert += NotifyDoctor;
alert += LogToConsole; // LogToConsole додано вдруге
alert += LogToConsole; // і втретє
alert("Тиск 180/110 — критично!");

void LogToConsole(string msg) => Console.WriteLine($"[LOG] {msg}");
void NotifyDoctor(string msg) => Console.WriteLine($"[DR]  {msg}");
delegate void AlertHandler(string message);
```

![Список виклику multicast-делегата](_assets/06-01/invocation-list.png)

Подібним чином ми можемо видаляти методи з делегата за допомогою операції `-=`:

```csharp run
using System;

AlertHandler? alert = LogToConsole;
alert += NotifyDoctor;
alert("Температура 39.5°C"); // викликаються обидва методи

alert -= NotifyDoctor; // видаляємо NotifyDoctor
if (alert != null) alert("Температура 38.0°C"); // викликається лише LogToConsole

void LogToConsole(string msg) => Console.WriteLine($"[LOG] {msg}");
void NotifyDoctor(string msg) => Console.WriteLine($"[DR]  {msg}");
delegate void AlertHandler(string message);
```

При видаленні методів з делегата фактично також створюється новий делегат, який у списку виклику містить на один метод менше.

Варто відзначити: при видаленні може скластися ситуація, що в делегаті не залишиться жодного методу — тоді змінна матиме значення `null`. Тому в даному випадку змінна оголошена як `AlertHandler?` (nullable), тобто тип, який може представляти як делегат, так і значення `null`. Крім того, перед другим викликом ми перевіряємо змінну на `null`.

При видаленні слід враховувати: якщо делегат містить кілька посилань на один і той самий метод, то операція `-=` починає пошук із кінця списку виклику і видаляє лише перше знайдене входження. Якщо такого методу у списку немає — операція `-=` не має жодного ефекту.

## Об'єднання делегатів

Делегати можна поєднувати в інші делегати за допомогою оператора `+`. Отримаємо новий делегат, чий список виклику містить усі методи обох:

```csharp run
using System;

AlertHandler group1 = LogToConsole;
group1 += NotifyDoctor;

AlertHandler group2 = SendSMS;

AlertHandler all = group1 + group2; // об'єднуємо делегати
all("Пацієнт Сидоренко: пульс 145 уд/хв"); // викликаються всі методи з group1 і group2

void LogToConsole(string msg) => Console.WriteLine($"[LOG]  {msg}");
void NotifyDoctor(string msg) => Console.WriteLine($"[DR]   {msg}");
void SendSMS(string msg)      => Console.WriteLine($"[SMS]  {msg}");
delegate void AlertHandler(string message);
```

Об'єднання делегатів означає, що до списку виклику делегата `all` потраплять усі методи із делегатів `group1` та `group2`. При виклику `all` всі ці методи викликаються одночасно.

## Виклик делегата

У прикладах вище делегат викликався як звичайний метод. Якщо делегат приймає параметри — при виклику передаються необхідні значення:

```csharp run
using System;

AlertHandler alert = LogToConsole;
alert("Критичний показник!");

Calculate calc = Add;
int n = calc(120, 80);
Console.WriteLine($"Результат: {n.ToString()}");

void LogToConsole(string msg) => Console.WriteLine($"[LOG] {msg}");
int Add(int x, int y) => x + y;

delegate void AlertHandler(string message);
delegate int Calculate(int x, int y);
```

Інший спосіб виклику делегата — метод `Invoke()`:

```csharp run
using System;

AlertHandler alert = LogToConsole;
alert.Invoke("Критичний показник!"); // еквівалентно alert(...)

Calculate calc = Add;
int n = calc.Invoke(120, 80);
Console.WriteLine($"Результат: {n.ToString()}");

void LogToConsole(string msg) => Console.WriteLine($"[LOG] {msg}");
int Add(int x, int y) => x + y;

delegate void AlertHandler(string message);
delegate int Calculate(int x, int y);
```

Якщо делегат приймає параметри — методу `Invoke` передаються їх значення.

Слід враховувати: якщо делегат порожній, тобто у його списку виклику немає жодного методу (делегат дорівнює `null`), то при виклику такого делегата виникне виняток:

```csharp
AlertHandler? alert;
// alert("Помилка!"); // NullReferenceException — делегат дорівнює null

Calculate? calc = Add;
calc -= Add; // делегат calc порожній
// int n = calc(10, 5); // NullReferenceException

delegate void AlertHandler(string message);
delegate int Calculate(int x, int y);
int Add(int x, int y) => x + y;
```

Тому при виклику делегата краще завжди перевіряти, чи він не дорівнює `null`. Або використовувати метод `Invoke` з оператором умовного null `?.`, який безпечно не виконає виклик якщо делегат `null`:

```csharp run
using System;

AlertHandler? alert = null;
alert?.Invoke("Безпечний виклик — нічого не станеться");

Calculate? calc = Add;
calc -= Add; // список виклику порожній
int? result = calc?.Invoke(10, 5); // result буде null, винятку немає
Console.WriteLine($"result = {result?.ToString() ?? "null"}");

int Add(int x, int y) => x + y;
delegate void AlertHandler(string message);
delegate int Calculate(int x, int y);
```

Якщо делегат повертає деяке значення і у його списку виклику кілька методів — повертається значення **останнього методу** зі списку. Наприклад:

```csharp run
using System;

Calculate calc = Method1;
calc += Method2;
calc += Method3;
Console.WriteLine($"Повернуто: {calc(10, 3).ToString()}"); // Add(10,3) = 13

int Method1(int x, int y) { Console.WriteLine($"Method1: {(x*y).ToString()}"); return x * y; }
int Method2(int x, int y) { Console.WriteLine($"Method2: {(x-y).ToString()}"); return x - y; }
int Method3(int x, int y) { Console.WriteLine($"Method3: {(x+y).ToString()}"); return x + y; }

delegate int Calculate(int x, int y);
```

## Узагальнені делегати

Делегати, як і інші типи, можуть бути узагальненими. Це дозволяє описати делегат, що відповідає методам із різними конкретними типами параметрів і повернення:

```csharp run
using System;

Transform<double, double> weightConv  = KgToLb;
Transform<int, int>       tempConv    = CelsiusToFahrenheit;
Transform<int, string>    pulseFormat = FormatPulse;

double result1 = weightConv(70.0);
Console.WriteLine($"70 кг = {result1.ToString("F1")} фунтів");

int result2 = tempConv(37);
Console.WriteLine($"37°C = {result2.ToString()}°F");

Console.WriteLine(pulseFormat(72));

double KgToLb(double kg) => kg * 2.20462;
int CelsiusToFahrenheit(int celsius) => celsius * 9 / 5 + 32;
string FormatPulse(int pulse) => $"{pulse.ToString()} уд/хв";

delegate T Transform<K, T>(K value);
```

Тут делегат `Transform` типізується двома параметрами типів. Параметр `K` представляє тип вхідного параметра, а параметр `T` — тип значення, що повертається. Таким чином, цьому делегату відповідає метод, який приймає параметр будь-якого типу та повертає значення будь-якого типу. Делегату `Transform<double, double>` відповідає метод, що приймає і повертає `double`, а делегату `Transform<int, string>` — метод, що приймає `int` і повертає `string`.

## Делегати як параметри методів

Делегати можуть бути параметрами методів. Завдяки цьому один метод може отримувати інші методи як дії — параметри. Це і є функції вищого порядку:

```csharp run
using System;

CalculateVitals(120, 80, AddPressure);
CalculateVitals(120, 80, SubtractPressure);
CalculateVitals(120, 80, MultiplyPressure);

void CalculateVitals(int systolic, int diastolic, Operation op)
{
    Console.WriteLine($"Результат: {op(systolic, diastolic).ToString()}");
}

int AddPressure(int x, int y)      => x + y;
int SubtractPressure(int x, int y) => x - y;
int MultiplyPressure(int x, int y) => x * y;

delegate int Operation(int x, int y);
```

Тут метод `CalculateVitals` як параметри приймає два числа і деяку дію у вигляді делегата `Operation`. Всередині методу викликаємо делегат, передаючи йому числа з перших двох параметрів. При виклику методу `CalculateVitals` ми можемо передати як третій параметр будь-який метод, що відповідає делегату `Operation`.

## Повернення делегатів із методів

Також делегати можна повертати з методів. Тобто ми можемо повертати з методу якусь дію у вигляді іншого методу:

```csharp run
using System;

Operation op1 = SelectOperation(OperationType.Add);
Console.WriteLine($"Результат: {op1(120, 80).ToString()}");

Operation op2 = SelectOperation(OperationType.Subtract);
Console.WriteLine($"Результат: {op2(120, 80).ToString()}");

Operation op3 = SelectOperation(OperationType.Multiply);
Console.WriteLine($"Результат: {op3(120, 80).ToString()}");

Operation SelectOperation(OperationType opType)
{
    switch (opType)
    {
        case OperationType.Add:      return Add;
        case OperationType.Subtract: return Subtract;
        default:                     return Multiply;
    }
}

int Add(int x, int y)      => x + y;
int Subtract(int x, int y) => x - y;
int Multiply(int x, int y) => x * y;

enum OperationType { Add, Subtract, Multiply }
delegate int Operation(int x, int y);
```

В даному випадку метод `SelectOperation` як параметр приймає значення перерахування `OperationType`. Залежно від значення параметра повертається певний метод. Оскільки тип методу, що повертається — делегат `Operation`, то метод повинен повернути метод, який відповідає цьому делегату. Тобто, якщо параметр дорівнює `OperationType.Add`, повертається метод `Add`.

При виклику `SelectOperation` ми отримуємо необхідну дію у змінну `op1`. І при виклику змінної `op1` фактично буде викликатися отриманий з `SelectOperation` метод.

## Застосування делегатів

Наведені вище приклади, можливо, не показують справжньої сили делегатів, оскільки потрібні нам методи ми могли б викликати і без будь-яких делегатів. Однак найбільш сильна сторона делегатів полягає в тому, що вони дозволяють **делегувати виконання певного коду ззовні**. На момент написання класу ми можемо не знати, що саме буде виконуватися — ми просто викликаємо делегат. А який метод безпосередньо виконуватиметься, вирішуватиметься потім, при використанні класу.

![Патерн зворотного виклику через делегат](_assets/06-01/callback-pattern.png)

Розглянемо детальний приклад. Нехай у нас є клас, який описує пацієнта в системі:

```csharp
public class Patient
{
    int _balance; // умовний баланс страхових коштів
    public Patient(int balance) => _balance = balance;
    public void AddFunds(int amount) => _balance += amount;
    public void Spend(int amount)
    {
        if (_balance >= amount) _balance -= amount;
    }
}
```

Припустимо, нам треба повідомляти про кожне списання страхових коштів пацієнта. Якщо клас використовується лише в консольній програмі того самого проекту, де він створений, можна написати просто:

```csharp
public void Spend(int amount)
{
    if (_balance >= amount)
    {
        _balance -= amount;
        Console.WriteLine($"Списано {amount} грн. зі страхового рахунку.");
    }
}
```

Але якщо наш клас планується використовувати в інших проектах — у графічному додатку Windows Forms або WPF, у мобільному додатку, у веб-API — рядок повідомлення `Console.WriteLine(...)` не матиме жодного сенсу. Більш того, якщо клас `Patient` використовуватиметься іншими розробниками у вигляді окремої бібліотеки, ці розробники захочуть повідомляти про списання коштів якимось іншим чином — про який ми навіть не здогадуємося на момент написання класу.

Тому жорстко вшитий `Console.WriteLine` — не найкраще рішення. Делегати дозволяють делегувати визначення дії із класу у зовнішній код, який використовуватиме цей клас. Змінимо клас, застосувавши делегати:

```csharp run
using System;

// Створюємо пацієнта зі страховим рахунком
Patient patient = new Patient(500);
// Передаємо обробник — консольний вивід
patient.RegisterHandler(PrintMessage);
// Двічі намагаємось списати кошти
patient.Spend(200);
patient.Spend(400);

void PrintMessage(string message) => Console.WriteLine(message);

// Оголошуємо делегат — тип для обробника подій
public delegate void PatientHandler(string message);

public class Patient
{
    int _balance;
    // Змінна делегата — зберігає посилання на обробник
    PatientHandler? _onSpend;

    public Patient(int balance) => _balance = balance;

    // Метод для реєстрації обробника
    public void RegisterHandler(PatientHandler handler)
    {
        _onSpend = handler;
    }

    public void AddFunds(int amount) => _balance += amount;

    public void Spend(int amount)
    {
        if (_balance >= amount)
        {
            _balance -= amount;
            // Викликаємо делегат — що саме відбудеться, вирішить зовнішній код
            _onSpend?.Invoke($"Списано {amount.ToString()} грн. Залишок: {_balance.ToString()} грн.");
        }
        else
        {
            _onSpend?.Invoke($"Недостатньо коштів. Баланс: {_balance.ToString()} грн.");
        }
    }
}
```

Для делегування дії тут визначено делегат `PatientHandler`. Цей делегат відповідає будь-яким методам, які мають тип `void` та приймають параметр типу `string`:

```csharp
public delegate void PatientHandler(string message);
```

У класі `Patient` визначається змінна `_onSpend`, що представляє цей делегат. Далі визначається спеціальний метод `RegisterHandler`, через який передається реальна дія — конкретний метод ззовні:

```csharp
public void RegisterHandler(PatientHandler handler)
{
    _onSpend = handler;
}
```

Виклик делегата відбувається у методі `Spend`. Залежно від того, чи відбулося списання, передаються різні повідомлення. Класу `Patient` не важливо, що саме відбудеться — він лише надсилає повідомлення через делегат.

Таким чином, ми створили механізм зворотного виклику для класу `Patient`. Тут ми виводимо повідомлення на консоль. Але зовнішній код міг би записати повідомлення у файл, надіслати на email, показати у графічному вікні — будь-який спосіб обробки, незалежно від класу `Patient`.

## Додавання та видалення методів у делегаті

Хоча у прикладі наш делегат приймав адресу одного методу, насправді він може вказувати відразу на кілька. Крім того, за потреби ми можемо видалити посилання на певні методи, щоб вони не викликалися при виклику делегата. Змінимо клас `Patient`: метод `RegisterHandler` тепер використовуватиме `+=`, а новий метод `UnregisterHandler` — `-=`:

```csharp run
using System;

Patient patient = new Patient(500);

// Реєструємо два обробники
patient.RegisterHandler(PrintSimpleMessage);
patient.RegisterHandler(PrintHighlightedMessage);

patient.Spend(200);
patient.Spend(400);

// Видаляємо другий обробник
patient.UnregisterHandler(PrintHighlightedMessage);
// Тепер спрацьовує лише перший
patient.Spend(100);

void PrintSimpleMessage(string message) => Console.WriteLine(message);
void PrintHighlightedMessage(string message)
{
    Console.WriteLine($"*** {message} ***");
}

public delegate void PatientHandler(string message);

public class Patient
{
    int _balance;
    PatientHandler? _onSpend;

    public Patient(int balance) => _balance = balance;

    // Реєструємо обробник — додаємо до списку
    public void RegisterHandler(PatientHandler handler)
    {
        _onSpend += handler;
    }

    // Скасування реєстрації обробника — видаляємо зі списку
    public void UnregisterHandler(PatientHandler handler)
    {
        _onSpend -= handler;
    }

    public void AddFunds(int amount) => _balance += amount;

    public void Spend(int amount)
    {
        if (_balance >= amount)
        {
            _balance -= amount;
            _onSpend?.Invoke($"Списано {amount.ToString()} грн. Залишок: {_balance.ToString()} грн.");
        }
        else
        {
            _onSpend?.Invoke($"Недостатньо коштів. Баланс: {_balance.ToString()} грн.");
        }
    }
}
```

У методі `RegisterHandler` делегати `_onSpend` і `handler` об'єднуються в один, який присвоюється змінній `_onSpend`. У методі `UnregisterHandler` зі змінної `_onSpend` видаляється делегат `handler`.

## Анонімні методи

З делегатами тісно пов'язані анонімні методи. Анонімні методи використовуються для створення екземплярів делегатів без оголошення окремого іменованого методу.

Визначення анонімних методів починається з ключового слова `delegate`, після якого у дужках йде список параметрів та тіло методу у фігурних дужках:

```text
delegate(параметри)
{
    // інструкції
}
```

Наприклад:

```csharp run
using System;

PatientHandler handler = delegate(string msg)
{
    Console.WriteLine($"[ОБРОБНИК] {msg}");
};

handler("Пацієнт Коваль: списано 150 грн.");

delegate void PatientHandler(string message);
```

Анонімний метод не може існувати сам по собі — він використовується для ініціалізації екземпляра делегата. У даному випадку змінна `handler` є анонімним методом, і через цю змінну делегата можна викликати цей анонімний метод.

Інший приклад анонімних методів — передача як аргумент для параметра, який представляє делегат:

```csharp run
using System;

ShowAlert("Пульс 145 уд/хв — критично!", delegate(string mes)
{
    Console.WriteLine($"[СПОВІЩЕННЯ] {mes}");
});

void ShowAlert(string message, PatientHandler handler)
{
    handler(message);
}

delegate void PatientHandler(string message);
```

Якщо анонімному методу не потрібні параметри — дужки з параметрами опускаються. При цьому навіть якщо делегат приймає кілька параметрів, в анонімному методі можна їх не вказувати:

```csharp run
using System;

PatientHandler handler = delegate
{
    Console.WriteLine("Отримано сповіщення");
};

handler("будь-яке повідомлення"); // параметр ігнорується

delegate void PatientHandler(string message);
```

Тобто якщо анонімний метод містить параметри — вони обов'язково повинні відповідати параметрам делегата. Або анонімний метод взагалі може не містити жодних параметрів, тоді він відповідає будь-якому делегату з тим самим типом значення, що повертається. При цьому параметри анонімного методу не можуть бути опущені, якщо один або декілька параметрів визначено модифікатором `out`.

Так само, як і звичайні методи, анонімні можуть повертати результат:

```csharp run
using System;

Calculate calc = delegate(int x, int y)
{
    return x + y;
};

int result = calc(120, 80);
Console.WriteLine($"Результат: {result.ToString()}");

delegate int Calculate(int x, int y);
```

При цьому анонімний метод має доступ до всіх змінних, визначених у зовнішньому коді (замикання):

```csharp run
using System;

string wardName  = "Кардіологія";
int    alertCount = 0;

PatientHandler handler = delegate(string msg)
{
    alertCount++;
    Console.WriteLine($"[{wardName}] #{alertCount.ToString()}: {msg}");
};

handler("Пульс 145");
handler("Тиск 180/100");
handler("Температура 39.2");
Console.WriteLine($"Всього сповіщень: {alertCount.ToString()}");

delegate void PatientHandler(string message);
```

Анонімний метод захоплює змінні `wardName` і `alertCount` із зовнішнього контексту — це замикання (closure). Зміна `alertCount` всередині анонімного методу відображається і в зовнішньому коді. Анонімні методи зазвичай використовують тоді, коли потрібно визначити одноразову дію, яка не має багато інструкцій та ніде більше не використовується. Зокрема, їх часто застосовують для обробки подій, які будуть розглянуті далі. Анонімні методи є попередниками лямбда-виразів — більш компактного сучасного способу запису того самого, який розглядатиметься у наступних розділах.
