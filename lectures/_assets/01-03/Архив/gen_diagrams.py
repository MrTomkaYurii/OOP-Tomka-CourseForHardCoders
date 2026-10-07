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

def draw_managed_vs_unmanaged():
    W, H = 860, 340
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(17, bold=True)
    label_f = load_font(14, bold=True)
    note_f  = load_font(11)

    d.text((W // 2, 20), "Керований та некерований код", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    bw = (W - 80) // 2 - 10
    bh = H - 60

    # Left: managed
    mx, my = 40, 48
    d.rounded_rectangle([mx, my, mx + bw, my + bh], radius=10,
                         fill=hex_to_rgb(PANEL), outline=hex_to_rgb(ACCENT), width=2)
    d.text((mx + bw // 2, my + 22), "Керований код", font=label_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")
    d.text((mx + bw // 2, my + 40), "C#, F#, Visual Basic → .NET CLR",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")
    d.line([(mx + 14, my + 52), (mx + bw - 14, my + 52)], fill=hex_to_rgb(LINE), width=1)

    managed_items = [
        (ACCENT,  "Компілюється у CIL (проміжний код)"),
        (ACCENT,  "Виконується під контролем CLR"),
        (ACCENT,  "Автоматичне керування пам'яттю (GC)"),
        (ACCENT,  "Перевірка типів на етапі компіляції"),
        (ACCENT,  "Єдина модель обробки винятків"),
        (ACCENT,  "Доступ до стандартної бібліотеки .NET"),
        (YELLOW,  "Підходить для більшості прикладних задач"),
    ]
    for i, (color, text) in enumerate(managed_items):
        d.text((mx + 18, my + 70 + i * 24), f"✓  {text}",
               font=note_f, fill=hex_to_rgb(color), anchor="lm")

    # Right: unmanaged
    ux, uy = mx + bw + 20, 48
    d.rounded_rectangle([ux, uy, ux + bw, uy + bh], radius=10,
                         fill=hex_to_rgb(PANEL), outline=hex_to_rgb(RED), width=2)
    d.text((ux + bw // 2, uy + 22), "Некерований код", font=label_f,
           fill=hex_to_rgb(RED), anchor="mm")
    d.text((ux + bw // 2, uy + 40), "C, C++, Rust → компілятор платформи",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")
    d.line([(ux + 14, uy + 52), (ux + bw - 14, uy + 52)], fill=hex_to_rgb(LINE), width=1)

    unmanaged_items = [
        (RED,    "Компілюється одразу у машинний код"),
        (RED,    "Виконується без CLR"),
        (RED,    "Ручне керування пам'яттю (malloc/free)"),
        (MUTED,  "Більше відповідальності за безпеку"),
        (MUTED,  "Вказівники, адреси пам'яті"),
        (YELLOW, "Системне програмування, драйвери"),
        (YELLOW, "Рушії, high-performance бібліотеки"),
    ]
    for i, (color, text) in enumerate(unmanaged_items):
        d.text((ux + 18, uy + 70 + i * 24), f"•  {text}",
               font=note_f, fill=hex_to_rgb(color), anchor="lm")

    save_if_new(img, "managed-vs-unmanaged.png")

def draw_clr_services():
    W, H = 820, 220
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(17, bold=True)
    label_f = load_font(12, bold=True)
    note_f  = load_font(11)

    d.text((W // 2, 18), "Служби, які CLR надає керованому коду", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    services = [
        ("JIT\nкомпіляція",      ACCENT),
        ("Garbage\nCollection",   ACCENT),
        ("Перевірка\nтипів",      YELLOW),
        ("Обробка\nвинятків",     YELLOW),
        ("Метадані\nта рефлексія",MUTED),
        ("Interop\nз нативним",   MUTED),
    ]

    bw, bh = 116, 70
    gap = 12
    total = len(services) * bw + (len(services) - 1) * gap
    sx = (W - total) // 2
    y0 = 48

    for i, (label, color) in enumerate(services):
        x0 = sx + i * (bw + gap)
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=8,
                             fill=hex_to_rgb(PANEL), outline=hex_to_rgb(color), width=2)
        for j, ln in enumerate(label.split("\n")):
            d.text((x0 + bw // 2, y0 + 22 + j * 20), ln, font=label_f,
                   fill=hex_to_rgb(color), anchor="mm")

    # bottom note
    d.text((W // 2, y0 + bh + 28),
           "Весь керований C#-код автоматично отримує всі ці служби — без додаткових зусиль програміста.",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")
    d.text((W // 2, y0 + bh + 48),
           "Завдяки цьому C# дозволяє зосередитися на логіці програми, а не на деталях платформи.",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "clr-services.png")

draw_managed_vs_unmanaged()
draw_clr_services()
print("Done.")
