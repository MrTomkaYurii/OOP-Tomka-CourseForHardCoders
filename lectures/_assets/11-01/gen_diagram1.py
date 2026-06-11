# -*- coding: utf-8 -*-
# String immutability — heap allocation diagram
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"
RED="#c77676"

W,H=940,440
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",14)
fr=load("C:/Windows/Fonts/arial.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11)
ft=load("C:/Windows/Fonts/arialbd.ttf",16)
fh=load("C:/Windows/Fonts/arialbd.ttf",13)

d.text((W//2,24),"string — незмінний тип: кожна операція створює новий об'єкт у heap",
       font=ft,fill=ACCENT,anchor="mm")

# === STACK (left) ===
sx,sy,sw,sh = 30,65,180,300
d.rounded_rectangle([sx,sy,sx+sw,sy+sh],radius=8,fill=PANEL,outline=LINE,width=2)
d.text((sx+sw//2,sy+14),"STACK (змінні)",font=fh,fill=MUTED,anchor="mm")
d.line([(sx+10,sy+30),(sx+sw-10,sy+30)],fill=LINE,width=1)

stack_vars=[
    ("diagnosis", ACCENT),
    ("step1",     ORANGE),
    ("step2",     RED),
    ("step3",     ACCENT),
]
for i,(name,col) in enumerate(stack_vars):
    vy=sy+48+i*54
    d.rounded_rectangle([sx+10,vy,sx+sw-10,vy+34],radius=4,fill=DARK,outline=col,width=1)
    d.text((sx+sw//2,vy+10),name,font=fb,fill=col,anchor="mm")
    d.text((sx+sw//2,vy+24),"ref ->",font=fs,fill=MUTED,anchor="mm")

# === HEAP (right) ===
hx,hy,hw = 320,55,560
heap_h=360
d.rounded_rectangle([hx,hy,hx+hw,hy+heap_h],radius=8,fill=PANEL,outline=LINE,width=2)
d.text((hx+hw//2,hy+14),"HEAP (рядкові об'єкти)",font=fh,fill=MUTED,anchor="mm")
d.line([(hx+10,hy+30),(hx+hw-10,hy+30)],fill=LINE,width=1)

heap_items=[
    (ACCENT, '"Гіпертензія"',             'string diagnosis = "Гіпертензія";'),
    (ORANGE, '"гіпертензія"',             'string step1 = diagnosis.ToLower();'),
    (RED,    '"гіпертензія артеріальна"', 'string step2 = step1 + " артеріальна";'),
    (ACCENT, '"ГІПЕРТЕНЗІЯ АРТЕРІАЛЬНА"', 'string step3 = step2.ToUpper();'),
]
box_h=58; gap=14
for i,(col,val,code) in enumerate(heap_items):
    by=hy+44+i*(box_h+gap)
    d.rounded_rectangle([hx+16,by,hx+hw-16,by+box_h],radius=5,fill=DARK,outline=col,width=2)
    d.text((hx+32,by+14),val,font=fb,fill=col,anchor="lm")
    d.text((hx+32,by+34),code,font=fs,fill=MUTED,anchor="lm")

# === ARROWS stack -> heap ===
cols=[ACCENT,ORANGE,RED,ACCENT]
for i,col in enumerate(cols):
    ay = sy+48+i*54+17
    heap_by = hy+44+i*(box_h+gap)+box_h//2
    # arrow from stack var -> heap box
    x0=sx+sw-10; x1=hx+16
    d.line([(x0,ay),(x0+60,ay),(x0+60,heap_by),(x1,heap_by)],fill=col,width=1)
    d.polygon([(x1,heap_by),(x1+8,heap_by-4),(x1+8,heap_by+4)],fill=col)

# === NEW badge ===
new_x=hx+hw-80
for i in range(1,4):
    by=hy+44+i*(box_h+gap)
    d.rounded_rectangle([new_x,by+4,new_x+52,by+22],radius=4,fill=RED)
    d.text((new_x+26,by+13),"NEW obj",font=fs,fill=TEXT,anchor="mm")

# Bottom legend
ly=H-60
d.line([(30,ly-8),(W-30,ly-8)],fill=LINE,width=1)
d.text((30,ly),   "string незмінний (immutable): жоден метод не змінює оригінал — завжди повертає новий рядок",font=fs,fill=TEXT)
d.text((30,ly+18),"string interning: однакові рядкові літерали в коді можуть вказувати на той самий об'єкт у heap",font=fs,fill=MUTED)
d.text((30,ly+36),"Наслідок: для багатьох змін у циклі використовуйте StringBuilder (розд. 11.4)",font=fs,fill=ORANGE)

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/11-01/string-immutability.png"
img.save(out); print("OK:",out)
