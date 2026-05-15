
## 8.3. Перевантаження операцій перетворення типів

У минулій темі було розглянуто тему перевантаження операторів. І з цією темою тісно пов'язана тема перевантаження операторів перетворення типів.

Раніше ми розглядали явні та неявні перетворення примітивних типів. Наприклад:

```csharp
int x = 50;
byte y = (byte)x; // явне перетворення від int до byte
int z = y; // неявне перетворення від byte до int
```
було б непогано мати можливість визначати логіку перетворення одних типів на інші. І за допомогою перевантаження операторів ми можемо це робити. Для цього у класі визначається метод наступної форми:

```csharp
public static implicit|explicit operator Тип_в_який_потрібно_перетворити(вихідний_тип param)
{
    // логіка перетворення
}
```
Після модифікаторів public static йде ключове слово explicit (якщо явне перетворення, тобто потрібна операція приведення типів) або implicit (якщо перетворення неявне). Потім йде ключове слово operator і далі тип, що повертається, в який треба перетворити об'єкт. У дужках як параметр передається об'єкт, який треба перетворити.

Наприклад, нехай ми маємо наступний клас Counter, який представляє лічильник-секундомір і який зберігає кількість секунд у властивості Seconds:

```csharp
class Counter
{
    public int Seconds { get; set; }
    public static implicit operator Counter(int x)
    {
        return new Counter { Seconds = x };
    }
    public static explicit operator int(Counter counter)
    {
        return counter.Seconds;
    }
}
```
Перший оператор перетворює число - об'єкт типу int до типу Counter. Його логіка проста – створюється новий об'єкт Counter, у якого встановлюється властивість Seconds.

Другий оператор перетворює об'єкт Counter до типу int, тобто отримує з Counter число.

Застосування операторів перетворення у програмі:

```csharp
Counter counter1 = new Counter { Seconds = 23 };
int x = (int)counter1;
Console.WriteLine(x); // 23
Counter counter2 = x;
Console.WriteLine(counter2.Seconds); // 23
```
Оскільки операція перетворення з Counter на int визначена з ключовим словом explicit, тобто як явне перетворення, то в цьому випадку необхідно застосувати операцію приведення типів:

```csharp
int x = (int)counter1;
```
У випадку з операцією перетворення від int до Counter нічого подібного робити не треба, оскільки ця операція визначена з ключовим словом implicit, тобто як неявна. Які операції перетворення робити явними, а які неявні, у цьому разі не настільки важливо, це вирішує розробник на власний розсуд.

Слід враховувати, що оператор перетворення типів повинен перетворювати з типу чи до типу, у якому цей оператор визначено. Тобто оператор перетворення, визначений у типі Counter, повинен або приймати як параметр об'єкт типу Counter, або повертати об'єкт типу Counter.

Розглянемо також складніші перетворення, наприклад, з одного складового типу в інший складовий тип. Допустимо, у нас є ще клас Timer:

```csharp
class Timer
{
    public int Hours { get; set; }
    public int Minutes { get; set; }
    public int Seconds { get; set; }
}
class Counter
{
    public int Seconds { get; set; }
    public static implicit operator Counter(int x)
    {
        return new Counter { Seconds = x };
    }
    public static explicit operator int(Counter counter)
    {
        return counter.Seconds;
    }
    public static explicit operator Counter(Timer timer)
    {
        int h = timer.Hours * 3600;
        int m = timer.Minutes * 60;
        return new Counter { Seconds = h + m + timer.Seconds };
    }
    public static implicit operator Timer(Counter counter)
    {
        int h = counter.Seconds / 3600;
        int m = (counter.Seconds % 3600) / 60;
        int s = counter.Seconds % 60;
        return new Timer { Hours = h, Minutes = m, Seconds = s };
    }
}
```
Клас Timer представляє умовний таймер, який зберігає години, хвилини та секунди. Клас Counter представляє умовний лічильник-секундомір, який зберігає кількість секунд. Виходячи з цього ми можемо визначити деяку логіку перетворення з одного типу до іншого, тобто отримання секунд в об'єкті Counter з годин, хвилин і секунд в об'єкті Timer. Наприклад, 3675 секунд по суті це 1 година, 1 хвилина та 15 секунд

Застосування операцій перетворення:

```csharp
Counter counter1 = new Counter { Seconds = 115 };
Timer timer = counter1;
Console.WriteLine($"{timer.Hours}:{timer.Minutes}:{timer.Seconds}");
Counter counter2 = (Counter)timer;
Console.WriteLine(counter2.Seconds); // 115
```
