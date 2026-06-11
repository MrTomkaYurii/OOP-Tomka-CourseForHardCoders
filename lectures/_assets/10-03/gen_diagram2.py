# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

BG     = "#111413"
ACCENT = "#76c7ad"
TEXT   = "#e5e9e7"
MUTED  = "#a1aaa6"
LINE   = "#2c3531"
PANEL  = "#191e1c"
ORANGE = "#c7a276"
GREEN  = "#76c7ad"
RED    = "#c77676"

W, H = 900, 340
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

d.text((W//2, 24), "Queue<T> — складність операцій та порівняння з List<T>", font=ft, fill=ACCENT, anchor="mm")

# Table
col_x = [28, 240, 360, 480, 650]
col_w = [212, 120, 120, 170, 250]
row_h = 36
header_h = 40
table_top = 50

headers = ["Операція", "Queue<T>", "List<T>", "Stack<T>", "Примітка"]

d.rectangle([col_x[0]-4, table_top, W-12, table_top+header_h], fill=PANEL)
for i, h in enumerate(headers):
    cx = col_x[i] + col_w[i] // 2
    color = ACCENT if i == 1 else (ORANGE if i == 2 else TEXT)
    d.text((cx, table_top + header_h//2), h, font=fh, fill=color, anchor="mm")

d.line([(col_x[0]-4, table_top+header_h), (W-12, table_top+header_h)], fill=LINE, width=1)
for x in col_x[1:]:
    d.line([(x-6, table_top), (x-6, table_top+header_h)], fill=LINE, width=1)

rows = [
    # op, queue, list, stack, note, q_good, l_good, s_good
    ("Enqueue / Add в кінець", "O(1)*",    "O(1)*",    "—",      "Обидва — амортизована",         True,  True,  None),
    ("Dequeue / з початку",    "O(1)",     "O(n)",     "—",      "List зсуває всі елементи",       True,  False, None),
    ("Push / Pop (стек)",      "—",        "—",        "O(1)",   "Stack: тільки з вершини",        None,  None,  True),
    ("Peek (підглянути)",      "O(1)",     "O(1)*",    "O(1)",   "list[0] — O(1) але не Dequeue",  True,  True,  True),
    ("Contains",               "O(n)",     "O(n)",     "O(n)",   "Всі: лінійний пошук",            True,  True,  True),
    ("Доступ за індексом",     "❌ немає", "O(1)",     "❌ немає","Queue/Stack не індексовані",     False, True,  False),
    ("Обхід foreach",          "O(n)",     "O(n)",     "O(n)",   "Всі реалізують IEnumerable<T>",  True,  True,  True),
]

table_bot_y = table_top + header_h + len(rows) * row_h

for ri, row_data in enumerate(rows):
    op, qv, lv, sv, note = row_data[0], row_data[1], row_data[2], row_data[3], row_data[4]
    q_good, l_good, s_good = row_data[5], row_data[6], row_data[7]

    ry = table_top + header_h + ri * row_h
    row_fill = PANEL if ri % 2 == 0 else BG
    d.rectangle([col_x[0]-4, ry, W-12, ry+row_h], fill=row_fill)

    d.text((col_x[0]+4, ry+row_h//2), op, font=fr, fill=TEXT, anchor="lm")

    def cell_color(good):
        if good is None: return MUTED
        return GREEN if good else RED

    for ci, (val, good, cx_base, cw) in enumerate([
        (qv, q_good, col_x[1], col_w[1]),
        (lv, l_good, col_x[2], col_w[2]),
        (sv, s_good, col_x[3], col_w[3]),
    ]):
        cx = cx_base + cw // 2
        d.text((cx, ry+row_h//2), val, font=fb, fill=cell_color(good), anchor="mm")

    d.text((col_x[4]+6, ry+row_h//2), note, font=fs, fill=MUTED, anchor="lm")
    d.line([(col_x[0]-4, ry+row_h), (W-12, ry+row_h)], fill=LINE, width=1)

for x in col_x[1:]:
    d.line([(x-6, table_top), (x-6, table_bot_y)], fill=LINE, width=1)
d.rectangle([col_x[0]-4, table_top, W-12, table_bot_y], outline=LINE, width=1)

note_y = table_bot_y + 14
d.text((28, note_y), "* амортизована: більшість операцій O(1), але при заповненні буфера — перевиділення O(n)", font=fs, fill=MUTED)

lx2 = W - 220
d.rounded_rectangle([lx2, note_y - 4, W - 12, note_y + 34], radius=5, fill=PANEL)
d.rectangle([lx2+10, note_y+4,  lx2+22, note_y+14], fill=GREEN)
d.text((lx2+28, note_y+9), "— ефективно", font=fs, fill=TEXT, anchor="lm")
d.rectangle([lx2+10, note_y+20, lx2+22, note_y+30], fill=RED)
d.text((lx2+28, note_y+25), "— неефективно або відсутнє", font=fs, fill=TEXT, anchor="lm")

out = "C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/10-03/queue-complexity.png"
img.save(out)
print("OK:", out)
