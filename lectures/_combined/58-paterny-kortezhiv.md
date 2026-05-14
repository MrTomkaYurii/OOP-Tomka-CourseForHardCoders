## 9.3. Патерни кортежів

Патерни кортежів дозволяють порівнювати значення кортежів. Наприклад, передамо конструкції switch кортеж з назвою мови та часу дня і в залежності від переданих даних повернемо певне повідомлення:

```csharp
string GetWelcome(string lang, string daytime) => (lang, daytime) switch
{
    ("english", "morning") => "Good morning",
    ("english", "evening") => "Good evening",
    ("german", "morning") => "Guten Morgen",
    ("german", "evening") => "Guten Abend",
    _ => "Привіт"
};
```

Тут методу передаються два значення, з яких створюється кортеж (можна й відразу передати методу кортеж). Далі у конструкції switch за допомогою круглих дужок визначаються значення, яким повинні відповідати елементи кортежу. Наприклад, вираз ("english", "morning") => "Good morning" буде виконуватися, якщо одночасно lang = "english" та daytime = "morning".

Застосування:

```csharp
string message = GetWelcome("english", "evening");
Console.WriteLine(message);  // Good evening

message = GetWelcome("french", "morning");
Console.WriteLine(message);  // Привіт
```

Нам не обов'язково порівнювати всі значення кортежу, ми можемо використовувати лише деякі елементи кортежу. Якщо ми не хочемо використовувати елемент кортежу, то замість нього ставимо прочерк:

```csharp
string GetWelcome(string lang, string daytime, string status) =>
    (lang, daytime, status) switch
    {
        ("english", "morning", _) => "Good morning",
        ("english", "evening", _) => "Good evening",
        ("german", "morning", _) => "Guten Morgen",
        ("german", "evening", _) => "Guten Abend",
        (_, _, "admin") => "Hello, Admin",
        _ => "Вітання"
    };
```

Тепер кортеж складається із трьох елементів. Але перші чотири вирази не використовують останній елемент кортежу, припустимо, він не важливий, тому замість нього ставиться прочерк ("english", "morning", _).

На передостанньому прикладі, навпаки, не важливі перші два елементи, а важливий третій елемент: (_, _, "admin") =>.

Але в будь-якому разі нам треба вказати конкретні значення чи прочерки для всіх елементів кортежу.

```csharp
string message = GetWelcome("english", "evening", "user");
Console.WriteLine(message);  // Good evening

message = GetWelcome("french", "morning", "admin");
Console.WriteLine(message);  // Hello, Admin
```
