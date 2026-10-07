namespace ClinicApp.Managers;

using ClinicApp.Models;

public class AppointmentPipeline
{
    private readonly AppointmentFilter _filter = new();
    private readonly AppointmentProcessor _processor = new();

    // Додати умову фільтрації — повертає this для ланцюга
    public AppointmentPipeline Filter(Func<Appointment, bool> predicate)
    {
        _filter.Add(predicate);
        return this;
    }

    // Додати дію після фільтрації — повертає this для ланцюга
    public AppointmentPipeline Then(Action<Appointment> action)
    {
        _processor.Run(action);
        return this;
    }

    // Запустити пайплайн: відфільтрувати → виконати дії → повернути кількість оброблених
    public int Execute(IEnumerable<Appointment> source)
    {
        Appointment[] filtered = _filter.Apply(source).ToArray();
        _processor.Execute(filtered);
        return filtered.Length;
    }

    // Скинути фільтр і дії — готовий до нового запуску
    public void Reset()
    {
        _filter.Reset();
        _processor.Clear();
    }
}
