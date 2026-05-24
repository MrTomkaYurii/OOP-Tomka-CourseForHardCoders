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

def draw_exception_hierarchy():
    W, H = 900, 560
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(18, bold=True)
    label_f = load_font(14, bold=True)
    small_f = load_font(12)
    prop_f  = load_font(11)

    d.text((W // 2, 22), "Ієрархія класу Exception", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    # Exception root box
    ex_x, ex_y, ex_w, ex_h = 280, 55, 340, 130
    d.rounded_rectangle([ex_x, ex_y, ex_x + ex_w, ex_y + ex_h],
                        radius=10, fill=hex_to_rgb(PANEL),
                        outline=hex_to_rgb(ACCENT), width=2)
    d.text((ex_x + ex_w // 2, ex_y + 18), "System.Exception",
           font=label_f, fill=hex_to_rgb(ACCENT), anchor="mm")
    d.line([(ex_x + 12, ex_y + 33), (ex_x + ex_w - 12, ex_y + 33)],
           fill=hex_to_rgb(LINE), width=1)

    props = [
        ("Message",        "текст помилки"),
        ("StackTrace",     "стек викликів"),
        ("InnerException", "внутрішній виняток"),
        ("TargetSite",     "метод, де стався виняток"),
    ]
    for i, (pname, pdesc) in enumerate(props):
        py = ex_y + 46 + i * 19
        d.text((ex_x + 16, py), f"{pname}:", font=prop_f,
               fill=hex_to_rgb(YELLOW), anchor="lm")
        d.text((ex_x + 130, py), pdesc, font=prop_f,
               fill=hex_to_rgb(MUTED), anchor="lm")

    # Child exception boxes
    children = [
        ("FormatException",           RED,    "некоректний\nформат рядка"),
        ("NullReferenceException",    MUTED,  "звернення\nдо null"),
        ("IndexOutOfRangeException",  YELLOW, "вихід за\nмежі масиву"),
        ("InvalidCastException",      RED,    "неприпустиме\nперетворення типу"),
        ("OverflowException",         MUTED,  "переповнення\nчислового типу"),
        ("DivideByZeroException",     ACCENT, "ділення цілого\nна нуль"),
    ]

    box_w = 128
    box_h = 72
    gap   = 10
    total = len(children) * box_w + (len(children) - 1) * gap
    start_x = (W - total) // 2
    child_y = 240

    root_bottom = ex_y + ex_h
    root_cx = ex_x + ex_w // 2
    line_y  = child_y - 20

    d.line([(root_cx, root_bottom), (root_cx, line_y)],
           fill=hex_to_rgb(LINE), width=2)

    for i, (name, color, desc) in enumerate(children):
        cx = start_x + i * (box_w + gap)
        ccx = cx + box_w // 2
        d.line([(ccx, line_y), (ccx, child_y)],
               fill=hex_to_rgb(LINE), width=1)
        d.line([(root_cx, line_y), (ccx, line_y)],
               fill=hex_to_rgb(LINE), width=1)

        d.rounded_rectangle([cx, child_y, cx + box_w, child_y + box_h],
                             radius=8, fill=hex_to_rgb(PANEL),
                             outline=hex_to_rgb(color), width=2)
        # short name
        short = name.replace("Exception", "")
        d.text((ccx, child_y + 18), short + "Exception",
               font=prop_f, fill=hex_to_rgb(color), anchor="mm")
        d.line([(cx + 8, child_y + 28), (cx + box_w - 8, child_y + 28)],
               fill=hex_to_rgb(LINE), width=1)
        for j, line in enumerate(desc.split("\n")):
            d.text((ccx, child_y + 42 + j * 15), line,
                   font=prop_f, fill=hex_to_rgb(MUTED), anchor="mm")

    # catch order note
    note_y = child_y + box_h + 40
    note_x0, note_x1 = 80, W - 80
    d.rounded_rectangle([note_x0, note_y, note_x1, note_y + 80],
                        radius=8, fill=hex_to_rgb(PANEL),
                        outline=hex_to_rgb(LINE), width=1)
    d.text((W // 2, note_y + 20), "Порядок catch: конкретний → загальний",
           font=label_f, fill=hex_to_rgb(YELLOW), anchor="mm")
    d.text((W // 2, note_y + 45),
           "catch (FormatException) { }   →   catch (Exception ex) { }",
           font=small_f, fill=hex_to_rgb(TEXT), anchor="mm")
    d.text((W // 2, note_y + 65),
           "Загальний Exception завжди останнім — інакше перехопить усі винятки",
           font=prop_f, fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "exception-hierarchy.png")

draw_exception_hierarchy()
print("Done.")
