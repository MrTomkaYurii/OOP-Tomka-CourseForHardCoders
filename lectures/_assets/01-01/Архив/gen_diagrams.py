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

# Diagram 1: C# code → CIL → CLR → Machine code pipeline
def draw_pipeline():
    W, H = 820, 200
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(17, bold=True)
    label_f = load_font(13, bold=True)
    note_f  = load_font(11)

    d.text((W // 2, 18), "Шлях C#-коду до виконання", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    steps = [
        ("Код C#\n.cs файл",        ACCENT),
        ("Компілятор\nC#",          MUTED),
        ("CIL + метадані\n.dll/.exe", YELLOW),
        ("CLR / JIT",               MUTED),
        ("Машинний код\nпроцесора", ACCENT),
    ]

    bw, bh = 120, 60
    gap = 20
    total = len(steps) * bw + (len(steps) - 1) * gap
    sx = (W - total) // 2
    y0 = 50

    for i, (label, color) in enumerate(steps):
        x0 = sx + i * (bw + gap)
        x1 = x0 + bw
        d.rounded_rectangle([x0, y0, x1, y0 + bh], radius=8,
                             fill=hex_to_rgb(PANEL), outline=hex_to_rgb(color), width=2)
        for j, line in enumerate(label.split("\n")):
            d.text((x0 + bw // 2, y0 + 18 + j * 18), line, font=note_f,
                   fill=hex_to_rgb(color), anchor="mm")
        if i < len(steps) - 1:
            ax = x1 + 4
            ay = y0 + bh // 2
            d.line([(ax, ay), (ax + gap - 8, ay)], fill=hex_to_rgb(LINE), width=2)
            d.polygon([(ax + gap - 8, ay - 5), (ax + gap - 8, ay + 5),
                       (ax + gap, ay)], fill=hex_to_rgb(LINE))

    # bottom note
    d.text((W // 2, y0 + bh + 30),
           "JIT компілює CIL у машинний код під час першого виклику методу — не весь код одразу.",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")
    d.text((W // 2, y0 + bh + 50),
           "Збірка (.dll/.exe) є кросплатформовою — виконується на будь-якій ОС, де є .NET runtime.",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "dotnet-pipeline.png")

# Diagram 2: .NET ecosystem — types of apps
def draw_ecosystem():
    W, H = 820, 300
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(17, bold=True)
    label_f = load_font(13, bold=True)
    note_f  = load_font(11)

    d.text((W // 2, 18), "Екосистема .NET: типи застосунків", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    # Center: C# + .NET
    cx, cy, cr = W // 2, 155, 48
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
              fill=hex_to_rgb(PANEL), outline=hex_to_rgb(ACCENT), width=3)
    d.text((cx, cy - 8), "C#", font=label_f, fill=hex_to_rgb(ACCENT), anchor="mm")
    d.text((cx, cy + 10), ".NET", font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")

    apps = [
        ("Консоль",     90,  65,  YELLOW),
        ("ASP.NET Core\nвеб-API", 210, 50, ACCENT),
        ("Blazor\nWASM",  360, 50, ACCENT),
        ("WPF / WinForms\nWindows UI", 580, 65, MUTED),
        ("MAUI\nкросплатформа", 700, 155, MUTED),
        ("Фонові служби\nWorker",    580, 245, YELLOW),
        ("Бібліотеки\nкласів",       360, 255, ACCENT),
        ("CLI-інструменти",          170, 250, MUTED),
        ("Тести\nxUnit/NUnit",        60, 205, YELLOW),
    ]

    for label, ax, ay, color in apps:
        bw, bh = 120, 44
        bx, by = ax - bw // 2, ay - bh // 2
        d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=6,
                             fill=hex_to_rgb(PANEL), outline=hex_to_rgb(color), width=2)
        for j, ln in enumerate(label.split("\n")):
            d.text((ax, ay - 8 + j * 16), ln, font=note_f,
                   fill=hex_to_rgb(color), anchor="mm")
        # line from center to box edge
        dx, dy = ax - cx, ay - cy
        dist = (dx**2 + dy**2) ** 0.5
        if dist > 0:
            nx, ny = dx / dist, dy / dist
            lx1 = int(cx + nx * cr)
            ly1 = int(cy + ny * cr)
            lx2 = int(ax - nx * (bw // 2 + 4))
            ly2 = int(ay - ny * (bh // 2 + 4))
            d.line([(lx1, ly1), (lx2, ly2)], fill=hex_to_rgb(LINE), width=1)

    save_if_new(img, "dotnet-ecosystem.png")

draw_pipeline()
draw_ecosystem()
print("Done.")
