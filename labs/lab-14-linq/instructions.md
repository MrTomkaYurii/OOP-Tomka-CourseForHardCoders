# Лабораторна робота №14. LINQ

## Мета

Навчитися використовувати LINQ-оператори для роботи з колекціями: фільтрація (`.Where`), проєкція (`.Select`), групування (`.GroupBy`), агрегація (`.Sum`, `.Count`, `.Max`), з'єднання (`.Join`), та ланцюгове складання запитів.

## Контекст

До цієї лаби аналітика клініки рахувалася вручну — через вкладені `for`-цикли зі змінними-лічильниками. LINQ дозволяє виразити той самий алгоритм декларативно: _що_ потрібно отримати, а не _як_ ітерувати.

У цій роботі ви:
1. Перепишете існуючий `AnalyticsManager` з циклів на LINQ.
2. Створите новий `ReportManager` із сімома різними звітами.

## Гілка

```
feature/linq
```

---

## Завдання 1. Рефакторинг `AnalyticsManager`

Відкрийте `src/Managers/AnalyticsManager.cs`. Обидва методи (`ComputeDoctorStats`, `ComputePatientStats`) зараз використовують `for`-цикли для підрахунку кількості прийомів та виручки на кожного лікаря/пацієнта.

Перепишіть обидва методи з використанням LINQ:

- `.Select()` — для трансформації кожного лікаря/пацієнта у `DoctorStats`/`PatientStats`
- `.Where()` — для фільтрації прийомів, що належать цьому лікарю/пацієнту
- `.Count()`, `.Sum()`, `.Max()`, `.Any()` — для агрегованих значень

**Підказка для `ComputeDoctorStats`:**

```csharp
return _doctors.GetAll().Select(d =>
{
    var own = appointments.Where(a => a.DoctorId == d.Id);
    return new DoctorStats(
        d.Id,
        d.FullName,
        own.Count(),
        own.Sum(a => a.GetCost()),
        own.Any() ? own.Max(a => a.ScheduledAt) : DateTime.MinValue
    );
});
```

Зверніть увагу: `own.Any()` перевіряється перед `own.Max()`, бо `Max` на порожній послідовності кидає виняток.

---

## Завдання 2. DTO `SpecialityReport`

Створіть файл `src/Models/SpecialityReport.cs`:

```csharp
public class SpecialityReport
{
    public Speciality Speciality { get; }
    public int DoctorCount { get; }
    public int AppointmentCount { get; }
    public decimal TotalRevenue { get; }

    public SpecialityReport(Speciality speciality, int doctorCount,
                             int appointmentCount, decimal totalRevenue) { ... }

    public override string ToString() => ...;
}
```

Клас зберігає агреговані дані по одній спеціальності: скільки лікарів, скільки прийомів і яка загальна виручка.

---

## Завдання 3. Новий клас `ReportManager`

Створіть `src/Managers/ReportManager.cs`. Клас приймає у конструктор ті ж залежності, що й `AnalyticsManager`: `AppointmentManager`, `DoctorManager`, `PatientManager`.

### Метод `GetSpecialityStats` — `GroupBy`

Згрупуйте лікарів за спеціальністю (`.GroupBy(d => d.Speciality)`). Для кожної групи підрахуйте кількість лікарів, прийомів і загальну виручку. Поверніть `IEnumerable<SpecialityReport>`, відсортований за виручкою спадно.

```csharp
return doctors
    .GroupBy(d => d.Speciality)
    .Select(g =>
    {
        int[] ids = g.Select(d => d.Id).ToArray();
        var groupApps = appointments.Where(a => ids.Contains(a.DoctorId));
        return new SpecialityReport(g.Key, g.Count(),
                                    groupApps.Count(), groupApps.Sum(a => a.GetCost()));
    })
    .OrderByDescending(r => r.TotalRevenue);
```

### Метод `FindBusiestDoctorName` — `OrderByDescending` + `FirstOrDefault`

Знайдіть лікаря з найбільшою кількістю прийомів. Поверніть його ім'я (`string?`).

```csharp
return _doctors.GetAll()
    .OrderByDescending(d => appointments.Count(a => a.DoctorId == d.Id))
    .Select(d => d.FullName)
    .FirstOrDefault();
```

### Метод `GetPatientsWithMultipleVisits(int minVisits)` — `GroupBy` + `Join`

Згрупуйте прийоми за `PatientId`, залиште групи де кількість записів >= `minVisits`, а потім з'єднайте з таблицею пацієнтів щоб отримати їхні імена.

```csharp
return _appointments.GetAll()
    .GroupBy(a => a.PatientId)
    .Where(g => g.Count() >= minVisits)
    .Join(patients,
        g => g.Key,
        p => p.Id,
        (g, p) => p.FullName);
```

### Метод `GetTopEarners(int n)` — `OrderByDescending` + `Take`

Поверніть топ-N лікарів за виручкою у вигляді `IEnumerable<DoctorStats>`. Логіка формування `DoctorStats` — як у `AnalyticsManager`, але в кінці ланцюга додається `.OrderByDescending(s => s.TotalRevenue).Take(n)`.

### Метод `HasAnyUrgentAppointments` — `Any`

Перевірте, чи є в системі хоч один прийом типу `UrgentAppointment`:

```csharp
return _appointments.GetAll().Any(a => a is UrgentAppointment);
```

### Метод `GetActiveSpecialities` — `Distinct` + `OrderBy`

Отримайте список унікальних спеціальностей лікарів, які реально є у клініці:

```csharp
return _doctors.GetAll()
    .Select(d => d.Speciality)
    .Distinct()
    .OrderBy(s => s.ToString());
```

### Метод `GetMonthlyRevenue` — `GroupBy` анонімним типом

Згрупуйте прийоми за роком і місяцем, підрахуйте виручку в кожному місяці. Поверніть `IEnumerable<(int Year, int Month, decimal Total)>`.

```csharp
return _appointments.GetAll()
    .GroupBy(a => new { a.ScheduledAt.Year, a.ScheduledAt.Month })
    .Select(g => (g.Key.Year, g.Key.Month, g.Sum(a => a.GetCost())))
    .OrderBy(r => r.Year)
    .ThenBy(r => r.Month);
```

---

## Завдання 4. Підключення до `Clinic` і `Program`

**`src/Clinic.cs`** — додайте властивість і ініціалізацію в конструкторі:

```csharp
public ReportManager Reports { get; }
// ...
Reports = new ReportManager(Appointments, Doctors, Patients);
```

**`src/Program.cs`** — додайте пункт `11` у головне меню і реалізуйте `ReportsMenu(Clinic clinic)` з підменю:

| Пункт | Метод                              |
|-------|------------------------------------|
| 1     | `GetSpecialityStats()`             |
| 2     | `FindBusiestDoctorName()`          |
| 3     | `GetPatientsWithMultipleVisits(n)` |
| 4     | `GetTopEarners(3)`                 |
| 5     | `HasAnyUrgentAppointments()`       |
| 6     | `GetActiveSpecialities()`          |
| 7     | `GetMonthlyRevenue()`              |

---

## Перевірка

Запустіть програму:

```
dotnet run --project src
```

Перейдіть у розділ **11. Звіти** і перевірте:

- Пункт 1 показує список спеціальностей з кількістю лікарів і виручкою.
- Пункт 2 виводить ім'я лікаря з найбільшою кількістю записів.
- Пункт 3 при введенні `1` показує всіх пацієнтів, що мають хоч один запис.
- Пункт 5 виводить `"У системі є термінові записи."` (якщо є `UrgentAppointment`).
- Пункт 7 виводить рядки виду `2025/06 — 1350.00 грн`.

## Збереження

```
git add src/Models/SpecialityReport.cs
git add src/Managers/ReportManager.cs
git add src/Clinic.cs
git add src/Program.cs
git add src/Managers/AnalyticsManager.cs
git commit -m "lab-14: LINQ — AnalyticsManager rewrite + ReportManager"
git checkout main
git merge feature/linq
```
