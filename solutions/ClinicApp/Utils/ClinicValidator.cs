namespace ClinicApp.Utils;

public static class ClinicValidator
{
    public static void ValidateName(string value, string fieldName)
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException(fieldName + " не може бути порожнім.");
        if (value.Length > 50)
            throw new ArgumentException(fieldName + " занадто довге (макс. 50 символів).");
    }

    public static void ValidatePhone(string phone)
    {
        if (string.IsNullOrWhiteSpace(phone))
            throw new ArgumentException("Телефон не може бути порожнім.");
        if (phone.Length != 10)
            throw new ArgumentException("Телефон має містити рівно 10 цифр.");
        for (int i = 0; i < phone.Length; i++)
            if (phone[i] < '0' || phone[i] > '9')
                throw new ArgumentException("Телефон має містити тільки цифри.");
    }

    public static void ValidateDate(DateTime value, string fieldName)
    {
        if (value > DateTime.Today)
            throw new ArgumentOutOfRangeException(fieldName, "Дата не може бути в майбутньому.");
        if (value.Year < 1900)
            throw new ArgumentOutOfRangeException(fieldName, "Дата не може бути раніше 1900 року.");
    }

    public static void ValidatePositive(int value, string fieldName)
    {
        if (value <= 0)
            throw new ArgumentOutOfRangeException(fieldName, fieldName + " має бути більше нуля.");
    }
}
