namespace ClinicApp.Models;

public class UrgentAppointment : Appointment
{
    // private set — EF Core (TPH) встановлює при завантаженні з дискримінатором
    public string UrgencyNote { get; private set; } = "";

    protected UrgentAppointment() { }

    public UrgentAppointment(int patientId, int doctorId, DateTime scheduledAt,
                              string urgencyNote = "", int durationMinutes = 30)
        : base(patientId, doctorId, scheduledAt, durationMinutes)
    {
        UrgencyNote = urgencyNote;
    }

    public override decimal GetCost() => base.GetCost() * 1.5m;

    public sealed override string GetDescription() =>
        "Терміновий" + (UrgencyNote.Length > 0 ? " (" + UrgencyNote + ")" : "");

    public new int GetPriority() => 1;
}
