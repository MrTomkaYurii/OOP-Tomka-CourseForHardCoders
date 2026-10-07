namespace ClinicApp.Services;

using ClinicApp.Models;
using ClinicApp.Utils;

/// <summary>
/// LoggingPatientService — Decorator поверх IPatientService.
///
/// Lab 22 / Task 5: Паттерн Decorator + ISP + DIP.
///
/// Decorator:
///   — реалізує той самий інтерфейс що і декорований об'єкт (IPatientService)
///   — тримає посилання на "справжній" сервіс (_inner)
///   — делегує всі виклики до _inner, але додає поведінку (логування)
///
/// Переваги:
///   — PatientService не знає про логування (SRP)
///   — Логування можна увімкнути/вимкнути через DI без зміни PatientService
///   — LoggingPatientService можна тестувати окремо з mock-об'єктом _inner
///
/// DI реєстрація (ServiceContainer.cs):
///   services.AddScoped&lt;IPatientService&gt;(sp =&gt;
///       new LoggingPatientService(
///           new PatientService(sp.GetRequiredService&lt;ClinicDbContext&gt;()),
///           sp.GetRequiredService&lt;ClinicLogger&gt;()));
/// </summary>
public class LoggingPatientService(IPatientService inner, ClinicLogger logger) : IPatientService
{
    public async Task<List<Patient>> GetAllAsync(CancellationToken ct = default)
    {
        logger.LogInfo("[PatientService] GetAllAsync викликано");
        var result = await inner.GetAllAsync(ct);
        logger.LogInfo($"[PatientService] GetAllAsync → {result.Count} пацієнтів");
        return result;
    }

    public async Task<Patient?> GetByIdAsync(int id, CancellationToken ct = default)
    {
        var result = await inner.GetByIdAsync(id, ct);
        logger.LogInfo($"[PatientService] GetByIdAsync({id}) → {(result is null ? "не знайдено" : result.FullName)}");
        return result;
    }

    public async Task<List<Patient>> SearchAsync(string query, CancellationToken ct = default)
    {
        var result = await inner.SearchAsync(query, ct);
        logger.LogInfo($"[PatientService] SearchAsync('{query}') → {result.Count} результатів");
        return result;
    }

    public async Task<int> AddAsync(Patient patient, CancellationToken ct = default)
    {
        logger.LogInfo($"[PatientService] AddAsync: {patient.FullName}");
        var result = await inner.AddAsync(patient, ct);
        logger.LogInfo($"[PatientService] AddAsync → збережено {result} рядків");
        return result;
    }

    public async Task<bool> SoftDeleteAsync(int id, CancellationToken ct = default)
    {
        logger.LogInfo($"[PatientService] SoftDeleteAsync({id})");
        var result = await inner.SoftDeleteAsync(id, ct);
        logger.LogInfo($"[PatientService] SoftDeleteAsync({id}) → {(result ? "успішно" : "не знайдено")}");
        return result;
    }

    public Task<int> CountAsync(CancellationToken ct = default)
        => inner.CountAsync(ct);
}
