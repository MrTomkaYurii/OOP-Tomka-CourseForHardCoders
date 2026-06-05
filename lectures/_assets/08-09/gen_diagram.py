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

W, H = 1000, 470
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
fb = font("arialbd.ttf", 13)

# ── TITLE ──
d.text((W//2, 28), "Кортежі в C#: System.Tuple (старий) vs ValueTuple (новий)", ACCENT, font=ft, anchor="mm")
d.line([(W//2, 48), (W//2, 355)], LINE_C, width=1)

# ══ LEFT: Old Tuple ══
d.text((250, 60), "System.Tuple<T1,T2>  (до C# 7)", RED, font=fb, anchor="mm")
d.line([(20, 75), (W//2-15, 75)], LINE_C, width=1)

old_items = [
    ("Тип даних:",    "reference type (клас)",      RED),
    ("Пам'ять:",      "виділяється в heap",         RED),
    ("Синтаксис:",    "Tuple.Create(\"Іван\", 45)", MUTED),
    ("Доступ:",       ".Item1  .Item2  (readonly)",  MUTED),
    ("Мутабельність:","властивості readonly",        RED),
    ("Довжина:",      "до 8 елементів (потім nest)", MUTED),
    ("Рівність:",     "за посиланням (object)",      RED),
]
for i, (label, value, col) in enumerate(old_items):
    y = 90 + i * 33
    d.rounded_rectangle([22, y, W//2-17, y+26], radius=4, fill=PANEL, outline=LINE_C, width=1)
    d.text((34, y+13), label, MUTED, font=fs, anchor="lm")
    d.text((170, y+13), value, col, font=fs, anchor="lm")

# ══ RIGHT: New ValueTuple ══
d.text((750, 60), "(string Name, int Age)  — C# 7+", ACCENT, font=fb, anchor="mm")
d.line([(W//2+15, 75), (W-20, 75)], LINE_C, width=1)

new_items = [
    ("Тип даних:",    "value type (struct)",        ACCENT),
    ("Пам'ять:",      "виділяється на stack",       ACCENT),
    ("Синтаксис:",    "(\"Іван\", 45)",             ACCENT),
    ("Доступ:",       ".Name  .Age  (або .Item1)",  ACCENT),
    ("Мутабельність:","поля можна змінювати",       ACCENT),
    ("Довжина:",      "необмежена",                 ACCENT),
    ("Рівність:",     "структурна (==, Equals)",    ACCENT),
]
for i, (label, value, col) in enumerate(new_items):
    y = 90 + i * 33
    d.rounded_rectangle([W//2+17, y, W-22, y+26], radius=4, fill=PANEL, outline=LINE_C, width=1)
    d.text((W//2+29, y+13), label, MUTED, font=fs, anchor="lm")
    d.text((W//2+167, y+13), value, col, font=fs, anchor="lm")

# ══ BOTTOM: Named fields as aliases ══
sep_y = 360
d.line([(20, sep_y), (W-20, sep_y)], LINE_C, width=1)
d.text((W//2, sep_y+16), "Іменовані поля — лише compile-time аліаси (в IL завжди Item1, Item2)", MUTED, font=fl, anchor="mm")

# Show alias mapping
alias_y = sep_y + 38
# Left: source code
d.rounded_rectangle([30, alias_y, 440, alias_y+64], radius=6, fill=PANEL, outline=LINE_C, width=1)
d.text((44, alias_y+14), "(string Name, int Age) patient;", TEXT, font=fc, anchor="lm")
d.text((44, alias_y+34), "patient.Name  patient.Age", ACCENT, font=fc, anchor="lm")
d.text((44, alias_y+50), "// зручні аліаси у C# коді", MUTED, font=fs, anchor="lm")

# Arrow
d.line([(445, alias_y+32), (510, alias_y+32)], MUTED, width=2)
d.polygon([(510, alias_y+26), (510, alias_y+38), (523, alias_y+32)], MUTED)
d.text((478, alias_y+18), "IL", MUTED, font=fs, anchor="mm")

# Right: IL
d.rounded_rectangle([526, alias_y, W-30, alias_y+64], radius=6, fill=PANEL, outline=LINE_C, width=1)
d.text((540, alias_y+14), "ValueTuple<string, int> patient;", TEXT, font=fc, anchor="lm")
d.text((540, alias_y+34), "patient.Item1  patient.Item2", MUTED, font=fc, anchor="lm")
d.text((540, alias_y+50), "// в скомпільованому коді", MUTED, font=fs, anchor="lm")

out = "lectures/_assets/08-09/tuple-old-vs-new.png"
img.save(out)
print(f"OK: {out}")
