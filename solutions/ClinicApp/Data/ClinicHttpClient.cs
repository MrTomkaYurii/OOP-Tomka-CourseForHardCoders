namespace ClinicApp.Data;

using System.Net.Http.Json;
using System.Text.Json.Serialization;

/// <summary>
/// ClinicHttpClient — async HTTP-запити до зовнішніх сервісів.
///
/// Task 6: HttpClient + async + JSON десеріалізація + обробка помилок.
///
/// ВАЖЛИВО про HttpClient:
///   HttpClient реалізує IDisposable, але НЕ варто створювати new HttpClient() на кожен запит!
///   Причина: HttpClient тримає TCP-з'єднання відкритим для повторного використання.
///   Якщо створювати/dispose на кожен запит → socket exhaustion (вичерпання портів).
///
///   ✅ Правильно: статичний або singleton HttpClient
///   ✅ В ASP.NET Core: IHttpClientFactory (управляє пулом)
///   ❌ Неправильно: using var http = new HttpClient() { ... запити ... }
///
/// Демонстрація:
///   — GetFromJsonAsync&lt;T&gt; — отримати JSON і десеріалізувати
///   — CancellationToken для таймаутів
///   — Обробка HttpRequestException (мережа) та TaskCanceledException (таймаут)
///   — Task.WhenAny для race між запитом і таймаутом
///
/// API: FDA Open Data (https://open.fda.gov/apis/)
///   Публічний API без реєстрації. Пошук інформації про ліки за назвою.
/// </summary>
public class ClinicHttpClient
{
    // Статичний HttpClient — один на весь час роботи застосунку
    // BaseAddress: не обов'язковий, але спрощує відносні URL
    // Timeout: HttpClient.Timeout — глобальний таймаут (default: 100 сек)
    private static readonly HttpClient _http = new()
    {
        BaseAddress = new Uri("https://api.fda.gov/"),
        Timeout = TimeSpan.FromSeconds(15)
    };

    // ─────────────────────────────────────────────────────────────────────
    // Task 6A: GetFromJsonAsync<T> — отримати і десеріалізувати JSON
    //
    // GetFromJsonAsync<T>(url, ct):
    //   1. await _http.GetAsync(url, ct)    — надсилає GET-запит
    //   2. response.ReadFromJsonAsync<T>()  — читає тіло і десеріалізує
    //   Еквівалент: GetAsync + ReadAsStringAsync + JsonSerializer.Deserialize
    //
    // [JsonPropertyName("...")] — маппінг JSON-поля на C# властивість
    //   (потрібен коли JSON snake_case, а C# PascalCase)
    // ─────────────────────────────────────────────────────────────────────

    /// <summary>
    /// Пошук інформації про лікарський засіб за назвою (FDA Open API).
    /// </summary>
    public async Task<DrugInfo?> GetDrugInfoAsync(string drugName, CancellationToken ct = default)
    {
        try
        {
            // Uri.EscapeDataString — кодування спецсимволів у URL (%20 замість пробілу)
            string url = $"drug/label.json?search=openfda.brand_name:{Uri.EscapeDataString(drugName)}&limit=1";

            // GetFromJsonAsync<T> = GET + JSON десеріалізація в один виклик
            // Повертає null при 204 No Content
            var response = await _http.GetFromJsonAsync<FdaResponse>(url, ct);

            var result = response?.Results?.FirstOrDefault();
            if (result is null) return null;

            return new DrugInfo(
                drugName,
                TrimLong(result.Purpose?.FirstOrDefault()  ?? "Не вказано"),
                TrimLong(result.Warnings?.FirstOrDefault() ?? "Не вказано"),
                TrimLong(result.Dosage?.FirstOrDefault()   ?? "Не вказано")
            );
        }
        catch (HttpRequestException ex)
        {
            // Мережева помилка: нема з'єднання, DNS fail, SSL error тощо
            Console.WriteLine($"[ClinicHttpClient] Мережева помилка: {ex.StatusCode} — {ex.Message}");
            return null;
        }
        catch (TaskCanceledException) when (!ct.IsCancellationRequested)
        {
            // TaskCanceledException є при:
            //   1. HttpClient.Timeout → ловимо тут (ct.IsCancellationRequested == false)
            //   2. ct.Cancel()        → НЕ ловимо (дозволяємо спливати до caller)
            Console.WriteLine("[ClinicHttpClient] Таймаут запиту — FDA API не відповідає.");
            return null;
        }
        // OperationCanceledException (базовий клас TaskCanceledException) від ct — не ловимо!
        // Він спливе вгору і сигналізує caller про скасування.
    }

    // ─────────────────────────────────────────────────────────────────────
    // Task 6B: Health check — перевірка доступності API
    //
    // Демонстрація простого async bool методу:
    //   — try/catch навколо async виклику
    //   — return false при будь-якій помилці (fail-safe)
    // ─────────────────────────────────────────────────────────────────────

    public async Task<bool> IsApiAvailableAsync(CancellationToken ct = default)
    {
        try
        {
            // Мінімальний запит: limit=1 щоб не завантажувати зайве
            using var response = await _http.GetAsync("drug/label.json?limit=1", ct);
            return response.IsSuccessStatusCode;
        }
        catch
        {
            return false;
        }
    }

    // ─────────────────────────────────────────────────────────────────────
    // Task 6C: Task.WhenAny — race між запитом і таймаутом
    //
    // Альтернатива HttpClient.Timeout: більш гнучкий контроль.
    // Корисно коли потрібно: спробувати 3 секунди, потім показати cached дані.
    // ─────────────────────────────────────────────────────────────────────

    public async Task<DrugInfo?> GetDrugInfoWithRaceAsync(string drugName, int timeoutMs = 5000)
    {
        using var cts = CancellationTokenSource.CreateLinkedTokenSource(CancellationToken.None);

        var apiTask     = GetDrugInfoAsync(drugName, cts.Token);
        var timeoutTask = Task.Delay(timeoutMs, cts.Token);

        // Task.WhenAny — повертає Task який завершився першим (не кидає виключення)
        var winner = await Task.WhenAny(apiTask, timeoutTask);

        if (winner == timeoutTask)
        {
            // Таймаут виграв — скасовуємо API-запит
            await cts.CancelAsync();
            Console.WriteLine($"[ClinicHttpClient] Race: таймаут {timeoutMs}мс — API програло.");
            return null;
        }

        // API-запит виграв — повертаємо результат
        // apiTask.Result — безпечно, бо Task вже завершений
        return apiTask.Result;
    }

    // ── Допоміжний метод: обрізаємо довгі рядки з FDA API ────────────────
    private static string TrimLong(string s, int max = 200)
        => s.Length > max ? s[..max] + "..." : s;

    // ─────────────────────────────────────────────────────────────────────
    // Private DTO для десеріалізації JSON відповіді FDA API
    //
    // record з JsonPropertyName — зіставляє snake_case JSON → PascalCase C#
    // System.Text.Json (вбудований в .NET) — без додаткових пакетів
    // ─────────────────────────────────────────────────────────────────────

    private record FdaResponse(
        [property: JsonPropertyName("results")] List<FdaResult>? Results
    );

    private record FdaResult(
        [property: JsonPropertyName("purpose")]                   List<string>? Purpose,
        [property: JsonPropertyName("warnings")]                  List<string>? Warnings,
        [property: JsonPropertyName("dosage_and_administration")] List<string>? Dosage
    );
}

/// <summary>Інформація про лікарський засіб з FDA Open API.</summary>
public record DrugInfo(
    string Name,
    string Purpose,
    string Warnings,
    string Dosage
);
