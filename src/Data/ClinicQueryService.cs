namespace ClinicApp.Data;

using Microsoft.EntityFrameworkCore;
using ClinicApp.Models;
using ClinicApp.Enums;

/// <summary>
/// ClinicQueryService — демонстрація просунутих запитів EF Core:
///   — IQueryable&lt;T&gt; відкладене виконання
///   — .Skip().Take() пагінація
///   — .Select(new DTO) проєкції
///   — .IgnoreQueryFilters() для soft-deleted записів
/// </summary>
public class ClinicQueryService
{
    private readonly ClinicDbContext _context;

    public ClinicQueryService(ClinicDbContext context)
    {
        _context = context;
    }

    // ─────────────────────────────────────────────────────────────────────
    // Task 1: IQueryable<T> — відкладене виконання (deferred execution)
    //
    // IQueryable<T> — це НЕ колекція даних. Це ОПИС запиту (Expression Tree).
    // SQL виконується тільки при матеріалізації: .ToList(), .First(), .Count()...
    //
    // IEnumerable<T> — дані вже в пам'яті; LINQ-операції виконуються в C#.
    // IQueryable<T>  — дані ще в БД; LINQ-операції перетворюються в SQL.
    // ─────────────────────────────────────────────────────────────────────

    /// <summary>
    /// Повертає IQueryable — SQL ще не виконується.
    /// Викликаючий код може ДОДАТИ ще умови перед матеріалізацією.
    /// </summary>
    public IQueryable<Patient> QueryPatients()
    {
        // Тут SQL-запит ще не виконується! Це лише "рецепт" запиту.
        return _context.Patients.AsNoTracking();
    }

    /// <summary>
    /// Демонстрація: IQueryable vs IEnumerable.
    /// Variant A — ефективний: фільтр у SQL (WHERE на сервері).
    /// Variant B — неефективний: всі записи в пам'ять, потім фільтр в C#.
    /// </summary>
    public (List<Patient> Efficient, List<Patient> Inefficient) DemoQueryableVsEnumerable(
        string lastNameFilter)
    {
        // ✅ ЕФЕКТИВНО: EF генерує WHERE LastName LIKE '%filter%' у SQL
        // Завантажується тільки відфільтрований результат.
        var efficient = _context.Patients
            .AsNoTracking()
            .Where(p => p.LastName.Contains(lastNameFilter))
            .ToList();    // <── тут SQL виконується

        // ❌ НЕЕФЕКТИВНО: .ToList() СПОЧАТКУ завантажує ВСЕ в пам'ять,
        // потім Where() фільтрує в C# — зайвий трафік і пам'ять.
        var inefficient = _context.Patients
            .AsNoTracking()
            .ToList()     // <── тут SQL: SELECT * FROM Patients (без фільтру!)
            .Where(p => p.LastName.Contains(lastNameFilter))
            .ToList();    // <── це вже LINQ to Objects, не SQL

        return (efficient, inefficient);
    }

    // ─────────────────────────────────────────────────────────────────────
    // Task 2: Пагінація — .Skip().Take()
    //
    // Skip((page-1) * pageSize) — пропустити N записів
    // Take(pageSize)            — взяти наступні M записів
    //
    // SQL Server: OFFSET (n) ROWS FETCH NEXT (m) ROWS ONLY
    // ─────────────────────────────────────────────────────────────────────

    /// <summary>
    /// Пагінований список пацієнтів.
    /// Повертає сторінку + загальну кількість для відображення "Сторінка 1 з 5".
    /// </summary>
    public (List<Patient> Items, int TotalCount) GetPatientsPaged(
        int page     = 1,
        int pageSize = 10,
        string orderBy = "LastName")
    {
        // Рахуємо загальну кількість (окремий запит: SELECT COUNT(*))
        int total = _context.Patients.AsNoTracking().Count();

        // Будуємо IQueryable (SQL ще не виконується)
        IQueryable<Patient> query = _context.Patients.AsNoTracking();

        // Сортування — обов'язкове перед Skip/Take (без ORDER BY результат непередбачуваний)
        query = orderBy switch
        {
            "LastName"    => query.OrderBy(p => p.LastName).ThenBy(p => p.FirstName),
            "Age"         => query.OrderByDescending(p => p.DateOfBirth), // молодші спочатку
            "Appointments"=> query.OrderByDescending(p => p.Appointments.Count),
            _             => query.OrderBy(p => p.LastName),
        };

        // Пагінація: Skip і Take додають OFFSET/FETCH до SQL
        var items = query
            .Skip((page - 1) * pageSize)   // пропустити записи попередніх сторінок
            .Take(pageSize)                 // взяти тільки поточну сторінку
            .ToList();                      // <── виконується SQL

        return (items, total);
    }

    /// <summary>
    /// Пагінований список записів на прийом з фільтрацією.
    /// </summary>
    public (List<Appointment> Items, int TotalCount) GetAppointmentsPaged(
        int page          = 1,
        int pageSize      = 10,
        AppointmentStatus? status = null,
        int? patientId    = null)
    {
        IQueryable<Appointment> query = _context.Appointments
            .AsNoTracking()
            .Include(a => a.Patient)
            .Include(a => a.Doctor);

        // Умовне застосування фільтрів — IQueryable не виконується до ToList()
        if (status.HasValue)
            query = query.Where(a => a.Status == status.Value);

        if (patientId.HasValue)
            query = query.Where(a => a.PatientId == patientId.Value);

        int total = query.Count();  // COUNT з тими самими фільтрами

        var items = query
            .OrderByDescending(a => a.ScheduledAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToList();

        return (items, total);
    }

    // ─────────────────────────────────────────────────────────────────────
    // Task 3: Проєкції — Select(p => new DTO { ... })
    //
    // Замість завантаження повних об'єктів Patient (усі стовпці),
    // вибираємо тільки потрібні поля.
    //
    // SQL: SELECT Id, FirstName, LastName, DateOfBirth, Phone, BloodType
    //        FROM Patients WHERE ...
    // (НЕ завантажує Email, Appointments, MedicalRecords, RowVersion тощо)
    // ─────────────────────────────────────────────────────────────────────

    /// <summary>
    /// Список пацієнтів як PatientSummaryDto — тільки потрібні поля + кількість записів.
    /// SQL: SELECT ... COUNT(Appointments) — один запит, без завантаження Patient-об'єктів.
    /// </summary>
    public List<PatientSummaryDto> GetPatientSummaries(int page = 1, int pageSize = 20)
    {
        return _context.Patients
            .AsNoTracking()
            .OrderBy(p => p.LastName)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(p => new PatientSummaryDto(
                p.Id,
                p.FirstName + " " + p.LastName,     // обчислення в SQL
                DateTime.Today.Year - p.DateOfBirth.Year, // приблизний вік
                p.Phone,
                p.BloodType.ToString(),
                p.Appointments.Count                 // COUNT subquery
            ))
            .ToList();
    }

    /// <summary>
    /// Список записів на прийом як AppointmentSummaryDto.
    /// Об'єднує дані з Appointments, Patients, Doctors — без завантаження повних об'єктів.
    /// </summary>
    public List<AppointmentSummaryDto> GetAppointmentSummaries(
        int page = 1, int pageSize = 20,
        AppointmentStatus? status = null)
    {
        IQueryable<Appointment> query = _context.Appointments.AsNoTracking();

        if (status.HasValue)
            query = query.Where(a => a.Status == status.Value);

        return query
            .OrderByDescending(a => a.ScheduledAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(a => new AppointmentSummaryDto(
                a.Id,
                a.Patient!.FirstName + " " + a.Patient.LastName,
                a.Doctor!.FirstName + " " + a.Doctor.LastName,
                a.Doctor.Speciality.ToString(),
                a.ScheduledAt,
                a.DurationMinutes,
                a.Status.ToString(),
                (decimal)a.DurationMinutes * 10m,  // GetCost() логіка прямо в SQL
                a.IsPaid,
                a.GetType().Name  // NOTE: це виконається в C#, не SQL
            ))
            .ToList();
    }

    // ─────────────────────────────────────────────────────────────────────
    // Task 4: Global Query Filter та Soft Delete
    //
    // HasQueryFilter(p => !p.IsDeleted) додається в OnModelCreating.
    // Кожен запит до Patients автоматично: WHERE IsDeleted = 0
    //
    // Щоб побачити "видалені" записи — .IgnoreQueryFilters()
    // ─────────────────────────────────────────────────────────────────────

    /// <summary>
    /// "М'яке видалення": встановлює IsDeleted = true замість DELETE.
    /// </summary>
    public bool SoftDeletePatient(int patientId)
    {
        // HasQueryFilter автоматично додає WHERE IsDeleted = 0 —
        // тобто знайде тільки НЕвидаленого пацієнта
        var patient = _context.Patients.FirstOrDefault(p => p.Id == patientId);
        if (patient is null) return false;

        patient.SoftDelete();
        _context.SaveChanges();  // UPDATE Patients SET IsDeleted = 1 WHERE Id = @id
        return true;
    }

    /// <summary>
    /// Отримати всіх пацієнтів включно з "видаленими".
    /// .IgnoreQueryFilters() — ігнорує HasQueryFilter для цього запиту.
    /// </summary>
    public List<Patient> GetAllPatientsIncludingDeleted()
    {
        return _context.Patients
            .AsNoTracking()
            .IgnoreQueryFilters()   // скасовуємо HasQueryFilter для цього запиту
            .OrderBy(p => p.LastName)
            .ToList();
    }

    /// <summary>
    /// Тільки "видалені" пацієнти — для адміністративного відновлення.
    /// </summary>
    public List<Patient> GetDeletedPatients()
    {
        return _context.Patients
            .AsNoTracking()
            .IgnoreQueryFilters()
            .Where(p => p.IsDeleted)    // тепер явно фільтруємо тільки видалених
            .ToList();
    }

    /// <summary>
    /// Статистика по лікарях — без матеріалізації повних Doctor об'єктів.
    /// GROUP BY у SQL: кількість і виручка по кожному лікарю.
    /// </summary>
    public List<(string DoctorName, string Speciality, int AppointmentCount, decimal Revenue)>
        GetDoctorRevenueSummary()
    {
        return _context.Doctors
            .AsNoTracking()
            .Select(d => new
            {
                Name      = d.FirstName + " " + d.LastName,
                Speciality = d.Speciality.ToString(),
                Count     = d.Appointments.Count(a => a.Status != AppointmentStatus.Cancelled),
                Revenue   = d.Appointments
                    .Where(a => a.IsPaid)
                    .Sum(a => (decimal)a.DurationMinutes * 10m),
            })
            .OrderByDescending(x => x.Revenue)
            .ToList()
            .Select(x => (x.Name, x.Speciality, x.Count, x.Revenue))
            .ToList();
    }
}
