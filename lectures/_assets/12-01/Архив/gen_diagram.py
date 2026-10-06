# -*- coding: utf-8 -*-
# DateTime — struct overview: ticks, Kind, UTC vs Local, properties
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"; RED="#c77676"

W,H=960,500
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11)
ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)

d.text((W//2,22),"Структура DateTime — внутрішня будова та ключові властивості",
       font=ft,fill=ACCENT,anchor="mm")

# === TOP: Ticks concept
tx,ty,tw,th=20,44,W-40,66
d.rounded_rectangle([tx,ty,tx+tw,ty+th],radius=6,fill=PANEL,outline=ORANGE,width=2)
d.text((tx+10,ty+12),"Внутрішнє представлення: Ticks",font=fh,fill=ORANGE)
d.text((tx+10,ty+28),"1 Tick = 100 наносекунд  |  DateTime = ціле число Ticks від 01.01.0001 00:00:00",font=fs,fill=TEXT)
d.text((tx+10,ty+44),'DateTime d = new DateTime(2026,6,11);  //  d.Ticks = 638 546 304 000 000 000',font=fs,fill=ACCENT)

# === LEFT: Properties
lx,lt,lw=20,125,290
d.rounded_rectangle([lx,lt,lx+lw,lt+266],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((lx+lw//2,lt+13),"Властивості екземпляра",font=fh,fill=ACCENT,anchor="mm")
d.line([(lx+8,lt+27),(lx+lw-8,lt+27)],fill=LINE,width=1)

props=[
    ("Year / Month / Day",   "рік, місяць, день"),
    ("Hour / Minute / Second","година, хвилина, секунда"),
    ("Millisecond",          "мілісекунди (0–999)"),
    ("Ticks",                "тіки з 01.01.0001"),
    ("DayOfWeek",            "день тижня (enum)"),
    ("DayOfYear",            "номер дня у році"),
    ("TimeOfDay",            "час як TimeSpan"),
    ("Date",                 "дата без часу (DateTime)"),
    ("Kind",                 "Unspecified / Local / Utc"),
]
for i,(name,desc) in enumerate(props):
    iy=lt+34+i*25
    d.text((lx+8,iy),name,font=fs,fill=ORANGE,anchor="lm")
    d.text((lx+8,iy+11),f"  {desc}",font=fc,fill=MUTED,anchor="lm")

# === MIDDLE: Static
mx=lx+lw+20; mw=250
d.rounded_rectangle([mx,lt,mx+mw,lt+120],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((mx+mw//2,lt+13),"Статичні властивості",font=fh,fill=ACCENT,anchor="mm")
d.line([(mx+8,lt+27),(mx+mw-8,lt+27)],fill=LINE,width=1)

statics=[
    ("DateTime.Now",    "поточна дата+час (Local)"),
    ("DateTime.UtcNow", "поточна дата+час (UTC)"),
    ("DateTime.Today",  "поточна дата, час = 0:00"),
    ("DateTime.MinValue","01.01.0001 00:00:00"),
    ("DateTime.MaxValue","31.12.9999 23:59:59"),
]
for i,(name,desc) in enumerate(statics):
    iy=lt+36+i*16
    d.text((mx+8,iy),name,font=fs,fill=ACCENT,anchor="lm")
    d.text((mx+8,iy+8),f"  → {desc}",font=fc,fill=MUTED,anchor="lm")

# Kind panel
d.rounded_rectangle([mx,lt+130,mx+mw,lt+266],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((mx+mw//2,lt+143),"DateTimeKind",font=fh,fill=ORANGE,anchor="mm")
d.line([(mx+8,lt+157),(mx+mw-8,lt+157)],fill=LINE,width=1)
kinds=[
    ("Unspecified","час без мітки (за замовч.)"),
    ("Local",      "локальний час ОС"),
    ("Utc",        "UTC (рекоменд. для БД)"),
]
for i,(k,desc) in enumerate(kinds):
    iy=lt+165+i*30
    d.rounded_rectangle([mx+8,iy-10,mx+mw-8,iy+18],radius=4,fill=DARK,outline=LINE,width=1)
    d.text((mx+14,iy),k,font=fb,fill=TEXT,anchor="lm")
    d.text((mx+14,iy+10),desc,font=fc,fill=MUTED,anchor="lm")

# === RIGHT: Add methods + operators
rx=mx+mw+20; rw=W-rx-20
d.rounded_rectangle([rx,lt,rx+rw,lt+150],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((rx+rw//2,lt+13),"Методи Add* та Subtract",font=fh,fill=ACCENT,anchor="mm")
d.line([(rx+8,lt+27),(rx+rw-8,lt+27)],fill=LINE,width=1)

adds=[
    "AddYears(n)   / AddMonths(n)",
    "AddDays(n)    / AddHours(n)",
    "AddMinutes(n) / AddSeconds(n)",
    "Add(TimeSpan) — додати будь-який інтервал",
    "Subtract(dt2) → повертає TimeSpan",
    "dt1 - dt2     → TimeSpan (різниця)",
    "dt + TimeSpan → DateTime (сума)",
]
for i,txt in enumerate(adds):
    col=ORANGE if "→" in txt else TEXT
    d.text((rx+8,lt+35+i*16),txt,font=fs,fill=col,anchor="lm")

# Operators
d.rounded_rectangle([rx,lt+160,rx+rw,lt+266],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((rx+rw//2,lt+173),"Оператори та порівняння",font=fh,fill=ORANGE,anchor="mm")
d.line([(rx+8,lt+187),(rx+rw-8,lt+187)],fill=LINE,width=1)
ops=[
    ("dt1 == dt2 / dt1 != dt2", "рівність / нерівність"),
    ("dt1 > dt2  / dt1 < dt2",  "порівняння хронологічно"),
    ("dt1 - dt2",                "→ TimeSpan (тривалість)"),
    ("dt + ts",                  "→ DateTime (нова точка)"),
    ("DateTime.Compare(d1,d2)",  "→ -1 / 0 / +1"),
]
for i,(op,desc) in enumerate(ops):
    iy=lt+195+i*14
    d.text((rx+8,iy),op,font=fs,fill=ACCENT,anchor="lm")
    d.text((rx+250,iy),f"// {desc}",font=fc,fill=MUTED,anchor="lm")

# Bottom: UTC vs Local
by=lt+276
d.rounded_rectangle([20,by,W-20,by+90],radius=6,fill=PANEL,outline=RED,width=1)
d.text((W//2,by+12),"UTC vs Local — чому важливо в медичних системах",font=fh,fill=RED,anchor="mm")
d.line([(30,by+26),(W-30,by+26)],fill=LINE,width=1)
notes=[
    "DateTime.Now   → Kind=Local  — прив'язаний до часового поясу ОС. Небезпечно зберігати в БД між серверами різних регіонів.",
    "DateTime.UtcNow → Kind=Utc   — незалежний від поясу. Рекомендується для аудит-журналів, timestamps у медичних записах.",
    "DateTime.SpecifyKind(dt, DateTimeKind.Utc) — позначити існуючий DateTime як UTC без конвертації значення.",
]
for i,note in enumerate(notes):
    d.text((30,by+32+i*18),note,font=fc,fill=TEXT,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/12-01/datetime-structure.png"
img.save(out); print("OK:",out)
