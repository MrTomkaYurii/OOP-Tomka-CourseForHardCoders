# -*- coding: utf-8 -*-
# Index and Range overview: ^ operator, .. range, array/string/span usage
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"; RED="#c77676"

W,H=960,540
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)
fcc=load("C:/Windows/Fonts/arial.ttf",9)

d.text((W//2,22),"Index та Range — індексування від кінця та діапазони",
       font=ft,fill=ACCENT,anchor="mm")

# ============================================================
# TOP: visual array with ^ and .. labels
# ============================================================
arr_vals = ["P1","P2","P3","P4","P5","P6","P7","P8"]
N = len(arr_vals)
cell_w=72; cell_h=34
arr_x=40; arr_y=50

# draw cells
for k,v in enumerate(arr_vals):
    cx=arr_x+k*cell_w; cy=arr_y+20
    d.rectangle([cx,cy,cx+cell_w-2,cy+cell_h],fill=DARK,outline=ACCENT)
    d.text((cx+cell_w//2-1,cy+cell_h//2),v,font=fc,fill=ACCENT,anchor="mm")

# forward indices (top)
for k in range(N):
    cx=arr_x+k*cell_w+cell_w//2-1
    d.text((cx,arr_y+8),str(k),font=fcc,fill=ORANGE,anchor="mm")

# ^-indices (below cells)
for k in range(N):
    cx=arr_x+k*cell_w+cell_w//2-1
    d.text((cx,arr_y+62),f"^{N-k}",font=fcc,fill=RED,anchor="mm")

# labels
d.text((arr_x+N*cell_w+10,arr_y+8),"прямі індекси (0..N-1)",font=fcc,fill=ORANGE,anchor="lm")
d.text((arr_x+N*cell_w+10,arr_y+62),"^ індекси від кінця",font=fcc,fill=RED,anchor="lm")
d.text((arr_x+N*cell_w+10,arr_y+35),"^0 = за межею (=Length)",font=fcc,fill=MUTED,anchor="lm")

# Range brackets: 2..5
r_start=2; r_end=5
bx1=arr_x+r_start*cell_w; bx2=arr_x+r_end*cell_w-2
bracket_y=arr_y+58
d.line([(bx1,bracket_y),(bx2,bracket_y)],fill=ACCENT,width=2)
d.line([(bx1,bracket_y-5),(bx1,bracket_y+5)],fill=ACCENT,width=2)
d.line([(bx2,bracket_y-5),(bx2,bracket_y+5)],fill=ACCENT,width=2)
d.text(((bx1+bx2)//2,bracket_y+12),"arr[2..5] = {P3,P4,P5}",font=fcc,fill=ACCENT,anchor="mm")

# Range bracket ^3..^1
rs2=N-3; re2=N-1
bx3=arr_x+rs2*cell_w; bx4=arr_x+re2*cell_w-2
bracket_y2=arr_y+76
d.line([(bx3,bracket_y2),(bx4,bracket_y2)],fill=ORANGE,width=2)
d.line([(bx3,bracket_y2-5),(bx3,bracket_y2+5)],fill=ORANGE,width=2)
d.line([(bx4,bracket_y2-5),(bx4,bracket_y2+5)],fill=ORANGE,width=2)
d.text(((bx3+bx4)//2,bracket_y2+12),"arr[^3..^1] = {P6,P7}",font=fcc,fill=ORANGE,anchor="mm")

# ============================================================
# MIDDLE: 3 panels
# ============================================================
row2_y=arr_y+100; row2_h=200

panels=[
    {
        "title":"Index — синтаксис ^",
        "color":RED,
        "items":[
            ("arr[^1]",         "останній елемент"),
            ("arr[^2]",         "передостанній"),
            ("arr[^n]",         "n-й від кінця"),
            ("Index i = ^1",    "зберегти у змінній"),
            ("^0",              "= Length (за межею!)"),
            ("Index.IsFromEnd",  "true якщо ^ індекс"),
            ("i.GetOffset(len)", "→ числовий індекс"),
        ]
    },
    {
        "title":"Range — синтаксис ..",
        "color":ACCENT,
        "items":[
            ("arr[2..5]",         "від 2 включно, до 5 виключно"),
            ("arr[..3]",          "перші 3: 0..3"),
            ("arr[^3..]",         "останні 3: ^3..^0"),
            ("arr[..]",           "весь масив"),
            ("Range r = 1..^1",   "зберегти у змінній"),
            ("r.GetOffsetAndLength(n)","→ (offset, length)"),
            ("arr[r]",            "застосувати Range"),
        ]
    },
    {
        "title":"Масив vs Span vs String",
        "color":ORANGE,
        "items":[
            ("arr[1..4]",        "новий масив (копія!)"),
            ("span[1..4]",       "Span<T> без копії"),
            ("str[2..5]",        "новий рядок (копія)"),
            ("str.AsSpan()[2..5]","ReadOnlySpan без копії"),
            ("list[1..3]",       "List<T>: не підтримує"),
            ("IList: не підтримує","тільки T[] і Span"),
        ]
    },
]

PW=(W-40-2*12)//3
for i,panel in enumerate(panels):
    px=20+i*(PW+12)
    col=panel["color"]
    d.rounded_rectangle([px,row2_y,px+PW,row2_y+row2_h],radius=8,fill=PANEL,outline=col,width=2)
    d.text((px+PW//2,row2_y+13),panel["title"],font=fh,fill=col,anchor="mm")
    d.line([(px+6,row2_y+27),(px+PW-6,row2_y+27)],fill=LINE,width=1)
    for j,(name,desc) in enumerate(panel["items"]):
        iy=row2_y+35+j*24
        if iy+16>row2_y+row2_h-4: break
        d.rounded_rectangle([px+5,iy-6,px+PW-5,iy+14],radius=3,fill=DARK,outline=LINE,width=1)
        d.text((px+9,iy+3),name,font=fc,fill=col,anchor="lm")
        d.text((px+9,iy+13),f"  // {desc}",font=fcc,fill=MUTED,anchor="lm")

# ============================================================
# BOTTOM: examples table
# ============================================================
bot_y=row2_y+row2_h+10; bot_h=75
d.rounded_rectangle([20,bot_y,W-20,bot_y+bot_h],radius=6,fill=PANEL,outline=ORANGE,width=1)
d.text((W//2,bot_y+12),"Приклади індексів та діапазонів",font=fh,fill=ORANGE,anchor="mm")
d.line([(30,bot_y+26),(W-30,bot_y+26)],fill=LINE,width=1)

ex_rows=[
    ("Вираз",          "Що повертає",          "Примітка"),
    ("arr[^1]",        "останній елемент",      "arr[arr.Length-1]"),
    ("arr[0..3]",      "{arr[0],arr[1],arr[2]}","до 3 — виключно"),
    ("arr[^3..]",      "останні 3 елементи",    "^3..^0 (^0=Length)"),
    ("str[^4..^1]",    "4-й..2-й символ від кінця","рядки теж підтримують"),
    ("span[1..^1]",    "Span без першого і останнього","без копіювання"),
]
cx_ex=[28,190,390,570]
for ri,row in enumerate(ex_rows):
    iy=bot_y+30+ri*13
    if iy+12>bot_y+bot_h: break
    clrs=[MUTED,MUTED,MUTED] if ri==0 else [ACCENT,TEXT,ORANGE]
    for ci,(val,cx) in enumerate(zip(row,cx_ex)):
        d.text((cx,iy),val,font=fcc,fill=clrs[ci],anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/13-06/index-range-overview.png"
img.save(out); print("OK:",out)
