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

const decimalLevel = {
  level:     0,
  format:    LevelFormat.DECIMAL,
  text:      '%1.',
  alignment: AlignmentType.LEFT,
  style: {
    paragraph: {
      indent:  { left: IND.LIST_LEFT, hanging: IND.LIST_HANG },
      spacing: { after: SP.LIST_AFT },
    },
    run: { font: 'Times New Roman' },
  },
};

// Будує конфіг нумерації з N незалежних слотів для нумерованих списків.
// Кожен слот numbers-0, numbers-1, … починає відлік з 1 незалежно від інших.
function buildNumberingConfig(slots = 50) {
  const config = [
    {
      reference: 'bullets',
      levels: [{
        level:     0,
        format:    LevelFormat.BULLET,
        text:      '—',
        alignment: AlignmentType.LEFT,
        style: {
          paragraph: {
            indent:  { left: IND.LIST_LEFT, hanging: IND.LIST_HANG },
            spacing: { after: SP.LIST_AFT },
          },
          run: { font: 'Times New Roman' },
        },
      }],
    },
  ];
  for (let i = 0; i < slots; i++) {
    config.push({ reference: `numbers-${i}`, levels: [decimalLevel] });
  }
  return config;
}

module.exports = { buildNumberingConfig };
