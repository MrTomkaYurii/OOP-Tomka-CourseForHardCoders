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

W, H = 920, 360
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
fh  = load("C:/Windows/Fonts/arialbd.ttf", 13)

# Title
d.text((W//2, 24), "Queue<T> — принцип FIFO (перший прийшов — перший вийшов)", font=ft, fill=ACCENT, anchor="mm")

# Layout: 140px left zone | nodes | 140px right zone
side = 140
nodes_area = W - 2 * side   # 640px for nodes

nw, nh = 140, 56
gap = 10
n = 4
total_w = n * nw + (n-1) * gap   # 590
x0 = side + (nodes_area - total_w) // 2   # center within middle zone
y0 = 90

names = ["Петренко І.", "Коваль М.", "Сидоренко О.", "Мельник Г."]

for i, name in enumerate(names):
    nx = x0 + i * (nw + gap)
    ny = y0
    cx = nx + nw // 2
    shade = PANEL if i % 2 == 0 else DARK
    d.rounded_rectangle([nx, ny, nx+nw, ny+nh], radius=6, fill=shade, outline=LINE, width=1)
    d.text((cx, ny + nh//2), name, font=fb, fill=TEXT, anchor="mm")
    d.text((nx + 8, ny + 6), f"{i+1}", font=fs, fill=MUTED)

node_left  = x0
node_right = x0 + total_w
mid_y = y0 + nh // 2

# ---- LEFT ZONE: Head + Dequeue ----
head_cx = side // 2   # 70

# Head label
d.text((head_cx, y0 - 14), "Head / Front", font=fh, fill=ACCENT, anchor="mm")

# Arrow: from head_cx+30 → node_left, pointing right INTO node  (element exits left so arrow points LEFT)
arrow_end   = node_left - 6
arrow_start = head_cx + 30
d.line([(arrow_start, mid_y), (arrow_end, mid_y)], fill=ACCENT, width=2)
# arrowhead pointing LEFT (dequeue exits the queue to the left)
d.polygon([(arrow_start, mid_y),
           (arrow_start + 10, mid_y - 5),
           (arrow_start + 10, mid_y + 5)], fill=ACCENT)

d.text((head_cx, mid_y - 14), "Dequeue()", font=fh, fill=ACCENT, anchor="mm")
d.text((head_cx, mid_y + 8),  "← виходить", font=fs, fill=MUTED, anchor="mm")

# ---- RIGHT ZONE: Tail + Enqueue ----
tail_cx = W - side // 2   # 850

d.text((tail_cx, y0 - 14), "Tail / Rear", font=fh, fill=ORANGE, anchor="mm")

arrow_start2 = node_right + 6
arrow_end2   = tail_cx - 30
d.line([(arrow_start2, mid_y), (arrow_end2, mid_y)], fill=ORANGE, width=2)
# arrowhead pointing RIGHT INTO queue
d.polygon([(arrow_start2, mid_y),
           (arrow_start2 + 10, mid_y - 5),
           (arrow_start2 + 10, mid_y + 5)], fill=ORANGE)

d.text((tail_cx, mid_y - 14), "Enqueue()", font=fh, fill=ORANGE, anchor="mm")
d.text((tail_cx, mid_y + 8),  "входить →", font=fs, fill=MUTED, anchor="mm")

# Count badge
bx = W//2 - 65
by = y0 + nh + 22
d.rounded_rectangle([bx, by, bx+130, by+32], radius=6, fill=PANEL, outline=LINE)
d.text((bx + 65, by + 16), "Count = 4", font=fb, fill=ACCENT, anchor="mm")

# Separator
sep_y = by + 52
d.line([(40, sep_y), (W-40, sep_y)], fill=LINE, width=1)

# FIFO rules block
rule_y = sep_y + 18
d.text((W//2, rule_y), "Ключові методи:", font=fh, fill=ACCENT, anchor="mm")
rules = [
    ("Enqueue(item)", "— додає елемент до КІНЦЯ черги (Tail).  Завжди O(1)."),
    ("Dequeue()",     "— видаляє і повертає перший елемент з ПОЧАТКУ (Head).  Завжди O(1)."),
    ("Peek()",        "— повертає перший елемент БЕЗ видалення.  O(1)."),
]
for ri, (meth, desc) in enumerate(rules):
    ry = rule_y + 24 + ri * 24
    d.text((90, ry), meth, font=fb, fill=ORANGE, anchor="lm")
    d.text((270, ry), desc, font=fr, fill=TEXT, anchor="lm")

out = "C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/10-03/queue-fifo-structure.png"
img.save(out)
print("OK:", out)
