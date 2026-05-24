"""
Generate diagrams for lecture 04-02 (Type conversions).
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

# ─────────────────────────────────────────────────────────────────
# Diagram 1: Type hierarchy (Object → Person → Patient | Doctor)
# ─────────────────────────────────────────────────────────────────
def make_hierarchy():
    W, H = 760, 420
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)
    ft = try_bold(17); fb = try_font(13); fs = try_font(12)

    d.text((W//2, 22), "Ієрархія типів у C#", font=ft,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    def box(x, y, w, h, label, sub, color=ACCENT):
        d.rounded_rectangle([x+3,y+3,x+w+3,y+h+3], radius=7, fill=hex_to_rgb(LINE))
        d.rounded_rectangle([x,y,x+w,y+h], radius=7, fill=hex_to_rgb(PANEL),
                            outline=hex_to_rgb(color), width=2)
        d.rounded_rectangle([x+2,y+2,x+w-2,y+26], radius=6,
                            fill=hex_to_rgb(color))
        d.text((x+w//2, y+14), label, font=try_bold(14),
               fill=hex_to_rgb(BG), anchor="mm")
        if sub:
            d.text((x+w//2, y+h//2+8), sub, font=fb,
                   fill=hex_to_rgb(MUTED), anchor="mm")

    def arrow(x1,y1,x2,y2, label=""):
        d.line([(x1,y1),(x2,y2)], fill=hex_to_rgb(MUTED), width=2)
        dx,dy = x2-x1, y2-y1
        import math
        length = math.sqrt(dx*dx+dy*dy)
        ux,uy = dx/length, dy/length
        px,py = -uy, ux
        size = 8
        d.polygon([(x2,y2),(x2-ux*size+px*4,y2-uy*size+py*4),
                           (x2-ux*size-px*4,y2-uy*size-py*4)],
                  fill=hex_to_rgb(MUTED))
        if label:
            mx,my = (x1+x2)//2,(y1+y2)//2
            d.text((mx+14,my), label, font=fs, fill=hex_to_rgb(MUTED))

    # Object
    bw,bh = 220,60
    ox,oy = W//2-bw//2, 50
    box(ox,oy,bw,bh,"System.Object","базовий для всіх", MUTED)

    # Person
    pw,ph = 260,70
    px,py = W//2-pw//2, 170
    box(px,py,pw,ph,"Person","Name, Age\nPrint()", ACCENT)

    # Patient
    dw,dh = 220,70
    ptx,pty = 130, 310
    box(ptx,pty,dw,dh,"Patient","Diagnosis\nPrintInfo()", YELLOW)

    # Doctor
    drx,dry = 420, 310
    box(drx,dry,dw,dh,"Doctor","Specialization\nPrintInfo()", YELLOW)

    # Arrows
    arrow(ox+bw//2, oy+bh, px+pw//2, py)
    arrow(px+pw//2, py+ph, ptx+dw//2, pty)
    arrow(px+pw//2, py+ph, drx+dw//2, dry)

    # Labels
    d.text((W//2+6, oy+bh+10), "неявно", font=fs, fill=hex_to_rgb(MUTED))
    d.text((ptx-70, pty+35), "is-a", font=fs, fill=hex_to_rgb(MUTED))
    d.text((drx+dw+6, dry+35), "is-a", font=fs, fill=hex_to_rgb(MUTED))

    save_if_new(img, "type-hierarchy.png")

# ─────────────────────────────────────────────────────────────────
# Diagram 2: Upcasting vs Downcasting
# ─────────────────────────────────────────────────────────────────
def make_casting():
    W, H = 720, 400
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)
    ft = try_bold(17); fb = try_font(13); fs = try_font(12)

    d.text((W//2, 22), "Upcasting та Downcasting", font=ft,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    def box(x,y,w,h,label,color):
        d.rounded_rectangle([x+3,y+3,x+w+3,y+h+3],radius=7,fill=hex_to_rgb(LINE))
        d.rounded_rectangle([x,y,x+w,y+h],radius=7,fill=hex_to_rgb(PANEL),
                            outline=hex_to_rgb(color),width=2)
        d.rounded_rectangle([x+2,y+2,x+w-2,y+26],radius=6,fill=hex_to_rgb(color))
        d.text((x+w//2,y+14),label,font=try_bold(14),fill=hex_to_rgb(BG),anchor="mm")

    # Boxes
    bw,bh = 240,60
    # Person top
    px,py = W//2-bw//2, 55
    box(px,py,bw,bh,"Person", ACCENT)
    d.text((px+bw//2,py+44),"Name, Age, Print()",font=fb,fill=hex_to_rgb(MUTED),anchor="mm")

    # Patient bottom
    ptx,pty = W//2-bw//2, 270
    box(ptx,pty,bw,bh,"Patient", YELLOW)
    d.text((ptx+bw//2,pty+44),"Diagnosis, PrintInfo()",font=fb,fill=hex_to_rgb(MUTED),anchor="mm")

    cx = W//2

    # Upcasting arrow (left, upward) — green
    ux = cx - 60
    d.line([(ux, pty), (ux, py+bh)], fill=hex_to_rgb(ACCENT), width=3)
    d.polygon([(ux, py+bh), (ux-7, py+bh+14), (ux+7, py+bh+14)],
              fill=hex_to_rgb(ACCENT))
    # label
    d.text((ux-90, (pty+py+bh)//2), "Upcasting", font=try_bold(14),
           fill=hex_to_rgb(ACCENT), anchor="mm")
    d.text((ux-90, (pty+py+bh)//2+20), "(неявне)", font=fs,
           fill=hex_to_rgb(MUTED), anchor="mm")

    # Downcasting arrow (right, downward) — yellow
    dx2 = cx + 60
    d.line([(dx2, py+bh), (dx2, pty)], fill=hex_to_rgb(YELLOW), width=3)
    d.polygon([(dx2, pty), (dx2-7, pty-14), (dx2+7, pty-14)],
              fill=hex_to_rgb(YELLOW))
    d.text((dx2+95, (pty+py+bh)//2), "Downcasting", font=try_bold(14),
           fill=hex_to_rgb(YELLOW), anchor="mm")
    d.text((dx2+95, (pty+py+bh)//2+20), "(явне: (Patient))", font=fs,
           fill=hex_to_rgb(MUTED), anchor="mm")

    # Memory note
    d.text((W//2, 360),
           "Обидві змінні вказують на один об'єкт у купі",
           font=fs, fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "upcasting-downcasting.png")

make_hierarchy()
make_casting()
print("Done.")
