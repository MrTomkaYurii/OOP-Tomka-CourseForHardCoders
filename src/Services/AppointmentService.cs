namespace ClinicApp.Services;

using Microsoft.EntityFrameworkCore;
using ClinicApp.Data;
using ClinicApp.Models;
using ClinicApp.Enums;

/// <summary>AppointmentService — реалізація IAppointmentService (DIP, constructor injection).</summary>
public class AppointmentService(ClinicDbContext context) : IAppointmentService
{
    public async Task<List<Appointment>> GetUpcomingAsync(CancellationToken ct = default)
        => await context.Appointments
            .AsNoTracking()
            .Include(a => a.Patient)
            .Include(a => a.Doctor)
            .Where(a => a.Status == AppointmentStatus.Scheduled && a.ScheduledAt > DateTime.Now)
            .OrderBy(a => a.ScheduledAt)
            .ToListAsync(ct);

    public async Task<List<Appointment>> GetByPatientAsync(int patientId, CancellationToken ct = default)
        => await context.Appointments
            .AsNoTracking()
            .Include(a => a.Doctor)
            .Where(a => a.PatientId == patientId)
            .OrderByDescending(a => a.ScheduledAt)
            .ToListAsync(ct);

    public async Task<List<Appointment>> GetByDoctorAsync(int doctorId, CancellationToken ct = default)
        => await context.Appointments
            .AsNoTracking()
            .Include(a => a.Patient)
            .Where(a => a.DoctorId == doctorId)
            .OrderByDescending(a => a.ScheduledAt)
            .ToListAsync(ct);

    public async Task<int> BookAsync(Appointment appointment, CancellationToken ct = default)
    {
        context.Appointments.Add(appointment);
        return await context.SaveChangesAsync(ct);
    }

    public async Task<bool> CancelAsync(int id, CancellationToken ct = default)
    {
        var a = await context.Appointments.FindAsync(new object[] { id }, ct);
        if (a is null) return false;
        a.Cancel();
        await context.SaveChangesAsync(ct);
        return true;
    }

    public async Task<bool> CompleteAsync(int id, CancellationToken ct = default)
    {
        var a = await context.Appointments.FindAsync(new object[] { id }, ct);
        if (a is null) return false;
        a.Complete();
        await context.SaveChangesAsync(ct);
        return true;
    }

    public async Task<decimal> GetTotalRevenueAsync(CancellationToken ct = default)
        => await context.Appointments
            .Where(a => a.IsPaid)
            .SumAsync(a => (decimal)a.DurationMinutes * 10m, ct);
}
