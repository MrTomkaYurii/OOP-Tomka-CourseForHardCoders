"""
Diagrams for section 7.7 — Covariance and Contravariance
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

BG = "#111413"; ACCENT = "#76c7ad"; MUTED = "#a1aaa6"
LINE = "#2c3531"; PANEL = "#191e1c"; RED = "#e07070"
YELLOW = "#d4b96a"; BLUE = "#6a9fd4"; PURPLE = "#c47ab8"
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

def arrow_left(draw, x1, x2, y, col, w=2, head=8):
    """Arrow pointing LEFT (x1 > x2)."""
    draw.line([(x1, y), (x2, y)], fill=col, width=w)
    draw.polygon([(x2, y), (x2 + head + 2, y - head // 2), (x2 + head + 2, y + head // 2)], fill=col)

def arrow_right(draw, x1, x2, y, col, w=2, head=8):
    """Arrow pointing RIGHT (x2 > x1)."""
    draw.line([(x1, y), (x2, y)], fill=col, width=w)
    draw.polygon([(x2, y), (x2 - head - 2, y - head // 2), (x2 - head - 2, y + head // 2)], fill=col)

def make_variance_directions():
    W, H = 1020, 530
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(17, bold=True)
    ft_sub   = load_font(13, bold=True)
    ft_body  = load_font(12)
    ft_note  = load_font(11)
    ft_code  = load_font(11)

    draw.text((W // 2, 26), "Коваріантність та контраваріантність узагальнених інтерфейсів",
              font=ft_title, fill=ACCENT, anchor="mm")

    BW, BH = 220, 50  # box width/height
    LX = 100          # left box x
    RX = W - BW - 100 # right box x
    MID_X = W // 2   # mid arrow x

    rows = [
        # (y, label, left_title, left_col, right_title, right_col, arrow_dir, arrow_col, note)
        (70,
         "Ієрархія класів",
         "Doctor", MUTED,
         "Cardiologist : Doctor", BLUE,
         "left",   MUTED,
         "Cardiologist успадковує Doctor (більш конкретний)"),
        (190,
         "Коваріантність  (out T)",
         "IFactory<Doctor>", ACCENT,
         "IFactory<Cardiologist>", YELLOW,
         "left",  YELLOW,
         "IFactory<Cardiologist> можна присвоїти до IFactory<Doctor>  (той самий напрям)"),
        (310,
         "Контраваріантність  (in T)",
         "IHandler<Doctor>", PURPLE,
         "IHandler<Cardiologist>", ACCENT,
         "right", PURPLE,
         "IHandler<Doctor> можна присвоїти до IHandler<Cardiologist>  (зворотний напрям)"),
        (430,
         "Інваріантність  (без ключового слова)",
         "IRepo<Doctor>", RED,
         "IRepo<Cardiologist>", RED,
         "none",  RED,
         "Присвоєння в будь-який бік заборонено — типи несумісні"),
    ]

    for y, label, lt, lc, rt, rc, adir, acol, note in rows:
        # Section label
        draw.text((W // 2, y + 4), label, font=ft_sub, fill=acol, anchor="mm")

        # Left box
        rr(draw, [LX, y + 18, LX + BW, y + 18 + BH], outline=lc, fill=PANEL)
        draw.text((LX + BW // 2, y + 18 + BH // 2), lt, font=ft_body, fill=lc, anchor="mm")

        # Right box
        rr(draw, [RX, y + 18, RX + BW, y + 18 + BH], outline=rc, fill=PANEL)
        draw.text((RX + BW // 2, y + 18 + BH // 2), rt, font=ft_body, fill=rc, anchor="mm")

        # Arrow
        ay = y + 18 + BH // 2
        ax1 = LX + BW + 10
        ax2 = RX - 10
        if adir == "left":
            arrow_left(draw, ax2, ax1, ay, acol, w=2)
        elif adir == "right":
            arrow_right(draw, ax1, ax2, ay, acol, w=2)
        else:  # none — double X
            mid = (ax1 + ax2) // 2
            draw.line([(ax1, ay), (ax2, ay)], fill=RED, width=1)
            draw.text((mid, ay - 2), "[X]", font=ft_sub, fill=RED, anchor="mm")

        # Note below arrow
        draw.text((W // 2, y + 18 + BH + 8), note, font=ft_note, fill=MUTED, anchor="mm")

    # Bottom legend
    ly = H - 28
    draw.line([(30, ly - 6), (W - 30, ly - 6)], fill=LINE, width=1)
    draw.text((W // 2, ly + 8),
              "out = тип лише повертається з методу  |  in = тип лише передається до методу",
              font=ft_note, fill=MUTED, anchor="mm")

    img.save(os.path.join(OUT_DIR, "variance-directions.png"))
    print("Saved variance-directions.png")

if __name__ == "__main__":
    make_variance_directions()
    print("Done.")
