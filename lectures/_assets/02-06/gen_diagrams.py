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

def draw_arithmetic():
    W, H = 860, 400
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Арифметичні операції C#", font=font(16, True), fill=h(ACCENT), anchor="mm")

    # Binary operations (left column)
    lx = 20
    d.text((lx + 190, 48), "Бінарні операції", font=font(13, True), fill=h(YELLOW), anchor="mm")

    binary = [
        ("+", "додавання", "x + y"),
        ("-", "віднімання", "x - y"),
        ("*", "множення", "x * y"),
        ("/", "ділення (ціле або дробове)", "x / y"),
        ("%", "залишок від ділення", "x % y"),
    ]

    for i, (op, name, ex) in enumerate(binary):
        ry = 64 + i * 56
        d.rounded_rectangle([lx, ry, lx + 380, ry + 46], radius=6, fill=h(PANEL), outline=h(YELLOW), width=2)
        d.text((lx + 10, ry + 13), op, font=font(16, True), fill=h(YELLOW), anchor="lm")
        d.text((lx + 40, ry + 13), name, font=font(12), fill=h(TEXT), anchor="lm")
        d.text((lx + 370, ry + 13), ex, font=font(11), fill=h(MUTED), anchor="rm")

    # Unary operations (right column)
    rx = 450
    d.text((rx + 190, 48), "Унарні операції та пріоритет", font=font(13, True), fill=h(ACCENT), anchor="mm")

    unary = [
        ("++x", "префіксний інкремент: спочатку +1, потім значення"),
        ("x++", "постфіксний інкремент: спочатку значення, потім +1"),
        ("--x", "префіксний декремент: спочатку -1, потім значення"),
        ("x--", "постфіксний декремент: спочатку значення, потім -1"),
    ]

    for i, (op, desc) in enumerate(unary):
        ry = 64 + i * 56
        d.rounded_rectangle([rx, ry, rx + 390, ry + 46], radius=6, fill=h(PANEL), outline=h(ACCENT), width=2)
        d.text((rx + 10, ry + 13), op, font=font(13, True), fill=h(ACCENT), anchor="lm")
        d.text((rx + 10, ry + 31), desc, font=font(10), fill=h(TEXT), anchor="lm")

    # Priority note at bottom
    note_y = H - 65
    d.rounded_rectangle([20, note_y, W - 20, H - 10], radius=6, fill=h(PANEL), outline=h(MUTED), width=1)
    d.text((30, note_y + 12), "Пріоритет (від вищого до нижчого):", font=font(11, True), fill=h(MUTED), anchor="lm")
    d.text((30, note_y + 32), "1. ++, --   →   2. *, /, %   →   3. +, -     (усі лівоасоціативні)", font=font(11), fill=h(TEXT), anchor="lm")

    save_if_new(img, "arithmetic-ops.png")

draw_arithmetic()
print("Done.")
