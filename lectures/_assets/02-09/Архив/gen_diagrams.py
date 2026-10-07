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

def draw_type_conversion():
    W, H = 880, 360
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Перетворення базових типів", font=font(16, True), fill=h(ACCENT), anchor="mm")

    # Left: widening (розширювальне) - implicit
    lx = 20
    d.text((lx + 190, 48), "Розширювальне (implicit)", font=font(13, True), fill=h(ACCENT), anchor="mm")
    d.text((lx + 190, 66), "менший тип → більший, компілятор автоматично", font=font(10), fill=h(MUTED), anchor="mm")

    widening = [
        ("byte",    "→",  "short / int / long / float / double / decimal"),
        ("short",   "→",  "int / long / float / double / decimal"),
        ("int",     "→",  "long / float / double / decimal"),
        ("long",    "→",  "float / double / decimal"),
        ("float",   "→",  "double"),
        ("char",    "→",  "int / long / float / double"),
    ]

    for i, (src, arr, dst) in enumerate(widening):
        ry = 82 + i * 38
        d.rounded_rectangle([lx, ry, lx + 380, ry + 30], radius=5, fill=h(PANEL), outline=h(ACCENT), width=1)
        d.text((lx + 8, ry + 9), src, font=font(11, True), fill=h(ACCENT), anchor="lm")
        d.text((lx + 54, ry + 9), arr, font=font(11), fill=h(MUTED), anchor="lm")
        d.text((lx + 72, ry + 9), dst, font=font(10), fill=h(TEXT), anchor="lm")

    # Right: narrowing (звужувальне) - explicit
    rx = 450
    d.text((rx + 200, 48), "Звужувальне (explicit)", font=font(13, True), fill=h(YELLOW), anchor="mm")
    d.text((rx + 200, 66), "більший тип → менший, потрібне явне приведення (Тип)", font=font(10), fill=h(MUTED), anchor="mm")

    narrowing = [
        ("int / long",    "→", "byte / short"),
        ("double",        "→", "int / long / decimal"),
        ("decimal",       "→", "int / long / double"),
        ("long",          "→", "int"),
        ("double / float","→", "float / int"),
    ]

    for i, (src, arr, dst) in enumerate(narrowing):
        ry = 82 + i * 38
        d.rounded_rectangle([rx, ry, rx + 410, ry + 30], radius=5, fill=h(PANEL), outline=h(YELLOW), width=1)
        d.text((rx + 8, ry + 9), src, font=font(11, True), fill=h(YELLOW), anchor="lm")
        d.text((rx + 110, ry + 9), arr, font=font(11), fill=h(MUTED), anchor="lm")
        d.text((rx + 128, ry + 9), dst, font=font(10), fill=h(TEXT), anchor="lm")

    # Explicit cast syntax note
    note_y = H - 52
    d.rounded_rectangle([20, note_y, W - 20, H - 8], radius=5, fill=h(PANEL), outline=h(RED), width=1)
    d.text((30, note_y + 14), "Синтаксис явного приведення:   (тип) значення     наприклад:  int b = (int) 3.7;   →   b = 3", font=font(11), fill=h(TEXT), anchor="lm")

    save_if_new(img, "type-conversion.png")

draw_type_conversion()
print("Done.")
