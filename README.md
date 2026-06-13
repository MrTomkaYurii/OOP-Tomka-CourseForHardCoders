# OOP C# Course — Медична Клініка

Еталонний навчальний курс з об'єктно-орієнтованого програмування на C# / .NET 9.  
Курс побудований навколо єдиного наскрізного проєкту — **консольної системи управління медичною клінікою**, яка розвивається від лабораторної до лабораторної.

**Сайт курсу:** [tomka.space](https://tomka.space)

---

## Концепція

Студент будує **одну живу систему** протягом усього семестру. Кожна лаба = нова гілка = нова функціональність поверх попередньої. Еталонний домен — **Медична Клініка**. Студент обирає свій домен (готель, ресторан, бібліотека тощо) і транспонує завдання під нього.

Правило прогресії: кожна лаба вводить **тільки свої** C# конструкції. Використання конструкцій наперед — заборонено (наприклад, `List<T>` не раніше Lab 04, LINQ не раніше Lab 14).

---

## Структура репозиторію

```
OOP-Tomka-CourseForHardCoders/
├── src/                        ← Еталонний C# проєкт (росте весь курс)
├── sandbox/                    ← Ізольовані завдання Lab 01–02
├── labs/                       ← Інструкції до кожної лабораторної
├── lectures/                   ← Теоретичні матеріали (20 розділів, 151 секція)
├── runner/                     ← Blazor WASM — виконання C# у браузері
├── site/                       ← Astro сайт курсу
├── tools/                      ← Інструменти розробки курсу
├── сoncept/                    ← Документи з проєктування курсу
├── .github/workflows/          ← CI/CD: GitHub Actions → tomka.space
└── OOP-Tomka-CourseForHardCoders.sln
```

---

## `src/` — Еталонний проєкт

Головний C# проєкт (`ClinicApp.csproj`). Єдина точка входу — `Program.cs`. Росте з кожною лабою.

```
src/
├── Program.cs                  ← точка входу, росте весь курс
├── Clinic.cs                   ← оркестратор (Lab 03+)
├── ClinicApp.csproj
├── Models/                     ← Patient, Doctor, Appointment, WorkSchedule (Lab 03+)
│                                  MedicalRecord, Diagnosis, LabResult, Prescription (Lab 06+)
├── Managers/                   ← PatientManager, DoctorManager, AppointmentManager (Lab 03+)
│                                  MedicalRecordManager (Lab 06+), BillingManager (Lab 07+)
│                                  Repository<T> (Lab 09+), AnalyticsManager (Lab 10+)
│                                  ReportManager (Lab 14+)
├── Interfaces/                 ← IPayable, ICancellable, ISchedulable (Lab 07+)
│                                  IIdentifiable (Lab 09+)
├── Enums/                      ← BloodType, Speciality, AppointmentStatus (Lab 04+)
├── Attributes/                 ← RequiredAttribute, MaxLengthAttribute (Lab 11+)
├── Comparators/                ← IComparer<T> реалізації (Lab 10+)
├── Events/                     ← EventArgs класи (Lab 13+)
├── Extensions/                 ← методи розширення (Lab 15+)
├── Strategies/                 ← стратегії (Lab 15+)
├── Infrastructure/             ← EF Core контекст, конфігурації (Lab 17+)
├── Data/                       ← Migrations, seeding (Lab 17+)
├── Services/                   ← сервісний шар (Lab 19+)
└── Utils/                      ← ClinicFormatter (Lab 04), ClinicValidator (Lab 05),
                                   ModelValidator, FormBuilder (Lab 11),
                                   ClinicLogger, ClinicExporter, CsvImporter (Lab 12)
```

---

## `sandbox/` — Ізольовані вправи

Використовується тільки для перших двох лаб, де ще немає доменної моделі.

```
sandbox/
├── intro/          ← Lab 01: базовий C# (типи, умови, цикли, методи)
└── arrays/         ← Lab 02: масиви (1D, 2D, jagged, 3D)
```

---

## `labs/` — Інструкції до лабораторних

Кожна лаба — окрема папка з файлом `instructions.md`. Інструкції написані **в абстрактному вигляді** (Сутність A, Операція, Користувач) — студент підставляє свій домен.

```
labs/
├── lab-01-intro/
├── lab-02-arrays/
├── lab-03-classes/
├── lab-04-class-members/
├── lab-05-encapsulation/
├── lab-06-inheritance/
├── lab-07-interfaces/
├── lab-08-polymorphism/
├── lab-09-generics/
├── lab-10-iterators/
├── lab-11-reflection/
├── lab-12-files/
├── lab-13-events/
├── lab-14-linq/
├── lab-15-functional/
├── lab-16-console-ui/
├── lab-17-ef-basic/
├── lab-18-ef-relations/
├── lab-19-ef-advanced/
├── lab-20-ef-queries/
├── lab-21-async/
└── lab-22-solid-di/
```

---

## `lectures/` — Теоретичні матеріали

151 секція у форматі Markdown, розподілені по 20 розділах. Кожен файл — одна тема.

```
lectures/
├── sections/                   ← 151 .md файл (01-01 … 20-06)
│   ├── 01-xx-*.md              ← Розділ 1: Роль платформи, .NET, JIT
│   ├── 02-xx-*.md              ← Розділ 2: Синтаксис C# (змінні, типи, методи)
│   ├── 03-xx-*.md              ← Розділ 3: Класи та об'єкти
│   ├── 04-xx-*.md              ← Розділ 4: Члени класу (enum, struct, індексатори)
│   ├── 05-xx-*.md              ← Розділ 5: Інкапсуляція
│   ├── 06-xx-*.md              ← Розділ 6: Делегати, лямбди, події
│   ├── 07-xx-*.md              ← Розділ 7: Інтерфейси
│   ├── 08-xx-*.md              ← Розділ 8: Додаткові можливості ООП
│   ├── 09-xx-*.md              ← Розділ 9: Pattern matching
│   ├── 10-xx-*.md              ← Розділ 10: Успадкування
│   ├── 11-xx-*.md              ← Розділ 11: Рефлексія та атрибути
│   ├── 12-xx-*.md              ← Розділ 12: Файли та серіалізація
│   ├── 13-xx-*.md              ← Розділ 13: Додаткові класи .NET (Array, List, Dictionary)
│   ├── 14-xx-*.md              ← Розділ 14: LINQ
│   ├── 15-xx-*.md              ← Розділ 15: Функціональне програмування
│   ├── 16-xx-*.md              ← Розділ 16: Console UI
│   ├── 17-xx-*.md              ← Розділ 17: Асинхронне програмування
│   ├── 18-xx-*.md              ← Розділ 18: Entity Framework Core (базовий)
│   ├── 19-xx-*.md              ← Розділ 19: EF Core (відносини)
│   └── 20-xx-*.md              ← Розділ 20: EF Core (запити та оптимізація)
├── _assets/                    ← PNG діаграми (по папці на кожну секцію)
│   └── XX-XX/                  ← наприклад _assets/07-02/multiple-interfaces.png
└── _docx/                      ← .docx джерела (Word-версії лекцій)
```

### Формат секції

Кожен `.md` файл має frontmatter:

```yaml
---
chapter: 7
chapterTitle: "Розділ 7. Інтерфейси"
section: 2
number: "7.2"
title: "Застосування інтерфейсів"
---
```

Блоки коду з атрибутом ` ```csharp run ` є **виконуваними** — вони запускаються безпосередньо в браузері через Blazor WASM runner.

---

## `runner/` — Blazor WASM Runner

In-browser C# компілятор на основі Roslyn. Компілює та виконує `csharp run` блоки прямо у браузері без серверної частини.

```
runner/
├── runner.csproj               ← .NET 9 Blazor WASM
├── Program.cs
├── App.razor
├── Services/
│   └── CSharpRunner.cs         ← Roslyn компіляція + виконання
├── Pages/
│   └── RunnerPage.razor        ← UI runner-а
└── wwwroot/
    ├── index.html              ← base href встановлюється при deploy
    └── js/runner.js            ← postMessage міст між сайтом та runner iframe
```

**Обмеження:** `System.Threading.Thread` не підтримується у WebAssembly (однопоточна модель). При виклику `Thread.Start()` runner показує людське повідомлення з посиланням на dotnetfiddle.net.

---

## `site/` — Astro сайт

Статичний сайт курсу на [Astro](https://astro.build). Деплоїться на [tomka.space](https://tomka.space) через GitHub Actions.

```
site/
├── astro.config.mjs            ← base path визначається з configure-pages output
├── package.json
├── src/
│   ├── pages/                  ← маршрути сайту
│   ├── layouts/                ← BaseLayout, LectureLayout
│   ├── components/             ← UI компоненти
│   ├── data/                   ← дані курсу (лекції, лаби)
│   ├── styles/                 ← глобальні стилі
│   └── utils/                  ← утиліти
└── public/
    ├── CNAME                   ← tomka.space (для GitHub Pages)
    └── runner/                 ← Blazor runner (копіюється при build)
```

---

## `tools/` — Інструменти розробки

```
tools/
├── code-checker/               ← .NET 9 консольний проєкт
│   ├── code-checker.csproj     ← використовує Microsoft.CodeAnalysis.CSharp
│   └── Program.cs              ← сканує всі секції, компілює csharp run блоки
└── report.md                   ← згенерований звіт (727 блоків, 0 помилок)
```

### Запуск перевірки

```bash
cd tools/code-checker
dotnet run
```

Генерує `tools/report.md` — таблицю з усіма `csharp run` блоками, статусом компіляції та помилками. Використовується для контролю якості лекційних прикладів перед публікацією.

---

## `сoncept/` — Документи проєктування

Внутрішні документи курсу для викладача та Claude Code.

```
сoncept/
├── oop_project_concept_for_claude_code.md  ← головний концепт-документ
├── COURSE_DESIGN.md                        ← таблиця всіх лаб з деталями
├── CONCEPTS_BY_LAB.md                      ← що вводиться в кожній лабі
├── CODEBASE_STATE.md                       ← стан src/ після кожної лаби
├── MENU_BY_LAB.md                          ← структура меню по лабах
└── LOC_ANALYSIS.md                         ← аналіз кількості рядків коду
```

---

## CI/CD

```
.github/workflows/
└── deploy-site.yml             ← build Astro + Blazor → deploy → tomka.space
```

**Pipeline:**
1. `actions/configure-pages` → визначає `base_path` (`/` з custom domain)
2. `npm run build` — Astro сайт з `BASE_PATH` env var
3. `dotnet publish` — Blazor WASM runner з правильним `base href`
4. `actions/deploy-pages` → GitHub Pages → [tomka.space](https://tomka.space)

---

## Правила роботи з матеріалами

### Лекції
- Кожна секція містить **академічний текст** + **runnable приклади** + **PNG діаграми**
- Діаграми генеруються через PIL (Python) і зберігаються в `lectures/_assets/XX-XX/`
- Блоки ` ```csharp run ` мають компілюватись без помилок (перевіряється `tools/code-checker`)
- Порядок роботи над секцією: **діаграма → аналіз → план → підтвердження → текст**

### Лабораторні
- Кожна лаба вводить **тільки ті конструкції**, які зазначені в `сoncept/CONCEPTS_BY_LAB.md`
- Код в `src/` не може використовувати конструкції з майбутніх лаб
- `List<T>` — не раніше Lab 04, LINQ — не раніше Lab 14

### Коміти
- Коміти в `main` тригерять автоматичний deploy на [tomka.space](https://tomka.space)
- Нові лекційні секції розробляються в окремих гілках
