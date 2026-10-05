"""
Diagrams for section 21.3 — Service Lifetimes
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


def make_service_lifetimes():
    W, H = 1200, 600
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(16, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(12)
    ft_small = load_font(11)

    draw.text((W//2, 28), "Часи життя сервісів: Singleton, Scoped, Transient",
              font=ft_title, fill=ACCENT, anchor="mm")

    # ── Timeline axis ─────────────────────────────────────────────────
    ax_y = 90
    draw.text((W//2, ax_y), "Час роботи додатку →", font=ft_note, fill=MUTED, anchor="mm")
    draw.line([(30, ax_y + 20), (W - 30, ax_y + 20)], fill=LINE, width=2)

    # Request markers
    req_x = [180, 420, 660, 900]
    req_w = 220
    for i, rx in enumerate(req_x):
        draw.rectangle([rx, ax_y+10, rx+req_w, ax_y+30], outline=LINE, fill="#161b19")
        draw.text((rx + req_w//2, ax_y + 20), f"Запит {i+1}",
                  font=ft_small, fill=MUTED, anchor="mm")

    # ── SINGLETON row ─────────────────────────────────────────────────
    row1_y = 145
    draw.text((80, row1_y + 30), "Singleton", font=ft_name, fill=ACCENT, anchor="mm")
    draw.text((80, row1_y + 52), "(1 екз.)", font=ft_note, fill=MUTED, anchor="mm")
    # One long bar across entire timeline
    rr(draw, [180, row1_y + 10, W - 30, row1_y + 60], radius=6, fill="#1a2e28", outline=ACCENT, width=2)
    draw.text(((180 + W - 30)//2, row1_y + 35), "AppConfiguration  [InstanceId=1]",
              font=ft_meth, fill=ACCENT, anchor="mm")

    # ── SCOPED row ────────────────────────────────────────────────────
    row2_y = 245
    draw.text((80, row2_y + 30), "Scoped", font=ft_name, fill=YELLOW, anchor="mm")
    draw.text((80, row2_y + 52), "(1 на scope)", font=ft_note, fill=MUTED, anchor="mm")
    # One bar per request
    for i, rx in enumerate(req_x):
        rr(draw, [rx + 4, row2_y + 10, rx + req_w - 4, row2_y + 60],
           radius=6, fill="#2a2510", outline=YELLOW, width=2)
        draw.text((rx + req_w//2, row2_y + 35), f"ClinicUnitOfWork [#{i+1}]",
                  font=ft_note, fill=YELLOW, anchor="mm")

    # ── TRANSIENT row ─────────────────────────────────────────────────
    row3_y = 345
    draw.text((80, row3_y + 30), "Transient", font=ft_name, fill=BLUE, anchor="mm")
    draw.text((80, row3_y + 52), "(новий щоразу)", font=ft_note, fill=MUTED, anchor="mm")
    # Multiple small bars per request (2 per request)
    inst_id = 1
    for i, rx in enumerate(req_x):
        for j in range(2):
            bx = rx + 4 + j * (req_w // 2 - 2)
            bw2 = req_w // 2 - 6
            rr(draw, [bx, row3_y + 10, bx + bw2, row3_y + 60],
               radius=4, fill="#101828", outline=BLUE, width=2)
            draw.text((bx + bw2//2, row3_y + 35), f"#{inst_id}",
                      font=ft_note, fill=BLUE, anchor="mm")
            inst_id += 1

    # ── Captive dependency warning ────────────────────────────────────
    warn_y = 460
    rr(draw, [30, warn_y, W - 30, warn_y + 100], radius=8, fill=PANEL, outline=RED, width=2)
    draw.text((W//2, warn_y + 18), "Captive Dependency — ЗАБОРОНЕНI комбінації",
              font=load_font(14, bold=True), fill=RED, anchor="mm")
    hline(draw, 44, W-44, warn_y + 34, RED)

    combos = [
        (80,  warn_y + 50, "Singleton", "→", "Scoped",    "[X] Scoped буде «захоплено» — не знищиться після запиту"),
        (80,  warn_y + 76, "Singleton", "→", "Transient", "[!] Transient стане фактичним Singleton — витік"),
    ]
    for cx, cy, from_lt, arrow_s, to_lt, note in combos:
        draw.text((cx,       cy), from_lt, font=ft_meth, fill=ACCENT)
        draw.text((cx + 85,  cy), arrow_s, font=ft_meth, fill=RED)
        draw.text((cx + 105, cy), to_lt,   font=ft_meth, fill=YELLOW)
        draw.text((cx + 195, cy), note,    font=ft_small, fill=RED)

    draw.text((W//2, H - 14),
              "Правило: час залежності не коротший за час того, хто залежить",
              font=ft_note, fill=ACCENT, anchor="mm")

    img.save(os.path.join(OUT_DIR, "service-lifetimes.png"))
    print("Saved service-lifetimes.png")


if __name__ == "__main__":
    make_service_lifetimes()
    print("All diagrams done.")
