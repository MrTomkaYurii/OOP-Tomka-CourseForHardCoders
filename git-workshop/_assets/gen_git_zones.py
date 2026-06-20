from PIL import Image, ImageDraw, ImageFont

BG      = (17, 20, 19)
PANEL   = (25, 30, 28)
TEXT    = (229, 233, 231)
MUTED   = (161, 170, 166)
ACCENT  = (118, 199, 173)
LINE_C  = (44, 53, 49)
WARN    = (240, 160, 75)
BLUE    = (90, 150, 210)
DIM     = (80, 100, 95)

W, H = 1400, 580
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

f_title = font(r"C:\Windows\Fonts\arialbd.ttf", 24)
f_head  = font(r"C:\Windows\Fonts\arialbd.ttf", 18)
f_sub   = font(r"C:\Windows\Fonts\arial.ttf", 13)
f_body  = font(r"C:\Windows\Fonts\arial.ttf", 15)
f_cmd   = font(r"C:\Windows\Fonts\cour.ttf", 14)
f_note  = font(r"C:\Windows\Fonts\arial.ttf", 13)
f_badge = font(r"C:\Windows\Fonts\arialbd.ttf", 13)

def rr(d, xy, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def ctext(d, cx, cy, text, fnt, fill):
    bb = d.textbbox((0,0), text, font=fnt)
    d.text((cx-(bb[2]-bb[0])//2, cy-(bb[3]-bb[1])//2), text, font=fnt, fill=fill)

def ltext(d, x, cy, text, fnt, fill):
    bb = d.textbbox((0,0), text, font=fnt)
    d.text((x, cy-(bb[3]-bb[1])//2), text, font=fnt, fill=fill)

# ── Layout ────────────────────────────────────────────────────────────────────
TITLE_Y = 18
BOX_Y0  = 60
BOX_H   = 360
GAP     = 72          # gap between boxes — enough room for arrows
MARGIN  = 28
ZONE_W  = (W - MARGIN*2 - GAP*3) // 4

xs = [MARGIN + i*(ZONE_W + GAP) for i in range(4)]

zones = [
    {
        "title": "Working Directory",
        "sub":   "Робоча директорія",
        "items": [("Untracked  (нові файли)", WARN),
                  ("Modified  (змінені)", (220,120,120)),
                  ("Deleted  (видалені)", DIM)],
        "note1": "git status",
        "note2": "показує стан цієї зони",
        "bg": (22, 32, 27), "border": (55, 85, 68),
    },
    {
        "title": "Staging Area",
        "sub":   "Індекс (Index)",
        "items": [("Staged changes", ACCENT),
                  ("Готові до коміту", MUTED),
                  ("", (0,0,0))],
        "note1": "git diff --cached",
        "note2": "показує що тут",
        "bg": (22, 32, 27), "border": (60, 95, 75),
    },
    {
        "title": "Local Repository",
        "sub":   ".git — локальний репо",
        "items": [("Commit objects (SHA)", ACCENT),
                  ("Branches / Tags", (150,200,180)),
                  ("Stash", MUTED)],
        "note1": "git log --oneline",
        "note2": "показує історію",
        "bg": (20, 28, 34), "border": (50, 90, 140),
    },
    {
        "title": "Remote (GitHub)",
        "sub":   "Віддалений репозиторій",
        "items": [("origin/main", BLUE),
                  ("origin/Lab-01", (130,180,220)),
                  ("origin/Lab-02 …", (110,155,195))],
        "note1": "github.com / your-repo",
        "note2": "git remote -v",
        "bg": (18, 22, 34), "border": (50, 80, 160),
    },
]

# ── Title ─────────────────────────────────────────────────────────────────────
ctext(draw, W//2, TITLE_Y+10, "Git: Чотири зони роботи", f_title, ACCENT)

# ── Boxes ─────────────────────────────────────────────────────────────────────
for i, z in enumerate(zones):
    x0, x1 = xs[i], xs[i]+ZONE_W
    rr(draw, [x0, BOX_Y0, x1, BOX_Y0+BOX_H], 10, z["bg"], outline=z["border"], width=2)

    # Badge
    bx, by = x0+16, BOX_Y0+16
    draw.ellipse([bx-12,by-12,bx+12,by+12], fill=z["border"])
    ctext(draw, bx, by, str(i+1), f_badge, TEXT)

    # Title + sub
    ctext(draw, (x0+x1)//2, BOX_Y0+30, z["title"], f_head, TEXT)
    ctext(draw, (x0+x1)//2, BOX_Y0+52, z["sub"],   f_sub,  MUTED)
    draw.line([(x0+14, BOX_Y0+67),(x1-14, BOX_Y0+67)], fill=LINE_C, width=1)

    # Items
    for j,(txt,col) in enumerate(z["items"]):
        if not txt: continue
        ty = BOX_Y0 + 88 + j*40
        draw.ellipse([x0+22,ty+6,x0+30,ty+14], fill=col)
        ltext(draw, x0+40, ty+10, txt, f_body, col)

    # Note box
    ny = BOX_Y0 + BOX_H - 82
    rr(draw, [x0+12, ny, x1-12, ny+68], 6, (0,0,0), outline=LINE_C, width=1)
    ctext(draw, (x0+x1)//2, ny+22, z["note1"], f_cmd,  ACCENT if i<3 else BLUE)
    ctext(draw, (x0+x1)//2, ny+46, z["note2"], f_note, MUTED)

# ── Arrows between boxes ───────────────────────────────────────────────────────
FWD_Y  = BOX_Y0 + BOX_H//2 - 22   # forward  (green, going right)
BACK_Y = BOX_Y0 + BOX_H//2 + 22   # backward (orange, going left)

fwd_labels  = ["git add", "git commit", "git push"]
back_labels = ["git restore\n--staged", "git restore", "git pull /\ngit fetch"]

for i in range(3):
    gx0 = xs[i]   + ZONE_W + 4   # left  edge of gap
    gx1 = xs[i+1] - 4            # right edge of gap
    mid = (gx0 + gx1) // 2

    # Forward arrow
    col_fwd = ACCENT
    draw.line([(gx0, FWD_Y),(gx1-8, FWD_Y)], fill=col_fwd, width=2)
    draw.polygon([(gx1-8,FWD_Y-5),(gx1,FWD_Y),(gx1-8,FWD_Y+5)], fill=col_fwd)
    lbl = fwd_labels[i]
    bb  = draw.textbbox((0,0), lbl, font=f_cmd)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    rr(draw, [mid-tw//2-3, FWD_Y-th-10, mid+tw//2+3, FWD_Y-4], 3, (28,40,34))
    draw.text((mid-tw//2, FWD_Y-th-8), lbl, font=f_cmd, fill=col_fwd)

    # Back arrow
    col_back = WARN
    draw.line([(gx1, BACK_Y),(gx0+8, BACK_Y)], fill=col_back, width=2)
    draw.polygon([(gx0+8,BACK_Y-5),(gx0,BACK_Y),(gx0+8,BACK_Y+5)], fill=col_back)
    for li, line in enumerate(back_labels[i].split("\n")):
        bb2 = draw.textbbox((0,0), line, font=f_cmd)
        tw2 = bb2[2]-bb2[0]
        draw.text((mid-tw2//2, BACK_Y+6+li*17), line, font=f_cmd, fill=col_back)

# ── Bottom bar: git status + git clone ────────────────────────────────────────
BAR_Y = BOX_Y0 + BOX_H + 22

# git status bar spans zones 0-1
bar_x0 = xs[0]
bar_x1 = xs[1] + ZONE_W
rr(draw, [bar_x0, BAR_Y, bar_x1, BAR_Y+34], 6, (25,42,34), outline=(50,85,65), width=1)
ctext(draw, (bar_x0+bar_x1)//2, BAR_Y+17, "git status  —  стан зон 1 i 2", f_cmd, ACCENT)

# git log bar — zone 2 only
rr(draw, [xs[2], BAR_Y, xs[2]+ZONE_W, BAR_Y+34], 6, (20,28,42), outline=(40,70,130), width=1)
ctext(draw, xs[2]+ZONE_W//2, BAR_Y+17, "git log  —  зона 3", f_cmd, BLUE)

# git clone arrow — below zone 3→4, pointing LEFT (Remote → Local)
CL_Y   = BAR_Y + 58
cl_xR  = xs[3]              # left edge of Remote box
cl_xL  = xs[2] + ZONE_W    # right edge of Local Repo box
mid_cl = (cl_xL + cl_xR) // 2

# line goes from Remote left edge → Local right edge
draw.line([(cl_xR, CL_Y),(cl_xL+8, CL_Y)], fill=(130,180,220), width=2)
# arrowhead points LEFT (into Local Repo)
draw.polygon([(cl_xL+8,CL_Y-5),(cl_xL,CL_Y),(cl_xL+8,CL_Y+5)], fill=(130,180,220))

lbl_cl = "git clone  (Remote -> Local, одноразово)"
bb_cl  = draw.textbbox((0,0), lbl_cl, font=f_cmd)
tw_cl  = bb_cl[2]-bb_cl[0]
rr(draw, [mid_cl-tw_cl//2-4, CL_Y-22, mid_cl+tw_cl//2+4, CL_Y-4], 3, (20,26,38))
draw.text((mid_cl-tw_cl//2, CL_Y-20), lbl_cl, font=f_cmd, fill=(130,180,220))

out = r"C:\Users\Yurii\source\repos\OOP-Tomka-CourseForHardCoders\git-workshop\_assets\git-zones.png"
img.save(out, "PNG")
print(f"Saved {W}x{H}")
