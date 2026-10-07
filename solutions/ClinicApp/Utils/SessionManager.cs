using System.Globalization;
using System.Text;
using ClinicApp.Enums;
using ClinicApp.Models;

namespace ClinicApp.Utils;

public class SessionManager
{
    private readonly string _sessionPath;

    public SessionManager(string sessionPath = "session.dat")
    {
        _sessionPath = sessionPath;
    }

    public bool Exists() => File.Exists(_sessionPath);

    public void Save(Clinic clinic)
    {
        using StreamWriter writer = new StreamWriter(_sessionPath, false, Encoding.UTF8);

        writer.WriteLine("[PATIENTS]");
        foreach (Patient p in clinic.Patients.GetAll())
            writer.WriteLine($"{p.FirstName},{p.LastName},{p.DateOfBirth:dd.MM.yyyy},{p.BloodType},{p.Phone}");

        writer.WriteLine("[END]");
    }

    public int Load(Clinic clinic)
    {
        if (!File.Exists(_sessionPath)) return 0;

        string[] lines = File.ReadAllLines(_sessionPath, Encoding.UTF8);
        string section = "";
        int loaded = 0;

        foreach (string line in lines)
        {
            string trimmed = line.Trim();
            if (trimmed.StartsWith("[")) { section = trimmed; continue; }
            if (string.IsNullOrEmpty(trimmed)) continue;

            if (section == "[PATIENTS]")
            {
                try
                {
                    string[] parts = trimmed.Split(',');
                    string firstName = parts[0];
                    string lastName  = parts[1];
                    DateTime dob     = DateTime.ParseExact(parts[2], "dd.MM.yyyy",
                                           CultureInfo.InvariantCulture);
                    BloodType blood  = (BloodType)Enum.Parse(typeof(BloodType), parts[3]);
                    string phone     = parts[4];

                    Patient p = new Patient(firstName, lastName, dob, blood, phone);
                    clinic.Patients.Add(p);
                    loaded++;
                }
                catch
                {
                    // пропускаємо пошкоджений рядок
                }
            }
        }

        return loaded;
    }
}
