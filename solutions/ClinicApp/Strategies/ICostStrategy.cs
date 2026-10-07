namespace ClinicApp.Strategies;

using ClinicApp.Models;

/// <summary>
/// ICostStrategy — стратегія розрахунку вартості прийому.
///
/// Lab 22 / Task 2: Принцип відкритості/закритості (OCP).
///
/// Проблема без OCP:
///   AppointmentProcessor або Appointment містять switch/if для кожного типу:
///     if (appointment is UrgentAppointment) cost *= 1.5m;
///     else if (appointment is SpecialistAppointment) cost *= 1.3m;
///     // Щоб додати новий тип → змінюємо існуючий код → ризик регресій
///
/// Рішення (OCP):
///   — Визначаємо інтерфейс ICostStrategy (закритий для змін)
///   — Кожен новий спосіб розрахунку — нова реалізація (відкритий для розширення)
///   — AppointmentProcessor приймає будь-який ICostStrategy без змін своєї логіки
///
/// Паттерн: Strategy (GoF) — поведінка обміняна через інтерфейс.
/// </summary>
public interface ICostStrategy
{
    /// <summary>Людська назва стратегії (для логів, UI).</summary>
    string Description { get; }

    /// <summary>Розрахувати вартість прийому.</summary>
    decimal Calculate(Appointment appointment);
}
