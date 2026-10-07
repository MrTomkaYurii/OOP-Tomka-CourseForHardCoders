namespace ClinicApp.Models;

using ClinicApp.Utils;

public abstract class MedicalRecord
{
    private static int _nextId = 1;

    // private set — EF Core встановлює при завантаженні з БД
    public int Id { get; private set; }
    public int PatientId { get; private set; }
    public int DoctorId { get; private set; }
    public DateTime Date { get; private set; }
    public string Notes { get; set; } = "";

    // Navigation property — EF завантажить пацієнта через .Include()
    public Patient? Patient { get; set; }

    // EF Core hydration ctor (protected, abstract клас — тільки EF підкласи використають)
    protected MedicalRecord() { Date = DateTime.Today; }

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
