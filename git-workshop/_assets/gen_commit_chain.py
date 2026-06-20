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

W, H = 1400, 620
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def font(p, s):
    try:    return ImageFont.truetype(p, s)
    except: return ImageFont.load_default()

FB = r"C:\Windows\Fonts\arialbd.ttf"
FR = r"C:\Windows\Fonts\arial.ttf"
FM = r"C:\Windows\Fonts\cour.ttf"

f_title = font(FB, 24)
f_head  = font(FB, 17)
f_body  = font(FR, 14)
f_small = font(FR, 12)
f_sha   = font(FM, 12)
f_label = font(FB, 13)
f_cmd   = font(FM, 13)
f_note  = font(FR, 13)

def rr(d, xy, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def ctext(d, cx, cy, text, fnt, fill):
    bb = d.textbbox((0,0), text, font=fnt)
    d.text((cx-(bb[2]-bb[0])//2, cy-(bb[3]-bb[1])//2), text, font=fnt, fill=fill)

def ltext(d, x, cy, text, fnt, fill):
    bb = d.textbbox((0,0), text, font=fnt)
    d.text((x, cy-(bb[3]-bb[1])//2), text, font=fnt, fill=fill)

def wrap(msg, max_chars=18):
    """Split at last space before max_chars."""
    if len(msg) <= max_chars:
        return [msg]
    idx = msg.rfind(" ", 0, max_chars)
    if idx == -1: idx = max_chars
    return [msg[:idx].strip(), msg[idx:].strip()]

def arrow_down(d, x, y0, y1, color, w=2):
    d.line([(x,y0),(x,y1-8)], fill=color, width=w)
    d.polygon([(x-5,y1-8),(x,y1),(x+5,y1-8)], fill=color)

# ── TITLE ─────────────────────────────────────────────────────────────────────
ctext(draw, W//2, 22, "Git: Що таке коміт і гілка", f_title, ACCENT)

# ══════════════════════════════════════════════════════════════════════════════
# TOP SECTION: anatomy box (left) + commit chain (right)
# ══════════════════════════════════════════════════════════════════════════════
T_Y = 52

# ── Commit anatomy box ────────────────────────────────────────────────────────
AX, AY, AW, AH = 34, T_Y, 330, 215
rr(draw, [AX,AY,AX+AW,AY+AH], 10, (22,32,28), outline=(55,90,70), width=2)
ctext(draw, AX+AW//2, AY+22, "Об'єкт коміту", f_head, ACCENT)
draw.line([(AX+14,AY+38),(AX+AW-14,AY+38)], fill=LINE_C, width=1)

fields = [
    ("SHA",     "a3f82c1",              ACCENT),
    ("tree",    "знімок файлів",        MUTED),
    ("parent",  "SHA попереднього",     BLUE),
    ("author",  "Ivan Petrenko",        TEXT),
    ("date",    "2025-09-01 10:23",     MUTED),
    ("message", "Lab01 Task01: add..",  WARN),
]
for i,(k,v,c) in enumerate(fields):
    fy = AY + 54 + i*26
    ltext(draw, AX+18, fy, k, f_sha, DIM)
    ltext(draw, AX+105, fy, v, f_sha, c)

rr(draw, [AX,AY+AH+8,AX+AW,AY+AH+54], 8, (20,30,25), outline=(50,80,60), width=1)
ctext(draw, AX+AW//2, AY+AH+24, "Коміт НЕЗМІННИЙ (immutable)", f_body, ACCENT)
ctext(draw, AX+AW//2, AY+AH+42, "Зміна повідомлення = новий SHA", f_small, MUTED)

# ── Commit chain ──────────────────────────────────────────────────────────────
CB_W, CB_H, CB_GAP = 148, 70, 46
CS_X = 384   # chain start X
CS_Y = T_Y + 10

commits_data = [
    ("a1b2c3d", "Initial commit",       MUTED),
    ("e4f5a6b", "Lab01 Task01: Hello",  TEXT),
    ("c7d8e9f", "Lab01 Task02: Patient",TEXT),
    ("3a4b5c6", "Lab01 Task03: Doctor", ACCENT),
]

commit_cx = []   # center X of each commit box
for i,(sha,msg,col) in enumerate(commits_data):
    cx = CS_X + i*(CB_W+CB_GAP)
    cy = CS_Y
    is_last = (i == len(commits_data)-1)
    bdr = (75,120,95) if is_last else (55,80,66)
    rr(draw, [cx,cy,cx+CB_W,cy+CB_H], 8, (22,32,28), outline=bdr, width=2 if is_last else 1)
    ctext(draw, cx+CB_W//2, cy+16, sha, f_sha, col)
    draw.line([(cx+10,cy+28),(cx+CB_W-10,cy+28)], fill=LINE_C, width=1)
    lines = wrap(msg)
    for li,line in enumerate(lines):
        ctext(draw, cx+CB_W//2, cy+40+li*17, line, f_small, MUTED)
    commit_cx.append(cx+CB_W//2)

    if i>0:
        ax0 = cx - 2
        ax1 = cx - CB_GAP + 2
        ay  = cy + CB_H//2 - 6
        draw.line([(ax0,ay),(ax1+8,ay)], fill=BLUE, width=2)
        draw.polygon([(ax1+8,ay-4),(ax1,ay),(ax1+8,ay+4)], fill=BLUE)
        ctext(draw, cx-CB_GAP//2, ay-13, "parent", f_small, BLUE)

# Branch + HEAD pointers on latest commit
LAT_CX = commit_cx[-1]
BR_Y   = CS_Y + CB_H + 14
HD_Y   = BR_Y + 32 + 10

# Lab-01 branch box
rr(draw, [LAT_CX-42,BR_Y,LAT_CX+42,BR_Y+30], 6, (26,46,33), outline=ACCENT, width=2)
ctext(draw, LAT_CX, BR_Y+15, "Lab-01", f_label, ACCENT)
arrow_down(draw, LAT_CX, BR_Y, CS_Y+CB_H, ACCENT)

# HEAD box
rr(draw, [LAT_CX-32,HD_Y,LAT_CX+32,HD_Y+28], 6, (38,32,18), outline=WARN, width=2)
ctext(draw, LAT_CX, HD_Y+14, "HEAD", f_label, WARN)
arrow_down(draw, LAT_CX, HD_Y, BR_Y+30, WARN)

# Insight box — positioned to the LEFT of the branch pointer, not right
INS_X  = LAT_CX - 270
INS_Y  = BR_Y - 4
INS_W  = 200
rr(draw, [INS_X,INS_Y,INS_X+INS_W,INS_Y+76], 8, (22,28,24), outline=LINE_C, width=1)
ctext(draw, INS_X+INS_W//2, INS_Y+18, "Гілка = pointer", f_body,  ACCENT)
ctext(draw, INS_X+INS_W//2, INS_Y+36, "на коміт", f_body,  ACCENT)
ctext(draw, INS_X+INS_W//2, INS_Y+54, "Створити гілку — дешево:", f_small, MUTED)
ctext(draw, INS_X+INS_W//2, INS_Y+68, "лише 41-байтний файл", f_small, DIM)

# "Ланцюжок комітів" label
ltext(draw, CS_X, T_Y+2, "Ланцюжок комітів (кожен знає свого батька):", f_label, MUTED)

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM SECTION: before / after git checkout -b Lab-01
# ══════════════════════════════════════════════════════════════════════════════
SEP_Y = HD_Y + 48
draw.line([(34,SEP_Y),(W-34,SEP_Y)], fill=LINE_C, width=1)

# Command label on separator
CMD_LBL = "  git checkout -b Lab-01  "
bb = draw.textbbox((0,0), CMD_LBL, font=f_cmd)
cw = bb[2]-bb[0]; ch = bb[3]-bb[1]
cx_cmd = W//2
rr(draw, [cx_cmd-cw//2-6,SEP_Y-ch//2-5,cx_cmd+cw//2+6,SEP_Y+ch//2+5], 4, (35,28,15), outline=WARN, width=1)
ctext(draw, cx_cmd, SEP_Y, CMD_LBL, f_cmd, WARN)

S2_Y = SEP_Y + 14
PAN_H = H - S2_Y - 16
HALF  = (W - 100) // 2

# ── BEFORE ────────────────────────────────────────────────────────────────────
BX = 34
rr(draw, [BX,S2_Y,BX+HALF,S2_Y+PAN_H], 8, (20,26,24), outline=(45,65,54), width=1)
ctext(draw, BX+HALF//2, S2_Y+18, "ДО  (знаходимось на main)", f_head, MUTED)

b_cs_x = BX + 50
b_cb_w, b_cb_h, b_cb_g = 130, 56, 40
b_commits = [("a1b2c3","Init"), ("e4f5a6","Task01")]
b_centers = []
for i,(sha,msg) in enumerate(b_commits):
    cx = b_cs_x + i*(b_cb_w+b_cb_g)
    cy = S2_Y + 40
    rr(draw, [cx,cy,cx+b_cb_w,cy+b_cb_h], 6, (22,32,28), outline=(55,80,66), width=1)
    ctext(draw, cx+b_cb_w//2, cy+16, sha, f_sha, TEXT)
    ctext(draw, cx+b_cb_w//2, cy+38, msg, f_small, MUTED)
    b_centers.append(cx+b_cb_w//2)
    if i>0:
        draw.line([(cx-2,cy+b_cb_h//2),(cx-b_cb_g+2,cy+b_cb_h//2)], fill=BLUE, width=2)
        draw.polygon([(cx-b_cb_g+2,cy+b_cb_h//2-4),(cx-b_cb_g-6,cy+b_cb_h//2),(cx-b_cb_g+2,cy+b_cb_h//2+4)], fill=BLUE)

b_lat = b_centers[-1]
b_lat_cy = S2_Y + 40
rr(draw, [b_lat-32,b_lat_cy+b_cb_h+8,b_lat+32,b_lat_cy+b_cb_h+36], 6, (28,45,35), outline=GREEN2, width=2)
ctext(draw, b_lat, b_lat_cy+b_cb_h+22, "main", f_label, GREEN2)
arrow_down(draw, b_lat, b_lat_cy+b_cb_h+8, b_lat_cy+b_cb_h, GREEN2)

rr(draw, [b_lat-30,b_lat_cy+b_cb_h+48,b_lat+30,b_lat_cy+b_cb_h+74], 6, (38,32,18), outline=WARN, width=2)
ctext(draw, b_lat, b_lat_cy+b_cb_h+61, "HEAD", f_label, WARN)
arrow_down(draw, b_lat, b_lat_cy+b_cb_h+48, b_lat_cy+b_cb_h+38, WARN)

# note
rr(draw, [BX+14,S2_Y+PAN_H-56,BX+HALF-14,S2_Y+PAN_H-14], 6, (18,24,22), outline=LINE_C, width=1)
ctext(draw, BX+HALF//2, S2_Y+PAN_H-42, "HEAD вказує на main,", f_small, MUTED)
ctext(draw, BX+HALF//2, S2_Y+PAN_H-24, "main вказує на Task01", f_small, MUTED)

# ── AFTER ─────────────────────────────────────────────────────────────────────
AX2 = BX + HALF + 32
rr(draw, [AX2,S2_Y,AX2+HALF,S2_Y+PAN_H], 8, (20,26,24), outline=(45,80,60), width=1)
ctext(draw, AX2+HALF//2, S2_Y+18, "ПІСЛЯ  (тепер на Lab-01)", f_head, ACCENT)

a_cs_x = AX2 + 50
a_commits = [("a1b2c3","Init"), ("e4f5a6","Task01")]
a_centers = []
for i,(sha,msg) in enumerate(a_commits):
    cx = a_cs_x + i*(b_cb_w+b_cb_g)
    cy = S2_Y + 40
    rr(draw, [cx,cy,cx+b_cb_w,cy+b_cb_h], 6, (22,32,28), outline=(55,80,66), width=1)
    ctext(draw, cx+b_cb_w//2, cy+16, sha, f_sha, TEXT)
    ctext(draw, cx+b_cb_w//2, cy+38, msg, f_small, MUTED)
    a_centers.append(cx+b_cb_w//2)
    if i>0:
        draw.line([(cx-2,cy+b_cb_h//2),(cx-b_cb_g+2,cy+b_cb_h//2)], fill=BLUE, width=2)
        draw.polygon([(cx-b_cb_g+2,cy+b_cb_h//2-4),(cx-b_cb_g-6,cy+b_cb_h//2),(cx-b_cb_g+2,cy+b_cb_h//2+4)], fill=BLUE)

a_lat  = a_centers[-1]
a_cy   = S2_Y + 40

# main (unchanged, greyed out slightly)
m_off = -46
rr(draw, [a_lat+m_off-32,a_cy+b_cb_h+8,a_lat+m_off+32,a_cy+b_cb_h+36], 6, (24,38,29), outline=GREEN2, width=1)
ctext(draw, a_lat+m_off, a_cy+b_cb_h+22, "main", f_label, GREEN2)
arrow_down(draw, a_lat+m_off, a_cy+b_cb_h+8, a_cy+b_cb_h, GREEN2)

# Lab-01 (new, bright)
l_off = +50
rr(draw, [a_lat+l_off-38,a_cy+b_cb_h+8,a_lat+l_off+38,a_cy+b_cb_h+36], 6, (26,48,34), outline=ACCENT, width=2)
ctext(draw, a_lat+l_off, a_cy+b_cb_h+22, "Lab-01", f_label, ACCENT)
arrow_down(draw, a_lat+l_off, a_cy+b_cb_h+8, a_cy+b_cb_h, ACCENT)

# HEAD → Lab-01
head_ax = a_lat + l_off
rr(draw, [head_ax-30,a_cy+b_cb_h+48,head_ax+30,a_cy+b_cb_h+74], 6, (38,32,18), outline=WARN, width=2)
ctext(draw, head_ax, a_cy+b_cb_h+61, "HEAD", f_label, WARN)
arrow_down(draw, head_ax, a_cy+b_cb_h+48, a_cy+b_cb_h+38, WARN)

# note
rr(draw, [AX2+14,S2_Y+PAN_H-56,AX2+HALF-14,S2_Y+PAN_H-14], 6, (18,24,22), outline=LINE_C, width=1)
ctext(draw, AX2+HALF//2, S2_Y+PAN_H-42, "Обидва (main + Lab-01) вказують", f_small, MUTED)
ctext(draw, AX2+HALF//2, S2_Y+PAN_H-24, "на ОДИН коміт — файли не копіюються!", f_small, ACCENT)

out = r"C:\Users\Yurii\source\repos\OOP-Tomka-CourseForHardCoders\git-workshop\_assets\commit-chain.png"
img.save(out, "PNG")
print(f"Saved {W}x{H}")
