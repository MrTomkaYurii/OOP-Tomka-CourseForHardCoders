namespace ClinicApp.Data;

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using ClinicApp.Models;
using ClinicApp.Enums;

/// <summary>
/// Головний "клас-посередник" між C#-об'єктами та базою даних.
/// DbContext:
///   — зберігає з'єднання з БД (OnConfiguring)
///   — описує, які таблиці існують (DbSet&lt;T&gt;)
///   — визначає правила відображення класів у таблиці (OnModelCreating)
///   — відстежує зміни об'єктів і генерує SQL при SaveChanges()
/// </summary>
public class ClinicDbContext : DbContext
{
    // DbSet<T> — це "таблиця" в C#-термінах.
    // LINQ-запити до DbSet<Patient> EF перетворює на SQL SELECT * FROM Patients.
    public DbSet<Patient> Patients => Set<Patient>();
    public DbSet<Doctor>  Doctors  => Set<Doctor>();

    // ─────────────────────────────────────────────────────────────
    // Task 1: Рядок підключення до SQL Server LocalDB
    // LocalDB — вбудований SQL Server для розробки, не потребує інсталяції сервера.
    // ─────────────────────────────────────────────────────────────
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlServer(
            "Server=(localdb)\\mssqllocaldb;" +
            "Database=ClinicApp;" +
            "Trusted_Connection=True;" +
            "TrustServerCertificate=True;");
    }

    // ─────────────────────────────────────────────────────────────
    // Fluent API — "текучий" API конфігурації.
    // Альтернатива Data Annotations ([Required], [MaxLength(100)]).
    // Fluent API має вищий пріоритет і тримає конфігурацію окремо від моделі.
    // ─────────────────────────────────────────────────────────────
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // ── Task 2: Таблиця Patients ──────────────────────────────
        modelBuilder.Entity<Patient>(entity =>
        {
            entity.ToTable("Patients");

            // HasKey — явно вказуємо первинний ключ (зазвичай EF знаходить Id автоматично)
            entity.HasKey(p => p.Id);

            // ValueGeneratedOnAdd — БД генерує Id (IDENTITY), EF Core оновить поле після INSERT
            entity.Property(p => p.Id)
                  .ValueGeneratedOnAdd();

            // Property — Fluent API для окремих стовпців
            entity.Property(p => p.FirstName)
                  .HasMaxLength(100)
                  .IsRequired();

            entity.Property(p => p.LastName)
                  .HasMaxLength(100)
                  .IsRequired();

            entity.Property(p => p.Phone)
                  .HasMaxLength(20)
                  .IsRequired();

            entity.Property(p => p.Email)
                  .HasMaxLength(200);

            // HasConversion<string> — enum зберігається як текст, не як число.
            // Причина: читабельні дані в БД; додавання нових значень enum не ламає старі дані.
            entity.Property(p => p.BloodType)
                  .HasConversion<string>()
                  .HasMaxLength(10);

            // Індекс для прискорення пошуку за прізвищем
            entity.HasIndex(p => p.LastName).HasDatabaseName("IX_Patients_LastName");
        });

        // ── Task 3: Таблиця Doctors ───────────────────────────────
        modelBuilder.Entity<Doctor>(entity =>
        {
            entity.ToTable("Doctors");

            entity.HasKey(d => d.Id);

            entity.Property(d => d.Id)
                  .ValueGeneratedOnAdd();

            entity.Property(d => d.FirstName)
                  .HasMaxLength(100)
                  .IsRequired();

            entity.Property(d => d.LastName)
                  .HasMaxLength(100)
                  .IsRequired();

            entity.Property(d => d.LicenseNumber)
                  .HasMaxLength(50)
                  .IsRequired();

            entity.HasIndex(d => d.LicenseNumber)
                  .IsUnique()
                  .HasDatabaseName("UX_Doctors_License");

            entity.Property(d => d.Phone)
                  .HasMaxLength(20)
                  .IsRequired();

            entity.Property(d => d.Speciality)
                  .HasConversion<string>()
                  .HasMaxLength(30);

            // Value Conversion для struct WorkSchedule.
            // WorkSchedule — це value object (значення "8-17" описує розклад).
            // Зберігаємо як рядок "Start-End" (наприклад "8-17"), читаємо назад через конструктор.
            // Перевага: не потрібна окрема таблиця, немає JOIN, просте зберігання.
            //
            // Використовуємо ValueConverter<TModel, TProvider> — клас, а не лямбда напряму,
            // тому що expression trees (які EF будує з лямбд) не підтримують методи
            // з опціональними параметрами (обмеження CS0854).
            var workScheduleConverter = new ValueConverter<WorkSchedule, string>(
                // C# → SQL: WorkSchedule { Start=8, End=17 } → "8-17"
                schedule => schedule.Start.ToString() + "-" + schedule.End.ToString(),
                // SQL → C#: "8-17" → new WorkSchedule(8, 17)
                value    => ParseWorkSchedule(value));

            entity.Property(d => d.Schedule)
                  .HasConversion(workScheduleConverter)
                  .HasColumnName("WorkSchedule")
                  .HasMaxLength(10)
                  .IsRequired();
        });
    }

    // ─────────────────────────────────────────────────────────────
    // Допоміжний метод для ValueConverter: парсинг рядка "8-17"
    // Виноситься в окремий метод, бо expression tree (CS0854) не може
    // містити виклики з опціональними параметрами всередині лямбди.
    // ─────────────────────────────────────────────────────────────
    private static WorkSchedule ParseWorkSchedule(string value)
    {
        string[] parts = value.Split('-');
        int start = int.Parse(parts[0]);
        int end   = int.Parse(parts[1]);
        return new WorkSchedule(start, end);
    }
}
