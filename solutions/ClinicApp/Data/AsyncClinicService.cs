namespace ClinicApp.Data;

using Microsoft.EntityFrameworkCore;
using ClinicApp.Models;
using ClinicApp.Enums;

/// <summary>
/// AsyncClinicService — демонстрація async/await в контексті EF Core.
///
/// Основний принцип:
///   Синхронний виклик: потік ЗАБЛОКОВАНИЙ під час очікування SQL
///     thread ──BLOCKED──────────────▶ SQL done ──▶ continue
///
///   Асинхронний виклик: потік ВІЛЬНИЙ під час очікування SQL
///     thread ──FREE──▶ (SQL in progress) ──▶ resume via continuation
///
/// Це критично для серверних застосунків: якщо 100 запитів одночасно,
/// синхронний код заблокує 100 потоків; async — жодного.
///
/// Tasks:
///   Task 2 — базові async методи EF Core
///   Task 3 — Task.WhenAll, Parallel.ForEachAsync, CancellationToken
///   Task 4 — AggregateException, ContinueWith
///   Task 5 — IProgress&lt;T&gt; для звітування прогресу
/// </summary>
public class AsyncClinicService
{
    private readonly ClinicDbContext _context;

    public AsyncClinicService(ClinicDbContext context)
    {
        _context = context;
    }

    // ─────────────────────────────────────────────────────────────────────
    // Task 2: Базові async методи EF Core
    //
    // Кожен синхронний метод EF Core має async-варіант:
    //   .ToList()           → .ToListAsync(ct)
    //   .FirstOrDefault()   → .FirstOrDefaultAsync(ct)
    //   .Count()            → .CountAsync(ct)
    //   .Any()              → .AnyAsync(ct)
    //   .Sum()              → .SumAsync(ct)
    //   .SaveChanges()      → .SaveChangesAsync(ct)
    //
    // CancellationToken ct = default:
    //   — якщо не передати → CancellationToken.None (ніколи не скасовується)
    //   — якщо передати → операцію можна скасувати ззовні
    //
    // ConfigureAwait(false):
    //   — у бібліотечному коді: прибирає захоплення SynchronizationContext
    //   — у консольних застосунках: не має значення (немає UI-потоку)
    //   — у ASP.NET Core: теж не потрібен (немає SynchronizationContext з .NET Core)
    //   — залишається актуальним у WinForms/WPF-бібліотеках
    // ─────────────────────────────────────────────────────────────────────

    public async Task<List<Patient>> GetAllPatientsAsync(CancellationToken ct = default)
    {
        return await _context.Patients
            .AsNoTracking()
            .OrderBy(p => p.LastName)
            .ToListAsync(ct);
    }

    public async Task<Patient?> GetPatientByIdAsync(int id, CancellationToken ct = default)
    {
        return await _context.Patients
            .Include(p => p.Appointments)
            .FirstOrDefaultAsync(p => p.Id == id, ct);
    }

    public async Task<Doctor?> GetDoctorByIdAsync(int id, CancellationToken ct = default)
    {
        return await _context.Doctors
            .Include(d => d.Appointments)
            .FirstOrDefaultAsync(d => d.Id == id, ct);
    }

    public async Task<List<Appointment>> GetUpcomingAppointmentsAsync(CancellationToken ct = default)
    {
        return await _context.Appointments
            .AsNoTracking()
            .Include(a => a.Patient)
            .Include(a => a.Doctor)
            .Where(a => a.Status == AppointmentStatus.Scheduled && a.ScheduledAt > DateTime.Now)
            .OrderBy(a => a.ScheduledAt)
            .ToListAsync(ct);
    }

    public async Task<int> SaveAppointmentAsync(Appointment appointment, CancellationToken ct = default)
    {
        _context.Appointments.Add(appointment);
        // SaveChangesAsync → SQL INSERT без блокування потоку
        // Повертає кількість змінених рядків у БД
        return await _context.SaveChangesAsync(ct);
    }

    // ─────────────────────────────────────────────────────────────────────
    // Task 3: Task.WhenAll — паралельне виконання кількох async операцій
    //
    // Варіант A (ПОСЛІДОВНО — неефективно):
    //   int patients  = await _context.Patients.CountAsync();   // чекаємо
    //   int doctors   = await _context.Doctors.CountAsync();    // чекаємо
    //   decimal rev   = await _context.Appointments.SumAsync(); // чекаємо
    //   // Час = t1 + t2 + t3
    //
    // Варіант B (ПАРАЛЕЛЬНО — Task.WhenAll):
    //   var t1 = _context.Patients.CountAsync();     // ЗАПУСКАЄМО (не чекаємо)
    //   var t2 = _context.Doctors.CountAsync();      // ЗАПУСКАЄМО (не чекаємо)
    //   var t3 = _context.Appointments.SumAsync();   // ЗАПУСКАЄМО (не чекаємо)
    //   await Task.WhenAll(t1, t2, t3);             // ЧЕКАЄМО ВСІ РАЗОМ
    //   // Час = max(t1, t2, t3)
    //
    // УВАГА: DbContext НЕ є thread-safe!
    // Паралельні запити можливі тільки якщо кожен запит — окремий SQL-виклик
    // до одного і того ж _context. EF Core 8 підтримує це в межах одного контексту,
    // але не рекомендує виконувати паралельні SaveChanges до одного контексту.
    // ─────────────────────────────────────────────────────────────────────

    public async Task<ClinicDashboard> GetDashboardAsync(CancellationToken ct = default)
    {
        // Запускаємо всі п'ять запитів ОДНОЧАСНО
        var patientCountTask  = _context.Patients.CountAsync(ct);
        var doctorCountTask   = _context.Doctors.CountAsync(ct);
        var revenueTask       = _context.Appointments
                                    .Where(a => a.IsPaid)
                                    .SumAsync(a => (decimal)a.DurationMinutes * 10m, ct);
        var upcomingCountTask = _context.Appointments
                                    .CountAsync(a => a.Status == AppointmentStatus.Scheduled
                                                     && a.ScheduledAt > DateTime.Now, ct);
        var todayCountTask    = _context.Appointments
                                    .CountAsync(a => a.ScheduledAt.Date == DateTime.Today, ct);

        // Чекаємо поки ВСІ завершаться — результат доступний через .Result після WhenAll
        await Task.WhenAll(patientCountTask, doctorCountTask, revenueTask,
                           upcomingCountTask, todayCountTask);

        return new ClinicDashboard(
            patientCountTask.Result,
            doctorCountTask.Result,
            revenueTask.Result,
            upcomingCountTask.Result,
            todayCountTask.Result
        );
    }

    // ── Task.WhenAny — перемагає ПЕРШИЙ завершений Task ───────────────────
    //
    // Task.WhenAny використовується для:
    //   — race умов (хто відповість першим?)
    //   — таймаутів: WhenAny(actualTask, Task.Delay(timeout))
    //   — обробки результатів по мірі готовності

    public async Task<ClinicDashboard?> GetDashboardWithTimeoutAsync(int timeoutMs = 3000)
    {
        using var cts = new CancellationTokenSource();

        var dashboardTask = GetDashboardAsync(cts.Token);
        var timeoutTask   = Task.Delay(timeoutMs, cts.Token);

        var winner = await Task.WhenAny(dashboardTask, timeoutTask);

        if (winner == timeoutTask)
        {
            // Таймаут — скасовуємо дашборд-запит
            await cts.CancelAsync();
            Console.WriteLine($"[AsyncClinicService] Таймаут {timeoutMs}мс — дашборд не завантажено.");
            return null;
        }

        return dashboardTask.Result;
    }

    // ── Parallel.ForEachAsync — масова async операція ─────────────────────
    //
    // Parallel.ForEachAsync (C# /.NET 6+) — обробляє колекцію елементів
    // з обмеженим паралелізмом; підтримує async лямбди.
    //
    // Відміна від Task.WhenAll:
    //   Task.WhenAll          — фіксований список задач (знаємо всі наперед)
    //   Parallel.ForEachAsync — динамічна колекція + обмеження паралелізму
    //
    // ВАЖЛИВО для DbContext:
    //   DbContext НЕ є thread-safe для паралельних SaveChanges.
    //   Тому: завантажуємо дані спочатку → обробляємо паралельно в пам'яті → зберігаємо разом.

    public async Task<int> MarkAppointmentsAsPaidAsync(
        IEnumerable<int> appointmentIds,
        CancellationToken ct = default)
    {
        var ids = appointmentIds.ToList();

        // Крок 1: завантажуємо всі потрібні записи ОДНИМ запитом
        var appointments = await _context.Appointments
            .Where(a => ids.Contains(a.Id) && !a.IsPaid)
            .ToListAsync(ct);

        int count = 0;

        // Крок 2: паралельна обробка в пам'яті (CPU-bound, thread-safe)
        // Interlocked.Increment — атомарний інкремент для thread-safe лічильника
        await Parallel.ForEachAsync(appointments, new ParallelOptions
        {
            MaxDegreeOfParallelism = Environment.ProcessorCount,
            CancellationToken = ct
        }, async (appointment, token) =>
        {
            // Симуляція async обробки (наприклад: відправка повідомлення, виклик API)
            await Task.Delay(10, token);
            appointment.MarkPaid();
            Interlocked.Increment(ref count);
        });

        // Крок 3: зберігаємо всі зміни ОДНИМ SaveChangesAsync (не всередині ForEachAsync!)
        await _context.SaveChangesAsync(ct);
        return count;
    }

    // ── CancellationToken — скасування довгої операції ─────────────────────
    //
    // CancellationTokenSource — джерело токену скасування.
    // Сценарії використання:
    //   var cts = new CancellationTokenSource(TimeSpan.FromSeconds(5));  // авто-таймаут
    //   var cts = new CancellationTokenSource();  cts.Cancel();           // ручне скасування
    //
    // При скасуванні: async методи кидають OperationCanceledException.
    // Правило: ловити OperationCanceledException окремо від Exception.

    public async Task<List<Patient>> SearchPatientsAsync(string query, CancellationToken ct = default)
    {
        // ct.ThrowIfCancellationRequested() — можна перевіряти явно
        // Task.Delay(n, ct) — кидає OperationCanceledException при скасуванні

        // Симуляція затримки (в реальному коді це запит до пошукового індексу)
        await Task.Delay(200, ct);

        return await _context.Patients
            .AsNoTracking()
            .Where(p => p.FirstName.Contains(query) || p.LastName.Contains(query))
            .OrderBy(p => p.LastName)
            .ToListAsync(ct);
    }

    // ─────────────────────────────────────────────────────────────────────
    // Task 4: AggregateException — обробка помилок паралельних задач
    //
    // Task.WhenAll при помилці в одній або кількох задачах:
    //   — збирає ВСІ виключення в AggregateException
    //   — await Task.WhenAll(...) → розгортає і кидає ПЕРШЕ InnerException
    //   — щоб отримати ВСІ помилки → ContinueWith + перевірка t.Exception
    //
    // TaskContinuationOptions:
    //   OnlyOnFaulted          — виконати continuation тільки при помилці
    //   OnlyOnCanceled         — тільки при скасуванні
    //   OnlyOnRanToCompletion  — тільки при успіху
    //
    // task.IsCompletedSuccessfully — true якщо завершилась без помилки/скасування
    // task.IsFaulted              — true якщо завершилась з винятком
    // ─────────────────────────────────────────────────────────────────────

    public record PatientReport(
        Patient                Patient,
        List<Appointment>      RecentAppointments,
        List<MedicalRecord>    MedicalRecords,
        ClinicDashboard        Dashboard
    );

    public async Task<PatientReport> BuildPatientReportAsync(int patientId, CancellationToken ct = default)
    {
        // Запускаємо всі 4 задачі паралельно
        var patientTask      = _context.Patients
                                   .FirstOrDefaultAsync(p => p.Id == patientId, ct);
        var appointmentsTask = _context.Appointments
                                   .AsNoTracking()
                                   .Include(a => a.Doctor)
                                   .Where(a => a.PatientId == patientId)
                                   .OrderByDescending(a => a.ScheduledAt)
                                   .Take(5)
                                   .ToListAsync(ct);
        var recordsTask      = _context.MedicalRecords
                                   .AsNoTracking()
                                   .Where(r => r.PatientId == patientId)
                                   .ToListAsync(ct);
        var dashboardTask    = GetDashboardAsync(ct);

        // Об'єднуємо в одну задачу — для перехоплення AggregateException
        var allTasks = Task.WhenAll(patientTask, appointmentsTask, recordsTask, dashboardTask);

        // ContinueWith: виконується ПІСЛЯ allTasks завершення (незалежно від результату)
        // OnlyOnFaulted: виконується ТІЛЬКИ якщо allTasks завершилась з помилкою
        _ = allTasks.ContinueWith(t =>
        {
            // t.Exception — AggregateException з УСІМА помилками (не тільки першою!)
            foreach (var ex in t.Exception!.InnerExceptions)
                Console.WriteLine($"[AsyncClinicService] Паралельна помилка: {ex.GetType().Name}: {ex.Message}");
        }, TaskContinuationOptions.OnlyOnFaulted);

        try
        {
            await allTasks;
            // Якщо allTasks завершилась без помилок — всі результати доступні
        }
        catch (Exception ex)
        {
            // await розгортає AggregateException → кидає тільки ПЕРШЕ InnerException
            // Щоб отримати всі помилки — дивись ContinueWith вище
            throw new InvalidOperationException(
                $"Не вдалось зібрати звіт для пацієнта #{patientId}: {ex.Message}", ex);
        }

        // Перевірка статусу окремих задач
        if (!patientTask.IsCompletedSuccessfully || patientTask.Result is null)
            throw new KeyNotFoundException($"Пацієнта #{patientId} не знайдено.");

        return new PatientReport(
            patientTask.Result,
            appointmentsTask.Result,
            recordsTask.Result,
            dashboardTask.Result
        );
    }

    // ─────────────────────────────────────────────────────────────────────
    // Task 5: IProgress<T> — звітування про прогрес довгої операції
    //
    // Проблема: як повідомляти UI про прогрес з async методу?
    //   — не можна пряму записувати в Console всередині бібліотечного методу (зв'язок з UI)
    //   — IProgress<T> — абстракція: метод викликає Report(value), а хто слухає — не знає
    //
    // Progress<T> (конкретна реалізація IProgress<T>):
    //   — автоматично маршалює Report() на UI-потік (SynchronizationContext)
    //   — у консольному застосунку: просто виконує callback
    //
    // Патерн використання:
    //   // Викликаючий код (Program.cs):
    //   var progress = new Progress<(int Current, int Total, string Msg)>(p =>
    //       Console.WriteLine($"[{p.Current}/{p.Total}] {p.Msg}"));
    //   await service.BulkProcessAppointmentsAsync(AppointmentStatus.Completed, progress, ct);
    //
    //   // Метод нічого не знає про Console або UI — тільки викликає progress?.Report(...)
    // ─────────────────────────────────────────────────────────────────────

    public async Task<int> BulkProcessAppointmentsAsync(
        AppointmentStatus newStatus,
        IProgress<(int Current, int Total, string Message)>? progress = null,
        CancellationToken ct = default)
    {
        // Завантажуємо записи, що потребують обробки
        var appointments = await _context.Appointments
            .Where(a => a.Status == AppointmentStatus.Scheduled
                       && a.ScheduledAt < DateTime.Now)
            .ToListAsync(ct);

        int total   = appointments.Count;
        int current = 0;

        // Повідомляємо про початок (? — якщо progress == null, нічого не відбувається)
        progress?.Report((0, total, $"Знайдено {total} записів для обробки..."));

        if (total == 0)
        {
            progress?.Report((0, 0, "Немає записів для обробки."));
            return 0;
        }

        foreach (var appointment in appointments)
        {
            // ThrowIfCancellationRequested — перевіряємо скасування на кожній ітерації
            ct.ThrowIfCancellationRequested();

            // Симуляція async роботи: відправка email, виклик зовнішнього сервісу тощо
            await Task.Delay(80, ct);

            switch (newStatus)
            {
                case AppointmentStatus.Completed: appointment.Complete(); break;
                case AppointmentStatus.Cancelled: appointment.Cancel();   break;
            }

            current++;
            int percent = (int)((double)current / total * 100);
            progress?.Report((current, total, $"Оброблено {current}/{total} ({percent}%)"));
        }

        await _context.SaveChangesAsync(ct);
        progress?.Report((total, total, $"Завершено! Оновлено {total} записів."));
        return total;
    }

    // ── Демо: async void — чому це погано ──────────────────────────────────
    //
    // async void — єдиний прийнятний випадок: event handlers (onclick, etc.)
    // Проблема 1: виключення з async void НЕ можна перехопити ззовні (крашить процес)
    // Проблема 2: немає способу await async void — не можна дочекатись завершення
    // Проблема 3: CancellationToken не можна передати
    //
    // ПРАВИЛО: завжди async Task або async Task<T>, НІКОЛИ async void

    // ❌ ПОГАНО — так НЕ роблять (тільки для демонстрації у коментарі):
    // private async void BadFireAndForget() { ... }  // виключення вб'ють процес

    // ✅ ДОБРЕ — якщо треба fire-and-forget:
    public async Task GoodFireAndForgetAsync(CancellationToken ct = default)
    {
        // Повертаємо Task — caller може await якщо хоче, або просто _ = service.GoodFireAndForgetAsync()
        await Task.Delay(100, ct);
        Console.WriteLine("[AsyncClinicService] Fire-and-forget завершено.");
    }
}
