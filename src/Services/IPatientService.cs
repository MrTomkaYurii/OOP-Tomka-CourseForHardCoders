namespace ClinicApp.Services;

using ClinicApp.Models;

/// <summary>
/// IPatientService — інтерфейс сервісу пацієнтів.
///
/// Lab 22 / Task 3: Interface Segregation Principle (ISP).
///
/// ISP: "Клієнти не повинні залежати від методів, які вони не використовують."
///
/// Погано (один великий інтерфейс):
///   interface IClinicService {
///       Task GetPatients(); Task AddPatient(); Task GetDoctors(); Task BookAppointment();
///       Task GenerateReport(); Task ExportCsv(); ...  // 20+ методів
///   }
///   — Клас що потребує тільки GetPatients() — все одно знає про Export, Report тощо.
///
/// Добре (ISP — розбито на маленькі інтерфейси):
///   IPatientService      — тільки операції з пацієнтами
///   IDoctorService       — тільки операції з лікарями
///   IAppointmentService  — тільки операції з прийомами
///
/// Lab 22 / Task 4: Dependency Inversion Principle (DIP).
///
/// DIP: "Модулі верхнього рівня не повинні залежати від модулів нижнього рівня.
///       Обидва повинні залежати від абстракцій."
///
/// Погано (пряма залежність від конкретного класу):
///   public class ReportGenerator {
///       private readonly PatientService _service;  // ← конкретний клас
///       public ReportGenerator(PatientService s) { _service = s; }
///   }
///
/// Добре (залежність від абстракції):
///   public class ReportGenerator {
///       private readonly IPatientService _service;  // ← інтерфейс
///       public ReportGenerator(IPatientService s) { _service = s; }
///   }
///   // DI-контейнер вирішить: яку реалізацію підставити
/// </summary>
public interface IPatientService
{
    Task<List<Patient>> GetAllAsync(CancellationToken ct = default);
    Task<Patient?>      GetByIdAsync(int id, CancellationToken ct = default);
    Task<List<Patient>> SearchAsync(string query, CancellationToken ct = default);
    Task<int>           AddAsync(Patient patient, CancellationToken ct = default);
    Task<bool>          SoftDeleteAsync(int id, CancellationToken ct = default);
    Task<int>           CountAsync(CancellationToken ct = default);
}
