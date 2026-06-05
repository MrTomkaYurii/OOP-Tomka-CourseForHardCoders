from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)

W, H = 1000, 440
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
fb = font("arialbd.ttf", 12)

# ── TITLE ──
d.text((W//2, 28), "Патерн властивостей: анатомія та варіанти", ACCENT, font=ft, anchor="mm")

# ── PART 1: Anatomy ──
d.text((W//2, 54), "Структура патерну властивостей", MUTED, font=fl, anchor="mm")
sig_y = 68
d.rounded_rectangle([20, sig_y, W-20, sig_y+52], radius=8, fill=PANEL, outline=LINE_C, width=1)

# tokens
tokens = [
    ("patient",     TEXT),
    (" is ",        MUTED),
    ("Patient",     ACCENT),
    (" { ",         TEXT),
    ("Status",      AMBER),
    (": ",          MUTED),
    ('"Active"',    ACCENT),
    (", ",          MUTED),
    ("Priority",    AMBER),
    (": ",          MUTED),
    ("> 2",         ACCENT),
    (" }",          TEXT),
]
x = 35
y_tok = sig_y + 26
for tok, col in tokens:
    d.text((x, y_tok), tok, col, font=fc, anchor="lm")
    bb = d.textbbox((x, y_tok), tok, font=fc, anchor="lm")
    x = bb[2]

lbl_y = sig_y + 52
label_items = [
    (36,  "patient",   TEXT,   "об'єкт"),
    (160, "Patient",   ACCENT, "перевірка типу (optional)"),
    (370, "Status",    AMBER,  "ім'я властивості"),
    (520, '\"Active\"', ACCENT, "очікуване значення"),
    (680, "Priority",  AMBER,  "друга властивість"),
    (800, "> 2",       ACCENT, "може бути патерном"),
]
for lx, code, col, desc in label_items:
    d.text((lx, lbl_y+4),  code, col,  font=fs, anchor="lm")
    d.text((lx, lbl_y+18), desc, MUTED, font=fs, anchor="lm")

# ── PART 2: 4 variants ──
div_y = lbl_y + 44
d.line([(20, div_y), (W-20, div_y)], LINE_C, width=1)
d.text((W//2, div_y+14), "Варіанти патерну властивостей", MUTED, font=fl, anchor="mm")

variants = [
    ("Тип + властивість",   "patient is Patient { Status: \"Active\" }",               ACCENT),
    ("Тільки властивість",  "patient is { Status: \"Active\" }",                       TEXT),
    ("Вкладений об'єкт",    'patient is { Department.Name: "Кардіологія" }',           ACCENT),
    ("З захопленням var",   '{ Status: var s, Priority: var p }  =>  $"{s}/{p}"',      AMBER),
]
for i, (label, code, col) in enumerate(variants):
    y = div_y + 34 + i * 52
    d.rounded_rectangle([20, y, W-20, y+44], radius=6, fill=PANEL, outline=LINE_C, width=1)
    d.text((34, y+14), label + ":", MUTED, font=fb, anchor="lm")
    d.text((34, y+32), code, col, font=fc, anchor="lm")

out = "lectures/_assets/09-02/property-pattern-anatomy.png"
img.save(out)
print(f"OK: {out}")
