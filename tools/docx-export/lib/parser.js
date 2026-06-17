'use strict';
// ═══════════════════════════════════════════════════════════════════════════════
// parser.js — Markdown → Block AST
// Чиста функція: нема залежностей від docx.
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
    // Bold+Italic ***
    if (text[i]==='*' && text[i+1]==='*' && text[i+2]==='*') {
      const e = text.indexOf('***', i+3);
      if (e !== -1) { flush(); tokens.push({ type:'bolditalic', text: text.slice(i+3,e) }); i=e+3; continue; }
    }
    // Bold **
    if (text[i]==='*' && text[i+1]==='*' && text[i+2]!=='*') {
      const e = text.indexOf('**', i+2);
      if (e !== -1) { flush(); tokens.push({ type:'bold', text: text.slice(i+2,e) }); i=e+2; continue; }
    }
    // Italic *
    if (text[i]==='*' && text[i+1]!=='*') {
      const e = text.indexOf('*', i+1);
      if (e !== -1) { flush(); tokens.push({ type:'italic', text: text.slice(i+1,e) }); i=e+1; continue; }
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
          tokens.push({ type:'link', text: text.slice(i+1,cb), href: text.slice(cb+2,cp) });
          i=cp+1; continue;
        }
      }
    }
    buf += text[i++];
  }
  flush();
  return tokens;
}

// ── Блоковий парсер ───────────────────────────────────────────────────────────
function parseMd(content) {
  const { meta, body } = parseFrontmatter(content);
  const lines = body.split(/\r?\n/);
  const blocks = [];
  let i = 0;
  let lastWasHead = false;  // для firstAfterHead на наступному абзаці

  while (i < lines.length) {
    const ln = lines[i];
    if (!ln || !ln.trim()) { i++; if (!lastWasHead) lastWasHead = false; continue; }

    // ── Code fence (підтримує відступні ``` всередині списків) ───────────────
    if (ln.trimStart().startsWith('```')) {
      const indent  = ln.length - ln.trimStart().length;
      const lang    = ln.trimStart().slice(3).trim().toLowerCase();
      const pfx     = ' '.repeat(indent);
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

    // ── Table ─────────────────────────────────────────────────────────────────
    if (ln.startsWith('|')) {
      const rows = [];
      while (i < lines.length && lines[i].startsWith('|')) {
        const row = lines[i]; i++;
        if (/^\|[-:\s|]+\|$/.test(row)) continue;  // separator
        const cells = row.split('|').slice(1,-1).map(c => c.trim());
        rows.push(cells);
      }
      if (rows.length) blocks.push({ type: 'table', rows });
      lastWasHead = false;
      continue;
    }

    // ── Headings ──────────────────────────────────────────────────────────────
    const h1m = ln.match(/^# (.+)/);
    if (h1m) {
      blocks.push({ type: 'h1', text: h1m[1].trim() });
      i++; lastWasHead = true; continue;
    }

    const h2m = ln.match(/^## (.+)/);
    if (h2m) {
      const text = h2m[1].trim();
      let type;
      if (/^\d+\.\d+/.test(text))       type = 'section';
      else if (/^підсумок$/i.test(text)) type = 'summary_h';
      else                               type = 'h2';
      blocks.push({ type, text });
      i++; lastWasHead = true; continue;
    }

    // ### і #### — обидва → h3 (h4 зустрічається 2 рази в усьому курсі)
    const h3m = ln.match(/^#{3,4} (.+)/);
    if (h3m) {
      blocks.push({ type: 'h3', text: h3m[1].trim() });
      i++; lastWasHead = true; continue;
    }

    // ── Image ─────────────────────────────────────────────────────────────────
    if (/^!\[/.test(ln)) {
      const m = ln.match(/^!\[([^\]]*)\]\(([^)]*)\)/);
      blocks.push({ type: 'image', alt: m?m[1]:'', src: m?m[2]:'' });
      i++; lastWasHead = false; continue;
    }

    // ── Bullet list ───────────────────────────────────────────────────────────
    if (/^- /.test(ln)) {
      const items = [];
      while (i < lines.length && /^- /.test(lines[i])) { items.push(lines[i].slice(2).trim()); i++; }
      blocks.push({ type: 'bullets', items });
      lastWasHead = false; continue;
    }

    // ── Numbered list ─────────────────────────────────────────────────────────
    if (/^\d+\. /.test(ln)) {
      const items = [];
      while (i < lines.length && /^\d+\. /.test(lines[i])) {
        items.push(lines[i].replace(/^\d+\. /, '').trim()); i++;
      }
      blocks.push({ type: 'numbered', items });
      lastWasHead = false; continue;
    }

    // ── Blockquote ────────────────────────────────────────────────────────────
    if (/^> /.test(ln)) {
      let text = ln.slice(2).trim(); i++;
      while (i < lines.length && /^> /.test(lines[i])) { text += ' ' + lines[i].slice(2).trim(); i++; }
      blocks.push({ type: 'blockquote', text });
      lastWasHead = false; continue;
    }

    // ── Paragraph (накопичує рядки-продовження) ───────────────────────────────
    let paraText = ln.trim(); i++;
    while (i < lines.length) {
      const nx = lines[i];
      if (!nx || !nx.trim()) break;
      if (/^(#{1,4} |```|\||!\[|-\s|\d+\. |> )/.test(nx)) break;
      paraText += ' ' + nx.trim(); i++;
    }
    blocks.push({ type: 'para', text: paraText, firstAfterHead: lastWasHead });
    lastWasHead = false;
  }

  return { meta, blocks };
}

module.exports = { parseMd, parseInline, parseFrontmatter };
