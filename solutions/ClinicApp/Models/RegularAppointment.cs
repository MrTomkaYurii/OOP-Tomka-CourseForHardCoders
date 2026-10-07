namespace ClinicApp.Models;

public class RegularAppointment : Appointment
{
    protected RegularAppointment() { }

    public RegularAppointment(int patientId, int doctorId, DateTime scheduledAt, int durationMinutes = 30)
        : base(patientId, doctorId, scheduledAt, durationMinutes) { }

    public override string GetDescription() => "Звичайний прийом";
}
