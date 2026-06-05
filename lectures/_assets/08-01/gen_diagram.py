from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE   = (44, 53, 49)
PANEL  = (25, 30, 28)

W, H = 1000, 470
img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

def font(name, size):
    for path in [f"C:/Windows/Fonts/{name}", f"/usr/share/fonts/truetype/dejavu/{name}"]:
        try:
            return ImageFont.truetype(path, size)
        except:
            pass
    return ImageFont.load_default()

ft = font("arialbd.ttf", 17)
fl = font("arial.ttf",   14)
fc = font("cour.ttf",    14)
fs = font("arial.ttf",   12)

# ── TITLE ──
d.text((W//2, 28), "Перевантаження оператора: від виразу до виклику методу", ACCENT, font=ft, anchor="mm")

# ── PART 1: Transformation ──
# Left box
d.rounded_rectangle([30, 58, 290, 168], radius=8, fill=PANEL, outline=ACCENT, width=2)
d.text((160, 78), "Код програміста", ACCENT, font=fl, anchor="mm")
d.line([(40, 92), (280, 92)], LINE, width=1)
d.text((160, 118), "t1 + delta", TEXT, font=fc, anchor="mm")
d.text((160, 148), "t1 > t2", TEXT, font=fc, anchor="mm")

# Double arrow
for ay, label in [(118, "operator+"), (148, "operator>")]:
    d.line([(295, ay), (400, ay)], MUTED, width=2)
    d.polygon([(400, ay-6), (400, ay+6), (414, ay)], MUTED)
    d.text((354, ay - 13), label, MUTED, font=fs, anchor="mm")

# Right box: actual calls
d.rounded_rectangle([418, 58, 720, 168], radius=8, fill=PANEL, outline=LINE, width=2)
d.text((569, 78), "Виклик статичного методу", MUTED, font=fl, anchor="mm")
d.line([(428, 92), (710, 92)], LINE, width=1)
d.text((569, 118), "BodyTemp.operator+(t1, delta)", TEXT, font=fc, anchor="mm")
d.text((569, 148), "BodyTemp.operator>(t1, t2)", TEXT, font=fc, anchor="mm")

# Return types
d.line([(725, 113), (770, 113)], MUTED, width=1)
d.polygon([(770, 107), (770, 119), (782, 113)], MUTED)
d.rounded_rectangle([785, 95, 970, 170], radius=8, fill=PANEL, outline=LINE, width=1)
d.text((877, 108), "→ BodyTemperature", ACCENT, font=fs, anchor="mm")
d.text((877, 130), "(новий обʼєкт)", MUTED, font=fs, anchor="mm")
d.text((877, 150), "→ bool", ACCENT, font=fs, anchor="mm")

# ── DIVIDER ──
d.text((W//2, 193), "Правила визначення оператора в класі", MUTED, font=fl, anchor="mm")
d.line([(30, 208), (W-30, 208)], LINE, width=1)

# ── PART 2: 4 syntax rules ──
rows = [
    ("public static",              "— обов'язкові модифікатори, оператор належить типу, не екземпляру"),
    ("ТипРезультату",              "— будь-який тип: клас, struct, bool, int, double..."),
    ("operator  СИМВОЛ",           "— ключове слово operator + символ (+, -, >, ==, ...)"),
    ("(КласТипу param, ...)",      "— ≥1 параметр повинен бути типом цього класу або структури"),
]

for i, (code_part, desc) in enumerate(rows):
    y = 225 + i * 52
    d.rounded_rectangle([30, y, W-30, y+42], radius=6, fill=PANEL, outline=LINE, width=1)
    d.text((48, y+21), code_part, ACCENT, font=fc, anchor="lm")
    bbox = d.textbbox((48, y+21), code_part, font=fc, anchor="lm")
    d.text((bbox[2] + 18, y+21), desc, MUTED, font=fl, anchor="lm")

out = "lectures/_assets/08-01/operator-mechanism.png"
img.save(out)
print(f"OK: {out}")
