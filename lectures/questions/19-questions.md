---
chapter: 19
chapterTitle: "Розділ 19. Серіалізація JSON та XML"
type: self-assessment
---

# Питання для самоконтролю — Розділ 19. Серіалізація JSON та XML

## 19.1. System.Text.Json — розширені можливості

1. Навіщо `JsonDocument` використовує `ArrayPool` і чому обов'язковий блок `using`? Що відбудеться, якщо не викликати `Dispose()` на `JsonDocument`?

2. Розгляньте код:
   ```csharp
   using var doc = JsonDocument.Parse(jsonString);
   JsonElement root = doc.RootElement;
   if (root.TryGetProperty("patient", out JsonElement patient))
   {
       Console.WriteLine(patient.GetProperty("name").GetString());
       Console.WriteLine(patient.GetProperty("age").GetInt32());
   }
   ```
   Чим `TryGetProperty` відрізняється від `GetProperty`? Коли і яке з них використовувати?

3. Перелічіть значення `JsonValueKind`. Напишіть метод `PrintJsonStructure(JsonElement element, int depth)`, що рекурсивно обходить JSON та виводить структуру з відступами, розрізняючи об'єкти, масиви та примітивні значення.

4. Реалізуйте за допомогою `Utf8JsonWriter` JSON-документ такого вигляду:
   ```json
   { "report": { "date": "2024-01-15", "items": [1, 2, 3], "valid": true } }
   ```
   Назвіть методи, що ви використаєте для кожного елементу.

5. Для чого потрібен `JsonConverter<T>`? Реалізуйте конвертер `DateOnlyJsonConverter`, що серіалізує `DateOnly` у рядок формату `"dd.MM.yyyy"` і десеріалізує назад. Як зареєструвати його через атрибут і через глобальні налаштування?

6. Поясніть `[JsonPolymorphic]` і `[JsonDerivedType]`. Яку проблему вони вирішують? Напишіть ієрархію `Animal` (базовий) → `Dog`, `Cat` з дискримінатором та продемонструйте, як JSON виглядає після серіалізації списку.

7. Що таке JSON Source Generators? Яку проблему з рефлексією вони вирішують і в яких середовищах особливо важливі (AOT, Blazor WASM)? Напишіть мінімальний приклад з `[JsonSerializable]` та `JsonSerializerContext`.

8. Назвіть щонайменше 3 проблеми безпеки при десеріалізації JSON від зовнішніх джерел. Чому рекомендують мати окремі DTO для вводу та виводу? Що таке `MaxDepth` і чому важливо його обмежувати?

## 19.2. XML та XmlDocument

1. Поясніть структуру XML-документа: що таке декларація, елемент, атрибут, namespace? Напишіть XML-фрагмент для опису лікаря з атрибутом `id` та вкладеними елементами.

2. Розгляньте код:
   ```csharp
   var doc = new XmlDocument();
   doc.LoadXml(xml);
   XmlNode root = doc.DocumentElement;
   foreach (XmlNode child in root.ChildNodes)
   {
       Console.WriteLine(child.InnerText);
   }
   ```
   Чим `InnerText` відрізняється від `InnerXml`? Наведіть XML, де ці два значення різні.

3. Напишіть XPath-вираз і відповідний C# код для `XmlDocument.SelectNodes()`, що знаходить всі елементи `<appointment>` де атрибут `status` дорівняє `"confirmed"` і дочірній елемент `<doctor>` має значення `"Smith"`.

4. Порівняйте `SelectSingleNode` і `SelectNodes`. Що повертає `SelectSingleNode`, якщо нічого не знайдено? Що станеться, якщо передати хибний XPath? Напишіть безпечний виклик з перевіркою результату.

5. Програмно побудуйте за допомогою `XmlDocument` наступну структуру:
   ```xml
   <patients>
     <patient id="1">
       <name>John Doe</name>
       <age>35</age>
     </patient>
   </patients>
   ```
   Назвіть методи `CreateElement`, `CreateAttribute`, `SetAttribute`, `AppendChild` у правильному порядку.

6. Як зберегти `XmlDocument` у файл? Як зберегти у рядок? Напишіть обидва варіанти та поясніть, коли кожен з них доцільний.

7. Що таке `XmlTextWriter` і коли він використовується разом з `XmlDocument.WriteTo()`? Покажіть, як налаштувати форматований вивід з відступами.

## 19.3. XDocument та LINQ to XML

1. Порівняйте стиль створення XML-документа в `XmlDocument` проти `XDocument`. У чому перевага декларативного синтаксису `XDocument`? Відтворіть той самий XML-фрагмент обома способами.

2. Розгляньте код:
   ```csharp
   var doc = XDocument.Parse(xml);
   var names = doc.Root
       .Elements("patient")
       .Where(p => (int)p.Element("age") > 30)
       .Select(p => (string)p.Element("name"))
       .OrderBy(n => n);
   ```
   Поясніть кожен крок LINQ-ланцюжка. Що станеться, якщо елемент `<age>` відсутній?

3. Чим `Element("name")` відрізняється від `Elements("name")` та `Descendants("name")`? Наведіть XML, де ці три методи дадуть різні результати.

4. Напишіть метод, що завантажує XML-файл пацієнтів, знаходить пацієнта за ID, оновлює його вік та зберігає файл назад. Використайте `SetValue` або `SetAttributeValue`.

5. Реалізуйте LINQ запит по `XDocument`, що групує лікарів за спеціальністю і для кожної групи виводить кількість та середній стаж. Використайте `GroupBy` і `Select`.

6. Напишіть метод `List<Patient> ParsePatients(XDocument doc)`, що витягує всі записи пацієнтів з XML і повертає строго типізований список C# об'єктів. Обробіть відсутні необов'язкові елементи.

7. Як `XDocument` порівнюється з `XmlDocument` за продуктивністю? Коли краще використовувати `XmlDocument`, а коли `XDocument`? Що таке LINQ to XML і чим воно відрізняється від XPath у `XmlDocument`?

## 19.4. XmlReader та XmlWriter

1. Що означає "forward-only" читання? У яких сценаріях `XmlReader` є єдиним правильним вибором порівняно з `XmlDocument` або `XDocument`?

2. Розгляньте код:
   ```csharp
   using var reader = XmlReader.Create("data.xml");
   while (reader.Read())
   {
       if (reader.NodeType == XmlNodeType.Element && reader.Name == "patient")
       {
           string id = reader.GetAttribute("id");
           reader.ReadToDescendant("name");
           string name = reader.ReadElementContentAsString();
       }
   }
   ```
   Поясніть кожен крок. Що відбудеться, якщо елемент `<name>` відсутній всередині `<patient>`?

3. Назвіть 5 значень `XmlNodeType`, які зустрічаються при читанні реального XML. Напишіть умову, що ігнорує пробіли та коментарі за допомогою `XmlReaderSettings`.

4. Чим `ReadToFollowing`, `ReadToDescendant` і `ReadToNextSibling` відрізняються один від одного? Намалюйте (текстово) XML-дерево та покажіть, до якого вузла переміститься кожен метод від поточної позиції.

5. Реалізуйте метод `XmlToJsonStream(Stream xmlInput, Stream jsonOutput)`, що зчитує XML пацієнтів за допомогою `XmlReader` і записує їх у JSON за допомогою `Utf8JsonWriter`, не завантажуючи весь документ у пам'ять.

6. Напишіть за допомогою `XmlWriter` документ з правильною декларацією, коментарем, кількома елементами та атрибутами. Налаштуйте `XmlWriterSettings` для форматованого виводу з `Indent = true` та кодуванням UTF-8.

7. Опишіть паттерн "XmlReader + XmlWriter трансформація". Напишіть метод `FilterLargeXml(string inputPath, string outputPath, Predicate<string> keepPatient)`, що читає великий XML пацієнтів і записує тільки тих, що задовольняють умову.

## 19.5. XmlSerializer

1. Які вимоги до класу для роботи з `XmlSerializer`? Що станеться, якщо клас не має публічного конструктора без параметрів? Чому поля та властивості мають бути публічними?

2. Розгляньте код:
   ```csharp
   [XmlRoot("medicalRecord")]
   public class Record
   {
       [XmlAttribute("id")]
       public int Id { get; set; }
       [XmlElement("patientName")]
       public string Name { get; set; }
       [XmlIgnore]
       public string InternalNotes { get; set; }
   }
   ```
   Як виглядатиме XML після серіалізації? Як виглядатиме XML без жодних атрибутів?

3. Поясніть різницю між `[XmlElement]` і `[XmlAttribute]`. Яка між ними семантична різниця з погляду XML-моделювання? Коли краще використовувати атрибут, а коли елемент?

4. Як серіалізувати список за допомогою `[XmlArray]` і `[XmlArrayItem]`? Напишіть клас `Hospital` зі списком `Doctors` та покажіть очікуваний XML. Як виглядатиме XML без цих атрибутів?

5. Що таке `[XmlInclude]`? Напишіть ієрархію `Payment` → `CashPayment`, `CardPayment` з можливістю серіалізації через `XmlSerializer`. Чим це відрізняється від `[JsonPolymorphic]`?

6. Як позбутися namespace-ів `xmlns:xsi` та `xmlns:xsd` у серіалізованому XML? Напишіть код з `XmlSerializerNamespaces`, що генерує чистий XML без зайвих просторів імен.

7. Порівняйте `XmlSerializer` з ручним підходом через `XmlDocument`. Коли варто обрати `XmlSerializer`, а коли ручне керування? Які обмеження є у `XmlSerializer`?

## 19.6. XPath та порівняння JSON і XML

1. Поясніть XPath-вирази: `/root/patient`, `//patient`, `patient[@status='active']`, `patient[1]`, `patient[last()]`. Чим `/` відрізняється від `//`?

2. Напишіть XPath для таких задач:
   - Знайти всі `<appointment>` елементи на будь-якому рівні вкладеності
   - Знайти `<patient>`, у якого `<age>` більше 30
   - Знайти перший `<doctor>` з атрибутом `specialty`, що містить слово "cardio"
   - Підрахувати кількість `<appointment>` зі статусом "pending"

3. Які вісі XPath (axes) ви знаєте? Поясніть різницю між `child::`, `descendant::`, `following-sibling::` і `ancestor::`. Наведіть приклад XPath з явною назвою вісі.

4. Порівняйте використання XPath у `XmlDocument.SelectNodes()` і в `XDocument.XPathSelectElements()`. Що треба підключити для використання XPath у `XDocument`? Напишіть однаковий запит обома способами.

5. Що таке `XPathNavigator` і `XPathExpression`? Яку перевагу дає компіляція XPath-виразу через `XPathExpression.Compile()`? Коли це суттєво впливає на продуктивність?

6. Заповніть таблицю порівняння JSON і XML за ознаками: розмір, читабельність, підтримка атрибутів, namespace-и, стандартна схема, типовий API (REST/SOAP), інструменти запитів. Для яких галузей/стандартів XML залишається обов'язковим?

7. Дано задачу: потрібно зберігати конфігурацію для веб-API. Аргументуйте вибір JSON або XML, враховуючи: читабельність, розмір, підтримку в .NET, тип клієнтів (браузер/мобільний/корпоративний).

8. Напишіть метод, що приймає XML-рядок медичного запису і за допомогою `XPathNavigator` та скомпільованого `XPathExpression` виконує багаторазовий пошук різних полів. Порівняйте продуктивність з некомпільованим підходом.
