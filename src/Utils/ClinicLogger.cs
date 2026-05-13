using System.Text;

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
}
