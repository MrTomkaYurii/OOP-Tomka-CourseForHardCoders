using Basic.Reference.Assemblies;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using System.Text;

var repoRoot = FindRepoRoot(AppContext.BaseDirectory);
var lecturesDir = Path.Combine(repoRoot, "lectures", "sections");
var reportPath = Path.Combine(repoRoot, "tools", "report.md");

var mdFiles = Directory.GetFiles(lecturesDir, "*.md").Order().ToArray();
Console.WriteLine($"Лекцій: {mdFiles.Length}");

var references = Net90.References.All;
var results = new List<CheckResult>();

foreach (var file in mdFiles)
{
    var name = Path.GetFileName(file);
    var content = File.ReadAllText(file);
    var blocks = ExtractRunBlocks(content);

    for (int i = 0; i < blocks.Count; i++)
    {
        var (code, lineNumber) = blocks[i];
        var errors = Compile(code, references);
        results.Add(new CheckResult(name, i + 1, lineNumber, code, errors));

        var icon = errors.Count == 0 ? "✅" : "❌";
        Console.WriteLine($"  {icon} {name} блок {i + 1} (рядок {lineNumber})");
    }
}

var report = BuildReport(results);
File.WriteAllText(reportPath, report, Encoding.UTF8);

int errCount = results.Count(r => r.Errors.Count > 0);
Console.WriteLine();
Console.WriteLine($"Блоків: {results.Count}  ❌ помилок: {errCount}  ✅ ок: {results.Count - errCount}");
Console.WriteLine($"Звіт: {reportPath}");

// ── helpers ──────────────────────────────────────────────────────────────────

static List<(string code, int line)> ExtractRunBlocks(string content)
{
    var result = new List<(string, int)>();
    var lines = content.Split('\n');

    for (int i = 0; i < lines.Length; i++)
    {
        var trimmed = lines[i].TrimStart();
        if (!trimmed.StartsWith("```csharp run", StringComparison.Ordinal)) continue;

        int startLine = i + 2; // 1-based, первий рядок коду
        var code = new List<string>();
        i++;

        while (i < lines.Length && !lines[i].TrimStart().StartsWith("```"))
        {
            code.Add(lines[i]);
            i++;
        }

        result.Add((string.Join('\n', code), startLine));
    }

    return result;
}

static List<string> Compile(string code, IReadOnlyList<MetadataReference> references)
{
    var tree = CSharpSyntaxTree.ParseText(code);
    var compilation = CSharpCompilation.Create(
        "Check",
        [tree],
        references,
        new CSharpCompilationOptions(
            OutputKind.ConsoleApplication,
            optimizationLevel: OptimizationLevel.Release,
            concurrentBuild: false));

    using var ms = new MemoryStream();
    var emit = compilation.Emit(ms);

    return emit.Diagnostics
        .Where(d => d.Severity == DiagnosticSeverity.Error)
        .Select(d => $"рядок {d.Location.GetLineSpan().StartLinePosition.Line + 1}: {d.GetMessage()}")
        .ToList();
}

static string BuildReport(List<CheckResult> all)
{
    var sb = new StringBuilder();
    var errors = all.Where(r => r.Errors.Count > 0).ToList();
    var ok = all.Where(r => r.Errors.Count == 0).ToList();

    sb.AppendLine("# Звіт: runnable коди в лекціях");
    sb.AppendLine();
    sb.AppendLine($"Дата: {DateTime.Now:yyyy-MM-dd HH:mm}  |  " +
                  $"Всього: {all.Count}  |  ❌ {errors.Count}  |  ✅ {ok.Count}");
    sb.AppendLine();

    // ── Таблиця помилок ──────────────────────────────────────────────────────
    sb.AppendLine("## ❌ Блоки з помилками компіляції");
    sb.AppendLine();

    if (errors.Count == 0)
    {
        sb.AppendLine("_Немає помилок — всі блоки компілюються._");
    }
    else
    {
        sb.AppendLine("| Файл | Блок | Рядок у файлі | Помилка (перша) | Код (5 рядків) |");
        sb.AppendLine("|------|:----:|:-------------:|-----------------|----------------|");

        foreach (var r in errors)
        {
            var firstErr = r.Errors[0];
            var moreErr  = r.Errors.Count > 1 ? $" _(+{r.Errors.Count - 1})_" : "";
            var preview  = string.Join(" ↵ ", r.Code.Split('\n').Take(5)
                               .Select(l => l.Trim())
                               .Where(l => l.Length > 0))
                               .Replace("|", "\\|");
            if (preview.Length > 80) preview = preview[..80] + "…";

            sb.AppendLine($"| `{r.File}` | #{r.BlockIndex} | {r.LineNumber} | {EscapeMd(firstErr)}{moreErr} | `{preview}` |");
        }
    }

    sb.AppendLine();

    // ── Детальний розбір кожного блоку з помилками ───────────────────────────
    if (errors.Count > 0)
    {
        sb.AppendLine("## Деталі помилок");
        sb.AppendLine();

        foreach (var r in errors)
        {
            sb.AppendLine($"### `{r.File}` — блок #{r.BlockIndex} (рядок файлу {r.LineNumber})");
            sb.AppendLine();
            sb.AppendLine("**Помилки:**");
            foreach (var e in r.Errors)
                sb.AppendLine($"- {EscapeMd(e)}");
            sb.AppendLine();
            sb.AppendLine("**Код:**");
            sb.AppendLine("```csharp");
            sb.AppendLine(r.Code);
            sb.AppendLine("```");
            sb.AppendLine();
        }
    }

    // ── Успішні блоки ────────────────────────────────────────────────────────
    sb.AppendLine("## ✅ Блоки що компілюються успішно");
    sb.AppendLine();
    sb.AppendLine("| Файл | Блок | Рядок у файлі |");
    sb.AppendLine("|------|:----:|:-------------:|");
    foreach (var r in ok)
        sb.AppendLine($"| `{r.File}` | #{r.BlockIndex} | {r.LineNumber} |");

    return sb.ToString();
}

static string EscapeMd(string s) => s.Replace("|", "\\|").Replace("`", "'");

static string FindRepoRoot(string start)
{
    var dir = new DirectoryInfo(start);
    while (dir != null)
    {
        if (Directory.Exists(Path.Combine(dir.FullName, "lectures")))
            return dir.FullName;
        dir = dir.Parent;
    }
    throw new InvalidOperationException("Не знайдено папку 'lectures' — переконайтесь що запускаєте з репозиторію.");
}

record CheckResult(string File, int BlockIndex, int LineNumber, string Code, List<string> Errors);
