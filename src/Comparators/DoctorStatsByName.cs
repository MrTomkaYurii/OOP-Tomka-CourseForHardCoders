namespace ClinicApp.Comparators;

using ClinicApp.Models;

public class DoctorStatsByName : IComparer<DoctorStats>
{
    public int Compare(DoctorStats? x, DoctorStats? y)
    {
        if (x == null && y == null) return 0;
        if (x == null) return -1;
        if (y == null) return 1;
        return string.Compare(x.FullName, y.FullName, StringComparison.CurrentCulture);
    }
}
