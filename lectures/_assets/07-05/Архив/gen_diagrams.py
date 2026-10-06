"""
Diagrams for section 7.5 — Generic Interfaces & Constraints
"""
from PIL import Image, ImageDraw, ImageFont
import os

BG = "#111413"; ACCENT = "#76c7ad"; MUTED = "#a1aaa6"
LINE = "#2c3531"; PANEL = "#191e1c"; RED = "#e07070"
YELLOW = "#d4b96a"; BLUE = "#6a9fd4"
OUT_DIR = os.path.dirname(__file__)

def load_font(size, bold=False):
    cands = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    bold_cands = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    for p in (bold_cands if bold else cands):
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def rr(draw, xy, radius=8, fill=PANEL, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def make_generic_constraint():
    W, H = 960, 400
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(17, bold=True)
    ft_name  = load_font(13, bold=True)
    ft_body  = load_font(12)
    ft_note  = load_font(11)

    draw.text((W // 2, 26), "Обмеження узагальнень: where T : IExaminable, IPrintable",
              font=ft_title, fill=ACCENT, anchor="mm")

    # ── Left column: candidate types ─────────────────────────────────────
    draw.text((160, 58), "Кандидати для T", font=ft_name, fill=MUTED, anchor="mm")

    candidates = [
        ("Doctor",         ACCENT, "[OK] IExaminable", "[OK] IPrintable"),
        ("Nurse",          YELLOW, "[OK] IExaminable", "[X]  IPrintable"),
        ("Administrator",  MUTED,  "[X]  IExaminable", "[X]  IPrintable"),
    ]
    bx, bw, bh = 20, 280, 80
    starts_y = [80, 180, 280]
    for (name, col, line1, line2), sy in zip(candidates, starts_y):
        rr(draw, [bx, sy, bx + bw, sy + bh], outline=col, fill=PANEL)
        draw.text((bx + bw // 2, sy + 18), name, font=ft_name, fill=col, anchor="mm")
        c1 = ACCENT if "[OK]" in line1 else RED
        c2 = ACCENT if "[OK]" in line2 else RED
        draw.text((bx + 14, sy + 36), line1, font=ft_body, fill=c1)
        draw.text((bx + 14, sy + 54), line2, font=ft_body, fill=c2)

    # ── Center: filter block ──────────────────────────────────────────────
    fx, fy, fw, fh = 330, 95, 280, 200
    rr(draw, [fx, fy, fx + fw, fy + fh], radius=10, outline=BLUE, fill="#101820", width=2)
    draw.text((fx + fw // 2, fy + 22), "Обмеження", font=ft_name, fill=BLUE, anchor="mm")
    draw.line([(fx + 14, fy + 38), (fx + fw - 14, fy + 38)], fill=LINE, width=1)
    constraint_lines = [
        "where T :",
        "  IExaminable,",
        "  IPrintable",
    ]
    for i, ln in enumerate(constraint_lines):
        draw.text((fx + 20, fy + 50 + i * 22), ln, font=load_font(13, bold=True), fill=BLUE)
    draw.text((fx + fw // 2, fy + 136), "Тип T повинен", font=ft_note, fill=MUTED, anchor="mm")
    draw.text((fx + fw // 2, fy + 154), "реалізувати обидва", font=ft_note, fill=MUTED, anchor="mm")
    draw.text((fx + fw // 2, fy + 172), "інтерфейси", font=ft_note, fill=MUTED, anchor="mm")

    # Arrows from candidates to filter
    for sy in starts_y:
        mid_y = sy + 40
        draw.line([(bx + bw, mid_y), (fx, fy + fh // 2)], fill=LINE, width=1)

    # ── Right column: results ─────────────────────────────────────────────
    draw.text((790, 58), "Результат", font=ft_name, fill=MUTED, anchor="mm")

    results = [
        ("ClinicReporter<Doctor>",        ACCENT, "[OK] допустимий"),
        ("ClinicReporter<Nurse>",         RED,    "[X]  помилка компіляції"),
        ("ClinicReporter<Administrator>", RED,    "[X]  помилка компіляції"),
    ]
    rx, rw, rh = 640, 300, 78
    for (label, col, verdict), sy in zip(results, starts_y):
        rr(draw, [rx, sy, rx + rw, sy + rh], outline=col, fill=PANEL)
        draw.text((rx + rw // 2, sy + 20), label, font=ft_body, fill=col, anchor="mm")
        draw.text((rx + rw // 2, sy + 50), verdict, font=ft_name, fill=col, anchor="mm")
        # Arrow from filter
        draw.line([(fx + fw, fy + fh // 2), (rx, sy + rh // 2)], fill=LINE, width=1)

    draw.text((W // 2, H - 16),
              "Компілятор перевіряє обмеження під час збірки — помилка виникає до запуску програми",
              font=ft_note, fill=MUTED, anchor="mm")

    img.save(os.path.join(OUT_DIR, "generic-constraint.png"))
    print("Saved generic-constraint.png")

if __name__ == "__main__":
    make_generic_constraint()
    print("Done.")
