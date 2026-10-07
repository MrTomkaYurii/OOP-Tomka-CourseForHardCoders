namespace ClinicApp.Utils;

using ClinicApp.Enums;

public static class ClinicFormatter
{
    public static string FormatBloodType(BloodType bt) => bt switch
    {
        BloodType.APositive  => "A+",
        BloodType.ANegative  => "A-",
        BloodType.BPositive  => "B+",
        BloodType.BNegative  => "B-",
        BloodType.ABPositive => "AB+",
        BloodType.ABNegative => "AB-",
        BloodType.OPositive  => "O+",
        BloodType.ONegative  => "O-",
        _                    => "Невідомо"
    };

    public static string FormatSpeciality(Speciality s) => s switch
    {
        Speciality.General      => "Загальна практика",
        Speciality.Cardiology   => "Кардіологія",
        Speciality.Neurology    => "Неврологія",
        Speciality.Pediatrics   => "Педіатрія",
        Speciality.Surgery      => "Хірургія",
        Speciality.Orthopedics  => "Ортопедія",
        Speciality.Dermatology  => "Дерматологія",
        Speciality.Emergency    => "Невідкладна допомога",
        _                       => "Невідомо"
    };

    public static string FormatAge(int age)
    {
        if (age % 100 >= 11 && age % 100 <= 19) return age + " років";
        switch (age % 10)
        {
            case 1:            return age + " рік";
            case 2: case 3: case 4: return age + " роки";
            default:           return age + " років";
        }
    }

    public static string FormatPhone(string phone)
    {
        if (phone == null || phone.Length != 10) return phone ?? "";
        for (int i = 0; i < phone.Length; i++)
            if (phone[i] < '0' || phone[i] > '9') return phone;
        return "(" + phone.Substring(0, 3) + ") " + phone.Substring(3, 3) + "-" + phone.Substring(6);
    }
}
