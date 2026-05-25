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

def draw_console_io():
    W, H = 860, 380
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Консольне введення-виведення", font=font(16, True), fill=h(ACCENT), anchor="mm")

    # Left column: Output methods
    lx = 30
    d.text((lx + 170, 50), "Виведення", font=font(13, True), fill=h(YELLOW), anchor="mm")

    methods_out = [
        ("Console.WriteLine(value)", "Виводить значення + перехід на новий рядок"),
        ("Console.Write(value)", "Виводить значення без переходу на новий рядок"),
        ('$"... {змінна} ..."', "Інтерполяція рядка — вбудовування значень"),
        ('"... {0} {1} ..."', "Форматний рядок з плейсхолдерами"),
    ]

    for i, (name, desc) in enumerate(methods_out):
        ry = 68 + i * 62
        d.rounded_rectangle([lx, ry, lx + 340, ry + 52], radius=6, fill=h(PANEL), outline=h(YELLOW), width=2)
        d.text((lx + 10, ry + 13), name, font=font(11, True), fill=h(YELLOW), anchor="lm")
        d.text((lx + 10, ry + 33), desc, font=font(10), fill=h(TEXT), anchor="lm")

    # Right column: Input methods
    rx = 460
    d.text((rx + 170, 50), "Введення", font=font(13, True), fill=h(ACCENT), anchor="mm")

    methods_in = [
        ("Console.ReadLine()", "Зчитує рядок; повертає string?"),
        ("Convert.ToInt32(...)", "Перетворює рядок → int"),
        ("Convert.ToDouble(...)", "Перетворює рядок → double"),
        ("Convert.ToDecimal(...)", "Перетворює рядок → decimal"),
    ]

    for i, (name, desc) in enumerate(methods_in):
        ry = 68 + i * 62
        d.rounded_rectangle([rx, ry, rx + 370, ry + 52], radius=6, fill=h(PANEL), outline=h(ACCENT), width=2)
        d.text((rx + 10, ry + 13), name, font=font(11, True), fill=h(ACCENT), anchor="lm")
        d.text((rx + 10, ry + 33), desc, font=font(10), fill=h(TEXT), anchor="lm")

    # Arrow between columns
    mid_x = (lx + 340 + rx) // 2
    d.line([(lx + 340, H // 2 - 10), (rx, H // 2 - 10)], fill=h(MUTED), width=2)
    d.text((mid_x, H // 2 - 20), "Програма", font=font(10, True), fill=h(MUTED), anchor="mm")

    # Bottom note
    d.text((W // 2, H - 20), "string? — може бути null, якщо введення недоступне", font=font(10), fill=h(MUTED), anchor="mm")

    save_if_new(img, "console-io.png")

draw_console_io()
print("Done.")
