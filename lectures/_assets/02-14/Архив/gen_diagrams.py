from PIL import Image, ImageDraw, ImageFont
import os
OUTPUT_DIR = os.path.dirname(__file__)
BG = "#111413"; ACCENT = "#76c7ad"; TEXT = "#e5e9e7"; MUTED = "#a1aaa6"
LINE = "#2c3531"; PANEL = "#191e1c"; YELLOW = "#c7b876"; RED = "#e07070"

def h(c):
    c = c.lstrip("#"); return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

def save_if_new(img, name):
    p = os.path.join(OUTPUT_DIR, name)
    if not os.path.exists(p): img.save(p); print(f"Saved: {name}")
    else: print(f"Skipped: {name}")

def font(s, b=False):
    try: return ImageFont.truetype("arialbd.ttf" if b else "arial.ttf", s)
    except: return ImageFont.load_default()

def draw_array_1d():
    W, H = 760, 220
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 18), "Одновимірний масив: int[] ages = { 45, 32, 67, 28, 55 };", font=font(13, True), fill=h(ACCENT), anchor="mm")

    values = [45, 32, 67, 28, 55]
    BOX = 70; GAP = 6; start_x = (W - (BOX + GAP) * len(values) + GAP) // 2
    box_y = 50

    for i, v in enumerate(values):
        bx = start_x + i * (BOX + GAP)
        d.rectangle([bx, box_y, bx + BOX, box_y + BOX], fill=h(PANEL), outline=h(ACCENT), width=2)
        d.text((bx + BOX // 2, box_y + BOX // 2), str(v), font=font(18, True), fill=h(TEXT), anchor="mm")
        # index below
        d.text((bx + BOX // 2, box_y + BOX + 16), f"[{i}]", font=font(12, True), fill=h(YELLOW), anchor="mm")
        # hat index (^)
        hat = len(values) - i
        d.text((bx + BOX // 2, box_y + BOX + 32), f"[^{hat}]", font=font(10), fill=h(MUTED), anchor="mm")

    # labels
    lx = start_x - 8
    rx = start_x + len(values) * (BOX + GAP) - GAP + 8
    d.text((lx, box_y + BOX // 2), "ages", font=font(12, True), fill=h(ACCENT), anchor="rm")
    d.text((start_x + BOX // 2, box_y - 14), "індекс [0]", font=font(10), fill=h(YELLOW), anchor="mm")
    d.text((start_x + (len(values) - 1) * (BOX + GAP) + BOX // 2, box_y - 14), f"індекс [{len(values)-1}]", font=font(10), fill=h(YELLOW), anchor="mm")

    # Length annotation
    arr_start = start_x
    arr_end = start_x + len(values) * (BOX + GAP) - GAP
    brace_y = box_y + BOX + 56
    d.line([(arr_start, brace_y), (arr_end, brace_y)], fill=h(MUTED), width=1)
    d.line([(arr_start, brace_y - 5), (arr_start, brace_y + 5)], fill=h(MUTED), width=1)
    d.line([(arr_end, brace_y - 5), (arr_end, brace_y + 5)], fill=h(MUTED), width=1)
    d.text(((arr_start + arr_end) // 2, brace_y + 14), "ages.Length = 5", font=font(11, True), fill=h(MUTED), anchor="mm")

    # Type note
    d.text((W // 2, H - 12), "Кожен елемент займає 4 байти (int). Масив з 5 елементів — 20 байт у пам'яті.", font=font(10), fill=h(MUTED), anchor="mm")

    save_if_new(img, "array-1d.png")

def draw_array_2d():
    W, H = 760, 270
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 18), "Двовимірний масив: int[,] schedule = new int[3, 4];", font=font(13, True), fill=h(YELLOW), anchor="mm")

    rows, cols = 3, 4
    BOX_W, BOX_H = 90, 44; GAP = 4
    start_x = (W - cols * (BOX_W + GAP) + GAP) // 2
    start_y = 48

    data = [
        [8, 10, 12, 14],
        [9, 11, 13, 15],
        [8, 12, 14, 16],
    ]

    for r in range(rows):
        for c in range(cols):
            bx = start_x + c * (BOX_W + GAP)
            by = start_y + r * (BOX_H + GAP)
            d.rectangle([bx, by, bx + BOX_W, by + BOX_H], fill=h(PANEL), outline=h(YELLOW), width=1)
            d.text((bx + BOX_W // 2, by + BOX_H // 2 - 8), str(data[r][c]), font=font(14, True), fill=h(TEXT), anchor="mm")
            d.text((bx + BOX_W // 2, by + BOX_H // 2 + 10), f"[{r},{c}]", font=font(9), fill=h(YELLOW), anchor="mm")

    # Row labels
    for r in range(rows):
        by = start_y + r * (BOX_H + GAP) + BOX_H // 2
        d.text((start_x - 12, by), f"рядок {r}", font=font(10), fill=h(ACCENT), anchor="rm")

    # Col labels
    for c in range(cols):
        bx = start_x + c * (BOX_W + GAP) + BOX_W // 2
        d.text((bx, start_y - 14), f"стовп. {c}", font=font(10), fill=h(ACCENT), anchor="mm")

    # Dimensions annotation
    arr_end_y = start_y + rows * (BOX_H + GAP) - GAP
    arr_end_x = start_x + cols * (BOX_W + GAP) - GAP

    note_y = arr_end_y + 22
    d.text((W // 2, note_y), "Ранг = 2   |   Рядків = 3   |   Стовпців = 4   |   Загальна кількість елементів: 12", font=font(11, True), fill=h(MUTED), anchor="mm")
    d.text((W // 2, note_y + 22), "Доступ: schedule[рядок, стовпець]     Наприклад: schedule[1, 2] = 13", font=font(10), fill=h(MUTED), anchor="mm")
    d.text((W // 2, H - 12), "Декларація: int[,] schedule = new int[3, 4];     Розмір у пам'яті: 3 × 4 × 4 = 48 байт", font=font(10), fill=h(MUTED), anchor="mm")

    save_if_new(img, "array-2d.png")

draw_array_1d()
draw_array_2d()
print("Done.")
