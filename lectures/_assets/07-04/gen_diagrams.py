"""
Diagrams for section 7.4 — Interface Inheritance
Palette: BG=#111413, ACCENT=#76c7ad, TEXT=#e5e9e7, MUTED=#a1aaa6, LINE=#2c3531, PANEL=#191e1c
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

BG     = "#111413"
ACCENT = "#76c7ad"
TEXT   = "#e5e9e7"
MUTED  = "#a1aaa6"
LINE   = "#2c3531"
PANEL  = "#191e1c"
RED    = "#e07070"
YELLOW = "#d4b96a"
BLUE   = "#6a9fd4"
PURPLE = "#c47ab8"

OUT_DIR = os.path.dirname(__file__)


def load_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    bold_candidates = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    pool = bold_candidates if bold else candidates
    for p in pool:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def rr(draw, xy, radius=10, fill=PANEL, outline=None, width=2):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)


def hline(draw, x0, x1, y, col=LINE, width=1):
    draw.line([(x0, y), (x1, y)], fill=col, width=width)


def arrow_up(draw, x, y_from, y_to, col=MUTED, w=2, head=7):
    """Vertical arrow pointing UP (inheritance direction)."""
    draw.line([(x, y_from), (x, y_to)], fill=col, width=w)
    # arrowhead at y_to (pointing up)
    draw.polygon([
        (x, y_to),
        (x - head, y_to + head + 2),
        (x + head, y_to + head + 2),
    ], fill=None, outline=col)


def arrow_right(draw, x_from, x_to, y, col=MUTED, w=2, head=7):
    """Horizontal arrow pointing RIGHT."""
    draw.line([(x_from, y), (x_to, y)], fill=col, width=w)
    draw.polygon([
        (x_to, y),
        (x_to - head - 2, y - head),
        (x_to - head - 2, y + head),
    ], fill=None, outline=col)


def make_inheritance_chain():
    """Diagram 1: single-chain interface inheritance in clinic domain."""
    W, H = 900, 560
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(18, bold=True)
    ft_name  = load_font(13, bold=True)
    ft_meth  = load_font(11)
    ft_label = load_font(11)

    draw.text((W // 2, 28), "Ланцюжок успадкування інтерфейсів",
              font=ft_title, fill=ACCENT, anchor="mm")

    # Boxes: bottom-to-top (IExaminable → IDiagnosable → ITreatable → class Doctor)
    BW, BH = 320, 80
    CX = W // 2  # center x

    boxes = [
        # (label_type, title, color, members, y)
        ("class",      "Doctor",       BLUE,   ["+ Examine() : void", "+ Diagnose() : void", "+ Treat() : void"], 420),
        ("interface",  "ITreatable",   ACCENT, ["Treat() : void"], 290),
        ("interface",  "IDiagnosable", YELLOW, ["Diagnose() : void"], 170),
        ("interface",  "IExaminable",  PURPLE, ["Examine() : void"],  55),
    ]

    box_tops = {}
    box_bottoms = {}

    for ltype, title, col, members, by in boxes:
        bx = CX - BW // 2
        # header bar
        header_h = 28
        rr(draw, [bx, by, bx + BW, by + BH], radius=8, fill=PANEL, outline=col, width=2)
        # stereotype
        stereo = "«interface»" if ltype == "interface" else "«class»"
        draw.text((CX, by + 13), stereo, font=ft_label, fill=MUTED, anchor="mm")
        # name
        draw.text((CX, by + 29), title, font=ft_name, fill=col, anchor="mm")
        hline(draw, bx + 10, bx + BW - 10, by + 42, col)
        for i, m in enumerate(members):
            draw.text((bx + 18, by + 48 + i * 16), m, font=ft_meth, fill=MUTED)
        box_tops[title]    = by
        box_bottoms[title] = by + BH

    # Arrows (inheritance: hollow triangle pointing to parent)
    pairs = [
        ("IDiagnosable", "IExaminable"),
        ("ITreatable",   "IDiagnosable"),
        ("Doctor",       "ITreatable"),
    ]
    for child, parent in pairs:
        y_from = box_tops[child]
        y_to   = box_bottoms[parent]
        mx = CX
        # dashed line for interface, solid for class→interface
        col = MUTED
        draw.line([(mx, y_from - 2), (mx, y_to + 2)], fill=col, width=1)
        # open triangle arrowhead pointing UP
        tri_size = 9
        draw.polygon([
            (mx, y_to + 2),
            (mx - tri_size, y_from - 2 - 3),
            (mx + tri_size, y_from - 2 - 3),
        ], fill=None, outline=col)

    # Legend
    lx, ly = 30, H - 60
    draw.text((lx, ly),       "——  успадкування інтерфейсу (extends)",   font=ft_label, fill=MUTED)
    draw.text((lx, ly + 18),  "——  реалізація інтерфейсу (implements)",  font=ft_label, fill=BLUE)

    # Annotation on the right
    ax = CX + BW // 2 + 18
    annots = [
        (55 + 40,  "базовий інтерфейс"),
        (170 + 40, "успадковує IExaminable"),
        (290 + 40, "успадковує IDiagnosable"),
        (420 + 40, "реалізує весь ланцюжок"),
    ]
    for ay, txt in annots:
        draw.line([(ax - 2, ay), (ax + 12, ay)], fill=LINE, width=1)
        draw.text((ax + 16, ay), txt, font=ft_label, fill=MUTED, anchor="lm")

    img.save(os.path.join(OUT_DIR, "interface-inheritance-chain.png"))
    print("Saved interface-inheritance-chain.png")


def make_multiple_inheritance():
    """Diagram 2: multiple interface inheritance — IClinicAppointment."""
    W, H = 1000, 480
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(18, bold=True)
    ft_name  = load_font(13, bold=True)
    ft_meth  = load_font(11)
    ft_label = load_font(11)
    ft_note  = load_font(11)

    draw.text((W // 2, 28), "Множинне успадкування інтерфейсів",
              font=ft_title, fill=ACCENT, anchor="mm")

    BW, BH = 280, 80

    # Top row: two parent interfaces
    parents = [
        ("ISchedulable", YELLOW, ["Schedule() : void", "GetSlot() : TimeSpan"], 70,  120),
        ("IPayable",     PURPLE, ["CalculateCost() : decimal", "ApplyDiscount() : void"], 70, 600),
    ]
    # Middle: derived interface
    mid = ("IClinicAppointment", ACCENT,
           ["PatientName : string", "DoctorName : string"], 230, W // 2 - BW // 2)
    # Bottom: class
    bot = ("Appointment", BLUE,
           ["Schedule() : void", "GetSlot() : TimeSpan",
            "CalculateCost() : decimal", "ApplyDiscount() : void",
            "PatientName : string", "DoctorName : string"], 370, W // 2 - BW // 2)

    def draw_box(ltype, title, col, members, by, bx):
        stereo = "«interface»" if ltype == "interface" else "«class»"
        rr(draw, [bx, by, bx + BW, by + BH], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((bx + BW // 2, by + 13), stereo, font=ft_label, fill=MUTED, anchor="mm")
        draw.text((bx + BW // 2, by + 29), title, font=ft_name, fill=col, anchor="mm")
        hline(draw, bx + 10, bx + BW - 10, by + 42, col)
        for i, m in enumerate(members):
            draw.text((bx + 14, by + 48 + i * 16), m, font=ft_meth, fill=MUTED)
        return {"top": by, "bottom": by + BH, "cx": bx + BW // 2}

    coords = {}
    for title, col, members, by, bx in parents:
        coords[title] = draw_box("interface", title, col, members, by, bx)

    mid_title, mid_col, mid_members, mid_by, mid_bx = mid
    coords[mid_title] = draw_box("interface", mid_title, mid_col, mid_members, mid_by, mid_bx)

    bot_title, bot_col, bot_members, bot_by, bot_bx = bot
    coords[bot_title] = draw_box("class", bot_title, bot_col, bot_members, bot_by, bot_bx)

    mid_cx = coords[mid_title]["cx"]
    mid_top = coords[mid_title]["top"]

    # Arrow from ISchedulable → IClinicAppointment
    p1 = coords["ISchedulable"]
    draw.line([(p1["cx"], p1["bottom"]), (mid_cx - 60, mid_top - 4)], fill=MUTED, width=1)
    # Arrow from IPayable → IClinicAppointment
    p2 = coords["IPayable"]
    draw.line([(p2["cx"], p2["bottom"]), (mid_cx + 60, mid_top - 4)], fill=MUTED, width=1)
    # Arrowhead at mid_top
    draw.polygon([
        (mid_cx, mid_top - 2),
        (mid_cx - 9, mid_top + 10),
        (mid_cx + 9, mid_top + 10),
    ], fill=None, outline=MUTED)

    # Arrow from IClinicAppointment → Appointment
    bot_cx = coords[bot_title]["cx"]
    bot_top = coords[bot_title]["top"]
    mid_bot = coords[mid_title]["bottom"]
    draw.line([(mid_cx, mid_bot), (bot_cx, bot_top - 2)], fill=MUTED, width=1)
    draw.polygon([
        (bot_cx, bot_top - 2),
        (bot_cx - 9, bot_top + 10),
        (bot_cx + 9, bot_top + 10),
    ], fill=None, outline=MUTED)

    # Note: IClinicAppointment inherits from BOTH
    note_x = mid_cx + BW // 2 + 16
    note_y = mid_by + 30
    draw.text((note_x, note_y),
              "успадковує обидва\nбатьківські інтерфейси",
              font=ft_note, fill=ACCENT)

    # Bottom note
    draw.text((W // 2, H - 18),
              "Інтерфейс може успадковувати будь-яку кількість інтерфейсів — на відміну від класів",
              font=ft_note, fill=MUTED, anchor="mm")

    img.save(os.path.join(OUT_DIR, "multiple-interface-inheritance.png"))
    print("Saved multiple-interface-inheritance.png")


if __name__ == "__main__":
    make_inheritance_chain()
    make_multiple_inheritance()
    print("All diagrams done.")
