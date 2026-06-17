'use strict';
// ═══════════════════════════════════════════════════════════════════════════════
// styles.js — визначення Word-стилів абзаців
// ═══════════════════════════════════════════════════════════════════════════════

const { AlignmentType } = require('docx');
const { C, SZ, IND, LS, SP } = require('./constants');

// Шрифт за замовчуванням для документа
const defaultStyle = {
  document: {
    run: { font: 'Times New Roman', size: SZ.BODY, color: C.BODY },
    paragraph: { spacing: { line: LS.BODY, before: 0, after: 0 } },
  },
};

// ── Визначення стилів ─────────────────────────────────────────────────────────
// Примітка: shading і border задаються прямо в renderer, а не тут —
// docx-js не завжди правильно передає їх через paragraphStyles у всіх версіях.

const paragraphStyles = [

  // ── Пригнічення вбудованих Word-стилів (не показувати в галереї) ─────────
  {
    id: 'Normal',
    name: 'Normal',
    quickFormat: false,
    run: { font: 'Times New Roman', size: SZ.BODY, color: C.BODY },
    paragraph: { spacing: { line: LS.BODY, before: 0, after: 0 } },
  },
  {
    id: 'ListParagraph',
    name: 'List Paragraph',
    basedOn: 'Normal',
    quickFormat: false,
    paragraph: { spacing: { before: 0, after: SP.LIST_AFT, line: LS.BODY } },
  },

  // ── ChapterTitle: "Розділ 1. Вступ" ──────────────────────────────────────
  {
    id: 'ChapterTitle',
    name: 'Chapter Title',
    basedOn: 'Normal',
    next: 'ChapterIntro',
    quickFormat: true,
    run: {
      font: 'Times New Roman',
      size: SZ.CHAPTER,
      bold: true,
      color: C.NAVY,
    },
    paragraph: {
      spacing: { before: 0, after: SP.CHAPTER_AFTER },
      keepNext: true,
      outlineLevel: 0,
    },
  },

  // ── ChapterIntro: вступний абзац розділу (без відступу, більший після) ───
  {
    id: 'ChapterIntro',
    name: 'Chapter Intro',
    basedOn: 'Normal',
    next: 'BodyText',
    quickFormat: false,
    run: {
      font: 'Times New Roman',
      size: SZ.BODY,
      color: C.BODY,
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      spacing: { before: SP.SECTION_AFT, after: SP.SUBHEAD_BEF, line: LS.BODY },
    },
  },

  // ── SectionTitle: "1.1. Роль платформи" ──────────────────────────────────
  {
    id: 'SectionTitle',
    name: 'Section Title',
    basedOn: 'Normal',
    next: 'BodyTextFirst',
    quickFormat: true,
    run: {
      font: 'Times New Roman',
      size: SZ.SECTION,
      bold: true,
      color: C.DARK_BLUE,
    },
    paragraph: {
      spacing: { before: SP.SECTION_BEF, after: SP.SECTION_AFT },
      keepNext: true,
      outlineLevel: 1,
    },
  },

  // ── SubHeading: тематичний підзаголовок ## ────────────────────────────────
  {
    id: 'SubHeading',
    name: 'Sub Heading',
    basedOn: 'Normal',
    next: 'BodyTextFirst',
    quickFormat: true,
    run: {
      font: 'Times New Roman',
      size: SZ.SUBHEAD,
      bold: true,
      italics: true,
      color: C.MID_BLUE,
    },
    paragraph: {
      spacing: { before: SP.SUBHEAD_BEF, after: SP.SUBHEAD_AFT },
      keepNext: true,
    },
  },

  // ── SummaryTitle: "## Підсумок" ───────────────────────────────────────────
  {
    id: 'SummaryTitle',
    name: 'Summary Title',
    basedOn: 'Normal',
    next: 'SummaryText',
    quickFormat: true,
    run: {
      font: 'Times New Roman',
      size: SZ.SUBHEAD,
      bold: true,
      color: C.ACCENT,
    },
    paragraph: {
      spacing: { before: SP.SUBHEAD_BEF, after: SP.MINOR_AFT },
      keepNext: true,
    },
  },

  // ── MinorHeading: ### підзаголовок третього рівня ─────────────────────────
  {
    id: 'MinorHeading',
    name: 'Minor Heading',
    basedOn: 'Normal',
    next: 'BodyTextFirst',
    quickFormat: true,
    run: {
      font: 'Times New Roman',
      size: SZ.MINOR,
      bold: true,
      color: C.MID_BLUE,
    },
    paragraph: {
      spacing: { before: SP.MINOR_BEF, after: SP.MINOR_AFT },
      keepNext: true,
    },
  },

  // ── BodyText: основний текст з відступом першого рядка ───────────────────
  {
    id: 'BodyText',
    name: 'Body Text',
    basedOn: 'Normal',
    next: 'BodyText',
    quickFormat: true,
    run: {
      font: 'Times New Roman',
      size: SZ.BODY,
      color: C.BODY,
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      indent: { firstLine: IND.FIRST_LINE },
      spacing: { line: LS.BODY, before: 0, after: 0 },
    },
  },

  // ── BodyTextFirst: перший абзац після заголовка — без відступу ───────────
  {
    id: 'BodyTextFirst',
    name: 'Body Text First',
    basedOn: 'BodyText',
    next: 'BodyText',
    quickFormat: false,
    run: {
      font: 'Times New Roman',
      size: SZ.BODY,
      color: C.BODY,
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      indent: { firstLine: 0 },
      spacing: { line: LS.BODY, before: 0, after: 0 },
    },
  },

  // ── CodeLabel: мітка мови над блоком коду ─────────────────────────────────
  {
    id: 'CodeLabel',
    name: 'Code Label',
    basedOn: 'Normal',
    next: 'CodeBlock',
    quickFormat: true,
    run: {
      font: 'Consolas',
      size: SZ.CODE_LABEL,
      bold: true,
      color: C.GRAY,
    },
    paragraph: {
      indent: { left: IND.CODE_LEFT, right: IND.CODE_RIGHT },
      spacing: { before: SP.CODE_BEF, after: 0 },
    },
  },

  // ── CodeBlock: рядок блоку коду ───────────────────────────────────────────
  {
    id: 'CodeBlock',
    name: 'Code Block',
    basedOn: 'Normal',
    next: 'CodeBlock',
    quickFormat: true,
    run: {
      font: 'Consolas',
      size: SZ.CODE,
      color: C.CODE_TEXT,
    },
    paragraph: {
      indent: { left: IND.CODE_LEFT, right: IND.CODE_RIGHT },
      spacing: { before: 0, after: 0, line: LS.CODE },
    },
  },

  // ── FigureCaption: підпис під рисунком ────────────────────────────────────
  {
    id: 'FigureCaption',
    name: 'Figure Caption',
    basedOn: 'Normal',
    next: 'BodyText',
    quickFormat: true,
    run: {
      font: 'Times New Roman',
      size: SZ.CAPTION,
      italics: true,
      color: C.CAPTION,
    },
    paragraph: {
      alignment: AlignmentType.CENTER,
      spacing: { before: SP.CAPTION_BEF, after: SP.CAPTION_AFT },
    },
  },

  // ── TableTitle: підпис над таблицею ──────────────────────────────────────
  {
    id: 'TableTitle',
    name: 'Table Title',
    basedOn: 'Normal',
    next: 'Normal',
    quickFormat: true,
    run: {
      font: 'Times New Roman',
      size: SZ.TABLE_H,
      bold: true,
      italics: true,
      color: C.BODY,
    },
    paragraph: {
      spacing: { before: SP.SECTION_AFT, after: SP.CAPTION_BEF },
      keepNext: true,
    },
  },

  // ── SummaryText: тіло секції "Підсумок" ──────────────────────────────────
  {
    id: 'SummaryText',
    name: 'Summary Text',
    basedOn: 'Normal',
    next: 'SummaryText',
    quickFormat: true,
    run: {
      font: 'Times New Roman',
      size: SZ.BODY,
      color: C.BODY,
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      indent: { left: IND.SUMM_LEFT, firstLine: 0 },
      spacing: { line: LS.BODY, before: 0, after: SP.LIST_AFT },
    },
  },

  // ── NoteText: блок "Примітка" (> blockquote) ─────────────────────────────
  {
    id: 'NoteText',
    name: 'Note Text',
    basedOn: 'Normal',
    next: 'NoteText',
    quickFormat: true,
    run: {
      font: 'Times New Roman',
      size: SZ.BODY,
      color: C.BODY,
    },
    paragraph: {
      alignment: AlignmentType.JUSTIFIED,
      indent: { left: IND.NOTE_LEFT, firstLine: 0 },
      spacing: { line: LS.BODY, before: 0, after: SP.LIST_AFT },
    },
  },

  // ── ListBullet / ListNumber ───────────────────────────────────────────────
  {
    id: 'ListBullet',
    name: 'List Bullet',
    basedOn: 'Normal',
    next: 'ListBullet',
    quickFormat: true,
    run: { font: 'Times New Roman', size: SZ.BODY, color: C.BODY },
    paragraph: { spacing: { before: 0, after: SP.LIST_AFT, line: LS.BODY } },
  },
  {
    id: 'ListNumber',
    name: 'List Number',
    basedOn: 'Normal',
    next: 'ListNumber',
    quickFormat: true,
    run: { font: 'Times New Roman', size: SZ.BODY, color: C.BODY },
    paragraph: { spacing: { before: 0, after: SP.LIST_AFT, line: LS.BODY } },
  },

];

module.exports = { paragraphStyles, defaultStyle };
