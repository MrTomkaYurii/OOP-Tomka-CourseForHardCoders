from PIL import Image, ImageDraw, ImageFont
import os

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; YELLOW="#c7b876"; RED="#e07070"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def rgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def save_if_new(img, name):
    p=os.path.join(SCRIPT_DIR,name)
    if os.path.exists(p): print(f"SKIP: {name}"); return
    img.save(p); print(f"CREATED: {name}")

def font(size, bold=False):
    cands = (["C:/Windows/Fonts/consolab.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"]
             if bold else
             ["C:/Windows/Fonts/consola.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"])
    for c in cands:
        if os.path.exists(c): return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def make_constraints():
    W,H = 840,440
    img = Image.new("RGB",(W,H),rgb(BG))
    d = ImageDraw.Draw(img)
    d.text((W//2,22),"Обмеження узагальнень — where T : ...",
           font=font(17,True),fill=rgb(ACCENT),anchor="mm")

    constraints = [
        ("where T : Notification",  "T — Notification\nабо похідний клас",   ACCENT),
        ("where T : class",         "T — будь-який\nreference type",          YELLOW),
        ("where T : struct",        "T — будь-який\nvalue type",              MUTED),
        ("where T : new()",         "T — має публічний\nконструктор без парам",ACCENT),
        ("where T : IComparable<T>","T — реалізує\nінтерфейс",               YELLOW),
        ("where T : Notification,\n  new()", "Кілька обмежень\nодночасно",   MUTED),
    ]

    bw,bh = 230,90
    cols, rows = 3, 2
    gx, gy = 40, 65
    gap_x = (W - 2*gx - cols*bw) // (cols-1)
    gap_y = 20

    for i,(constraint,desc,color) in enumerate(constraints):
        col = i % cols
        row = i // cols
        x = gx + col*(bw+gap_x)
        y = gy + row*(bh+gap_y)
        d.rounded_rectangle([x+2,y+2,x+bw+2,y+bh+2],radius=7,fill=rgb(LINE))
        d.rounded_rectangle([x,y,x+bw,y+bh],radius=7,fill=rgb(PANEL),outline=rgb(color),width=2)
        # constraint label
        lines = constraint.split('\n')
        for j,line in enumerate(lines):
            d.text((x+10,y+8+j*18),line,font=font(12,True),fill=rgb(color))
        # desc
        desc_lines = desc.split('\n')
        for j,line in enumerate(desc_lines):
            d.text((x+10,y+bh-32+j*16),line,font=font(11),fill=rgb(MUTED))

    # Arrow + example
    ey = gy + rows*(bh+gap_y) + 10
    d.text((W//2, ey),
           "Sender<T> where T : Notification  →  T гарантовано має властивості Notification",
           font=font(13),fill=rgb(TEXT),anchor="mm")
    d.text((W//2, ey+24),
           "без обмеження  →  T — лише object, звернення до Text/Email неможливе",
           font=font(13),fill=rgb(RED),anchor="mm")

    save_if_new(img,"constraints-overview.png")

make_constraints()
print("Done.")
