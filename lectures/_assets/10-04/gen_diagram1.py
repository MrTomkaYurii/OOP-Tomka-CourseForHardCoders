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
fh  = load("C:/Windows/Fonts/arialbd.ttf", 13)

# Title
d.text((W//2, 24), "Stack<T> — принцип LIFO (останній прийшов — перший вийшов)", font=ft, fill=ACCENT, anchor="mm")

# Stack items (vertical, drawn from bottom to top)
items = [
    ("Аспірин 500мг",     "1"),
    ("Ібупрофен 400мг",   "2"),
    ("Метформін 850мг",   "3"),
    ("Лізиноприл 10мг",   "4 ← Top"),
]

nw, nh = 240, 48
gap = 3
stack_x = W // 2 - nw // 2
bottom_y = H - 80

# Bottom plate of stack
plate_y = bottom_y + nh + 6
d.rectangle([stack_x - 10, plate_y, stack_x + nw + 10, plate_y + 8], fill=LINE)

for i, (name, label) in enumerate(items):
    ny = bottom_y - i * (nh + gap)
    shade = PANEL if i % 2 == 0 else DARK
    is_top = (i == len(items) - 1)
    outline_color = ACCENT if is_top else LINE
    d.rounded_rectangle([stack_x, ny, stack_x + nw, ny + nh], radius=5,
                         fill=shade, outline=outline_color, width=2 if is_top else 1)
    d.text((stack_x + nw // 2, ny + nh // 2), name, font=fb, fill=TEXT if not is_top else ACCENT, anchor="mm")
    d.text((stack_x + nw - 10, ny + 8), label, font=fs, fill=MUTED, anchor="rm")

# Top marker
top_ny = bottom_y - (len(items) - 1) * (nh + gap)
top_label_y = top_ny - 20
d.text((stack_x + nw + 16, top_ny + nh // 2), "← Top (верхівка)", font=fh, fill=ACCENT, anchor="lm")

# Push arrow (coming FROM above going DOWN into stack)
push_x = stack_x - 100
push_arrow_bottom = top_ny - 4
push_arrow_top    = top_ny - 60
d.line([(push_x + 30, push_arrow_top), (push_x + 30, push_arrow_bottom)], fill=ORANGE, width=2)
d.polygon([(push_x + 30, push_arrow_bottom),
           (push_x + 25, push_arrow_bottom - 10),
           (push_x + 35, push_arrow_bottom - 10)], fill=ORANGE)
d.text((push_x + 30, push_arrow_top - 12), "Push(item)", font=fh, fill=ORANGE, anchor="mm")
d.text((push_x + 30, push_arrow_top + 4), "додати", font=fs, fill=MUTED, anchor="mm")

# Pop arrow (going FROM top UP and out)
pop_x = stack_x + nw + 80
pop_arrow_bottom = top_ny + 8
pop_arrow_top    = top_ny - 52
d.line([(pop_x, pop_arrow_bottom), (pop_x, pop_arrow_top)], fill=ACCENT, width=2)
d.polygon([(pop_x, pop_arrow_top),
           (pop_x - 5, pop_arrow_top + 10),
           (pop_x + 5, pop_arrow_top + 10)], fill=ACCENT)
d.text((pop_x, pop_arrow_top - 12), "Pop()", font=fh, fill=ACCENT, anchor="mm")
d.text((pop_x, pop_arrow_top + 4),  "зняти", font=fs, fill=MUTED, anchor="mm")

# Peek annotation
peek_x = stack_x + nw + 80
peek_y = top_ny + nh // 2
d.line([(stack_x + nw + 4, peek_y), (peek_x - 10, peek_y)], fill=MUTED, width=1)
d.text((peek_x, peek_y + 18), "Peek() — підглянути", font=fs, fill=MUTED, anchor="lm")
d.text((peek_x, peek_y + 32), "без видалення", font=fs, fill=MUTED, anchor="lm")

# Count badge
bx = W - 180
by = H - 60
d.rounded_rectangle([bx, by, bx+150, by+34], radius=6, fill=PANEL, outline=LINE)
d.text((bx + 75, by + 17), f"Count = {len(items)}", font=fb, fill=ACCENT, anchor="mm")

# LIFO rule at bottom left
lx, ly = 28, H - 70
d.text((lx, ly),     "Правило LIFO:", font=fh, fill=ACCENT)
d.text((lx, ly+20),  "  Push(item)  — кладе елемент НА ВЕРХІВКУ стека.  O(1).", font=fs, fill=TEXT)
d.text((lx, ly+36),  "  Pop()       — знімає елемент З ВЕРХІВКИ стека.  O(1).", font=fs, fill=TEXT)
d.text((lx, ly+52),  "  Peek()      — читає верхівку БЕЗ видалення.     O(1).", font=fs, fill=TEXT)

out = "C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/10-04/stack-lifo-structure.png"
img.save(out)
print("OK:", out)
