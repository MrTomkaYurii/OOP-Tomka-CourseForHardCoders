from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)

W, H = 1000, 520
img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

def font(name, size):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
    except:
        return ImageFont.load_default()

ft = font("arialbd.ttf", 17)
fl = font("arial.ttf",   14)
fc = font("cour.ttf",    13)
fs = font("arial.ttf",   12)
fb = font("arialbd.ttf", 13)

# ── TITLE ──
d.text((W//2, 28), "Індексатор: синтаксис та порівняння з властивістю", ACCENT, font=ft, anchor="mm")

# ── PART 1: Anatomy ──
d.text((W//2, 56), "Анатомія індексатора", MUTED, font=fl, anchor="mm")
sig_y = 72
d.rounded_rectangle([20, sig_y, W-20, sig_y+50], radius=8, fill=PANEL, outline=LINE_C, width=1)

tokens = [
    ("public ", MUTED),
    ("Patient ", ACCENT),
    ("this", AMBER),
    ("[", TEXT),
    ("int ", ACCENT),
    ("index", TEXT),
    ("]", TEXT),
    ("  {  get { ... }  set { ... }  }", MUTED),
]
x = 35
y_tok = sig_y + 25
for tok, col in tokens:
    d.text((x, y_tok), tok, col, font=fc, anchor="lm")
    bb = d.textbbox((x, y_tok), tok, font=fc, anchor="lm")
    x = bb[2]

# Labels
lbl_y = sig_y + 50 + 14
label_items = [
    (50,  "public",  MUTED,  "модифікатор доступу"),
    (180, "Patient", ACCENT, "тип результату"),
    (340, "this",    AMBER,  "ключове слово (замість імені)"),
    (560, "int index", ACCENT, "тип та ім'я параметра"),
]
for lx, code, col, desc in label_items:
    d.text((lx, lbl_y),    code, col,  font=fs, anchor="lm")
    d.text((lx, lbl_y+16), desc, MUTED, font=fs, anchor="lm")

# ── DIVIDER ──
div_y = lbl_y + 42
d.line([(20, div_y), (W-20, div_y)], LINE_C, width=1)
d.line([(W//2, div_y), (W//2, H-20)], LINE_C, width=1)

# ── LEFT: Property ──
d.text((250, div_y+18), "Властивість", AMBER, font=fb, anchor="mm")

prop_lines = [
    ("public Patient FirstPatient", TEXT),
    ("{", MUTED),
    ("    get => patients[0];", ACCENT),
    ("    set => patients[0] = value;", ACCENT),
    ("}", MUTED),
    ("// ward.FirstPatient — фіксована назва", MUTED),
]
for i, (line, col) in enumerate(prop_lines):
    d.text((35, div_y + 42 + i*28), line, col, font=fc, anchor="lm")

# ── RIGHT: Indexer ──
d.text((750, div_y+18), "Індексатор", ACCENT, font=fb, anchor="mm")

idx_lines = [
    ("public Patient this[int index]", TEXT),
    ("{", MUTED),
    ("    get => patients[index];", ACCENT),
    ("    set => patients[index] = value;", ACCENT),
    ("}", MUTED),
    ("// ward[0], ward[1], ward[i] — динамічно", MUTED),
]
for i, (line, col) in enumerate(idx_lines):
    d.text((W//2+15, div_y + 42 + i*28), line, col, font=fc, anchor="lm")

# ── BOTTOM: Key differences ──
note_y = div_y + 42 + 6*28 + 10
d.line([(20, note_y), (W-20, note_y)], LINE_C, width=1)
d.text((W//2, note_y+16),
    "Індексатор — як властивість, але з параметром. Замість фіксованої назви — this[параметр].",
    MUTED, font=fs, anchor="mm")
d.text((W//2, note_y+34),
    "Можна визначити кілька індексаторів з різними типами параметрів (перевантаження).",
    MUTED, font=fs, anchor="mm")

out = "lectures/_assets/08-04/indexer-anatomy.png"
img.save(out)
print(f"OK: {out}")
