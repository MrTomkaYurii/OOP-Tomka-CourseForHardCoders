# -*- coding: utf-8 -*-
# Array class overview: Sort, Search, Copy, Fill/Clear, Exists + Resize memory model
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"; RED="#c77676"

W,H=960,530
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)
fcc=load("C:/Windows/Fonts/arial.ttf",9)

d.text((W//2,22),"Клас Array — пошук, сортування, копіювання",
       font=ft,fill=ACCENT,anchor="mm")

# === ROW 1: 5 panels ===
panels = [
    {
        "title": "Sort / Reverse",
        "color": ACCENT,
        "items": [
            ("Array.Sort(arr)",           "in-place, IComparable"),
            ("Array.Sort(arr, comparer)", "з IComparer<T>"),
            ("Array.Sort(arr, (a,b)=>…)", "лямбда-порівняння"),
            ("Array.Sort(keys, values)",  "паралельне сортування"),
            ("Array.Reverse(arr)",        "перевернути in-place"),
        ]
    },
    {
        "title": "Пошук",
        "color": ORANGE,
        "items": [
            ("Array.IndexOf(arr, val)",   "лінійний, O(n), →-1"),
            ("Array.BinarySearch(arr,v)", "бінарний, O(log n)"),
            ("Array.Find(arr, pred)",     "перший за умовою"),
            ("Array.FindAll(arr, pred)",  "всі за умовою → T[]"),
            ("Array.FindIndex(arr, pred)","індекс першого"),
        ]
    },
    {
        "title": "Перевірки",
        "color": RED,
        "items": [
            ("Array.Exists(arr, pred)",   "чи є хоча б один"),
            ("Array.TrueForAll(arr, p)",  "чи всі відповідають"),
            (".Length",                   "загальна кількість"),
            (".Rank",                     "кількість вимірів"),
            (".GetLength(dim)",           "розмір виміру dim"),
        ]
    },
    {
        "title": "Копіювання",
        "color": ACCENT,
        "items": [
            ("Array.Copy(src,dst,n)",     "перші n елементів"),
            ("Array.Copy(s,si,d,di,n)",   "зі зсувами"),
            (".Clone()",                  "поверхнева копія"),
            ("Array.Resize(ref a, n)",    "новий масив + копія"),
        ]
    },
    {
        "title": "Fill / Clear",
        "color": ORANGE,
        "items": [
            ("Array.Fill(arr, val)",      "заповнити значенням"),
            ("Array.Fill(arr,v,i,n)",     "діапазон [i, i+n)"),
            ("Array.Clear(arr,i,n)",      "→ 0 / null / false"),
            ("Array.Clear(arr)",          "весь масив (.NET 6+)"),
        ]
    },
]

PW = (W - 40 - 4*8) // 5
py = 45; ph = 175

for i, panel in enumerate(panels):
    px = 20 + i*(PW+8)
    col = panel["color"]
    d.rounded_rectangle([px,py,px+PW,py+ph],radius=8,fill=PANEL,outline=col,width=2)
    d.text((px+PW//2, py+13), panel["title"], font=fh, fill=col, anchor="mm")
    d.line([(px+6, py+27),(px+PW-6, py+27)], fill=LINE, width=1)
    for j,(name,desc) in enumerate(panel["items"]):
        iy = py + 34 + j*27
        d.rounded_rectangle([px+5,iy-8,px+PW-5,iy+14],radius=3,fill=DARK,outline=LINE,width=1)
        d.text((px+9, iy+1), name, font=fcc, fill=col, anchor="lm")
        d.text((px+9, iy+11), f"// {desc}", font=fcc, fill=MUTED, anchor="lm")

# === ROW 2: Array.Resize memory model + BinarySearch note ===
row2_y = py + ph + 14

# Resize memory model
rw = 430
d.rounded_rectangle([20,row2_y,20+rw,row2_y+205],radius=8,fill=PANEL,outline=RED,width=2)
d.text((20+rw//2, row2_y+13),"Array.Resize — нова ділянка пам'яті", font=fh, fill=RED, anchor="mm")
d.line([(26, row2_y+27),(20+rw-6, row2_y+27)], fill=LINE, width=1)

# Before resize — small array
bx=30; by=row2_y+38
d.text((bx, by),"До Resize(ref arr, 6):", font=fcc, fill=MUTED, anchor="lm")
cells_before = ["P1","P2","P3"]
for k,val in enumerate(cells_before):
    cx=bx+k*48; cy=by+14
    d.rectangle([cx,cy,cx+44,cy+24], fill=DARK, outline=ACCENT)
    d.text((cx+22,cy+12), val, font=fc, fill=ACCENT, anchor="mm")
d.text((bx+3*48+8, by+26), "← arr (3 елементи)", font=fcc, fill=MUTED, anchor="lm")

# Arrow down
ax_mid=bx+3*48//2+30; arr_y=by+48
d.line([(ax_mid,arr_y),(ax_mid,arr_y+18)],fill=ORANGE,width=2)
d.polygon([(ax_mid-5,arr_y+18),(ax_mid+5,arr_y+18),(ax_mid,arr_y+26)],fill=ORANGE)
d.text((ax_mid+10,arr_y+8),"Resize створює НОВИЙ масив", font=fcc, fill=ORANGE, anchor="lm")

# After resize — bigger array
by2=arr_y+32
d.text((bx, by2),"Після Resize:", font=fcc, fill=MUTED, anchor="lm")
cells_after = ["P1","P2","P3","","",""]
cols_after  = [ACCENT,ACCENT,ACCENT,MUTED,MUTED,MUTED]
for k,(val,col) in enumerate(zip(cells_after,cols_after)):
    cx=bx+k*48; cy=by2+14
    d.rectangle([cx,cy,cx+44,cy+24], fill=DARK, outline=col)
    label = val if val else "null"
    d.text((cx+22,cy+12), label, font=fcc, fill=col, anchor="mm")
d.text((bx+6*48-44, by2+26), "← новий arr (6 елементів)", font=fcc, fill=MUTED, anchor="lm")

# Warning note
wy = by2+52
d.rounded_rectangle([bx-2,wy,20+rw-8,wy+50],radius=4,fill=DARK,outline=RED,width=1)
d.text((bx+4, wy+8),  "!  Стара змінна-посилання arr", font=fcc, fill=RED, anchor="lm")
d.text((bx+4, wy+20), "   оновлюється через ref-параметр.", font=fcc, fill=TEXT, anchor="lm")
d.text((bx+4, wy+32), "   Інші посилання на старий масив", font=fcc, fill=TEXT, anchor="lm")
d.text((bx+4, wy+44), "   залишаються незмінними!", font=fcc, fill=ORANGE, anchor="lm")

# BinarySearch + Sort requirement panel
bsx = 20+rw+14; bsw = W-bsx-20
d.rounded_rectangle([bsx,row2_y,bsx+bsw,row2_y+205],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((bsx+bsw//2, row2_y+13),"Умови та складність методів", font=fh, fill=ACCENT, anchor="mm")
d.line([(bsx+6, row2_y+27),(bsx+bsw-6, row2_y+27)], fill=LINE, width=1)

tbl_rows = [
    ("Метод",             "Вимога",          "Складність", "Повертає"),
    ("IndexOf",           "—",               "O(n)",       "індекс або -1"),
    ("BinarySearch",      "масив відсортов.", "O(log n)",   "індекс або ~індекс"),
    ("Find",              "—",               "O(n)",       "перший елемент"),
    ("FindAll",           "—",               "O(n)",       "T[] підмасив"),
    ("Sort (default)",    "IComparable<T>",  "O(n log n)", "void (in-place)"),
    ("Sort (lambda)",     "—",               "O(n log n)", "void (in-place)"),
    ("Exists/TrueForAll", "—",               "O(n)",       "bool"),
]
col_x = [bsx+8, bsx+120, bsx+230, bsx+320]
for ri,row in enumerate(tbl_rows):
    iy = row2_y+34 + ri*21
    bg = DARK if ri%2==0 and ri>0 else (PANEL if ri==0 else BG)
    if ri>0: d.rectangle([bsx+6,iy-3,bsx+bsw-6,iy+15], fill=bg)
    clr = [MUTED,MUTED,MUTED,MUTED] if ri==0 else [ACCENT,TEXT,ORANGE,TEXT]
    for ci,(val,cx) in enumerate(zip(row,col_x)):
        d.text((cx, iy+6), val, font=fcc, fill=clr[ci], anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/13-04/array-overview.png"
img.save(out); print("OK:",out)
