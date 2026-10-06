"""
Generate diagrams for lecture 04-03 (Virtual methods).
NEVER overwrites existing files.
"""
from PIL import Image, ImageDraw, ImageFont
import os

BG     = "#111413"
ACCENT = "#76c7ad"
TEXT   = "#e5e9e7"
MUTED  = "#a1aaa6"
LINE   = "#2c3531"
PANEL  = "#191e1c"
YELLOW = "#c7b876"
RED    = "#e07070"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def save_if_new(img, name):
    path = os.path.join(SCRIPT_DIR, name)
    if os.path.exists(path):
        print(f"SKIP (exists): {name}")
        return
    img.save(path)
    print(f"CREATED: {name}")

def try_font(size):
    for c in ["C:/Windows/Fonts/consola.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def try_bold(size):
    for c in ["C:/Windows/Fonts/consolab.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"]:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return try_font(size)

# ─────────────────────────────────────────────────────────────
# Diagram 1: Virtual dispatch — runtime method resolution
# ─────────────────────────────────────────────────────────────
def make_dispatch():
    W, H = 820, 460
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)
    ft = try_bold(17)
    fb = try_font(13)
    fs = try_font(12)
    fbold = try_bold(13)

    d.text((W//2, 24), "Virtual dispatch — виклик за реальним типом об'єкта",
           font=ft, fill=hex_to_rgb(ACCENT), anchor="mm")

    # Code block on left
    code_x, code_y = 30, 55
    code_w, code_h = 330, 130
    d.rounded_rectangle([code_x, code_y, code_x+code_w, code_y+code_h],
                        radius=7, fill=hex_to_rgb(PANEL), outline=hex_to_rgb(LINE), width=1)
    code_lines = [
        "Person[] staff = {",
        "  new Person(...),",
        "  new Patient(...),",
        "  new Doctor(...),",
        "};",
        "foreach (var p in staff)",
        "  p.Print(); // який метод?",
    ]
    for i, line in enumerate(code_lines):
        color = ACCENT if "p.Print()" in line else TEXT
        d.text((code_x+12, code_y+10+i*16), line, font=fb, fill=hex_to_rgb(color))

    # Arrow right from code to dispatch boxes
    ax1, ay1 = code_x+code_w, code_y+code_h//2
    ax2, ay2 = code_x+code_w+50, code_y+code_h//2
    d.line([(ax1, ay1), (ax2, ay2)], fill=hex_to_rgb(MUTED), width=2)
    d.text((ax1+5, ay1-14), "runtime", font=fs, fill=hex_to_rgb(MUTED))
    d.text((ax1+5, ay1+2), "тип?", font=fs, fill=hex_to_rgb(MUTED))

    # Three dispatch boxes
    boxes = [
        ("Person", "Person.Print()", MUTED,  170),
        ("Patient", "Patient.Print()", YELLOW, 270),
        ("Doctor",  "Doctor.Print()",  ACCENT, 370),
    ]
    bx = ax2+50
    for label, method, color, by in boxes:
        bw, bh = 290, 52
        d.rounded_rectangle([bx+3,by+3,bx+bw+3,by+bh+3],radius=7,fill=hex_to_rgb(LINE))
        d.rounded_rectangle([bx,by,bx+bw,by+bh],radius=7,
                            fill=hex_to_rgb(PANEL), outline=hex_to_rgb(color), width=2)
        d.rounded_rectangle([bx+2,by+2,bx+100,by+bh-2],radius=6,fill=hex_to_rgb(color))
        d.text((bx+51, by+bh//2), label, font=fbold, fill=hex_to_rgb(BG), anchor="mm")
        d.text((bx+195, by+bh//2), method, font=fb, fill=hex_to_rgb(color), anchor="mm")
        # connector from dispatch point
        d.line([(ax2, ay1), (bx, by+bh//2)], fill=hex_to_rgb(LINE), width=1)

    # Key label
    d.text((W//2, 435),
           "Змінна Person — але викликається метод реального типу об'єкта",
           font=fs, fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "virtual-dispatch.png")

# ─────────────────────────────────────────────────────────────
# Diagram 2: virtual → override chain
# ─────────────────────────────────────────────────────────────
def make_override_chain():
    W, H = 720, 320
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)
    ft = try_bold(17)
    fb = try_font(13)
    fs = try_font(12)

    d.text((W//2, 22), "virtual → override: ланцюжок перевизначень",
           font=ft, fill=hex_to_rgb(ACCENT), anchor="mm")

    classes = [
        ("Person",      "virtual void Print()",          MUTED,   80),
        ("Patient",     "override void Print()",          YELLOW, 175),
        ("Inpatient",   "override void Print()",          ACCENT, 270),
    ]

    bw, bh = 380, 55
    cx = W//2
    prev_y = None
    for name, method, color, by in classes:
        bx = cx - bw//2
        d.rounded_rectangle([bx+3,by+3,bx+bw+3,by+bh+3],radius=7,fill=hex_to_rgb(LINE))
        d.rounded_rectangle([bx,by,bx+bw,by+bh],radius=7,
                            fill=hex_to_rgb(PANEL), outline=hex_to_rgb(color), width=2)
        d.rounded_rectangle([bx+2,by+2,bx+130,by+bh-2],radius=6,fill=hex_to_rgb(color))
        d.text((bx+66, by+bh//2), name, font=try_bold(14), fill=hex_to_rgb(BG), anchor="mm")
        d.text((bx+265, by+bh//2), method, font=fb, fill=hex_to_rgb(color), anchor="mm")
        if prev_y is not None:
            d.line([(cx, prev_y), (cx, by)], fill=hex_to_rgb(MUTED), width=2)
            d.polygon([(cx, by), (cx-7, by-14), (cx+7, by-14)], fill=hex_to_rgb(MUTED))
        prev_y = by + bh

    d.text((W//2, 300), "Кожен рівень може перевизначати або використовувати base.Print()",
           font=fs, fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "override-chain.png")

make_dispatch()
make_override_chain()
print("Done.")
