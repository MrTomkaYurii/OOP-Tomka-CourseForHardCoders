from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)

W, H = 1000, 490
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
d.text((W//2, 28), "Анонімний тип: що генерує компілятор", ACCENT, font=ft, anchor="mm")

# ── LEFT: User code ──
lx, ly, lw, lh = 20, 55, 290, 110
d.rounded_rectangle([lx, ly, lx+lw, ly+lh], radius=8, fill=PANEL, outline=ACCENT, width=2)
d.text((lx+lw//2, ly+16), "Код програміста", ACCENT, font=fb, anchor="mm")
d.line([(lx+10, ly+30), (lx+lw-10, ly+30)], LINE_C, width=1)
user_lines = [
    ("var patient = new {", TEXT),
    ('    Name = "Іван",', ACCENT),
    ('    Age  = 45', ACCENT),
    ("};", TEXT),
]
for i, (line, col) in enumerate(user_lines):
    d.text((lx+14, ly+40+i*18), line, col, font=fc, anchor="lm")

# Arrow
arr_cx = lx+lw+60
arr_cy = ly+lh//2+10
d.line([(lx+lw+4, arr_cy), (arr_cx-18, arr_cy)], MUTED, width=2)
d.polygon([(arr_cx-18, arr_cy-6), (arr_cx-18, arr_cy+6), (arr_cx-4, arr_cy)], MUTED)
d.text((lx+lw+32, arr_cy-14), "компілятор", MUTED, font=fs, anchor="mm")
d.text((lx+lw+32, arr_cy+2), "генерує", MUTED, font=fs, anchor="mm")

# ── RIGHT: Generated class ──
rx, ry, rw = arr_cx+14, 55, 560
rh = 375
d.rounded_rectangle([rx, ry, rx+rw, ry+rh], radius=8, fill=PANEL, outline=AMBER, width=2)
d.text((rx+rw//2, ry+16), "Згенерований внутрішній клас (спрощено)", AMBER, font=fb, anchor="mm")
d.line([(rx+10, ry+30), (rx+rw-10, ry+30)], LINE_C, width=1)

gen_lines = [
    ("[CompilerGenerated]",                            MUTED),
    ("internal sealed class <>f__AnonymousType0",      TEXT),
    ("{",                                              MUTED),
    ("    // readonly властивості",                    MUTED),
    ("    public string Name { get; }",                ACCENT),
    ("    public int    Age  { get; }",                ACCENT),
    ("",                                               TEXT),
    ("    // конструктор",                             MUTED),
    ("    public <>f__AnonymousType0(string name, int age)", TEXT),
    ("    { Name = name; Age = age; }",                TEXT),
    ("",                                               TEXT),
    ("    // структурна рівність",                     MUTED),
    ("    public override bool Equals(object o) =>",   TEXT),
    ("        o is <>f__AnonymousType0 t &&",          TEXT),
    ("        Name == t.Name && Age == t.Age;",        ACCENT),
    ("",                                               TEXT),
    ("    public override int GetHashCode() => ...",   MUTED),
    ("    public override string ToString() =>",       MUTED),
    ('        "{ Name = Іван, Age = 45 }";',           MUTED),
    ("}",                                              MUTED),
]
for i, (line, col) in enumerate(gen_lines):
    d.text((rx+14, ry+40+i*17), line, col, font=fc, anchor="lm")

# ── KEY OBSERVATIONS (2 рядки по 2) ──
obs_y = ry + rh + 12
obs_items = [
    ("sealed",   "не можна успадкуватися від анонімного типу",        AMBER),
    ("readonly", "властивості immutable — значення фіксується при new", ACCENT),
    ("Equals",   "структурна рівність: однакові значення → рівні об'єкти", ACCENT),
    ("<>",       "ім'я з кутовими дужками — навмисно недоступне в C# коді", MUTED),
]
for row in range(2):
    for col_idx in range(2):
        i = row * 2 + col_idx
        if i >= len(obs_items): break
        code, desc, col = obs_items[i]
        x_obs = 22 + col_idx * 490
        y_obs = obs_y + row * 24 + 10
        d.text((x_obs, y_obs), f"{code}:", col, font=fb, anchor="lm")
        bb = d.textbbox((x_obs, y_obs), f"{code}:", font=fb, anchor="lm")
        d.text((bb[2]+8, y_obs), desc, MUTED, font=fs, anchor="lm")

out = "lectures/_assets/08-08/anonymous-type-generated.png"
img.save(out)
print(f"OK: {out}")
