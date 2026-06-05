from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)

W, H = 960, 450
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

# Title
d.text((W//2, 28), "Постфіксний і префіксний ++: одне визначення, різна поведінка", ACCENT, font=ft, anchor="mm")

# Vertical divider
d.line([(W//2, 48), (W//2, H-30)], LINE_C, width=1)

# ── LEFT: POSTFIX  t2 = t1++ ──
d.text((240, 63), "Постфіксний:  t2 = t1++", AMBER, font=fl, anchor="mm")
d.line([(20, 78), (W//2-10, 78)], LINE_C, width=1)

post_steps = [
    ("тимчасова = t1",         "зберегти поточний об'єкт"),
    ("t1 = operator++(t1)",    "t1 отримує новий об'єкт"),
    ("результат = тимчасова",  "повернути СТАРУ копію"),
]

for i, (code, desc) in enumerate(post_steps):
    y = 92 + i * 78
    d.rounded_rectangle([20, y, W//2-10, y+62], radius=6, fill=PANEL, outline=LINE_C, width=1)
    cx, cy = 40, y + 31
    d.ellipse([cx-13, cy-13, cx+13, cy+13], fill=ACCENT)
    d.text((cx, cy), str(i + 1), BG, font=fl, anchor="mm")
    d.text((62, y + 18), code, ACCENT, font=fc, anchor="lm")
    d.text((62, y + 44), desc, MUTED, font=fs, anchor="lm")

rb_y = 92 + 3 * 78 + 6
d.rounded_rectangle([20, rb_y, W//2-10, rb_y+40], radius=6, fill=PANEL, outline=AMBER, width=2)
d.text((240, rb_y+20), "t2 отримує СТАРЕ значення (до інкременту)", AMBER, font=fl, anchor="mm")

# ── RIGHT: PREFIX  t2 = ++t1 ──
d.text((720, 63), "Префіксний:  t2 = ++t1", ACCENT, font=fl, anchor="mm")
d.line([(W//2+10, 78), (W-20, 78)], LINE_C, width=1)

pre_steps = [
    ("t1 = operator++(t1)",   "t1 отримує новий об'єкт"),
    ("результат = t1",        "повернути НОВУ копію"),
]

for i, (code, desc) in enumerate(pre_steps):
    y = 92 + i * 78
    d.rounded_rectangle([W//2+10, y, W-20, y+62], radius=6, fill=PANEL, outline=LINE_C, width=1)
    cx, cy = W//2+30, y+31
    d.ellipse([cx-13, cy-13, cx+13, cy+13], fill=ACCENT)
    d.text((cx, cy), str(i + 1), BG, font=fl, anchor="mm")
    d.text((W//2+52, y+18), code, ACCENT, font=fc, anchor="lm")
    d.text((W//2+52, y+44), desc, MUTED, font=fs, anchor="lm")

rb_y2 = 92 + 2 * 78 + 6
d.rounded_rectangle([W//2+10, rb_y2, W-20, rb_y2+40], radius=6, fill=PANEL, outline=ACCENT, width=2)
d.text((720, rb_y2+20), "t2 отримує НОВЕ значення (після інкременту)", ACCENT, font=fl, anchor="mm")

# Bottom note
d.text((W//2, H-14),
       "operator++() визначається один раз — різницю між t++ і ++t реалізує компілятор",
       MUTED, font=fs, anchor="mm")

out = "lectures/_assets/08-02/increment-prefix-postfix.png"
img.save(out)
print(f"OK: {out}")
