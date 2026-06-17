---
chapter: 16
chapterTitle: "Розділ 16. Паралельне програмування та TPL"
type: self-assessment
---

# Питання для самоконтролю — Розділ 16. Паралельне програмування та TPL

## 16.1. Клас Task. Основи TPL

1. Що таке TPL і яку проблему вона вирішує порівняно з прямим використанням класу `Thread`? Поясніть концепцію пулу потоків (ThreadPool) і чому він ефективніший за постійне створення нових потоків.

2. Порівняйте три способи створення завдання: `new Task(...) + Start()`, `Task.Factory.StartNew()` і `Task.Run()`. Коли кожен з них є доцільним вибором?

3. Що виведе наступний код? Чи гарантований порядок виводу?
   ```csharp
   Task t = Task.Run(() =>
   {
       Console.WriteLine($"Task: {Task.CurrentId}");
   });
   Console.WriteLine("Main before Wait");
   t.Wait();
   Console.WriteLine("Main after Wait");
   ```

4. Поясніть різницю між `Task.WaitAll` і `Task.WaitAny`. Для яких клінічних сценаріїв підходить кожен? Що повертає `WaitAny` і що відбувається з рештою завдань після повернення?

5. Які стани описує перерахування `TaskStatus`? Намалюйте (або опишіть словами) граф переходів між станами від `Created` до термінального стану.

6. Що відбудеться, якщо завдання кине виняток, а виклик `Wait()` відбудеться? Яким типом буде виняток, що прилетить до `catch`? Як отримати оригінальне повідомлення про помилку?

7. Що робить `Task.RunSynchronously()`? В яких сценаріях він корисний і що є його обмеженнями?

8. Метод `Task.CurrentId` повертає `null` поза завданням. Напишіть невеликий приклад, що демонструє, де `Task.CurrentId` дорівнює `null`, а де — числовому значенню.

---

## 16.2. Вкладені завдання та масиви завдань. Task<T>

1. Що таке вкладене (nested) завдання і яка його поведінка за замовчуванням щодо батьківського? Чому батьківське завдання може завершитись раніше вкладеного?

2. Що означає `TaskCreationOptions.AttachedToParent`? Як ця опція змінює взаємозалежність між батьківським і дочірнім завданням? Як поширюються виключення дочірнього завдання?

3. Порівняйте поведінку наступних двох фрагментів:
   ```csharp
   // Фрагмент A
   Task parent = Task.Factory.StartNew(() =>
   {
       Task.Factory.StartNew(() => { Thread.Sleep(500); Console.WriteLine("Inner"); });
       Console.WriteLine("Outer done");
   });
   parent.Wait();
   Console.WriteLine("Main done");

   // Фрагмент B — те саме, але з AttachedToParent
   Task parent = Task.Factory.StartNew(() =>
   {
       Task.Factory.StartNew(() => { Thread.Sleep(500); Console.WriteLine("Inner"); },
           TaskCreationOptions.AttachedToParent);
       Console.WriteLine("Outer done");
   });
   parent.Wait();
   Console.WriteLine("Main done");
   ```
   Опишіть порядок виводу для обох фрагментів.

4. Що повертає властивість `Result` у `Task<T>`? Чому звернення до `Result` може заблокувати поточний потік? Коли звернення до `Result` після `Task.WaitAll` не є блокуючим?

5. Напишіть код, що паралельно запускає три `Task<string>`, потім через `Task.WaitAll` чекає завершення всіх і виводить результати у порядку їх оголошення (не обов'язково завершення).

6. Розробіть клас `LabResult` з полями `PatientName`, `Glucose`, `Hemoglobin` і метод `Task<LabResult> RunLabAsync(string name)`. Запустіть завдання для 4 пацієнтів паралельно, дочекайтесь всіх і виведіть зведену таблицю результатів.

7. Якщо один із Task у масиві `Task<T>[]` завершився з виключенням, що станеться при зверненні до `task.Result` після `WaitAll`? Як безпечно отримати результати тільки успішних завдань?

---

## 16.3. Продовження завдань. ContinueWith

1. Що таке завдання-продовження (continuation task)? Яку перевагу воно дає над `Wait()` + новий `Task.Run()`?

2. Який параметр отримує делегат у `ContinueWith`? Що через нього можна дізнатись про попереднє завдання?

3. Що виведе наступний код і в якому порядку?
   ```csharp
   Task<int> t = Task.Run(() => { Thread.Sleep(100); return 42; });
   Task t2 = t.ContinueWith(prev => Console.WriteLine($"Результат: {prev.Result}"));
   t2.Wait();
   Console.WriteLine("Головний потік");
   ```

4. Поясніть `TaskContinuationOptions.OnlyOnRanToCompletion` і `TaskContinuationOptions.OnlyOnFaulted`. У якому стані опиниться продовження, якщо умова не виконалась? Яке виключення кине `WaitAll` у цьому випадку?

5. Побудуйте ланцюг із чотирьох кроків через `ContinueWith` (реєстрація → огляд → аналізи → призначення), де кожен крок повертає результат типу `string`, що передається наступному. Використовуйте `Task<string>` і `ContinueWith<string>`.

6. Що таке `TaskCompletionSource<T>`? У яких трьох сценаріях він корисний? Поясніть різницю між `SetResult` і `TrySetResult`.

7. Реалізуйте функцію `Task<string> WrapCallbackAsync(Action<string> callback)`, що перетворює callback-based API в Task-based за допомогою `TaskCompletionSource`. Покажіть, як `SetResult` і `SetException` відповідають різним сценаріям callback.

8. Знайдіть потенційну проблему в наступному коді:
   ```csharp
   Task step1 = Task.Run(() => throw new Exception("fail"));
   Task step2 = step1.ContinueWith(t => Console.WriteLine("Success"));
   step2.Wait();
   ```
   Чи виконається `step2`? Чому? Як виправити за допомогою `TaskContinuationOptions`?

---

## 16.4. Клас Parallel

1. Яка головна відмінність між `Parallel` і ручним управлінням завданнями через `Task.Run`? У яких сценаріях `Parallel` є зручнішим вибором?

2. Що гарантує `Parallel.Invoke` щодо завершення переданих дій? Чи гарантується порядок виконання? Чи гарантується, що кожна дія виконається в окремому потоці?

3. Порівняйте `Parallel.For` і `Parallel.ForEach`. Яка різниця в типах даних, з якими вони працюють? Що повертає `ParallelLoopResult` і які його властивості?

4. Що станеться, якщо написати `break` у тілі лямбди у `Parallel.For`? Як правильно перервати виконання паралельного циклу?

5. Поясніть різницю між `ParallelLoopState.Break()` і `ParallelLoopState.Stop()`. Після якого методу `IsCompleted` буде `false`? Коли `LowestBreakIteration` має значення?

6. Що означає `MaxDegreeOfParallelism = 1` у `ParallelOptions`? Коли це корисно? Що означає `MaxDegreeOfParallelism = -1`?

7. Знайдіть проблему в наступному коді і поясніть, як її виправити:
   ```csharp
   int total = 0;
   Parallel.For(0, 1000, i =>
   {
       total++; // небезпечно
   });
   Console.WriteLine(total);
   ```

8. Спроєктуйте паралельне обчислення ризику для списку пацієнтів через `Parallel.ForEach`. Реалізуйте зупинку при виявленні першого пацієнта з критичним показником через `ParallelLoopState.Stop()`. Чому після зупинки результат може містити пацієнтів з індексом вище за той, на якому викликали `Stop()`?

---

## 16.5. Скасування завдань. CancellationToken

1. Що таке кооперативне скасування? Чому `Thread.Abort()` є небезпечним і чому він вилучений з .NET 5+?

2. Поясніть розподіл ролей між `CancellationTokenSource` і `CancellationToken`. Чому завдання отримує лише `CancellationToken`, а не `CancellationTokenSource`?

3. У чому різниця між м'яким скасуванням (через `IsCancellationRequested`) і жорстким (через `ThrowIfCancellationRequested`)? Який стан отримає Task після кожного варіанту скасування — `RanToCompletion` чи `Canceled`?

4. Що виведе наступний код?
   ```csharp
   CancellationTokenSource cts = new CancellationTokenSource();
   Task task = Task.Run(() =>
   {
       for (int i = 0; i < 10; i++)
       {
           cts.Token.ThrowIfCancellationRequested();
           Thread.Sleep(100);
           Console.WriteLine($"Step {i}");
       }
   }, cts.Token);
   Thread.Sleep(250);
   cts.Cancel();
   try { task.Wait(); } catch (AggregateException ae)
   {
       Console.WriteLine(ae.InnerException?.GetType().Name);
   }
   Console.WriteLine(task.Status);
   ```

5. Що робить `CancellationToken.Register()`? У якому потоці виконується зареєстрований делегат? Для яких задач він корисний?

6. Як реалізувати тайм-аут для завдання за допомогою `CancelAfter`? Напишіть приклад, де завдання скасовується через 500 мс, якщо не завершилось раніше.

7. Що таке пов'язані токени (`CreateLinkedTokenSource`)? Наведіть приклад, де операція може бути скасована двома незалежними причинами: за тайм-аутом і за запитом користувача. Як після скасування визначити, яка саме причина спрацювала?

8. Передайте `CancellationToken` у `Parallel.ForEach` через `ParallelOptions`. Яке виключення кине `Parallel` при скасуванні? Порівняйте це з поведінкою при скасуванні звичайного `Task.Run()`.
