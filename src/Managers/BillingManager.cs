namespace ClinicApp.Managers;

using ClinicApp.Interfaces;
using ClinicApp.Models;

public class BillingManager
{
    private readonly AppointmentManager _appointments;

    public BillingManager(AppointmentManager appointments)
    {
        _appointments = appointments;
    }

    public IPayable[] GetAllUnpaid()
    {
        Appointment[] all = _appointments.GetAll();
        int count = 0;
        for (int i = 0; i < all.Length; i++)
            if (!all[i].IsPaid && !all[i].IsCancelled) count++;
        IPayable[] result = new IPayable[count];
        int idx = 0;
        for (int i = 0; i < all.Length; i++)
            if (!all[i].IsPaid && !all[i].IsCancelled) result[idx++] = all[i];
        return result;
    }

    public IPayable[] GetUnpaidByPatient(int patientId)
    {
        Appointment[] all = _appointments.GetByPatient(patientId);
        int count = 0;
        for (int i = 0; i < all.Length; i++)
            if (!all[i].IsPaid && !all[i].IsCancelled) count++;
        IPayable[] result = new IPayable[count];
        int idx = 0;
        for (int i = 0; i < all.Length; i++)
            if (!all[i].IsPaid && !all[i].IsCancelled) result[idx++] = all[i];
        return result;
    }

    public decimal GetTotalDebt()
    {
        IPayable[] unpaid = GetAllUnpaid();
        decimal total = 0m;
        for (int i = 0; i < unpaid.Length; i++) total += unpaid[i].GetCost();
        return total;
    }

    public decimal GetPatientDebt(int patientId)
    {
        IPayable[] unpaid = GetUnpaidByPatient(patientId);
        decimal total = 0m;
        for (int i = 0; i < unpaid.Length; i++) total += unpaid[i].GetCost();
        return total;
    }

    public bool PayAppointment(int appointmentId)
    {
        Appointment[] all = _appointments.GetAll();
        for (int i = 0; i < all.Length; i++)
        {
            if (all[i].Id == appointmentId)
            {
                if (all[i].IsPaid || all[i].IsCancelled) return false;
                all[i].MarkPaid();
                return true;
            }
        }
        return false;
    }

    public void DisplayUnpaid(IPayable[] items)
    {
        if (items.Length == 0) { Console.WriteLine("Немає неоплачених записів."); return; }
        for (int i = 0; i < items.Length; i++)
        {
            if (items[i] is Appointment a)
                Console.WriteLine(a + " | Сума: " + items[i].GetCost().ToString("F2") + " грн");
            else
                Console.WriteLine("[" + (i + 1) + "] " + items[i].GetCost().ToString("F2") + " грн");
        }
    }
}
