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

    public int Id { get; }

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
