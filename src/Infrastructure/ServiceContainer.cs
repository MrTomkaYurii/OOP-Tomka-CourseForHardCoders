namespace ClinicApp.Infrastructure;

using Microsoft.Extensions.DependencyInjection;
using Microsoft.EntityFrameworkCore;
using ClinicApp.Data;
using ClinicApp.Services;
using ClinicApp.Utils;

/// <summary>
/// ServiceContainer — точка конфігурації DI-контейнера.
///
/// Lab 22 / Task 5: IServiceCollection + lifetimes + Decorator.
///
/// IServiceCollection — список реєстрацій сервісів.
/// BuildServiceProvider() — будує IServiceProvider (вирішувач залежностей).
///
/// Lifetimes:
/// ┌──────────────┬──────────────────────────────────────────────────────┐
/// │ AddSingleton │ Один екземпляр на весь час роботи застосунку.        │
/// │              │ Підходить: Logger, HttpClient, конфігурація.         │
/// │              │ НЕ підходить: DbContext (не thread-safe для write).  │
/// ├──────────────┼──────────────────────────────────────────────────────┤
/// │ AddScoped    │ Новий екземпляр на кожен "scope" (запит у веб-апі,   │
/// │              │ або явний `using var scope = provider.CreateScope()`). │
/// │              │ Підходить: DbContext, Repository, Service-класи.     │
/// ├──────────────┼──────────────────────────────────────────────────────┤
/// │ AddTransient │ Новий екземпляр при КОЖНОМУ GetRequiredService.      │
/// │              │ Підходить: легкі stateless-сервіси, validator-и.    │
/// └──────────────┴──────────────────────────────────────────────────────┘
///
/// GetRequiredService&lt;T&gt;() — кидає InvalidOperationException якщо T не зареєстровано.
/// GetService&lt;T&gt;()         — повертає null якщо T не зареєстровано.
/// </summary>
public static class ServiceContainer
{
    public static IServiceProvider Build()
    {
        var services = new ServiceCollection();

        // ── DbContext: Scoped ──────────────────────────────────────────────
        // AddDbContext реєструє ClinicDbContext як Scoped автоматично.
        // Transient НЕ підходить: міграції, трекінг змін потребують стабільного контексту.
        // Singleton НЕ підходить: DbContext не є thread-safe.
        services.AddDbContext<ClinicDbContext>();

        // ── Logger: Singleton ──────────────────────────────────────────────
        // Один файл логу на весь застосунок — один ClinicLogger.
        services.AddSingleton<ClinicLogger>();

        // ── IDoctorService, IAppointmentService: Scoped ───────────────────
        // Залежать від ClinicDbContext (теж Scoped) — правильна комбінація.
        // Singleton що залежить від Scoped → помилка часу виконання!
        services.AddScoped<IDoctorService,      DoctorService>();
        services.AddScoped<IAppointmentService, AppointmentService>();

        // ── IPatientService: Scoped + Decorator ───────────────────────────
        // Замість прямої реєстрації PatientService — обгортаємо у Decorator.
        // sp (IServiceProvider) — вирішувач, що передається у фабричну лямбду.
        services.AddScoped<IPatientService>(sp =>
            new LoggingPatientService(
                inner:  new PatientService(sp.GetRequiredService<ClinicDbContext>()),
                logger: sp.GetRequiredService<ClinicLogger>()));

        return services.BuildServiceProvider();
    }

    /// <summary>
    /// Допоміжний метод: створити scope і отримати сервіс.
    /// У консольному застосунку scope моделює "один запит".
    /// </summary>
    public static IServiceScope CreateScope(IServiceProvider provider)
        => provider.CreateScope();
}
