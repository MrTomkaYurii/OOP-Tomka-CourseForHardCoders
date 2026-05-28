"""
Diagrams for section 20.1 — Вступ до SOLID
Palette: BG=#111413, ACCENT=#76c7ad, TEXT=#e5e9e7, MUTED=#a1aaa6, LINE=#2c3531, PANEL=#191e1c
"""
from PIL import Image, ImageDraw, ImageFont
import os

BG      = "#111413"
ACCENT  = "#76c7ad"
TEXT    = "#e5e9e7"
MUTED   = "#a1aaa6"
LINE    = "#2c3531"
PANEL   = "#191e1c"
RED     = "#e07070"
YELLOW  = "#d4b96a"
BLUE    = "#6a9fd4"

OUT_DIR = os.path.dirname(__file__)

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

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
    for path in pool:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

# ─────────────────────────────────────────────────────────────────────
# Diagram 1: God Class — ClinicManager робить все
# ─────────────────────────────────────────────────────────────────────
def make_god_class():
    W, H = 1100, 700
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title  = load_font(22, bold=True)
    ft_label  = load_font(17, bold=True)
    ft_small  = load_font(14)
    ft_note   = load_font(13)

    # Title
    title = "God Class — один клас, що робить усе"
    draw.text((W//2, 30), title, font=ft_title, fill=ACCENT, anchor="mm")

    # Central God class box
    cx, cy = W//2, H//2
    bw, bh = 220, 180
    draw_rounded_rect(draw, [cx-bw//2, cy-bh//2, cx+bw//2, cy+bh//2],
                      radius=12, fill=PANEL, outline=RED, width=3)

    draw.text((cx, cy - 50), "ClinicManager", font=ft_label, fill=RED, anchor="mm")
    draw.text((cx, cy - 22), "«God Class»", font=ft_note, fill=MUTED, anchor="mm")

    methods = [
        "AddPatient()     RemovePatient()",
        "BookAppointment()  CancelAppt()",
        "SendEmailAlert()   SendSms()",
        "SaveToFile()      LoadFromDb()",
        "GenerateReport()  CalcBilling()",
    ]
    for i, m in enumerate(methods):
        draw.text((cx, cy + 10 + i * 22), m, font=ft_note, fill=MUTED, anchor="mm")

    # Satellites
    satellites = [
        (130,  80, "Пацієнти",      ACCENT),
        (W-130, 80, "Лікарі",       ACCENT),
        (80,   H//2, "База даних",  BLUE),
        (W-80, H//2, "Email / SMS", YELLOW),
        (130,  H-80, "Файли",       ACCENT),
        (W-130,H-80, "Звіти",       ACCENT),
    ]

    for sx, sy, label, col in satellites:
        sw, sh = 130, 52
        draw_rounded_rect(draw, [sx-sw//2, sy-sh//2, sx+sw//2, sy+sh//2],
                          radius=8, fill=PANEL, outline=col, width=2)
        draw.text((sx, sy), label, font=ft_small, fill=col, anchor="mm")

        # Arrow from satellite to center (double-headed)
        # compute edge of god box
        dx, dy = cx - sx, cy - sy
        dist = (dx**2 + dy**2) ** 0.5
        ratio_src = 30 / dist
        ratio_dst = max(bw, bh) / 2 / dist
        x1a = int(sx + dx * ratio_src)
        y1a = int(sy + dy * ratio_src)
        x1b = int(cx - dx * ratio_dst)
        y1b = int(cy - dy * ratio_dst)
        draw.line([(x1a, y1a), (x1b, y1b)], fill=LINE, width=2)

    # Annotation: кількість відповідальностей
    draw.text((cx, H - 28), "6 різних відповідальностей → 6 причин для зміни → неможливо тестувати й розширювати",
              font=ft_note, fill=RED, anchor="mm")

    img.save(os.path.join(OUT_DIR, "god-class.png"))
    print("Saved god-class.png")


# ─────────────────────────────────────────────────────────────────────
# Diagram 2: SOLID — огляд п'яти принципів
# ─────────────────────────────────────────────────────────────────────
def make_solid_overview():
    W, H = 1100, 620
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title  = load_font(22, bold=True)
    ft_letter = load_font(52, bold=True)
    ft_name   = load_font(18, bold=True)
    ft_ukr    = load_font(16)
    ft_desc   = load_font(14)

    draw.text((W//2, 36), "П'ять принципів SOLID", font=ft_title, fill=ACCENT, anchor="mm")

    principles = [
        ("S", "Single Responsibility",  "Принцип єдиної відповідальності",
         "Клас має лише одну причину\nдля зміни"),
        ("O", "Open / Closed",          "Принцип відкритості / закритості",
         "Відкритий для розширення,\nзакритий для модифікації"),
        ("L", "Liskov Substitution",    "Принцип підстановки Ліскова",
         "Підклас заміняє базовий клас\nбез порушення поведінки"),
        ("I", "Interface Segregation",  "Принцип розподілу інтерфейсів",
         "Багато малих інтерфейсів кращі\nза один великий"),
        ("D", "Dependency Inversion",   "Принцип інверсії залежностей",
         "Залежте від абстракцій,\nне від конкретних класів"),
    ]

    colors = [ACCENT, "#d4b96a", "#6a9fd4", "#c47ab8", "#e07070"]

    block_w = 185
    gap     = 24
    total_w = 5 * block_w + 4 * gap
    x0      = (W - total_w) // 2
    y0      = 80

    for i, (letter, eng, ukr, desc) in enumerate(principles):
        col  = colors[i]
        bx   = x0 + i * (block_w + gap)
        by   = y0
        bh   = H - y0 - 20

        draw_rounded_rect(draw, [bx, by, bx + block_w, by + bh],
                          radius=12, fill=PANEL, outline=col, width=2)

        # Big letter
        draw.text((bx + block_w//2, by + 62), letter,
                  font=ft_letter, fill=col, anchor="mm")

        # Separator line
        draw.line([(bx + 18, by + 105), (bx + block_w - 18, by + 105)],
                  fill=LINE, width=1)

        # English name
        for j, word in enumerate(eng.split(" / ") if " / " in eng else [eng]):
            draw.text((bx + block_w//2, by + 125 + j * 22), word,
                      font=ft_name, fill=TEXT, anchor="mm")

        offset = 170 if " / " not in eng else 192

        # Ukrainian name
        for j, line in enumerate(ukr.split("\n")):
            draw.text((bx + block_w//2, by + offset + j * 20), line,
                      font=ft_ukr, fill=MUTED, anchor="mm")

        # Separator
        draw.line([(bx + 18, by + offset + 48), (bx + block_w - 18, by + offset + 48)],
                  fill=LINE, width=1)

        # Description
        for j, line in enumerate(desc.split("\n")):
            draw.text((bx + block_w//2, by + offset + 62 + j * 20), line,
                      font=ft_desc, fill=TEXT, anchor="mm")

    img.save(os.path.join(OUT_DIR, "solid-overview.png"))
    print("Saved solid-overview.png")


# ─────────────────────────────────────────────────────────────────────
# Diagram 3: Ціна змін — без SOLID vs з SOLID
# ─────────────────────────────────────────────────────────────────────
def make_change_cost():
    W, H = 1000, 520
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title  = load_font(20, bold=True)
    ft_label  = load_font(17, bold=True)
    ft_small  = load_font(14)
    ft_note   = load_font(13)

    draw.text((W//2, 30), "Ціна однієї зміни — без SOLID vs з SOLID", font=ft_title, fill=ACCENT, anchor="mm")

    # Left side: without SOLID — chain reaction
    draw.text((W//4, 70), "БЕЗ SOLID", font=ft_label, fill=RED, anchor="mm")

    bad_chain = [
        ("ClinicManager",   RED,    "Змінити формат звіту"),
        ("AppointmentLogic",YELLOW, "Зламалось бронювання"),
        ("BillingCalc",     RED,    "Збій у рахунках"),
        ("FileExporter",    YELLOW, "Файл не зберігається"),
        ("EmailSender",     RED,    "Email не надсилається"),
    ]
    bx, by = 90, 95
    bw, bh = 220, 46
    for i, (name, col, note) in enumerate(bad_chain):
        y = by + i * (bh + 14)
        draw_rounded_rect(draw, [bx, y, bx+bw, y+bh], radius=8,
                          fill=PANEL, outline=col, width=2)
        draw.text((bx + bw//2, y + bh//2 - 8), name,
                  font=ft_small, fill=col, anchor="mm")
        draw.text((bx + bw//2, y + bh//2 + 10), note,
                  font=ft_note, fill=MUTED, anchor="mm")
        if i < len(bad_chain) - 1:
            ay = y + bh + 1
            draw.line([(bx + bw//2, ay), (bx + bw//2, ay + 12)], fill=RED, width=2)
            draw.polygon([(bx + bw//2 - 7, ay + 9), (bx + bw//2 + 7, ay + 9),
                          (bx + bw//2, ay + 14)], fill=RED)

    draw.text((bx + bw//2, by + len(bad_chain) * (bh + 14)),
              "Змінили 1 → поламали 5", font=ft_note, fill=RED, anchor="mm")

    # Right side: with SOLID — isolated change
    rx = W//2 + 40
    draw.text((rx + (W - rx)//2, 70), "З SOLID", font=ft_label, fill=ACCENT, anchor="mm")

    services = [
        ("ReportService",      ACCENT, "← змінюємо тільки цей"),
        ("AppointmentService", MUTED,  "нічого не знає про звіти"),
        ("BillingService",     MUTED,  "ізольований від решти"),
        ("FileService",        MUTED,  "ізольований від решти"),
        ("NotificationService",MUTED,  "ізольований від решти"),
    ]
    gw, gh = 230, 46
    for i, (name, col, note) in enumerate(services):
        y = by + i * (gh + 14)
        draw_rounded_rect(draw, [rx, y, rx+gw, y+gh], radius=8,
                          fill=PANEL, outline=col, width=2)
        draw.text((rx + gw//2, y + gh//2 - 8), name,
                  font=ft_small, fill=col, anchor="mm")
        draw.text((rx + gw//2, y + gh//2 + 10), note,
                  font=ft_note, fill=MUTED, anchor="mm")

    draw.text((rx + gw//2, by + len(services) * (gh + 14)),
              "Змінили 1 → все інше не торкнулось", font=ft_note, fill=ACCENT, anchor="mm")

    # Divider
    draw.line([(W//2, 60), (W//2, H - 20)], fill=LINE, width=1)

    img.save(os.path.join(OUT_DIR, "change-cost.png"))
    print("Saved change-cost.png")


if __name__ == "__main__":
    make_god_class()
    make_solid_overview()
    make_change_cost()
    print("All diagrams done.")
