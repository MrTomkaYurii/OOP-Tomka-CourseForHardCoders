namespace ClinicApp.Services;

using ClinicApp.Models;
using ClinicApp.Enums;

/// <summary>
/// IDoctorService — інтерфейс сервісу лікарів (ISP + DIP).
/// Окремий від IPatientService — клієнт що знає тільки про лікарів
/// не залежить від операцій з пацієнтами.
/// </summary>
public interface IDoctorService
{
    Task<List<Doctor>> GetAllAsync(CancellationToken ct = default);
    Task<Doctor?>      GetByIdAsync(int id, CancellationToken ct = default);
    Task<List<Doctor>> GetBySpecialityAsync(Speciality speciality, CancellationToken ct = default);
    Task<int>          CountAsync(CancellationToken ct = default);
}
