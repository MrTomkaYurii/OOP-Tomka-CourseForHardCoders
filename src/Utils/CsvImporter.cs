using System.Globalization;
using System.Text;
using ClinicApp.Enums;
using ClinicApp.Models;

namespace ClinicApp.Utils;

public class CsvImporter
{
    private readonly Clinic _clinic;

    public CsvImporter(Clinic clinic)
    {
        _clinic = clinic;
    }

    public ImportResult ImportPatients(string filePath)
    {
        var result = new ImportResult();

        if (!File.Exists(filePath))
        {
            result.AddError(0, $"Файл не знайдено: {filePath}");
            return result;
        }

        string[] lines = File.ReadAllLines(filePath, Encoding.UTF8);

        // перший рядок — заголовок, пропускаємо
        for (int i = 1; i < lines.Length; i++)
        {
            string line = lines[i].Trim();
            if (string.IsNullOrEmpty(line)) continue;

            try
            {
                string[] parts = line.Split(',');
                if (parts.Length < 3)
                {
                    result.AddError(i + 1, "Недостатньо полів (потрібно: ім'я,прізвище,дата_народження[,група_крові][,телефон])");
                    continue;
                }

                string firstName = parts[0].Trim();
                string lastName  = parts[1].Trim();
                DateTime dob     = DateTime.ParseExact(parts[2].Trim(), "dd.MM.yyyy",
                                       CultureInfo.InvariantCulture);

                BloodType blood = BloodType.Unknown;
                if (parts.Length > 3 && !string.IsNullOrWhiteSpace(parts[3]))
                    blood = (BloodType)Enum.Parse(typeof(BloodType), parts[3].Trim());

                string phone = parts.Length > 4 && !string.IsNullOrWhiteSpace(parts[4])
                    ? parts[4].Trim()
                    : "0000000000";

                Patient p = new Patient(firstName, lastName, dob, blood, phone);

                _clinic.Patients.Add(p);
                result.AddSuccess();
            }
            catch (Exception ex)
            {
                result.AddError(i + 1, ex.Message);
            }
        }

        return result;
    }
}
