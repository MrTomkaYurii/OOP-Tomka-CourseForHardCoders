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
        name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(name, size)
    except:
        return ImageFont.load_default()

def draw_throw_diagram():
    W, H = 860, 480
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(18, bold=True)
    label_f = load_font(14, bold=True)
    code_f  = load_font(12)
    note_f  = load_font(11)

    d.text((W // 2, 22), "Оператор throw: дві форми", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    # Left panel: throw new ...
    lx, ly, lw, lh = 60, 55, 340, 200
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh],
                        radius=10, fill=hex_to_rgb(PANEL),
                        outline=hex_to_rgb(YELLOW), width=2)
    d.text((lx + lw // 2, ly + 20), "throw new Exception(...)",
           font=label_f, fill=hex_to_rgb(YELLOW), anchor="mm")
    d.line([(lx + 12, ly + 36), (lx + lw - 12, ly + 36)],
           fill=hex_to_rgb(LINE), width=1)

    left_lines = [
        "Генерує новий виняток",
        "Використовується будь-де:",
        "  — у методах для валідації",
        "  — у блоці try",
        "  — у блоці catch (new виняток)",
        "Передає повідомлення через",
        "конструктор: new Ex(\"текст\")",
    ]
    for i, line in enumerate(left_lines):
        d.text((lx + 14, ly + 52 + i * 20), line, font=note_f,
               fill=hex_to_rgb(TEXT) if not line.startswith(" ") else hex_to_rgb(MUTED),
               anchor="lm")

    # Right panel: throw;
    rx, ry, rw, rh = 460, 55, 340, 200
    d.rounded_rectangle([rx, ry, rx + rw, ry + rh],
                        radius=10, fill=hex_to_rgb(PANEL),
                        outline=hex_to_rgb(RED), width=2)
    d.text((rx + rw // 2, ry + 20), "throw;",
           font=label_f, fill=hex_to_rgb(RED), anchor="mm")
    d.line([(rx + 12, ry + 36), (rx + rw - 12, ry + 36)],
           fill=hex_to_rgb(LINE), width=1)

    right_lines = [
        "Перекидає поточний виняток далі",
        "Можна лише у блоці catch",
        "Зберігає оригінальний StackTrace",
        "",
        "throw ex; — НЕБЕЗПЕЧНО:",
        "  скидає StackTrace до місця",
        "  повторного кидання",
    ]
    for i, line in enumerate(right_lines):
        color = RED if "НЕБЕЗПЕЧНО" in line else (MUTED if line.startswith("  ") else TEXT)
        d.text((rx + 14, ry + 52 + i * 20), line, font=note_f,
               fill=hex_to_rgb(color), anchor="lm")

    # Arrow between panels
    mid_x = (lx + lw + rx) // 2
    arrow_y = ly + lh // 2
    d.line([(lx + lw + 8, arrow_y), (rx - 8, arrow_y)],
           fill=hex_to_rgb(LINE), width=2)
    d.polygon([(rx - 8, arrow_y - 6), (rx - 8, arrow_y + 6), (rx, arrow_y)],
              fill=hex_to_rgb(LINE))
    d.text((mid_x, arrow_y - 14), "або", font=note_f,
           fill=hex_to_rgb(MUTED), anchor="mm")

    # InnerException section
    iy = ly + lh + 40
    ix0, ix1 = 60, W - 60
    d.rounded_rectangle([ix0, iy, ix1, iy + 110],
                        radius=10, fill=hex_to_rgb(PANEL),
                        outline=hex_to_rgb(ACCENT), width=2)
    d.text((W // 2, iy + 20), "Ланцюжок винятків — InnerException",
           font=label_f, fill=hex_to_rgb(ACCENT), anchor="mm")
    d.line([(ix0 + 16, iy + 36), (ix1 - 16, iy + 36)],
           fill=hex_to_rgb(LINE), width=1)
    d.text((W // 2, iy + 56),
           'throw new ApplicationException("опис", ex);',
           font=code_f, fill=hex_to_rgb(TEXT), anchor="mm")
    d.text((W // 2, iy + 80),
           "Другий аргумент конструктора — оригінальний виняток (InnerException).",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")
    d.text((W // 2, iy + 98),
           "Дозволяє зберегти першопричину при загортанні помилки у новий виняток.",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "throw-forms.png")

draw_throw_diagram()
print("Done.")
