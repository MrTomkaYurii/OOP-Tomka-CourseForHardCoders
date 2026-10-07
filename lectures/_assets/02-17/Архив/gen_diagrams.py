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

def draw_parameters():
    W, H = 880, 380
    img = Image.new("RGB", (W, H), h(BG))
    d = ImageDraw.Draw(img)

    d.text((W // 2, 20), "Параметри та аргументи методу", font=font(15, True), fill=h(ACCENT), anchor="mm")

    # Left: formal params
    lx = 10
    d.rounded_rectangle([lx, 42, lx + 390, 175], radius=8, fill=h(PANEL), outline=h(YELLOW), width=2)
    d.text((lx + 195, 60), "Формальні параметри (оголошення)", font=font(12, True), fill=h(YELLOW), anchor="mm")
    d.text((lx + 14, 82), "void RegisterPatient(string name,  int age,  string ward)", font=font(11), fill=h(TEXT), anchor="lm")
    d.text((lx + 14, 104), "                     ↑             ↑         ↑", font=font(11), fill=h(YELLOW), anchor="lm")
    d.text((lx + 14, 122), "              тип+ім'я       тип+ім'я   тип+ім'я", font=font(10), fill=h(MUTED), anchor="lm")
    d.text((lx + 14, 148), "Параметри отримують значення лише при виклику методу.", font=font(10), fill=h(MUTED), anchor="lm")

    # Right: actual params (arguments)
    rx = 420
    d.rounded_rectangle([rx, 42, rx + 450, 175], radius=8, fill=h(PANEL), outline=h(ACCENT), width=2)
    d.text((rx + 225, 60), "Фактичні параметри (аргументи)", font=font(12, True), fill=h(ACCENT), anchor="mm")
    d.text((rx + 14, 82), 'RegisterPatient("Іван Петренко",  45,  "Кардіологія")', font=font(11), fill=h(TEXT), anchor="lm")
    d.text((rx + 14, 104), '                ↓                 ↓    ↓', font=font(11), fill=h(ACCENT), anchor="lm")
    d.text((rx + 14, 122), '           name="Іван..."    age=45  ward="Кардіологія"', font=font(10), fill=h(MUTED), anchor="lm")
    d.text((rx + 14, 148), "Аргументи передаються за позицією (зліва направо).", font=font(10), fill=h(MUTED), anchor="lm")

    # Optional params
    oy = 190
    d.rounded_rectangle([10, oy, W // 2 - 5, oy + 110], radius=7, fill=h(PANEL), outline=h(YELLOW), width=1)
    d.text((20, oy + 16), "Необов'язкові параметри (зі значенням за замовч.)", font=font(11, True), fill=h(YELLOW), anchor="lm")
    d.text((14, oy + 36), 'void Log(string msg, int level = 1, bool urgent = false)', font=font(10), fill=h(TEXT), anchor="lm")
    d.text((14, oy + 58), 'Log("Прийом");              // level=1, urgent=false', font=font(10), fill=h(MUTED), anchor="lm")
    d.text((14, oy + 76), 'Log("Критично", 3);         // level=3, urgent=false', font=font(10), fill=h(MUTED), anchor="lm")
    d.text((14, oy + 94), 'Log("Аварія", 3, true);     // всі явно', font=font(10), fill=h(MUTED), anchor="lm")

    # Named params
    nx = W // 2 + 5
    d.rounded_rectangle([nx, oy, W - 10, oy + 110], radius=7, fill=h(PANEL), outline=h(ACCENT), width=1)
    d.text((nx + 10, oy + 16), "Іменовані параметри", font=font(11, True), fill=h(ACCENT), anchor="lm")
    d.text((nx + 10, oy + 36), 'void Log(string msg, int level = 1, bool urgent = false)', font=font(10), fill=h(TEXT), anchor="lm")
    d.text((nx + 10, oy + 58), 'Log("Прийом", urgent: true);      // порядок порушено', font=font(10), fill=h(MUTED), anchor="lm")
    d.text((nx + 10, oy + 76), 'Log(level: 3, msg: "Критично");   // обидва іменовані', font=font(10), fill=h(MUTED), anchor="lm")
    d.text((nx + 10, oy + 94), 'Після іменованих можна ставити лише іменовані.', font=font(9), fill=h(MUTED), anchor="lm")

    # Type compatibility note
    ty = oy + 122
    d.rounded_rectangle([10, ty, W - 10, ty + 62], radius=6, fill=h(PANEL), outline=h(RED), width=1)
    d.text((20, ty + 14), "Відповідність типів:", font=font(11, True), fill=h(RED), anchor="lm")
    d.text((170, ty + 14), "аргумент повинен відповідати типу параметра або неявно перетворюватися до нього.", font=font(10), fill=h(TEXT), anchor="lm")
    d.text((20, ty + 38), "byte b = 37;  RegisterAge(b);  // ✓ byte → int неявно", font=font(10), fill=h(ACCENT), anchor="lm")
    d.text((400, ty + 38), 'RegisterAge("37");  // ✗ string → int: помилка компіляції', font=font(10), fill=h(RED), anchor="lm")

    save_if_new(img, "method-parameters.png")

draw_parameters()
print("Done.")
