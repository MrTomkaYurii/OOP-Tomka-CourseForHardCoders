using Basic.Reference.Assemblies;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using System.Reflection;
using System.Text;

namespace runner.Services;

public record RunResult(bool Success, string Output);

public class CSharpRunner
{
    // Reference assemblies вбудовані в пакет Basic.Reference.Assemblies.Net90
    // Ніяких HTTP запитів, ніяких проблем з _framework/
    private static readonly IReadOnlyList<MetadataReference> References = Net90.References.All;

    public Task<RunResult> RunAsync(string code) => Task.Run(() => Run(code));

    private RunResult Run(string code)
    {
        var syntaxTree = CSharpSyntaxTree.ParseText(code);

        var compilation = CSharpCompilation.Create(
            assemblyName: "UserCode",
            syntaxTrees: [syntaxTree],
            references: References,
            options: new CSharpCompilationOptions(
                OutputKind.ConsoleApplication,
                optimizationLevel: OptimizationLevel.Release,
                allowUnsafe: false,
                concurrentBuild: false));

        using var ms = new MemoryStream();
        var emitResult = compilation.Emit(ms);

        if (!emitResult.Success)
        {
            var errors = emitResult.Diagnostics
                .Where(d => d.Severity == DiagnosticSeverity.Error)
                .Select(d =>
                {
                    var line = d.Location.GetLineSpan().StartLinePosition.Line + 1;
                    return $"Рядок {line}: {d.GetMessage()}";
                });

            return new RunResult(false, string.Join("\n", errors));
        }

        // Виконуємо скомпільовану збірку
        ms.Seek(0, SeekOrigin.Begin);
        var assembly = Assembly.Load(ms.ToArray());
        var entryPoint = assembly.EntryPoint;

        if (entryPoint is null)
            return new RunResult(false, "Помилка: точку входу (Main) не знайдено.");

        var sb = new StringBuilder();
        var oldOut = Console.Out;
        var oldErr = Console.Error;
        var writer = new StringWriter(sb);

        Console.SetOut(writer);
        Console.SetError(writer);

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
            if (inner is PlatformNotSupportedException)
            {
                sb.Append("\n[Браузер] System.Threading.Thread не підтримується у браузері (WebAssembly однопоточний).\nВідкрий цей приклад у dotnetfiddle.net — там працює повноцінний .NET.");
                return new RunResult(false, sb.ToString());
            }
            else if (inner is MissingMethodException mme)
            {
                sb.Append($"\n[{inner.GetType().Name}] {inner.Message}");
                var msg = mme.Message;
                if (msg.Contains("ToUpper") || msg.Contains("ToLower") ||
                    msg.Contains("ToTitle") || msg.Contains("Compare") ||
                    msg.Contains("String.Normalize") || msg.Contains("CultureInfo"))
                {
                    sb.Append("\n\n[Браузер] Runner працює з інваріантною культурою (Invariant Globalization Mode).\nЗамість ToUpper() використовуй ToUpperInvariant(), замість ToLower() — ToLowerInvariant().");
                }
                else
                {
                    sb.Append("\n\n[Браузер] Цей API недоступний у WebAssembly runner.\nВідкрий цей приклад у dotnetfiddle.net — там працює повноцінний .NET.");
                }
                return new RunResult(false, sb.ToString());
            }
            sb.Append($"\n[{inner.GetType().Name}] {inner.Message}");
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
}
