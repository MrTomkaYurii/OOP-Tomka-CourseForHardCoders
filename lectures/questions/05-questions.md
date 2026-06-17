---
chapter: 5
chapterTitle: "Розділ 5. Обробка винятків"
type: self-assessment
---

# Питання для самоконтролю — Розділ 5. Обробка винятків

## 5.1. Конструкція try..catch..finally

1. Що таке виняток (exception) у C#? Від якого базового класу успадковуються всі класи винятків? Хто і коли створює об'єкт винятку?

2. Опишіть порядок виконання блоків `try`, `catch`, `finally` у двох сценаріях: коли виняток виникає і коли не виникає.

3. Що виведе наступний код?

   ```csharp
   try
   {
       Console.WriteLine("try");
       int x = int.Parse("abc");
       Console.WriteLine("після Parse");
   }
   catch
   {
       Console.WriteLine("catch");
   }
   finally
   {
       Console.WriteLine("finally");
   }
   Console.WriteLine("після блоку");
   ```

4. Чи виконається `finally`, якщо у `catch` теж виник виняток? Чи виконається `finally`, якщо у `try` вжито `return`?

5. Поясніть механізм **поширення винятку по стеку викликів**. Якщо метод `A` викликає `B`, який викликає `C`, а виняток виникає в `C` — де він може бути перехоплений?

6. Порівняйте два підходи: `try { int age = int.Parse(s); }` і `if (int.TryParse(s, out int age))`. Коли перший підхід кращий, коли другий? Чому не варто використовувати `try...catch` для передбачуваних сценаріїв?

7. Для чого може використовуватись `try...finally` без блоку `catch`? Наведіть приклад, де це потрібно, і поясніть: чи перехоплює така конструкція виняток?

8. Спроєктуйте метод `ParseAndRegister(string name, string ageStr)`, який парсить вік, реєструє пацієнта і гарантує виведення рядка `"Операцію завершено"` у будь-якому разі — навіть при помилці. Використайте `try...catch...finally`.

---

## 5.2. Блок catch та фільтри винятків

1. Чим відрізняються три форми блоку `catch`? Запишіть синтаксис кожної і поясніть, що перехоплює кожна.

2. Що виведе наступний код?

   ```csharp
   try
   {
       string s = null;
       Console.WriteLine(s.Length);
   }
   catch (FormatException)
   {
       Console.WriteLine("FormatException");
   }
   catch (NullReferenceException ex)
   {
       Console.WriteLine($"NullRef: {ex.Message}");
   }
   catch (Exception ex)
   {
       Console.WriteLine($"Exception: {ex.Message}");
   }
   ```

3. Якщо поставити `catch (Exception ex)` першим серед кількох блоків `catch`, що станеться? Чи виникне помилка компіляції?

4. Поясніть оператор `when` у блоці `catch`. Що відбувається, якщо тип винятку збігається, але умова `when` повертає `false`?

5. Напишіть метод `ProcessInput(string input)`, що обробляє `FormatException` по-різному: окремо якщо рядок порожній (через `when`) і окремо для всіх інших некоректних значень.

6. Поясніть антипатерн «ковтання винятку» — порожній або беззмістовний блок `catch`. Чому він небезпечний у медичній або фінансовій системі?

7. Розробник написав `catch (ArgumentException)` перед `catch (ArgumentOutOfRangeException)`. Яка проблема? Як виправити?

8. Є три блоки `catch`: `FormatException`, `OverflowException`, `Exception`. Для яких вхідних значень `int.Parse(s)` спрацює кожен з них? Наведіть конкретні приклади рядків-вхідних даних.

---

## 5.3. Типи винятків. Клас Exception

1. Перелічіть і коротко опишіть п'ять властивостей класу `Exception`. Яка з них найчастіше використовується у повідомленнях користувачу?

2. Що виведе `ex.GetType().Name`, якщо `ex` перехоплено через `catch (Exception ex)`, а реальний виняток є `FormatException`?

3. Що таке `InnerException`? Наведіть сценарій, де воно корисне для діагностики помилки.

4. Що виведе цей код і в якому порядку?

   ```csharp
   string input = "999999999999999";
   try
   {
       int val = int.Parse(input);
   }
   catch (OverflowException ex)
   {
       Console.WriteLine($"Overflow: {ex.Message}");
   }
   catch (FormatException ex)
   {
       Console.WriteLine($"Format: {ex.Message}");
   }
   catch (Exception ex)
   {
       Console.WriteLine($"Other: {ex.Message}");
   }
   ```

5. Поясніть правило: «конкретніший тип — раніше». Чому `ArgumentOutOfRangeException` має стояти перед `ArgumentException` у ланцюжку `catch`?

6. Що означає «виняток зупиняє виконання `try`»? Напишіть приклад, де у `try` є три рядки коду, і виняток виникає на другому. Що відбувається з третім рядком?

7. Як `catch (Exception ex)` виступає «страхувальним мережем»? Чи слід його завжди додавати? В яких ситуаціях він обов'язковий, а в яких зайвий?

8. Для яких ситуацій призначені такі типи винятків: `NullReferenceException`, `IndexOutOfRangeException`, `InvalidCastException`, `ArgumentNullException`? Наведіть по одному рядку коду, що спровокує кожен.

---

## 5.4. Генерація винятку та оператор throw

1. Навіщо генерувати виняток вручну через `throw`? Наведіть приклад бізнес-правила, порушення якого технічно не є помилкою, але потребує `throw`.

2. Чим відрізняються `throw;` (без аргументу) і `throw ex;` (з аргументом) у блоці `catch`? Яку помилку допускають при використанні `throw ex;`?

3. Що виведе цей код?

   ```csharp
   void Process(string name)
   {
       try
       {
           Validate(name);
           Console.WriteLine("OK");
       }
       catch (ArgumentException ex)
       {
           Console.WriteLine($"Caught: {ex.Message}");
       }
   }
   void Validate(string name)
   {
       if (string.IsNullOrEmpty(name))
           throw new ArgumentException("Ім'я порожнє");
   }
   Process("");
   Process("Іван");
   ```

4. Що таке **ланцюжок винятків** (`InnerException`)? Напишіть метод, що перехоплює `FormatException` і загортає його у `InvalidOperationException` зі збереженням оригіналу.

5. Яке призначення оператора `nameof` у `throw new ArgumentOutOfRangeException(nameof(age), ...)`? Що повертає `nameof(age)` і чому це краще, ніж рядок `"age"`?

6. Напишіть метод `SetAge(int age)`, що кидає `ArgumentOutOfRangeException` якщо вік менший за 0 або більший за 150. Загорніть виклик у блок `try...catch` і виведіть повідомлення про помилку разом з некоректним значенням.

7. Розробник написав такий код:

   ```csharp
   catch (Exception ex)
   {
       Log(ex);
       throw ex;
   }
   ```

   Знайдіть помилку і поясніть наслідки. Як виправити?

8. Де правильніше розміщувати `throw` для валідації аргументів: на початку методу чи в середині? Чому так зручніше для читача коду і для відлагодження?

---

## 5.5. Створення класів винятків

1. Чому варто створювати власні класи винятків для доменних помилок, якщо у .NET вже є понад 200 вбудованих типів?

2. Яка мінімальна реалізація необхідна для власного класу винятку? Що обов'язково вказати і навіщо?

3. Від якого класу краще успадковувати власний виняток, якщо він описує некоректний аргумент методу? А якщо стан об'єкта не дозволяє виконати операцію?

4. Що виведе цей код?

   ```csharp
   class AppException : Exception
   {
       public string Code { get; }
       public AppException(string message, string code) : base(message)
       { Code = code; }
   }
   try
   {
       throw new AppException("Недостатньо прав", "AUTH_ERR");
   }
   catch (Exception ex)
   {
       Console.WriteLine(ex.Message);
       if (ex is AppException app)
           Console.WriteLine($"Код: {app.Code}");
   }
   ```

5. Поясніть перевагу зберігання доменних даних у власному виняткові (наприклад, поле `InvalidAge`) порівняно з формуванням рядку `Message`.

6. Спроєктуйте ієрархію винятків для інтернет-магазину: базовий `ShopException` (з полем `OrderId`) та два конкретних — `OutOfStockException` (з `ProductName`) і `PaymentException` (з `Amount`). Напишіть метод обробки замовлення, що кидає обидва типи і ловить їх окремо.

7. Яка конвенція щодо іменування власних класів винятків? Наведіть три правильні і три неправильні назви.

8. Розробник вирішив не створювати власний клас, а покласти всі деталі у рядок `Message`. Порівняйте цей підхід із власним класом з властивостями. Де кожен з них кращий?

---

## 5.6. Пошук блоку catch при обробці винятків

1. Опишіть дві фази роботи CLR при виникненні винятку: фазу **пошуку** і фазу **розкрутки стека**. Що відбувається у кожній фазі і в якому порядку виконуються `finally`-блоки?

2. Дано ланцюжок викликів `Main` → `A` → `B` → `C`. Виняток виникає у `C`. У якому порядку CLR перевіряє рівні стека у фазі пошуку?

3. Що виведе цей код?

   ```csharp
   void A()
   {
       try { B(); }
       catch (FormatException ex) { Console.WriteLine($"A catch: {ex.Message}"); }
       finally { Console.WriteLine("A finally"); }
   }
   void B()
   {
       try { C(); }
       catch (NullReferenceException) { Console.WriteLine("B catch NullRef"); }
       finally { Console.WriteLine("B finally"); }
   }
   void C()
   {
       try { int.Parse("abc"); }
       finally { Console.WriteLine("C finally"); }
   }
   A();
   ```

4. Виняток виник у методі на 3-му рівні стека. `catch` знайдено на 1-му рівні. Які `finally`-блоки виконаються і в якому порядку?

5. Якщо CLR не знаходить відповідного `catch` на жодному рівні стека, що відбувається? Чи гарантовано при цьому виконання `finally`-блоків?

6. Поясніть патерн «логування + перекидання»: `catch (Exception ex) { Log(ex); throw; }`. Чому це краще, ніж повністю ковтати виняток або перехоплювати лише для логування і не перекидати?

7. Зверніть увагу: у прикладі нижче рядок після `try...catch` у `SaveRecord` **не виконується**, хоча у методі є `finally`. Поясніть чому.

   ```csharp
   void SaveRecord(string id, string input)
   {
       try { int age = int.Parse(input); Console.WriteLine("Збережено"); }
       catch (NullReferenceException) { Console.WriteLine("NullRef"); }
       finally { Console.WriteLine("SaveRecord finally"); }
       Console.WriteLine("Після try у SaveRecord"); // коли виконується?
   }
   SaveRecord("P1", "abc");
   ```

8. Спроєктуйте трирівневий ланцюжок: `UI()` → `Service()` → `Repository()`. `Repository` кидає `InvalidOperationException`. `Service` логує помилку через `finally` і перекидає. `UI` перехоплює і відображає повідомлення користувачу. Напишіть повний код і поясніть порядок виконання кожного блоку.
