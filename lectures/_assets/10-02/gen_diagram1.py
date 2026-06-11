# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

BG     = "#111413"
ACCENT = "#76c7ad"
TEXT   = "#e5e9e7"
MUTED  = "#a1aaa6"
LINE   = "#2c3531"
PANEL  = "#191e1c"
ORANGE = "#c7a276"
DARK   = "#161c1a"

W, H = 900, 440
img = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(img)

def load(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

fb  = load("C:/Windows/Fonts/arialbd.ttf", 15)
fr  = load("C:/Windows/Fonts/arial.ttf",   13)
fs  = load("C:/Windows/Fonts/arial.ttf",   11)
ft  = load("C:/Windows/Fonts/arialbd.ttf", 17)

# Title
d.text((W//2, 24), "LinkedList<T> — структура двозв'язного списку", font=ft, fill=ACCENT, anchor="mm")

# Node dimensions
nw, nh = 155, 90
gap = 32
n = 4
total_w = n * nw + (n-1) * gap
x0 = (W - total_w) // 2
y0 = 110

names = ["Петренко І.", "Коваль М.", "Сидоренко О.", "Мельник Г."]
centers = []

for i, name in enumerate(names):
    nx = x0 + i * (nw + gap)
    ny = y0
    cx = nx + nw // 2
    centers.append(cx)

    # node background
    d.rounded_rectangle([nx, ny, nx+nw, ny+nh], radius=8, fill=PANEL, outline=LINE, width=1)

    rh = nh // 3

    # top stripe: Previous
    d.rounded_rectangle([nx+2, ny+2, nx+nw-2, ny+rh], radius=4, fill=DARK)
    d.text((cx, ny + rh//2), "← Previous", font=fs, fill=MUTED, anchor="mm")

    # middle: Value
    d.text((cx, ny + rh + rh//2), name, font=fb, fill=TEXT, anchor="mm")

    # bottom stripe: Next
    d.rounded_rectangle([nx+2, ny+2*rh, nx+nw-2, ny+nh-2], radius=4, fill=DARK)
    d.text((cx, ny + 2*rh + rh//2), "Next →", font=fs, fill=MUTED, anchor="mm")

    # "Value" label above node
    d.text((cx, ny - 13), "Value", font=fs, fill=MUTED, anchor="mm")

# Head / Tail labels
d.text((centers[0], y0 - 34), "Head  (First)", font=fb, fill=ACCENT, anchor="mm")
d.line([(centers[0], y0-22), (centers[0], y0+2)], fill=ACCENT, width=2)
d.polygon([(centers[0], y0+2), (centers[0]-5, y0-7), (centers[0]+5, y0-7)], fill=ACCENT)

d.text((centers[-1], y0 - 34), "Tail  (Last)", font=fb, fill=ORANGE, anchor="mm")
d.line([(centers[-1], y0-22), (centers[-1], y0+2)], fill=ORANGE, width=2)
d.polygon([(centers[-1], y0+2), (centers[-1]-5, y0-7), (centers[-1]+5, y0-7)], fill=ORANGE)

# Arrows between nodes — two separate rows
ay_fwd  = y0 + nh + 22   # forward (Next →)
ay_back = y0 + nh + 46   # backward (← Previous)

for i in range(n - 1):
    xl = x0 + i * (nw + gap) + nw + 4
    xr = x0 + (i+1) * (nw + gap) - 4

    # forward →
    d.line([(xl, ay_fwd), (xr, ay_fwd)], fill=ACCENT, width=2)
    d.polygon([(xr, ay_fwd), (xr-8, ay_fwd-5), (xr-8, ay_fwd+5)], fill=ACCENT)

    # backward ←
    d.line([(xl, ay_back), (xr, ay_back)], fill=ORANGE, width=2)
    d.polygon([(xl, ay_back), (xl+8, ay_back-5), (xl+8, ay_back+5)], fill=ORANGE)

# Arrow direction labels — placed to the right of the last arrow row
label_x = x0 + n * (nw + gap) - gap + 8
d.text((label_x, ay_fwd), "Next →", font=fs, fill=ACCENT, anchor="lm")
d.text((label_x, ay_back), "← Previous", font=fs, fill=ORANGE, anchor="lm")

# null terminators
null_xl = x0 - 52
null_xr = x0 + n * (nw + gap) - gap + 52
null_y  = y0 + nh // 2

d.text((null_xl, null_y), "null", font=fb, fill=MUTED, anchor="mm")
d.line([(null_xl + 16, null_y + 2), (x0 - 4, null_y + 2)], fill=MUTED, width=1)

d.text((null_xr, null_y), "null", font=fb, fill=MUTED, anchor="mm")
d.line([(x0 + n*(nw+gap)-gap+4, null_y + 2), (null_xr - 16, null_y + 2)], fill=MUTED, width=1)

# Count badge
bx, by = W - 160, H - 62
d.rounded_rectangle([bx, by, bx+135, by+36], radius=6, fill=PANEL, outline=LINE)
d.text((bx + 67, by + 18), "Count = 4", font=fb, fill=ACCENT, anchor="mm")

# Legend
lx, ly = 28, H - 78
d.text((lx, ly),     "Кожен вузол — LinkedListNode<T>:", font=fs, fill=MUTED)
d.text((lx, ly+16),  "  Value        — значення елементу", font=fs, fill=TEXT)
d.text((lx, ly+30),  "  Next         — посилання на наступний вузол", font=fs, fill=ACCENT)
d.text((lx, ly+44),  "  Previous  — посилання на попередній вузол", font=fs, fill=ORANGE)

out = "C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/10-02/linkedlist-structure.png"
img.save(out)
print("OK:", out)
