'use strict';
// ═══════════════════════════════════════════════════════════════════════════════
// md-to-docx.js — CLI-точка входу
//
// Використання:
//   node md-to-docx.js "lectures/sections/01-*.md" -o output/chapter-01.docx
//   node md-to-docx.js file1.md file2.md -o out.docx [--title "..."] [--assets path]
// ═══════════════════════════════════════════════════════════════════════════════

const {
  Document, Packer, Paragraph, TextRun, Footer,
  AlignmentType, PageNumber,
} = require('docx');
const fs    = require('fs');
const path  = require('path');
const JSZip = require('jszip');

const { parseMd }                       = require('./lib/parser');
const { render }                        = require('./lib/renderer');
const { paragraphStyles, defaultStyle } = require('./lib/styles');
const { numberingConfig }               = require('./lib/numbering');
const { C, SZ, PAGE }                   = require('./lib/constants');

// ── Простий glob (замість залежності) ─────────────────────────────────────────
function expandGlob(pattern) {
  if (!pattern.includes('*')) {
    return fs.existsSync(pattern) ? [pattern] : [];
  }
  const dir     = path.dirname(pattern);
  const basePat = path.basename(pattern)
    .replace(/[.+^${}()|[\]\\]/g, '\\$&') // escape regex-спецсимволи крім *
    .replace(/\*/g, '.*');
  const re = new RegExp(`^${basePat}$`);
  return fs.readdirSync(dir)
    .filter(f => re.test(f))
    .sort()
    .map(f => path.join(dir, f));
}

// ── Розбір CLI-аргументів ──────────────────────────────────────────────────────
function parseArgs(argv) {
  const args = argv.slice(2);
  const opts  = { output: null, title: null, assets: null, files: [] };

  for (let i = 0; i < args.length; i++) {
    if      (args[i] === '-o' || args[i] === '--output') opts.output = args[++i];
    else if (args[i] === '--title')  opts.title  = args[++i];
    else if (args[i] === '--assets') opts.assets = args[++i];
    else opts.files.push(args[i]);
  }
  return opts;
}

// ── Автопошук теки _assets/ ───────────────────────────────────────────────────
// Піднімається від директорії першого файлу — шукає _assets/
function findAssetsBase(firstFile) {
  let dir = path.dirname(path.resolve(firstFile));
  for (let depth = 0; depth < 5; depth++) {
    const candidate = path.join(dir, '_assets');
    if (fs.existsSync(candidate)) return candidate;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

// ── Footer: номер сторінки по центру ──────────────────────────────────────────
function makeFooter() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children:  [new TextRun({
        children: [PageNumber.CURRENT],
        font:     'Times New Roman',
        size:     SZ.FOOTER,
        color:    C.GRAY,
      })],
    })],
  });
}

// ── Приховати вбудовані Word-стилі через latentStyles у styles.xml ────────────
// docx-js не підтримує latentStyles в API, тому правимо ZIP вручну.
// defSemiHidden="1" + defQFormat="0" прибирає всі вбудовані стилі з галереї.
// Наші стилі з <w:qFormat/> залишаються видимими.
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

// ── Головна функція ───────────────────────────────────────────────────────────
async function main() {
  const opts = parseArgs(process.argv);

  // Розгортаємо glob-патерни у конкретні файли
  const files = opts.files.flatMap(expandGlob);
  if (!files.length) {
    console.error('❌  Не знайдено жодного файлу. Перевірте шлях або патерн.');
    process.exit(1);
  }

  if (!opts.output) {
    console.error('❌  Вкажіть вихідний файл: -o output/chapter-01.docx');
    process.exit(1);
  }

  console.log(`📄  Файлів: ${files.length}`);
  files.forEach(f => console.log(`    ${path.basename(f)}`));

  // Пошук _assets/
  const assetsBase = opts.assets
    ? path.resolve(opts.assets)
    : findAssetsBase(files[0]);

  if (assetsBase) {
    console.log(`🖼   Assets: ${assetsBase}`);
  } else {
    console.warn('⚠️   Теку _assets/ не знайдено — зображення будуть placeholders');
  }

  // ── Парсинг ─────────────────────────────────────────────────────────────────
  const allBlocks = [];
  let currentChapter = null;

  for (const file of files) {
    const content          = fs.readFileSync(file, 'utf-8');
    const { meta, blocks } = parseMd(content);

    // Ідентифікуємо главу: з frontmatter або з імені файлу (перші 2 символи)
    const chKey   = meta.chapter ? String(meta.chapter) : path.basename(file).slice(0, 2);
    const chTitle = opts.title && currentChapter === null
      ? opts.title
      : (meta.chapterTitle || meta.title || `Розділ ${chKey}`);

    if (chKey !== currentChapter) {
      currentChapter = chKey;
      allBlocks.push({ type: 'chapter', title: chTitle });
    }
    allBlocks.push(...blocks);
  }

  // ── Рендеринг ────────────────────────────────────────────────────────────────
  console.log('\n🔧  Рендеринг...');
  const children = render(allBlocks, assetsBase);

  // ── Збірка документа ─────────────────────────────────────────────────────────
  const doc = new Document({
    styles: {
      default:         defaultStyle,
      paragraphStyles: paragraphStyles,
    },
    numbering: {
      config: numberingConfig,
    },
    sections: [{
      properties: {
        page: {
          size:   { width: PAGE.A5_W, height: PAGE.A5_H },
          margin: { top: PAGE.M_TOP, bottom: PAGE.M_BOT, left: PAGE.M_INN, right: PAGE.M_OUT },
        },
      },
      footers:  { default: makeFooter() },
      children: children,
    }],
  });

  // ── Збереження ───────────────────────────────────────────────────────────────
  const outAbs = path.resolve(opts.output);
  fs.mkdirSync(path.dirname(outAbs), { recursive: true });

  let buf = await Packer.toBuffer(doc);
  buf = await suppressBuiltinStyles(buf);
  fs.writeFileSync(outAbs, buf);

  const kb = Math.round(buf.length / 1024);
  console.log(`\n✅  Збережено: ${outAbs}  (${kb} KB)`);
}

main().catch(err => {
  console.error('❌', err.message);
  if (process.env.DEBUG) console.error(err.stack);
  process.exit(1);
});
