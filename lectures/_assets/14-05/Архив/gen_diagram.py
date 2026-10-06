# -*- coding: utf-8 -*-
# Assembly loading: Assembly class, AppDomain, AssemblyLoadContext, plugin pattern
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

d.text((W//2,22),"Динамічне завантаження збірок — Assembly та AssemblyLoadContext",
       font=ft,fill=ACCENT,anchor="mm")

# ============================================================
# LEFT: Assembly class API
# ============================================================
lx=20; ly=42; lw=280; lh=314
d.rounded_rectangle([lx,ly,lx+lw,ly+lh],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((lx+lw//2,ly+13),"Клас Assembly",font=fh,fill=ACCENT,anchor="mm")
d.line([(lx+6,ly+27),(lx+lw-6,ly+27)],fill=LINE,width=1)

# Load methods
d.text((lx+lw//2,ly+38),"Завантаження",font=fcc,fill=MUTED,anchor="mm")
load_methods=[
    ("Assembly.Load(name)",        "з GAC / NuGet cache"),
    ("Assembly.LoadFrom(path)",    "з файлу .dll / .exe"),
    ("Assembly.LoadFile(path)",    "повний шлях, ізольовано"),
    ("Assembly.GetEntryAssembly()","стартова збірка"),
    ("Assembly.GetCallingAssembly()","збірка-викликач"),
    ("Assembly.GetExecutingAssembly()","поточна збірка"),
]
ay=ly+48
for name,desc in load_methods:
    d.rounded_rectangle([lx+8,ay-3,lx+lw-8,ay+13],radius=2,fill=DARK,outline=ACCENT,width=1)
    d.text((lx+12,ay+4),name,font=fcc,fill=ACCENT,anchor="lm")
    d.text((lx+12,ay+12),f"  // {desc}",font=fcc,fill=MUTED,anchor="lm")
    ay+=17

d.line([(lx+10,ay+2),(lx+lw-10,ay+2)],fill=LINE,width=1)

# Assembly properties
d.text((lx+lw//2,ay+12),"Властивості",font=fcc,fill=MUTED,anchor="mm")
asm_props=[
    (".FullName",        "AssemblyQualifiedName"),
    (".GetName().Version","Version об'єкт"),
    (".Location",        "шлях до .dll файлу"),
    (".GetTypes()",      "всі типи збірки"),
    (".GetExportedTypes()","тільки public типи"),
    (".GetType(name)",   "знайти тип за ім'ям"),
    (".GetCustomAttributes()","атрибути збірки"),
]
ay+=22
for name,desc in asm_props:
    d.rounded_rectangle([lx+8,ay-3,lx+lw-8,ay+13],radius=2,fill=DARK,outline=LINE,width=1)
    d.text((lx+12,ay+4),name,font=fcc,fill=ORANGE,anchor="lm")
    d.text((lx+12,ay+12),f"  // {desc}",font=fcc,fill=MUTED,anchor="lm")
    ay+=17

# ============================================================
# MIDDLE: AssemblyLoadContext (ALC)
# ============================================================
mx=lx+lw+14; my=ly; mw=310; mh=lh
d.rounded_rectangle([mx,my,mx+mw,my+mh],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((mx+mw//2,my+13),"AssemblyLoadContext (.NET Core+)",font=fh,fill=ORANGE,anchor="mm")
d.line([(mx+6,my+27),(mx+mw-6,my+27)],fill=LINE,width=1)

alc_items=[
    ("AssemblyLoadContext.Default",  "стандартний контекст"),
    ("new PluginLoadContext(path)",  "ізольований контекст"),
    (".LoadFromAssemblyPath(path)",  "завантажити в контекст"),
    (".LoadFromStream(stream)",      "з байтового потоку"),
    (".Unload()",                    "вивантажити збірки контексту"),
    ("IsCollectible = true",         "дозволити GC зібрати збірку"),
]
cy=my+34
for name,desc in alc_items:
    d.rounded_rectangle([mx+8,cy-3,mx+mw-8,cy+13],radius=2,fill=DARK,outline=ORANGE,width=1)
    d.text((mx+12,cy+4),name,font=fcc,fill=ORANGE,anchor="lm")
    d.text((mx+12,cy+12),f"  // {desc}",font=fcc,fill=MUTED,anchor="lm")
    cy+=17

# LoadFrom vs LoadFile vs ALC table
d.line([(mx+10,cy+4),(mx+mw-10,cy+4)],fill=LINE,width=1)
d.text((mx+mw//2,cy+14),"Порівняння методів завантаження",font=fcc,fill=MUTED,anchor="mm")
cy+=24
cmp=[
    ("LoadFrom",     "GAC sharing, dependency resolve"),
    ("LoadFile",     "ізольовано, без GAC sharing"),
    ("ALC + path",   "повна ізоляція + Unload"),
    ("LoadFrom stream","з пам'яті, без файлу на диску"),
]
for method,note in cmp:
    d.rounded_rectangle([mx+8,cy-3,mx+mw-8,cy+20],radius=3,fill=DARK,outline=LINE,width=1)
    d.text((mx+12,cy+4),method,font=fcc,fill=ORANGE,anchor="lm")
    d.text((mx+12,cy+13),f"  {note}",font=fcc,fill=MUTED,anchor="lm")
    cy+=23

# Unload warning
uw_y=my+mh-48
d.rounded_rectangle([mx+8,uw_y,mx+mw-8,uw_y+40],radius=4,fill=DARK,outline=RED,width=1)
d.text((mx+mw//2,uw_y+9),"Unload — умови",font=fcc,fill=RED,anchor="mm")
d.text((mx+12,uw_y+19),"IsCollectible=true при створенні ALC",font=fcc,fill=MUTED,anchor="lm")
d.text((mx+12,uw_y+29),"Усі посилання на типи збірки знищено",font=fcc,fill=MUTED,anchor="lm")

# ============================================================
# RIGHT: Plugin pattern diagram
# ============================================================
rx=mx+mw+14; ry=my; rw=W-rx-20; rh=mh
d.rounded_rectangle([rx,ry,rx+rw,ry+rh],radius=8,fill=PANEL,outline=RED,width=2)
d.text((rx+rw//2,ry+13),"Патерн Plugin через рефлексію",font=fh,fill=RED,anchor="mm")
d.line([(rx+6,ry+27),(rx+rw-6,ry+27)],fill=LINE,width=1)

steps=[
    (ACCENT, "1. Визначити інтерфейс",       "IAnalysisPlugin у host-збірці"),
    (ORANGE, "2. Завантажити .dll",           "AssemblyLoadContext.LoadFromPath"),
    (ORANGE, "3. GetExportedTypes()",         "всі public типи плагіна"),
    (RED,    "4. Фільтрувати по інтерфейсу", "IsAssignableTo(typeof(IPlugin))"),
    (ACCENT, "5. Activator.CreateInstance",   "створити об'єкт плагіна"),
    (ACCENT, "6. Привести до інтерфейсу",     "(IPlugin)instance  →  .Execute()"),
]
sy=ry+34
for col,title,note in steps:
    d.rounded_rectangle([rx+8,sy,rx+rw-8,sy+30],radius=4,fill=DARK,outline=col,width=2)
    d.text((rx+14,sy+9),title,font=fc,fill=col,anchor="lm")
    d.text((rx+14,sy+21),f"  {note}",font=fcc,fill=MUTED,anchor="lm")
    if sy+30 < ry+rh-60:
        arr_x=rx+rw//2
        d.line([(arr_x,sy+30),(arr_x,sy+38)],fill=MUTED,width=1)
        d.polygon([(arr_x-4,sy+36),(arr_x+4,sy+36),(arr_x,sy+42)],fill=MUTED)
    sy+=42

# IsAssignableTo note
note_y=ry+rh-54
d.rounded_rectangle([rx+8,note_y,rx+rw-8,note_y+46],radius=4,fill=DARK,outline=ORANGE,width=1)
d.text((rx+rw//2,note_y+9),"Перевірка відповідності типу",font=fcc,fill=ORANGE,anchor="mm")
checks=[
    ("IsAssignableTo(T)",      "чи реалізує тип T"),
    ("IsSubclassOf(T)",        "чи є нащадком T"),
    ("GetInterface(name)",     "чи реалізує інтерфейс"),
    ("!t.IsAbstract && !t.IsInterface","лише конкретні типи"),
]
for j,(k,v) in enumerate(checks):
    d.text((rx+12,note_y+18+j*7),k,font=fcc,fill=ACCENT,anchor="lm")
    d.text((rx+130,note_y+18+j*7),v,font=fcc,fill=MUTED,anchor="lm")

# ============================================================
# BOTTOM
# ============================================================
bot_y=ly+lh+12; bot_h=68
d.rounded_rectangle([20,bot_y,W-20,bot_y+bot_h],radius=6,fill=PANEL,outline=ORANGE,width=1)
d.text((W//2,bot_y+11),"Де застосовується динамічне завантаження",font=fh,fill=ORANGE,anchor="mm")
d.line([(30,bot_y+24),(W-30,bot_y+24)],fill=LINE,width=1)

cases=[
    ("Плагінні системи","MEF, MAF,\nвласні plugin\nloaders"),
    ("Тестові раннери","NUnit/xUnit завант.\nтестову збірку і\nшукають [Test] методи"),
    ("Hot reload","Zavant. нової версії\nbez restartu (ALC\n+ Unload старої)"),
    ("DI-контейнери","Scan збірок для\nреєстрації всіх\nIService-реалізацій"),
    ("Code generation","Roslyn генерує .dll\nв пам'яті, ALC\nзавантажує результат"),
]
uw=(W-50)//len(cases)
for i,(title,desc) in enumerate(cases):
    ux=28+i*uw
    d.text((ux,bot_y+30),title,font=fcc,fill=ACCENT,anchor="lm")
    for j,line in enumerate(desc.split("\n")):
        d.text((ux,bot_y+40+j*9),line,font=fcc,fill=TEXT,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/14-05/assembly-loading.png"
img.save(out); print("OK:",out)
