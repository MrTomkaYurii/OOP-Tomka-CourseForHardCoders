# Лабораторна робота №15. Functional C#

## Мета

Навчитися використовувати `Func<>`, `Action<>`, `Predicate<>` як повноцінні значення — передавати їх у методи, зберігати у полях, комбінувати. Зрозуміти що таке замикання (closure) та методи розширення (`extension methods`).

## Контекст

До цієї лаби всі умови фільтрації були захардкоджені у методах менеджерів або у LINQ-запитах. Тепер ми робимо поведінку **параметром**: замість того щоб писати "що фільтрувати" всередині методу — передаємо цей опис ззовні як `Func<Appointment, bool>`.

У цій лабі ви:
1. Напишете **методи розширення** на колекціях — як влаштовані `.Where()`, `.Select()` зсередини.
2. Створите **`AppointmentFilter`** — клас що збирає предикати та комбінує їх через AND/OR.
3. Створите **`AppointmentProcessor`** — клас що виконує `Action<Appointment>` для кожного прийому.
4. Зберете все разом у **`AppointmentPipeline`** — фільтр → дія в одному ланцюгу.

## Гілка

```
feature/functional
```

---

## Теорія: що таке Func<> і Action<>

`Func<T, TResult>` — це тип для методу що **приймає `T` і повертає `TResult`**.  
`Action<T>` — це тип для методу що **приймає `T` і нічого не повертає**.

```csharp
Func<Appointment, bool> isUrgent = a => a is UrgentAppointment;
Action<Appointment> print = a => Console.WriteLine(a);
```

Лямбда — це просто короткий спосіб написати анонімний метод. Вона може бути збережена у змінну, передана у метод як аргумент, або збережена у поле класу.

---

## Завдання 1. Методи розширення для `Appointment`

Створіть файл `src/Extensions/AppointmentExtensions.cs`.

```csharp
namespace ClinicApp.Extensions;

public static class AppointmentExtensions
{
    public static IEnumerable<Appointment> Unpaid(this IEnumerable<Appointment> source)
        => source.Where(a => !a.IsPaid && !a.IsCancelled);

    public static IEnumerable<Appointment> Upcoming(this IEnumerable<Appointment> source)
        => source.Where(a => a.IsUpcoming);

    public static IEnumerable<Appointment> ByDoctor(this IEnumerable<Appointment> source, int doctorId)
        => source.Where(a => a.DoctorId == doctorId);

    public static IEnumerable<Appointment> ByPatient(this IEnumerable<Appointment> source, int patientId)
        => source.Where(a => a.PatientId == patientId);

    public static IEnumerable<Appointment> Overdue(this IEnumerable<Appointment> source)
        => source.Where(a => a.ScheduledAt < DateTime.Now && !a.IsCancelled && !a.IsPaid);

    public static IEnumerable<Appointment> CostAbove(this IEnumerable<Appointment> source, decimal minCost)
        => source.Where(a => a.GetCost() > minCost);

    public static decimal TotalCost(this IEnumerable<Appointment> source)
        => source.Sum(a => a.GetCost());
}
```

**Ключове:** `this IEnumerable<Appointment> source` — перший параметр з `this` перетворює звичайний статичний метод на метод розширення. Після цього можна писати `appointments.Unpaid()` замість `AppointmentExtensions.Unpaid(appointments)`.

**Зверніть увагу на `CostAbove(decimal minCost)`:** параметр `minCost` — це **замикання** (closure). Лямбда `a => a.GetCost() > minCost` "захоплює" змінну `minCost` з зовнішнього контексту і пам'ятає її значення навіть після того як метод завершився.

---

## Завдання 2. Методи розширення для `Patient` та `Doctor`

Створіть `src/Extensions/PatientExtensions.cs`:

```csharp
public static class PatientExtensions
{
    public static IEnumerable<Patient> Adults(this IEnumerable<Patient> source)
        => source.Where(p => p.Age >= 18);

    public static IEnumerable<Patient> ByBloodType(this IEnumerable<Patient> source, BloodType bloodType)
        => source.Where(p => p.BloodType == bloodType);

    public static IEnumerable<Patient> WithAppointments(
        this IEnumerable<Patient> source, IEnumerable<Appointment> appointments)
        => source.Where(p => appointments.Any(a => a.PatientId == p.Id));
}
```

Створіть `src/Extensions/DoctorExtensions.cs`:

```csharp
public static class DoctorExtensions
{
    public static IEnumerable<Doctor> BySpeciality(this IEnumerable<Doctor> source, Speciality speciality)
        => source.Where(d => d.Speciality == speciality);

    public static IEnumerable<Doctor> Available(this IEnumerable<Doctor> source)
        => source.Where(d => d.IsAvailableNow);

    public static IEnumerable<Doctor> WithAppointments(
        this IEnumerable<Doctor> source, IEnumerable<Appointment> appointments)
        => source.Where(d => appointments.Any(a => a.DoctorId == d.Id));
}
```

Усі три класи мають бути `public static class` і знаходитись у просторі імен `ClinicApp.Extensions`.

---

## Завдання 3. Клас `AppointmentFilter`

Створіть `src/Managers/AppointmentFilter.cs`.

Клас зберігає **один комбінований предикат** типу `Func<Appointment, bool>?`. Кожен виклик `Add` або `And` комбінує новий предикат з існуючим через AND. `Or` — через OR. `Negate` — інвертує все.

```csharp
public class AppointmentFilter
{
    private Func<Appointment, bool>? _combined;

    public AppointmentFilter Add(Func<Appointment, bool> predicate)
    {
        if (_combined == null)
            _combined = predicate;
        else
        {
            var prev = _combined;           // захоплюємо поточний стан у замикання
            _combined = a => prev(a) && predicate(a);
        }
        return this;                        // повертаємо this для ланцюга
    }

    public AppointmentFilter And(Func<Appointment, bool> predicate) => Add(predicate);

    public AppointmentFilter Or(Func<Appointment, bool> predicate)
    {
        if (_combined == null)
            _combined = predicate;
        else
        {
            var prev = _combined;
            _combined = a => prev(a) || predicate(a);
        }
        return this;
    }

    public AppointmentFilter Negate()
    {
        if (_combined != null)
        {
            var prev = _combined;
            _combined = a => !prev(a);
        }
        return this;
    }

    public IEnumerable<Appointment> Apply(IEnumerable<Appointment> source)
    {
        if (_combined == null) return source;
        return source.Where(_combined);
    }

    public void Reset() => _combined = null;
}
```

**Зверніть увагу:** `var prev = _combined;` всередині методу — це **критично важливо**. Без цього рядка лямбда `a => prev(a) && predicate(a)` захопить посилання на поле `_combined`, яке продовжує змінюватись. Локальна копія `prev` фіксує **поточний стан** предиката в момент виклику.

---

## Завдання 4. Клас `AppointmentProcessor`

Створіть `src/Managers/AppointmentProcessor.cs`.

Клас зберігає список дій `List<Action<Appointment>>` і виконує їх усі для кожного прийому.

```csharp
public class AppointmentProcessor
{
    private readonly List<Action<Appointment>> _actions = new();

    public AppointmentProcessor Run(Action<Appointment> action)
    {
        _actions.Add(action);
        return this;
    }

    public AppointmentProcessor RunIf(Func<Appointment, bool> predicate, Action<Appointment> action)
    {
        _actions.Add(a => { if (predicate(a)) action(a); });
        return this;
    }

    public AppointmentProcessor Combine(Action<Appointment> first, Action<Appointment> second)
    {
        _actions.Add(a => { first(a); second(a); });
        return this;
    }

    public void Execute(IEnumerable<Appointment> appointments)
    {
        foreach (Appointment a in appointments)
            foreach (Action<Appointment> action in _actions)
                action(a);
    }

    public void Clear() => _actions.Clear();
}
```

**`Combine`** — об'єднує дві незалежні дії в одну лямбду. Це аналог `+=` для делегатів але ручний. Студент передає дві дії, і процесор завжди виконує обидві разом.

**`RunIf`** — умовна дія: лямбда перевіряє предикат і викликає `action` тільки якщо умова виконана. Сама умова і дія залишаються зовні — процесор їх не знає.

---

## Завдання 5. Клас `AppointmentPipeline`

Створіть `src/Managers/AppointmentPipeline.cs`.

Пайплайн — це фасад над `AppointmentFilter` + `AppointmentProcessor`. Він забезпечує зручний fluent-інтерфейс: спочатку всі умови фільтрації, потім усі дії.

```csharp
public class AppointmentPipeline
{
    private readonly AppointmentFilter _filter = new();
    private readonly AppointmentProcessor _processor = new();

    public AppointmentPipeline Filter(Func<Appointment, bool> predicate)
    {
        _filter.Add(predicate);
        return this;
    }

    public AppointmentPipeline Then(Action<Appointment> action)
    {
        _processor.Run(action);
        return this;
    }

    public int Execute(IEnumerable<Appointment> source)
    {
        Appointment[] filtered = _filter.Apply(source).ToArray();
        _processor.Execute(filtered);
        return filtered.Length;     // повертає кількість оброблених записів
    }

    public void Reset()
    {
        _filter.Reset();
        _processor.Clear();
    }
}
```

Приклад використання:
```csharp
pipeline
    .Filter(a => !a.IsPaid)
    .Filter(a => a.IsUpcoming)
    .Then(a => Console.WriteLine(a))
    .Then(a => logger.Log(a.ToString()));

int processed = pipeline.Execute(appointments);
```

---

## Завдання 6. Підключення до `Clinic` і `Program`

**`src/Clinic.cs`** — додайте властивість і ініціалізацію:

```csharp
public AppointmentPipeline Pipeline { get; }
// у конструкторі:
Pipeline = new AppointmentPipeline();
```

**`src/Program.cs`** — додайте `using ClinicApp.Extensions;` на початку файлу, пункт `12` у головне меню і реалізуйте `FunctionalMenu(Clinic clinic)` з підменю:

| Пункт | Що демонструє | Концепція |
|-------|--------------|-----------|
| 1 | `.Unpaid()` + `.TotalCost()` | метод розширення |
| 2 | `.Upcoming().CostAbove(threshold)` | замикання на `threshold` |
| 3 | `.Adults()` | метод розширення на Patient |
| 4 | `.WithAppointments(allApps)` | метод розширення на Doctor |
| 5 | `filter.Add(...).And(...)` | `Func<>` + AND-комбінація |
| 6 | `filter.Add(...).Or(...)` | OR-комбінація |
| 7 | `processor.Combine(print, log)` | `Action<>` + Combine |
| 8 | `pipeline.Filter(...).Then(...)` | пайплайн цілком |

---

## Перевірка

```
dotnet run --project src
```

Перейдіть у розділ **12. Фільтри та пайплайн** і перевірте:

- Пункт 1 виводить список неоплачених записів і суму.
- Пункт 2 запитує поріг — введіть `300`, отримаєте майбутні записи дорожче 300 грн.
- Пункт 5 виводить тільки термінові майбутні — перетин двох умов.
- Пункт 6 виводить більше записів — об'єднання двох умов.
- Пункт 8 виводить "Оброблено: N записів."

---

## Збереження

```
git add src/Extensions/
git add src/Managers/AppointmentFilter.cs
git add src/Managers/AppointmentProcessor.cs
git add src/Managers/AppointmentPipeline.cs
git add src/Clinic.cs
git add src/Program.cs
git commit -m "lab-15: Functional — extensions, AppointmentFilter, Processor, Pipeline"
git checkout main
git merge --no-ff feature/functional -m "Merge feature/functional: Lab15 Functional"
```
