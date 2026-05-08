namespace ClinicApp;

public class AppointmentManager
{
    private const int MaxAppointments = 500;
    private Appointment[] _appointments = new Appointment[MaxAppointments];
    private int _count = 0;

    private PatientManager _patients;
    private DoctorManager _doctors;

    public int Count => _count;

    public Appointment this[int index]
    {
        get
        {
            if (index < 0 || index >= _count) return null!;
            return _appointments[index];
        }
    }

    public AppointmentManager(PatientManager patients, DoctorManager doctors)
    {
        _patients = patients;
        _doctors = doctors;
    }

    private Appointment FindById(int id)
    {
        for (int i = 0; i < _count; i++)
        {
            if (_appointments[i].Id == id)
                return _appointments[i];
        }
        return null!;
    }

    public bool Book(int patientId, int doctorId, DateTime scheduledAt, int durationMinutes = 30)
    {
        Patient patient = _patients.FindById(patientId);
        if (patient == null)
        {
            Console.WriteLine("Помилка: пацієнта з ID " + patientId + " не знайдено.");
            return false;
        }

        Doctor doctor = _doctors.FindById(doctorId);
        if (doctor == null)
        {
            Console.WriteLine("Помилка: лікаря з ID " + doctorId + " не знайдено.");
            return false;
        }

        if (_count >= MaxAppointments)
        {
            Console.WriteLine("Помилка: досягнуто ліміт записів.");
            return false;
        }

        Appointment appointment = new Appointment(patientId, doctorId, scheduledAt, durationMinutes);
        _appointments[_count] = appointment;
        _count++;

        Console.WriteLine("Запис [" + appointment.Id + "] створено: " +
                          patient.FullName + " → " + doctor.FullName +
                          " о " + scheduledAt.ToString("dd.MM.yyyy HH:mm"));
        return true;
    }

    public bool Cancel(int id, string reason = "")
    {
        Appointment appointment = FindById(id);
        if (appointment == null)
        {
            Console.WriteLine("Запис з ID " + id + " не знайдено.");
            return false;
        }

        string reasonArg = reason.Length > 0 ? reason : null!;
        bool result = appointment.Cancel(reasonArg);
        if (result)
            Console.WriteLine("Запис [" + id + "] скасовано.");
        else
            Console.WriteLine("Запис [" + id + "] неможливо скасувати (статус: " + appointment.Status + ").");
        return result;
    }

    public bool Complete(int id)
    {
        Appointment appointment = FindById(id);
        if (appointment == null)
        {
            Console.WriteLine("Запис з ID " + id + " не знайдено.");
            return false;
        }

        bool result = appointment.Complete();
        if (result)
            Console.WriteLine("Запис [" + id + "] позначено як виконаний.");
        else
            Console.WriteLine("Запис [" + id + "] неможливо завершити (статус: " + appointment.Status + ").");
        return result;
    }

    public Appointment[] GetByPatient(int patientId)
    {
        int matchCount = 0;
        for (int i = 0; i < _count; i++)
        {
            if (_appointments[i].PatientId == patientId)
                matchCount++;
        }

        Appointment[] result = new Appointment[matchCount];
        int idx = 0;
        for (int i = 0; i < _count; i++)
        {
            if (_appointments[i].PatientId == patientId)
                result[idx++] = _appointments[i];
        }
        return result;
    }

    public Appointment[] GetByDoctor(int doctorId)
    {
        int matchCount = 0;
        for (int i = 0; i < _count; i++)
        {
            if (_appointments[i].DoctorId == doctorId)
                matchCount++;
        }

        Appointment[] result = new Appointment[matchCount];
        int idx = 0;
        for (int i = 0; i < _count; i++)
        {
            if (_appointments[i].DoctorId == doctorId)
                result[idx++] = _appointments[i];
        }
        return result;
    }

    // Перевантаження: отримати записи за датою через окремі параметри
    public Appointment[] GetByDate(int year, int month, int day)
    {
        return GetByDate(new DateTime(year, month, day));
    }

    public Appointment[] GetByDate(DateTime date)
    {
        int matchCount = 0;
        for (int i = 0; i < _count; i++)
        {
            if (_appointments[i].ScheduledAt.Date == date.Date)
                matchCount++;
        }

        Appointment[] result = new Appointment[matchCount];
        int idx = 0;
        for (int i = 0; i < _count; i++)
        {
            if (_appointments[i].ScheduledAt.Date == date.Date)
                result[idx++] = _appointments[i];
        }
        return result;
    }

    public Appointment[] GetUpcoming()
    {
        int matchCount = 0;
        for (int i = 0; i < _count; i++)
        {
            if (_appointments[i].IsUpcoming)
                matchCount++;
        }

        Appointment[] result = new Appointment[matchCount];
        int idx = 0;
        for (int i = 0; i < _count; i++)
        {
            if (_appointments[i].IsUpcoming)
                result[idx++] = _appointments[i];
        }
        return result;
    }

    public void DisplayAppointment(Appointment a)
    {
        Patient patient = _patients.FindById(a.PatientId);
        Doctor doctor = _doctors.FindById(a.DoctorId);

        string patientName = patient != null ? patient.FullName : "Пацієнт #" + a.PatientId;
        string doctorName  = doctor  != null ? doctor.FullName  : "Лікар #"   + a.DoctorId;

        string line = "[" + a.Id + "] " + patientName + " → " + doctorName +
                      " | " + a.ScheduledAt.ToString("dd.MM.yyyy HH:mm") +
                      "–" + a.EndsAt.ToString("HH:mm") +
                      " | " + a.Status;

        if (a.Notes != null)
            line += " | " + a.Notes;

        Console.WriteLine(line);
    }

    public void DisplayList(Appointment[] appointments)
    {
        if (appointments.Length == 0)
        {
            Console.WriteLine("Записів не знайдено.");
            return;
        }

        for (int i = 0; i < appointments.Length; i++)
            DisplayAppointment(appointments[i]);
    }
}
