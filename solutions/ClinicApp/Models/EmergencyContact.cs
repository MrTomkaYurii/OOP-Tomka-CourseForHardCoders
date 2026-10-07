namespace ClinicApp.Models;

/// <summary>
/// EmergencyContact — Value Object для контакту на випадок надзвичайної ситуації.
///
/// Value Object (Owned Entity в EF термінах):
///   — не має власного Id
///   — існує тільки як частина власника (Patient)
///   — зберігається в таблиці Patients (не в окремій таблиці)
///   — стовпці: EmergencyContact_Name, EmergencyContact_Phone, EmergencyContact_Relationship
///
/// Відмінність від ValueConverter:
///   ValueConverter (WorkSchedule) — один стовпець, серіалізація в рядок.
///   OwnsOne (EmergencyContact) — кілька стовпців у таблиці власника.
/// </summary>
public class EmergencyContact
{
    // EF Core Owned Entity: EF встановлює властивості через setters після побудови
    public string Name         { get; private set; } = "";
    public string Phone        { get; private set; } = "";
    public string Relationship { get; private set; } = "";

    // EF Core hydration constructor
    public EmergencyContact() { }

    public EmergencyContact(string name, string phone, string relationship)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Ім'я контакту не може бути порожнім.");
        if (string.IsNullOrWhiteSpace(phone))
            throw new ArgumentException("Телефон контакту не може бути порожнім.");
        Name         = name.Trim();
        Phone        = phone.Trim();
        Relationship = relationship.Trim();
    }

    public override string ToString() =>
        Name + " (" + Relationship + ") — " + Phone;
}
