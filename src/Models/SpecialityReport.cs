namespace ClinicApp.Models;

using ClinicApp.Enums;

public class SpecialityReport
{
    public Speciality Speciality { get; }
    public int DoctorCount { get; }
    public int AppointmentCount { get; }
    public decimal TotalRevenue { get; }

    public SpecialityReport(Speciality speciality, int doctorCount, int appointmentCount, decimal totalRevenue)
    {
        Speciality = speciality;
        DoctorCount = doctorCount;
        AppointmentCount = appointmentCount;
        TotalRevenue = totalRevenue;
    }

    public override string ToString()
    {
        return $"{Speciality,-15} | Лікарів: {DoctorCount,2} | Прийомів: {AppointmentCount,3} | Виручка: {TotalRevenue,8:F2} грн";
    }
}
