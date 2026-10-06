# -*- coding: utf-8 -*-
# Lazy<T> — eager vs lazy init timeline + IsValueCreated + thread-safety modes
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"; RED="#c77676"

W,H=960,490
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11)
ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)

d.text((W//2,22),"Lazy<T> — відкладена ініціалізація: Eager vs Lazy",
       font=ft,fill=ACCENT,anchor="mm")

# === TOP: Timeline comparison
tl_y = 50; tl_h = 130

# Eager
ex, ew = 20, 440
d.rounded_rectangle([ex,tl_y,ex+ew,tl_y+tl_h],radius=8,fill=PANEL,outline=RED,width=2)
d.text((ex+ew//2,tl_y+13),"EAGER (звичайне поле)",font=fh,fill=RED,anchor="mm")
d.line([(ex+8,tl_y+27),(ex+ew-8,tl_y+27)],fill=LINE,width=1)

# Timeline line
tl_start=ex+20; tl_end=ex+ew-20; tl_mid=tl_y+70
d.line([(tl_start,tl_mid),(tl_end,tl_mid)],fill=MUTED,width=2)
d.polygon([(tl_end,tl_mid-5),(tl_end+8,tl_mid),(tl_end,tl_mid+5)],fill=MUTED)

# Events on eager timeline
events_e=[
    (tl_start+20, "Старт", "new HeavyObj()\nстворюється ЗАВЖДИ", RED),
    (tl_start+180,"ReadBook()\nвикликано","obj.Method()",ACCENT),
    (tl_start+320,"ReadEbook()\nвикликано","obj не потрібен\nале вже в пам'яті",MUTED),
]
for x,label,note,col in events_e:
    d.line([(x,tl_mid-20),(x,tl_mid+20)],fill=col,width=2)
    d.text((x,tl_mid-28),label,font=fc,fill=col,anchor="mm")
    for i,line in enumerate(note.split("\n")):
        d.text((x,tl_mid+30+i*12),line,font=fc,fill=col,anchor="mm")

# Lazy
lx = ex+ew+20; lw = W-lx-20
d.rounded_rectangle([lx,tl_y,lx+lw,tl_y+tl_h],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((lx+lw//2,tl_y+13),"LAZY (Lazy<T>)",font=fh,fill=ACCENT,anchor="mm")
d.line([(lx+8,tl_y+27),(lx+lw-8,tl_y+27)],fill=LINE,width=1)

ll_start=lx+20; ll_end=lx+lw-20
d.line([(ll_start,tl_mid),(ll_end,tl_mid)],fill=MUTED,width=2)
d.polygon([(ll_end,tl_mid-5),(ll_end+8,tl_mid),(ll_end,tl_mid+5)],fill=MUTED)

events_l=[
    (ll_start+20,  "Старт","Lazy<T> wrapper\nLightweight",ACCENT),
    (ll_start+110, "ReadEbook()\nвикликано","Value не чіпаємо\nоб'єкт = null",MUTED),
    (ll_start+230, "ReadBook()\nвикликано","Value! → new HeavyObj()\nСтворюється ТЕПЕР",ORANGE),
    (ll_start+340, "ReadBook()\nще раз","Value cached\nшвидко",ACCENT),
]
for x,label,note,col in events_l:
    d.line([(x,tl_mid-20),(x,tl_mid+20)],fill=col,width=2)
    d.text((x,tl_mid-28),label,font=fc,fill=col,anchor="mm")
    for i,line in enumerate(note.split("\n")):
        d.text((x,tl_mid+30+i*12),line,font=fc,fill=col,anchor="mm")

# === MIDDLE: API + thread modes side by side
my = tl_y+tl_h+14

# API panel
ax,aw=20,380
d.rounded_rectangle([ax,my,ax+aw,my+200],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((ax+aw//2,my+13),"API класу Lazy<T>",font=fh,fill=ORANGE,anchor="mm")
d.line([(ax+8,my+27),(ax+aw-8,my+27)],fill=LINE,width=1)

apis=[
    ("Lazy<T>()",                     "конструктор (потребує new T())"),
    ("Lazy<T>(() => new T(...))",     "з фабричною функцією"),
    ("Lazy<T>(factory, safetyMode)", "з режимом безпеки потоків"),
    (".Value",                         "перший доступ — створює; далі кеш"),
    (".IsValueCreated",                "bool — чи вже створено (без тригеру)"),
]
for i,(name,desc) in enumerate(apis):
    iy=my+36+i*30
    d.rounded_rectangle([ax+6,iy-10,ax+aw-6,iy+16],radius=4,fill=DARK,outline=LINE,width=1)
    d.text((ax+14,iy),name,font=fs,fill=ACCENT,anchor="lm")
    d.text((ax+14,iy+10),f"  // {desc}",font=fc,fill=MUTED,anchor="lm")

# Thread safety modes
tx=ax+aw+20; tw=260
d.rounded_rectangle([tx,my,tx+tw,my+200],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((tx+tw//2,my+13),"LazyThreadSafetyMode",font=fh,fill=ACCENT,anchor="mm")
d.line([(tx+8,my+27),(tx+tw-8,my+27)],fill=LINE,width=1)

modes=[
    ("ExecutionAndPublication","за замовчуванням","тільки один потік створює\nін. чекають — безпечно"),
    ("PublicationOnly",        "дозволяє кілька","кілька потоків можуть\nстворити, один збережеться"),
    ("None",                   "без синхронізації","найшвидший, небезпечний\nдля однопотокового"),
]
for i,(mode,comment,desc) in enumerate(modes):
    iy=my+38+i*54
    d.rounded_rectangle([tx+6,iy-10,tx+tw-6,iy+42],radius=4,fill=DARK,outline=LINE,width=1)
    d.text((tx+12,iy),mode,font=fs,fill=ORANGE,anchor="lm")
    d.text((tx+tw-10,iy),comment,font=fc,fill=MUTED,anchor="rm")
    for li,line in enumerate(desc.split("\n")):
        d.text((tx+12,iy+14+li*12),line,font=fc,fill=TEXT,anchor="lm")

# Clinical example
cx=tx+tw+20; cw=W-cx-20
d.rounded_rectangle([cx,my,cx+cw,my+200],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((cx+cw//2,my+13),"Клінічний приклад",font=fh,fill=ACCENT,anchor="mm")
d.line([(cx+8,my+27),(cx+cw-8,my+27)],fill=LINE,width=1)

code=[
    "class PatientRecord",
    "{",
    "  // Важкий об'єкт — завантаж. тільки",
    "  // якщо лікар відкриє повну картку",
    "  Lazy<string[]> _history",
    "    = new Lazy<string[]>(",
    "        () => LoadFullHistory());",
    "",
    "  // Легке поле — завжди потрібне",
    "  public string Name { get; }",
    "",
    "  public string[] GetHistory()",
    "    => _history.Value; // тригер",
    "}",
]
for i,line in enumerate(code):
    col=MUTED if line.startswith("  //") else (ORANGE if "Lazy" in line else (ACCENT if "=>" in line else TEXT))
    d.text((cx+8,my+34+i*11),line,font=fc,fill=col,anchor="lm")

# Bottom: when to use
by=my+214
d.rounded_rectangle([20,by,W-20,by+64],radius=6,fill=PANEL,outline=ORANGE,width=1)
d.text((W//2,by+12),"Коли застосовувати Lazy<T>",font=fh,fill=ORANGE,anchor="mm")
d.line([(30,by+26),(W-30,by+26)],fill=LINE,width=1)
tips=[
    "Важкий об'єкт (DB-з'єднання, великий кеш, парсер файлу) — використовується лише частиною сценаріїв",
    "Singleton — один екземпляр на весь застосунок, створений потокобезпечно при першому зверненні",
]
for i,tip in enumerate(tips):
    d.text((30,by+32+i*14),f"• {tip}",font=fc,fill=TEXT,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/13-01/lazy-init.png"
img.save(out); print("OK:",out)
