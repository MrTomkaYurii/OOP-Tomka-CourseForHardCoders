"""
Diagrams for section 20.6 — DIP
Palette: BG=#111413, ACCENT=#76c7ad, TEXT=#e5e9e7, MUTED=#a1aaa6, LINE=#2c3531, PANEL=#191e1c
Notes: Use [OK] / [X] — Unicode check/cross marks not supported in Segoe UI
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


# ─── Diagram: DIP Overview ───────────────────────────────────────────
def make_dip_overview():
    W, H = 1100, 560
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(15, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "DIP — інверсія напряму залежностей через абстракцію",
              font=ft_title, fill=ACCENT, anchor="mm")

    # ── Left: WITHOUT DIP ──────────────────────────────────────────
    draw.text((200, 68), "БЕЗ DIP", font=load_font(15, bold=True), fill=RED, anchor="mm")

    rr(draw, [30, 90, 370, 160], radius=8, fill=PANEL, outline=YELLOW, width=2)
    draw.text((200, 117), "AppointmentService", font=ft_name, fill=YELLOW, anchor="mm")
    draw.text((200, 143), "(high-level module)", font=ft_meth, fill=MUTED, anchor="mm")

    rr(draw, [30, 230, 370, 300], radius=8, fill=PANEL, outline=RED, width=2)
    draw.text((200, 257), "SqlAppointmentRepository", font=ft_name, fill=RED, anchor="mm")
    draw.text((200, 280), "(concrete class, low-level)", font=ft_meth, fill=MUTED, anchor="mm")

    arrow(draw, 200, 160, 200, 230, RED, w=2, head=8)
    draw.text((248, 196), "залежить від", font=ft_note, fill=RED)
    draw.text((248, 212), "конкретного класу", font=ft_note, fill=RED)

    rr(draw, [30, 330, 370, 380], radius=6, fill=PANEL, outline=RED, width=1)
    draw.text((200, 345), "[X] Замінити SQL на Mongo?", font=ft_note, fill=RED, anchor="mm")
    draw.text((200, 365), "      Треба міняти Service!", font=ft_note, fill=RED, anchor="mm")

    # ── Divider ────────────────────────────────────────────────────
    draw.line([(W//2, 60), (W//2, H - 30)], fill=LINE, width=1)

    # ── Right: WITH DIP ───────────────────────────────────────────
    draw.text((880, 68), "З DIP", font=load_font(15, bold=True), fill=ACCENT, anchor="mm")

    rr(draw, [600, 90, 1060, 160], radius=8, fill=PANEL, outline=YELLOW, width=2)
    draw.text((830, 117), "AppointmentService", font=ft_name, fill=YELLOW, anchor="mm")
    draw.text((830, 143), "залежить від IAppointmentRepository", font=ft_meth, fill=MUTED, anchor="mm")

    rr(draw, [650, 230, 1010, 300], radius=8, fill=PANEL, outline=ACCENT, width=2)
    draw.text((830, 248), "<<interface>>", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((830, 272), "IAppointmentRepository", font=ft_name, fill=ACCENT, anchor="mm")

    arrow(draw, 830, 160, 830, 230, ACCENT, w=2, head=8)
    draw.text((840, 190), "залежить від абстракції", font=ft_note, fill=ACCENT)

    # Concrete implementations
    rr(draw, [600, 360, 790, 430], radius=8, fill=PANEL, outline=BLUE, width=2)
    draw.text((695, 395), "SqlRepository", font=ft_name, fill=BLUE, anchor="mm")
    arrow(draw, 695, 360, 780, 300, MUTED, head=5)

    rr(draw, [820, 360, 1010, 430], radius=8, fill=PANEL, outline=YELLOW, width=2)
    draw.text((915, 395), "MongoRepository", font=ft_name, fill=YELLOW, anchor="mm")
    arrow(draw, 915, 360, 880, 300, MUTED, head=5)

    rr(draw, [610, 460, 1050, 510], radius=6, fill=PANEL, outline=ACCENT, width=1)
    draw.text((830, 478), "[OK] Замінити SQL на Mongo?", font=ft_note, fill=ACCENT, anchor="mm")
    draw.text((830, 498), "      Тільки новий клас, Service не чіпаємо!", font=ft_note, fill=ACCENT, anchor="mm")

    draw.text((W//2, H - 18),
              "Високорівневі модулі залежать від абстракцій — конкретика підставляється ззовні",
              font=ft_note, fill=ACCENT, anchor="mm")

    img.save(os.path.join(OUT_DIR, "dip-overview.png"))
    print("Saved dip-overview.png")


if __name__ == "__main__":
    make_dip_overview()
    print("All diagrams done.")
