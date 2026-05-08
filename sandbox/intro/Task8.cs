// Задача 8. Методи
//
// Перепишіть логіку Задач 1–4 так, щоб кожен розрахунок
// був винесений у окремий метод. У Run() — тільки зчитування
// та виклики методів, жодних розрахунків у тілі Run.
//
// Методи:
//   CalculateBMI(weight, height)       → double
//   GetBMICategory(bmi)                → string
//   CalculateCost(price, visits, disc) → double
//   GetAgeCategory(age)                → string
//   GetPressureStatus(sys, dia)        → string
//
// Вхідні дані (всі дані разом, рядок за рядком):
//   вага кг          (дробове)
//   зріст м          (дробове)
//   ціна прийому     (дробове)
//   кількість        (ціле)
//   знижка %         (ціле)
//   рік народження   (ціле)
//   систолічний      (ціле)
//   діастолічний     (ціле)
//
// Вихідні дані:
//   ІМТ: X.XX -> Y
//   Сума: X.XX грн
//   Вік: X р., категорія: Y
//   Тиск: X/Y — Z
//
// Приклади:
//   Вхід:       Вихід:
//   82.0        ІМТ: 25.88 -> надмірна вага
//   1.78        Сума: 1350.00 грн
//   500         Вік: 36 р., категорія: дорослий
//   3           Тиск: 120/80 — гіпертонія 1 ступеня
//   10
//   1990
//   120
//   80
//
//   Вхід:       Вихід:
//   55.0        ІМТ: 20.95 -> норма
//   1.62        Сума: 340.00 грн
//   200         Вік: 16 р., категорія: дитина
//   2           Тиск: 155/100 — гіпертонія 2 ступеня
//   15
//   2010
//   155
//   100

public static class Task8
{
    public static void Run()
    {
        double weight   = double.Parse(Console.ReadLine()!);
        double height   = double.Parse(Console.ReadLine()!);
        double price    = double.Parse(Console.ReadLine()!);
        int    visits   = int.Parse(Console.ReadLine()!);
        int    discount = int.Parse(Console.ReadLine()!);
        int    birthYear = int.Parse(Console.ReadLine()!);
        int    systolic  = int.Parse(Console.ReadLine()!);
        int    diastolic = int.Parse(Console.ReadLine()!);

        double bmi  = CalculateBMI(weight, height);
        double cost = CalculateCost(price, visits, discount);
        int    age  = 2026 - birthYear;

        Console.WriteLine($"ІМТ: {bmi:F2} -> {GetBMICategory(bmi)}");
        Console.WriteLine($"Сума: {cost:F2} грн");
        Console.WriteLine($"Вік: {age} р., категорія: {GetAgeCategory(age)}");
        Console.WriteLine($"Тиск: {systolic}/{diastolic} — {GetPressureStatus(systolic, diastolic)}");
    }

    static double CalculateBMI(double weight, double height)
        => weight / (height * height);

    static string GetBMICategory(double bmi)
    {
        if (bmi < 18.5) return "недостатня вага";
        if (bmi < 25.0) return "норма";
        if (bmi < 30.0) return "надмірна вага";
        return "ожиріння";
    }

    static double CalculateCost(double price, int visits, int discount)
        => price * visits * (1 - discount / 100.0);

    static string GetAgeCategory(int age)
    {
        if (age < 18) return "дитина";
        if (age < 60) return "дорослий";
        return "пенсіонер";
    }

    static string GetPressureStatus(int systolic, int diastolic)
    {
        if (systolic < 120 && diastolic < 80) return "норма";
        if (systolic < 130 && diastolic < 80) return "підвищений";
        if (systolic < 140 || diastolic < 90) return "гіпертонія 1 ступеня";
        return "гіпертонія 2 ступеня";
    }
}
