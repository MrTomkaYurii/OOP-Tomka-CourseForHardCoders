namespace ClinicApp.Models;

/// <summary>
/// AppointmentSummaryDto — DTO для відображення записів у списках і звітах.
/// Зберігає тільки необхідні поля — не підтягує повні Patient та Doctor об'єкти.
/// </summary>
public record AppointmentSummaryDto(
    int      Id,
    string   PatientFullName,
    string   DoctorFullName,
    string   DoctorSpeciality,
    DateTime ScheduledAt,
    int      DurationMinutes,
    string   Status,
    decimal  Cost,
    bool     IsPaid,
    string   AppointmentType
);
