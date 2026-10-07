from PIL import Image, ImageDraw, ImageFont
import os

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; YELLOW="#c7b876"
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

def make_object_methods():
    W,H = 820,420
    img = Image.new("RGB",(W,H),rgb(BG))
    d = ImageDraw.Draw(img)
    d.text((W//2,22),"System.Object — методи доступні у кожному класі C#",
           font=font(17,True),fill=rgb(ACCENT),anchor="mm")

    methods = [
        ("ToString()",    "string",  ACCENT,  "Рядкове представлення об'єкта\nПеревизначається: так"),
        ("GetHashCode()", "int",     YELLOW,  "Числовий хеш-код об'єкта\nПеревизначається: так"),
        ("Equals(obj)",   "bool",    ACCENT,  "Порівняння двох об'єктів\nПеревизначається: так"),
        ("GetType()",     "Type",    MUTED,   "Реальний тип об'єкта\nПеревизначається: ні"),
    ]

    bw,bh = 170,100
    gap = 20
    total_w = len(methods)*(bw+gap)-gap
    start_x = (W-total_w)//2
    top_y = 60

    # Object box at top
    ow,oh = 300,45
    ox,oy = W//2-ow//2, top_y
    d.rounded_rectangle([ox,oy,ox+ow,oy+oh],radius=7,fill=rgb(PANEL),outline=rgb(MUTED),width=2)
    d.text((W//2,oy+oh//2),"System.Object",font=font(15,True),fill=rgb(MUTED),anchor="mm")

    for i,(name,ret,color,desc) in enumerate(methods):
        x = start_x + i*(bw+gap)
        y = top_y+oh+60
        # connector
        mx = x+bw//2
        d.line([(W//2,oy+oh),(W//2,oy+oh+20)],fill=rgb(LINE),width=1)
        d.line([(start_x+bw//2,oy+oh+20),(start_x+3*(bw+gap)+bw//2,oy+oh+20)],fill=rgb(LINE),width=1)
        d.line([(mx,oy+oh+20),(mx,y)],fill=rgb(LINE),width=1)
        d.polygon([(mx,y),(mx-6,y-12),(mx+6,y-12)],fill=rgb(color))

        d.rounded_rectangle([x+2,y+2,x+bw+2,y+bh+2],radius=7,fill=rgb(LINE))
        d.rounded_rectangle([x,y,x+bw,y+bh],radius=7,fill=rgb(PANEL),outline=rgb(color),width=2)
        d.rounded_rectangle([x+2,y+2,x+bw-2,y+28],radius=6,fill=rgb(color))
        d.text((x+bw//2,y+15),name,font=font(12,True),fill=rgb(BG),anchor="mm")
        d.text((x+bw//2,y+36),f"→ {ret}",font=font(11),fill=rgb(color),anchor="mm")
        for j,line in enumerate(desc.split('\n')):
            d.text((x+8,y+54+j*18),line,font=font(10),fill=rgb(MUTED))

    d.text((W//2,385),
           "Equals і GetHashCode завжди перевизначаються разом (контракт рівності)",
           font=font(12),fill=rgb(YELLOW),anchor="mm")

    save_if_new(img,"object-methods.png")

make_object_methods()
print("Done.")
