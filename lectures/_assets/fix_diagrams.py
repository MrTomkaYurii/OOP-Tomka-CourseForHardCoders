"""
Fix/regenerate all diagrams for lecture 20 (SOLID).
Palette: BG=#111413, ACCENT=#76c7ad, TEXT=#e5e9e7, MUTED=#a1aaa6, LINE=#2c3531, PANEL=#191e1c
Rules:
  - No Unicode check/cross marks — use [OK] / [X] instead
  - solid-overview: widen to 1400px so Ukrainian text fits
  - before-srp: annotation boxes stay on screen (left margin >= 16px)
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

BG     = "#111413"
ACCENT = "#76c7ad"
TEXT   = "#e5e9e7"
MUTED  = "#a1aaa6"
LINE   = "#2c3531"
PANEL  = "#191e1c"
RED    = "#e07070"
YELLOW = "#d4b96a"
BLUE   = "#6a9fd4"
PURPLE = "#c47ab8"

BASE = os.path.dirname(__file__)

def dir_for(section):
    d = os.path.join(BASE, section)
    os.makedirs(d, exist_ok=True)
    return d

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
    for p in pool:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def rr(draw, xy, radius=10, fill=PANEL, outline=None, width=2):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def arrow(draw, x1, y1, x2, y2, col, w=2, head=8):
    draw.line([(x1, y1), (x2, y2)], fill=col, width=w)
    angle = math.atan2(y2 - y1, x2 - x1)
    draw.polygon([
        (x2, y2),
        (int(x2 - head * math.cos(angle - 0.4)), int(y2 - head * math.sin(angle - 0.4))),
        (int(x2 - head * math.cos(angle + 0.4)), int(y2 - head * math.sin(angle + 0.4))),
    ], fill=col)

def hline(draw, x0, x1, y, col=LINE, width=1):
    draw.line([(x0, y), (x1, y)], fill=col, width=width)

def save(img, section, name):
    path = os.path.join(dir_for(section), name)
    img.save(path)
    print(f"Saved {section}/{name}")


# ═══════════════════════════════════════════════════════════════════════
# 20-01  god-class.png
# ═══════════════════════════════════════════════════════════════════════
def make_god_class():
    W, H = 1100, 700
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(22, bold=True)
    ft_label = load_font(17, bold=True)
    ft_small = load_font(14)
    ft_note  = load_font(13)

    draw.text((W//2, 30), "God Class — один клас, що робить усе",
              font=ft_title, fill=ACCENT, anchor="mm")

    cx, cy = W//2, H//2
    bw, bh = 220, 180
    rr(draw, [cx-bw//2, cy-bh//2, cx+bw//2, cy+bh//2], radius=12, fill=PANEL, outline=RED, width=3)
    draw.text((cx, cy - 50), "ClinicManager", font=ft_label, fill=RED, anchor="mm")
    draw.text((cx, cy - 22), "God Class", font=ft_note, fill=MUTED, anchor="mm")

    methods = [
        "AddPatient()     RemovePatient()",
        "BookAppointment()  CancelAppt()",
        "SendEmailAlert()   SendSms()",
        "SaveToFile()      LoadFromDb()",
        "GenerateReport()  CalcBilling()",
    ]
    for i, m in enumerate(methods):
        draw.text((cx, cy + 10 + i * 22), m, font=ft_note, fill=MUTED, anchor="mm")

    satellites = [
        (130,    80,   "Пацієнти",   ACCENT),
        (W-130,  80,   "Лікарі",     ACCENT),
        (80,     H//2, "База даних", BLUE),
        (W-80,   H//2, "Email/SMS",  YELLOW),
        (130,    H-80, "Файли",      ACCENT),
        (W-130,  H-80, "Звіти",      ACCENT),
    ]
    for sx, sy, label, col in satellites:
        sw, sh = 130, 52
        rr(draw, [sx-sw//2, sy-sh//2, sx+sw//2, sy+sh//2], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((sx, sy), label, font=ft_small, fill=col, anchor="mm")
        dx, dy = cx - sx, cy - sy
        dist = (dx**2 + dy**2) ** 0.5
        ratio_src = 30 / dist
        ratio_dst = max(bw, bh) / 2 / dist
        x1a = int(sx + dx * ratio_src)
        y1a = int(sy + dy * ratio_src)
        x1b = int(cx - dx * ratio_dst)
        y1b = int(cy - dy * ratio_dst)
        draw.line([(x1a, y1a), (x1b, y1b)], fill=LINE, width=2)

    draw.text((cx, H - 28),
              "6 різних відповідальностей — 6 причин для зміни — неможливо тестувати й розширювати",
              font=ft_note, fill=RED, anchor="mm")

    save(img, "20-01", "god-class.png")


# ═══════════════════════════════════════════════════════════════════════
# 20-01  solid-overview.png  (FIX: wider canvas, bigger blocks)
# ═══════════════════════════════════════════════════════════════════════
def make_solid_overview():
    W, H = 1400, 650
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title  = load_font(22, bold=True)
    ft_letter = load_font(52, bold=True)
    ft_name   = load_font(17, bold=True)
    ft_ukr    = load_font(14)
    ft_desc   = load_font(13)

    draw.text((W//2, 46), "П'ять принципів SOLID", font=ft_title, fill=ACCENT, anchor="mm")

    principles = [
        ("S", "Single", "Responsibility",
         "Принцип єдиної\nвідповідальності",
         "Клас має лише одну\nпричину для зміни"),
        ("O", "Open /", "Closed",
         "Принцип відкритості\nта закритості",
         "Відкритий до розширення,\nзакритий до модифікації"),
        ("L", "Liskov", "Substitution",
         "Принцип підстановки\nЛіскова",
         "Підклас замінює базовий\nбез порушення поведінки"),
        ("I", "Interface", "Segregation",
         "Принцип розподілу\nінтерфейсів",
         "Багато малих інтерфейсів\nкращі за один великий"),
        ("D", "Dependency", "Inversion",
         "Принцип інверсії\nзалежностей",
         "Залежте від абстракцій,\nне від конкретних класів"),
    ]
    colors = [ACCENT, YELLOW, BLUE, PURPLE, RED]

    block_w = 228
    gap     = 25
    total_w = 5 * block_w + 4 * gap
    x0      = (W - total_w) // 2
    y0      = 90
    bh      = H - y0 - 20

    for i, (letter, eng1, eng2, ukr, desc) in enumerate(principles):
        col = colors[i]
        bx  = x0 + i * (block_w + gap)

        rr(draw, [bx, y0, bx + block_w, y0 + bh], radius=12, fill=PANEL, outline=col, width=2)

        # Big letter
        draw.text((bx + block_w//2, y0 + 62), letter,
                  font=ft_letter, fill=col, anchor="mm")

        # Separator
        hline(draw, bx+18, bx+block_w-18, y0+108, LINE)

        # English name (two-word wrap)
        draw.text((bx + block_w//2, y0 + 128), eng1,
                  font=ft_name, fill=TEXT, anchor="mm")
        draw.text((bx + block_w//2, y0 + 150), eng2,
                  font=ft_name, fill=TEXT, anchor="mm")

        # Separator
        hline(draw, bx+18, bx+block_w-18, y0+175, LINE)

        # Ukrainian name
        for j, line in enumerate(ukr.split("\n")):
            draw.text((bx + block_w//2, y0 + 192 + j * 20), line,
                      font=ft_ukr, fill=MUTED, anchor="mm")

        # Separator
        hline(draw, bx+18, bx+block_w-18, y0+238, LINE)

        # Description
        for j, line in enumerate(desc.split("\n")):
            draw.text((bx + block_w//2, y0 + 254 + j * 20), line,
                      font=ft_desc, fill=TEXT, anchor="mm")

    save(img, "20-01", "solid-overview.png")


# ═══════════════════════════════════════════════════════════════════════
# 20-01  change-cost.png
# ═══════════════════════════════════════════════════════════════════════
def make_change_cost():
    W, H = 1000, 520
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_label = load_font(17, bold=True)
    ft_small = load_font(14)
    ft_note  = load_font(13)

    draw.text((W//2, 30), "Ціна однієї зміни — без SOLID vs з SOLID",
              font=ft_title, fill=ACCENT, anchor="mm")

    # Left: without SOLID
    draw.text((W//4, 70), "БЕЗ SOLID", font=ft_label, fill=RED, anchor="mm")

    bad_chain = [
        ("ClinicManager",    RED,    "Змінити формат звіту"),
        ("AppointmentLogic", YELLOW, "Зламалось бронювання"),
        ("BillingCalc",      RED,    "Збій у рахунках"),
        ("FileExporter",     YELLOW, "Файл не зберігається"),
        ("EmailSender",      RED,    "Email не надсилається"),
    ]
    bx, by = 90, 95
    bw, bh = 220, 46
    for i, (name, col, note) in enumerate(bad_chain):
        y = by + i * (bh + 14)
        rr(draw, [bx, y, bx+bw, y+bh], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((bx + bw//2, y + bh//2 - 8), name, font=ft_small, fill=col, anchor="mm")
        draw.text((bx + bw//2, y + bh//2 + 10), note, font=ft_note, fill=MUTED, anchor="mm")
        if i < len(bad_chain) - 1:
            ay = y + bh + 1
            draw.line([(bx + bw//2, ay), (bx + bw//2, ay + 12)], fill=RED, width=2)
            draw.polygon([(bx + bw//2 - 7, ay + 9),
                          (bx + bw//2 + 7, ay + 9),
                          (bx + bw//2, ay + 14)], fill=RED)

    draw.text((bx + bw//2, by + len(bad_chain) * (bh + 14) + 8),
              "Змінили 1 — поламали 5", font=ft_note, fill=RED, anchor="mm")

    # Right: with SOLID
    rx = W//2 + 40
    draw.text((rx + (W - rx)//2, 70), "З SOLID", font=ft_label, fill=ACCENT, anchor="mm")

    services = [
        ("ReportService",       ACCENT, "змінюємо тільки цей"),
        ("AppointmentService",  MUTED,  "нічого не знає про звіти"),
        ("BillingService",      MUTED,  "ізольований від решти"),
        ("FileService",         MUTED,  "ізольований від решти"),
        ("NotificationService", MUTED,  "ізольований від решти"),
    ]
    gw, gh = 230, 46
    for i, (name, col, note) in enumerate(services):
        y = by + i * (gh + 14)
        rr(draw, [rx, y, rx+gw, y+gh], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((rx + gw//2, y + gh//2 - 8), name, font=ft_small, fill=col, anchor="mm")
        draw.text((rx + gw//2, y + gh//2 + 10), note, font=ft_note, fill=MUTED, anchor="mm")

    draw.text((rx + gw//2, by + len(services) * (gh + 14) + 8),
              "Змінили 1 — все інше не зачеплено", font=ft_note, fill=ACCENT, anchor="mm")

    draw.line([(W//2, 60), (W//2, H - 20)], fill=LINE, width=1)

    save(img, "20-01", "change-cost.png")


# ═══════════════════════════════════════════════════════════════════════
# 20-02  before-srp.png  (FIX: annotation boxes must stay on screen)
# ═══════════════════════════════════════════════════════════════════════
def make_before_srp():
    W, H = 1000, 560
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(17, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 30),
              "До SRP — AppointmentManager: три відповідальності в одному класі",
              font=ft_title, fill=RED, anchor="mm")

    # Big central box — shifted right to leave room for annotations on left
    bx, by, bw, bh = 300, 65, 480, 440
    rr(draw, [bx, by, bx+bw, by+bh], radius=12, fill=PANEL, outline=RED, width=3)
    draw.text((bx + bw//2, by + 24), "AppointmentManager",
              font=ft_name, fill=RED, anchor="mm")

    sections = [
        ("Відповідальність 1: Бізнес-логіка", ACCENT, [
            "Book(patient, doctor, time)",
            "Cancel(appointmentId)",
            "Reschedule(id, newTime)",
            "IsSlotAvailable(doctor, time)",
        ]),
        ("Відповідальність 2: Збереження даних", BLUE, [
            "SaveToDatabase(appointment)",
            "LoadFromDatabase(id)",
            "UpdateStatus(id, status)",
            "DeleteRecord(id)",
        ]),
        ("Відповідальність 3: Сповіщення", YELLOW, [
            "SendEmailConfirmation(patient)",
            "SendSmsReminder(patient)",
            "NotifyDoctor(doctor)",
            "SendCancellationAlert(id)",
        ]),
    ]

    y_off = by + 50
    for title, col, methods in sections:
        hline(draw, bx+16, bx+bw-16, y_off, LINE)
        draw.text((bx + bw//2, y_off + 14), title, font=ft_note, fill=col, anchor="mm")
        for i, m in enumerate(methods):
            draw.text((bx + 30, y_off + 32 + i * 20), m, font=ft_meth, fill=MUTED)
        y_off += 140

    # Annotation boxes on the left — guaranteed visible: left-edge = 16px
    tw, th = 160, 60
    margin_left = 16
    annotations = [
        (by + 90,  "Змінюється коли\nзмінюється\nбізнес-логіка",   RED),
        (by + 230, "Змінюється коли\nзмінюється\nбаза даних",       RED),
        (by + 370, "Змінюється коли\nзмінюється\nканал сповіщень",  RED),
    ]
    for ay, text, col in annotations:
        box_x0 = margin_left
        box_x1 = margin_left + tw
        rr(draw, [box_x0, ay, box_x1, ay+th], radius=6, fill=PANEL, outline=col, width=1)
        for i, line in enumerate(text.split("\n")):
            draw.text((box_x0 + tw//2, ay + 10 + i * 17), line,
                      font=load_font(12), fill=col, anchor="mm")
        # connector: right edge of annotation box → left edge of central box
        draw.line([(box_x1, ay + th//2), (bx, ay + th//2)], fill=col, width=1)

    draw.text((W//2, H - 22),
              "Три причини для зміни — будь-яка правка ризикує зламати всі три частини",
              font=ft_note, fill=RED, anchor="mm")

    save(img, "20-02", "before-srp.png")


# ═══════════════════════════════════════════════════════════════════════
# 20-02  after-srp.png
# ═══════════════════════════════════════════════════════════════════════
def make_after_srp():
    W, H = 1050, 480
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(16, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "Після SRP — кожен клас має одну відповідальність",
              font=ft_title, fill=ACCENT, anchor="mm")

    boxes = [
        (40,  80, "AppointmentService",    ACCENT, [
            "Book(patient, doctor, time)",
            "Cancel(id)",
            "Reschedule(id, newTime)",
            "IsSlotAvailable(doc, time)",
        ], "Лише бізнес-логіка\nЗмінюється тільки\nколи змінюються правила"),
        (380, 80, "AppointmentRepository", BLUE, [
            "Save(appointment)",
            "GetById(id)",
            "UpdateStatus(id, status)",
            "Delete(id)",
        ], "Лише збереження\nЗмінюється тільки\nколи змінюється БД"),
        (720, 80, "AppointmentNotifier",   YELLOW, [
            "SendConfirmation(appt)",
            "SendReminder(appt)",
            "NotifyDoctor(appt)",
            "SendCancelAlert(appt)",
        ], "Лише сповіщення\nЗмінюється тільки\nколи змінюється канал"),
    ]

    bw, bh = 280, 210
    for bx, by, name, col, methods, note in boxes:
        rr(draw, [bx, by, bx+bw, by+bh], radius=10, fill=PANEL, outline=col, width=2)
        draw.text((bx + bw//2, by + 22), name, font=ft_name, fill=col, anchor="mm")
        hline(draw, bx+14, bx+bw-14, by+40, LINE)
        for i, m in enumerate(methods):
            draw.text((bx + 14, by + 52 + i * 22), m, font=ft_meth, fill=MUTED)
        ny = by + bh + 14
        for j, line in enumerate(note.split("\n")):
            draw.text((bx + bw//2, ny + j * 18), line,
                      font=load_font(12), fill=col, anchor="mm")

    # Arrows between boxes
    arrow(draw, 40+bw, 80+bh//2, 380, 80+bh//2, LINE, head=7)
    arrow(draw, 380+bw, 80+bh//2, 720, 80+bh//2, LINE, head=7)

    draw.text((W//2, H - 22),
              "Одна причина для зміни — кожен клас можна змінювати й тестувати незалежно",
              font=ft_note, fill=ACCENT, anchor="mm")

    save(img, "20-02", "after-srp.png")


# ═══════════════════════════════════════════════════════════════════════
# 20-03  before-ocp.png
# ═══════════════════════════════════════════════════════════════════════
def make_before_ocp():
    W, H = 1000, 540
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(16, bold=True)
    ft_code  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "До OCP — switch-ланцюг вимагає зміни існуючого коду",
              font=ft_title, fill=RED, anchor="mm")

    # CostCalculator box with switch
    bx, by, bw, bh = 60, 65, 420, 350
    rr(draw, [bx, by, bx+bw, by+bh], radius=10, fill=PANEL, outline=RED, width=2)
    draw.text((bx + bw//2, by + 22), "CostCalculator", font=ft_name, fill=RED, anchor="mm")
    hline(draw, bx+14, bx+bw-14, by+40, LINE)

    code_lines = [
        "Calculate(type, basePrice):",
        "  switch(type)",
        "  {",
        '    case "Standard":',
        "      return basePrice;",
        '    case "Urgent":',
        "      return basePrice * 1.5;",
        '    case "VIP":',
        "      return basePrice * 2.0;",
        "    // додати новий тип?",
        "    // ЗМІНИТИ цей метод!",
        "  }",
    ]
    for i, line in enumerate(code_lines):
        col = RED if "ЗМІНИТИ" in line else (YELLOW if "//" in line else MUTED)
        draw.text((bx + 18, by + 54 + i * 22), line, font=ft_code, fill=col)

    # Arrow: new type triggers change
    ax, ay = bx + bw, by + bh//2
    arrow(draw, ax + 160, ay, ax + 10, ay, RED, head=8)
    draw.text((ax + 90, ay - 20), "Новий тип", font=ft_note, fill=YELLOW, anchor="mm")
    draw.text((ax + 90, ay + 8), "AppointmentType", font=ft_note, fill=YELLOW, anchor="mm")

    # Annotation boxes: problems
    problems = [
        (bx + bw + 200, by + 60,  "Порушення OCP",     "Модифікуємо", "існуючий код"),
        (bx + bw + 200, by + 160, "Ризик регресії",    "Кожна зміна", "зачіпає всіх"),
        (bx + bw + 200, by + 260, "Немає розширення",  "Новий тип =", "новий switch-case"),
    ]
    pw, ph = 190, 64
    for px, py, title, l1, l2 in problems:
        rr(draw, [px, py, px+pw, py+ph], radius=8, fill=PANEL, outline=RED, width=1)
        draw.text((px + pw//2, py + 14), title, font=load_font(13, bold=True), fill=RED, anchor="mm")
        draw.text((px + pw//2, py + 34), l1, font=ft_note, fill=MUTED, anchor="mm")
        draw.text((px + pw//2, py + 50), l2, font=ft_note, fill=MUTED, anchor="mm")

    draw.text((W//2, H - 22),
              "Будь-яке розширення вимагає модифікації класу — порушення принципу OCP",
              font=ft_note, fill=RED, anchor="mm")

    save(img, "20-03", "before-ocp.png")


# ═══════════════════════════════════════════════════════════════════════
# 20-03  after-ocp.png
# ═══════════════════════════════════════════════════════════════════════
def make_after_ocp():
    W, H = 1100, 520
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(15, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "Після OCP — новий тип = новий клас, CostCalculator не чіпаємо",
              font=ft_title, fill=ACCENT, anchor="mm")

    # Interface box
    ix, iy, iw, ih = 380, 70, 340, 90
    rr(draw, [ix, iy, ix+iw, iy+ih], radius=10, fill=PANEL, outline=ACCENT, width=2)
    draw.text((ix + iw//2, iy + 18), "<<interface>>", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((ix + iw//2, iy + 38), "IAppointmentType", font=ft_name, fill=ACCENT, anchor="mm")
    hline(draw, ix+14, ix+iw-14, iy+58, LINE)
    draw.text((ix + iw//2, iy + 72), "GetCost(basePrice): decimal", font=ft_meth, fill=MUTED, anchor="mm")

    # Concrete classes below
    impl_classes = [
        (60,  260, "StandardAppointment", MUTED,  ["GetCost(p) => p"]),
        (330, 260, "UrgentAppointment",   YELLOW, ["GetCost(p) => p * 1.5m"]),
        (600, 260, "VIPAppointment",      PURPLE, ["GetCost(p) => p * 2.0m"]),
        (870, 260, "NightShiftAppt",      BLUE,   ["GetCost(p) => p * 1.8m", "(новий тип!)"]),
    ]
    cw, ch = 200, 90
    for cx2, cy2, name, col, meths in impl_classes:
        rr(draw, [cx2, cy2, cx2+cw, cy2+ch], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((cx2 + cw//2, cy2 + 20), name, font=ft_name, fill=col, anchor="mm")
        hline(draw, cx2+12, cx2+cw-12, cy2+36, LINE)
        for j, m in enumerate(meths):
            draw.text((cx2 + cw//2, cy2 + 52 + j * 20), m, font=ft_meth, fill=MUTED, anchor="mm")
        # Arrow up to interface
        tx = cx2 + cw//2
        arrow(draw, tx, cy2, tx, iy + ih + 4, MUTED, w=1, head=6)

    # CostCalculator depends on interface only
    ccx, ccy, ccw, cch = 380, 420, 340, 70
    rr(draw, [ccx, ccy, ccx+ccw, ccy+cch], radius=8, fill=PANEL, outline=ACCENT, width=2)
    draw.text((ccx + ccw//2, ccy + 20), "CostCalculator", font=ft_name, fill=ACCENT, anchor="mm")
    draw.text((ccx + ccw//2, ccy + 46), "Calculate(IAppointmentType t, decimal p)", font=ft_meth, fill=MUTED, anchor="mm")
    arrow(draw, ccx + ccw//2, ccy, ccx + ccw//2, iy + ih + 4, ACCENT, head=7)

    draw.text((W//2, H - 22),
              "Новий тип — новий клас. CostCalculator закритий для змін, відкритий для розширення",
              font=ft_note, fill=ACCENT, anchor="mm")

    save(img, "20-03", "after-ocp.png")


# ═══════════════════════════════════════════════════════════════════════
# 20-04  lsp-violation.png  (FIX: replace X-mark with [X])
# ═══════════════════════════════════════════════════════════════════════
def make_lsp_violation():
    W, H = 1000, 540
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(15, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "Порушення LSP — ReadOnlyRecord кидає виняток де не очікується",
              font=ft_title, fill=RED, anchor="mm")

    # Base class
    bx, by, bw, bh = 330, 70, 340, 110
    rr(draw, [bx, by, bx+bw, by+bh], radius=10, fill=PANEL, outline=ACCENT, width=2)
    draw.text((bx + bw//2, by + 20), "MedicalRecord", font=ft_name, fill=ACCENT, anchor="mm")
    hline(draw, bx+14, bx+bw-14, by+38, LINE)
    for i, m in enumerate(["UpdateDiagnosis(text)", "AddNote(text)", "GetSummary(): string"]):
        draw.text((bx + bw//2, by + 54 + i * 20), m, font=ft_meth, fill=MUTED, anchor="mm")

    # ReadOnlyRecord (violation)
    rx, ry, rw, rh = 550, 250, 360, 130
    rr(draw, [rx, ry, rx+rw, ry+rh], radius=10, fill=PANEL, outline=RED, width=2)
    draw.text((rx + rw//2, ry + 20), "ReadOnlyRecord", font=ft_name, fill=RED, anchor="mm")
    hline(draw, rx+14, rx+rw-14, ry+38, LINE)
    violation_lines = [
        "UpdateDiagnosis(text):",
        "  throw NotSupportedException",
        "AddNote(text):",
        "  throw NotSupportedException",
    ]
    for i, line in enumerate(violation_lines):
        col = RED if "throw" in line else MUTED
        draw.text((rx + rw//2, ry + 54 + i * 18), line, font=ft_meth, fill=col, anchor="mm")

    # Correct subclass
    cx2, cy2, cw2, ch2 = 90, 250, 340, 110
    rr(draw, [cx2, cy2, cx2+cw2, cy2+ch2], radius=10, fill=PANEL, outline=ACCENT, width=2)
    draw.text((cx2 + cw2//2, cy2 + 20), "DetailedRecord", font=ft_name, fill=ACCENT, anchor="mm")
    hline(draw, cx2+14, cx2+cw2-14, cy2+38, LINE)
    for i, m in enumerate(["UpdateDiagnosis(text)", "AddNote(text)", "+ AddAttachment(file)"]):
        draw.text((cx2 + cw2//2, cy2 + 54 + i * 20), m, font=ft_meth, fill=MUTED, anchor="mm")

    # Arrows from base to subclasses
    arrow(draw, bx + bw//2 - 80, by + bh, cx2 + cw2//2, cy2, MUTED, head=7)
    arrow(draw, bx + bw//2 + 80, by + bh, rx + rw//2, ry, RED, head=7)

    # Client code
    kx, ky, kw, kh = 330, 430, 340, 60
    rr(draw, [kx, ky, kx+kw, ky+kh], radius=8, fill=PANEL, outline=YELLOW, width=2)
    draw.text((kx + kw//2, ky + 16), "ProcessRecord(MedicalRecord r)", font=ft_meth, fill=YELLOW, anchor="mm")
    draw.text((kx + kw//2, ky + 38), "r.UpdateDiagnosis(...)  // OK для базового", font=ft_meth, fill=MUTED, anchor="mm")

    # Problem annotation
    draw.text((rx + rw//2, ry + rh + 18), "[X] Передали ReadOnlyRecord — Exception!", font=ft_note, fill=RED, anchor="mm")
    draw.text((cx2 + cw2//2, cy2 + ch2 + 18), "[OK] DetailedRecord — працює коректно", font=ft_note, fill=ACCENT, anchor="mm")

    draw.text((W//2, H - 22),
              "Якщо підтип кидає виняток замість виконання — це порушення LSP",
              font=ft_note, fill=RED, anchor="mm")

    save(img, "20-04", "lsp-violation.png")


# ═══════════════════════════════════════════════════════════════════════
# 20-04  lsp-correct.png  (FIX: replace check-mark with [OK])
# ═══════════════════════════════════════════════════════════════════════
def make_lsp_correct():
    W, H = 1000, 520
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(15, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "Правильна ієрархія — підкласи розширюють, не звужують контракт",
              font=ft_title, fill=ACCENT, anchor="mm")

    # Base interface
    ix, iy, iw, ih = 330, 65, 340, 100
    rr(draw, [ix, iy, ix+iw, iy+ih], radius=10, fill=PANEL, outline=ACCENT, width=2)
    draw.text((ix + iw//2, iy + 16), "<<interface>>", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((ix + iw//2, iy + 36), "IMedicalRecord", font=ft_name, fill=ACCENT, anchor="mm")
    hline(draw, ix+14, ix+iw-14, iy+56, LINE)
    draw.text((ix + iw//2, iy + 72), "GetSummary(): string", font=ft_meth, fill=MUTED, anchor="mm")

    # IEditableMedicalRecord
    ex, ey, ew, eh = 330, 220, 340, 110
    rr(draw, [ex, ey, ex+ew, ey+eh], radius=10, fill=PANEL, outline=BLUE, width=2)
    draw.text((ex + ew//2, ey + 16), "<<interface>>", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((ex + ew//2, ey + 36), "IEditableMedicalRecord", font=ft_name, fill=BLUE, anchor="mm")
    hline(draw, ex+14, ex+ew-14, ey+56, LINE)
    for i, m in enumerate(["UpdateDiagnosis(text)", "AddNote(text)"]):
        draw.text((ex + ew//2, ey + 70 + i * 20), m, font=ft_meth, fill=MUTED, anchor="mm")
    arrow(draw, ex + ew//2, ey, ix + iw//2, iy + ih, MUTED, head=6)

    # Concrete: ReadOnlyRecord implements only IMedicalRecord
    rx, ry, rw, rh = 60, 390, 280, 90
    rr(draw, [rx, ry, rx+rw, ry+rh], radius=8, fill=PANEL, outline=MUTED, width=2)
    draw.text((rx + rw//2, ry + 20), "ReadOnlyRecord", font=ft_name, fill=MUTED, anchor="mm")
    hline(draw, rx+12, rx+rw-12, ry+38, LINE)
    draw.text((rx + rw//2, ry + 54), "GetSummary(): string", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((rx + rw//2, ry + 76), "[OK] Не реалізує IEditable", font=ft_note, fill=ACCENT, anchor="mm")
    arrow(draw, rx + rw//2, ry, ix + iw//2 - 60, iy + ih, MUTED, head=6)

    # Concrete: DetailedRecord implements both
    dx, dy, dw, dh = 660, 390, 280, 90
    rr(draw, [dx, dy, dx+dw, dy+dh], radius=8, fill=PANEL, outline=ACCENT, width=2)
    draw.text((dx + dw//2, dy + 20), "DetailedRecord", font=ft_name, fill=ACCENT, anchor="mm")
    hline(draw, dx+12, dx+dw-12, dy+38, LINE)
    draw.text((dx + dw//2, dy + 54), "GetSummary(), UpdateDiagnosis()", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((dx + dw//2, dy + 76), "[OK] Контракт виконано повністю", font=ft_note, fill=ACCENT, anchor="mm")
    arrow(draw, dx + dw//2, dy, ex + ew//2, ey + eh, MUTED, head=6)

    draw.text((W//2, H - 22),
              "Кожен клас реалізує рівно ті інтерфейси, контракт яких може виконати",
              font=ft_note, fill=ACCENT, anchor="mm")

    save(img, "20-04", "lsp-correct.png")


# ═══════════════════════════════════════════════════════════════════════
# 20-05  before-isp.png  (FIX: [X] замість ✗, H=580 щоб не клипало)
# ═══════════════════════════════════════════════════════════════════════
def make_before_isp():
    W, H = 1100, 580
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(15, bold=True)
    ft_meth  = load_font(12)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "До ISP — «жирний» інтерфейс примушує реалізовувати непотрібне",
              font=ft_title, fill=RED, anchor="mm")

    # Fat interface
    fx, fy, fw, fh = 350, 60, 400, 220
    rr(draw, [fx, fy, fx+fw, fy+fh], radius=10, fill=PANEL, outline=RED, width=2)
    draw.text((fx + fw//2, fy + 16), "<<interface>>", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((fx + fw//2, fy + 36), "IClinicService", font=ft_name, fill=RED, anchor="mm")
    hline(draw, fx+14, fx+fw-14, fy+56, LINE)
    all_methods = [
        "RegisterPatient(patient)",
        "GetPatientHistory(id)",
        "BookAppointment(appt)",
        "CancelAppointment(id)",
        "GenerateReport(period)",
        "ExportToPdf(report)",
        "SendNotification(msg)",
    ]
    for i, m in enumerate(all_methods):
        draw.text((fx + fw//2, fy + 72 + i * 22), m, font=ft_meth, fill=MUTED, anchor="mm")

    # Implementors
    implementors = [
        (30,  360, "PatientPortal",    ACCENT, [
            "[OK] RegisterPatient",
            "[OK] GetPatientHistory",
            "[X]  BookAppointment",
            "[X]  GenerateReport",
            "[X]  ExportToPdf",
            "[X]  SendNotification",
        ]),
        (380, 360, "SchedulerService", YELLOW, [
            "[X]  RegisterPatient",
            "[X]  GetPatientHistory",
            "[OK] BookAppointment",
            "[OK] CancelAppointment",
            "[X]  GenerateReport",
            "[X]  SendNotification",
        ]),
        (730, 360, "ReportingService", BLUE, [
            "[X]  RegisterPatient",
            "[X]  BookAppointment",
            "[X]  CancelAppointment",
            "[OK] GenerateReport",
            "[OK] ExportToPdf",
            "[X]  SendNotification",
        ]),
    ]
    iw2, ih2 = 310, 165
    for ix2, iy2, name, col, meths in implementors:
        rr(draw, [ix2, iy2, ix2+iw2, iy2+ih2], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((ix2 + iw2//2, iy2 + 18), name, font=ft_name, fill=col, anchor="mm")
        hline(draw, ix2+12, ix2+iw2-12, iy2+34, LINE)
        for j, m in enumerate(meths):
            mcol = MUTED if "[OK]" in m else RED
            draw.text((ix2 + 14, iy2 + 48 + j * 20), m, font=ft_meth, fill=mcol)
        arrow(draw, ix2 + iw2//2, iy2, fx + fw//2, fy + fh, MUTED, head=6)

    draw.text((W//2, H - 22),
              "[X] позначає методи, що не потрібні — але клас зобов'язаний їх реалізувати",
              font=ft_note, fill=RED, anchor="mm")

    save(img, "20-05", "before-isp.png")


# ═══════════════════════════════════════════════════════════════════════
# 20-05  after-isp.png  (FIX: [OK] замість ✓)
# ═══════════════════════════════════════════════════════════════════════
def make_after_isp():
    W, H = 1100, 540
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(14, bold=True)
    ft_meth  = load_font(12)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "Після ISP — маленькі інтерфейси, кожен клієнт бере лише потрібне",
              font=ft_title, fill=ACCENT, anchor="mm")

    # Three small interfaces
    ifaces = [
        (60,  70, "IPatientService",     ACCENT, ["RegisterPatient(p)", "GetPatientHistory(id)"]),
        (410, 70, "IAppointmentService", YELLOW, ["BookAppointment(appt)", "CancelAppointment(id)"]),
        (760, 70, "IReportService",      BLUE,   ["GenerateReport(period)", "ExportToPdf(report)"]),
    ]
    iw2, ih2 = 280, 110
    for ix2, iy2, name, col, meths in ifaces:
        rr(draw, [ix2, iy2, ix2+iw2, iy2+ih2], radius=10, fill=PANEL, outline=col, width=2)
        draw.text((ix2 + iw2//2, iy2 + 16), "<<interface>>", font=ft_meth, fill=MUTED, anchor="mm")
        draw.text((ix2 + iw2//2, iy2 + 36), name, font=ft_name, fill=col, anchor="mm")
        hline(draw, ix2+12, ix2+iw2-12, iy2+56, LINE)
        for j, m in enumerate(meths):
            draw.text((ix2 + iw2//2, iy2 + 72 + j * 20), m, font=ft_meth, fill=MUTED, anchor="mm")

    # Implementors
    implementors = [
        (60,  280, "PatientPortal",    ACCENT, ["[OK] IPatientService"],   [0]),
        (410, 280, "SchedulerService", YELLOW, ["[OK] IAppointmentService"], [1]),
        (760, 280, "ReportingService", BLUE,   ["[OK] IReportService"],    [2]),
    ]
    cw, ch = 280, 80
    for cx2, cy2, name, col, labels, iface_indices in implementors:
        rr(draw, [cx2, cy2, cx2+cw, cy2+ch], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((cx2 + cw//2, cy2 + 18), name, font=ft_name, fill=col, anchor="mm")
        hline(draw, cx2+12, cx2+cw-12, cy2+34, LINE)
        for j, lb in enumerate(labels):
            draw.text((cx2 + cw//2, cy2 + 50 + j * 20), lb, font=ft_meth, fill=ACCENT, anchor="mm")
        for idx in iface_indices:
            ix3, iy3 = ifaces[idx][0], ifaces[idx][1]
            arrow(draw, cx2 + cw//2, cy2, ix3 + iw2//2, iy3 + ih2, MUTED, head=6)

    # ClinicFacade implements all
    ffx, ffy, ffw, ffh = 350, 430, 400, 70
    rr(draw, [ffx, ffy, ffx+ffw, ffy+ffh], radius=8, fill=PANEL, outline=MUTED, width=2)
    draw.text((ffx + ffw//2, ffy + 18), "ClinicFacade", font=ft_name, fill=MUTED, anchor="mm")
    draw.text((ffx + ffw//2, ffy + 46),
              "[OK] IPatientService + IAppointmentService + IReportService",
              font=ft_meth, fill=ACCENT, anchor="mm")
    for idx in range(3):
        ix3, iy3 = ifaces[idx][0], ifaces[idx][1]
        arrow(draw, ffx + ffw//2, ffy, ix3 + iw2//2, iy3 + ih2, MUTED, head=5)

    draw.text((W//2, H - 22),
              "Кожен клієнт залежить тільки від тих методів, які йому справді потрібні",
              font=ft_note, fill=ACCENT, anchor="mm")

    save(img, "20-05", "after-isp.png")


# ═══════════════════════════════════════════════════════════════════════
# 20-06  dip-overview.png  (FIX: [X] замість ✗)
# ═══════════════════════════════════════════════════════════════════════
def make_dip_overview():
    W, H = 1100, 560
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(15, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W//2, 28), "DIP — інверсія напряму залежностей через абстракцію",
              font=ft_title, fill=ACCENT, anchor="mm")

    # ── Left side: BEFORE (violation) ──────────────────────────────────
    draw.text((200, 68), "БЕЗ DIP", font=load_font(15, bold=True), fill=RED, anchor="mm")

    # AppointmentService (high-level)
    rr(draw, [30, 90, 370, 160], radius=8, fill=PANEL, outline=YELLOW, width=2)
    draw.text((200, 117), "AppointmentService", font=ft_name, fill=YELLOW, anchor="mm")
    draw.text((200, 143), "(high-level module)", font=ft_meth, fill=MUTED, anchor="mm")

    # Concrete SqlRepository
    rr(draw, [30, 230, 370, 300], radius=8, fill=PANEL, outline=RED, width=2)
    draw.text((200, 257), "SqlAppointmentRepository", font=ft_name, fill=RED, anchor="mm")
    draw.text((200, 280), "(concrete class, low-level)", font=ft_meth, fill=MUTED, anchor="mm")

    # Direct dependency arrow
    arrow(draw, 200, 160, 200, 230, RED, w=2, head=8)
    draw.text((248, 196), "залежить від", font=ft_note, fill=RED)
    draw.text((248, 212), "конкретного класу", font=ft_note, fill=RED)

    # Problem label
    rr(draw, [30, 330, 370, 380], radius=6, fill=PANEL, outline=RED, width=1)
    draw.text((200, 345), "[X] Замінити SQL на Mongo?", font=ft_note, fill=RED, anchor="mm")
    draw.text((200, 365), "      Треба міняти Service!", font=ft_note, fill=RED, anchor="mm")

    # ── Divider ──────────────────────────────────────────────────────
    draw.line([(W//2, 60), (W//2, H - 30)], fill=LINE, width=1)

    # ── Right side: AFTER (DIP) ──────────────────────────────────────
    draw.text((880, 68), "З DIP", font=load_font(15, bold=True), fill=ACCENT, anchor="mm")

    # AppointmentService
    rr(draw, [600, 90, 1060, 160], radius=8, fill=PANEL, outline=YELLOW, width=2)
    draw.text((830, 117), "AppointmentService", font=ft_name, fill=YELLOW, anchor="mm")
    draw.text((830, 143), "залежить від IAppointmentRepository", font=ft_meth, fill=MUTED, anchor="mm")

    # Interface
    rr(draw, [650, 230, 1010, 300], radius=8, fill=PANEL, outline=ACCENT, width=2)
    draw.text((830, 248), "<<interface>>", font=ft_meth, fill=MUTED, anchor="mm")
    draw.text((830, 272), "IAppointmentRepository", font=ft_name, fill=ACCENT, anchor="mm")

    arrow(draw, 830, 160, 830, 230, ACCENT, w=2, head=8)
    draw.text((840, 190), "залежить від абстракції", font=ft_note, fill=ACCENT)

    # Concrete implementations
    impls = [
        (600, 360, "SqlRepository",   BLUE),
        (830, 360, "MongoRepository", YELLOW),
        (1060 - 20, 360, "+InMemory...",  MUTED),
    ]
    for ix3, iy3, name, col in impls:
        if ix3 + 180 > W - 20:
            continue
        rr(draw, [ix3, iy3, ix3+190, iy3+70], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((ix3 + 95, iy3 + 35), name, font=ft_name, fill=col, anchor="mm")
        arrow(draw, ix3 + 95, iy3, ix3 + 95 - (ix3 + 95 - 830), 300, MUTED, head=5)

    # OK label
    rr(draw, [610, 460, 1050, 510], radius=6, fill=PANEL, outline=ACCENT, width=1)
    draw.text((830, 478), "[OK] Замінити SQL на Mongo?", font=ft_note, fill=ACCENT, anchor="mm")
    draw.text((830, 498), "      Тільки новий клас, Service не чіпаємо!", font=ft_note, fill=ACCENT, anchor="mm")

    draw.text((W//2, H - 18),
              "Високорівневі модулі залежать від абстракцій — конкретика підставляється ззовні",
              font=ft_note, fill=ACCENT, anchor="mm")

    save(img, "20-06", "dip-overview.png")


# ═══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    make_god_class()
    make_solid_overview()
    make_change_cost()
    make_before_srp()
    make_after_srp()
    make_before_ocp()
    make_after_ocp()
    make_lsp_violation()
    make_lsp_correct()
    make_before_isp()
    make_after_isp()
    make_dip_overview()
    print("\nAll diagrams regenerated successfully.")
