using System.Reflection;
using ClinicApp.Attributes;

namespace ClinicApp.Utils;

public static class ModelValidator
{
    public static ValidationResult Validate(object obj)
    {
        var result = new ValidationResult();
        var type = obj.GetType();

        foreach (var prop in type.GetProperties())
        {
            var value = prop.GetValue(obj);

            var required = prop.GetCustomAttribute<RequiredAttribute>();
            if (required != null)
            {
                if (value is null || (value is string s && string.IsNullOrWhiteSpace(s)))
                    result.AddError($"{prop.Name}: {required.ErrorMessage}");
            }

            var maxLength = prop.GetCustomAttribute<MaxLengthAttribute>();
            if (maxLength != null && value is string str)
            {
                if (str.Length > maxLength.Length)
                    result.AddError($"{prop.Name}: {maxLength.ErrorMessage}");
            }

            var minValue = prop.GetCustomAttribute<MinValueAttribute>();
            if (minValue != null)
            {
                double numericValue = value switch
                {
                    int i => i,
                    double d => d,
                    decimal dec => (double)dec,
                    float f => f,
                    long l => l,
                    _ => double.MaxValue
                };
                if (numericValue < minValue.Min)
                    result.AddError($"{prop.Name}: {minValue.ErrorMessage}");
            }
        }

        return result;
    }

    public static void PrintInfo(Type type)
    {
        Console.WriteLine($"Type: {type.Name}");
        Console.WriteLine("Properties:");
        foreach (var prop in type.GetProperties())
        {
            var attrs = prop.GetCustomAttributes().ToArray();
            string attrList = attrs.Length > 0
                ? string.Join(", ", attrs.Select(a => a.GetType().Name.Replace("Attribute", "")))
                : "none";
            Console.WriteLine($"  {prop.PropertyType.Name} {prop.Name} [{attrList}]");
        }
    }
}
