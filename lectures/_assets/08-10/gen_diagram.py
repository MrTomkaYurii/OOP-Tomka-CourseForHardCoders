from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)

W, H = 1000, 480
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
d.text((W//2, 28), "Record: один рядок коду → що генерує компілятор", ACCENT, font=ft, anchor="mm")

# ── LEFT: one line of code ──
lx, ly, lw, lh = 20, 55, 285, 70
d.rounded_rectangle([lx, ly, lx+lw, ly+lh], radius=8, fill=PANEL, outline=ACCENT, width=2)
d.text((lx+lw//2, ly+16), "Код розробника", ACCENT, font=fb, anchor="mm")
d.line([(lx+10, ly+30), (lx+lw-10, ly+30)], LINE_C, width=1)
d.text((lx+14, ly+50), "record Patient(string Name, int Age);", TEXT, font=fc, anchor="lm")

# Arrow
arr_x = lx+lw+14
arr_y = ly+lh//2+10
d.line([(arr_x, arr_y), (arr_x+46, arr_y)], MUTED, width=2)
d.polygon([(arr_x+46, arr_y-6), (arr_x+46, arr_y+6), (arr_x+60, arr_y)], MUTED)
d.text((arr_x+30, arr_y-14), "компілятор", MUTED, font=fs, anchor="mm")

# ── RIGHT: generated members ──
rx = arr_x+64
ry = 55
rw = W - rx - 18
rh = 390
d.rounded_rectangle([rx, ry, rx+rw, ry+rh], radius=8, fill=PANEL, outline=AMBER, width=2)
d.text((rx+rw//2, ry+16), "Згенеровані члени (спрощено)", AMBER, font=fb, anchor="mm")
d.line([(rx+10, ry+30), (rx+rw-10, ry+30)], LINE_C, width=1)

gen = [
    ("// Конструктор",                           MUTED),
    ("Patient(string Name, int Age)",             TEXT),
    ("",                                          TEXT),
    ("// init-властивості (immutable after new)", MUTED),
    ("public string Name { get; init; }",         ACCENT),
    ("public int    Age  { get; init; }",         ACCENT),
    ("",                                          TEXT),
    ("// Структурна рівність",                   MUTED),
    ("bool Equals(Patient other)  // за значеннями", TEXT),
    ("bool operator ==(Patient, Patient)",        TEXT),
    ("int  GetHashCode()",                        TEXT),
    ("",                                          TEXT),
    ("// Виведення стану",                        MUTED),
    ('string ToString()  // "Patient { Name=..., Age=... }"', TEXT),
    ("",                                          TEXT),
    ("// Клонування + зміна",                    MUTED),
    ("Patient <Clone>()   // використовує with", TEXT),
    ("",                                          TEXT),
    ("// Декомпозиція",                           MUTED),
    ("void Deconstruct(out string Name, out int Age)", TEXT),
]
for i, (line, col) in enumerate(gen):
    d.text((rx+14, ry+40+i*17), line, col, font=fc, anchor="lm")

# ── BOTTOM: key insight ──
note_y = ry + rh + 12
d.text((W//2, note_y),
    "Один рядок позиційного record замінює ~50 рядків класу з усіма цими членами.",
    MUTED, font=fs, anchor="mm")
d.text((W//2, note_y+20),
    "init = властивість можна встановити лише в конструкторі або ініціалізаторі об'єкта.",
    ACCENT, font=fs, anchor="mm")

out = "lectures/_assets/08-10/record-generated-members.png"
img.save(out)
print(f"OK: {out}")
