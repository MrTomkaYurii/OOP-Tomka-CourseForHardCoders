from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.dirname(__file__)

BG     = "#111413"
ACCENT = "#76c7ad"
TEXT   = "#e5e9e7"
MUTED  = "#a1aaa6"
LINE   = "#2c3531"
PANEL  = "#191e1c"
YELLOW = "#c7b876"
RED    = "#e07070"

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def save_if_new(img, name):
    path = os.path.join(OUTPUT_DIR, name)
    if not os.path.exists(path):
        img.save(path)
        print(f"Saved: {name}")
    else:
        print(f"Skipped (exists): {name}")

def load_font(size, bold=False):
    try:
        name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(name, size)
    except:
        return ImageFont.load_default()

def draw_call_stack_search():
    W, H = 860, 560
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(18, bold=True)
    label_f = load_font(14, bold=True)
    code_f  = load_font(12)
    note_f  = load_font(11)

    d.text((W // 2, 22), "Пошук catch у стеку викликів", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    # Three method frames in a stack (bottom = outermost, top = innermost)
    frames = [
        {
            "name":  "ProcessAdmission()  ← точка входу",
            "catch": "catch (FormatException) ✓  ← знайдено!",
            "finally": "finally ← виконується 3-м",
            "catch_color": ACCENT,
            "border": ACCENT,
        },
        {
            "name":  "SaveRecord()",
            "catch": "catch (NullReferenceException)  ✗",
            "finally": "finally ← виконується 2-м",
            "catch_color": RED,
            "border": MUTED,
        },
        {
            "name":  "ParseAge()  ← виняток тут",
            "catch": "немає catch  ✗",
            "finally": "finally ← виконується 1-м",
            "catch_color": RED,
            "border": RED,
        },
    ]

    bw, bh = 400, 95
    bx = 80
    gap = 18
    total_h = len(frames) * bh + (len(frames) - 1) * gap
    start_y = (H - total_h) // 2 + 20

    # Draw frames bottom to top (visual: top of screen = top of stack)
    frame_positions = []
    for i, frame in enumerate(frames):
        fy = start_y + i * (bh + gap)
        frame_positions.append((bx, fy, bw, bh))
        color = frame["border"]
        d.rounded_rectangle([bx, fy, bx + bw, fy + bh], radius=8,
                             fill=hex_to_rgb(PANEL), outline=hex_to_rgb(color), width=2)
        d.text((bx + 12, fy + 16), frame["name"], font=label_f,
               fill=hex_to_rgb(color), anchor="lm")
        d.line([(bx + 10, fy + 30), (bx + bw - 10, fy + 30)],
               fill=hex_to_rgb(LINE), width=1)
        d.text((bx + 12, fy + 50), frame["catch"], font=code_f,
               fill=hex_to_rgb(frame["catch_color"]), anchor="lm")
        d.text((bx + 12, fy + 72), frame["finally"], font=note_f,
               fill=hex_to_rgb(YELLOW), anchor="lm")

    # Right side: phase annotations
    rx = bx + bw + 40
    rw = W - rx - 20

    # Phase 1: Search upward
    phase1_y = start_y
    d.rounded_rectangle([rx, phase1_y, rx + rw, phase1_y + total_h // 2 - 10],
                         radius=8, fill=hex_to_rgb(PANEL), outline=hex_to_rgb(LINE), width=1)
    d.text((rx + rw // 2, phase1_y + 14), "Фаза 1: пошук catch",
           font=label_f, fill=hex_to_rgb(YELLOW), anchor="mm")
    d.line([(rx + 10, phase1_y + 28), (rx + rw - 10, phase1_y + 28)],
           fill=hex_to_rgb(LINE), width=1)
    search_lines = [
        "ParseAge → немає catch",
        "↓ підіймається вище",
        "SaveRecord → не той тип",
        "↓ підіймається вище",
        "ProcessAdmission → знайдено!",
    ]
    for i, line in enumerate(search_lines):
        color = ACCENT if "знайдено" in line else (MUTED if "підіймається" in line else TEXT)
        d.text((rx + 12, phase1_y + 44 + i * 18), line, font=note_f,
               fill=hex_to_rgb(color), anchor="lm")

    # Phase 2: Execute finally downward
    phase2_y = start_y + total_h // 2 + 10
    d.rounded_rectangle([rx, phase2_y, rx + rw, phase2_y + total_h // 2 - 10],
                         radius=8, fill=hex_to_rgb(PANEL), outline=hex_to_rgb(LINE), width=1)
    d.text((rx + rw // 2, phase2_y + 14), "Фаза 2: finally + catch",
           font=label_f, fill=hex_to_rgb(ACCENT), anchor="mm")
    d.line([(rx + 10, phase2_y + 28), (rx + rw - 10, phase2_y + 28)],
           fill=hex_to_rgb(LINE), width=1)
    exec_lines = [
        "finally у ParseAge",
        "↓",
        "finally у SaveRecord",
        "↓",
        "catch + finally у ProcessAdmission",
    ]
    for i, line in enumerate(exec_lines):
        color = ACCENT if "catch" in line else (MUTED if line == "↓" else TEXT)
        d.text((rx + 12, phase2_y + 44 + i * 18), line, font=note_f,
               fill=hex_to_rgb(color), anchor="lm")

    # Bottom note
    note_y = start_y + total_h + 30
    d.rounded_rectangle([bx, note_y, W - 20, note_y + 50], radius=8,
                         fill=hex_to_rgb(PANEL), outline=hex_to_rgb(LINE), width=1)
    d.text((W // 2, note_y + 16),
           "Код після try...catch у ParseAge та SaveRecord НЕ виконується.",
           font=note_f, fill=hex_to_rgb(RED), anchor="mm")
    d.text((W // 2, note_y + 34),
           "Якщо catch не знайдено ніде — програма аварійно завершується.",
           font=note_f, fill=hex_to_rgb(MUTED), anchor="mm")

    save_if_new(img, "call-stack-search.png")

draw_call_stack_search()
print("Done.")
