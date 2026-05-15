namespace ClinicApp.Managers;

using ClinicApp.Models;

public class AppointmentProcessor
{
    private readonly List<Action<Appointment>> _actions = new();

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
    public void Clear() => _actions.Clear();
}
