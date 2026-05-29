"""
Diagrams for section 21.1 — Generic Host
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


def make_host_architecture():
    W, H = 1200, 620
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(15, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(12)

    draw.text((W//2, 28), "Generic Host — архітектура та потік запуску",
              font=ft_title, fill=ACCENT, anchor="mm")

    # ── Central IHost box ────────────────────────────────────────────
    hx, hy, hw, hh = 380, 65, 440, 80
    rr(draw, [hx, hy, hx+hw, hy+hh], radius=12, fill=PANEL, outline=ACCENT, width=3)
    draw.text((hx + hw//2, hy + 22), "IHost", font=load_font(18, bold=True), fill=ACCENT, anchor="mm")
    draw.text((hx + hw//2, hy + 50), "Start()  /  RunAsync()  /  StopAsync()",
              font=ft_meth, fill=MUTED, anchor="mm")

    # ── Three pillars ─────────────────────────────────────────────────
    pillars = [
        (60,  190, 300, 180, "IServiceProvider", BLUE,
         ["DI-контейнер", "Реєстрація сервісів", "Resolve залежностей", "Управління lifetime"]),
        (450, 190, 300, 180, "IConfiguration", YELLOW,
         ["appsettings.json", "Змінні середовища", "Аргументи cmd", "User Secrets"]),
        (840, 190, 300, 180, "Lifecycle Manager", PURPLE,
         ["IHostedService start", "CancellationToken", "Shutdown (зворотн.)", "IHostApplicationLifetime"]),
    ]

    for bx, by, bw, bh, title, col, items in pillars:
        rr(draw, [bx, by, bx+bw, by+bh], radius=10, fill=PANEL, outline=col, width=2)
        draw.text((bx + bw//2, by + 20), title, font=ft_name, fill=col, anchor="mm")
        hline(draw, bx+14, bx+bw-14, by+36, LINE)
        for i, item in enumerate(items):
            draw.text((bx + bw//2, by + 52 + i * 28), item, font=ft_meth, fill=MUTED, anchor="mm")
        # Arrow from IHost down to pillar
        arrow(draw, hx + hw//2, hy + hh, bx + bw//2, by, LINE, w=1, head=6)

    # ── IHostedServices row ──────────────────────────────────────────
    svc_y = 440
    draw.text((W//2, svc_y - 20), "IHostedService  (фонові сервіси)",
              font=ft_name, fill=MUTED, anchor="mm")

    svcs = [
        (60,  svc_y, "AppointmentReminder",  ACCENT, "каждні 24год"),
        (340, svc_y, "DatabaseMigrator",     BLUE,   "одноразово при старті"),
        (620, svc_y, "ReportScheduler",      YELLOW, "щодня о 23:00"),
        (900, svc_y, "HealthCheckService",   PURPLE, "кожні 30с"),
    ]
    sw, sh = 240, 70
    for sx, sy, name, col, note in svcs:
        rr(draw, [sx, sy, sx+sw, sy+sh], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((sx + sw//2, sy + 22), name, font=ft_meth, fill=col, anchor="mm")
        draw.text((sx + sw//2, sy + 48), note, font=ft_note, fill=MUTED, anchor="mm")

    # Arrow from Lifecycle Manager to services
    arrow(draw, 840 + 150, 190 + 180, W//2, svc_y, PURPLE, w=1, head=6)

    # ── Startup sequence ─────────────────────────────────────────────
    seq_y = H - 80
    steps = [
        (80,  "1. IHostBuilder\n.Build()",      ACCENT),
        (280, "2. ConfigureServices\n(DI setup)",BLUE),
        (480, "3. IHost.StartAsync\n(hosted svcs)", YELLOW),
        (680, "4. RunAsync\n(чекаємо сигнал)",  MUTED),
        (880, "5. StopAsync\n(shutdown reverse)", PURPLE),
    ]
    for sx, label, col in steps:
        rr(draw, [sx, seq_y, sx+160, seq_y+60], radius=8, fill=PANEL, outline=col, width=1)
        for j, line in enumerate(label.split("\n")):
            draw.text((sx + 80, seq_y + 16 + j * 20), line, font=ft_note, fill=col, anchor="mm")
        if sx < 880:
            draw.line([(sx + 160, seq_y + 30), (sx + 170, seq_y + 30)], fill=LINE, width=1)
            draw.polygon([(sx+170, seq_y+26), (sx+170, seq_y+34), (sx+178, seq_y+30)], fill=LINE)

    img.save(os.path.join(OUT_DIR, "host-architecture.png"))
    print("Saved host-architecture.png")


if __name__ == "__main__":
    make_host_architecture()
    print("All diagrams done.")
