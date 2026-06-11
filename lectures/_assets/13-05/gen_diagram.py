# -*- coding: utf-8 -*-
# Span<T> overview: memory model, API, ReadOnlySpan, ref struct limits
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

d.text((W//2,22),"Span<T> — безкопійний доступ до пам'яті",
       font=ft,fill=ACCENT,anchor="mm")

# ============================================================
# TOP: memory model — Substring vs Span
# ============================================================
my=45; mh=150
d.rounded_rectangle([20,my,W-20,my+mh],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((W//2,my+13),"Substring (копія) vs Span (вказівник)",font=fh,fill=ORANGE,anchor="mm")
d.line([(30,my+27),(W-30,my+27)],fill=LINE,width=1)

# Source array / string on heap
src_x=40; src_y=my+35; cell_w=36; cell_h=28
source_vals=["P","0","0","1",",","І","в","а","н",",","6","7",",","I","1","0"]
d.text((src_x,src_y-2),"Heap (рядок або масив):",font=fcc,fill=MUTED,anchor="lm")
for k,v in enumerate(source_vals):
    cx=src_x+k*cell_w; cy=src_y+10
    col=ACCENT if 5<=k<=8 else (ORANGE if 0<=k<=3 else MUTED)
    d.rectangle([cx,cy,cx+cell_w-2,cy+cell_h],fill=DARK,outline=col)
    d.text((cx+cell_w//2-1,cy+cell_h//2),v,font=fc,fill=col,anchor="mm")

# Substring path — arrow + new heap block
sub_y=src_y+50
d.text((src_x,sub_y),"Substring(5,4):",font=fcc,fill=RED,anchor="lm")
d.line([(src_x+5*cell_w+cell_w//2,src_y+38),(src_x+5*cell_w+cell_w//2,sub_y+6)],fill=RED,width=1)
new_x=src_x+220
for k,v in enumerate(["І","в","а","н"]):
    cx=new_x+k*cell_w; cy=sub_y+8
    d.rectangle([cx,cy,cx+cell_w-2,cy+cell_h],fill=DARK,outline=RED)
    d.text((cx+cell_w//2-1,cy+cell_h//2),v,font=fc,fill=RED,anchor="mm")
d.text((new_x+4*cell_w+6,sub_y+20),"← НОВА ділянка heap (копія!)",font=fcc,fill=RED,anchor="lm")

# Span path — arrow + bracket
span_y=src_y+10
span_bx=src_x+5*cell_w-1; span_ex=src_x+9*cell_w-3
d.line([(span_bx,span_y-4),(span_bx,span_y-12)],fill=ACCENT,width=2)
d.line([(span_ex,span_y-4),(span_ex,span_y-12)],fill=ACCENT,width=2)
d.line([(span_bx,span_y-12),(span_ex,span_y-12)],fill=ACCENT,width=2)
mid_span=(span_bx+span_ex)//2
d.text((mid_span,span_y-16),"Span (вказівник+довжина, стек)",font=fcc,fill=ACCENT,anchor="mm")

# Stack box for Span
stk_x=src_x+500; stk_y=src_y+8
d.rounded_rectangle([stk_x,stk_y,stk_x+200,stk_y+60],radius=4,fill=DARK,outline=ACCENT,width=1)
d.text((stk_x+100,stk_y+8),"Span<char> (стек)",font=fcc,fill=ACCENT,anchor="mm")
d.text((stk_x+8,stk_y+20),"ptr  → адреса [5]",font=fcc,fill=TEXT,anchor="lm")
d.text((stk_x+8,stk_y+32),"len  = 4",font=fcc,fill=TEXT,anchor="lm")
d.text((stk_x+8,stk_y+44),"heap НЕ виділяється!",font=fcc,fill=ORANGE,anchor="lm")
d.line([(mid_span,span_y-16+2),(stk_x,stk_y+30)],fill=ACCENT,width=1)

# ============================================================
# MIDDLE: 3 panels — API, ReadOnlySpan, ref struct limits
# ============================================================
row2_y=my+mh+12; row2_h=185

panels=[
    {
        "title":"Span<T> — API",
        "color":ACCENT,
        "items":[
            ("arr.AsSpan()",          "весь масив як Span"),
            ("arr.AsSpan(i, len)",    "зріз масиву"),
            ("str.AsSpan()",          "рядок → ReadOnlySpan<char>"),
            ("span[i]",               "доступ за індексом"),
            ("span.Slice(i, len)",    "підзріз без копії"),
            ("span.Length",           "кількість елементів"),
            ("span.CopyTo(dst)",      "копіювати у масив/Span"),
            ("span.Fill(val)",        "заповнити значенням"),
            ("span.Clear()",          "→ 0 / null / false"),
            ("span.SequenceEqual(s2)","побайтне порівняння"),
        ]
    },
    {
        "title":"ReadOnlySpan<T>",
        "color":ORANGE,
        "items":[
            ("ReadOnlySpan<char>",       "незмінний span рядка"),
            ("str.AsSpan()",             "→ ReadOnlySpan<char>"),
            ("int.TryParse(span, …)",    "парсинг без string"),
            ("double.TryParse(span, …)", "те саме для double"),
            ("span.IndexOf(',')",        "пошук символу"),
            ("span.Slice(0,i)",          "підрядок без копії"),
            ("MemoryExtensions.Trim(sp)","Trim без копії"),
            ("span == other",            "порівняння вмісту"),
        ]
    },
    {
        "title":"Обмеження ref struct",
        "color":RED,
        "items":[
            ("НЕ можна поле класу",   "тільки локальна змінна"),
            ("НЕ можна async/await",  "Span живе на стеку"),
            ("НЕ можна boxing",       "object x = span → помилка"),
            ("НЕ можна у масиві",     "Span<T>[] неможливо"),
            ("НЕ можна IEnumerable",  "foreach OK, LINQ — ні"),
            ("Memory<T>",             "для heap/async-сценаріїв"),
            ("ReadOnlyMemory<T>",     "незмінний аналог Memory"),
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
        iy=row2_y+34+j*17
        if iy+14>row2_y+row2_h-4: break
        d.rounded_rectangle([px+5,iy-3,px+PW-5,iy+12],radius=2,fill=DARK,outline=LINE,width=1)
        d.text((px+9,iy+4),name,font=fcc,fill=col,anchor="lm")
        d.text((px+PW//2+4,iy+4),f"// {desc}",font=fcc,fill=MUTED,anchor="lm")

# ============================================================
# BOTTOM: performance comparison
# ============================================================
bot_y=row2_y+row2_h+10; bot_h=58
d.rounded_rectangle([20,bot_y,W-20,bot_y+bot_h],radius=6,fill=PANEL,outline=ACCENT,width=1)
d.text((W//2,bot_y+12),"Порівняння: string.Split vs Span-парсинг",font=fh,fill=ACCENT,anchor="mm")
d.line([(30,bot_y+26),(W-30,bot_y+26)],fill=LINE,width=1)

cmp_rows=[
    ("Підхід","Виділяє heap?","GC-тиск","Підходить для"),
    ("string.Split / Substring","Так (кожен підрядок)","Високий","простого коду, малих даних"),
    ("ReadOnlySpan<char> + Slice","Ні (вказівники)","Нульовий","гарячий шлях, парсинг потоків"),
]
cx2=[30,230,430,560]
for ri,row in enumerate(cmp_rows):
    iy=bot_y+30+ri*14
    clrs=[MUTED,MUTED,MUTED,MUTED] if ri==0 else ([RED,RED,MUTED] if ri==1 else [ACCENT,ACCENT,TEXT])
    for ci,(val,cx) in enumerate(zip(row,cx2)):
        d.text((cx,iy),val,font=fcc,fill=clrs[ci] if ci<3 else TEXT,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/13-05/span-overview.png"
img.save(out); print("OK:",out)
