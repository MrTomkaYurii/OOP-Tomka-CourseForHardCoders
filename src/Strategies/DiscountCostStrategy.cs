namespace ClinicApp.Strategies;

using ClinicApp.Models;

/// <summary>Знижкова ставка: базова × (1 - відсоток знижки).</summary>
public class DiscountCostStrategy : ICostStrategy
{
    private readonly decimal _discountPercent;

    /// <param name="discountPercent">Відсоток знижки від 0 до 1. Напр. 0.2 = 20%.</param>
    public DiscountCostStrategy(decimal discountPercent = 0.2m)
    {
        if (discountPercent is < 0 or > 1)
            throw new ArgumentOutOfRangeException(nameof(discountPercent), "Знижка: 0.0–1.0");
        _discountPercent = discountPercent;
    }

    public string Description => $"Знижка {_discountPercent * 100:F0}%";

    public decimal Calculate(Appointment appointment)
        => (decimal)appointment.DurationMinutes * 10m * (1m - _discountPercent);
}
