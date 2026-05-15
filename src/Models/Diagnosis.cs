namespace ClinicApp.Models;

using ClinicApp.Utils;

public class Diagnosis : MedicalRecord
{
    private string _diagnosisCode = "";
    private string _description = "";

    public string DiagnosisCode
    {
        get => _diagnosisCode;
        set { ClinicValidator.ValidateName(value, "Код діагнозу"); _diagnosisCode = value; }
    }

    public string Description
    {
        get => _description;
        set { ClinicValidator.ValidateName(value, "Опис діагнозу"); _description = value; }
    }

    public bool IsChronic { get; set; }

    // EF Core hydration constructor
    protected Diagnosis() { }

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
