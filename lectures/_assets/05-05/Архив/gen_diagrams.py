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

def draw_custom_exception():
    W, H = 880, 520
    img = Image.new("RGB", (W, H), hex_to_rgb(BG))
    d = ImageDraw.Draw(img)

    title_f = load_font(18, bold=True)
    label_f = load_font(14, bold=True)
    code_f  = load_font(12)
    note_f  = load_font(11)

    d.text((W // 2, 22), "Власні класи винятків: ієрархія", font=title_f,
           fill=hex_to_rgb(ACCENT), anchor="mm")

    # System.Exception at top
    bx, by, bw, bh = (W - 200) // 2, 50, 200, 48
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8,
                        fill=hex_to_rgb(PANEL), outline=hex_to_rgb(MUTED), width=2)
    d.text((bx + bw // 2, by + bh // 2), "System.Exception",
           font=code_f, fill=hex_to_rgb(MUTED), anchor="mm")

    # ArgumentException
    ax, ay, aw, ah = (W - 200) // 2, 140, 200, 48
    d.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=8,
                        fill=hex_to_rgb(PANEL), outline=hex_to_rgb(MUTED), width=2)
    d.text((ax + aw // 2, ay + ah // 2), "ArgumentException",
           font=code_f, fill=hex_to_rgb(MUTED), anchor="mm")

    # Arrow Exception -> ArgumentException
    mid = bx + bw // 2
    d.line([(mid, by + bh), (mid, ay)], fill=hex_to_rgb(LINE), width=2)
    d.polygon([(mid - 6, ay), (mid + 6, ay), (mid, ay - 8)], fill=hex_to_rgb(LINE))

    # MedicalException (from Exception)
    mx, my, mw, mh = 60, 250, 240, 80
    d.rounded_rectangle([mx, my, mx + mw, my + mh], radius=8,
                        fill=hex_to_rgb(PANEL), outline=hex_to_rgb(ACCENT), width=2)
    d.text((mx + mw // 2, my + 20), "MedicalException",
           font=label_f, fill=hex_to_rgb(ACCENT), anchor="mm")
    d.line([(mx + 10, my + 34), (mx + mw - 10, my + 34)], fill=hex_to_rgb(LINE), width=1)
    d.text((mx + mw // 2, my + 52), ": Exception", font=note_f,
           fill=hex_to_rgb(MUTED), anchor="mm")
    d.text((mx + mw // 2, my + 68), "+ PatientId: string", font=note_f,
           fill=hex_to_rgb(YELLOW), anchor="mm")

    # arrow Exception -> MedicalException
    cx1 = bx + bw // 2
    d.line([(cx1, by + bh), (cx1, my - 20)], fill=hex_to_rgb(LINE), width=1)
    d.line([(cx1, my - 20), (mx + mw // 2, my - 20)], fill=hex_to_rgb(LINE), width=1)
    d.line([(mx + mw // 2, my - 20), (mx + mw // 2, my)], fill=hex_to_rgb(LINE), width=1)
    d.polygon([(mx + mw // 2 - 6, my), (mx + mw // 2 + 6, my),
               (mx + mw // 2, my - 8)], fill=hex_to_rgb(LINE))

    # PatientAgeException (from MedicalException)
    pax, pay, paw, pah = 30, 390, 220, 80
    d.rounded_rectangle([pax, pay, pax + paw, pay + pah], radius=8,
                        fill=hex_to_rgb(PANEL), outline=hex_to_rgb(YELLOW), width=2)
    d.text((pax + paw // 2, pay + 20), "PatientAgeException",
           font=label_f, fill=hex_to_rgb(YELLOW), anchor="mm")
    d.line([(pax + 10, pay + 34), (pax + paw - 10, pay + 34)], fill=hex_to_rgb(LINE), width=1)
    d.text((pax + paw // 2, pay + 52), ": MedicalException", font=note_f,
           fill=hex_to_rgb(MUTED), anchor="mm")
    d.text((pax + paw // 2, pay + 68), "+ InvalidAge: int", font=note_f,
           fill=hex_to_rgb(YELLOW), anchor="mm")

    # arrow MedicalException -> PatientAgeException
    mx_cx = mx + mw // 2
    pax_cx = pax + paw // 2
    d.line([(mx_cx, my + mh), (mx_cx, pay - 20)], fill=hex_to_rgb(LINE), width=1)
    d.line([(mx_cx, pay - 20), (pax_cx, pay - 20)], fill=hex_to_rgb(LINE), width=1)
    d.line([(pax_cx, pay - 20), (pax_cx, pay)], fill=hex_to_rgb(LINE), width=1)
    d.polygon([(pax_cx - 6, pay), (pax_cx + 6, pay), (pax_cx, pay - 8)],
              fill=hex_to_rgb(LINE))

    # DiagnosisException (from MedicalException)
    dx, dy, dw, dh = 290, 390, 220, 80
    d.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=8,
                        fill=hex_to_rgb(PANEL), outline=hex_to_rgb(RED), width=2)
    d.text((dx + dw // 2, dy + 20), "DiagnosisException",
           font=label_f, fill=hex_to_rgb(RED), anchor="mm")
    d.line([(dx + 10, dy + 34), (dx + dw - 10, dy + 34)], fill=hex_to_rgb(LINE), width=1)
    d.text((dx + dw // 2, dy + 52), ": MedicalException", font=note_f,
           fill=hex_to_rgb(MUTED), anchor="mm")
    d.text((dx + dw // 2, dy + 68), "+ DiagnosisCode: string", font=note_f,
           fill=hex_to_rgb(RED), anchor="mm")

    # arrow MedicalException -> DiagnosisException
    dx_cx = dx + dw // 2
    d.line([(mx_cx, my + mh), (mx_cx, dy - 20)], fill=hex_to_rgb(LINE), width=1)
    d.line([(mx_cx, dy - 20), (dx_cx, dy - 20)], fill=hex_to_rgb(LINE), width=1)
    d.line([(dx_cx, dy - 20), (dx_cx, dy)], fill=hex_to_rgb(LINE), width=1)
    d.polygon([(dx_cx - 6, dy), (dx_cx + 6, dy), (dx_cx, dy - 8)],
              fill=hex_to_rgb(LINE))

    # PatientValidationException (from ArgumentException)
    vx, vy, vw, vh = 570, 250, 260, 80
    d.rounded_rectangle([vx, vy, vx + vw, vy + vh], radius=8,
                        fill=hex_to_rgb(PANEL), outline=hex_to_rgb(ACCENT), width=2)
    d.text((vx + vw // 2, vy + 20), "PatientValidationException",
           font=label_f, fill=hex_to_rgb(ACCENT), anchor="mm")
    d.line([(vx + 10, vy + 34), (vx + vw - 10, vy + 34)], fill=hex_to_rgb(LINE), width=1)
    d.text((vx + vw // 2, vy + 52), ": ArgumentException", font=note_f,
           fill=hex_to_rgb(MUTED), anchor="mm")
    d.text((vx + vw // 2, vy + 68), "+ FieldName: string", font=note_f,
           fill=hex_to_rgb(YELLOW), anchor="mm")

    # arrow ArgumentException -> PatientValidationException
    ax_cx = ax + aw // 2
    vx_cx = vx + vw // 2
    d.line([(ax_cx, ay + ah), (ax_cx, vy - 20)], fill=hex_to_rgb(LINE), width=1)
    d.line([(ax_cx, vy - 20), (vx_cx, vy - 20)], fill=hex_to_rgb(LINE), width=1)
    d.line([(vx_cx, vy - 20), (vx_cx, vy)], fill=hex_to_rgb(LINE), width=1)
    d.polygon([(vx_cx - 6, vy), (vx_cx + 6, vy), (vx_cx, vy - 8)],
              fill=hex_to_rgb(LINE))

    save_if_new(img, "custom-exception-hierarchy.png")

draw_custom_exception()
print("Done.")
