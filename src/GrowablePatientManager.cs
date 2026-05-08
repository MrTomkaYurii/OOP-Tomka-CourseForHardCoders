namespace ClinicApp;

public class GrowablePatientManager
{
    private Patient[] _patients = new Patient[4];
    private int _count = 0;

    public int Count => _count;
    public int Capacity => _patients.Length;

    private void Grow()
    {
        int newCapacity = _patients.Length * 2;
        Patient[] newArray = new Patient[newCapacity];
        for (int i = 0; i < _count; i++)
            newArray[i] = _patients[i];
        _patients = newArray;
        Console.WriteLine("  Масив заповнений! Розширення: " + _count + " → " + newCapacity);
    }

    public void Add(Patient patient)
    {
        if (_count == _patients.Length)
            Grow();
        _patients[_count] = patient;
        _count++;
        Console.WriteLine("  Додано [" + patient.Id + "]. Розмір: " + _count + " / " + _patients.Length);
    }

    public Patient FindById(int id)
    {
        for (int i = 0; i < _count; i++)
            if (_patients[i].Id == id) return _patients[i];
        return null!;
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
        if (_count == 0)
        {
            Console.WriteLine("Список порожній.");
            return;
        }
        Console.WriteLine("=== GrowablePatientManager (" + _count + " / " + _patients.Length + " ємність) ===");
        for (int i = 0; i < _count; i++)
            Console.WriteLine(_patients[i]);
    }
}
