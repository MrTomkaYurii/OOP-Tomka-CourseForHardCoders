from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.dirname(__file__)

BG     = "#111413"
ACCENT = "#76c7ad"
TEXT   = "#e5e9e7"
MUTED  = "#a1aaa6"
LINE   = "#2c3531"
PANEL  = "#191e1c"
YELLOW = "#c7b876"
RED    = "#e07070"

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
        fn = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(fn, size)
    except:
        return ImageFont.load_default()

# Diagram 1: JIT execution flow (step by step)
def draw_jit_flow():
    W, H = 860, 320
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(17, bold=True)
    label_f = load_font(13, bold=True)
    note_f  = load_font(11)

    d.text((W // 2, 20), "Як JIT компілює методи під час виконання", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    # Steps
    steps = [
        ("1. Запуск\nпрограми",     "CLR завантажує\nзбірку (.dll)",         ACCENT),
        ("2. Виклик\nметоду",       "Метод викликається\nвперше",             YELLOW),
        ("3. JIT\nкомпіляція",      "CIL → машинний код\nдля поточного CPU",  RED),
        ("4. Виконання",            "Скомпільований код\nзапускається",       ACCENT),
        ("5. Повторний\nвиклик",    "Кешований код\nвикористовується знову",  MUTED),
    ]

    bw, bh = 140, 80
    gap    = 16
    total  = len(steps) * bw + (len(steps) - 1) * gap
    sx     = (W - total) // 2
    y0     = 50

    for i, (title, note, color) in enumerate(steps):
        x0 = sx + i * (bw + gap)
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=8,
                             fill=hex_to_rgb(PANEL), outline=hex_to_rgb(color), width=2)
        for j, ln in enumerate(title.split("\n")):
            d.text((x0 + bw // 2, y0 + 16 + j * 17), ln,
                   font=label_f, fill=hex_to_rgb(color), anchor="mm")
        d.line([(x0 + 10, y0 + 38), (x0 + bw - 10, y0 + 38)],
               fill=hex_to_rgb(LINE), width=1)
        for j, ln in enumerate(note.split("\n")):
            d.text((x0 + bw // 2, y0 + 52 + j * 15), ln,
                   font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")

        if i < len(steps) - 1:
            ax = x0 + bw + 4
            ay = y0 + bh // 2
            d.line([(ax, ay), (ax + gap - 8, ay)], fill=hex_to_rgb(LINE), width=2)
            d.polygon([(ax + gap - 8, ay - 5), (ax + gap - 8, ay + 5),
                       (ax + gap, ay)], fill=hex_to_rgb(LINE))

    # Cache annotation
    cache_y = y0 + bh + 30
    d.rounded_rectangle([sx, cache_y, sx + total, cache_y + 60], radius=8,
                         fill=hex_to_rgb(PANEL), outline=hex_to_rgb(LINE), width=1)
    d.text((W // 2, cache_y + 16), "Кеш скомпільованого коду",
           font=label_f, fill=hex_to_rgb(YELLOW), anchor="mm")
    d.text((W // 2, cache_y + 36),
           "Після першої JIT-компіляції машинний код зберігається в пам'яті.",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")
    d.text((W // 2, cache_y + 52),
           "Повторні виклики методу виконуються без JIT — одразу у нативному коді.",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "jit-flow.png")

# Diagram 2: JIT vs AOT
def draw_jit_vs_aot():
    W, H = 820, 220
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(17, bold=True)
    label_f = load_font(13, bold=True)
    note_f  = load_font(11)

    d.text((W // 2, 18), "JIT vs AOT компіляція", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    bw = (W - 80) // 2 - 10
    bh = H - 60

    panels = [
        ("JIT — Just-In-Time", ACCENT, [
            "Компіляція під час першого виклику методу",
            "Кросплатформова збірка (.dll)",
            "Оптимізує під конкретний CPU",
            "Невеликий «розігрів» при старті",
            "Стандарт для більшості .NET-програм",
        ]),
        ("AOT — Ahead-Of-Time", YELLOW, [
            "Компіляція наперед, до запуску",
            "Результат — нативний бінарний файл",
            "Миттєвий старт без «розігріву»",
            "Менший обсяг пам'яті при запуску",
            "Корисно: Lambda, MAUI, Blazor WASM",
        ]),
    ]

    for i, (title, color, items) in enumerate(panels):
        bx = 40 + i * (bw + 20)
        by = 48
        d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8,
                             fill=hex_to_rgb(PANEL), outline=hex_to_rgb(color), width=2)
        d.text((bx + bw // 2, by + 20), title, font=label_f,
               fill=hex_to_rgb(color), anchor="mm")
        d.line([(bx + 12, by + 34), (bx + bw - 12, by + 34)],
               fill=hex_to_rgb(LINE), width=1)
        for k, item in enumerate(items):
            d.text((bx + 16, by + 52 + k * 24), f"• {item}",
                   font=note_f, fill=hex_to_rgb(TEXT), anchor="lm")

    save_if_new(img, "jit-vs-aot.png")

draw_jit_flow()
draw_jit_vs_aot()
print("Done.")
