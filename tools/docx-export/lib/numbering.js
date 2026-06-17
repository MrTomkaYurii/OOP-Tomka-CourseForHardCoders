'use strict';
// ═══════════════════════════════════════════════════════════════════════════════
// numbering.js — конфіг маркованих і нумерованих списків
//
// Передається у Document({ numbering: { config: [...] } })
// Посилання з renderer.js: { reference: 'bullets', level: 0 }
//                           { reference: 'numbers', level: 0 }
// ═══════════════════════════════════════════════════════════════════════════════

const { LevelFormat, AlignmentType } = require('docx');
const { IND, SP } = require('./constants');

const numberingConfig = [
  // ── Маркований список: — (em dash) ──────────────────────────────────────────
  {
    reference: 'bullets',
    levels: [{
      level:     0,
      format:    LevelFormat.BULLET,
      text:      '—',                    // — em dash
      alignment: AlignmentType.LEFT,
      style: {
        paragraph: {
          indent:  { left: IND.LIST_LEFT, hanging: IND.LIST_HANG },
          spacing: { after: SP.LIST_AFT },
        },
        run: {
          font: 'Times New Roman',
        },
      },
    }],
  },

  // ── Нумерований список: 1. 2. 3. ────────────────────────────────────────────
  {
    reference: 'numbers',
    levels: [{
      level:     0,
      format:    LevelFormat.DECIMAL,
      text:      '%1.',
      alignment: AlignmentType.LEFT,
      style: {
        paragraph: {
          indent:  { left: IND.LIST_LEFT, hanging: IND.LIST_HANG },
          spacing: { after: SP.LIST_AFT },
        },
        run: {
          font: 'Times New Roman',
        },
      },
    }],
  },
];

module.exports = { numberingConfig };
