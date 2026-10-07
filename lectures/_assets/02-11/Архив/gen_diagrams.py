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

def draw_conditional_ops():
    W, H = 900, 420
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Умовні вирази в C#", font=font(16, True), fill=h(ACCENT), anchor="mm")

    # Left panel: comparison operators
    lx = 15
    d.rounded_rectangle([lx, 40, lx + 400, H - 15], radius=8, fill=h(PANEL), outline=h(YELLOW), width=2)
    d.text((lx + 200, 58), "Оператори порівняння", font=font(13, True), fill=h(YELLOW), anchor="mm")

    cmp_ops = [
        ("==",  "Рівність",           "age == 18   → true / false"),
        ("!=",  "Нерівність",         "age != 0    → true / false"),
        ("<",   "Менше ніж",          "age < 60    → true / false"),
        (">",   "Більше ніж",         "age > 18    → true / false"),
        ("<=",  "Менше або рівно",    "age <= 110  → true / false"),
        (">=",  "Більше або рівно",   "age >= 0    → true / false"),
    ]
    for i, (op, name, ex) in enumerate(cmp_ops):
        ry = 74 + i * 52
        d.rounded_rectangle([lx + 10, ry, lx + 390, ry + 42], radius=5, fill=h(BG), outline=h(YELLOW), width=1)
        d.text((lx + 50, ry + 21), op, font=font(15, True), fill=h(YELLOW), anchor="mm")
        d.text((lx + 130, ry + 13), name, font=font(11, True), fill=h(TEXT), anchor="lm")
        d.text((lx + 130, ry + 30), ex, font=font(10), fill=h(MUTED), anchor="lm")

    note = "< > <= >= мають вищий пріоритет ніж == !="
    d.text((lx + 200, H - 28), note, font=font(10), fill=h(MUTED), anchor="mm")

    # Right panel: logical operators
    rx = 460
    d.rounded_rectangle([rx, 40, rx + 425, H - 15], radius=8, fill=h(PANEL), outline=h(ACCENT), width=2)
    d.text((rx + 212, 58), "Логічні оператори", font=font(13, True), fill=h(ACCENT), anchor="mm")

    log_ops = [
        ("&&",  "Логічне І (AND)",        "true && false → false", "коротке обчислення: якщо ліве false — праве не обч."),
        ("||",  "Логічне АБО (OR)",       "false || true → true",  "коротке обчислення: якщо ліве true — праве не обч."),
        ("!",   "Логічне НЕ (NOT)",       "!true → false",         "унарний оператор: інвертує значення"),
        ("^",   "Виключне АБО (XOR)",     "true ^ true → false",   "true тільки якщо операнди різні"),
        ("&",   "AND без скор. обч.",     "true & false → false",  "обидва операнди обчислюються завжди"),
        ("|",   "OR без скор. обч.",      "false | true → true",   "обидва операнди обчислюються завжди"),
    ]
    for i, (op, name, ex, note2) in enumerate(log_ops):
        ry = 74 + i * 52
        col = ACCENT if op in ("&&", "||", "!", "^") else MUTED
        d.rounded_rectangle([rx + 10, ry, rx + 415, ry + 42], radius=5, fill=h(BG), outline=h(col), width=1)
        d.text((rx + 50, ry + 21), op, font=font(14, True), fill=h(col), anchor="mm")
        d.text((rx + 80, ry + 13), name, font=font(11, True), fill=h(TEXT), anchor="lm")
        d.text((rx + 80, ry + 28), ex, font=font(10), fill=h(YELLOW), anchor="lm")
        d.text((rx + 190, ry + 30), note2, font=font(9), fill=h(MUTED), anchor="lm")

    save_if_new(img, "conditional-ops.png")

draw_conditional_ops()
print("Done.")
