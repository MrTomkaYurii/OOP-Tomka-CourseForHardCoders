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

def draw_method_anatomy():
    W, H = 860, 320
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 18), "Анатомія методу в C#", font=font(15, True), fill=h(ACCENT), anchor="mm")

    # Central method code display
    code_x = 60
    code_y = 50

    parts = [
        # (text, x_offset, color, label, label_y_offset)
        ("string",       0,    YELLOW,  "тип результату", -1),
        (" ",            52,   TEXT,    "",                0),
        ("GetDiagnosis", 58,   ACCENT,  "назва методу",   -1),
        ("(",            148,  MUTED,   "",                0),
        ("string",       153,  YELLOW,  "тип параметра",  1),
        (" ",            196,  TEXT,    "",                0),
        ("patientId",    202,  TEXT,    "ім'я параметра", 1),
        (")",            270,  MUTED,   "",                0),
    ]

    # Draw code line
    line_text = 'string GetDiagnosis(string patientId)'
    d.text((code_x, code_y + 8), line_text, font=font(14, True), fill=h(TEXT), anchor="lm")

    # Body
    body_y = code_y + 36
    d.text((code_x, body_y), "{", font=font(14), fill=h(MUTED), anchor="lm")
    d.text((code_x + 20, body_y + 24), 'if (patientId == "P-001") return "Гіпертонія";', font=font(12), fill=h(TEXT), anchor="lm")
    d.text((code_x + 20, body_y + 46), 'return "Невідомо";', font=font(12), fill=h(TEXT), anchor="lm")
    d.text((code_x, body_y + 68), "}", font=font(14), fill=h(MUTED), anchor="lm")

    # Annotation arrows + labels
    annotations = [
        # (arrow_from_x, arrow_from_y, label_x, label_y, text, color)
        (code_x + 25,  code_y + 8,   code_x - 10,   code_y + 80, "Тип результату:\n'string' означає\nметод повертає рядок", YELLOW),
        (code_x + 108, code_y + 8,   code_x + 108,  code_y + 120, "Назва методу:\nз великої літери,\nдієслово або дієслово+іменник", ACCENT),
        (code_x + 185, code_y + 8,   code_x + 280,  code_y + 78, "Параметри:\nтип і назва,\nрозділені комою", YELLOW),
        (code_x + 20,  body_y + 30,  code_x + 480,  body_y + 10, "Тіло методу:\n— return завершує виконання\n— значення після return = результат", ACCENT),
    ]

    for (ax, ay, lx, ly, txt, col) in annotations:
        d.line([(ax, ay), (lx, ly)], fill=h(col), width=1)
        for j, line in enumerate(txt.split("\n")):
            d.text((lx, ly + j * 15), line, font=font(10), fill=h(col), anchor="lm")

    # void note
    note_y = H - 68
    d.line([(10, note_y - 4), (W - 10, note_y - 4)], fill=h(LINE), width=1)
    d.text((20, note_y + 10), "void", font=font(12, True), fill=h(RED), anchor="lm")
    d.text((62, note_y + 10), "— метод нічого не повертає (без return зі значенням).", font=font(10), fill=h(TEXT), anchor="lm")
    d.text((20, note_y + 30), "Скорочений запис:", font=font(10, True), fill=h(MUTED), anchor="lm")
    d.text((138, note_y + 30), "void PrintName(string n) => Console.WriteLine(n);   — стрілочний синтаксис для однієї інструкції.", font=font(10), fill=h(TEXT), anchor="lm")

    save_if_new(img, "method-anatomy.png")

draw_method_anatomy()
print("Done.")
