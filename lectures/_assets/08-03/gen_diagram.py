from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)

W, H = 1000, 500
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
d.text((W//2, 28), "Оператор перетворення типів: implicit vs explicit", ACCENT, font=ft, anchor="mm")

# ── PART 1: Syntax anatomy ──
d.text((W//2, 58), "Анатомія оператора", MUTED, font=fl, anchor="mm")

sig_y = 75
d.rounded_rectangle([20, sig_y, W-20, sig_y+52], radius=8, fill=PANEL, outline=LINE_C, width=1)

# Draw the signature token by token with colors
tokens = [
    ("public static ", MUTED),
    ("implicit", AMBER),
    (" operator ", TEXT),
    ("BodyTemperature", ACCENT),
    ("(", TEXT),
    ("double", ACCENT),
    (" celsius", TEXT),
    (")", TEXT),
]
x = 35
y_tok = sig_y + 26
for tok, col in tokens:
    d.text((x, y_tok), tok, col, font=fc, anchor="lm")
    bb = d.textbbox((x, y_tok), tok, font=fc, anchor="lm")
    x = bb[2]

# Labels below signature
label_data = [
    (45,  sig_y+52+18, "public static", MUTED,  "обов'язково"),
    (185, sig_y+52+18, "implicit",      AMBER,  "або explicit"),
    (330, sig_y+52+18, "operator",      TEXT,   "ключове слово"),
    (480, sig_y+52+18, "BodyTemp...",   ACCENT, "тип результату (куди)"),
    (680, sig_y+52+18, "double celsius",ACCENT, "параметр (звідки)"),
]
for lx, ly, code, col, desc in label_data:
    d.text((lx, ly), f"{code}:", col, font=fs, anchor="lm")
    d.text((lx, ly+16), desc, MUTED, font=fs, anchor="lm")

# ── DIVIDER ──
div_y = sig_y + 52 + 58
d.line([(20, div_y), (W-20, div_y)], LINE_C, width=1)
d.line([(W//2, div_y), (W//2, H-20)], LINE_C, width=1)

# ── LEFT: implicit ──
d.text((250, div_y+20), "implicit — неявне перетворення", AMBER, font=fb, anchor="mm")

impl_rows = [
    ("double celsius = 36.6;",          "оголошуємо double"),
    ("BodyTemperature t = celsius;",    "← компілятор сам викликає operator"),
    ("// не потрібен (double) cast",    ""),
]
for i, (code, note) in enumerate(impl_rows):
    y = div_y + 48 + i * 52
    d.rounded_rectangle([25, y, W//2-15, y+42], radius=6, fill=PANEL, outline=LINE_C, width=1)
    d.text((40, y+14), code, TEXT if not code.startswith("//") else MUTED, font=fc, anchor="lm")
    if note:
        d.text((40, y+32), note, MUTED, font=fs, anchor="lm")

badge_y = div_y + 48 + 3*52 + 4
d.rounded_rectangle([25, badge_y, W//2-15, badge_y+36], radius=6, fill=PANEL, outline=AMBER, width=2)
d.text((250, badge_y+18), "Використовувати коли: безпечне, без втрат, очевидне", AMBER, font=fs, anchor="mm")

# ── RIGHT: explicit ──
d.text((750, div_y+20), "explicit — явне перетворення", ACCENT, font=fb, anchor="mm")

expl_rows = [
    ("BodyTemperature t = new(38.5);", "оголошуємо об'єкт"),
    ("double c = (double)t;",          "← потрібен явний (double) cast"),
    ("// без (double) — помилка",      ""),
]
for i, (code, note) in enumerate(expl_rows):
    y = div_y + 48 + i * 52
    d.rounded_rectangle([W//2+15, y, W-25, y+42], radius=6, fill=PANEL, outline=LINE_C, width=1)
    d.text((W//2+30, y+14), code, TEXT if not code.startswith("//") else MUTED, font=fc, anchor="lm")
    if note:
        d.text((W//2+30, y+32), note, MUTED, font=fs, anchor="lm")

badge_y2 = div_y + 48 + 3*52 + 4
d.rounded_rectangle([W//2+15, badge_y2, W-25, badge_y2+36], radius=6, fill=PANEL, outline=ACCENT, width=2)
d.text((750, badge_y2+18), "Використовувати коли: можлива втрата даних або неочевидно", ACCENT, font=fs, anchor="mm")

# ── BOTTOM NOTE ──
d.text((W//2, H-12),
    "Обмеження: оператор повинен перетворювати З типу або ДО типу, де він визначений",
    MUTED, font=fs, anchor="mm")

out = "lectures/_assets/08-03/conversion-implicit-explicit.png"
img.save(out)
print(f"OK: {out}")
