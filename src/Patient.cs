namespace ClinicApp;

public class Patient
{
    private static int _nextId = 1;

    public int Id { get; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public DateTime DateOfBirth { get; set; }
    public string BloodType { get; set; }
    public string Phone { get; set; }
    public string? Email { get; set; }

    public string FullName => FirstName + " " + LastName;

    public int Age
    {
        get
        {
            var today = DateTime.Today;
            int age = today.Year - DateOfBirth.Year;
            if (DateOfBirth.Date > today.AddYears(-age))
                age--;
            return age;
        }
    }

    public bool IsAdult => Age >= 18;

    // Constructor 1: default values
    public Patient()
        : this("Невідомий", "Пацієнт", new DateTime(2000, 1, 1), "Невідомо", "0000000000")
    {
    }

    // Constructor 2: first and last name only
    public Patient(string firstName, string lastName)
        : this(firstName, lastName, new DateTime(2000, 1, 1), "Невідомо", "0000000000")
    {
    }

    // Constructor 3: full — assigns Id
    public Patient(string firstName, string lastName, DateTime dateOfBirth, string bloodType, string phone)
    {
        Id = _nextId++;
        FirstName = firstName;
        LastName = lastName;
        DateOfBirth = dateOfBirth;
        BloodType = bloodType;
        Phone = phone;
    }

    public string GetAgeCategory()
    {
        if (Age < 18) return "дитина";
        if (Age < 60) return "дорослий";
        return "літній";
    }

    public override string ToString()
    {
        string result = $"[{Id}] {FullName} | Вік: {Age} ({GetAgeCategory()}) | Кров: {BloodType} | Тел: {Phone}";
        if (Email is not null)
            result += $" | Email: {Email}";
        return result;
    }
}
