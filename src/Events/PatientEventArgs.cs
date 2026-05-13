namespace ClinicApp.Events;

public class PatientEventArgs : EventArgs
{
    public int PatientId  { get; }
    public string FullName { get; }

    public PatientEventArgs(int id, string fullName)
    {
        PatientId = id;
        FullName  = fullName;
    }
}
