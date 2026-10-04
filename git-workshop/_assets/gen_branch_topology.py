from PIL import Image, ImageDraw, ImageFont

BG     = (17, 20, 19)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
ACCENT = (118, 199, 173)
LINE_C = (44, 53, 49)
WARN   = (240, 160, 75)
RED    = (215, 110, 110)
BLUE   = (90, 150, 210)
DIM    = (95, 112, 106)
GREEN2 = (80, 170, 120)
PURPLE = (160, 120, 210)
GOLD   = (200, 175, 90)

W, H = 1400, 790
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def font(p, s):
    try:    return ImageFont.truetype(p, s)
    except: return ImageFont.load_default()

FB = r"C:\Windows\Fonts\arialbd.ttf"
FR = r"C:\Windows\Fonts\arial.ttf"
FM = r"C:\Windows\Fonts\cour.ttf"

f_title = font(FB, 24)
f_head  = font(FB, 15)
f_body  = font(FR, 13)
f_label = font(FB, 12)
f_cmd   = font(FM, 12)
f_tiny  = font(FR, 11)

def rr(d, xy, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def tsize(text, fnt):
    bb = draw.textbbox((0, 0), text, font=fnt)
    return bb[2] - bb[0], bb[3] - bb[1]

def ctext(cx, cy, text, fnt, fill):
    bb = draw.textbbox((0, 0), text, font=fnt)
    draw.text((cx - (bb[2] - bb[0]) // 2 - bb[0], cy - (bb[3] - bb[1]) // 2 - bb[1]), text, font=fnt, fill=fill)

def ltext(x, cy, text, fnt, fill):
    bb = draw.textbbox((0, 0), text, font=fnt)
    draw.text((x - bb[0], cy - (bb[3] - bb[1]) // 2 - bb[1]), text, font=fnt, fill=fill)

def node(x, y, col, r=8):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=BG, width=2)

def merge_node(x, y, col):
    draw.ellipse([x - 13, y - 13, x + 13, y + 13], fill=col, outline=TEXT, width=2)

def badge(cx, cy, text, col):
    tw, _ = tsize(text, f_label)
    rr(draw, [cx - tw // 2 - 9, cy - 11, cx + tw // 2 + 9, cy + 11], 5, (22, 28, 26), outline=col, width=1)
    ctext(cx, cy, text, f_label, col)

def dots(x, y, col):
    for i in range(3):
        draw.ellipse([x + i * 10 - 2, y - 2, x + i * 10 + 2, y + 2], fill=col)

def lane(x_from, y_from, x_to, y_to, col, bend=60):
    """Diagonal from the fork commit, then horizontal along the lane."""
    draw.line([(x_from, y_from), (x_from + bend, y_to)], fill=col, width=3)
    draw.line([(x_from + bend, y_to), (x_to, y_to)], fill=col, width=3)

# ── Title ─────────────────────────────────────────────────────────────────────
ctext(W // 2, 26, "Git Workflow: структура курсу (Lab-01 → Lab-22)", f_title, ACCENT)

# ══════════════════════════════════════════════════════════════════════════════
# Graph
# ══════════════════════════════════════════════════════════════════════════════
L1_Y, L2_Y, MAIN_Y, L3_Y = 92, 162, 262, 352
INIT_X = 140

# Lab-01 / Lab-02: fork from the initial commit, never come back
for y, name, title, col in [(L1_Y, "Lab-01", "Основи C#", ACCENT),
                            (L2_Y, "Lab-02", "Масиви", BLUE)]:
    lane(INIT_X, MAIN_Y, 520, y, col, bend=80)
    for x in [240, 310, 380]:
        node(x, y, col)
    dots(422, y, col)
    node(480, y, col)
    node(520, y, col)
    ltext(232, y + 20, f"{name.replace('-', '')}: project", f_tiny, MUTED)
    ctext(520, y + 20, "Task08", f_tiny, MUTED)
    badge(590, y, name, col)
    ltext(638, y, f"({title})  →  push на GitHub, у main НЕ зливається", f_body, RED)

# main line
draw.line([(INIT_X, MAIN_Y), (1340, MAIN_Y)], fill=GREEN2, width=3)
node(INIT_X, MAIN_Y, GREEN2, 10)
for i, (txt, col) in enumerate([("initial commit", MUTED), (".gitignore + .slnx", DIM)]):
    tw, _ = tsize(txt, f_tiny)
    ltext(INIT_X - 16 - tw, MAIN_Y + 14 + i * 15, txt, f_tiny, col)
badge(INIT_X - 50, MAIN_Y - 22, "main", GREEN2)

# Lab-03 .. Lab-04: fork from main, come back with --no-ff merge
cycles = [
    (INIT_X, 600, "Lab-03", "Класи", PURPLE, "Merge Lab-03"),
    (600, 1020, "Lab-04", "Члени класу", GOLD, "Merge Lab-04"),
]
for fork_x, merge_x, name, title, col, mmsg in cycles:
    start = fork_x + 70
    end = merge_x - 70
    draw.line([(fork_x, MAIN_Y), (start, L3_Y)], fill=col, width=3)
    draw.line([(start, L3_Y), (end, L3_Y)], fill=col, width=3)
    draw.line([(end, L3_Y), (merge_x, MAIN_Y)], fill=col, width=3)
    tag = name.replace("-", "")
    pts = [start + 20, start + 90, start + 160]
    for x in pts:
        node(x, L3_Y, col)
    dots(start + 202, L3_Y, col)
    node(end - 10, L3_Y, col)
    ctext(pts[0], L3_Y + 20, "project", f_tiny, MUTED)
    ctext(pts[1], L3_Y + 20, "Task01", f_tiny, MUTED)
    ctext(pts[2], L3_Y + 20, "Task02", f_tiny, MUTED)
    ctext(end - 10, L3_Y + 20, "Task08", f_tiny, MUTED)
    badge((start + end) // 2, L3_Y + 48, name, col)
    ctext((start + end) // 2, L3_Y + 72, title, f_tiny, MUTED)
    merge_node(merge_x, MAIN_Y, col)
    ctext(merge_x, MAIN_Y - 42, "--no-ff", f_cmd, DIM)
    ctext(merge_x, MAIN_Y - 26, mmsg, f_cmd, col)

dots(1100, MAIN_Y - 14, MUTED)
ctext(1110, MAIN_Y + 22, "Lab-05 … Lab-21", f_tiny, MUTED)

merge_node(1210, MAIN_Y, ACCENT)
ctext(1210, MAIN_Y - 26, "Merge Lab-22", f_cmd, ACCENT)
ctext(1210, MAIN_Y + 28, "SOLID + DI", f_tiny, MUTED)

badge(1310, MAIN_Y - 24, "main", GREEN2)

# legend under the graph
ltext(60, 452, "Коміт завдання:  LabXX TaskYY   ·   гілка:  Lab-XX   ·   кожна гілка відходить від поточного main",
      f_body, MUTED)

# ══════════════════════════════════════════════════════════════════════════════
# Bottom panels
# ══════════════════════════════════════════════════════════════════════════════
SEP_Y = 478
draw.line([(40, SEP_Y), (W - 40, SEP_Y)], fill=LINE_C, width=1)

S2_Y = SEP_Y + 14
PAN_H = H - S2_Y - 16
LW = 760
RW = W - 80 - LW - 20

# ── LEFT: one lab cycle ───────────────────────────────────────────────────────
LX = 40
rr(draw, [LX, S2_Y, LX + LW, S2_Y + PAN_H], 8, (20, 26, 24), outline=(45, 65, 54), width=1)
ctext(LX + LW // 2, S2_Y + 20, "Повний цикл однієї лаби (Лаби 03+)", f_head, ACCENT)

steps = [
    ("git checkout main",                       "старт від main"),
    ("git checkout -b Lab-03",                  "гілка для лаби"),
    ("git add <файли завдання>",                ""),
    ('git commit -m "Lab03 Task01"',            "коміт після кожного завдання"),
    ("# ... Task02 ... Task08 ...",             ""),
    ("git push -u origin Lab-03",               "гілка на GitHub"),
    ("git checkout main",                       ""),
    ('git merge --no-ff Lab-03 -m "Merge Lab-03: ..."', "злиття"),
    ("git push",                                "main на GitHub"),
]
CMD_COL_W = 430
for i, (cmd, comment) in enumerate(steps):
    cy = S2_Y + 50 + i * 23
    col = DIM if cmd.startswith("#") else TEXT
    ltext(LX + 22, cy, cmd, f_cmd, col)
    if comment:
        ltext(LX + 22 + CMD_COL_W, cy, f"← {comment}", f_tiny, DIM)
ltext(LX + 22, S2_Y + PAN_H - 18, "Лаби 01–02: лише git push -u origin Lab-0X, без merge.", f_tiny, RED)

# ── RIGHT: why --no-ff ────────────────────────────────────────────────────────
RX = LX + LW + 20
rr(draw, [RX, S2_Y, RX + RW, S2_Y + PAN_H], 8, (20, 26, 24), outline=(45, 65, 54), width=1)
ctext(RX + RW // 2, S2_Y + 20, "Навіщо --no-ff ?", f_head, WARN)

# fast-forward
FF_Y = S2_Y + 62
ltext(RX + 24, FF_Y - 18, "Без --no-ff (fast-forward):", f_body, RED)
ff = [RX + 50, RX + 130, RX + 210, RX + 290]
draw.line([(ff[0], FF_Y + 10), (ff[-1], FF_Y + 10)], fill=MUTED, width=2)
for i, x in enumerate(ff):
    node(x, FF_Y + 10, GREEN2 if i == 0 else PURPLE, 7)
ltext(RX + 24, FF_Y + 36, "main просто «з'їдає» коміти — межі лаби не видно", f_tiny, RED)

# no-ff
NF_Y = FF_Y + 92
ltext(RX + 24, NF_Y - 22, "З --no-ff (наш підхід):", f_body, ACCENT)
m0, m1 = RX + 50, RX + 290
t = [RX + 130, RX + 210]
draw.line([(m0, NF_Y), (m1, NF_Y)], fill=GREEN2, width=2)
draw.line([(m0, NF_Y), (t[0], NF_Y + 34)], fill=PURPLE, width=2)
draw.line([(t[0], NF_Y + 34), (t[1], NF_Y + 34)], fill=PURPLE, width=2)
draw.line([(t[1], NF_Y + 34), (m1, NF_Y)], fill=PURPLE, width=2)
node(m0, NF_Y, GREEN2, 7)
for x in t:
    node(x, NF_Y + 34, PURPLE, 7)
merge_node(m1, NF_Y, PURPLE)
ltext(RX + 24, NF_Y + 60, "окремий merge-коміт — видно, де лаба почалась і закінчилась", f_tiny, ACCENT)

out = r"C:\Users\Yurii\source\repos\OOP-Tomka-CourseForHardCoders\git-workshop\_assets\branch-topology.png"
img.save(out, "PNG")
print(f"Saved {W}x{H}")
