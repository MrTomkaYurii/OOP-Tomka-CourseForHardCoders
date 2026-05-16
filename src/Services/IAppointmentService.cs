namespace ClinicApp.Services;

using ClinicApp.Models;
using ClinicApp.Enums;

/// <summary>
/// IAppointmentService — інтерфейс сервісу записів на прийом (ISP + DIP).
/// </summary>
public interface IAppointmentService
{
    Task<List<Appointment>> GetUpcomingAsync(CancellationToken ct = default);
    Task<List<Appointment>> GetByPatientAsync(int patientId, CancellationToken ct = default);
    Task<List<Appointment>> GetByDoctorAsync(int doctorId, CancellationToken ct = default);
    Task<int>               BookAsync(Appointment appointment, CancellationToken ct = default);
    Task<bool>              CancelAsync(int id, CancellationToken ct = default);
    Task<bool>              CompleteAsync(int id, CancellationToken ct = default);
    Task<decimal>           GetTotalRevenueAsync(CancellationToken ct = default);
}
