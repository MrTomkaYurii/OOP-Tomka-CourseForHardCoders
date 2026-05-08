// Задача 7. Паралельні масиви — рейтинг ІМТ пацієнтів
//
// Зчитайте N пацієнтів (ім'я + ІМТ) у два паралельні масиви.
// Відсортуйте за спаданням ІМТ методом бульбашки,
// переміщуючи обидва масиви синхронно. Виведіть пронумерований рейтинг.
//
// Вхідні дані:
//   N          — кількість пацієнтів (int)
//   Для кожного: рядок з іменем, потім рядок з ІМТ (double)
//
// Вихідні дані:
//   === Рейтинг ІМТ ===
//   #1 Ім'я: X.XX
//   #2 Ім'я: X.XX
//   ...
//
// Приклади:
//   Вхід:       Вихід:
//   4           === Рейтинг ІМТ ===
//   Ivan        #1 Petro: 35.10
//   28.5        #2 Ivan: 28.50
//   Olha        #3 Olha: 22.30
//   22.3        #4 Maria: 19.80
//   Petro
//   35.1
//   Maria
//   19.8
//
//   Вхід:       Вихід:
//   3           === Рейтинг ІМТ ===
//   Anna        #1 Bob: 30.50
//   24.0        #2 Anna: 24.00
//   Bob         #3 Carl: 17.20
//   30.5
//   Carl
//   17.2

public static class Task7
{
    public static void Run()
    {
        int n = int.Parse(Console.ReadLine()!);
        string[] names = new string[n];
        double[] bmis  = new double[n];

        for (int i = 0; i < n; i++)
        {
            names[i] = Console.ReadLine()!;
            bmis[i]  = double.Parse(Console.ReadLine()!);
        }

        // Bubble sort descending — обидва масиви синхронно
        for (int i = 0; i < n - 1; i++)
            for (int j = 0; j < n - 1 - i; j++)
                if (bmis[j] < bmis[j + 1])
                {
                    (bmis[j], bmis[j + 1])   = (bmis[j + 1], bmis[j]);
                    (names[j], names[j + 1]) = (names[j + 1], names[j]);
                }

        Console.WriteLine("=== Рейтинг ІМТ ===");
        for (int i = 0; i < n; i++)
            Console.WriteLine($"#{i + 1} {names[i]}: {bmis[i]:F2}");
    }
}
