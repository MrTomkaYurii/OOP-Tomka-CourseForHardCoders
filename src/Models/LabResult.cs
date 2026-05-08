namespace ClinicApp.Models;

public class LabResult : MedicalRecord
{
    public string TestName { get; set; }
    public double Value { get; set; }
    public string Unit { get; set; }
    public string ReferenceRange { get; set; }
    public bool IsNormal { get; set; }

    public LabResult(int patientId, int doctorId, DateTime date,
                     string testName, double value, string unit,
                     string referenceRange, bool isNormal)
        : base(patientId, doctorId, date)
    {
        TestName = testName;
        Value = value;
        Unit = unit;
        ReferenceRange = referenceRange;
        IsNormal = isNormal;
    }

    public override string GetSummary() =>
        TestName + ": " + Value + " " + Unit +
        " (норма: " + ReferenceRange + ")" +
        (IsNormal ? "" : " ⚠ поза нормою");

    public override string GetRecordType() => "Аналіз";
}
