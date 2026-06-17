---
chapter: 21
chapterTitle: "Розділ 21. Generic Host та Dependency Injection"
type: self-assessment
---

# Питання для самоконтролю — Розділ 21. Generic Host та Dependency Injection

## 21.1. Generic Host

1. Назвіть три ролі Generic Host в .NET-застосунку. Які проблеми він вирішує порівняно зі стандартним підходом "все в `Main()`"? Що відбувається без хоста при спробі реалізувати DI, конфігурацію та логування вручну?

2. Розгляньте код:
   ```csharp
   var host = Host.CreateDefaultBuilder(args)
       .ConfigureServices(services =>
       {
           services.AddSingleton<IPatientService, PatientService>();
           services.AddHostedService<SchedulerWorker>();
       })
       .Build();
   await host.RunAsync();
   ```
   Що автоматично налаштовує `Host.CreateDefaultBuilder`? Що робить `Build()`? Чому `RunAsync()` блокує до отримання Ctrl+C?

3. Що таке `IHostedService`? Назвіть два методи інтерфейсу та поясніть їх параметр `CancellationToken`. Як він відрізняється від `BackgroundService`? У яких випадках краще реалізовувати `IHostedService` напряму?

4. Опишіть порядок запуску та зупинки хоста: коли викликаються `StartAsync` кожного `IHostedService`? У якому порядку викликаються `StopAsync`? Що відбувається з Singleton-ами, що реалізують `IDisposable`?

5. Реалізуйте `BackgroundService`-клас `HeartbeatWorker`, що кожні 30 секунд записує в лог рядок "alive" і коректно завершується при зупинці хоста (обробляє `CancellationToken` у циклі).

6. Порівняйте Generic Host і `WebApplication` (мінімальний ASP.NET Core). Що спільного і чим вони відрізняються? Коли варто використовувати Generic Host без ASP.NET Core?

7. Що таке fluent API в контексті `IHostBuilder`? Поясніть методи `ConfigureServices`, `ConfigureAppConfiguration`, `ConfigureLogging`. Чи можна викликати `ConfigureServices` двічі в ланцюжку і що відбудеться?

## 21.2. IServiceCollection

1. Що таке `ServiceDescriptor`? Назвіть три поля, що він містить. Які три форми реєстрації сервісів існують в `IServiceCollection`? Наведіть приклад кожної.

2. Розгляньте код:
   ```csharp
   services.AddSingleton<ILogger, FileLogger>();
   services.AddSingleton<ILogger, ConsoleLogger>();
   
   var logger = provider.GetService<ILogger>();
   var allLoggers = provider.GetServices<ILogger>();
   ```
   Що поверне `GetService<ILogger>()`? Що поверне `GetServices<ILogger>()`? Яким чином використати `allLoggers` для відправки логу всім реалізаціям одночасно?

3. Поясніть різницю між `AddSingleton`, `TryAddSingleton` та `AddSingleton` з перевіркою. Коли `TryAddSingleton` захищає від подвійної реєстрації? Наведіть сценарій, де це важливо.

4. Що відбувається після виклику `BuildServiceProvider()`? Чи можна реєструвати нові сервіси після `Build`? Що таке "фіксація колекції" (locking)?

5. Що таке `ValidateOnBuild`? Яку помилку він виловлює ще на старті? Напишіть приклад неправильної реєстрації (де залежність не зареєстрована), що `ValidateOnBuild` знайде при запуску.

6. Що таке антипаттерн Service Locator? Порівняйте з Constructor DI за критеріями: явність залежностей, тестованість, відстеження залежностей. Наведіть приклад коду обома способами та поясніть, чому один кращий.

7. Коли `IServiceProvider` у коді є прийнятним (не антипаттерном)? Назвіть 3 легітимних сценарії і поясніть кожен.

## 21.3. Service Lifetimes

1. Порівняйте три lifetime-и: Singleton, Scoped, Transient. Заповніть таблицю: скільки екземплярів на процес/scope/resolve, чи потрібна thread-safety, типовий use case.

2. Розгляньте код:
   ```csharp
   services.AddSingleton<MySingletonService>();
   services.AddScoped<MyDbContext>();
   services.AddTransient<MyHelperService>();
   ```
   `MySingletonService` у конструкторі приймає `MyDbContext`. Що станеться? Яка ця проблема називається і чому вона небезпечна?

3. Поясніть "captive dependency" (захоплена залежність) детально: чому Singleton, що тримає Scoped, є помилкою? Що конкретно відбувається зі Scoped-сервісом у цьому випадку (чи він знищується, чи живе нескінченно)?

4. Що таке `IServiceScopeFactory`? Напишіть реалізацію Singleton-сервісу `ReportGeneratorService`, що використовує `IServiceScopeFactory` для правильного доступу до Scoped-залежності `IReportRepository` всередині методу `GenerateReport()`.

5. Правило "lifetime залежності не може бути коротшим за lifetime споживача" — поясніть усі заборонені комбінації (Singleton→Scoped, Singleton→Transient, Scoped→Transient). Які з них дозволені і чому?

6. Розгляньте сценарій:
   ```csharp
   services.AddTransient<IEmailSender, SmtpEmailSender>();
   ```
   `SmtpEmailSender` реалізує `IDisposable` і відкриває TCP-з'єднання. Яка проблема виникне, якщо `IEmailSender` резолвиться з кореневого `IServiceProvider` (не зі scope)? Як це виправити?

7. Для кожного lifetime наведіть конкретний приклад класу в медичній системі (клінічна ІС), де він є природним вибором: Singleton → ?, Scoped → ?, Transient → ?. Обґрунтуйте кожен вибір.

8. Напишіть клас `InstanceCounter` з полем `public int Id { get; }`, що у конструкторі отримує унікальний ID через `Interlocked.Increment`. Зареєструйте його як Singleton, Scoped і Transient в одному тестовому застосунку та продемонструйте різницю в ID між трьома resolve-ами.

## 21.4. Options Pattern

1. Що таке проблема "магічних рядків" при роботі з `IConfiguration`? Чому `configuration["Database:ConnectionString"]` є поганою практикою? Як Options Pattern вирішує цю проблему?

2. Поясніть три кроки впровадження Options Pattern: POCO клас, реєстрація в DI, отримання через конструктор. Напишіть повний приклад для `DatabaseOptions` з полями `ConnectionString`, `CommandTimeout`, `MaxRetries`.

3. Порівняйте `IOptions<T>`, `IOptionsSnapshot<T>` і `IOptionsMonitor<T>` за: lifetime, коли перечитує config, підтримка hot reload, використання в Singleton/Scoped. Коли кожен з них є правильним вибором?

4. Розгляньте код:
   ```csharp
   public class SmtpService
   {
       private readonly SmtpOptions _opts;
       public SmtpService(IOptions<SmtpOptions> options)
       {
           _opts = options.Value;
       }
   }
   ```
   Якщо `SmtpService` зареєстрований як Singleton і config змінюється під час роботи — чи побачить `SmtpService` нові значення? Що треба змінити, щоб побачив?

5. Що таке Named Options? Напишіть приклад реєстрації двох різних конфігурацій `SmtpOptions` ("primary" і "backup") та отримання потрібної через `IOptionsMonitor<SmtpOptions>.Get("primary")`.

6. Як валідувати Options за допомогою Data Annotations? Напишіть клас `AppointmentOptions` з атрибутами `[Required]`, `[Range]` і покажіть, як підключити `ValidateDataAnnotations()` та `ValidateOnStart()` так, щоб помилки конфігурації виявлялися на старті.

7. Поясніть пріоритет джерел конфігурації (від нижчого до вищого): `appsettings.json`, `appsettings.{Environment}.json`, User Secrets, змінні середовища, аргументи командного рядка. Навіщо саме такий порядок? Наведіть реальний сценарій, де кожен рівень корисний.

8. Дизайн задача: потрібно реалізувати перемикання між production і staging режимами без перекомпіляції коду, де staging конфігурація перекриває тільки окремі поля. Опишіть рекомендовану стратегію з файлами `appsettings.json` і `appsettings.Staging.json`, змінними середовища та чому Options Pattern тут кращий за `IConfiguration` напряму.
