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
PURPLE = (160, 120, 210)

W, H = 1400, 620
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def font(p, s):
    try:    return ImageFont.truetype(p, s)
    except: return ImageFont.load_default()

FB = r"C:\Windows\Fonts\arialbd.ttf"
FR = r"C:\Windows\Fonts\arial.ttf"
FM = r"C:\Windows\Fonts\cour.ttf"

f_title  = font(FB, 24)
f_head   = font(FB, 15)
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

def circle(d, cx, cy, r, fill, outline=None, width=1):
    d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=fill, outline=outline, width=width)

# ── Title ─────────────────────────────────────────────────────────────────────
ctext(draw, W//2, 20, "Git Workflow: Структура курсу (Lab-01 → Lab-22)", f_title, ACCENT)

# ══════════════════════════════════════════════════════════════════════════════
# Layout constants
# ══════════════════════════════════════════════════════════════════════════════
MAIN_Y   = 130        # Y of main branch line
LAB_Y    = 220        # Y of lab branch line (below main)
MERGE_Y  = MAIN_Y     # merge commit back to main
NODE_R   = 8          # commit node radius

# Columns: each "lab cycle" = [branch_point, T1, T2, T3, merge_point]
# We show 3 full cycles + dots + Lab-22 — must fit in W=1400
COL_START = 60
COL_STEP  = 65        # X distance between nodes within a lab (smaller = more fits)

# Helper: draw a commit node
def node(cx, cy, color, label=None, label_above=True, sha=None):
    circle(draw, cx, cy, NODE_R, color, outline=BG, width=2)
    if sha:
        ty = cy - 22 if label_above else cy + 14
        ctext(draw, cx, ty, sha, f_sha, DIM)
    if label:
        ty = cy - 36 if label_above else cy + 26
        ctext(draw, cx, ty, label, f_tiny, MUTED)

# ── Labs to display ───────────────────────────────────────────────────────────
labs = [
    {
        "name": "Lab-01",
        "title": "Intro to C#",
        "color": ACCENT,
        "tasks": ["Task01", "Task02", "Task03"],
        "merge_msg": "Merge Lab-01",
    },
    {
        "name": "Lab-02",
        "title": "Arrays",
        "color": BLUE,
        "tasks": ["Task01", "Task02", "Task03"],
        "merge_msg": "Merge Lab-02",
    },
    {
        "name": "Lab-03",
        "title": "Classes",
        "color": PURPLE,
        "tasks": ["Task01", "Task02", "Task03"],
        "merge_msg": "Merge Lab-03",
    },
]

# ── Draw main branch backbone ─────────────────────────────────────────────────
# main goes from left to right; we'll draw it segment by segment

# Initial commit
INIT_X = COL_START + 20
node(INIT_X, MAIN_Y, GREEN2, sha="a1b2c3", label="Initial\ncommit", label_above=False)

all_merge_xs  = []   # X positions of merge commits on main
branch_xs     = []   # X positions of branch-out points

cur_x = INIT_X

for li, lab in enumerate(labs):
    color    = lab["color"]
    n_tasks  = len(lab["tasks"])

    # Branch-out point (on main)
    branch_x = cur_x + (50 if li == 0 else COL_STEP)
    branch_xs.append(branch_x)

    # Task commits (on lab branch at LAB_Y)
    task_xs  = [branch_x + (t+1)*COL_STEP for t in range(n_tasks)]

    # Merge commit (back on main)
    merge_x  = task_xs[-1] + COL_STEP
    all_merge_xs.append(merge_x)

    # ── main line before branch ──────────────────────────────────────────
    draw.line([(cur_x+NODE_R, MAIN_Y),(branch_x-NODE_R, MAIN_Y)], fill=GREEN2, width=3)

    # branch-out node on main
    node(branch_x, MAIN_Y, GREEN2)

    # ── diagonal: main → lab branch ──────────────────────────────────────
    draw.line([(branch_x, MAIN_Y+NODE_R),(task_xs[0]-NODE_R, LAB_Y-NODE_R)],
              fill=color, width=2)

    # ── lab branch line ───────────────────────────────────────────────────
    if n_tasks > 1:
        draw.line([(task_xs[0]+NODE_R, LAB_Y),(task_xs[-1]-NODE_R, LAB_Y)],
                  fill=color, width=2)

    # Task commit nodes
    for ti, tx in enumerate(task_xs):
        task_label = lab["tasks"][ti]
        node(tx, LAB_Y, color, sha=f"T{li+1}{ti+1:02d}", label=task_label, label_above=False)

    # ── diagonal: lab branch → merge commit on main ───────────────────────
    draw.line([(task_xs[-1]+NODE_R, LAB_Y-NODE_R),(merge_x-NODE_R, MAIN_Y+NODE_R)],
              fill=color, width=2)

    # Merge commit node (on main, highlighted)
    circle(draw, merge_x, MAIN_Y, NODE_R+3, color, outline=GREEN2, width=2)

    # merge label above
    ctext(draw, merge_x, MAIN_Y-28, lab["merge_msg"], f_sha, color)
    ctext(draw, merge_x, MAIN_Y-44, "--no-ff", f_sha, DIM)

    # ── Lab branch label ──────────────────────────────────────────────────
    label_x = branch_x + 10
    rr(draw, [label_x-36, LAB_Y-48, label_x+36, LAB_Y-26], 5,
       (22,28,26), outline=color, width=1)
    ctext(draw, label_x, LAB_Y-37, lab["name"], f_label, color)
    ctext(draw, label_x, LAB_Y-18, lab["title"], f_tiny, MUTED)

    cur_x = merge_x

# ── "…" dots and Lab-22 hint ─────────────────────────────────────────────────
dots_x = cur_x + 40
for i in range(3):
    circle(draw, dots_x + i*18, MAIN_Y, 4, MUTED)

# Line continues after dots
draw.line([(dots_x+60, MAIN_Y),(dots_x+130, MAIN_Y)], fill=GREEN2, width=3)

# Final "Lab-22" note
fin_x = dots_x + 180
rr(draw, [fin_x-50, MAIN_Y-24, fin_x+50, MAIN_Y+24], 8,
   (24,38,28), outline=ACCENT, width=2)
ctext(draw, fin_x, MAIN_Y-8, "Lab-22", f_label, ACCENT)
ctext(draw, fin_x, MAIN_Y+10, "SOLID+DI", f_tiny, MUTED)
node(fin_x, MAIN_Y, ACCENT)

# main label at the start
rr(draw, [INIT_X-14, MAIN_Y-52, INIT_X+62, MAIN_Y-30], 5,
   (26,44,33), outline=GREEN2, width=2)
ctext(draw, INIT_X+24, MAIN_Y-41, "main", f_label, GREEN2)

# ── HEAD pointer ──────────────────────────────────────────────────────────────
head_x = fin_x
rr(draw, [head_x-26, MAIN_Y+30, head_x+26, MAIN_Y+54], 5,
   (38,32,18), outline=WARN, width=2)
ctext(draw, head_x, MAIN_Y+42, "HEAD", f_label, WARN)
draw.line([(head_x, MAIN_Y+30),(head_x, MAIN_Y+NODE_R+3)], fill=WARN, width=2)

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM: Two panels — workflow steps + --no-ff explanation
# ══════════════════════════════════════════════════════════════════════════════
SEP_Y = LAB_Y + 80
draw.line([(40, SEP_Y),(W-40, SEP_Y)], fill=LINE_C, width=1)

S2_Y = SEP_Y + 12
PAN_H = H - S2_Y - 16
HALF  = (W - 80) // 2

# ── LEFT: step-by-step workflow ───────────────────────────────────────────────
LX = 40
rr(draw, [LX, S2_Y, LX+HALF, S2_Y+PAN_H], 8, (20,26,24), outline=(45,65,54), width=1)
ctext(draw, LX+HALF//2, S2_Y+18, "Повний цикл однієї лаби", f_head, ACCENT)

steps = [
    ("git checkout main",                    "переконатись що ми на main"),
    ("git checkout -b Lab-01",               "створити гілку для лаби"),
    ("# ... виконувати завдання ...",        ""),
    ("git add src/",                         ""),
    ("git commit -m \"Lab01 Task01: ...\"",  "коміт після кожного завдання"),
    ("# ... Task02, Task03 ...",             ""),
    ("git checkout main",                    ""),
    ("git merge --no-ff Lab-01 -m \"...\"",  "злити в main, зберегти топологію"),
    ("git checkout -b Lab-02",               "відразу починаємо наступну"),
]
for i, (cmd, comment) in enumerate(steps):
    cy = S2_Y + 38 + i*28
    is_comment = cmd.startswith("#")
    col = DIM if is_comment else TEXT
    draw.text((LX+18, cy), cmd, font=f_cmd, fill=col)
    if comment:
        bb = draw.textbbox((0,0), cmd, font=f_cmd)
        cx2 = LX + 18 + bb[2]-bb[0] + 12
        draw.text((cx2, cy+1), f"  ← {comment}", font=f_tiny, fill=DIM)

# ── RIGHT: --no-ff vs fast-forward explanation ────────────────────────────────
RX = LX + HALF + 20
rr(draw, [RX, S2_Y, RX+HALF, S2_Y+PAN_H], 8, (20,26,24), outline=(45,65,54), width=1)
ctext(draw, RX+HALF//2, S2_Y+18, "Навіщо  --no-ff ?", f_head, WARN)

# Fast-forward (bad for us)
FF_Y = S2_Y + 44
ctext(draw, RX+HALF//4, FF_Y, "БЕЗ --no-ff  (fast-forward)", f_body, (200,100,100))

FF_nodes = [RX+40, RX+110, RX+180, RX+250]
for i,nx in enumerate(FF_nodes):
    circle(draw, nx, FF_Y+30, 8, TEXT if i<2 else BLUE)
    if i>0:
        draw.line([(FF_nodes[i-1]+8,FF_Y+30),(nx-8,FF_Y+30)], fill=MUTED, width=2)
# no merge commit visible
ctext(draw, RX+HALF//4, FF_Y+58, "Гілка не видна — лінійна історія", f_tiny, (200,100,100))

# With --no-ff (our approach)
NFF_Y = FF_Y + 80
ctext(draw, RX+HALF//4, NFF_Y, "З --no-ff  (наш підхід)", f_body, ACCENT)

# main nodes
M_NFF = [RX+40, RX+250]
draw.line([(M_NFF[0]+8,NFF_Y+28),(M_NFF[1]-8,NFF_Y+28)], fill=GREEN2, width=2)
for nx in M_NFF:
    circle(draw, nx, NFF_Y+28, 8, GREEN2)

# lab task nodes
T_NFF = [RX+110, RX+180]
draw.line([(T_NFF[0]+8,NFF_Y+60),(T_NFF[1]-8,NFF_Y+60)], fill=ACCENT, width=2)
for nx in T_NFF:
    circle(draw, nx, NFF_Y+60, 7, ACCENT)
# diagonals
draw.line([(M_NFF[0]+8,NFF_Y+34),(T_NFF[0]-4,NFF_Y+56)], fill=ACCENT, width=2)
draw.line([(T_NFF[1]+4,NFF_Y+56),(M_NFF[1]-8,NFF_Y+34)], fill=ACCENT, width=2)

# merge commit (diamond shape on main)
circle(draw, M_NFF[1], NFF_Y+28, 10, ACCENT, outline=GREEN2, width=2)

ctext(draw, RX+HALF//4, NFF_Y+84, "Гілка видна — можна простежити кожну лабу", f_tiny, ACCENT)

# git log --graph note
rr(draw, [RX+14, S2_Y+PAN_H-42, RX+HALF-14, S2_Y+PAN_H-12], 5,
   (18,24,22), outline=LINE_C, width=1)
ctext(draw, RX+HALF//2, S2_Y+PAN_H-27,
      "git log --oneline --graph --all  —  побачити весь граф", f_cmd, MUTED)

out = r"C:\Users\Yurii\source\repos\OOP-Tomka-CourseForHardCoders\git-workshop\_assets\branch-topology.png"
img.save(out, "PNG")
print(f"Saved {W}x{H}")
