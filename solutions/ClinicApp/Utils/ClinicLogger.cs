using System.Text;
using ClinicApp.Events;

namespace ClinicApp.Utils;

public class ClinicLogger
{
    private readonly string _logPath;

    public string LogPath => _logPath;

    public ClinicLogger(string logPath = "clinic.log")
    {
        _logPath = logPath;
    }

    private void Write(string level, string message)
    {
        string line = $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] [{level}] {message}";
        File.AppendAllText(_logPath, line + Environment.NewLine, Encoding.UTF8);
    }

    public void LogInfo(string message)    => Write("INFO ", message);
    public void LogWarning(string message) => Write("WARN ", message);
    public void LogError(string message)   => Write("ERROR", message);

    public string[] GetLastLines(int n)
    {
        if (!File.Exists(_logPath)) return Array.Empty<string>();

        string[] all = File.ReadAllLines(_logPath, Encoding.UTF8);
        int skip = Math.Max(0, all.Length - n);
        string[] result = new string[all.Length - skip];
        Array.Copy(all, skip, result, 0, result.Length);
        return result;
    }

    public void Clear()
    {
        if (File.Exists(_logPath))
            File.Delete(_logPath);
    }

    public bool Exists() => File.Exists(_logPath);

    // ── обробники подій ────────────────────────────────────────────

    public void OnPatientAdded(object? sender, PatientEventArgs e)
        => LogInfo($"Новий пацієнт #{e.PatientId}: {e.FullName}");

    public void OnAppointmentBooked(object? sender, AppointmentEventArgs e)
        => LogInfo($"Запис #{e.AppointmentId}: пацієнт {e.PatientId} → лікар {e.DoctorId}, {e.ScheduledAt:dd.MM.yyyy HH:mm}");

    public void OnAppointmentCancelled(object? sender, AppointmentEventArgs e)
        => LogWarning($"Скасовано запис #{e.AppointmentId}: {e.Notes}");

    public void OnAppointmentCompleted(object? sender, AppointmentEventArgs e)
        => LogInfo($"Завершено запис #{e.AppointmentId}");

    public void OnPaymentReceived(object? sender, PaymentEventArgs e)
        => LogInfo($"Оплата #{e.AppointmentId}: {e.Amount:F2} грн");

    public void OnUrgentBooked(object? sender, AppointmentEventArgs e)
    {
        LogWarning($"ТЕРМІНОВИЙ запис #{e.AppointmentId}: {e.Notes}");

        string alertsDir = "alerts";
        Directory.CreateDirectory(alertsDir);
        string alertPath = Path.Combine(alertsDir, $"urgent_{DateTime.Today:yyyy-MM-dd}.txt");
        string line = $"[{DateTime.Now:HH:mm:ss}] Запис #{e.AppointmentId} | {e.Notes}{Environment.NewLine}";
        File.AppendAllText(alertPath, line, Encoding.UTF8);
    }

    public void OnPlanCompleted(object? sender, TreatmentPlanEventArgs e)
        => LogInfo($"План #{e.PlanId} завершено: {e.Diagnosis} (пацієнт {e.PatientId})");
}
