"""
Diagrams for section 21.2 — IServiceCollection
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


def make_service_registration():
    W, H = 1200, 580
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(14, bold=True)
    ft_meth  = load_font(12)
    ft_note  = load_font(12)

    draw.text((W//2, 28), "Реєстрація та розпізнавання сервісів у IServiceCollection",
              font=ft_title, fill=ACCENT, anchor="mm")

    # ── Phase 1: IServiceCollection (Registration) ────────────────────
    draw.text((240, 65), "Фаза 1: Реєстрація", font=load_font(15, bold=True), fill=ACCENT, anchor="mm")

    col_box = [
        (30,  90, "ServiceDescriptor", ACCENT,
         ["ServiceType: IPatientRepository", "ImplType: SqlPatientRepository", "Lifetime: Singleton"]),
        (30, 220, "ServiceDescriptor", BLUE,
         ["ServiceType: AppointmentService", "ImplType: AppointmentService", "Lifetime: Scoped"]),
        (30, 350, "ServiceDescriptor", YELLOW,
         ["ServiceType: INotificationService", "Factory: provider => ...", "Lifetime: Transient"]),
    ]
    dw, dh = 390, 100
    for bx, by, title, col, lines in col_box:
        rr(draw, [bx, by, bx+dw, by+dh], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((bx + dw//2, by + 18), title, font=ft_name, fill=col, anchor="mm")
        hline(draw, bx+12, bx+dw-12, by+34, LINE)
        for i, line in enumerate(lines):
            draw.text((bx + 18, by + 46 + i * 20), line, font=ft_note, fill=MUTED)

    # IServiceCollection bracket
    rr(draw, [20, 80, 430, 465], radius=12, fill=None, outline=ACCENT, width=1)
    draw.text((225, 480), "IServiceCollection", font=ft_name, fill=ACCENT, anchor="mm")

    # ── Arrow: Build ──────────────────────────────────────────────────
    bx2 = 480
    draw.line([(440, 270), (540, 270)], fill=ACCENT, width=2)
    draw.polygon([(536, 264), (536, 276), (546, 270)], fill=ACCENT)
    draw.text((490, 248), ".Build()", font=load_font(14, bold=True), fill=ACCENT, anchor="mm")
    draw.text((490, 294), "(незмінний", font=ft_note, fill=MUTED, anchor="mm")
    draw.text((490, 310), "після Build)", font=ft_note, fill=MUTED, anchor="mm")

    # ── Phase 2: IServiceProvider (Resolution) ────────────────────────
    draw.text((870, 65), "Фаза 2: Розпізнавання", font=load_font(15, bold=True), fill=BLUE, anchor="mm")

    # ServiceProvider box
    spx, spy, spw, sph = 560, 90, 320, 100
    rr(draw, [spx, spy, spx+spw, spy+sph], radius=10, fill=PANEL, outline=BLUE, width=2)
    draw.text((spx + spw//2, spy + 22), "IServiceProvider", font=ft_name, fill=BLUE, anchor="mm")
    hline(draw, spx+14, spx+spw-14, spy+40, LINE)
    draw.text((spx + spw//2, spy + 56), "GetService<T>()", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((spx + spw//2, spy + 76), "GetRequiredService<T>()", font=ft_meth, fill=MUTED, anchor="mm")

    # Resolution results
    results = [
        (900, 90,  "IPatientRepository",  ACCENT, "Singleton: завжди 1 екз."),
        (900, 220, "AppointmentService",  BLUE,   "Scoped: 1 на запит"),
        (900, 350, "INotificationService",YELLOW, "Transient: новий щоразу"),
    ]
    rw, rh = 270, 80
    for rx, ry, name, col, note in results:
        rr(draw, [rx, ry, rx+rw, ry+rh], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((rx + rw//2, ry + 22), name, font=ft_name, fill=col, anchor="mm")
        draw.text((rx + rw//2, ry + 52), note, font=ft_note, fill=MUTED, anchor="mm")
        arrow(draw, spx + spw, spy + sph//2, rx, ry + rh//2, col, w=1, head=6)

    # ── ServiceDescriptor structure ───────────────────────────────────
    sx, sy = 560, 260
    rr(draw, [sx, sy, sx+300, sy+160], radius=8, fill=PANEL, outline=MUTED, width=1)
    draw.text((sx + 150, sy + 18), "ServiceDescriptor", font=ft_name, fill=MUTED, anchor="mm")
    hline(draw, sx+12, sx+288, sy+34, LINE)
    fields = [
        ("ServiceType",    "IPatientRepository",    ACCENT),
        ("ImplType",       "SqlPatientRepository",  ACCENT),
        ("Factory",        "null | Func<...>",      MUTED),
        ("Instance",       "null | object",         MUTED),
        ("Lifetime",       "Singleton",             YELLOW),
    ]
    for i, (name, val, col) in enumerate(fields):
        draw.text((sx + 18, sy + 46 + i * 22), f"{name}:", font=ft_note, fill=MUTED)
        draw.text((sx + 130, sy + 46 + i * 22), val, font=ft_note, fill=col)

    draw.text((W//2, H - 22),
              "Реєстрація → Build → Розпізнавання: контейнер незмінний пiсля Build",
              font=ft_note, fill=ACCENT, anchor="mm")

    img.save(os.path.join(OUT_DIR, "service-registration.png"))
    print("Saved service-registration.png")


if __name__ == "__main__":
    make_service_registration()
    print("All diagrams done.")
