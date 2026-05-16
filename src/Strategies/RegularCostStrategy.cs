namespace ClinicApp.Strategies;

using ClinicApp.Models;

/// <summary>Базова ставка: тривалість × 10 грн/хв.</summary>
public class RegularCostStrategy : ICostStrategy
{
    public string Description => "Базова ставка (10 грн/хв)";

    public decimal Calculate(Appointment appointment)
        => (decimal)appointment.DurationMinutes * 10m;
}
