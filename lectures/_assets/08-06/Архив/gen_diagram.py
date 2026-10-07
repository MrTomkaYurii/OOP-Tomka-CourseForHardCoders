from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)

W, H = 1000, 460
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
d.text((W//2, 28), "Методи розширення: синтаксис і механізм компіляції", ACCENT, font=ft, anchor="mm")

# ── PART 1: Anatomy ──
d.text((W//2, 55), "Структура методу розширення", MUTED, font=fl, anchor="mm")
sig_y = 70
d.rounded_rectangle([20, sig_y, W-20, sig_y+50], radius=8, fill=PANEL, outline=LINE_C, width=1)

tokens = [
    ("public static ", MUTED),
    ("bool ", ACCENT),
    ("IsFever", TEXT),
    ("(", TEXT),
    ("this ", AMBER),
    ("double ", ACCENT),
    ("celsius", TEXT),
    (")  =>  celsius > 37.5;", MUTED),
]
x = 35
y_tok = sig_y + 25
for tok, col in tokens:
    d.text((x, y_tok), tok, col, font=fc, anchor="lm")
    bb = d.textbbox((x, y_tok), tok, font=fc, anchor="lm")
    x = bb[2]

lbl_y = sig_y + 52
label_items = [
    (50,  "public static", MUTED,  "клас і метод — статичні"),
    (230, "bool",          ACCENT, "тип результату"),
    (380, "IsFever",       TEXT,   "назва методу"),
    (530, "this double",   AMBER,  "тип, що розширюється"),
    (730, "celsius",       ACCENT, "параметр-значення"),
]
for lx, code, col, desc in label_items:
    d.text((lx, lbl_y+4),  code, col,  font=fs, anchor="lm")
    d.text((lx, lbl_y+20), desc, MUTED, font=fs, anchor="lm")

# ── DIVIDER ──
div_y = lbl_y + 46
d.line([(20, div_y), (W-20, div_y)], LINE_C, width=1)

# ── PART 2: Call translation ──
d.text((W//2, div_y+16), "Як компілятор транслює виклик", MUTED, font=fl, anchor="mm")

# Left box: user call
box1_y = div_y + 36
d.rounded_rectangle([30, box1_y, 370, box1_y+76], radius=8, fill=PANEL, outline=ACCENT, width=2)
d.text((200, box1_y+16), "Запис програміста", ACCENT, font=fs, anchor="mm")
d.line([(40, box1_y+30), (360, box1_y+30)], LINE_C, width=1)
d.text((200, box1_y+50), "temp.IsFever()", TEXT, font=fc, anchor="mm")
d.text((200, box1_y+68), "// як звичайний метод", MUTED, font=fs, anchor="mm")

# Arrow
arr_y = box1_y + 38
d.line([(375, arr_y), (450, arr_y)], MUTED, width=2)
d.polygon([(450, arr_y-6), (450, arr_y+6), (463, arr_y)], MUTED)
d.text((417, arr_y-14), "компілятор", MUTED, font=fs, anchor="mm")

# Right box: actual call
d.rounded_rectangle([466, box1_y, W-30, box1_y+76], radius=8, fill=PANEL, outline=LINE_C, width=2)
d.text((718, box1_y+16), "Реальний виклик", MUTED, font=fs, anchor="mm")
d.line([(476, box1_y+30), (960, box1_y+30)], LINE_C, width=1)
d.text((718, box1_y+50), "TemperatureExtensions.IsFever(temp)", TEXT, font=fc, anchor="mm")
d.text((718, box1_y+68), "// статичний метод зі static-класу", MUTED, font=fs, anchor="mm")

# ── RULES ──
rules_y = box1_y + 96
d.line([(20, rules_y), (W-20, rules_y)], LINE_C, width=1)

rules = [
    ("✓", "Метод розширення визначається у public static класі",            MUTED),
    ("✓", "Перший параметр — this ТипЩоРозширюється — не передається явно", MUTED),
    ("✓", "Namespace статик-класу повинен бути підключений через using",     MUTED),
    ("✗", "Instance-метод завжди перемагає extension з тією самою сигнатурою", AMBER),
]
for i, (sign, rule, col) in enumerate(rules):
    y = rules_y + 14 + i * 24
    sign_col = ACCENT if sign == "✓" else AMBER
    d.text((32, y), sign, sign_col, font=fb, anchor="lm")
    d.text((52, y), rule, col, font=fs, anchor="lm")

out = "lectures/_assets/08-06/extension-method-anatomy.png"
img.save(out)
print(f"OK: {out}")
