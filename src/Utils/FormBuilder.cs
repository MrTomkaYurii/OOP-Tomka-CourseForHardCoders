using System.Reflection;
using ClinicApp.Attributes;

namespace ClinicApp.Utils;

public static class FormBuilder
{
    public static T Build<T>() where T : new()
    {
        var obj = new T();
        var type = typeof(T);

        Console.WriteLine($"=== Fill in {type.Name} ===");

        foreach (var prop in type.GetProperties().Where(p => p.CanWrite))
        {
            var required = prop.GetCustomAttribute<RequiredAttribute>();
            var maxLength = prop.GetCustomAttribute<MaxLengthAttribute>();
            var minVal = prop.GetCustomAttribute<MinValueAttribute>();

            string hint = BuildHint(required, maxLength, minVal);
            Console.Write($"  {prop.Name}{hint}: ");

            string? input = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(input)) continue;

            try
            {
                object? converted = Convert.ChangeType(input.Trim(), prop.PropertyType);
                prop.SetValue(obj, converted);
            }
            catch
            {
                Console.WriteLine($"  [!] Invalid value for {prop.Name}, skipped.");
            }
        }

        return obj;
    }

    private static string BuildHint(RequiredAttribute? req, MaxLengthAttribute? max, MinValueAttribute? min)
    {
        var parts = new List<string>();
        if (req != null) parts.Add("required");
        if (max != null) parts.Add($"max {max.Length}");
        if (min != null) parts.Add($"min {min.Min}");
        return parts.Count > 0 ? $" ({string.Join(", ", parts)})" : "";
    }
}
