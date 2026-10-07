from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)
RED    = (190, 80, 80)

W, H = 1000, 430
img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

def font(name, size):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
    except:
        return ImageFont.load_default()

ft = font("arialbd.ttf", 17)
fl = font("arial.ttf",   14)
fc = font("cour.ttf",    13)
fs = font("arial.ttf",   12)
fb = font("arialbd.ttf", 12)

# ── TITLE ──
d.text((W//2, 28), "Патерн типів: стара форма vs pattern matching", ACCENT, font=ft, anchor="mm")
d.line([(W//2, 48), (W//2, H-30)], LINE_C, width=1)

# ══ LEFT: Old way ══
d.text((250, 60), "Стара форма (до C# 7)", RED, font=fb, anchor="mm")
d.line([(20, 75), (W//2-15, 75)], LINE_C, width=1)

old_lines = [
    ("MedicalStaff staff = GetStaff();",             TEXT),
    ("",                                              TEXT),
    ("// 1. Перевірка типу",                          MUTED),
    ("if (staff is Doctor)",                          TEXT),
    ("{",                                             MUTED),
    ("    // 2. Явний cast",                          MUTED),
    ("    Doctor doc = (Doctor)staff;",               RED),
    ("    doc.PrescribeMeds();",                      TEXT),
    ("}",                                             MUTED),
    ("",                                              TEXT),
    ("// Або через as + null-check:",                 MUTED),
    ("Doctor? doc = staff as Doctor;",                TEXT),
    ("if (doc != null)",                              TEXT),
    ("    doc.PrescribeMeds();",                      TEXT),
]
for i, (line, col) in enumerate(old_lines):
    d.text((30, 88+i*21), line, col, font=fc, anchor="lm")

# ══ RIGHT: New pattern matching ══
d.text((750, 60), "Pattern matching (C# 7+)", ACCENT, font=fb, anchor="mm")
d.line([(W//2+15, 75), (W-20, 75)], LINE_C, width=1)

new_lines = [
    ("MedicalStaff staff = GetStaff();",             TEXT),
    ("",                                              TEXT),
    ("// Перевірка + cast + змінна — одним виразом", MUTED),
    ("if (staff is Doctor doc)",                      ACCENT),
    ("{",                                             MUTED),
    ("    // doc вже типу Doctor, готова до використання", MUTED),
    ("    doc.PrescribeMeds();",                      ACCENT),
    ("}",                                             MUTED),
    ("",                                              TEXT),
    ("// Або в switch expression:",                    MUTED),
    ("string role = staff switch",                    TEXT),
    ("{",                                             MUTED),
    ("    Doctor   => \"Лікар\"  ,",                  ACCENT),
    ("    Nurse    => \"Медсестра\",",                 ACCENT),
    ("    _        => \"Персонал\"",                   MUTED),
    ("};",                                            MUTED),
]
for i, (line, col) in enumerate(new_lines):
    d.text((W//2+25, 88+i*21), line, col, font=fc, anchor="lm")

# ── BOTTOM: Key advantages ══
note_y = H - 46
d.line([(20, note_y-8), (W-20, note_y-8)], LINE_C, width=1)
d.text((W//2, note_y+6),
    "Pattern matching: перевірка типу + cast + прив'язка змінної — все в одній операції, без дублювання.",
    MUTED, font=fs, anchor="mm")
d.text((W//2, note_y+22),
    "Компілятор гарантує: якщо is-перевірка пройшла, змінна не є null і має правильний тип.",
    ACCENT, font=fs, anchor="mm")

out = "lectures/_assets/09-01/type-pattern-old-vs-new.png"
img.save(out)
print(f"OK: {out}")
