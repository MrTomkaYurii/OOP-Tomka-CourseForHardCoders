namespace ClinicApp.Models;

using ClinicApp.Utils;

public abstract class MedicalRecord
{
    private static int _nextId = 1;

    public int Id { get; }
    public int PatientId { get; }
    public int DoctorId { get; }
    public DateTime Date { get; }
    public string Notes { get; set; } = "";

    protected MedicalRecord(int patientId, int doctorId, DateTime date)
    {
        ClinicValidator.ValidatePositive(patientId, "PatientId");
        ClinicValidator.ValidatePositive(doctorId, "DoctorId");
        Id = _nextId++;
        PatientId = patientId;
        DoctorId = doctorId;
        Date = date;
    }

    public abstract string GetSummary();

    public virtual string GetRecordType() => "Медичний запис";

    public virtual bool IsActive() => Date >= DateTime.Today.AddMonths(-6);

    public override string ToString() =>
        "[" + Id + "] " + GetRecordType() +
        " | " + Date.ToString("dd.MM.yyyy") +
        " | " + GetSummary() +
        (Notes.Length > 0 ? " | " + Notes : "");
}
