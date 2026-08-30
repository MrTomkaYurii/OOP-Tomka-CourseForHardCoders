'use strict';
// ═══════════════════════════════════════════════════════════════════════════════
// labs-to-docx.js — конвертер інструкцій лабораторних у окремі Word-файли (A4)
//
// Кожна лабораторна labs/lab-NN-*/instructions.md → output/labs/lab-NN-*.docx
//
// Використання:
//   node labs-to-docx.js                  # усі 22
//   node labs-to-docx.js --only 1          # лише Lab 01
//   node labs-to-docx.js --only 1,2,3      # порційно
//   node labs-to-docx.js --only 4-6        # діапазон
//   node labs-to-docx.js --outdir ../../output/labs
// ═══════════════════════════════════════════════════════════════════════════════

const {
  Document, Packer, Paragraph, TextRun, Header, Footer,
  AlignmentType, PageNumber, BorderStyle,
} = require('docx');
const fs    = require('fs');
const path  = require('path');
const JSZip = require('jszip');

const { parseMd }                       = require('./lib/parser');
const { render }                        = require('./lib/renderer');
const { paragraphStyles, defaultStyle } = require('./lib/styles');
const { buildNumberingConfig }          = require('./lib/numbering');
const { C, SZ, PAGE_A4 }                = require('./lib/constants');

const REPO      = path.resolve(__dirname, '..', '..');
const LABS_DIR  = path.join(REPO, 'labs');
const OUT_DIR   = path.join(REPO, 'output', 'labs');

// ── CLI ──────────────────────────────────────────────────────────────────────
function parseArgs(argv) {
  const args = argv.slice(2);
  const opts = { only: null, outdir: OUT_DIR };
  for (let i = 0; i < args.length; i++) {
    if      (args[i] === '--only')   opts.only   = args[++i];
    else if (args[i] === '--outdir') opts.outdir = path.resolve(args[++i]);
  }
  return opts;
}

// "1,2,3" | "4-6" | "7" → Set<number>
function parseOnly(spec) {
  if (!spec) return null;
  const set = new Set();
  for (const part of spec.split(',')) {
    const m = part.trim().match(/^(\d+)(?:-(\d+))?$/);
    if (!m) continue;
    const a = +m[1], b = m[2] ? +m[2] : a;
    for (let n = a; n <= b; n++) set.add(n);
  }
  return set;
}

// ── Колонтитули ──────────────────────────────────────────────────────────────
function makeHeader(title) {
  return new Header({
    children: [new Paragraph({
      alignment: AlignmentType.RIGHT,
      border:    { bottom: { style: BorderStyle.SINGLE, size: 4, color: C.CODE_BORD } },
      spacing:   { after: 120 },
      children:  [new TextRun({ text: title, font: 'Times New Roman', size: SZ.FOOTER, color: C.GRAY })],
    })],
  });
}

function makeFooter() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children:  [new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: SZ.FOOTER, color: C.GRAY })],
    })],
  });
}

// ── Приховати вбудовані Word-стилі (як у md-to-docx.js) ───────────────────────
async function suppressBuiltinStyles(buf) {
  const zip = await JSZip.loadAsync(buf);
  const stylesFile = zip.file('word/styles.xml');
  if (!stylesFile) return buf;
  let xml = await stylesFile.async('string');
  if (!xml.includes('<w:latentStyles')) {
    const latent = '<w:latentStyles w:defLockedState="0" w:defUnhideWhenUsed="0"' +
      ' w:defSemiHidden="1" w:defQFormat="0" w:count="376"/>';
    xml = xml.replace(/<\/w:docDefaults>/, '</w:docDefaults>\n  ' + latent);
  }
  zip.file('word/styles.xml', xml);
  return zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' });
}

// ── Конвертація однієї лабораторної ──────────────────────────────────────────
async function convertLab(slug, outdir) {
  const srcPath = path.join(LABS_DIR, slug, 'instructions.md');
  const md      = fs.readFileSync(srcPath, 'utf-8');

  const { blocks } = parseMd(md, { lab: true });
  const h1         = blocks.find(b => b.type === 'h1');
  const title      = h1 ? h1.text.replace(/[⭐️]/g, '').trim() : slug;

  const children = render(blocks, null, { lab: true });

  const doc = new Document({
    styles:    { default: defaultStyle, paragraphStyles },
    numbering: { config: buildNumberingConfig(200) },
    sections:  [{
      properties: {
        page: {
          size:   { width: PAGE_A4.W, height: PAGE_A4.H },
          margin: { top: PAGE_A4.M_TOP, bottom: PAGE_A4.M_BOT, left: PAGE_A4.M_LEFT, right: PAGE_A4.M_RIGHT },
        },
      },
      headers:  { default: makeHeader(title) },
      footers:  { default: makeFooter() },
      children,
    }],
  });

  let buf = await Packer.toBuffer(doc);
  buf = await suppressBuiltinStyles(buf);

  fs.mkdirSync(outdir, { recursive: true });
  const outPath = path.join(outdir, `${slug}.docx`);
  fs.writeFileSync(outPath, buf);
  return { outPath, kb: Math.round(buf.length / 1024), blocks: blocks.length };
}

// ── Main ─────────────────────────────────────────────────────────────────────
async function main() {
  const opts = parseArgs(process.argv);
  const only = parseOnly(opts.only);

  const slugs = fs.readdirSync(LABS_DIR, { withFileTypes: true })
    .filter(e => e.isDirectory() && /^lab-\d{2}-/.test(e.name))
    .map(e => e.name)
    .filter(s => !only || only.has(+s.slice(4, 6)))
    .sort();

  if (!slugs.length) { console.error('❌  Жодної лабораторної не знайдено'); process.exit(1); }

  console.log(`📄  Конвертую ${slugs.length} лаб → ${opts.outdir}\n`);
  for (const slug of slugs) {
    try {
      const r = await convertLab(slug, opts.outdir);
      console.log(`  ✅  ${slug}.docx  (${r.kb} KB, ${r.blocks} блоків)`);
    } catch (err) {
      console.error(`  ❌  ${slug}: ${err.message}`);
      if (process.env.DEBUG) console.error(err.stack);
    }
  }
  console.log('\n✨  Готово');
}

main().catch(err => { console.error('❌', err.stack || err.message); process.exit(1); });
