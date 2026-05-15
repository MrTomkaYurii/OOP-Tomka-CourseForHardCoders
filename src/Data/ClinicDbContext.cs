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
    public DbSet<Patient>        Patients        => Set<Patient>();
    public DbSet<Doctor>         Doctors         => Set<Doctor>();
    public DbSet<Appointment>    Appointments    => Set<Appointment>();
    public DbSet<MedicalRecord>  MedicalRecords  => Set<MedicalRecord>();

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

            // Soft Delete — IsDeleted прапор замість фізичного DELETE
            entity.Property(p => p.IsDeleted).HasDefaultValue(false);

            // Global Query Filter (Lab 20): автоматично додає WHERE IsDeleted = 0 до кожного запиту.
            // Не потрібно писати .Where(p => !p.IsDeleted) вручну скрізь.
            // Щоб побачити "видалені" — використати .IgnoreQueryFilters()
            entity.HasQueryFilter(p => !p.IsDeleted);
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

        // ── Task 2 (Lab 18): Таблиця Appointments — One-to-Many ───
        // TPH (Table Per Hierarchy) — усі підтипи Appointment в одній таблиці.
        // EF розрізняє їх через стовпець-дискримінатор "AppointmentType".
        modelBuilder.Entity<Appointment>(entity =>
        {
            entity.ToTable("Appointments");

            entity.HasKey(a => a.Id);
            entity.Property(a => a.Id).ValueGeneratedOnAdd();

            entity.Property(a => a.ScheduledAt).IsRequired();

            entity.Property(a => a.DurationMinutes)
                  .IsRequired()
                  .HasDefaultValue(30);

            entity.Property(a => a.Status)
                  .HasConversion<string>()
                  .HasMaxLength(20)
                  .IsRequired();

            entity.Property(a => a.Notes)
                  .HasMaxLength(500)
                  .HasDefaultValue("");

            entity.Property(a => a.IsPaid)
                  .HasDefaultValue(false);

            // HasDiscriminator — стовпець що визначає конкретний тип запису.
            // TPH: RegularAppointment, UrgentAppointment, SpecialistAppointment
            // зберігаються в одній таблиці Appointments, розрізняються "AppointmentType".
            entity.HasDiscriminator<string>("AppointmentType")
                  .HasValue<Appointment>("Base")
                  .HasValue<RegularAppointment>("Regular")
                  .HasValue<UrgentAppointment>("Urgent")
                  .HasValue<SpecialistAppointment>("Specialist");

            // ── One-to-Many: Patient → Appointments ──────────────
            // HasOne: "один Patient"; WithMany: "багато Appointments"
            // HasForeignKey: стовпець FK у таблиці Appointments
            // OnDelete Cascade: видалення Patient → видаляє всі його Appointments
            entity.HasOne(a => a.Patient)
                  .WithMany(p => p.Appointments)
                  .HasForeignKey(a => a.PatientId)
                  .OnDelete(DeleteBehavior.Cascade);

            // ── One-to-Many: Doctor → Appointments ───────────────
            // OnDelete Restrict: заборона видалити Doctor, якщо є Appointments
            // Причина: SQL Server не дозволяє дві каскадні доріжки до однієї таблиці
            entity.HasOne(a => a.Doctor)
                  .WithMany(d => d.Appointments)
                  .HasForeignKey(a => a.DoctorId)
                  .OnDelete(DeleteBehavior.Restrict);

            // Індекси для FK — прискорюють JOIN і фільтрацію
            entity.HasIndex(a => a.PatientId).HasDatabaseName("IX_Appointments_PatientId");
            entity.HasIndex(a => a.DoctorId).HasDatabaseName("IX_Appointments_DoctorId");
            entity.HasIndex(a => a.ScheduledAt).HasDatabaseName("IX_Appointments_ScheduledAt");
        });

        // Субтипи Appointment: оголошуємо їх і конфігуруємо унікальні стовпці
        modelBuilder.Entity<UrgentAppointment>()
            .Property(u => u.UrgencyNote).HasMaxLength(200).HasDefaultValue("");

        modelBuilder.Entity<SpecialistAppointment>()
            .Property(s => s.ConsultationTopic).HasMaxLength(200).HasDefaultValue("");

        // ── Task 1-3 (Lab 19): Таблиця MedicalRecords — TPH ──────────────────
        // Всі підтипи (Diagnosis, LabResult, Prescription) в одній таблиці.
        // Стовпець "RecordType" відрізняє типи.
        // NULL-стовпці для полів які стосуються лише одного підтипу.
        modelBuilder.Entity<MedicalRecord>(entity =>
        {
            entity.ToTable("MedicalRecords");
            entity.HasKey(r => r.Id);
            entity.Property(r => r.Id).ValueGeneratedOnAdd();

            entity.Property(r => r.Date).IsRequired();
            entity.Property(r => r.Notes).HasMaxLength(500).HasDefaultValue("");

            // TPH дискримінатор для MedicalRecord ієрархії
            entity.HasDiscriminator<string>("RecordType")
                  .HasValue<Diagnosis>("Diagnosis")
                  .HasValue<LabResult>("LabResult")
                  .HasValue<Prescription>("Prescription");

            // One-to-Many: Patient → MedicalRecords (Cascade)
            entity.HasOne(r => r.Patient)
                  .WithMany(p => p.MedicalRecords)
                  .HasForeignKey(r => r.PatientId)
                  .OnDelete(DeleteBehavior.Cascade);

            // DoctorId — просто FK без navigation (спрощення для Lab 19)
            entity.HasOne<Doctor>()
                  .WithMany()
                  .HasForeignKey(r => r.DoctorId)
                  .OnDelete(DeleteBehavior.Restrict);

            entity.HasIndex(r => r.PatientId).HasDatabaseName("IX_MedicalRecords_PatientId");
            entity.HasIndex(r => r.DoctorId).HasDatabaseName("IX_MedicalRecords_DoctorId");
        });

        // Diagnosis специфічні стовпці
        modelBuilder.Entity<Diagnosis>(entity =>
        {
            entity.Property(d => d.DiagnosisCode).HasMaxLength(20).HasDefaultValue("").IsRequired(false);
            entity.Property(d => d.Description).HasMaxLength(500).HasDefaultValue("").IsRequired(false);
        });

        // LabResult специфічні стовпці
        modelBuilder.Entity<LabResult>(entity =>
        {
            entity.Property(l => l.TestName).HasMaxLength(200).HasDefaultValue("").IsRequired(false);
            entity.Property(l => l.Unit).HasMaxLength(30).HasDefaultValue("").IsRequired(false);
            entity.Property(l => l.ReferenceRange).HasMaxLength(50).HasDefaultValue("").IsRequired(false);
        });

        // Prescription специфічні стовпці
        modelBuilder.Entity<Prescription>(entity =>
        {
            entity.Property(p => p.MedicationName).HasMaxLength(200).HasDefaultValue("").IsRequired(false);
            entity.Property(p => p.Dosage).HasMaxLength(100).HasDefaultValue("").IsRequired(false);
            entity.Property(p => p.Instructions).HasMaxLength(500).HasDefaultValue("").IsRequired(false);
        });

        // ── Task 2 (Lab 19): OwnsOne — EmergencyContact у таблиці Patients ────
        // OwnsOne: Owned Entity — декілька стовпців власника без окремої таблиці.
        // Відмінність від ValueConverter: OwnsOne → окремі стовпці (EmergencyContact_Name тощо).
        // ValueConverter (WorkSchedule) → один стовпець з серіалізованим значенням.
        modelBuilder.Entity<Patient>().OwnsOne(p => p.EmergencyContact, ec =>
        {
            // Префікс "EC_" для ясності в таблиці (замість дефолтного "EmergencyContact_")
            ec.Property(e => e.Name)        .HasColumnName("EC_Name")        .HasMaxLength(100);
            ec.Property(e => e.Phone)       .HasColumnName("EC_Phone")       .HasMaxLength(20);
            ec.Property(e => e.Relationship).HasColumnName("EC_Relationship").HasMaxLength(50);
        });

        // ── Task 3 (Lab 19): Concurrency Token — RowVersion ──────────────────
        // IsConcurrencyToken + ValueGeneratedOnAddOrUpdate:
        //   SQL Server автоматично оновлює rowversion при кожному UPDATE.
        //   EF додає "WHERE RowVersion = @original" до UPDATE/DELETE.
        //   Якщо за час між SELECT і UPDATE інший процес змінив запис —
        //   rowversion інша → WHERE не знаходить рядка → DbUpdateConcurrencyException.
        modelBuilder.Entity<Patient>()
            .Property(p => p.RowVersion)
            .IsRowVersion()     // це і є IsConcurrencyToken + ValueGeneratedOnAddOrUpdate
            .HasColumnName("RowVersion");
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
