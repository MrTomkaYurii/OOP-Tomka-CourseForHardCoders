namespace ClinicApp.Managers;

using ClinicApp.Enums;
using ClinicApp.Models;
using ClinicApp.Utils;

public class PatientManager
{
    private List<Patient> _patients = new List<Patient>();

    public int Count => _patients.Count;

    public Patient this[int index]
    {
        get
        {
            if (index < 0 || index >= _patients.Count) return null!;
            return _patients[index];
        }
    }

    public void Add(Patient patient)
    {
        _patients.Add(patient);
        Console.WriteLine("Пацієнта [" + patient.Id + "] " + patient.FullName + " додано.");
    }

    public Patient FindById(int id)
    {
        for (int i = 0; i < _patients.Count; i++)
            if (_patients[i].Id == id) return _patients[i];
        return null!;
    }

    public bool TryFindById(int id, out Patient patient)
    {
        patient = FindById(id);
        return patient != null;
    }

    public Patient[] FindByName(string query)
    {
        string q = query.ToLower();
        List<Patient> result = new List<Patient>();
        for (int i = 0; i < _patients.Count; i++)
            if (_patients[i].FirstName.ToLower().Contains(q) || _patients[i].LastName.ToLower().Contains(q))
                result.Add(_patients[i]);
        return result.ToArray();
    }

    public Patient[] FindByBloodType(BloodType bloodType)
    {
        List<Patient> result = new List<Patient>();
        for (int i = 0; i < _patients.Count; i++)
            if (_patients[i].BloodType == bloodType) result.Add(_patients[i]);
        return result.ToArray();
    }

    public bool Remove(int id)
    {
        for (int i = 0; i < _patients.Count; i++)
        {
            if (_patients[i].Id == id)
            {
                _patients.RemoveAt(i);
                return true;
            }
        }
        return false;
    }

    public void DisplayAll()
    {
        if (_patients.Count == 0) { Console.WriteLine("Список пацієнтів порожній."); return; }
        Console.WriteLine("\n=== Пацієнти (" + _patients.Count + ") ===");
        for (int i = 0; i < _patients.Count; i++) Console.WriteLine(_patients[i]);
        Console.WriteLine(new string('─', 60));
    }

    public void DisplayStats()
    {
        if (_patients.Count == 0) { Console.WriteLine("Немає пацієнтів для статистики."); return; }

        double totalAge = 0;
        int minAge = _patients[0].Age, maxAge = _patients[0].Age;
        int minIdx = 0, maxIdx = 0, adultsCount = 0;

        for (int i = 0; i < _patients.Count; i++)
        {
            totalAge += _patients[i].Age;
            if (_patients[i].Age < minAge) { minAge = _patients[i].Age; minIdx = i; }
            if (_patients[i].Age > maxAge) { maxAge = _patients[i].Age; maxIdx = i; }
            if (_patients[i].IsAdult) adultsCount++;
        }

        Console.WriteLine("\n=== Статистика пацієнтів ===");
        Console.WriteLine("Всього:       " + _patients.Count);
        Console.WriteLine("Середній вік: " + (totalAge / _patients.Count).ToString("F1") + " р.");
        Console.WriteLine("Наймолодший:  " + _patients[minIdx].FullName + " (" + minAge + " р.)");
        Console.WriteLine("Найстарший:   " + _patients[maxIdx].FullName + " (" + maxAge + " р.)");
        Console.WriteLine("Дорослих:     " + adultsCount + " з " + _patients.Count);
        Console.WriteLine("============================");
    }

    public Patient[] GetAll() => _patients.ToArray();
}
