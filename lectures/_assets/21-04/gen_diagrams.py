"""
Diagrams for section 21.4 — Options Pattern
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


def make_options_pattern():
    W, H = 1200, 600
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(14, bold=True)
    ft_meth  = load_font(12)
    ft_note  = load_font(12)

    draw.text((W//2, 28), "Options Pattern — IOptions, IOptionsSnapshot, IOptionsMonitor",
              font=ft_title, fill=ACCENT, anchor="mm")

    # ── Config sources (left column) ─────────────────────────────────
    draw.text((120, 62), "Джерела конфігурації", font=ft_name, fill=MUTED, anchor="mm")
    sources = [
        (20,  90,  "appsettings.json",        MUTED),
        (20, 160,  "appsettings.Prod.json",   MUTED),
        (20, 230,  "Змінні середовища",        BLUE),
        (20, 300,  "Аргументи CMD",            BLUE),
        (20, 370,  "User Secrets",             YELLOW),
    ]
    sw, sh = 220, 52
    for sx, sy, label, col in sources:
        rr(draw, [sx, sy, sx+sw, sy+sh], radius=6, fill=PANEL, outline=col, width=1)
        draw.text((sx + sw//2, sy + sh//2), label, font=ft_note, fill=col, anchor="mm")

    # Arrow to IConfiguration
    icx, icy = 290, 235
    for sx, sy, _, col in sources:
        draw.line([(sx+sw, sy+sh//2), (icx, icy+30)], fill=LINE, width=1)

    # ── IConfiguration (center-left) ─────────────────────────────────
    icw, ich = 200, 60
    rr(draw, [icx, icy, icx+icw, icy+ich], radius=8, fill=PANEL, outline=MUTED, width=2)
    draw.text((icx + icw//2, icy + 20), "IConfiguration", font=ft_name, fill=MUTED, anchor="mm")
    draw.text((icx + icw//2, icy + 42), "GetSection(\"..\")", font=ft_meth, fill=MUTED, anchor="mm")

    # Arrow to Options binder
    obx, oby = 540, 215
    arrow(draw, icx + icw, icy + ich//2, obx, oby + 30, LINE, w=1, head=6)

    # ── Options binder ────────────────────────────────────────────────
    obw, obh = 220, 60
    rr(draw, [obx, oby, obx+obw, oby+obh], radius=8, fill=PANEL, outline=ACCENT, width=2)
    draw.text((obx + obw//2, oby + 20), "Configure<T>()", font=ft_name, fill=ACCENT, anchor="mm")
    draw.text((obx + obw//2, oby + 42), "Bind + Validate", font=ft_meth, fill=MUTED, anchor="mm")

    # ── Three IOptions variants ───────────────────────────────────────
    variants = [
        (800,  90, "IOptions<T>",          ACCENT,
         ["Singleton", "Зчитується один раз", "Не оновлюється", "[OK] Статична конфігурація"]),
        (800, 240, "IOptionsSnapshot<T>",  YELLOW,
         ["Scoped", "Нове значення на запит", "Hot reload per request", "[OK] Entity Framework opts"]),
        (800, 390, "IOptionsMonitor<T>",   PURPLE,
         ["Singleton", "Реактивне оновлення", "OnChange(callback)", "[OK] Hot reload фонових сервісів"]),
    ]
    vw, vh = 360, 130
    for vx, vy, name, col, items in variants:
        rr(draw, [vx, vy, vx+vw, vy+vh], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((vx + vw//2, vy + 18), name, font=ft_name, fill=col, anchor="mm")
        hline(draw, vx+12, vx+vw-12, vy+34, LINE)
        for i, item in enumerate(items):
            mcol = ACCENT if "[OK]" in item else MUTED
            draw.text((vx + 18, vy + 46 + i * 20), item, font=ft_note, fill=mcol)
        arrow(draw, obx + obw, oby + obh//2, vx, vy + vh//2, col, w=1, head=6)

    # ── Consumer class ────────────────────────────────────────────────
    cx2, cy2, cw2, ch2 = 290, 420, 440, 120
    rr(draw, [cx2, cy2, cx2+cw2, cy2+ch2], radius=8, fill=PANEL, outline=BLUE, width=2)
    draw.text((cx2 + cw2//2, cy2 + 18), "Клас-споживач (через конструктор DI)", font=ft_name, fill=BLUE, anchor="mm")
    hline(draw, cx2+12, cx2+cw2-12, cy2+34, LINE)
    consumer_lines = [
        "class AppointmentService",
        "{",
        "  private readonly AppointmentOptions _opts;",
        "  public AppointmentService(IOptions<AppointmentOptions> opts)",
        "    => _opts = opts.Value;  // типізовано, без magic strings",
        "}",
    ]
    for i, line in enumerate(consumer_lines):
        col = MUTED if not line.strip().startswith("class") else BLUE
        draw.text((cx2 + 14, cy2 + 44 + i * 14), line, font=load_font(11), fill=col)

    draw.text((W//2, H - 14),
              "Configure<T>() один раз — сервіс отримує типізований об'єкт без IConfiguration",
              font=ft_note, fill=ACCENT, anchor="mm")

    img.save(os.path.join(OUT_DIR, "options-pattern.png"))
    print("Saved options-pattern.png")


if __name__ == "__main__":
    make_options_pattern()
    print("All diagrams done.")
