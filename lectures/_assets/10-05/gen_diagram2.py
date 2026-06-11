# -*- coding: utf-8 -*-
# Diagram 2: Dictionary method complexity table
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

W, H = 920, 370
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

d.text((W//2, 24), "Dictionary<K,V> — складність операцій vs List<T>", font=ft, fill=ACCENT, anchor="mm")

col_x = [28, 260, 390, 520, 690]
col_w = [232, 130, 130, 170, 230]
row_h = 36
header_h = 40
table_top = 50

headers = ["Операція", "Dictionary", "List<T>", "Причина", ""]
header_colors = [TEXT, ACCENT, ORANGE, TEXT, TEXT]

d.rectangle([col_x[0]-4, table_top, W-12, table_top+header_h], fill=PANEL)
for i, (h, hc) in enumerate(zip(headers[:4], header_colors[:4])):
    cx = col_x[i] + col_w[i] // 2
    d.text((cx, table_top + header_h//2), h, font=fh, fill=hc, anchor="mm")
d.line([(col_x[0]-4, table_top+header_h), (W-12, table_top+header_h)], fill=LINE, width=1)
for x in col_x[1:4]:
    d.line([(x-6, table_top), (x-6, table_top+header_h)], fill=LINE, width=1)

rows = [
    # op, dict_val, list_val, reason, d_good, l_good
    ("dict[key]  або  dict[key] = v",   "O(1)*",   "❌ немає",  "List не підтримує пошук за ключем",    True,  False),
    ("ContainsKey(key)",                 "O(1)*",   "O(n)",     "List: перебір; Dict: хеш",             True,  False),
    ("ContainsValue(val)",               "O(n)",    "O(n)",     "Обидва: лінійний перебір значень",      True,  True),
    ("Add / TryAdd",                     "O(1)*",   "O(1)*",    "Обидва амортизовані",                  True,  True),
    ("Remove(key)",                      "O(1)*",   "O(n)",     "List: зсув елементів після видалення", True,  False),
    ("TryGetValue(key, out v)",          "O(1)*",   "—",        "Безпечний доступ без виключення",      True,  None),
    ("foreach / перебір",                "O(n)",    "O(n)",     "Обидва: ітерація по всіх елементах",   True,  True),
    ("Count",                            "O(1)",    "O(1)",     "Обидва: зберігають лічильник",         True,  True),
]

table_bot = table_top + header_h + len(rows) * row_h

for ri, (op, dv, lv, reason, d_good, l_good) in enumerate(rows):
    ry = table_top + header_h + ri * row_h
    row_fill = PANEL if ri % 2 == 0 else BG
    d.rectangle([col_x[0]-4, ry, W-12, ry+row_h], fill=row_fill)
    d.text((col_x[0]+4, ry+row_h//2), op, font=fr, fill=TEXT, anchor="lm")

    def cc(good):
        if good is None: return MUTED
        return GREEN if good else RED

    cx_d = col_x[1] + col_w[1]//2
    cx_l = col_x[2] + col_w[2]//2
    d.text((cx_d, ry+row_h//2), dv, font=fb, fill=cc(d_good), anchor="mm")
    d.text((cx_l, ry+row_h//2), lv, font=fb, fill=cc(l_good), anchor="mm")
    d.text((col_x[3]+6, ry+row_h//2), reason, font=fs, fill=MUTED, anchor="lm")
    d.line([(col_x[0]-4, ry+row_h), (W-12, ry+row_h)], fill=LINE, width=1)

for x in col_x[1:4]:
    d.line([(x-6, table_top), (x-6, table_bot)], fill=LINE, width=1)
d.rectangle([col_x[0]-4, table_top, W-12, table_bot], outline=LINE, width=1)

note_y = table_bot + 14
d.text((28, note_y), "* O(1) — середній випадок (хеш без колізій); у гіршому випадку (багато колізій) — O(n), але на практиці майже завжди O(1)", font=fs, fill=MUTED)

lx2 = W - 220
d.rounded_rectangle([lx2, note_y-4, W-12, note_y+34], radius=5, fill=PANEL)
d.rectangle([lx2+10, note_y+4,  lx2+22, note_y+14], fill=GREEN)
d.text((lx2+28, note_y+9), "— ефективно", font=fs, fill=TEXT, anchor="lm")
d.rectangle([lx2+10, note_y+20, lx2+22, note_y+30], fill=RED)
d.text((lx2+28, note_y+25), "— неефективно або відсутнє", font=fs, fill=TEXT, anchor="lm")

out = "C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/10-05/dictionary-complexity.png"
img.save(out)
print("OK:", out)
