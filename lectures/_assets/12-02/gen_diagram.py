# -*- coding: utf-8 -*-
# DateTime formatting — standard and custom specifiers
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"

W,H=960,510
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11)
ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)

d.text((W//2,22),"Форматування DateTime — стандартні та кастомні специфікатори",
       font=ft,fill=ACCENT,anchor="mm")

# === LEFT: Standard format specifiers
lx,lt,lw=20,44,390
d.rounded_rectangle([lx,lt,lx+lw,lt+330],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((lx+lw//2,lt+13),'Стандартні специфікатори  now.ToString("X")',font=fh,fill=ACCENT,anchor="mm")
d.line([(lx+8,lt+27),(lx+lw-8,lt+27)],fill=LINE,width=1)

specs=[
    ("d","06.01.2026","короткий формат дати"),
    ("D","6 січня 2026 р.","довгий формат дати"),
    ("t","14:45","короткий час"),
    ("T","14:45:20","довгий час"),
    ("f","6 січня 2026 р. 14:45","довгий дата + короткий час"),
    ("F","6 січня 2026 р. 14:45:20","довгий дата + довгий час"),
    ("g","06.01.2026 14:45","короткий дата + короткий час"),
    ("G","06.01.2026 14:45:20","короткий дата + довгий час (за замовч.)"),
    ("M","6 січня","місяць та день"),
    ("Y","січень 2026 р.","рік та місяць"),
    ("s","2026-01-06T14:45:20","ISO 8601 (sortable, без поясу)"),
    ("O","2026-01-06T14:45:20.000+02:00","ISO 8601 з часовим поясом"),
    ("R","Thu, 06 Jan 2026 12:45:20 GMT","RFC 1123 (HTTP заголовки)"),
    ("u","2026-01-06 14:45:20Z","UTC sortable"),
]
for i,(spec,example,desc) in enumerate(specs):
    iy=lt+35+i*21
    d.rounded_rectangle([lx+6,iy-9,lx+24,iy+9],radius=3,fill=DARK,outline=ORANGE,width=1)
    d.text((lx+15,iy),spec,font=fb,fill=ORANGE,anchor="mm")
    d.text((lx+30,iy),example,font=fs,fill=ACCENT,anchor="lm")
    d.text((lx+30,iy+10),f"  {desc}",font=fc,fill=MUTED,anchor="lm")

# === RIGHT: Custom format specifiers
rx=lx+lw+20; rw=W-rx-20
d.rounded_rectangle([rx,lt,rx+rw,lt+330],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((rx+rw//2,lt+13),'Кастомні специфікатори  now.ToString("dd.MM.yyyy")',font=fh,fill=ORANGE,anchor="mm")
d.line([(rx+8,lt+27),(rx+rw-8,lt+27)],fill=LINE,width=1)

custom=[
    ("yyyy","рік 4 цифри","2026"),
    ("yy",  "рік 2 цифри","26"),
    ("MM",  "місяць 2 цифри","01"),
    ("MMM", "місяць коротко","січ"),
    ("MMMM","місяць повністю","січень"),
    ("dd",  "день 2 цифри","06"),
    ("ddd", "день тижня коротко","Чт"),
    ("dddd","день тижня повністю","четвер"),
    ("HH",  "година 24h (00-23)","14"),
    ("hh",  "година 12h (01-12)","02"),
    ("mm",  "хвилина (00-59)","45"),
    ("ss",  "секунда (00-59)","20"),
    ("fff", "мілісекунди","123"),
    ("tt",  "AM/PM","PM"),
    ("zzz", "зсув часового поясу","+02:00"),
]
for i,(spec,desc,example) in enumerate(custom):
    iy=lt+35+i*20
    d.rounded_rectangle([rx+6,iy-8,rx+52,iy+9],radius=3,fill=DARK,outline=ACCENT,width=1)
    d.text((rx+30,iy),spec,font=fb,fill=ACCENT,anchor="mm")
    d.text((rx+60,iy),desc,font=fs,fill=TEXT,anchor="lm")
    d.text((rx+rw-8,iy),example,font=fs,fill=ORANGE,anchor="rm")

# === BOTTOM: Parse examples
by=lt+340
d.rounded_rectangle([20,by,W-20,by+108],radius=6,fill=PANEL,outline=ACCENT,width=1)
d.text((W//2,by+12),"Парсинг рядка у DateTime — Parse / TryParse / ParseExact",font=fh,fill=ACCENT,anchor="mm")
d.line([(30,by+26),(W-30,by+26)],fill=LINE,width=1)

examples=[
    ('DateTime dt = DateTime.Parse("06.01.2026 14:45");',                           "// авто-парсинг (culture-sensitive, кидає виняток)"),
    ('if (DateTime.TryParse("06.01.2026", out DateTime dt)) { ... }',               "// безпечний варіант, повертає bool"),
    ('DateTime dt = DateTime.ParseExact("11.06.2026", "dd.MM.yyyy", null);',        "// точний формат (null = поточна культура)"),
    ('DateTime dt = DateTime.ParseExact("2026-06-11", "yyyy-MM-dd",',               ""),
    ('                                  CultureInfo.InvariantCulture);',             "// з явною культурою — рекомендовано"),
]
for i,(code,comment) in enumerate(examples):
    iy=by+32+i*15
    d.text((30,iy),code,font=fc,fill=TEXT,anchor="lm")
    if comment:
        d.text((30+len(code)*6,iy),comment,font=fc,fill=MUTED,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/12-02/datetime-formatting.png"
img.save(out); print("OK:",out)
