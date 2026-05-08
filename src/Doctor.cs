namespace ClinicApp;

public class Doctor
{
    private static int _nextId = 1;

    public int Id { get; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string Speciality { get; set; }
    public string LicenseNumber { get; set; }
    public string Phone { get; set; }
    public int WorkStartHour { get; set; }
    public int WorkEndHour { get; set; }

    public string FullName => FirstName + " " + LastName;

    public int WorkingHoursPerDay => WorkEndHour - WorkStartHour;

    public string WorkSchedule => WorkStartHour.ToString("D2") + ":00–" + WorkEndHour.ToString("D2") + ":00";

    public bool IsAvailableNow
    {
        get
        {
            int currentHour = DateTime.Now.Hour;
            return currentHour >= WorkStartHour && currentHour < WorkEndHour;
        }
    }

    // Конструктор 1: значення за замовчуванням
    public Doctor()
        : this("Невідомий", "Лікар", "Загальна практика", "LIC-000", "0000000000")
    {
    }

    // Конструктор 2: ім'я + спеціальність
    public Doctor(string firstName, string lastName, string speciality)
        : this(firstName, lastName, speciality, "LIC-000", "0000000000")
    {
    }

    // Конструктор 3: повний — призначає Id, встановлює робочий час 8:00–17:00
    public Doctor(string firstName, string lastName, string speciality, string licenseNumber, string phone)
    {
        Id = _nextId++;
        FirstName = firstName;
        LastName = lastName;
        Speciality = speciality;
        LicenseNumber = licenseNumber;
        Phone = phone;
        WorkStartHour = 8;
        WorkEndHour = 17;
    }

    public bool CanAcceptAt(int hour)
    {
        return hour >= WorkStartHour && hour < WorkEndHour;
    }

    public override string ToString()
    {
        string availability = IsAvailableNow ? "доступний зараз" : "не в робочий час";
        return "[" + Id + "] " + FullName + " | " + Speciality + " | " + LicenseNumber +
               " | Тел: " + Phone + " | " + WorkSchedule + " (" + WorkingHoursPerDay + " год) | " + availability;
    }
}
