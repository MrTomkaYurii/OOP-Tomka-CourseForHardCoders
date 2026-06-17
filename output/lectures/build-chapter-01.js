'use strict';

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, LevelFormat,
  PageNumber, Footer, ImageRun,
} = require('docx');
const fs = require('fs');
const path = require('path');

// ── PNG dimension reader (from IHDR, no extra deps) ──────────────────────────
function pngDims(filePath) {
  try {
    const buf = fs.readFileSync(filePath);
    if (buf[0] !== 0x89 || buf[1] !== 0x50) return null; // not PNG
    return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
  } catch { return null; }
}

// ── Page geometry (DXA = 1/1440 inch = 1/20 pt) ──────────────────────────────
const A5_W = 8391;   // 148 mm
const A5_H = 11906;  // 210 mm
const M_T  = 1134;   // 20 mm top
const M_B  = 1134;   // 20 mm bottom
const M_L  = 1418;   // 25 mm left (binding)
const M_R  = 851;    // 15 mm right
const CW   = A5_W - M_L - M_R; // 6122 DXA — content width

// ── Colors ────────────────────────────────────────────────────────────────────
const C = {
  NAVY:      '1A1A2E', DARK:     '16213E', BLUE:     '0F3460',
  ACCENT:    '0078D4', BODY:     '1A1A1A', CODE:     '1E1E1E',
  CODE_BG:   'F8F8F8', CODE_LBL: 'EEEEEE', CODE_BD:  'D0D0D0',
  SUMM_BG:   'EBF3FB', TBL_H:   '1A1A2E', TBL_ODD:  'F0F4FF',
  GRAY:      '666666', IMG:      '999999', WHITE:    'FFFFFF',
  INLBG:     'F0F0F0',
};

// ── Font sizes (half-points = pt × 2) ─────────────────────────────────────────
const SZ = {
  BODY: 21, CODE: 17, LCODE: 15, INLINE: 18, TBL: 18, TBL_H: 19,
  H2: 26, H3: 22, H4: 21, TITLE: 36, FOOT: 18,
};

// ── Indents (DXA) ──────────────────────────────────────────────────────────────
const IND = {
  FIRST: 425,   // 0.75 cm first-line
  CODE:  283,   // 0.5 cm code left/right
  SUMM:  200,   // summary left
  BUL_L: 567,   // bullet left
  BUL_H: 284,   // bullet hanging
};

// ── Helpers ────────────────────────────────────────────────────────────────────
const bdr  = (size, color) => ({ style: BorderStyle.SINGLE, size, color });
const noBdr = () => ({ style: BorderStyle.NIL });

// ── Inline Markdown parser → TextRun[] ────────────────────────────────────────
function parseInline(text, base = {}) {
  const runs = [];
  let i = 0, buf = '';

  const emit = (t, extra = {}) => {
    if (!t) return;
    runs.push(new TextRun({
      text: t, font: 'Times New Roman', size: SZ.BODY, color: C.BODY,
      ...base, ...extra,
    }));
  };
  const flush = (extra = {}) => { emit(buf, extra); buf = ''; };

  while (i < text.length) {
    // Bold-italic ***
    if (text[i]==='*' && text[i+1]==='*' && text[i+2]==='*') {
      const e = text.indexOf('***', i+3);
      if (e !== -1) { flush(); emit(text.slice(i+3,e), {bold:true,italics:true}); i=e+3; continue; }
    }
    // Bold **
    if (text[i]==='*' && text[i+1]==='*' && text[i+2]!=='*') {
      const e = text.indexOf('**', i+2);
      if (e !== -1) { flush(); emit(text.slice(i+2,e), {bold:true}); i=e+2; continue; }
    }
    // Italic *
    if (text[i]==='*' && text[i+1]!=='*') {
      const e = text.indexOf('*', i+1);
      if (e !== -1) { flush(); emit(text.slice(i+1,e), {italics:true}); i=e+1; continue; }
    }
    // Inline code `
    if (text[i]==='`') {
      const e = text.indexOf('`', i+1);
      if (e !== -1) {
        flush();
        runs.push(new TextRun({
          text: text.slice(i+1,e),
          font: 'Consolas', size: SZ.INLINE, color: C.CODE,
          shading: { type: ShadingType.CLEAR, color: 'auto', fill: C.INLBG },
          ...((base.bold) ? {bold: true} : {}),
        }));
        i=e+1; continue;
      }
    }
    buf += text[i++];
  }
  flush();
  return runs.filter(r => r);
}

// ── Markdown block parser ──────────────────────────────────────────────────────
function parseMd(content) {
  const lines = content.split('\n');
  const blocks = [];
  let i = 0;

  // Skip YAML frontmatter
  if (lines[i] && lines[i].trim() === '---') {
    i++;
    while (i < lines.length && lines[i].trim() !== '---') i++;
    i++;
  }

  while (i < lines.length) {
    const ln = lines[i];
    if (!ln || !ln.trim()) { i++; continue; }

    // ── Code fence
    if (ln.startsWith('```')) {
      const lang = ln.slice(3).trim().replace(/ run$/, '').toLowerCase();
      i++;
      const code = [];
      while (i < lines.length && !lines[i].startsWith('```')) {
        code.push(lines[i]);
        i++;
      }
      i++;
      blocks.push({ type: 'code', lang, code });
      continue;
    }

    // ── Table
    if (ln.startsWith('|')) {
      const rows = [];
      while (i < lines.length && lines[i].startsWith('|')) {
        const row = lines[i]; i++;
        if (/^\|[-:\s|]+\|$/.test(row)) continue; // separator
        const cells = row.split('|').slice(1,-1).map(c => c.trim());
        rows.push(cells);
      }
      if (rows.length) blocks.push({ type: 'table', rows });
      continue;
    }

    // ── Headings
    const h2 = ln.match(/^## (.+)/);
    if (h2) {
      const txt = h2[1].trim();
      blocks.push({
        type: /^\d+\.\d+/.test(txt) ? 'section' : 'h2',
        text: txt,
      });
      i++; continue;
    }
    const h3 = ln.match(/^### (.+)/);
    if (h3) { blocks.push({ type: 'h3', text: h3[1].trim() }); i++; continue; }
    const h4 = ln.match(/^#### (.+)/);
    if (h4) { blocks.push({ type: 'h4', text: h4[1].trim() }); i++; continue; }

    // ── Image
    if (/^!\[/.test(ln)) {
      const m = ln.match(/^!\[([^\]]*)\]\(([^)]*)\)/);
      blocks.push({ type: 'image', alt: m ? m[1] : '', src: m ? m[2] : '' });
      i++; continue;
    }

    // ── Bullet list
    if (/^- /.test(ln)) {
      const items = [];
      while (i < lines.length && /^- /.test(lines[i])) {
        items.push(lines[i].slice(2).trim()); i++;
      }
      blocks.push({ type: 'bullets', items });
      continue;
    }

    // ── Numbered list
    if (/^\d+\. /.test(ln)) {
      const items = [];
      while (i < lines.length && /^\d+\. /.test(lines[i])) {
        items.push(lines[i].replace(/^\d+\. /, '').trim()); i++;
      }
      blocks.push({ type: 'numbered', items });
      continue;
    }

    // ── Paragraph — accumulate continuation lines
    let para = ln.trim();
    i++;
    while (i < lines.length) {
      const nx = lines[i];
      if (!nx || !nx.trim()) break;
      if (/^(#|```|\||!\[|-\s|\d+\. )/.test(nx)) break;
      para += ' ' + nx.trim();
      i++;
    }
    blocks.push({ type: 'para', text: para });
  }
  return blocks;
}

// ── Paths (needed in toElems for image resolution) ───────────────────────────
const ASSETS_BASE = path.join(
  'C:', 'Users', 'Yurii', 'source', 'repos',
  'OOP-Tomka-CourseForHardCoders', '.claude', 'worktrees',
  'frosty-rhodes-cc8a89', 'lectures', '_assets'
);
// A5 content width in pixels at 96 DPI: 6122 DXA / 1440 * 96 ≈ 408 px
const IMG_MAX_W = 408;

// ── Block → DocX element(s) ───────────────────────────────────────────────────
let inSummary = false;

function toElems(block) {
  switch (block.type) {

    // ── Section heading (numbered: 1.1, 1.2 ...)
    case 'section':
      inSummary = false;
      return [new Paragraph({
        children: parseInline(block.text, { bold: true, size: SZ.H2, color: C.DARK }),
        spacing: { before: 320, after: 160 },
        keepNext: true,
        border: { bottom: bdr(6, 'D0DCEE') },
      })];

    // ── Generic ## heading
    case 'h2': {
      const isSumm = /^підсумок$/i.test(block.text.trim());
      inSummary = isSumm;
      return [new Paragraph({
        children: parseInline(block.text, {
          bold: true,
          italics: !isSumm,
          size: SZ.H3,
          color: isSumm ? C.ACCENT : C.BLUE,
        }),
        spacing: { before: 240, after: 100 },
        keepNext: !isSumm,
      })];
    }

    // ── ### heading
    case 'h3':
      return [new Paragraph({
        children: parseInline(block.text, { bold: true, size: SZ.H3, color: C.BLUE }),
        spacing: { before: 200, after: 80 },
        keepNext: true,
      })];

    // ── #### heading
    case 'h4':
      return [new Paragraph({
        children: parseInline(block.text, { bold: true, size: SZ.H4, color: C.BLUE }),
        spacing: { before: 160, after: 60 },
        keepNext: true,
      })];

    // ── Body paragraph
    case 'para': {
      if (inSummary) {
        return [new Paragraph({
          children: parseInline(block.text),
          indent: { left: IND.SUMM + 170 },
          spacing: { line: 276, after: 80 },
          alignment: AlignmentType.JUSTIFIED,
          shading: { type: ShadingType.CLEAR, color: 'auto', fill: C.SUMM_BG },
          border: { left: bdr(20, C.ACCENT) },
        })];
      }
      return [new Paragraph({
        children: parseInline(block.text),
        indent: { firstLine: IND.FIRST },
        spacing: { line: 276, after: 120 },
        alignment: AlignmentType.JUSTIFIED,
      })];
    }

    // ── Code block
    case 'code': {
      const langMap = {
        csharp: 'C#', bash: 'Bash', xml: 'XML', json: 'JSON',
        powershell: 'PowerShell', text: '', '': '',
      };
      const label = langMap[block.lang] !== undefined ? langMap[block.lang] : block.lang.toUpperCase();
      const elems = [];

      // Label bar (top of code block)
      if (label) {
        elems.push(new Paragraph({
          children: [new TextRun({ text: label, font: 'Consolas', size: SZ.LCODE, bold: true, color: C.GRAY })],
          indent: { left: IND.CODE, right: IND.CODE },
          spacing: { before: 160, after: 0 },
          shading: { type: ShadingType.CLEAR, color: 'auto', fill: C.CODE_LBL },
          border: {
            top:    bdr(8, C.CODE_BD),
            left:   bdr(8, C.CODE_BD),
            right:  bdr(8, C.CODE_BD),
            bottom: noBdr(),
          },
        }));
      }

      const n = block.code.length;
      // Ensure at least one line renders
      const codeLines = n === 0 ? [' '] : block.code;
      codeLines.forEach((codeLine, idx) => {
        const isLast = idx === codeLines.length - 1;
        elems.push(new Paragraph({
          children: [new TextRun({ text: codeLine === '' ? ' ' : codeLine, font: 'Consolas', size: SZ.CODE, color: C.CODE })],
          indent: { left: IND.CODE, right: IND.CODE },
          spacing: { before: 0, after: isLast ? 160 : 0, line: 240 },
          shading: { type: ShadingType.CLEAR, color: 'auto', fill: C.CODE_BG },
          border: {
            top:    noBdr(),
            left:   bdr(24, C.ACCENT),   // 3 pt blue left accent
            right:  bdr(8,  C.CODE_BD),
            bottom: isLast ? bdr(8, C.CODE_BD) : noBdr(),
          },
        }));
      });
      return elems;
    }

    // ── Table
    case 'table': {
      if (!block.rows.length) return [];
      const [header, ...body] = block.rows;
      const nc = Math.max(...block.rows.map(r => r.length), 1);
      const baseW = Math.floor(CW / nc);
      const colW = Array(nc).fill(baseW);
      colW[nc-1] += CW - baseW * nc; // absorb rounding

      const cellBd = bdr(4, 'C0C8D8');
      const bds = { top: cellBd, bottom: cellBd, left: cellBd, right: cellBd };

      const mkCell = (rawText, ci, fill, isHead = false) => {
        const w = colW[ci] !== undefined ? colW[ci] : baseW;
        return new TableCell({
          width: { size: w, type: WidthType.DXA },
          shading: { type: ShadingType.CLEAR, color: 'auto', fill },
          borders: bds,
          margins: { top: 60, bottom: 60, left: 110, right: 110 },
          children: [new Paragraph({
            alignment: AlignmentType.LEFT,
            children: parseInline(rawText || '', isHead
              ? { bold: true, color: C.WHITE, size: SZ.TBL_H }
              : { size: SZ.TBL }),
            spacing: { before: 0, after: 0 },
          })],
        });
      };

      const padRow = (row) => {
        const padded = [...row];
        while (padded.length < nc) padded.push('');
        return padded;
      };

      const tableRows = [
        new TableRow({
          tableHeader: true,
          children: padRow(header).map((c, ci) => mkCell(c, ci, C.TBL_H, true)),
        }),
        ...body.map((row, ri) => new TableRow({
          children: padRow(row).map((c, ci) =>
            mkCell(c, ci, ri % 2 === 0 ? C.TBL_ODD : C.WHITE)),
        })),
      ];

      return [
        new Table({
          width: { size: CW, type: WidthType.DXA },
          columnWidths: colW,
          rows: tableRows,
        }),
        new Paragraph({ children: [], spacing: { after: 120 } }),
      ];
    }

    // ── Bullet list
    case 'bullets':
      return block.items.map(item => new Paragraph({
        numbering: { reference: 'bullets', level: 0 },
        children: parseInline(item),
        spacing: { after: 60 },
      }));

    // ── Numbered list
    case 'numbered':
      return block.items.map(item => new Paragraph({
        numbering: { reference: 'numbers', level: 0 },
        children: parseInline(item),
        spacing: { after: 60 },
      }));

    // ── Image — insert actual PNG if file exists
    case 'image': {
      // src is like "_assets/01-01/dotnet-pipeline.png"
      // strip leading "_assets/" and resolve from ASSETS_BASE
      const relParts = block.src.replace(/^_assets\//, '').split('/');
      const imgPath = path.join(ASSETS_BASE, ...relParts);

      if (block.src && fs.existsSync(imgPath)) {
        const dims = pngDims(imgPath);
        const scale = dims && dims.w > IMG_MAX_W ? IMG_MAX_W / dims.w : 1;
        const dispW = dims ? Math.round(dims.w * scale) : IMG_MAX_W;
        const dispH = dims ? Math.round(dims.h * scale) : Math.round(IMG_MAX_W * 0.6);

        return [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new ImageRun({
              type: 'png',
              data: fs.readFileSync(imgPath),
              transformation: { width: dispW, height: dispH },
              altText: { title: block.alt, description: block.alt, name: block.alt || 'image' },
            })],
            spacing: { before: 140, after: 40 },
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: block.alt,
              font: 'Times New Roman', size: 17,
              italics: true, color: C.GRAY,
            })],
            spacing: { before: 0, after: 160 },
          }),
        ];
      }

      // Fallback: file missing → grey placeholder
      return [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({
          text: `[ Діаграма: ${block.alt} ]`,
          font: 'Times New Roman', size: SZ.BODY,
          italics: true, color: C.IMG,
        })],
        spacing: { before: 120, after: 160 },
        shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'F5F5F5' },
        border: {
          top: bdr(4,'E0E0E0'), bottom: bdr(4,'E0E0E0'),
          left: bdr(4,'E0E0E0'), right: bdr(4,'E0E0E0'),
        },
      })];
    }

    default:
      return [];
  }
}

// ── File paths ────────────────────────────────────────────────────────────────
const SECT_DIR = path.join(
  'C:', 'Users', 'Yurii', 'source', 'repos',
  'OOP-Tomka-CourseForHardCoders', '.claude', 'worktrees',
  'frosty-rhodes-cc8a89', 'lectures', 'sections'
);
const OUT_DIR = path.join(
  'C:', 'Users', 'Yurii', 'source', 'repos',
  'OOP-Tomka-CourseForHardCoders', 'output', 'lectures'
);
const FILES = [
  '01-01-rol-platformy.md',
  '01-02-dotnet-framework-ta-dotnet-6.md',
  '01-03-kerovanyi-ta-nekerovanyi-kod.md',
  '01-04-jit-kompiliatsiia.md',
];

// ── Numbering config ──────────────────────────────────────────────────────────
const numbering = {
  config: [
    {
      reference: 'bullets',
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: '—', // em dash
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: IND.BUL_L, hanging: IND.BUL_H } } },
      }],
    },
    {
      reference: 'numbers',
      levels: [{
        level: 0, format: LevelFormat.DECIMAL, text: '%1.',
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: IND.BUL_L, hanging: IND.BUL_H } } },
      }],
    },
  ],
};

// ── Build document content ────────────────────────────────────────────────────
const INTRO = 'На сьогоднішній момент мова програмування C# — одна з найпотужніших мов, що швидко розвиваються і є затребуваними в ІT-галузі. Зараз на ній пишуться різні програми: від невеликих десктопних програм до великих веб-порталів і веб-сервісів, що обслуговують щодня мільйони користувачів.';

const docChildren = [
  // Chapter title
  new Paragraph({
    children: [new TextRun({ text: 'Розділ 1. Вступ', bold: true, size: SZ.TITLE, font: 'Times New Roman', color: C.NAVY })],
    spacing: { before: 0, after: 100 },
    border: { bottom: bdr(16, C.ACCENT) },
  }),
  // Intro paragraph
  new Paragraph({
    children: parseInline(INTRO),
    indent: { firstLine: IND.FIRST },
    spacing: { line: 276, before: 160, after: 240 },
    alignment: AlignmentType.JUSTIFIED,
  }),
];

// Process each section file
for (const file of FILES) {
  inSummary = false;
  const content = fs.readFileSync(path.join(SECT_DIR, file), 'utf-8');
  const blocks = parseMd(content);
  for (const block of blocks) {
    docChildren.push(...toElems(block));
  }
}
docChildren.push(new Paragraph({ children: [] }));

// ── Create document ───────────────────────────────────────────────────────────
const doc = new Document({
  numbering,
  sections: [{
    properties: {
      page: {
        size: { width: A5_W, height: A5_H },
        margin: { top: M_T, bottom: M_B, left: M_L, right: M_R },
      },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: SZ.FOOT, color: C.GRAY }),
          ],
        })],
      }),
    },
    children: docChildren,
  }],
});

// ── Save ──────────────────────────────────────────────────────────────────────
Packer.toBuffer(doc)
  .then(buf => {
    const out = path.join(OUT_DIR, 'chapter-01-vstup.docx');
    fs.writeFileSync(out, buf);
    console.log('OK ' + out);
  })
  .catch(err => {
    console.error('ERR', err.message);
    process.exit(1);
  });
