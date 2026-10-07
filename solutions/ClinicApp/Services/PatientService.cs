namespace ClinicApp.Services;

using Microsoft.EntityFrameworkCore;
using ClinicApp.Data;
using ClinicApp.Models;

/// <summary>
/// PatientService — реалізація IPatientService поверх EF Core.
///
/// Lab 22 / Task 4: DIP — Constructor Injection.
///
/// PatientService не знає ЗВІДКИ береться ClinicDbContext.
/// Хто створює PatientService — той відповідає за надання контексту.
/// DI-контейнер вирішує це автоматично.
///
/// Primary constructor (C# 12): замість явного поля і конструктора —
///   public class PatientService(ClinicDbContext context) { ... }
///   Параметр 'context' доступний у всьому класі як неявне поле.
/// </summary>
public class PatientService(ClinicDbContext context) : IPatientService
{
    public async Task<List<Patient>> GetAllAsync(CancellationToken ct = default)
        => await context.Patients
            .AsNoTracking()
            .OrderBy(p => p.LastName)
            .ToListAsync(ct);

    public async Task<Patient?> GetByIdAsync(int id, CancellationToken ct = default)
        => await context.Patients
            .Include(p => p.Appointments)
            .FirstOrDefaultAsync(p => p.Id == id, ct);

    public async Task<List<Patient>> SearchAsync(string query, CancellationToken ct = default)
        => await context.Patients
            .AsNoTracking()
            .Where(p => p.FirstName.Contains(query) || p.LastName.Contains(query))
            .OrderBy(p => p.LastName)
            .ToListAsync(ct);

    public async Task<int> AddAsync(Patient patient, CancellationToken ct = default)
    {
        context.Patients.Add(patient);
        return await context.SaveChangesAsync(ct);
    }

    public async Task<bool> SoftDeleteAsync(int id, CancellationToken ct = default)
    {
        var patient = await context.Patients.FindAsync(new object[] { id }, ct);
        if (patient is null) return false;
        patient.SoftDelete();
        await context.SaveChangesAsync(ct);
        return true;
    }

    public async Task<int> CountAsync(CancellationToken ct = default)
        => await context.Patients.CountAsync(ct);
}
