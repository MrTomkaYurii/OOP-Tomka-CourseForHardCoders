# -*- coding: utf-8 -*-
# yield return — lazy execution flow
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"

W,H=920,420
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",14); fr=load("C:/Windows/Fonts/arial.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11); ft=load("C:/Windows/Fonts/arialbd.ttf",16)
fh=load("C:/Windows/Fonts/arialbd.ttf",13)

d.text((W//2,24),"yield return — ліниве виконання ітератора",font=ft,fill=ACCENT,anchor="mm")

# === LEFT: Iterator method code ===
lx,ty=40,65; lw,lh=280,250
d.rounded_rectangle([lx,ty,lx+lw,ty+lh],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((lx+lw//2,ty+14),"Метод-ітератор",font=fh,fill=ORANGE,anchor="mm")
code=[
    "IEnumerable<Patient> ActivePat()",
    "{",
    "  yield return patients[0]; // 1)",
    "  yield return patients[1]; // 2)",
    "  yield return patients[2]; // 3)",
    "  // кінець — yield break",
    "}",
]
for i,line in enumerate(code):
    col=ACCENT if "yield return" in line else (MUTED if "//" in line and "yield" not in line else TEXT)
    d.text((lx+12,ty+36+i*26),line,font=fs,fill=col,anchor="lm")

# === RIGHT: foreach consumer ===
rx=lx+lw+160; rw=260; rh=250; ry=ty
d.rounded_rectangle([rx,ry,rx+rw,ry+rh],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((rx+rw//2,ry+14),"foreach-споживач",font=fh,fill=ACCENT,anchor="mm")
cons=[
    "foreach (var p in ActivePat())",
    "{",
    "   // ітерація 1: p = patients[0]",
    "   // ітерація 2: p = patients[1]",
    "   // ітерація 3: p = patients[2]",
    "   Process(p);",
    "}",
]
for i,line in enumerate(cons):
    col=MUTED if "//" in line else TEXT
    d.text((rx+12,ry+36+i*26),line,font=fs,fill=col,anchor="lm")

# === MIDDLE: bidirectional arrows with step labels ===
mx=(lx+lw+rx)//2; arrow_y0=ty+62

steps=[
    ("1) MoveNext()",  "yield return [0]", ty+82),
    ("2) MoveNext()",  "yield return [1]", ty+108),
    ("3) MoveNext()",  "yield return [2]", ty+134),
    ("4) MoveNext()",  "false (кінець)",   ty+160),
]
for label_fwd, label_back, ay in steps:
    # MoveNext: right → left (consumer calls iterator)
    d.line([(rx-2,ay),(lx+lw+2,ay)],fill=ACCENT,width=1)
    d.polygon([(lx+lw+2,ay),(lx+lw+10,ay-4),(lx+lw+10,ay+4)],fill=ACCENT)
    # yield return: left → right (iterator returns value)
    back_y=ay+18
    d.line([(lx+lw+2,back_y),(rx-2,back_y)],fill=ORANGE,width=1)
    d.polygon([(rx-2,back_y),(rx-10,back_y-4),(rx-10,back_y+4)],fill=ORANGE)
    d.text((mx,ay-1),label_fwd,font=fs,fill=ACCENT,anchor="mm")
    d.text((mx,back_y-1),label_back,font=fs,fill=ORANGE,anchor="mm")

# State save annotation
ann_x=mx-50; ann_y=ty+200
d.rounded_rectangle([ann_x,ann_y,ann_x+100,ann_y+36],radius=4,fill=DARK,outline=LINE)
d.text((ann_x+50,ann_y+10),"стан збережено",font=fs,fill=MUTED,anchor="mm")
d.text((ann_x+50,ann_y+24),"(позиція i)",font=fs,fill=MUTED,anchor="mm")

# Bottom legend
ly=H-65
d.line([(30,ly-8),(W-30,ly-8)],fill=LINE,width=1)
d.text((30,ly),"Ключові факти про yield:",font=fh,fill=ACCENT)
facts=[
    "yield return — повертає один елемент і зупиняє виконання до наступного MoveNext()",
    "yield break  — завершує ітерацію достроково (аналог return у звичайному методі)",
    "Ліниве виконання: тіло методу не запускається, поки foreach не запросить перший елемент",
]
for i,f in enumerate(facts):
    d.text((30,ly+20+i*16),f"  {f}",font=fs,fill=TEXT)

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/10-08/yield-lazy-execution.png"
img.save(out); print("OK:",out)
