using System.Text;
using ClinicApp.Events;
using ClinicApp.Models;

namespace ClinicApp.Utils;

public class PatientPassportWriter
{
    private readonly Clinic _clinic;
    private readonly string _baseDir;

    public PatientPassportWriter(Clinic clinic, string baseDir = "patients")
    {
        _clinic  = clinic;
        _baseDir = baseDir;
        Directory.CreateDirectory(baseDir);
    }

    public void OnPatientAdded(object? sender, PatientEventArgs e)
        => Write(e.PatientId);

    public void OnAppointmentCompleted(object? sender, AppointmentEventArgs e)
        => Write(e.PatientId);

    public void OnPlanCompleted(object? sender, TreatmentPlanEventArgs e)
        => Write(e.PatientId);

    private void Write(int patientId)
    {
        Patient? patient = _clinic.Patients.FindById(patientId);
        if (patient == null) return;

        string path = Path.Combine(_baseDir, $"passport_{patientId}.txt");

        using StreamWriter w = new StreamWriter(path, false, Encoding.UTF8);

        // ── Заголовок ──────────────────────────────────────────────
        w.WriteLine("╔══════════════════════════════════════════════╗");
        w.WriteLine("║         МЕДИЧНА КАРТКА ПАЦІЄНТА             ║");
        w.WriteLine("╚══════════════════════════════════════════════╝");
        w.WriteLine($"Згенеровано: {DateTime.Now:dd.MM.yyyy HH:mm:ss}");
        w.WriteLine();

        // ── Особисті дані ──────────────────────────────────────────
        w.WriteLine("── Особисті дані ─────────────────────────────");
        w.WriteLine($"  ID:          {patient.Id}");
        w.WriteLine($"  ПІБ:         {patient.FullName}");
        w.WriteLine($"  Дата нар.:   {patient.DateOfBirth:dd.MM.yyyy}");
        w.WriteLine($"  Вік:         {patient.Age} р.");
        w.WriteLine($"  Група крові: {patient.BloodType}");
        w.WriteLine($"  Телефон:     {patient.Phone}");
        w.WriteLine();

        // ── Медичні записи ─────────────────────────────────────────
        MedicalRecord[] records = _clinic.MedicalRecords.GetByPatient(patientId);

        w.WriteLine("── Діагнози ──────────────────────────────────");
        int diagCount = 0;
        for (int i = 0; i < records.Length; i++)
        {
            if (records[i] is Diagnosis d)
            {
                diagCount++;
                string chronic = d.IsChronic ? " [хронічна]" : "";
                w.WriteLine($"  {diagCount}. [{d.Date:dd.MM.yyyy}] {d.DiagnosisCode} — {d.Description}{chronic}");
            }
        }
        if (diagCount == 0) w.WriteLine("  Немає діагнозів.");
        w.WriteLine();

        w.WriteLine("── Аналізи ───────────────────────────────────");
        int labCount = 0;
        for (int i = 0; i < records.Length; i++)
        {
            if (records[i] is LabResult lab)
            {
                labCount++;
                string norm = lab.IsNormal ? "✓" : "✗";
                w.WriteLine($"  {labCount}. [{lab.Date:dd.MM.yyyy}] {lab.TestName}: {lab.Value} {lab.Unit} (норма: {lab.ReferenceRange}) {norm}");
            }
        }
        if (labCount == 0) w.WriteLine("  Немає аналізів.");
        w.WriteLine();

        w.WriteLine("── Рецепти ───────────────────────────────────");
        int rxCount = 0;
        for (int i = 0; i < records.Length; i++)
        {
            if (records[i] is Prescription rx)
            {
                rxCount++;
                string active = rx.IsActive() ? "[активний]" : "[завершений]";
                w.WriteLine($"  {rxCount}. [{rx.Date:dd.MM.yyyy}] {rx.MedicationName} {rx.Dosage} × {rx.DurationDays} дн. {active}");
                w.WriteLine($"       {rx.Instructions} | до {rx.ExpiresAt:dd.MM.yyyy}");
            }
        }
        if (rxCount == 0) w.WriteLine("  Немає рецептів.");
        w.WriteLine();

        // ── Записи на прийом ───────────────────────────────────────
        w.WriteLine("── Записи на прийом ──────────────────────────");
        Appointment[] apps = _clinic.Appointments.GetByPatient(patientId);
        if (apps.Length == 0)
        {
            w.WriteLine("  Немає записів.");
        }
        else
        {
            for (int i = 0; i < apps.Length; i++)
                w.WriteLine($"  {i + 1}. [{apps[i].ScheduledAt:dd.MM.yyyy HH:mm}] Лікар #{apps[i].DoctorId} | {apps[i].GetDescription()} | {apps[i].Status}");
        }
        w.WriteLine();

        // ── Плани лікування ────────────────────────────────────────
        w.WriteLine("── Плани лікування ───────────────────────────");
        TreatmentPlan[] plans = _clinic.TreatmentPlans.GetByPatient(patientId);
        if (plans.Length == 0)
        {
            w.WriteLine("  Немає планів.");
        }
        else
        {
            for (int i = 0; i < plans.Length; i++)
                w.WriteLine($"  {i + 1}. #{plans[i].Id} | {plans[i].Diagnosis} | {plans[i].Status} | {plans[i].DurationDays} дн.");
        }
        w.WriteLine();

        // ── Фінанси ────────────────────────────────────────────────
        w.WriteLine("── Фінанси ───────────────────────────────────");
        decimal debt = _clinic.Billing.GetPatientDebt(patientId);
        w.WriteLine($"  Заборгованість: {debt:F2} грн");
        w.WriteLine();
        w.WriteLine(new string('═', 46));
    }
}
