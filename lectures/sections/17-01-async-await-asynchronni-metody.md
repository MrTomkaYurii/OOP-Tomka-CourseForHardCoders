---
chapter: 17
chapterTitle: "Розділ 17. Асинхронне програмування"
section: 1
number: "17.1"
title: "async та await. Асинхронні методи"
source: ""
---

## 17.1. async та await. Асинхронні методи

Асинхронне програмування — один з найважливіших концептів сучасної розробки програмного забезпечення. Щоб зрозуміти, навіщо воно існує, почнімо з проблеми, яку воно вирішує.

## Проблема: блокуючий ввід-вивід

Більшість програм значну частину часу **чекають**: чекають відповіді від бази даних, чекають завантаження файлу з диску, чекають відповіді від зовнішнього API. У синхронному коді під час такого очікування потік просто заморожується — він не виконує жодної корисної роботи, але займає пам'ять і ресурс ОС.

Уявімо клінічну інформаційну систему. При синхронному підході: реєстратор запитує медичну картку пацієнта → програма чекає відповіді від бази даних (200 мс) → потік заблокований, інтерфейс завис. За 200 мс можна було зареєструвати ще трьох пацієнтів.

Ця проблема стає критичною у веб-застосунках: якщо сервер обслуговує тисячі одночасних запитів і кожен блокує потік на час очікування бази даних — сервер швидко вичерпає пул потоків і перестане відповідати.

**Асинхронність вирішує цю проблему радикально**: замість того щоб блокувати потік на час очікування, програма «відпускає» потік займатися іншою роботою. Коли очікувана операція завершується — потік (можливо, інший) повертається і продовжує виконання з того місця, де зупинився.

## Ключові слова async та await

C# надає дві ключові синтаксичні конструкції для асинхронного програмування:

**`async`** — модифікатор, що додається до заголовку методу. Він повідомляє компілятору, що цей метод є асинхронним і може містити вирази `await`. Важливо: **сам по собі `async` не робить метод асинхронним**. Це лише дозволяє використовувати `await` усередині.

**`await`** — оператор, що застосовується до об'єкта `Task` або `Task<T>`. Він каже: «зупинись тут, передай управління назад викликаючому коду, і продовж виконання цього методу тоді, коли Task завершиться». `await` може використовуватись **виключно всередині методу з модифікатором `async`**.

![Модель виконання async/await: що відбувається з потоком](_assets/17-01/async-await-flow.png)

Ключова відмінність від блокування: при `await` поточний потік **не зависає в очікуванні** — він повертається у пул потоків (або продовжує виконувати інші задачі). Коли очікувана операція завершується, .NET планувальник призначає продовження методу — можливо, тому ж потоку, а можливо, іншому з пулу.

## Оголошення асинхронного методу

Асинхронний метод визначається за такими ознаками:
- Модифікатор `async` у заголовку
- Хоча б один вираз `await` у тілі
- Тип повернення: `void`, `Task`, `Task<T>` або `ValueTask<T>`
- За угодою — суфікс `Async` у назві

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

// Виклик асинхронного методу
await LoadPatientCardAsync("PT-2024-001");
Console.WriteLine("[Main] Метод Main продовжує виконання після await");

// Асинхронний метод: async + Task + Async-суфікс
async Task LoadPatientCardAsync(string patientId)
{
    Console.WriteLine($"[LoadPatient] Запит до бази даних: {patientId}");
    await Task.Delay(500); // імітуємо мережевий запит (не блокує потік!)
    Console.WriteLine($"[LoadPatient] Картка {patientId} завантажена");
}
```

## Task.Delay vs Thread.Sleep

`Task.Delay` — асинхронна затримка, обов'язково вживається з `await`. На відміну від `Thread.Sleep`, вона **не блокує потік** — потік звільняється під час очікування.

```csharp run
using System;
using System.Threading;
using System.Threading.Tasks;

Console.WriteLine("=== Thread.Sleep (блокує потік) ===");
Console.WriteLine($"До Sleep: потік {Thread.CurrentThread.ManagedThreadId.ToString()}");
Thread.Sleep(100); // потік ЗАМОРОЖЕНО на 100мс
Console.WriteLine($"Після Sleep: потік {Thread.CurrentThread.ManagedThreadId.ToString()}");

Console.WriteLine("\n=== Task.Delay (звільняє потік) ===");
Console.WriteLine($"До Delay: потік {Thread.CurrentThread.ManagedThreadId.ToString()}");
await Task.Delay(100); // потік ЗВІЛЬНЕНИЙ під час очікування
Console.WriteLine($"Після Delay: потік {Thread.CurrentThread.ManagedThreadId.ToString()}");
// ID може відрізнятися — продовжив інший потік з пулу!
```

## Як async/await влаштований під капотом

Коли компілятор зустрічає метод з `async`, він перетворює його на **стейт-машину** (state machine) — клас, що зберігає стан виконання між точками `await`. Кожна точка `await` — це стан, де метод може «припинитись» і «продовжитись» пізніше.

Спрощено: оригінальний асинхронний метод:

```csharp
async Task DoWorkAsync()
{
    Console.WriteLine("Крок 1");
    await Task.Delay(200);
    Console.WriteLine("Крок 2");
    await Task.Delay(100);
    Console.WriteLine("Крок 3");
}
```

Компілятор генерує стейт-машину з трьома станами: State 0 (до першого await), State 1 (після першого await), State 2 (після другого await). При кожному `await` метод зберігає поточний стан і повертає управління; коли Task завершується, відновлення виконання планується з правильного стану. Розробнику не потрібно писати цей код вручну — `async/await` є синтаксичним цукром поверх цієї механіки.

## Паралельний запуск асинхронних методів

Часта помилка: `await` кожного методу по черзі, коли методи насправді незалежні:

```csharp run
using System;
using System.Threading.Tasks;

// НЕЕФЕКТИВНО: послідовний await — загальний час = сума всіх
Console.WriteLine("=== Послідовно (неефективно) ===");
var sw1 = System.Diagnostics.Stopwatch.StartNew();
await RunTestAsync("Аналіз крові",   400);
await RunTestAsync("Аналіз сечі",    250);
await RunTestAsync("ЕКГ",            300);
sw1.Stop();
Console.WriteLine($"Послідовно: {sw1.ElapsedMilliseconds.ToString()} мс\n");

// ЕФЕКТИВНО: старт всіх → потім await — загальний час = максимум
Console.WriteLine("=== Паралельно (ефективно) ===");
var sw2 = System.Diagnostics.Stopwatch.StartNew();
var t1 = RunTestAsync("Аналіз крові",   400);
var t2 = RunTestAsync("Аналіз сечі",    250);
var t3 = RunTestAsync("ЕКГ",            300);
await t1; await t2; await t3;
sw2.Stop();
Console.WriteLine($"Паралельно: {sw2.ElapsedMilliseconds.ToString()} мс");

async Task RunTestAsync(string name, int ms)
{
    Console.WriteLine($"  → Початок: {name}");
    await Task.Delay(ms);
    Console.WriteLine($"  ✓ Готово:  {name} ({ms.ToString()} мс)");
}
```

Різниця суттєва: послідовно — ~950 мс, паралельно — ~400 мс. Правило: якщо задачі **незалежні** одна від одної — запускайте їх усі, потім очікуйте.

## Асинхронні лямбда-вирази

Лямбди також можуть бути асинхронними — для цього перед параметрами ставиться ключове слово `async`. Тип такої лямбди — `Func<Task>`, `Func<T, Task>`, `Func<Task<TResult>>` тощо:

```csharp run
using System;
using System.Threading.Tasks;

// Async-лямбда без параметрів: Func<Task>
Func<Task> sendAlert = async () =>
{
    Console.WriteLine("[Alert] Надсилаю критичне сповіщення...");
    await Task.Delay(200);
    Console.WriteLine("[Alert] Сповіщення надіслано персоналу");
};

// Async-лямбда з параметром: Func<string, Task>
Func<string, Task> notifyDoctor = async (doctorName) =>
{
    Console.WriteLine($"[Notify] Виклик лікаря: {doctorName}");
    await Task.Delay(150);
    Console.WriteLine($"[Notify] Лікар {doctorName} сповіщений");
};

// Async-лямбда що повертає результат: Func<string, Task<bool>>
Func<string, Task<bool>> checkAvailability = async (room) =>
{
    await Task.Delay(100);
    return room != "Операційна-1"; // операційна зайнята
};

await sendAlert();
await notifyDoctor("Петренко І.О.");
bool available = await checkAvailability("Палата-5");
Console.WriteLine($"Палата-5 вільна: {available.ToString()}");
```

## Суфікс Async — угода іменування

Всі асинхронні методи в .NET мають суфікс `Async` у назві: `ReadAsync`, `WriteAsync`, `GetAsync`, `SendAsync`. Це угода, прийнята в усій екосистемі .NET, яка:
- Відрізняє асинхронну версію від синхронної (`Read` vs `ReadAsync`)
- Нагадує розробнику, що метод потребує `await`
- Дозволяє надавати обидві версії в бібліотеках

```csharp run
using System;
using System.Threading.Tasks;

// Синхронна версія
string LoadPatientCard(string id)
{
    System.Threading.Thread.Sleep(100); // блокує потік
    return $"Картка пацієнта {id}";
}

// Асинхронна версія — суфікс Async
async Task<string> LoadPatientCardAsync(string id)
{
    await Task.Delay(100); // не блокує
    return $"Картка пацієнта {id}";
}

// Синхронний виклик
string card1 = LoadPatientCard("PT-001");
Console.WriteLine(card1);

// Асинхронний виклик
string card2 = await LoadPatientCardAsync("PT-002");
Console.WriteLine(card2);
```

Бібліотека .NET дотримується цієї угоди скрізь: `File.ReadAllTextAsync`, `HttpClient.GetAsync`, `DbContext.SaveChangesAsync` — якщо є суфікс `Async`, метод поверне `Task` і очікує `await`.
