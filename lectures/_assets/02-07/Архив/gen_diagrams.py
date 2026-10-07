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

def draw_bitwise():
    W, H = 880, 420
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Порозрядні операції C#", font=font(16, True), fill=h(ACCENT), anchor="mm")

    # Left: logical bitwise
    lx = 20
    d.text((lx + 195, 48), "Побітові логічні операції", font=font(13, True), fill=h(YELLOW), anchor="mm")

    ops = [
        ("&", "AND (і)", "1, якщо обидва розряди = 1",  "2 & 5 = 0"),
        ("|", "OR (або)", "1, якщо хоча б один = 1",     "2 | 5 = 7"),
        ("^", "XOR (виключне або)", "1, якщо розряди різні",   "45 ^ 102 = 75"),
        ("~", "NOT (інверсія)", "Інвертує всі розряди",   "~12 = -13"),
    ]

    for i, (op, name, rule, ex) in enumerate(ops):
        ry = 64 + i * 62
        d.rounded_rectangle([lx, ry, lx + 390, ry + 52], radius=6, fill=h(PANEL), outline=h(YELLOW), width=2)
        d.text((lx + 10, ry + 13), op, font=font(16, True), fill=h(YELLOW), anchor="lm")
        d.text((lx + 36, ry + 13), name, font=font(12, True), fill=h(TEXT), anchor="lm")
        d.text((lx + 10, ry + 33), rule, font=font(10), fill=h(MUTED), anchor="lm")
        d.text((lx + 380, ry + 23), ex, font=font(10), fill=h(ACCENT), anchor="rm")

    # Right: shift operations + two's complement note
    rx = 460
    d.text((rx + 195, 48), "Операції зсуву", font=font(13, True), fill=h(ACCENT), anchor="mm")

    shifts = [
        ("x << n", "Зсув вліво на n розрядів", "= x * 2ⁿ (якщо немає переповн.)", "16 << 2 = 64"),
        ("x >> n", "Зсув вправо на n розрядів", "= x / 2ⁿ (ціле ділення)",          "16 >> 2 = 4"),
    ]

    for i, (op, name, rule, ex) in enumerate(shifts):
        ry = 64 + i * 70
        d.rounded_rectangle([rx, ry, rx + 400, ry + 60], radius=6, fill=h(PANEL), outline=h(ACCENT), width=2)
        d.text((rx + 10, ry + 13), op, font=font(14, True), fill=h(ACCENT), anchor="lm")
        d.text((rx + 10, ry + 31), name, font=font(11), fill=h(TEXT), anchor="lm")
        d.text((rx + 10, ry + 47), rule, font=font(10), fill=h(MUTED), anchor="lm")
        d.text((rx + 390, ry + 13), ex, font=font(10), fill=h(YELLOW), anchor="rm")

    # Two's complement note
    note_y = 64 + 2 * 70 + 10
    d.rounded_rectangle([rx, note_y, rx + 400, note_y + 100], radius=6, fill=h(PANEL), outline=h(RED), width=2)
    d.text((rx + 10, note_y + 14), "Додатковий код (two's complement)", font=font(11, True), fill=h(RED), anchor="lm")
    d.text((rx + 10, note_y + 34), "Старший біт = знаковий розряд", font=font(10), fill=h(TEXT), anchor="lm")
    d.text((rx + 10, note_y + 52), "0... = позитивне число", font=font(10), fill=h(TEXT), anchor="lm")
    d.text((rx + 10, note_y + 70), "1... = негативне число", font=font(10), fill=h(TEXT), anchor="lm")
    d.text((rx + 10, note_y + 88), "Приклад: ~12 + 1 = -12", font=font(10), fill=h(MUTED), anchor="lm")

    save_if_new(img, "bitwise-ops.png")

def draw_twos_complement():
    """Подання від'ємних чисел у доповнювальному коді (two's complement)."""
    W, H = 820, 320
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Подання від'ємних чисел (доповнювальний код)", font=font(15, True), fill=h(ACCENT), anchor="mm")

    # Helper: draw one row with label, bits, value
    def draw_row(y, label, bits_str, value, color):
        # label
        d.text((30, y + 12), label, font=font(11, True), fill=h(color), anchor="lm")
        # individual bit boxes
        BOX = 34
        GAP = 3
        start_x = 160
        for bi, bit in enumerate(bits_str.replace(" ", "")):
            bx = start_x + bi * (BOX + GAP)
            is_sign = (bi == 0)
            box_color = RED if is_sign else PANEL
            d.rectangle([bx, y, bx + BOX, y + 26], fill=h(box_color), outline=h(color), width=1)
            d.text((bx + BOX // 2, y + 13), bit, font=font(12, True),
                   fill=h(YELLOW) if is_sign else h(TEXT), anchor="mm")
        # decimal value
        d.text((W - 30, y + 12), value, font=font(13, True), fill=h(color), anchor="rm")

    # Three examples from original image15
    rows = [
        (55,  "0000 0001",  "0000 0001",  "= +1",   ACCENT),
        (105, "1111 1111",  "11111111",   "= -1",   YELLOW),
        (155, "1111 0011",  "11110011",   "= -13",  RED),
    ]
    for y, label, bits, value, col in rows:
        draw_row(y, label, bits, value, col)

    # Sign bit legend
    d.text((160, 200), "↑", font=font(13, True), fill=h(RED), anchor="mm")
    d.text((160, 215), "знаковий біт", font=font(10), fill=h(RED), anchor="mm")
    d.text((160, 230), "0 = +, 1 = −", font=font(10), fill=h(MUTED), anchor="mm")

    # Rule box
    note_y = 252
    d.rounded_rectangle([30, note_y, W - 30, H - 10], radius=6, fill=h(PANEL), outline=h(MUTED), width=1)
    d.text((40, note_y + 14), "Щоб отримати від'ємне з позитивного:", font=font(11, True), fill=h(MUTED), anchor="lm")
    d.text((40, note_y + 32), "інвертувати всі біти  (~x)  →  додати 1  →  від'ємне число", font=font(11), fill=h(TEXT), anchor="lm")
    d.text((40, note_y + 50), "Приклад:  12 = 00001100  →  ~12 = 11110011  →  +1  →  11110100 = -12", font=font(10), fill=h(MUTED), anchor="lm")

    save_if_new(img, "twos-complement.png")

draw_twos_complement()
draw_bitwise()
print("Done.")
