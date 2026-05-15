namespace ClinicApp.Models;

/// <summary>
/// PatientSummaryDto — Data Transfer Object для відображення пацієнта в списках.
///
/// DTO — це "плаский" об'єкт без логіки, тільки дані.
/// Відмінність від Patient:
///   Patient — доменна модель: validators, computed props, navigation collections.
///   PatientSummaryDto — тільки те що потрібно для UI списку: ім'я, вік, телефон.
///
/// Навіщо проєкція замість повного Patient:
///   SELECT * FROM Patients         — всі стовпці (зайві дані)
///   SELECT Id, FirstName, LastName, — тільки потрібні (менше трафіку, швидше)
///          DateOfBirth, Phone FROM Patients
/// </summary>
public record PatientSummaryDto(
    int      Id,
    string   FullName,
    int      Age,
    string   Phone,
    string   BloodType,
    int      AppointmentCount
);
