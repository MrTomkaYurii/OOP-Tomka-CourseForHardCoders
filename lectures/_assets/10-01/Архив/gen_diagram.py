from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)
RED    = (190, 80, 80)
FILL   = (40, 90, 75)
EMPTY  = (30, 40, 35)

W, H = 1000, 440
img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

def font(name, size):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
    except:
        return ImageFont.load_default()

ft = font("arialbd.ttf", 17)
fl = font("arial.ttf",   14)
fc = font("cour.ttf",    13)
fs = font("arial.ttf",   12)
fb = font("arialbd.ttf", 12)

d.text((W//2, 28), "List<T>: динамічний масив — Capacity vs Count", ACCENT, font=ft, anchor="mm")

# === STATE 1: Initial ===
def draw_state(x_off, y_off, title, items, capacity, label_count, label_cap, note=""):
    d.text((x_off + 180, y_off), title, ACCENT, font=fb, anchor="mm")
    cell_w = 48
    for i in range(capacity):
        cx = x_off + i * cell_w
        fill = FILL if i < len(items) else EMPTY
        outline = ACCENT if i < len(items) else LINE_C
        d.rectangle([cx+2, y_off+16, cx+cell_w-2, y_off+50], fill=fill, outline=outline)
        if i < len(items):
            d.text((cx+cell_w//2, y_off+33), items[i], TEXT, font=fs, anchor="mm")

    # Count brace
    count_end = x_off + len(items)*cell_w
    d.line([(x_off, y_off+62), (count_end, y_off+62)], ACCENT, width=2)
    d.text((x_off + len(items)*cell_w//2, y_off+76), label_count, ACCENT, font=fs, anchor="mm")

    # Capacity brace
    cap_end = x_off + capacity*cell_w
    d.line([(x_off, y_off+88), (cap_end, y_off+88)], AMBER, width=2)
    d.text((x_off + capacity*cell_w//2, y_off+102), label_cap, AMBER, font=fs, anchor="mm")

    if note:
        d.text((x_off + capacity*cell_w//2, y_off+118), note, MUTED, font=fs, anchor="mm")

# Row 1: initial
draw_state(30, 55,  "Count=3, Capacity=4",
           ["P1","P2","P3"], 4,
           "Count = 3", "Capacity = 4")

draw_state(390, 55, "Count=4, Capacity=4 — Add → розширення!",
           ["P1","P2","P3","P4"], 4,
           "Count = 4", "Capacity = 4",
           "⚠ Count == Capacity → наступний Add виділить новий масив ×2")

draw_state(30, 210, "Після розширення: Capacity подвоюється",
           ["P1","P2","P3","P4","P5"], 8,
           "Count = 5", "Capacity = 8  (×2)",
           "Всі старі елементи скопійовані в новий масив")

# === Right: Complexity table ===
tbl_x, tbl_y = 620, 200
d.text((tbl_x+160, tbl_y), "Складність операцій", MUTED, font=fl, anchor="mm")
d.line([(tbl_x, tbl_y+16), (tbl_x+320, tbl_y+16)], LINE_C, width=1)

ops = [
    ("Add(item)",       "O(1)*",  "* амортизована"),
    ("Insert(i, item)", "O(n)",   "зсув елементів"),
    ("Remove(item)",    "O(n)",   "пошук + зсув"),
    ("RemoveAt(i)",     "O(n)",   "зсув елементів"),
    ("list[i]",         "O(1)",   "прямий доступ"),
    ("Contains",        "O(n)",   "лінійний пошук"),
    ("Sort()",          "O(n log n)", "QuickSort"),
]
for i, (op, complexity, note) in enumerate(ops):
    y = tbl_y + 28 + i * 26
    col = ACCENT if complexity == "O(1)" or complexity == "O(1)*" else (AMBER if "log" in complexity else RED)
    d.text((tbl_x+4,   y), op,         TEXT, font=fc, anchor="lm")
    d.text((tbl_x+180, y), complexity,  col,  font=fb, anchor="lm")
    d.text((tbl_x+250, y), note,        MUTED, font=fs, anchor="lm")

out = "lectures/_assets/10-01/list-capacity-complexity.png"
img.save(out)
print(f"OK: {out}")
