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

def make_abstract_hierarchy():
    W,H = 820,480
    img = Image.new("RGB",(W,H),rgb(BG))
    d = ImageDraw.Draw(img)
    d.text((W//2,22),"Абстрактний клас: ієрархія медичного персоналу",
           font=font(17,True),fill=rgb(ACCENT),anchor="mm")

    def box(x,y,w,h,title,subtitle,lines,color,abstract=False):
        d.rounded_rectangle([x+3,y+3,x+w+3,y+h+3],radius=8,fill=rgb(LINE))
        d.rounded_rectangle([x,y,x+w,y+h],radius=8,fill=rgb(PANEL),outline=rgb(color),width=2)
        # header
        hh=30
        d.rounded_rectangle([x+2,y+2,x+w-2,y+hh],radius=7,fill=rgb(color))
        prefix = "«abstract» " if abstract else ""
        d.text((x+w//2,y+hh//2),prefix+title,font=font(13,True),fill=rgb(BG),anchor="mm")
        if subtitle:
            d.text((x+w//2,y+hh+12),subtitle,font=font(11),fill=rgb(MUTED),anchor="mm")
        for i,line in enumerate(lines):
            col=rgb(RED) if "abstract" in line else rgb(TEXT)
            d.text((x+10,y+hh+(14 if subtitle else 4)+16+i*18),line,font=font(11),fill=col)

    # Abstract base — top center
    bw,bh=380,130
    bx=W//2-bw//2; by=50
    box(bx,by,bw,bh,"MedicalStaff","(абстрактний клас)",[
        "  Name, Age",
        "  abstract string Role { get; }",
        "  abstract void Examine()",
        "  void PrintCard()  ← звичайний метод",
    ],MUTED,abstract=True)

    # Derived: Doctor, Nurse
    dw,dh=280,130
    positions=[(120,300,"Doctor",ACCENT,[
        "  Role = \"Лікар\"",
        "  Specialization",
        "  override Examine()",
    ]),(440,300,"Nurse",YELLOW,[
        "  Role = \"Медсестра\"",
        "  Ward",
        "  override Examine()",
    ])]

    fork_y=by+bh+30
    d.line([(W//2,by+bh),(W//2,fork_y)],fill=rgb(MUTED),width=2)
    for dx,dy,name,color,lines in positions:
        d.line([(W//2,fork_y),(dx+dw//2,fork_y),(dx+dw//2,dy)],fill=rgb(MUTED),width=2)
        d.polygon([(dx+dw//2,dy),(dx+dw//2-7,dy-14),(dx+dw//2+7,dy-14)],fill=rgb(MUTED))
        box(dx,dy,dw,dh,name,None,lines,color)

    # Cannot instantiate note
    d.rounded_rectangle([bx+bw+10,by+10,bx+bw+200,by+60],radius=6,fill=rgb(PANEL),outline=rgb(RED),width=1)
    d.text((bx+bw+105,by+35),"new MedicalStaff()\n  → Помилка!",font=font(11),fill=rgb(RED),anchor="mm")

    d.text((W//2,455),"Абстрактний клас визначає контракт — похідні зобов'язані реалізувати abstract-члени",
           font=font(12),fill=rgb(MUTED),anchor="mm")

    save_if_new(img,"abstract-hierarchy.png")

make_abstract_hierarchy()
print("Done.")
