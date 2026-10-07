using System.Text;
using ClinicApp.Events;

namespace ClinicApp.Utils;

public class SessionEventTracker
{
    private readonly Clinic _clinic;

    public int PatientsAdded          { get; private set; }
    public int AppointmentsBooked     { get; private set; }
    public int UrgentBooked           { get; private set; }
    public int AppointmentsCancelled  { get; private set; }
    public int AppointmentsCompleted  { get; private set; }
    public int PaymentsReceived       { get; private set; }
    public int PlansCompleted         { get; private set; }

    public SessionEventTracker(Clinic clinic)
    {
        _clinic = clinic;
    }

    public void OnPatientAdded(object? sender, PatientEventArgs e)
        => PatientsAdded++;

    public void OnAppointmentBooked(object? sender, AppointmentEventArgs e)
        => AppointmentsBooked++;

    public void OnUrgentBooked(object? sender, AppointmentEventArgs e)
        => UrgentBooked++;

    public void OnAppointmentCancelled(object? sender, AppointmentEventArgs e)
    {
        AppointmentsCancelled++;

        if (!_clinic.WaitingRoom.IsEmpty)
        {
            var next = _clinic.WaitingRoom.Peek();
            Console.WriteLine($"  [!] Слот звільнився. Наступний у черзі: {next.FullName}");
        }
    }

    public void OnAppointmentCompleted(object? sender, AppointmentEventArgs e)
        => AppointmentsCompleted++;

    public void OnPaymentReceived(object? sender, PaymentEventArgs e)
        => PaymentsReceived++;

    public void OnPlanCompleted(object? sender, TreatmentPlanEventArgs e)
        => PlansCompleted++;

    public void PrintSummary()
    {
        Console.WriteLine("── Підсумок сесії ────────────────────────────");
        Console.WriteLine($"  Нових пацієнтів:    {PatientsAdded}");
        Console.WriteLine($"  Записів створено:   {AppointmentsBooked} (терм.: {UrgentBooked})");
        Console.WriteLine($"  Скасувань:          {AppointmentsCancelled}");
        Console.WriteLine($"  Завершених прийомів:{AppointmentsCompleted}");
        Console.WriteLine($"  Оплат:              {PaymentsReceived}");
        Console.WriteLine($"  Планів завершено:   {PlansCompleted}");
    }

    public void SaveSummary(string path = "session_summary.txt")
    {
        using StreamWriter writer = new StreamWriter(path, false, Encoding.UTF8);
        writer.WriteLine("=== Підсумок сесії ===");
        writer.WriteLine($"Дата: {DateTime.Now:dd.MM.yyyy HH:mm}");
        writer.WriteLine();
        writer.WriteLine($"Нових пацієнтів:     {PatientsAdded}");
        writer.WriteLine($"Записів створено:    {AppointmentsBooked}");
        writer.WriteLine($"  з них термінових:  {UrgentBooked}");
        writer.WriteLine($"Скасувань:           {AppointmentsCancelled}");
        writer.WriteLine($"Завершених прийомів: {AppointmentsCompleted}");
        writer.WriteLine($"Оплат прийнято:      {PaymentsReceived}");
        writer.WriteLine($"Планів завершено:    {PlansCompleted}");
    }
}
