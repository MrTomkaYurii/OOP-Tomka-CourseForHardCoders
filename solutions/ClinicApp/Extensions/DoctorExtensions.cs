namespace ClinicApp.Extensions;

using ClinicApp.Enums;
using ClinicApp.Models;

public static class DoctorExtensions
{
    // Лікарі певної спеціальності
    public static IEnumerable<Doctor> BySpeciality(this IEnumerable<Doctor> source, Speciality speciality)
        => source.Where(d => d.Speciality == speciality);

    // Лікарі, що зараз у робочому часі
    public static IEnumerable<Doctor> Available(this IEnumerable<Doctor> source)
        => source.Where(d => d.IsAvailableNow);

    // Лікарі, що мають хоч один запис у переданому списку
    public static IEnumerable<Doctor> WithAppointments(
        this IEnumerable<Doctor> source,
        IEnumerable<Appointment> appointments)
        => source.Where(d => appointments.Any(a => a.DoctorId == d.Id));
}
