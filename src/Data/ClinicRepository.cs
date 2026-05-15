namespace ClinicApp.Data;

using Microsoft.EntityFrameworkCore;
using ClinicApp.Models;
using ClinicApp.Enums;

/// <summary>
/// ClinicRepository — шар доступу до даних поверх ClinicDbContext.
///
/// Інкапсулює запити з .Include() та складніші LINQ-вирази,
/// відокремлюючи "як завантажити" від "що відобразити" (SRP).
///
/// Ключова концепція: Eager Loading через .Include()
///
/// Проблема N+1:
///   — якщо завантажити 100 Appointments без .Include(),
///     а потім для кожного звертатись до a.Patient.FullName,
///     EF виконає 1 (Appointments) + 100 (Patient) = 101 SQL-запити.
///   — .Include(a => a.Patient) вирішує це: 1 SQL з JOIN.
/// </summary>
public class ClinicRepository
{
    private readonly ClinicDbContext _context;

    public ClinicRepository(ClinicDbContext context)
    {
        _context = context;
    }

    // ── Task 4: Пацієнт з усіма записами (Eager Loading) ──────────────────
    // .Include() генерує JOIN: SELECT ... FROM Patients JOIN Appointments ON ...
    public Patient? GetPatientWithAppointments(int patientId)
    {
        return _context.Patients
            .Include(p => p.Appointments)   // завантажити колекцію Appointments
            .FirstOrDefault(p => p.Id == patientId);
    }

    // ── Лікар з усіма записами ─────────────────────────────────────────────
    public Doctor? GetDoctorWithAppointments(int doctorId)
    {
        return _context.Doctors
            .Include(d => d.Appointments)
            .FirstOrDefault(d => d.Id == doctorId);
    }

    // ── Усі заплановані записи з повними даними про пацієнта і лікаря ──────
    // .Include(a => a.Patient) + .Include(a => a.Doctor) — два окремих JOIN
    public List<Appointment> GetUpcomingAppointments()
    {
        return _context.Appointments
            .Include(a => a.Patient)    // JOIN на Patients
            .Include(a => a.Doctor)     // JOIN на Doctors
            .Where(a => a.Status == AppointmentStatus.Scheduled
                        && a.ScheduledAt > DateTime.Now)
            .OrderBy(a => a.ScheduledAt)
            .ToList();
    }

    // ── Усі записи конкретного пацієнта (через FK PatientId) ──────────────
    // Зверніть увагу: можна без .Include() якщо треба тільки дані запису
    public List<Appointment> GetAppointmentsByPatient(int patientId)
    {
        return _context.Appointments
            .Include(a => a.Doctor)         // потрібен для відображення імені лікаря
            .Where(a => a.PatientId == patientId)
            .OrderByDescending(a => a.ScheduledAt)
            .ToList();
    }

    // ── Статистика: кількість записів по кожному лікарю ───────────────────
    // .AsNoTracking() — без відстеження змін; підходить для запитів тільки на читання
    public List<(Doctor Doctor, int Count, decimal Revenue)> GetDoctorStats()
    {
        return _context.Doctors
            .AsNoTracking()
            .Include(d => d.Appointments)
            .Select(d => new
            {
                Doctor   = d,
                Count    = d.Appointments.Count,
                Revenue  = d.Appointments.Sum(a => (decimal)a.DurationMinutes * 10m),
            })
            .OrderByDescending(x => x.Count)
            .ToList()
            .Select(x => (x.Doctor, x.Count, x.Revenue))
            .ToList();
    }

    // ── Пошук пацієнтів із незавершеними записами ─────────────────────────
    public List<Patient> GetPatientsWithActiveAppointments()
    {
        return _context.Patients
            .AsNoTracking()
            .Include(p => p.Appointments)
            .Where(p => p.Appointments.Any(a => a.Status == AppointmentStatus.Scheduled))
            .OrderBy(p => p.LastName)
            .ToList();
    }
}
