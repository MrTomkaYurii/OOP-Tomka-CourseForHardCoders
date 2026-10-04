from PIL import Image, ImageDraw, ImageFont

BG     = (17, 20, 19)
PANEL  = (20, 26, 24)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
ACCENT = (118, 199, 173)
LINE_C = (44, 53, 49)
WARN   = (240, 160, 75)
RED    = (215, 110, 110)
BLUE   = (90, 150, 210)
DIM    = (85, 100, 95)
GREEN2 = (80, 170, 120)
PURPLE = (160, 120, 210)

W, H = 1400, 660
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
f_node  = font(FB, 13)
f_label = font(FB, 12)
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

def node(x, y, col, name, r=13, txt=BG):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=BG, width=2)
    ctext(x, y, name, f_node, txt)

def ghost(x, y, name, r=13):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=BG, outline=DIM, width=2)
    ctext(x, y, name, f_node, DIM)

def edge(a, b, col, w=3, dashed=False):
    if not dashed:
        draw.line([a, b], fill=col, width=w)
        return
    (x0, y0), (x1, y1) = a, b
    n = 14
    for i in range(0, n, 2):
        t0, t1 = i / n, (i + 1) / n
        draw.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0), (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)], fill=col, width=2)

def badge(cx, cy, text, col):
    tw, _ = tsize(text, f_label)
    rr([cx - tw // 2 - 9, cy - 11, cx + tw // 2 + 9, cy + 11], 5, (22, 28, 26), outline=col, width=1)
    ctext(cx, cy, text, f_label, col)

def bullets(x, y, items):
    for i, (txt, col) in enumerate(items):
        ltext(x, y + i * 22, txt, f_body, col)

# ── Title ─────────────────────────────────────────────────────────────────────
ctext(W // 2, 26, "Git: Merge vs Rebase", f_title, ACCENT)

# ══════════════════════════════════════════════════════════════════════════════
# TOP-LEFT: starting situation
# ══════════════════════════════════════════════════════════════════════════════
TX0, TY0, TX1, TY1 = 30, 56, 690, 236
rr([TX0, TY0, TX1, TY1], 10, PANEL, outline=(55, 85, 68), width=1)
ltext(TX0 + 20, TY0 + 22, "Вихідна ситуація", f_head, TEXT)

MY, FY = TY0 + 80, TY0 + 140
xa, xb, xc, xd = 110, 220, 330, 440
edge((xa, MY), (xd, MY), GREEN2)
edge((xb, MY), (xb + 60, FY), PURPLE)
edge((xb + 60, FY), (xc + 60, FY), PURPLE)
for x, n in [(xa, "A"), (xb, "B"), (xc, "C"), (xd, "D")]:
    node(x, MY, GREEN2, n)
node(xb + 60, FY, PURPLE, "E")
node(xc + 60, FY, PURPLE, "F")
badge(xd + 60, MY, "main", GREEN2)
badge(xc + 130, FY, "feature", PURPLE)
ltext(520, FY - 9, "C, D — нові коміти в main,", f_small, MUTED)
ltext(520, FY + 7, "поки йшла робота над E, F", f_small, MUTED)

# ══════════════════════════════════════════════════════════════════════════════
# TOP-RIGHT: summary
# ══════════════════════════════════════════════════════════════════════════════
SX0, SX1 = 710, W - 30
rr([SX0, TY0, SX1, TY1], 10, PANEL, outline=(55, 85, 68), width=1)
ltext(SX0 + 20, TY0 + 22, "Як об'єднати гілки?", f_head, TEXT)
bullets(SX0 + 20, TY0 + 58, [
    ("●  Merge — додає merge-коміт, історія лишається як була", GREEN2),
    ("●  Rebase — переписує E, F поверх D як нові коміти E', F'", BLUE),
    ("●  Код у результаті однаковий, різниться лише історія", MUTED),
    ("●  У курсі — тільки  git merge --no-ff", WARN),
])

# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM: merge | rebase
# ══════════════════════════════════════════════════════════════════════════════
BY0, BY1 = 256, H - 20
LX0, LX1 = 30, 690
RX0, RX1 = 710, W - 30

# ── MERGE ─────────────────────────────────────────────────────────────────────
rr([LX0, BY0, LX1, BY1], 10, (19, 26, 22), outline=(60, 100, 75), width=2)
ctext((LX0 + LX1) // 2, BY0 + 24, "git merge", f_head, GREEN2)
ctext((LX0 + LX1) // 2, BY0 + 46, "git checkout main  →  git merge --no-ff feature", f_cmd, MUTED)

MY2, FY2 = BY0 + 110, BY0 + 170
xa, xb, xc, xd, xm = 90, 190, 290, 390, 510
edge((xa, MY2), (xm, MY2), GREEN2)
edge((xb, MY2), (xb + 60, FY2), PURPLE)
edge((xb + 60, FY2), (xc + 60, FY2), PURPLE)
edge((xc + 60, FY2), (xm, MY2), PURPLE)
for x, n in [(xa, "A"), (xb, "B"), (xc, "C"), (xd, "D")]:
    node(x, MY2, GREEN2, n)
node(xb + 60, FY2, PURPLE, "E")
node(xc + 60, FY2, PURPLE, "F")
node(xm, MY2, ACCENT, "M", r=17)
badge(xm + 70, MY2, "main", GREEN2)
ltext(xm + 30, MY2 - 34, "merge-коміт", f_small, ACCENT)
ltext(xm + 30, MY2 - 20, "(2 батьки: D і F)", f_small, MUTED)

bullets(LX0 + 30, BY0 + 230, [
    ("+  Жоден існуючий коміт не змінюється", GREEN2),
    ("+  Видно, де гілка відійшла і де повернулась", GREEN2),
    ("+  Безпечно для гілок, які вже на GitHub", GREEN2),
    ("−  Граф з «ромбами» складніший", RED),
])
rr([LX0 + 16, BY1 - 54, LX1 - 16, BY1 - 14], 6, (24, 40, 30), outline=(60, 100, 75))
ctext((LX0 + LX1) // 2, BY1 - 34, "Так курс зливає кожну лабу в main", f_body, ACCENT)

# ── REBASE ────────────────────────────────────────────────────────────────────
rr([RX0, BY0, RX1, BY1], 10, (18, 22, 30), outline=(55, 85, 150), width=2)
ctext((RX0 + RX1) // 2, BY0 + 24, "git rebase", f_head, BLUE)
ctext((RX0 + RX1) // 2, BY0 + 46, "git checkout feature  →  git rebase main", f_cmd, MUTED)

ox = RX0 - 30 + 50
xa, xb, xc, xd, xe, xf = ox + 30, ox + 120, ox + 210, ox + 300, ox + 390, ox + 480
edge((xa, MY2), (xd, MY2), GREEN2)
edge((xd, MY2), (xf, MY2), BLUE)
edge((xb, MY2), (xb + 60, FY2), DIM, dashed=True)
edge((xb + 60, FY2), (xc + 60, FY2), DIM, dashed=True)
for x, n in [(xa, "A"), (xb, "B"), (xc, "C"), (xd, "D")]:
    node(x, MY2, GREEN2, n)
node(xe, MY2, BLUE, "E'")
node(xf, MY2, BLUE, "F'")
ghost(xb + 60, FY2, "E")
ghost(xc + 60, FY2, "F")
badge(xd, MY2 - 34, "main", GREEN2)
badge(xf + 70, MY2, "feature", BLUE)
ltext(xc + 90, FY2, "старі E, F — більше не в жодній гілці", f_small, DIM)
ctext((xe + xf) // 2, MY2 + 30, "нові SHA", f_small, BLUE)

bullets(RX0 + 30, BY0 + 230, [
    ("+  Лінійна історія без «ромбів»", BLUE),
    ("−  E', F' — нові коміти з новими SHA", RED),
    ("−  Запушену гілку після rebase треба force-push", RED),
    ("−  У інших копіях репозиторію історія «ламається»", RED),
])
rr([RX0 + 16, BY1 - 54, RX1 - 16, BY1 - 14], 6, (22, 28, 44), outline=(55, 85, 150))
ctext((RX0 + RX1) // 2, BY1 - 34, "Ніколи не роби rebase гілки, яку вже запушив", f_body, WARN)

out = r"C:\Users\Yurii\source\repos\OOP-Tomka-CourseForHardCoders\git-workshop\_assets\merge-vs-rebase.png"
img.save(out, "PNG")
print(f"Saved {W}x{H}")
