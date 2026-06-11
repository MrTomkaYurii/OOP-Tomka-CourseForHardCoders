# -*- coding: utf-8 -*-
# Regex — syntax elements + API overview
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"
RED="#c77676"

W,H=940,490
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11)
ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)

d.text((W//2,22),"Регулярні вирази у C# — синтаксис та API класу Regex",
       font=ft,fill=ACCENT,anchor="mm")

# === TOP: Pattern example with annotations ===
ex_x,ex_y,ex_w,ex_h=30,46,880,80
d.rounded_rectangle([ex_x,ex_y,ex_x+ex_w,ex_y+ex_h],radius=6,fill=PANEL,outline=ORANGE,width=2)
d.text((ex_x+10,ex_y+12),"Шаблон МКХ-10 коду:",font=fh,fill=ORANGE,anchor="lm")

# Pattern tokens
tokens=[
    ("[A-Z]",      ACCENT,  "велика літера A-Z"),
    ("\\d{2}",     ORANGE,  "рівно 2 цифри"),
    ("(\\.\\d)?",  RED,     "необов. .цифра"),
]
tx=ex_x+200
for i,(tok,col,desc) in enumerate(tokens):
    bx=tx+i*210
    d.rounded_rectangle([bx,ex_y+10,bx+80,ex_y+36],radius=4,fill=DARK,outline=col,width=2)
    d.text((bx+40,ex_y+23),tok,font=fb,fill=col,anchor="mm")
    d.line([(bx+40,ex_y+36),(bx+40,ex_y+56)],fill=col,width=1)
    d.text((bx+40,ex_y+64),desc,font=fc,fill=col,anchor="mm")

d.text((ex_x+870,ex_y+23),'@"[A-Z]\\d{2}(\\.\\d)?"',font=fb,fill=TEXT,anchor="rm")

# === LEFT: Syntax elements ===
lx,lt,lw=30,140,410
d.rounded_rectangle([lx,lt,lx+lw,lt+240],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((lx+lw//2,lt+13),"Синтаксис регулярних виразів",font=fh,fill=ACCENT,anchor="mm")
d.line([(lx+10,lt+27),(lx+lw-10,lt+27)],fill=LINE,width=1)

syntax=[
    ("^  $",       "початок / кінець рядка"),
    (".",          "будь-який один символ"),
    ("*  +  ?",    "0+ / 1+ / 0 або 1 раз"),
    ("{3}  {2,4}", "рівно 3 / від 2 до 4 разів"),
    ("\\d  \\D",   "цифра / не цифра"),
    ("\\w  \\W",   "слово-символ / не словесний"),
    ("\\s  \\S",   "пробіл / не пробіл"),
    ("[abc]",      "один із символів a, b, c"),
    ("[A-Z]",      "символ у діапазоні A-Z"),
    ("(abc)",      "група збігу"),
    ("(?<name>…)", "іменована група"),
    ("|",          "альтернатива: abc|def"),
    ("\\.",        "екранування: літеральна крапка"),
]
for i,(sym,desc) in enumerate(syntax):
    iy=lt+38+i*15
    d.text((lx+10,iy),sym,font=fs,fill=ORANGE,anchor="lm")
    d.text((lx+120,iy),desc,font=fs,fill=TEXT,anchor="lm")

# === RIGHT: API methods ===
rx=lx+lw+20; rw=W-rx-30
d.rounded_rectangle([rx,lt,rx+rw,lt+240],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((rx+rw//2,lt+13),"API класу Regex",font=fh,fill=ORANGE,anchor="mm")
d.line([(rx+10,lt+27),(rx+rw-10,lt+27)],fill=LINE,width=1)

apis=[
    ("Matches(input)",           "всі збіги -> MatchCollection"),
    ("Match(input)",             "перший збіг -> Match"),
    ("IsMatch(input)",           "bool: чи є хоч один збіг"),
    ("Replace(input, replacement)","замінити всі збіги"),
    ("Split(input)",             "розбити по збігах"),
    ("match.Value",              "рядок знайденого збігу"),
    ("match.Index",              "позиція збігу у вхідному рядку"),
    ("match.Groups[1]",          "значення першої групи ()"),
    ('match.Groups["name"]',     "іменована група (?<name>...)"),
    ("RegexOptions.IgnoreCase",  "нечутливість до регістру"),
    ("RegexOptions.Multiline",   "^ та $ — початок/кінець рядка"),
    ("[GeneratedRegex(...)]",    "compile-time генерація (C# 7+)"),
]
for i,(sig,desc) in enumerate(apis):
    iy=lt+38+i*16
    d.text((rx+8,iy),sig,font=fs,fill=ACCENT,anchor="lm")
    d.text((rx+8,iy+9),f"  // {desc}",font=fc,fill=MUTED,anchor="lm")

# === BOTTOM: named groups example ===
by2=lt+252
d.rounded_rectangle([30,by2,W-30,by2+106],radius=6,fill=PANEL,outline=ACCENT,width=1)
d.text((W//2,by2+12),"Іменована група (?<name>...) — витягуємо поля без обліку порядку",font=fh,fill=ACCENT,anchor="mm")
d.line([(40,by2+26),(W-40,by2+26)],fill=LINE,width=1)

code=[
    r'var re = new Regex(@"(?<last>\w+);(?<first>\w+);(?<age>\d+);(?<icd>[A-Z]\d{2}\.?\d?)");',
    r'var m  = re.Match("Петренко;Іван;67;I10.9");',
    r'if (m.Success)',
    r'    Console.WriteLine($"{m.Groups["last"].Value}, {m.Groups["age"].Value} р., {m.Groups["icd"].Value}");',
    r'// Петренко, 67 р., I10.9',
]
for i,line in enumerate(code):
    col=MUTED if line.startswith("//") else (ACCENT if "Groups" in line else TEXT)
    d.text((42,by2+34+i*14),line,font=fc,fill=col,anchor="lm")

# Bottom
bl=H-24
d.line([(30,bl-6),(W-30,bl-6)],fill=LINE,width=1)
d.text((30,bl),"Regex використовує рядки @\"...\" (verbatim) щоб уникнути подвійного екранування зворотних слешів",
       font=fc,fill=MUTED)

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/11-05/regex-syntax-and-api.png"
img.save(out); print("OK:",out)
