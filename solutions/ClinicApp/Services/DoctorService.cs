namespace ClinicApp.Services;

using Microsoft.EntityFrameworkCore;
using ClinicApp.Data;
using ClinicApp.Models;
using ClinicApp.Enums;

/// <summary>DoctorService — реалізація IDoctorService (DIP, constructor injection).</summary>
public class DoctorService(ClinicDbContext context) : IDoctorService
{
    public async Task<List<Doctor>> GetAllAsync(CancellationToken ct = default)
        => await context.Doctors
            .AsNoTracking()
            .OrderBy(d => d.LastName)
            .ToListAsync(ct);

    public async Task<Doctor?> GetByIdAsync(int id, CancellationToken ct = default)
        => await context.Doctors
            .Include(d => d.Appointments)
            .FirstOrDefaultAsync(d => d.Id == id, ct);

    public async Task<List<Doctor>> GetBySpecialityAsync(Speciality speciality, CancellationToken ct = default)
        => await context.Doctors
            .AsNoTracking()
            .Where(d => d.Speciality == speciality)
            .OrderBy(d => d.LastName)
            .ToListAsync(ct);

    public async Task<int> CountAsync(CancellationToken ct = default)
        => await context.Doctors.CountAsync(ct);
}
