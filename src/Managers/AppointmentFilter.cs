namespace ClinicApp.Managers;

using ClinicApp.Models;

public class AppointmentFilter
{
    private Func<Appointment, bool>? _combined;

    // Додати умову через AND (усі умови мають виконуватись одночасно)
    public AppointmentFilter Add(Func<Appointment, bool> predicate)
    {
        if (_combined == null)
        {
            _combined = predicate;
        }
        else
        {
            var prev = _combined;
            _combined = a => prev(a) && predicate(a);
        }
        return this;
    }

    // Синонім Add — для читабельності ланцюга: .Add(...).And(...)
    public AppointmentFilter And(Func<Appointment, bool> predicate) => Add(predicate);

    // Об'єднати поточний фільтр з новим через OR
    public AppointmentFilter Or(Func<Appointment, bool> predicate)
    {
        if (_combined == null)
        {
            _combined = predicate;
        }
        else
        {
            var prev = _combined;
            _combined = a => prev(a) || predicate(a);
        }
        return this;
    }

    // Інвертувати весь фільтр — NOT
    public AppointmentFilter Negate()
    {
        if (_combined != null)
        {
            var prev = _combined;
            _combined = a => !prev(a);
        }
        return this;
    }

    // Застосувати фільтр до колекції
    public IEnumerable<Appointment> Apply(IEnumerable<Appointment> source)
    {
        if (_combined == null) return source;
        return source.Where(_combined);
    }

    // Скинути всі умови
    public void Reset() => _combined = null;
}
