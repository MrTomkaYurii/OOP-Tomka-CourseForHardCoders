from PIL import Image, ImageDraw, ImageFont

BG     = (17, 20, 19)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
ACCENT = (118, 199, 173)
LINE_C = (44, 53, 49)
WARN   = (240, 160, 75)
BLUE   = (90, 150, 210)
DIM    = (80, 100, 95)
GREEN2 = (80, 170, 120)
RED2   = (200, 90, 90)
PURPLE = (160, 120, 210)

W, H = 1400, 640
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def font(p, s):
    try:    return ImageFont.truetype(p, s)
    except: return ImageFont.load_default()

FB = r"C:\Windows\Fonts\arialbd.ttf"
FR = r"C:\Windows\Fonts\arial.ttf"
FM = r"C:\Windows\Fonts\cour.ttf"

f_title  = font(FB, 24)
f_head   = font(FB, 16)
f_body   = font(FR, 13)
f_small  = font(FR, 12)
f_sha    = font(FM, 11)
f_label  = font(FB, 12)
f_cmd    = font(FM, 12)
f_tiny   = font(FR, 11)

def rr(d, xy, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def ctext(d, cx, cy, text, fnt, fill):
    bb = d.textbbox((0,0), text, font=fnt)
    d.text((cx-(bb[2]-bb[0])//2, cy-(bb[3]-bb[1])//2), text, font=fnt, fill=fill)

def ltext(d, x, cy, text, fnt, fill):
    bb = d.textbbox((0,0), text, font=fnt)
    d.text((x, cy-(bb[3]-bb[1])//2), text, font=fnt, fill=fill)

def circle(d, cx, cy, r, fill, outline=None, width=1):
    d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=fill, outline=outline, width=width)

def commit(cx, cy, r, color, label=None, label_above=True, sha=None, sha_color=None):
    circle(draw, cx, cy, r, color, outline=BG, width=2)
    if sha:
        sy = cy-(r+13) if label_above else cy+(r+4)
        ctext(draw, cx, sy, sha, f_sha, sha_color or DIM)
    if label:
        ly = cy-(r+26) if label_above else cy+(r+18)
        ctext(draw, cx, ly, label, f_tiny, MUTED)

# ── Title ─────────────────────────────────────────────────────────────────────
ctext(draw, W//2, 22, "Git: Merge vs Rebase", f_title, ACCENT)

# ══════════════════════════════════════════════════════════════════════════════
# SETUP: "BEFORE" state — horizontal strip at top
# A ── B ── C ── D  (main, C,D = new)
#       └── E ── F  (Lab-01, your work)
# ══════════════════════════════════════════════════════════════════════════════
NR = 10    # bigger nodes for clarity

BEF_X0, BEF_Y0, BEF_W, BEF_H = 34, 48, 640, 148
rr(draw,[BEF_X0,BEF_Y0,BEF_X0+BEF_W,BEF_Y0+BEF_H],8,(20,28,24),outline=LINE_C,width=1)
ctext(draw,BEF_X0+BEF_W//2,BEF_Y0+14,
      "Ситуація перед вибором стратегії",f_body,MUTED)

MAIN_Y = BEF_Y0 + 58
FEAT_Y = BEF_Y0 + 112
AX,BX,CX,DX = 80,170,260,350
EX,FX        = 260,350

# lines
draw.line([(AX-NR,MAIN_Y),(DX+NR,MAIN_Y)],fill=GREEN2,width=3)
draw.line([(EX-NR,FEAT_Y),(FX+NR,FEAT_Y)],fill=ACCENT,width=3)
draw.line([(BX+NR,MAIN_Y+NR),(EX-NR,FEAT_Y-NR)],fill=ACCENT,width=2)

for (cx,cy,col,sha,lbl,la) in [
    (AX,MAIN_Y,GREEN2,"A","Init",    True),
    (BX,MAIN_Y,GREEN2,"B","",        True),
    (CX,MAIN_Y,GREEN2,"C","new!",   True),
    (DX,MAIN_Y,GREEN2,"D","new!",   True),
    (EX,FEAT_Y,ACCENT,"E","Task01", False),
    (FX,FEAT_Y,ACCENT,"F","Task02", False),
]:
    commit(cx,cy,NR,col,sha=sha,label=lbl,label_above=la)

rr(draw,[AX-16,MAIN_Y-48,AX+50,MAIN_Y-28],5,(26,44,33),outline=GREEN2,width=1)
ctext(draw,AX+17,MAIN_Y-38,"main",f_label,GREEN2)
rr(draw,[EX-22,FEAT_Y+24,EX+56,FEAT_Y+42],5,(22,36,30),outline=ACCENT,width=1)
ctext(draw,EX+17,FEAT_Y+33,"Lab-01",f_label,ACCENT)

# callouts
ctext(draw,(CX+DX)//2,MAIN_Y-60,"нові коміти main",f_tiny,MUTED)
draw.line([((CX+DX)//2,MAIN_Y-52),((CX+DX)//2,MAIN_Y-NR-2)],fill=DIM,width=1)
ctext(draw,(EX+FX)//2,FEAT_Y+56,"ваша робота",f_tiny,MUTED)

# Legend box (right side of BEFORE strip)
LEG_X = BEF_X0 + BEF_W + 20
rr(draw,[LEG_X,BEF_Y0,LEG_X+340,BEF_Y0+BEF_H],8,(20,26,24),outline=LINE_C,width=1)
ctext(draw,LEG_X+170,BEF_Y0+16,"Як синхронізуватись з main?",f_head,MUTED)
items = [
    (GREEN2, "Merge —  зберігає топологію ('ромб' у grafі)"),
    (BLUE,   "Rebase — лінійна історія (E,F перебазовуються)"),
    (WARN,   "Обидва дають однаковий кінцевий код!"),
]
for i,(col,txt) in enumerate(items):
    iy = BEF_Y0 + 46 + i*30
    circle(draw, LEG_X+22, iy, 7, col)
    ltext(draw, LEG_X+40, iy, txt, f_body, col)

MA_Y0 = BEF_Y0 + BEF_H + 18

# ══════════════════════════════════════════════════════════════════════════════
# VARIANT A — Merge (left panel)
# ══════════════════════════════════════════════════════════════════════════════
# Result:
#   A ── B ── C ── D ── M    ← main (M = merge commit)
#             └── E ── F ──┘  ← Lab-01
#

MA_X  = 140
MA_Y0 = BEF_Y0 + BEF_H + 18
PAN_W = (W - 80) // 2
PAN_H = H - MA_Y0 - 16

rr(draw,[MA_X,MA_Y0,MA_X+PAN_W,MA_Y0+PAN_H],10,(19,26,23),outline=(45,75,58),width=2)

A_TITLE_Y = MA_Y0+20
ctext(draw,MA_X+PAN_W//2, A_TITLE_Y, "git merge main", f_head, GREEN2)
ctext(draw,MA_X+PAN_W//2, A_TITLE_Y+22,"(або git merge --no-ff Lab-01 після завершення)",f_tiny,MUTED)

# Graph
GM_Y = MA_Y0 + 80   # main row
GF_Y = MA_Y0 + 148  # feature row

GBX  = MA_X+45
step = 82
GA   = GBX
GB   = GBX+step
GC   = GBX+step*2
GD   = GBX+step*3
GM_m = GBX+step*4   # merge commit on main
GE   = GC
GF   = GD

# main line
draw.line([(GA-NR,GM_Y),(GM_m+NR,GM_Y)],fill=GREEN2,width=2)
# feature line
draw.line([(GE-NR,GF_Y),(GF+NR,GF_Y)],fill=ACCENT,width=2)
# diagonal: GB → GE
draw.line([(GB+NR,GM_Y+NR),(GE-NR,GF_Y-NR)],fill=ACCENT,width=2)
# diagonal: GF → merge (GM_m)
draw.line([(GF+NR,GF_Y-NR),(GM_m-NR,GM_Y+NR)],fill=ACCENT,width=2)

# merge commit node (special)
circle(draw,GM_m,GM_Y,NR+3,GREEN2,outline=ACCENT,width=2)
ctext(draw,GM_m,GM_Y-32,"Merge\ncommit",f_sha,GREEN2)
ctext(draw,GM_m,GM_Y-54,"M",f_sha,MUTED)

for (cx,cy,col,sha) in [(GA,GM_Y,GREEN2,"A"),(GB,GM_Y,GREEN2,"B"),
                         (GC,GM_Y,GREEN2,"C"),(GD,GM_Y,GREEN2,"D"),
                         (GE,GF_Y,ACCENT,"E"),(GF,GF_Y,ACCENT,"F")]:
    commit(cx,cy,NR,col,sha=sha,label_above=(cy==GM_Y))

# Labels
rr(draw,[GA-12,GM_Y-52,GA+48,GM_Y-34],5,(26,44,33),outline=GREEN2,width=1)
ctext(draw,GA+18,GM_Y-43,"main",f_label,GREEN2)
rr(draw,[GE-22,GF_Y+22,GE+50,GF_Y+40],5,(22,36,30),outline=ACCENT,width=1)
ctext(draw,GE+14,GF_Y+31,"Lab-01",f_label,ACCENT)

# Pros/cons
PC_Y = GF_Y + 56
pros = ["+ Зберігає точну історію гілки",
        "+ Видно коли саме злиття відбулось",
        "+ Безпечно для спільних гілок"]
cons = ["- Граф ускладнюється з часом",
        "- git log виглядає 'брудним'"]

for i,t in enumerate(pros):
    ltext(draw, MA_X+18, PC_Y+i*20, t, f_small, GREEN2)
for i,t in enumerate(cons):
    ltext(draw, MA_X+18, PC_Y+len(pros)*20+8+i*20, t, f_small, RED2)

# When to use box
WU_Y = MA_Y0+PAN_H-52
rr(draw,[MA_X+14,WU_Y,MA_X+PAN_W-14,WU_Y+38],6,(22,36,28),outline=(50,85,60),width=1)
ctext(draw,MA_X+PAN_W//2,WU_Y+14,"В курсі — ЗАВЖДИ merge --no-ff",f_body,ACCENT)
ctext(draw,MA_X+PAN_W//2,WU_Y+30,"(злиття лаби в main по завершенню)",f_tiny,MUTED)

# ══════════════════════════════════════════════════════════════════════════════
# VARIANT B — Rebase (right panel)
# ══════════════════════════════════════════════════════════════════════════════
# Result:
#   A ── B ── C ── D ── E' ── F'   ← main / Lab-01 (linear!)
# E', F' = перезаписані коміти з новим SHA

RB_X  = MA_X + PAN_W + 20
rr(draw,[RB_X,MA_Y0,RB_X+PAN_W,MA_Y0+PAN_H],10,(19,22,30),outline=(45,60,110),width=2)

B_TITLE_Y = MA_Y0+20
ctext(draw,RB_X+PAN_W//2, B_TITLE_Y, "git rebase main", f_head, BLUE)
ctext(draw,RB_X+PAN_W//2, B_TITLE_Y+22,"перебазовує коміти Lab-01 поверх нового main",f_tiny,MUTED)

# Graph — linear
RL_Y  = MA_Y0 + 104   # single line
RBX   = RB_X+40
rstep = 76

RA,RB,RC,RD,RE2,RF2 = [RBX+i*rstep for i in range(6)]

# main line
draw.line([(RA-NR,RL_Y),(RF2+NR,RL_Y)],fill=GREEN2,width=2)

for (cx,col,sha,orig) in [
    (RA,GREEN2,"A",""), (RB,GREEN2,"B",""), (RC,GREEN2,"C","new!"),
    (RD,GREEN2,"D","new!"),
    (RE2,BLUE,"E'",""), (RF2,BLUE,"F'",""),
]:
    commit(cx,RL_Y,NR,col,sha=sha,label=orig,label_above=True)

# Annotate E' and F' — rebased (new SHA)
ctext(draw,RE2,RL_Y+26,"= E (новий SHA)",f_sha,BLUE)
ctext(draw,RF2,RL_Y+26,"= F (новий SHA)",f_sha,BLUE)

# "Until" arrow showing where E,F were
ghost_y = RL_Y + 70
draw.line([(RD+NR,RL_Y+NR),(RE2-NR,ghost_y-NR)],fill=DIM,width=1)
draw.line([(RE2-NR,ghost_y),(RF2+NR,ghost_y)],fill=DIM,width=1)
commit(RE2,ghost_y,NR-2,DIM,sha="E",label_above=False)
commit(RF2,ghost_y,NR-2,DIM,sha="F",label_above=False)
ctext(draw,(RE2+RF2)//2,ghost_y+26,"старі E,F — видалені",f_tiny,DIM)

# Labels
rr(draw,[RA-12,RL_Y-52,RA+48,RL_Y-34],5,(26,36,48),outline=GREEN2,width=1)
ctext(draw,RA+18,RL_Y-43,"main",f_label,GREEN2)
rr(draw,[RE2-38,RL_Y-52,RE2+50,RL_Y-34],5,(20,28,44),outline=BLUE,width=2)
ctext(draw,RE2+6,RL_Y-43,"Lab-01",f_label,BLUE)

# Pros/cons
PC2_Y = ghost_y + 46
pros2 = ["+ Лінійна, чиста історія",
         "+ git log без 'ромбів'",
         "+ Простіше читати blame"]
cons2 = ["- Змінює SHA комітів (переписує)"]
warn2 =  "! НІКОЛИ не rebase спільних гілок"

STEP2 = 18
for i,t in enumerate(pros2):
    ltext(draw, RB_X+18, PC2_Y+i*STEP2, t, f_small, GREEN2)
off = len(pros2)*STEP2+6
for i,t in enumerate(cons2):
    ltext(draw, RB_X+18, PC2_Y+off+i*STEP2, t, f_small, RED2)
ltext(draw, RB_X+18, PC2_Y+off+len(cons2)*STEP2+6, warn2, f_small, WARN)

# When to use box
WU2_Y = MA_Y0+PAN_H-52
rr(draw,[RB_X+14,WU2_Y,RB_X+PAN_W-14,WU2_Y+38],6,(22,28,42),outline=(40,65,120),width=1)
ctext(draw,RB_X+PAN_W//2,WU2_Y+14,"Rebase — для прибирання локальних комітів",f_body,BLUE)
ctext(draw,RB_X+PAN_W//2,WU2_Y+30,"до PR або перед злиттям (інтерактивний: -i)",f_tiny,MUTED)

out = r"C:\Users\Yurii\source\repos\OOP-Tomka-CourseForHardCoders\git-workshop\_assets\merge-vs-rebase.png"
img.save(out, "PNG")
print(f"Saved {W}x{H}")
