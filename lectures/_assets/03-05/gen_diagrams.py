from PIL import Image, ImageDraw, ImageFont
import math, os

BG    = "#111413"
PANEL = "#191e1c"
LINE  = "#2c3531"
ACCENT= "#76c7ad"
TEXT  = "#e5e9e7"
MUTED = "#a1aaa6"
RED   = "#f97583"
BLUE  = "#79b8ff"

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def try_font(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

def arrow_down(d, x, y1, y2, color):
    d.line([(x, y1), (x, y2)], fill=hex2rgb(color), width=2)
    for da in [0.4, -0.4]:
        ex = x - 8*math.cos(math.pi/2 + da)
        ey = y2 - 8*math.sin(math.pi/2 + da)
        d.line([(x, y2), (int(ex), int(ey))], fill=hex2rgb(color), width=2)

def arrow_right(d, x1, x2, y, color):
    d.line([(x1, y), (x2, y)], fill=hex2rgb(color), width=2)
    for da in [0.4, -0.4]:
        ex = x2 - 8*math.cos(da)
        ey = y - 8*math.sin(da)
        d.line([(x2, y), (int(ex), int(ey))], fill=hex2rgb(color), width=2)

OUT_DIR = os.path.dirname(__file__)

# ─────────────────────────────────────────────
# Diagram 1: Stack vs Heap
# ─────────────────────────────────────────────
W, H = 860, 380
img = Image.new("RGB", (W, H), hex2rgb(BG))
d = ImageDraw.Draw(img)
font_b = try_font("C:/Windows/Fonts/consolab.ttf", 13)
font_s = try_font("C:/Windows/Fonts/consola.ttf",  11)
font_t = try_font("C:/Windows/Fonts/consola.ttf",  13)

d.text((30, 18), "Розміщення struct та class у пам'яті: стек та купа", font=font_b, fill=hex2rgb(TEXT))

# Stack column
sx, sy, sw, sh = 30, 55, 300, 290
d.rectangle([sx, sy, sx+sw, sy+sh], fill=hex2rgb(PANEL), outline=hex2rgb(LINE), width=1)
d.text((sx+sw//2 - 25, sy+6), "СТЕК", font=font_b, fill=hex2rgb(MUTED))

# bp (struct) in stack
bx, by, bw, bh = sx+14, sy+32, sw-28, 80
d.rectangle([bx, by, bx+bw, by+bh], fill=hex2rgb(BG), outline=hex2rgb(ACCENT), width=1)
d.text((bx+8, by+6),  "BloodPressure bp", font=font_b, fill=hex2rgb(ACCENT))
d.text((bx+8, by+26), "systolic  = 120", font=font_s, fill=hex2rgb(TEXT))
d.text((bx+8, by+42), "diastolic =  80", font=font_s, fill=hex2rgb(TEXT))
d.text((bx+8, by+60), "← значення прямо у стеку", font=font_s, fill=hex2rgb(MUTED))

# patient ref in stack
rx2, ry2, rw2, rh2 = sx+14, by+bh+18, sw-28, 50
d.rectangle([rx2, ry2, rx2+rw2, ry2+rh2], fill=hex2rgb(BG), outline=hex2rgb(BLUE), width=1)
d.text((rx2+8, ry2+6),  "Patient patient", font=font_b, fill=hex2rgb(BLUE))
d.text((rx2+8, ry2+26), "ref → 0x1A2B  (адреса в купі)", font=font_s, fill=hex2rgb(MUTED))

# Heap column
hx, hy, hw, hh = 480, 55, 350, 290
d.rectangle([hx, hy, hx+hw, hy+hh], fill=hex2rgb(PANEL), outline=hex2rgb(LINE), width=1)
d.text((hx+hw//2 - 25, hy+6), "КУПА", font=font_b, fill=hex2rgb(MUTED))

# patient object in heap
ox, oy, ow, oh = hx+14, hy+60, hw-28, 100
d.rectangle([ox, oy, ox+ow, oy+oh], fill=hex2rgb(BG), outline=hex2rgb(BLUE), width=1)
d.text((ox+8, oy+6),  "Patient  @0x1A2B", font=font_b, fill=hex2rgb(BLUE))
d.text((ox+8, oy+26), "name = \"Іван Петренко\"", font=font_s, fill=hex2rgb(TEXT))
d.text((ox+8, oy+42), "age  = 45", font=font_s, fill=hex2rgb(TEXT))
d.text((ox+8, oy+62), "← збирач сміття очищає", font=font_s, fill=hex2rgb(MUTED))
d.text((ox+8, oy+78), "   коли немає посилань", font=font_s, fill=hex2rgb(MUTED))

# arrow from stack ref → heap object
mid_ref_y = ry2 + rh2//2
arrow_right(d, rx2+rw2, hx, mid_ref_y, BLUE)

# note at bottom
d.text((30, sy+sh+12), "struct зберігає значення безпосередньо у стеку.  class — лише посилання у стеку, дані — у купі.", font=font_s, fill=hex2rgb(MUTED))

img.save(os.path.join(OUT_DIR, "stack-vs-heap.png"))
print("Saved: stack-vs-heap.png")

# ─────────────────────────────────────────────
# Diagram 2: Two structs sharing reference
# ─────────────────────────────────────────────
W2, H2 = 860, 360
img2 = Image.new("RGB", (W2, H2), hex2rgb(BG))
d2 = ImageDraw.Draw(img2)

d2.text((30, 18), "Копіювання struct з полем-посиланням: обидві вказують на один об'єкт у купі", font=font_b, fill=hex2rgb(TEXT))

# Stack
sx2, sy2, sw2, sh2 = 30, 55, 340, 265
d2.rectangle([sx2, sy2, sx2+sw2, sy2+sh2], fill=hex2rgb(PANEL), outline=hex2rgb(LINE), width=1)
d2.text((sx2+sw2//2 - 25, sy2+6), "СТЕК", font=font_b, fill=hex2rgb(MUTED))

def draw_visit(d, x, y, w, h, label, diag_label, ref_addr, border_color):
    d.rectangle([x, y, x+w, y+h], fill=hex2rgb(BG), outline=hex2rgb(border_color), width=1)
    d.text((x+8, y+6),  label, font=font_b, fill=hex2rgb(border_color))
    d.text((x+8, y+26), "date   = \"2026-05-21\"", font=font_s, fill=hex2rgb(TEXT))
    d.text((x+8, y+42), f"diagnosis → {ref_addr}", font=font_s, fill=hex2rgb(MUTED))

draw_visit(d2, sx2+14, sy2+30, sw2-28, 70, "visit1  (struct)", "", "0xBEEF", ACCENT)
draw_visit(d2, sx2+14, sy2+120, sw2-28, 70, "visit2 = visit1  (копія)", "", "0xBEEF", ACCENT)

d2.text((sx2+22, sy2+106), "visit2 = visit1 → int-поля скопійовані, ref — ні", font=font_s, fill=hex2rgb(MUTED))

# Heap
hx2, hy2, hw2, hh2 = 490, 55, 340, 200
d2.rectangle([hx2, hy2, hx2+hw2, hy2+hh2], fill=hex2rgb(PANEL), outline=hex2rgb(LINE), width=1)
d2.text((hx2+hw2//2 - 25, hy2+6), "КУПА", font=font_b, fill=hex2rgb(MUTED))

ox2, oy2, ow2, oh2 = hx2+14, hy2+50, hw2-28, 80
d2.rectangle([ox2, oy2, ox2+ow2, oy2+oh2], fill=hex2rgb(BG), outline=hex2rgb(RED), width=1)
d2.text((ox2+8, oy2+6),  "Diagnosis  @0xBEEF", font=font_b, fill=hex2rgb(RED))
d2.text((ox2+8, oy2+26), "title = \"Грип\"", font=font_s, fill=hex2rgb(TEXT))
d2.text((ox2+8, oy2+46), "← один об'єкт!", font=font_s, fill=hex2rgb(RED))
d2.text((ox2+8, oy2+62), "   зміна через visit2 → видно у visit1", font=font_s, fill=hex2rgb(RED))

# arrows from both structs to heap object
mid_heap_y = oy2 + oh2//2
arrow_right(d2, sx2+sw2, hx2, sy2+65, ACCENT)
arrow_right(d2, sx2+sw2, hx2, sy2+155, ACCENT)
d2.line([(hx2, sy2+65), (ox2, oy2+20)], fill=hex2rgb(ACCENT), width=1)
d2.line([(hx2, sy2+155), (ox2, oy2+50)], fill=hex2rgb(ACCENT), width=1)

d2.text((30, sy2+sh2+10), "Поле-посилання НЕ копіюється глибоко — обидві struct.diagnosis вказують на один Diagnosis у купі.", font=font_s, fill=hex2rgb(MUTED))

img2.save(os.path.join(OUT_DIR, "struct-shared-reference.png"))
print("Saved: struct-shared-reference.png")
