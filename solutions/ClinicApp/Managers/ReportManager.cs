namespace ClinicApp.Managers;

using ClinicApp.Enums;
using ClinicApp.Models;

public class ReportManager
{
    private readonly AppointmentManager _appointments;
    private readonly DoctorManager _doctors;
    private readonly PatientManager _patients;

    public ReportManager(AppointmentManager appointments, DoctorManager doctors, PatientManager patients)
    {
        _appointments = appointments;
        _doctors = doctors;
        _patients = patients;
    }

    // Task 2: GroupBy — статистика по спеціальностях лікарів
    public IEnumerable<SpecialityReport> GetSpecialityStats()
    {
        Appointment[] appointments = _appointments.GetAll();
        Doctor[] doctors = _doctors.GetAll();

        return doctors
            .GroupBy(d => d.Speciality)
            .Select(g =>
            {
                int[] ids = g.Select(d => d.Id).ToArray();
                var groupApps = appointments.Where(a => ids.Contains(a.DoctorId));
                return new SpecialityReport(
                    g.Key,
                    g.Count(),
                    groupApps.Count(),
                    groupApps.Sum(a => a.GetCost())
                );
            })
            .OrderByDescending(r => r.TotalRevenue);
    }

    // Task 3: OrderByDescending + FirstOrDefault — найзайнятіший лікар
    public string? FindBusiestDoctorName()
    {
        Appointment[] appointments = _appointments.GetAll();

        return _doctors.GetAll()
            .OrderByDescending(d => appointments.Count(a => a.DoctorId == d.Id))
            .Select(d => d.FullName)
            .FirstOrDefault();
    }

    // Task 4: GroupBy + Join — пацієнти з кількістю записів >= minVisits
    public IEnumerable<string> GetPatientsWithMultipleVisits(int minVisits)
    {
        Patient[] patients = _patients.GetAll();

        return _appointments.GetAll()
            .GroupBy(a => a.PatientId)
            .Where(g => g.Count() >= minVisits)
            .Join(patients,
                g => g.Key,
                p => p.Id,
                (g, p) => p.FullName);
    }

    // Task 5: OrderByDescending + Take — топ-N лікарів за виручкою
    public IEnumerable<DoctorStats> GetTopEarners(int n)
    {
        Appointment[] appointments = _appointments.GetAll();

        return _doctors.GetAll()
            .Select(d =>
            {
                var own = appointments.Where(a => a.DoctorId == d.Id);
                return new DoctorStats(
                    d.Id,
                    d.FullName,
                    own.Count(),
                    own.Sum(a => a.GetCost()),
                    own.Any() ? own.Max(a => a.ScheduledAt) : DateTime.MinValue
                );
            })
            .OrderByDescending(s => s.TotalRevenue)
            .Take(n);
    }

    // Task 6: Any — чи є хоч один терміновий запис у системі
    public bool HasAnyUrgentAppointments()
    {
        return _appointments.GetAll().Any(a => a is UrgentAppointment);
    }

    // Task 7: Distinct + OrderBy — унікальні спеціальності активних лікарів
    public IEnumerable<Speciality> GetActiveSpecialities()
    {
        return _doctors.GetAll()
            .Select(d => d.Speciality)
            .Distinct()
            .OrderBy(s => s.ToString());
    }

    // Task 8: GroupBy + Select (анонімний тип) — місячна виручка клініки
    public IEnumerable<(int Year, int Month, decimal Total)> GetMonthlyRevenue()
    {
        return _appointments.GetAll()
            .GroupBy(a => new { a.ScheduledAt.Year, a.ScheduledAt.Month })
            .Select(g => (g.Key.Year, g.Key.Month, g.Sum(a => a.GetCost())))
            .OrderBy(r => r.Year)
            .ThenBy(r => r.Month);
    }
}
