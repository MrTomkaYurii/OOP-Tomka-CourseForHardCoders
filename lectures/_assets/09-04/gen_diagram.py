from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)

W, H = 960, 360
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

d.text((W//2, 28), "Позиційний патерн: Deconstruct → кортеж → зіставлення", ACCENT, font=ft, anchor="mm")

# Step 1: Object
bx, by, bw, bh = 20, 55, 200, 90
d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=8, fill=PANEL, outline=ACCENT, width=2)
d.text((bx+bw//2, by+16), "Об'єкт", ACCENT, font=fb, anchor="mm")
d.line([(bx+10, by+30), (bx+bw-10, by+30)], LINE_C, width=1)
d.text((bx+14, by+46), "appointment", TEXT, font=fc, anchor="lm")
d.text((bx+14, by+65), "VitalSigns { 37.2, 88, 95 }", MUTED, font=fs, anchor="lm")

# Arrow 1
ax1 = bx+bw+8
ay1 = by+bh//2
d.line([(ax1, ay1), (ax1+55, ay1)], MUTED, width=2)
d.polygon([(ax1+55, ay1-6), (ax1+55, ay1+6), (ax1+68, ay1)], MUTED)
d.text((ax1+30, ay1-16), "компілятор", MUTED, font=fs, anchor="mm")
d.text((ax1+30, ay1),    "викликає", MUTED, font=fs, anchor="mm")
d.text((ax1+30, ay1+14), "Deconstruct", AMBER, font=fs, anchor="mm")

# Step 2: Deconstruct
dx, dy = ax1+70, 55
dw, dh = 280, 90
d.rounded_rectangle([dx, dy, dx+dw, dy+dh], radius=8, fill=PANEL, outline=AMBER, width=2)
d.text((dx+dw//2, dy+16), "Deconstruct", AMBER, font=fb, anchor="mm")
d.line([(dx+10, dy+30), (dx+dw-10, dy+30)], LINE_C, width=1)
d.text((dx+14, dy+46), "void Deconstruct(", TEXT, font=fc, anchor="lm")
d.text((dx+14, dy+64), "  out double t, out int p, out int s)", TEXT, font=fc, anchor="lm")

# Arrow 2
ax2 = dx+dw+8
ay2 = dy+dh//2
d.line([(ax2, ay2), (ax2+55, ay2)], MUTED, width=2)
d.polygon([(ax2+55, ay2-6), (ax2+55, ay2+6), (ax2+68, ay2)], MUTED)
d.text((ax2+30, ay2-10), "результат", MUTED, font=fs, anchor="mm")
d.text((ax2+30, ay2+6),  "— кортеж", MUTED, font=fs, anchor="mm")

# Step 3: Tuple
tx, ty = ax2+70, 55
tw, th = 200, 90
d.rounded_rectangle([tx, ty, tx+tw, ty+th], radius=8, fill=PANEL, outline=LINE_C, width=2)
d.text((tx+tw//2, ty+16), "Кортеж позицій", MUTED, font=fb, anchor="mm")
d.line([(tx+10, ty+30), (tx+tw-10, ty+30)], LINE_C, width=1)
d.text((tx+14, ty+46), "(37.2,  88,  95)", TEXT, font=fc, anchor="lm")
d.text((tx+14, ty+66), " [0]   [1]  [2]", ACCENT, font=fs, anchor="lm")

# Switch matching
sw_y = by+bh+30
d.line([(20, sw_y), (W-20, sw_y)], LINE_C, width=1)
d.text((W//2, sw_y+14), "Зіставлення позицій у switch", MUTED, font=fl, anchor="mm")

code_y = sw_y + 36
code_lines = [
    ("appointment switch",               TEXT),
    ("{",                                MUTED),
    ("    (> 38.5, > 100, _) => \"Жар + тахікардія\",", ACCENT),
    ("    (>= 36, <= 37, var p, _) => $\"Норма, пульс {p}\",", ACCENT),
    ("    (var t, var p, var s) => $\"{t} / {p} / {s}\",", MUTED),
    ("    _ => \"Невизначено\"",          MUTED),
    ("}",                                MUTED),
]
for i, (line, col) in enumerate(code_lines):
    d.text((30, code_y + i*26), line, col, font=fc, anchor="lm")

out = "lectures/_assets/09-04/positional-pattern-flow.png"
img.save(out)
print(f"OK: {out}")
