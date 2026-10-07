namespace ClinicApp.Models;

using ClinicApp.Enums;
using ClinicApp.Interfaces;
using ClinicApp.Utils;

public class Patient : IIdentifiable
{
    private static int _nextId = 1;

    private string _firstName = "";
    private string _lastName = "";
    private DateTime _dateOfBirth;
    private string _phone = "";

    // private set — дозволяє EF Core встановлювати Id після збереження в БД
    public int Id { get; private set; }

    public string FirstName
    {
        get => _firstName;
        set { ClinicValidator.ValidateName(value, "Ім'я"); _firstName = value; }
    }

    public string LastName
    {
        get => _lastName;
        set { ClinicValidator.ValidateName(value, "Прізвище"); _lastName = value; }
    }

    public DateTime DateOfBirth
    {
        get => _dateOfBirth;
        set { ClinicValidator.ValidateDate(value, "Дата народження"); _dateOfBirth = value; }
    }

    public BloodType BloodType { get; set; }

    public string Phone
    {
        get => _phone;
        set { ClinicValidator.ValidatePhone(value); _phone = value; }
    }

    public string? Email { get; set; }

    // Navigation properties
    public ICollection<Appointment>   Appointments   { get; private set; } = new List<Appointment>();
    public ICollection<MedicalRecord> MedicalRecords { get; private set; } = new List<MedicalRecord>();

    // Owned Entity — EmergencyContact зберігається в таблиці Patients (не окрема таблиця)
    public EmergencyContact? EmergencyContact { get; set; }

    // Concurrency Token — EF перевіряє при UPDATE/DELETE; кидає DbUpdateConcurrencyException якщо застарілий
    public byte[]? RowVersion { get; private set; }

    // Soft Delete — замість фізичного DELETE: позначаємо IsDeleted = true
    // Global Query Filter: HasQueryFilter(p => !p.IsDeleted) — EF автоматично додає WHERE IsDeleted = 0
    public bool IsDeleted { get; private set; }

    // "Видалити" — встановлює прапор, а не фізично видаляє з БД
    public void SoftDelete() { IsDeleted = true; }

    public string FullName => FirstName + " " + LastName;

    public int Age
    {
        get
        {
            var today = DateTime.Today;
            int age = today.Year - DateOfBirth.Year;
            if (DateOfBirth.Date > today.AddYears(-age)) age--;
            return age;
        }
    }

    public bool IsAdult => Age >= 18;

    // public Patient() нижче слугує і як EF Core hydration constructor.
    // EF Core може використовувати будь-який parameterless ctor (public, protected або private).
    // Оскільки клас вже має public Patient(), окремий protected ctor не потрібен.

    public Patient()
        : this("Невідомий", "Пацієнт", new DateTime(2000, 1, 1), BloodType.Unknown, "0000000000")
    {
    }

    public Patient(string firstName, string lastName)
        : this(firstName, lastName, new DateTime(2000, 1, 1), BloodType.Unknown, "0000000000")
    {
    }

    public Patient(string firstName, string lastName, DateTime dateOfBirth, BloodType bloodType, string phone)
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
        string result = "[" + Id + "] " + FullName +
                        " | Вік: " + ClinicFormatter.FormatAge(Age) + " (" + GetAgeCategory() + ")" +
                        " | Кров: " + ClinicFormatter.FormatBloodType(BloodType) +
                        " | Тел: " + ClinicFormatter.FormatPhone(Phone);
        if (Email != null && Email.Length > 0)
            result += " | Email: " + Email;
        return result;
    }
}
