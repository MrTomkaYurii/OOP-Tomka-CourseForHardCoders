from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.dirname(__file__)

BG      = "#111413"
ACCENT  = "#76c7ad"
TEXT    = "#e5e9e7"
MUTED   = "#a1aaa6"
LINE    = "#2c3531"
PANEL   = "#191e1c"
YELLOW  = "#c7b876"
RED     = "#e07070"

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def save_if_new(img, name):
    path = os.path.join(OUTPUT_DIR, name)
    if not os.path.exists(path):
        img.save(path)
        print(f"Saved: {name}")
    else:
        print(f"Skipped (exists): {name}")

def load_font(size, bold=False):
    try:
        name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(name, size)
    except:
        return ImageFont.load_default()

# Diagram: three catch forms + when filter
def draw_catch_forms():
    W, H = 860, 520
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f  = load_font(18, bold=True)
    label_f  = load_font(15, bold=True)
    code_f   = load_font(13)
    note_f   = load_font(12)

    d.text((W//2, 22), "Форми блоку catch", font=title_f, fill=hex_to_rgb(ACCENT), anchor="mm")

    forms = [
        {
            "title": "Форма 1 — без типу",
            "code":  "catch { ... }",
            "note":  "Перехоплює будь-який виняток.\nНе дає доступу до інформації про помилку.",
            "color": MUTED,
        },
        {
            "title": "Форма 2 — з типом",
            "code":  "catch (FormatException) { ... }",
            "note":  "Перехоплює лише вказаний тип.\nІнші типи винятків ігноруються.",
            "color": ACCENT,
        },
        {
            "title": "Форма 3 — тип + змінна",
            "code":  "catch (FormatException ex) { ... }",
            "note":  "Перехоплює вказаний тип.\nex.Message — текст помилки.",
            "color": YELLOW,
        },
    ]

    box_w = 240
    box_h = 160
    gap   = 30
    total = len(forms) * box_w + (len(forms) - 1) * gap
    start_x = (W - total) // 2
    y0 = 65

    for i, f in enumerate(forms):
        x0 = start_x + i * (box_w + gap)
        x1 = x0 + box_w
        y1 = y0 + box_h
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=hex_to_rgb(PANEL), outline=hex_to_rgb(f["color"]), width=2)
        d.text((x0 + box_w//2, y0 + 22), f["title"], font=label_f, fill=hex_to_rgb(f["color"]), anchor="mm")
        d.line([(x0 + 16, y0 + 38), (x1 - 16, y0 + 38)], fill=hex_to_rgb(LINE), width=1)
        d.text((x0 + box_w//2, y0 + 62), f["code"], font=code_f, fill=hex_to_rgb(TEXT), anchor="mm")
        note_lines = f["note"].split("\n")
        for j, line in enumerate(note_lines):
            d.text((x0 + box_w//2, y0 + 95 + j * 20), line, font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")

    # when filter section
    wy = y0 + box_h + 50
    wx0, wx1 = 80, W - 80
    d.rounded_rectangle([wx0, wy, wx1, wy + 120], radius=10, fill=hex_to_rgb(PANEL), outline=hex_to_rgb(RED), width=2)
    d.text((W//2, wy + 20), "Фільтр when", font=label_f, fill=hex_to_rgb(RED), anchor="mm")
    d.line([(wx0 + 20, wy + 36), (wx1 - 20, wy + 36)], fill=hex_to_rgb(LINE), width=1)
    d.text((W//2, wy + 60), "catch (ExceptionType ex) when (умова) { ... }",
           font=code_f, fill=hex_to_rgb(TEXT), anchor="mm")
    d.text((W//2, wy + 88), "Блок виконується лише якщо умова == true.",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")
    d.text((W//2, wy + 106), "Декілька catch одного типу — розрізняються через when.",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "catch-forms.png")

draw_catch_forms()
print("Done.")
