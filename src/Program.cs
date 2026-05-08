using ClinicApp;

// ──────────────────────────────────────────────
//  Ініціалізація клініки та тестові дані
// ──────────────────────────────────────────────
Clinic clinic = new Clinic("Медична Клініка");

// Пацієнти
clinic.Patients.Add(new Patient("Іван", "Петренко", new DateTime(1985, 3, 15), "A+", "0501234567"));
clinic.Patients.Add(new Patient("Олена", "Коваль", new DateTime(1992, 7, 22), "B-", "0672345678"));
clinic.Patients.Add(new Patient("Максим", "Бойко", new DateTime(2010, 1, 5), "O+", "0933456789"));
clinic.Patients.Add(new Patient("Марія", "Ткач"));

// Лікарі
Doctor d1 = new Doctor("Олег", "Сидоренко", "Кардіологія", "LIC-001", "0441234567");
d1.WorkStartHour = 8;
d1.WorkEndHour = 16;
clinic.Doctors.Add(d1);

Doctor d2 = new Doctor("Наталія", "Мороз", "Неврологія", "LIC-002", "0442345678");
d2.WorkStartHour = 9;
d2.WorkEndHour = 18;
clinic.Doctors.Add(d2);

Doctor d3 = new Doctor("Андрій", "Власенко", "Педіатрія", "LIC-003", "0443456789");
clinic.Doctors.Add(d3);

// Записи
DateTime tomorrow = DateTime.Today.AddDays(1);
DateTime dayAfter = DateTime.Today.AddDays(2);

clinic.Appointments.Book(1, 1, tomorrow.AddHours(10));
clinic.Appointments.Book(2, 2, tomorrow.AddHours(11), 45);
clinic.Appointments.Book(3, 3, dayAfter.AddHours(9), 20);

Console.WriteLine();

// ──────────────────────────────────────────────
//  Головне меню
// ──────────────────────────────────────────────
bool running = true;
while (running)
{
    Console.WriteLine();
    Console.WriteLine("╔══════════════════════════════╗");
    Console.WriteLine("║     МЕДИЧНА КЛІНІКА          ║");
    Console.WriteLine("╠══════════════════════════════╣");
    Console.WriteLine("║  1. Пацієнти                 ║");
    Console.WriteLine("║  2. Лікарі                   ║");
    Console.WriteLine("║  3. Записи на прийом         ║");
    Console.WriteLine("║  4. Звіт                     ║");
    Console.WriteLine("║  0. Вийти                    ║");
    Console.WriteLine("╚══════════════════════════════╝");
    Console.Write("Оберіть розділ: ");

    string choice = Console.ReadLine() ?? "";
    Console.WriteLine();

    switch (choice)
    {
        case "1": PatientsMenu(clinic); break;
        case "2": DoctorsMenu(clinic); break;
        case "3": AppointmentsMenu(clinic); break;
        case "4": clinic.GenerateReport(); break;
        case "0":
            running = false;
            Console.WriteLine("До побачення!");
            break;
        default:
            Console.WriteLine("Невідома команда. Спробуйте ще раз.");
            break;
    }
}

// ──────────────────────────────────────────────
//  Меню пацієнтів
// ──────────────────────────────────────────────
static void PatientsMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        Console.WriteLine("── Пацієнти ──────────────────");
        Console.WriteLine("  1. Показати всіх");
        Console.WriteLine("  2. Додати пацієнта");
        Console.WriteLine("  3. Знайти за ім'ям");
        Console.WriteLine("  4. Видалити пацієнта");
        Console.WriteLine("  5. Статистика");
        Console.WriteLine("  0. Назад");
        Console.Write("Оберіть: ");

        string cmd = Console.ReadLine() ?? "";

        switch (cmd)
        {
            case "1":
                clinic.Patients.DisplayAll();
                break;

            case "2":
                Console.Write("Ім'я: ");
                string firstName = Console.ReadLine() ?? "";
                Console.Write("Прізвище: ");
                string lastName = Console.ReadLine() ?? "";
                Console.Write("Дата народження (dd.MM.yyyy): ");
                string dobStr = Console.ReadLine() ?? "";
                DateTime dob;
                if (!DateTime.TryParseExact(dobStr, "dd.MM.yyyy",
                    System.Globalization.CultureInfo.InvariantCulture,
                    System.Globalization.DateTimeStyles.None, out dob))
                {
                    Console.WriteLine("Невірний формат дати.");
                    break;
                }
                Console.Write("Група крові (напр. A+): ");
                string bloodType = Console.ReadLine() ?? "Невідомо";
                Console.Write("Телефон: ");
                string phone = Console.ReadLine() ?? "0000000000";
                clinic.Patients.Add(new Patient(firstName, lastName, dob, bloodType, phone));
                break;

            case "3":
                Console.Write("Пошуковий запит: ");
                string query = Console.ReadLine() ?? "";
                Patient[] found = clinic.Patients.FindByName(query);
                if (found.Length == 0)
                    Console.WriteLine("Не знайдено.");
                else
                {
                    Console.WriteLine("Знайдено: " + found.Length);
                    for (int i = 0; i < found.Length; i++)
                        Console.WriteLine(found[i]);
                }
                break;

            case "4":
                Console.Write("ID пацієнта для видалення: ");
                int removeId;
                if (int.TryParse(Console.ReadLine(), out removeId))
                    Console.WriteLine(clinic.Patients.Remove(removeId) ? "Видалено." : "Не знайдено.");
                else
                    Console.WriteLine("Невірний ID.");
                break;

            case "5":
                clinic.Patients.DisplayStats();
                break;

            case "0":
                inMenu = false;
                break;

            default:
                Console.WriteLine("Невідома команда.");
                break;
        }
        Console.WriteLine();
    }
}

// ──────────────────────────────────────────────
//  Меню лікарів
// ──────────────────────────────────────────────
static void DoctorsMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        Console.WriteLine("── Лікарі ────────────────────");
        Console.WriteLine("  1. Показати всіх");
        Console.WriteLine("  2. Додати лікаря");
        Console.WriteLine("  3. Знайти за спеціальністю");
        Console.WriteLine("  4. Статистика");
        Console.WriteLine("  0. Назад");
        Console.Write("Оберіть: ");

        string cmd = Console.ReadLine() ?? "";

        switch (cmd)
        {
            case "1":
                clinic.Doctors.DisplayAll();
                break;

            case "2":
                Console.Write("Ім'я: ");
                string firstName = Console.ReadLine() ?? "";
                Console.Write("Прізвище: ");
                string lastName = Console.ReadLine() ?? "";
                Console.Write("Спеціальність: ");
                string speciality = Console.ReadLine() ?? "Загальна практика";
                Console.Write("Номер ліцензії: ");
                string license = Console.ReadLine() ?? "LIC-000";
                Console.Write("Телефон: ");
                string phone = Console.ReadLine() ?? "0000000000";
                Console.Write("Початок роботи (година, напр. 8): ");
                int workStart;
                if (!int.TryParse(Console.ReadLine(), out workStart))
                    workStart = 8;
                Console.Write("Кінець роботи (година, напр. 17): ");
                int workEnd;
                if (!int.TryParse(Console.ReadLine(), out workEnd))
                    workEnd = 17;
                Doctor newDoctor = new Doctor(firstName, lastName, speciality, license, phone);
                newDoctor.WorkStartHour = workStart;
                newDoctor.WorkEndHour = workEnd;
                clinic.Doctors.Add(newDoctor);
                break;

            case "3":
                Console.Write("Спеціальність: ");
                string specQuery = Console.ReadLine() ?? "";
                Doctor[] doctors = clinic.Doctors.FindBySpeciality(specQuery);
                if (doctors.Length == 0)
                    Console.WriteLine("Не знайдено.");
                else
                {
                    Console.WriteLine("Знайдено: " + doctors.Length);
                    for (int i = 0; i < doctors.Length; i++)
                        Console.WriteLine(doctors[i]);
                }
                break;

            case "4":
                clinic.Doctors.DisplayStats();
                break;

            case "0":
                inMenu = false;
                break;

            default:
                Console.WriteLine("Невідома команда.");
                break;
        }
        Console.WriteLine();
    }
}

// ──────────────────────────────────────────────
//  Меню записів
// ──────────────────────────────────────────────
static void AppointmentsMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        Console.WriteLine("── Записи ────────────────────");
        Console.WriteLine("  1. Записати пацієнта");
        Console.WriteLine("  2. Скасувати запис");
        Console.WriteLine("  3. Позначити виконаним");
        Console.WriteLine("  4. Записи пацієнта");
        Console.WriteLine("  5. Записи лікаря");
        Console.WriteLine("  6. Розклад на дату");
        Console.WriteLine("  7. Майбутні записи");
        Console.WriteLine("  0. Назад");
        Console.Write("Оберіть: ");

        string cmd = Console.ReadLine() ?? "";

        switch (cmd)
        {
            case "1":
                clinic.Patients.DisplayAll();
                Console.Write("ID пацієнта: ");
                int patientId;
                if (!int.TryParse(Console.ReadLine(), out patientId)) break;

                clinic.Doctors.DisplayAll();
                Console.Write("ID лікаря: ");
                int doctorId;
                if (!int.TryParse(Console.ReadLine(), out doctorId)) break;

                Console.Write("Дата та час (dd.MM.yyyy HH:mm): ");
                DateTime scheduledAt;
                if (!DateTime.TryParseExact(Console.ReadLine() ?? "", "dd.MM.yyyy HH:mm",
                    System.Globalization.CultureInfo.InvariantCulture,
                    System.Globalization.DateTimeStyles.None, out scheduledAt))
                {
                    Console.WriteLine("Невірний формат дати/часу.");
                    break;
                }
                Console.Write("Тривалість у хвилинах (Enter = 30): ");
                string durStr = Console.ReadLine() ?? "";
                int duration = 30;
                if (durStr.Length > 0)
                    int.TryParse(durStr, out duration);
                clinic.Appointments.Book(patientId, doctorId, scheduledAt, duration);
                break;

            case "2":
                Console.Write("ID запису: ");
                int cancelId;
                if (!int.TryParse(Console.ReadLine(), out cancelId)) break;
                Console.Write("Причина (Enter = без причини): ");
                string reason = Console.ReadLine() ?? "";
                clinic.Appointments.Cancel(cancelId, reason);
                break;

            case "3":
                Console.Write("ID запису: ");
                int completeId;
                if (!int.TryParse(Console.ReadLine(), out completeId)) break;
                clinic.Appointments.Complete(completeId);
                break;

            case "4":
                Console.Write("ID пацієнта: ");
                int pId;
                if (!int.TryParse(Console.ReadLine(), out pId)) break;
                Console.WriteLine("Записи пацієнта #" + pId + ":");
                clinic.Appointments.DisplayList(clinic.Appointments.GetByPatient(pId));
                break;

            case "5":
                Console.Write("ID лікаря: ");
                int dId;
                if (!int.TryParse(Console.ReadLine(), out dId)) break;
                Console.WriteLine("Записи лікаря #" + dId + ":");
                clinic.Appointments.DisplayList(clinic.Appointments.GetByDoctor(dId));
                break;

            case "6":
                Console.Write("Дата (dd.MM.yyyy): ");
                DateTime schedDate;
                if (!DateTime.TryParseExact(Console.ReadLine() ?? "", "dd.MM.yyyy",
                    System.Globalization.CultureInfo.InvariantCulture,
                    System.Globalization.DateTimeStyles.None, out schedDate))
                {
                    Console.WriteLine("Невірний формат дати.");
                    break;
                }
                clinic.DisplaySchedule(schedDate);
                break;

            case "7":
                Console.WriteLine("Майбутні записи:");
                clinic.Appointments.DisplayList(clinic.Appointments.GetUpcoming());
                break;

            case "0":
                inMenu = false;
                break;

            default:
                Console.WriteLine("Невідома команда.");
                break;
        }
        Console.WriteLine();
    }
}
