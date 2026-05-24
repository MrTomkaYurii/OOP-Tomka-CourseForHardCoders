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

def make_generics():
    W,H = 840,420
    img = Image.new("RGB",(W,H),rgb(BG))
    d = ImageDraw.Draw(img)
    d.text((W//2,22),"Узагальнений клас: один шаблон — різні типи",
           font=font(17,True),fill=rgb(ACCENT),anchor="mm")

    # Template box (center top)
    tw,th=340,90
    tx,ty=W//2-tw//2,55
    d.rounded_rectangle([tx+3,ty+3,tx+tw+3,ty+th+3],radius=8,fill=rgb(LINE))
    d.rounded_rectangle([tx,ty,tx+tw,ty+th],radius=8,fill=rgb(PANEL),outline=rgb(ACCENT),width=2)
    d.rounded_rectangle([tx+2,ty+2,tx+tw-2,ty+30],radius=7,fill=rgb(ACCENT))
    d.text((tx+tw//2,ty+16),"MedicalRecord<T>",font=font(15,True),fill=rgb(BG),anchor="mm")
    d.text((tx+tw//2,ty+50),"T Id { get; }",font=font(13),fill=rgb(TEXT),anchor="mm")
    d.text((tx+tw//2,ty+70),"string Description { get; }",font=font(13),fill=rgb(MUTED),anchor="mm")

    # Three instantiations
    instances=[
        (80, "MedicalRecord<int>","Id: int","record = new(1001, ...)",ACCENT),
        (310,"MedicalRecord<string>","Id: string","record = new(\"P-001\", ...)",YELLOW),
        (540,"MedicalRecord<Guid>","Id: Guid","record = new(Guid.NewGuid(), ...)",MUTED),
    ]
    iw,ih=220,100
    fork_y=ty+th+30
    d.line([(W//2,ty+th),(W//2,fork_y)],fill=rgb(MUTED),width=2)
    centers=[ix+iw//2 for ix,*_ in instances]
    d.line([(centers[0],fork_y),(centers[-1],fork_y)],fill=rgb(MUTED),width=2)

    for ix,title,line1,line2,color in instances:
        iy=fork_y+40
        cx=ix+iw//2
        d.line([(cx,fork_y),(cx,iy)],fill=rgb(MUTED),width=2)
        d.polygon([(cx,iy),(cx-7,iy-14),(cx+7,iy-14)],fill=rgb(color))
        d.rounded_rectangle([ix+2,iy+2,ix+iw+2,iy+ih+2],radius=7,fill=rgb(LINE))
        d.rounded_rectangle([ix,iy,ix+iw,iy+ih],radius=7,fill=rgb(PANEL),outline=rgb(color),width=2)
        d.rounded_rectangle([ix+2,iy+2,ix+iw-2,iy+28],radius=6,fill=rgb(color))
        d.text((ix+iw//2,iy+15),title,font=font(12,True),fill=rgb(BG),anchor="mm")
        d.text((ix+iw//2,iy+45),line1,font=font(11),fill=rgb(color),anchor="mm")
        d.text((ix+iw//2,iy+65),line2,font=font(10),fill=rgb(MUTED),anchor="mm")

    # Object vs Generic comparison
    cy2=iy+ih+30
    d.text((W//2,cy2),"object Id  →  boxing + небезпечне приведення     |     T Id  →  без boxing, перевірка компілятором",
           font=font(12),fill=rgb(TEXT),anchor="mm")
    d.text((W//2,cy2+22),"                   "+RED+"  ✗ object"+" "*40+ACCENT+"  ✓ generics",
           font=font(12),fill=rgb(MUTED),anchor="mm")
    # simpler
    d.text((280,cy2+22),"✗  object — boxing, InvalidCastException",font=font(12),fill=rgb(RED))
    d.text((280,cy2+40),"✓  T      — типобезпечно, без boxing",font=font(12),fill=rgb(ACCENT))

    save_if_new(img,"generics-overview.png")

make_generics()
print("Done.")
