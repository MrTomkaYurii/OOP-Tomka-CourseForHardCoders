namespace ClinicApp;

public struct WorkSchedule
{
    public int Start { get; }
    public int End { get; }

    public WorkSchedule(int start, int end)
    {
        Start = start;
        End = end;
    }

    public int HoursPerDay => End - Start;
    public string Display => Start.ToString("D2") + ":00–" + End.ToString("D2") + ":00";
    public bool Contains(int hour) => hour >= Start && hour < End;
    public bool IsNow => Contains(DateTime.Now.Hour);

    public override string ToString() => Display + " (" + HoursPerDay + " год)";
}
