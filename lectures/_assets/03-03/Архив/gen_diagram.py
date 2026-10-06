from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 860, 320
BG    = "#111413"
PANEL = "#191e1c"
LINE  = "#2c3531"
ACCENT= "#76c7ad"
TEXT  = "#e5e9e7"
MUTED = "#a1aaa6"

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

img = Image.new("RGB", (W, H), hex2rgb(BG))
d = ImageDraw.Draw(img)

def try_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

font_b = try_font("C:/Windows/Fonts/consolab.ttf", 13)
font   = try_font("C:/Windows/Fonts/consola.ttf",  13)
font_s = try_font("C:/Windows/Fonts/consola.ttf",  11)

# Left box — top-level
lx, ly, lw, lh = 30, 70, 310, 180
d.rectangle([lx, ly, lx+lw, ly+lh], fill=hex2rgb(PANEL), outline=hex2rgb(ACCENT), width=1)
d.text((lx+10, ly+10), "// top-level statements", font=font_s, fill=hex2rgb(MUTED))
left_lines = [
    ("using System;", TEXT),
    ("", TEXT),
    ("Patient p = new(\"Іван\", 45);", ACCENT),
    ("p.PrintInfo();", ACCENT),
    ("", TEXT),
    ("class Patient {", TEXT),
    ("  ...", MUTED),
    ("}", TEXT),
]
for i, (line, color) in enumerate(left_lines):
    d.text((lx+10, ly+32+i*17), line, font=font_s, fill=hex2rgb(color))

# Label under left
d.text((lx + lw//2 - 60, ly+lh+8), "Програма верхнього рівня", font=font_s, fill=hex2rgb(MUTED))

# Arrow
ax1, ay = lx+lw+10, ly+lh//2
ax2 = W - 310 - 10
d.line([(ax1, ay), (ax2, ay)], fill=hex2rgb(ACCENT), width=2)
size = 9
for da in [0.4, -0.4]:
    ex = ax2 - size * math.cos(da)
    ey = ay  - size * math.sin(da)
    d.line([(ax2, ay), (int(ex), int(ey))], fill=hex2rgb(ACCENT), width=2)
mid_x = (ax1 + ax2) // 2
d.text((mid_x - 30, ay - 18), "компілятор", font=font_s, fill=hex2rgb(TEXT))

# Right box — explicit class Program
rx, ry, rw, rh = W-310, 70, 300, 200
d.rectangle([rx, ry, rx+rw, ry+rh], fill=hex2rgb(PANEL), outline=hex2rgb(LINE), width=1)
d.text((rx+10, ry+10), "// еквівалентний код", font=font_s, fill=hex2rgb(MUTED))
right_lines = [
    ("class Program {", TEXT),
    ("  static void Main(", TEXT),
    ("      string[] args) {", TEXT),
    ("    Patient p =", ACCENT),
    ("      new(\"Іван\", 45);", ACCENT),
    ("    p.PrintInfo();", ACCENT),
    ("  }", TEXT),
    ("}", TEXT),
]
for i, (line, color) in enumerate(right_lines):
    d.text((rx+10, ry+32+i*18), line, font=font_s, fill=hex2rgb(color))

d.text((rx + rw//2 - 70, ry+rh+8), "Явне визначення Main", font=font_s, fill=hex2rgb(MUTED))

# Title
d.text((30, 22), "Top-level statements → компілятор генерує клас Program і метод Main", font=font_b, fill=hex2rgb(TEXT))

out = os.path.join(os.path.dirname(__file__), "toplevel-to-main.png")
img.save(out)
print("Saved:", out)
