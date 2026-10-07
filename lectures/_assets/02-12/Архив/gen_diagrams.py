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

def draw_if_else():
    W, H = 880, 400
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Конструкція if / else if / else та тернарна операція", font=font(15, True), fill=h(ACCENT), anchor="mm")

    # ---- if/else if/else flow (left part) ----
    cx = 200

    # condition box
    d.rounded_rectangle([cx - 100, 50, cx + 100, 90], radius=6, fill=h(PANEL), outline=h(YELLOW), width=2)
    d.text((cx, 70), "if (умова)", font=font(12, True), fill=h(YELLOW), anchor="mm")

    # true arrow down-left
    d.line([(cx - 50, 90), (cx - 50, 115), (cx - 130, 115), (cx - 130, 145)], fill=h(ACCENT), width=2)
    d.text((cx - 90, 105), "true", font=font(10), fill=h(ACCENT), anchor="mm")
    d.rounded_rectangle([cx - 195, 145, cx - 65, 185], radius=5, fill=h(PANEL), outline=h(ACCENT), width=1)
    d.text((cx - 130, 165), "дії if-блоку", font=font(10), fill=h(ACCENT), anchor="mm")

    # false arrow down-right to else-if
    d.line([(cx + 50, 90), (cx + 50, 115), (cx + 130, 115), (cx + 130, 145)], fill=h(MUTED), width=2)
    d.text((cx + 90, 105), "false", font=font(10), fill=h(MUTED), anchor="mm")

    d.rounded_rectangle([cx + 65, 145, cx + 195, 185], radius=6, fill=h(PANEL), outline=h(YELLOW), width=2)
    d.text((cx + 130, 165), "else if (умова 2)", font=font(10, True), fill=h(YELLOW), anchor="mm")

    # else-if branches
    d.line([(cx + 100, 185), (cx + 100, 210), (cx + 35, 210), (cx + 35, 240)], fill=h(ACCENT), width=2)
    d.text((cx + 65, 200), "true", font=font(10), fill=h(ACCENT), anchor="mm")
    d.rounded_rectangle([cx - 30, 240, cx + 100, 275], radius=5, fill=h(PANEL), outline=h(ACCENT), width=1)
    d.text((cx + 35, 257), "дії else-if", font=font(10), fill=h(ACCENT), anchor="mm")

    d.line([(cx + 160, 185), (cx + 160, 210), (cx + 220, 210), (cx + 220, 240)], fill=h(MUTED), width=2)
    d.text((cx + 195, 200), "false", font=font(10), fill=h(MUTED), anchor="mm")
    d.rounded_rectangle([cx + 155, 240, cx + 285, 275], radius=5, fill=h(PANEL), outline=h(RED), width=1)
    d.text((cx + 220, 257), "else: дії", font=font(10), fill=h(RED), anchor="mm")

    # merge line
    d.line([(cx - 130, 185), (cx - 130, 310), (cx + 130, 310)], fill=h(MUTED), width=1)
    d.line([(cx + 35, 275), (cx + 35, 310)], fill=h(MUTED), width=1)
    d.line([(cx + 220, 275), (cx + 220, 310)], fill=h(MUTED), width=1)
    d.line([(cx + 130, 310), (cx + 130, 340)], fill=h(MUTED), width=2)
    d.polygon([(cx + 125, 336), (cx + 135, 336), (cx + 130, 345)], fill=h(MUTED))
    d.text((cx + 130, 358), "наступний рядок програми", font=font(10), fill=h(MUTED), anchor="mm")

    # ---- Ternary (right part) ----
    rx = 580
    d.rounded_rectangle([rx, 44, rx + 285, H - 20], radius=8, fill=h(PANEL), outline=h(YELLOW), width=2)
    d.text((rx + 142, 62), "Тернарна операція", font=font(13, True), fill=h(YELLOW), anchor="mm")

    d.text((rx + 12, 90), "синтаксис:", font=font(11, True), fill=h(MUTED), anchor="lm")
    d.rounded_rectangle([rx + 10, 102, rx + 272, 130], radius=4, fill=h(BG), outline=h(YELLOW), width=1)
    d.text((rx + 141, 116), "умова ? значення1 : значення2", font=font(10), fill=h(TEXT), anchor="mm")

    d.text((rx + 12, 148), "умова == true  →  значення1", font=font(11), fill=h(ACCENT), anchor="lm")
    d.text((rx + 12, 170), "умова == false →  значення2", font=font(11), fill=h(RED), anchor="lm")

    d.text((rx + 12, 200), "Приклад:", font=font(11, True), fill=h(MUTED), anchor="lm")
    lines = [
        "int age = 45;",
        'string group = age >= 60',
        '    ? "Пенсіонер"',
        '    : "Дорослий";',
    ]
    for i, l in enumerate(lines):
        d.text((rx + 14, 218 + i * 20), l, font=font(10), fill=h(TEXT), anchor="lm")

    d.text((rx + 12, 308), "Тернарна операція є скороченою", font=font(10), fill=h(MUTED), anchor="lm")
    d.text((rx + 12, 325), "формою if/else для виразів.", font=font(10), fill=h(MUTED), anchor="lm")
    d.text((rx + 12, 348), "Використовуйте лише для простих", font=font(10), fill=h(MUTED), anchor="lm")
    d.text((rx + 12, 365), "умов — складні знижують читабельність.", font=font(10), fill=h(MUTED), anchor="lm")

    save_if_new(img, "if-else-ternary.png")

draw_if_else()
print("Done.")
