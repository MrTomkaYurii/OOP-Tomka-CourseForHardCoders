namespace ClinicApp.Models;

/// <summary>
/// Знімок поточного стану клініки.
/// Результат паралельних async запитів у AsyncClinicService.GetDashboardAsync().
///
/// record — незмінний тип даних, ідеальний для результату запиту:
///   — автоматичний Equals/GetHashCode по значеннях полів
///   — автоматичний ToString
///   — немає "стану" — тільки дані (немає set, тільки init)
///
/// Відміна від class: record не призначений для змін; він описує факт на момент часу.
/// </summary>
public record ClinicDashboard(
    int     PatientCount,
    int     DoctorCount,
    decimal TotalRevenue,
    int     UpcomingCount,
    int     TodayCount
)
{
    public override string ToString() =>
        $"Пацієнтів: {PatientCount} | Лікарів: {DoctorCount} | " +
        $"Дохід: {TotalRevenue:F2} грн | Майбутніх записів: {UpcomingCount} | Сьогодні: {TodayCount}";
}
