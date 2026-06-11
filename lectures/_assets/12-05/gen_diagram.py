# -*- coding: utf-8 -*-
# Parsing DateTime + DateTimeOffset + TimeZoneInfo
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

d.text((W//2,22),"Парсинг DateTime та DateTimeOffset — безпечне перетворення рядків",
       font=ft,fill=ACCENT,anchor="mm")

# === LEFT: Parse methods flow
lx,lt,lw=20,44,360
d.rounded_rectangle([lx,lt,lx+lw,lt+290],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((lx+lw//2,lt+13),"Методи парсингу DateTime",font=fh,fill=ACCENT,anchor="mm")
d.line([(lx+8,lt+27),(lx+lw-8,lt+27)],fill=LINE,width=1)

methods=[
    ("Parse(s)",             "culture-sensitive, кидає виняток\nякщо рядок некоректний"),
    ("TryParse(s, out dt)",  "повертає bool, НЕ кидає виняток\nрекомендований для вводу користувача"),
    ("ParseExact(s, fmt)",   "точний формат обов'язковий\nкидає виняток при невідповідності"),
    ("TryParseExact(s, fmt, out dt)","точний формат + bool\nнайбезпечніший варіант"),
]
for i,(name,desc) in enumerate(methods):
    iy=lt+35+i*60
    # box
    d.rounded_rectangle([lx+6,iy,lx+lw-6,iy+50],radius=5,fill=DARK,outline=ACCENT,width=1)
    d.text((lx+14,iy+8),name,font=fb,fill=ACCENT,anchor="lm")
    lines=desc.split("\n")
    for li,line in enumerate(lines):
        d.text((lx+14,iy+22+li*14),line,font=fc,fill=TEXT,anchor="lm")
    # arrow between
    if i<len(methods)-1:
        ay=iy+52
        d.line([(lx+lw//2,ay),(lx+lw//2,ay+6)],fill=MUTED,width=1)
        d.text((lx+lw//2,ay+12),"або безпечніше:",font=fc,fill=MUTED,anchor="mm")

d.rounded_rectangle([lx+6,lt+272,lx+lw-6,lt+284],radius=4,fill=DARK,outline=ORANGE,width=1)
d.text((lx+lw//2,lt+278),"Рекомендація: TryParseExact для медичних форм",font=fc,fill=ORANGE,anchor="mm")

# === MIDDLE: DateTimeOffset
mx=lx+lw+20; mw=270
d.rounded_rectangle([mx,lt,mx+mw,lt+290],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((mx+mw//2,lt+13),"DateTimeOffset",font=fh,fill=ORANGE,anchor="mm")
d.line([(mx+8,lt+27),(mx+mw-8,lt+27)],fill=LINE,width=1)

d.text((mx+8,lt+35),"DateTime + зсув від UTC (offset)",font=fs,fill=TEXT)
d.text((mx+8,lt+49),"Зберігає точку в часі та часовий пояс.",font=fc,fill=MUTED)

d.text((mx+8,lt+68),"Конструктори:",font=fb,fill=TEXT)
dtos=[
    "new DateTimeOffset(2026, 6, 11, 10, 30, 0,",
    "    TimeSpan.FromHours(2))",
    "→ 2026-06-11T10:30:00+02:00",
    "",
    "DateTimeOffset.Now      // Local + offset",
    "DateTimeOffset.UtcNow   // UTC, offset=0",
    "new DateTimeOffset(dt, offset)",
]
for i,line in enumerate(dtos):
    col=ACCENT if line.startswith("→") else (ORANGE if "Now" in line else TEXT)
    if line: d.text((mx+8,lt+82+i*14),line,font=fc,fill=col,anchor="lm")

d.text((mx+8,lt+184),"Властивості:",font=fb,fill=TEXT)
props=[
    ("Offset","зсув від UTC як TimeSpan"),
    ("UtcDateTime","час у UTC"),
    ("LocalDateTime","час у Local"),
    ("DateTime","без offset-мітки"),
]
for i,(name,desc) in enumerate(props):
    iy=lt+198+i*18
    d.text((mx+8,iy),name,font=fs,fill=ORANGE,anchor="lm")
    d.text((mx+110,iy),f"→ {desc}",font=fc,fill=TEXT,anchor="lm")

d.rounded_rectangle([mx+6,lt+272,mx+mw-6,lt+284],radius=4,fill=DARK,outline=ORANGE,width=1)
d.text((mx+mw//2,lt+278),"Для медичних БД: зберігайте DateTimeOffset.UtcNow",font=fc,fill=ORANGE,anchor="mm")

# === RIGHT: TimeZoneInfo
rx=mx+mw+20; rw=W-rx-20
d.rounded_rectangle([rx,lt,rx+rw,lt+290],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((rx+rw//2,lt+13),"TimeZoneInfo",font=fh,fill=ACCENT,anchor="mm")
d.line([(rx+8,lt+27),(rx+rw-8,lt+27)],fill=LINE,width=1)

d.text((rx+8,lt+35),"Представляє часовий пояс",font=fs,fill=TEXT)

tzinfo=[
    ('TimeZoneInfo.Local',        "пояс ОС"),
    ('TimeZoneInfo.Utc',          "UTC"),
    ('TimeZoneInfo.FindSystemTimeZoneById',
                                  '"Europe/Kiev"'),
    ('TimeZoneInfo.ConvertTime',  "конвертувати час"),
    ('TimeZoneInfo.ConvertTimeToUtc',"→ UTC"),
    ('TimeZoneInfo.ConvertTimeFromUtc',"UTC →"),
    ('tz.GetUtcOffset(dt)',        "зсув для конкретної дати"),
    ('tz.IsDaylightSavingTime(dt)',"перехід на літній час?"),
]
d.text((rx+8,lt+50),"Методи та властивості:",font=fb,fill=TEXT)
for i,(name,desc) in enumerate(tzinfo):
    iy=lt+64+i*22
    d.text((rx+8,iy),name,font=fs,fill=ORANGE,anchor="lm")
    d.text((rx+8,iy+11),f"  // {desc}",font=fc,fill=MUTED,anchor="lm")

# Bottom: comparison DateTime vs DateTimeOffset
by=lt+302
d.rounded_rectangle([20,by,W-20,by+102],radius=6,fill=PANEL,outline=RED,width=1)
d.text((W//2,by+12),"DateTime vs DateTimeOffset — коли що обрати",font=fh,fill=RED,anchor="mm")
d.line([(30,by+26),(W-30,by+26)],fill=LINE,width=1)

comparison=[
    ("DateTime",     ORANGE,"Локальне відображення, UI, не потрібна інформація про пояс"),
    ("DateTime UTC", ACCENT,"Timestamps для аудит-журналів (Kind=Utc, без offset-метадати)"),
    ("DateTimeOffset",TEXT, "Найповніша інформація. Рекомендовано для медичних БД та API"),
]
for i,(typ,col,desc) in enumerate(comparison):
    iy=by+34+i*22
    d.rounded_rectangle([30,iy-8,160,iy+12],radius=4,fill=DARK,outline=col,width=1)
    d.text((95,iy),typ,font=fs,fill=col,anchor="mm")
    d.text((170,iy),f"→ {desc}",font=fc,fill=TEXT,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/12-05/parsing-and-datetimeoffset.png"
img.save(out); print("OK:",out)
