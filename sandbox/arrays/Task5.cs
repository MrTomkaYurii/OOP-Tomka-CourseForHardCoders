// Задача 5. Аналіз квадратної матриці показників
//
// Зчитайте квадратну матрицю N×N (наприклад, показники пацієнтів
// у N відділеннях за N тижнів). Знайдіть і виведіть елементи
// та суми головної і побічної діагоналей.
//
// Головна діагональ: клітинки де рядок == стовпець (i == j)
// Побічна діагональ: клітинки де i + j == N - 1
//
// Вхідні дані:
//   N          — розмір матриці (int, ≥ 2)
//   N рядків   — по N цілих чисел через пробіл
//
// Вихідні дані:
//   Головна діагональ: a, b, c, ... (сума = X)
//   Побічна діагональ: a, b, c, ... (сума = Y)
//
// Приклади:
//   Вхід:       Вихід:
//   3           Головна діагональ: 1, 5, 9 (сума = 15)
//   1 2 3       Побічна діагональ: 3, 5, 7 (сума = 15)
//   4 5 6
//   7 8 9
//
//   Вхід:       Вихід:
//   4           Головна діагональ: 2, 8, 4, 5 (сума = 19)
//   2 4 1 3     Побічна діагональ: 3, 6, 1, 3 (сума = 13)
//   5 8 6 7
//   9 1 4 2
//   3 6 8 5

public static class Task5
{
    public static void Run()
    {
        int n = int.Parse(Console.ReadLine()!);
        int[,] matrix = new int[n, n];
        for (int i = 0; i < n; i++)
        {
            string[] parts = Console.ReadLine()!.Split(' ');
            for (int j = 0; j < n; j++)
                matrix[i, j] = int.Parse(parts[j]);
        }

        int[] mainDiag = new int[n];
        int[] secDiag  = new int[n];
        int mainSum = 0, secSum = 0;

        for (int i = 0; i < n; i++)
        {
            mainDiag[i] = matrix[i, i];
            mainSum += matrix[i, i];
            secDiag[i] = matrix[i, n - 1 - i];
            secSum += matrix[i, n - 1 - i];
        }

        Console.WriteLine($"Головна діагональ: {string.Join(", ", mainDiag)} (сума = {mainSum})");
        Console.WriteLine($"Побічна діагональ: {string.Join(", ", secDiag)} (сума = {secSum})");
    }
}
