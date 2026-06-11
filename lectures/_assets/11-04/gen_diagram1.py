# -*- coding: utf-8 -*-
# StringBuilder vs String — memory allocation comparison
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"
RED="#c77676"

W,H=940,460
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11)
ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)

d.text((W//2,22),"StringBuilder vs string — алокація пам'яті при побудові рядка у циклі",
       font=ft,fill=ACCENT,anchor="mm")

# ===== LEFT: string concatenation in loop =====
lx,ly_top=30,50; lw=400
d.rounded_rectangle([lx,ly_top,lx+lw,ly_top+380],radius=8,fill=PANEL,outline=RED,width=2)
d.text((lx+lw//2,ly_top+14),"string + concat у циклі (N ітерацій)",font=fh,fill=RED,anchor="mm")

# heap objects stacked
items_str=[
    ('"Результат:"',        "алок. 1"),
    ('"Результат:Петр"',    "алок. 2"),
    ('"Результат:ПетрКов"', "алок. 3"),
    ('"Результат:ПетрКовСид"',"алок. 4"),
    ("... (N нових об'єктів у heap)", "алок. N"),
]
for i,(val,label) in enumerate(items_str):
    iy=ly_top+36+i*58
    alpha=1.0 if i<4 else 0.5
    col=RED if i<4 else MUTED
    d.rounded_rectangle([lx+16,iy,lx+lw-16,iy+42],radius=4,fill=DARK,outline=col,width=1+(1 if i<4 else 0))
    d.text((lx+28,iy+14),val,font=fs,fill=col,anchor="lm")
    d.text((lx+lw-22,iy+14),label,font=fc,fill=MUTED,anchor="rm")
    if i<4:
        d.text((lx+28,iy+28),"(попередній залишається у heap — GC збере потім)",font=fc,fill=MUTED,anchor="lm")

d.text((lx+lw//2,ly_top+340),"O(N^2) алокацій | GC pressure",font=fb,fill=RED,anchor="mm")
d.text((lx+lw//2,ly_top+360),"Кожна += виділяє НОВИЙ блок пам'яті",font=fs,fill=MUTED,anchor="mm")

# ===== RIGHT: StringBuilder =====
rx=lx+lw+40; rw=lw
d.rounded_rectangle([rx,ly_top,rx+rw,ly_top+380],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((rx+rw//2,ly_top+14),"StringBuilder.Append() у циклі",font=fh,fill=ACCENT,anchor="mm")

# Buffer growth stages
stages=[
    ("Capacity=16",  "Результат:",         16, 10),
    ("Capacity=16",  "Результат:Петр",     16, 14),
    ("Capacity=32",  "Результат:ПетрКов",  32, 18),
    ("Capacity=32",  "Результат:ПетрКовСид",32,22),
]
for i,(cap,content,buf,used) in enumerate(stages):
    sy=ly_top+36+i*72
    # buffer bar
    bar_x=rx+16; bar_w=rw-32; bar_h=28
    d.rounded_rectangle([bar_x,sy,bar_x+bar_w,sy+bar_h],radius=3,fill=DARK,outline=LINE)
    # used portion
    used_w=int(bar_w * used/buf * 0.8)
    d.rectangle([bar_x,sy,bar_x+used_w,sy+bar_h],fill=ACCENT)
    d.text((bar_x+used_w//2,sy+bar_h//2),content[:18],font=fc,fill=DARK,anchor="mm")
    # label
    free_w=int(bar_w*(buf-used)/buf*0.8)
    if free_w>40:
        d.text((bar_x+used_w+free_w//2,sy+bar_h//2),"вільно",font=fc,fill=MUTED,anchor="mm")
    d.text((bar_x,sy+bar_h+6),cap,font=fc,fill=ORANGE,anchor="lm")
    if i==2:
        d.text((bar_x+200,sy+bar_h+6),"<-- подвоєння ємності",font=fc,fill=ORANGE,anchor="lm")

d.text((rx+rw//2,ly_top+340),"O(N) алокацій | один буфер",font=fb,fill=ACCENT,anchor="mm")
d.text((rx+rw//2,ly_top+360),"Append розширює буфер тільки при переповненні",font=fs,fill=MUTED,anchor="mm")

# Center arrow / vs
mid=(lx+lw+rx)//2
d.text((mid,ly_top+190),"vs",font=fb,fill=MUTED,anchor="mm")

# Bottom
by=H-32
d.line([(30,by-8),(W-30,by-8)],fill=LINE,width=1)
d.text((30,by),"Правило: string для <10 операцій, StringBuilder для циклів і невідомої кількості змін",
       font=fs,fill=TEXT)

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/11-04/stringbuilder-vs-string-memory.png"
img.save(out); print("OK:",out)
