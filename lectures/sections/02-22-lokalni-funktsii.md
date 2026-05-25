---
chapter: 2
chapterTitle: "Розділ 2. Основи програмування на C#"
section: 22
number: "2.22"
title: "Локальні функції"
source: "../_migration/source-chunks/11-rekursiia-ta-lokalni-funktsii.md"
---

## 2.22. Локальні функції

Локальна функція — це функція, оголошена безпосередньо всередині іншого методу. Вона існує і видима виключно в межах того методу, де оголошена, і не може бути викликана ззовні. Локальні функції вирішують конкретну проблему: дозволяють виокремити фрагмент логіки у власний іменований блок, не виносячи його у простір імен класу як окремий метод. Це корисно тоді, коли певна допоміжна операція потрібна лише в одному місці і немає сенсу робити її частиною публічного або навіть приватного API класу.

## Навіщо потрібні локальні функції

Розглянемо метод, який аналізує результати аналізів пацієнта і перевіряє кілька показників. Без локальної функції повторювана логіка перевірки дублюється:

```csharp run
using System;

void AnalyzeBloodTest(double hemoglobin, double glucose, double cholesterol)
{
    // перевірка гемоглобіну
    string hgbStatus = hemoglobin < 120 ? "Низький" : hemoglobin > 170 ? "Високий" : "Норма";
    Console.WriteLine($"Гемоглобін {hemoglobin.ToString("F1")}: {hgbStatus}");

    // та сама логіка для глюкози і холестерину — дублювання
    string glcStatus = glucose < 3.9 ? "Низький" : glucose > 6.1 ? "Високий" : "Норма";
    Console.WriteLine($"Глюкоза {glucose.ToString("F1")}: {glcStatus}");

    string chlStatus = cholesterol < 3.0 ? "Низький" : cholesterol > 5.2 ? "Високий" : "Норма";
    Console.WriteLine($"Холестерин {cholesterol.ToString("F1")}: {chlStatus}");
}

AnalyzeBloodTest(115.0, 5.4, 6.1);
```

Логіка `"Низький" / "Норма" / "Високий"` повторюється тричі. Локальна функція усуває це дублювання, залишаючи код лише всередині методу:

```csharp run
using System;

void AnalyzeBloodTest(double hemoglobin, double glucose, double cholesterol)
{
    Console.WriteLine($"Гемоглобін {hemoglobin.ToString("F1")}: {Classify(hemoglobin, 120, 170)}");
    Console.WriteLine($"Глюкоза {glucose.ToString("F1")}: {Classify(glucose, 3.9, 6.1)}");
    Console.WriteLine($"Холестерин {cholesterol.ToString("F1")}: {Classify(cholesterol, 3.0, 5.2)}");

    string Classify(double value, double low, double high)
    {
        if (value < low)  return "Низький";
        if (value > high) return "Високий";
        return "Норма";
    }
}

AnalyzeBloodTest(115.0, 5.4, 6.1);
AnalyzeBloodTest(135.0, 4.5, 4.8);
```

Локальна функція `Classify` визначена після того, як використовується — у C# порядок оголошення всередині методу не має значення. Вона видима у всьому тілі методу `AnalyzeBloodTest`, але абсолютно невидима ззовні.

![Область видимості локальної функції](_assets/02-22/local-function-scope.png)

## Доступ до змінних зовнішнього методу

Звичайна (нестатична) локальна функція має доступ до змінних і параметрів методу, всередині якого вона визначена. Ці змінні можна читати і змінювати без явної передачі як параметри:

```csharp run
using System;

void GeneratePatientReport(string patientName, int wardNumber)
{
    string header = $"=== Пацієнт: {patientName} (Палата {wardNumber.ToString()}) ===";

    PrintSection("Анамнез", "Хронічний бронхіт, 5 років");
    PrintSection("Скарги", "Кашель, задишка при навантаженні");
    PrintSection("Призначення", "Інгалятор, фізіотерапія");

    void PrintSection(string title, string content)
    {
        // header — змінна зовнішнього методу, доступна без параметра
        Console.WriteLine(header);
        Console.WriteLine($"  [{title}]: {content}");
    }
}

GeneratePatientReport("Іван Петренко", 7);
```

Функція `PrintSection` читає змінну `header` зовнішнього методу напряму. Це зручно, але вимагає уваги: локальна функція може ненавмисно змінити змінні зовнішнього контексту, що ускладнює розуміння коду.

## Статичні локальні функції

Щоб гарантовано заборонити локальній функції звертатися до змінних зовнішнього методу, її можна оголосити зі словом `static`. Статична локальна функція ізольована: вона бачить лише те, що отримує через свої параметри. Будь-яка спроба звернутися до змінної зовнішнього методу всередині статичної локальної функції — це помилка компіляції.

```csharp run
using System;

void ProcessLabResults(double[] values, double minNorm, double maxNorm)
{
    int belowCount = 0;
    int aboveCount = 0;

    foreach (var v in values)
    {
        string status = Classify(v, minNorm, maxNorm);
        Console.WriteLine($"  {v.ToString("F1")} → {status}");
        if (status == "Нижче норми") belowCount++;
        if (status == "Вище норми")  aboveCount++;
    }

    Console.WriteLine($"Нижче норми: {belowCount.ToString()}, Вище норми: {aboveCount.ToString()}");

    static string Classify(double value, double low, double high)
    {
        // minNorm, maxNorm — НЕ доступні тут (статична функція)
        if (value < low)  return "Нижче норми";
        if (value > high) return "Вище норми";
        return "Норма";
    }
}

double[] glucoseReadings = { 3.5, 5.1, 7.2, 4.8, 6.8, 3.1 };
ProcessLabResults(glucoseReadings, 3.9, 6.1);
```

![Звичайна vs static локальна функція](_assets/02-22/static-vs-nonstatic-local.png)

Перевага `static` локальної функції — явна гарантія ізольованості. Читаючи сигнатуру `static string Classify(...)`, розробник одразу розуміє: ця функція не має прихованих побічних ефектів через захоплені змінні, її поведінка визначається лише аргументами. Це робить код передбачуваним і простішим для тестування.

## Локальні функції проти приватних методів

Локальна функція і приватний метод класу вирішують схожу задачу — ізоляція допоміжної логіки — але мають різну область застосування:

- **Приватний метод** доступний усьому класу. Використовуйте його, якщо допоміжна логіка може знадобитися кільком методам класу.
- **Локальна функція** доступна лише одному методу. Використовуйте її, якщо логіка потрібна виключно в одному місці і виносити її в клас означало б штучно розширювати API.

Локальні функції також корисні для покращення читабельності складних методів: замість того щоб читати 80 рядків коду підряд, читач бачить короткий метод з виразними викликами іменованих локальних функцій і занурюється в деталі лише за потреби.
