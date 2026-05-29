"""
Diagrams for section 20.3 — OCP
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

def arrow(draw, x1, y1, x2, y2, col, w=2, head=8):
    draw.line([(x1, y1), (x2, y2)], fill=col, width=w)
    angle = math.atan2(y2 - y1, x2 - x1)
    draw.polygon([
        (x2, y2),
        (int(x2 - head * math.cos(angle - 0.4)), int(y2 - head * math.sin(angle - 0.4))),
        (int(x2 - head * math.cos(angle + 0.4)), int(y2 - head * math.sin(angle + 0.4))),
    ], fill=col)


# ─── Diagram 1: Before OCP ───────────────────────────────────────────
def make_before_ocp():
    W, H = 1000, 540
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(16, bold=True)
    ft_code  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "До OCP — switch-ланцюг вимагає зміни існуючого коду",
              font=ft_title, fill=RED, anchor="mm")

    bx, by, bw, bh = 60, 65, 420, 350
    rr(draw, [bx, by, bx+bw, by+bh], radius=10, fill=PANEL, outline=RED, width=2)
    draw.text((bx + bw//2, by + 22), "CostCalculator", font=ft_name, fill=RED, anchor="mm")
    hline(draw, bx+14, bx+bw-14, by+40, LINE)

    code_lines = [
        "Calculate(type, basePrice):",
        "  switch(type)",
        "  {",
        '    case "Standard":',
        "      return basePrice;",
        '    case "Urgent":',
        "      return basePrice * 1.5;",
        '    case "VIP":',
        "      return basePrice * 2.0;",
        "    // додати новий тип?",
        "    // ЗМІНИТИ цей метод!",
        "  }",
    ]
    for i, line in enumerate(code_lines):
        col = RED if "ЗМІНИТИ" in line else (YELLOW if "//" in line else MUTED)
        draw.text((bx + 18, by + 54 + i * 22), line, font=ft_code, fill=col)

    # Arrow: new type → triggers change in calculator
    ax, ay = bx + bw, by + bh//2
    arrow(draw, ax + 160, ay, ax + 10, ay, RED, head=8)
    draw.text((ax + 90, ay - 20), "Новий тип", font=ft_note, fill=YELLOW, anchor="mm")
    draw.text((ax + 90, ay + 8), "AppointmentType", font=ft_note, fill=YELLOW, anchor="mm")

    # Problem boxes
    problems = [
        (ax + 200, by + 60,  "Порушення OCP",    "Модифікуємо", "існуючий код"),
        (ax + 200, by + 160, "Ризик регресії",   "Кожна зміна", "зачіпає всіх"),
        (ax + 200, by + 260, "Немає розширення", "Новий тип =", "новий switch-case"),
    ]
    pw, ph = 190, 64
    for px, py, title, l1, l2 in problems:
        rr(draw, [px, py, px+pw, py+ph], radius=8, fill=PANEL, outline=RED, width=1)
        draw.text((px + pw//2, py + 14), title, font=load_font(13, bold=True), fill=RED, anchor="mm")
        draw.text((px + pw//2, py + 34), l1, font=ft_note, fill=MUTED, anchor="mm")
        draw.text((px + pw//2, py + 50), l2, font=ft_note, fill=MUTED, anchor="mm")

    draw.text((W//2, H - 22),
              "Будь-яке розширення вимагає модифікації класу — порушення принципу OCP",
              font=ft_note, fill=RED, anchor="mm")

    img.save(os.path.join(OUT_DIR, "before-ocp.png"))
    print("Saved before-ocp.png")


# ─── Diagram 2: After OCP ────────────────────────────────────────────
def make_after_ocp():
    W, H = 1100, 520
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(15, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "Після OCP — новий тип = новий клас, CostCalculator не чіпаємо",
              font=ft_title, fill=ACCENT, anchor="mm")

    # Interface
    ix, iy, iw, ih = 380, 70, 340, 90
    rr(draw, [ix, iy, ix+iw, iy+ih], radius=10, fill=PANEL, outline=ACCENT, width=2)
    draw.text((ix + iw//2, iy + 18), "<<interface>>", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((ix + iw//2, iy + 38), "IAppointmentType", font=ft_name, fill=ACCENT, anchor="mm")
    hline(draw, ix+14, ix+iw-14, iy+58, LINE)
    draw.text((ix + iw//2, iy + 72), "GetCost(basePrice): decimal", font=ft_meth, fill=MUTED, anchor="mm")

    # Concrete implementations
    impl_classes = [
        (60,  260, "StandardAppointment", MUTED,  ["GetCost(p) => p"]),
        (330, 260, "UrgentAppointment",   YELLOW, ["GetCost(p) => p * 1.5m"]),
        (600, 260, "VIPAppointment",      PURPLE, ["GetCost(p) => p * 2.0m"]),
        (870, 260, "NightShiftAppt",      BLUE,   ["GetCost(p) => p * 1.8m", "(новий тип!)"]),
    ]
    cw, ch = 200, 90
    for cx2, cy2, name, col, meths in impl_classes:
        rr(draw, [cx2, cy2, cx2+cw, cy2+ch], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((cx2 + cw//2, cy2 + 20), name, font=ft_name, fill=col, anchor="mm")
        hline(draw, cx2+12, cx2+cw-12, cy2+36, LINE)
        for j, m in enumerate(meths):
            draw.text((cx2 + cw//2, cy2 + 52 + j * 20), m, font=ft_meth, fill=MUTED, anchor="mm")
        arrow(draw, cx2 + cw//2, cy2, cx2 + cw//2, iy + ih + 4, MUTED, w=1, head=6)

    # CostCalculator
    ccx, ccy, ccw, cch = 380, 420, 340, 70
    rr(draw, [ccx, ccy, ccx+ccw, ccy+cch], radius=8, fill=PANEL, outline=ACCENT, width=2)
    draw.text((ccx + ccw//2, ccy + 20), "CostCalculator", font=ft_name, fill=ACCENT, anchor="mm")
    draw.text((ccx + ccw//2, ccy + 46), "Calculate(IAppointmentType t, decimal p)", font=ft_meth, fill=MUTED, anchor="mm")
    arrow(draw, ccx + ccw//2, ccy, ccx + ccw//2, iy + ih + 4, ACCENT, head=7)

    draw.text((W//2, H - 22),
              "Новий тип — новий клас. CostCalculator закритий для змін, відкритий для розширення",
              font=ft_note, fill=ACCENT, anchor="mm")

    img.save(os.path.join(OUT_DIR, "after-ocp.png"))
    print("Saved after-ocp.png")


if __name__ == "__main__":
    make_before_ocp()
    make_after_ocp()
    print("All diagrams done.")
