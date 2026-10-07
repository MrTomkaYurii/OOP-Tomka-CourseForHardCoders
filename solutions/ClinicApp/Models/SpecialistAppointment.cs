namespace ClinicApp.Models;

public sealed class SpecialistAppointment : Appointment
{
    // private set — EF Core (TPH) встановлює при завантаженні
    public string ConsultationTopic { get; private set; } = "";

    // sealed клас — не може мати protected ctor. EF Core використовує private через рефлексію.
    private SpecialistAppointment() { }

    public SpecialistAppointment(int patientId, int doctorId, DateTime scheduledAt,
                                  string topic = "", int durationMinutes = 45)
        : base(patientId, doctorId, scheduledAt, durationMinutes)
    {
        ConsultationTopic = topic;
    }

    public override decimal GetCost() => base.GetCost() * 1.3m;

    public override string GetDescription() =>
        "Консультація спеціаліста" + (ConsultationTopic.Length > 0 ? ": " + ConsultationTopic : "");
}
