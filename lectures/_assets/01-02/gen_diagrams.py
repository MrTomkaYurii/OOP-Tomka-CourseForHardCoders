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

def draw_timeline():
    W, H = 860, 260
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(17, bold=True)
    label_f = load_font(13, bold=True)
    note_f  = load_font(11)

    d.text((W // 2, 18), "Еволюція платформи .NET", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    # Timeline line
    lx0, lx1, ly = 60, W - 60, 110
    d.line([(lx0, ly), (lx1, ly)], fill=hex_to_rgb(LINE), width=3)
    d.polygon([(lx1 - 8, ly - 5), (lx1 - 8, ly + 5), (lx1, ly)],
              fill=hex_to_rgb(LINE))

    events = [
        (0.0,  ".NET\nFramework\n2002",   MUTED,  True,  "Windows only"),
        (0.25, ".NET Core\n2016",         YELLOW, False, "кросплатформовий\nперезапуск"),
        (0.5,  ".NET 5\n2020",            ACCENT, True,  "злиття гілок,\nприбрано Core"),
        (0.72, ".NET 6\n(LTS)\n2021",     ACCENT, False, "попередня LTS"),
        (0.88, ".NET 8\n(LTS)\n2023",     ACCENT, True,  "підтримується"),
        (1.0,  ".NET 10\n(LTS)\n2025",    ACCENT, False, "поточна LTS"),
    ]

    for frac, label, color, above, note in events:
        ex = int(lx0 + frac * (lx1 - lx0 - 10))
        d.ellipse([ex - 6, ly - 6, ex + 6, ly + 6],
                  fill=hex_to_rgb(color), outline=hex_to_rgb(BG), width=2)

        lines = label.split("\n")
        if above:
            ty = ly - 20 - len(lines) * 16
            for i, ln in enumerate(lines):
                d.text((ex, ty + i * 16), ln, font=note_f,
                       fill=hex_to_rgb(color), anchor="mm")
            for j, nl in enumerate(note.split("\n")):
                d.text((ex, ly + 16 + j * 14), nl, font=note_f,
                       fill=hex_to_rgb(MUTED), anchor="mm")
        else:
            ty = ly + 20
            for i, ln in enumerate(lines):
                d.text((ex, ty + i * 16), ln, font=note_f,
                       fill=hex_to_rgb(color), anchor="mm")
            for j, nl in enumerate(note.split("\n")):
                d.text((ex, ly - 16 - j * 14), nl, font=note_f,
                       fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "dotnet-timeline.png")

def draw_versions_table():
    W, H = 820, 200
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(17, bold=True)
    label_f = load_font(13, bold=True)
    note_f  = load_font(11)

    d.text((W // 2, 18), "Типи релізів .NET", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    cols = [
        ("LTS\nLong Term Support",  ACCENT, [
            "Підтримка 3 роки",
            "Парні версії: 6, 8, 10...",
            "Для production і навчання",
            "Рекомендовано для курсів",
        ]),
        ("STS\nStandard Term Support", YELLOW, [
            "Підтримка 18 місяців",
            "Непарні версії: 7, 9...",
            "Нові функції швидше",
            "Для активних проєктів",
        ]),
    ]

    bw = (W - 80) // 2 - 10
    bh = H - 60
    for i, (title, color, items) in enumerate(cols):
        bx = 40 + i * (bw + 20)
        by = 48
        d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8,
                             fill=hex_to_rgb(PANEL), outline=hex_to_rgb(color), width=2)
        for j, ln in enumerate(title.split("\n")):
            d.text((bx + bw // 2, by + 16 + j * 17), ln,
                   font=label_f if j == 0 else note_f,
                   fill=hex_to_rgb(color), anchor="mm")
        d.line([(bx + 10, by + 52), (bx + bw - 10, by + 52)],
               fill=hex_to_rgb(LINE), width=1)
        for k, item in enumerate(items):
            d.text((bx + 16, by + 68 + k * 22), f"• {item}",
                   font=note_f, fill=hex_to_rgb(TEXT), anchor="lm")

    save_if_new(img, "dotnet-lts-sts.png")

draw_timeline()
draw_versions_table()
print("Done.")
