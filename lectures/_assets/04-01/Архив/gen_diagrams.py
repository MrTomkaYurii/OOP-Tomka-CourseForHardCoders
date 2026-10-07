"""
Generate diagrams for lecture 04-01 (Inheritance).
NEVER overwrites existing files — only creates new ones.
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Palette
BG      = "#111413"
ACCENT  = "#76c7ad"
TEXT    = "#e5e9e7"
MUTED   = "#a1aaa6"
LINE    = "#2c3531"
PANEL   = "#191e1c"
RED     = "#e07070"
YELLOW  = "#c7b876"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def save_if_new(img, name):
    path = os.path.join(SCRIPT_DIR, name)
    if os.path.exists(path):
        print(f"SKIP (exists): {name}")
        return
    img.save(path)
    print(f"CREATED: {name}")

def try_font(size):
    candidates = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def try_font_bold(size):
    candidates = [
        "C:/Windows/Fonts/consolab.ttf",
        "C:/Windows/Fonts/courbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return try_font(size)

# ─────────────────────────────────────────────
# Diagram 1: Inheritance hierarchy
# Person (base) → Patient, Doctor
# ─────────────────────────────────────────────
def make_hierarchy():
    W, H = 820, 500
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    fn_title = try_font_bold(18)
    fn_label = try_font_bold(15)
    fn_body  = try_font(13)
    fn_small = try_font(12)

    # Title
    d.text((W//2, 22), "Ієрархія успадкування", font=fn_title, fill=hex_to_rgb(ACCENT), anchor="mm")

    # Box helper
    def box(x, y, w, h, header, lines, color=ACCENT):
        r = 8
        # shadow
        d.rounded_rectangle([x+4, y+4, x+w+4, y+h+4], radius=r, fill=hex_to_rgb(LINE))
        # panel
        d.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=hex_to_rgb(PANEL))
        d.rounded_rectangle([x, y, x+w, y+h], radius=r, outline=hex_to_rgb(color), width=2)
        # header bar
        d.rounded_rectangle([x+2, y+2, x+w-2, y+28], radius=r-2, fill=hex_to_rgb(color))
        # header text
        d.text((x+w//2, y+15), header, font=fn_label, fill=hex_to_rgb(BG), anchor="mm")
        # body lines
        for i, line in enumerate(lines):
            d.text((x+14, y+38 + i*20), line, font=fn_body, fill=hex_to_rgb(TEXT))

    # ── Person (base class) — top center
    bw, bh = 300, 130
    bx = W//2 - bw//2
    by = 55
    box(bx, by, bw, bh, "Person  (базовий клас)", [
        "  string Name { get; set; }",
        "  int Age { get; set; }",
        "",
        "  void Print()",
    ], ACCENT)

    # ── Arrow down-left to Patient
    arrow_top_x = W//2
    arrow_top_y = by + bh
    patient_cx = 200
    doctor_cx  = 620
    row2_y = 270

    # Line from base to fork
    fork_y = row2_y - 40
    d.line([(arrow_top_x, arrow_top_y), (arrow_top_x, fork_y)], fill=hex_to_rgb(MUTED), width=2)
    # Fork left
    d.line([(arrow_top_x, fork_y), (patient_cx, fork_y), (patient_cx, row2_y)],
           fill=hex_to_rgb(MUTED), width=2)
    # Fork right
    d.line([(arrow_top_x, fork_y), (doctor_cx, fork_y), (doctor_cx, row2_y)],
           fill=hex_to_rgb(MUTED), width=2)
    # Arrowheads
    for cx in [patient_cx, doctor_cx]:
        d.polygon([(cx, row2_y+10), (cx-7, row2_y-4), (cx+7, row2_y-4)],
                  fill=hex_to_rgb(MUTED))

    # ── Patient (left)
    pw, ph = 280, 140
    px = patient_cx - pw//2
    py = row2_y + 10
    box(px, py, pw, ph, "Patient  (похідний)", [
        "  string Diagnosis",
        "  DateTime AdmissionDate",
        "",
        "  void PrintInfo()",
    ], YELLOW)

    # ── Doctor (right)
    dw, dh = 280, 140
    dx = doctor_cx - dw//2
    dy = row2_y + 10
    box(dx, dy, dw, dh, "Doctor  (похідний)", [
        "  string Specialization",
        "  string LicenseNumber",
        "",
        "  void PrintInfo()",
    ], YELLOW)

    # ── Legend labels
    d.text((W//2, row2_y - 18), "is-a", font=fn_small, fill=hex_to_rgb(MUTED), anchor="mm")

    # Object base
    ob_y = 475
    d.text((W//2, ob_y - 10), "▲  Person : Object  (неявно)", font=fn_small,
           fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "inheritance-hierarchy.png")

# ─────────────────────────────────────────────
# Diagram 2: Constructor call order
# ─────────────────────────────────────────────
def make_constructor_order():
    W, H = 780, 500
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    fn_title  = try_font_bold(17)
    fn_label  = try_font_bold(14)
    fn_body   = try_font(13)

    d.text((W//2, 22), "Порядок виклику конструкторів при new Doctor(...)",
           font=fn_title, fill=hex_to_rgb(ACCENT), anchor="mm")

    steps = [
        ("1", "Doctor(name, age, spec)",         "Doctor",        YELLOW,  "виклик → делегує base(name, age)"),
        ("2", "Person(name, age) : this(name)",   "Person",        ACCENT,  "виклик → делегує this(name)"),
        ("3", "Person(name)",                     "Person",        ACCENT,  "виклик → неявно Object()"),
        ("4", "Object()",                         "System.Object", MUTED,   "виконання тіла Object"),
        ("5", "Person(name)",                     "Person",        ACCENT,  "виконання тіла Person(name)"),
        ("6", "Person(name, age)",                "Person",        ACCENT,  "виконання тіла Person(name, age)"),
        ("7", "Doctor(name, age, spec)",          "Doctor",        YELLOW,  "виконання тіла Doctor → об'єкт створено"),
    ]

    row_h = 55
    start_y = 55
    left_pad = 50

    for i, (num, ctor, cls, color, note) in enumerate(steps):
        y = start_y + i * row_h
        # number circle
        cx, cy = left_pad, y + row_h//2
        d.ellipse([cx-16, cy-16, cx+16, cy+16], fill=hex_to_rgb(color), outline=hex_to_rgb(color))
        d.text((cx, cy), num, font=fn_label, fill=hex_to_rgb(BG), anchor="mm")

        # panel
        px, py2, pw, ph = left_pad + 30, y + 6, 660, row_h - 12
        d.rounded_rectangle([px, py2, px+pw, py2+ph], radius=6, fill=hex_to_rgb(PANEL),
                             outline=hex_to_rgb(LINE), width=1)

        # constructor name
        d.text((px + 12, py2 + ph//2), ctor, font=fn_label, fill=hex_to_rgb(color), anchor="lm")
        # class tag
        tag_x = px + 310
        d.text((tag_x, py2 + ph//2), f"[{cls}]", font=fn_body, fill=hex_to_rgb(MUTED), anchor="lm")
        # note
        note_x = tag_x + 140
        d.text((note_x, py2 + ph//2), note, font=fn_body, fill=hex_to_rgb(TEXT), anchor="lm")

        # connector arrow to next
        if i < len(steps) - 1:
            next_y = start_y + (i+1) * row_h
            d.line([(cx, cy + 16), (cx, next_y + row_h//2 - 16)],
                   fill=hex_to_rgb(LINE), width=2)

    save_if_new(img, "constructor-order.png")

make_hierarchy()
make_constructor_order()
print("Done.")
