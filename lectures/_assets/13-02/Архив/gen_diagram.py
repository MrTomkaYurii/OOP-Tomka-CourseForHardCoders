# -*- coding: utf-8 -*-
# Math class overview: rounding, abs/sign, min/max/clamp, pow/sqrt, trig
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"; RED="#c77676"

W,H=960,520
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11)
ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)
fcc=load("C:/Windows/Fonts/arial.ttf",9)

d.text((W//2,22),"Клас Math — огляд методів",
       font=ft,fill=ACCENT,anchor="mm")

# === 4 panels top row ===
panels_top = [
    {
        "title": "Константи",
        "color": ORANGE,
        "items": [
            ("Math.PI",  "3.14159265358979..."),
            ("Math.E",   "2.71828182845904..."),
            ("Math.Tau", "6.28318... (2*PI, .NET 5+)"),
        ]
    },
    {
        "title": "Округлення",
        "color": ACCENT,
        "items": [
            ("Math.Round(x)",             "банківське (ToEven)"),
            ("Math.Round(x, n)",          "до n знаків"),
            ("Math.Round(x, AwayFromZero)","шкільне (2.5→3)"),
            ("Math.Floor(x)",             "вниз (до -∞)"),
            ("Math.Ceiling(x)",           "вгору (до +∞)"),
            ("Math.Truncate(x)",          "відкинути дробову"),
        ]
    },
    {
        "title": "Abs / Sign",
        "color": ORANGE,
        "items": [
            ("Math.Abs(x)",      "модуль: |-5| = 5"),
            ("Math.Sign(x)",     "-1, 0, або 1"),
            ("Math.CopySign(x,y)","знак від y (.NET 6+)"),
        ]
    },
    {
        "title": "Min / Max / Clamp",
        "color": RED,
        "items": [
            ("Math.Min(a, b)",        "менший з двох"),
            ("Math.Max(a, b)",        "більший з двох"),
            ("Math.Clamp(v, lo, hi)", "обмежити в [lo, hi]"),
        ]
    },
]

PW = (W - 40 - 3*10) // 4
py = 45; ph = 185

for i, panel in enumerate(panels_top):
    px = 20 + i*(PW+10)
    col = panel["color"]
    d.rounded_rectangle([px,py,px+PW,py+ph],radius=8,fill=PANEL,outline=col,width=2)
    d.text((px+PW//2, py+13), panel["title"], font=fh, fill=col, anchor="mm")
    d.line([(px+6, py+27),(px+PW-6, py+27)], fill=LINE, width=1)
    for j,(name,desc) in enumerate(panel["items"]):
        iy = py + 34 + j*26
        d.rounded_rectangle([px+6,iy-8,px+PW-6,iy+14],radius=3,fill=DARK,outline=LINE,width=1)
        d.text((px+10, iy-1), name, font=fc, fill=col, anchor="lm")
        d.text((px+10, iy+8), f"  // {desc}", font=fcc, fill=MUTED, anchor="lm")

# === 3 panels bottom row ===
panels_bot = [
    {
        "title": "Степінь та корінь",
        "color": ACCENT,
        "items": [
            ("Math.Pow(b, e)",  "b^e: Pow(2,10)=1024"),
            ("Math.Sqrt(x)",    "квадратний корінь"),
            ("Math.Cbrt(x)",    "кубічний корінь (.NET 5+)"),
            ("Math.Log(x)",     "натуральний логарифм"),
            ("Math.Log2(x)",    "логарифм за основою 2"),
            ("Math.Log10(x)",   "логарифм за основою 10"),
        ]
    },
    {
        "title": "Тригонометрія",
        "color": ORANGE,
        "items": [
            ("Math.Sin(rad)",    "синус (аргумент у рад.)"),
            ("Math.Cos(rad)",    "косинус"),
            ("Math.Tan(rad)",    "тангенс"),
            ("Math.Asin(x)",     "арксинус → рад."),
            ("deg * PI/180",     "градуси → радіани"),
        ]
    },
    {
        "title": "Перевірка double",
        "color": RED,
        "items": [
            ("double.IsNaN(x)",     "Not a Number (0.0/0.0)"),
            ("double.IsInfinity(x)","±∞ (1.0/0.0)"),
            ("double.IsFinite(x)",  "скінченне число"),
            ("double.NaN",          "константа NaN"),
            ("double.PositiveInfinity","константа +∞"),
        ]
    },
]

BW = (W - 40 - 2*10) // 3
by2 = py + ph + 14; bh = 185

for i, panel in enumerate(panels_bot):
    bx = 20 + i*(BW+10)
    col = panel["color"]
    d.rounded_rectangle([bx,by2,bx+BW,by2+bh],radius=8,fill=PANEL,outline=col,width=2)
    d.text((bx+BW//2, by2+13), panel["title"], font=fh, fill=col, anchor="mm")
    d.line([(bx+6, by2+27),(bx+BW-6, by2+27)], fill=LINE, width=1)
    for j,(name,desc) in enumerate(panel["items"]):
        iy = by2 + 34 + j*26
        d.rounded_rectangle([bx+6,iy-8,bx+BW-6,iy+14],radius=3,fill=DARK,outline=LINE,width=1)
        d.text((bx+10, iy-1), name, font=fc, fill=col, anchor="lm")
        d.text((bx+10, iy+8), f"  // {desc}", font=fcc, fill=MUTED, anchor="lm")

# === Bottom: rounding comparison table ===
ty = by2 + bh + 14; th = 64
d.rounded_rectangle([20,ty,W-20,ty+th],radius=6,fill=PANEL,outline=ORANGE,width=1)
d.text((W//2, ty+12),"Порівняння режимів округлення", font=fh, fill=ORANGE, anchor="mm")
d.line([(30,ty+26),(W-30,ty+26)], fill=LINE, width=1)

cols_x = [60, 200, 360, 530, 700, 860]
headers = ["Значення","Floor","Ceiling","Truncate","Round (ToEven)","Round (Away0)"]
vals    = ["2.5", "2", "3", "2", "2 (парне!)", "3"]
vals2   = ["-2.5", "-3", "-2", "-2", "-2 (парне!)", "-3"]

for j,(hdr,col) in enumerate(zip(headers, cols_x)):
    d.text((col, ty+32), hdr, font=fcc, fill=MUTED, anchor="lm")
    d.text((col, ty+44), vals[j], font=fc, fill=ACCENT, anchor="lm")
    d.text((col, ty+54), vals2[j], font=fc, fill=ORANGE, anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/13-02/math-overview.png"
img.save(out); print("OK:",out)
