# -*- coding: utf-8 -*-
# TimeSpan — structure, construction, Total* vs components, arithmetic
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"

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

d.text((W//2,22),"TimeSpan — представлення тривалості часового інтервалу",
       font=ft,fill=ACCENT,anchor="mm")

# === TOP: What is TimeSpan
tx,ty,tw,th=20,44,920,52
d.rounded_rectangle([tx,ty,tx+tw,ty+th],radius=6,fill=PANEL,outline=ORANGE,width=2)
d.text((tx+tw//2,ty+13),"TimeSpan = ТРИВАЛІСТЬ (не точка в часі). Внутрішньо = int64 Ticks (100 нс)",
       font=fh,fill=ORANGE,anchor="mm")
d.text((tx+8,ty+32),"DateTime — момент часу  |  TimeSpan — проміжок між моментами  |  1 Tick = 100 наносекунд  |  1 день = 864 000 000 000 тіків",
       font=fs,fill=TEXT,anchor="lm")

# === LEFT: Construction
lx,lt,lw=20,112,300
d.rounded_rectangle([lx,lt,lx+lw,lt+264],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((lx+lw//2,lt+13),"Створення TimeSpan",font=fh,fill=ACCENT,anchor="mm")
d.line([(lx+8,lt+27),(lx+lw-8,lt+27)],fill=LINE,width=1)

ctors=[
    ("new TimeSpan(h, m, s)",      "години, хв, сек"),
    ("new TimeSpan(d, h, m, s)",   "дні, год, хв, сек"),
    ("new TimeSpan(d, h, m, s, ms)","+ мілісекунди"),
    ("new TimeSpan(ticks)",         "з тіків"),
    ("TimeSpan.FromDays(7.5)",      "7 днів 12 годин"),
    ("TimeSpan.FromHours(36)",      "36 годин"),
    ("TimeSpan.FromMinutes(90)",    "1 год 30 хв"),
    ("TimeSpan.FromSeconds(3600)",  "1 година"),
    ("TimeSpan.Zero",               "нульова тривалість"),
    ("dt1 - dt2",                   "різниця двох DateTime"),
]
for i,(ctor,desc) in enumerate(ctors):
    iy=lt+35+i*23
    d.rounded_rectangle([lx+6,iy-9,lx+lw-6,iy+12],radius=3,fill=DARK,outline=LINE,width=1)
    d.text((lx+10,iy),ctor,font=fs,fill=ACCENT,anchor="lm")
    d.text((lx+10,iy+10),f"  // {desc}",font=fc,fill=MUTED,anchor="lm")

# === MIDDLE: Properties
mx=lx+lw+20; mw=290
d.rounded_rectangle([mx,lt,mx+mw,lt+264],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((mx+mw//2,lt+13),"Властивості",font=fh,fill=ORANGE,anchor="mm")
d.line([(mx+8,lt+27),(mx+mw-8,lt+27)],fill=LINE,width=1)

# Component properties
d.text((mx+8,lt+35),"Компоненти (цілі частини):",font=fb,fill=TEXT)
comp=[
    ("Days",       "дні (ціла частина)","4"),
    ("Hours",      "години (0-23)","2"),
    ("Minutes",    "хвилини (0-59)","30"),
    ("Seconds",    "секунди (0-59)","0"),
    ("Milliseconds","мілісекунди (0-999)","0"),
]
for i,(name,desc,ex) in enumerate(comp):
    iy=lt+50+i*20
    d.text((mx+8,iy),name,font=fs,fill=ACCENT,anchor="lm")
    d.text((mx+120,iy),desc,font=fc,fill=TEXT,anchor="lm")
    d.text((mx+mw-8,iy),ex,font=fs,fill=ORANGE,anchor="rm")

# Example: 4d 2h 30m
d.rounded_rectangle([mx+6,lt+152,mx+mw-6,lt+172],radius=4,fill=DARK,outline=ACCENT,width=1)
d.text((mx+mw//2,lt+162),"TimeSpan ts = new TimeSpan(4, 2, 30, 0)",font=fc,fill=ACCENT,anchor="mm")

# Total properties
d.text((mx+8,lt+178),"Загальні Total* (як double):",font=fb,fill=TEXT)
total=[
    ("TotalDays",    "усі дні як дробове","4.104..."),
    ("TotalHours",   "усі години","98.5"),
    ("TotalMinutes", "усі хвилини","5910.0"),
    ("TotalSeconds", "усі секунди","354600.0"),
]
for i,(name,desc,ex) in enumerate(total):
    iy=lt+193+i*18
    d.text((mx+8,iy),name,font=fs,fill=ORANGE,anchor="lm")
    d.text((mx+120,iy),desc,font=fc,fill=TEXT,anchor="lm")
    d.text((mx+mw-8,iy),ex,font=fs,fill=ACCENT,anchor="rm")

d.text((mx+8,lt+250),"Duration → завжди невід'ємний TimeSpan",font=fc,fill=MUTED)

# === RIGHT: Arithmetic + clinical
rx=mx+mw+20; rw=W-rx-20
d.rounded_rectangle([rx,lt,rx+rw,lt+264],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((rx+rw//2,lt+13),"Арифметика та клінічне застосування",font=fh,fill=ACCENT,anchor="mm")
d.line([(rx+8,lt+27),(rx+rw-8,lt+27)],fill=LINE,width=1)

arith=[
    ("ts1 + ts2","→ TimeSpan (сума тривалостей)"),
    ("ts1 - ts2","→ TimeSpan (різниця)"),
    ("dt + ts",  "→ DateTime (нова точка)"),
    ("dt - ts",  "→ DateTime (нова точка)"),
    ("dt1 - dt2","→ TimeSpan (тривалість)"),
    ("ts.Negate()","→ від'ємний TimeSpan"),
    ("ts.Duration()","→ |ts| (абс. значення)"),
]
d.text((rx+8,lt+34),"Операції:",font=fb,fill=TEXT)
for i,(op,desc) in enumerate(arith):
    iy=lt+48+i*18
    d.text((rx+8,iy),op,font=fs,fill=ORANGE,anchor="lm")
    d.text((rx+120,iy),desc,font=fc,fill=TEXT,anchor="lm")

# Clinical use
d.line([(rx+8,lt+180),(rx+rw-8,lt+180)],fill=LINE,width=1)
d.text((rx+rw//2,lt+190),"Клінічні сценарії",font=fh,fill=ACCENT,anchor="mm")
clinical=[
    "TimeSpan stay = discharge - admission;",
    "// → Тривалість госпіталізації: stay.Days днів",
    "",
    "TimeSpan cycle = new TimeSpan(21, 0, 0, 0);",
    "Наступний прийом = lastVisit + cycle;",
    "",
    "TimeSpan shift = new TimeSpan(0, 8, 0, 0);",
    "Кінець зміни = shiftStart + shift;",
]
for i,line in enumerate(clinical):
    col=MUTED if line.startswith("→") else (ORANGE if "=" in line else TEXT)
    if line: d.text((rx+8,lt+204+i*10),line,font=fc,fill=col,anchor="lm")

# Bottom
by=lt+276
d.rounded_rectangle([20,by,W-20,by+84],radius=6,fill=PANEL,outline=ORANGE,width=1)
d.text((W//2,by+12),"TimeSpan vs TimeOnly — ключова різниця",font=fh,fill=ORANGE,anchor="mm")
d.line([(30,by+26),(W-30,by+26)],fill=LINE,width=1)
notes=[
    "TimeOnly  — час доби (0:00 – 23:59). Представляє годину на годиннику. Не може бути >24h або від'ємним.",
    "TimeSpan  — ТРИВАЛІСТЬ. Може бути більше 24 годин (наприклад 72 години) або від'ємним (різниця в зворотному порядку).",
    "TimeOnly.ToTimeSpan() — конвертація часу доби в тривалість від початку дня.",
]
for i,note in enumerate(notes):
    d.text((30,by+32+i*18),note,font=fc,fill=TEXT,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/12-04/timespan-overview.png"
img.save(out); print("OK:",out)
