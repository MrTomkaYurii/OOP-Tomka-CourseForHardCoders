namespace ClinicApp.Strategies;

using ClinicApp.Models;

/// <summary>Терміновий прийом: базова ставка × коефіцієнт терміновості.</summary>
public class UrgentCostStrategy : ICostStrategy
{
    private readonly decimal _multiplier;

    public UrgentCostStrategy(decimal multiplier = 1.5m)
    {
        _multiplier = multiplier;
    }

    public string Description => $"Терміновий прийом (×{_multiplier})";

    public decimal Calculate(Appointment appointment)
        => (decimal)appointment.DurationMinutes * 10m * _multiplier;
}
