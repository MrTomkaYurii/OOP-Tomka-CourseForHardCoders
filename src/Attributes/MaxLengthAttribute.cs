namespace ClinicApp.Attributes;

[AttributeUsage(AttributeTargets.Property, AllowMultiple = false)]
public sealed class MaxLengthAttribute : Attribute
{
    public int Length { get; }
    public string ErrorMessage { get; }

    public MaxLengthAttribute(int length, string errorMessage = "")
    {
        Length = length;
        ErrorMessage = string.IsNullOrEmpty(errorMessage)
            ? $"Maximum length is {length} characters."
            : errorMessage;
    }
}
