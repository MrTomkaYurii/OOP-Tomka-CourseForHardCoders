namespace ClinicApp.Managers;

using ClinicApp.Models;

public class MedicalRecordManager
{
    private const int MaxRecords = 1000;
    private MedicalRecord[] _records = new MedicalRecord[MaxRecords];
    private int _count = 0;

    public int Count => _count;

    public MedicalRecord this[int index]
    {
        get
        {
            if (index < 0 || index >= _count) return null!;
            return _records[index];
        }
    }

    public void Add(MedicalRecord record)
    {
        if (_count >= MaxRecords)
        {
            Console.WriteLine("Помилка: досягнуто ліміт медичних записів.");
            return;
        }
        _records[_count++] = record;
        Console.WriteLine("Запис [" + record.Id + "] " + record.GetRecordType() + " додано.");
    }

    public MedicalRecord FindById(int id)
    {
        for (int i = 0; i < _count; i++)
            if (_records[i].Id == id) return _records[i];
        return null!;
    }

    public MedicalRecord[] GetByPatient(int patientId)
    {
        int n = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId) n++;

        MedicalRecord[] result = new MedicalRecord[n];
        int idx = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId) result[idx++] = _records[i];
        return result;
    }

    public MedicalRecord[] GetByDoctor(int doctorId)
    {
        int n = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].DoctorId == doctorId) n++;

        MedicalRecord[] result = new MedicalRecord[n];
        int idx = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].DoctorId == doctorId) result[idx++] = _records[i];
        return result;
    }

    public Diagnosis[] GetDiagnoses(int patientId)
    {
        int n = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId && _records[i] is Diagnosis) n++;

        Diagnosis[] result = new Diagnosis[n];
        int idx = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId && _records[i] is Diagnosis d) result[idx++] = d;
        return result;
    }

    public LabResult[] GetLabResults(int patientId)
    {
        int n = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId && _records[i] is LabResult) n++;

        LabResult[] result = new LabResult[n];
        int idx = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId && _records[i] is LabResult lr) result[idx++] = lr;
        return result;
    }

    public Prescription[] GetPrescriptions(int patientId)
    {
        int n = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId && _records[i] is Prescription) n++;

        Prescription[] result = new Prescription[n];
        int idx = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId && _records[i] is Prescription p) result[idx++] = p;
        return result;
    }

    public Diagnosis[] GetChronicDiagnoses(int patientId)
    {
        int n = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId && _records[i] is Diagnosis d && d.IsChronic) n++;

        Diagnosis[] result = new Diagnosis[n];
        int idx = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId && _records[i] is Diagnosis diag && diag.IsChronic)
                result[idx++] = diag;
        return result;
    }

    public Prescription[] GetActivePrescriptions(int patientId)
    {
        int n = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId && _records[i] is Prescription p && p.IsActive()) n++;

        Prescription[] result = new Prescription[n];
        int idx = 0;
        for (int i = 0; i < _count; i++)
            if (_records[i].PatientId == patientId && _records[i] is Prescription pr && pr.IsActive())
                result[idx++] = pr;
        return result;
    }

    public void DisplayPatientSummary(int patientId)
    {
        MedicalRecord[] all = GetByPatient(patientId);
        if (all.Length == 0) { Console.WriteLine("Медичних записів не знайдено."); return; }

        int diagCount = 0, labCount = 0, prescCount = 0;
        for (int i = 0; i < all.Length; i++)
        {
            if (all[i] is Diagnosis) diagCount++;
            else if (all[i] is LabResult) labCount++;
            else if (all[i] is Prescription) prescCount++;
        }

        Console.WriteLine("=== Медична картка пацієнта #" + patientId + " ===");
        Console.WriteLine("Всього записів: " + all.Length +
                          " (діагнозів: " + diagCount +
                          ", аналізів: " + labCount +
                          ", рецептів: " + prescCount + ")");

        Diagnosis[] chronic = GetChronicDiagnoses(patientId);
        if (chronic.Length > 0)
        {
            Console.WriteLine("Хронічні діагнози (" + chronic.Length + "):");
            for (int i = 0; i < chronic.Length; i++)
                Console.WriteLine("  " + chronic[i]);
        }

        Prescription[] active = GetActivePrescriptions(patientId);
        if (active.Length > 0)
        {
            Console.WriteLine("Активні рецепти (" + active.Length + "):");
            for (int i = 0; i < active.Length; i++)
                Console.WriteLine("  " + active[i] + " | до " + active[i].ExpiresAt.ToString("dd.MM.yyyy"));
        }
    }

    public void DisplayList(MedicalRecord[] records)
    {
        if (records.Length == 0) { Console.WriteLine("Записів не знайдено."); return; }
        for (int i = 0; i < records.Length; i++) Console.WriteLine(records[i]);
    }

    public void DisplayAll()
    {
        if (_count == 0) { Console.WriteLine("Медичних записів немає."); return; }
        Console.WriteLine("\n=== Медичні записи (" + _count + " / " + MaxRecords + ") ===");
        for (int i = 0; i < _count; i++) Console.WriteLine(_records[i]);
        Console.WriteLine(new string('─', 60));
    }
}
