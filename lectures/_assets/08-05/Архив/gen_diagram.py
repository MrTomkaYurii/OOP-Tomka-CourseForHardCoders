from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)
RED    = (200, 90, 90)

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
fb = font("arialbd.ttf", 13)

# ── TITLE ──
d.text((W//2, 28), "ref-змінна: псевдонім vs копія", ACCENT, font=ft, anchor="mm")
d.line([(W//2, 48), (W//2, H-20)], LINE_C, width=1)

# ── LEFT: Regular variable (copy) ──
d.text((250, 60), "Звичайна змінна — КОПІЯ значення", AMBER, font=fb, anchor="mm")

# Code
code_lines_left = [
    ("double pulse = 72.0;", TEXT),
    ("double copy = pulse;", AMBER),
    ("copy = 90.0;", AMBER),
    ("// pulse = 72.0  (не змінилась)", MUTED),
]
for i, (line, col) in enumerate(code_lines_left):
    d.text((35, 82 + i*24), line, col, font=fc, anchor="lm")

# Memory model
mem_y = 192
d.text((250, mem_y), "Модель пам'яті:", MUTED, font=fs, anchor="mm")

# Variable: pulse
d.rounded_rectangle([50, mem_y+16, 200, mem_y+52], radius=4, fill=PANEL, outline=ACCENT, width=2)
d.text((125, mem_y+34), "pulse", ACCENT, font=fs, anchor="mm")
d.text((125, mem_y+46), "72.0", TEXT, font=fc, anchor="mm")

# Variable: copy
d.rounded_rectangle([50, mem_y+70, 200, mem_y+106], radius=4, fill=PANEL, outline=AMBER, width=2)
d.text((125, mem_y+88), "copy", AMBER, font=fs, anchor="mm")
d.text((125, mem_y+100), "90.0", TEXT, font=fc, anchor="mm")

# Memory cells
d.rounded_rectangle([250, mem_y+16, 390, mem_y+52], radius=4, fill=PANEL, outline=LINE_C, width=1)
d.text((320, mem_y+26), "0x1A4C", MUTED, font=fs, anchor="mm")
d.text((320, mem_y+42), "72.0", TEXT, font=fc, anchor="mm")

d.rounded_rectangle([250, mem_y+70, 390, mem_y+106], radius=4, fill=PANEL, outline=LINE_C, width=1)
d.text((320, mem_y+80), "0x1A50", MUTED, font=fs, anchor="mm")
d.text((320, mem_y+96), "90.0", TEXT, font=fc, anchor="mm")

# Arrows
d.line([(205, mem_y+34), (245, mem_y+34)], ACCENT, width=2)
d.polygon([(245, mem_y+28), (245, mem_y+40), (258, mem_y+34)], ACCENT)

d.line([(205, mem_y+88), (245, mem_y+88)], AMBER, width=2)
d.polygon([(245, mem_y+82), (245, mem_y+94), (258, mem_y+88)], AMBER)

# Label
d.text((220, mem_y+130), "← два різних осередки пам'яті", MUTED, font=fs, anchor="mm")

# ── RIGHT: Ref variable ──
d.text((750, 60), "ref-змінна — ПСЕВДОНІМ (alias)", ACCENT, font=fb, anchor="mm")

code_lines_right = [
    ("double pulse = 72.0;", TEXT),
    ("ref double r = ref pulse;", ACCENT),
    ("r = 90.0;", ACCENT),
    ("// pulse = 90.0  (змінилась!)", MUTED),
]
for i, (line, col) in enumerate(code_lines_right):
    d.text((535, 82 + i*24), line, col, font=fc, anchor="lm")

# Memory model
d.text((750, mem_y), "Модель пам'яті:", MUTED, font=fs, anchor="mm")

# Variable: pulse
d.rounded_rectangle([550, mem_y+16, 700, mem_y+52], radius=4, fill=PANEL, outline=ACCENT, width=2)
d.text((625, mem_y+34), "pulse", ACCENT, font=fs, anchor="mm")
d.text((625, mem_y+46), "90.0", TEXT, font=fc, anchor="mm")

# ref r
d.rounded_rectangle([550, mem_y+70, 700, mem_y+106], radius=4, fill=PANEL, outline=ACCENT, width=2)
d.text((625, mem_y+88), "r  (ref)", ACCENT, font=fs, anchor="mm")
d.text((625, mem_y+100), "→ псевдонім", MUTED, font=fs, anchor="mm")

# Memory cell (one)
d.rounded_rectangle([750, mem_y+16, 890, mem_y+52], radius=4, fill=PANEL, outline=ACCENT, width=2)
d.text((820, mem_y+26), "0x1A4C", MUTED, font=fs, anchor="mm")
d.text((820, mem_y+42), "90.0", ACCENT, font=fc, anchor="mm")

# Arrows — both pointing to same cell
d.line([(705, mem_y+34), (745, mem_y+34)], ACCENT, width=2)
d.polygon([(745, mem_y+28), (745, mem_y+40), (758, mem_y+34)], ACCENT)

d.line([(705, mem_y+88), (820, mem_y+88)], ACCENT, width=1)
d.line([(820, mem_y+88), (820, mem_y+56)], ACCENT, width=1)
d.polygon([(814, mem_y+56), (826, mem_y+56), (820, mem_y+44)], ACCENT)

# Label
d.text((720, mem_y+130), "← один осередок, два імені", ACCENT, font=fs, anchor="mm")

# ── BOTTOM ──
d.text((W//2, H-14),
    "ref r = ref pulse   означає: r — це інше ім'я для тієї самої ділянки пам'яті, що й pulse",
    MUTED, font=fs, anchor="mm")

out = "lectures/_assets/08-05/ref-variable-memory.png"
img.save(out)
print(f"OK: {out}")
