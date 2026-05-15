namespace ClinicApp.Models;

using ClinicApp.Enums;
using ClinicApp.Interfaces;
using ClinicApp.Utils;

public class Appointment : IPayable, ICancellable, IIdentifiable
{
    private static int _nextId = 1;

    private int _durationMinutes; // backing field з валідацією

    // private set — EF Core встановлює Id після INSERT
    public int Id { get; private set; }

    // PatientId і DoctorId — Foreign Key властивості для EF Core
    public int PatientId { get; private set; }
    public int DoctorId { get; private set; }

    // Navigation properties — EF Core завантажує пов'язані об'єкти через .Include()
    public Patient? Patient { get; set; }
    public Doctor? Doctor { get; set; }
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

    // private set — EF Core може встановити значення при завантаженні з БД
    public bool IsPaid { get; private set; }
    public void MarkPaid() { if (!IsCancelled) IsPaid = true; }

    // EF Core hydration constructor — не валідує, бо дані вже перевірені при збереженні
    protected Appointment()
    {
        Notes = "";
        Status = AppointmentStatus.Scheduled;
    }

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
