namespace ClinicApp.Managers;

using ClinicApp.Models;
using ClinicApp.Strategies;

/// <summary>
/// Lab 22 / Task 2: OCP — Open/Closed Principle.
///
/// AppointmentProcessor розширено підтримкою ICostStrategy БЕЗ зміни існуючої логіки.
/// Новий метод WithCostStrategy() — додаткова точка розширення.
///
/// Принцип: клас відкритий для розширення (новий метод + поле),
///          закритий для змін (Run, RunIf, Combine, Execute — не змінювались).
/// </summary>
public class AppointmentProcessor
{
    private readonly List<Action<Appointment>> _actions = new();

    // Lab 22: опціональна стратегія вартості (null = не застосовувати)
    private ICostStrategy? _costStrategy;

    // Додати дію, що виконується для кожного прийому
    public AppointmentProcessor Run(Action<Appointment> action)
    {
        _actions.Add(action);
        return this;
    }

    // Додати умовну дію — виконується тільки якщо predicate повертає true
    public AppointmentProcessor RunIf(Func<Appointment, bool> predicate, Action<Appointment> action)
    {
        _actions.Add(a => { if (predicate(a)) action(a); });
        return this;
    }

    // Об'єднати дві дії в одну — виконуються послідовно для кожного прийому
    public AppointmentProcessor Combine(Action<Appointment> first, Action<Appointment> second)
    {
        _actions.Add(a => { first(a); second(a); });
        return this;
    }

    // Виконати всі зареєстровані дії для кожного прийому в колекції
    public void Execute(IEnumerable<Appointment> appointments)
    {
        foreach (Appointment a in appointments)
            foreach (Action<Appointment> action in _actions)
                action(a);
    }

    // Скинути всі зареєстровані дії
    public void Clear()
    {
        _actions.Clear();
        _costStrategy = null;
    }

    // ── Lab 22 / Task 2: OCP розширення ───────────────────────────────────
    // Встановити стратегію розрахунку вартості.
    // Fluent API: processor.WithCostStrategy(new UrgentCostStrategy()).Run(...).Execute(...)
    public AppointmentProcessor WithCostStrategy(ICostStrategy strategy)
    {
        _costStrategy = strategy;
        return this;
    }

    // Розрахувати вартість прийому через поточну стратегію.
    // Якщо стратегія не встановлена — використовує GetCost() з самого Appointment.
    public decimal CalculateCost(Appointment appointment)
        => _costStrategy?.Calculate(appointment) ?? appointment.GetCost();

    // Порівняти дві стратегії для одного прийому (демо для студентів)
    public static (decimal Regular, decimal WithStrategy) CompareCost(
        Appointment appointment, ICostStrategy strategy)
        => (appointment.GetCost(), strategy.Calculate(appointment));
}
