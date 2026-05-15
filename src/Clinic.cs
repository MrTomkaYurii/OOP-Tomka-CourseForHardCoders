namespace ClinicApp;

using ClinicApp.Managers;
using ClinicApp.Models;
using ClinicApp.Utils;

public class Clinic
{
    public string Name { get; }
    public PatientManager Patients { get; }
    public DoctorManager Doctors { get; }
    public AppointmentManager Appointments { get; }
    public MedicalRecordManager MedicalRecords { get; }
    public BillingManager Billing { get; }
    public WaitingQueue<Patient> WaitingRoom { get; }
    public AnalyticsManager Analytics { get; }
    public ReportManager Reports { get; }
    public TreatmentPlanManager TreatmentPlans { get; }
    public ClinicLogger Logger { get; }
    public ClinicExporter Exporter { get; }
    public CsvImporter Importer { get; }
    public SessionManager Session { get; }
    public PatientPassportWriter Passport { get; }
    public SessionEventTracker Tracker { get; }

    public Clinic(string name)
    {
        Name = name;
        Patients = new PatientManager();
        Doctors = new DoctorManager();
        Appointments = new AppointmentManager(Patients, Doctors);
        MedicalRecords = new MedicalRecordManager();
        Billing = new BillingManager(Appointments);
        WaitingRoom = new WaitingQueue<Patient>();
        Analytics = new AnalyticsManager(Appointments, Doctors, Patients);
        Reports = new ReportManager(Appointments, Doctors, Patients);
        TreatmentPlans = new TreatmentPlanManager();
        Logger = new ClinicLogger();
        Exporter = new ClinicExporter(this);
        Importer = new CsvImporter(this);
        Session = new SessionManager();
        Passport = new PatientPassportWriter(this);
        Tracker  = new SessionEventTracker(this);

        SubscribeEvents();
    }

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

        // Tracker рахує статистику сесії + реагує на чергу
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
        Appointment[] upcoming = Appointments.GetUpcoming();
        Doctor[] allDoctors = Doctors.GetAll();

        Console.WriteLine("╔══════════════════════════════════════════════╗");
        Console.WriteLine("║  Звіт — " + Name);
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
