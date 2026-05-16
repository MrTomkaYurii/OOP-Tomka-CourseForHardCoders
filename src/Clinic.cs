namespace ClinicApp;

using ClinicApp.Managers;
using ClinicApp.Models;
using ClinicApp.Utils;

/// <summary>
/// Clinic — головний клас-оркестратор in-memory частини застосунку.
///
/// Lab 22 / Task 1: Аналіз порушень SRP.
///
/// Поточний стан (порушення):
///   ❌ Відповідальність 1: конфігурація (Name) → винесено у ClinicConfig
///   ❌ Відповідальність 2: оркестрування 16 менеджерів (конструктор)
///   ❌ Відповідальність 3: event wire-up (SubscribeEvents)
///   ❌ Відповідальність 4: генерація звітів (GenerateReport)
///   ❌ Відповідальність 5: відображення розкладу (DisplaySchedule)
///
/// Що виправлено в Lab 22:
///   ✅ ClinicConfig виділено в окремий record
///   ✅ Config-властивість замінює пряме поле Name
///
/// Що залишається для розширеного завдання (не обов'язково):
///   — Виділити ClinicReporter { GenerateReport, DisplaySchedule }
///   — Виділити ClinicEventBus { SubscribeEvents }
/// </summary>
public class Clinic
{
    // Lab 22: конфігурація тепер в окремому record-і (SRP)
    public ClinicConfig Config { get; }

    // Зворотна сумісність: Name як властивість-делегат до Config.Name
    public string Name => Config.Name;

    public PatientManager    Patients       { get; }
    public DoctorManager     Doctors        { get; }
    public AppointmentManager Appointments  { get; }
    public MedicalRecordManager MedicalRecords { get; }
    public BillingManager    Billing        { get; }
    public WaitingQueue<Patient> WaitingRoom { get; }
    public AnalyticsManager  Analytics      { get; }
    public ReportManager     Reports        { get; }
    public AppointmentPipeline Pipeline     { get; }
    public TreatmentPlanManager TreatmentPlans { get; }
    public ClinicLogger      Logger         { get; }
    public ClinicExporter    Exporter       { get; }
    public CsvImporter       Importer       { get; }
    public SessionManager    Session        { get; }
    public PatientPassportWriter Passport   { get; }
    public SessionEventTracker Tracker      { get; }

    // Конструктор з ClinicConfig (новий, рекомендований — Lab 22)
    public Clinic(ClinicConfig config)
    {
        Config         = config;
        Patients       = new PatientManager();
        Doctors        = new DoctorManager();
        Appointments   = new AppointmentManager(Patients, Doctors);
        MedicalRecords = new MedicalRecordManager();
        Billing        = new BillingManager(Appointments);
        WaitingRoom    = new WaitingQueue<Patient>();
        Analytics      = new AnalyticsManager(Appointments, Doctors, Patients);
        Reports        = new ReportManager(Appointments, Doctors, Patients);
        Pipeline       = new AppointmentPipeline();
        TreatmentPlans = new TreatmentPlanManager();
        Logger         = new ClinicLogger();
        Exporter       = new ClinicExporter(this);
        Importer       = new CsvImporter(this);
        Session        = new SessionManager();
        Passport       = new PatientPassportWriter(this);
        Tracker        = new SessionEventTracker(this);
        SubscribeEvents();
    }

    // Конструктор зі string — зворотна сумісність з Labs 03-21
    // `: this(new ClinicConfig(name))` — делегування до основного конструктора
    public Clinic(string name) : this(new ClinicConfig(name)) { }

    private void SubscribeEvents()
    {
        // Logger слухає всі події
        Patients.PatientAdded                  += Logger.OnPatientAdded;
        Appointments.AppointmentBooked         += Logger.OnAppointmentBooked;
        Appointments.AppointmentCancelled      += Logger.OnAppointmentCancelled;
        Appointments.AppointmentCompleted      += Logger.OnAppointmentCompleted;
        Appointments.UrgentAppointmentBooked   += Logger.OnUrgentBooked;
        Billing.PaymentReceived                += Logger.OnPaymentReceived;
        TreatmentPlans.PlanCompleted           += Logger.OnPlanCompleted;

        // PassportWriter оновлює файл паспорту
        Patients.PatientAdded                  += Passport.OnPatientAdded;
        Appointments.AppointmentCompleted      += Passport.OnAppointmentCompleted;
        TreatmentPlans.PlanCompleted           += Passport.OnPlanCompleted;

        // Tracker рахує статистику сесії
        Patients.PatientAdded                  += Tracker.OnPatientAdded;
        Appointments.AppointmentBooked         += Tracker.OnAppointmentBooked;
        Appointments.UrgentAppointmentBooked   += Tracker.OnUrgentBooked;
        Appointments.AppointmentCancelled      += Tracker.OnAppointmentCancelled;
        Appointments.AppointmentCompleted      += Tracker.OnAppointmentCompleted;
        Billing.PaymentReceived                += Tracker.OnPaymentReceived;
        TreatmentPlans.PlanCompleted           += Tracker.OnPlanCompleted;
    }

    public void DisplaySchedule(DateTime date)
    {
        Console.WriteLine("\n=== Розклад на " + date.ToString("dd.MM.yyyy") + " ===");
        Appointment[] appointments = Appointments.GetByDate(date);
        Appointments.DisplayList(appointments);
    }

    public void GenerateReport()
    {
        Appointment[] upcoming  = Appointments.GetUpcoming();
        Doctor[]      allDoctors = Doctors.GetAll();

        Console.WriteLine("╔══════════════════════════════════════════════╗");
        Console.WriteLine("║  Звіт — " + Config.Name);
        Console.WriteLine("╠══════════════════════════════════════════════╣");
        Console.WriteLine("║  Пацієнтів:          " + Patients.Count);
        Console.WriteLine("║  Лікарів:            " + Doctors.Count);
        Console.WriteLine("║  Майбутніх записів:  " + upcoming.Length);
        Console.WriteLine("╠══════════════════════════════════════════════╣");
        Console.WriteLine("║  Навантаження лікарів (майбутні записи):");

        for (int i = 0; i < allDoctors.Length; i++)
        {
            int doctorAppCount = 0;
            for (int j = 0; j < upcoming.Length; j++)
                if (upcoming[j].DoctorId == allDoctors[i].Id) doctorAppCount++;
            Console.WriteLine("║    " + allDoctors[i].FullName + ": " + doctorAppCount + " записів");
        }

        Console.WriteLine("╚══════════════════════════════════════════════╝");
    }
}
