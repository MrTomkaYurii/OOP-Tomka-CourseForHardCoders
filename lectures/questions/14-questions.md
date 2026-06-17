---
chapter: 14
chapterTitle: "Розділ 14. Рефлексія"
type: self-assessment
---

# Питання для самоконтролю — Розділ 14. Рефлексія

## 14.1. Введення у рефлексію. Клас System.Type

1. Що таке рефлексія і що робить її можливою у .NET? Чому збірки `.dll` і `.exe` містять не лише IL-код, але й метадані?

2. Назвіть п'ять реальних інструментів або фреймворків (DI-контейнери, ORM, тестові фреймворки), які використовують рефлексію «під капотом». Поясніть, для чого саме вона їм потрібна.

3. В чому різниця між трьома способами отримати об'єкт `Type`:
   - `typeof(PatientRecord)`
   - `patient.GetType()`
   - `Type.GetType("PatientRecord")`
   Коли кожен із них є єдиним або кращим вибором?

4. Що виведе наступний код? Поясніть результат:
   ```csharp
   object obj = new InpatientRecord("R001", 7);
   Console.WriteLine(obj.GetType().Name);
   Console.WriteLine(typeof(MedicalRecord).Name);
   Console.WriteLine(obj.GetType() == typeof(MedicalRecord));
   ```
   *(де `InpatientRecord` успадковує `MedicalRecord`)*

5. Яке головне застереження щодо продуктивності рефлексії? В яких частинах програми вона доречна, а в яких — ні?

6. Що повертає `GetInterfaces()` і чому кожний елемент масиву є об'єктом `Type`, а не рядком?

7. Що повертає `Type.IsAssignableFrom(other)` і чим це відрізняється від `other.IsSubclassOf(type)`? Напишіть перевірку, яка визначає, чи реалізує тип `t` інтерфейс `IDisposable`.

8. Спроєктуйте функцію `PrintTypeInfo(Type t)`, яка виводить: ім'я типу, чи є він класом/структурою/інтерфейсом, базовий клас і список реалізованих інтерфейсів.

---

## 14.2. Застосування рефлексії та дослідження типів

1. Що таке `MemberInfo` і чому `GetMembers()` повертає саме цей тип, а не конкретніші `MethodInfo` чи `FieldInfo`?

2. Поясніть різницю між `DeclaringType` та `ReflectedType` для члена типу. Наведіть конкретний приклад з ієрархією класів, де вони відрізняються.

3. Що таке `BindingFlags`? Чому при явній передачі прапорців потрібно вказувати всі потрібні категорії (наприклад, і `Public`, і `Instance`)?

4. Що виведе наступний код і чому `name` не з'являється у списку?
   ```csharp
   Type t = typeof(Person);
   foreach (var m in t.GetMembers())
       Console.WriteLine($"{m.MemberType} {m.Name}");

   public class Person
   {
       string name;
       public int Age { get; set; }
   }
   ```

5. Що таке «backing field» автовластивості (`<Name>k__BackingField`)? Як його виявити через рефлексію і чому потрібно вміти відрізняти backing fields від звичайних полів?

6. Напишіть код, який отримує тільки **власні** (не успадковані) публічні та приватні методи-екземпляри класу `PatientRecord`, використовуючи правильну комбінацію `BindingFlags`.

7. Чому `GetMember("AddNote")` може повернути масив з кількох елементів? Як отримати конкретне перевантаження методу, якщо потрібна версія з параметрами `(string, DateTime)`?

8. Опишіть практичний сценарій, де необхідно динамічно аналізувати структуру невідомого класу (наприклад, у системі звітності або серіалізатора), і поясніть, який набір `BindingFlags` підходить для отримання повної картини типу.

---

## 14.3. Дослідження методів та конструкторів за допомогою рефлексії

1. Що таке `MethodInfo`? Які властивості дозволяють визначити, є метод `public`, `private`, `static`, `virtual` або `abstract`?

2. Що таке `IsSpecialName` для методів і для чого воно потрібне? Чому при виведенні списку методів типу часто фільтрують `!m.IsSpecialName`?

3. Що виведе наступний код? Який тип результату і чому?
   ```csharp
   var patient = new PatientRecord("Іван", new DateTime(1985, 1, 1));
   MethodInfo m = typeof(PatientRecord).GetMethod("GetSummary")!;
   object? result = m.Invoke(patient, null);
   Console.WriteLine(result?.GetType().Name);
   ```

4. Що таке `TargetInvocationException` і чому CLR перегортає реальне виключення в цю обгортку? Як правильно «розпакувати» справжнє виключення?

5. В чому різниця між `ConstructorInfo.Invoke` і `Activator.CreateInstance`? Назвіть сценарій, де краще використовувати кожен із підходів.

6. Що таке `.cctor` (статичний конструктор) з точки зору рефлексії? Чому його можна побачити через `GetConstructors`, але не можна викликати через `Invoke`?

7. Напишіть код, який динамічно викликає метод `SetBmi(decimal)` для масиву пацієнтів, кешуючи `MethodInfo` у статичне поле, а не шукаючи його щоразу всередині циклу.

8. Що таке `MethodInfo.CreateDelegate` і яку перевагу він дає порівняно з `Invoke`? Для якого сценарію використання делегат є кращим вибором: одноразовий виклик чи виклик у циклі на тисячах об'єктів?

---

## 14.4. Дослідження полів та властивостей за допомогою рефлексії

1. В чому принципова відмінність між `FieldInfo` і `PropertyInfo`? Чому властивість — це абстракція, а не просто «поле з доступом»?

2. Що виведе наступний код і чому?
   ```csharp
   public class Patient
   {
       public const int MaxAge = 150;
       public readonly string Ward = "Cardiology";
   }

   var fi = typeof(Patient).GetFields(BindingFlags.Public | BindingFlags.Static | BindingFlags.Instance);
   foreach (var f in fi)
       Console.WriteLine($"{f.Name}: IsLiteral={f.IsLiteral}, IsInitOnly={f.IsInitOnly}");
   ```

3. Як прочитати значення приватного поля `_bmi` об'єкта через рефлексію? Напишіть код із правильним `BindingFlags`.

4. Що таке `init`-аксесор у C# 9 і чому `PropertyInfo.CanWrite` може вводити в оману? Як обійти обмеження `init` через `FieldInfo.SetValue`?

5. Як прочитати значення статичного поля через `FieldInfo.GetValue(null)`? Що означає `null` як аргумент у цьому контексті?

6. Назвіть три реальні сценарії застосування `PropertyInfo.GetValue` і `PropertyInfo.SetValue` у відомих вам фреймворках або бібліотеках.

7. Напишіть метод `static void PrintProperties(object obj)`, який через рефлексію виводить імена і значення всіх публічних властивостей об'єкта. Обробіть випадок, коли `CanRead = false`.

8. Спроєктуйте спрощений клонувальник `ShallowClone<T>(T source)`, який через `FieldInfo` копіює всі поля (крім `const`) у новий об'єкт, створений без конструктора через `FormatterServices.GetUninitializedObject`. Поясніть, чому `const`-поля (IsLiteral) потрібно пропускати.

---

## 14.5. Динамічне завантаження збірок та пізнє зв'язування

1. В чому різниця між статичним і динамічним завантаженням збірок? Який сценарій вимагає динамічного завантаження?

2. Порівняйте `Assembly.LoadFrom(path)` і `Assembly.LoadFile(path)`. В яких ситуаціях кожен із них використовується і в чому їхня різниця у вирішенні залежностей?

3. Що таке `AssemblyLoadContext` (ALC) і яку проблему він вирішує порівняно з `AppDomain` у .NET Framework? Що означає `isCollectible: true`?

4. Чому `GetTypes()` може кинути `ReflectionTypeLoadException` і як правильно обробити цю ситуацію? Яка альтернатива є надійнішою?

5. Опишіть 6 кроків плагінної архітектури через рефлексію: від визначення інтерфейсу до виклику методів плагіна через цей інтерфейс.

6. Що означає `pluginInterface.IsAssignableFrom(t)` у контексті сканування типів? Чим це відрізняється від `t.IsSubclassOf(pluginInterface)`?

7. Що виведе наступний код? Чому перевірка `!t.IsAbstract && !t.IsInterface` є важливою?
   ```csharp
   Type iface = typeof(IAnalysisPlugin);
   var candidates = assembly.GetExportedTypes()
       .Where(t => iface.IsAssignableFrom(t));
   Console.WriteLine(candidates.Count());
   ```
   *(де збірка містить: `IAnalysisPlugin` (інтерфейс), `BmiPlugin : IAnalysisPlugin`, `AbstractPlugin : IAnalysisPlugin` (abstract))*

8. Поясніть, що потрібно для коректного `Unload()` у `AssemblyLoadContext`. Які три умови мають бути виконані? Що відбувається, якщо хоч одна не виконана?

---

## 14.6. Атрибути у .NET

1. Що таке атрибут у .NET? Від якого класу успадковують всі атрибути і де зберігаються їхні дані після компіляції?

2. Поясніть різницю між позиційними аргументами атрибута та іменованими аргументами:
   ```csharp
   [MedRange(10.0, 60.0, Message = "ІМТ поза нормою")]
   ```
   Які з цих аргументів потрапляють у конструктор, а які — у властивості?

3. Що таке `[AttributeUsage]`? Поясніть, що задають параметри `AttributeTargets`, `AllowMultiple` і `Inherited`.

4. Що виведе наступний код і чому?
   ```csharp
   [AttributeUsage(AttributeTargets.Class, Inherited = true)]
   public sealed class MarkerAttribute : Attribute { }

   [Marker]
   public class Base { }
   public class Derived : Base { }

   Console.WriteLine(typeof(Derived).IsDefined(typeof(MarkerAttribute), true));
   Console.WriteLine(typeof(Derived).IsDefined(typeof(MarkerAttribute), false));
   ```

5. Чому рекомендується оголошувати класи атрибутів як `sealed`? Чому за конвенцією назви атрибутів мають суфікс `Attribute`, і як це впливає на синтаксис застосування?

6. Назвіть чотири методи для читання атрибутів через рефлексію і поясніть, чим вони відрізняються. Який із них найшвидший для простої перевірки «чи є атрибут»?

7. Напишіть власний атрибут `[MedRequired]` і клас-валідатор, який через рефлексію перевіряє всі публічні властивості об'єкта і повертає список назв властивостей, що мають цей атрибут, але значення яких є `null` або порожнім рядком.

8. Порівняйте `GetCustomAttribute<T>()` і `GetCustomAttributesData()`. Коли варто використовувати другий метод? Наведіть приклад ситуації, де важливо отримати дані атрибута **без** виклику його конструктора.
