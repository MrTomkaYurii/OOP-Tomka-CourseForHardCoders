namespace ClinicApp.Events;

public class AppointmentEventArgs : EventArgs
{
    public int AppointmentId { get; }
    public int PatientId     { get; }
    public int DoctorId      { get; }
    public DateTime ScheduledAt { get; }
    public string Notes      { get; }

    public AppointmentEventArgs(int id, int patientId, int doctorId, DateTime at, string notes = "")
    {
        AppointmentId = id;
        PatientId     = patientId;
        DoctorId      = doctorId;
        ScheduledAt   = at;
        Notes         = notes;
    }
}
