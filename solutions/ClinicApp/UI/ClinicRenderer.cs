using Spectre.Console;
using ClinicApp.Enums;
using ClinicApp.Models;

namespace ClinicApp.UI;

/// <summary>
/// Єдиний UI-шар: всі операції відображення та введення зосереджені тут.
/// Program.cs викликає методи цього класу — не знає про Spectre.Console напряму.
/// </summary>
public static class ClinicRenderer
{
    // ────────────────────────────────────────────────────────────────
    //  Базові утиліти — кольоровий текст і роздільники
    // ────────────────────────────────────────────────────────────────

    public static void PrintHeader(string title)
    {
        AnsiConsole.WriteLine();
        AnsiConsole.Write(new Rule($"[bold steelblue1]{Markup.Escape(title)}[/]")
        {
            Justification = Justify.Left
        });
    }

    public static void PrintSuccess(string message)
        => AnsiConsole.MarkupLine($"[green]✓[/] {Markup.Escape(message)}");

    public static void PrintError(string message)
        => AnsiConsole.MarkupLine($"[red]✗ {Markup.Escape(message)}[/]");

    public static void PrintWarning(string message)
        => AnsiConsole.MarkupLine($"[yellow]⚠[/] {Markup.Escape(message)}");

    public static void PrintInfo(string message)
        => AnsiConsole.MarkupLine($"[dim]{Markup.Escape(message)}[/]");

    // ────────────────────────────────────────────────────────────────
    //  Інтерактивне меню — стрілки замість цифр
    // ────────────────────────────────────────────────────────────────

    public static string SelectMenu(string title, string[] options)
    {
        return AnsiConsole.Prompt(
            new SelectionPrompt<string>()
                .Title($"[bold]{Markup.Escape(title)}[/]")
                .HighlightStyle(new Style(Color.SteelBlue1, decoration: Decoration.Bold))
                .AddChoices(options));
    }

    // ────────────────────────────────────────────────────────────────
    //  Введення даних — типізовані промпти з авто-валідацією
    // ────────────────────────────────────────────────────────────────

    public static int PromptInt(string label)
    {
        return AnsiConsole.Prompt(
            new TextPrompt<int>($"[steelblue1]{Markup.Escape(label)}:[/]")
                .ValidationErrorMessage("[red]Введіть ціле число[/]"));
    }

    public static string PromptString(string label, bool allowEmpty = false)
    {
        if (allowEmpty)
        {
            return AnsiConsole.Prompt(
                new TextPrompt<string>($"[steelblue1]{Markup.Escape(label)}:[/]")
                    .AllowEmpty());
        }
        return AnsiConsole.Prompt(
            new TextPrompt<string>($"[steelblue1]{Markup.Escape(label)}:[/]"));
    }

    public static decimal PromptDecimal(string label)
    {
        return AnsiConsole.Prompt(
            new TextPrompt<decimal>($"[steelblue1]{Markup.Escape(label)}:[/]")
                .ValidationErrorMessage("[red]Введіть число[/]"));
    }

    public static bool PromptConfirm(string question)
        => AnsiConsole.Prompt(new ConfirmationPrompt(question));

    public static DateTime PromptDate(string label)
    {
        string raw = AnsiConsole.Prompt(
            new TextPrompt<string>($"[steelblue1]{Markup.Escape(label)} (dd.MM.yyyy):[/]")
                .Validate(s =>
                {
                    bool ok = DateTime.TryParseExact(s, "dd.MM.yyyy",
                        System.Globalization.CultureInfo.InvariantCulture,
                        System.Globalization.DateTimeStyles.None, out _);
                    return ok ? ValidationResult.Success() : ValidationResult.Error("[red]Формат дати: дд.ММ.рррр[/]");
                }));
        DateTime.TryParseExact(raw, "dd.MM.yyyy",
            System.Globalization.CultureInfo.InvariantCulture,
            System.Globalization.DateTimeStyles.None, out DateTime result);
        return result;
    }

    public static DateTime PromptDateTime(string label)
    {
        string raw = AnsiConsole.Prompt(
            new TextPrompt<string>($"[steelblue1]{Markup.Escape(label)} (dd.MM.yyyy HH:mm):[/]")
                .Validate(s =>
                {
                    bool ok = DateTime.TryParseExact(s, "dd.MM.yyyy HH:mm",
                        System.Globalization.CultureInfo.InvariantCulture,
                        System.Globalization.DateTimeStyles.None, out _);
                    return ok ? ValidationResult.Success() : ValidationResult.Error("[red]Формат: дд.ММ.рррр ГГ:хх[/]");
                }));

        DateTime.TryParseExact(raw, "dd.MM.yyyy HH:mm",
            System.Globalization.CultureInfo.InvariantCulture,
            System.Globalization.DateTimeStyles.None, out DateTime result);
        return result;
    }

    // ────────────────────────────────────────────────────────────────
    //  Таблиця пацієнтів
    // ────────────────────────────────────────────────────────────────

    public static void RenderPatients(IEnumerable<Patient> patients)
    {
        var table = new Table()
            .Border(TableBorder.Rounded)
            .BorderColor(Color.SteelBlue1)
            .AddColumn(new TableColumn("[bold]ID[/]").Centered())
            .AddColumn("[bold]Ім'я[/]")
            .AddColumn(new TableColumn("[bold]Вік[/]").Centered())
            .AddColumn("[bold]Група крові[/]")
            .AddColumn("[bold]Телефон[/]");

        int count = 0;
        foreach (Patient p in patients)
        {
            string age = p.IsAdult
                ? p.Age.ToString()
                : $"[yellow]{p.Age}[/]";

            table.AddRow(
                p.Id.ToString(),
                Markup.Escape(p.FullName),
                age,
                Markup.Escape(p.BloodType.ToString()),
                Markup.Escape(p.Phone));
            count++;
        }

        if (count == 0) { PrintWarning("Список пацієнтів порожній."); return; }

        AnsiConsole.Write(table);
        PrintInfo($"Всього: {count}");
    }

    // ────────────────────────────────────────────────────────────────
    //  Таблиця лікарів
    // ────────────────────────────────────────────────────────────────

    public static void RenderDoctors(IEnumerable<Doctor> doctors)
    {
        var table = new Table()
            .Border(TableBorder.Rounded)
            .BorderColor(Color.SteelBlue1)
            .AddColumn(new TableColumn("[bold]ID[/]").Centered())
            .AddColumn("[bold]Ім'я[/]")
            .AddColumn("[bold]Спеціальність[/]")
            .AddColumn(new TableColumn("[bold]Доступний[/]").Centered())
            .AddColumn("[bold]Розклад[/]");

        int count = 0;
        foreach (Doctor d in doctors)
        {
            string available = d.IsAvailableNow ? "[green]Так[/]" : "[dim]Ні[/]";

            table.AddRow(
                d.Id.ToString(),
                Markup.Escape(d.FullName),
                Markup.Escape(d.Speciality.ToString()),
                available,
                Markup.Escape(d.Schedule.ToString()));
            count++;
        }

        if (count == 0) { PrintWarning("Список лікарів порожній."); return; }

        AnsiConsole.Write(table);
        PrintInfo($"Всього: {count}");
    }

    // ────────────────────────────────────────────────────────────────
    //  Таблиця записів із кольоровими статусами
    // ────────────────────────────────────────────────────────────────

    public static void RenderAppointments(IEnumerable<Appointment> appointments)
    {
        var table = new Table()
            .Border(TableBorder.Rounded)
            .BorderColor(Color.SteelBlue1)
            .AddColumn(new TableColumn("[bold]ID[/]").Centered())
            .AddColumn("[bold]Тип[/]")
            .AddColumn("[bold]Пацієнт[/]")
            .AddColumn("[bold]Лікар[/]")
            .AddColumn("[bold]Дата/час[/]")
            .AddColumn(new TableColumn("[bold]Вартість[/]").RightAligned())
            .AddColumn("[bold]Статус[/]");

        int count = 0;
        foreach (Appointment a in appointments)
        {
            string status;
            if (a.IsCancelled)        status = "[red]Скасовано[/]";
            else if (a.IsPaid)        status = "[green]Оплачено[/]";
            else if (!a.IsUpcoming)   status = "[dim]Прострочено[/]";
            else                      status = "[yellow]Заплановано[/]";

            string type = a switch
            {
                UrgentAppointment      => "[bold red]Терміновий[/]",
                SpecialistAppointment  => "[blue]Спеціаліст[/]",
                _                      => "Звичайний"
            };

            table.AddRow(
                a.Id.ToString(),
                type,
                $"#{a.PatientId}",
                $"#{a.DoctorId}",
                a.ScheduledAt.ToString("dd.MM.yyyy HH:mm"),
                a.GetCost().ToString("F2") + " грн",
                status);
            count++;
        }

        if (count == 0) { PrintWarning("Записів немає."); return; }

        AnsiConsole.Write(table);
        PrintInfo($"Всього: {count}");
    }

    // ────────────────────────────────────────────────────────────────
    //  Картка пацієнта (Panel)
    // ────────────────────────────────────────────────────────────────

    public static void RenderPatientCard(Patient patient)
    {
        string adultTag = patient.IsAdult ? "[green]Повнолітній[/]" : "[yellow]Неповнолітній[/]";
        string content =
            $"[bold]ID:[/] {patient.Id}\n" +
            $"[bold]Дата народження:[/] {patient.DateOfBirth:dd.MM.yyyy}\n" +
            $"[bold]Вік:[/] {patient.Age} рр. ({adultTag})\n" +
            $"[bold]Група крові:[/] {Markup.Escape(patient.BloodType.ToString())}\n" +
            $"[bold]Телефон:[/] {Markup.Escape(patient.Phone)}";

        var panel = new Panel(content)
        {
            Header    = new PanelHeader($"[bold steelblue1] Пацієнт: {Markup.Escape(patient.FullName)} [/]"),
            Border    = BoxBorder.Rounded,
            Padding   = new Padding(1, 0)
        };

        AnsiConsole.Write(panel);
    }

    // ────────────────────────────────────────────────────────────────
    //  Картка лікаря (Panel)
    // ────────────────────────────────────────────────────────────────

    public static void RenderDoctorCard(Doctor doctor)
    {
        string available = doctor.IsAvailableNow
            ? "[green]Доступний зараз[/]"
            : "[dim]Недоступний[/]";

        string content =
            $"[bold]ID:[/] {doctor.Id}\n" +
            $"[bold]Спеціальність:[/] {Markup.Escape(doctor.Speciality.ToString())}\n" +
            $"[bold]Ліцензія:[/] {Markup.Escape(doctor.LicenseNumber)}\n" +
            $"[bold]Телефон:[/] {Markup.Escape(doctor.Phone)}\n" +
            $"[bold]Розклад:[/] {Markup.Escape(doctor.Schedule.ToString())}\n" +
            $"[bold]Статус:[/] {available}";

        var panel = new Panel(content)
        {
            Header  = new PanelHeader($"[bold steelblue1] Лікар: {Markup.Escape(doctor.FullName)} [/]"),
            Border  = BoxBorder.Rounded,
            Padding = new Padding(1, 0)
        };

        AnsiConsole.Write(panel);
    }

    // ────────────────────────────────────────────────────────────────
    //  Медична картка (Tree — ієрархічне відображення)
    // ────────────────────────────────────────────────────────────────

    public static void RenderMedicalRecord(Patient patient, IEnumerable<MedicalRecord> records)
    {
        var root = new Tree(
            $"[bold steelblue1]Медична картка: {Markup.Escape(patient.FullName)}[/]");

        MedicalRecord[] all = records.ToArray();
        Diagnosis[]    diagnoses     = all.OfType<Diagnosis>().ToArray();
        LabResult[]    labResults    = all.OfType<LabResult>().ToArray();
        Prescription[] prescriptions = all.OfType<Prescription>().ToArray();

        // Гілка: Діагнози
        var diagBranch = root.AddNode($"[bold]Діагнози[/] ({diagnoses.Length})");
        if (diagnoses.Length == 0)
            diagBranch.AddNode("[dim]немає[/]");
        else
            foreach (Diagnosis d in diagnoses)
            {
                string chronic = d.IsChronic ? " [red]⟳ хронічне[/]" : "";
                diagBranch.AddNode(
                    $"[bold]{Markup.Escape(d.DiagnosisCode)}[/] — {Markup.Escape(d.Description)}{chronic}");
            }

        // Гілка: Аналізи
        var labBranch = root.AddNode($"[bold]Аналізи[/] ({labResults.Length})");
        if (labResults.Length == 0)
            labBranch.AddNode("[dim]немає[/]");
        else
            foreach (LabResult lr in labResults)
            {
                string normal = lr.IsNormal ? "[green]✓[/]" : "[red]⚠[/]";
                labBranch.AddNode(
                    $"{normal} {Markup.Escape(lr.TestName)}: " +
                    $"{lr.Value} {Markup.Escape(lr.Unit)} " +
                    $"[dim](норма: {Markup.Escape(lr.ReferenceRange)})[/]");
            }

        // Гілка: Рецепти
        var rxBranch = root.AddNode($"[bold]Рецепти[/] ({prescriptions.Length})");
        if (prescriptions.Length == 0)
            rxBranch.AddNode("[dim]немає[/]");
        else
            foreach (Prescription p in prescriptions)
            {
                string active = p.IsActive() ? "[green]активний[/]" : "[dim]завершено[/]";
                rxBranch.AddNode(
                    $"{Markup.Escape(p.MedicationName)} {Markup.Escape(p.Dosage)} " +
                    $"× {p.DurationDays} днів [{active}]");
            }

        AnsiConsole.Write(root);
    }

    // ────────────────────────────────────────────────────────────────
    //  Звіти: таблиця по спеціальностях
    // ────────────────────────────────────────────────────────────────

    public static void RenderSpecialityStats(IEnumerable<SpecialityReport> reports)
    {
        var table = new Table()
            .Border(TableBorder.Rounded)
            .BorderColor(Color.SteelBlue1)
            .AddColumn("[bold]Спеціальність[/]")
            .AddColumn(new TableColumn("[bold]Лікарів[/]").Centered())
            .AddColumn(new TableColumn("[bold]Прийомів[/]").Centered())
            .AddColumn(new TableColumn("[bold]Виручка[/]").RightAligned());

        int count = 0;
        foreach (SpecialityReport r in reports)
        {
            table.AddRow(
                Markup.Escape(r.Speciality.ToString()),
                r.DoctorCount.ToString(),
                r.AppointmentCount.ToString(),
                r.TotalRevenue.ToString("F2") + " грн");
            count++;
        }

        if (count == 0) { PrintWarning("Немає даних."); return; }
        AnsiConsole.Write(table);
    }

    // ────────────────────────────────────────────────────────────────
    //  Звіти: стовпчаста діаграма виручки по місяцях
    // ────────────────────────────────────────────────────────────────

    public static void RenderMonthlyRevenue(IEnumerable<(int Year, int Month, decimal Total)> data)
    {
        var chart = new BarChart()
            .Width(60)
            .Label("[bold steelblue1]Виручка по місяцях, грн[/]")
            .CenterLabel();

        bool hasData = false;
        foreach (var (year, month, total) in data)
        {
            chart.AddItem($"{year}/{month:D2}", (double)total, Color.SteelBlue1);
            hasData = true;
        }

        if (!hasData) { PrintWarning("Даних про виручку немає."); return; }
        AnsiConsole.Write(chart);
    }

    // ────────────────────────────────────────────────────────────────
    //  Спіннер — візуальний зворотній зв'язок для "довгих" операцій
    // ────────────────────────────────────────────────────────────────

    public static void WithSpinner(string message, Action action)
    {
        AnsiConsole.Status()
            .Spinner(Spinner.Known.Dots)
            .SpinnerStyle(Style.Parse("steelblue1"))
            .Start(Markup.Escape(message), _ => action());
    }
}
