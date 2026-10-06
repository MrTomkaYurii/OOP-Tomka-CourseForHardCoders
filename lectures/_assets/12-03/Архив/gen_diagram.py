# -*- coding: utf-8 -*-
# DateOnly + TimeOnly — structure, ranges, combination
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"

W,H=960,480
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11)
ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)

d.text((W//2,22),"DateOnly та TimeOnly — спеціалізовані типи для дати та часу (.NET 6+)",
       font=ft,fill=ACCENT,anchor="mm")

# === TOP: DateTime vs DateOnly vs TimeOnly comparison
cx,cy,cw,ch=20,44,920,72
d.rounded_rectangle([cx,cy,cx+cw,cy+ch],radius=6,fill=PANEL,outline=LINE,width=1)

cols=[("DateTime",ACCENT,"дата + час + Kind\n01.01.0001 — 31.12.9999\nКоли важлива обидва компоненти: timestamp події"),
      ("DateOnly",ORANGE,"тільки дата (без часу)\n01.01.0001 — 31.12.9999\nДата народження, дата виписки, розклад"),
      ("TimeOnly",ACCENT,"тільки час (0:00 — 23:59:59)\nНе прив'язаний до дати\nГодини прийому, зміни, розклад занять")]
cw3=cw//3
for ci,(title,col,desc) in enumerate(cols):
    bx=cx+ci*cw3
    if ci>0: d.line([(bx,cy+4),(bx,cy+ch-4)],fill=LINE,width=1)
    d.text((bx+cw3//2,cy+12),title,font=fb,fill=col,anchor="mm")
    lines=desc.split("\n")
    for li,line in enumerate(lines):
        d.text((bx+cw3//2,cy+26+li*16),line,font=fc,fill=TEXT if li>0 else MUTED,anchor="mm")

# === LEFT: DateOnly
lx,lt,lw=20,132,430
d.rounded_rectangle([lx,lt,lx+lw,lt+230],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((lx+lw//2,lt+13),"DateOnly",font=fh,fill=ORANGE,anchor="mm")
d.line([(lx+8,lt+27),(lx+lw-8,lt+27)],fill=LINE,width=1)

d.text((lx+8,lt+38),"Конструктори:",font=fb,fill=TEXT)
ctors_d=[
    'new DateOnly(2026, 6, 11)              // рік, місяць, день',
    'DateOnly.FromDateTime(DateTime.Today)  // із DateTime',
    'DateOnly.Parse("11.06.2026")           // із рядка',
    'DateOnly.FromDayNumber(738660)         // із номера дня',
]
for i,c in enumerate(ctors_d):
    d.text((lx+8,lt+52+i*13),c,font=fc,fill=ACCENT,anchor="lm")

d.text((lx+8,lt+108),"Властивості: Year / Month / Day / DayOfWeek / DayOfYear",font=fc,fill=TEXT)

d.text((lx+8,lt+126),"Методи:",font=fb,fill=TEXT)
meths_d=[
    "AddDays(n) / AddMonths(n) / AddYears(n)",
    "ToDateTime(TimeOnly)  → DateTime",
    'ToShortDateString() → "11.06.2026"',
    'ToLongDateString()  → "11 червня 2026 р."',
]
for i,m in enumerate(meths_d):
    d.text((lx+8,lt+140+i*14),m,font=fc,fill=TEXT,anchor="lm")

# Use case box
d.rounded_rectangle([lx+6,lt+200,lx+lw-6,lt+224],radius=4,fill=DARK,outline=ORANGE,width=1)
d.text((lx+lw//2,lt+212),"Медична картка: дата народження, дата прийому, дата виписки",
       font=fc,fill=ORANGE,anchor="mm")

# === RIGHT: TimeOnly
rx=lx+lw+20; rw=W-rx-20
d.rounded_rectangle([rx,lt,rx+rw,lt+230],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((rx+rw//2,lt+13),"TimeOnly",font=fh,fill=ACCENT,anchor="mm")
d.line([(rx+8,lt+27),(rx+rw-8,lt+27)],fill=LINE,width=1)

d.text((rx+8,lt+38),"Конструктори:",font=fb,fill=TEXT)
ctors_t=[
    'new TimeOnly(14, 30)         // год, хв',
    'new TimeOnly(9, 0, 0)        // год, хв, сек',
    'TimeOnly.FromDateTime(now)   // із DateTime',
    'TimeOnly.Parse("14:30")      // із рядка',
]
for i,c in enumerate(ctors_t):
    d.text((rx+8,lt+52+i*13),c,font=fc,fill=ACCENT,anchor="lm")

d.text((rx+8,lt+108),"Властивості: Hour / Minute / Second / Millisecond / Ticks",font=fc,fill=TEXT)

d.text((rx+8,lt+126),"Методи:",font=fb,fill=TEXT)
meths_t=[
    "AddHours(n) / AddMinutes(n)",
    "IsBetween(start, end) → bool",
    "ToTimeSpan() → TimeSpan",
    "ToShortTimeString() / ToLongTimeString()",
]
for i,m in enumerate(meths_t):
    d.text((rx+8,lt+140+i*14),m,font=fc,fill=TEXT,anchor="lm")

d.rounded_rectangle([rx+6,lt+200,rx+rw-6,lt+224],radius=4,fill=DARK,outline=ACCENT,width=1)
d.text((rx+rw//2,lt+212),"Розклад прийомів, робочі зміни, години роботи відділення",
       font=fc,fill=ACCENT,anchor="mm")

# === BOTTOM: Combination pattern
by=lt+242
d.rounded_rectangle([20,by,W-20,by+104],radius=6,fill=PANEL,outline=ACCENT,width=1)
d.text((W//2,by+12),"Комбінування DateOnly + TimeOnly → DateTime",font=fh,fill=ACCENT,anchor="mm")
d.line([(30,by+26),(W-30,by+26)],fill=LINE,width=1)

combo=[
    ('DateOnly date = new DateOnly(2026, 6, 15);   // дата прийому',ORANGE),
    ('TimeOnly time = new TimeOnly(10, 30);         // час прийому',ACCENT),
    ('DateTime appointment = date.ToDateTime(time); // 15.06.2026 10:30:00',TEXT),
    ('',None),
    ('// Зворотно:',MUTED),
    ('DateOnly d = DateOnly.FromDateTime(appointment);  // 15.06.2026',ORANGE),
    ('TimeOnly t = TimeOnly.FromDateTime(appointment);  // 10:30:00',ACCENT),
]
for i,(line,col) in enumerate(combo):
    if col:
        d.text((30,by+32+i*10),line,font=fc,fill=col,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/12-03/dateonly-timeonly.png"
img.save(out); print("OK:",out)
