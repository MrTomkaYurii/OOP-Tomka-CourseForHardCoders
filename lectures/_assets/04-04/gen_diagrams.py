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

def make_hiding_vs_override():
    W,H = 820, 400
    img = Image.new("RGB",(W,H),rgb(BG))
    d = ImageDraw.Draw(img)
    d.text((W//2,22),"new (приховування) vs override (перевизначення)",
           font=font(17,True),fill=rgb(ACCENT),anchor="mm")

    # Two columns
    cols = [
        ("override",ACCENT,[
            "virtual у базовому класі",
            "Поліморфна поведінка",
            "Person p = new Doctor()",
            "→ p.Print() = Doctor.Print()",
            "Реальний тип вирішує",
        ]),
        ("new",YELLOW,[
            "Будь-який метод базового",
            "Статична прив'язка",
            "Person p = new Doctor()",
            "→ p.Print() = Person.Print()",
            "Тип змінної вирішує",
        ]),
    ]
    bw,bh = 340,280
    for i,(title,color,lines) in enumerate(cols):
        x = 30 + i*(bw+50); y=55
        d.rounded_rectangle([x+3,y+3,x+bw+3,y+bh+3],radius=8,fill=rgb(LINE))
        d.rounded_rectangle([x,y,x+bw,y+bh],radius=8,fill=rgb(PANEL),outline=rgb(color),width=2)
        d.rounded_rectangle([x+2,y+2,x+bw-2,y+32],radius=7,fill=rgb(color))
        d.text((x+bw//2,y+17),title,font=font(16,True),fill=rgb(BG),anchor="mm")
        for j,line in enumerate(lines):
            col = rgb(TEXT) if j<2 else (rgb(ACCENT) if i==0 else rgb(YELLOW))
            d.text((x+18,y+50+j*42),line,font=font(13),fill=col)

    d.text((W//2,370),"override — поліморфізм | new — локальне перевизначення для конкретного типу змінної",
           font=font(12),fill=rgb(MUTED),anchor="mm")
    save_if_new(img,"hiding-vs-override.png")

make_hiding_vs_override()
print("Done.")
