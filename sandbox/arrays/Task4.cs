// Задача 4. Матриця прийомів лікарів (2D масив)
//
// Зчитайте матрицю N×M, де рядок = лікар, стовпець = робочий день.
// Кожна клітинка — кількість прийомів.
// Виведіть суми по рядках (навантаження лікаря), суми по стовпцях
// (навантаження дня) і знайдіть максимальний елемент.
//
// Вхідні дані:
//   N          — кількість лікарів (int)
//   M          — кількість робочих днів (int)
//   N рядків   — по M цілих чисел через пробіл
//
// Вихідні дані:
//   Лікар 1: X прийомів
//   ...
//   По днях: d1, d2, ..., dM
//   Максимум: X (Лікар K, День J)
//
// Приклад:
//   Вхід:       Вихід:
//   3           Лікар 1: 12 прийомів
//   3           Лікар 2: 11 прийомів
//   5 3 4       Лікар 3: 15 прийомів
//   2 8 1       По днях: 13, 13, 12
//   6 2 7       Максимум: 8 (Лікар 2, День 2)
//
//   Вхід:       Вихід:
//   2           Лікар 1: 14 прийомів
//   4           Лікар 2: 18 прийомів
//   4 3 5 2     По днях: 6, 8, 9, 9
//   2 5 4 7     Максимум: 7 (Лікар 2, День 4)

public static class Task4
{
    public static void Run()
    {
        int n = int.Parse(Console.ReadLine()!);
        int m = int.Parse(Console.ReadLine()!);

        int[,] matrix = new int[n, m];
        for (int i = 0; i < n; i++)
        {
            string[] parts = Console.ReadLine()!.Split(' ');
            for (int j = 0; j < m; j++)
                matrix[i, j] = int.Parse(parts[j]);
        }

        // Row sums (per doctor)
        for (int i = 0; i < n; i++)
        {
            int rowSum = 0;
            for (int j = 0; j < m; j++)
                rowSum += matrix[i, j];
            Console.WriteLine($"Лікар {i + 1}: {rowSum} прийомів");
        }

        // Column sums (per day)
        int[] colSums = new int[m];
        for (int j = 0; j < m; j++)
            for (int i = 0; i < n; i++)
                colSums[j] += matrix[i, j];
        Console.WriteLine($"По днях: {string.Join(", ", colSums)}");

        // Max element with position
        int maxVal = matrix[0, 0], maxRow = 0, maxCol = 0;
        for (int i = 0; i < n; i++)
            for (int j = 0; j < m; j++)
                if (matrix[i, j] > maxVal)
                {
                    maxVal = matrix[i, j];
                    maxRow = i;
                    maxCol = j;
                }
        Console.WriteLine($"Максимум: {maxVal} (Лікар {maxRow + 1}, День {maxCol + 1})");
    }
}
