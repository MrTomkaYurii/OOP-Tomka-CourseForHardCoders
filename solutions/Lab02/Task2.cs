// Задача 2. Сортування черги прийомів
//
// Зчитайте N вартостей прийомів і відсортуйте масив
// методом бульбашки (bubble sort) за зростанням.
//
// Вхідні дані:
//   N          — кількість прийомів (int, > 0)
//   N рядків   — вартість кожного (int, грн)
//
// Вихідні дані:
//   Черга (до):    c1 c2 ... cN
//   Черга (після): c1 c2 ... cN  (відсортована)
//   Найдешевший:   X грн
//   Найдорожчий:   X грн
//
// Приклади:
//   Вхід:       Вихід:
//   5           Черга (до):    500 200 800 350 150
//   500         Черга (після): 150 200 350 500 800
//   200         Найдешевший:   150 грн
//   800         Найдорожчий:   800 грн
//   350
//   150
//
//   Вхід:       Вихід:
//   3           Черга (до):    300 100 200
//   300         Черга (після): 100 200 300
//   100         Найдешевший:   100 грн
//   200         Найдорожчий:   300 грн

public static class Task2
{
    public static void Run()
    {
        int n = int.Parse(Console.ReadLine()!);
        int[] queue = new int[n];
        for (int i = 0; i < n; i++)
            queue[i] = int.Parse(Console.ReadLine()!);

        Console.WriteLine($"Черга (до):    {string.Join(" ", queue)}");

        // Bubble sort
        for (int i = 0; i < n - 1; i++)
            for (int j = 0; j < n - 1 - i; j++)
                if (queue[j] > queue[j + 1])
                {
                    int temp = queue[j];
                    queue[j] = queue[j + 1];
                    queue[j + 1] = temp;
                }

        Console.WriteLine($"Черга (після): {string.Join(" ", queue)}");
        Console.WriteLine($"Найдешевший:   {queue[0]} грн");
        Console.WriteLine($"Найдорожчий:   {queue[n - 1]} грн");
    }
}
