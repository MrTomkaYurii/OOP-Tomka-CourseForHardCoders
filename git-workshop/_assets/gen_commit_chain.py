from PIL import Image, ImageDraw, ImageFont

BG     = (17, 20, 19)
PANEL  = (20, 26, 24)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
ACCENT = (118, 199, 173)
LINE_C = (44, 53, 49)
WARN   = (240, 160, 75)
BLUE   = (90, 150, 210)
DIM    = (95, 112, 106)
GREEN2 = (80, 170, 120)

W, H = 1400, 700
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def font(p, s):
    try:    return ImageFont.truetype(p, s)
    except: return ImageFont.load_default()

FB = r"C:\Windows\Fonts\arialbd.ttf"
FR = r"C:\Windows\Fonts\arial.ttf"
FM = r"C:\Windows\Fonts\cour.ttf"

f_title = font(FB, 24)
f_head  = font(FB, 16)
f_body  = font(FR, 13)
f_small = font(FR, 12)
f_sha   = font(FM, 13)
f_label = font(FB, 13)
f_cmd   = font(FM, 14)

def rr(xy, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def tsize(text, fnt):
    bb = draw.textbbox((0, 0), text, font=fnt)
    return bb[2] - bb[0], bb[3] - bb[1]

def ctext(cx, cy, text, fnt, fill):
    bb = draw.textbbox((0, 0), text, font=fnt)
    draw.text((cx - (bb[2] - bb[0]) // 2 - bb[0], cy - (bb[3] - bb[1]) // 2 - bb[1]), text, font=fnt, fill=fill)

def ltext(x, cy, text, fnt, fill):
    bb = draw.textbbox((0, 0), text, font=fnt)
    draw.text((x - bb[0], cy - (bb[3] - bb[1]) // 2 - bb[1]), text, font=fnt, fill=fill)

def arrow_left(x_from, x_to, y, col, label=None):
    draw.line([(x_from, y), (x_to + 8, y)], fill=col, width=2)
    draw.polygon([(x_to + 8, y - 5), (x_to, y), (x_to + 8, y + 5)], fill=col)
    if label:
        ctext((x_from + x_to) // 2, y - 11, label, f_small, col)

def arrow_up(x, y_from, y_to, col):
    draw.line([(x, y_from), (x, y_to + 7)], fill=col, width=2)
    draw.polygon([(x - 5, y_to + 7), (x, y_to), (x + 5, y_to + 7)], fill=col)

CW, CH = 150, 54

def commit(cx, cy, sha, msg, hi=False):
    col = ACCENT if hi else (70, 90, 82)
    rr([cx - CW // 2, cy - CH // 2, cx + CW // 2, cy + CH // 2], 6, (24, 32, 29), outline=col, width=2 if hi else 1)
    ctext(cx, cy - 11, sha, f_sha, ACCENT if hi else MUTED)
    ctext(cx, cy + 12, msg, f_small, TEXT)

def pointer(cx, top, text, col, w=None):
    tw, _ = tsize(text, f_label)
    w = w or tw + 22
    rr([cx - w // 2, top, cx + w // 2, top + 26], 5, (22, 30, 27), outline=col, width=2)
    ctext(cx, top + 13, text, f_label, col)
    return top + 26

# ── Title ─────────────────────────────────────────────────────────────────────
ctext(W // 2, 26, "Git: що таке коміт і гілка", f_title, ACCENT)

# ══════════════════════════════════════════════════════════════════════════════
# TOP-LEFT: commit object
# ══════════════════════════════════════════════════════════════════════════════
OX0, OY0, OX1, OY1 = 30, 56, 420, 330
rr([OX0, OY0, OX1, OY1], 10, PANEL, outline=(55, 85, 68), width=2)
ctext((OX0 + OX1) // 2, OY0 + 22, "Об'єкт коміту  3a4b5c6", f_head, ACCENT)
draw.line([(OX0 + 14, OY0 + 42), (OX1 - 14, OY0 + 42)], fill=LINE_C)

fields = [
    ("tree",    "знімок усіх файлів проєкту",  TEXT),
    ("parent",  "c7d8e9f  (попередній коміт)", BLUE),
    ("author",  "Іван Петренко",               TEXT),
    ("date",    "2026-09-14 10:23",            TEXT),
    ("message", "Lab01 Task02",                WARN),
]
for i, (k, v, col) in enumerate(fields):
    y = OY0 + 66 + i * 30
    ltext(OX0 + 20, y, k, f_sha, DIM)
    ltext(OX0 + 112, y, v, f_body, col)

draw.line([(OX0 + 14, OY0 + 212), (OX1 - 14, OY0 + 212)], fill=LINE_C)
ltext(OX0 + 20, OY0 + 232, "SHA = хеш від усього вмісту вище", f_body, ACCENT)
ltext(OX0 + 20, OY0 + 254, "змінив будь-що → новий коміт з новим SHA", f_small, MUTED)

# ══════════════════════════════════════════════════════════════════════════════
# TOP-RIGHT: chain of commits + branch pointers
# ══════════════════════════════════════════════════════════════════════════════
ltext(450, 66, "Ланцюжок комітів (кожен знає свого батька — parent):", f_body, MUTED)
CY = 118
xs = [530, 735, 940, 1145]
chain = [("a1b2c3d", "initial commit"), ("e4f5a6b", "Lab01: project"),
         ("c7d8e9f", "Lab01 Task01"), ("3a4b5c6", "Lab01 Task02")]
for i, (sha, msg) in enumerate(chain):
    commit(xs[i], CY, sha, msg, hi=(i == 3))
for i in range(1, 4):
    arrow_left(xs[i] - CW // 2, xs[i - 1] + CW // 2, CY, BLUE, "parent")

# main → a1b2c3d ; Lab-01 → 3a4b5c6 ; HEAD → Lab-01
arrow_up(xs[0], CY + 52, CY + CH // 2 + 2, GREEN2)
pointer(xs[0], CY + 52, "main", GREEN2)
arrow_up(xs[3], CY + 52, CY + CH // 2 + 2, ACCENT)
b = pointer(xs[3], CY + 52, "Lab-01", ACCENT)
arrow_up(xs[3], b + 18, b + 2, WARN)
pointer(xs[3], b + 18, "HEAD", WARN)

# note about branches
NX0, NY0, NX1, NY1 = 640, 182, 1040, 314
rr([NX0, NY0, NX1, NY1], 8, PANEL, outline=LINE_C)
ctext((NX0 + NX1) // 2, NY0 + 20, "Гілка = вказівник на коміт", f_head, ACCENT)
ctext((NX0 + NX1) // 2, NY0 + 48, "файл .git/refs/heads/Lab-01, у ньому — SHA", f_body, TEXT)
ctext((NX0 + NX1) // 2, NY0 + 70, "новий коміт → гілка сама пересувається на нього", f_body, TEXT)
ctext((NX0 + NX1) // 2, NY0 + 96, "HEAD = «ти тут»: на якій гілці ти зараз", f_body, WARN)

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM: before / after git checkout -b Lab-01 / after first commit
# ══════════════════════════════════════════════════════════════════════════════
SEP_Y = 350
draw.line([(30, SEP_Y), (W - 30, SEP_Y)], fill=LINE_C)

PY0, PY1 = 366, H - 20
PW = (W - 60 - 2 * 16) // 3
panels = []
for i in range(3):
    x0 = 30 + i * (PW + 16)
    panels.append((x0, x0 + PW))

titles = [("1. Ти на main", MUTED, None),
          ("2. Після  git checkout -b Lab-01", ACCENT, None),
          ('3. Після  git commit -m "Lab01: project"', ACCENT, None)]
notes = [
    ("HEAD → main → a1b2c3d", "одна гілка, один коміт"),
    ("обидві гілки на ОДНОМУ коміті", "файли не копіюються, HEAD → Lab-01"),
    ("Lab-01 пересунулась на новий коміт", "main лишився на місці"),
]

for i, (x0, x1) in enumerate(panels):
    rr([x0, PY0, x1, PY1], 10, (19, 24, 22), outline=(50, 72, 60), width=1)
    t, col, _ = titles[i]
    ctext((x0 + x1) // 2, PY0 + 24, t, f_cmd if i else f_head, col)
    rr([x0 + 14, PY1 - 62, x1 - 14, PY1 - 12], 6, PANEL, outline=LINE_C)
    ctext((x0 + x1) // 2, PY1 - 46, notes[i][0], f_body, ACCENT if i else TEXT)
    ctext((x0 + x1) // 2, PY1 - 26, notes[i][1], f_small, MUTED)

ROW = PY0 + 98
# panel 1
x0, x1 = panels[0]
c = (x0 + x1) // 2
commit(c, ROW, "a1b2c3d", "initial commit")
arrow_up(c, ROW + 48, ROW + CH // 2 + 2, GREEN2)
b = pointer(c, ROW + 48, "main", GREEN2, 80)
arrow_up(c, b + 16, b + 2, WARN)
pointer(c, b + 16, "HEAD", WARN, 80)

# panel 2
x0, x1 = panels[1]
c = (x0 + x1) // 2
commit(c, ROW, "a1b2c3d", "initial commit")
for dx, name, col in [(-50, "main", GREEN2), (50, "Lab-01", ACCENT)]:
    draw.line([(c + dx, ROW + 48), (c + dx // 3, ROW + CH // 2 + 4)], fill=col, width=2)
    pointer(c + dx, ROW + 48, name, col, 80)
arrow_up(c + 50, ROW + 90, ROW + 76, WARN)
pointer(c + 50, ROW + 90, "HEAD", WARN, 80)

# panel 3
x0, x1 = panels[2]
ca, cb = x0 + 100, x1 - 100
commit(ca, ROW, "a1b2c3d", "initial commit")
commit(cb, ROW, "e4f5a6b", "Lab01: project", hi=True)
arrow_left(cb - CW // 2, ca + CW // 2, ROW, BLUE)
arrow_up(ca, ROW + 48, ROW + CH // 2 + 2, GREEN2)
pointer(ca, ROW + 48, "main", GREEN2, 80)
arrow_up(cb, ROW + 48, ROW + CH // 2 + 2, ACCENT)
b = pointer(cb, ROW + 48, "Lab-01", ACCENT, 80)
arrow_up(cb, b + 16, b + 2, WARN)
pointer(cb, b + 16, "HEAD", WARN, 80)

out = r"C:\Users\Yurii\source\repos\OOP-Tomka-CourseForHardCoders\git-workshop\_assets\commit-chain.png"
img.save(out, "PNG")
print(f"Saved {W}x{H}")
