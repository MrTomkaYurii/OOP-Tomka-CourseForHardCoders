namespace ClinicApp.Models;

public class Diagnosis : MedicalRecord
{
    public string DiagnosisCode { get; set; }
    public string Description { get; set; }
    public bool IsChronic { get; set; }

    public Diagnosis(int patientId, int doctorId, DateTime date,
                     string diagnosisCode, string description, bool isChronic = false)
        : base(patientId, doctorId, date)
    {
        DiagnosisCode = diagnosisCode;
        Description = description;
        IsChronic = isChronic;
    }

    public override string GetSummary() =>
        DiagnosisCode + ": " + Description + (IsChronic ? " [хронічне]" : "");

    public override string GetRecordType() => "Діагноз";
}
