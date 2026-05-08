namespace ClinicApp.Models;

using ClinicApp.Utils;

public class Prescription : MedicalRecord
{
    private string _medicationName = "";
    private string _dosage = "";
    private int _durationDays;

    public string MedicationName
    {
        get => _medicationName;
        set { ClinicValidator.ValidateName(value, "Назва препарату"); _medicationName = value; }
    }

    public string Dosage
    {
        get => _dosage;
        set { ClinicValidator.ValidateName(value, "Дозування"); _dosage = value; }
    }

    public int DurationDays
    {
        get => _durationDays;
        set { ClinicValidator.ValidatePositive(value, "Тривалість курсу"); _durationDays = value; }
    }

    public string Instructions { get; set; }

    public DateTime ExpiresAt => Date.AddDays(DurationDays);

    public Prescription(int patientId, int doctorId, DateTime date,
                        string medicationName, string dosage,
                        int durationDays, string instructions = "")
        : base(patientId, doctorId, date)
    {
        MedicationName = medicationName;
        Dosage = dosage;
        DurationDays = durationDays;
        Instructions = instructions;
    }

    public override string GetSummary() =>
        MedicationName + " " + Dosage + " × " + DurationDays + " днів" +
        (Instructions.Length > 0 ? " (" + Instructions + ")" : "");

    public override string GetRecordType() => "Рецепт";

    public override bool IsActive() => ExpiresAt >= DateTime.Today;
}
