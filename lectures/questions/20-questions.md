---
chapter: 20
chapterTitle: "Розділ 20. Принципи SOLID"
type: self-assessment
---

# Питання для самоконтролю — Розділ 20. Принципи SOLID

## 20.1. Вступ до SOLID

1. Назвіть 4 симптоми поганого дизайну (за Робертом Мартіном) та поясніть кожен. Чому "жорсткість" (Rigidity) та "крихкість" (Fragility) часто виникають разом?

2. Розгляньте клас:
   ```csharp
   public class ClinicManager
   {
       public void AddPatient(Patient p) { ... }
       public void ScheduleAppointment(int patientId, DateTime dt) { ... }
       public void SendReminderEmail(int appointmentId) { ... }
       public void GeneratePdfReport(List<Appointment> list) { ... }
       public void SaveToDatabase(Patient p) { ... }
       public void ValidateInsurance(Patient p) { ... }
   }
   ```
   Скільки "відповідальностей" у цього класу? Перелічіть їх. Як називається цей антипаттерн?

3. Що таке технічний борг? Наведіть аналогію з реального фінансового боргу. Як накопичення технічного боргу впливає на здатність команди додавати нові функції?

4. Поясніть, як пов'язані між собою принципи SOLID. Чому порушення одного принципу часто означає порушення іншого? Наведіть приклад ланцюгової реакції.

5. Що таке "Immobility" (нерухомість) коду? Чому її важко помітити під час розробки? Наведіть конкретний приклад, де код у одному модулі неможливо перевикористати в іншому через погані залежності.

6. Чому існування класів з суфіксами `Manager`, `Helper`, `Processor`, `Utils` часто є сигналом проблеми дизайну? В яких випадках такі назви все ж є прийнятними?

## 20.2. Single Responsibility Principle

1. SRP стверджує: "клас має мати одну причину для змін". Що означає "причина для змін" і чому вона пов'язана з поняттям "актор"? Чим це відрізняється від "клас має мати лише одну функцію"?

2. Розгляньте клас:
   ```csharp
   public class AppointmentManager
   {
       public void Book(Appointment a) { /* записати в БД */ }
       public void Cancel(int id) { /* видалити з БД */ }
       public void SendConfirmation(Appointment a) { /* відправити email */ }
       public List<Appointment> GetReport(DateTime from, DateTime to) { /* LINQ */ }
   }
   ```
   Визначте акторів, що зацікавлені в цьому класі. Запропонуйте рефакторинг з розподілом по відповідних класах.

3. Студент каже: "Я розбив клас на 5 маленьких — тепер у кожного по одному методу. Це SRP?" Оцініть цю думку. Де межа між правильним розбиттям і надмірною фрагментацією?

4. Клас `Patient` містить:
   ```csharp
   public string Name { get; set; }
   public DateTime BirthDate { get; set; }
   public int CalculateAge() { ... }
   public bool IsAdult() { ... }
   ```
   Чи порушує цей клас SRP? Обґрунтуйте відповідь.

5. Як SRP полегшує написання юніт-тестів? Наведіть конкретний приклад: клас, що порушує SRP, і як це ускладнює тестування; після рефакторингу — як тести спрощуються.

6. Назвіть 4 ознаки порушення SRP у коді. Для кожної наведіть приклад в контексті медичної інформаційної системи.

7. Реалізуйте рефакторинг класу `ReportManager`, що зараз містить: завантаження даних з БД, форматування звіту, відправку на email і збереження PDF. Розбийте на окремі класи з чіткими відповідальностями та покажіть, як вони взаємодіють через оркестратор.

## 20.3. Open/Closed Principle

1. Сформулюйте OCP. Що означає "відкритий для розширення, закритий для модифікації"? Чому обидві частини важливі одночасно?

2. Розгляньте код:
   ```csharp
   public decimal CalculateFee(Appointment a)
   {
       return a.Type switch
       {
           "General" => 100m,
           "Specialist" => 250m,
           "Emergency" => 500m,
           _ => throw new ArgumentException("Unknown type")
       };
   }
   ```
   Яка проблема виникне при додаванні нового типу прийому "Telemedicine"? Як переписати цей код, щоб він відповідав OCP?

3. Поясніть, як паттерн Стратегія (Strategy) реалізує OCP. Намалюйте (текстово) UML-подібну структуру для системи знижок: різні стратегії знижок без зміни класу `BillingService`.

4. Чим паттерн Template Method відрізняється від Strategy у контексті OCP? Наведіть медичний приклад, де Template Method є більш природним вибором.

5. Студент каже: "OCP вимагає робити все через інтерфейс. Я завжди пишу `IService` перед реалізацією." Оцініть це твердження. Що таке "правило трьох" і як воно обмежує надмірне використання OCP?

6. Де OCP найбільш важливий: на початку проєкту чи коли вже є стабільна кодова база? Поясніть зв'язок між OCP і принципом YAGNI (You Aren't Gonna Need It).

7. Реалізуйте систему нотифікацій, що відповідає OCP: базовий клас/інтерфейс `INotificationChannel` та реалізації `EmailNotification`, `SmsNotification`, `PushNotification`. Покажіть, як `NotificationService` відправляє через всі канали без `if`/`switch` по типу.

## 20.4. Liskov Substitution Principle

1. Сформулюйте LSP своїми словами. Чим "підстановна сумісність" відрізняється від звичайної "типової сумісності" в ООП? Наведіть приклад типу, що успадковується, але порушує LSP.

2. Розгляньте класичний приклад:
   ```csharp
   public class Rectangle
   {
       public virtual int Width { get; set; }
       public virtual int Height { get; set; }
       public int Area() => Width * Height;
   }
   public class Square : Rectangle
   {
       public override int Width { set { base.Width = value; base.Height = value; } }
       public override int Height { set { base.Width = value; base.Height = value; } }
   }
   ```
   Напишіть тест, що проходить для `Rectangle`, але падає для `Square`. Чому це порушення LSP?

3. Що таке "контракт" класу в контексті LSP? Поясніть три складові контракту: передумови (preconditions), постумови (postconditions) та інваріанти. Як підклас може (і не може) їх змінювати?

4. Розгляньте код:
   ```csharp
   public class ReadOnlyRecord : MedicalRecord
   {
       public override void Update(string data)
           => throw new NotSupportedException("Record is read-only");
   }
   ```
   Поясніть, чому це порушення LSP, навіть якщо компілятор не скаржиться. Як правильно вирішити цю проблему через розбиття інтерфейсів?

5. Як перевірити, чи дотримується LSP у системі? Опишіть правило "тест базового класу повинен проходити для підкласів". Напишіть клас `AppointmentTests` з тестом, що може перевірити будь-яку реалізацію `IScheduler`.

6. Назвіть 4 типові ознаки порушення LSP у коді. Що сигналізує про проблему: `is`, `as`, `NotSupportedException`, перевірка типу в клієнтському коді?

7. Студент пропонує: "Нехай `ArchiveRecord` успадковується від `MedicalRecord`, але перевизначає `Delete()` як порожній метод — нічого не робить, але й не падає." Чи це виправляє порушення LSP? Обґрунтуйте відповідь.

8. Дизайн задача: є ієрархія `Payment` → `CashPayment`, `CardPayment`, `InsurancePayment`. Клас `InsurancePayment` вимагає попередньої авторизації перед `Process()`. Як спроєктувати ієрархію, щоб не порушувати LSP?

## 20.5. Interface Segregation Principle

1. Сформулюйте ISP. Чому "жирний" інтерфейс є проблемою? Поясніть термін "залежність від непотрібних методів" та її наслідки.

2. Розгляньте інтерфейс:
   ```csharp
   public interface IClinicService
   {
       void RegisterPatient(Patient p);
       Appointment BookAppointment(int patientId);
       void CancelAppointment(int id);
       List<Patient> GetAllPatients();
       Report GenerateMonthlyReport(DateTime month);
       void ExportToExcel(Report report);
       void SendBulkEmail(string message);
   }
   ```
   Визначте "ролі" в цьому інтерфейсі та запропонуйте розбиття на менші інтерфейси.

3. Студент каже: "Я реалізую `IClinicService` в класі `ClinicFacade` — він все одно все реалізовує, тому ISP не потрібен." Що не так у цьому міркуванні?

4. Поясніть концепцію "інтерфейс як роль". Наведіть приклади ролей `ISaveable`, `IAuditable`, `ISendable`. Як один клас може реалізовувати кілька ролей?

5. Розгляньте сценарій: є зовнішня бібліотека `LegacyPatientSystem` з методом `GetAllData()`, що повертає все одразу. Ваш код очікує `IPatientReader` з методом `GetPatient(int id)`. Як адаптер вирішує цю проблему без порушення ISP?

6. Чи суперечить ISP принципу "єдиного місця для зміни"? Тобто: якщо я розбив на 5 інтерфейсів, чи не стане важче вносити зміни? Аргументуйте.

7. Коли ISP не потрібен? Назвіть ситуації, де один великий інтерфейс є кращим вибором ніж кілька дрібних.

## 20.6. Dependency Inversion Principle

1. DIP складається з двох частин. Сформулюйте обидві. Чому він називається "Inversion" (інверсія)? Що саме інвертується порівняно з "природнім" способом написання коду?

2. Розгляньте код:
   ```csharp
   public class AppointmentService
   {
       private readonly SqlAppointmentRepository _repo = new SqlAppointmentRepository();
       public void Book(Appointment a) => _repo.Save(a);
   }
   ```
   Назвіть всі проблеми цього дизайну. Перепишіть код відповідно до DIP.

3. Поясніть три методи Dependency Injection: через конструктор, через властивість, через метод. Для кожного наведіть приклад коду та вкажіть, коли він доцільний.

4. Розгляньте:
   ```csharp
   public class ReportService
   {
       private IEmailSender _emailSender;
       public void SetEmailSender(IEmailSender sender) { _emailSender = sender; }
       public void Send(Report r) { _emailSender?.Send(r.ToString()); }
   }
   ```
   Який метод DI тут використовується? Яка ризик, що `_emailSender` може бути `null` під час виклику `Send`? Чи є Constructor Injection кращим варіантом?

5. Як DIP пов'язаний з тестованістю? Напишіть `FakeAppointmentRepository : IAppointmentRepository`, що зберігає дані в пам'яті, та покажіть юніт-тест для `AppointmentService` без підключення до бази даних.

6. Що таке IoC Container (контейнер інверсії залежностей)? Реалізуйте спрощений `SimpleContainer` з методами `Register<TInterface, TImplementation>()` та `Resolve<T>()`. Поясніть, як він знаходить потрібну реалізацію.

7. Поясніть, як SOLID як система підсилює себе: як SRP веде до менших класів → що спрощує DIP → що дозволяє реалізовувати OCP → що безпечно завдяки LSP → що стає можливим через ISP. Наведіть конкретний приклад системи, де всі 5 принципів працюють разом.

8. "DIP означає, що треба скрізь писати інтерфейси" — правда чи ні? Де DIP є обов'язковим, а де надмірним? Наведіть 2 приклади кожного варіанту.
