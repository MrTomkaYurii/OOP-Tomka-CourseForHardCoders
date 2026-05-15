using ClinicApp;
using ClinicApp.Comparators;
using ClinicApp.Enums;
using ClinicApp.Events;
using ClinicApp.Extensions;
using ClinicApp.Managers;
using ClinicApp.Models;
using ClinicApp.UI;
using ClinicApp.Utils;
using Spectre.Console;

// ──────────────────────────────────────────────
//  Ініціалізація клініки та тестові дані
// ──────────────────────────────────────────────
Clinic clinic = new Clinic("Медична Клініка");

if (clinic.Session.Exists())
{
    if (ClinicRenderer.PromptConfirm("Знайдено збережену сесію. Завантажити?"))
    {
        int loaded = clinic.Session.Load(clinic);
        ClinicRenderer.PrintSuccess($"Завантажено {loaded} пацієнтів із сесії.");
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
Appointment urgentRef = clinic.Appointments[1];
AnsiConsole.MarkupLine("[dim]GetDescription (override): " + Markup.Escape(urgentRef.GetDescription()) + "[/]");
AnsiConsole.MarkupLine("[dim]GetPriority   (new):       " + urgentRef.GetPriority() + "[/]");

clinic.MedicalRecords.Add(new Diagnosis(1, 1, DateTime.Today.AddDays(-30),  "I10",  "Гіпертонічна хвороба", isChronic: true));
clinic.MedicalRecords.Add(new Diagnosis(1, 1, DateTime.Today.AddDays(-5),   "J06.9","Гострий ринофарингіт"));
clinic.MedicalRecords.Add(new LabResult(1, 1, DateTime.Today.AddDays(-7),   "Гемоглобін",    145, "г/л",  "120–160", true));
clinic.MedicalRecords.Add(new LabResult(1, 1, DateTime.Today.AddDays(-7),   "Холестерин",    6.2, "ммоль/л", "< 5.2",  false));
clinic.MedicalRecords.Add(new Prescription(1, 1, DateTime.Today.AddDays(-5), "Лізиноприл",   "10 мг", 30, "1 раз на добу вранці"));
clinic.MedicalRecords.Add(new Diagnosis(2, 2, DateTime.Today.AddDays(-60),  "G43",  "Мігрень без аури",  isChronic: true));
clinic.MedicalRecords.Add(new Prescription(2, 2, DateTime.Today.AddDays(-3), "Суматриптан",  "50 мг", 5,  "при нападі"));
clinic.MedicalRecords.Add(new LabResult(3, 3, DateTime.Today.AddDays(-14),   "Загальний аналіз крові", 4.8, "×10⁹/л", "4.0–9.0", true));

// Lab13: підписка обробника для демонстрації механіки події
clinic.Appointments.AppointmentBooked += OnAppointmentBookedConsole;

// ──────────────────────────────────────────────
//  Головне меню
// ──────────────────────────────────────────────
bool running = true;
while (running)
{
    string choice = ClinicRenderer.SelectMenu("МЕДИЧНА КЛІНІКА", new[]
    {
        "Пацієнти",
        "Лікарі",
        "Записи",
        "Медична картка",
        "Рахунки",
        "Черга",
        "Звіт",
        "Аналітика",
        "Плани лікування",
        "Файли",
        "Звіти (LINQ)",
        "Фільтри (Functional)",
        "Вийти"
    });

    switch (choice)
    {
        case "Пацієнти":           PatientsMenu(clinic);         break;
        case "Лікарі":             DoctorsMenu(clinic);          break;
        case "Записи":             AppointmentsMenu(clinic);     break;
        case "Медична картка":     MedicalRecordsMenu(clinic);   break;
        case "Рахунки":            BillingMenu(clinic);          break;
        case "Черга":              WaitingRoomMenu(clinic);      break;
        case "Звіт":               clinic.GenerateReport();      break;
        case "Аналітика":          AnalyticsMenu(clinic);        break;
        case "Плани лікування":    TreatmentPlansMenu(clinic);   break;
        case "Файли":              FilesMenu(clinic);            break;
        case "Звіти (LINQ)":       ReportsMenu(clinic);          break;
        case "Фільтри (Functional)": FunctionalMenu(clinic);    break;
        case "Вийти":
            clinic.Tracker.PrintSummary();
            clinic.Tracker.SaveSummary();
            if (ClinicRenderer.PromptConfirm("Зберегти сесію перед виходом?"))
            {
                clinic.Session.Save(clinic);
                clinic.Logger.LogInfo("Сесію збережено при виході.");
                ClinicRenderer.PrintSuccess("Сесію збережено.");
            }
            running = false;
            ClinicRenderer.PrintInfo("До побачення!");
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
        ClinicRenderer.PrintHeader("Пацієнти");
        string cmd = ClinicRenderer.SelectMenu("Оберіть дію", new[]
        {
            "Показати всіх",
            "Додати пацієнта",
            "Знайти за ім'ям",
            "Видалити пацієнта",
            "Статистика",
            "← Назад"
        });

        switch (cmd)
        {
            case "Показати всіх":
                ClinicRenderer.RenderPatients(clinic.Patients.GetAll());
                break;

            case "Додати пацієнта":
                try
                {
                    string firstName = ClinicRenderer.PromptString("Ім'я");
                    string lastName  = ClinicRenderer.PromptString("Прізвище");
                    DateTime dob     = ClinicRenderer.PromptDate("Дата народження");

                    string[] bloodTypes = Enum.GetNames(typeof(BloodType));
                    string btChoice = ClinicRenderer.SelectMenu("Група крові", bloodTypes);
                    BloodType bloodType = Enum.Parse<BloodType>(btChoice);

                    string phone = ClinicRenderer.PromptString("Телефон");
                    clinic.Patients.Add(new Patient(firstName, lastName, dob, bloodType, phone));
                    ClinicRenderer.PrintSuccess("Пацієнта додано.");
                }
                catch (Exception e)
                {
                    ClinicRenderer.PrintError(e.Message);
                }
                break;

            case "Знайти за ім'ям":
                string query = ClinicRenderer.PromptString("Пошуковий запит");
                Patient[] found = clinic.Patients.FindByName(query);
                if (found.Length == 0)
                    ClinicRenderer.PrintWarning("Не знайдено.");
                else
                    ClinicRenderer.RenderPatients(found);
                break;

            case "Видалити пацієнта":
                int removeId = ClinicRenderer.PromptInt("ID пацієнта");
                if (clinic.Patients.Remove(removeId))
                    ClinicRenderer.PrintSuccess("Видалено.");
                else
                    ClinicRenderer.PrintError("Пацієнта не знайдено.");
                break;

            case "Статистика":
                clinic.Patients.DisplayStats();
                break;

            case "← Назад":
                inMenu = false;
                break;
        }
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
        ClinicRenderer.PrintHeader("Лікарі");
        string cmd = ClinicRenderer.SelectMenu("Оберіть дію", new[]
        {
            "Показати всіх",
            "Додати лікаря",
            "Знайти за спеціальністю",
            "Статистика",
            "← Назад"
        });

        switch (cmd)
        {
            case "Показати всіх":
                ClinicRenderer.RenderDoctors(clinic.Doctors.GetAll());
                break;

            case "Додати лікаря":
                try
                {
                    string firstName = ClinicRenderer.PromptString("Ім'я");
                    string lastName  = ClinicRenderer.PromptString("Прізвище");

                    string[] specs = Enum.GetNames(typeof(Speciality));
                    string specChoice = ClinicRenderer.SelectMenu("Спеціальність", specs);
                    Speciality speciality = Enum.Parse<Speciality>(specChoice);

                    string license   = ClinicRenderer.PromptString("Номер ліцензії");
                    string phone     = ClinicRenderer.PromptString("Телефон");
                    int workStart    = ClinicRenderer.PromptInt("Початок роботи (година)");
                    int workEnd      = ClinicRenderer.PromptInt("Кінець роботи (година)");

                    Doctor newDoctor = new Doctor(firstName, lastName, speciality, license, phone);
                    newDoctor.Schedule = new WorkSchedule(workStart, workEnd);
                    clinic.Doctors.Add(newDoctor);
                    ClinicRenderer.PrintSuccess("Лікаря додано.");
                }
                catch (Exception e)
                {
                    ClinicRenderer.PrintError(e.Message);
                }
                break;

            case "Знайти за спеціальністю":
                string specQuery = ClinicRenderer.PromptString("Спеціальність");
                Doctor[] doctors = clinic.Doctors.FindBySpeciality(specQuery);
                if (doctors.Length == 0)
                    ClinicRenderer.PrintWarning("Не знайдено.");
                else
                    ClinicRenderer.RenderDoctors(doctors);
                break;

            case "Статистика":
                clinic.Doctors.DisplayStats();
                break;

            case "← Назад":
                inMenu = false;
                break;
        }
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
        ClinicRenderer.PrintHeader("Записи на прийом");
        string cmd = ClinicRenderer.SelectMenu("Оберіть дію", new[]
        {
            "Записати пацієнта",
            "Скасувати запис",
            "Позначити виконаним",
            "Записи пацієнта",
            "Записи лікаря",
            "Розклад на дату",
            "Майбутні записи",
            "За типом прийому",
            "← Назад"
        });

        switch (cmd)
        {
            case "Записати пацієнта":
                ClinicRenderer.RenderPatients(clinic.Patients.GetAll());
                int patientId = ClinicRenderer.PromptInt("ID пацієнта");
                ClinicRenderer.RenderDoctors(clinic.Doctors.GetAll());
                int doctorId = ClinicRenderer.PromptInt("ID лікаря");
                try
                {
                    DateTime scheduledAt = ClinicRenderer.PromptDateTime("Дата та час");
                    int duration = ClinicRenderer.PromptInt("Тривалість хвилин (Enter 30 для стандарту)");
                    clinic.Appointments.Book(patientId, doctorId, scheduledAt, duration);
                    ClinicRenderer.PrintSuccess("Запис створено.");
                }
                catch (Exception e) { ClinicRenderer.PrintError(e.Message); }
                break;

            case "Скасувати запис":
                int cancelId = ClinicRenderer.PromptInt("ID запису");
                string reason = ClinicRenderer.PromptString("Причина (Enter щоб пропустити)", allowEmpty: true);
                clinic.Appointments.Cancel(cancelId, reason);
                ClinicRenderer.PrintSuccess("Запис скасовано.");
                break;

            case "Позначити виконаним":
                int completeId = ClinicRenderer.PromptInt("ID запису");
                clinic.Appointments.Complete(completeId);
                ClinicRenderer.PrintSuccess("Запис позначено виконаним.");
                break;

            case "Записи пацієнта":
                int pId = ClinicRenderer.PromptInt("ID пацієнта");
                ClinicRenderer.RenderAppointments(clinic.Appointments.GetByPatient(pId));
                break;

            case "Записи лікаря":
                int dId = ClinicRenderer.PromptInt("ID лікаря");
                ClinicRenderer.RenderAppointments(clinic.Appointments.GetByDoctor(dId));
                break;

            case "Розклад на дату":
                DateTime schedDate = ClinicRenderer.PromptDate("Дата");
                clinic.DisplaySchedule(schedDate);
                break;

            case "Майбутні записи":
                ClinicRenderer.RenderAppointments(clinic.Appointments.GetUpcoming());
                break;

            case "За типом прийому":
                AppointmentsByTypeMenu(clinic);
                break;

            case "← Назад":
                inMenu = false;
                break;
        }
    }
}

static void AppointmentsByTypeMenu(Clinic clinic)
{
    ClinicRenderer.PrintHeader("Записи за типом");
    string choice = ClinicRenderer.SelectMenu("Тип прийому", new[]
    {
        "Термінові",
        "Консультації спеціаліста",
        "Звичайні",
        "← Назад"
    });

    switch (choice)
    {
        case "Термінові":
            ClinicRenderer.RenderAppointments(clinic.Appointments.GetUrgent());
            break;
        case "Консультації спеціаліста":
            ClinicRenderer.RenderAppointments(clinic.Appointments.GetSpecialist());
            break;
        case "Звичайні":
            ClinicRenderer.RenderAppointments(clinic.Appointments.GetRegular());
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
        ClinicRenderer.PrintHeader("Медична картка");
        string cmd = ClinicRenderer.SelectMenu("Оберіть дію", new[]
        {
            "Картка пацієнта (Tree)",
            "Всі записи пацієнта",
            "Додати діагноз",
            "Додати аналіз",
            "Додати рецепт",
            "Записи лікаря",
            "← Назад"
        });

        switch (cmd)
        {
            case "Картка пацієнта (Tree)":
                int summaryId = ClinicRenderer.PromptInt("ID пацієнта");
                Patient? pp = clinic.Patients.FindById(summaryId);
                if (pp == null) { ClinicRenderer.PrintError("Пацієнта не знайдено."); break; }
                ClinicRenderer.RenderMedicalRecord(pp, clinic.MedicalRecords.GetByPatient(summaryId));
                break;

            case "Всі записи пацієнта":
                int pId = ClinicRenderer.PromptInt("ID пацієнта");
                clinic.MedicalRecords.DisplayList(clinic.MedicalRecords.GetByPatient(pId));
                break;

            case "Додати діагноз":
                ClinicRenderer.RenderPatients(clinic.Patients.GetAll());
                int dpId = ClinicRenderer.PromptInt("ID пацієнта");
                ClinicRenderer.RenderDoctors(clinic.Doctors.GetAll());
                int ddId = ClinicRenderer.PromptInt("ID лікаря");
                string code = ClinicRenderer.PromptString("Код діагнозу (напр. J06.9)");
                string desc = ClinicRenderer.PromptString("Опис");
                bool isChronic = ClinicRenderer.PromptConfirm("Хронічне захворювання?");
                try
                {
                    clinic.MedicalRecords.Add(new Diagnosis(dpId, ddId, DateTime.Today, code, desc, isChronic));
                    ClinicRenderer.PrintSuccess("Діагноз додано.");
                }
                catch (Exception e) { ClinicRenderer.PrintError(e.Message); }
                break;

            case "Додати аналіз":
                ClinicRenderer.RenderPatients(clinic.Patients.GetAll());
                int lpId = ClinicRenderer.PromptInt("ID пацієнта");
                ClinicRenderer.RenderDoctors(clinic.Doctors.GetAll());
                int ldId = ClinicRenderer.PromptInt("ID лікаря");
                string testName = ClinicRenderer.PromptString("Назва аналізу");
                decimal rawVal  = ClinicRenderer.PromptDecimal("Значення");
                string unit     = ClinicRenderer.PromptString("Одиниці виміру");
                string range    = ClinicRenderer.PromptString("Норма (напр. 4.0–9.0)");
                bool isNormal   = ClinicRenderer.PromptConfirm("В нормі?");
                try
                {
                    clinic.MedicalRecords.Add(
                        new LabResult(lpId, ldId, DateTime.Today, testName, (double)rawVal, unit, range, isNormal));
                    ClinicRenderer.PrintSuccess("Аналіз додано.");
                }
                catch (Exception e) { ClinicRenderer.PrintError(e.Message); }
                break;

            case "Додати рецепт":
                ClinicRenderer.RenderPatients(clinic.Patients.GetAll());
                int ppId = ClinicRenderer.PromptInt("ID пацієнта");
                ClinicRenderer.RenderDoctors(clinic.Doctors.GetAll());
                int pdId   = ClinicRenderer.PromptInt("ID лікаря");
                string med = ClinicRenderer.PromptString("Препарат");
                string dosage = ClinicRenderer.PromptString("Дозування (напр. 10 мг)");
                int days   = ClinicRenderer.PromptInt("Кількість днів");
                string instr = ClinicRenderer.PromptString("Інструкція (Enter щоб пропустити)", allowEmpty: true);
                try
                {
                    clinic.MedicalRecords.Add(new Prescription(ppId, pdId, DateTime.Today, med, dosage, days, instr));
                    ClinicRenderer.PrintSuccess("Рецепт додано.");
                }
                catch (Exception e) { ClinicRenderer.PrintError(e.Message); }
                break;

            case "Записи лікаря":
                int dId = ClinicRenderer.PromptInt("ID лікаря");
                clinic.MedicalRecords.DisplayList(clinic.MedicalRecords.GetByDoctor(dId));
                break;

            case "← Назад":
                inMenu = false;
                break;
        }
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
        ClinicRenderer.PrintHeader("Рахунки та оплата");
        string cmd = ClinicRenderer.SelectMenu("Оберіть дію", new[]
        {
            "Борги пацієнта",
            "Всі неоплачені записи",
            "Оплатити запис",
            "Загальний борг клініки",
            "← Назад"
        });

        switch (cmd)
        {
            case "Борги пацієнта":
                int pId = ClinicRenderer.PromptInt("ID пацієнта");
                ClinicRenderer.RenderAppointments(
                    clinic.Billing.GetUnpaidByPatient(pId).Cast<Appointment>());
                AnsiConsole.MarkupLine(
                    $"[bold]Борг: [green]{clinic.Billing.GetPatientDebt(pId):F2} грн[/][/]");
                break;

            case "Всі неоплачені записи":
                ClinicRenderer.RenderAppointments(
                    clinic.Billing.GetAllUnpaid().Cast<Appointment>());
                break;

            case "Оплатити запис":
                int aId = ClinicRenderer.PromptInt("ID запису");
                if (clinic.Billing.PayAppointment(aId))
                    ClinicRenderer.PrintSuccess($"Запис [{aId}] оплачено.");
                else
                    ClinicRenderer.PrintError("Не вдалося: запис не знайдено, вже оплачено або скасовано.");
                break;

            case "Загальний борг клініки":
                AnsiConsole.MarkupLine(
                    $"[bold]Загальний борг: [red]{clinic.Billing.GetTotalDebt():F2} грн[/][/]");
                break;

            case "← Назад":
                inMenu = false;
                break;
        }
    }
}

// ──────────────────────────────────────────────
//  Меню черги
// ──────────────────────────────────────────────
static void WaitingRoomMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        ClinicRenderer.PrintHeader($"Черга очікування ({clinic.WaitingRoom.Count} у черзі)");
        string cmd = ClinicRenderer.SelectMenu("Оберіть дію", new[]
        {
            "Додати пацієнта до черги",
            "Прийняти першого (Dequeue)",
            "Хто перший? (Peek)",
            "Переглянути всю чергу",
            "← Назад"
        });

        switch (cmd)
        {
            case "Додати пацієнта до черги":
                ClinicRenderer.RenderPatients(clinic.Patients.GetAll());
                int pid = ClinicRenderer.PromptInt("ID пацієнта");
                Patient? p = clinic.Patients.FindById(pid);
                if (p == null) { ClinicRenderer.PrintError("Пацієнта не знайдено."); break; }
                clinic.WaitingRoom.Enqueue(p);
                ClinicRenderer.PrintSuccess($"{p.FullName} додано. У черзі: {clinic.WaitingRoom.Count}");
                break;

            case "Прийняти першого (Dequeue)":
                try
                {
                    Patient next = clinic.WaitingRoom.Dequeue();
                    ClinicRenderer.PrintSuccess($"Прийнято: {next.FullName}. Залишилось: {clinic.WaitingRoom.Count}");
                }
                catch (InvalidOperationException e) { ClinicRenderer.PrintError(e.Message); }
                break;

            case "Хто перший? (Peek)":
                try
                {
                    Patient first = clinic.WaitingRoom.Peek();
                    ClinicRenderer.RenderPatientCard(first);
                }
                catch (InvalidOperationException e) { ClinicRenderer.PrintError(e.Message); }
                break;

            case "Переглянути всю чергу":
                Patient[] queue = clinic.WaitingRoom.ToArray();
                if (queue.Length == 0) { ClinicRenderer.PrintWarning("Черга порожня."); break; }
                ClinicRenderer.RenderPatients(queue);
                break;

            case "← Назад":
                inMenu = false;
                break;
        }
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
        ClinicRenderer.PrintHeader("Аналітика");
        string cmd = ClinicRenderer.SelectMenu("Оберіть критерій", new[]
        {
            "Лікарі — за навантаженням",
            "Лікарі — за виручкою",
            "Лікарі — за іменем",
            "Пацієнти — за кількістю візитів",
            "Пацієнти — за витратами",
            "← Назад"
        });

        if (cmd == "← Назад") { inMenu = false; break; }

        List<DoctorStats>  doctorStats  = CollectDoctorStats(clinic);
        List<PatientStats> patientStats = CollectPatientStats(clinic);

        switch (cmd)
        {
            case "Лікарі — за навантаженням":
                doctorStats.Sort();
                PrintDoctorStats(doctorStats);
                break;
            case "Лікарі — за виручкою":
                doctorStats.Sort(new DoctorStatsByRevenue());
                PrintDoctorStats(doctorStats);
                break;
            case "Лікарі — за іменем":
                doctorStats.Sort(new DoctorStatsByName());
                PrintDoctorStats(doctorStats);
                break;
            case "Пацієнти — за кількістю візитів":
                patientStats.Sort();
                PrintPatientStats(patientStats);
                break;
            case "Пацієнти — за витратами":
                patientStats.Sort(new PatientStatsBySpent());
                PrintPatientStats(patientStats);
                break;
        }
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
        AnsiConsole.MarkupLine($"  {i + 1}. {Markup.Escape(stats[i].ToString())}");
}

static void PrintPatientStats(List<PatientStats> stats)
{
    for (int i = 0; i < stats.Count; i++)
        AnsiConsole.MarkupLine($"  {i + 1}. {Markup.Escape(stats[i].ToString())}");
}

// ──────────────────────────────────────────────
//  Меню звітів (Lab 14 — LINQ)
// ──────────────────────────────────────────────
static void ReportsMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        ClinicRenderer.PrintHeader("Звіти (LINQ)");
        string cmd = ClinicRenderer.SelectMenu("Оберіть звіт", new[]
        {
            "Статистика по спеціальностях",
            "Найзайнятіший лікар",
            "Пацієнти з кількома візитами",
            "Топ-3 лікарів за виручкою",
            "Чи є термінові записи?",
            "Активні спеціальності",
            "Виручка по місяцях",
            "← Назад"
        });

        switch (cmd)
        {
            case "Статистика по спеціальностях":
                ClinicRenderer.RenderSpecialityStats(clinic.Reports.GetSpecialityStats());
                break;

            case "Найзайнятіший лікар":
                string? busiest = clinic.Reports.FindBusiestDoctorName();
                AnsiConsole.MarkupLine("[bold]Найзайнятіший лікар:[/] " +
                    Markup.Escape(busiest ?? "немає даних"));
                break;

            case "Пацієнти з кількома візитами":
                int minVisits = ClinicRenderer.PromptInt("Мінімальна кількість візитів");
                var names = clinic.Reports.GetPatientsWithMultipleVisits(minVisits).ToList();
                if (names.Count == 0)
                    ClinicRenderer.PrintWarning("Таких пацієнтів немає.");
                else
                {
                    AnsiConsole.MarkupLine($"[bold]Пацієнти з {minVisits}+ візитами ({names.Count}):[/]");
                    foreach (string name in names)
                        AnsiConsole.MarkupLine("  — " + Markup.Escape(name));
                }
                break;

            case "Топ-3 лікарів за виручкою":
                ClinicRenderer.PrintHeader("Топ-3 лікарів за виручкою");
                int rank = 1;
                foreach (DoctorStats s in clinic.Reports.GetTopEarners(3))
                    AnsiConsole.MarkupLine($"  {rank++}. {Markup.Escape(s.ToString())}");
                break;

            case "Чи є термінові записи?":
                bool hasUrgent = clinic.Reports.HasAnyUrgentAppointments();
                if (hasUrgent)
                    ClinicRenderer.PrintWarning("У системі є термінові записи.");
                else
                    ClinicRenderer.PrintSuccess("Термінових записів немає.");
                break;

            case "Активні спеціальності":
                AnsiConsole.MarkupLine("[bold]Активні спеціальності:[/]");
                foreach (var spec in clinic.Reports.GetActiveSpecialities())
                    AnsiConsole.MarkupLine("  — " + Markup.Escape(spec.ToString()));
                break;

            case "Виручка по місяцях":
                ClinicRenderer.RenderMonthlyRevenue(clinic.Reports.GetMonthlyRevenue());
                break;

            case "← Назад":
                inMenu = false;
                break;
        }
    }
}

// ──────────────────────────────────────────────
//  Меню фільтрів та пайплайну (Lab 15 — Functional)
// ──────────────────────────────────────────────
static void FunctionalMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        ClinicRenderer.PrintHeader("Фільтри та пайплайн (Functional)");
        string cmd = ClinicRenderer.SelectMenu("Оберіть демонстрацію", new[]
        {
            "Розширення: неоплачені записи",
            "Розширення: майбутні дорожче порогу (замикання)",
            "Розширення: дорослі пацієнти",
            "Розширення: лікарі з активними записами",
            "Фільтр AND: термінові + майбутні",
            "Фільтр OR: термінові або дорожче 600 грн",
            "Процесор: вивести + логувати (Combine)",
            "Пайплайн: фільтр → вивести результат",
            "← Назад"
        });

        switch (cmd)
        {
            case "Розширення: неоплачені записи":
                Appointment[] unpaid = clinic.Appointments.GetAll().Unpaid().ToArray();
                ClinicRenderer.RenderAppointments(unpaid);
                AnsiConsole.MarkupLine(
                    $"[bold]Загальна сума: [green]{unpaid.TotalCost():F2} грн[/][/]");
                break;

            case "Розширення: майбутні дорожче порогу (замикання)":
                decimal threshold = ClinicRenderer.PromptDecimal("Мінімальна вартість (грн)");
                Appointment[] expensive = clinic.Appointments.GetAll()
                    .Upcoming()
                    .CostAbove(threshold)
                    .ToArray();
                ClinicRenderer.RenderAppointments(expensive);
                break;

            case "Розширення: дорослі пацієнти":
                ClinicRenderer.RenderPatients(clinic.Patients.GetAll().Adults());
                break;

            case "Розширення: лікарі з активними записами":
                Appointment[] allApps = clinic.Appointments.GetAll();
                ClinicRenderer.RenderDoctors(clinic.Doctors.GetAll().WithAppointments(allApps));
                break;

            case "Фільтр AND: термінові + майбутні":
                var filterAnd = new AppointmentFilter();
                filterAnd.Add(a => a is UrgentAppointment).And(a => a.IsUpcoming);
                ClinicRenderer.RenderAppointments(filterAnd.Apply(clinic.Appointments.GetAll()));
                break;

            case "Фільтр OR: термінові або дорожче 600 грн":
                var filterOr = new AppointmentFilter();
                filterOr.Add(a => a is UrgentAppointment).Or(a => a.GetCost() > 600m);
                ClinicRenderer.RenderAppointments(filterOr.Apply(clinic.Appointments.GetAll()));
                break;

            case "Процесор: вивести + логувати (Combine)":
                var processor = new AppointmentProcessor();
                processor.Combine(
                    a => ClinicRenderer.PrintInfo("[ВИВІД] " + a),
                    a => clinic.Logger.LogInfo("Processed: appointment #" + a.Id));
                Appointment[] upcoming = clinic.Appointments.GetAll().Upcoming().ToArray();
                AnsiConsole.MarkupLine($"[bold]Обробка майбутніх записів ({upcoming.Length}):[/]");
                processor.Execute(upcoming);
                break;

            case "Пайплайн: фільтр → вивести результат":
                clinic.Pipeline.Reset();
                clinic.Pipeline
                    .Filter(a => !a.IsPaid && !a.IsCancelled)
                    .Filter(a => a.ScheduledAt >= DateTime.Today)
                    .Then(a => ClinicRenderer.PrintInfo("  → " + a));
                AnsiConsole.MarkupLine("[bold]Пайплайн: неоплачені майбутні записи:[/]");
                int count = clinic.Pipeline.Execute(clinic.Appointments.GetAll());
                ClinicRenderer.PrintSuccess($"Оброблено: {count} записів.");
                break;

            case "← Назад":
                inMenu = false;
                break;
        }
    }
}

// ──────────────────────────────────────────────
//  Меню файлів (Lab 12)
// ──────────────────────────────────────────────
static void FilesMenu(Clinic clinic)
{
    bool inMenu = true;
    while (inMenu)
    {
        ClinicRenderer.PrintHeader("Файли — експорт / імпорт / лог");
        string cmd = ClinicRenderer.SelectMenu("Оберіть дію", new[]
        {
            "Експортувати всі звіти",
            "Експортувати пацієнтів",
            "Експортувати записи на прийом",
            "Імпортувати пацієнтів з CSV",
            "Переглянути останні записи логу",
            "Очистити лог",
            "← Назад"
        });

        switch (cmd)
        {
            case "Експортувати всі звіти":
                ClinicRenderer.WithSpinner("Експортую...", () =>
                {
                    clinic.Exporter.ExportAll();
                    clinic.Logger.LogInfo("Виконано повний експорт звітів.");
                });
                ClinicRenderer.PrintSuccess("Готово.");
                break;

            case "Експортувати пацієнтів":
                string p2 = clinic.Exporter.ExportPatients();
                ClinicRenderer.PrintSuccess($"Збережено: {p2}");
                break;

            case "Експортувати записи на прийом":
                string p3 = clinic.Exporter.ExportAppointments();
                ClinicRenderer.PrintSuccess($"Збережено: {p3}");
                break;

            case "Імпортувати пацієнтів з CSV":
                string csvPath = ClinicRenderer.PromptString("Шлях до CSV файлу");
                ImportResult result = clinic.Importer.ImportPatients(csvPath);
                result.Print();
                clinic.Logger.LogInfo(
                    $"Імпорт CSV '{csvPath}': {result.Imported} успішно, {result.Skipped} пропущено.");
                break;

            case "Переглянути останні записи логу":
                int n = ClinicRenderer.PromptInt("Кількість рядків");
                string[] lines = clinic.Logger.GetLastLines(n);
                if (lines.Length == 0) { ClinicRenderer.PrintWarning("Лог порожній."); break; }
                foreach (string line in lines)
                    AnsiConsole.MarkupLine("[dim]  " + Markup.Escape(line) + "[/]");
                break;

            case "Очистити лог":
                if (ClinicRenderer.PromptConfirm("Очистити лог?"))
                {
                    clinic.Logger.Clear();
                    ClinicRenderer.PrintSuccess("Лог очищено.");
                }
                break;

            case "← Назад":
                inMenu = false;
                break;
        }
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
        ClinicRenderer.PrintHeader("Плани лікування");
        string cmd = ClinicRenderer.SelectMenu("Оберіть дію", new[]
        {
            "Показати всі плани",
            "Додати план лікування",
            "Плани пацієнта",
            "Активувати план",
            "Завершити план",
            "Скасувати план",
            "Інформація про тип TreatmentPlan",
            "← Назад"
        });

        switch (cmd)
        {
            case "Показати всі плани":
                TreatmentPlan[] all = clinic.TreatmentPlans.GetAll();
                if (all.Length == 0) { ClinicRenderer.PrintWarning("Немає планів."); break; }
                for (int i = 0; i < all.Length; i++)
                    AnsiConsole.MarkupLine("  " + Markup.Escape(all[i].ToString()));
                break;

            case "Додати план лікування":
                TreatmentPlan plan = FormBuilder.Build<TreatmentPlan>();
                if (clinic.TreatmentPlans.Add(plan))
                    ClinicRenderer.PrintSuccess($"План #{plan.Id} додано.");
                else
                    ClinicRenderer.PrintError("Не вдалось додати план.");
                break;

            case "Плани пацієнта":
                int patId = ClinicRenderer.PromptInt("ID пацієнта");
                TreatmentPlan[] byPatient = clinic.TreatmentPlans.GetByPatient(patId);
                if (byPatient.Length == 0) { ClinicRenderer.PrintWarning("Немає планів."); break; }
                for (int i = 0; i < byPatient.Length; i++)
                    AnsiConsole.MarkupLine("  " + Markup.Escape(byPatient[i].ToString()));
                break;

            case "Активувати план":
                int actId = ClinicRenderer.PromptInt("ID плану");
                if (clinic.TreatmentPlans.Activate(actId))
                    ClinicRenderer.PrintSuccess("Активовано.");
                else
                    ClinicRenderer.PrintError("Не знайдено або неможливо активувати.");
                break;

            case "Завершити план":
                int compId = ClinicRenderer.PromptInt("ID плану");
                if (clinic.TreatmentPlans.Complete(compId))
                    ClinicRenderer.PrintSuccess("Завершено.");
                else
                    ClinicRenderer.PrintError("Не знайдено або неможливо завершити.");
                break;

            case "Скасувати план":
                int canId = ClinicRenderer.PromptInt("ID плану");
                if (clinic.TreatmentPlans.Cancel(canId))
                    ClinicRenderer.PrintSuccess("Скасовано.");
                else
                    ClinicRenderer.PrintError("Не знайдено або неможливо скасувати.");
                break;

            case "Інформація про тип TreatmentPlan":
                ModelValidator.PrintInfo(typeof(TreatmentPlan));
                break;

            case "← Назад":
                inMenu = false;
                break;
        }
    }
}

// Lab13: обробник для демонстрації механіки події
static void OnAppointmentBookedConsole(object? sender, AppointmentEventArgs e)
{
    ClinicRenderer.PrintInfo(
        $"[EVENT] Запис #{e.AppointmentId} створено — пацієнт {e.PatientId}, лікар {e.DoctorId}");
}
