# -*- coding: utf-8 -*-
# String operations — method overview diagram
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"
RED="#c77676"

W,H=940,470
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",13)
fr=load("C:/Windows/Fonts/arial.ttf",12)
fs=load("C:/Windows/Fonts/arial.ttf",11)
ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)

d.text((W//2,22),"Операції з рядками — групи методів класу String",
       font=ft,fill=ACCENT,anchor="mm")

# === Source string banner ===
bx,by,bw,bh=30,50,880,40
d.rounded_rectangle([bx,by,bx+bw,by+bh],radius=6,fill=PANEL,outline=ACCENT,width=2)
d.text((bx+bw//2,by+20),
       'string record = "Петренко;Іван;67;кардіологія;I10.9";',
       font=fb,fill=ACCENT,anchor="mm")

# === 6 groups ===
groups=[
  ("Пошук",  ACCENT, [
    'Contains("кардіо")',
    'StartsWith("Петр")',
    'EndsWith("I10.9")',
    'IndexOf("Іван")',
    'LastIndexOf(";")',
  ]),
  ("Поділ / З'єднання", ORANGE, [
    'Split(";")   -> ["Петренко","Іван",...]',
    'string.Join(";", parts)',
    'string.Concat(a, b, c)',
    'Substring(10, 4)',
  ]),
  ("Зміна", RED, [
    'Replace("67","68")',
    'ToUpper() / ToLower()',
    'Insert(9, " Степанович")',
    'Remove(0, 9)',
  ]),
  ("Обрізка", ACCENT, [
    'Trim()',
    'TrimStart()',
    'TrimEnd()',
    'PadLeft(20)',
    'PadRight(20)',
  ]),
  ("Порівняння", ORANGE, [
    'Compare(s1, s2)',
    'Equals(s1, s2,',
    '  OrdinalIgnoreCase)',
    'CompareTo(other)',
  ]),
  ("Перевірка", RED, [
    'IsNullOrEmpty(s)',
    'IsNullOrWhiteSpace(s)',
    'Length',
    '[index]  (char)',
  ]),
]

cols=3; col_w=(W-60)//cols; row_h=170; top=110
for i,( title,col,items) in enumerate(groups):
    cx=30+(i%cols)*col_w
    cy=top+(i//cols)*row_h
    gw=col_w-12; gh=row_h-14
    d.rounded_rectangle([cx,cy,cx+gw,cy+gh],radius=6,fill=PANEL,outline=col,width=2)
    d.text((cx+gw//2,cy+13),title,font=fh,fill=col,anchor="mm")
    d.line([(cx+8,cy+26),(cx+gw-8,cy+26)],fill=LINE,width=1)
    for j,item in enumerate(items):
        d.text((cx+10,cy+38+j*20),item,font=fs,fill=TEXT,anchor="lm")

# bottom
ly=H-36
d.line([(30,ly-8),(W-30,ly-8)],fill=LINE,width=1)
d.text((30,ly),"Всі методи повертають НОВИЙ рядок (immutability) — оригінал не змінюється",
       font=fs,fill=MUTED)

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/11-02/string-operations-overview.png"
img.save(out); print("OK:",out)
