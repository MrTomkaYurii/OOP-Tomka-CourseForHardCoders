"""
Diagrams for section 20.2 — SRP
Palette: BG=#111413, ACCENT=#76c7ad, TEXT=#e5e9e7, MUTED=#a1aaa6, LINE=#2c3531, PANEL=#191e1c
Notes:
  - before-srp: annotation boxes anchored at left margin 16px (never off-screen)
  - No Unicode check/cross marks — use [OK] / [X]
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

OUT_DIR = os.path.dirname(__file__)

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

def hline(draw, x0, x1, y, col=LINE, width=1):
    draw.line([(x0, y), (x1, y)], fill=col, width=width)

def arrow(draw, x1, y1, x2, y2, col, w=2, head=8):
    draw.line([(x1, y1), (x2, y2)], fill=col, width=w)
    angle = math.atan2(y2 - y1, x2 - x1)
    draw.polygon([
        (x2, y2),
        (int(x2 - head * math.cos(angle - 0.4)), int(y2 - head * math.sin(angle - 0.4))),
        (int(x2 - head * math.cos(angle + 0.4)), int(y2 - head * math.sin(angle + 0.4))),
    ], fill=col)


# ─── Diagram 1: Before SRP ───────────────────────────────────────────
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

    # Central box — shifted right to leave room for left annotations
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

    # Annotation boxes — left margin guaranteed >= 16px
    tw, th = 160, 60
    margin_left = 16
    annotations = [
        (by + 90,  "Змінюється коли\nзмінюється\nбізнес-логіка",   RED),
        (by + 230, "Змінюється коли\nзмінюється\nбаза даних",       RED),
        (by + 370, "Змінюється коли\nзмінюється\nканал сповіщень",  RED),
    ]
    for ay, text, col in annotations:
        box_x0, box_x1 = margin_left, margin_left + tw
        rr(draw, [box_x0, ay, box_x1, ay+th], radius=6, fill=PANEL, outline=col, width=1)
        for i, line in enumerate(text.split("\n")):
            draw.text((box_x0 + tw//2, ay + 10 + i * 17), line,
                      font=load_font(12), fill=col, anchor="mm")
        # connector: right edge of box → left edge of central class
        draw.line([(box_x1, ay + th//2), (bx, ay + th//2)], fill=col, width=1)

    draw.text((W//2, H - 22),
              "Три причини для зміни — будь-яка правка ризикує зламати всі три частини",
              font=ft_note, fill=RED, anchor="mm")

    img.save(os.path.join(OUT_DIR, "before-srp.png"))
    print("Saved before-srp.png")


# ─── Diagram 2: After SRP ────────────────────────────────────────────
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

    arrow(draw, 40+bw, 80+bh//2, 380, 80+bh//2, LINE, head=7)
    arrow(draw, 380+bw, 80+bh//2, 720, 80+bh//2, LINE, head=7)

    draw.text((W//2, H - 22),
              "Одна причина для зміни — кожен клас можна змінювати й тестувати незалежно",
              font=ft_note, fill=ACCENT, anchor="mm")

    img.save(os.path.join(OUT_DIR, "after-srp.png"))
    print("Saved after-srp.png")


if __name__ == "__main__":
    make_before_srp()
    make_after_srp()
    print("All diagrams done.")
