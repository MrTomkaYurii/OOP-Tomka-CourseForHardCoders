namespace ClinicApp;

public class DoctorManager
{
    private const int MaxDoctors = 50;
    private Doctor[] _doctors = new Doctor[MaxDoctors];
    private int _count = 0;

    public int Count => _count;

    public Doctor this[int index]
    {
        get
        {
            if (index < 0 || index >= _count) return null!;
            return _doctors[index];
        }
    }

    public void Add(Doctor doctor)
    {
        if (_count >= MaxDoctors)
        {
            Console.WriteLine("Помилка: досягнуто ліміт лікарів (" + MaxDoctors + ").");
            return;
        }
        _doctors[_count] = doctor;
        _count++;
        Console.WriteLine("Лікаря [" + doctor.Id + "] " + doctor.FullName +
                          " (" + ClinicFormatter.FormatSpeciality(doctor.Speciality) + ") додано.");
    }

    public Doctor FindById(int id)
    {
        for (int i = 0; i < _count; i++)
        {
            if (_doctors[i].Id == id)
                return _doctors[i];
        }
        return null!;
    }

    public bool TryFindById(int id, out Doctor doctor)
    {
        doctor = FindById(id);
        return doctor != null;
    }

    // Перевантаження 1: пошук за рядком (часткове співпадіння у назві)
    public Doctor[] FindBySpeciality(string query)
    {
        string q = query.ToLower();
        int matchCount = 0;
        for (int i = 0; i < _count; i++)
            if (ClinicFormatter.FormatSpeciality(_doctors[i].Speciality).ToLower().Contains(q))
                matchCount++;

        Doctor[] result = new Doctor[matchCount];
        int idx = 0;
        for (int i = 0; i < _count; i++)
            if (ClinicFormatter.FormatSpeciality(_doctors[i].Speciality).ToLower().Contains(q))
                result[idx++] = _doctors[i];
        return result;
    }

    // Перевантаження 2: пошук за enum (точне співпадіння)
    public Doctor[] FindBySpeciality(Speciality speciality)
    {
        int matchCount = 0;
        for (int i = 0; i < _count; i++)
            if (_doctors[i].Speciality == speciality) matchCount++;

        Doctor[] result = new Doctor[matchCount];
        int idx = 0;
        for (int i = 0; i < _count; i++)
            if (_doctors[i].Speciality == speciality) result[idx++] = _doctors[i];
        return result;
    }

    public bool Remove(int id)
    {
        for (int i = 0; i < _count; i++)
        {
            if (_doctors[i].Id == id)
            {
                for (int j = i; j < _count - 1; j++)
                    _doctors[j] = _doctors[j + 1];
                _doctors[_count - 1] = null!;
                _count--;
                return true;
            }
        }
        return false;
    }

    public void DisplayAll()
    {
        if (_count == 0)
        {
            Console.WriteLine("Список лікарів порожній.");
            return;
        }

        Console.WriteLine("\n=== Лікарі (" + _count + " / " + MaxDoctors + ") ===");
        for (int i = 0; i < _count; i++)
            Console.WriteLine(_doctors[i]);
        Console.WriteLine(new string('─', 60));
    }

    public void DisplayStats()
    {
        if (_count == 0)
        {
            Console.WriteLine("Немає лікарів для статистики.");
            return;
        }

        int availableNow = 0;
        for (int i = 0; i < _count; i++)
        {
            if (_doctors[i].IsAvailableNow)
                availableNow++;
        }

        Console.WriteLine("\n=== Статистика лікарів ===");
        Console.WriteLine("Всього:         " + _count);
        Console.WriteLine("Доступні зараз: " + availableNow);
        Console.WriteLine("По спеціальностях:");

        for (int i = 0; i < _count; i++)
        {
            Speciality spec = _doctors[i].Speciality;
            bool alreadyCounted = false;
            for (int j = 0; j < i; j++)
            {
                if (_doctors[j].Speciality == spec) { alreadyCounted = true; break; }
            }
            if (!alreadyCounted)
            {
                int specCount = 0;
                for (int k = 0; k < _count; k++)
                    if (_doctors[k].Speciality == spec) specCount++;
                Console.WriteLine("  " + ClinicFormatter.FormatSpeciality(spec) + ": " + specCount);
            }
        }

        Console.WriteLine("==========================");
    }

    // Повертає всіх лікарів (копія масиву)
    public Doctor[] GetAll()
    {
        Doctor[] result = new Doctor[_count];
        for (int i = 0; i < _count; i++)
            result[i] = _doctors[i];
        return result;
    }
}
