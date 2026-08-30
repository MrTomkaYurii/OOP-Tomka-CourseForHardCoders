'use strict';
// ═══════════════════════════════════════════════════════════════════════════════
// parser.js — Markdown → Block AST
// Чиста функція: нема залежностей від docx.
//
// parseMd(content, opts)
//   opts.lab === true → режим лабораторних:
//     • горизонтальні лінії "---" пропускаються
//     • усі "## …" стають секціями (не лише "1.1")
//     • списки збирають вкладений контент (код, під-списки) у item.children
// ═══════════════════════════════════════════════════════════════════════════════

// ── Frontmatter ───────────────────────────────────────────────────────────────
function parseFrontmatter(content) {
  const lines = content.split(/\r?\n/);
  if (!lines[0] || lines[0].trim() !== '---') return { meta: {}, body: content };

  let i = 1;
  const yamlLines = [];
  while (i < lines.length && lines[i].trim() !== '---') { yamlLines.push(lines[i]); i++; }
  i++; // skip closing ---

  const meta = {};
  for (const ln of yamlLines) {
    const m = ln.match(/^(\w+):\s*"?(.+?)"?\s*$/);
    if (m) meta[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
  return { meta, body: lines.slice(i).join('\n') };
}

// ── Inline parser → токени ────────────────────────────────────────────────────
// Токен: { type: 'text'|'bold'|'italic'|'bolditalic'|'code'|'link', text, href? }
function parseInline(text) {
  const tokens = [];
  let i = 0, buf = '';
  const flush = () => { if (buf) { tokens.push({ type: 'text', text: buf }); buf = ''; } };

  while (i < text.length) {
    // Backslash-екранування: \<  \>  \|  \*  \_  \` … → літерал
    if (text[i] === '\\' && i + 1 < text.length && /[!-/:-@[-`{-~]/.test(text[i+1])) {
      buf += text[i+1]; i += 2; continue;
    }
    // Bold+Italic ***
    if (text[i]==='*' && text[i+1]==='*' && text[i+2]==='*') {
      const e = text.indexOf('***', i+3);
      if (e !== -1) { flush(); const s = text.slice(i+3,e); tokens.push({ type:'bolditalic', text: s, children: parseInline(s) }); i=e+3; continue; }
    }
    // Bold **
    if (text[i]==='*' && text[i+1]==='*' && text[i+2]!=='*') {
      const e = text.indexOf('**', i+2);
      if (e !== -1) { flush(); const s = text.slice(i+2,e); tokens.push({ type:'bold', text: s, children: parseInline(s) }); i=e+2; continue; }
    }
    // Italic *
    if (text[i]==='*' && text[i+1]!=='*') {
      const e = text.indexOf('*', i+1);
      if (e !== -1) { flush(); const s = text.slice(i+1,e); tokens.push({ type:'italic', text: s, children: parseInline(s) }); i=e+1; continue; }
    }
    // Inline code `
    if (text[i]==='`') {
      const e = text.indexOf('`', i+1);
      if (e !== -1) { flush(); tokens.push({ type:'code', text: text.slice(i+1,e) }); i=e+1; continue; }
    }
    // Link [text](url)
    if (text[i]==='[') {
      const cb = text.indexOf(']', i+1);
      if (cb !== -1 && text[cb+1]==='(') {
        const cp = text.indexOf(')', cb+2);
        if (cp !== -1) {
          flush();
          const linkText = text.slice(i+1,cb).replace(/\\([!-/:-@[-`{-~])/g, '$1');
          tokens.push({ type:'link', text: linkText, href: text.slice(cb+2,cp) });
          i=cp+1; continue;
        }
      }
    }
    buf += text[i++];
  }
  flush();
  return tokens;
}

// ── Прибрати спільний лівий відступ у наборі рядків ───────────────────────────
function dedent(lines) {
  const indents = lines
    .filter(l => l.trim())
    .map(l => l.length - l.trimStart().length);
  const min = indents.length ? Math.min(...indents) : 0;
  return lines.map(l => (l.length >= min ? l.slice(min) : l));
}

const HR_RE      = /^(-{3,}|\*{3,}|_{3,})$/;
const H_RE       = /^(#{1,6})\s+(.+)$/;
const FENCE_RE    = /^```/;
const BULLET_RE   = /^(\s*)[-*]\s+(.*)$/;
const ORDERED_RE  = /^(\s*)\d+\.\s+(.*)$/;

// ── Вкладений парсер списку (lab-режим) ───────────────────────────────────────
// Повертає { block, next } — item.children = вкладені блоки (код, під-списки…)
function parseList(lines, start, ordered, opts) {
  const markerRe = ordered ? ORDERED_RE : BULLET_RE;
  const items = [];
  let i = start;
  const baseIndent = (lines[i].match(markerRe) || [,''])[1].length;

  while (i < lines.length) {
    // Пропускаємо порожні рядки між елементами (loose list),
    // але лише якщо далі — елемент того ж рівня.
    if (!lines[i].trim()) {
      let j = i;
      while (j < lines.length && !lines[j].trim()) j++;
      const mm = j < lines.length ? lines[j].match(markerRe) : null;
      if (mm && mm[1].length === baseIndent) { i = j; } else { break; }
    }
    const m = lines[i].match(markerRe);
    if (!m || m[1].length !== baseIndent) break;
    const itemText = m[2].trim();
    i++;

    // Збираємо вкладені рядки (глибший відступ), поки не наступний маркер того ж рівня.
    // Порожній рядок не завершує item, якщо далі йде глибше вкладений блок.
    const childLines = [];
    while (i < lines.length) {
      const ln = lines[i];
      if (!ln.trim()) {
        let j = i + 1;
        while (j < lines.length && !lines[j].trim()) j++;
        if (j >= lines.length) { i = j; break; }
        const nextIndent = lines[j].length - lines[j].trimStart().length;
        if (nextIndent > baseIndent) { childLines.push(''); i++; continue; }
        break;
      }
      const indent = ln.length - ln.trimStart().length;
      if (indent <= baseIndent) break;                         // наступний елемент або рядок поза списком
      childLines.push(ln);
      i++;
    }

    const children = childLines.length
      ? parseBlocks(dedent(childLines), opts)
      : [];
    items.push({ text: itemText, children });
  }

  return { block: { type: ordered ? 'numbered' : 'bullets', items }, next: i };
}

// ── Блоковий парсер (працює зі списком рядків) ────────────────────────────────
function parseBlocks(lines, opts = {}) {
  const lab = !!opts.lab;
  const blocks = [];
  let i = 0;
  let lastWasHead = false;

  while (i < lines.length) {
    const ln = lines[i];
    if (!ln || !ln.trim()) { i++; continue; }

    // ── Горизонтальна лінія "---" ────────────────────────────────────────────
    if (HR_RE.test(ln.trim())) {
      if (!lab) blocks.push({ type: 'para', text: ln.trim(), firstAfterHead: lastWasHead });
      // у lab-режимі просто пропускаємо
      i++; lastWasHead = false; continue;
    }

    // ── Code fence ──────────────────────────────────────────────────────────
    if (ln.trimStart().startsWith('```')) {
      const indent = ln.length - ln.trimStart().length;
      const lang   = ln.trimStart().slice(3).trim().toLowerCase();
      const pfx    = ' '.repeat(indent);
      i++;
      const codeLines = [];
      while (i < lines.length && !lines[i].trimStart().startsWith('```')) {
        const cl = lines[i];
        codeLines.push(indent > 0 && cl.startsWith(pfx) ? cl.slice(indent) : cl);
        i++;
      }
      i++; // skip closing ```
      blocks.push({ type: 'code', lang, lines: codeLines });
      lastWasHead = false;
      continue;
    }

    // ── Table (допускає лівий відступ — таблиці всередині списків) ────────────
    if (ln.trimStart().startsWith('|')) {
      const rows = [];
      while (i < lines.length && lines[i].trimStart().startsWith('|')) {
        const row = lines[i].trim(); i++;
        if (/^\|[-:\s|]+\|$/.test(row)) continue;
        const cells = row.split('|').slice(1, -1).map(c => c.trim());
        rows.push(cells);
      }
      if (rows.length) blocks.push({ type: 'table', rows });
      lastWasHead = false;
      continue;
    }

    // ── Headings ────────────────────────────────────────────────────────────
    const hm = ln.match(H_RE);
    if (hm) {
      const level = hm[1].length;
      const text  = hm[2].trim();
      if (level === 1) {
        blocks.push({ type: 'h1', text });
      } else if (level === 2) {
        let type;
        if (/^підсумок$/i.test(text))          type = 'summary_h';
        else if (!lab && /^\d+\.\d+/.test(text)) type = 'section';
        else if (lab)                           type = 'section';
        else                                    type = 'h2';
        blocks.push({ type, text });
      } else {
        blocks.push({ type: 'h3', text });
      }
      i++; lastWasHead = true; continue;
    }

    // ── Image ───────────────────────────────────────────────────────────────
    if (/^!\[/.test(ln)) {
      const m = ln.match(/^!\[([^\]]*)\]\(([^)]*)\)/);
      blocks.push({ type: 'image', alt: m ? m[1] : '', src: m ? m[2] : '' });
      i++; lastWasHead = false; continue;
    }

    // ── Bullet list ─────────────────────────────────────────────────────────
    if (BULLET_RE.test(ln) && (ln.length - ln.trimStart().length) === 0) {
      if (lab) {
        const { block, next } = parseList(lines, i, false, opts);
        blocks.push(block); i = next;
      } else {
        const items = [];
        while (i < lines.length && /^- /.test(lines[i])) { items.push(lines[i].slice(2).trim()); i++; }
        blocks.push({ type: 'bullets', items });
      }
      lastWasHead = false; continue;
    }

    // ── Numbered list ───────────────────────────────────────────────────────
    if (ORDERED_RE.test(ln) && (ln.length - ln.trimStart().length) === 0) {
      if (lab) {
        const { block, next } = parseList(lines, i, true, opts);
        blocks.push(block); i = next;
      } else {
        const items = [];
        while (i < lines.length && /^\d+\. /.test(lines[i])) {
          items.push(lines[i].replace(/^\d+\. /, '').trim()); i++;
        }
        blocks.push({ type: 'numbered', items });
      }
      lastWasHead = false; continue;
    }

    // ── Blockquote ──────────────────────────────────────────────────────────
    if (/^>\s?/.test(ln)) {
      let text = ln.replace(/^>\s?/, '').trim(); i++;
      while (i < lines.length && /^>\s?/.test(lines[i])) { text += ' ' + lines[i].replace(/^>\s?/, '').trim(); i++; }
      blocks.push({ type: 'blockquote', text: text.trim() });
      lastWasHead = false; continue;
    }

    // ── Paragraph ───────────────────────────────────────────────────────────
    let paraText = ln.trim(); i++;
    while (i < lines.length) {
      const nx = lines[i];
      if (!nx || !nx.trim()) break;
      if (/^(#{1,6} |```|\||!\[|[-*]\s|\d+\. |>\s?)/.test(nx)) break;
      if (HR_RE.test(nx.trim())) break;
      paraText += ' ' + nx.trim(); i++;
    }
    blocks.push({ type: 'para', text: paraText, firstAfterHead: lastWasHead });
    lastWasHead = false;
  }

  return blocks;
}

// ── Публічний вхід ───────────────────────────────────────────────────────────
function parseMd(content, opts = {}) {
  const { meta, body } = parseFrontmatter(content);
  const blocks = parseBlocks(body.split(/\r?\n/), opts);
  return { meta, blocks };
}

module.exports = { parseMd, parseBlocks, parseInline, parseFrontmatter, dedent };
