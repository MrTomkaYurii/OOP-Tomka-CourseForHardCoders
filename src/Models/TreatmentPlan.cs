using ClinicApp.Attributes;
using ClinicApp.Enums;

namespace ClinicApp.Models;

public class TreatmentPlan
{
    private static int _nextId = 1;

    public int Id { get; }

    [Required("Patient ID is required.")]
    public int PatientId { get; set; }

    [Required("Doctor ID is required.")]
    public int DoctorId { get; set; }

    [Required("Diagnosis cannot be empty.")]
    [MaxLength(200, "Diagnosis must not exceed 200 characters.")]
    public string Diagnosis { get; set; } = "";

    [Required("Treatment description cannot be empty.")]
    [MaxLength(500)]
    public string Treatment { get; set; } = "";

    [MinValue(1, "Duration must be at least 1 day.")]
    public int DurationDays { get; set; }

    public TreatmentStatus Status { get; private set; } = TreatmentStatus.Planned;

    public DateTime CreatedAt { get; } = DateTime.Now;

    public TreatmentPlan()
    {
        Id = _nextId++;
    }

    public bool Activate()
    {
        if (Status != TreatmentStatus.Planned) return false;
        Status = TreatmentStatus.Active;
        return true;
    }

    public bool Complete()
    {
        if (Status != TreatmentStatus.Active) return false;
        Status = TreatmentStatus.Completed;
        return true;
    }

    public bool Cancel()
    {
        if (Status == TreatmentStatus.Completed || Status == TreatmentStatus.Cancelled) return false;
        Status = TreatmentStatus.Cancelled;
        return true;
    }

    public override string ToString() =>
        $"Plan #{Id} | Patient:{PatientId} Doctor:{DoctorId} | {Diagnosis} | {Status} | {DurationDays}d";
}
