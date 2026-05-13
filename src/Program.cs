using System.Text;
using ClinicApp;
using ClinicApp.Attributes;
using ClinicApp.Comparators;
using ClinicApp.Enums;
using ClinicApp.Interfaces;
using ClinicApp.Managers;
using ClinicApp.Models;
using ClinicApp.Utils;

// ──────────────────────────────────────────────
//  Ініціалізація клініки та тестові дані
// ──────────────────────────────────────────────
Clinic clinic = new Clinic("Медична Клініка");

if (clinic.Session.Exists())
{
    Console.Write("Знайдено збережену сесію. Завантажити? (y/n): ");
    if ((Console.ReadLine() ?? "").Trim().ToLower() == "y")
    {
        int loaded = clinic.Session.Load(clinic);
        Console.WriteLine($"Завантажено {loaded} пацієнтів із сесії.");
        clinic.Logger.LogInfo($"Сесію завантажено: {loaded} пацієнтів.");
    }
}


clinic.Patients.Add(new Patient("Іван",   "Петренко", new DateTime(1985, 3, 15), BloodType.APositive,  "0501234567"));
clinic.Patients.Add(new Patient("Олена",  "Коваль",   new DateTime(1992, 7, 22), BloodType.BNegative,  "0672345678"));
clinic.Patients.Add(new Patient("Максим", "Бойко",    new DateTime(2010, 1,  5), BloodType.OPositive,  "0933456789"));
clinic.Patients.Add(new Patient("Марія",  "Ткач"));

Doctor d1 = new Doctor("Олег",    "Сидоренко", Speciality.Cardiology, "LIC-001", "0441234567");
d1.Schedule = new WorkSchedule(8, 16);
clinic.Doctors.Add(d1);

Doctor d2 = new Doctor("Наталія", "Мороз",     Speciality.Neurology,  "LIC-002", "0442345678");
d2.Schedule = new WorkSchedule(9, 18);
clinic.Doctors.Add(d2);

Doctor d3 = new Doctor("Андрій",  "Власенко",  Speciality.Pediatrics, "LIC-003", "0443456789");
clinic.Doctors.Add(d3);

DateTime tomorrow = DateTime.Today.AddDays(1);
DateTime dayAfter  = DateTime.Today.AddDays(2);
clinic.Appointments.Book(1, 1, tomorrow.AddHours(10));
clinic.Appointments.BookUrgent(2, 2, tomorrow.AddHours(11), "гострий головний біль", 45);
clinic.Appointments.BookSpecialist(3, 3, dayAfter.AddHours(9), "педіатрія", 20);

// Демонстрація: new (приховування) vs override (поліморфізм)
// Доступ через базовий тип Appointment:
Appointment urgentRef = clinic.Appointments[1]; // реальний тип — UrgentAppointment
Console.WriteLine("GetDescription (override): " + urgentRef.GetDescription()); // "Терміновий (...)" — поліморфізм ✓
Console.WriteLine("GetPriority   (new):       " + urgentRef.GetPriority());    // 3, а не 1 — new не дає поліморфізму!

clinic.MedicalRecords.Add(new Diagnosis(1, 1, DateTime.Today.AddDays(-30),  "I10",  "Гіпертонічна хвороба", isChronic: true));
clinic.MedicalRecords.Add(new Diagnosis(1, 1, DateTime.Today.AddDays(-5),   "J06.9","Гострий ринофарингіт"));
clinic.MedicalRecords.Add(new LabResult(1, 1, DateTime.Today.AddDays(-7),   "Гемоглобін",    145, "г/л",  "120–160", true));
clinic.MedicalRecords.Add(new LabResult(1, 1, DateTime.Today.AddDays(-7),   "Холестерин",    6.2, "ммоль/л", "< 5.2",  false));
clinic.MedicalRecords.Add(new Prescription(1, 1, DateTime.Today.AddDays(-5), "Лізиноприл",   "10 мг", 30, "1 раз на добу вранці"));
clinic.MedicalRecords.Add(new Diagnosis(2, 2, DateTime.Today.AddDays(-60),  "G43",  "Мігрень без аури",  isChronic: true));
clinic.MedicalRecords.Add(new Prescription(2, 2, DateTime.Today.AddDays(-3), "Суматриптан",  "50 мг", 5,  "при нападі"));
clinic.MedicalRecords.Add(new LabResult(3, 3, DateTime.Today.AddDays(-14),   "Загальний аналіз крові", 4.8, "×10⁹/л", "4.0–9.0", true));

Console.WriteLine();

// ──────────────────────────────────────────────
//  Головне меню
// ──────────────────────────────────────────────
bool running = true;
while (running)
{
    Console.WriteLine();
    Console.WriteLine("╔══════════════════════════════════════════════╗");
    Console.WriteLine("║           МЕДИЧНА КЛІНІКА                    ║");
    Console.WriteLine("╠══════════════════════════════════════════════╣");
    Console.WriteLine("║  1. Пацієнти       — реєстрація, пошук      ║");
    Console.WriteLine("║  2. Лікарі         — персонал, розклад      ║");
    Console.WriteLine("║  3. Записи         — прийоми, скасування    ║");
    Console.WriteLine("║  4. Медична картка — діагнози, рецепти      ║");
    Console.WriteLine("║  5. Рахунки        — оплата, борги          ║");
    Console.WriteLine("║  6. Черга          — очікування, прийом     ║");
    Console.WriteLine("║  7. Звіт           — загальна статистика    ║");
    Console.WriteLine("║  8. Аналітика      — статистика, рейтинги   ║");
    Console.WriteLine("║  9. Плани лікування — рефлексія, атрибути   ║");
    Console.WriteLine("║ 10. Файли           — експорт, імпорт, лог  ║");
    Console.WriteLine("║  0. Вийти (зберегти сесію)                  ║");
    Console.WriteLine("╚══════════════════════════════════════════════╝");
    Console.Write("Оберіть розділ: ");

    string choice = Console.ReadLine() ?? "";
    Console.WriteLine();

    switch (choice)
    {
        case "1": PatientsMenu(clinic); break;
        case "2": DoctorsMenu(clinic);  break;
        case "3": AppointmentsMenu(clinic); break;
        case "4": MedicalRecordsMenu(clinic); break;
        case "5": BillingMenu(clinic); break;
        case "6": WaitingRoomMenu(clinic); break;
        case "7": clinic.GenerateReport(); break;
        case "8": AnalyticsMenu(clinic); break;
        case "9":  TreatmentPlansMenu(clinic); break;
        case "10": FilesMenu(clinic); break;
        case "0":
            Console.Write("Зберегти сесію перед виходом? (y/n): ");
            if ((Console.ReadLine() ?? "").Trim().ToLower() == "y")
            {
                clinic.Session.Save(clinic);
                clinic.Logger.LogInfo("Сесію збережено при виході.");
                Console.WriteLine("Сесію збережено.");
            }
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
                Console.WriteLine("Група крові: 0=Невідомо 1=A+ 2=A- 3=B+ 4=B- 5=AB+ 6=AB- 7=O+ 8=O-");
                Console.Write("Оберіть: ");
                int.TryParse(Console.ReadLine(), out int bloodNum);
                BloodType bloodType = (BloodType)bloodNum;
                Console.Write("Телефон: ");
                string phone = Console.ReadLine() ?? "";
                try
                {
                    clinic.Patients.Add(new Patient(firstName, lastName, dob, bloodType, phone));
                }
                catch (ArgumentOutOfRangeException e)
                {
                    Console.WriteLine("Помилка: " + e.Message);
                }
                catch (ArgumentException e)
                {
                    Console.WriteLine("Помилка: " + e.Message);
                }
                break;

            case "3":
                Console.Write("Пошуковий запит: ");
                string query = Console.ReadLine() ?? "";
                Patient[] found = clinic.Patients.FindByName(query);
                if (found.Length == 0) Console.WriteLine("Не знайдено.");
                else
                {
                    Console.WriteLine("Знайдено: " + found.Length);
                    for (int i = 0; i < found.Length; i++) Console.WriteLine(found[i]);
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
                Console.WriteLine("Спеціальність: 0=Загальна 1=Кардіологія 2=Неврологія 3=Педіатрія 4=Хірургія 5=Ортопедія 6=Дерматологія 7=Невідкладна");
                Console.Write("Оберіть: ");
                int.TryParse(Console.ReadLine(), out int specNum);
                Speciality speciality = (Speciality)specNum;
                Console.Write("Номер ліцензії: ");
                string license = Console.ReadLine() ?? "";
                Console.Write("Телефон: ");
                string phone = Console.ReadLine() ?? "";
                Console.Write("Початок роботи (година, напр. 8): ");
                if (!int.TryParse(Console.ReadLine(), out int workStart)) workStart = 8;
                Console.Write("Кінець роботи (година, напр. 17): ");
                if (!int.TryParse(Console.ReadLine(), out int workEnd)) workEnd = 17;
                try
                {
                    Doctor newDoctor = new Doctor(firstName, lastName, speciality, license, phone);
                    newDoctor.Schedule = new WorkSchedule(workStart, workEnd);
                    clinic.Doctors.Add(newDoctor);
                }
                catch (ArgumentOutOfRangeException e)
                {
                    Console.WriteLine("Помилка: " + e.Message);
                }
                catch (ArgumentException e)
                {
                    Console.WriteLine("Помилка: " + e.Message);
                }
                break;

            case "3":
                Console.Write("Спеціальність: ");
                string specQuery = Console.ReadLine() ?? "";
                Doctor[] doctors = clinic.Doctors.FindBySpeciality(specQuery);
                if (doctors.Length == 0) Console.WriteLine("Не знайдено.");
                else
                {
                    Console.WriteLine("Знайдено: " + doctors.Length);
                    for (int i = 0; i < doctors.Length; i++) Console.WriteLine(doctors[i]);
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
        Console.WriteLine("  8. За типом прийому");
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
                if (durStr.Length > 0) int.TryParse(durStr, out duration);
                try
                {
                    clinic.Appointments.Book(patientId, doctorId, scheduledAt, duration);
                }
                catch (ArgumentOutOfRangeException e)
                {
                    Console.WriteLine("Помилка: " + e.Message);
                }
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

            case "8":
                AppointmentsByTypeMenu(clinic);
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

static void AppointmentsByTypeMenu(Clinic clinic)
{
    Console.WriteLine("── За типом прийому ──────────");
    Console.WriteLine("  1. Термінові");
    Console.WriteLine("  2. Консультації спеціаліста");
    Console.WriteLine("  3. Звичайні");
    Console.Write("Оберіть: ");
    string choice = Console.ReadLine() ?? "";
    switch (choice)
    {
        case "1":
            Console.WriteLine("Термінові записи:");
            clinic.Appointments.DisplayList(clinic.Appointments.GetUrgent());
            break;
        case "2":
            Console.WriteLine("Консультації спеціаліста:");
            clinic.Appointments.DisplayList(clinic.Appointments.GetSpecialist());
            break;
        case "3":
            Console.WriteLine("Звичайні записи:");
            clinic.Appointments.DisplayList(clinic.Appointments.GetRegular());
            break;
        default:
            Console.WriteLine("Невідома команда.");
            break;
    }
}

// ──────────────────────────────────────────────
//  Меню медичної картки
// ──────────────────────────────────────────────
static void MedicalRecordsMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        Console.WriteLine("── Медична картка ────────────");
        Console.WriteLine("  1. Картка пацієнта (зведення)");
        Console.WriteLine("  2. Всі записи пацієнта");
        Console.WriteLine("  3. Додати діагноз");
        Console.WriteLine("  4. Додати аналіз");
        Console.WriteLine("  5. Додати рецепт");
        Console.WriteLine("  6. Записи лікаря");
        Console.WriteLine("  0. Назад");
        Console.Write("Оберіть: ");

        string cmd = Console.ReadLine() ?? "";

        switch (cmd)
        {
            case "1":
                Console.Write("ID пацієнта: ");
                if (!int.TryParse(Console.ReadLine(), out int summaryId)) break;
                clinic.MedicalRecords.DisplayPatientSummary(summaryId);
                break;

            case "2":
                Console.Write("ID пацієнта: ");
                if (!int.TryParse(Console.ReadLine(), out int pId)) break;
                Console.WriteLine("Всі записи пацієнта #" + pId + ":");
                clinic.MedicalRecords.DisplayList(clinic.MedicalRecords.GetByPatient(pId));
                break;

            case "3":
                clinic.Patients.DisplayAll();
                Console.Write("ID пацієнта: ");
                if (!int.TryParse(Console.ReadLine(), out int dpId)) break;
                clinic.Doctors.DisplayAll();
                Console.Write("ID лікаря: ");
                if (!int.TryParse(Console.ReadLine(), out int ddId)) break;
                Console.Write("Код діагнозу (напр. J06.9): ");
                string code = Console.ReadLine() ?? "";
                Console.Write("Опис: ");
                string desc = Console.ReadLine() ?? "";
                Console.Write("Хронічне? (1=так, 0=ні): ");
                bool isChronic = Console.ReadLine() == "1";
                try
                {
                    clinic.MedicalRecords.Add(new Diagnosis(dpId, ddId, DateTime.Today, code, desc, isChronic));
                }
                catch (ArgumentOutOfRangeException e) { Console.WriteLine("Помилка: " + e.Message); }
                catch (ArgumentException e) { Console.WriteLine("Помилка: " + e.Message); }
                break;

            case "4":
                clinic.Patients.DisplayAll();
                Console.Write("ID пацієнта: ");
                if (!int.TryParse(Console.ReadLine(), out int lpId)) break;
                clinic.Doctors.DisplayAll();
                Console.Write("ID лікаря: ");
                if (!int.TryParse(Console.ReadLine(), out int ldId)) break;
                Console.Write("Назва аналізу: ");
                string testName = Console.ReadLine() ?? "";
                Console.Write("Значення (число): ");
                double.TryParse(Console.ReadLine(), out double val);
                Console.Write("Одиниці виміру: ");
                string unit = Console.ReadLine() ?? "";
                Console.Write("Норма (напр. 4.0–9.0): ");
                string range = Console.ReadLine() ?? "";
                Console.Write("В нормі? (1=так, 0=ні): ");
                bool isNormal = Console.ReadLine() == "1";
                try
                {
                    clinic.MedicalRecords.Add(new LabResult(lpId, ldId, DateTime.Today, testName, val, unit, range, isNormal));
                }
                catch (ArgumentOutOfRangeException e) { Console.WriteLine("Помилка: " + e.Message); }
                catch (ArgumentException e) { Console.WriteLine("Помилка: " + e.Message); }
                break;

            case "5":
                clinic.Patients.DisplayAll();
                Console.Write("ID пацієнта: ");
                if (!int.TryParse(Console.ReadLine(), out int ppId)) break;
                clinic.Doctors.DisplayAll();
                Console.Write("ID лікаря: ");
                if (!int.TryParse(Console.ReadLine(), out int pdId)) break;
                Console.Write("Препарат: ");
                string med = Console.ReadLine() ?? "";
                Console.Write("Дозування (напр. 10 мг): ");
                string dosage = Console.ReadLine() ?? "";
                Console.Write("Кількість днів: ");
                int.TryParse(Console.ReadLine(), out int days);
                Console.Write("Інструкція (Enter = пропустити): ");
                string instr = Console.ReadLine() ?? "";
                try
                {
                    clinic.MedicalRecords.Add(new Prescription(ppId, pdId, DateTime.Today, med, dosage, days, instr));
                }
                catch (ArgumentOutOfRangeException e) { Console.WriteLine("Помилка: " + e.Message); }
                catch (ArgumentException e) { Console.WriteLine("Помилка: " + e.Message); }
                break;

            case "6":
                Console.Write("ID лікаря: ");
                if (!int.TryParse(Console.ReadLine(), out int dId)) break;
                Console.WriteLine("Записи лікаря #" + dId + ":");
                clinic.MedicalRecords.DisplayList(clinic.MedicalRecords.GetByDoctor(dId));
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
//  Меню рахунків
// ──────────────────────────────────────────────
static void BillingMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        Console.WriteLine("── Рахунки ───────────────────");
        Console.WriteLine("  1. Борги пацієнта");
        Console.WriteLine("  2. Всі неоплачені записи");
        Console.WriteLine("  3. Оплатити запис");
        Console.WriteLine("  4. Загальний борг клініки");
        Console.WriteLine("  0. Назад");
        Console.Write("Оберіть: ");

        string cmd = Console.ReadLine() ?? "";

        switch (cmd)
        {
            case "1":
                Console.Write("ID пацієнта: ");
                if (!int.TryParse(Console.ReadLine(), out int pId)) break;
                IPayable[] patientUnpaid = clinic.Billing.GetUnpaidByPatient(pId);
                Console.WriteLine("Неоплачені записи пацієнта #" + pId + ":");
                clinic.Billing.DisplayUnpaid(patientUnpaid);
                Console.WriteLine("Борг: " + clinic.Billing.GetPatientDebt(pId).ToString("F2") + " грн");
                break;

            case "2":
                Console.WriteLine("Всі неоплачені записи:");
                clinic.Billing.DisplayUnpaid(clinic.Billing.GetAllUnpaid());
                break;

            case "3":
                Console.Write("ID запису для оплати: ");
                if (!int.TryParse(Console.ReadLine(), out int aId)) break;
                if (clinic.Billing.PayAppointment(aId))
                    Console.WriteLine("Запис [" + aId + "] оплачено.");
                else
                    Console.WriteLine("Не вдалося оплатити: запис не знайдено, вже оплачено або скасовано.");
                break;

            case "4":
                Console.WriteLine("Загальний борг по клініці: " + clinic.Billing.GetTotalDebt().ToString("F2") + " грн");
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

static void WaitingRoomMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        Console.WriteLine("── Черга очікування ──────────");
        Console.WriteLine("  Зараз у черзі: " + clinic.WaitingRoom.Count);
        Console.WriteLine("  1. Додати пацієнта до черги");
        Console.WriteLine("  2. Прийняти першого (Dequeue)");
        Console.WriteLine("  3. Хто перший? (Peek)");
        Console.WriteLine("  4. Переглянути всю чергу");
        Console.WriteLine("  0. Назад");
        Console.Write("Оберіть: ");

        string cmd = Console.ReadLine() ?? "";

        switch (cmd)
        {
            case "1":
                clinic.Patients.DisplayAll();
                Console.Write("ID пацієнта: ");
                int pid;
                if (!int.TryParse(Console.ReadLine(), out pid)) break;
                Patient p = clinic.Patients.FindById(pid);
                if (p == null) { Console.WriteLine("Пацієнта не знайдено."); break; }
                clinic.WaitingRoom.Enqueue(p);
                Console.WriteLine(p.FullName + " додано до черги. У черзі: " + clinic.WaitingRoom.Count);
                break;

            case "2":
                try
                {
                    Patient next = clinic.WaitingRoom.Dequeue();
                    Console.WriteLine("Прийнято: " + next.FullName + ". Залишилось у черзі: " + clinic.WaitingRoom.Count);
                }
                catch (InvalidOperationException e) { Console.WriteLine("Помилка: " + e.Message); }
                break;

            case "3":
                try
                {
                    Patient first = clinic.WaitingRoom.Peek();
                    Console.WriteLine("Наступний: " + first.FullName);
                }
                catch (InvalidOperationException e) { Console.WriteLine("Помилка: " + e.Message); }
                break;

            case "4":
                Patient[] queue = clinic.WaitingRoom.ToArray();
                if (queue.Length == 0) { Console.WriteLine("Черга порожня."); break; }
                Console.WriteLine("Черга очікування (" + queue.Length + "):");
                for (int i = 0; i < queue.Length; i++)
                    Console.WriteLine("  " + (i + 1) + ". " + queue[i].FullName);
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
//  Меню аналітики
// ──────────────────────────────────────────────
static void AnalyticsMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        Console.WriteLine("── Аналітика ─────────────────");
        Console.WriteLine("  1. Лікарі — за навантаженням");
        Console.WriteLine("  2. Лікарі — за виручкою");
        Console.WriteLine("  3. Лікарі — за іменем");
        Console.WriteLine("  4. Пацієнти — за кількістю візитів");
        Console.WriteLine("  5. Пацієнти — за витратами");
        Console.WriteLine("  0. Назад");
        Console.Write("Оберіть: ");

        string cmd = Console.ReadLine() ?? "";
        Console.WriteLine();

        switch (cmd)
        {
            case "1":
                List<DoctorStats> byLoad = CollectDoctorStats(clinic);
                byLoad.Sort();
                Console.WriteLine("=== Лікарі за навантаженням ===");
                PrintDoctorStats(byLoad);
                break;

            case "2":
                List<DoctorStats> byRevenue = CollectDoctorStats(clinic);
                byRevenue.Sort(new DoctorStatsByRevenue());
                Console.WriteLine("=== Лікарі за виручкою ===");
                PrintDoctorStats(byRevenue);
                break;

            case "3":
                List<DoctorStats> byName = CollectDoctorStats(clinic);
                byName.Sort(new DoctorStatsByName());
                Console.WriteLine("=== Лікарі за іменем ===");
                PrintDoctorStats(byName);
                break;

            case "4":
                List<PatientStats> byVisits = CollectPatientStats(clinic);
                byVisits.Sort();
                Console.WriteLine("=== Пацієнти за кількістю візитів ===");
                PrintPatientStats(byVisits);
                break;

            case "5":
                List<PatientStats> bySpent = CollectPatientStats(clinic);
                bySpent.Sort(new PatientStatsBySpent());
                Console.WriteLine("=== Пацієнти за витратами ===");
                PrintPatientStats(bySpent);
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

static List<DoctorStats> CollectDoctorStats(Clinic clinic)
{
    List<DoctorStats> list = new List<DoctorStats>();
    foreach (DoctorStats s in clinic.Analytics.ComputeDoctorStats())
        list.Add(s);
    return list;
}

static List<PatientStats> CollectPatientStats(Clinic clinic)
{
    List<PatientStats> list = new List<PatientStats>();
    foreach (PatientStats s in clinic.Analytics.ComputePatientStats())
        list.Add(s);
    return list;
}

static void PrintDoctorStats(List<DoctorStats> stats)
{
    for (int i = 0; i < stats.Count; i++)
        Console.WriteLine("  " + (i + 1) + ". " + stats[i]);
}

static void PrintPatientStats(List<PatientStats> stats)
{
    for (int i = 0; i < stats.Count; i++)
        Console.WriteLine("  " + (i + 1) + ". " + stats[i]);
}

// ──────────────────────────────────────────────
//  Меню файлів (Lab 12)
// ──────────────────────────────────────────────
static void FilesMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        Console.WriteLine("── Файли ─────────────────────────────");
        Console.WriteLine("  1. Експортувати всі звіти");
        Console.WriteLine("  2. Експортувати пацієнтів");
        Console.WriteLine("  3. Експортувати записи на прийом");
        Console.WriteLine("  4. Імпортувати пацієнтів з CSV");
        Console.WriteLine("  5. Переглянути останні записи логу");
        Console.WriteLine("  6. Очистити лог");
        Console.WriteLine("  0. Назад");
        Console.Write("Оберіть: ");

        string cmd = Console.ReadLine() ?? "";

        switch (cmd)
        {
            case "1":
                Console.WriteLine("Експорт...");
                clinic.Exporter.ExportAll();
                clinic.Logger.LogInfo("Виконано повний експорт звітів.");
                break;

            case "2":
                string p2 = clinic.Exporter.ExportPatients();
                Console.WriteLine("Збережено: " + p2);
                clinic.Logger.LogInfo($"Експортовано пацієнтів: {p2}");
                break;

            case "3":
                string p3 = clinic.Exporter.ExportAppointments();
                Console.WriteLine("Збережено: " + p3);
                clinic.Logger.LogInfo($"Експортовано записи: {p3}");
                break;

            case "4":
                Console.Write("Шлях до CSV файлу (наприклад import/patients.csv): ");
                string csvPath = Console.ReadLine() ?? "";
                ImportResult result = clinic.Importer.ImportPatients(csvPath);
                result.Print();
                clinic.Logger.LogInfo($"Імпорт CSV '{csvPath}': {result.Imported} успішно, {result.Skipped} пропущено.");
                break;

            case "5":
                Console.Write("Скільки останніх рядків показати? ");
                if (!int.TryParse(Console.ReadLine(), out int n)) n = 10;
                string[] lines = clinic.Logger.GetLastLines(n);
                if (lines.Length == 0) { Console.WriteLine("Лог порожній."); break; }
                foreach (string line in lines)
                    Console.WriteLine("  " + line);
                break;

            case "6":
                Console.Write("Очистити лог? (y/n): ");
                if ((Console.ReadLine() ?? "").Trim().ToLower() == "y")
                {
                    clinic.Logger.Clear();
                    Console.WriteLine("Лог очищено.");
                }
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
//  Меню планів лікування (Lab 11 — Reflection)
// ──────────────────────────────────────────────
static void TreatmentPlansMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        Console.WriteLine("── Плани лікування ───────────────────");
        Console.WriteLine("  1. Показати всі плани");
        Console.WriteLine("  2. Додати план лікування");
        Console.WriteLine("  3. Плани пацієнта");
        Console.WriteLine("  4. Активувати план");
        Console.WriteLine("  5. Завершити план");
        Console.WriteLine("  6. Скасувати план");
        Console.WriteLine("  7. Інформація про тип TreatmentPlan");
        Console.WriteLine("  0. Назад");
        Console.Write("Оберіть: ");

        string cmd = Console.ReadLine() ?? "";

        switch (cmd)
        {
            case "1":
                TreatmentPlan[] all = clinic.TreatmentPlans.GetAll();
                if (all.Length == 0) { Console.WriteLine("Немає планів."); break; }
                for (int i = 0; i < all.Length; i++)
                    Console.WriteLine("  " + all[i]);
                break;

            case "2":
                TreatmentPlan plan = FormBuilder.Build<TreatmentPlan>();
                if (clinic.TreatmentPlans.Add(plan))
                    Console.WriteLine("План #" + plan.Id + " додано.");
                else
                    Console.WriteLine("Не вдалось додати план — перевірте помилки вище.");
                break;

            case "3":
                Console.Write("ID пацієнта: ");
                if (!int.TryParse(Console.ReadLine(), out int patId))
                {
                    Console.WriteLine("Невірний ID.");
                    break;
                }
                TreatmentPlan[] byPatient = clinic.TreatmentPlans.GetByPatient(patId);
                if (byPatient.Length == 0) { Console.WriteLine("Немає планів для цього пацієнта."); break; }
                for (int i = 0; i < byPatient.Length; i++)
                    Console.WriteLine("  " + byPatient[i]);
                break;

            case "4":
                Console.Write("ID плану для активації: ");
                if (!int.TryParse(Console.ReadLine(), out int actId))
                {
                    Console.WriteLine("Невірний ID.");
                    break;
                }
                TreatmentPlan? toActivate = clinic.TreatmentPlans.GetById(actId);
                if (toActivate == null) { Console.WriteLine("План не знайдено."); break; }
                Console.WriteLine(toActivate.Activate() ? "Активовано." : "Не можна активувати (статус: " + toActivate.Status + ").");
                break;

            case "5":
                Console.Write("ID плану для завершення: ");
                if (!int.TryParse(Console.ReadLine(), out int compId))
                {
                    Console.WriteLine("Невірний ID.");
                    break;
                }
                TreatmentPlan? toComplete = clinic.TreatmentPlans.GetById(compId);
                if (toComplete == null) { Console.WriteLine("План не знайдено."); break; }
                Console.WriteLine(toComplete.Complete() ? "Завершено." : "Не можна завершити (статус: " + toComplete.Status + ").");
                break;

            case "6":
                Console.Write("ID плану для скасування: ");
                if (!int.TryParse(Console.ReadLine(), out int canId))
                {
                    Console.WriteLine("Невірний ID.");
                    break;
                }
                TreatmentPlan? toCancel = clinic.TreatmentPlans.GetById(canId);
                if (toCancel == null) { Console.WriteLine("План не знайдено."); break; }
                Console.WriteLine(toCancel.Cancel() ? "Скасовано." : "Не можна скасувати (статус: " + toCancel.Status + ").");
                break;

            case "7":
                ModelValidator.PrintInfo(typeof(TreatmentPlan));
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
