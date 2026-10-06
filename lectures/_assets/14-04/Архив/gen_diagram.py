# -*- coding: utf-8 -*-
# FieldInfo + PropertyInfo — reflection access to fields and properties
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

d.text((W//2,22),"FieldInfo та PropertyInfo — читання та запис значень через рефлексію",
       font=ft,fill=ACCENT,anchor="mm")

# ============================================================
# LEFT: FieldInfo
# ============================================================
lx=20; ly=42; lw=280; lh=316
d.rounded_rectangle([lx,ly,lx+lw,ly+lh],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((lx+lw//2,ly+13),"FieldInfo",font=fh,fill=ACCENT,anchor="mm")
d.line([(lx+6,ly+27),(lx+lw-6,ly+27)],fill=LINE,width=1)

field_props=[
    (".Name",           "ім'я поля"),
    (".FieldType",      "Type поля"),
    (".IsPublic",       "public"),
    (".IsPrivate",      "private"),
    (".IsStatic",       "static"),
    (".IsInitOnly",     "readonly"),
    (".IsLiteral",      "const (compile-time)"),
    (".IsNotSerialized","[NonSerialized]"),
    (".GetValue(obj)",  "прочитати значення"),
    (".SetValue(obj,v)","записати значення"),
]
fy=ly+34
for name,desc in field_props:
    d.rounded_rectangle([lx+8,fy-3,lx+lw-8,fy+13],radius=2,fill=DARK,outline=ACCENT,width=1)
    d.text((lx+12,fy+4),name,font=fcc,fill=ACCENT,anchor="lm")
    d.text((lx+12,fy+12),f"  // {desc}",font=fcc,fill=MUTED,anchor="lm")
    fy+=17

# IsLiteral / IsInitOnly note
note_y=ly+lh-64
d.rounded_rectangle([lx+8,note_y,lx+lw-8,note_y+56],radius=4,fill=DARK,outline=ORANGE,width=1)
d.text((lx+lw//2,note_y+9),"const vs readonly",font=fcc,fill=ORANGE,anchor="mm")
rows=[
    ("const",    "IsLiteral=true, IsInitOnly=false"),
    ("readonly", "IsLiteral=false, IsInitOnly=true"),
    ("static readonly","IsStatic=true, IsInitOnly=true"),
    ("SetValue на readonly","→ FieldAccessException"),
]
for j,(k,v) in enumerate(rows):
    d.text((lx+12,note_y+19+j*9),k,font=fcc,fill=ACCENT,anchor="lm")
    d.text((lx+80,note_y+19+j*9),v,font=fcc,fill=MUTED,anchor="lm")

# ============================================================
# MIDDLE: PropertyInfo
# ============================================================
mx=lx+lw+14; my=ly; mw=320; mh=lh
d.rounded_rectangle([mx,my,mx+mw,my+mh],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((mx+mw//2,my+13),"PropertyInfo",font=fh,fill=ORANGE,anchor="mm")
d.line([(mx+6,my+27),(mx+mw-6,my+27)],fill=LINE,width=1)

prop_props=[
    (".Name",           "ім'я властивості"),
    (".PropertyType",   "Type значення"),
    (".CanRead",        "є getter"),
    (".CanWrite",       "є setter"),
    (".IsSpecialName",  "обслуговуюча (рідко)"),
    (".GetMethod",      "MethodInfo? getter"),
    (".SetMethod",      "MethodInfo? setter"),
    (".GetValue(obj)",  "прочитати значення"),
    (".SetValue(obj,v)","записати значення"),
    (".GetIndexParameters()","індексатори"),
    (".GetAccessors()", "get + set як масив"),
]
py_=my+34
for name,desc in prop_props:
    d.rounded_rectangle([mx+8,py_-3,mx+mw-8,py_+13],radius=2,fill=DARK,outline=ORANGE,width=1)
    d.text((mx+12,py_+4),name,font=fcc,fill=ORANGE,anchor="lm")
    d.text((mx+12,py_+12),f"  // {desc}",font=fcc,fill=MUTED,anchor="lm")
    py_+=17

# init-only note
init_y=my+mh-64
d.rounded_rectangle([mx+8,init_y,mx+mw-8,init_y+56],radius=4,fill=DARK,outline=RED,width=1)
d.text((mx+mw//2,init_y+9),"init-only setter (C# 9)",font=fcc,fill=RED,anchor="mm")
init_rows=[
    "Name { get; init; }  → CanWrite = true",
    "SetMethod  → [IsExternalInit] attr",
    "SetValue через рефлексію  → FieldAccessException",
    "Обійти: SetValue на backing field",
]
for j,row in enumerate(init_rows):
    d.text((mx+12,init_y+19+j*9),row,font=fcc,fill=MUTED,anchor="lm")

# ============================================================
# RIGHT: GetValue/SetValue workflow + field vs property comparison
# ============================================================
rx=mx+mw+14; ry=my; rw=W-rx-20; rh=mh
d.rounded_rectangle([rx,ry,rx+rw,ry+rh],radius=8,fill=PANEL,outline=RED,width=2)
d.text((rx+rw//2,ry+13),"GetValue / SetValue workflow",font=fh,fill=RED,anchor="mm")
d.line([(rx+6,ry+27),(rx+rw-6,ry+27)],fill=LINE,width=1)

steps=[
    (ACCENT, "1. GetField / GetProperty","з BindingFlags"),
    (ORANGE, "2. Перевірити CanRead/CanWrite","(для Property)"),
    (RED,    "3. GetValue(instance)","→ object? (boxing)"),
    (ORANGE, "4. SetValue(instance, val)","val приводиться до типу"),
    (ACCENT, "5. Розкастити результат","(T)val або Convert.ChangeType"),
]
sy=ry+34
for col,title,note in steps:
    d.rounded_rectangle([rx+8,sy,rx+rw-8,sy+30],radius=4,fill=DARK,outline=col,width=2)
    d.text((rx+14,sy+9),title,font=fc,fill=col,anchor="lm")
    d.text((rx+14,sy+21),f"  {note}",font=fcc,fill=MUTED,anchor="lm")
    if sy+30 < ry+rh-100:
        arr_x=rx+rw//2
        d.line([(arr_x,sy+30),(arr_x,sy+38)],fill=MUTED,width=1)
        d.polygon([(arr_x-4,sy+36),(arr_x+4,sy+36),(arr_x,sy+42)],fill=MUTED)
    sy+=42

# Field vs Property comparison table
cmp_y=sy+6
d.rounded_rectangle([rx+8,cmp_y,rx+rw-8,cmp_y+74],radius=4,fill=DARK,outline=LINE,width=1)
d.text((rx+rw//2,cmp_y+9),"Field vs Property",font=fcc,fill=MUTED,anchor="mm")
cmp_rows=[
    ("Field",    "прямий доступ до пам'яті",    "швидко"),
    ("Property", "через get/set (може кидати)", "безпечно"),
    ("init-only","CanWrite=true, але SetValue fails","обходь полем"),
    ("const",    "GetValue(null) — static read",  "IsLiteral=true"),
]
for j,(kind,what,note) in enumerate(cmp_rows):
    d.text((rx+12, cmp_y+18+j*13),kind,font=fcc,fill=ORANGE,anchor="lm")
    d.text((rx+70, cmp_y+18+j*13),what,font=fcc,fill=TEXT,anchor="lm")
    d.text((rx+200,cmp_y+18+j*13),note,font=fcc,fill=MUTED,anchor="lm")

# ============================================================
# BOTTOM: Use cases
# ============================================================
bot_y=ly+lh+12; bot_h=68
d.rounded_rectangle([20,bot_y,W-20,bot_y+bot_h],radius=6,fill=PANEL,outline=ORANGE,width=1)
d.text((W//2,bot_y+11),"Практичне застосування",font=fh,fill=ORANGE,anchor="mm")
d.line([(30,bot_y+24),(W-30,bot_y+24)],fill=LINE,width=1)

cases=[
    ("Серіалізація\n(JSON/XML)","Читання всіх\nвластивостей\nGetValue → string"),
    ("ORM (EF Core)","Запис із БД\nSetValue для кожної\nколонки→властивості"),
    ("AutoMapper","Копіювання полів\nміж DTO і domain\nGetValue→SetValue"),
    ("Клонування","Deep copy через\nGetFields + GetValue\n+ SetValue нового obj"),
    ("Валідатори","Читання [Required]\nGetCustomAttributes\n+ GetValue ≠ null"),
]
uw=(W-50)//len(cases)
for i,(title,desc) in enumerate(cases):
    ux=28+i*uw
    d.text((ux,bot_y+30),title,font=fcc,fill=ACCENT,anchor="lm")
    for j,line in enumerate(desc.split("\n")):
        d.text((ux,bot_y+41+j*9),line,font=fcc,fill=TEXT,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/14-04/fields-properties.png"
img.save(out); print("OK:",out)
