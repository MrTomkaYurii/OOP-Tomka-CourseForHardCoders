using System.Text;
using ClinicApp.Interfaces;
using ClinicApp.Models;

namespace ClinicApp.Utils;

public class ClinicExporter
{
    private readonly Clinic _clinic;
    private readonly string _baseDir;

    public ClinicExporter(Clinic clinic, string baseDir = "reports")
    {
        _clinic = clinic;
        _baseDir = baseDir;
    }

    private string PrepareDir()
    {
        string dir = Path.Combine(_baseDir, DateTime.Today.ToString("yyyy-MM-dd"));
        Directory.CreateDirectory(dir);
        return dir;
    }

    public string ExportPatients()
    {
        string path = Path.Combine(PrepareDir(), "patients.txt");

        using StreamWriter writer = new StreamWriter(path, false, Encoding.UTF8);
        writer.WriteLine("=== Список пацієнтів ===");
        writer.WriteLine($"Дата: {DateTime.Now:dd.MM.yyyy HH:mm}");
        writer.WriteLine(new string('─', 50));

        Patient[] patients = _clinic.Patients.GetAll();
        for (int i = 0; i < patients.Length; i++)
            writer.WriteLine($"{i + 1,3}. {patients[i]}");

        writer.WriteLine(new string('─', 50));
        writer.WriteLine($"Всього: {patients.Length}");

        return path;
    }

    public string ExportAppointments()
    {
        string path = Path.Combine(PrepareDir(), "appointments.txt");

        using StreamWriter writer = new StreamWriter(path, false, Encoding.UTF8);
        writer.WriteLine("=== Записи на прийом ===");
        writer.WriteLine($"Дата: {DateTime.Now:dd.MM.yyyy HH:mm}");
        writer.WriteLine(new string('─', 50));

        Appointment[] apps = _clinic.Appointments.GetAll();
        for (int i = 0; i < apps.Length; i++)
            writer.WriteLine($"{i + 1,3}. {apps[i]}");

        writer.WriteLine(new string('─', 50));
        writer.WriteLine($"Всього: {apps.Length}");

        return path;
    }

    public string ExportBilling()
    {
        string path = Path.Combine(PrepareDir(), "billing.txt");

        using StreamWriter writer = new StreamWriter(path, false, Encoding.UTF8);
        writer.WriteLine("=== Неоплачені рахунки ===");
        writer.WriteLine($"Дата: {DateTime.Now:dd.MM.yyyy HH:mm}");
        writer.WriteLine(new string('─', 50));

        IPayable[] unpaid = _clinic.Billing.GetAllUnpaid();
        decimal total = 0;
        for (int i = 0; i < unpaid.Length; i++)
        {
            writer.WriteLine($"{i + 1,3}. {unpaid[i]} — {unpaid[i].GetCost():C}");
            total += unpaid[i].GetCost();
        }

        writer.WriteLine(new string('─', 50));
        writer.WriteLine($"Загальний борг: {total:C}");

        return path;
    }

    public string ExportTreatmentPlans()
    {
        string path = Path.Combine(PrepareDir(), "treatment_plans.txt");

        using StreamWriter writer = new StreamWriter(path, false, Encoding.UTF8);
        writer.WriteLine("=== Плани лікування ===");
        writer.WriteLine($"Дата: {DateTime.Now:dd.MM.yyyy HH:mm}");
        writer.WriteLine(new string('─', 50));

        var plans = _clinic.TreatmentPlans.GetAll();
        for (int i = 0; i < plans.Length; i++)
            writer.WriteLine($"{i + 1,3}. {plans[i]}");

        writer.WriteLine(new string('─', 50));
        writer.WriteLine($"Всього: {plans.Length}");

        return path;
    }

    public void ExportAll()
    {
        string p1 = ExportPatients();
        string p2 = ExportAppointments();
        string p3 = ExportBilling();
        string p4 = ExportTreatmentPlans();

        Console.WriteLine($"  Пацієнти:       {p1}");
        Console.WriteLine($"  Записи:         {p2}");
        Console.WriteLine($"  Рахунки:        {p3}");
        Console.WriteLine($"  Плани лікування:{p4}");
    }
}
