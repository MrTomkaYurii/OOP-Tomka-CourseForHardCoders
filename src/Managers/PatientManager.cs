namespace ClinicApp.Managers;

using ClinicApp.Enums;
using ClinicApp.Models;
using ClinicApp.Utils;

public class PatientManager
{
    private const int MaxPatients = 100;
    private Patient[] _patients = new Patient[MaxPatients];
    private int _count = 0;

    public int Count => _count;

    public Patient this[int index]
    {
        get
        {
            if (index < 0 || index >= _count) return null!;
            return _patients[index];
        }
    }

    public void Add(Patient patient)
    {
        if (_count >= MaxPatients)
        {
            Console.WriteLine("Помилка: досягнуто ліміт пацієнтів (" + MaxPatients + ").");
            return;
        }
        _patients[_count] = patient;
        _count++;
        Console.WriteLine("Пацієнта [" + patient.Id + "] " + patient.FullName + " додано.");
    }

    public Patient FindById(int id)
    {
        for (int i = 0; i < _count; i++)
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
        int matchCount = 0;
        for (int i = 0; i < _count; i++)
            if (_patients[i].FirstName.ToLower().Contains(q) || _patients[i].LastName.ToLower().Contains(q))
                matchCount++;

        Patient[] result = new Patient[matchCount];
        int idx = 0;
        for (int i = 0; i < _count; i++)
            if (_patients[i].FirstName.ToLower().Contains(q) || _patients[i].LastName.ToLower().Contains(q))
                result[idx++] = _patients[i];
        return result;
    }

    public Patient[] FindByBloodType(BloodType bloodType)
    {
        int matchCount = 0;
        for (int i = 0; i < _count; i++)
            if (_patients[i].BloodType == bloodType) matchCount++;

        Patient[] result = new Patient[matchCount];
        int idx = 0;
        for (int i = 0; i < _count; i++)
            if (_patients[i].BloodType == bloodType) result[idx++] = _patients[i];
        return result;
    }

    public bool Remove(int id)
    {
        for (int i = 0; i < _count; i++)
        {
            if (_patients[i].Id == id)
            {
                for (int j = i; j < _count - 1; j++)
                    _patients[j] = _patients[j + 1];
                _patients[_count - 1] = null!;
                _count--;
                return true;
            }
        }
        return false;
    }

    public void DisplayAll()
    {
        if (_count == 0) { Console.WriteLine("Список пацієнтів порожній."); return; }
        Console.WriteLine("\n=== Пацієнти (" + _count + " / " + MaxPatients + ") ===");
        for (int i = 0; i < _count; i++) Console.WriteLine(_patients[i]);
        Console.WriteLine(new string('─', 60));
    }

    public void DisplayStats()
    {
        if (_count == 0) { Console.WriteLine("Немає пацієнтів для статистики."); return; }

        double totalAge = 0;
        int minAge = _patients[0].Age, maxAge = _patients[0].Age;
        int minIdx = 0, maxIdx = 0, adultsCount = 0;

        for (int i = 0; i < _count; i++)
        {
            totalAge += _patients[i].Age;
            if (_patients[i].Age < minAge) { minAge = _patients[i].Age; minIdx = i; }
            if (_patients[i].Age > maxAge) { maxAge = _patients[i].Age; maxIdx = i; }
            if (_patients[i].IsAdult) adultsCount++;
        }

        Console.WriteLine("\n=== Статистика пацієнтів ===");
        Console.WriteLine("Всього:       " + _count);
        Console.WriteLine("Середній вік: " + (totalAge / _count).ToString("F1") + " р.");
        Console.WriteLine("Наймолодший:  " + _patients[minIdx].FullName + " (" + minAge + " р.)");
        Console.WriteLine("Найстарший:   " + _patients[maxIdx].FullName + " (" + maxAge + " р.)");
        Console.WriteLine("Дорослих:     " + adultsCount + " з " + _count);
        Console.WriteLine("============================");
    }

    public Patient[] GetAll()
    {
        Patient[] result = new Patient[_count];
        for (int i = 0; i < _count; i++) result[i] = _patients[i];
        return result;
    }
}
