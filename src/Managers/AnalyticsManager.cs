namespace ClinicApp.Managers;

using ClinicApp.Models;

public class AnalyticsManager
{
    private readonly AppointmentManager _appointments;
    private readonly DoctorManager _doctors;
    private readonly PatientManager _patients;

    public AnalyticsManager(AppointmentManager appointments, DoctorManager doctors, PatientManager patients)
    {
        _appointments = appointments;
        _doctors = doctors;
        _patients = patients;
    }

    public IEnumerable<DoctorStats> ComputeDoctorStats()
    {
        Appointment[] appointments = _appointments.GetAll();

        return _doctors.GetAll().Select(d =>
        {
            var own = appointments.Where(a => a.DoctorId == d.Id);
            return new DoctorStats(
                d.Id,
                d.FullName,
                own.Count(),
                own.Sum(a => a.GetCost()),
                own.Any() ? own.Max(a => a.ScheduledAt) : DateTime.MinValue
            );
        });
    }

    public IEnumerable<PatientStats> ComputePatientStats()
    {
        Appointment[] appointments = _appointments.GetAll();

        return _patients.GetAll().Select(p =>
        {
            var own = appointments.Where(a => a.PatientId == p.Id);
            return new PatientStats(
                p.Id,
                p.FullName,
                own.Count(),
                own.Sum(a => a.GetCost()),
                own.Any() ? own.Max(a => a.ScheduledAt) : DateTime.MinValue
            );
        });
    }
}
