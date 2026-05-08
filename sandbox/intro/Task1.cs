// Задача 1. ІМТ пацієнта
//
// Напишіть програму, яка зчитує вагу та зріст пацієнта
// і розраховує Індекс маси тіла за формулою:
//
//   ІМТ = вага / (зріст * зріст)
//
// Вхідні дані:
//   вага — дійсне число (кг)
//   зріст — дійсне число (м)
//
// Вихідні дані:
//   ІМТ: X.XX
//
// Приклади:
//   Вхід     Вихід
//   70       ІМТ: 22.86
//   1.75
//
//   Вхід     Вихід
//   90       ІМТ: 27.78
//   1.80
//
//   Вхід     Вихід
//   55       ІМТ: 20.95
//   1.62

public static class Task1
{
    public static void Run()
    {
        double weight = double.Parse(Console.ReadLine()!);
        double height = double.Parse(Console.ReadLine()!);

        double bmi = weight / (height * height);

        Console.WriteLine($"ІМТ: {bmi:F2}");
    }
}
