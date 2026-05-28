"""
Diagrams for section 20.2 — SRP
Palette: BG=#111413, ACCENT=#76c7ad, TEXT=#e5e9e7, MUTED=#a1aaa6, LINE=#2c3531, PANEL=#191e1c
"""
from PIL import Image, ImageDraw, ImageFont
import os

BG     = "#111413"
ACCENT = "#76c7ad"
TEXT   = "#e5e9e7"
MUTED  = "#a1aaa6"
LINE   = "#2c3531"
PANEL  = "#191e1c"
RED    = "#e07070"
YELLOW = "#d4b96a"
BLUE   = "#6a9fd4"

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

def arrow(draw, x1, y1, x2, y2, col, w=2, head=8):
    draw.line([(x1, y1), (x2, y2)], fill=col, width=w)
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    draw.polygon([
        (x2, y2),
        (int(x2 - head * math.cos(angle - 0.4)), int(y2 - head * math.sin(angle - 0.4))),
        (int(x2 - head * math.cos(angle + 0.4)), int(y2 - head * math.sin(angle + 0.4))),
    ], fill=col)

# ─── Diagram 1: Before SRP — один великий клас ───────────────────────
def make_before_srp():
    W, H = 1000, 560
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(17, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W // 2, 30), "До SRP — AppointmentManager: три відповідальності в одному класі",
              font=ft_title, fill=RED, anchor="mm")

    # Big central box
    bx, by, bw, bh = 260, 65, 480, 440
    draw_rounded_rect(draw, [bx, by, bx + bw, by + bh], radius=12,
                      fill=PANEL, outline=RED, width=3)
    draw.text((bx + bw // 2, by + 24), "AppointmentManager", font=ft_name, fill=RED, anchor="mm")

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
        draw.line([(bx + 16, y_off), (bx + bw - 16, y_off)], fill=LINE, width=1)
        draw.text((bx + bw // 2, y_off + 14), title, font=ft_note, fill=col, anchor="mm")
        for i, m in enumerate(methods):
            draw.text((bx + 30, y_off + 32 + i * 20), m, font=ft_meth, fill=MUTED)
        y_off += 140

    # Side annotation boxes
    annotations = [
        (bx - 10, by + 90,  "Змінюється\nколи змінюється\nбізнес-логіка",    RED),
        (bx - 10, by + 230, "Змінюється\nколи змінюється\nбаза даних",        RED),
        (bx - 10, by + 370, "Змінюється\nколи змінюється\nканал сповіщень",   RED),
    ]
    for ax, ay, text, col in annotations:
        tw, th = 150, 60
        draw_rounded_rect(draw, [ax - tw - 8, ay, ax - tw - 8 + tw, ay + th],
                          radius=6, fill=PANEL, outline=col, width=1)
        for i, line in enumerate(text.split("\n")):
            draw.text((ax - tw - 8 + tw // 2, ay + 12 + i * 16), line,
                      font=load_font(12), fill=col, anchor="mm")
        draw.line([(ax - 8, ay + th // 2), (ax, ay + th // 2)], fill=col, width=1)

    draw.text((W // 2, H - 22),
              "Три причини для зміни → будь-яка правка ризикує зламати всі три частини",
              font=ft_note, fill=RED, anchor="mm")

    img.save(os.path.join(OUT_DIR, "before-srp.png"))
    print("Saved before-srp.png")


# ─── Diagram 2: After SRP — три окремі класи ─────────────────────────
def make_after_srp():
    W, H = 1050, 480
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    ft_title = load_font(20, bold=True)
    ft_name  = load_font(16, bold=True)
    ft_meth  = load_font(13)
    ft_note  = load_font(13)

    draw.text((W // 2, 28), "Після SRP — кожен клас має одну відповідальність",
              font=ft_title, fill=ACCENT, anchor="mm")

    boxes = [
        (60,   80, "AppointmentService",  ACCENT, [
            "Book(patient, doctor, time)",
            "Cancel(id)",
            "Reschedule(id, newTime)",
            "IsSlotAvailable(doc, time)",
        ], "Лише бізнес-логіка\nЗмінюється тільки\nколи змінюються правила"),
        (400,  80, "AppointmentRepository", BLUE, [
            "Save(appointment)",
            "GetById(id)",
            "UpdateStatus(id, status)",
            "Delete(id)",
        ], "Лише збереження\nЗмінюється тільки\nколи змінюється БД"),
        (740,  80, "AppointmentNotifier", YELLOW, [
            "SendConfirmation(appt)",
            "SendReminder(appt)",
            "NotifyDoctor(appt)",
            "SendCancelAlert(appt)",
        ], "Лише сповіщення\nЗмінюється тільки\nколи змінюється канал"),
    ]

    bw, bh = 270, 210
    for bx, by, name, col, methods, note in boxes:
        draw_rounded_rect(draw, [bx, by, bx + bw, by + bh], radius=10,
                          fill=PANEL, outline=col, width=2)
        draw.text((bx + bw // 2, by + 22), name, font=ft_name, fill=col, anchor="mm")
        draw.line([(bx + 14, by + 40), (bx + bw - 14, by + 40)], fill=LINE, width=1)
        for i, m in enumerate(methods):
            draw.text((bx + 14, by + 52 + i * 22), m, font=ft_meth, fill=MUTED)

        # Note below
        ny = by + bh + 14
        for j, line in enumerate(note.split("\n")):
            draw.text((bx + bw // 2, ny + j * 18), line,
                      font=load_font(12), fill=col, anchor="mm")

    # Connecting arrow: AppointmentService → Repository + Notifier
    ax1, ay1 = 60 + bw, 80 + bh // 2
    ax2, ay2 = 400, 80 + bh // 2
    arrow(draw, ax1, ay1, ax2, ay2, LINE, head=7)

    ax3, ay3 = 400 + bw, 80 + bh // 2
    ax4, ay4 = 740, 80 + bh // 2
    arrow(draw, ax3, ay3, ax4, ay4, LINE, head=7)

    draw.text((W // 2, H - 22),
              "Одна причина для зміни → кожен клас можна змінювати, тестувати і розгортати незалежно",
              font=ft_note, fill=ACCENT, anchor="mm")

    img.save(os.path.join(OUT_DIR, "after-srp.png"))
    print("Saved after-srp.png")


if __name__ == "__main__":
    make_before_srp()
    make_after_srp()
    print("All diagrams done.")
