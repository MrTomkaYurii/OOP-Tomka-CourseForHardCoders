'use strict';
// ═══════════════════════════════════════════════════════════════════════════════
// images.js — PNG: читання, масштаб, побудова Paragraph з ImageRun
// ═══════════════════════════════════════════════════════════════════════════════

const fs   = require('fs');
const path = require('path');
const { Paragraph, TextRun, ImageRun, AlignmentType, BorderStyle, ShadingType } = require('docx');
const { C, SZ, SP, BD, IMG } = require('./constants');

// ── Читання розмірів PNG з IHDR (без сторонніх залежностей) ──────────────────
// Формат PNG: [8-байт сигнатура] + чанки. Перший чанк = IHDR (13 байт).
// Байти 16–19 = ширина (BE uint32), байти 20–23 = висота (BE uint32).
function readPngDims(filePath) {
  try {
    const buf = fs.readFileSync(filePath);
    // Перевірка PNG-сигнатури: 89 50 4E 47
    if (buf[0] !== 0x89 || buf[1] !== 0x50) return null;
    return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
  } catch {
    return null;
  }
}

// ── Пошук файлу зображення ────────────────────────────────────────────────────
// src у md: "_assets/01-01/dotnet-pipeline.png"
// assetsBase: абсолютний шлях до теки _assets/
function resolveImagePath(src, assetsBase) {
  if (!src || !assetsBase) return null;
  // Прибираємо "_assets/" якщо є — вже врахований у assetsBase
  const rel = src.replace(/^_assets\//, '');
  const candidate = path.join(assetsBase, ...rel.split('/'));
  return fs.existsSync(candidate) ? candidate : null;
}

// ── Масштаб під ширину контенту ───────────────────────────────────────────────
function scaleToFit(dims, maxW = IMG.MAX_W) {
  if (!dims || dims.w === 0) return { width: maxW, height: Math.round(maxW * 0.5) };
  const scale = dims.w > maxW ? maxW / dims.w : 1;
  return {
    width:  Math.round(dims.w * scale),
    height: Math.round(dims.h * scale),
  };
}

// ── Побудова [imageParagraph, captionParagraph] ────────────────────────────────
function buildImageElems(block, assetsBase) {
  const imgPath = resolveImagePath(block.src, assetsBase);

  if (imgPath) {
    const dims = readPngDims(imgPath);
    const { width, height } = scaleToFit(dims);

    const imgPara = new Paragraph({
      alignment: AlignmentType.CENTER,
      keepNext: true,        // не відривати від підпису
      spacing: { before: SP.IMG_BEF, after: SP.CAPTION_BEF },
      children: [new ImageRun({
        type: 'png',
        data: fs.readFileSync(imgPath),
        transformation: { width, height },
        altText: {
          title:       block.alt || 'Рисунок',
          description: block.alt || '',
          name:        block.alt || 'image',
        },
      })],
    });

    const caption = new Paragraph({
      style: 'FigureCaption',
      children: [new TextRun({
        text:    block.alt,
        font:    'Times New Roman',
        size:    SZ.CAPTION,
        italics: true,
        color:   C.CAPTION,
      })],
    });

    // Звіт у консоль
    process.stdout.write(`  ✔ ${width}×${height}px  ${block.src}\n`);

    return [imgPara, caption];
  }

  // Файл відсутній — placeholder
  if (block.src) {
    process.stdout.write(`  ✗ відсутній    ${block.src}\n`);
  }

  return [new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: SP.IMG_BEF, after: SP.CAPTION_AFT },
    shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'F5F5F5' },
    border: {
      top:    { style: BorderStyle.DASHED, size: 4, color: 'CCCCCC' },
      bottom: { style: BorderStyle.DASHED, size: 4, color: 'CCCCCC' },
      left:   { style: BorderStyle.DASHED, size: 4, color: 'CCCCCC' },
      right:  { style: BorderStyle.DASHED, size: 4, color: 'CCCCCC' },
    },
    children: [new TextRun({
      text:    `[ Діаграма: ${block.alt} ]`,
      font:    'Times New Roman',
      size:    SZ.BODY,
      italics: true,
      color:   C.PLACEHOLDER,
    })],
  })];
}

module.exports = { readPngDims, resolveImagePath, scaleToFit, buildImageElems };
