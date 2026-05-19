using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using System.Reflection;
using System.Text;

namespace runner.Services;

public record RunResult(bool Success, string Output, int ExitCode = 0);

public class CSharpRunner
{
    private readonly HttpClient _http;
    private List<MetadataReference>? _references;

    // Базові збірки для типових консольних програм C#
    private static readonly string[] ReferenceAssemblies =
    [
        "System.Private.CoreLib.dll",
        "System.Runtime.dll",
        "System.Console.dll",
        "System.Linq.dll",
        "System.Linq.Expressions.dll",
        "System.Collections.dll",
        "System.Collections.Concurrent.dll",
        "System.Text.RegularExpressions.dll",
        "System.Threading.dll",
        "System.Threading.Tasks.dll",
        "System.IO.dll",
        "System.Runtime.Extensions.dll",
        "System.ObjectModel.dll",
        "System.Text.Json.dll",
        "netstandard.dll",
        "mscorlib.dll",
    ];

    public CSharpRunner(HttpClient http) => _http = http;

    public async Task<RunResult> RunAsync(string code)
    {
        // Завантажуємо reference збірки один раз, далі кешуємо
        if (_references is null)
        {
            _references = await LoadReferencesAsync();
        }

        // Парсимо та компілюємо
        var syntaxTree = CSharpSyntaxTree.ParseText(code);

        var compilation = CSharpCompilation.Create(
            assemblyName: "UserCode_" + Guid.NewGuid().ToString("N"),
            syntaxTrees: [syntaxTree],
            references: _references,
            options: new CSharpCompilationOptions(OutputKind.ConsoleApplication,
                optimizationLevel: OptimizationLevel.Release,
                allowUnsafe: false));

        using var ms = new MemoryStream();
        var emitResult = compilation.Emit(ms);

        if (!emitResult.Success)
        {
            var errors = emitResult.Diagnostics
                .Where(d => d.Severity == DiagnosticSeverity.Error)
                .Select(d => $"{d.GetMessage()} (рядок {d.Location.GetLineSpan().StartLinePosition.Line + 1})")
                .ToArray();

            return new RunResult(false, string.Join("\n", errors));
        }

        // Виконуємо скомпільовану збірку
        ms.Seek(0, SeekOrigin.Begin);
        var assembly = Assembly.Load(ms.ToArray());
        var entryPoint = assembly.EntryPoint;

        if (entryPoint is null)
        {
            return new RunResult(false, "Помилка: точку входу не знайдено.");
        }

        var sb = new StringBuilder();
        var oldOut = Console.Out;
        var oldErr = Console.Error;

        Console.SetOut(new StringWriter(sb));
        Console.SetError(new StringWriter(sb));

        try
        {
            var parameters = entryPoint.GetParameters().Length > 0
                ? new object[] { Array.Empty<string>() }
                : null;

            entryPoint.Invoke(null, parameters);
        }
        catch (TargetInvocationException ex)
        {
            var inner = ex.InnerException ?? ex;
            sb.Append($"\n[Exception] {inner.GetType().Name}: {inner.Message}");
            return new RunResult(false, sb.ToString());
        }
        catch (Exception ex)
        {
            sb.Append($"\n[Exception] {ex.Message}");
            return new RunResult(false, sb.ToString());
        }
        finally
        {
            Console.SetOut(oldOut);
            Console.SetError(oldErr);
        }

        return new RunResult(true, sb.ToString());
    }

    private async Task<List<MetadataReference>> LoadReferencesAsync()
    {
        var refs = new List<MetadataReference>();

        foreach (var name in ReferenceAssemblies)
        {
            try
            {
                var bytes = await _http.GetByteArrayAsync($"_framework/{name}");
                refs.Add(MetadataReference.CreateFromImage(bytes));
            }
            catch
            {
                // Якщо збірку не знайдено — пропускаємо
            }
        }

        return refs;
    }
}
