// Задача 1. Ваги пацієнтів
//
// Зчитайте N ваг пацієнтів і обрахуйте статистику.
//
// Вхідні дані:
//   N          — кількість пацієнтів (int, > 0)
//   N рядків   — вага кожного (double, кг)
//
// Вихідні дані:
//   Кількість:       N
//   Середня вага:    X.X кг
//   Мін / Макс:      X.X / X.X кг
//   Вище середнього: K з N
//
// Приклади:
//   Вхід:       Вихід:
//   5           Кількість:       5
//   70.0        Середня вага:    77.4 кг
//   85.5        Мін / Макс:      62.0 / 91.0 кг
//   62.0        Вище середнього: 3 з 5
//   91.0
//   78.3
//
//   Вхід:       Вихід:
//   3           Кількість:       3
//   55.0        Середня вага:    71.7 кг
//   70.0        Мін / Макс:      55.0 / 90.0 кг
//   90.0        Вище середнього: 1 з 3

public static class Task1
{
    public static void Run()
    {
        int n = int.Parse(Console.ReadLine()!);
        double[] weights = new double[n];
        for (int i = 0; i < n; i++)
            weights[i] = double.Parse(Console.ReadLine()!);

        double sum = 0, min = weights[0], max = weights[0];
        foreach (double w in weights)
        {
            sum += w;
            if (w < min) min = w;
            if (w > max) max = w;
        }
        double avg = sum / n;

        int aboveAvg = 0;
        for (int i = 0; i < n; i++)
            if (weights[i] > avg) aboveAvg++;

        Console.WriteLine($"Кількість:       {n}");
        Console.WriteLine($"Середня вага:    {avg:F1} кг");
        Console.WriteLine($"Мін / Макс:      {min:F1} / {max:F1} кг");
        Console.WriteLine($"Вище середнього: {aboveAvg} з {n}");
    }
}
