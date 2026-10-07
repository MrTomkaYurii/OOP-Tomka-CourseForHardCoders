// Задача 7. Статистика прийомів
//
// Напишіть програму, яка зчитує кількість прийомів N
// та вартість кожного, після чого виводить зведену статистику.
//
// Вхідні дані:
//   N          — кількість прийомів (ціле > 0)
//   N рядків   — вартість кожного прийому (дробове, грн)
//
// Вихідні дані:
//   === Звіт по прийомах ===
//   Кількість:        N
//   Загальна сума:    X.XX грн
//   Середня:          X.XX грн
//   Мін / Макс:       X.XX / X.XX грн
//   Вище середнього:  K з N
//   Перший > 1000:    #M — X.XX грн   (або "немає")
//   ========================
//
// Приклади:
//   Вхід:        Вихід:
//   5            === Звіт по прийомах ===
//   350          Кількість:        5
//   800          Загальна сума:    3000.00 грн
//   200          Середня:          600.00 грн
//   1200         Мін / Макс:       200.00 / 1200.00 грн
//   450          Вище середнього:  2 з 5
//                Перший > 1000:    #4 — 1200.00 грн
//                ========================
//
//   Вхід:        Вихід:
//   3            === Звіт по прийомах ===
//   300          Кількість:        3
//   450          Загальна сума:    1100.00 грн
//   350          Середня:          366.67 грн
//                Мін / Макс:       300.00 / 450.00 грн
//                Вище середнього:  1 з 3
//                Перший > 1000:    немає
//                ========================

public static class Task7
{
    public static void Run()
    {
        int n = int.Parse(Console.ReadLine()!);

        decimal[] costs = new decimal[n];
        for (int i = 0; i < n; i++)
            costs[i] = decimal.Parse(Console.ReadLine()!);

        // foreach: сума, мін, макс
        decimal total = 0, min = costs[0], max = costs[0];
        foreach (decimal c in costs)
        {
            total += c;
            if (c < min) min = c;
            if (c > max) max = c;
        }

        decimal avg = total / n;

        // for: кількість вище середнього
        int aboveAvg = 0;
        for (int i = 0; i < n; i++)
            if (costs[i] > avg) aboveAvg++;

        // while: перший прийом дорожче 1000 грн
        int expIdx = -1;
        int j = 0;
        while (j < n)
        {
            if (costs[j] > 1000m) { expIdx = j; break; }
            j++;
        }

        Console.WriteLine("=== Звіт по прийомах ===");
        Console.WriteLine($"Кількість:        {n}");
        Console.WriteLine($"Загальна сума:    {total:F2} грн");
        Console.WriteLine($"Середня:          {avg:F2} грн");
        Console.WriteLine($"Мін / Макс:       {min:F2} / {max:F2} грн");
        Console.WriteLine($"Вище середнього:  {aboveAvg} з {n}");

        if (expIdx >= 0)
            Console.WriteLine($"Перший > 1000:    #{expIdx + 1} — {costs[expIdx]:F2} грн");
        else
            Console.WriteLine("Перший > 1000:    немає");

        Console.WriteLine("========================");
    }
}
