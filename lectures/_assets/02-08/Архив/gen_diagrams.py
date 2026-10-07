from PIL import Image, ImageDraw, ImageFont
import os
OUTPUT_DIR = os.path.dirname(__file__)
BG = "#111413"; ACCENT = "#76c7ad"; TEXT = "#e5e9e7"; MUTED = "#a1aaa6"
LINE = "#2c3531"; PANEL = "#191e1c"; YELLOW = "#c7b876"; RED = "#e07070"

def h(c):
    c = c.lstrip("#"); return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

def save_if_new(img, name):
    p = os.path.join(OUTPUT_DIR, name)
    if not os.path.exists(p): img.save(p); print(f"Saved: {name}")
    else: print(f"Skipped: {name}")

def font(s, b=False):
    try: return ImageFont.truetype("arialbd.ttf" if b else "arial.ttf", s)
    except: return ImageFont.load_default()

def draw_assignment():
    W, H = 880, 420
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Операції присвоєння C#", font=font(16, True), fill=h(ACCENT), anchor="mm")

    # Left column: arithmetic assignment
    lx = 20
    d.text((lx + 195, 50), "Арифметичні", font=font(13, True), fill=h(YELLOW), anchor="mm")

    arith = [
        ("+=",  "A += B", "A = A + B"),
        ("-=",  "A -= B", "A = A - B"),
        ("*=",  "A *= B", "A = A * B"),
        ("/=",  "A /= B", "A = A / B"),
        ("%=",  "A %= B", "A = A % B"),
    ]

    for i, (op, short, full) in enumerate(arith):
        ry = 68 + i * 56
        d.rounded_rectangle([lx, ry, lx + 390, ry + 46], radius=6, fill=h(PANEL), outline=h(YELLOW), width=2)
        d.text((lx + 10, ry + 13), op, font=font(14, True), fill=h(YELLOW), anchor="lm")
        d.text((lx + 55, ry + 13), short, font=font(12), fill=h(TEXT), anchor="lm")
        d.text((lx + 380, ry + 13), full, font=font(11), fill=h(MUTED), anchor="rm")

    # Right column: bitwise assignment
    rx = 460
    d.text((rx + 195, 50), "Побітові та зсуву", font=font(13, True), fill=h(ACCENT), anchor="mm")

    bitwise = [
        ("&=",  "A &= B",  "A = A & B"),
        ("|=",  "A |= B",  "A = A | B"),
        ("^=",  "A ^= B",  "A = A ^ B"),
        ("<<=", "A <<= B", "A = A << B"),
        (">>=", "A >>= B", "A = A >> B"),
    ]

    for i, (op, short, full) in enumerate(bitwise):
        ry = 68 + i * 56
        d.rounded_rectangle([rx, ry, rx + 400, ry + 46], radius=6, fill=h(PANEL), outline=h(ACCENT), width=2)
        d.text((rx + 10, ry + 13), op, font=font(14, True), fill=h(ACCENT), anchor="lm")
        d.text((rx + 55, ry + 13), short, font=font(12), fill=h(TEXT), anchor="lm")
        d.text((rx + 390, ry + 13), full, font=font(11), fill=h(MUTED), anchor="rm")

    # Bottom note: right-associativity
    note_y = H - 55
    d.rounded_rectangle([20, note_y, W - 20, H - 10], radius=6, fill=h(PANEL), outline=h(RED), width=1)
    d.text((30, note_y + 14), "Правоасоціативність:", font=font(11, True), fill=h(RED), anchor="lm")
    d.text((30, note_y + 32), "c = a += b -= 5   →   спочатку b-=5, потім a+=b, потім c=a", font=font(11), fill=h(TEXT), anchor="lm")

    save_if_new(img, "assignment-ops.png")

draw_assignment()
print("Done.")
