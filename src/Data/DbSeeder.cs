namespace ClinicApp.Data;

using ClinicApp.Models;
using ClinicApp.Enums;

/// <summary>
/// DbSeeder — початкове наповнення бази даних тестовими даними.
/// Викликається один раз при першому запуску (якщо таблиці порожні).
///
/// Принцип: перевіряємо context.Patients.Any() — якщо вже є записи, пропускаємо.
/// Це ідемпотентна операція: можна запускати багато разів без дублювання.
/// </summary>
public static class DbSeeder
{
    public static void Seed(ClinicDbContext context)
    {
        SeedPatients(context);
        SeedDoctors(context);
        SeedAppointments(context);
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
}
