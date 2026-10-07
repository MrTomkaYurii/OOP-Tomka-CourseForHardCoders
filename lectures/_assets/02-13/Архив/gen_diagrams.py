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

def draw_loops():
    W, H = 920, 430
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Типи циклів у C#", font=font(16, True), fill=h(ACCENT), anchor="mm")

    panels = [
        ("for",
         ["for (int i = 0; i < n; i++)", "{", "    // тіло циклу", "}"],
         ["ініціалізація → умова → тіло → крок → умова...",
          "Відомо кількість ітерацій заздалегідь.",
          "Приклад: перебрати масив з 10 пацієнтів."],
         YELLOW),
        ("while",
         ["while (умова)", "{", "    // тіло циклу", "}"],
         ["умова перевіряється ДО тіла.",
          "Тіло може не виконатись жодного разу.",
          "Приклад: читати записи, поки є дані."],
         ACCENT),
        ("do...while",
         ["do", "{", "    // тіло циклу", "} while (умова);"],
         ["тіло виконується ПЕРЕД перевіркою умови.",
          "Мінімум 1 ітерація гарантована.",
          "Приклад: показати меню хоча б раз."],
         RED),
        ("foreach",
         ["foreach (тип змін in колекція)", "{", "    // тіло циклу", "}"],
         ["перебирає кожен елемент колекції.",
          "Тільки читання — не можна змінювати.",
          "Приклад: вивести список усіх пацієнтів."],
         MUTED),
    ]

    pw = (W - 30) // 4 - 5
    for i, (title, code, notes, col) in enumerate(panels):
        px = 10 + i * (pw + 7)
        d.rounded_rectangle([px, 44, px + pw, H - 15], radius=7, fill=h(PANEL), outline=h(col), width=2)
        d.text((px + pw // 2, 62), title, font=font(13, True), fill=h(col), anchor="mm")

        # code block
        cy = 80
        d.rounded_rectangle([px + 6, cy, px + pw - 6, cy + len(code) * 20 + 8], radius=4, fill=h(BG), outline=h(col), width=1)
        for j, ln in enumerate(code):
            d.text((px + 10, cy + 6 + j * 20), ln, font=font(9), fill=h(TEXT), anchor="lm")

        # notes
        ny = cy + len(code) * 20 + 22
        for j, note in enumerate(notes):
            d.text((px + 8, ny + j * 22), note, font=font(9), fill=h(MUTED), anchor="lm")

    # break/continue note at bottom
    note_y = H - 60
    d.line([(10, note_y - 6), (W - 10, note_y - 6)], fill=h(LINE), width=1)
    d.text((20, note_y + 8), "break", font=font(11, True), fill=h(RED), anchor="lm")
    d.text((75, note_y + 8), "— негайно завершує цикл і передає керування за його межі.", font=font(10), fill=h(TEXT), anchor="lm")
    d.text((20, note_y + 28), "continue", font=font(11, True), fill=h(YELLOW), anchor="lm")
    d.text((90, note_y + 28), "— пропускає решту поточної ітерації та переходить до наступної.", font=font(10), fill=h(TEXT), anchor="lm")

    save_if_new(img, "loops.png")

draw_loops()
print("Done.")
