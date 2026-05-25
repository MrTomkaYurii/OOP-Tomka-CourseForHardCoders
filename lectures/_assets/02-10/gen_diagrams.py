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

def draw_implicit_explicit():
    W, H = 880, 380
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Явні та неявні перетворення типів", font=font(16, True), fill=h(ACCENT), anchor="mm")

    # Left: implicit
    lx = 20
    box_h = 160
    d.rounded_rectangle([lx, 44, lx + 390, 44 + box_h], radius=8, fill=h(PANEL), outline=h(ACCENT), width=2)
    d.text((lx + 195, 60), "Неявне (implicit)", font=font(13, True), fill=h(ACCENT), anchor="mm")
    lines_l = [
        "byte a = 10;",
        "int  b = a;      // автоматично",
        "long c = b;      // автоматично",
        "double d = c;    // автоматично",
        "✓ безпечно, без ризику втрати даних",
    ]
    for i, line in enumerate(lines_l):
        col = h(MUTED) if line.startswith("✓") else h(TEXT)
        d.text((lx + 14, 76 + i * 24), line, font=font(11), fill=col, anchor="lm")

    # Right: explicit
    rx = 460
    d.rounded_rectangle([rx, 44, rx + 400, 44 + box_h], radius=8, fill=h(PANEL), outline=h(YELLOW), width=2)
    d.text((rx + 200, 60), "Явне (explicit)", font=font(13, True), fill=h(YELLOW), anchor="mm")
    lines_r = [
        "double d = 3.7;",
        "int    b = (int)d;    // = 3, не 3.7",
        "ushort u = 1000;",
        "byte   c = (byte)u;  // можлива втрата",
        "! потрібне явне (тип), ризик переповнення",
    ]
    for i, line in enumerate(lines_r):
        col = h(RED) if line.startswith("!") else h(TEXT)
        d.text((rx + 14, 76 + i * 24), line, font=font(11), fill=col, anchor="lm")

    # Overflow + checked section
    ov_y = 220
    d.text((W // 2, ov_y + 8), "Переповнення та ключове слово checked", font=font(13, True), fill=h(RED), anchor="mm")

    # Two panels side by side
    d.rounded_rectangle([lx, ov_y + 26, lx + 390, ov_y + 130], radius=6, fill=h(PANEL), outline=h(RED), width=1)
    d.text((lx + 10, ov_y + 40), "unchecked (за замовчуванням):", font=font(11, True), fill=h(RED), anchor="lm")
    unc = [
        "int a = 33, b = 600;",
        "byte c = (byte)(a + b);",
        "// c = 121  (633 % 256 = 121)",
        "// Старші біти мовчки відкидаються",
    ]
    for i, line in enumerate(unc):
        d.text((lx + 10, ov_y + 58 + i * 18), line, font=font(10), fill=h(MUTED), anchor="lm")

    d.rounded_rectangle([rx, ov_y + 26, rx + 400, ov_y + 130], radius=6, fill=h(PANEL), outline=h(ACCENT), width=1)
    d.text((rx + 10, ov_y + 40), "checked — захист від переповнення:", font=font(11, True), fill=h(ACCENT), anchor="lm")
    chk = [
        "byte c = checked((byte)(33 + 600));",
        "// Кидає OverflowException!",
        "// Безпечно — помилку видно одразу",
    ]
    for i, line in enumerate(chk):
        d.text((rx + 10, ov_y + 58 + i * 22), line, font=font(10), fill=h(TEXT), anchor="lm")

    save_if_new(img, "implicit-explicit.png")

def draw_sign_extension(title, src_label, src_bits, dst_bits, result_label, filename):
    """Діаграма розширення зі знаком: малий тип → великий тип (image16 / image17)."""
    W, H = 760, 220
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 18), title, font=font(14, True), fill=h(ACCENT), anchor="mm")

    BOX = 30
    GAP = 2

    def draw_bits_row(y, bits, label, is_src):
        # draw bit boxes
        n = len(bits)
        total_w = n * (BOX + GAP) - GAP
        start_x = (W - total_w) // 2
        for bi, bit in enumerate(bits):
            bx = start_x + bi * (BOX + GAP)
            # sign bit = first box
            is_sign = (bi == 0)
            # extension bits = first (len_dst - len_src) bits when dst
            is_ext = (not is_src) and (bi < len(dst_bits) - len(src_bits))
            fill_col = RED if is_ext else PANEL
            outline_col = YELLOW if is_sign else (ACCENT if not is_src else YELLOW)
            d.rectangle([bx, y, bx + BOX, y + BOX], fill=h(fill_col), outline=h(outline_col), width=2 if is_sign else 1)
            d.text((bx + BOX // 2, y + BOX // 2), bit, font=font(12, True),
                   fill=h(YELLOW) if is_sign else (h(RED) if is_ext else h(TEXT)), anchor="mm")
        # label on left
        d.text((start_x - 10, y + BOX // 2), label, font=font(11, True), fill=h(MUTED), anchor="rm")
        # result on right
        return start_x + total_w

    end_src = draw_bits_row(55, src_bits, src_label, True)
    end_dst = draw_bits_row(130, dst_bits, result_label, False)

    # Arrow
    cx = W // 2
    d.line([(cx, 95), (cx, 122)], fill=h(ACCENT), width=2)
    d.polygon([(cx - 5, 118), (cx + 5, 118), (cx, 128)], fill=h(ACCENT))
    d.text((cx + 15, 108), "розширення", font=font(10), fill=h(MUTED), anchor="lm")

    # Legend at bottom
    leg_y = H - 36
    d.rounded_rectangle([30, leg_y, W - 30, H - 4], radius=4, fill=h(PANEL), outline=h(MUTED), width=1)
    d.text((40, leg_y + 14), "■ розряди, що додаються при розширенні (копія знакового біту)", font=font(10), fill=h(RED), anchor="lm")

    save_if_new(img, filename)

def draw_implicit_conversion_table():
    """Таблиця безпечних неявних перетворень (image18)."""
    W, H = 820, 340
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Безпечні неявні перетворення (widening)", font=font(15, True), fill=h(ACCENT), anchor="mm")

    chains = [
        ("byte",    ["short", "ushort", "int", "uint", "long", "ulong", "float", "double", "decimal"]),
        ("sbyte",   ["short", "int", "long", "float", "double", "decimal"]),
        ("short",   ["int", "long", "float", "double", "decimal"]),
        ("ushort",  ["int", "uint", "long", "ulong", "float", "double", "decimal"]),
        ("int",     ["long", "float", "double", "decimal"]),
        ("uint",    ["long", "ulong", "float", "double", "decimal"]),
        ("long",    ["float", "double", "decimal"]),
        ("ulong",   ["float", "double", "decimal"]),
        ("float",   ["double"]),
        ("char",    ["ushort", "int", "uint", "long", "ulong", "float", "double", "decimal"]),
    ]

    row_h = 26
    for i, (src, targets) in enumerate(chains):
        ry = 46 + i * row_h
        # source type
        d.rounded_rectangle([10, ry + 1, 78, ry + row_h - 2], radius=4, fill=h(PANEL), outline=h(YELLOW), width=1)
        d.text((44, ry + row_h // 2), src, font=font(11, True), fill=h(YELLOW), anchor="mm")
        # arrow
        d.text((86, ry + row_h // 2), "→", font=font(11), fill=h(MUTED), anchor="mm")
        # targets
        tx = 100
        for t in targets:
            tw = len(t) * 7 + 12
            d.rounded_rectangle([tx, ry + 2, tx + tw, ry + row_h - 3], radius=3, fill=h(PANEL), outline=h(ACCENT), width=1)
            d.text((tx + tw // 2, ry + row_h // 2), t, font=font(10), fill=h(ACCENT), anchor="mm")
            tx += tw + 5

    # Bottom note
    note_y = H - 38
    d.rounded_rectangle([10, note_y, W - 10, H - 4], radius=4, fill=h(PANEL), outline=h(RED), width=1)
    d.text((20, note_y + 14), "double ↔ decimal: НЕ є автоматичним — потрібне явне (тип), незважаючи на розмір", font=font(10), fill=h(RED), anchor="lm")

    save_if_new(img, "implicit-conversion-table.png")

draw_sign_extension(
    "Розширення зі знаком — позитивне число (sbyte 4 → short)",
    "sbyte  4",  "00000100",
    "0000000000000100",
    "short  4",
    "sign-extension-positive.png"
)
draw_sign_extension(
    "Розширення зі знаком — від'ємне число (sbyte -4 → short)",
    "sbyte  -4", "11111100",
    "1111111111111100",
    "short  -4",
    "sign-extension-negative.png"
)
draw_implicit_conversion_table()
draw_implicit_explicit()
print("Done.")
