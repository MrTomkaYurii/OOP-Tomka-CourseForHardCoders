# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

BG     = "#111413"
ACCENT = "#76c7ad"   # List<T>  color
TEXT   = "#e5e9e7"
MUTED  = "#a1aaa6"
LINE   = "#2c3531"
PANEL  = "#191e1c"
ORANGE = "#c7a276"   # LinkedList color
RED    = "#c77676"
GREEN  = "#76c7ad"

W, H = 900, 480
img = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(img)

def load(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

fb  = load("C:/Windows/Fonts/arialbd.ttf", 14)
fr  = load("C:/Windows/Fonts/arial.ttf",   13)
fs  = load("C:/Windows/Fonts/arial.ttf",   11)
ft  = load("C:/Windows/Fonts/arialbd.ttf", 16)
fh  = load("C:/Windows/Fonts/arialbd.ttf", 13)

# Title
d.text((W//2, 24), "LinkedList<T> vs List<T> — складність ключових операцій", font=ft, fill=ACCENT, anchor="mm")

# Table layout
col_x = [28, 260, 410, 560, 710]   # Operation | List O() | LinkedList O() | Note
col_w = [232, 150, 150, 340]
row_h = 36
header_h = 40
table_top = 52

headers = ["Операція", "List<T>", "LinkedList<T>", "Пояснення"]

# Header row
d.rectangle([col_x[0]-4, table_top, W-12, table_top+header_h], fill=PANEL)
for i, h in enumerate(headers):
    cx = col_x[i] + col_w[i] // 2
    color = ACCENT if i == 1 else (ORANGE if i == 2 else TEXT)
    d.text((cx, table_top + header_h//2), h, font=fh, fill=color, anchor="mm")

# Separator line
d.line([(col_x[0]-4, table_top+header_h), (W-12, table_top+header_h)], fill=LINE, width=1)
# Vertical dividers
for x in col_x[1:]:
    d.line([(x-6, table_top), (x-6, table_top+header_h)], fill=LINE, width=1)

# Data rows
# (operation, list_val, linked_val, note, list_good, linked_good)
# list_good / linked_good: True = green, False = red/orange
rows = [
    ("Доступ за індексом  list[i]",  "O(1)",      "❌ немає",    "LinkedList не підтримує індексацію",          True,  False),
    ("Add в кінець",                  "O(1)*",     "O(1)",       "Обидва ефективні; * — амортизована",          True,  True),
    ("AddFirst / на початок",         "O(n)",      "O(1)",       "LinkedList: лише змінити посилання Head",     False, True),
    ("Insert в середину",             "O(n)",      "O(1)**",     "** після знаходження вузла; пошук O(n)",      False, True),
    ("Remove за значенням",           "O(n)",      "O(n)",       "Обидва: лінійний пошук",                      True,  True),
    ("RemoveFirst / RemoveLast",      "O(n)",      "O(1)",       "LinkedList: лише переставити Head/Tail",      False, True),
    ("Contains / Find",               "O(n)",      "O(n)",       "Обидва: повний перебір",                      True,  True),
    ("Обхід foreach",                 "O(n)",      "O(n)",       "Обидва реалізують IEnumerable<T>",            True,  True),
    ("Пам'ять на елемент",            "~мінімум",  "+ 2 покажч.", "LinkedList: додатково Next + Previous",     True,  False),
]

for ri, (op, lv, llv, note, lg, llg) in enumerate(rows):
    ry = table_top + header_h + ri * row_h
    row_fill = PANEL if ri % 2 == 0 else BG
    d.rectangle([col_x[0]-4, ry, W-12, ry+row_h], fill=row_fill)

    # Operation name
    d.text((col_x[0] + 4, ry + row_h//2), op, font=fr, fill=TEXT, anchor="lm")

    # List<T> value
    lv_color = GREEN if lg else RED
    lx = col_x[1] + col_w[1] // 2
    d.text((lx, ry + row_h//2), lv, font=fb, fill=lv_color, anchor="mm")

    # LinkedList<T> value
    llv_color = GREEN if llg else RED
    llx = col_x[2] + col_w[2] // 2
    d.text((llx, ry + row_h//2), llv, font=fb, fill=llv_color, anchor="mm")

    # Note
    d.text((col_x[3] + 8, ry + row_h//2), note, font=fs, fill=MUTED, anchor="lm")

    # Horizontal divider
    d.line([(col_x[0]-4, ry+row_h), (W-12, ry+row_h)], fill=LINE, width=1)

# Vertical dividers (full table)
table_bot = table_top + header_h + len(rows) * row_h
for x in col_x[1:]:
    d.line([(x-6, table_top), (x-6, table_bot)], fill=LINE, width=1)
# Outer border
d.rectangle([col_x[0]-4, table_top, W-12, table_bot], outline=LINE, width=1)

# Legend / footnote
note_y = table_bot + 14
d.text((28, note_y),     "* амортизована: більшість Add — O(1), але іноді список подвоює буфер — O(n)", font=fs, fill=MUTED)
d.text((28, note_y+16),  "** Insert в середину: знайти вузол — O(n), саму вставку — O(1); вказується O(1) після отримання вузла", font=fs, fill=MUTED)

# Color legend
lx2 = W - 260
d.rounded_rectangle([lx2, note_y - 4, W - 12, note_y + 34], radius=5, fill=PANEL)
d.rectangle([lx2 + 10, note_y + 4, lx2 + 22, note_y + 14], fill=GREEN)
d.text((lx2 + 28, note_y + 9), "— ефективно", font=fs, fill=TEXT, anchor="lm")
d.rectangle([lx2 + 10, note_y + 20, lx2 + 22, note_y + 30], fill=RED)
d.text((lx2 + 28, note_y + 25), "— неефективно або відсутнє", font=fs, fill=TEXT, anchor="lm")

out = "C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/10-02/linkedlist-complexity.png"
img.save(out)
print("OK:", out)
