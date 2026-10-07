// Задача 8. Тривимірний масив — аналіз відділень по змінах
//
// Зчитайте тривимірний масив [відділення][тиждень][зміна]
// де зміна 0 = ранкова, зміна 1 = вечірня.
// Виведіть детальну аналітику і знайдіть найзавантаженіше відділення.
//
// Вхідні дані:
//   D          — кількість відділень (int)
//   W          — кількість тижнів (int)
//   D×W×2 рядків — пацієнтів (int), порядок:
//                  [відд0,тижд0,ранок], [відд0,тижд0,вечір],
//                  [відд0,тижд1,ранок], [відд0,тижд1,вечір], ...
//                  [відд1,тижд0,ранок], ...
//
// Вихідні дані:
//   Відділення 1:
//     Тиждень 1: ранок X, вечір Y → разом Z
//     ...
//     Разом: X пацієнтів
//   ...
//   Найзавантаженіше: Відділення K (X пацієнтів)
//
// Приклад:
//   Вхід:       Вихід:
//   2           Відділення 1:
//   2             Тиждень 1: ранок 15, вечір 10 → разом 25
//   15            Тиждень 2: ранок 12, вечір 8 → разом 20
//   10            Разом: 45 пацієнтів
//   12          Відділення 2:
//   8             Тиждень 1: ранок 20, вечір 15 → разом 35
//   20            Тиждень 2: ранок 18, вечір 12 → разом 30
//   15            Разом: 65 пацієнтів
//   18          Найзавантаженіше: Відділення 2 (65 пацієнтів)
//   12

public static class Task8
{
    public static void Run()
    {
        int d = int.Parse(Console.ReadLine()!);
        int w = int.Parse(Console.ReadLine()!);

        int[,,] data = new int[d, w, 2];
        for (int dept = 0; dept < d; dept++)
            for (int week = 0; week < w; week++)
                for (int shift = 0; shift < 2; shift++)
                    data[dept, week, shift] = int.Parse(Console.ReadLine()!);

        int[] totals = new int[d];
        for (int dept = 0; dept < d; dept++)
        {
            Console.WriteLine($"Відділення {dept + 1}:");
            for (int week = 0; week < w; week++)
            {
                int morning   = data[dept, week, 0];
                int evening   = data[dept, week, 1];
                int weekTotal = morning + evening;
                totals[dept] += weekTotal;
                Console.WriteLine($"  Тиждень {week + 1}: ранок {morning}, вечір {evening} → разом {weekTotal}");
            }
            Console.WriteLine($"  Разом: {totals[dept]} пацієнтів");
        }

        int maxIdx = 0;
        for (int i = 1; i < d; i++)
            if (totals[i] > totals[maxIdx]) maxIdx = i;

        Console.WriteLine($"Найзавантаженіше: Відділення {maxIdx + 1} ({totals[maxIdx]} пацієнтів)");
    }
}
