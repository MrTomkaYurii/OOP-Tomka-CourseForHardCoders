namespace ClinicApp.Extensions;

using ClinicApp.Models;

public static class AppointmentExtensions
{
    // Тільки неоплачені (і не скасовані)
    public static IEnumerable<Appointment> Unpaid(this IEnumerable<Appointment> source)
        => source.Where(a => !a.IsPaid && !a.IsCancelled);

    // Тільки майбутні заплановані
    public static IEnumerable<Appointment> Upcoming(this IEnumerable<Appointment> source)
        => source.Where(a => a.IsUpcoming);

    // Записи конкретного лікаря
    public static IEnumerable<Appointment> ByDoctor(this IEnumerable<Appointment> source, int doctorId)
        => source.Where(a => a.DoctorId == doctorId);

    // Записи конкретного пацієнта
    public static IEnumerable<Appointment> ByPatient(this IEnumerable<Appointment> source, int patientId)
        => source.Where(a => a.PatientId == patientId);

    // Прострочені: дата минула, не скасовані, не оплачені
    public static IEnumerable<Appointment> Overdue(this IEnumerable<Appointment> source)
        => source.Where(a => a.ScheduledAt < DateTime.Now && !a.IsCancelled && !a.IsPaid);

    // Дорожче за поріг — демонстрація замикання на параметрі
    public static IEnumerable<Appointment> CostAbove(this IEnumerable<Appointment> source, decimal minCost)
        => source.Where(a => a.GetCost() > minCost);

    // Сума вартості всіх прийомів у послідовності
    public static decimal TotalCost(this IEnumerable<Appointment> source)
        => source.Sum(a => a.GetCost());
}
