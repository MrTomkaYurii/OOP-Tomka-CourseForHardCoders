namespace ClinicApp.Extensions;

using ClinicApp.Enums;
using ClinicApp.Models;

public static class PatientExtensions
{
    // Тільки повнолітні (18+)
    public static IEnumerable<Patient> Adults(this IEnumerable<Patient> source)
        => source.Where(p => p.Age >= 18);

    // Пацієнти з певною групою крові
    public static IEnumerable<Patient> ByBloodType(this IEnumerable<Patient> source, BloodType bloodType)
        => source.Where(p => p.BloodType == bloodType);

    // Тільки ті пацієнти, що мають хоч один запис у переданому списку
    public static IEnumerable<Patient> WithAppointments(
        this IEnumerable<Patient> source,
        IEnumerable<Appointment> appointments)
        => source.Where(p => appointments.Any(a => a.PatientId == p.Id));
}
