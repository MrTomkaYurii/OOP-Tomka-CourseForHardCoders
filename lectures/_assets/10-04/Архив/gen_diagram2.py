# -*- coding: utf-8 -*-
# Diagram 2: step-by-step state of stack (Push/Pop sequence)
from PIL import Image, ImageDraw, ImageFont

BG     = "#111413"
ACCENT = "#76c7ad"
TEXT   = "#e5e9e7"
MUTED  = "#a1aaa6"
LINE   = "#2c3531"
PANEL  = "#191e1c"
ORANGE = "#c7a276"
DARK   = "#161c1a"
RED    = "#c77676"

W, H = 920, 380
img = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(img)

def load(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

fb  = load("C:/Windows/Fonts/arialbd.ttf", 13)
fr  = load("C:/Windows/Fonts/arial.ttf",   12)
fs  = load("C:/Windows/Fonts/arial.ttf",   11)
ft  = load("C:/Windows/Fonts/arialbd.ttf", 16)
fh  = load("C:/Windows/Fonts/arialbd.ttf", 12)

d.text((W//2, 22), "Stack<T> — покрокова зміна стану при Push та Pop", font=ft, fill=ACCENT, anchor="mm")

# States: list of (operation_label, stack_contents_top_first, op_color)
states = [
    ("Початок\n(порожній)",      [],                          MUTED),
    ("Push(\"Аспірин\")",         ["Аспірин"],                 ORANGE),
    ("Push(\"Ібупрофен\")",       ["Ібупрофен", "Аспірин"],    ORANGE),
    ("Push(\"Лізиноприл\")",      ["Лізиноприл","Ібупрофен","Аспірин"], ORANGE),
    ("Pop() → \"Лізиноприл\"",   ["Ібупрофен", "Аспірин"],    ACCENT),
    ("Peek() → \"Ібупрофен\"",   ["Ібупрофен", "Аспірин"],    MUTED),
]

n_states = len(states)
state_w = (W - 40) // n_states
item_h = 30
item_w = state_w - 16
max_items = 3

col_top = 60

for si, (op_label, items, op_color) in enumerate(states):
    sx = 20 + si * state_w
    cx = sx + state_w // 2

    # Operation label (may have \n)
    lines = op_label.split("\n")
    for li, line in enumerate(lines):
        d.text((cx, col_top + li * 16), line, font=fh, fill=op_color, anchor="mm")

    # Stack visual — draw from bottom, max_items slots
    base_y = H - 80
    slot_gap = 4

    # Draw empty slots first
    for slot in range(max_items):
        sy = base_y - slot * (item_h + slot_gap)
        d.rounded_rectangle([sx + 8, sy, sx + 8 + item_w, sy + item_h],
                             radius=4, fill=DARK, outline=LINE, width=1)

    # Fill with actual items (bottom to top)
    for ii, item_name in enumerate(reversed(items)):
        sy = base_y - ii * (item_h + slot_gap)
        is_top = (ii == len(items) - 1)
        shade = PANEL if ii % 2 == 0 else "#1a2120"
        outline = ACCENT if is_top else LINE
        d.rounded_rectangle([sx + 8, sy, sx + 8 + item_w, sy + item_h],
                             radius=4, fill=shade, outline=outline, width=2 if is_top else 1)
        # Truncate long names
        name = item_name if len(item_name) <= 11 else item_name[:10] + "…"
        d.text((cx, sy + item_h // 2), name, font=fb,
               fill=ACCENT if is_top else TEXT, anchor="mm")

    # Count label
    d.text((cx, base_y + item_h + 14), f"Count={len(items)}", font=fs, fill=MUTED, anchor="mm")

    # Separator between states
    if si < n_states - 1:
        line_x = sx + state_w - 2
        d.line([(line_x, col_top + 36), (line_x, H - 50)], fill=LINE, width=1)

# Bottom footnote
d.text((W//2, H - 22),
       "foreach по Stack<T> повертає елементи у порядку LIFO: спочатку вершина (Top), потім вниз",
       font=fs, fill=MUTED, anchor="mm")

out = "C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude\worktrees/ecstatic-merkle-5676fd/lectures/_assets/10-04/stack-state-steps.png"
img.save(out)
print("OK:", out)
