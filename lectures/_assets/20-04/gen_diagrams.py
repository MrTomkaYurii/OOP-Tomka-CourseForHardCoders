"""
Diagrams for section 20.4 — LSP
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


# ─── Diagram 1: LSP Violation ────────────────────────────────────────
def make_lsp_violation():
    W, H = 1000, 540
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(15, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "Порушення LSP — ReadOnlyRecord кидає виняток де не очікується",
              font=ft_title, fill=RED, anchor="mm")

    # Base class
    bx, by, bw, bh = 330, 70, 340, 110
    rr(draw, [bx, by, bx+bw, by+bh], radius=10, fill=PANEL, outline=ACCENT, width=2)
    draw.text((bx + bw//2, by + 20), "MedicalRecord", font=ft_name, fill=ACCENT, anchor="mm")
    hline(draw, bx+14, bx+bw-14, by+38, LINE)
    for i, m in enumerate(["UpdateDiagnosis(text)", "AddNote(text)", "GetSummary(): string"]):
        draw.text((bx + bw//2, by + 54 + i * 20), m, font=ft_meth, fill=MUTED, anchor="mm")

    # ReadOnlyRecord — violates LSP
    rx, ry, rw, rh = 550, 250, 360, 130
    rr(draw, [rx, ry, rx+rw, ry+rh], radius=10, fill=PANEL, outline=RED, width=2)
    draw.text((rx + rw//2, ry + 20), "ReadOnlyRecord", font=ft_name, fill=RED, anchor="mm")
    hline(draw, rx+14, rx+rw-14, ry+38, LINE)
    for i, line in enumerate(["UpdateDiagnosis(text):",
                               "  throw NotSupportedException",
                               "AddNote(text):",
                               "  throw NotSupportedException"]):
        col = RED if "throw" in line else MUTED
        draw.text((rx + rw//2, ry + 54 + i * 18), line, font=ft_meth, fill=col, anchor="mm")

    # DetailedRecord — correct
    cx2, cy2, cw2, ch2 = 90, 250, 340, 110
    rr(draw, [cx2, cy2, cx2+cw2, cy2+ch2], radius=10, fill=PANEL, outline=ACCENT, width=2)
    draw.text((cx2 + cw2//2, cy2 + 20), "DetailedRecord", font=ft_name, fill=ACCENT, anchor="mm")
    hline(draw, cx2+14, cx2+cw2-14, cy2+38, LINE)
    for i, m in enumerate(["UpdateDiagnosis(text)", "AddNote(text)", "+ AddAttachment(file)"]):
        draw.text((cx2 + cw2//2, cy2 + 54 + i * 20), m, font=ft_meth, fill=MUTED, anchor="mm")

    arrow(draw, bx + bw//2 - 80, by + bh, cx2 + cw2//2, cy2, MUTED, head=7)
    arrow(draw, bx + bw//2 + 80, by + bh, rx + rw//2, ry, RED, head=7)

    # Client code
    kx, ky, kw, kh = 330, 430, 340, 60
    rr(draw, [kx, ky, kx+kw, ky+kh], radius=8, fill=PANEL, outline=YELLOW, width=2)
    draw.text((kx + kw//2, ky + 16), "ProcessRecord(MedicalRecord r)", font=ft_meth, fill=YELLOW, anchor="mm")
    draw.text((kx + kw//2, ky + 38), "r.UpdateDiagnosis(...)  // OK для базового", font=ft_meth, fill=MUTED, anchor="mm")

    draw.text((rx + rw//2, ry + rh + 18), "[X] Передали ReadOnlyRecord — Exception!", font=ft_note, fill=RED, anchor="mm")
    draw.text((cx2 + cw2//2, cy2 + ch2 + 18), "[OK] DetailedRecord — працює коректно", font=ft_note, fill=ACCENT, anchor="mm")

    draw.text((W//2, H - 22),
              "Якщо підтип кидає виняток замість виконання — це порушення LSP",
              font=ft_note, fill=RED, anchor="mm")

    img.save(os.path.join(OUT_DIR, "lsp-violation.png"))
    print("Saved lsp-violation.png")


# ─── Diagram 2: LSP Correct ──────────────────────────────────────────
def make_lsp_correct():
    W, H = 1000, 520
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(15, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "Правильна ієрархія — підкласи розширюють, не звужують контракт",
              font=ft_title, fill=ACCENT, anchor="mm")

    # Base interface
    ix, iy, iw, ih = 330, 65, 340, 100
    rr(draw, [ix, iy, ix+iw, iy+ih], radius=10, fill=PANEL, outline=ACCENT, width=2)
    draw.text((ix + iw//2, iy + 16), "<<interface>>", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((ix + iw//2, iy + 36), "IMedicalRecord", font=ft_name, fill=ACCENT, anchor="mm")
    hline(draw, ix+14, ix+iw-14, iy+56, LINE)
    draw.text((ix + iw//2, iy + 72), "GetSummary(): string", font=ft_meth, fill=MUTED, anchor="mm")

    # IEditableMedicalRecord
    ex, ey, ew, eh = 330, 220, 340, 110
    rr(draw, [ex, ey, ex+ew, ey+eh], radius=10, fill=PANEL, outline=BLUE, width=2)
    draw.text((ex + ew//2, ey + 16), "<<interface>>", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((ex + ew//2, ey + 36), "IEditableMedicalRecord", font=ft_name, fill=BLUE, anchor="mm")
    hline(draw, ex+14, ex+ew-14, ey+56, LINE)
    for i, m in enumerate(["UpdateDiagnosis(text)", "AddNote(text)"]):
        draw.text((ex + ew//2, ey + 70 + i * 20), m, font=ft_meth, fill=MUTED, anchor="mm")
    arrow(draw, ex + ew//2, ey, ix + iw//2, iy + ih, MUTED, head=6)

    # ReadOnlyRecord — only implements IMedicalRecord
    rx, ry, rw, rh = 60, 390, 280, 90
    rr(draw, [rx, ry, rx+rw, ry+rh], radius=8, fill=PANEL, outline=MUTED, width=2)
    draw.text((rx + rw//2, ry + 20), "ReadOnlyRecord", font=ft_name, fill=MUTED, anchor="mm")
    hline(draw, rx+12, rx+rw-12, ry+38, LINE)
    draw.text((rx + rw//2, ry + 54), "GetSummary(): string", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((rx + rw//2, ry + 76), "[OK] Не реалізує IEditable", font=ft_note, fill=ACCENT, anchor="mm")
    arrow(draw, rx + rw//2, ry, ix + iw//2 - 60, iy + ih, MUTED, head=6)

    # DetailedRecord — implements both
    dx, dy, dw, dh = 660, 390, 280, 90
    rr(draw, [dx, dy, dx+dw, dy+dh], radius=8, fill=PANEL, outline=ACCENT, width=2)
    draw.text((dx + dw//2, dy + 20), "DetailedRecord", font=ft_name, fill=ACCENT, anchor="mm")
    hline(draw, dx+12, dx+dw-12, dy+38, LINE)
    draw.text((dx + dw//2, dy + 54), "GetSummary(), UpdateDiagnosis()", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((dx + dw//2, dy + 76), "[OK] Контракт виконано повністю", font=ft_note, fill=ACCENT, anchor="mm")
    arrow(draw, dx + dw//2, dy, ex + ew//2, ey + eh, MUTED, head=6)

    draw.text((W//2, H - 22),
              "Кожен клас реалізує рівно ті інтерфейси, контракт яких може виконати",
              font=ft_note, fill=ACCENT, anchor="mm")

    img.save(os.path.join(OUT_DIR, "lsp-correct.png"))
    print("Saved lsp-correct.png")


if __name__ == "__main__":
    make_lsp_violation()
    make_lsp_correct()
    print("All diagrams done.")
