---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 4
number: "7.4"
title: "Успадкування інтерфейсів"
source: "../_combined/42-uspadkuvannia-interfeisiv.md"
---

## 7.4. Успадкування інтерфейсів

Інтерфейси, як і класи, можуть успадковуватися:

```csharp
interface IAction
{
    void Move();
}
interface IRunAction : IAction
{
    void Run();
}
class BaseAction : IRunAction
{
    public void Move()
    {
        Console.WriteLine("Move");
    }
public void Run()
{
    Console.WriteLine("Run");
}
}
```

При застосуванні цього інтерфейсу клас BaseAction повинен буде реалізувати як методи та властивості інтерфейсу IRunAction, так і методи та властивості базового інтерфейсу IAction, якщо ці методи та властивості не мають реалізації за умовчанням.

Однак, на відміну від класів, ми не можемо застосовувати до інтерфейсів модифікатор sealed, щоб заборонити успадкування інтерфейсів.

Також ми не можемо застосовувати до інтерфейсів модифікатор abstract, оскільки інтерфейс фактично, як правило, надає абстрактний функціонал, який має бути реалізований у класі чи структурі (за винятком методів та властивостей із реалізацією за умовчанням).

Однак методи інтерфейсів можуть використовувати ключове слово new для приховування методів базового інтерфейсу:

```csharp
IAction action1 = new RunAction();
action1.Move(); // I am moving
IRunAction action2 = new RunAction();
action2.Move(); // I am running
interface IAction
{
    void Move() => Console.WriteLine("I am moving");
}
interface IRunAction : IAction
{
    // приховуємо реалізацію IAction
    new void Move() => Console.WriteLine("I am running");
}
class RunAction : IRunAction { }
```

Тут метод Move із IRunAction приховує метод Move із базового інтерфейсу IAction. Це має сенс, якщо в базовому інтерфейсі визначено реалізацію за умовчанням, як вище, яку потрібно перевизначити. І якщо змінна представляє тип IRunAction, то для методу Move викликається реалізація цього інтерфейсу:

```csharp
IRunAction action2 = new RunAction();
action2.Move(); // I am running
```

Інакше якщо змінна є типом IAction, то для методу Move застосовується реалізація цього інтерфейсу:

```csharp
IAction action1 = new RunAction();
action1.Move(); // I am moving
```

Але клас RunAction може перевизначити метод Move для обох інтерфейсів.

```csharp
IAction action1 = new RunAction();
action1.Move(); // I am tired
IRunAction action2 = new RunAction();
action2.Move(); // I am tired
interface IAction
{
    void Move() => Console.WriteLine("I am moving");
}
interface IRunAction : IAction
{
    new void Move() => Console.WriteLine("I am running");
}
class RunAction : IRunAction
{
    public void Move() => Console.WriteLine("I am tired");
}
```

При наслідуванні інтерфейсів слід враховувати, що, як і при наслідуванні класів, похідний інтерфейс повинен мати той самий рівень доступу або більш суворий, ніж базовий інтерфейс. Наприклад:

```csharp
public interface IAction
{
    void Move();
}
internal interface IRunAction : IAction
{
    void Run();
}
```

Але не навпаки. Наприклад, у наступному випадку ми отримаємо помилку, і програма не скомпілюється, оскільки похідний інтерфейс має менш суворий рівень доступу, ніж базовий:

```csharp
internal interface IAction
{
    void Move();
}
public interface IRunAction : IAction // Помилка IRunAction може бути лише internal
{
    void Run();
}
```
