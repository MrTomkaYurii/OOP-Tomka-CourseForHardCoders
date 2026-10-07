namespace ClinicApp.Comparators;

using ClinicApp.Models;

public class PatientStatsByLastVisit : IComparer<PatientStats>
{
    public int Compare(PatientStats? x, PatientStats? y)
    {
        if (x == null && y == null) return 0;
        if (x == null) return -1;
        if (y == null) return 1;
        return y.LastVisitDate.CompareTo(x.LastVisitDate); // найновіший візит = вище
    }
}
