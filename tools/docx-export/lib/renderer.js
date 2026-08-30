'use strict';
// ═══════════════════════════════════════════════════════════════════════════════
// renderer.js — Block AST → docx-елементи
// ═══════════════════════════════════════════════════════════════════════════════

const {
  Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType,
} = require('docx');

const { C, SZ, IND, LS, SP, BD, PAGE, CODE_LABELS } = require('./constants');
const { parseInline }     = require('./parser');
const { buildImageElems } = require('./images');

// ── Допоміжники ───────────────────────────────────────────────────────────────
const bdr = (size, color) => ({ style: BorderStyle.SINGLE, size, color });
const nil = ()             => ({ style: BorderStyle.NIL });

// ── Inline-токени → TextRun[] ─────────────────────────────────────────────────
function tokensToRuns(tokens, base) {
  const defaults = { font: 'Times New Roman', size: SZ.BODY, color: C.BODY };
  const out = [];
  for (const tok of tokens) {
    const merged = { ...defaults, ...base };
    switch (tok.type) {
      case 'text':
        out.push(new TextRun({ text: tok.text, ...merged })); break;
      case 'bold':
        out.push(...(tok.children ? tokensToRuns(tok.children, { ...base, bold: true })
                                  : [new TextRun({ text: tok.text, ...merged, bold: true })])); break;
      case 'italic':
        out.push(...(tok.children ? tokensToRuns(tok.children, { ...base, italics: true })
                                  : [new TextRun({ text: tok.text, ...merged, italics: true })])); break;
      case 'bolditalic':
        out.push(...(tok.children ? tokensToRuns(tok.children, { ...base, bold: true, italics: true })
                                  : [new TextRun({ text: tok.text, ...merged, bold: true, italics: true })])); break;
      case 'code':
        out.push(new TextRun({
          text:    tok.text,
          font:    'Consolas',
          size:    SZ.TABLE,   // 9pt — inline-код трохи менший за тіло
          color:   C.CODE_TEXT,
          bold:    base.bold || undefined,
          shading: { type: ShadingType.CLEAR, color: 'auto', fill: C.INLINE_BG },
        })); break;
      case 'link':
        out.push(new TextRun({ text: tok.text, ...merged, color: C.ACCENT })); break;
      default:
        out.push(new TextRun({ text: tok.text || '', ...merged }));
    }
  }
  return out.filter(Boolean);
}

function toRuns(text, base = {}) {
  return tokensToRuns(parseInline(text), base);
}

// ── Побудова одного абзацу тіла ───────────────────────────────────────────────
function bodyPara(text, opts = {}) {
  return new Paragraph({
    style:    opts.first ? 'BodyTextFirst' : 'BodyText',
    children: toRuns(text),
    ...opts.extra,
  });
}

// ── Рендер вкладених блоків елемента списку (lab-режим) ───────────────────────
function renderChildren(children, assetsBase, opts) {
  if (!children || !children.length) return [];
  return render(children, assetsBase, opts);
}

// ── Основна функція ───────────────────────────────────────────────────────────
function render(blocks, assetsBase, opts = {}) {
  const lab = !!opts.lab;
  let inSummary   = false;
  let inQuestions = false;  // true між h1 і наступним chapter
  let numbersIdx  = 0;      // індекс поточного слота нумерованого списку
  let numSeq      = 0;      // lab: свіжий слот нумерації на кожен список
  const elems = [];

  for (const block of blocks) {

    // Скидаємо summary при будь-якому заголовку нового підрозділу
    if (block.type === 'section' || block.type === 'h2' || block.type === 'h3') {
      if (block.type !== 'summary_h') inSummary = false;
    }

    switch (block.type) {

      // ── h1: у lab-режимі — назва лабораторної (як ChapterTitle без розриву) ─
      //        у лекціях — заголовок блоку питань ("# Питання для самоконтролю")
      case 'h1': {
        if (lab) {
          elems.push(new Paragraph({
            style:    'ChapterTitle',
            children: toRuns(block.text, { bold: true, size: SZ.CHAPTER, color: C.NAVY }),
            border:   { bottom: bdr(BD.CHAPTER_W, C.ACCENT) },
          }));
          break;
        }
        numbersIdx++;
        inQuestions = true;
        elems.push(new Paragraph({
          style:    'SectionTitle',
          children: toRuns(block.text, { bold: true, size: SZ.SECTION, color: C.DARK_BLUE }),
          border:   { bottom: { style: BorderStyle.DOTTED, size: BD.SECTION_W, color: 'D0D8E8' } },
        }));
        break;
      }

      // ── chapter: синтетичний блок, який генерує md-to-docx.js ──────────────
      case 'chapter': {
        numbersIdx++;
        inQuestions = false;
        elems.push(new Paragraph({
          style:          'ChapterTitle',
          children:       toRuns(block.title, { bold: true, size: SZ.CHAPTER, color: C.NAVY }),
          border:         { bottom: bdr(BD.CHAPTER_W, C.ACCENT) },
          pageBreakBefore: true,
        }));
        if (block.intro) {
          elems.push(new Paragraph({
            style:    'ChapterIntro',
            children: toRuns(block.intro),
          }));
        }
        break;
      }

      // ── section: "1.1. Роль платформи" ────────────────────────────────────
      case 'section': {
        inSummary = false;
        if (inQuestions) {
          // Всередині блоку питань — просто жирний абзац, без стильного заголовка
          elems.push(new Paragraph({
            style:    'BodyTextFirst',
            children: toRuns(block.text, { bold: true, size: SZ.BODY, color: C.BODY }),
            spacing:  { before: SP.SUBHEAD_BEF, after: SP.SUBHEAD_AFT },
          }));
        } else {
          elems.push(new Paragraph({
            style:    'SectionTitle',
            children: toRuns(block.text, { bold: true, size: SZ.SECTION, color: C.DARK_BLUE }),
            border:   { bottom: { style: BorderStyle.DOTTED, size: BD.SECTION_W, color: 'D0D8E8' } },
          }));
        }
        break;
      }

      // ── h2: тематичний підзаголовок ────────────────────────────────────────
      case 'h2': {
        elems.push(new Paragraph({
          style:    'SubHeading',
          children: toRuns(block.text, { bold: true, italics: true, size: SZ.SUBHEAD, color: C.MID_BLUE }),
        }));
        break;
      }

      // ── summary_h: "## Підсумок" ───────────────────────────────────────────
      case 'summary_h': {
        inSummary = true;
        elems.push(new Paragraph({
          style:    'SummaryTitle',
          children: toRuns(block.text, { bold: true, size: SZ.SUBHEAD, color: C.ACCENT }),
        }));
        break;
      }

      // ── h3: ### підзаголовок ───────────────────────────────────────────────
      case 'h3': {
        elems.push(new Paragraph({
          style:    'MinorHeading',
          children: toRuns(block.text, { bold: true, size: SZ.MINOR, color: C.MID_BLUE }),
        }));
        break;
      }

      // ── para: абзац тексту ─────────────────────────────────────────────────
      case 'para': {
        if (inSummary) {
          elems.push(new Paragraph({
            style:    'SummaryText',
            children: toRuns(block.text),
            shading:  { type: ShadingType.CLEAR, color: 'auto', fill: C.SUMM_BG },
            border:   { left: bdr(BD.ACCENT_W, C.ACCENT) },
          }));
        } else if (lab) {
          // Лабораторні — технічний документ: без абзацного відступу, з відбивкою
          elems.push(new Paragraph({
            style:    'BodyTextFirst',
            children: toRuns(block.text),
            spacing:  { line: LS.BODY, before: 0, after: SP.SUBHEAD_AFT },
          }));
        } else {
          elems.push(bodyPara(block.text, { first: block.firstAfterHead }));
        }
        break;
      }

      // ── code: блок коду ────────────────────────────────────────────────────
      case 'code': {
        const label = CODE_LABELS[block.lang] ?? block.lang.toUpperCase();

        // Мітка мови (тільки якщо є)
        if (label) {
          elems.push(new Paragraph({
            style:    'CodeLabel',
            children: [new TextRun({
              text:  label,
              font:  'Consolas',
              size:  SZ.CODE_LABEL,
              bold:  true,
              color: C.GRAY,
            })],
            shading: { type: ShadingType.CLEAR, color: 'auto', fill: C.CODE_LBL },
            border: {
              top:    bdr(BD.CODE_SIDE, C.CODE_BORD),
              left:   bdr(BD.CODE_SIDE, C.CODE_BORD),
              right:  bdr(BD.CODE_SIDE, C.CODE_BORD),
              bottom: nil(),
            },
          }));
        }

        // Рядки коду
        const codeLines = block.lines.length ? block.lines : [''];
        const last = codeLines.length - 1;

        codeLines.forEach((codeLine, idx) => {
          elems.push(new Paragraph({
            style:    'CodeBlock',
            children: [new TextRun({
              text:  codeLine === '' ? ' ' : codeLine,
              font:  'Consolas',
              size:  SZ.CODE,
              color: C.CODE_TEXT,
            })],
            shading: { type: ShadingType.CLEAR, color: 'auto', fill: C.CODE_BG },
            spacing: {
              before: 0,
              after:  idx === last ? SP.CODE_AFT : 0,
              line:   LS.CODE,
            },
            border: {
              top:    nil(),
              left:   bdr(BD.ACCENT_W, C.ACCENT),     // 3pt синя смуга
              right:  bdr(BD.CODE_SIDE, C.CODE_BORD),
              bottom: idx === last ? bdr(BD.CODE_SIDE, C.CODE_BORD) : nil(),
            },
          }));
        });
        break;
      }

      // ── table ──────────────────────────────────────────────────────────────
      case 'table': {
        if (!block.rows.length) break;

        const [headerRow, ...dataRows] = block.rows;
        const nc   = Math.max(...block.rows.map(r => r.length), 1);
        const base = Math.floor(PAGE.CW / nc);
        const colW = Array(nc).fill(base);
        colW[nc - 1] += PAGE.CW - base * nc;  // remainder → остання колонка

        const cellBorder = bdr(BD.TABLE_INN, C.TBL_BORDER);
        const allBorders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };

        // Широкі таблиці — дрібніший шрифт і вужчі поля клітинок
        const wide   = nc >= 6;
        const szBody = wide ? SZ.CODE  : SZ.TABLE;
        const szHead = wide ? SZ.TABLE : SZ.TABLE_H;
        const cellMx = wide ? 60       : 110;

        const mkCell = (text, ci, fill, isHead = false) =>
          new TableCell({
            width:   { size: colW[ci] ?? base, type: WidthType.DXA },
            shading: { type: ShadingType.CLEAR, color: 'auto', fill },
            borders: allBorders,
            margins: { top: 80, bottom: 80, left: cellMx, right: cellMx },
            children: [new Paragraph({
              alignment: AlignmentType.LEFT,
              spacing:   { before: 0, after: 0 },
              children:  toRuns(text || '', isHead
                ? { bold: true, color: C.WHITE, size: szHead }
                : { size: szBody }),
            })],
          });

        const padRow = row => {
          const r = [...row];
          while (r.length < nc) r.push('');
          return r;
        };

        const rows = [
          new TableRow({
            tableHeader: true,
            cantSplit:   true,
            children: padRow(headerRow).map((c, ci) => mkCell(c, ci, C.TBL_HEADER, true)),
          }),
          ...dataRows.map((row, ri) => new TableRow({
            cantSplit: true,
            children: padRow(row).map((c, ci) =>
              mkCell(c, ci, ri % 2 === 0 ? C.TBL_ODD : C.TBL_EVEN)),
          })),
        ];

        elems.push(new Table({
          width:        { size: PAGE.CW, type: WidthType.DXA },
          columnWidths: colW,
          rows,
        }));
        // Порожній абзац після таблиці для відступу
        elems.push(new Paragraph({ children: [], spacing: { after: SP.SUBHEAD_AFT } }));
        break;
      }

      // ── bullets ────────────────────────────────────────────────────────────
      case 'bullets': {
        for (const item of block.items) {
          let text       = typeof item === 'string' ? item : item.text;
          const children = typeof item === 'string' ? null : item.children;
          // GitHub task-list: "- [ ] …" / "- [x] …"
          text = text.replace(/^\[[xX]\]\s+/, '☑ ').replace(/^\[\s?\]\s+/, '☐ ');
          const para = new Paragraph({
            style:     inSummary ? 'SummaryText' : 'ListBullet',
            numbering: { reference: 'bullets', level: 0 },
            children:  toRuns(text),
          });
          if (inSummary) {
            Object.assign(para, {
              shading: { type: ShadingType.CLEAR, color: 'auto', fill: C.SUMM_BG },
              border:  { left: bdr(BD.ACCENT_W, C.ACCENT) },
            });
          }
          elems.push(para);
          elems.push(...renderChildren(children, assetsBase, opts));
        }
        break;
      }

      // ── numbered ───────────────────────────────────────────────────────────
      case 'numbered': {
        const ref = lab ? `numbers-${++numSeq}` : `numbers-${numbersIdx}`;
        for (const item of block.items) {
          const text     = typeof item === 'string' ? item : item.text;
          const children = typeof item === 'string' ? null : item.children;
          elems.push(new Paragraph({
            style:     'ListNumber',
            numbering: { reference: ref, level: 0 },
            children:  toRuns(text),
          }));
          elems.push(...renderChildren(children, assetsBase, opts));
        }
        break;
      }

      // ── image ──────────────────────────────────────────────────────────────
      case 'image': {
        elems.push(...buildImageElems(block, assetsBase));
        break;
      }

      // ── blockquote: "Примітка" ─────────────────────────────────────────────
      case 'blockquote': {
        elems.push(new Paragraph({
          style:    'NoteText',
          children: toRuns(block.text),
          shading:  { type: ShadingType.CLEAR, color: 'auto', fill: C.NOTE_BG },
          border:   { left: bdr(BD.ACCENT_W, C.NOTE_BORD) },
        }));
        break;
      }

      default:
        break;
    }
  }

  return elems;
}

module.exports = { render };
