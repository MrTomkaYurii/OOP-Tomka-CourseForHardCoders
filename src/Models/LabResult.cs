namespace ClinicApp.Models;

using ClinicApp.Utils;

public class LabResult : MedicalRecord
{
    private string _testName = "";
    private string _unit = "";
    private string _referenceRange = "";

    public string TestName
    {
        get => _testName;
        set { ClinicValidator.ValidateName(value, "Назва аналізу"); _testName = value; }
    }

    public double Value { get; set; }

    public string Unit
    {
        get => _unit;
        set { ClinicValidator.ValidateName(value, "Одиниці виміру"); _unit = value; }
    }

    public string ReferenceRange
    {
        get => _referenceRange;
        set { ClinicValidator.ValidateName(value, "Норма"); _referenceRange = value; }
    }

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
