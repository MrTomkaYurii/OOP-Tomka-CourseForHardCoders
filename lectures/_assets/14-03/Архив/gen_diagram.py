# -*- coding: utf-8 -*-
# MethodInfo + ConstructorInfo + Invoke workflow
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"; RED="#c77676"

W,H=960,560
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)
fcc=load("C:/Windows/Fonts/arial.ttf",9)

d.text((W//2,22),"MethodInfo та ConstructorInfo — виклик через рефлексію",
       font=ft,fill=ACCENT,anchor="mm")

# ============================================================
# LEFT: MethodInfo API
# ============================================================
lx=20; ly=42; lw=290; lh=310
d.rounded_rectangle([lx,ly,lx+lw,ly+lh],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((lx+lw//2,ly+13),"MethodInfo",font=fh,fill=ACCENT,anchor="mm")
d.line([(lx+6,ly+27),(lx+lw-6,ly+27)],fill=LINE,width=1)

method_props=[
    (".Name",           "ім'я методу"),
    (".ReturnType",     "Type повернення"),
    (".IsPublic",       "доступність"),
    (".IsStatic",       "чи статичний"),
    (".IsVirtual",      "чи virtual/override"),
    (".IsAbstract",     "чи abstract"),
    (".IsGenericMethod","чи generic"),
    (".GetParameters()","ParameterInfo[]"),
    (".GetGenericArguments()","Type[] для generic"),
    (".Invoke(obj, args)","виклик методу"),
]
my2=ly+34
for name,desc in method_props:
    d.rounded_rectangle([lx+8,my2-3,lx+lw-8,my2+13],radius=2,fill=DARK,outline=ACCENT,width=1)
    d.text((lx+12,my2+4),name,font=fcc,fill=ACCENT,anchor="lm")
    d.text((lx+12,my2+12),f"  // {desc}",font=fcc,fill=MUTED,anchor="lm")
    my2+=18

# Invoke signature
inv_y=ly+lh-46
d.rounded_rectangle([lx+8,inv_y,lx+lw-8,inv_y+38],radius=4,fill=DARK,outline=ORANGE,width=1)
d.text((lx+lw//2,inv_y+9),"Invoke(object? obj, object?[]? args)",font=fcc,fill=ORANGE,anchor="mm")
d.text((lx+lw//2,inv_y+21),"obj = null → static method",font=fcc,fill=MUTED,anchor="mm")
d.text((lx+lw//2,inv_y+31),"args = null/[] → no parameters",font=fcc,fill=MUTED,anchor="mm")

# ============================================================
# MIDDLE: ParameterInfo + ConstructorInfo
# ============================================================
mx2=lx+lw+14; my3=ly; mw2=320; mh2=lh
d.rounded_rectangle([mx2,my3,mx2+mw2,my3+mh2],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((mx2+mw2//2,my3+13),"ParameterInfo  та  ConstructorInfo",font=fh,fill=ORANGE,anchor="mm")
d.line([(mx2+6,my3+27),(mx2+mw2-6,my3+27)],fill=LINE,width=1)

# ParameterInfo block
d.text((mx2+mw2//2,my3+38),"ParameterInfo",font=fc,fill=ORANGE,anchor="mm")
param_props=[
    (".Name",           "ім'я параметра"),
    (".ParameterType",  "Type параметра"),
    (".Position",       "індекс у сигнатурі"),
    (".IsOptional",     "чи має default value"),
    (".DefaultValue",   "значення за замовч."),
    (".IsOut",          "out-параметр"),
    (".IsIn",           "in-параметр"),
]
py3=my3+50
for name,desc in param_props:
    d.rounded_rectangle([mx2+8,py3-3,mx2+mw2-8,py3+12],radius=2,fill=DARK,outline=ORANGE,width=1)
    d.text((mx2+12,py3+4),name,font=fcc,fill=ORANGE,anchor="lm")
    d.text((mx2+130,py3+4),f"// {desc}",font=fcc,fill=MUTED,anchor="lm")
    py3+=16

# Separator
d.line([(mx2+10,py3+5),(mx2+mw2-10,py3+5)],fill=LINE,width=1)

# ConstructorInfo block
d.text((mx2+mw2//2,py3+16),"ConstructorInfo",font=fc,fill=RED,anchor="mm")
ctor_props=[
    (".Name",              "завжди \".ctor\""),
    (".IsPublic",          "доступність"),
    (".IsStatic",          "статичний конструктор"),
    (".GetParameters()",   "ParameterInfo[]"),
    (".Invoke(args)",      "створює об'єкт"),
    ("Activator.CreateInstance(t)","спрощений виклик"),
]
py4=py3+28
for name,desc in ctor_props:
    d.rounded_rectangle([mx2+8,py4-3,mx2+mw2-8,py4+12],radius=2,fill=DARK,outline=RED,width=1)
    d.text((mx2+12,py4+4),name,font=fcc,fill=RED,anchor="lm")
    d.text((mx2+170,py4+4),f"// {desc}",font=fcc,fill=MUTED,anchor="lm")
    py4+=16

# ============================================================
# RIGHT: Invoke workflow diagram
# ============================================================
rx=mx2+mw2+14; ry=my3; rw=W-rx-20; rh=lh
d.rounded_rectangle([rx,ry,rx+rw,ry+rh],radius=8,fill=PANEL,outline=RED,width=2)
d.text((rx+rw//2,ry+13),"Workflow виклику через Invoke",font=fh,fill=RED,anchor="mm")
d.line([(rx+6,ry+27),(rx+rw-6,ry+27)],fill=LINE,width=1)

steps=[
    (ACCENT, "1. Отримати Type",      "typeof(T) / obj.GetType()"),
    (ORANGE, "2. GetMethod(name)",    "→ MethodInfo?"),
    (ORANGE, "3. GetParameters()",   "перевірити сигнатуру"),
    (RED,    "4. Invoke(obj, args)",  "object?[] з аргументами"),
    (ACCENT, "5. Розкастити результат","(T)result  / as T"),
]
sy=ry+34
for col,title,note in steps:
    d.rounded_rectangle([rx+8,sy,rx+rw-8,sy+32],radius=4,fill=DARK,outline=col,width=2)
    d.text((rx+14,sy+9),title,font=fc,fill=col,anchor="lm")
    d.text((rx+14,sy+21),note,font=fcc,fill=MUTED,anchor="lm")
    if sy+32 < ry+rh-50:
        arr_x=rx+rw//2
        d.line([(arr_x,sy+32),(arr_x,sy+40)],fill=MUTED,width=1)
        d.polygon([(arr_x-4,sy+38),(arr_x+4,sy+38),(arr_x,sy+44)],fill=MUTED)
    sy+=46

# Exception note
exc_y=ry+rh-55
d.rounded_rectangle([rx+8,exc_y,rx+rw-8,exc_y+48],radius=4,fill=DARK,outline=RED,width=1)
d.text((rx+rw//2,exc_y+10),"Виключення Invoke",font=fcc,fill=RED,anchor="mm")
exc=[
    "TargetInvocationException   // обгортка реального exc.",
    "  .InnerException            // справжня причина",
    "ArgumentException            // неправильний тип арг.",
    "TargetParameterCountException// кількість аргументів",
]
for j,line in enumerate(exc):
    d.text((rx+12,exc_y+20+j*8),line,font=fcc,fill=MUTED,anchor="lm")

# ============================================================
# BOTTOM: Invoke vs direct call performance note + generic
# ============================================================
bot_y=ly+lh+12; bot_h=72
d.rounded_rectangle([20,bot_y,W-20,bot_y+bot_h],radius=6,fill=PANEL,outline=ORANGE,width=1)
d.text((W//2,bot_y+11),"Продуктивність та Generic-методи",font=fh,fill=ORANGE,anchor="mm")
d.line([(30,bot_y+24),(W-30,bot_y+24)],fill=LINE,width=1)

perf=[
    ("Прямий виклик","~1 нс","компілятор вбудовує"),
    ("Invoke","~200–500 нс","boxing args, security check"),
    ("Cached MethodInfo","~150–300 нс","зберігати MethodInfo, не шукати щоразу"),
    ("Delegate via CreateDelegate","~5–20 нс","найкращий варіант для гарячого шляху"),
]
pw=(W-50)//len(perf)
for i,(method,time,note) in enumerate(perf):
    px=28+i*pw
    d.text((px,bot_y+30),method,font=fcc,fill=ACCENT,anchor="lm")
    d.text((px,bot_y+40),time,font=fc,fill=ORANGE,anchor="lm")
    d.text((px,bot_y+52),note,font=fcc,fill=MUTED,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/14-03/methods-constructors.png"
img.save(out); print("OK:",out)
