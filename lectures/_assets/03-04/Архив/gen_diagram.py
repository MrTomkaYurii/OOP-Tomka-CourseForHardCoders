from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 860, 360
BG    = "#111413"
PANEL = "#191e1c"
LINE  = "#2c3531"
ACCENT= "#76c7ad"
TEXT  = "#e5e9e7"
MUTED = "#a1aaa6"
RED   = "#f97583"

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

img = Image.new("RGB", (W, H), hex2rgb(BG))
d = ImageDraw.Draw(img)

def try_font(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

font_b = try_font("C:/Windows/Fonts/consolab.ttf", 13)
font   = try_font("C:/Windows/Fonts/consola.ttf",  13)
font_s = try_font("C:/Windows/Fonts/consola.ttf",  11)

# Title
d.text((30, 22), "Struct — тип значення: копіювання створює незалежний об'єкт", font=font_b, fill=hex2rgb(TEXT))

# ---- LEFT side: struct ----
d.text((30, 58), "struct  (тип значення)", font=font_b, fill=hex2rgb(ACCENT))

# variable a box
ax, ay, aw, ah = 30, 85, 180, 60
d.rectangle([ax, ay, ax+aw, ay+ah], fill=hex2rgb(PANEL), outline=hex2rgb(ACCENT), width=1)
d.text((ax+8, ay+8),  "bp1", font=font_b, fill=hex2rgb(ACCENT))
d.text((ax+8, ay+28), "systolic  = 120", font=font_s, fill=hex2rgb(TEXT))
d.text((ax+8, ay+42), "diastolic =  80", font=font_s, fill=hex2rgb(TEXT))

# copy arrow down
d.line([(ax+aw//2, ay+ah), (ax+aw//2, ay+ah+30)], fill=hex2rgb(ACCENT), width=2)
cx, cy = ax+aw//2, ay+ah+30
for da in [0.4, -0.4]:
    ex = cx - 9*math.cos(math.pi/2 + da)
    ey = cy - 9*math.sin(math.pi/2 + da)
    d.line([(cx, cy), (int(ex), int(ey))], fill=hex2rgb(ACCENT), width=2)
d.text((ax+aw+6, ay+ah+8), "bp2 = bp1", font=font_s, fill=hex2rgb(TEXT))
d.text((ax+aw+6, ay+ah+22), "(копія значень)", font=font_s, fill=hex2rgb(MUTED))

# variable b box
bx, by = ax, ay+ah+50
d.rectangle([bx, by, bx+aw, by+ah], fill=hex2rgb(PANEL), outline=hex2rgb(ACCENT), width=1)
d.text((bx+8, by+8),  "bp2", font=font_b, fill=hex2rgb(ACCENT))
d.text((bx+8, by+28), "systolic  = 120", font=font_s, fill=hex2rgb(TEXT))
d.text((bx+8, by+42), "diastolic =  80", font=font_s, fill=hex2rgb(TEXT))

# after mutation — bp2.systolic = 140
mx, my = bx, by+ah+20
d.text((mx, my), "bp2.systolic = 140  →  bp1 НЕ змінюється", font=font_s, fill=hex2rgb(RED))

bx2, by2 = bx, my+20
d.rectangle([bx2, by2, bx2+aw, by2+ah], fill=hex2rgb(PANEL), outline=hex2rgb(RED), width=1)
d.text((bx2+8, by2+8),  "bp2 (після зміни)", font=font_b, fill=hex2rgb(RED))
d.text((bx2+8, by2+28), "systolic  = 140", font=font_s, fill=hex2rgb(RED))
d.text((bx2+8, by2+42), "diastolic =  80", font=font_s, fill=hex2rgb(TEXT))

ax2, ay2 = bx+aw+60, by2
d.rectangle([ax2, ay2, ax2+aw, ay2+ah], fill=hex2rgb(PANEL), outline=hex2rgb(ACCENT), width=1)
d.text((ax2+8, ay2+8),  "bp1 (не змінився)", font=font_b, fill=hex2rgb(ACCENT))
d.text((ax2+8, ay2+28), "systolic  = 120", font=font_s, fill=hex2rgb(TEXT))
d.text((ax2+8, ay2+42), "diastolic =  80", font=font_s, fill=hex2rgb(TEXT))

# ---- RIGHT side: class comparison ----
rx = W // 2 + 40
d.text((rx, 58), "class  (тип посилання)", font=font_b, fill=hex2rgb(MUTED))

# ref1 box (small — pointer)
r1x, r1y, r1w, r1h = rx, 85, 110, 40
d.rectangle([r1x, r1y, r1x+r1w, r1y+r1h], fill=hex2rgb(PANEL), outline=hex2rgb(MUTED), width=1)
d.text((r1x+8, r1y+12), "ref1 → ", font=font_s, fill=hex2rgb(MUTED))

# ref2 box
r2x, r2y = rx, 85+50
d.rectangle([r2x, r2y, r2x+r1w, r2y+r1h], fill=hex2rgb(PANEL), outline=hex2rgb(MUTED), width=1)
d.text((r2x+8, r2y+12), "ref2 → ", font=font_s, fill=hex2rgb(MUTED))

# heap object
hx, hy, hw, hh = rx+r1w+50, 85+10, 170, 70
d.rectangle([hx, hy, hx+hw, hy+hh], fill=hex2rgb(PANEL), outline=hex2rgb(MUTED), width=1)
d.text((hx+8, hy+6),  "Об'єкт у купі", font=font_s, fill=hex2rgb(MUTED))
d.text((hx+8, hy+24), "systolic  = 120", font=font_s, fill=hex2rgb(TEXT))
d.text((hx+8, hy+40), "diastolic =  80", font=font_s, fill=hex2rgb(TEXT))

# arrows from ref1 and ref2 to heap
d.line([(r1x+r1w, r1y+r1h//2), (hx, hy+20)], fill=hex2rgb(MUTED), width=1)
d.line([(r2x+r1w, r2y+r1h//2), (hx, hy+50)], fill=hex2rgb(MUTED), width=1)

d.text((rx, r2y+r1h+12), "ref2 = ref1 → обидві вказують", font=font_s, fill=hex2rgb(MUTED))
d.text((rx, r2y+r1h+26), "на один і той самий об'єкт", font=font_s, fill=hex2rgb(MUTED))
d.text((rx, r2y+r1h+44), "ref2.systolic = 140 → ref1 теж = 140!", font=font_s, fill=hex2rgb(RED))

out = os.path.join(os.path.dirname(__file__), "struct-copy-semantics.png")
img.save(out)
print("Saved:", out)
