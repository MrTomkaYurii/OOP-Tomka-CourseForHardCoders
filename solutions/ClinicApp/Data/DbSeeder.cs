namespace ClinicApp.Data;

using Microsoft.EntityFrameworkCore;
using ClinicApp.Models;
using ClinicApp.Enums;

/// <summary>
/// DbSeeder — початкове наповнення бази даних тестовими даними.
/// Викликається один раз при першому запуску (якщо таблиці порожні).
///
/// Принцип: перевіряємо context.Patients.Any() — якщо вже є записи, пропускаємо.
/// Це ідемпотентна операція: можна запускати багато разів без дублювання.
///
/// Lab 21: додано SeedAsync() — async варіант для демонстрації Task 1.
/// Відміна: SaveChanges() → SaveChangesAsync(ct); Any() → AnyAsync(ct).
/// </summary>
public static class DbSeeder
{
    // ── Синхронна версія (Labs 17-20) ─────────────────────────────────────
    public static void Seed(ClinicDbContext context)
    {
        SeedPatients(context);
        SeedDoctors(context);
        SeedAppointments(context);
        SeedMedicalRecords(context);
    }

    // ── Task 1: Async версія (Lab 21) ──────────────────────────────────────
    //
    // async Task — правильний тип для async void-методу що нічого не повертає.
    // CancellationToken ct = default → не обов'язковий параметр:
    //   DbSeeder.SeedAsync(context)          — без токена (CancellationToken.None)
    //   DbSeeder.SeedAsync(context, myToken) — з токеном
    //
    // Ключова відміна від Seed():
    //   Any()         → AnyAsync(ct)        — не блокує потік
    //   SaveChanges() → SaveChangesAsync(ct) — не блокує потік під час INSERT
    public static async Task SeedAsync(ClinicDbContext context, CancellationToken ct = default)
    {
        await SeedPatientsAsync(context, ct);
        await SeedDoctorsAsync(context, ct);
        await SeedAppointmentsAsync(context, ct);
        await SeedMedicalRecordsAsync(context, ct);
    }

    private static void SeedPatients(ClinicDbContext context)
    {
        // Перевіряємо: Any() → SELECT TOP 1 FROM Patients; не завантажує всі записи
        if (context.Patients.Any()) return;

        var patients = new[]
        {
            new Patient("Олена",   "Коваль",    new DateTime(1985, 3, 14), BloodType.APositive,  "0671234567") { Email = "o.koval@email.com" },
            new Patient("Микола",  "Шевченко",  new DateTime(1992, 7,  8), BloodType.OPositive,  "0682345678"),
            new Patient("Дарина",  "Бондаренко", new DateTime(2010, 11, 2), BloodType.BNegative, "0673456789") { Email = "darina.b@email.com" },
            new Patient("Андрій",  "Мельник",   new DateTime(1978, 5, 20), BloodType.ABPositive, "0634567890"),
            new Patient("Тетяна",  "Лисенко",   new DateTime(1960, 9,  1), BloodType.ANegative,  "0685678901") { Email = "t.lysenko@email.com" },
        };

        // AddRange відправляє всі об'єкти до трекера як "Added"
        context.Patients.AddRange(patients);

        // SaveChanges генерує INSERT для кожного об'єкта і оновлює Id з БД
        context.SaveChanges();

        Console.WriteLine($"[DbSeeder] Додано {patients.Length} пацієнтів.");
    }

    private static void SeedDoctors(ClinicDbContext context)
    {
        if (context.Doctors.Any()) return;

        var doctors = new[]
        {
            new Doctor("Іван",    "Петренко",  Speciality.General,  "LIC-001", "0671111111"),
            new Doctor("Марія",   "Савченко",  Speciality.Cardiology,"LIC-002","0672222222"),
            new Doctor("Сергій",  "Ткаченко",  Speciality.Neurology,"LIC-003", "0673333333"),
            new Doctor("Наталя",  "Кравченко", Speciality.Pediatrics,"LIC-004","0674444444"),
            new Doctor("Василь",  "Гриценко",  Speciality.Surgery,  "LIC-005", "0675555555"),
        };

        context.Doctors.AddRange(doctors);
        context.SaveChanges();

        Console.WriteLine($"[DbSeeder] Додано {doctors.Length} лікарів.");
    }

    private static void SeedAppointments(ClinicDbContext context)
    {
        if (context.Appointments.Any()) return;

        // Отримуємо реальні Id з БД (після SaveChanges в SeedPatients/SeedDoctors)
        var patients = context.Patients.ToList();
        var doctors  = context.Doctors.ToList();

        if (patients.Count < 2 || doctors.Count < 2)
        {
            Console.WriteLine("[DbSeeder] Недостатньо пацієнтів або лікарів для записів.");
            return;
        }

        // Дати для тестових записів
        var now  = DateTime.Now;
        var past = now.AddDays(-7);
        var future = now.AddDays(3);

        var appointments = new Appointment[]
        {
            // Звичайний запис (минулий)
            new RegularAppointment(patients[0].Id, doctors[0].Id, past.Date.AddHours(9), 30),
            // Терміновий (майбутній)
            new UrgentAppointment(patients[1].Id, doctors[1].Id, future.Date.AddHours(10), "Гострий біль", 45),
            // Консультація (минула, оплачена)
            new SpecialistAppointment(patients[2 % patients.Count].Id, doctors[2 % doctors.Count].Id,
                past.Date.AddHours(14), "Серцева аритмія", 60),
            // Ще один звичайний (майбутній)
            new RegularAppointment(patients[0].Id, doctors[2 % doctors.Count].Id, future.Date.AddHours(15), 30),
        };

        // Відзначаємо перший запис як завершений і оплачений
        appointments[0].Complete();
        appointments[0].MarkPaid();

        // Третій — завершений і оплачений
        appointments[2].Complete();
        appointments[2].MarkPaid();

        context.Appointments.AddRange(appointments);
        context.SaveChanges();

        Console.WriteLine($"[DbSeeder] Додано {appointments.Length} записів на прийом.");
    }

    private static void SeedMedicalRecords(ClinicDbContext context)
    {
        if (context.MedicalRecords.Any()) return;

        var patients = context.Patients.ToList();
        var doctors  = context.Doctors.ToList();

        if (patients.Count < 1 || doctors.Count < 1)
        {
            Console.WriteLine("[DbSeeder] Недостатньо даних для медичних записів.");
            return;
        }

        var p0 = patients[0];
        var p1 = patients[1 % patients.Count];
        var d0 = doctors[0];
        var d1 = doctors[1 % doctors.Count];
        var past = DateTime.Today.AddMonths(-3);

        var records = new MedicalRecord[]
        {
            new Diagnosis(p0.Id, d0.Id, past,
                "K29.7", "Хронічний гастрит", isChronic: true),
            new Diagnosis(p1.Id, d1.Id, past.AddDays(10),
                "J06.9", "ГРВІ", isChronic: false),
            new LabResult(p0.Id, d0.Id, past.AddDays(5),
                "Гемоглобін", 130.0, "г/л", "120-160", isNormal: true),
            new Prescription(p0.Id, d0.Id, past,
                "Омепразол", "20 мг × 2 рази/день", 14,
                "Приймати за 30 хв до їди"),
        };

        // EmergencyContact — Owned Entity: зберігається в таблиці Patients
        // Встановлюємо для першого пацієнта
        p0.EmergencyContact = new EmergencyContact("Іванна Коваль", "0671111000", "Дружина");
        context.Patients.Update(p0);

        context.MedicalRecords.AddRange(records);
        context.SaveChanges();

        Console.WriteLine($"[DbSeeder] Додано {records.Length} медичних записів і EmergencyContact.");
    }

    // ── Async private методи (Lab 21) ──────────────────────────────────────

    private static async Task SeedPatientsAsync(ClinicDbContext context, CancellationToken ct)
    {
        // AnyAsync → SELECT TOP 1 FROM Patients; не блокує потік
        if (await context.Patients.AnyAsync(ct)) return;

        var patients = new[]
        {
            new Patient("Олена",  "Коваль",     new DateTime(1985, 3, 14), BloodType.APositive,  "0671234567") { Email = "o.koval@email.com" },
            new Patient("Микола", "Шевченко",   new DateTime(1992, 7,  8), BloodType.OPositive,  "0682345678"),
            new Patient("Дарина", "Бондаренко", new DateTime(2010, 11, 2), BloodType.BNegative,  "0673456789") { Email = "darina.b@email.com" },
            new Patient("Андрій", "Мельник",    new DateTime(1978, 5, 20), BloodType.ABPositive, "0634567890"),
            new Patient("Тетяна", "Лисенко",    new DateTime(1960, 9,  1), BloodType.ANegative,  "0685678901") { Email = "t.lysenko@email.com" },
        };

        context.Patients.AddRange(patients);
        // SaveChangesAsync → INSERT SQL без блокування потоку
        await context.SaveChangesAsync(ct);
        Console.WriteLine($"[DbSeeder] Async: Додано {patients.Length} пацієнтів.");
    }

    private static async Task SeedDoctorsAsync(ClinicDbContext context, CancellationToken ct)
    {
        if (await context.Doctors.AnyAsync(ct)) return;

        var doctors = new[]
        {
            new Doctor("Іван",   "Петренко",  Speciality.General,   "LIC-001", "0671111111"),
            new Doctor("Марія",  "Савченко",  Speciality.Cardiology,"LIC-002", "0672222222"),
            new Doctor("Сергій", "Ткаченко",  Speciality.Neurology, "LIC-003", "0673333333"),
            new Doctor("Наталя", "Кравченко", Speciality.Pediatrics,"LIC-004", "0674444444"),
            new Doctor("Василь", "Гриценко",  Speciality.Surgery,   "LIC-005", "0675555555"),
        };

        context.Doctors.AddRange(doctors);
        await context.SaveChangesAsync(ct);
        Console.WriteLine($"[DbSeeder] Async: Додано {doctors.Length} лікарів.");
    }

    private static async Task SeedAppointmentsAsync(ClinicDbContext context, CancellationToken ct)
    {
        if (await context.Appointments.AnyAsync(ct)) return;

        // ToListAsync — завантажуємо вже збережені Id
        var patients = await context.Patients.ToListAsync(ct);
        var doctors  = await context.Doctors.ToListAsync(ct);

        if (patients.Count < 2 || doctors.Count < 2) return;

        var now    = DateTime.Now;
        var past   = now.AddDays(-7);
        var future = now.AddDays(3);

        var appointments = new Appointment[]
        {
            new RegularAppointment(patients[0].Id, doctors[0].Id, past.Date.AddHours(9), 30),
            new UrgentAppointment(patients[1].Id, doctors[1].Id, future.Date.AddHours(10), "Гострий біль", 45),
            new SpecialistAppointment(patients[2 % patients.Count].Id, doctors[2 % doctors.Count].Id,
                past.Date.AddHours(14), "Серцева аритмія", 60),
            new RegularAppointment(patients[0].Id, doctors[2 % doctors.Count].Id, future.Date.AddHours(15), 30),
        };

        appointments[0].Complete(); appointments[0].MarkPaid();
        appointments[2].Complete(); appointments[2].MarkPaid();

        context.Appointments.AddRange(appointments);
        await context.SaveChangesAsync(ct);
        Console.WriteLine($"[DbSeeder] Async: Додано {appointments.Length} записів.");
    }

    private static async Task SeedMedicalRecordsAsync(ClinicDbContext context, CancellationToken ct)
    {
        if (await context.MedicalRecords.AnyAsync(ct)) return;

        var patients = await context.Patients.ToListAsync(ct);
        var doctors  = await context.Doctors.ToListAsync(ct);

        if (patients.Count < 1 || doctors.Count < 1) return;

        var p0   = patients[0];
        var p1   = patients[1 % patients.Count];
        var d0   = doctors[0];
        var d1   = doctors[1 % doctors.Count];
        var past = DateTime.Today.AddMonths(-3);

        var records = new MedicalRecord[]
        {
            new Diagnosis(p0.Id, d0.Id, past,              "K29.7", "Хронічний гастрит", isChronic: true),
            new Diagnosis(p1.Id, d1.Id, past.AddDays(10),  "J06.9", "ГРВІ", isChronic: false),
            new LabResult(p0.Id, d0.Id, past.AddDays(5),   "Гемоглобін", 130.0, "г/л", "120-160", isNormal: true),
            new Prescription(p0.Id, d0.Id, past,           "Омепразол", "20 мг × 2 рази/день", 14, "Приймати за 30 хв до їди"),
        };

        p0.EmergencyContact = new EmergencyContact("Іванна Коваль", "0671111000", "Дружина");
        context.Patients.Update(p0);

        context.MedicalRecords.AddRange(records);
        await context.SaveChangesAsync(ct);
        Console.WriteLine($"[DbSeeder] Async: Додано {records.Length} медичних записів.");
    }
}
