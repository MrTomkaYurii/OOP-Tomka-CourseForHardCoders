# md-to-docx — конвертер лекцій у Word

Перетворює Markdown-файли лекцій курсу на A5-документ Word із повною системою стилів навчального видання.

## Використання

```bash
# Один розділ (всі секції по glob)
node md-to-docx.js "lectures/sections/01-*.md" -o "output/chapter-01.docx"

# Явний перелік файлів
node md-to-docx.js file1.md file2.md -o out.docx

# З кастомною назвою розділу
node md-to-docx.js "lectures/sections/02-*.md" -o out.docx --title "Розділ 2. Основи мови"
```

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
