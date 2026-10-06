from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)

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

d.text((W//2, 28), "Патерн списків: синтаксис елементів та slice", ACCENT, font=ft, anchor="mm")

# Array visual: [72, 88, 95, 101, 88]
arr_y = 65
arr_vals = ["72", "88", "95", "101", "88"]
cell_w, cell_h = 80, 44
arr_x0 = (W - len(arr_vals)*cell_w) // 2

for i, val in enumerate(arr_vals):
    cx = arr_x0 + i * cell_w
    d.rounded_rectangle([cx+2, arr_y, cx+cell_w-2, arr_y+cell_h], radius=4, fill=PANEL, outline=ACCENT, width=1)
    d.text((cx+cell_w//2, arr_y+16), val, TEXT, font=fc, anchor="mm")
    d.text((cx+cell_w//2, arr_y+32), f"[{i}]", MUTED, font=fs, anchor="mm")

# Pattern rows
patterns_y = arr_y + cell_h + 22
patterns = [
    ("[_, .., _]",           "≥2 елементи: перший і останній — будь-які",    ACCENT),
    ("[var first, .., var last]", "захопити перший і останній у змінні",     AMBER),
    ("[72, ..]",             "масив що починається з 72",                     ACCENT),
    ("[.., 88]",             "масив що закінчується на 88",                   ACCENT),
    ("[72, .. var middle, 88]","перший=72, останній=88, середину в middle",   AMBER),
    ("[]",                   "порожній масив",                                MUTED),
    ("[..]",                 "будь-який масив (≥0 елементів)",               MUTED),
]

for i, (pattern, desc, col) in enumerate(patterns):
    y = patterns_y + i * 34
    d.rounded_rectangle([20, y, W-20, y+28], radius=4, fill=PANEL, outline=LINE_C, width=1)
    d.text((34, y+14), pattern, col, font=fc, anchor="lm")
    bb = d.textbbox((34, y+14), pattern, font=fc, anchor="lm")
    d.text((bb[2]+20, y+14), "→  " + desc, MUTED, font=fs, anchor="lm")

out = "lectures/_assets/09-06/list-pattern-syntax.png"
img.save(out)
print(f"OK: {out}")
