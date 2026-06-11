# -*- coding: utf-8 -*-
# IEnumerable/IEnumerator — foreach decomposition diagram
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"

W,H=920,430
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",14); fr=load("C:/Windows/Fonts/arial.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11); ft=load("C:/Windows/Fonts/arialbd.ttf",16)
fh=load("C:/Windows/Fonts/arialbd.ttf",13)

d.text((W//2,24),"IEnumerable<T> і IEnumerator<T> — як працює foreach",font=ft,fill=ACCENT,anchor="mm")

# === LEFT: foreach source code ===
left_x,top_y=40,65
d.rounded_rectangle([left_x,top_y,left_x+230,top_y+200],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((left_x+115,top_y+14),"foreach (синтаксис)",font=fh,fill=ACCENT,anchor="mm")
code_lines=[
    "foreach (var p in ward)",
    "{",
    "   Console.WriteLine(p);",
    "}",
]
for i,line in enumerate(code_lines):
    d.text((left_x+12,top_y+38+i*22),line,font=fr,fill=TEXT,anchor="lm")

arrow_y=top_y+210//2+top_y
# Arrow → compiled
arr_end=left_x+230+8
d.text((left_x+115,top_y+170),"компілятор розгортає у:",font=fs,fill=MUTED,anchor="mm")

# === MIDDLE: compiled expansion ===
comp_x=left_x+240+10; comp_y=top_y; comp_w=260; comp_h=280
d.rounded_rectangle([comp_x,comp_y,comp_x+comp_w,comp_y+comp_h],radius=8,fill=DARK,outline=ORANGE,width=2)
d.text((comp_x+comp_w//2,comp_y+14),"Скомпільований код",font=fh,fill=ORANGE,anchor="mm")
comp_code=[
    "var e = ward.GetEnumerator();",
    "try {",
    "  while (e.MoveNext())",
    "  {",
    "    var p = e.Current;",
    "    Console.WriteLine(p);",
    "  }",
    "}",
    "finally { e.Dispose(); }",
]
for i,line in enumerate(comp_code):
    color=ACCENT if "GetEnumerator" in line else (ORANGE if "MoveNext" in line or "Current" in line else TEXT)
    d.text((comp_x+10,comp_y+36+i*22),line,font=fs,fill=color,anchor="lm")
# arrow comp → interface
d.line([(left_x+230,comp_y+comp_h//2-30),(comp_x,comp_y+comp_h//2-30)],fill=ORANGE,width=2)
d.polygon([(comp_x,comp_y+comp_h//2-30),(comp_x-8,comp_y+comp_h//2-35),(comp_x-8,comp_y+comp_h//2-25)],fill=ORANGE)

# === RIGHT: Interface boxes ===
iface_x=comp_x+comp_w+20; iface_y=top_y; iface_w=240

# IEnumerable
ie_h=90
d.rounded_rectangle([iface_x,iface_y,iface_x+iface_w,iface_y+ie_h],radius=6,fill=PANEL,outline=ACCENT,width=2)
d.text((iface_x+iface_w//2,iface_y+14),"IEnumerable<T>",font=fh,fill=ACCENT,anchor="mm")
d.line([(iface_x+10,iface_y+30),(iface_x+iface_w-10,iface_y+30)],fill=LINE,width=1)
d.text((iface_x+12,iface_y+48),"IEnumerator<T> GetEnumerator()",font=fs,fill=TEXT,anchor="lm")
d.text((iface_x+12,iface_y+66),"реалізують: List, Array, Queue...",font=fs,fill=MUTED,anchor="lm")

# IEnumerator
ier_y=iface_y+ie_h+20; ier_h=140
d.rounded_rectangle([iface_x,ier_y,iface_x+iface_w,ier_y+ier_h],radius=6,fill=PANEL,outline=ORANGE,width=2)
d.text((iface_x+iface_w//2,ier_y+14),"IEnumerator<T>",font=fh,fill=ORANGE,anchor="mm")
d.line([(iface_x+10,ier_y+30),(iface_x+iface_w-10,ier_y+30)],fill=LINE,width=1)
ier_items=[
    ("bool MoveNext()",   "перейти до наступного"),
    ("T Current { get; }","поточний елемент"),
    ("void Reset()",      "на початок"),
    ("void Dispose()",    "звільнити ресурси"),
]
for i,(sig,desc) in enumerate(ier_items):
    iy=ier_y+40+i*22
    d.text((iface_x+12,iy),sig,font=fs,fill=ORANGE,anchor="lm")
    d.text((iface_x+12,iy+11),f"  // {desc}",font=fs,fill=MUTED,anchor="lm")

# Arrow from comp → IEnumerable
arr_cx=comp_x+comp_w+2
d.line([(arr_cx,iface_y+ie_h//2),(iface_x-2,iface_y+ie_h//2)],fill=ACCENT,width=1)
d.polygon([(iface_x-2,iface_y+ie_h//2),(iface_x-10,iface_y+ie_h//2-4),(iface_x-10,iface_y+ie_h//2+4)],fill=ACCENT)
d.line([(arr_cx,ier_y+ier_h//2),(iface_x-2,ier_y+ier_h//2)],fill=ORANGE,width=1)
d.polygon([(iface_x-2,ier_y+ier_h//2),(iface_x-10,ier_y+ier_h//2-4),(iface_x-10,ier_y+ier_h//2+4)],fill=ORANGE)

# Bottom
ly=H-52
d.line([(30,ly-8),(W-30,ly-8)],fill=LINE,width=1)
d.text((30,ly),"Щоб власний клас підтримував foreach — реалізуйте IEnumerable<T>  або визначте метод GetEnumerator()",font=fs,fill=TEXT)
d.text((30,ly+18),"yield return (10.8) дає той самий результат, але без написання класу-перелічувача вручну",font=fs,fill=MUTED)

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/10-07/ienumerable-foreach-decomposition.png"
img.save(out); print("OK:",out)
