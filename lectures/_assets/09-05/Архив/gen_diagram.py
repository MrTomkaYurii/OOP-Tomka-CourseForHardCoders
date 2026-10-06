from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)
RED    = (190, 80, 80)

W, H = 960, 400
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

d.text((W//2, 28), "Реляційний патерн: температура тіла — діапазони та рішення", ACCENT, font=ft, anchor="mm")

# ── Number line ──
line_y = 95
line_x0, line_x1 = 40, W-40
d.line([(line_x0, line_y), (line_x1, line_y)], TEXT, width=2)

# Arrow at end
d.polygon([(line_x1, line_y-5), (line_x1, line_y+5), (line_x1+12, line_y)], TEXT)
d.text((line_x1+18, line_y), "°C", TEXT, font=fs, anchor="lm")

# Tick marks and labels
ticks = [35, 36, 37, 37.5, 38.5, 39.5, 41]
tick_labels = ["35", "36", "37", "37.5", "38.5", "39.5", "41"]
scale_min, scale_max = 34.5, 41.5
scale_w = line_x1 - line_x0

def to_x(val):
    return int(line_x0 + (val - scale_min) / (scale_max - scale_min) * scale_w)

for val, lbl in zip(ticks, tick_labels):
    tx = to_x(val)
    d.line([(tx, line_y-8), (tx, line_y+8)], MUTED, width=1)
    d.text((tx, line_y+18), lbl, MUTED, font=fs, anchor="mm")

# Color zones
zones = [
    (35.0, 36.0, (60, 80, 190),   "Гіпотермія"),
    (36.0, 37.0, (60, 150, 80),   "Норма"),
    (37.0, 37.5, (130, 160, 60),  "Субфебрильна"),
    (37.5, 38.5, (200, 140, 40),  "Жар"),
    (38.5, 39.5, (200, 100, 40),  "Висока"),
    (39.5, 41.0, (190, 60, 60),   "Критично"),
]
for v_start, v_end, color, label in zones:
    x_start = to_x(v_start)
    x_end   = to_x(v_end)
    d.rectangle([x_start, line_y-30, x_end, line_y-2], fill=color)
    mid = (x_start + x_end) // 2
    d.text((mid, line_y-16), label, TEXT, font=fs, anchor="mm")

# ── Switch code ──
code_y = line_y + 50
d.text((W//2, code_y), "temperature switch — реляційні патерни", MUTED, font=fs, anchor="mm")
code_y += 22
d.rounded_rectangle([20, code_y, W-20, code_y+180], radius=8, fill=PANEL, outline=LINE_C, width=1)
arms = [
    ("< 35.0",                      "\"Гіпотермія — термінова допомога\"",   RED),
    (">= 36.0 and <= 37.0",         "\"Нормальна температура\"",             ACCENT),
    ("> 37.0 and < 37.5",           "\"Субфебрильна — спостереження\"",      AMBER),
    (">= 37.5 and < 38.5",          "\"Жар — жарознижуюче\"",                AMBER),
    (">= 38.5 and < 39.5",          "\"Висока — термінова оцінка\"",         RED),
    (">= 39.5",                     "\"Критична — госпіталізація\"",          RED),
]
for i, (pattern, result, col) in enumerate(arms):
    d.text((36, code_y + 12 + i*26), pattern, col, font=fc, anchor="lm")
    d.text((370, code_y + 12 + i*26), "=> " + result, MUTED, font=fc, anchor="lm")

out = "lectures/_assets/09-05/relational-pattern-ranges.png"
img.save(out)
print(f"OK: {out}")
