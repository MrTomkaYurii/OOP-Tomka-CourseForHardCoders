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

def make_vmt():
    W,H = 860,460
    img = Image.new("RGB",(W,H),rgb(BG))
    d = ImageDraw.Draw(img)
    d.text((W//2,22),"VMT (таблиця віртуальних методів) — пізнє зв'язування",
           font=font(17,True),fill=rgb(ACCENT),anchor="mm")

    # ── Left: code
    cx,cy,cw,ch = 20,50,310,130
    d.rounded_rectangle([cx,cy,cx+cw,cy+ch],radius=7,fill=rgb(PANEL),outline=rgb(LINE),width=1)
    for i,line in enumerate([
        "Person p = new Doctor(...);",
        "",
        "p.Print();",
        "// override → Doctor.Print()",
        "// new      → Person.Print()",
    ]):
        col = rgb(ACCENT) if "override" in line else rgb(YELLOW) if "new" in line else rgb(TEXT)
        d.text((cx+12,cy+10+i*22),line,font=font(12),fill=col)

    # ── Center: VMT boxes
    # Person VMT
    pvx,pvy = 370,55
    d.text((pvx+80,pvy-18),"VMT — Person",font=font(13,True),fill=rgb(MUTED),anchor="mm")
    d.rounded_rectangle([pvx,pvy,pvx+160,pvy+50],radius=6,fill=rgb(PANEL),outline=rgb(MUTED),width=1)
    d.text((pvx+80,pvy+25),"Print → Person.Print",font=font(11),fill=rgb(MUTED),anchor="mm")

    # Doctor VMT
    dvx,dvy = 370,175
    d.text((dvx+80,dvy-18),"VMT — Doctor",font=font(13,True),fill=rgb(ACCENT),anchor="mm")
    d.rounded_rectangle([dvx,dvy,dvx+160,dvy+50],radius=6,fill=rgb(PANEL),outline=rgb(ACCENT),width=2)
    d.text((dvx+80,dvy+25),"Print → Doctor.Print",font=font(11),fill=rgb(ACCENT),anchor="mm")

    # Arrow: object → VMT
    d.line([(cx+cw,cy+ch//2),(dvx,dvy+25)],fill=rgb(ACCENT),width=2)
    d.text((dvx-120,dvy+10),"override:",font=font(11,True),fill=rgb(ACCENT))
    d.text((dvx-120,dvy+26),"об'єкт Doctor",font=font(11),fill=rgb(ACCENT))
    d.text((dvx-120,dvy+42),"→ VMT Doctor",font=font(11),fill=rgb(ACCENT))

    # ── Right: static binding (new)
    svx,svy = 650,55
    d.text((svx+90,svy-18),"Статична прив'язка",font=font(13,True),fill=rgb(YELLOW),anchor="mm")
    d.rounded_rectangle([svx,svy,svx+180,svy+100],radius=6,fill=rgb(PANEL),outline=rgb(YELLOW),width=2)
    lines2=[
        "Person p = new Doctor()",
        "p.Print()",
        "→ тип змінної = Person",
        "→ Person.Print()",
    ]
    for i,l in enumerate(lines2):
        col=rgb(YELLOW) if i>=2 else rgb(TEXT)
        d.text((svx+10,svy+12+i*20),l,font=font(11),fill=col)

    d.line([(cx+cw,cy+30),(svx,svy+50)],fill=rgb(YELLOW),width=2)
    d.text((svx-110,svy+40),"new:",font=font(11,True),fill=rgb(YELLOW))
    d.text((svx-110,svy+56),"тип змінної",font=font(11),fill=rgb(YELLOW))
    d.text((svx-110,svy+72),"вирішує",font=font(11),fill=rgb(YELLOW))

    # Summary table
    ty=310
    d.text((W//2,ty),  "override (virtual)          new (hiding)",
           font=font(13,True),fill=rgb(TEXT),anchor="mm")
    rows=[
        ("Пізнє зв'язування (runtime)","Раннє зв'язування (compile)"),
        ("Реальний тип об'єкта","Тип змінної"),
        ("Поліморфна поведінка","Локальна поведінка"),
        ("Потрібен virtual у базовому","Будь-який метод базового"),
    ]
    for i,(l,r) in enumerate(rows):
        y=ty+28+i*32
        d.text((W//2-20,y),l,font=font(12),fill=rgb(ACCENT),anchor="rm")
        d.text((W//2-10,y),"│",font=font(12),fill=rgb(MUTED),anchor="lm")
        d.text((W//2+20,y),r,font=font(12),fill=rgb(YELLOW),anchor="lm")
    save_if_new(img,"vmt-vs-static.png")

make_vmt()
print("Done.")
