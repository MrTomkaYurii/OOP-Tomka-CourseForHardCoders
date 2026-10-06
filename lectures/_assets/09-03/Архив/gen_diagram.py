from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)

W, H = 960, 380
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
d.text((W//2, 28), "Патерн кортежів: двовимірне зіставлення", ACCENT, font=ft, anchor="mm")

# ── Matrix ──
d.text((W//2, 54), "(спеціалізація, зміна) switch — кожна комбінація → окремий arm", MUTED, font=fs, anchor="mm")

# Draw matrix: rows = shift (day/night), cols = specialty
rows = ["\"День\"", "\"Ніч\"",  "\"_\" (будь-яка)"]
cols = ["\"Кардіологія\"", "\"Хірургія\"", "\"_\" (будь-яка)"]
results = [
    ["Кардіо / День",   "Хірург / День",   "Відділення / День"],
    ["Кардіо / Ніч",    "Хірург / Ніч",    "Відділення / Ніч"],
    ["Кардіо / ?",      "Хірург / ?",       "— загальний"],
]

cx0, cy0 = 120, 80
cw, rh = 210, 52

# Column headers
for j, col in enumerate(cols):
    cx = cx0 + j * cw + cw//2
    d.text((cx, cy0 - 16), col, AMBER, font=fs, anchor="mm")

# Row headers + cells
for i, row in enumerate(rows):
    ry = cy0 + i * rh
    d.text((cx0 - 10, ry + rh//2), row, AMBER, font=fs, anchor="rm")
    for j, result in enumerate(results[i]):
        rx = cx0 + j * cw
        col = ACCENT if i < 2 and j < 2 else (TEXT if i < 2 else MUTED)
        outline = ACCENT if i == 2 or j == 2 else LINE_C
        d.rounded_rectangle([rx+4, ry+4, rx+cw-4, ry+rh-4], radius=4, fill=PANEL, outline=outline, width=1)
        d.text((rx + cw//2, ry + rh//2), result, col, font=fs, anchor="mm")

# Legend
leg_y = cy0 + 3 * rh + 20
d.text((cx0, leg_y), "_ = discard: позиція не важлива, збігається з будь-яким значенням", MUTED, font=fs, anchor="lm")

# ── Right: code ──
code_x = cx0 + 3 * cw + 30
code_y = 72
d.rounded_rectangle([code_x, code_y, W-20, code_y+240], radius=8, fill=PANEL, outline=LINE_C, width=1)
code_lines = [
    ("(specialty, shift) switch", TEXT),
    ("{",                          MUTED),
    ('  ("Кардіологія","День") =>', TEXT),
    ('      "Кардіо-денна зміна",', ACCENT),
    ('  ("Кардіологія","Ніч")  =>', TEXT),
    ('      "Кардіо-нічна",',       ACCENT),
    ('  ("Хірургія",   _)      =>', TEXT),
    ('      "Хірург будь-яка",',    ACCENT),
    ('  (_,            "Ніч")  =>', TEXT),
    ('      "Нічна зміна",',        ACCENT),
    ('  _                      =>', TEXT),
    ('      "Загальний",',          MUTED),
    ("};",                          MUTED),
]
for i, (line, col) in enumerate(code_lines):
    d.text((code_x+12, code_y+16+i*17), line, col, font=fc, anchor="lm")

out = "lectures/_assets/09-03/tuple-pattern-matrix.png"
img.save(out)
print(f"OK: {out}")
