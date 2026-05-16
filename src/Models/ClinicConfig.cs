namespace ClinicApp.Models;

/// <summary>
/// ClinicConfig — конфігурація клініки (S: Single Responsibility).
///
/// Lab 22 / Task 1: Принцип єдиної відповідальності (SRP).
///
/// Проблема в Clinic.cs:
///   Клас Clinic робить ЗАНАДТО БАГАТО:
///     — зберігає дані клініки (Name)
///     — створює і тримає 16 менеджерів / сервісів
///     — оркеструє підписки на події (SubscribeEvents)
///     — генерує текстовий звіт (GenerateReport)
///     — відображає розклад (DisplaySchedule)
///
///   Це порушення SRP: "клас повинен мати тільки одну причину для зміни".
///   У поточному Clinic — таких причин п'ять.
///
/// Рішення (повне, для продакшн-коду):
///   Clinic         → тільки оркестрування (створення, wire-up)
///   ClinicConfig   → конфігурація (ім'я, адреса, дата відкриття)
///   ClinicReporter → звіти (GenerateReport, DisplaySchedule)
///   ClinicEventBus → підписки подій (SubscribeEvents)
///
/// В Lab 22 ми виділяємо ClinicConfig і показуємо принцип.
/// Повне розбиття — за бажанням студента як розширене завдання.
/// </summary>
public record ClinicConfig(
    string   Name,
    string   Address  = "",
    DateTime? Founded = null
)
{
    /// <summary>Рік заснування або "невідомо".</summary>
    public string FoundedYear => Founded.HasValue
        ? Founded.Value.Year.ToString()
        : "невідомо";

    public override string ToString() =>
        $"{Name}" +
        (string.IsNullOrEmpty(Address) ? "" : $", {Address}") +
        $" (засновано: {FoundedYear})";
}
