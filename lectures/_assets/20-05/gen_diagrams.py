"""
Diagrams for section 20.5 — ISP
Palette: BG=#111413, ACCENT=#76c7ad, TEXT=#e5e9e7, MUTED=#a1aaa6, LINE=#2c3531, PANEL=#191e1c
Notes: Use [OK] / [X] — Unicode check/cross marks not supported in Segoe UI
       before-isp: H=580 so bottom text is not clipped
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


# ─── Diagram 1: Before ISP ───────────────────────────────────────────
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

    # Fat interface box
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

    # Three implementors
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

    img.save(os.path.join(OUT_DIR, "before-isp.png"))
    print("Saved before-isp.png")


# ─── Diagram 2: After ISP ────────────────────────────────────────────
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

    # Three focused interfaces
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

    # Three focused implementors
    implementors = [
        (60,  280, "PatientPortal",    ACCENT, "[OK] IPatientService",     [0]),
        (410, 280, "SchedulerService", YELLOW, "[OK] IAppointmentService", [1]),
        (760, 280, "ReportingService", BLUE,   "[OK] IReportService",      [2]),
    ]
    cw, ch = 280, 80
    for cx2, cy2, name, col, label, iface_indices in implementors:
        rr(draw, [cx2, cy2, cx2+cw, cy2+ch], radius=8, fill=PANEL, outline=col, width=2)
        draw.text((cx2 + cw//2, cy2 + 18), name, font=ft_name, fill=col, anchor="mm")
        hline(draw, cx2+12, cx2+cw-12, cy2+34, LINE)
        draw.text((cx2 + cw//2, cy2 + 55), label, font=ft_meth, fill=ACCENT, anchor="mm")
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

    img.save(os.path.join(OUT_DIR, "after-isp.png"))
    print("Saved after-isp.png")


if __name__ == "__main__":
    make_before_isp()
    make_after_isp()
    print("All diagrams done.")
