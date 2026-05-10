namespace ClinicApp.Models;

using ClinicApp.Enums;
using ClinicApp.Interfaces;
using ClinicApp.Utils;

public class Appointment : IPayable, ICancellable, IIdentifiable
{
    private static int _nextId = 1;

    private int _durationMinutes;
    private bool _isPaid;

    public int Id { get; }
    public int PatientId { get; }
    public int DoctorId { get; }
    public DateTime ScheduledAt { get; set; }

    public int DurationMinutes
    {
        get => _durationMinutes;
        set { ClinicValidator.ValidatePositive(value, "Тривалість"); _durationMinutes = value; }
    }

    public AppointmentStatus Status { get; private set; }
    public string Notes { get; private set; }

    public DateTime EndsAt => ScheduledAt.AddMinutes(DurationMinutes);
    public bool IsUpcoming => ScheduledAt > DateTime.Now && Status == AppointmentStatus.Scheduled;

    public virtual decimal GetCost() => (decimal)DurationMinutes * 10m;
    public virtual string GetDescription() => "Звичайний прийом";
    public int GetPriority() => 3;

    public bool IsPaid => _isPaid;
    public void MarkPaid() { if (!IsCancelled) _isPaid = true; }

    public Appointment(int patientId, int doctorId, DateTime scheduledAt, int durationMinutes = 30)
    {
        Id = _nextId++;
        PatientId = patientId;
        DoctorId = doctorId;
        ScheduledAt = scheduledAt;
        DurationMinutes = durationMinutes;
        Status = AppointmentStatus.Scheduled;
        Notes = "";
    }

    public bool IsCancelled => Status == AppointmentStatus.Cancelled;
    public string CancellationReason => IsCancelled ? Notes : "";

    public bool Cancel(string reason = "")
    {
        if (Status != AppointmentStatus.Scheduled) return false;
        Status = AppointmentStatus.Cancelled;
        if (reason.Length > 0) Notes = reason;
        return true;
    }

    public bool Complete()
    {
        if (Status != AppointmentStatus.Scheduled) return false;
        Status = AppointmentStatus.Completed;
        return true;
    }

    public override string ToString()
    {
        string result = "[" + Id + "] " + GetDescription() +
                        " | Пацієнт #" + PatientId + " → Лікар #" + DoctorId +
                        " | " + ScheduledAt.ToString("dd.MM.yyyy HH:mm") + "–" + EndsAt.ToString("HH:mm") +
                        " | " + Status +
                        " | " + GetCost().ToString("F2") + " грн";
        if (Notes.Length > 0) result += " | " + Notes;
        return result;
    }
}
