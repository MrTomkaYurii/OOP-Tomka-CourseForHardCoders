"""
Diagrams for section 7.6 — ICloneable: shallow vs deep copy
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

def arrow_h(draw, x1, x2, y, col=MUTED, w=1):
    draw.line([(x1, y), (x2, y)], fill=col, width=w)
    dx = 1 if x2 > x1 else -1
    draw.polygon([(x2, y), (x2 - dx * 8, y - 4), (x2 - dx * 8, y + 4)], fill=col)

def make_shallow_deep_copy():
    W, H = 1040, 460
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(17, bold=True)
    ft_sub   = load_font(13, bold=True)
    ft_body  = load_font(12)
    ft_note  = load_font(11)
    ft_small = load_font(10)

    draw.text((W // 2, 26), "Поверхневе та глибоке копіювання об'єктів",
              font=ft_title, fill=ACCENT, anchor="mm")

    # Divider
    draw.line([(W // 2, 50), (W // 2, H - 30)], fill=LINE, width=1)

    # ── LEFT: Shallow copy ────────────────────────────────────────────────
    draw.text((W // 4, 55), "Поверхневе (MemberwiseClone)", font=ft_sub, fill=YELLOW, anchor="mm")

    # Stack variables
    sx, sy = 30, 90
    for i, (var, name) in enumerate([("patient1", "Петренко"), ("patient2", "Іваненко")]):
        vy = sy + i * 100
        rr(draw, [sx, vy, sx + 110, vy + 36], outline=MUTED, fill=PANEL)
        draw.text((sx + 55, vy + 18), var, font=ft_body, fill=MUTED, anchor="mm")

    # Heap Patient objects
    hx, hy = 175, 85
    for i, (var, name) in enumerate([("patient1", "Петренко"), ("patient2", "Іваненко")]):
        vy = hy + i * 100
        rr(draw, [hx, vy, hx + 170, vy + 50], outline=YELLOW, fill=PANEL)
        draw.text((hx + 85, vy + 14), f"Patient", font=ft_body, fill=YELLOW, anchor="mm")
        draw.text((hx + 85, vy + 34), f"Name={name}", font=ft_small, fill=MUTED, anchor="mm")
        # Arrow from stack to heap
        arrow_h(draw, sx + 110, hx, sy + i * 100 + 18, MUTED)

    # Shared Diagnosis object — in the middle below both
    dx_shallow, dy_shallow = 175, 280
    rr(draw, [dx_shallow, dy_shallow, dx_shallow + 170, dy_shallow + 54], outline=RED, fill="#1f1010")
    draw.text((dx_shallow + 85, dy_shallow + 16), "Diagnosis", font=ft_body, fill=RED, anchor="mm")
    draw.text((dx_shallow + 85, dy_shallow + 36), "Code=\"J18.0\"", font=ft_small, fill=MUTED, anchor="mm")

    # Arrows from both Patient objects to same Diagnosis
    for i in range(2):
        py = hy + i * 100 + 48
        draw.line([(hx + 85, py), (dx_shallow + 85, dy_shallow)], fill=RED, width=1)

    draw.text((dx_shallow + 85, dy_shallow + 72),
              "[!] спільний об'єкт — зміна у patient2",
              font=ft_note, fill=RED, anchor="mm")
    draw.text((dx_shallow + 85, dy_shallow + 88),
              "позначиться на patient1!",
              font=ft_note, fill=RED, anchor="mm")

    # ── RIGHT: Deep copy ──────────────────────────────────────────────────
    mid = W // 2
    draw.text((mid + W // 4, 55), "Глибоке (явне копіювання)", font=ft_sub, fill=ACCENT, anchor="mm")

    # Stack
    for i, var in enumerate(["patient1", "patient2"]):
        vy = sy + i * 100
        rr(draw, [mid + 30, vy, mid + 140, vy + 36], outline=MUTED, fill=PANEL)
        draw.text((mid + 85, vy + 18), var, font=ft_body, fill=MUTED, anchor="mm")

    # Heap Patient objects (right side)
    rhx = mid + 175
    for i, (var, name) in enumerate([("patient1", "Петренко"), ("patient2", "Іваненко")]):
        vy = hy + i * 100
        rr(draw, [rhx, vy, rhx + 170, vy + 50], outline=ACCENT, fill=PANEL)
        draw.text((rhx + 85, vy + 14), "Patient", font=ft_body, fill=ACCENT, anchor="mm")
        draw.text((rhx + 85, vy + 34), f"Name={name}", font=ft_small, fill=MUTED, anchor="mm")
        arrow_h(draw, mid + 140, rhx, sy + i * 100 + 18, MUTED)

        # Each has OWN Diagnosis
        ddx, ddy = rhx, vy + 58
        rr(draw, [ddx, ddy, ddx + 170, ddy + 40], outline=ACCENT, fill=PANEL)
        draw.text((ddx + 85, ddy + 12), "Diagnosis", font=ft_body, fill=ACCENT, anchor="mm")
        draw.text((ddx + 85, ddy + 28), "Code=\"J18.0\"", font=ft_small, fill=MUTED, anchor="mm")
        draw.line([(rhx + 85, vy + 50), (ddx + 85, ddy)], fill=ACCENT, width=1)

    draw.text((mid + W // 4, 370),
              "[OK] кожен пацієнт має власну копію Diagnosis",
              font=ft_note, fill=ACCENT, anchor="mm")
    draw.text((mid + W // 4, 388),
              "зміни в одному не торкаються іншого",
              font=ft_note, fill=MUTED, anchor="mm")

    draw.text((W // 2, H - 14),
              "Глибоке копіювання: Clone() вручну створює нові об'єкти для всіх полів-посилань",
              font=ft_note, fill=MUTED, anchor="mm")

    img.save(os.path.join(OUT_DIR, "shallow-deep-copy.png"))
    print("Saved shallow-deep-copy.png")

if __name__ == "__main__":
    make_shallow_deep_copy()
    print("Done.")
