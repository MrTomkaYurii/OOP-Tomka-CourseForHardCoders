from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 860, 340
BG    = "#111413"
PANEL = "#191e1c"
LINE  = "#2c3531"
ACCENT= "#76c7ad"
TEXT  = "#e5e9e7"
MUTED = "#a1aaa6"

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

img = Image.new("RGB", (W, H), hex2rgb(BG))
d = ImageDraw.Draw(img)

def try_font(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

font_b = try_font("C:/Windows/Fonts/consolab.ttf", 13)
font   = try_font("C:/Windows/Fonts/consola.ttf",  13)
font_s = try_font("C:/Windows/Fonts/consola.ttf",  11)

boxes = [
    {"x": 30,  "lines": ["Patient()", ""], "sub": ["name = \"Невідомий\"", "age = 0"]},
    {"x": 300, "lines": ["Patient(string name)", ""], "sub": ["name = name", "age = 0"]},
    {"x": 570, "lines": ["Patient(string name,", "         int age)"], "sub": ["this.name = name", "this.age  = age"]},
]

box_w, box_h = 240, 100
box_y = 120

for b in boxes:
    x = b["x"]
    d.rectangle([x, box_y, x+box_w, box_y+box_h], fill=hex2rgb(PANEL), outline=hex2rgb(ACCENT), width=1)
    for i, line in enumerate(b["lines"]):
        d.text((x+10, box_y+10+i*16), line, font=font_b, fill=hex2rgb(ACCENT))
    for i, line in enumerate(b["sub"]):
        d.text((x+10, box_y+52+i*16), line, font=font_s, fill=hex2rgb(MUTED))

def arrow(x1, y1, x2, y2):
    color = hex2rgb(ACCENT)
    d.line([(x1,y1),(x2,y2)], fill=color, width=2)
    angle = math.atan2(y2-y1, x2-x1)
    size = 9
    for da in [0.4, -0.4]:
        ax = x2 - size*math.cos(angle+da)
        ay = y2 - size*math.sin(angle+da)
        d.line([(x2,y2),(int(ax),int(ay))], fill=color, width=2)

mid_y = box_y + box_h // 2

# box0 -> box1
arrow(boxes[0]["x"]+box_w, mid_y, boxes[1]["x"], mid_y)
d.text((boxes[0]["x"]+box_w+4, mid_y-18), ": this(\"Невідомий\", 0)", font=font_s, fill=hex2rgb(TEXT))

# box1 -> box2
arrow(boxes[1]["x"]+box_w, mid_y, boxes[2]["x"], mid_y)
d.text((boxes[1]["x"]+box_w+4, mid_y-18), ": this(name, 0)", font=font_s, fill=hex2rgb(TEXT))

# title
title = "Ланцюжок виклику конструкторів через this()"
d.text((30, 40), title, font=font_b, fill=hex2rgb(TEXT))

# bottom note
d.text((30, box_y+box_h+20), "Виконання — справа наліво: спочатку найповніший конструктор, потім попередні.", font=font_s, fill=hex2rgb(MUTED))

out = os.path.join(os.path.dirname(__file__), "constructor-chain.png")
img.save(out)
print("Saved:", out)
