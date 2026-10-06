# -*- coding: utf-8 -*-
# String formatting — comparison of approaches
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"
RED="#c77676"

W,H=940,500
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",13)
fr=load("C:/Windows/Fonts/arial.ttf",12)
fs=load("C:/Windows/Fonts/arial.ttf",11)
ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)

d.text((W//2,22),"Форматування рядків у C# — три підходи та специфікатори",
       font=ft,fill=ACCENT,anchor="mm")

# Result banner
bx,by,bw,bh=30,46,880,34
d.rounded_rectangle([bx,by,bx+bw,by+bh],radius=5,fill=PANEL,outline=MUTED,width=1)
d.text((bx+bw//2,by+17),
       'Результат у всіх трьох випадках: "Пацієнт: Петренко, вік: 67, АТ: 140.00 мм рт.ст."',
       font=fr,fill=TEXT,anchor="mm")

# === 3 approach columns ===
approaches=[
  (ORANGE, "Конкатенація  +", [
    'string s = "Пацієнт: " + name',
    '  + ", вік: " + age',
    '  + ", АТ: " + bp.ToString("F2")',
    '  + " мм рт.ст.";',
    "",
    "Мінуси:",
    "- кожен + = новий об'єкт у heap",
    "- важко читати при >3 значень",
    "- форматування через ToString()",
  ]),
  (ACCENT, "string.Format()", [
    'string s = string.Format(',
    '  "Пацієнт: {0}, вік: {1},',
    '   АТ: {2:F2} мм рт.ст.",',
    '  name, age, bp);',
    "",
    "Плюси:",
    "- шаблон відокремлено від даних",
    "- повторний аргумент: {0}...{0}",
    "- локалізація шаблону",
  ]),
  (ACCENT, 'Інтерполяція  $"..."', [
    'string s = $"Пацієнт: {name},'
    ,
    '  вік: {age},'
    ,
    '  АТ: {bp:F2} мм рт.ст.";'
    ,
    "",
    "Плюси:",
    "- найчитабельніший синтаксис",
    "- вирази прямо у {}",
    "- компілятор перевіряє типи",
  ]),
]

col_w=(W-60)//3; top=96
for i,(col,title,lines) in enumerate(approaches):
    cx=30+i*col_w; cy=top
    gw=col_w-12; gh=220
    d.rounded_rectangle([cx,cy,cx+gw,cy+gh],radius=6,fill=PANEL,outline=col,width=2)
    d.text((cx+gw//2,cy+13),title,font=fh,fill=col,anchor="mm")
    d.line([(cx+8,cy+26),(cx+gw-8,cy+26)],fill=LINE,width=1)
    for j,line in enumerate(lines):
        col2=MUTED if line.startswith("-") or line.startswith("Мін") or line.startswith("Плю") else TEXT
        d.text((cx+10,cy+38+j*19),line,font=fs,fill=col2,anchor="lm")

# === SPECIFIERS table ===
ty=top+238
d.text((W//2,ty+10),"Основні специфікатори форматування",font=fh,fill=ORANGE,anchor="mm")

specs=[
  ("{0:C2}",  "Валюта",    "23.70 -> 23,70 грн."),
  ("{0:D4}",  "Ціле",      "23    -> 0023"),
  ("{0:F2}",  "Дробове",   "140.5 -> 140,50"),
  ("{0:N0}",  "Тисячний",  "12345 -> 12 345"),
  ("{0:P1}",  "Відсоток",  "0.153 -> 15,3%"),
  ("{0:E2}",  "Науковий",  "12345 -> 1,23E+004"),
  ("{name,-15}","Вирівнювання","лів. вирівнювання (15 символів)"),
  ("{name,15}", "Вирівнювання","прав. вирівнювання (15 символів)"),
]

row_h=22; spec_x=30; tw1=100; tw2=110; tw3=210; per_col=4
for i,( spec,name,example) in enumerate(specs):
    col_idx=i//per_col; row_idx=i%per_col
    bsx=spec_x+col_idx*(tw1+tw2+tw3+30)
    bsy=ty+28+row_idx*row_h
    shade=PANEL if row_idx%2==0 else DARK
    d.rectangle([bsx,bsy,bsx+tw1+tw2+tw3+20,bsy+row_h-2],fill=shade)
    d.text((bsx+4,  bsy+row_h//2),spec,    font=fs,fill=ORANGE,anchor="lm")
    d.text((bsx+tw1+6,bsy+row_h//2),name,  font=fs,fill=MUTED, anchor="lm")
    d.text((bsx+tw1+tw2+10,bsy+row_h//2),example,font=fs,fill=TEXT,anchor="lm")

# bottom
ly=H-28
d.line([(30,ly-8),(W-30,ly-8)],fill=LINE,width=1)
d.text((30,ly),"$\"...\" компілюється у string.Format() — однаковий IL. Перевага $\"\" — читабельність і перевірка типів компілятором.",
       font=fc,fill=MUTED)

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/11-03/string-formatting-approaches.png"
img.save(out); print("OK:",out)
