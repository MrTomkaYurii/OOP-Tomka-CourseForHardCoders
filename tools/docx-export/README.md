# md-to-docx — конвертер Markdown → Word

Дві точки входу зі спільним рушієм (`lib/`):

| Скрипт | Що робить | Формат |
|---|---|---|
| `md-to-docx.js` | лекції: багато секцій → один документ розділу | A5, книжкова верстка |
| `labs-to-docx.js` | лабораторні: кожна `labs/lab-NN-*/instructions.md` → окремий `.docx` | A4, технічна методичка |

Усі результати — у `tools/docx-export/output/` (тека в `.gitignore`, у git не потрапляє).
Команди запускаються з теки `tools/docx-export/`.

## Лабораторні

```bash
node labs-to-docx.js                 # усі 22 → output/labs/lab-NN-*.docx
node labs-to-docx.js --only 1        # лише Lab 01
node labs-to-docx.js --only 1,2,3    # порційно
node labs-to-docx.js --only 4-6      # діапазон
npm run labs                         # = усі 22

# Візуальна перевірка (потрібен MS Word): docx → pdf
npm run labs:pdf                     # to-pdf-all.ps1 → output/labs/*.pdf
```

**lab-режим рушія** (`parseMd(md,{lab:true})`, `render(blocks,null,{lab:true})`) додає:
- `---` (горизонтальні лінії) пропускаються;
- усі `## …` → секції (не лише нумеровані `1.1`);
- `# …` → назва лабораторної (ChapterTitle без розриву сторінки);
- списки збирають вкладений контент (код, під-списки, таблиці) у `item.children`;
- loose-списки (порожній рядок між пунктами) не розриваються, нумерація 1,2,3…;
- кожен нумерований список отримує свій слот нумерації (перезапуск з 1);
- GitHub task-list `- [ ]` / `- [x]` → `☐` / `☑`;
- backslash-екранування `\<` `\|` тощо знімається;
- вкладений inline (`**\`code\`**`) рендериться коректно;
- таблиці з ≥ 6 колонок — дрібніший шрифт і вужчі поля;
- рядки таблиць `cantSplit` (не рвуться між сторінками);
- колонтитул зверху — назва лабораторної, знизу — номер сторінки.

## Лекції (книга)

```bash
npm run book                         # уся книга: 21 розділ + питання → output/full-course.docx
node md-to-docx.js --all -o output/full-course-v5.docx   # те саме, з власним ім'ям файлу

# Один розділ (секції по glob + питання)
node md-to-docx.js "../../lectures/sections/01-*.md" "../../lectures/questions/01-questions.md" -o output/chapter-01.docx

# Явний перелік файлів / власна назва розділу
node md-to-docx.js file1.md file2.md -o output/test.docx --title "Розділ 2. Основи мови"
```

Книжкова верстка лекцій (A5): поля верх/низ 15 мм, ліве 25 мм, праве 10 мм; рисунки —
ч/б версії з `book/` на всю ширину тексту; inline-код — шрифтом тексту без заливки;
блоки коду з номерами рядків; таблиці в сірих тонах. Деталі — `style-guide.md`.

## Структура проєкту

```
tools/docx-export/
├── md-to-docx.js        CLI-точка входу
├── lib/
│   ├── constants.js     Розміри, кольори, шрифти (єдине джерело правди)
│   ├── styles.js        Word-стилі для Document()
│   ├── numbering.js     Конфіг списків
│   ├── parser.js        Markdown → блоки AST
│   ├── renderer.js      Блоки AST → docx-елементи
│   └── images.js        PNG: читання, масштаб, ImageRun
├── style-guide.md       Повна специфікація стилів ← читати перед редагуванням
└── README.md
```

## Підтримувані елементи

| Markdown | Word-стиль |
|---|---|
| Frontmatter `chapterTitle` | ChapterTitle + синя риска |
| `## 1.1. Назва` | SectionTitle |
| `## Підзаголовок` | SubHeading |
| `## Підсумок` | SummaryTitle + SummaryText |
| `### Назва` | MinorHeading |
| Абзац тексту | BodyText / BodyTextFirst |
| ` ```csharp ` | CodeLabel (C#) + CodeBlock |
| ` ```bash ` | CodeLabel (Bash) + CodeBlock |
| `- пункт` | ListBullet (em dash) |
| `1. пункт` | ListNumber |
| `\| таблиця \|` | Таблиця з navy-шапкою |
| `![alt](src)` | Зображення + FigureCaption |

## Залежності

```bash
npm install docx
```

Node.js ≥ 18
