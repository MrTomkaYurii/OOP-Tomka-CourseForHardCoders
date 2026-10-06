# -*- coding: utf-8 -*-
# Reflection overview: CLR metadata model + 3 ways to get Type + use cases
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"; RED="#c77676"

W,H=960,540
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)
fcc=load("C:/Windows/Fonts/arial.ttf",9)

d.text((W//2,22),"Рефлексія: модель метаданих CLR та клас System.Type",
       font=ft,fill=ACCENT,anchor="mm")

# ============================================================
# LEFT: CLR metadata model — Assembly → Module → Type → Members
# ============================================================
mx=20; my=42; mw=340; mh=300
d.rounded_rectangle([mx,my,mx+mw,my+mh],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((mx+mw//2,my+13),"Модель метаданих CLR",font=fh,fill=ACCENT,anchor="mm")
d.line([(mx+6,my+27),(mx+mw-6,my+27)],fill=LINE,width=1)

# Assembly box
ax=mx+10; ay=my+34; aw=mw-20; ah=30
d.rounded_rectangle([ax,ay,ax+aw,ay+ah],radius=5,fill=DARK,outline=ORANGE,width=2)
d.text((ax+aw//2,ay+ah//2),"Assembly  (.dll / .exe)",font=fc,fill=ORANGE,anchor="mm")
d.text((ax+6,ay+ah//2+1),"MyMedApp.dll",font=fcc,fill=MUTED,anchor="lm")

# Arrow
arr_x=ax+aw//2
for yy in range(ay+ah+2, ay+ah+14, 3):
    d.point((arr_x,yy),fill=MUTED)
d.polygon([(arr_x-5,ay+ah+14),(arr_x+5,ay+ah+14),(arr_x,ay+ah+20)],fill=MUTED)

# Module box
my2=ay+ah+22; mh2=24
d.rounded_rectangle([ax,my2,ax+aw,my2+mh2],radius=5,fill=DARK,outline=MUTED,width=1)
d.text((ax+aw//2,my2+mh2//2),"Module  (зазвичай один на збірку)",font=fcc,fill=MUTED,anchor="mm")

for yy in range(my2+mh2+2, my2+mh2+14, 3):
    d.point((arr_x,yy),fill=MUTED)
d.polygon([(arr_x-5,my2+mh2+14),(arr_x+5,my2+mh2+14),(arr_x,my2+mh2+20)],fill=MUTED)

# Types box
ty2=my2+mh2+22; th2=26
d.rounded_rectangle([ax,ty2,ax+aw,ty2+th2],radius=5,fill=DARK,outline=ACCENT,width=2)
d.text((ax+aw//2,ty2+th2//2),"System.Type  (клас, структура, інтерфейс, enum…)",font=fcc,fill=ACCENT,anchor="mm")

# Members fanout
mem_y=ty2+th2+18
members=[
    ("MethodInfo[]","GetMethods()",ACCENT),
    ("ConstructorInfo[]","GetConstructors()",ORANGE),
    ("FieldInfo[]","GetFields()",RED),
    ("PropertyInfo[]","GetProperties()",ACCENT),
    ("EventInfo[]","GetEvents()",MUTED),
]
box_w=58; box_h=28; gap=4
total_w=len(members)*(box_w+gap)-gap
start_x=ax+(aw-total_w)//2
# fan lines
for i,(cls,method,col) in enumerate(members):
    bx=start_x+i*(box_w+gap); by=mem_y
    mid=(bx+box_w//2)
    d.line([(arr_x,ty2+th2),(mid,by-4)],fill=LINE,width=1)
    d.rounded_rectangle([bx,by,bx+box_w,by+box_h],radius=3,fill=DARK,outline=col,width=1)
    d.text((bx+box_w//2,by+9),cls,font=fcc,fill=col,anchor="mm")
    d.text((bx+box_w//2,by+20),method,font=fcc,fill=MUTED,anchor="mm")

# MemberInfo base note
note_y=mem_y+box_h+8
d.rounded_rectangle([ax,note_y,ax+aw,note_y+22],radius=3,fill=DARK,outline=LINE,width=1)
d.text((ax+aw//2,note_y+11),"MemberInfo — базовий клас для всіх вище",font=fcc,fill=MUTED,anchor="mm")

# ============================================================
# MIDDLE: 3 ways to get Type
# ============================================================
gx=mx+mw+14; gy=my; gw=270; gh=mh
d.rounded_rectangle([gx,gy,gx+gw,gy+gh],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((gx+gw//2,gy+13),"3 способи отримати Type",font=fh,fill=ORANGE,anchor="mm")
d.line([(gx+6,gy+27),(gx+gw-6,gy+27)],fill=LINE,width=1)

ways=[
    {
        "num":"1",
        "title":"typeof(T)",
        "sub":"compile-time, T відомий",
        "code":["Type t = typeof(PatientRecord);","// Тип відомий на етапі","// компіляції — найшвидший"],
        "col":ACCENT,
        "note":"Помилка компіляції якщо T невідомий"
    },
    {
        "num":"2",
        "title":"obj.GetType()",
        "sub":"runtime, є екземпляр",
        "code":["var p = new PatientRecord();","Type t = p.GetType();","// Фактичний тип об'єкта"],
        "col":ORANGE,
        "note":"Поліморфний: дає похідний тип"
    },
    {
        "num":"3",
        "title":"Type.GetType(name)",
        "sub":"runtime, є рядок імені",
        "code":["Type? t = Type.GetType(","  \"MyNS.PatientRecord\");","// null якщо не знайдено"],
        "col":RED,
        "note":"Потрібне повне ім'я з namespace"
    },
]
wy=gy+32
for way in ways:
    col=way["col"]
    d.rounded_rectangle([gx+8,wy,gx+gw-8,wy+72],radius=4,fill=DARK,outline=col,width=1)
    d.text((gx+14,wy+8),f"{way['num']}. {way['title']}",font=fc,fill=col,anchor="lm")
    d.text((gx+14,wy+20),f"   {way['sub']}",font=fcc,fill=MUTED,anchor="lm")
    for i,line in enumerate(way["code"]):
        d.text((gx+14,wy+30+i*10),line,font=fcc,fill=TEXT,anchor="lm")
    d.text((gx+14,wy+62),f"! {way['note']}",font=fcc,fill=MUTED,anchor="lm")
    wy+=78

# ============================================================
# RIGHT: Type properties table + use cases
# ============================================================
rx=gx+gw+14; ry=my; rw=W-rx-20; rh=mh
d.rounded_rectangle([rx,ry,rx+rw,ry+rh],radius=8,fill=PANEL,outline=RED,width=2)
d.text((rx+rw//2,ry+13),"Властивості System.Type",font=fh,fill=RED,anchor="mm")
d.line([(rx+6,ry+27),(rx+rw-6,ry+27)],fill=LINE,width=1)

props=[
    (".Name",       "коротке ім'я: \"PatientRecord\""),
    (".FullName",   "з namespace: \"Med.PatientRecord\""),
    (".Namespace",  "простір імен"),
    (".Assembly",   "збірка де визначено тип"),
    (".BaseType",   "базовий клас (Type?)"),
    (".IsClass",    "true якщо клас"),
    (".IsValueType","true якщо struct/enum"),
    (".IsInterface","true якщо інтерфейс"),
    (".IsAbstract", "true якщо abstract"),
    (".IsGenericType","true якщо List<T> тощо"),
    (".IsArray",    "true якщо масив"),
    (".IsEnum",     "true якщо enum"),
]
py2=ry+32
for name,desc in props:
    d.rounded_rectangle([rx+5,py2-3,rx+rw-5,py2+13],radius=2,fill=DARK,outline=LINE,width=1)
    d.text((rx+9,py2+4),name,font=fcc,fill=RED,anchor="lm")
    d.text((rx+rw//2+4,py2+4),f"// {desc}",font=fcc,fill=MUTED,anchor="lm")
    py2+=17

# ============================================================
# BOTTOM: Where reflection is used
# ============================================================
bot_y=my+mh+12; bot_h=72
d.rounded_rectangle([20,bot_y,W-20,bot_y+bot_h],radius=6,fill=PANEL,outline=ORANGE,width=1)
d.text((W//2,bot_y+12),"Де застосовується рефлексія",font=fh,fill=ORANGE,anchor="mm")
d.line([(30,bot_y+26),(W-30,bot_y+26)],fill=LINE,width=1)

use_cases=[
    ("DI-контейнери","Autofac/DI сканують типи,\nзнаходять конструктори, \nінжектують залежності"),
    ("ORM (EF Core)","Відображають властивості\nкласу на колонки БД,\nчитають/записують поля"),
    ("Серіалізація","JSON/XML читають\nвластивості типу,\nконвертують у рядок"),
    ("Тестові фреймворки","NUnit/xUnit знаходять\nметоди з [Test],\nвикликають через Invoke"),
    ("Плагіни","Завантаження сторонніх\nзбірок, пошук типів\nзо інтерфейсом"),
]
uw=( W-50)//len(use_cases)
for i,(title,desc) in enumerate(use_cases):
    ux=28+i*uw
    d.text((ux,bot_y+30),title,font=fcc,fill=ACCENT,anchor="lm")
    for j,line in enumerate(desc.split("\n")):
        d.text((ux,bot_y+41+j*10),line,font=fcc,fill=TEXT,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/14-01/reflection-type.png"
img.save(out); print("OK:",out)
