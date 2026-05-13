---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 3
number: "7.3"
title: "Явна реалізація інтерфейсів"
source: "../_combined/41-yavna-realizatsiia-interfeisiv.md"
---

## 7.3. Явна реалізація інтерфейсів

Окрім неявного застосування інтерфейсів, яке було розглянуто у минулій статті, існує також явна реалізація інтерфейсу. При явній реалізації вказується назва методу або властивості разом із назвою інтерфейсу, при цьому ми не можемо використовувати модифікатор public, тобто методи закриті:

```csharp
interface IAction
{
    void Move();
}
class BaseAction : IAction
{
    void IAction.Move() => Console.WriteLine("Move in Base Class");
}
```

Слід враховувати, що з явної реалізації інтерфейсу його методи та властивості є частиною інтерфейсу класу. Тому безпосередньо через об'єкт класу ми до них не зможемо звернутися:

```csharp
BaseAction baseAction1 = new BaseAction();
// baseAction1.Move(); // ! Помилка - в BaseAction немає методу Move
// необхідне приведення до типу IAction
// небезпечне приведення
((IAction)baseAction1).Move();
// безпечне приведення
if (baseAction1 is IAction action) action.Move();
// чи так
IAction baseAction2 = new BaseAction();
baseAction2.Move();
```

У якій ситуації може справді знадобитися явна реалізація інтерфейсу? Наприклад, коли клас застосовує кілька інтерфейсів, але вони мають один і той же метод з одним і тим же результатом, що повертається, і одним і тим же набором параметрів:

```csharp
class Person : ISchool, IUniversity
{
    public void Study() => Console.WriteLine("Навчання в школі або університеті");
}
interface ISchool
{
    void Study();
}
interface IUniversity
{
    void Study();
}
```

Клас Person визначає один метод Study(), створюючи одну загальну реалізацію обох застосованих інтерфейсів. І незалежно від того, чи будемо ми розглядати об'єкт Person як об'єкт типу ISchool або IUniversity, результат методу буде той самий.

Щоб розмежувати реалізовані інтерфейси, треба явно застосувати інтерфейс:

```csharp
class Person : ISchool, IUniversity
{
    void ISchool.Study() => Console.WriteLine("Навчання в школі");
    void IUniversity.Study() => Console.WriteLine("Навчання в універі");
}
```

Використання:

```csharp
Person person = new Person();
((ISchool)person).Study();
((IUniversity)person).Study();
```

Інша ситуація, коли у базовому класі вже реалізований інтерфейс, але необхідно у похідному класі по-своєму реалізувати інтерфейс:

```csharp
interface IAction
{
    void Move();
}
class BaseAction : IAction
{
    public void Move() => Console.WriteLine("Move in BaseAction");
}
class HeroAction : BaseAction, IAction
{
    void IAction.Move() => Console.WriteLine("Move in HeroAction");
}
```

Незважаючи на те, що базовий клас BaseAction вже реалізував інтерфейс IAction, похідний клас по-своєму реалізує його. Застосування класів:

```csharp
HeroAction action1 = new HeroAction();
action1.Move(); // Move in BaseAction
((IAction)action1).Move(); // Move in HeroAction
IAction action2 = new HeroAction();
action2.Move(); // Move in HeroAction
```

### Модифікатори доступу

Члени інтерфейсу можуть мати різні модифікатори доступу. Якщо модифікатор доступу не public, а якийсь інший, то для реалізації методу, властивості або події інтерфейсу в класах і структурах необхідно використовувати явну реалізацію інтерфейсу.

```csharp
IMovable tom = new Person("Tom");
// підписуємось на подію
tom.MoveEvent += () => Console.WriteLine($"{tom.Name} is moving");
tom.Move();
interface IMovable
{
    protected internal void Move();
    protected internal string Name { get;}
    delegate void MoveHandler();
    protected internal event MoveHandler MoveEvent;
}
class Person : IMovable
{
    string name;
    // явна реалізація події - додатково створюється змінна
    IMovable.MoveHandler? moveEvent;
    event IMovable.MoveHandler IMovable.MoveEvent
    {
        add => moveEvent += value;
        remove => moveEvent -= value;
    }
// явна реалізація властивості - як автовластивості
string IMovable.Name { get => name; }
public Person(string name) => this.name = name;
// явна реалізація методу
void IMovable.Move()
{
    Console.WriteLine($"{name} is walking");
    moveEvent?.Invoke();
}
}
```

В даному випадку знову ж таки треба враховувати, що безпосередньо ми можемо звернутися до подібних методів, властивостей та подій через змінну інтерфейсу, але не змінну класу.

### Реалізація інтерфейсів у базових та похідних класах

Якщо клас застосовує інтерфейс, цей клас повинен реалізувати всі методи і властивості інтерфейсу, які не мають реалізації за умовчанням. Однак також можна і не реалізувати методи, зробивши їх абстрактними, переклавши право їх реалізації на похідні класи:

```csharp
interface IMovable
{
    void Move();
}
abstract class Person : IMovable
{
    public abstract void Move();
}
class Driver : Person
{
    public override void Move() => Console.WriteLine("Шофер веде машину");
}
```

При реалізації інтерфейсу враховуються також методи та властивості, успадковані від базового класу. Наприклад:

```csharp
IAction action = new HeroAction();
action.Move(); // Move in BaseAction
interface IAction
{
    void Move();
}
class BaseAction
{
    public void Move() => Console.WriteLine("Move in BaseAction");
}
class HeroAction : BaseAction, IAction { }
```

Тут клас HeroAction реалізує інтерфейс IAction, проте реалізації методу Move з інтерфейсу застосовується метод Move, успадкований від базового класу BaseAction. Таким чином, клас HeroAction може реалізувати метод Move, оскільки цей метод вже визначено у базовому класі BaseAction.

Слід зазначити, що якщо клас одночасно успадковує інший клас і реалізує інтерфейс, як у прикладі вище клас HeroAction, то назва базового класу має бути вказана до реалізованих інтерфейсів:

```csharp
class HeroAction : BaseAction, IAction
```

### Зміна реалізації інтерфейсів у похідних класах

Може скластися ситуація, що базовий клас реалізував інтерфейс, але у класі-спадкоємці необхідно змінити реалізацію цього інтерфейсу. Що робити в цьому випадку? І тут ми можемо використовувати або перевизначення, або приховування методу чи властивості інтерфейсу.

Перший варіант - перевизначення віртуальних/абстрактних методів:

```csharp
interface IAction
{
    void Move();
}
class BaseAction : IAction
{
    public virtual void Move() => Console.WriteLine("Move in BaseAction");
}
class HeroAction : BaseAction
{
    public override void Move() => Console.WriteLine("Move in HeroAction");
}
```

У базовому класі BaseAction реалізований метод інтерфейсу визначено як віртуальний (можна було б зробити його абстрактним), а в похідному класі він перевизначений.

При виклику методу через змінну інтерфейсу, якщо вона посилається на об'єкт похідного класу, використовуватиметься реалізація з похідного класу:

```csharp
BaseAction action1 = new HeroAction();
action1.Move(); // Move in HeroAction
IAction action2 = new HeroAction();
action2.Move(); // Move in HeroAction
```

Другий варіант - приховування методу у похідному класі:

```csharp
interface IAction
{
    void Move();
}
class BaseAction : IAction
{
    public void Move() => Console.WriteLine("Move in BaseAction");
}
class HeroAction : BaseAction
{
    public new void Move() => Console.WriteLine("Move in HeroAction");
}
```

Також використовуємо ці класи:

```csharp
BaseAction action1 = new HeroAction();
action1.Move(); // Move in BaseAction
IAction action2 = new HeroAction();
action2.Move(); // Move in BaseAction
```

Оскільки інтерфейс реалізований саме у класі BaseAction, через змінну action2 можна звернутися лише до реалізації методу Move з базового класу BaseAction.

Третій варіант - повторна реалізація інтерфейсу в класі-спадкоємці:

```csharp
interface IAction
{
    void Move();
}
class BaseAction : IAction
{
    public void Move() => Console.WriteLine("Move in BaseAction");
}
class HeroAction : BaseAction, IAction
{
    public new void Move() => Console.WriteLine("Move in HeroAction");
}
```

У цьому випадку реалізації цього методу з базового класу ігноруватиметься:

```csharp
BaseAction action1 = new HeroAction();
action1.Move(); // Move in BaseAction
IAction action2 = new HeroAction();
action2.Move(); // Move in HeroAction
HeroAction action3 = new HeroAction();
action3.Move(); // Move in HeroAction
```

Також варто зазначити, що у випадку зі змінною action1, як і раніше, діє раніше зв'язування, в силу якого через цю змінну можна викликати реалізацію методу Move тільки з базового класу, який ця змінна представляє.

Четвертий варіант: явна реалізація інтерфейсу:

```csharp
interface IAction
{
    void Move();
}
class BaseAction : IAction
{
    public void Move() => Console.WriteLine("Move in BaseAction");
}
class HeroAction : BaseAction, IAction
{
    public new void Move() => Console.WriteLine("Move in HeroAction");
    // явна реалізація інтерфейсу
    void IAction.Move() => Console.WriteLine("Move in IAction");
}
```

У цьому випадку для змінної IAction буде використовуватися явна реалізація інтерфейсу IAction, а для змінної HeroAction, як і раніше, буде використовуватися неявна реалізація:

```csharp
BaseAction action1 = new HeroAction();
action1.Move(); // Move in BaseAction
IAction action2 = new HeroAction();
action2.Move(); // Move in IAction
HeroAction action3 = new HeroAction();
action3.Move(); // Move in HeroAction
```
