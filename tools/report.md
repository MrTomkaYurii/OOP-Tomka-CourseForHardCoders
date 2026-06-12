# Звіт: runnable коди в лекціях

Дата: 2026-06-12 12:45  |  Всього: 727  |  ❌ 99  |  ✅ 628

## ❌ Блоки з помилками компіляції

| Файл | Блок | Рядок у файлі | Помилка (перша) | Код (5 рядків) |
|------|:----:|:-------------:|-----------------|----------------|
| `02-24-enum.md` | #1 | 31 | рядок 12: Top-level statements must precede namespace and type declarations. | `using System; ↵ enum PatientStatus ↵ { ↵ Registered,       // 0` |
| `02-24-enum.md` | #2 | 56 | рядок 5: Top-level statements must precede namespace and type declarations. | `using System; ↵ enum PatientStatus { Registered, Admitted, UnderTreatment, Disch…` |
| `02-24-enum.md` | #3 | 86 | рядок 5: Top-level statements must precede namespace and type declarations. | `using System; ↵ enum WardType { ICU, Surgery, Cardiology, Neurology, General } ↵…` |
| `02-24-enum.md` | #4 | 128 | рядок 15: Top-level statements must precede namespace and type declarations. | `using System; ↵ enum BloodType : byte   // byte: 0–255, економить пам'ять ↵ { ↵ …` |
| `02-24-enum.md` | #5 | 154 | рядок 11: Top-level statements must precede namespace and type declarations. | `using System; ↵ enum PriorityLevel ↵ { ↵ Low    = 1,` |
| `06-01-delehaty.md` | #15 | 471 | рядок 38: Top-level statements must precede namespace and type declarations. | `using System; ↵ // Оголошуємо делегат — тип для обробника подій ↵ public delegat…` |
| `06-01-delehaty.md` | #16 | 542 | рядок 40: Top-level statements must precede namespace and type declarations. | `using System; ↵ public delegate void PatientHandler(string message); ↵ public cl…` |
| `06-02-liambdy.md` | #9 | 147 | рядок 7: Cannot implicitly convert type 'System.Action' to 'AlertChain' _(+3)_ | `using System; ↵ var logAlert = () => Console.WriteLine("[LOG] Сигнал тривоги"); …` |
| `06-03-podii.md` | #1 | 77 | рядок 33: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Patient ↵ { ↵ public delegate void PatientHandler(string m…` |
| `06-03-podii.md` | #2 | 123 | рядок 29: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Patient ↵ { ↵ public delegate void PatientHandler(string m…` |
| `06-03-podii.md` | #3 | 173 | рядок 29: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Patient ↵ { ↵ public delegate void PatientHandler(string m…` |
| `06-03-podii.md` | #4 | 223 | рядок 17: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Patient ↵ { ↵ public delegate void PatientHandler(string m…` |
| `06-03-podii.md` | #5 | 256 | рядок 41: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Patient ↵ { ↵ public delegate void PatientHandler(string m…` |
| `06-03-podii.md` | #6 | 315 | рядок 44: Top-level statements must precede namespace and type declarations. | `using System; ↵ class PatientEventArgs ↵ { ↵ public string Message { get; }` |
| `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` | #1 | 20 | рядок 23: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Notification ↵ { ↵ public string Text { get; }` |
| `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` | #2 | 55 | рядок 19: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Notification ↵ { ↵ public string Text { get; }` |
| `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` | #3 | 88 | рядок 19: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Notification ↵ { ↵ public string Text { get; }` |
| `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` | #4 | 125 | рядок 18: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Notification ↵ { ↵ public string Text { get; }` |
| `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` | #5 | 158 | рядок 18: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Notification ↵ { ↵ public string Text { get; }` |
| `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` | #6 | 192 | рядок 24: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Notification ↵ { ↵ public string Text { get; }` |
| `07-01-vyznachennia-interfeisiv.md` | #2 | 105 | рядок 22: Top-level statements must precede namespace and type declarations. | `using System; ↵ interface IDiagnosable ↵ { ↵ void RunDiagnostics();` |
| `07-01-vyznachennia-interfeisiv.md` | #3 | 134 | рядок 17: Top-level statements must precede namespace and type declarations. | `using System; ↵ interface IDiagnosable ↵ { ↵ void RunDiagnostics() => Console.Wr…` |
| `07-02-zastosuvannia-interfeisiv.md` | #1 | 34 | рядок 23: Top-level statements must precede namespace and type declarations. | `using System; ↵ // реалізація інтерфейсу в класі ↵ class Patient : IDiagnosable …` |
| `07-03-yavna-realizatsiia-interfeisiv.md` | #1 | 19 | рядок 14: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Patient : IDiagnosable ↵ { ↵ public string Name { get; }` |
| `07-03-yavna-realizatsiia-interfeisiv.md` | #3 | 89 | рядок 13: Top-level statements must precede namespace and type declarations. | `using System; ↵ // без явної реалізації — один спільний метод ↵ class Patient : …` |
| `07-03-yavna-realizatsiia-interfeisiv.md` | #4 | 112 | рядок 15: Top-level statements must precede namespace and type declarations. | `using System; ↵ class Patient : IDiagnosable, ITreatment ↵ { ↵ public string Nam…` |
| `07-03-yavna-realizatsiia-interfeisiv.md` | #6 | 192 | рядок 31: Top-level statements must precede namespace and type declarations. | `using System; ↵ interface IDiagnosable ↵ { ↵ void RunDiagnostics();` |
| `07-03-yavna-realizatsiia-interfeisiv.md` | #7 | 231 | рядок 18: Top-level statements must precede namespace and type declarations. | `using System; ↵ interface IDiagnosable ↵ { ↵ void RunDiagnostics();` |
| `07-03-yavna-realizatsiia-interfeisiv.md` | #8 | 268 | рядок 17: Top-level statements must precede namespace and type declarations. | `using System; ↵ interface IDiagnosable { void RunDiagnostics(); } ↵ class BaseRe…` |
| `07-03-yavna-realizatsiia-interfeisiv.md` | #9 | 298 | рядок 17: Top-level statements must precede namespace and type declarations. | `using System; ↵ interface IDiagnosable { void RunDiagnostics(); } ↵ class BaseRe…` |
| `07-03-yavna-realizatsiia-interfeisiv.md` | #10 | 328 | рядок 18: Top-level statements must precede namespace and type declarations. | `using System; ↵ interface IDiagnosable { void RunDiagnostics(); } ↵ class BaseRe…` |
| `07-03-yavna-realizatsiia-interfeisiv.md` | #11 | 359 | рядок 21: Top-level statements must precede namespace and type declarations. | `using System; ↵ interface IDiagnosable { void RunDiagnostics(); } ↵ class BaseRe…` |
| `07-06-kopiiuvannia-obiektiv-interfeis-icloneable.md` | #6 | 292 | рядок 18: The type or namespace name 'IComparer<>' could not be found (are you missing a using directive or an assembly reference?) _(+3)_ | `using System; ↵ class Patient ↵ { ↵ public string LastName { get; }` |
| `08-09-kortezhi.md` | #1 | 79 | рядок 18: Identifier expected _(+5)_ | `using System; ↵ // Виконуваний код ↵ // Явний кортеж ↵ (string Name, int Age, do…` |
| `09-05-reliatsiinyi-ta-lohichnyi-paterny.md` | #2 | 93 | рядок 22: The pattern is unreachable. It has already been handled by a previous arm of the switch expression or it is impossible to match. _(+1)_ | `using System; ↵ // Виконуваний код ↵ // Комплексна оцінка стану пацієнта ↵ int[]…` |
| `13-01-vidkladena-initsializatsiia-ta-typ-lazy.md` | #1 | 158 | рядок 33: Top-level statements must precede namespace and type declarations. | `using System; ↵ class PatientRecord ↵ { ↵ public string Name { get; }` |
| `13-01-vidkladena-initsializatsiia-ta-typ-lazy.md` | #2 | 211 | рядок 33: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ class LabNormService ↵ {` |
| `13-04-klas-array.md` | #1 | 198 | рядок 12: Top-level statements must precede namespace and type declarations. _(+1)_ | `using System; ↵ struct Patient ↵ { ↵ public string Id;` |
| `14-01-vvedennia-u-refleksiiu-klas-system-type.md` | #1 | 194 | рядок 21: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Reflection; ↵ class PatientRecord ↵ {` |
| `14-01-vvedennia-u-refleksiiu-klas-system-type.md` | #2 | 249 | рядок 24: Top-level statements must precede namespace and type declarations. | `using System; ↵ class MedicalRecord ↵ { ↵ public string Id { get; }` |
| `15-02-stvorennia-potokiv-threadstart.md` | #5 | 136 | рядок 19: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Threading; ↵ // Клас-обгортка для передачі кількох …` |
| `15-02-stvorennia-potokiv-threadstart.md` | #7 | 223 | рядок 21: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Threading; ↵ // Завдання для обробки в окремому пот…` |
| `15-03-synkhronizatsiia-potokiv-lock.md` | #3 | 105 | рядок 31: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Threading; ↵ // Розклад лікаря — спільний ресурс дл…` |
| `15-04-klas-monitor.md` | #1 | 70 | рядок 53: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ using System.Threading; ↵ //…` |
| `15-04-klas-monitor.md` | #2 | 169 | рядок 47: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ using System.Threading; ↵ cl…` |
| `16-02-vkladeni-zavdannia-task-t.md` | #6 | 173 | рядок 21: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Threading; ↵ using System.Threading.Tasks; ↵ class …` |
| `16-05-skasuvannia-zavdan-cancellationtoken.md` | #2 | 72 | рядок 13: Cannot use local variable 'token' before it is declared | `using System; ↵ using System.Threading; ↵ using System.Threading.Tasks; ↵ Cancel…` |
| `17-02-typy-povernennia-async-metodiv.md` | #5 | 231 | рядок 41: Top-level statements must precede namespace and type declarations. _(+1)_ | `using System; ↵ using System.Threading.Tasks; ↵ // Інтерфейс репозиторію ↵ inter…` |
| `17-06-async-potoky-iasyncenumerable.md` | #6 | 271 | рядок 35: Top-level statements must precede namespace and type declarations. _(+1)_ | `using System; ↵ using System.Collections.Generic; ↵ using System.Runtime.Compile…` |
| `18-01-path-file-directory.md` | #12 | 297 | рядок 34: 'IEnumerable<string>' does not contain a definition for 'OrderByDescending' and no accessible extension method 'OrderByDescending' accepting a first argument of type 'IEnumerable<string>' could be found (are you missing a using directive or an assembly reference?) | `using System; ↵ using System.IO; ↵ // Структура архіву: MedArchive/{рік}/{місяць…` |
| `18-04-streamreader-streamwriter.md` | #8 | 322 | рядок 10: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ using System.IO; ↵ using Sys…` |
| `18-06-system-text-json.md` | #1 | 25 | рядок 16: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Text.Json; ↵ // Моделі даних медичної картки ↵ clas…` |
| `18-06-system-text-json.md` | #2 | 72 | рядок 17: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ using System.IO; ↵ using Sys…` |
| `18-06-system-text-json.md` | #3 | 140 | рядок 14: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Text.Json; ↵ using System.Text.Json.Serialization; …` |
| `18-06-system-text-json.md` | #4 | 194 | рядок 27: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Text.Json; ↵ using System.Text.Json.Serialization; …` |
| `18-06-system-text-json.md` | #5 | 235 | рядок 29: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Text.Json; ↵ using System.Text.Json.Serialization; …` |
| `18-06-system-text-json.md` | #6 | 296 | рядок 21: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ using System.Text.Json; ↵ //…` |
| `18-06-system-text-json.md` | #7 | 347 | рядок 34: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.IO; ↵ using System.Text.Json; ↵ using System.Text.J…` |
| `19-01-system-text-json-advanced.md` | #4 | 170 | рядок 44: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Text.Json; ↵ using System.Text.Json.Serialization; …` |
| `19-01-system-text-json-advanced.md` | #5 | 240 | рядок 34: Top-level statements must precede namespace and type declarations. _(+2)_ | `using System; ↵ using System.Text.Json; ↵ using System.Text.Json.Serialization; …` |
| `19-01-system-text-json-advanced.md` | #6 | 307 | рядок 14: Top-level statements must precede namespace and type declarations. _(+1)_ | `using System; ↵ using System.Collections.Generic; ↵ using System.IO; ↵ using Sys…` |
| `19-02-xml-xmldocument.md` | #6 | 316 | рядок 9: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ using System.IO; ↵ using Sys…` |
| `19-03-xdocument-linq-to-xml.md` | #2 | 73 | рядок 26: No overload for method 'Count' takes 0 arguments _(+1)_ | `using System; ↵ using System.IO; ↵ using System.Xml.Linq; ↵ string path = Path.C…` |
| `19-03-xdocument-linq-to-xml.md` | #3 | 111 | рядок 29: No overload for method 'Count' takes 0 arguments _(+2)_ | `using System; ↵ using System.Xml.Linq; ↵ XDocument doc = XDocument.Parse(""" ↵ <…` |
| `19-03-xdocument-linq-to-xml.md` | #6 | 298 | рядок 8: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ using System.Linq; ↵ using S…` |
| `19-04-xmlreader-xmlwriter.md` | #5 | 290 | рядок 9: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ using System.IO; ↵ using Sys…` |
| `19-05-xmlserializer.md` | #1 | 21 | рядок 14: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.IO; ↵ using System.Xml.Serialization; ↵ public clas…` |
| `19-05-xmlserializer.md` | #2 | 57 | рядок 28: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.IO; ↵ using System.Xml.Serialization; ↵ [XmlRoot("p…` |
| `19-05-xmlserializer.md` | #3 | 112 | рядок 50: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ using System.IO; ↵ using Sys…` |
| `19-05-xmlserializer.md` | #4 | 186 | рядок 16: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.IO; ↵ using System.Xml; ↵ using System.Xml.Serializ…` |
| `19-05-xmlserializer.md` | #5 | 222 | рядок 34: Top-level statements must precede namespace and type declarations. _(+2)_ | `using System; ↵ using System.IO; ↵ using System.Xml.Serialization; ↵ [XmlRoot("e…` |
| `19-05-xmlserializer.md` | #6 | 288 | рядок 43: Top-level statements must precede namespace and type declarations. _(+3)_ | `using System; ↵ using System.IO; ↵ using System.Xml.Serialization; ↵ // Базовий …` |
| `19-05-xmlserializer.md` | #7 | 358 | рядок 46: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ using System.IO; ↵ using Sys…` |
| `20-01-vstup-do-solid.md` | #1 | 45 | рядок 59: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── God Class — еволюція …` |
| `20-01-vstup-do-solid.md` | #2 | 129 | рядок 57: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ using System.Text.RegularExp…` |
| `20-02-srp.md` | #1 | 31 | рядок 77: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── ПОРУШЕННЯ SRP ───────…` |
| `20-02-srp.md` | #2 | 122 | рядок 114: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── ПРАВИЛЬНО: кожен клас…` |
| `20-02-srp.md` | #3 | 258 | рядок 23: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // Тест AppointmentService —…` |
| `20-02-srp.md` | #4 | 313 | рядок 48: Top-level statements must precede namespace and type declarations. | `using System; ↵ // Клас Patient — відповідальність: доменна модель пацієнта ↵ //…` |
| `20-02-srp.md` | #5 | 385 | рядок 43: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── Демонстрація: великий…` |
| `20-03-ocp.md` | #1 | 23 | рядок 61: Top-level statements must precede namespace and type declarations. | `using System; ↵ // ─── ПОРУШЕННЯ OCP ───────────────────────────────────────────…` |
| `20-03-ocp.md` | #2 | 109 | рядок 99: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── ПРАВИЛЬНО: OCP через …` |
| `20-03-ocp.md` | #3 | 237 | рядок 58: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── Strategy Pattern: алг…` |
| `20-03-ocp.md` | #4 | 308 | рядок 65: Top-level statements must precede namespace and type declarations. | `using System; ↵ // ─── Template Method: базовий алгоритм закрито, кроки — відкри…` |
| `20-03-ocp.md` | #5 | 394 | рядок 54: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── Демонстрація: полімор…` |
| `20-04-lsp.md` | #1 | 35 | рядок 31: Top-level statements must precede namespace and type declarations. | `using System; ↵ // ─── Класичний приклад порушення LSP ─────────────────────────…` |
| `20-04-lsp.md` | #2 | 90 | рядок 60: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── ПОРУШЕННЯ LSP ───────…` |
| `20-04-lsp.md` | #3 | 177 | рядок 70: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── ПРАВИЛЬНО: ієрархія в…` |
| `20-04-lsp.md` | #4 | 287 | рядок 68: Top-level statements must precede namespace and type declarations. | `using System; ↵ // ─── Демонстрація правильно побудованої ієрархії MedicalRecord…` |
| `20-04-lsp.md` | #5 | 380 | рядок 34: Top-level statements must precede namespace and type declarations. | `using System; ↵ // Базовий клас ↵ abstract class Doctor ↵ {` |
| `20-05-isp.md` | #1 | 26 | рядок 60: Top-level statements must precede namespace and type declarations. | `using System; ↵ // ─── ПОРУШЕННЯ ISP — «жирний» інтерфейс ──────────────────────…` |
| `20-05-isp.md` | #2 | 99 | рядок 85: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── ПРАВИЛЬНО: вузькі інт…` |
| `20-05-isp.md` | #3 | 218 | рядок 88: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── ISP: інтерфейси як ро…` |
| `20-05-isp.md` | #4 | 347 | рядок 56: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── Правильне застосуванн…` |
| `20-06-dip.md` | #1 | 26 | рядок 48: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── ПОРУШЕННЯ DIP: Appoin…` |
| `20-06-dip.md` | #2 | 91 | рядок 88: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── ПРАВИЛЬНО: DIP через …` |
| `20-06-dip.md` | #3 | 204 | рядок 64: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ interface IPatientLogger ↵ {` |
| `20-06-dip.md` | #4 | 294 | рядок 69: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── Симуляція DI-контейне…` |
| `20-06-dip.md` | #5 | 401 | рядок 49: Top-level statements must precede namespace and type declarations. | `using System; ↵ using System.Collections.Generic; ↵ // ─── DIP + тестові дублі ─…` |

## Деталі помилок

### `02-24-enum.md` — блок #1 (рядок файлу 31)

**Помилки:**
- рядок 12: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

enum PatientStatus
{
    Registered,       // 0
    Admitted,         // 1
    UnderTreatment,   // 2
    Discharged,       // 3
    Critical          // 4
}

PatientStatus status = PatientStatus.Admitted;
Console.WriteLine($"Статус пацієнта: {status.ToString()}");
Console.WriteLine($"Числове значення: {((int)status).ToString()}");
```

### `02-24-enum.md` — блок #2 (рядок файлу 56)

**Помилки:**
- рядок 5: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

enum PatientStatus { Registered, Admitted, UnderTreatment, Discharged, Critical }

void PrintStatus(string patientName, PatientStatus status)
{
    string label = status switch
    {
        PatientStatus.Registered      => "зареєстрований",
        PatientStatus.Admitted        => "прийнятий до відділення",
        PatientStatus.UnderTreatment  => "проходить лікування",
        PatientStatus.Discharged      => "виписаний",
        PatientStatus.Critical        => "критичний стан",
        _                             => "невідомий статус"
    };
    Console.WriteLine($"{patientName}: {label}");
}

PrintStatus("Іван Петренко",   PatientStatus.Admitted);
PrintStatus("Марія Сидоренко", PatientStatus.UnderTreatment);
PrintStatus("Олег Бойко",      PatientStatus.Critical);
```

### `02-24-enum.md` — блок #3 (рядок файлу 86)

**Помилки:**
- рядок 5: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

enum WardType { ICU, Surgery, Cardiology, Neurology, General }

void DescribeWard(WardType ward)
{
    switch (ward)
    {
        case WardType.ICU:
            Console.WriteLine("Інтенсивна терапія: цілодобовий моніторинг");
            break;
        case WardType.Surgery:
            Console.WriteLine("Хірургія: операційні, реанімація");
            break;
        case WardType.Cardiology:
            Console.WriteLine("Кардіологія: ЕКГ, ехокардіографія");
            break;
        case WardType.Neurology:
            Console.WriteLine("Неврологія: МРТ, ЕЕГ");
            break;
        case WardType.General:
            Console.WriteLine("Загальна палата: стандартне лікування");
            break;
    }
}

DescribeWard(WardType.ICU);
DescribeWard(WardType.Cardiology);
DescribeWard(WardType.General);
```

### `02-24-enum.md` — блок #4 (рядок файлу 128)

**Помилки:**
- рядок 15: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

enum BloodType : byte   // byte: 0–255, економить пам'ять
{
    O_Positive,   // 0
    O_Negative,   // 1
    A_Positive,   // 2
    A_Negative,   // 3
    B_Positive,   // 4
    B_Negative,   // 5
    AB_Positive,  // 6
    AB_Negative   // 7
}

BloodType blood = BloodType.A_Positive;
Console.WriteLine($"Група крові: {blood.ToString()}");
Console.WriteLine($"Код: {((byte)blood).ToString()}");
```

### `02-24-enum.md` — блок #5 (рядок файлу 154)

**Помилки:**
- рядок 11: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

enum PriorityLevel
{
    Low    = 1,
    Medium = 2,
    High   = 5,
    Critical = 10
}

void HandleRequest(string patientName, PriorityLevel priority)
{
    Console.WriteLine($"{patientName}: пріоритет {((int)priority).ToString()} ({priority.ToString()})");
    if ((int)priority >= (int)PriorityLevel.High)
        Console.WriteLine("  → Негайне втручання!");
}

HandleRequest("Іван Петренко",   PriorityLevel.Low);
HandleRequest("Марія Сидоренко", PriorityLevel.High);
HandleRequest("Олег Бойко",      PriorityLevel.Critical);
```

### `06-01-delehaty.md` — блок #15 (рядок файлу 471)

**Помилки:**
- рядок 38: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

// Оголошуємо делегат — тип для обробника подій
public delegate void PatientHandler(string message);

public class Patient
{
    int _balance;
    // Змінна делегата — зберігає посилання на обробник
    PatientHandler? _onSpend;

    public Patient(int balance) => _balance = balance;

    // Метод для реєстрації обробника
    public void RegisterHandler(PatientHandler handler)
    {
        _onSpend = handler;
    }

    public void AddFunds(int amount) => _balance += amount;

    public void Spend(int amount)
    {
        if (_balance >= amount)
        {
            _balance -= amount;
            // Викликаємо делегат — що саме відбудеться, вирішить зовнішній код
            _onSpend?.Invoke($"Списано {amount.ToString()} грн. Залишок: {_balance.ToString()} грн.");
        }
        else
        {
            _onSpend?.Invoke($"Недостатньо коштів. Баланс: {_balance.ToString()} грн.");
        }
    }
}

// Створюємо пацієнта зі страховим рахунком
Patient patient = new Patient(500);
// Передаємо обробник — консольний вивід
patient.RegisterHandler(PrintMessage);
// Двічі намагаємось списати кошти
patient.Spend(200);
patient.Spend(400);

void PrintMessage(string message) => Console.WriteLine(message);
```

### `06-01-delehaty.md` — блок #16 (рядок файлу 542)

**Помилки:**
- рядок 40: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

public delegate void PatientHandler(string message);

public class Patient
{
    int _balance;
    PatientHandler? _onSpend;

    public Patient(int balance) => _balance = balance;

    // Реєструємо обробник — додаємо до списку
    public void RegisterHandler(PatientHandler handler)
    {
        _onSpend += handler;
    }

    // Скасування реєстрації обробника — видаляємо зі списку
    public void UnregisterHandler(PatientHandler handler)
    {
        _onSpend -= handler;
    }

    public void AddFunds(int amount) => _balance += amount;

    public void Spend(int amount)
    {
        if (_balance >= amount)
        {
            _balance -= amount;
            _onSpend?.Invoke($"Списано {amount.ToString()} грн. Залишок: {_balance.ToString()} грн.");
        }
        else
        {
            _onSpend?.Invoke($"Недостатньо коштів. Баланс: {_balance.ToString()} грн.");
        }
    }
}

Patient patient = new Patient(500);

// Реєструємо два обробники
patient.RegisterHandler(PrintSimpleMessage);
patient.RegisterHandler(PrintHighlightedMessage);

patient.Spend(200);
patient.Spend(400);

// Видаляємо другий обробник
patient.UnregisterHandler(PrintHighlightedMessage);
// Тепер спрацьовує лише перший
patient.Spend(100);

void PrintSimpleMessage(string message) => Console.WriteLine(message);
void PrintHighlightedMessage(string message)
{
    Console.WriteLine($"*** {message} ***");
}
```

### `06-02-liambdy.md` — блок #9 (рядок файлу 147)

**Помилки:**
- рядок 7: Cannot implicitly convert type 'System.Action' to 'AlertChain'
- рядок 8: Cannot implicitly convert type 'System.Action' to 'AlertChain'
- рядок 9: Cannot implicitly convert type 'System.Action' to 'AlertChain'
- рядок 13: Cannot implicitly convert type 'System.Action' to 'AlertChain'

**Код:**
```csharp
using System;

var logAlert = () => Console.WriteLine("[LOG] Сигнал тривоги");
var notifyDoc = () => Console.WriteLine("[DR] Виклик лікаря");
var sendSMS = () => Console.WriteLine("[SMS] Повідомлення відправлено");

AlertChain alert = logAlert;
alert += notifyDoc;
alert += sendSMS;
alert();

Console.WriteLine("--- видаляємо SMS ---");
alert -= sendSMS;
alert?.Invoke();

delegate void AlertChain();
```

### `06-03-podii.md` — блок #1 (рядок файлу 77)

**Помилки:**
- рядок 33: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Patient
{
    public delegate void PatientHandler(string message);
    public event PatientHandler? Notify;        // 1. Визначення події

    public string Name { get; }
    public int Balance { get; private set; }

    public Patient(string name, int balance) { Name = name; Balance = balance; }

    public void AddFunds(int amount)
    {
        Balance += amount;
        Notify?.Invoke($"На рахунок {Name} зараховано: {amount.ToString()} грн.");  // 2. Виклик
    }

    public void Spend(int amount)
    {
        if (Balance >= amount)
        {
            Balance -= amount;
            Notify?.Invoke($"З рахунку {Name} списано: {amount.ToString()} грн.");  // 3. Виклик
        }
        else
        {
            Notify?.Invoke($"Недостатньо коштів. Баланс {Name}: {Balance.ToString()} грн.");
        }
    }
}

Patient p = new Patient("Іван Петренко", 500);
// обробник ще не встановлено — виклики події не дають ефекту
p.AddFunds(100);
p.Spend(200);
Console.WriteLine($"Баланс: {p.Balance.ToString()} грн.");
```

### `06-03-podii.md` — блок #2 (рядок файлу 123)

**Помилки:**
- рядок 29: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Patient
{
    public delegate void PatientHandler(string message);
    public event PatientHandler? Notify;
    public string Name { get; }
    public int Balance { get; private set; }
    public Patient(string name, int balance) { Name = name; Balance = balance; }
    public void AddFunds(int amount)
    {
        Balance += amount;
        Notify?.Invoke($"На рахунок {Name} зараховано: {amount.ToString()} грн.");
    }
    public void Spend(int amount)
    {
        if (Balance >= amount)
        {
            Balance -= amount;
            Notify?.Invoke($"З рахунку {Name} списано: {amount.ToString()} грн.");
        }
        else
        {
            Notify?.Invoke($"Недостатньо коштів. Баланс {Name}: {Balance.ToString()} грн.");
        }
    }
}

Patient p = new Patient("Марія Коваль", 500);
p.Notify += DisplayMessage;         // підписуємось на подію

p.AddFunds(200);
Console.WriteLine($"Баланс: {p.Balance.ToString()} грн.");
p.Spend(300);
Console.WriteLine($"Баланс: {p.Balance.ToString()} грн.");
p.Spend(600);
Console.WriteLine($"Баланс: {p.Balance.ToString()} грн.");

void DisplayMessage(string message) => Console.WriteLine(message);
```

### `06-03-podii.md` — блок #3 (рядок файлу 173)

**Помилки:**
- рядок 29: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Patient
{
    public delegate void PatientHandler(string message);
    public event PatientHandler? Notify;
    public string Name { get; }
    public int Balance { get; private set; }
    public Patient(string name, int balance) { Name = name; Balance = balance; }
    public void AddFunds(int amount)
    {
        Balance += amount;
        Notify?.Invoke($"На рахунок {Name} зараховано: {amount.ToString()} грн.");
    }
    public void Spend(int amount)
    {
        if (Balance >= amount)
        {
            Balance -= amount;
            Notify?.Invoke($"З рахунку {Name} списано: {amount.ToString()} грн.");
        }
        else
        {
            Notify?.Invoke($"Недостатньо коштів. Баланс: {Balance.ToString()} грн.");
        }
    }
}

Patient p = new Patient("Олег Бойко", 800);

p.Notify += DisplayMessage;         // реєструємо перший обробник
p.Notify += DisplayWarningMessage;  // реєструємо другий

p.AddFunds(100);                    // спрацюють обидва
Console.WriteLine("---");
p.Notify -= DisplayWarningMessage;  // видаляємо другий
p.Spend(300);                       // спрацює лише перший

void DisplayMessage(string message) => Console.WriteLine(message);
void DisplayWarningMessage(string message)
{
    Console.ForegroundColor = ConsoleColor.Yellow;
    Console.WriteLine($"[!] {message}");
    Console.ResetColor();
}
```

### `06-03-podii.md` — блок #4 (рядок файлу 223)

**Помилки:**
- рядок 17: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Patient
{
    public delegate void PatientHandler(string message);
    public event PatientHandler? Notify;
    public string Name { get; }
    public int Balance { get; private set; }
    public Patient(string name, int balance) { Name = name; Balance = balance; }
    public void Spend(int amount)
    {
        if (Balance >= amount) { Balance -= amount; Notify?.Invoke($"Списано: {amount.ToString()} грн."); }
        else Notify?.Invoke($"Недостатньо коштів. Баланс: {Balance.ToString()} грн.");
    }
}

Patient p = new Patient("Тетяна Руденко", 500);

// обробник через делегат
p.Notify += new Patient.PatientHandler(msg => Console.WriteLine($"[ДЕЛЕГАТ] {msg}"));
// обробник через анонімний метод
p.Notify += delegate(string msg) { Console.WriteLine($"[АНОНІМНИЙ] {msg}"); };
// обробник через лямбду
p.Notify += msg => Console.WriteLine($"[ЛЯМБДА] {msg}");

p.Spend(200);
```

### `06-03-podii.md` — блок #5 (рядок файлу 256)

**Помилки:**
- рядок 41: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Patient
{
    public delegate void PatientHandler(string message);

    PatientHandler? _notify;        // приватна змінна делегата

    public event PatientHandler Notify
    {
        add
        {
            _notify += value;
            Console.WriteLine($"[ПІДПИСКА] Обробник '{value.Method.Name}' зареєстровано");
        }
        remove
        {
            _notify -= value;
            Console.WriteLine($"[ВІДПИСКА] Обробник '{value.Method.Name}' видалено");
        }
    }

    public string Name { get; }
    public int Balance { get; private set; }
    public Patient(string name, int balance) { Name = name; Balance = balance; }

    public void Spend(int amount)
    {
        if (Balance >= amount)
        {
            Balance -= amount;
            _notify?.Invoke($"З рахунку {Name} списано: {amount.ToString()} грн.");
        }
        else
        {
            _notify?.Invoke($"Недостатньо коштів. Баланс: {Balance.ToString()} грн.");
        }
    }
}

Patient p = new Patient("Василь Мороз", 600);

p.Notify += DisplayMessage;
p.Spend(100);
p.Notify -= DisplayMessage;
p.Spend(50);

void DisplayMessage(string message) => Console.WriteLine(message);
```

### `06-03-podii.md` — блок #6 (рядок файлу 315)

**Помилки:**
- рядок 44: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class PatientEventArgs
{
    public string Message { get; }
    public int Amount { get; }
    public PatientEventArgs(string message, int amount)
    {
        Message = message;
        Amount  = amount;
    }
}

class Patient
{
    public delegate void PatientHandler(Patient sender, PatientEventArgs e);
    public event PatientHandler? Notify;

    public string Name { get; }
    public int Balance { get; private set; }

    public Patient(string name, int balance) { Name = name; Balance = balance; }

    public void AddFunds(int amount)
    {
        Balance += amount;
        Notify?.Invoke(this, new PatientEventArgs($"На рахунок зараховано {amount.ToString()} грн.", amount));
    }

    public void Spend(int amount)
    {
        if (Balance >= amount)
        {
            Balance -= amount;
            Notify?.Invoke(this, new PatientEventArgs($"Списано {amount.ToString()} грн. зі страхового рахунку", amount));
        }
        else
        {
            Notify?.Invoke(this, new PatientEventArgs("Недостатньо коштів на страховому рахунку", amount));
        }
    }
}

Patient p = new Patient("Надія Литвин", 700);
p.Notify += DisplayTransactionInfo;

p.AddFunds(150);
p.Spend(400);
p.Spend(600);

void DisplayTransactionInfo(Patient sender, PatientEventArgs e)
{
    Console.WriteLine($"Пацієнт: {sender.Name}");
    Console.WriteLine($"Операція: {e.Message}");
    Console.WriteLine($"Сума: {e.Amount.ToString()} грн. | Поточний баланс: {sender.Balance.ToString()} грн.");
    Console.WriteLine("---");
}
```

### `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` — блок #1 (рядок файлу 20)

**Помилки:**
- рядок 23: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}

class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}

class SmsNotification : Notification
{
    public SmsNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"SMS: {Text}");
}

// просто перевіряємо ієрархію
Notification n = new EmailNotification("Результати аналізів готові");
n.Print();
n = new SmsNotification("Прийом завтра о 10:00");
n.Print();
```

### `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` — блок #2 (рядок файлу 55)

**Помилки:**
- рядок 19: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}
class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}

// делегат повертає базовий тип Notification
delegate Notification NotificationBuilder(string text);

// метод повертає похідний тип EmailNotification — коваріантність
NotificationBuilder builder = CreateEmail;

Notification result = builder("Аналізи пацієнта Петренка готові");
result.Print(); // Email: ...

EmailNotification CreateEmail(string text) => new EmailNotification(text);
```

### `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` — блок #3 (рядок файлу 88)

**Помилки:**
- рядок 19: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}
class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}

// делегат приймає похідний тип EmailNotification
delegate void EmailReceiver(EmailNotification notification);

// метод приймає базовий тип Notification — контраваріантність
EmailReceiver receiver = ProcessNotification;
receiver(new EmailNotification("Прийом лікаря підтверджено"));

void ProcessNotification(Notification n) => n.Print();
```

### `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` — блок #4 (рядок файлу 125)

**Помилки:**
- рядок 18: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}
class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}

delegate T NotificationBuilder<out T>(string text);

// повертає EmailNotification — більш конкретний тип
NotificationBuilder<EmailNotification> emailBuilder = text => new EmailNotification(text);

// завдяки out — можна присвоїти делегату з базовим типом
NotificationBuilder<Notification> generalBuilder = emailBuilder; // коваріантність

Notification n = generalBuilder("Результати МРТ");
n.Print(); // Email: Результати МРТ
```

### `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` — блок #5 (рядок файлу 158)

**Помилки:**
- рядок 18: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}
class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}

delegate void NotificationReceiver<in T>(T notification);

// приймає базовий тип Notification
NotificationReceiver<Notification> generalReceiver = n => n.Print();

// завдяки in — можна присвоїти делегату з похідним типом
NotificationReceiver<EmailNotification> emailReceiver = generalReceiver; // контраваріантність

generalReceiver(new Notification("Загальне повідомлення"));     // Сповіщення: ...
generalReceiver(new EmailNotification("Результати аналізів"));  // Email: ...
emailReceiver(new EmailNotification("Прийом підтверджено"));    // Email: ...
```

### `06-04-kovariantnist-ta-kontravariantnist-delehativ.md` — блок #6 (рядок файлу 192)

**Помилки:**
- рядок 24: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Notification
{
    public string Text { get; }
    public Notification(string text) => Text = text;
    public virtual void Print() => Console.WriteLine($"Сповіщення: {Text}");
}
class EmailNotification : Notification
{
    public EmailNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"Email: {Text}");
}
class SmsNotification : Notification
{
    public SmsNotification(string text) : base(text) { }
    public override void Print() => Console.WriteLine($"SMS: {Text}");
}

// конвертер: приймає тип M, повертає тип E
delegate E NotificationConverter<in M, out E>(M source);

// конвертер: з будь-якого Notification створює EmailNotification
NotificationConverter<Notification, EmailNotification> toEmail =
    n => new EmailNotification($"[Email] {n.Text}");

// контраваріантність по M: SmsNotification → Notification (ширший тип)
// коваріантність по E:     EmailNotification → Notification (ширший тип)
NotificationConverter<SmsNotification, Notification> converter = toEmail;

Notification result = converter(new SmsNotification("Аналіз крові"));
result.Print(); // Email: [Email] Аналіз крові
```

### `07-01-vyznachennia-interfeisiv.md` — блок #2 (рядок файлу 105)

**Помилки:**
- рядок 22: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

interface IDiagnosable
{
    void RunDiagnostics();
    // реалізація методу за замовчуванням
    void LogDiagnostics()
    {
        Console.WriteLine("[LOG] Діагностика завершена — результат записано");
    }
}

class Patient : IDiagnosable
{
    public string Name { get; }
    public Patient(string name) => Name = name;
    public void RunDiagnostics() =>
        Console.WriteLine($"Діагностика пацієнта {Name}");
    // LogDiagnostics не перевизначаємо — використовується default
}

IDiagnosable p = new Patient("Марія Коваль");
p.RunDiagnostics();
p.LogDiagnostics();
```

### `07-01-vyznachennia-interfeisiv.md` — блок #3 (рядок файлу 134)

**Помилки:**
- рядок 17: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

interface IDiagnosable
{
    void RunDiagnostics() => Console.WriteLine("Стандартна діагностика");
    // властивість тільки для читання з реалізацією за замовчуванням
    int DefaultSeverity { get { return 1; } }
}

class LabSample : IDiagnosable
{
    public string SampleId { get; }
    public LabSample(string id) => SampleId = id;
    // RunDiagnostics і DefaultSeverity — використовуємо default
}

IDiagnosable sample = new LabSample("LAB-2024-001");
sample.RunDiagnostics();
Console.WriteLine($"Рівень тяжкості за замовчуванням: {sample.DefaultSeverity.ToString()}");
```

### `07-02-zastosuvannia-interfeisiv.md` — блок #1 (рядок файлу 34)

**Помилки:**
- рядок 23: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

// реалізація інтерфейсу в класі
class Patient : IDiagnosable
{
    public string Name { get; }
    public Patient(string name) => Name = name;

    public void RunDiagnostics()
        => Console.WriteLine($"Діагностика пацієнта {Name} розпочата");
}

// реалізація інтерфейсу в структурі
struct LabSample : IDiagnosable
{
    public string SampleId { get; }
    public LabSample(string id) => SampleId = id;

    public void RunDiagnostics()
        => Console.WriteLine($"Аналіз зразка {SampleId} виконано");
}

Patient p      = new Patient("Марія Коваль");
LabSample s    = new LabSample("LAB-2024-099");
p.RunDiagnostics();
s.RunDiagnostics();

interface IDiagnosable
{
    void RunDiagnostics();
}
```

### `07-03-yavna-realizatsiia-interfeisiv.md` — блок #1 (рядок файлу 19)

**Помилки:**
- рядок 14: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Patient : IDiagnosable
{
    public string Name { get; }
    public Patient(string name) => Name = name;

    // явна реалізація — без public, з префіксом інтерфейсу
    void IDiagnosable.RunDiagnostics()
        => Console.WriteLine($"[IDiagnosable] Діагностика пацієнта {Name}");
}

// доступ ТІЛЬКИ через змінну інтерфейсу
IDiagnosable p = new Patient("Марія Коваль");
p.RunDiagnostics();

interface IDiagnosable
{
    void RunDiagnostics();
}
```

### `07-03-yavna-realizatsiia-interfeisiv.md` — блок #3 (рядок файлу 89)

**Помилки:**
- рядок 13: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

// без явної реалізації — один спільний метод
class Patient : IDiagnosable, ITreatment
{
    public string Name { get; }
    public Patient(string name) => Name = name;

    public void RunProcedure()
        => Console.WriteLine($"{Name}: загальна процедура (однакова для обох інтерфейсів)");
}

Patient p = new Patient("Василь Мороз");
((IDiagnosable)p).RunProcedure();  // загальна процедура
((ITreatment)p).RunProcedure();    // загальна процедура — той самий метод

interface IDiagnosable { void RunProcedure(); }
interface ITreatment   { void RunProcedure(); }
```

### `07-03-yavna-realizatsiia-interfeisiv.md` — блок #4 (рядок файлу 112)

**Помилки:**
- рядок 15: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class Patient : IDiagnosable, ITreatment
{
    public string Name { get; }
    public Patient(string name) => Name = name;

    void IDiagnosable.RunProcedure()
        => Console.WriteLine($"{Name}: діагностична процедура — МРТ, аналізи");

    void ITreatment.RunProcedure()
        => Console.WriteLine($"{Name}: лікувальна процедура — ін'єкція, крапельниця");
}

Patient p = new Patient("Тетяна Руденко");
((IDiagnosable)p).RunProcedure();
((ITreatment)p).RunProcedure();

interface IDiagnosable { void RunProcedure(); }
interface ITreatment   { void RunProcedure(); }
```

### `07-03-yavna-realizatsiia-interfeisiv.md` — блок #6 (рядок файлу 192)

**Помилки:**
- рядок 31: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

interface IDiagnosable
{
    void RunDiagnostics();
}

// абстрактний клас реалізує інтерфейс, але відкладає реалізацію
abstract class MedicalRecord : IDiagnosable
{
    public string PatientName { get; }
    protected MedicalRecord(string name) => PatientName = name;

    public abstract void RunDiagnostics(); // нехай похідні класи вирішують
}

class ClinicalRecord : MedicalRecord
{
    public ClinicalRecord(string name) : base(name) { }
    public override void RunDiagnostics()
        => Console.WriteLine($"{PatientName}: клінічний огляд — анамнез, симптоми");
}

class LabRecord : MedicalRecord
{
    public LabRecord(string name) : base(name) { }
    public override void RunDiagnostics()
        => Console.WriteLine($"{PatientName}: лабораторна діагностика — кров, сеча, біопсія");
}

IDiagnosable r1 = new ClinicalRecord("Олег Бойко");
IDiagnosable r2 = new LabRecord("Марина Шевченко");
r1.RunDiagnostics();
r2.RunDiagnostics();
```

### `07-03-yavna-realizatsiia-interfeisiv.md` — блок #7 (рядок файлу 231)

**Помилки:**
- рядок 18: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

interface IDiagnosable
{
    void RunDiagnostics();
}

class BaseRecord
{
    // публічний метод — компілятор підхопить його як реалізацію IDiagnosable
    public void RunDiagnostics()
        => Console.WriteLine("BaseRecord: стандартна діагностика");
}

// HeroRecord успадковує метод і реалізує IDiagnosable через нього
class SpecialRecord : BaseRecord, IDiagnosable { }

IDiagnosable sr = new SpecialRecord();
sr.RunDiagnostics(); // викликається метод з BaseRecord

```

### `07-03-yavna-realizatsiia-interfeisiv.md` — блок #8 (рядок файлу 268)

**Помилки:**
- рядок 17: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

interface IDiagnosable { void RunDiagnostics(); }

class BaseRecord : IDiagnosable
{
    public virtual void RunDiagnostics()
        => Console.WriteLine("BaseRecord: стандартна діагностика");
}

class SpecialRecord : BaseRecord
{
    public override void RunDiagnostics()
        => Console.WriteLine("SpecialRecord: розширена діагностика");
}

BaseRecord  r1 = new SpecialRecord();
IDiagnosable r2 = new SpecialRecord();
SpecialRecord r3 = new SpecialRecord();

r1.RunDiagnostics(); // SpecialRecord — поліморфізм
r2.RunDiagnostics(); // SpecialRecord — поліморфізм
r3.RunDiagnostics(); // SpecialRecord
```

### `07-03-yavna-realizatsiia-interfeisiv.md` — блок #9 (рядок файлу 298)

**Помилки:**
- рядок 17: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

interface IDiagnosable { void RunDiagnostics(); }

class BaseRecord : IDiagnosable
{
    public void RunDiagnostics()
        => Console.WriteLine("BaseRecord: стандартна діагностика");
}

class SpecialRecord : BaseRecord
{
    public new void RunDiagnostics()
        => Console.WriteLine("SpecialRecord: спеціальна діагностика");
}

BaseRecord   r1 = new SpecialRecord();
IDiagnosable r2 = new SpecialRecord();
SpecialRecord r3 = new SpecialRecord();

r1.RunDiagnostics(); // BaseRecord — раннє зв'язування
r2.RunDiagnostics(); // BaseRecord — інтерфейс реалізований у BaseRecord
r3.RunDiagnostics(); // SpecialRecord — прямий тип
```

### `07-03-yavna-realizatsiia-interfeisiv.md` — блок #10 (рядок файлу 328)

**Помилки:**
- рядок 18: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

interface IDiagnosable { void RunDiagnostics(); }

class BaseRecord : IDiagnosable
{
    public void RunDiagnostics()
        => Console.WriteLine("BaseRecord: стандартна діагностика");
}

// повторна реалізація — IDiagnosable вказаний явно у SpecialRecord
class SpecialRecord : BaseRecord, IDiagnosable
{
    public new void RunDiagnostics()
        => Console.WriteLine("SpecialRecord: спеціальна діагностика");
}

BaseRecord   r1 = new SpecialRecord();
IDiagnosable r2 = new SpecialRecord();
SpecialRecord r3 = new SpecialRecord();

r1.RunDiagnostics(); // BaseRecord — раннє зв'язування за типом змінної
r2.RunDiagnostics(); // SpecialRecord — інтерфейс тепер прив'язаний до SpecialRecord
r3.RunDiagnostics(); // SpecialRecord
```

### `07-03-yavna-realizatsiia-interfeisiv.md` — блок #11 (рядок файлу 359)

**Помилки:**
- рядок 21: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

interface IDiagnosable { void RunDiagnostics(); }

class BaseRecord : IDiagnosable
{
    public void RunDiagnostics()
        => Console.WriteLine("BaseRecord: стандартна діагностика");
}

class SpecialRecord : BaseRecord, IDiagnosable
{
    public new void RunDiagnostics()
        => Console.WriteLine("SpecialRecord: спеціальна діагностика");

    // явна реалізація — виключно для змінної типу IDiagnosable
    void IDiagnosable.RunDiagnostics()
        => Console.WriteLine("SpecialRecord (явна IDiagnosable): протокол діагностики");
}

BaseRecord   r1 = new SpecialRecord();
IDiagnosable r2 = new SpecialRecord();
SpecialRecord r3 = new SpecialRecord();

r1.RunDiagnostics(); // BaseRecord — раннє зв'язування
r2.RunDiagnostics(); // явна IDiagnosable — найвищий пріоритет
r3.RunDiagnostics(); // SpecialRecord — новий public метод
```

### `07-06-kopiiuvannia-obiektiv-interfeis-icloneable.md` — блок #6 (рядок файлу 292)

**Помилки:**
- рядок 18: The type or namespace name 'IComparer<>' could not be found (are you missing a using directive or an assembly reference?)
- рядок 29: The type or namespace name 'IComparer<>' could not be found (are you missing a using directive or an assembly reference?)
- рядок 51: Argument 2: cannot convert from 'PatientAgeComparer' to 'System.Array?'
- рядок 58: Argument 2: cannot convert from 'PatientNameComparer' to 'System.Array?'

**Код:**
```csharp
using System;

class Patient
{
    public string LastName { get; }
    public int Age { get; }

    public Patient(string lastName, int age)
    {
        LastName = lastName;
        Age = age;
    }

    public override string ToString() => $"{LastName}, {Age.ToString()} р.";
}

// Компаратор за віком (від молодшого до старшого)
class PatientAgeComparer : IComparer<Patient>
{
    public int Compare(Patient? x, Patient? y)
    {
        if (x is null || y is null)
            throw new ArgumentException("Некоректне значення параметра");
        return x.Age.CompareTo(y.Age);
    }
}

// Компаратор за прізвищем
class PatientNameComparer : IComparer<Patient>
{
    public int Compare(Patient? x, Patient? y)
    {
        if (x is null || y is null)
            throw new ArgumentException("Некоректне значення параметра");
        return x.LastName.CompareTo(y.LastName);
    }
}

class Program
{
    static void Main()
    {
        Patient[] patients =
        {
            new Patient("Шевченко", 34),
            new Patient("Іваненко", 52),
            new Patient("Бойко",    28),
            new Patient("Ковальчук",41),
        };

        Array.Sort(patients, new PatientAgeComparer());
        Console.WriteLine("За віком:");
        foreach (Patient p in patients)
            Console.WriteLine($"  {p.ToString()}");

        Console.WriteLine();

        Array.Sort(patients, new PatientNameComparer());
        Console.WriteLine("За прізвищем:");
        foreach (Patient p in patients)
            Console.WriteLine($"  {p.ToString()}");
    }
}
```

### `08-09-kortezhi.md` — блок #1 (рядок файлу 79)

**Помилки:**
- рядок 18: Identifier expected
- рядок 18: { expected
- рядок 18: } expected
- рядок 18: Type or namespace definition, or end-of-file expected
- рядок 18: Top-level statements must precede namespace and type declarations.
- рядок 18: The name 'Room' does not exist in the current context

**Код:**
```csharp
using System;

// Виконуваний код
// Явний кортеж
(string Name, int Age, double Temp) patient = ("Іван Петренко", 45, 38.2);
Console.WriteLine($"Пацієнт: {patient.Name}, вік: {patient.Age}, t°: {patient.Temp}");

// Декомпозиція
var (name, age, temp) = patient;
Console.WriteLine($"Після декомпозиції: {name}, {age} р., {temp}°C");

// Discard: нас цікавить лише ім'я
var (patientName, _, _) = patient;
Console.WriteLine($"Ім'я: {patientName}");

// Мутабельність — на відміну від анонімних типів
var record = (Diagnosis: "Гіпертонія", Room: 7);
record.Room = 12; // можна змінити
Console.WriteLine($"Діагноз: {record.Diagnosis}, палата: {record.Room}");

// Обмін значеннями через кортеж
string doctorA = "Олег Петренко";
string doctorB = "Марія Іванова";
(doctorA, doctorB) = (doctorB, doctorA);
Console.WriteLine($"Після ротації: {doctorA}, {doctorB}");
```

### `09-05-reliatsiinyi-ta-lohichnyi-paterny.md` — блок #2 (рядок файлу 93)

**Помилки:**
- рядок 22: The pattern is unreachable. It has already been handled by a previous arm of the switch expression or it is impossible to match.
- рядок 29: The pattern is unreachable. It has already been handled by a previous arm of the switch expression or it is impossible to match.

**Код:**
```csharp
using System;

// Виконуваний код
// Комплексна оцінка стану пацієнта
int[] pulseReadings = { 45, 60, 82, 105, 130 };
int[] systolicValues = { 85, 110, 135, 160, 195 };

Console.WriteLine("--- Оцінка пульсу ---");
foreach (var p in pulseReadings)
    Console.WriteLine($"  {p} уд/хв → {AssessPulse(p)}");

Console.WriteLine("--- Оцінка тиску ---");
foreach (var s in systolicValues)
    Console.WriteLine($"  {s} мм рт.ст. → {AssessPressure(s)}");

string AssessPulse(int pulse) => pulse switch
{
    // not + range
    not (>= 60 and <= 100) when pulse < 60 => "Брадикардія",
    not (>= 60 and <= 100)                  => "Тахікардія",
    >= 60 and <= 100                         => "Норма",
    _                                        => "Невизначено"
};

string AssessPressure(int systolic) => systolic switch
{
    // or: критичні значення з двох боків
    < 90 or > 180   => "КРИТИЧНО",
    < 90            => "Гіпотонія",
    >= 90 and < 120 => "Норма",
    >= 120 and < 140=> "Підвищений",
    >= 140 and < 180=> "Гіпертонія",
    _               => "Невизначено"
};
```

### `13-01-vidkladena-initsializatsiia-ta-typ-lazy.md` — блок #1 (рядок файлу 158)

**Помилки:**
- рядок 33: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class PatientRecord
{
    public string Name { get; }
    public string IcdCode { get; }

    // Анамнез — важкий об'єкт, завантажується лише при потребі
    private Lazy<string[]> _history;

    public PatientRecord(string name, string icd)
    {
        Name    = name;
        IcdCode = icd;
        // Фабрика захоплює Name через замикання
        _history = new Lazy<string[]>(() => LoadHistory(name));
    }

    private static string[] LoadHistory(string name)
    {
        Console.WriteLine($"  [ЗАВАНТАЖЕННЯ анамнезу: {name}]");
        return new[] {
            $"2024-01 — первинний огляд",
            $"2024-06 — призначення лікування",
            $"2026-06 — плановий контроль",
        };
    }

    public bool IsHistoryLoaded => _history.IsValueCreated;
    public string[] History => _history.Value; // тригер
}

var p1 = new PatientRecord("Петренко Іван", "I10.9");
var p2 = new PatientRecord("Коваль Марія",  "J45.0");

Console.WriteLine("=== Списку пацієнтів ===");
Console.WriteLine($"{p1.Name} | {p1.IcdCode} | Анамнез завантажено: {p1.IsHistoryLoaded}");
Console.WriteLine($"{p2.Name} | {p2.IcdCode} | Анамнез завантажено: {p2.IsHistoryLoaded}");

Console.WriteLine("\n=== Лікар відкриває картку Петренка ===");
foreach (var item in p1.History)
    Console.WriteLine($"  • {item}");

Console.WriteLine($"\nПетренко: IsHistoryLoaded = {p1.IsHistoryLoaded}");
Console.WriteLine($"Коваль:   IsHistoryLoaded = {p2.IsHistoryLoaded}");
Console.WriteLine("(Анамнез Коваль так і не завантажено — економія ресурсів)");
```

### `13-01-vidkladena-initsializatsiia-ta-typ-lazy.md` — блок #2 (рядок файлу 211)

**Помилки:**
- рядок 33: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

class LabNormService
{
    // Таблиця норм будується один раз при першому зверненні
    private static readonly Lazy<Dictionary<string, (double Min, double Max, string Unit)>> _norms
        = new Lazy<Dictionary<string, (double, double, string)>>(() =>
        {
            Console.WriteLine("  [ІНІЦІАЛІЗАЦІЯ таблиці норм — відбувається один раз]");
            return new Dictionary<string, (double, double, string)>
            {
                ["glucose"]      = (3.9,  6.1,  "ммоль/л"),
                ["hemoglobin"]   = (120,  160,  "г/л"),
                ["erythrocytes"] = (3.8,  5.2,  "10¹²/л"),
                ["leukocytes"]   = (4.0,  9.0,  "10⁹/л"),
                ["cholesterol"]  = (0,    5.2,  "ммоль/л"),
            };
        });

    public static (bool ok, string msg) Check(string test, double value)
    {
        var norms = _norms.Value; // тригер при першому виклику
        if (!norms.TryGetValue(test, out var norm))
            return (false, $"Невідомий показник: {test}");

        bool ok = value >= norm.Min && value <= norm.Max;
        string status = ok ? "НОРМА" : (value < norm.Min ? "НИЖЧЕ НОРМИ" : "ВИЩЕ НОРМИ");
        return (ok, $"{value:F2} {norm.Unit} [{norm.Min}–{norm.Max}] → {status}");
    }
}

Console.WriteLine("=== Лабораторні показники — Петренко Іван ===");
Console.WriteLine($"IsValueCreated перед першим зверненням: (перевіряємо через Check)");
Console.WriteLine();

var results = new[]
{
    ("glucose",      7.3),
    ("hemoglobin",   135.0),
    ("leukocytes",   11.5),
    ("cholesterol",  4.8),
    ("erythrocytes", 4.2),
};

foreach (var (test, val) in results)
{
    var (ok, msg) = LabNormService.Check(test, val);
    string mark = ok ? "✓" : "!";
    Console.WriteLine($"  [{mark}] {test,-14}: {msg}");
}
```

### `13-04-klas-array.md` — блок #1 (рядок файлу 198)

**Помилки:**
- рядок 12: Top-level statements must precede namespace and type declarations.
- рядок 46: Operator '==' cannot be applied to operands of type 'int' and 'bool'

**Код:**
```csharp
using System;

struct Patient
{
    public string Id;
    public string Name;
    public int    Age;
    public double Bmi;
    public string Icd;
}

var patients = new Patient[]
{
    new Patient { Id="P001", Name="Петренко Іван",   Age=67, Bmi=27.3, Icd="I10.9" },
    new Patient { Id="P002", Name="Коваль Марія",    Age=45, Bmi=23.1, Icd="J45.0" },
    new Patient { Id="P003", Name="Сидоренко Олег",  Age=52, Bmi=31.8, Icd="E11.9" },
    new Patient { Id="P004", Name="Бойко Тетяна",    Age=71, Bmi=19.4, Icd="I10.9" },
    new Patient { Id="P005", Name="Мороз Василь",    Age=38, Bmi=25.6, Icd="J45.0" },
};

Console.WriteLine("=== Сортування за віком (спадно) ===");
Array.Sort(patients, (a, b) => b.Age.CompareTo(a.Age));
Console.WriteLine($"{"ID",-6} {"Пацієнт",-22} {"Вік",4} {"ІМТ",6}  ICD");
Console.WriteLine(new string('-', 48));
foreach (var p in patients)
    Console.WriteLine($"{p.Id,-6} {p.Name,-22} {p.Age,4} {p.Bmi,6:F1}  {p.Icd}");

Console.WriteLine("\n=== Сортування за ІМТ (зростаючи) ===");
Array.Sort(patients, (a, b) => a.Bmi.CompareTo(b.Bmi));
foreach (var p in patients)
    Console.WriteLine($"{p.Id,-6} {p.Name,-22} ІМТ={p.Bmi:F1}");

Console.WriteLine("\n=== Пошук: FindAll за діагнозом I10.9 ===");
var hypertensive = Array.FindAll(patients, p => p.Icd == "I10.9");
Console.WriteLine($"Гіпертонія (I10.9): {hypertensive.Length} пацієнтів");
foreach (var p in hypertensive)
    Console.WriteLine($"  {p.Name}, {p.Age} р.");

Console.WriteLine("\n=== Exists / TrueForAll ===");
bool hasObesity  = Array.Exists(patients, p => p.Bmi >= 30);
bool allAdults   = Array.TrueForAll(patients, p => p.Age >= 18);
Console.WriteLine($"Є ожиріння (ІМТ≥30): {hasObesity}");
Console.WriteLine($"Усі повнолітні:       {allAdults}");

Console.WriteLine("\n=== Find + FindIndex ===");
var oldest = Array.Find(patients, p => p.Age == Array.FindIndex(patients, x => x.Age >= 70) >= 0
    ? patients[Array.FindIndex(patients, x => x.Age >= 70)].Age : -1);
var firstSenior = Array.Find(patients, p => p.Age >= 65);
int seniorIdx   = Array.FindIndex(patients, p => p.Age >= 65);
Console.WriteLine($"Перший пацієнт 65+: {firstSenior.Name} (індекс {seniorIdx})");
```

### `14-01-vvedennia-u-refleksiiu-klas-system-type.md` — блок #1 (рядок файлу 194)

**Помилки:**
- рядок 21: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Reflection;

class PatientRecord
{
    public string  Id      { get; }
    public string  Name    { get; set; }
    public string  IcdCode { get; set; }
    public int     Age     { get; set; }
    private double _bmi;

    public PatientRecord(string id, string name, string icd, int age)
    {
        Id = id; Name = name; IcdCode = icd; Age = age;
    }

    public string GetSummary()    => $"{Name} ({Age} р.) — {IcdCode}";
    private bool  IsHighRisk()    => IcdCode.StartsWith("I") || IcdCode.StartsWith("C");
}

Type t = typeof(PatientRecord);

Console.WriteLine("=== Загальна інформація ===");
Console.WriteLine($"Name:        {t.Name}");
Console.WriteLine($"FullName:    {t.FullName}");
Console.WriteLine($"Namespace:   {t.Namespace ?? "(global)"}");
Console.WriteLine($"IsClass:     {t.IsClass}");
Console.WriteLine($"IsValueType: {t.IsValueType}");
Console.WriteLine($"IsAbstract:  {t.IsAbstract}");
Console.WriteLine($"BaseType:    {t.BaseType?.Name}");

Console.WriteLine("\n=== Реалізовані інтерфейси ===");
Type[] ifaces = t.GetInterfaces();
Console.WriteLine(ifaces.Length == 0 ? "  (немає)" : string.Join(", ", Array.ConvertAll(ifaces, i => i.Name)));

Console.WriteLine("\n=== 3 способи отримати Type ===");
// 1. typeof
Type t1 = typeof(PatientRecord);
Console.WriteLine($"typeof:     {t1.Name}");

// 2. GetType()
var p = new PatientRecord("P001", "Петренко", "I10.9", 67);
Type t2 = p.GetType();
Console.WriteLine($"GetType():  {t2.Name}");

// 3. Type.GetType з рядка
Type? t3 = Type.GetType("PatientRecord");
Console.WriteLine($"GetType(s): {(t3 != null ? t3.Name : "null (немає namespace)")}");

Console.WriteLine($"\nВсі три однакові: {t1 == t2}");
```

### `14-01-vvedennia-u-refleksiiu-klas-system-type.md` — блок #2 (рядок файлу 249)

**Помилки:**
- рядок 24: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

class MedicalRecord
{
    public string Id { get; }
    public MedicalRecord(string id) => Id = id;
    public virtual string RecordType => "Base";
}

class InpatientRecord : MedicalRecord
{
    public int StayDays { get; }
    public InpatientRecord(string id, int days) : base(id) => StayDays = days;
    public override string RecordType => "Inpatient";
}

class OutpatientRecord : MedicalRecord
{
    public string Clinic { get; }
    public OutpatientRecord(string id, string clinic) : base(id) => Clinic = clinic;
    public override string RecordType => "Outpatient";
}

MedicalRecord[] records = {
    new InpatientRecord("R001", 7),
    new OutpatientRecord("R002", "Кардіологія"),
    new InpatientRecord("R003", 3),
    new OutpatientRecord("R004", "Неврологія"),
};

Console.WriteLine("=== Поліморфне GetType() ===");
Console.WriteLine($"{"ID",-6} {"RecordType",-14} {"ActualType",-20} {"BaseType"}");
Console.WriteLine(new string('-', 58));

foreach (var rec in records)
{
    Type actual = rec.GetType();          // фактичний тип
    Type declared = typeof(MedicalRecord); // тип змінної — завжди MedicalRecord

    Console.WriteLine($"{rec.Id,-6} {rec.RecordType,-14} {actual.Name,-20} {actual.BaseType?.Name}");
}

Console.WriteLine("\n=== IsAssignableFrom — перевірка ієрархії ===");
Type baseType   = typeof(MedicalRecord);
Type inpatient  = typeof(InpatientRecord);
Type outpatient = typeof(OutpatientRecord);

Console.WriteLine($"MedicalRecord.IsAssignableFrom(InpatientRecord):  {baseType.IsAssignableFrom(inpatient)}");
Console.WriteLine($"MedicalRecord.IsAssignableFrom(OutpatientRecord): {baseType.IsAssignableFrom(outpatient)}");
Console.WriteLine($"InpatientRecord.IsAssignableFrom(MedicalRecord):  {inpatient.IsAssignableFrom(baseType)}");

Console.WriteLine("\n=== Підрахунок за типами ===");
int inCount  = 0; int outCount = 0;
foreach (var rec in records)
{
    if (rec.GetType() == typeof(InpatientRecord))  inCount++;
    if (rec.GetType() == typeof(OutpatientRecord)) outCount++;
}
Console.WriteLine($"Стаціонарних: {inCount}, Амбулаторних: {outCount}");
```

### `15-02-stvorennia-potokiv-threadstart.md` — блок #5 (рядок файлу 136)

**Помилки:**
- рядок 19: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Threading;

// Клас-обгортка для передачі кількох значень у потік
class PatientTask
{
    public string Name     { get; }
    public string Ward     { get; }
    public int    Priority { get; }

    public PatientTask(string name, string ward, int priority)
    {
        Name     = name;
        Ward     = ward;
        Priority = priority;
    }
}

Thread t1 = new Thread(ProcessAdmission);
Thread t2 = new Thread(ProcessAdmission);

t1.Name = "Admissions-1";
t2.Name = "Admissions-2";

t1.Start(new PatientTask("Марія Шевченко", "Терапія",    1));
t2.Start(new PatientTask("Олег Бондаренко", "Хірургія",  2));

t1.Join();
t2.Join();

void ProcessAdmission(object? param)
{
    if (param is not PatientTask task) return; // pattern matching — безпечне приведення

    Console.WriteLine($"[{Thread.CurrentThread.Name}] Прийом: {task.Name} → {task.Ward} (пріоритет {task.Priority.ToString()})");
    Thread.Sleep(200);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Завершено: {task.Name} оформлено до відділення '{task.Ward}'");
}
```

### `15-02-stvorennia-potokiv-threadstart.md` — блок #7 (рядок файлу 223)

**Помилки:**
- рядок 21: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Threading;

// Завдання для обробки в окремому потоці
class LabOrder
{
    public int    OrderId    { get; }
    public string PatientName { get; }
    public string TestType   { get; }
    public int    ProcessMs  { get; } // час обробки у мс

    public LabOrder(int id, string name, string test, int ms)
    {
        OrderId     = id;
        PatientName = name;
        TestType    = test;
        ProcessMs   = ms;
    }
}

LabOrder[] orders =
{
    new LabOrder(1, "Коваль М.В.",    "Загальний аналіз крові",   300),
    new LabOrder(2, "Петренко І.О.",  "Біохімія крові",            450),
    new LabOrder(3, "Бойко О.П.",     "Аналіз сечі",              200),
    new LabOrder(4, "Мороз В.К.",     "Коагулограма",             380),
};

Thread[] workers = new Thread[orders.Length];

for (int i = 0; i < orders.Length; i++)
{
    LabOrder order = orders[i]; // захоплюємо копію для замикання
    workers[i] = new Thread(() => ProcessLabOrder(order));
    workers[i].Name = $"Lab-{order.OrderId.ToString()}";
}

Console.WriteLine("=== Лабораторія: запуск паралельної обробки ===");

foreach (Thread w in workers) w.Start();
foreach (Thread w in workers) w.Join();

Console.WriteLine("=== Всі аналізи оброблено. Результати готові до видачі. ===");

void ProcessLabOrder(LabOrder order)
{
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Початок: {order.PatientName} — {order.TestType}");
    Thread.Sleep(order.ProcessMs);
    Console.WriteLine($"[{Thread.CurrentThread.Name}] Готово:  {order.PatientName} — {order.TestType} ({order.ProcessMs.ToString()} мс)");
}
```

### `15-03-synkhronizatsiia-potokiv-lock.md` — блок #3 (рядок файлу 105)

**Помилки:**
- рядок 31: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Threading;

// Розклад лікаря — спільний ресурс для кількох операторів
class AppointmentScheduler
{
    private int _appointmentsToday = 0;
    private readonly int _maxPerDay = 20;
    private readonly object _lock = new object();

    // Повертає true, якщо запис вдався
    public bool TryBook(string operatorName, string patientName)
    {
        lock (_lock) // тільки один оператор одночасно може модифікувати розклад
        {
            if (_appointmentsToday >= _maxPerDay)
            {
                Console.WriteLine($"[{operatorName}] Відмова: {patientName} — розклад повний ({_maxPerDay.ToString()}/{_maxPerDay.ToString()})");
                return false;
            }

            _appointmentsToday++;
            Console.WriteLine($"[{operatorName}] Записано: {patientName} — прийом #{_appointmentsToday.ToString()}");
            return true;
        }
    }

    public int Total => _appointmentsToday;
}

AppointmentScheduler scheduler = new AppointmentScheduler();

// Три оператори паралельно намагаються записати пацієнтів
string[][] operatorPatients =
{
    new[] { "Коваль М.", "Петренко І.", "Бойко О.", "Мороз В.", "Сидоренко Т.",
            "Руденко Н.", "Кравченко Р.", "Гриценко Л.", "Ткаченко А.", "Савченко Д." },
    new[] { "Бондаренко Є.", "Шевченко І.", "Яковенко В.", "Романенко О.", "Захаренко М.",
            "Лисенко Ю.", "Павленко С.", "Олійник В.", "Кириленко Т.", "Денисенко Н." },
    new[] { "Іваненко А.", "Сергієнко К.", "Тимошенко Б.", "Чорновіл Г.", "Гнатенко В." }
};

Thread[] operators = new Thread[3];
for (int i = 0; i < 3; i++)
{
    int idx = i; // копія для замикання
    operators[i] = new Thread(() =>
    {
        string opName = $"Реєстратор-{(idx + 1).ToString()}";
        foreach (string patient in operatorPatients[idx])
        {
            scheduler.TryBook(opName, patient);
            Thread.Sleep(20); // невелика затримка між записами
        }
    });
    operators[i].Name = $"Operator-{(i + 1).ToString()}";
}

foreach (Thread t in operators) t.Start();
foreach (Thread t in operators) t.Join();

Console.WriteLine($"\nПідсумок: записано {scheduler.Total.ToString()} пацієнтів із 20 доступних");
```

### `15-04-klas-monitor.md` — блок #1 (рядок файлу 70)

**Помилки:**
- рядок 53: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.Threading;

// Черга лабораторних зразків — спільний ресурс
class LabQueue
{
    private readonly Queue<string> _samples = new Queue<string>();
    private readonly object _lock = new object();
    private bool _accepting = true; // false = нові зразки більше не надходять

    // Медсестра додає зразок до черги
    public void AddSample(string sample)
    {
        lock (_lock)
        {
            _samples.Enqueue(sample);
            Console.WriteLine($"[Надходження] Зразок '{sample}' додано до черги (черга: {_samples.Count.ToString()})");
            Monitor.Pulse(_lock); // сповіщаємо лаборанта, що є новий зразок
        }
    }

    // Оголошуємо, що нових зразків більше не буде
    public void StopAccepting()
    {
        lock (_lock)
        {
            _accepting = false;
            Monitor.PulseAll(_lock); // розбуджуємо всіх, хто чекає — вони перевірять умову
        }
    }

    // Лаборант бере наступний зразок для обробки
    // Повертає null, якщо черга закрита і порожня
    public string? TakeSample()
    {
        lock (_lock)
        {
            // Очікуємо, поки черга стане непорожньою або прийом не зупинять
            while (_samples.Count == 0 && _accepting)
            {
                Monitor.Wait(_lock); // звільняємо замок і чекаємо
            }

            if (_samples.Count > 0)
                return _samples.Dequeue();

            return null; // черга порожня і прийом зупинено
        }
    }
}

LabQueue queue = new LabQueue();

// Лаборант — споживач (запускаємо першим, він чекатиме на зразки)
Thread labWorker = new Thread(() =>
{
    Console.WriteLine("[Лаборант] Готовий до роботи, очікую зразки...");
    while (true)
    {
        string? sample = queue.TakeSample();
        if (sample == null) break; // черга закрита і порожня — виходимо

        Console.WriteLine($"[Лаборант] Обробляю: '{sample}'");
        Thread.Sleep(150); // час аналізу
        Console.WriteLine($"[Лаборант] Аналіз '{sample}' завершено");
    }
    Console.WriteLine("[Лаборант] Робочий день завершено — всі зразки оброблено");
});
labWorker.Name = "LabWorker";
labWorker.Start();

// Медсестра — виробник
Thread nurse = new Thread(() =>
{
    string[] samples = { "Кров-Коваль", "Сеча-Петренко", "Кров-Бойко", "Мокрота-Мороз", "Кров-Сидоренко" };
    foreach (string sample in samples)
    {
        Thread.Sleep(100); // час між надходженнями зразків
        queue.AddSample(sample);
    }
    Console.WriteLine("[Медсестра] Всі зразки здано до лабораторії");
    queue.StopAccepting(); // сигналізуємо, що нових зразків не буде
});
nurse.Name = "Nurse";
nurse.Start();

nurse.Join();
labWorker.Join();
Console.WriteLine("\n=== Лабораторія закрита ===");
```

### `15-04-klas-monitor.md` — блок #2 (рядок файлу 169)

**Помилки:**
- рядок 47: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.Threading;

class MultiWorkerQueue
{
    private readonly Queue<string> _items = new Queue<string>();
    private readonly object _lock = new object();
    private bool _running = true;

    public void Produce(string item)
    {
        lock (_lock)
        {
            _items.Enqueue(item);
            Monitor.PulseAll(_lock); // розбуджуємо всіх лаборантів
        }
    }

    public void Stop()
    {
        lock (_lock)
        {
            _running = false;
            Monitor.PulseAll(_lock);
        }
    }

    public string? Consume(string workerName)
    {
        lock (_lock)
        {
            while (_items.Count == 0 && _running)
                Monitor.Wait(_lock);

            if (_items.Count > 0)
            {
                string item = _items.Dequeue();
                Console.WriteLine($"[{workerName}] Взяв зразок: {item}");
                return item;
            }
            return null;
        }
    }
}

MultiWorkerQueue queue = new MultiWorkerQueue();

// Два лаборанти-споживачі
void RunWorker(string name)
{
    while (true)
    {
        string? item = queue.Consume(name);
        if (item == null) break;
        Thread.Sleep(200);
        Console.WriteLine($"[{name}] Аналіз '{item}' завершено");
    }
    Console.WriteLine($"[{name}] Зміна завершена");
}

Thread w1 = new Thread(() => RunWorker("Лаборант-1")) { Name = "Worker1" };
Thread w2 = new Thread(() => RunWorker("Лаборант-2")) { Name = "Worker2" };

w1.Start();
w2.Start();

// Виробник
Thread.Sleep(50);
string[] batch = { "Зразок-А", "Зразок-Б", "Зразок-В", "Зразок-Г", "Зразок-Д", "Зразок-Е" };
foreach (string s in batch)
{
    queue.Produce(s);
    Thread.Sleep(80);
}
queue.Stop();

w1.Join();
w2.Join();
Console.WriteLine("Всі аналізи завершено");
```

### `16-02-vkladeni-zavdannia-task-t.md` — блок #6 (рядок файлу 173)

**Помилки:**
- рядок 21: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

class LabResult
{
    public string PatientName { get; }
    public double Glucose     { get; }
    public double Hemoglobin  { get; }
    public string Status      { get; }

    public LabResult(string name, double glucose, double hemoglobin)
    {
        PatientName = name;
        Glucose     = glucose;
        Hemoglobin  = hemoglobin;
        Status      = glucose > 6.1 ? "Глюкоза підвищена" : hemoglobin < 120 ? "Гемоглобін знижений" : "Норма";
    }
}

Task<LabResult> labTask = Task.Run(() =>
{
    Console.WriteLine("[Лабораторія] Виконую аналіз крові Коваль М.В...");
    Thread.Sleep(400);
    return new LabResult("Коваль М.В.", glucose: 5.8, hemoglobin: 138.0);
});

LabResult result = labTask.Result; // блокуємось до завершення

Console.WriteLine($"\n=== Результат аналізу ===");
Console.WriteLine($"Пацієнт:    {result.PatientName}");
Console.WriteLine($"Глюкоза:    {result.Glucose.ToString("F1")} ммоль/л");
Console.WriteLine($"Гемоглобін: {result.Hemoglobin.ToString("F0")} г/л");
Console.WriteLine($"Висновок:   {result.Status}");
```

### `16-05-skasuvannia-zavdan-cancellationtoken.md` — блок #2 (рядок файлу 72)

**Помилки:**
- рядок 13: Cannot use local variable 'token' before it is declared

**Код:**
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

CancellationTokenSource cts = new CancellationTokenSource();

Task dataExport = Task.Run(() =>
{
    Console.WriteLine("[Експорт] Початок експорту медичних даних...");

    for (int i = 1; i <= 20; i++)
    {
        token.ThrowIfCancellationRequested(); // кидає виняток при Cancel()

        Console.WriteLine($"[Експорт] Пакет {i.ToString()}/20 відправлено");
        Thread.Sleep(100);
    }

    Console.WriteLine("[Експорт] Експорт завершено повністю");
}, cts.Token);

CancellationToken token = cts.Token;

Thread.Sleep(450); // скасовуємо після ~4 пакетів
Console.WriteLine("[Main] Скасовую експорт (адміністратор зупинив)...");
cts.Cancel();

try
{
    dataExport.Wait();
}
catch (AggregateException ae)
{
    foreach (var ex in ae.InnerExceptions)
    {
        if (ex is TaskCanceledException)
            Console.WriteLine("[Main] Завдання коректно скасовано");
        else
            Console.WriteLine($"[Main] Неочікувана помилка: {ex.Message}");
    }
}

Console.WriteLine($"[Main] Статус: {dataExport.Status}"); // Canceled
cts.Dispose();
```

### `17-02-typy-povernennia-async-metodiv.md` — блок #5 (рядок файлу 231)

**Помилки:**
- рядок 41: Top-level statements must precede namespace and type declarations.
- рядок 1: Program does not contain a static 'Main' method suitable for an entry point

**Код:**
```csharp
using System;
using System.Threading.Tasks;

// Інтерфейс репозиторію
interface IPatientRepository
{
    Task<string> GetNameAsync(string id);
    Task SaveAsync(string id, string data);
}

// Реальна реалізація — справді асинхронна (звертається до БД)
class DatabaseRepository : IPatientRepository
{
    public async Task<string> GetNameAsync(string id)
    {
        await Task.Delay(100); // реальний асинхронний запит
        return $"Пацієнт {id} з бази даних";
    }

    public async Task SaveAsync(string id, string data)
    {
        await Task.Delay(50);
        Console.WriteLine($"[DB] Збережено: {id}");
    }
}

// Фейкова реалізація для тестів — синхронна, але мусить відповідати інтерфейсу
class FakeRepository : IPatientRepository
{
    public Task<string> GetNameAsync(string id)
        => Task.FromResult($"Тестовий пацієнт {id}"); // синхронно, без async

    public Task SaveAsync(string id, string data)
    {
        Console.WriteLine($"[Fake] Зберігаю (імітація): {id}");
        return Task.CompletedTask; // Task, що вже завершений
    }
}

// Використання
IPatientRepository repo = new FakeRepository();
string name = await repo.GetNameAsync("PT-001");
Console.WriteLine($"Отримано: {name}");

await repo.SaveAsync("PT-001", "дані");
Console.WriteLine("[Main] Операції завершено");
```

### `17-06-async-potoky-iasyncenumerable.md` — блок #6 (рядок файлу 271)

**Помилки:**
- рядок 35: Top-level statements must precede namespace and type declarations.
- рядок 1: Program does not contain a static 'Main' method suitable for an entry point

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;

// Симуляція репозиторію з підтримкою стрімінгу
class PatientRepository
{
    private readonly string[] _allPatients = {
        "Коваль М.А.", "Бойко О.П.", "Мороз В.І.", "Петренко І.О.",
        "Руденко С.В.", "Шевченко Т.М.", "Гриценко Д.Ю.", "Сидоренко Р.К."
    };

    // Стрімінг з пагінацією — симуляція курсору БД
    public async IAsyncEnumerable<string> GetPatientsStreamAsync(
        string ward,
        [EnumeratorCancellation] CancellationToken ct = default)
    {
        Console.WriteLine($"[Repo] Відкриваю курсор БД для відділення {ward}");

        for (int i = 0; i < _allPatients.Length; i++)
        {
            ct.ThrowIfCancellationRequested();
            await Task.Delay(60, ct); // симуляція мережевої затримки

            yield return $"{_allPatients[i]} (відділення: {ward})";
        }

        Console.WriteLine("[Repo] Курсор БД закрито");
    }
}

// Сервісний рівень: обробка потоку
async Task ProcessWardPatientsAsync(string ward, CancellationToken ct)
{
    var repo = new PatientRepository();
    int count = 0;

    await foreach (string patient in repo.GetPatientsStreamAsync(ward, ct))
    {
        count++;
        Console.WriteLine($"  [{count.ToString()}] Оброблено: {patient}");
    }

    Console.WriteLine($"[Service] Відділення {ward}: оброблено {count.ToString()} пацієнтів");
}

using CancellationTokenSource cts = new CancellationTokenSource(500);

try
{
    await ProcessWardPatientsAsync("Терапія", cts.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("[Main] Обробку зупинено за тайм-аутом");
}
```

### `18-01-path-file-directory.md` — блок #12 (рядок файлу 297)

**Помилки:**
- рядок 34: 'IEnumerable<string>' does not contain a definition for 'OrderByDescending' and no accessible extension method 'OrderByDescending' accepting a first argument of type 'IEnumerable<string>' could be found (are you missing a using directive or an assembly reference?)

**Код:**
```csharp
using System;
using System.IO;

// Структура архіву: MedArchive/{рік}/{місяць}/{пацієнт}.txt
string archiveRoot = Path.Combine(Path.GetTempPath(), "MedArchive");

void SaveLabResult(string patientId, string result)
{
    string year  = DateTime.Now.Year.ToString();
    string month = DateTime.Now.Month.ToString("D2");
    string dir   = Path.Combine(archiveRoot, year, month);

    // Гарантуємо існування ієрархії теок
    Directory.CreateDirectory(dir);

    string fileName = $"{patientId}_{DateTime.Now:yyyyMMdd_HHmmss}.txt";
    string filePath = Path.Combine(dir, fileName);

    File.WriteAllText(filePath, result);
    Console.WriteLine($"Збережено: {filePath}");
}

string LoadLatestResult(string patientId)
{
    string year  = DateTime.Now.Year.ToString();
    string month = DateTime.Now.Month.ToString("D2");
    string dir   = Path.Combine(archiveRoot, year, month);

    if (!Directory.Exists(dir)) return "Архів порожній";

    // Знаходимо всі файли цього пацієнта і беремо найновіший
    string pattern = $"{patientId}_*.txt";
    string? latest = Directory.EnumerateFiles(dir, pattern)
        .OrderByDescending(f => f)
        .FirstOrDefault();

    return latest != null ? File.ReadAllText(latest) : "Результатів не знайдено";
}

// Зберігаємо кілька результатів
SaveLabResult("PT001", "Гемоглобін: 135 г/л — норма\nЛейкоцити: 6.2 — норма");
SaveLabResult("PT002", "Глюкоза: 7.8 ммоль/л — вище норми\nХолестерин: 5.1 — норма");
SaveLabResult("PT001", "Глюкоза: 4.9 ммоль/л — норма");

// Читаємо останній результат
Console.WriteLine($"\nОстанній результат PT001:\n{LoadLatestResult("PT001")}");

// Прибираємо тестові дані
if (Directory.Exists(archiveRoot))
    Directory.Delete(archiveRoot, recursive: true);
```

### `18-04-streamreader-streamwriter.md` — блок #8 (рядок файлу 322)

**Помилки:**
- рядок 10: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

// Структура запису лабораторного аналізу
record LabResult(string PatientId, string TestName, double Value, string Unit, string Status);

// CSV-файл з результатами аналізів
string csvPath = Path.Combine(Path.GetTempPath(), "lab_results.csv");
using (StreamWriter sw = new StreamWriter(csvPath, false, Encoding.UTF8))
{
    sw.WriteLine("patient_id,test_name,value,unit,status");
    sw.WriteLine("PT001,Гемоглобін,135.0,г/л,норма");
    sw.WriteLine("PT001,Лейкоцити,6.2,10^9/л,норма");
    sw.WriteLine("PT002,Глюкоза,7.8,ммоль/л,вище норми");
    sw.WriteLine("PT002,Холестерин,5.1,ммоль/л,норма");
    sw.WriteLine("PT003,Гемоглобін,98.0,г/л,нижче норми");
}

// Парсинг CSV
List<LabResult> ParseLabCsv(string path)
{
    var results = new List<LabResult>();
    using StreamReader sr = new StreamReader(path, Encoding.UTF8);
    
    string? header = sr.ReadLine(); // пропускаємо заголовок
    Console.WriteLine($"Заголовок: {header}");
    
    string? line;
    while ((line = sr.ReadLine()) != null)
    {
        if (string.IsNullOrWhiteSpace(line)) continue;
        
        string[] parts = line.Split(',');
        if (parts.Length < 5) continue;
        
        if (!double.TryParse(parts[2], System.Globalization.NumberStyles.Float,
            System.Globalization.CultureInfo.InvariantCulture, out double val))
            continue;
        
        results.Add(new LabResult(parts[0], parts[1], val, parts[3], parts[4]));
    }
    return results;
}

List<LabResult> results = ParseLabCsv(csvPath);
Console.WriteLine($"\nЗчитано {results.Count.ToString()} записів:");
foreach (LabResult r in results)
{
    string icon = r.Status == "норма" ? "[OK]" : "[!!]";
    Console.WriteLine($"  {icon} {r.PatientId} | {r.TestName}: {r.Value.ToString()} {r.Unit} — {r.Status}");
}

// Формуємо звіт — відхилення від норми
Console.WriteLine("\n--- Відхилення від норми ---");
foreach (LabResult r in results)
    if (r.Status != "норма")
        Console.WriteLine($"  {r.PatientId}: {r.TestName} = {r.Value.ToString()} {r.Unit} [{r.Status}]");

File.Delete(csvPath);
```

### `18-06-system-text-json.md` — блок #1 (рядок файлу 25)

**Помилки:**
- рядок 16: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Text.Json;

// Моделі даних медичної картки
class PatientCard
{
    public int    Id          { get; set; }
    public string FullName    { get; set; } = "";
    public int    Age         { get; set; }
    public string Diagnosis   { get; set; } = "";
    public bool   Hospitalized { get; set; }
    public double Glucose     { get; set; }
}

// Серіалізація: об'єкт → JSON рядок
var card = new PatientCard
{
    Id           = 1001,
    FullName     = "Петренко Іван Олексійович",
    Age          = 45,
    Diagnosis    = "J06.9",
    Hospitalized = false,
    Glucose      = 5.1
};

string json = JsonSerializer.Serialize(card);
Console.WriteLine("JSON (compact):");
Console.WriteLine(json);

// Відформатований JSON з відступами
var options = new JsonSerializerOptions { WriteIndented = true };
string prettyJson = JsonSerializer.Serialize(card, options);
Console.WriteLine("\nJSON (indented):");
Console.WriteLine(prettyJson);

// Десеріалізація: JSON рядок → об'єкт
PatientCard? restored = JsonSerializer.Deserialize<PatientCard>(json);
Console.WriteLine($"\nВідновлено: {restored?.FullName}, діагноз={restored?.Diagnosis}, вік={restored?.Age.ToString()}");
```

### `18-06-system-text-json.md` — блок #2 (рядок файлу 72)

**Помилки:**
- рядок 17: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

class MedRecord
{
    public int      PatientId  { get; set; }
    public string   PatientName { get; set; } = "";
    public string   TestName   { get; set; } = "";
    public double   Value      { get; set; }
    public string   Unit       { get; set; } = "";
    public string   Status     { get; set; } = "";
    public DateTime RecordedAt { get; set; }
}

string filePath = Path.Combine(Path.GetTempPath(), "med_records.json");

var records = new List<MedRecord>
{
    new() { PatientId=1001, PatientName="Петренко І.О.", TestName="Гемоглобін", Value=135.0, Unit="г/л",     Status="норма",       RecordedAt=DateTime.Now.AddHours(-2) },
    new() { PatientId=1001, PatientName="Петренко І.О.", TestName="Глюкоза",    Value=5.1,   Unit="ммоль/л", Status="норма",       RecordedAt=DateTime.Now.AddHours(-2) },
    new() { PatientId=1002, PatientName="Бойко О.П.",    TestName="Глюкоза",    Value=8.7,   Unit="ммоль/л", Status="вище норми",  RecordedAt=DateTime.Now.AddHours(-1) },
    new() { PatientId=1003, PatientName="Мороз В.І.",    TestName="Гемоглобін", Value=98.0,  Unit="г/л",     Status="нижче норми", RecordedAt=DateTime.Now },
};

var options = new JsonSerializerOptions
{
    WriteIndented = true,
    // Серіалізація DateTime у ISO 8601
};

// Запис у файл через Stream — ефективніше ніж Serialize → string → WriteAllText
using (FileStream fs = File.Create(filePath))
{
    JsonSerializer.Serialize(fs, records, options);
}

FileInfo fi = new FileInfo(filePath);
Console.WriteLine($"Записано: {fi.Length.ToString()} байт");

// Читання з файлу
List<MedRecord>? loaded;
using (FileStream fs = File.OpenRead(filePath))
{
    loaded = JsonSerializer.Deserialize<List<MedRecord>>(fs);
}

Console.WriteLine($"Завантажено: {loaded?.Count.ToString()} записів");
if (loaded != null)
{
    foreach (MedRecord r in loaded)
    {
        string icon = r.Status == "норма" ? "[OK]" : "[!!]";
        Console.WriteLine($"  {icon} {r.PatientName} | {r.TestName}: {r.Value.ToString()} {r.Unit} ({r.Status})");
    }
}

File.Delete(filePath);
```

### `18-06-system-text-json.md` — блок #3 (рядок файлу 140)

**Помилки:**
- рядок 14: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

class PatientVitals
{
    public int    PatientId    { get; set; }
    public string fullName     { get; set; } = "";  // camelCase назва
    public double BloodPressure { get; set; }
    public int    HeartRate    { get; set; }
    public string? Notes       { get; set; }        // null-able
}

var vitals = new PatientVitals
{
    PatientId     = 1001,
    fullName      = "Петренко І.О.",
    BloodPressure = 120.0 / 80.0,
    HeartRate     = 72,
    Notes         = null
};

// За замовчуванням: PascalCase, null включається
Console.WriteLine("=== Стандартні опції ===");
Console.WriteLine(JsonSerializer.Serialize(vitals, new JsonSerializerOptions { WriteIndented = true }));

// camelCase назви полів (стандарт JavaScript/REST)
Console.WriteLine("\n=== camelCase ===");
var camelOptions = new JsonSerializerOptions
{
    WriteIndented      = true,
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
};
Console.WriteLine(JsonSerializer.Serialize(vitals, camelOptions));

// Ігнорування null-значень
Console.WriteLine("\n=== Без null полів ===");
var noNullOptions = new JsonSerializerOptions
{
    WriteIndented      = true,
    DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
};
Console.WriteLine(JsonSerializer.Serialize(vitals, noNullOptions));

// Десеріалізація нечутлива до регістру
string json = """{"patientid":1002,"fullname":"Бойко О.П.","bloodpressure":1.6,"heartrate":145,"notes":null}""";
var relaxedOptions = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
PatientVitals? loaded = JsonSerializer.Deserialize<PatientVitals>(json, relaxedOptions);
Console.WriteLine($"\nНечутливо до регістру: {loaded?.fullName}, пульс={loaded?.HeartRate.ToString()}");
```

### `18-06-system-text-json.md` — блок #4 (рядок файлу 194)

**Помилки:**
- рядок 27: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

// Рекомендований набір опцій для REST API / зберігання
var standardOptions = new JsonSerializerOptions
{
    WriteIndented              = false,               // компактний для API/файлів
    PropertyNamingPolicy       = JsonNamingPolicy.CamelCase, // camelCase для JS
    PropertyNameCaseInsensitive = true,               // гнучке читання
    DefaultIgnoreCondition     = JsonIgnoreCondition.WhenWritingNull, // без null
    // Enum як рядки замість чисел
    Converters = { new JsonStringEnumConverter() }
};

// Використовуємо enum
enum PatientStatus { Active, Discharged, InTreatment }

class Appointment
{
    public int           Id     { get; set; }
    public string        Doctor { get; set; } = "";
    public PatientStatus Status { get; set; }
    public string?       Room   { get; set; }
}

var apt = new Appointment { Id = 5, Doctor = "Коваленко О.П.", Status = PatientStatus.InTreatment, Room = null };
string json = JsonSerializer.Serialize(apt, standardOptions);
Console.WriteLine("Стандартний API JSON:");
Console.WriteLine(json);

// Десеріалізація
Appointment? loaded = JsonSerializer.Deserialize<Appointment>(json, standardOptions);
Console.WriteLine($"\nПовернуто: id={loaded?.Id.ToString()}, лікар={loaded?.Doctor}, статус={loaded?.Status}");
```

### `18-06-system-text-json.md` — блок #5 (рядок файлу 235)

**Помилки:**
- рядок 29: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

class DiagnosisRecord
{
    [JsonPropertyName("patient_id")]   // Перейменування поля у JSON
    public int PatientId { get; set; }
    
    [JsonPropertyName("diagnosis_code")]
    public string DiagnosisCode { get; set; } = "";
    
    [JsonIgnore]                        // Поле не включається у JSON
    public string InternalNotes { get; set; } = "внутрішні примітки";
    
    [JsonPropertyOrder(1)]              // Порядок полів у JSON
    public string PatientName { get; set; } = "";
    
    [JsonPropertyOrder(2)]
    public DateTime RecordedAt { get; set; }
    
    [JsonInclude]                       // Включає публічне поле (не тільки property)
    public string Ward = "";
    
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingDefault)]
    public double? OptionalValue { get; set; } // null або 0 — не записується
}

var record = new DiagnosisRecord
{
    PatientId     = 1001,
    DiagnosisCode = "J06.9",
    InternalNotes = "ці дані НЕ збережуться у JSON",
    PatientName   = "Петренко І.О.",
    RecordedAt    = DateTime.Now,
    Ward          = "Терапія",
    OptionalValue = null
};

string json = JsonSerializer.Serialize(record, new JsonSerializerOptions { WriteIndented = true });
Console.WriteLine("JSON з атрибутами:");
Console.WriteLine(json);

// Перевіряємо: InternalNotes відсутній у JSON
Console.WriteLine($"\nПоле 'InternalNotes' у JSON: {json.Contains("InternalNotes").ToString()} (має бути False)");
Console.WriteLine($"Поле 'patient_id' у JSON: {json.Contains("patient_id").ToString()} (має бути True)");
```

### `18-06-system-text-json.md` — блок #6 (рядок файлу 296)

**Помилки:**
- рядок 21: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.Text.Json;

// Вкладені класи
class Address
{
    public string City   { get; set; } = "";
    public string Street { get; set; } = "";
}

class Patient
{
    public int             Id         { get; set; }
    public string          Name       { get; set; } = "";
    public Address?        Address    { get; set; }
    public List<string>    Diagnoses  { get; set; } = new();
    public Dictionary<string, double> LabResults { get; set; } = new();
}

var patient = new Patient
{
    Id      = 1001,
    Name    = "Петренко І.О.",
    Address = new Address { City = "Київ", Street = "вул. Хрещатик, 1" },
    Diagnoses = new List<string> { "J06.9", "I10" },
    LabResults = new Dictionary<string, double>
    {
        ["Гемоглобін"] = 135.0,
        ["Глюкоза"]    = 5.1,
        ["Холестерин"] = 4.8
    }
};

var opts = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(patient, opts);
Console.WriteLine("Вкладений JSON:");
Console.WriteLine(json);

// Десеріалізація — вкладені об'єкти відновлюються автоматично
Patient? loaded = JsonSerializer.Deserialize<Patient>(json, opts);
Console.WriteLine($"\nВідновлено:");
Console.WriteLine($"  {loaded?.Name}, м.{loaded?.Address?.City}");
Console.WriteLine($"  Діагнози: {string.Join(", ", loaded?.Diagnoses ?? new())}");
foreach (var (test, val) in loaded?.LabResults ?? new())
    Console.WriteLine($"  {test}: {val.ToString()}");
```

### `18-06-system-text-json.md` — блок #7 (рядок файлу 347)

**Помилки:**
- рядок 34: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Collections.Generic;

// Конфігурація клініки — типовий сценарій для JSON
class ClinicConfig
{
    [JsonPropertyName("clinic_name")]
    public string ClinicName { get; set; } = "";
    
    [JsonPropertyName("departments")]
    public List<string> Departments { get; set; } = new();
    
    [JsonPropertyName("max_patients_per_day")]
    public int MaxPatientsPerDay { get; set; }
    
    [JsonPropertyName("lab_thresholds")]
    public LabThresholds Thresholds { get; set; } = new();
    
    [JsonPropertyName("last_updated")]
    public DateTime LastUpdated { get; set; }
}

class LabThresholds
{
    [JsonPropertyName("glucose_max")]    public double GlucoseMax    { get; set; }
    [JsonPropertyName("pulse_min")]      public int    PulseMin      { get; set; }
    [JsonPropertyName("pulse_max")]      public int    PulseMax      { get; set; }
    [JsonPropertyName("hemoglobin_min")] public double HemoglobinMin { get; set; }
}

string configPath = Path.Combine(Path.GetTempPath(), "clinic_config.json");

// Запис конфігурації
var config = new ClinicConfig
{
    ClinicName         = "Міська клінічна лікарня №1",
    Departments        = new List<string> { "Терапія", "Кардіологія", "Неврологія", "Хірургія" },
    MaxPatientsPerDay  = 200,
    Thresholds         = new LabThresholds { GlucoseMax=7.0, PulseMin=60, PulseMax=100, HemoglobinMin=110.0 },
    LastUpdated        = DateTime.Now
};

var opts = new JsonSerializerOptions { WriteIndented = true };
using (FileStream fs = File.Create(configPath))
    JsonSerializer.Serialize(fs, config, opts);

Console.WriteLine($"Конфіг збережено: {new FileInfo(configPath).Length.ToString()} байт");

// Завантаження та використання
ClinicConfig? loaded;
using (FileStream fs = File.OpenRead(configPath))
    loaded = JsonSerializer.Deserialize<ClinicConfig>(fs, opts);

Console.WriteLine($"\nКлініка: {loaded?.ClinicName}");
Console.WriteLine($"Відділення: {string.Join(", ", loaded?.Departments ?? new())}");
Console.WriteLine($"Ліміт пацієнтів/день: {loaded?.MaxPatientsPerDay.ToString()}");
Console.WriteLine($"Порогові значення:");
Console.WriteLine($"  Глюкоза: <= {loaded?.Thresholds.GlucoseMax.ToString()} ммоль/л");
Console.WriteLine($"  Пульс: {loaded?.Thresholds.PulseMin.ToString()} - {loaded?.Thresholds.PulseMax.ToString()} уд/хв");

// Перевірка пацієнта по конфігу
double patientGlucose = 8.5;
bool criticalGlucose = loaded != null && patientGlucose > loaded.Thresholds.GlucoseMax;
Console.WriteLine($"\nГлюкоза {patientGlucose.ToString()} ммоль/л — {(criticalGlucose ? "КРИТИЧНО" : "норма")}");

File.Delete(configPath);
```

### `19-01-system-text-json-advanced.md` — блок #4 (рядок файлу 170)

**Помилки:**
- рядок 44: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

// Кастомний тип — діапазон нормальних значень показника
struct NormalRange
{
    public double Min { get; }
    public double Max { get; }
    public NormalRange(double min, double max) { Min = min; Max = max; }
    public override string ToString() => $"{Min.ToString()}-{Max.ToString()}";
}

// За замовчуванням NormalRange серіалізується як об'єкт {"Min":...,"Max":...}
// Хочемо: рядок "4.0-6.5" для компактності

class NormalRangeConverter : JsonConverter<NormalRange>
{
    // Читання: "4.0-6.5" -> NormalRange(4.0, 6.5)
    public override NormalRange Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        string? s = reader.GetString() ?? throw new JsonException("Expected string for NormalRange");
        string[] parts = s.Split('-');
        if (parts.Length != 2) throw new JsonException($"Invalid NormalRange format: {s}");
        return new NormalRange(double.Parse(parts[0]), double.Parse(parts[1]));
    }

    // Запис: NormalRange(4.0, 6.5) -> "4.0-6.5"
    public override void Write(Utf8JsonWriter writer, NormalRange value, JsonSerializerOptions options)
    {
        writer.WriteStringValue($"{value.Min.ToString()}-{value.Max.ToString()}");
    }
}

class LabTest
{
    public string      Name    { get; set; } = "";
    public double      Value   { get; set; }
    public string      Unit    { get; set; } = "";
    [JsonConverter(typeof(NormalRangeConverter))]   // атрибут на конкретному полі
    public NormalRange Normal  { get; set; }
}

var test = new LabTest
{
    Name   = "Глюкоза",
    Value  = 5.4,
    Unit   = "ммоль/л",
    Normal = new NormalRange(3.9, 6.1)
};

var opts = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(test, opts);
Console.WriteLine("JSON з кастомним конвертером:");
Console.WriteLine(json);

// Десеріалізація — конвертер відпрацьовує автоматично
LabTest? loaded = JsonSerializer.Deserialize<LabTest>(json, opts);
Console.WriteLine($"\nВідновлено: {loaded?.Name} = {loaded?.Value.ToString()} {loaded?.Unit}");
Console.WriteLine($"Норма: {loaded?.Normal}");
Console.WriteLine($"Статус: {(loaded?.Value >= loaded?.Normal.Min && loaded?.Value <= loaded?.Normal.Max ? "норма" : "відхилення")}");
```

### `19-01-system-text-json-advanced.md` — блок #5 (рядок файлу 240)

**Помилки:**
- рядок 34: Top-level statements must precede namespace and type declarations.
- рядок 34: The type or namespace name 'List<>' could not be found (are you missing a using directive or an assembly reference?)
- рядок 47: The type or namespace name 'List<>' could not be found (are you missing a using directive or an assembly reference?)

**Код:**
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

[JsonPolymorphic(TypeDiscriminatorPropertyName = "$type")]
[JsonDerivedType(typeof(BloodTest),   typeDiscriminator: "blood")]
[JsonDerivedType(typeof(EcgRecord),   typeDiscriminator: "ecg")]
[JsonDerivedType(typeof(ImagingData), typeDiscriminator: "imaging")]
abstract class MedicalResult
{
    public int    PatientId  { get; set; }
    public DateTime RecordedAt { get; set; } = DateTime.Now;
}

class BloodTest : MedicalResult
{
    public double Glucose    { get; set; }
    public double Hemoglobin { get; set; }
}

class EcgRecord : MedicalResult
{
    public int    HeartRate  { get; set; }
    public string Rhythm     { get; set; } = "";
}

class ImagingData : MedicalResult
{
    public string Modality   { get; set; } = ""; // МРТ, КТ, УЗД
    public string BodyPart   { get; set; } = "";
}

// Список різних підтипів
var results = new List<MedicalResult>
{
    new BloodTest   { PatientId=1001, Glucose=5.1, Hemoglobin=135.0 },
    new EcgRecord   { PatientId=1001, HeartRate=72, Rhythm="синусовий" },
    new ImagingData { PatientId=1002, Modality="УЗД", BodyPart="черевна порожнина" },
};

var opts = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(results, opts);
Console.WriteLine("Поліморфний JSON:");
Console.WriteLine(json);

// Десеріалізація відновлює правильний підтип
var loaded = JsonSerializer.Deserialize<List<MedicalResult>>(json, opts)!;
foreach (MedicalResult r in loaded)
{
    string info = r switch
    {
        BloodTest   b => $"Кров: глюкоза={b.Glucose.ToString()}",
        EcgRecord   e => $"ЕКГ: пульс={e.HeartRate.ToString()}, ритм={e.Rhythm}",
        ImagingData i => $"Знімок: {i.Modality} ({i.BodyPart})",
        _             => "невідомий тип"
    };
    Console.WriteLine($"  [{r.GetType().Name}] пацієнт {r.PatientId.ToString()}: {info}");
}
```

### `19-01-system-text-json-advanced.md` — блок #6 (рядок файлу 307)

**Помилки:**
- рядок 14: Top-level statements must precede namespace and type declarations.
- рядок 1: Program does not contain a static 'Main' method suitable for an entry point

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

class PatientRecord
{
    public int      Id        { get; set; }
    public string   Name      { get; set; } = "";
    public string   Diagnosis { get; set; } = "";
    public DateTime AdmittedAt { get; set; }
}

string filePath = Path.Combine(Path.GetTempPath(), "patients_async.json");

var patients = new List<PatientRecord>
{
    new() { Id=1001, Name="Петренко І.О.", Diagnosis="J06.9", AdmittedAt=DateTime.Now.AddDays(-3) },
    new() { Id=1002, Name="Бойко О.П.",    Diagnosis="I10",   AdmittedAt=DateTime.Now.AddDays(-1) },
    new() { Id=1003, Name="Мороз В.І.",    Diagnosis="E11.9", AdmittedAt=DateTime.Now },
};

var opts = new JsonSerializerOptions { WriteIndented = true };

// Async запис у файл — не блокує потік під час I/O
await using (FileStream fs = File.Create(filePath))
    await JsonSerializer.SerializeAsync(fs, patients, opts);

Console.WriteLine($"Async запис: {new FileInfo(filePath).Length.ToString()} байт");

// Async читання з файлу
await using (FileStream fs = File.OpenRead(filePath))
{
    List<PatientRecord>? loaded = await JsonSerializer.DeserializeAsync<List<PatientRecord>>(fs, opts);
    Console.WriteLine($"Async читання: {loaded?.Count.ToString()} записів");
    foreach (var p in loaded ?? new())
        Console.WriteLine($"  [{p.Id.ToString()}] {p.Name} — {p.Diagnosis}");
}

File.Delete(filePath);
```

### `19-02-xml-xmldocument.md` — блок #6 (рядок файлу 316)

**Помилки:**
- рядок 9: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Xml;

record ExamResult(string TestName, double Value, string Unit, string Status, string ReferenceRange);
record PatientExam(int PatientId, string PatientName, DateTime ExamDate, List<ExamResult> Results);

string BuildExamXml(PatientExam exam)
{
    XmlDocument doc = new XmlDocument();
    doc.AppendChild(doc.CreateXmlDeclaration("1.0", "utf-8", null));

    XmlElement root = doc.CreateElement("examination");
    root.SetAttribute("version",  "2.0");
    root.SetAttribute("exportedAt", DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ"));
    doc.AppendChild(root);

    // Пацієнт
    XmlElement pt = doc.CreateElement("patient");
    pt.SetAttribute("id", exam.PatientId.ToString());
    pt.InnerText = exam.PatientName;
    root.AppendChild(pt);

    // Дата обстеження
    XmlElement dateEl = doc.CreateElement("examDate");
    dateEl.InnerText = exam.ExamDate.ToString("yyyy-MM-dd");
    root.AppendChild(dateEl);

    // Результати
    XmlElement resultsEl = doc.CreateElement("labResults");
    resultsEl.SetAttribute("count", exam.Results.Count.ToString());
    root.AppendChild(resultsEl);

    foreach (ExamResult r in exam.Results)
    {
        XmlElement res = doc.CreateElement("result");
        res.SetAttribute("status", r.Status);
        res.SetAttribute("ref",    r.ReferenceRange);

        XmlElement testEl = doc.CreateElement("test");  testEl.InnerText = r.TestName;
        XmlElement valEl  = doc.CreateElement("value"); valEl.InnerText = r.Value.ToString("F2");
        valEl.SetAttribute("unit", r.Unit);

        res.AppendChild(testEl);
        res.AppendChild(valEl);
        resultsEl.AppendChild(res);
    }

    using StringWriter sw = new StringWriter();
    using XmlTextWriter xw = new XmlTextWriter(sw) { Formatting = Formatting.Indented, Indentation = 4 };
    doc.WriteTo(xw);
    return sw.ToString();
}

// Тест
var exam = new PatientExam(1001, "Петренко Іван Олексійович", DateTime.Now, new List<ExamResult>
{
    new("Гемоглобін",   135.0, "г/л",     "норма",       "120-160"),
    new("Глюкоза",      7.8,   "ммоль/л", "вище норми",  "3.9-6.1"),
    new("Лейкоцити",    6.2,   "10^9/л",  "норма",       "4.0-9.0"),
    new("Холестерин",   5.1,   "ммоль/л", "норма",       "<5.2"),
});

string resultXml = BuildExamXml(exam);
Console.WriteLine(resultXml);

// Збереження
string path = Path.Combine(Path.GetTempPath(), "exam_result.xml");
File.WriteAllText(path, resultXml, System.Text.Encoding.UTF8);
Console.WriteLine($"\nФайл: {new FileInfo(path).Length.ToString()} байт");
File.Delete(path);
```

### `19-03-xdocument-linq-to-xml.md` — блок #2 (рядок файлу 73)

**Помилки:**
- рядок 26: No overload for method 'Count' takes 0 arguments
- рядок 31: No overload for method 'Count' takes 0 arguments

**Код:**
```csharp
using System;
using System.IO;
using System.Xml.Linq;

string path = Path.Combine(Path.GetTempPath(), "clinic_xdoc.xml");

XDocument doc = new XDocument(
    new XElement("clinic",
        new XElement("patient", new XAttribute("id","PT-1001"),
            new XElement("name","Петренко І.О."),
            new XElement("ward","Терапія")),
        new XElement("patient", new XAttribute("id","PT-1002"),
            new XElement("name","Бойко О.П."),
            new XElement("ward","Кардіологія"))
    )
);

// Save — з автоматичними відступами
doc.Save(path);
Console.WriteLine($"Збережено: {new FileInfo(path).Length.ToString()} байт");
Console.WriteLine(File.ReadAllText(path));

// Load — завантаження з файлу
XDocument loaded = XDocument.Load(path);
Console.WriteLine($"Кореневий елемент: {loaded.Root?.Name}");
Console.WriteLine($"Пацієнтів: {loaded.Root?.Elements("patient").Count().ToString()}");

// Parse — завантаження з рядка
string xmlStr = "<root><item>A</item><item>B</item></root>";
XDocument parsed = XDocument.Parse(xmlStr);
Console.WriteLine($"Parse: {parsed.Root?.Elements().Count().ToString()} елементів");

File.Delete(path);
```

### `19-03-xdocument-linq-to-xml.md` — блок #3 (рядок файлу 111)

**Помилки:**
- рядок 29: No overload for method 'Count' takes 0 arguments
- рядок 39: No overload for method 'Count' takes 0 arguments
- рядок 47: 'IEnumerable<XElement>' does not contain a definition for 'FirstOrDefault' and no accessible extension method 'FirstOrDefault' accepting a first argument of type 'IEnumerable<XElement>' could be found (are you missing a using directive or an assembly reference?)

**Код:**
```csharp
using System;
using System.Xml.Linq;

XDocument doc = XDocument.Parse("""
<clinic>
    <patient id="PT-1001" ward="Терапія">
        <name>Петренко Іван Олексійович</name>
        <diagnosis code="J06.9">ГРВІ</diagnosis>
        <diagnosis code="I10">Гіпертонія</diagnosis>
    </patient>
    <patient id="PT-1002" ward="Кардіологія">
        <name>Бойко Оксана Петрівна</name>
        <diagnosis code="I21.0">Інфаркт міокарда</diagnosis>
    </patient>
    <patient id="PT-1003" ward="Терапія">
        <name>Мороз Василь Іванович</name>
        <diagnosis code="E11.9">Діабет 2 типу</diagnosis>
    </patient>
</clinic>
""");

XElement root = doc.Root!;

// Element(name) — перший прямий дочірній елемент з такою назвою
XElement? first = root.Element("patient");
Console.WriteLine($"Перший: {first?.Attribute("id")?.Value}");

// Elements(name) — всі прямі дочірні з такою назвою
Console.WriteLine($"\nВсі пацієнти ({root.Elements("patient").Count().ToString()}):");
foreach (XElement p in root.Elements("patient"))
{
    string id   = p.Attribute("id")?.Value ?? "";
    string ward = p.Attribute("ward")?.Value ?? "";
    string name = p.Element("name")?.Value ?? "";
    Console.WriteLine($"  [{id}] {name} — {ward}");
}

// Descendants(name) — всі нащадки з назвою на будь-якій глибині
Console.WriteLine($"\nВсі діагнози ({root.Descendants("diagnosis").Count().ToString()}):");
foreach (XElement diag in root.Descendants("diagnosis"))
{
    string code = diag.Attribute("code")?.Value ?? "";
    Console.WriteLine($"  [{code}] {diag.Value}");
}

// Ancestors — навігація вгору
XElement? oneDiag = root.Descendants("diagnosis").FirstOrDefault();
Console.WriteLine($"\nБатьківський пацієнт діагнозу: {oneDiag?.Parent?.Element("name")?.Value}");
```

### `19-03-xdocument-linq-to-xml.md` — блок #6 (рядок файлу 298)

**Помилки:**
- рядок 8: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Xml.Linq;

record LabResult(int PatientId, string Name, string Test, double Value, string Unit, string Status);

var results = new List<LabResult>
{
    new(1001, "Петренко І.О.", "Гемоглобін",  135.0, "г/л",     "норма"),
    new(1001, "Петренко І.О.", "Глюкоза",     5.1,   "ммоль/л", "норма"),
    new(1002, "Бойко О.П.",    "Глюкоза",     8.7,   "ммоль/л", "вище норми"),
    new(1002, "Бойко О.П.",    "Холестерин",  5.8,   "ммоль/л", "вище норми"),
    new(1003, "Мороз В.І.",    "Гемоглобін",  98.0,  "г/л",     "нижче норми"),
};

// Генерація XML з групуванням по пацієнту
XDocument report = new XDocument(
    new XDeclaration("1.0", "utf-8", null),
    new XElement("labReport",
        new XAttribute("generatedAt", DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss")),
        new XAttribute("totalResults", results.Count.ToString()),

        // LINQ прямо у конструкторі XElement
        from g in results.GroupBy(r => r.PatientId)
        select new XElement("patient",
            new XAttribute("id",   g.Key.ToString()),
            new XAttribute("name", g.First().Name),
            new XAttribute("resultsCount", g.Count().ToString()),
            from r in g
            select new XElement("result",
                new XAttribute("status", r.Status),
                new XElement("test",  r.Test),
                new XElement("value", new XAttribute("unit", r.Unit), r.Value.ToString("F2"))
            )
        )
    )
);

Console.WriteLine(report.ToString());

// Підрахунок відхилень
int abnormal = report.Descendants("result")
    .Count(r => r.Attribute("status")?.Value != "норма");
Console.WriteLine($"\nВідхилень від норми: {abnormal.ToString()} з {results.Count.ToString()}");
```

### `19-04-xmlreader-xmlwriter.md` — блок #5 (рядок файлу 290)

**Помилки:**
- рядок 9: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Xml;

record Patient(int Id, string Name, string Ward, string[] Diagnoses, double Glucose, int Pulse);

var patients = new List<Patient>
{
    new(1001, "Петренко І.О.", "Терапія",     new[]{"J06.9","I10"},    5.1, 72),
    new(1002, "Бойко О.П.",   "Кардіологія", new[]{"I21.0"},          8.7, 145),
    new(1003, "Мороз В.І.",   "Неврологія",  new[]{"G43.9","G40.9"},  4.8, 68),
};

string path = Path.Combine(Path.GetTempPath(), "patients_export.xml");

var settings = new XmlWriterSettings { Indent = true, Encoding = Encoding.UTF8 };
using (XmlWriter w = XmlWriter.Create(path, settings))
{
    w.WriteStartDocument();
    w.WriteStartElement("clinicExport");
    w.WriteAttributeString("exportedAt", DateTime.Now.ToString("O"));
    w.WriteAttributeString("count",      patients.Count.ToString());

    foreach (Patient p in patients)
    {
        w.WriteStartElement("patient");
        w.WriteAttributeString("id",   p.Id.ToString());
        w.WriteAttributeString("ward", p.Ward);

        w.WriteElementString("name", p.Name);

        // Числові значення
        w.WriteStartElement("vitals");
        w.WriteElementString("glucose", p.Glucose.ToString("F1"));
        w.WriteElementString("pulse",   p.Pulse.ToString());
        w.WriteEndElement(); // </vitals>

        // Масив діагнозів
        w.WriteStartElement("diagnoses");
        foreach (string code in p.Diagnoses)
            w.WriteElementString("code", code);
        w.WriteEndElement(); // </diagnoses>

        // Умовний елемент — тільки якщо критичний стан
        bool critical = p.Glucose > 7.0 || p.Pulse > 120;
        if (critical)
        {
            w.WriteStartElement("alert");
            w.WriteAttributeString("level", "high");
            w.WriteString(p.Glucose > 7.0 ? $"Глюкоза: {p.Glucose.ToString("F1")}" : $"Пульс: {p.Pulse.ToString()}");
            w.WriteEndElement();
        }

        w.WriteEndElement(); // </patient>
    }

    w.WriteEndElement(); // </clinicExport>
    w.WriteEndDocument();
}

Console.WriteLine(File.ReadAllText(path, Encoding.UTF8));
Console.WriteLine($"Файл: {new FileInfo(path).Length.ToString()} байт");
File.Delete(path);
```

### `19-05-xmlserializer.md` — блок #1 (рядок файлу 21)

**Помилки:**
- рядок 14: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.IO;
using System.Xml.Serialization;

public class Patient
{
    public int    Id       { get; set; }
    public string Name     { get; set; } = "";
    public string Ward     { get; set; } = "";
    public int    Age      { get; set; }
}

// Серіалізація
Patient patient = new Patient { Id = 1001, Name = "Петренко Іван", Ward = "Терапія", Age = 45 };

XmlSerializer serializer = new XmlSerializer(typeof(Patient));

// У рядок через StringWriter
using StringWriter sw = new StringWriter();
serializer.Serialize(sw, patient);
string xml = sw.ToString();
Console.WriteLine(xml);

// Десеріалізація
using StringReader sr = new StringReader(xml);
Patient? loaded = (Patient?)serializer.Deserialize(sr);
Console.WriteLine($"\nЗавантажено: {loaded?.Name}, відділення: {loaded?.Ward}");
```

### `19-05-xmlserializer.md` — блок #2 (рядок файлу 57)

**Помилки:**
- рядок 28: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.IO;
using System.Xml.Serialization;

[XmlRoot("patient", Namespace = "http://clinic.ua/2024")]
public class PatientRecord
{
    // Властивість → XML-атрибут (не елемент)
    [XmlAttribute("id")]
    public string PatientId { get; set; } = "";

    // Властивість → елемент з іншою назвою
    [XmlElement("fullName")]
    public string Name { get; set; } = "";

    // Властивість → елемент у просторі імен
    [XmlElement("ward", Namespace = "http://clinic.ua/2024")]
    public string Ward { get; set; } = "";

    // Властивість повністю ігнорується
    [XmlIgnore]
    public DateTime LastAccessed { get; set; }

    // Числова властивість без зміни імені
    public int Age { get; set; }
}

PatientRecord rec = new PatientRecord
{
    PatientId    = "PT-1001",
    Name         = "Петренко Іван Олексійович",
    Ward         = "Терапія",
    Age          = 45,
    LastAccessed = DateTime.Now   // буде проігноровано
};

XmlSerializer xs = new XmlSerializer(typeof(PatientRecord));
using StringWriter sw = new StringWriter();
xs.Serialize(sw, rec);
Console.WriteLine(sw.ToString());
```

### `19-05-xmlserializer.md` — блок #3 (рядок файлу 112)

**Помилки:**
- рядок 50: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Xml.Serialization;

public class DiagnosisEntry
{
    [XmlAttribute("code")]
    public string Code { get; set; } = "";

    [XmlAttribute("system")]
    public string System { get; set; } = "ICD-10";

    [XmlText]
    public string Description { get; set; } = "";
}

public class VitalSign
{
    [XmlAttribute("type")]
    public string Type  { get; set; } = "";

    [XmlAttribute("unit")]
    public string Unit  { get; set; } = "";

    [XmlText]
    public string Value { get; set; } = "";
}

[XmlRoot("patientRecord")]
public class FullPatientRecord
{
    [XmlAttribute("id")]
    public string Id { get; set; } = "";

    [XmlElement("name")]
    public string Name { get; set; } = "";

    // List → <diagnoses><diagnosis ...>
    [XmlArray("diagnoses")]
    [XmlArrayItem("diagnosis")]
    public List<DiagnosisEntry> Diagnoses { get; set; } = new();

    // List → <vitals><sign ...>
    [XmlArray("vitals")]
    [XmlArrayItem("sign")]
    public List<VitalSign> Vitals { get; set; } = new();
}

FullPatientRecord record = new FullPatientRecord
{
    Id   = "PT-1001",
    Name = "Петренко Іван Олексійович",
    Diagnoses = new List<DiagnosisEntry>
    {
        new() { Code = "J06.9", Description = "ГРВІ" },
        new() { Code = "I10",   Description = "Гіпертонія" }
    },
    Vitals = new List<VitalSign>
    {
        new() { Type = "temperature", Unit = "C",   Value = "37.2" },
        new() { Type = "pulse",       Unit = "bpm", Value = "82"   }
    }
};

XmlSerializer xs = new XmlSerializer(typeof(FullPatientRecord));
using StringWriter sw = new StringWriter();
xs.Serialize(sw, record);
Console.WriteLine(sw.ToString());
```

### `19-05-xmlserializer.md` — блок #4 (рядок файлу 186)

**Помилки:**
- рядок 16: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.IO;
using System.Xml;
using System.Xml.Serialization;

[XmlRoot("clinic", Namespace = "http://clinic.ua/schema/2024")]
public class ClinicDocument
{
    [XmlElement("name")]
    public string ClinicName { get; set; } = "";

    [XmlElement("registrationDate")]
    public string RegDate { get; set; } = "";
}

ClinicDocument doc = new ClinicDocument
{
    ClinicName = "Міська клінічна лікарня №5",
    RegDate    = "2024-01-01"
};

XmlSerializer xs   = new XmlSerializer(typeof(ClinicDocument));
XmlSerializerNamespaces ns = new XmlSerializerNamespaces();
ns.Add("clinic", "http://clinic.ua/schema/2024");
ns.Add("",       "");   // прибирає зайвий xsi/xsd

using StringWriter sw = new StringWriter();
xs.Serialize(sw, doc, ns);
Console.WriteLine(sw.ToString());
```

### `19-05-xmlserializer.md` — блок #5 (рядок файлу 222)

**Помилки:**
- рядок 34: Top-level statements must precede namespace and type declarations.
- рядок 19: The type or namespace name 'List<>' could not be found (are you missing a using directive or an assembly reference?)
- рядок 58: 'MemoryExtensions.Count<T>(Span<T>, T)' is a method, which is not valid in the given context

**Код:**
```csharp
using System;
using System.IO;
using System.Xml.Serialization;

[XmlRoot("examination")]
public class ExamRecord
{
    [XmlAttribute("patientId")]
    public string PatientId { get; set; } = "";

    [XmlElement("examDate")]
    public string ExamDate { get; set; } = "";

    [XmlElement("conclusion")]
    public string Conclusion { get; set; } = "";

    [XmlArray("tests")]
    [XmlArrayItem("test")]
    public List<TestResult> Tests { get; set; } = new();
}

public class TestResult
{
    [XmlAttribute("name")]
    public string Name { get; set; } = "";

    [XmlAttribute("status")]
    public string Status { get; set; } = "";

    [XmlText]
    public string Value { get; set; } = "";
}

string xmlData = """
<?xml version="1.0" encoding="utf-16"?>
<examination patientId="PT-1002">
  <examDate>2024-03-15</examDate>
  <conclusion>Стан задовільний</conclusion>
  <tests>
    <test name="Гемоглобін" status="норма">135</test>
    <test name="Глюкоза" status="вище норми">8.7</test>
    <test name="Холестерин" status="норма">4.9</test>
  </tests>
</examination>
""";

XmlSerializer xs = new XmlSerializer(typeof(ExamRecord));

// Десеріалізація
using StringReader sr = new StringReader(xmlData);
ExamRecord? exam = (ExamRecord?)xs.Deserialize(sr);

if (exam != null)
{
    Console.WriteLine($"Пацієнт: {exam.PatientId}");
    Console.WriteLine($"Дата: {exam.ExamDate}");
    Console.WriteLine($"Висновок: {exam.Conclusion}");
    Console.WriteLine($"Тестів: {exam.Tests.Count.ToString()}");
    foreach (TestResult t in exam.Tests)
        Console.WriteLine($"  {t.Name}: {t.Value} [{t.Status}]");
}
```

### `19-05-xmlserializer.md` — блок #6 (рядок файлу 288)

**Помилки:**
- рядок 43: Top-level statements must precede namespace and type declarations.
- рядок 40: The type or namespace name 'List<>' could not be found (are you missing a using directive or an assembly reference?)
- рядок 45: The type or namespace name 'List<>' could not be found (are you missing a using directive or an assembly reference?)
- рядок 61: 'MemoryExtensions.Count<T>(Span<T>, T)' is a method, which is not valid in the given context

**Код:**
```csharp
using System;
using System.IO;
using System.Xml.Serialization;

// Базовий клас — треба оголосити всі похідні типи
[XmlInclude(typeof(BloodTest))]
[XmlInclude(typeof(EcgRecord))]
public abstract class MedicalTest
{
    [XmlAttribute("id")]
    public string TestId { get; set; } = "";

    [XmlElement("date")]
    public string Date { get; set; } = "";
}

public class BloodTest : MedicalTest
{
    [XmlElement("hemoglobin")]
    public double Hemoglobin { get; set; }

    [XmlElement("glucose")]
    public double Glucose { get; set; }
}

public class EcgRecord : MedicalTest
{
    [XmlElement("heartRate")]
    public int HeartRate { get; set; }

    [XmlElement("rhythm")]
    public string Rhythm { get; set; } = "";
}

[XmlRoot("lab")]
public class LabContainer
{
    // XmlSerializer серіалізує через [XmlInclude] типи з xsi:type
    [XmlElement("test")]
    public List<MedicalTest> Tests { get; set; } = new();
}

LabContainer lab = new LabContainer
{
    Tests = new List<MedicalTest>
    {
        new BloodTest { TestId = "BT-001", Date = "2024-03-15", Hemoglobin = 135.0, Glucose = 5.1 },
        new EcgRecord { TestId = "EC-001", Date = "2024-03-15", HeartRate = 72, Rhythm = "Синусовий" }
    }
};

XmlSerializer xs = new XmlSerializer(typeof(LabContainer));
using StringWriter sw = new StringWriter();
xs.Serialize(sw, lab);
string xml = sw.ToString();
Console.WriteLine(xml);

// Roundtrip — читаємо назад
using StringReader sr = new StringReader(xml);
LabContainer? loaded = (LabContainer?)xs.Deserialize(sr);
Console.WriteLine($"\nЗавантажено {loaded?.Tests.Count.ToString()} тестів:");
foreach (MedicalTest t in loaded?.Tests ?? new())
    Console.WriteLine($"  [{t.GetType().Name}] {t.TestId} — {t.Date}");
```

### `19-05-xmlserializer.md` — блок #7 (рядок файлу 358)

**Помилки:**
- рядок 46: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Xml.Serialization;

[XmlRoot("wardRound")]
public class WardRoundProtocol
{
    [XmlAttribute("date")]
    public string Date { get; set; } = "";

    [XmlAttribute("physician")]
    public string Physician { get; set; } = "";

    [XmlArray("patients")]
    [XmlArrayItem("patient")]
    public List<WardPatient> Patients { get; set; } = new();
}

public class WardPatient
{
    [XmlAttribute("id")]
    public string Id { get; set; } = "";

    [XmlElement("name")]
    public string Name { get; set; } = "";

    [XmlElement("ward")]
    public string Ward { get; set; } = "";

    [XmlElement("notes")]
    public string Notes { get; set; } = "";

    [XmlElement("status")]
    public string Status { get; set; } = "";

    // Порожній конструктор обов'язковий для XmlSerializer
    public WardPatient() {}

    public WardPatient(string id, string name, string ward, string notes, string status)
    {
        Id = id; Name = name; Ward = ward; Notes = notes; Status = status;
    }
}

WardRoundProtocol protocol = new WardRoundProtocol
{
    Date      = DateTime.Now.ToString("yyyy-MM-dd"),
    Physician = "Коваленко О.В.",
    Patients  = new List<WardPatient>
    {
        new("PT-1001", "Петренко І.О.", "Терапія",     "Стан покращився, t=36.8", "задовільний"),
        new("PT-1002", "Бойко О.П.",    "Кардіологія", "ЕКГ в нормі, АТ 125/80",  "стабільний"),
        new("PT-1003", "Мороз В.І.",    "Терапія",     "Скарги на слабкість",      "спостереження"),
    }
};

XmlSerializer xs = new XmlSerializer(typeof(WardRoundProtocol));
string path = Path.Combine(Path.GetTempPath(), "ward_round.xml");

// Серіалізація у файл
using (FileStream fs = File.Create(path))
    xs.Serialize(fs, protocol);

Console.WriteLine($"Збережено ({new FileInfo(path).Length.ToString()} байт):");
Console.WriteLine(File.ReadAllText(path));

// Десеріалізація з файлу
using FileStream fsr = File.OpenRead(path);
WardRoundProtocol? loaded = (WardRoundProtocol?)xs.Deserialize(fsr);

Console.WriteLine($"\nПротокол від {loaded?.Date}, лікар: {loaded?.Physician}");
Console.WriteLine($"Пацієнтів: {loaded?.Patients.Count.ToString()}");
foreach (WardPatient p in loaded?.Patients ?? new())
    Console.WriteLine($"  [{p.Id}] {p.Name} — {p.Status}");

File.Delete(path);
```

### `20-01-vstup-do-solid.md` — блок #1 (рядок файлу 45)

**Помилки:**
- рядок 59: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── God Class — еволюція без принципів ───────────────────────────
// Спочатку клас здавався невеличким. З кожним тижнем до нього
// «дочіплювали» нову відповідальність, бо «тут вже є доступ до даних».

class ClinicManager  // 800+ рядків у реальному проекті
{
    // --- Пацієнти ---
    private List<string> _patients = new();
    public void AddPatient(string name)    { _patients.Add(name); Console.WriteLine($"Додано: {name}"); }
    public void RemovePatient(string name) { _patients.Remove(name); Console.WriteLine($"Видалено: {name}"); }
    public List<string> GetPatients()      { return _patients; }

    // --- Лікарі ---
    private List<string> _doctors = new();
    public void AddDoctor(string name)    { _doctors.Add(name); }
    public List<string> GetDoctors()      { return _doctors; }

    // --- Бронювання ---
    private List<string> _appointments = new();
    public void BookAppointment(string patient, string doctor, DateTime time)
    {
        string entry = $"{patient} → {doctor} @ {time:HH:mm}";
        _appointments.Add(entry);
        Console.WriteLine($"[Booking] Заброньовано: {entry}");
        // А ще відразу надсилаємо email — «для зручності»
        SendEmailNotification(patient, $"Ваш запис: {entry}");
    }

    // --- Email — відповідальність #3 у класі пацієнтів?! ---
    public void SendEmailNotification(string to, string message)
    {
        // У реальності — SMTP-клієнт прямо тут
        Console.WriteLine($"[Email] → {to}: {message}");
    }

    // --- Збереження у файл --- відповідальність #4 ---
    public void SaveToFile(string path)
    {
        Console.WriteLine($"[File] Зберігаю {_patients.Count} пацієнтів у {path}");
    }

    // --- Генерація звіту --- відповідальність #5 ---
    public string GenerateReport()
    {
        return $"Звіт: пацієнтів={_patients.Count}, лікарів={_doctors.Count}, записів={_appointments.Count}";
    }

    // --- Рахунки --- відповідальність #6 ---
    public decimal CalculateBilling(string patient)
    {
        return _appointments.FindAll(a => a.StartsWith(patient)).Count * 500m;
    }
}

// ─── Використання — виглядає зручно, але... ──────────────────────
var clinic = new ClinicManager();
clinic.AddDoctor("Петренко І.О.");
clinic.AddPatient("Бойко Олена");
clinic.BookAppointment("Бойко Олена", "Петренко І.О.", DateTime.Now.AddHours(2));
Console.WriteLine(clinic.GenerateReport());
Console.WriteLine($"Рахунок: {clinic.CalculateBilling("Бойко Олена").ToString()} грн");
clinic.SaveToFile("clinic.dat");
```

### `20-01-vstup-do-solid.md` — блок #2 (рядок файлу 129)

**Помилки:**
- рядок 57: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

// Спрощена модель щільно зв'язаної системи
// де кожен компонент знає про внутрішній формат інших

class TightClinicSystem
{
    private List<string> _log = new(); // формат: "YYYY-MM-DD|PATIENT|DOCTOR|STATUS"

    public void Book(string patient, string doctor)
    {
        // Ключове рішення: формат рядка "зашитий" усюди
        string entry = $"{DateTime.Today:yyyy-MM-dd}|{patient}|{doctor}|ACTIVE";
        _log.Add(entry);
        Console.WriteLine($"[Book] {entry}");
    }

    // Цей метод знає про формат "yyyy-MM-dd|..." — зв'язаність!
    public int CountByDoctor(string doctor)
    {
        int count = 0;
        foreach (var e in _log)
        {
            string[] parts = e.Split('|'); // очікує саме цей формат
            if (parts.Length >= 3 && parts[2] == doctor) count++;
        }
        return count;
    }

    // Цей метод теж знає про формат — ще одна зв'язаність
    public void ExportReport()
    {
        Console.WriteLine("[Report] Активні записи:");
        foreach (var e in _log)
        {
            string[] parts = e.Split('|'); // знову той самий формат
            if (parts.Length >= 4 && parts[3] == "ACTIVE")
                Console.WriteLine($"  {parts[0]}: {parts[1]} → {parts[2]}");
        }
    }

    // Ще один компонент із залежністю від формату
    public bool HasActiveAppointment(string patient)
    {
        foreach (var e in _log)
        {
            string[] parts = e.Split('|'); // четверта залежність від формату
            if (parts.Length >= 4 && parts[1] == patient && parts[3] == "ACTIVE")
                return true;
        }
        return false;
    }
}

var sys = new TightClinicSystem();
sys.Book("Мороз Василь", "Петренко І.О.");
sys.Book("Бойко Олена", "Коваленко М.А.");
sys.ExportReport();
Console.WriteLine($"Лікар Петренко: {sys.CountByDoctor("Петренко І.О.").ToString()} записів");
Console.WriteLine($"Мороз активний: {sys.HasActiveAppointment("Мороз Василь").ToString()}");

// Тепер змінимо формат рядка на "DD.MM.YYYY;PATIENT;DOCTOR;STATUS"
// → треба виправити Book, CountByDoctor, ExportReport, HasActiveAppointment
// → чотири місця, і це лише в одному класі!
Console.WriteLine("\n[Проблема] Зміна формату = 4 місця для редагування у цьому класі");
Console.WriteLine("           У реальному проекті таких місць можуть бути десятки");
```

### `20-02-srp.md` — блок #1 (рядок файлу 31)

**Помилки:**
- рядок 77: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── ПОРУШЕННЯ SRP ──────────────────────────────────────────────────
// Три відповідальності: бізнес-логіка + збереження + сповіщення

class AppointmentManager_Bad
{
    private List<(string Patient, string Doctor, DateTime Time, string Status)> _data = new();

    // ── Відповідальність 1: Бізнес-логіка бронювання ──────────────
    // Актор: відділ прийому — змінює правила запису

    public bool Book(string patient, string doctor, DateTime time)
    {
        // Перевірка: лікар не зайнятий у цей час
        foreach (var a in _data)
            if (a.Doctor == doctor && a.Time == time && a.Status == "Active")
            {
                Console.WriteLine($"[Book] ВІДМОВА: {doctor} зайнятий о {time:HH:mm}");
                return false;
            }

        _data.Add((patient, doctor, time, "Active"));
        Console.WriteLine($"[Book] Заброньовано: {patient} → {doctor} о {time:HH:mm}");

        // Тут же — зберігаємо і сповіщаємо. Все в одному методі.
        SaveToDatabase(patient, doctor, time);
        SendEmailConfirmation(patient, doctor, time);
        return true;
    }

    public void Cancel(string patient, string doctor)
    {
        for (int i = 0; i < _data.Count; i++)
        {
            var a = _data[i];
            if (a.Patient == patient && a.Doctor == doctor && a.Status == "Active")
            {
                _data[i] = (a.Patient, a.Doctor, a.Time, "Cancelled");
                Console.WriteLine($"[Cancel] Скасовано: {patient} у {doctor}");
                SendCancellationAlert(patient);
                return;
            }
        }
    }

    // ── Відповідальність 2: Збереження даних ──────────────────────
    // Актор: ІТ-відділ — змінює коли переходять на нову БД

    private void SaveToDatabase(string patient, string doctor, DateTime time)
    {
        // Реально: SQL INSERT або ORM-виклик
        Console.WriteLine($"[DB] INSERT: {patient}, {doctor}, {time:yyyy-MM-dd HH:mm}");
    }

    public void LoadFromDatabase()
    {
        // Реально: SELECT з таблиці appointments
        Console.WriteLine("[DB] SELECT * FROM appointments");
    }

    // ── Відповідальність 3: Сповіщення ────────────────────────────
    // Актор: відділ маркетингу — змінює коли хочуть SMS замість email

    private void SendEmailConfirmation(string patient, string doctor, DateTime time)
    {
        Console.WriteLine($"[Email] → {patient}: Запис до {doctor} о {time:HH:mm} підтверджено");
    }

    private void SendCancellationAlert(string patient)
    {
        Console.WriteLine($"[Email] → {patient}: Ваш запис скасовано");
    }
}

var manager = new AppointmentManager_Bad();
manager.Book("Мороз Василь", "Петренко І.О.", DateTime.Today.AddHours(10));
manager.Book("Бойко Олена",  "Петренко І.О.", DateTime.Today.AddHours(10)); // зайнято
manager.Cancel("Мороз Василь", "Петренко І.О.");
```

### `20-02-srp.md` — блок #2 (рядок файлу 122)

**Помилки:**
- рядок 114: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── ПРАВИЛЬНО: кожен клас — одна відповідальність ─────────────────

// ── 1. Тільки бізнес-логіка ────────────────────────────────────────
class AppointmentService
{
    private List<(string Patient, string Doctor, DateTime Time, string Status)> _appointments = new();

    // Повертає true/false — і нічого більше. Не зберігає, не надсилає.
    public bool Book(string patient, string doctor, DateTime time)
    {
        foreach (var a in _appointments)
            if (a.Doctor == doctor && a.Time == time && a.Status == "Active")
                return false; // слот зайнятий

        _appointments.Add((patient, doctor, time, "Active"));
        return true;
    }

    public bool Cancel(string patient, string doctor)
    {
        for (int i = 0; i < _appointments.Count; i++)
        {
            var a = _appointments[i];
            if (a.Patient == patient && a.Doctor == doctor && a.Status == "Active")
            {
                _appointments[i] = (a.Patient, a.Doctor, a.Time, "Cancelled");
                return true;
            }
        }
        return false;
    }

    public int CountActive(string doctor) =>
        _appointments.FindAll(a => a.Doctor == doctor && a.Status == "Active").Count;
}

// ── 2. Тільки збереження ───────────────────────────────────────────
class AppointmentRepository
{
    // Лише відповідальність перед ІТ-відділом: зберегти і отримати.
    // Ніякої бізнес-логіки, ніяких email.

    public void Save(string patient, string doctor, DateTime time)
    {
        Console.WriteLine($"[DB] Збережено: {patient} → {doctor} @ {time:HH:mm}");
    }

    public void UpdateStatus(string patient, string doctor, string status)
    {
        Console.WriteLine($"[DB] Статус змінено: {patient}/{doctor} → {status}");
    }
}

// ── 3. Тільки сповіщення ───────────────────────────────────────────
class AppointmentNotifier
{
    // Лише відповідальність перед маркетингом: надіслати повідомлення.
    // Хочуть SMS — змінюємо тільки цей клас. Решта не торкається.

    public void SendConfirmation(string patient, string doctor, DateTime time)
    {
        Console.WriteLine($"[Email] → {patient}: Запис до {doctor} о {time:HH:mm} підтверджено");
    }

    public void SendCancellation(string patient)
    {
        Console.WriteLine($"[Email] → {patient}: Ваш запис скасовано");
    }
}

// ── Оркестратор (координує три класи) ─────────────────────────────
class ClinicCoordinator
{
    private readonly AppointmentService    _service;
    private readonly AppointmentRepository _repo;
    private readonly AppointmentNotifier   _notifier;

    public ClinicCoordinator(AppointmentService s, AppointmentRepository r, AppointmentNotifier n)
    {
        _service  = s;
        _repo     = r;
        _notifier = n;
    }

    public void Book(string patient, string doctor, DateTime time)
    {
        if (!_service.Book(patient, doctor, time))
        {
            Console.WriteLine($"[Clinic] {doctor} зайнятий о {time:HH:mm} — запис неможливий");
            return;
        }
        _repo.Save(patient, doctor, time);
        _notifier.SendConfirmation(patient, doctor, time);
        Console.WriteLine($"[Clinic] Запис успішний: {patient} → {doctor}");
    }

    public void Cancel(string patient, string doctor)
    {
        if (!_service.Cancel(patient, doctor))
        {
            Console.WriteLine($"[Clinic] Активний запис не знайдено");
            return;
        }
        _repo.UpdateStatus(patient, doctor, "Cancelled");
        _notifier.SendCancellation(patient);
        Console.WriteLine($"[Clinic] Запис скасовано: {patient}");
    }
}

// ── Використання ───────────────────────────────────────────────────
var coordinator = new ClinicCoordinator(
    new AppointmentService(),
    new AppointmentRepository(),
    new AppointmentNotifier()
);

coordinator.Book("Мороз Василь", "Петренко І.О.", DateTime.Today.AddHours(10));
coordinator.Book("Бойко Олена",  "Петренко І.О.", DateTime.Today.AddHours(10)); // зайнято
coordinator.Cancel("Мороз Василь", "Петренко І.О.");
```

### `20-02-srp.md` — блок #3 (рядок файлу 258)

**Помилки:**
- рядок 23: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// Тест AppointmentService — без бази даних і без email
class AppointmentService_Testable
{
    private List<(string Patient, string Doctor, DateTime Time, string Status)> _appointments = new();

    public bool Book(string patient, string doctor, DateTime time)
    {
        foreach (var a in _appointments)
            if (a.Doctor == doctor && a.Time == time && a.Status == "Active")
                return false;
        _appointments.Add((patient, doctor, time, "Active"));
        return true;
    }

    public int CountActiveForDoctor(string doctor) =>
        _appointments.FindAll(a => a.Doctor == doctor && a.Status == "Active").Count;
}

// ─── Симуляція юніт-тестів ─────────────────────────────────────────
void Assert(bool condition, string testName)
{
    Console.WriteLine(condition ? $"✓ PASS: {testName}" : $"✗ FAIL: {testName}");
}

var svc = new AppointmentService_Testable();
var time1 = new DateTime(2024, 3, 15, 10, 0, 0);
var time2 = new DateTime(2024, 3, 15, 11, 0, 0);

// Тест 1: успішне бронювання
bool result1 = svc.Book("Мороз В.", "Петренко", time1);
Assert(result1 == true, "Book — успішне бронювання");

// Тест 2: подвійне бронювання того самого слоту
bool result2 = svc.Book("Бойко О.", "Петренко", time1);
Assert(result2 == false, "Book — слот уже зайнятий");

// Тест 3: різний час — обидва успішні
bool result3 = svc.Book("Бойко О.", "Петренко", time2);
Assert(result3 == true, "Book — інший час, успішно");

// Тест 4: лічильник активних записів
int count = svc.CountActiveForDoctor("Петренко");
Assert(count == 2, $"CountActive — очікуємо 2, маємо {count.ToString()}");
```

### `20-02-srp.md` — блок #4 (рядок файлу 313)

**Помилки:**
- рядок 48: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

// Клас Patient — відповідальність: доменна модель пацієнта
// Причина для зміни: ТІЛЬКИ зміна в бізнес-правилах щодо пацієнта
class Patient
{
    public int    Id          { get; }
    public string FirstName   { get; private set; }
    public string LastName    { get; private set; }
    public DateTime DateOfBirth { get; }
    public string BloodType   { get; }

    public Patient(int id, string firstName, string lastName,
                   DateTime dateOfBirth, string bloodType)
    {
        if (string.IsNullOrWhiteSpace(firstName))
            throw new ArgumentException("Ім'я не може бути порожнім", nameof(firstName));
        if (string.IsNullOrWhiteSpace(lastName))
            throw new ArgumentException("Прізвище не може бути порожнім", nameof(lastName));
        if (dateOfBirth > DateTime.Today)
            throw new ArgumentException("Дата народження не може бути в майбутньому", nameof(dateOfBirth));

        Id          = id;
        FirstName   = firstName;
        LastName    = lastName;
        DateOfBirth = dateOfBirth;
        BloodType   = bloodType;
    }

    // Доменна поведінка: вік — це бізнес-знання про пацієнта
    public int Age => (DateTime.Today - DateOfBirth).Days / 365;

    // Доменна поведінка: чи є пацієнт неповнолітнім
    public bool IsMinor => Age < 18;

    // Форматування — частина відповідальності «представлення пацієнта»
    public string FullName => $"{LastName} {FirstName}";

    public override string ToString() =>
        $"{FullName}, {Age.ToString()} р., група крові: {BloodType}";
}

// Що НЕ має бути в Patient:
// ✗ SaveToDatabase()     — це відповідальність PatientRepository
// ✗ SendWelcomeEmail()   — це відповідальність PatientNotifier
// ✗ GenerateReport()     — це відповідальність ReportService

var patient = new Patient(1, "Іван", "Петренко", new DateTime(1985, 6, 20), "A(II)+");
Console.WriteLine(patient.ToString());
Console.WriteLine($"Вік: {patient.Age.ToString()} р.");
Console.WriteLine($"Неповнолітній: {patient.IsMinor.ToString()}");
```

### `20-02-srp.md` — блок #5 (рядок файлу 385)

**Помилки:**
- рядок 43: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── Демонстрація: великий, але правильний клас ────────────────────
// PatientRegistry відповідає за одне: реєстр пацієнтів у межах клініки.
// Багато методів — одна вісь змін: бізнес-правила щодо реєстру.

class PatientRegistry
{
    private Dictionary<int, string> _patients = new(); // id → ПІБ
    private int _nextId = 1;

    public int Register(string fullName)
    {
        int id = _nextId++;
        _patients[id] = fullName;
        Console.WriteLine($"[Registry] Зареєстровано #{id.ToString()}: {fullName}");
        return id;
    }

    public bool Deregister(int id)
    {
        bool removed = _patients.Remove(id);
        if (removed) Console.WriteLine($"[Registry] Видалено #{id.ToString()}");
        return removed;
    }

    public string? FindById(int id) =>
        _patients.TryGetValue(id, out string? name) ? name : null;

    public bool Exists(int id) => _patients.ContainsKey(id);

    public int Count => _patients.Count;

    public void PrintAll()
    {
        Console.WriteLine($"[Registry] Пацієнтів: {_patients.Count.ToString()}");
        foreach (var (id, name) in _patients)
            Console.WriteLine($"  #{id.ToString()}: {name}");
    }
}

var registry = new PatientRegistry();
int id1 = registry.Register("Мороз Василь Іванович");
int id2 = registry.Register("Бойко Олена Петрівна");
int id3 = registry.Register("Коваль Михайло Андрійович");
registry.PrintAll();

Console.WriteLine($"\nПошук #{id1.ToString()}: {registry.FindById(id1)}");
registry.Deregister(id2);
Console.WriteLine($"Пацієнтів після видалення: {registry.Count.ToString()}");
```

### `20-03-ocp.md` — блок #1 (рядок файлу 23)

**Помилки:**
- рядок 61: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

// ─── ПОРУШЕННЯ OCP ──────────────────────────────────────────────────
// Щоразу, як з'являється новий тип прийому, треба відкривати
// CostCalculator і дописувати новий case. Це пряме порушення:
// клас не закритий для модифікації.

enum AppointmentType { Regular, Urgent, Specialist, VIP }

class Appointment_Bad
{
    public string       PatientName { get; set; } = "";
    public AppointmentType Type     { get; set; }
    public int          DurationMin { get; set; }
}

class CostCalculator_Bad
{
    // Цей метод треба відкривати при кожному новому типі прийому
    public decimal CalculateCost(Appointment_Bad appt)
    {
        switch (appt.Type)
        {
            case AppointmentType.Regular:
                // 500 грн базова + 5 грн за хвилину понад 30
                decimal regular = 500m;
                if (appt.DurationMin > 30)
                    regular += (appt.DurationMin - 30) * 5m;
                return regular;

            case AppointmentType.Urgent:
                // Базова × 1.6 (коефіцієнт терміновості)
                return 500m * 1.6m;

            case AppointmentType.Specialist:
                // Фіксована вартість без урахування тривалості
                return 1200m;

            // ← Новий тип VIP: треба ВІДКРИТИ цей файл і дописати case
            // ← Ризик: можна випадково зачепити Regular або Urgent
            // ← Цей switch дублюється в GenerateReport(), in BillingService()...

            default:
                return 0m;
        }
    }

    // Другий метод з тим самим switch — OCP-порушення множиться
    public string GetTypeName(Appointment_Bad appt)
    {
        return appt.Type switch
        {
            AppointmentType.Regular    => "Первинний прийом",
            AppointmentType.Urgent     => "Терміновий прийом",
            AppointmentType.Specialist => "Консультація спеціаліста",
            _                          => "Невідомий тип",
        };
    }
}

var calc = new CostCalculator_Bad();

var appts = new[]
{
    new Appointment_Bad { PatientName = "Мороз В.",   Type = AppointmentType.Regular,    DurationMin = 45 },
    new Appointment_Bad { PatientName = "Бойко О.",   Type = AppointmentType.Urgent,     DurationMin = 20 },
    new Appointment_Bad { PatientName = "Коваль М.",  Type = AppointmentType.Specialist, DurationMin = 60 },
};

foreach (var a in appts)
{
    decimal cost = calc.CalculateCost(a);
    string name  = calc.GetTypeName(a);
    Console.WriteLine($"{a.PatientName}: {name} — {cost.ToString()} грн");
}
```

### `20-03-ocp.md` — блок #2 (рядок файлу 109)

**Помилки:**
- рядок 99: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── ПРАВИЛЬНО: OCP через абстракцію ───────────────────────────────

// Абстракція: контракт для будь-якого типу прийому
interface IAppointmentType
{
    string TypeName    { get; }
    decimal CalculateCost(int durationMinutes);
    string GetDescription();
}

// ─── Конкретні реалізації — окремі класи, не switch ────────────────

class RegularAppointment : IAppointmentType
{
    public string TypeName => "Первинний прийом";

    public decimal CalculateCost(int durationMinutes)
    {
        // 500 базова + 5 грн за кожну хвилину понад 30
        decimal cost = 500m;
        if (durationMinutes > 30)
            cost += (durationMinutes - 30) * 5m;
        return cost;
    }

    public string GetDescription() => "Базовий прийом у загальноклінічного лікаря";
}

class UrgentAppointment : IAppointmentType
{
    public string TypeName => "Терміновий прийом";

    public decimal CalculateCost(int durationMinutes)
    {
        // Коефіцієнт терміновості ×1.6 до базової
        return 500m * 1.6m;
    }

    public string GetDescription() => "Позачерговий прийом при загостренні стану";
}

class SpecialistAppointment : IAppointmentType
{
    private readonly string _speciality;

    public SpecialistAppointment(string speciality) => _speciality = speciality;

    public string TypeName => $"Консультація: {_speciality}";

    public decimal CalculateCost(int durationMinutes)
    {
        // Фіксована вартість спеціалістів — 1200 грн
        return 1200m;
    }

    public string GetDescription() => $"Консультація спеціаліста: {_speciality}";
}

// ─── Новий тип: VIP — НЕ ТОРКАЄМОСЬ існуючих класів ───────────────
class VipAppointment : IAppointmentType
{
    public string TypeName => "VIP-обслуговування";

    public decimal CalculateCost(int durationMinutes)
    {
        // Погодинна ставка: 150 грн/хв, мінімум 60 хв
        int billableMinutes = Math.Max(durationMinutes, 60);
        return billableMinutes * 150m;
    }

    public string GetDescription() => "Індивідуальне обслуговування у VIP-кабінеті";
}

// ─── Калькулятор: ЗАКРИТИЙ для модифікації, але відкритий для розширення ──
class CostCalculator
{
    // Метод не знає про конкретні типи — лише про абстракцію
    public decimal Calculate(IAppointmentType type, int durationMinutes)
    {
        return type.CalculateCost(durationMinutes);
    }

    public void PrintInvoice(IAppointmentType type, string patient, int durationMinutes)
    {
        decimal cost = type.CalculateCost(durationMinutes);
        Console.WriteLine($"Пацієнт:    {patient}");
        Console.WriteLine($"Тип:        {type.TypeName}");
        Console.WriteLine($"Опис:       {type.GetDescription()}");
        Console.WriteLine($"Тривалість: {durationMinutes.ToString()} хв");
        Console.WriteLine($"Вартість:   {cost.ToString()} грн");
        Console.WriteLine(new string('-', 40));
    }
}

// ─── Використання ──────────────────────────────────────────────────
var calculator = new CostCalculator();

// Список прийомів: різні типи, але один і той самий CostCalculator
var appointments = new List<(string Patient, IAppointmentType Type, int Duration)>
{
    ("Мороз Василь",   new RegularAppointment(),                 45),
    ("Бойко Олена",    new UrgentAppointment(),                  20),
    ("Коваль Михайло", new SpecialistAppointment("Кардіологія"), 60),
    ("Сидоренко Тетяна",new VipAppointment(),                   90),
};

foreach (var (patient, type, duration) in appointments)
    calculator.PrintInvoice(type, patient, duration);
```

### `20-03-ocp.md` — блок #3 (рядок файлу 237)

**Помилки:**
- рядок 58: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── Strategy Pattern: алгоритм знижки ─────────────────────────────

interface IDiscountStrategy
{
    decimal Apply(decimal originalCost);
    string Description { get; }
}

class NoDiscount : IDiscountStrategy
{
    public string Description => "Без знижки";
    public decimal Apply(decimal cost) => cost;
}

class PercentageDiscount : IDiscountStrategy
{
    private readonly int _percent;
    public PercentageDiscount(int percent) => _percent = percent;
    public string Description => $"Знижка {_percent.ToString()}%";
    public decimal Apply(decimal cost) => cost * (1 - _percent / 100m);
}

class FlatDiscount : IDiscountStrategy
{
    private readonly decimal _amount;
    public FlatDiscount(decimal amount) => _amount = amount;
    public string Description => $"Знижка {_amount.ToString()} грн";
    public decimal Apply(decimal cost) => Math.Max(0, cost - _amount);
}

// Новий тип знижки — без торкання до Billing ───────────────────────
class SeasonalDiscount : IDiscountStrategy
{
    private readonly int _percent;
    private readonly string _seasonName;
    public SeasonalDiscount(string season, int pct) { _seasonName = season; _percent = pct; }
    public string Description => $"Сезонна знижка «{_seasonName}» — {_percent.ToString()}%";
    public decimal Apply(decimal cost) => cost * (1 - _percent / 100m);
}

// BillingService: закритий для модифікації, відкритий для нових знижок
class BillingService
{
    public void GenerateBill(string patient, decimal baseCost, IDiscountStrategy discount)
    {
        decimal final = discount.Apply(baseCost);
        Console.WriteLine($"Пацієнт: {patient}");
        Console.WriteLine($"  Базова вартість:  {baseCost.ToString()} грн");
        Console.WriteLine($"  {discount.Description}");
        Console.WriteLine($"  До сплати:        {final.ToString("F2")} грн");
        Console.WriteLine();
    }
}

var billing = new BillingService();
billing.GenerateBill("Мороз Василь",    1200m, new NoDiscount());
billing.GenerateBill("Пенсіонер Іван",  1200m, new PercentageDiscount(30));
billing.GenerateBill("Абонемент Олена", 1200m, new FlatDiscount(300m));
billing.GenerateBill("Бойко Тетяна",   1200m, new SeasonalDiscount("Літо", 15));
```

### `20-03-ocp.md` — блок #4 (рядок файлу 308)

**Помилки:**
- рядок 65: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

// ─── Template Method: базовий алгоритм закрито, кроки — відкрито ───

abstract class MedicalExamination
{
    // Шаблонний метод: визначає порядок дій — закритий
    public void Conduct(string patient)
    {
        Console.WriteLine($"\n=== Обстеження: {patient} ===");
        RegisterPatient(patient);
        PerformExamination(patient);   // абстрактний — відкритий для підкласів
        RecordResults(patient);
        ScheduleFollowUp(patient);     // може бути перевизначений
        Console.WriteLine($"=== Завершено ===");
    }

    private void RegisterPatient(string patient)
        => Console.WriteLine($"[Reception] Реєстрація: {patient}");

    // Відкритий для розширення — підклас визначає конкретне обстеження
    protected abstract void PerformExamination(string patient);

    private void RecordResults(string patient)
        => Console.WriteLine($"[Records] Результати внесено до картки {patient}");

    // Virtual: підклас може перевизначити, але не зобов'язаний
    protected virtual void ScheduleFollowUp(string patient)
        => Console.WriteLine($"[Schedule] Повторний огляд через 4 тижні");
}

// Кожен підклас розширює алгоритм без зміни базового класу
class CardiologyExam : MedicalExamination
{
    protected override void PerformExamination(string patient)
    {
        Console.WriteLine($"[Cardio] ЕКГ, ехокардіографія, вимірювання тиску: {patient}");
    }

    protected override void ScheduleFollowUp(string patient)
        => Console.WriteLine($"[Schedule] Кардіологічний контроль через 2 тижні");
}

class NeurologyExam : MedicalExamination
{
    protected override void PerformExamination(string patient)
    {
        Console.WriteLine($"[Neuro] МРТ, рефлекси, когнітивні тести: {patient}");
    }
    // ScheduleFollowUp не перевизначено — використовується базова реалізація
}

// Новий тип обстеження — без зміни MedicalExamination ─────────────
class LabExam : MedicalExamination
{
    protected override void PerformExamination(string patient)
    {
        Console.WriteLine($"[Lab] Аналіз крові, сечі, біохімія: {patient}");
    }

    protected override void ScheduleFollowUp(string patient)
        => Console.WriteLine($"[Schedule] Результати готові через 2 дні");
}

new CardiologyExam().Conduct("Мороз Василь");
new NeurologyExam().Conduct("Бойко Олена");
new LabExam().Conduct("Коваль Михайло");
```

### `20-03-ocp.md` — блок #5 (рядок файлу 394)

**Помилки:**
- рядок 54: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── Демонстрація: поліморфна обробка списку через OCP ─────────────

interface IReportFormatter
{
    string Format(string title, List<string> rows);
}

class PlainTextFormatter : IReportFormatter
{
    public string Format(string title, List<string> rows)
    {
        var sb = new System.Text.StringBuilder();
        sb.AppendLine($"=== {title} ===");
        foreach (var row in rows) sb.AppendLine($"  {row}");
        return sb.ToString();
    }
}

class CsvFormatter : IReportFormatter
{
    public string Format(string title, List<string> rows)
    {
        var sb = new System.Text.StringBuilder();
        sb.AppendLine($"\"Звіт\",\"{title}\"");
        foreach (var row in rows) sb.AppendLine($"\"{row}\"");
        return sb.ToString();
    }
}

// Новий формат — без зміни ReportPrinter
class MarkdownFormatter : IReportFormatter
{
    public string Format(string title, List<string> rows)
    {
        var sb = new System.Text.StringBuilder();
        sb.AppendLine($"## {title}");
        foreach (var row in rows) sb.AppendLine($"- {row}");
        return sb.ToString();
    }
}

// ReportPrinter: закритий — ніколи не зміниться при нових форматах
class ReportPrinter
{
    public void Print(IReportFormatter formatter, string title, List<string> rows)
    {
        Console.WriteLine(formatter.Format(title, rows));
    }
}

var data = new List<string>
{
    "Петренко І.О. — 12 прийомів", "Коваленко М.А. — 9 прийомів", "Бойко О.Р. — 7 прийомів"
};

var printer = new ReportPrinter();
printer.Print(new PlainTextFormatter(), "Рейтинг лікарів", data);
printer.Print(new CsvFormatter(),       "Рейтинг лікарів", data);
printer.Print(new MarkdownFormatter(),  "Рейтинг лікарів", data);
```

### `20-04-lsp.md` — блок #1 (рядок файлу 35)

**Помилки:**
- рядок 31: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

// ─── Класичний приклад порушення LSP ───────────────────────────────

class Rectangle
{
    public virtual int Width  { get; set; }
    public virtual int Height { get; set; }

    public int Area() => Width * Height;

    public override string ToString() => $"Rectangle({Width.ToString()}×{Height.ToString()})";
}

class Square : Rectangle
{
    // Квадрат примушує Width == Height — але ламає контракт Rectangle!
    public override int Width
    {
        set { base.Width = value; base.Height = value; } // змінює обидва
        get => base.Width;
    }
    public override int Height
    {
        set { base.Width = value; base.Height = value; } // змінює обидва
        get => base.Height;
    }
}

// Код, що працює з Rectangle — нічого не знає про Square
void SetAndPrint(Rectangle r)
{
    r.Width  = 5;
    r.Height = 3;
    // Очікуємо: 5×3 = 15
    Console.WriteLine($"{r}: площа = {r.Area().ToString()}");
}

var rect = new Rectangle();
SetAndPrint(rect);   // Rectangle(5×3): площа = 15 ✓

var sq = new Square();
SetAndPrint(sq);     // Square(3×3): площа = 9  ✗ (очікувалось 15!)
// LSP порушено: підстановка Square замість Rectangle дає неочікуваний результат
```

### `20-04-lsp.md` — блок #2 (рядок файлу 90)

**Помилки:**
- рядок 60: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── ПОРУШЕННЯ LSP ──────────────────────────────────────────────────

abstract class MedicalRecord
{
    public int     Id        { get; protected set; }
    public int     PatientId { get; protected set; }
    public DateTime Date     { get; protected set; }
    protected List<string> _diagnoses = new();

    protected MedicalRecord(int id, int patientId)
    {
        Id = id; PatientId = patientId; Date = DateTime.Today;
    }

    // Контракт: метод доступний і виконує додавання
    public virtual void AddDiagnosis(string code)
    {
        _diagnoses.Add(code);
        Console.WriteLine($"[Record #{Id.ToString()}] Діагноз додано: {code}");
    }

    public virtual string GetSummary() =>
        $"Record #{Id.ToString()}, пацієнт #{PatientId.ToString()}, " +
        $"діагнозів: {_diagnoses.Count.ToString()}";
}

// Звичайний підклас — дотримується контракту ───────────────────────
class ActiveDiagnosis : MedicalRecord
{
    public string DiagnosisCode { get; private set; }

    public ActiveDiagnosis(int id, int patientId, string code) : base(id, patientId)
    {
        DiagnosisCode = code;
        _diagnoses.Add(code); // власний діагноз
    }

    // Розширює базовий клас, не порушуючи контракту
    public override string GetSummary() =>
        base.GetSummary() + $" | Основний: {DiagnosisCode}";
}

// ⚠ Підклас, що ПОРУШУЄ LSP ────────────────────────────────────────
class ReadOnlyRecord : MedicalRecord
{
    public ReadOnlyRecord(int id, int patientId) : base(id, patientId) { }

    // Порушення: посилює передумову до «ніколи не виклич мене»
    public override void AddDiagnosis(string code)
    {
        // Клієнт очікує: OK. Отримує: виняток!
        throw new InvalidOperationException("Цей запис у режимі тільки для читання");
    }
}

// ─── Клієнтський код — не знає про ReadOnlyRecord ──────────────────
void ProcessRecord(MedicalRecord record, string diagCode)
{
    Console.WriteLine($"Обробка: {record.GetSummary()}");
    record.AddDiagnosis(diagCode); // очікує: OK для будь-якого MedicalRecord
}

var active = new ActiveDiagnosis(1, 101, "J06.9");
ProcessRecord(active, "I10"); // ✓ Працює

var archived = new ReadOnlyRecord(2, 102);
try
{
    ProcessRecord(archived, "E11.9"); // ✗ Вибух у runtime!
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"[Помилка] {ex.Message}");
    Console.WriteLine("LSP порушено: підстановка ReadOnlyRecord зламала клієнтський код");
}
```

### `20-04-lsp.md` — блок #3 (рядок файлу 177)

**Помилки:**
- рядок 70: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── ПРАВИЛЬНО: ієрархія відповідає LSP ────────────────────────────

// Мінімальний контракт: тільки те, що виконає КОЖЕН нащадок
interface IMedicalRecord
{
    int     Id        { get; }
    int     PatientId { get; }
    DateTime Date     { get; }
    string  GetSummary();
}

// Розширений контракт: тільки для записів, що підтримують модифікацію
interface IEditableMedicalRecord : IMedicalRecord
{
    void AddDiagnosis(string code);
    void UpdateNotes(string notes);
}

// ── Активний запис: реалізує обидва інтерфейси ─────────────────────
class ActiveRecord : IEditableMedicalRecord
{
    private List<string> _diagnoses = new();
    private string _notes = "";

    public int      Id        { get; }
    public int      PatientId { get; }
    public DateTime Date      { get; } = DateTime.Today;

    public ActiveRecord(int id, int patientId) { Id = id; PatientId = patientId; }

    public void AddDiagnosis(string code)
    {
        _diagnoses.Add(code);
        Console.WriteLine($"[Record #{Id.ToString()}] Діагноз: {code}");
    }

    public void UpdateNotes(string notes)
    {
        _notes = notes;
        Console.WriteLine($"[Record #{Id.ToString()}] Нотатки оновлено");
    }

    public string GetSummary() =>
        $"ActiveRecord #{Id.ToString()}, пацієнт #{PatientId.ToString()}, " +
        $"діагнозів: {_diagnoses.Count.ToString()}";
}

// ── Архівний запис: реалізує лише IMedicalRecord — і це чесно ──────
class ArchivedRecord : IMedicalRecord
{
    private readonly string _summary;

    public int      Id        { get; }
    public int      PatientId { get; }
    public DateTime Date      { get; }

    public ArchivedRecord(int id, int patientId, DateTime date, string summary)
    {
        Id = id; PatientId = patientId; Date = date; _summary = summary;
    }

    public string GetSummary() => $"[АРХІВ] {_summary}";
    // Немає AddDiagnosis — і клієнт про це знає через тип
}

// ── Клієнтський код: чіткі контракти ───────────────────────────────
void DisplayRecord(IMedicalRecord record)
{
    // Може лише читати — LSP гарантований
    Console.WriteLine(record.GetSummary());
}

void EditRecord(IEditableMedicalRecord record, string code)
{
    // Може редагувати — LSP гарантований: тільки EditableRecord тут буде
    record.AddDiagnosis(code);
}

var active   = new ActiveRecord(1, 101);
var archived = new ArchivedRecord(2, 102, new DateTime(2023, 5, 10), "Хронічна гіпертонія");

DisplayRecord(active);    // ✓
DisplayRecord(archived);  // ✓
EditRecord(active, "J06.9"); // ✓

// ArchivedRecord компілятор просто не дозволить передати в EditRecord
// EditRecord(archived, "I10"); // ← помилка компіляції, не runtime!
Console.WriteLine("LSP дотримано: помилка виявляється на етапі компіляції");
```

### `20-04-lsp.md` — блок #4 (рядок файлу 287)

**Помилки:**
- рядок 68: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

// ─── Демонстрація правильно побудованої ієрархії MedicalRecord ─────

abstract class MedicalRecordBase
{
    public int      Id        { get; }
    public int      PatientId { get; }
    public int      DoctorId  { get; }
    public DateTime Date      { get; }
    public string   Notes     { get; protected set; }

    protected MedicalRecordBase(int id, int patientId, int doctorId, string notes)
    {
        if (id <= 0)        throw new ArgumentException("Id має бути додатнім");
        if (patientId <= 0) throw new ArgumentException("PatientId має бути додатнім");
        Id = id; PatientId = patientId; DoctorId = doctorId;
        Date = DateTime.Today; Notes = notes;
    }

    // Контракт: завжди повертає рядок з описом (ніколи null)
    public abstract string GetSummary();

    // Контракт: завжди повертає рядок — "Активний" або "Неактивний"
    public virtual string GetStatus() => "Активний";
}

class DiagnosisRecord : MedicalRecordBase
{
    public string DiagnosisCode { get; }
    public bool   IsChronic     { get; }

    public DiagnosisRecord(int id, int patientId, int doctorId,
                           string code, bool isChronic, string notes)
        : base(id, patientId, doctorId, notes)
    {
        DiagnosisCode = code; IsChronic = isChronic;
    }

    // Виконує контракт: повертає не-null рядок
    public override string GetSummary() =>
        $"Діагноз [{DiagnosisCode}]{(IsChronic ? " (хронічний)" : "")} — {Notes}";
}

class PrescriptionRecord : MedicalRecordBase
{
    public string   MedicationName { get; }
    public int      DurationDays   { get; }
    public DateTime ExpiresAt      { get; }

    public PrescriptionRecord(int id, int patientId, int doctorId,
                               string medication, int duration, string notes)
        : base(id, patientId, doctorId, notes)
    {
        MedicationName = medication; DurationDays = duration;
        ExpiresAt = DateTime.Today.AddDays(duration);
    }

    public override string GetSummary() =>
        $"Рецепт: {MedicationName}, {DurationDays.ToString()} днів — {Notes}";

    // Розширює постумову: уточнює статус (не звужує, не ламає)
    public override string GetStatus() =>
        ExpiresAt >= DateTime.Today ? "Активний" : "Прострочений";
}

// ─── Поліморфний код — правильний LSP ─────────────────────────────
void PrintRecord(MedicalRecordBase record)
{
    // Для БУДЬ-ЯКОГО підкласу контракт виконається: GetSummary() не null,
    // GetStatus() — один з очікуваних рядків
    Console.WriteLine($"[{record.GetStatus()}] {record.GetSummary()}");
    Console.WriteLine($"  Дата: {record.Date:dd.MM.yyyy}, пацієнт #{record.PatientId.ToString()}");
}

var records = new MedicalRecordBase[]
{
    new DiagnosisRecord(1, 101, 5, "J06.9", false, "ГРВІ, 7 днів лікування"),
    new DiagnosisRecord(2, 101, 5, "I10",   true,  "Гіпертонія, постійне спостереження"),
    new PrescriptionRecord(3, 101, 5, "Ібупрофен 400мг", 5, "3 рази на день після їжі"),
    new PrescriptionRecord(4, 102, 7, "Метформін 500мг", 30, "Вранці натщесерце"),
};

foreach (var r in records) PrintRecord(r);
```

### `20-04-lsp.md` — блок #5 (рядок файлу 380)

**Помилки:**
- рядок 34: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

// Базовий клас
abstract class Doctor
{
    public string Name { get; }
    public Doctor(string name) { Name = name; }

    // Контракт: завжди повертає додатнє число
    public abstract decimal GetConsultationFee();

    // Контракт: ніколи не повертає рядок довший за 100 символів
    public abstract string GetSpeciality();
}

class GeneralPractitioner : Doctor
{
    public GeneralPractitioner(string name) : base(name) { }
    public override decimal GetConsultationFee() => 500m;     // ✓ > 0
    public override string  GetSpeciality()      => "Загальна практика"; // ✓ < 100 символів
}

class Specialist : Doctor
{
    private readonly string _field;
    private readonly decimal _fee;
    public Specialist(string name, string field, decimal fee) : base(name)
    { _field = field; _fee = fee; }
    public override decimal GetConsultationFee() => _fee;    // ✓ > 0 (якщо fee > 0)
    public override string  GetSpeciality()      => _field;  // ✓ < 100 символів
}

// Тест-перевірка, що має проходити для БУДЬ-якого Doctor ──────────
void AssertDoctorContract(Doctor d)
{
    decimal fee = d.GetConsultationFee();
    string spec = d.GetSpeciality();

    bool feeOk  = fee > 0;
    bool specOk = spec != null && spec.Length <= 100;

    Console.WriteLine($"{d.Name} ({d.GetType().Name}):");
    Console.WriteLine($"  Fee={fee.ToString()} → {(feeOk ? "✓" : "✗ порушення!")}");
    Console.WriteLine($"  Speciality='{spec}' → {(specOk ? "✓" : "✗ порушення!")}");
}

var doctors = new Doctor[]
{
    new GeneralPractitioner("Петренко І.О."),
    new Specialist("Коваленко М.А.", "Кардіологія", 1200m),
    new Specialist("Бойко О.Р.",     "Неврологія",  1000m),
};

foreach (var d in doctors) AssertDoctorContract(d);
```

### `20-05-isp.md` — блок #1 (рядок файлу 26)

**Помилки:**
- рядок 60: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;

// ─── ПОРУШЕННЯ ISP — «жирний» інтерфейс ────────────────────────────

interface IClinicService
{
    // Група 1: Управління пацієнтами
    void   AddPatient(string name);
    void   RemovePatient(int id);
    string FindPatient(int id);

    // Група 2: Записи на прийом
    void BookAppointment(string patient, string doctor, DateTime time);
    void CancelAppointment(int id);
    int  GetAppointmentCount(string doctor);

    // Група 3: Звіти та аналітика
    string GeneratePdfReport();
    string ExportToCsv();
    void   SendReportByEmail(string to);
}

// ── ReceptionDesk потребує лише груп 1 і 2 ─────────────────────────
// Але мусить реалізувати ВСЕ — включно з PDF і Email, яких не знає

class ReceptionDesk : IClinicService
{
    public void   AddPatient(string name)          => Console.WriteLine($"Реєстрація: {name}");
    public void   RemovePatient(int id)            => Console.WriteLine($"Виписка: #{id.ToString()}");
    public string FindPatient(int id)              => $"Пацієнт #{id.ToString()}";
    public void   BookAppointment(string p, string d, DateTime t) =>
                                                      Console.WriteLine($"Запис: {p} → {d}");
    public void   CancelAppointment(int id)        => Console.WriteLine($"Скасовано: #{id.ToString()}");
    public int    GetAppointmentCount(string doc)  => 0;

    // ↓ Вимушені заглушки — ReceptionDesk не знає про PDF і Email!
    public string GeneratePdfReport() => throw new NotImplementedException("Не наша відповідальність");
    public string ExportToCsv()       => throw new NotImplementedException("Не наша відповідальність");
    public void   SendReportByEmail(string to) => throw new NotImplementedException("Не наша відповідальність");
}

// ── AnalyticsModule потребує лише групи 3 ──────────────────────────
class AnalyticsModule : IClinicService
{
    // ↓ Вимушені заглушки — AnalyticsModule нічого не знає про пацієнтів!
    public void   AddPatient(string name)          => throw new NotImplementedException();
    public void   RemovePatient(int id)            => throw new NotImplementedException();
    public string FindPatient(int id)              => throw new NotImplementedException();
    public void   BookAppointment(string p, string d, DateTime t) => throw new NotImplementedException();
    public void   CancelAppointment(int id)        => throw new NotImplementedException();
    public int    GetAppointmentCount(string doc)  => throw new NotImplementedException();

    // Реальна логіка — тільки тут
    public string GeneratePdfReport() { Console.WriteLine("PDF згенеровано"); return "report.pdf"; }
    public string ExportToCsv()       { Console.WriteLine("CSV експортовано"); return "data.csv";   }
    public void   SendReportByEmail(string to)     => Console.WriteLine($"Надіслано на {to}");
}

// ── Проблема стає очевидною ─────────────────────────────────────────
var desk = new ReceptionDesk();
desk.AddPatient("Мороз Василь");
desk.BookAppointment("Мороз Василь", "Петренко І.О.", DateTime.Today.AddHours(10));
try { desk.GeneratePdfReport(); }    // ✗ Вибух у runtime
catch (NotImplementedException) { Console.WriteLine("[Помилка] ReceptionDesk не вміє PDF — але змушений реалізовувати метод"); }
```

### `20-05-isp.md` — блок #2 (рядок файлу 99)

**Помилки:**
- рядок 85: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── ПРАВИЛЬНО: вузькі інтерфейси за роллю ─────────────────────────

// Кожен інтерфейс — мінімально необхідний контракт для конкретного клієнта

interface IPatientService
{
    void   AddPatient(string name);
    void   RemovePatient(int id);
    string FindPatient(int id);
}

interface IAppointmentService
{
    void BookAppointment(string patient, string doctor, DateTime time);
    void CancelAppointment(int id);
    int  GetAppointmentCount(string doctor);
}

interface IReportService
{
    string GeneratePdfReport();
    string ExportToCsv();
    void   SendReportByEmail(string to);
}

// ── ReceptionDesk: реалізує лише те, що потрібно ──────────────────
class ReceptionDesk : IPatientService, IAppointmentService
{
    private Dictionary<int, string> _patients     = new();
    private List<string>            _appointments = new();
    private int _nextId = 1;

    public void   AddPatient(string name)  { _patients[_nextId++] = name; Console.WriteLine($"+ {name}"); }
    public void   RemovePatient(int id)    { _patients.Remove(id); Console.WriteLine($"- #{id.ToString()}"); }
    public string FindPatient(int id)      => _patients.TryGetValue(id, out var n) ? n : "Не знайдено";

    public void BookAppointment(string patient, string doctor, DateTime time)
    {
        _appointments.Add($"{patient}|{doctor}|{time:HH:mm}");
        Console.WriteLine($"Запис: {patient} → {doctor} о {time:HH:mm}");
    }
    public void CancelAppointment(int id)        => Console.WriteLine($"Скасовано: #{id.ToString()}");
    public int  GetAppointmentCount(string doc)  =>
        _appointments.FindAll(a => a.Contains($"|{doc}|")).Count;

    // ✓ Нема жодної заглушки для PDF — ReceptionDesk чесно не знає про звіти
}

// ── AnalyticsModule: реалізує лише звіти ──────────────────────────
class AnalyticsModule : IReportService
{
    public string GeneratePdfReport()
    {
        Console.WriteLine("[Analytics] Генерація PDF-звіту...");
        return "clinic_report_2024.pdf";
    }
    public string ExportToCsv()
    {
        Console.WriteLine("[Analytics] Експорт у CSV...");
        return "clinic_data_2024.csv";
    }
    public void SendReportByEmail(string to)
        => Console.WriteLine($"[Analytics] Звіт надіслано на {to}");
}

// ── FullClinicService: реалізує всі ролі ───────────────────────────
class FullClinicService : IPatientService, IAppointmentService, IReportService
{
    public void   AddPatient(string name)  => Console.WriteLine($"[Full] Пацієнт: {name}");
    public void   RemovePatient(int id)    => Console.WriteLine($"[Full] Виписано: #{id.ToString()}");
    public string FindPatient(int id)      => $"[Full] Пацієнт #{id.ToString()}";
    public void   BookAppointment(string p, string d, DateTime t) =>
                                             Console.WriteLine($"[Full] Запис: {p}→{d}");
    public void   CancelAppointment(int id)       => Console.WriteLine($"[Full] Скасовано");
    public int    GetAppointmentCount(string doc) => 5;
    public string GeneratePdfReport() => "[Full] report.pdf";
    public string ExportToCsv()       => "[Full] data.csv";
    public void   SendReportByEmail(string to)    => Console.WriteLine($"[Full] Email: {to}");
}

// ── Клієнтський код — залежить від мінімального контракту ──────────
void RegisterPatient(IPatientService svc, string name) => svc.AddPatient(name);
void MakeReport(IReportService svc, string email)
{
    string pdf = svc.GeneratePdfReport();
    svc.SendReportByEmail(email);
    Console.WriteLine($"Звіт: {pdf}");
}

var desk     = new ReceptionDesk();
var analytics= new AnalyticsModule();
var full     = new FullClinicService();

RegisterPatient(desk, "Мороз Василь");
RegisterPatient(desk, "Бойко Олена");
Console.WriteLine($"Записів лікаря: {desk.GetAppointmentCount("Петренко").ToString()}");

MakeReport(analytics, "admin@clinic.ua");
MakeReport(full,      "boss@clinic.ua");

// Перевірка: desk не передається в MakeReport — компілятор не дозволить
// MakeReport(desk, "test@test.com"); // ← помилка компіляції
Console.WriteLine("\n✓ ISP дотримано: кожен клас реалізує лише свої методи");
```

### `20-05-isp.md` — блок #3 (рядок файлу 218)

**Помилки:**
- рядок 88: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── ISP: інтерфейси як ролі для медичної системи ──────────────────

// Роль: об'єкт, що можна зберегти
interface ISaveable
{
    void Save();
}

// Роль: об'єкт, що можна заархівувати
interface IArchivable
{
    void Archive(string reason);
    bool IsArchived { get; }
}

// Роль: об'єкт, що можна надіслати
interface ISendable
{
    void Send(string recipient);
}

// Роль: об'єкт із аудит-слідом
interface IAuditable
{
    DateTime CreatedAt  { get; }
    DateTime? UpdatedAt { get; }
    string    CreatedBy { get; }
}

// ── MedicalReport: зберігається і надсилається, але не архівується──
class MedicalReport : ISaveable, ISendable, IAuditable
{
    public string Title     { get; }
    public string Content   { get; }
    public DateTime CreatedAt  { get; } = DateTime.Now;
    public DateTime? UpdatedAt { get; private set; }
    public string    CreatedBy { get; }

    public MedicalReport(string title, string content, string doctor)
    {
        Title = title; Content = content; CreatedBy = doctor;
    }

    public void Save()
    {
        Console.WriteLine($"[Report] Збережено: '{Title}'");
    }

    public void Send(string recipient)
    {
        Console.WriteLine($"[Report] '{Title}' → {recipient}");
    }
}

// ── PatientRecord: зберігається, архівується, має аудит ───────────
class PatientRecord : ISaveable, IArchivable, IAuditable
{
    public int    PatientId { get; }
    public string Content   { get; }
    public DateTime CreatedAt  { get; } = DateTime.Now;
    public DateTime? UpdatedAt { get; private set; }
    public string    CreatedBy { get; }
    public bool      IsArchived{ get; private set; }

    public PatientRecord(int patientId, string content, string doctor)
    {
        PatientId = patientId; Content = content; CreatedBy = doctor;
    }

    public void Save()
    {
        UpdatedAt = DateTime.Now;
        Console.WriteLine($"[Record] Пацієнт #{PatientId.ToString()} збережено");
    }

    public void Archive(string reason)
    {
        IsArchived = true;
        UpdatedAt  = DateTime.Now;
        Console.WriteLine($"[Record] Пацієнт #{PatientId.ToString()} архівовано: {reason}");
    }
}

// ── Утиліти — кожна залежить від мінімального контракту ───────────
void SaveAll(IEnumerable<ISaveable> items)
{
    foreach (var item in items) item.Save();
}

void ArchiveOld(IEnumerable<IArchivable> items, string reason)
{
    foreach (var item in items)
        if (!item.IsArchived) item.Archive(reason);
}

void PrintAudit(IAuditable item)
{
    Console.WriteLine($"  Створено: {item.CreatedAt:dd.MM.yyyy HH:mm} ({item.CreatedBy})");
    Console.WriteLine($"  Змінено:  {(item.UpdatedAt.HasValue ? item.UpdatedAt.Value.ToString("dd.MM.yyyy HH:mm") : "ніколи")}");
}

var report = new MedicalReport("Кардіологічний огляд", "Норма", "Петренко І.О.");
var record1 = new PatientRecord(101, "Гіпертонія I ст.", "Коваленко М.А.");
var record2 = new PatientRecord(102, "ГРВІ", "Петренко І.О.");

// ISaveAble — save report and records
SaveAll(new ISaveable[] { report, record1, record2 });

// ISendable — тільки report
report.Send("patient@example.com");

// IArchivable — тільки records
ArchiveOld(new IArchivable[] { record1, record2 }, "Виписка");

// IAuditable — audit для record1
Console.WriteLine($"\nАудит запису пацієнта #{record1.PatientId.ToString()}:");
PrintAudit(record1);
```

### `20-05-isp.md` — блок #4 (рядок файлу 347)

**Помилки:**
- рядок 56: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── Правильне застосування ISP: адаптер для зовнішньої системи ────

// Зовнішня система лабораторних аналізів має великий API
// Ми використовуємо лише маленьку частину — виразимо це через вузький інтерфейс

interface ILabResultProvider
{
    // Тільки те, що потрібно клінічній системі
    string GetResult(string testCode, int patientId);
    bool   IsResultReady(string testCode, int patientId);
    DateTime GetResultDate(string testCode, int patientId);
}

// Наш адаптер реалізує вузький інтерфейс і «перекладає» до зовнішньої системи
class LabSystemAdapter : ILabResultProvider
{
    // Уявна зовнішня система з великим API — ми беремо лише 3 методи
    public string   GetResult(string code, int patientId)
    {
        // Реально: HTTP-запит до лабораторної системи
        return $"[Лаб. система] {code} для #{patientId.ToString()}: в нормі";
    }
    public bool     IsResultReady(string code, int patientId)   => true;
    public DateTime GetResultDate(string code, int patientId)   => DateTime.Today;
}

// Клінічна система залежить від мінімального ILabResultProvider
class PatientDashboard
{
    private readonly ILabResultProvider _lab;

    public PatientDashboard(ILabResultProvider lab) => _lab = lab;

    public void ShowLabResults(int patientId, string[] testCodes)
    {
        Console.WriteLine($"\nЛабораторні результати пацієнта #{patientId.ToString()}:");
        foreach (var code in testCodes)
        {
            if (_lab.IsResultReady(code, patientId))
            {
                string result = _lab.GetResult(code, patientId);
                DateTime date = _lab.GetResultDate(code, patientId);
                Console.WriteLine($"  [{code}] {date:dd.MM.yyyy}: {result}");
            }
            else
            {
                Console.WriteLine($"  [{code}] Ще не готово");
            }
        }
    }
}

var dashboard = new PatientDashboard(new LabSystemAdapter());
dashboard.ShowLabResults(101, new[] { "CBC", "BMP", "HbA1c" });
```

### `20-06-dip.md` — блок #1 (рядок файлу 26)

**Помилки:**
- рядок 48: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── ПОРУШЕННЯ DIP: AppointmentService знає про SqlRepository ──────

// Конкретна реалізація — нижній рівень
class SqlAppointmentRepository
{
    private List<string> _db = new(); // імітація таблиці в БД

    public void Save(string patient, string doctor, DateTime time)
    {
        string record = $"{patient}|{doctor}|{time:yyyy-MM-dd HH:mm}";
        _db.Add(record);
        Console.WriteLine($"[SQL] INSERT: {record}");
    }

    public List<string> GetByDoctor(string doctor)
    {
        var result = _db.FindAll(r => r.Contains($"|{doctor}|"));
        Console.WriteLine($"[SQL] SELECT WHERE doctor='{doctor}': {result.Count.ToString()} rows");
        return result;
    }
}

// Бізнес-логіка — верхній рівень
// ⚠ Залежить безпосередньо від SqlAppointmentRepository
class AppointmentService_Bad
{
    // Жорстка залежність: тут «зашита» конкретна реалізація
    private readonly SqlAppointmentRepository _repository = new SqlAppointmentRepository();

    public void Book(string patient, string doctor, DateTime time)
    {
        // Бізнес-правило: лікар не може приймати більш ніж 10 пацієнтів на день
        var existingToday = _repository.GetByDoctor(doctor);
        if (existingToday.Count >= 10)
        {
            Console.WriteLine($"[Service] {doctor}: максимум записів на сьогодні");
            return;
        }

        _repository.Save(patient, doctor, time);
        Console.WriteLine($"[Service] Заброньовано: {patient} → {doctor}");
    }
}

var svc = new AppointmentService_Bad();
svc.Book("Мороз Василь",  "Петренко І.О.", DateTime.Today.AddHours(9));
svc.Book("Бойко Олена",   "Петренко І.О.", DateTime.Today.AddHours(10));

// Проблеми:
// ✗ Написати тест без реального SQL-сервера неможливо
// ✗ Перейти на MongoDB = переписати AppointmentService_Bad
// ✗ Використати InMemory-репозиторій для розробки — неможливо
Console.WriteLine("\n⚠ AppointmentService залежить від SqlAppointmentRepository безпосередньо");
```

### `20-06-dip.md` — блок #2 (рядок файлу 91)

**Помилки:**
- рядок 88: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── ПРАВИЛЬНО: DIP через інтерфейс і Dependency Injection ─────────

// Абстракція — диктує умови, що мають виконати конкретні реалізації
interface IAppointmentRepository
{
    void         Save(string patient, string doctor, DateTime time);
    List<string> GetByDoctor(string doctor);
    int          CountByDoctor(string doctor);
}

// ── Конкретна реалізація 1: SQL ─────────────────────────────────────
class SqlAppointmentRepository : IAppointmentRepository
{
    private List<string> _db = new();

    public void Save(string patient, string doctor, DateTime time)
    {
        _db.Add($"{patient}|{doctor}|{time:HH:mm}");
        Console.WriteLine($"[SQL] Збережено: {patient} → {doctor}");
    }

    public List<string> GetByDoctor(string doctor) =>
        _db.FindAll(r => r.Contains($"|{doctor}|"));

    public int CountByDoctor(string doctor) => GetByDoctor(doctor).Count;
}

// ── Конкретна реалізація 2: In-Memory (для тестів і розробки) ───────
class InMemoryAppointmentRepository : IAppointmentRepository
{
    private List<(string Patient, string Doctor, DateTime Time)> _store = new();

    public void Save(string patient, string doctor, DateTime time)
    {
        _store.Add((patient, doctor, time));
        Console.WriteLine($"[Memory] Збережено: {patient} → {doctor}");
    }

    public List<string> GetByDoctor(string doctor) =>
        _store.FindAll(a => a.Doctor == doctor)
              .ConvertAll(a => $"{a.Patient}|{a.Doctor}|{a.Time:HH:mm}");

    public int CountByDoctor(string doctor) =>
        _store.FindAll(a => a.Doctor == doctor).Count;
}

// ── Бізнес-логіка: залежить ТІЛЬКИ від абстракції ──────────────────
class AppointmentService
{
    private readonly IAppointmentRepository _repo;

    // Dependency Injection через конструктор
    public AppointmentService(IAppointmentRepository repo)
    {
        _repo = repo;
    }

    public bool Book(string patient, string doctor, DateTime time)
    {
        // Бізнес-правило: не більше 10 записів на день
        if (_repo.CountByDoctor(doctor) >= 10)
        {
            Console.WriteLine($"[Service] {doctor}: максимум записів вичерпано");
            return false;
        }

        _repo.Save(patient, doctor, time);
        Console.WriteLine($"[Service] ✓ Заброньовано: {patient} → {doctor} о {time:HH:mm}");
        return true;
    }

    public void PrintDoctorSchedule(string doctor)
    {
        var appointments = _repo.GetByDoctor(doctor);
        Console.WriteLine($"\nРозклад {doctor} ({appointments.Count.ToString()} записів):");
        foreach (var a in appointments)
        {
            string[] parts = a.Split('|');
            Console.WriteLine($"  {(parts.Length > 2 ? parts[2] : "?")} — {(parts.Length > 0 ? parts[0] : "?")}");
        }
    }
}

// ── Виробничий варіант: використовуємо SQL ──────────────────────────
Console.WriteLine("=== Виробничий варіант (SQL) ===");
var sqlRepo      = new SqlAppointmentRepository();
var prodService  = new AppointmentService(sqlRepo); // SQL "вводиться" ззовні

prodService.Book("Мороз Василь",  "Петренко І.О.", DateTime.Today.AddHours(9));
prodService.Book("Бойко Олена",   "Петренко І.О.", DateTime.Today.AddHours(11));
prodService.PrintDoctorSchedule("Петренко І.О.");

// ── Тест / розробка: InMemory — ТОЙ САМИЙ AppointmentService ────────
Console.WriteLine("\n=== Тестовий варіант (InMemory) ===");
var memRepo     = new InMemoryAppointmentRepository();
var testService = new AppointmentService(memRepo); // InMemory "вводиться" ззовні

testService.Book("Тест Пацієнт",  "Тест Лікар", DateTime.Today.AddHours(14));
testService.Book("Тест Пацієнт2", "Тест Лікар", DateTime.Today.AddHours(15));
testService.PrintDoctorSchedule("Тест Лікар");

// AppointmentService НЕ змінювався між варіантами — лише репозиторій змінився
Console.WriteLine("\n✓ AppointmentService не знає, SQL він чи InMemory");
```

### `20-06-dip.md` — блок #3 (рядок файлу 204)

**Помилки:**
- рядок 64: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

interface IPatientLogger
{
    void Log(string message);
}

class ConsoleLogger : IPatientLogger
{
    public void Log(string msg) => Console.WriteLine($"[LOG] {msg}");
}

class FileLogger : IPatientLogger
{
    private string _path;
    public FileLogger(string path) => _path = path;
    public void Log(string msg) => Console.WriteLine($"[FILE:{_path}] {msg}");
}

// ── Спосіб 1: Constructor Injection ────────────────────────────────
// Рекомендований. Залежність обов'язкова, очевидна, незмінна після створення.
class PatientServiceV1
{
    private readonly IPatientLogger _logger;

    public PatientServiceV1(IPatientLogger logger) // ← залежність через конструктор
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    public void Register(string name)
    {
        _logger.Log($"Зареєстровано: {name}");
        Console.WriteLine($"[Service] Пацієнт додано: {name}");
    }
}

// ── Спосіб 2: Property Injection ───────────────────────────────────
// Для необов'язкових залежностей. Клас може працювати і без них.
class PatientServiceV2
{
    public IPatientLogger? Logger { get; set; } // ← залежність через властивість

    public void Register(string name)
    {
        Logger?.Log($"Зареєстровано: {name}"); // null-safe: якщо немає — просто не логуємо
        Console.WriteLine($"[Service] Пацієнт: {name}");
    }
}

// ── Спосіб 3: Method Injection ──────────────────────────────────────
// Якщо залежність потрібна лише в одному методі, не для всього класу.
class PatientServiceV3
{
    public void Register(string name, IPatientLogger logger) // ← залежність через метод
    {
        logger.Log($"Зареєстровано: {name}");
        Console.WriteLine($"[Service] Пацієнт: {name}");
    }
}

// ── Демонстрація трьох способів ─────────────────────────────────────
Console.WriteLine("=== Constructor Injection ===");
var svc1 = new PatientServiceV1(new ConsoleLogger());
svc1.Register("Мороз Василь");

Console.WriteLine("\n=== Property Injection ===");
var svc2 = new PatientServiceV2();
svc2.Logger = new FileLogger("clinic.log");
svc2.Register("Бойко Олена");

var svc2b = new PatientServiceV2(); // Logger = null — все одно працює
svc2b.Register("Коваль Михайло");

Console.WriteLine("\n=== Method Injection ===");
var svc3 = new PatientServiceV3();
svc3.Register("Сидоренко Тетяна", new ConsoleLogger());
svc3.Register("Петрів Іван",      new FileLogger("audit.log"));
```

### `20-06-dip.md` — блок #4 (рядок файлу 294)

**Помилки:**
- рядок 69: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── Симуляція DI-контейнера (спрощена версія) ─────────────────────
// У реальних проектах: Microsoft.Extensions.DependencyInjection

class SimpleContainer
{
    private Dictionary<Type, Func<object>> _registrations = new();

    public void Register<TInterface, TImplementation>()
        where TImplementation : TInterface, new()
    {
        _registrations[typeof(TInterface)] = () => new TImplementation();
    }

    public void RegisterFactory<TInterface>(Func<object> factory)
    {
        _registrations[typeof(TInterface)] = factory;
    }

    public T Resolve<T>() =>
        (T)(_registrations.TryGetValue(typeof(T), out var factory)
            ? factory()
            : throw new InvalidOperationException($"Не зареєстровано: {typeof(T).Name}"));
}

// ─── Інтерфейси і реалізації ──────────────────────────────────────
interface IDoctorRepository
{
    string GetById(int id);
}

interface IPatientRepository
{
    string GetById(int id);
}

class SqlDoctorRepository : IDoctorRepository
{
    public string GetById(int id) => $"[SQL] Лікар #{id.ToString()}: Петренко І.О.";
}

class SqlPatientRepository : IPatientRepository
{
    public string GetById(int id) => $"[SQL] Пацієнт #{id.ToString()}: Мороз Василь";
}

class AppointmentBookingService
{
    private readonly IDoctorRepository  _doctors;
    private readonly IPatientRepository _patients;

    public AppointmentBookingService(IDoctorRepository doctors, IPatientRepository patients)
    {
        _doctors  = doctors;
        _patients = patients;
    }

    public void Book(int patientId, int doctorId, DateTime time)
    {
        string patient = _patients.GetById(patientId);
        string doctor  = _doctors.GetById(doctorId);
        Console.WriteLine($"Запис: {patient} → {doctor} о {time:HH:mm}");
    }
}

// ─── Налаштування контейнера ──────────────────────────────────────
var container = new SimpleContainer();
container.Register<IDoctorRepository,  SqlDoctorRepository>();
container.Register<IPatientRepository, SqlPatientRepository>();

// Resolve: отримуємо залежності через контейнер
var doctorRepo  = container.Resolve<IDoctorRepository>();
var patientRepo = container.Resolve<IPatientRepository>();

// Конструюємо сервіс, передаючи залежності
var bookingService = new AppointmentBookingService(doctorRepo, patientRepo);
bookingService.Book(101, 5, DateTime.Today.AddHours(14));

// ─── Хочемо протестувати? Замінюємо реалізації ────────────────────
Console.WriteLine("\n=== Тестовий варіант: InMemory ===");

class TestDoctorRepository : IDoctorRepository
{
    public string GetById(int id) => $"[Test] Тест-Лікар #{id.ToString()}";
}

class TestPatientRepository : IPatientRepository
{
    public string GetById(int id) => $"[Test] Тест-Пацієнт #{id.ToString()}";
}

// Той самий AppointmentBookingService — інші реалізації
var testService = new AppointmentBookingService(
    new TestDoctorRepository(),
    new TestPatientRepository()
);
testService.Book(999, 1, DateTime.Today.AddHours(10));
Console.WriteLine("✓ AppointmentBookingService не змінювався");
```

### `20-06-dip.md` — блок #5 (рядок файлу 401)

**Помилки:**
- рядок 49: Top-level statements must precede namespace and type declarations.

**Код:**
```csharp
using System;
using System.Collections.Generic;

// ─── DIP + тестові дублі ───────────────────────────────────────────

interface IAppointmentStore
{
    void   Add(string patient, string doctor);
    int    Count(string doctor);
    bool   Exists(string patient, string doctor);
}

// Бізнес-логіка: перевіряє обмеження і зберігає
class SchedulingService
{
    private readonly IAppointmentStore _store;
    private const int MaxPerDoctor = 3; // для демонстрації — маленький ліміт

    public SchedulingService(IAppointmentStore store) => _store = store;

    public string Schedule(string patient, string doctor)
    {
        if (_store.Exists(patient, doctor))
            return $"DUPLICATE: {patient} вже записаний до {doctor}";

        if (_store.Count(doctor) >= MaxPerDoctor)
            return $"FULL: {doctor} має максимальну кількість записів ({MaxPerDoctor.ToString()})";

        _store.Add(patient, doctor);
        return $"OK: {patient} → {doctor}";
    }
}

// ─── Тестовий дубль (Stub/Fake) ───────────────────────────────────
class FakeAppointmentStore : IAppointmentStore
{
    private List<(string Patient, string Doctor)> _data = new();

    // Можна налаштовувати для різних тестових сценаріїв
    public void Preload(string patient, string doctor) => _data.Add((patient, doctor));

    public void   Add(string patient, string doctor) => _data.Add((patient, doctor));
    public int    Count(string doctor) => _data.FindAll(x => x.Doctor == doctor).Count;
    public bool   Exists(string patient, string doctor) =>
        _data.Exists(x => x.Patient == patient && x.Doctor == doctor);
}

// ─── Симуляція тестів — без БД, без файлів, без мережі ────────────
void Test(string name, string expected, string actual)
{
    bool pass = expected == actual;
    Console.WriteLine($"{(pass ? "✓" : "✗")} {name}");
    if (!pass) Console.WriteLine($"    Очікувалось: {expected}\n    Отримано:    {actual}");
}

// Тест 1: успішний запис
var store1 = new FakeAppointmentStore();
var svc1   = new SchedulingService(store1);
Test("Успішний запис",
     "OK: Мороз Василь → Петренко І.О.",
     svc1.Schedule("Мороз Василь", "Петренко І.О."));

// Тест 2: дублікат
var store2 = new FakeAppointmentStore();
store2.Preload("Бойко Олена", "Коваленко М.А."); // налаштовуємо початковий стан
var svc2   = new SchedulingService(store2);
Test("Дублікат запису",
     "DUPLICATE: Бойко Олена вже записаний до Коваленко М.А.",
     svc2.Schedule("Бойко Олена", "Коваленко М.А."));

// Тест 3: лікар переповнений
var store3 = new FakeAppointmentStore();
store3.Preload("P1", "Бойко О.Р.");
store3.Preload("P2", "Бойко О.Р.");
store3.Preload("P3", "Бойко О.Р."); // 3 записи — максимум
var svc3   = new SchedulingService(store3);
Test("Переповнений лікар",
     "FULL: Бойко О.Р. має максимальну кількість записів (3)",
     svc3.Schedule("P4", "Бойко О.Р."));
```

## ✅ Блоки що компілюються успішно

| Файл | Блок | Рядок у файлі |
|------|:----:|:-------------:|
| `01-01-rol-platformy.md` | #1 | 31 |
| `01-01-rol-platformy.md` | #2 | 75 |
| `01-01-rol-platformy.md` | #3 | 127 |
| `01-03-kerovanyi-ta-nekerovanyi-kod.md` | #1 | 38 |
| `01-03-kerovanyi-ta-nekerovanyi-kod.md` | #2 | 59 |
| `01-04-jit-kompiliatsiia.md` | #1 | 35 |
| `01-04-jit-kompiliatsiia.md` | #2 | 71 |
| `02-01-struktura-programy.md` | #1 | 21 |
| `02-01-struktura-programy.md` | #2 | 52 |
| `02-01-struktura-programy.md` | #3 | 64 |
| `02-01-struktura-programy.md` | #4 | 75 |
| `02-01-struktura-programy.md` | #5 | 97 |
| `02-01-struktura-programy.md` | #6 | 113 |
| `02-01-struktura-programy.md` | #7 | 133 |
| `02-01-struktura-programy.md` | #8 | 146 |
| `02-02-zminni-ta-konstanty.md` | #1 | 29 |
| `02-02-zminni-ta-konstanty.md` | #2 | 44 |
| `02-02-zminni-ta-konstanty.md` | #3 | 64 |
| `02-02-zminni-ta-konstanty.md` | #4 | 92 |
| `02-02-zminni-ta-konstanty.md` | #5 | 107 |
| `02-02-zminni-ta-konstanty.md` | #6 | 135 |
| `02-03-literaly.md` | #1 | 21 |
| `02-03-literaly.md` | #2 | 39 |
| `02-03-literaly.md` | #3 | 49 |
| `02-03-literaly.md` | #4 | 59 |
| `02-03-literaly.md` | #5 | 69 |
| `02-03-literaly.md` | #6 | 83 |
| `02-03-literaly.md` | #7 | 93 |
| `02-03-literaly.md` | #8 | 103 |
| `02-03-literaly.md` | #9 | 123 |
| `02-03-literaly.md` | #10 | 137 |
| `02-03-literaly.md` | #11 | 154 |
| `02-03-literaly.md` | #12 | 163 |
| `02-03-literaly.md` | #13 | 175 |
| `02-03-literaly.md` | #14 | 185 |
| `02-03-literaly.md` | #15 | 193 |
| `02-03-literaly.md` | #16 | 201 |
| `02-03-literaly.md` | #17 | 213 |
| `02-03-literaly.md` | #18 | 230 |
| `02-04-typy-danykh.md` | #1 | 23 |
| `02-04-typy-danykh.md` | #2 | 37 |
| `02-04-typy-danykh.md` | #3 | 52 |
| `02-04-typy-danykh.md` | #4 | 66 |
| `02-04-typy-danykh.md` | #5 | 79 |
| `02-04-typy-danykh.md` | #6 | 93 |
| `02-04-typy-danykh.md` | #7 | 109 |
| `02-04-typy-danykh.md` | #8 | 125 |
| `02-04-typy-danykh.md` | #9 | 139 |
| `02-04-typy-danykh.md` | #10 | 155 |
| `02-04-typy-danykh.md` | #11 | 169 |
| `02-04-typy-danykh.md` | #12 | 187 |
| `02-04-typy-danykh.md` | #13 | 203 |
| `02-04-typy-danykh.md` | #14 | 219 |
| `02-04-typy-danykh.md` | #15 | 234 |
| `02-04-typy-danykh.md` | #16 | 254 |
| `02-04-typy-danykh.md` | #17 | 274 |
| `02-04-typy-danykh.md` | #18 | 294 |
| `02-04-typy-danykh.md` | #19 | 311 |
| `02-05-konsolne-vvedennia-vyvedennia.md` | #1 | 21 |
| `02-05-konsolne-vvedennia-vyvedennia.md` | #2 | 41 |
| `02-05-konsolne-vvedennia-vyvedennia.md` | #3 | 58 |
| `02-05-konsolne-vvedennia-vyvedennia.md` | #4 | 75 |
| `02-05-konsolne-vvedennia-vyvedennia.md` | #5 | 93 |
| `02-05-konsolne-vvedennia-vyvedennia.md` | #6 | 112 |
| `02-05-konsolne-vvedennia-vyvedennia.md` | #7 | 143 |
| `02-06-aryfmetychni-operatsii.md` | #1 | 23 |
| `02-06-aryfmetychni-operatsii.md` | #2 | 35 |
| `02-06-aryfmetychni-operatsii.md` | #3 | 47 |
| `02-06-aryfmetychni-operatsii.md` | #4 | 59 |
| `02-06-aryfmetychni-operatsii.md` | #5 | 71 |
| `02-06-aryfmetychni-operatsii.md` | #6 | 83 |
| `02-06-aryfmetychni-operatsii.md` | #7 | 104 |
| `02-06-aryfmetychni-operatsii.md` | #8 | 118 |
| `02-06-aryfmetychni-operatsii.md` | #9 | 144 |
| `02-06-aryfmetychni-operatsii.md` | #10 | 159 |
| `02-06-aryfmetychni-operatsii.md` | #11 | 176 |
| `02-06-aryfmetychni-operatsii.md` | #12 | 188 |
| `02-07-porozriadni-operatsii.md` | #1 | 32 |
| `02-07-porozriadni-operatsii.md` | #2 | 50 |
| `02-07-porozriadni-operatsii.md` | #3 | 70 |
| `02-07-porozriadni-operatsii.md` | #4 | 89 |
| `02-07-porozriadni-operatsii.md` | #5 | 107 |
| `02-07-porozriadni-operatsii.md` | #6 | 124 |
| `02-07-porozriadni-operatsii.md` | #7 | 139 |
| `02-07-porozriadni-operatsii.md` | #8 | 154 |
| `02-08-operatsii-prysvoiennia.md` | #1 | 21 |
| `02-08-operatsii-prysvoiennia.md` | #2 | 39 |
| `02-08-operatsii-prysvoiennia.md` | #3 | 52 |
| `02-08-operatsii-prysvoiennia.md` | #4 | 79 |
| `02-08-operatsii-prysvoiennia.md` | #5 | 107 |
| `02-08-operatsii-prysvoiennia.md` | #6 | 134 |
| `02-08-operatsii-prysvoiennia.md` | #7 | 153 |
| `02-09-peretvorennia-bazovykh-typiv.md` | #1 | 21 |
| `02-09-peretvorennia-bazovykh-typiv.md` | #2 | 49 |
| `02-09-peretvorennia-bazovykh-typiv.md` | #3 | 66 |
| `02-09-peretvorennia-bazovykh-typiv.md` | #4 | 81 |
| `02-09-peretvorennia-bazovykh-typiv.md` | #5 | 96 |
| `02-09-peretvorennia-bazovykh-typiv.md` | #6 | 107 |
| `02-09-peretvorennia-bazovykh-typiv.md` | #7 | 131 |
| `02-09-peretvorennia-bazovykh-typiv.md` | #8 | 148 |
| `02-10-yavni-ta-neyavni-peretvorennia.md` | #1 | 23 |
| `02-10-yavni-ta-neyavni-peretvorennia.md` | #2 | 40 |
| `02-10-yavni-ta-neyavni-peretvorennia.md` | #3 | 53 |
| `02-10-yavni-ta-neyavni-peretvorennia.md` | #4 | 76 |
| `02-10-yavni-ta-neyavni-peretvorennia.md` | #5 | 105 |
| `02-10-yavni-ta-neyavni-peretvorennia.md` | #6 | 122 |
| `02-10-yavni-ta-neyavni-peretvorennia.md` | #7 | 138 |
| `02-10-yavni-ta-neyavni-peretvorennia.md` | #8 | 158 |
| `02-10-yavni-ta-neyavni-peretvorennia.md` | #9 | 182 |
| `02-11-umovni-vyrazy.md` | #1 | 32 |
| `02-11-umovni-vyrazy.md` | #2 | 53 |
| `02-11-umovni-vyrazy.md` | #3 | 70 |
| `02-11-umovni-vyrazy.md` | #4 | 83 |
| `02-11-umovni-vyrazy.md` | #5 | 95 |
| `02-11-umovni-vyrazy.md` | #6 | 111 |
| `02-11-umovni-vyrazy.md` | #7 | 132 |
| `02-12-if-else-ta-ternarna-operatsiia.md` | #1 | 28 |
| `02-12-if-else-ta-ternarna-operatsiia.md` | #2 | 53 |
| `02-12-if-else-ta-ternarna-operatsiia.md` | #3 | 72 |
| `02-12-if-else-ta-ternarna-operatsiia.md` | #4 | 109 |
| `02-12-if-else-ta-ternarna-operatsiia.md` | #5 | 144 |
| `02-12-if-else-ta-ternarna-operatsiia.md` | #6 | 161 |
| `02-12-if-else-ta-ternarna-operatsiia.md` | #7 | 178 |
| `02-13-tsykly.md` | #1 | 38 |
| `02-13-tsykly.md` | #2 | 54 |
| `02-13-tsykly.md` | #3 | 68 |
| `02-13-tsykly.md` | #4 | 98 |
| `02-13-tsykly.md` | #5 | 124 |
| `02-13-tsykly.md` | #6 | 152 |
| `02-13-tsykly.md` | #7 | 165 |
| `02-13-tsykly.md` | #8 | 186 |
| `02-13-tsykly.md` | #9 | 211 |
| `02-13-tsykly.md` | #10 | 230 |
| `02-14-masyvy.md` | #1 | 25 |
| `02-14-masyvy.md` | #2 | 44 |
| `02-14-masyvy.md` | #3 | 58 |
| `02-14-masyvy.md` | #4 | 73 |
| `02-14-masyvy.md` | #5 | 85 |
| `02-14-masyvy.md` | #6 | 97 |
| `02-14-masyvy.md` | #7 | 115 |
| `02-14-masyvy.md` | #8 | 135 |
| `02-14-masyvy.md` | #9 | 153 |
| `02-14-masyvy.md` | #10 | 169 |
| `02-14-masyvy.md` | #11 | 193 |
| `02-14-masyvy.md` | #12 | 229 |
| `02-15-zavdannia-z-masyviv.md` | #1 | 21 |
| `02-15-zavdannia-z-masyviv.md` | #2 | 48 |
| `02-15-zavdannia-z-masyviv.md` | #3 | 84 |
| `02-16-metody.md` | #1 | 40 |
| `02-16-metody.md` | #2 | 66 |
| `02-16-metody.md` | #3 | 98 |
| `02-16-metody.md` | #4 | 141 |
| `02-17-parametry-metodiv.md` | #1 | 30 |
| `02-17-parametry-metodiv.md` | #2 | 56 |
| `02-17-parametry-metodiv.md` | #3 | 81 |
| `02-17-parametry-metodiv.md` | #4 | 105 |
| `02-17-parametry-metodiv.md` | #5 | 125 |
| `02-18-return.md` | #1 | 33 |
| `02-18-return.md` | #2 | 88 |
| `02-18-return.md` | #3 | 114 |
| `02-18-return.md` | #4 | 144 |
| `02-18-return.md` | #5 | 189 |
| `02-18-return.md` | #6 | 240 |
| `02-19-ref-out-in.md` | #1 | 19 |
| `02-19-ref-out-in.md` | #2 | 44 |
| `02-19-ref-out-in.md` | #3 | 69 |
| `02-19-ref-out-in.md` | #4 | 102 |
| `02-19-ref-out-in.md` | #5 | 138 |
| `02-20-params.md` | #1 | 19 |
| `02-20-params.md` | #2 | 43 |
| `02-20-params.md` | #3 | 81 |
| `02-20-params.md` | #4 | 105 |
| `02-21-rekursyvni-funktsii.md` | #1 | 28 |
| `02-21-rekursyvni-funktsii.md` | #2 | 68 |
| `02-21-rekursyvni-funktsii.md` | #3 | 87 |
| `02-22-lokalni-funktsii.md` | #1 | 19 |
| `02-22-lokalni-funktsii.md` | #2 | 41 |
| `02-22-lokalni-funktsii.md` | #3 | 70 |
| `02-22-lokalni-funktsii.md` | #4 | 98 |
| `02-23-switch.md` | #1 | 41 |
| `02-23-switch.md` | #2 | 69 |
| `02-23-switch.md` | #3 | 97 |
| `02-23-switch.md` | #4 | 125 |
| `02-23-switch.md` | #5 | 151 |
| `02-23-switch.md` | #6 | 176 |
| `03-01-klasy-ta-obiekty.md` | #1 | 17 |
| `03-01-klasy-ta-obiekty.md` | #2 | 89 |
| `03-01-klasy-ta-obiekty.md` | #3 | 115 |
| `03-01-klasy-ta-obiekty.md` | #4 | 191 |
| `03-01-klasy-ta-obiekty.md` | #5 | 248 |
| `03-01-klasy-ta-obiekty.md` | #6 | 287 |
| `03-01-klasy-ta-obiekty.md` | #7 | 325 |
| `03-01-klasy-ta-obiekty.md` | #8 | 365 |
| `03-01-klasy-ta-obiekty.md` | #9 | 419 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #1 | 21 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #2 | 52 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #3 | 95 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #4 | 130 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #5 | 168 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #6 | 200 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #7 | 222 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #8 | 260 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #9 | 301 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #10 | 335 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #11 | 371 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #12 | 405 |
| `03-02-konstruktory-initsializatory-dekonstruktory.md` | #13 | 425 |
| `03-03-program-main-ta-top-level-statements.md` | #1 | 154 |
| `03-04-struktury.md` | #1 | 56 |
| `03-04-struktury.md` | #2 | 83 |
| `03-04-struktury.md` | #3 | 108 |
| `03-04-struktury.md` | #4 | 129 |
| `03-04-struktury.md` | #5 | 163 |
| `03-04-struktury.md` | #6 | 195 |
| `03-04-struktury.md` | #7 | 214 |
| `03-04-struktury.md` | #8 | 240 |
| `03-04-struktury.md` | #9 | 268 |
| `03-04-struktury.md` | #10 | 297 |
| `03-05-typy-znachen-ta-posylan.md` | #1 | 58 |
| `03-05-typy-znachen-ta-posylan.md` | #2 | 94 |
| `03-05-typy-znachen-ta-posylan.md` | #3 | 115 |
| `03-05-typy-znachen-ta-posylan.md` | #4 | 140 |
| `03-05-typy-znachen-ta-posylan.md` | #5 | 181 |
| `04-01-uspadkuvannia.md` | #1 | 45 |
| `04-01-uspadkuvannia.md` | #2 | 99 |
| `04-01-uspadkuvannia.md` | #3 | 140 |
| `04-01-uspadkuvannia.md` | #4 | 182 |
| `04-01-uspadkuvannia.md` | #5 | 231 |
| `04-01-uspadkuvannia.md` | #6 | 281 |
| `04-01-uspadkuvannia.md` | #7 | 333 |
| `04-01-uspadkuvannia.md` | #8 | 393 |
| `04-01-uspadkuvannia.md` | #9 | 446 |
| `04-02-peretvorennia-typiv.md` | #1 | 64 |
| `04-02-peretvorennia-typiv.md` | #2 | 93 |
| `04-02-peretvorennia-typiv.md` | #3 | 130 |
| `04-02-peretvorennia-typiv.md` | #4 | 154 |
| `04-02-peretvorennia-typiv.md` | #5 | 187 |
| `04-02-peretvorennia-typiv.md` | #6 | 230 |
| `04-02-peretvorennia-typiv.md` | #7 | 275 |
| `04-03-virtualni-metody-ta-vlastyvosti.md` | #1 | 21 |
| `04-03-virtualni-metody-ta-vlastyvosti.md` | #2 | 90 |
| `04-03-virtualni-metody-ta-vlastyvosti.md` | #3 | 141 |
| `04-03-virtualni-metody-ta-vlastyvosti.md` | #4 | 182 |
| `04-03-virtualni-metody-ta-vlastyvosti.md` | #5 | 230 |
| `04-03-virtualni-metody-ta-vlastyvosti.md` | #6 | 285 |
| `04-04-prykhovuvannia-metodiv-ta-vlastyvostei.md` | #1 | 21 |
| `04-04-prykhovuvannia-metodiv-ta-vlastyvostei.md` | #2 | 65 |
| `04-04-prykhovuvannia-metodiv-ta-vlastyvostei.md` | #3 | 102 |
| `04-04-prykhovuvannia-metodiv-ta-vlastyvostei.md` | #4 | 141 |
| `04-04-prykhovuvannia-metodiv-ta-vlastyvostei.md` | #5 | 180 |
| `04-05-vidminnist-perevyznachennia-ta-prykhovuvannia.md` | #1 | 19 |
| `04-05-vidminnist-perevyznachennia-ta-prykhovuvannia.md` | #2 | 66 |
| `04-05-vidminnist-perevyznachennia-ta-prykhovuvannia.md` | #3 | 105 |
| `04-06-abstraktni-klasy-ta-chleny-klasiv.md` | #1 | 25 |
| `04-06-abstraktni-klasy-ta-chleny-klasiv.md` | #2 | 75 |
| `04-06-abstraktni-klasy-ta-chleny-klasiv.md` | #3 | 137 |
| `04-06-abstraktni-klasy-ta-chleny-klasiv.md` | #4 | 186 |
| `04-07-system-object-ta-ioho-metody.md` | #1 | 21 |
| `04-07-system-object-ta-ioho-metody.md` | #2 | 45 |
| `04-07-system-object-ta-ioho-metody.md` | #3 | 91 |
| `04-07-system-object-ta-ioho-metody.md` | #4 | 119 |
| `04-07-system-object-ta-ioho-metody.md` | #5 | 152 |
| `04-07-system-object-ta-ioho-metody.md` | #6 | 190 |
| `04-08-uzahalnennia.md` | #1 | 21 |
| `04-08-uzahalnennia.md` | #2 | 66 |
| `04-08-uzahalnennia.md` | #3 | 112 |
| `04-08-uzahalnennia.md` | #4 | 144 |
| `04-08-uzahalnennia.md` | #5 | 165 |
| `04-08-uzahalnennia.md` | #6 | 194 |
| `04-08-uzahalnennia.md` | #7 | 232 |
| `04-09-obmezhennia-uzahalnen.md` | #1 | 21 |
| `04-09-obmezhennia-uzahalnen.md` | #2 | 55 |
| `04-09-obmezhennia-uzahalnen.md` | #3 | 97 |
| `04-09-obmezhennia-uzahalnen.md` | #4 | 140 |
| `04-09-obmezhennia-uzahalnen.md` | #5 | 173 |
| `04-09-obmezhennia-uzahalnen.md` | #6 | 203 |
| `04-09-obmezhennia-uzahalnen.md` | #7 | 227 |
| `04-09-obmezhennia-uzahalnen.md` | #8 | 259 |
| `04-10-nasliduvannia-uzahalnenykh-typiv.md` | #1 | 39 |
| `04-10-nasliduvannia-uzahalnenykh-typiv.md` | #2 | 75 |
| `04-10-nasliduvannia-uzahalnenykh-typiv.md` | #3 | 115 |
| `04-10-nasliduvannia-uzahalnenykh-typiv.md` | #4 | 152 |
| `04-10-nasliduvannia-uzahalnenykh-typiv.md` | #5 | 191 |
| `05-01-try-catch-finally.md` | #1 | 60 |
| `05-01-try-catch-finally.md` | #2 | 90 |
| `05-01-try-catch-finally.md` | #3 | 122 |
| `05-01-try-catch-finally.md` | #4 | 147 |
| `05-01-try-catch-finally.md` | #5 | 178 |
| `05-02-blok-catch-ta-filtry-vyniatkiv.md` | #1 | 30 |
| `05-02-blok-catch-ta-filtry-vyniatkiv.md` | #2 | 60 |
| `05-02-blok-catch-ta-filtry-vyniatkiv.md` | #3 | 95 |
| `05-02-blok-catch-ta-filtry-vyniatkiv.md` | #4 | 137 |
| `05-02-blok-catch-ta-filtry-vyniatkiv.md` | #5 | 175 |
| `05-03-typy-vyniatkiv-klas-exception.md` | #1 | 27 |
| `05-03-typy-vyniatkiv-klas-exception.md` | #2 | 69 |
| `05-03-typy-vyniatkiv-klas-exception.md` | #3 | 111 |
| `05-03-typy-vyniatkiv-klas-exception.md` | #4 | 141 |
| `05-03-typy-vyniatkiv-klas-exception.md` | #5 | 174 |
| `05-04-heneratsiia-vyniatku-ta-operator-throw.md` | #1 | 35 |
| `05-04-heneratsiia-vyniatku-ta-operator-throw.md` | #2 | 57 |
| `05-04-heneratsiia-vyniatku-ta-operator-throw.md` | #3 | 95 |
| `05-04-heneratsiia-vyniatku-ta-operator-throw.md` | #4 | 130 |
| `05-04-heneratsiia-vyniatku-ta-operator-throw.md` | #5 | 183 |
| `05-05-stvorennia-klasiv-vyniatkiv.md` | #1 | 23 |
| `05-05-stvorennia-klasiv-vyniatkiv.md` | #2 | 54 |
| `05-05-stvorennia-klasiv-vyniatkiv.md` | #3 | 92 |
| `05-05-stvorennia-klasiv-vyniatkiv.md` | #4 | 136 |
| `05-06-poshuk-bloku-catch-pry-obrobtsi-vyniatkiv.md` | #1 | 29 |
| `05-06-poshuk-bloku-catch-pry-obrobtsi-vyniatkiv.md` | #2 | 107 |
| `05-06-poshuk-bloku-catch-pry-obrobtsi-vyniatkiv.md` | #3 | 138 |
| `06-01-delehaty.md` | #1 | 27 |
| `06-01-delehaty.md` | #2 | 44 |
| `06-01-delehaty.md` | #3 | 110 |
| `06-01-delehaty.md` | #4 | 170 |
| `06-01-delehaty.md` | #5 | 188 |
| `06-01-delehaty.md` | #6 | 206 |
| `06-01-delehaty.md` | #7 | 231 |
| `06-01-delehaty.md` | #8 | 254 |
| `06-01-delehaty.md` | #9 | 273 |
| `06-01-delehaty.md` | #10 | 309 |
| `06-01-delehaty.md` | #11 | 327 |
| `06-01-delehaty.md` | #12 | 346 |
| `06-01-delehaty.md` | #13 | 374 |
| `06-01-delehaty.md` | #14 | 399 |
| `06-01-delehaty.md` | #17 | 620 |
| `06-01-delehaty.md` | #18 | 637 |
| `06-01-delehaty.md` | #19 | 655 |
| `06-01-delehaty.md` | #20 | 672 |
| `06-01-delehaty.md` | #21 | 688 |
| `06-02-liambdy.md` | #1 | 27 |
| `06-02-liambdy.md` | #2 | 41 |
| `06-02-liambdy.md` | #3 | 58 |
| `06-02-liambdy.md` | #4 | 71 |
| `06-02-liambdy.md` | #5 | 85 |
| `06-02-liambdy.md` | #6 | 95 |
| `06-02-liambdy.md` | #7 | 109 |
| `06-02-liambdy.md` | #8 | 126 |
| `06-02-liambdy.md` | #10 | 172 |
| `06-02-liambdy.md` | #11 | 200 |
| `06-05-delehaty-action-predicate-ta-func.md` | #1 | 28 |
| `06-05-delehaty-action-predicate-ta-func.md` | #2 | 48 |
| `06-05-delehaty-action-predicate-ta-func.md` | #3 | 72 |
| `06-05-delehaty-action-predicate-ta-func.md` | #4 | 87 |
| `06-05-delehaty-action-predicate-ta-func.md` | #5 | 120 |
| `06-05-delehaty-action-predicate-ta-func.md` | #6 | 134 |
| `06-05-delehaty-action-predicate-ta-func.md` | #7 | 168 |
| `06-05-delehaty-action-predicate-ta-func.md` | #8 | 194 |
| `06-05-delehaty-action-predicate-ta-func.md` | #9 | 223 |
| `06-05-delehaty-action-predicate-ta-func.md` | #10 | 250 |
| `07-01-vyznachennia-interfeisiv.md` | #1 | 61 |
| `07-01-vyznachennia-interfeisiv.md` | #4 | 158 |
| `07-02-zastosuvannia-interfeisiv.md` | #2 | 74 |
| `07-02-zastosuvannia-interfeisiv.md` | #3 | 118 |
| `07-02-zastosuvannia-interfeisiv.md` | #4 | 161 |
| `07-02-zastosuvannia-interfeisiv.md` | #5 | 204 |
| `07-02-zastosuvannia-interfeisiv.md` | #6 | 259 |
| `07-02-zastosuvannia-interfeisiv.md` | #7 | 288 |
| `07-03-yavna-realizatsiia-interfeisiv.md` | #2 | 50 |
| `07-03-yavna-realizatsiia-interfeisiv.md` | #5 | 143 |
| `07-04-uspadkuvannia-interfeisiv.md` | #1 | 37 |
| `07-04-uspadkuvannia-interfeisiv.md` | #2 | 93 |
| `07-04-uspadkuvannia-interfeisiv.md` | #3 | 175 |
| `07-04-uspadkuvannia-interfeisiv.md` | #4 | 258 |
| `07-04-uspadkuvannia-interfeisiv.md` | #5 | 298 |
| `07-05-interfeisy-v-uzahalnenniakh.md` | #1 | 33 |
| `07-05-interfeisy-v-uzahalnenniakh.md` | #2 | 105 |
| `07-05-interfeisy-v-uzahalnenniakh.md` | #3 | 178 |
| `07-05-interfeisy-v-uzahalnenniakh.md` | #4 | 234 |
| `07-06-kopiiuvannia-obiektiv-interfeis-icloneable.md` | #1 | 17 |
| `07-06-kopiiuvannia-obiektiv-interfeis-icloneable.md` | #2 | 69 |
| `07-06-kopiiuvannia-obiektiv-interfeis-icloneable.md` | #3 | 105 |
| `07-06-kopiiuvannia-obiektiv-interfeis-icloneable.md` | #4 | 159 |
| `07-06-kopiiuvannia-obiektiv-interfeis-icloneable.md` | #5 | 230 |
| `07-07-kovariantnist-ta-kontravariantnist-uzahalnenykh-interfeisiv.md` | #1 | 54 |
| `07-07-kovariantnist-ta-kontravariantnist-uzahalnenykh-interfeisiv.md` | #2 | 130 |
| `07-07-kovariantnist-ta-kontravariantnist-uzahalnenykh-interfeisiv.md` | #3 | 183 |
| `08-01-vyznachennia-operatoriv.md` | #1 | 71 |
| `08-01-vyznachennia-operatoriv.md` | #2 | 117 |
| `08-01-vyznachennia-operatoriv.md` | #3 | 162 |
| `08-02-vyznachennia-inkrementu-ta-dekrementu.md` | #1 | 44 |
| `08-02-vyznachennia-inkrementu-ta-dekrementu.md` | #2 | 88 |
| `08-02-vyznachennia-inkrementu-ta-dekrementu.md` | #3 | 130 |
| `08-02-vyznachennia-inkrementu-ta-dekrementu.md` | #4 | 180 |
| `08-03-perevantazhennia-operatsii-peretvorennia-typiv.md` | #1 | 49 |
| `08-03-perevantazhennia-operatsii-peretvorennia-typiv.md` | #2 | 85 |
| `08-03-perevantazhennia-operatsii-peretvorennia-typiv.md` | #3 | 119 |
| `08-04-indeksatory.md` | #1 | 39 |
| `08-04-indeksatory.md` | #2 | 104 |
| `08-04-indeksatory.md` | #3 | 160 |
| `08-04-indeksatory.md` | #4 | 223 |
| `08-05-zminni-posylannia-ta-povernennia-posylannia.md` | #1 | 36 |
| `08-05-zminni-posylannia-ta-povernennia-posylannia.md` | #2 | 84 |
| `08-05-zminni-posylannia-ta-povernennia-posylannia.md` | #3 | 118 |
| `08-06-metody-rozshyrennia.md` | #1 | 44 |
| `08-06-metody-rozshyrennia.md` | #2 | 75 |
| `08-06-metody-rozshyrennia.md` | #3 | 112 |
| `08-07-chastkovi-klasy-ta-metody.md` | #1 | 60 |
| `08-07-chastkovi-klasy-ta-metody.md` | #2 | 132 |
| `08-08-anonimni-typy.md` | #1 | 45 |
| `08-08-anonimni-typy.md` | #2 | 79 |
| `08-09-kortezhi.md` | #2 | 111 |
| `08-09-kortezhi.md` | #3 | 150 |
| `08-10-records.md` | #1 | 113 |
| `08-10-records.md` | #2 | 140 |
| `08-10-records.md` | #3 | 173 |
| `09-01-patern-typiv.md` | #1 | 67 |
| `09-01-patern-typiv.md` | #2 | 160 |
| `09-02-patern-vlastyvostei.md` | #1 | 35 |
| `09-02-patern-vlastyvostei.md` | #2 | 105 |
| `09-03-paterny-kortezhiv.md` | #1 | 46 |
| `09-03-paterny-kortezhiv.md` | #2 | 88 |
| `09-04-pozytsiinyi-patern.md` | #1 | 48 |
| `09-04-pozytsiinyi-patern.md` | #2 | 83 |
| `09-05-reliatsiinyi-ta-lohichnyi-paterny.md` | #1 | 68 |
| `09-06-paterny-spyskiv.md` | #1 | 64 |
| `09-06-paterny-spyskiv.md` | #2 | 110 |
| `10-01-spysok-list-t.md` | #1 | 79 |
| `10-01-spysok-list-t.md` | #2 | 116 |
| `10-02-dvozviazanyi-spysok-linkedlist-t.md` | #1 | 65 |
| `10-02-dvozviazanyi-spysok-linkedlist-t.md` | #2 | 136 |
| `10-03-cherha-queue.md` | #1 | 98 |
| `10-03-cherha-queue.md` | #2 | 134 |
| `10-04-stack-t.md` | #1 | 107 |
| `10-04-stack-t.md` | #2 | 148 |
| `10-05-slovnyk-dictionary-k-v.md` | #1 | 181 |
| `10-05-slovnyk-dictionary-k-v.md` | #2 | 234 |
| `10-06-klas-observablecollection.md` | #1 | 87 |
| `10-06-klas-observablecollection.md` | #2 | 136 |
| `10-07-ienumerable-ienumerator.md` | #1 | 77 |
| `10-07-ienumerable-ienumerator.md` | #2 | 126 |
| `10-08-iteratory-ta-yield-return.md` | #1 | 63 |
| `10-08-iteratory-ta-yield-return.md` | #2 | 115 |
| `11-01-riadky-ta-klas-string.md` | #1 | 200 |
| `11-01-riadky-ta-klas-string.md` | #2 | 230 |
| `11-02-operatsii-z-riadkamy.md` | #1 | 240 |
| `11-02-operatsii-z-riadkamy.md` | #2 | 276 |
| `11-03-formatuvannia-ta-interpoliatsiia-riadkiv.md` | #1 | 190 |
| `11-03-formatuvannia-ta-interpoliatsiia-riadkiv.md` | #2 | 226 |
| `11-04-klas-stringbuilder.md` | #1 | 193 |
| `11-04-klas-stringbuilder.md` | #2 | 223 |
| `11-05-rehuliarni-vyrazy.md` | #1 | 237 |
| `11-05-rehuliarni-vyrazy.md` | #2 | 272 |
| `12-01-struktura-datetime.md` | #1 | 188 |
| `12-01-struktura-datetime.md` | #2 | 224 |
| `12-02-nalashtuvannia-formatu-chasu-ta-daty.md` | #1 | 172 |
| `12-02-nalashtuvannia-formatu-chasu-ta-daty.md` | #2 | 205 |
| `12-03-dateonly-ta-timeonly.md` | #1 | 233 |
| `12-03-dateonly-ta-timeonly.md` | #2 | 278 |
| `12-04-timespan.md` | #1 | 146 |
| `12-04-timespan.md` | #2 | 187 |
| `12-05-datetimeoffset-ta-chasovi-poiasy.md` | #1 | 212 |
| `12-05-datetimeoffset-ta-chasovi-poiasy.md` | #2 | 250 |
| `13-02-klas-math.md` | #1 | 222 |
| `13-02-klas-math.md` | #2 | 276 |
| `13-03-klas-convert.md` | #1 | 143 |
| `13-03-klas-convert.md` | #2 | 203 |
| `13-04-klas-array.md` | #2 | 253 |
| `13-05-span.md` | #1 | 160 |
| `13-05-span.md` | #2 | 213 |
| `13-06-indeksy-ta-diapazony.md` | #1 | 136 |
| `13-06-indeksy-ta-diapazony.md` | #2 | 182 |
| `15-01-vstup-u-bahatopotochnist-klas-thread.md` | #1 | 47 |
| `15-01-vstup-u-bahatopotochnist-klas-thread.md` | #2 | 95 |
| `15-01-vstup-u-bahatopotochnist-klas-thread.md` | #3 | 124 |
| `15-01-vstup-u-bahatopotochnist-klas-thread.md` | #4 | 155 |
| `15-01-vstup-u-bahatopotochnist-klas-thread.md` | #5 | 197 |
| `15-01-vstup-u-bahatopotochnist-klas-thread.md` | #6 | 242 |
| `15-01-vstup-u-bahatopotochnist-klas-thread.md` | #7 | 303 |
| `15-01-vstup-u-bahatopotochnist-klas-thread.md` | #8 | 358 |
| `15-02-stvorennia-potokiv-threadstart.md` | #1 | 29 |
| `15-02-stvorennia-potokiv-threadstart.md` | #2 | 51 |
| `15-02-stvorennia-potokiv-threadstart.md` | #3 | 73 |
| `15-02-stvorennia-potokiv-threadstart.md` | #4 | 103 |
| `15-02-stvorennia-potokiv-threadstart.md` | #6 | 183 |
| `15-03-synkhronizatsiia-potokiv-lock.md` | #1 | 19 |
| `15-03-synkhronizatsiia-potokiv-lock.md` | #2 | 69 |
| `15-03-synkhronizatsiia-potokiv-lock.md` | #4 | 189 |
| `15-04-klas-monitor.md` | #3 | 256 |
| `15-05-autoresetevent.md` | #1 | 35 |
| `15-05-autoresetevent.md` | #2 | 74 |
| `15-05-autoresetevent.md` | #3 | 140 |
| `15-06-mutex.md` | #1 | 35 |
| `15-06-mutex.md` | #2 | 81 |
| `15-06-mutex.md` | #3 | 119 |
| `15-06-mutex.md` | #4 | 178 |
| `15-07-semaphore.md` | #1 | 48 |
| `15-07-semaphore.md` | #2 | 100 |
| `15-07-semaphore.md` | #3 | 147 |
| `15-07-semaphore.md` | #4 | 186 |
| `16-01-klas-task-osnovy-tpl.md` | #1 | 29 |
| `16-01-klas-task-osnovy-tpl.md` | #2 | 51 |
| `16-01-klas-task-osnovy-tpl.md` | #3 | 71 |
| `16-01-klas-task-osnovy-tpl.md` | #4 | 105 |
| `16-01-klas-task-osnovy-tpl.md` | #5 | 145 |
| `16-01-klas-task-osnovy-tpl.md` | #6 | 166 |
| `16-01-klas-task-osnovy-tpl.md` | #7 | 184 |
| `16-01-klas-task-osnovy-tpl.md` | #8 | 211 |
| `16-01-klas-task-osnovy-tpl.md` | #9 | 231 |
| `16-02-vkladeni-zavdannia-task-t.md` | #1 | 19 |
| `16-02-vkladeni-zavdannia-task-t.md` | #2 | 52 |
| `16-02-vkladeni-zavdannia-task-t.md` | #3 | 92 |
| `16-02-vkladeni-zavdannia-task-t.md` | #4 | 124 |
| `16-02-vkladeni-zavdannia-task-t.md` | #5 | 149 |
| `16-02-vkladeni-zavdannia-task-t.md` | #7 | 214 |
| `16-03-prodovzhennia-zavdan-continuewith.md` | #1 | 17 |
| `16-03-prodovzhennia-zavdan-continuewith.md` | #2 | 50 |
| `16-03-prodovzhennia-zavdan-continuewith.md` | #3 | 100 |
| `16-03-prodovzhennia-zavdan-continuewith.md` | #4 | 150 |
| `16-03-prodovzhennia-zavdan-continuewith.md` | #5 | 194 |
| `16-04-klas-parallel.md` | #1 | 21 |
| `16-04-klas-parallel.md` | #2 | 60 |
| `16-04-klas-parallel.md` | #3 | 87 |
| `16-04-klas-parallel.md` | #4 | 126 |
| `16-04-klas-parallel.md` | #5 | 156 |
| `16-04-klas-parallel.md` | #6 | 185 |
| `16-04-klas-parallel.md` | #7 | 223 |
| `16-05-skasuvannia-zavdan-cancellationtoken.md` | #1 | 33 |
| `16-05-skasuvannia-zavdan-cancellationtoken.md` | #3 | 123 |
| `16-05-skasuvannia-zavdan-cancellationtoken.md` | #4 | 151 |
| `16-05-skasuvannia-zavdan-cancellationtoken.md` | #5 | 190 |
| `16-05-skasuvannia-zavdan-cancellationtoken.md` | #6 | 222 |
| `16-05-skasuvannia-zavdan-cancellationtoken.md` | #7 | 260 |
| `17-01-async-await-asynchronni-metody.md` | #1 | 45 |
| `17-01-async-await-asynchronni-metody.md` | #2 | 67 |
| `17-01-async-await-asynchronni-metody.md` | #3 | 107 |
| `17-01-async-await-asynchronni-metody.md` | #4 | 144 |
| `17-01-async-await-asynchronni-metody.md` | #5 | 184 |
| `17-02-typy-povernennia-async-metodiv.md` | #1 | 23 |
| `17-02-typy-povernennia-async-metodiv.md` | #2 | 89 |
| `17-02-typy-povernennia-async-metodiv.md` | #3 | 132 |
| `17-02-typy-povernennia-async-metodiv.md` | #4 | 184 |
| `17-03-poslidovne-ta-paralelne-vykonannia.md` | #1 | 21 |
| `17-03-poslidovne-ta-paralelne-vykonannia.md` | #2 | 66 |
| `17-03-poslidovne-ta-paralelne-vykonannia.md` | #3 | 108 |
| `17-03-poslidovne-ta-paralelne-vykonannia.md` | #4 | 152 |
| `17-03-poslidovne-ta-paralelne-vykonannia.md` | #5 | 182 |
| `17-03-poslidovne-ta-paralelne-vykonannia.md` | #6 | 226 |
| `17-03-poslidovne-ta-paralelne-vykonannia.md` | #7 | 252 |
| `17-03-poslidovne-ta-paralelne-vykonannia.md` | #8 | 288 |
| `17-04-obrobka-pomylok-v-async.md` | #1 | 21 |
| `17-04-obrobka-pomylok-v-async.md` | #2 | 63 |
| `17-04-obrobka-pomylok-v-async.md` | #3 | 110 |
| `17-04-obrobka-pomylok-v-async.md` | #4 | 134 |
| `17-04-obrobka-pomylok-v-async.md` | #5 | 183 |
| `17-04-obrobka-pomylok-v-async.md` | #6 | 235 |
| `17-04-obrobka-pomylok-v-async.md` | #7 | 270 |
| `17-04-obrobka-pomylok-v-async.md` | #8 | 302 |
| `17-04-obrobka-pomylok-v-async.md` | #9 | 325 |
| `17-05-skasuvannia-async-operatsii.md` | #1 | 21 |
| `17-05-skasuvannia-async-operatsii.md` | #2 | 66 |
| `17-05-skasuvannia-async-operatsii.md` | #3 | 113 |
| `17-05-skasuvannia-async-operatsii.md` | #4 | 147 |
| `17-05-skasuvannia-async-operatsii.md` | #5 | 197 |
| `17-05-skasuvannia-async-operatsii.md` | #6 | 242 |
| `17-05-skasuvannia-async-operatsii.md` | #7 | 301 |
| `17-06-async-potoky-iasyncenumerable.md` | #1 | 21 |
| `17-06-async-potoky-iasyncenumerable.md` | #2 | 74 |
| `17-06-async-potoky-iasyncenumerable.md` | #3 | 118 |
| `17-06-async-potoky-iasyncenumerable.md` | #4 | 149 |
| `17-06-async-potoky-iasyncenumerable.md` | #5 | 205 |
| `18-01-path-file-directory.md` | #1 | 19 |
| `18-01-path-file-directory.md` | #2 | 35 |
| `18-01-path-file-directory.md` | #3 | 60 |
| `18-01-path-file-directory.md` | #4 | 83 |
| `18-01-path-file-directory.md` | #5 | 109 |
| `18-01-path-file-directory.md` | #6 | 144 |
| `18-01-path-file-directory.md` | #7 | 163 |
| `18-01-path-file-directory.md` | #8 | 189 |
| `18-01-path-file-directory.md` | #9 | 217 |
| `18-01-path-file-directory.md` | #10 | 235 |
| `18-01-path-file-directory.md` | #11 | 272 |
| `18-02-fileinfo-directoryinfo.md` | #1 | 25 |
| `18-02-fileinfo-directoryinfo.md` | #2 | 60 |
| `18-02-fileinfo-directoryinfo.md` | #3 | 106 |
| `18-02-fileinfo-directoryinfo.md` | #4 | 155 |
| `18-02-fileinfo-directoryinfo.md` | #5 | 201 |
| `18-02-fileinfo-directoryinfo.md` | #6 | 242 |
| `18-02-fileinfo-directoryinfo.md` | #7 | 285 |
| `18-02-fileinfo-directoryinfo.md` | #8 | 324 |
| `18-03-stream-filestream.md` | #1 | 23 |
| `18-03-stream-filestream.md` | #2 | 72 |
| `18-03-stream-filestream.md` | #3 | 128 |
| `18-03-stream-filestream.md` | #4 | 164 |
| `18-03-stream-filestream.md` | #5 | 202 |
| `18-03-stream-filestream.md` | #6 | 258 |
| `18-03-stream-filestream.md` | #7 | 304 |
| `18-03-stream-filestream.md` | #8 | 345 |
| `18-04-streamreader-streamwriter.md` | #1 | 25 |
| `18-04-streamreader-streamwriter.md` | #2 | 63 |
| `18-04-streamreader-streamwriter.md` | #3 | 99 |
| `18-04-streamreader-streamwriter.md` | #4 | 139 |
| `18-04-streamreader-streamwriter.md` | #5 | 176 |
| `18-04-streamreader-streamwriter.md` | #6 | 221 |
| `18-04-streamreader-streamwriter.md` | #7 | 274 |
| `18-05-binaryreader-binarywriter.md` | #1 | 21 |
| `18-05-binaryreader-binarywriter.md` | #2 | 60 |
| `18-05-binaryreader-binarywriter.md` | #3 | 117 |
| `18-05-binaryreader-binarywriter.md` | #4 | 177 |
| `18-05-binaryreader-binarywriter.md` | #5 | 256 |
| `19-01-system-text-json-advanced.md` | #1 | 23 |
| `19-01-system-text-json-advanced.md` | #2 | 81 |
| `19-01-system-text-json-advanced.md` | #3 | 126 |
| `19-01-system-text-json-advanced.md` | #7 | 354 |
| `19-02-xml-xmldocument.md` | #1 | 21 |
| `19-02-xml-xmldocument.md` | #2 | 62 |
| `19-02-xml-xmldocument.md` | #3 | 137 |
| `19-02-xml-xmldocument.md` | #4 | 190 |
| `19-02-xml-xmldocument.md` | #5 | 261 |
| `19-03-xdocument-linq-to-xml.md` | #1 | 23 |
| `19-03-xdocument-linq-to-xml.md` | #4 | 177 |
| `19-03-xdocument-linq-to-xml.md` | #5 | 248 |
| `19-04-xmlreader-xmlwriter.md` | #1 | 25 |
| `19-04-xmlreader-xmlwriter.md` | #2 | 91 |
| `19-04-xmlreader-xmlwriter.md` | #3 | 167 |
| `19-04-xmlreader-xmlwriter.md` | #4 | 232 |
| `19-04-xmlreader-xmlwriter.md` | #6 | 362 |
| `19-06-xpath-json-vs-xml.md` | #1 | 67 |
| `19-06-xpath-json-vs-xml.md` | #2 | 137 |
| `19-06-xpath-json-vs-xml.md` | #3 | 183 |
| `19-06-xpath-json-vs-xml.md` | #4 | 233 |
| `19-06-xpath-json-vs-xml.md` | #5 | 312 |
| `20-06-dip.md` | #6 | 489 |
| `21-01-generic-host.md` | #1 | 21 |
| `21-01-generic-host.md` | #2 | 159 |
| `21-02-iservicecollection.md` | #1 | 62 |
| `21-03-service-lifetimes.md` | #1 | 64 |
| `21-03-service-lifetimes.md` | #2 | 354 |
| `21-04-options-pattern.md` | #1 | 104 |
