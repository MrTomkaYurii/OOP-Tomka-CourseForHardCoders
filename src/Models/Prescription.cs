namespace ClinicApp.Models;

public class Prescription : MedicalRecord
{
    public string MedicationName { get; set; }
    public string Dosage { get; set; }
    public int DurationDays { get; set; }
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
