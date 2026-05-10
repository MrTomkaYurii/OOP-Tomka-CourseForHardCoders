namespace ClinicApp.Models;

using ClinicApp.Enums;
using ClinicApp.Interfaces;
using ClinicApp.Utils;

public class Doctor : ISchedulable, IIdentifiable
{
    private static int _nextId = 1;

    private string _firstName = "";
    private string _lastName = "";
    private string _licenseNumber = "";
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

    public Speciality Speciality { get; set; }

    public string LicenseNumber
    {
        get => _licenseNumber;
        set
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("Номер ліцензії не може бути порожнім.");
            _licenseNumber = value;
        }
    }

    public string Phone
    {
        get => _phone;
        set { ClinicValidator.ValidatePhone(value); _phone = value; }
    }

    public WorkSchedule Schedule { get; set; }

    public string FullName => FirstName + " " + LastName;
    public bool IsAvailableNow => Schedule.IsNow;

    public Doctor()
        : this("Невідомий", "Лікар", Speciality.General, "LIC-000", "0000000000")
    {
    }

    public Doctor(string firstName, string lastName, Speciality speciality)
        : this(firstName, lastName, speciality, "LIC-000", "0000000000")
    {
    }

    public Doctor(string firstName, string lastName, Speciality speciality, string licenseNumber, string phone)
    {
        Id = _nextId++;
        FirstName = firstName;
        LastName = lastName;
        Speciality = speciality;
        LicenseNumber = licenseNumber;
        Phone = phone;
        Schedule = new WorkSchedule(8, 17);
    }

    public bool CanAcceptAt(int hour) => Schedule.Contains(hour);

    public bool CanSchedule(DateTime at) => Schedule.Contains(at.Hour);

    public DateTime[] GetAvailableSlots(DateTime date, int slotCount)
    {
        int hoursInSchedule = Schedule.End - Schedule.Start;
        int count = slotCount < hoursInSchedule ? slotCount : hoursInSchedule;
        DateTime[] slots = new DateTime[count];
        for (int i = 0; i < count; i++)
            slots[i] = date.Date.AddHours(Schedule.Start + i);
        return slots;
    }

    public override string ToString()
    {
        string availability = IsAvailableNow ? "доступний зараз" : "не в робочий час";
        return "[" + Id + "] " + FullName +
               " | " + ClinicFormatter.FormatSpeciality(Speciality) +
               " | " + LicenseNumber +
               " | Тел: " + ClinicFormatter.FormatPhone(Phone) +
               " | " + Schedule +
               " | " + availability;
    }
}
