from PIL import Image, ImageDraw, ImageFont
import os

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; YELLOW="#c7b876"; RED="#e07070"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def rgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def save_if_new(img, name):
    p = os.path.join(SCRIPT_DIR, name)
    if os.path.exists(p): print(f"SKIP: {name}"); return
    img.save(p); print(f"CREATED: {name}")

def font(size, bold=False):
    cands = (["C:/Windows/Fonts/consolab.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"] if bold else
             ["C:/Windows/Fonts/consola.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"])
    for c in cands:
        if os.path.exists(c): return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def make_variants():
    W, H = 860, 480
    img = Image.new("RGB", (W, H), rgb(BG))
    d = ImageDraw.Draw(img)
    d.text((W//2, 22), "4 варіанти успадкування узагальнених класів",
           font=font(17, True), fill=rgb(ACCENT), anchor="mm")

    variants = [
        ("1",  "FlexibleRecord<T>",          ": MedicalRecord<T>",
         "T передається далі\nПараметр залишається відкритим", ACCENT),
        ("2",  "StringRecord",               ": MedicalRecord<string>",
         "T фіксується як string\nПохідний — звичайний клас", YELLOW),
        ("3",  "NumberedRecord<T>",          ": MedicalRecord<int>",
         "int фіксовано у базовому\nT — власний новий параметр", MUTED),
        ("4",  "AnnotatedRecord<T, TNote>",  ": MedicalRecord<T>",
         "T передається + додається\nновий параметр TNote", ACCENT),
    ]

    bw, bh = 370, 95
    for i, (num, child, parent, desc, color) in enumerate(variants):
        col = i % 2
        row = i // 2
        x = 30 + col * (bw + 50)
        y = 55 + row * (bh + 18)

        d.rounded_rectangle([x+2,y+2,x+bw+2,y+bh+2], radius=7, fill=rgb(LINE))
        d.rounded_rectangle([x,y,x+bw,y+bh], radius=7, fill=rgb(PANEL),
                            outline=rgb(color), width=2)
        # number badge
        d.ellipse([x+8,y+8,x+30,y+30], fill=rgb(color))
        d.text((x+19, y+19), num, font=font(13, True), fill=rgb(BG), anchor="mm")
        # child class
        d.text((x+38, y+14), child, font=font(13, True), fill=rgb(color))
        # parent
        d.text((x+38, y+32), parent, font=font(12), fill=rgb(MUTED))
        # desc
        for j, line in enumerate(desc.split('\n')):
            d.text((x+12, y+54+j*17), line, font=font(11), fill=rgb(TEXT))

    # Base class reminder
    by = 55 + 2*(bh+18) + 10
    d.rounded_rectangle([180, by, 680, by+45], radius=7,
                        fill=rgb(PANEL), outline=rgb(MUTED), width=1)
    d.text((W//2, by+23),
           "abstract class MedicalRecord<T>  { public T Id { get; } ... }",
           font=font(13), fill=rgb(MUTED), anchor="mm")

    save_if_new(img, "generic-inheritance-variants.png")

make_variants()
print("Done.")
