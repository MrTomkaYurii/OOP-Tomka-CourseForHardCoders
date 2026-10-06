from PIL import Image, ImageDraw, ImageFont
import os

BG     = (17, 20, 19)
ACCENT = (118, 199, 173)
TEXT   = (229, 233, 231)
MUTED  = (161, 170, 166)
LINE_C = (44, 53, 49)
PANEL  = (25, 30, 28)
AMBER  = (210, 165, 75)

W, H = 1000, 450
img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

def font(name, size):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
    except:
        return ImageFont.load_default()

ft = font("arialbd.ttf", 17)
fl = font("arial.ttf",   14)
fc = font("cour.ttf",    13)
fs = font("arial.ttf",   12)
fb = font("arialbd.ttf", 12)

# ── TITLE ──
d.text((W//2, 28), "Часткові класи: два визначення — один тип після компіляції", ACCENT, font=ft, anchor="mm")

# ── LEFT: Two partial definitions ──
# File 1
f1_x, f1_y, f1_w, f1_h = 20, 60, 310, 175
d.rounded_rectangle([f1_x, f1_y, f1_x+f1_w, f1_y+f1_h], radius=8, fill=PANEL, outline=ACCENT, width=2)
d.text((f1_x+f1_w//2, f1_y+16), "PatientBase.cs", ACCENT, font=fb, anchor="mm")
d.line([(f1_x+10, f1_y+30), (f1_x+f1_w-10, f1_y+30)], LINE_C, width=1)
base_lines = [
    ("public partial class Patient", TEXT),
    ("{", MUTED),
    ("    string Name { get; }", ACCENT),
    ("    int Age { get; }", ACCENT),
    ("    Patient(string n, int a)", TEXT),
    ("    void PrintBasicInfo()", TEXT),
    ("}", MUTED),
]
for i, (line, col) in enumerate(base_lines):
    d.text((f1_x+14, f1_y+42+i*18), line, col, font=fc, anchor="lm")

# File 2
f2_x, f2_y = 20, f1_y+f1_h+18
f2_h = 155
d.rounded_rectangle([f2_x, f2_y, f2_x+f1_w, f2_y+f2_h], radius=8, fill=PANEL, outline=ACCENT, width=2)
d.text((f2_x+f1_w//2, f2_y+16), "PatientMedical.cs", ACCENT, font=fb, anchor="mm")
d.line([(f2_x+10, f2_y+30), (f2_x+f1_w-10, f2_y+30)], LINE_C, width=1)
med_lines = [
    ("public partial class Patient", TEXT),
    ("{", MUTED),
    ("    string Diagnosis { get; set; }", ACCENT),
    ("    void UpdateDiagnosis(string d)", TEXT),
    ("    void PrintMedicalInfo()", TEXT),
    ("}", MUTED),
]
for i, (line, col) in enumerate(med_lines):
    d.text((f2_x+14, f2_y+42+i*18), line, col, font=fc, anchor="lm")

# ── CENTER: Arrow with label ──
center_x = 390
mid_y1 = f1_y + f1_h//2
mid_y2 = f2_y + f2_h//2
center_y = (mid_y1 + mid_y2) // 2

# Lines from both boxes to merge point
d.line([(f1_x+f1_w, mid_y1), (center_x-10, mid_y1)], MUTED, width=2)
d.line([(f2_x+f1_w, mid_y2), (center_x-10, mid_y2)], MUTED, width=2)
d.line([(center_x-10, mid_y1), (center_x-10, mid_y2)], MUTED, width=2)
d.line([(center_x-10, center_y), (center_x+60, center_y)], MUTED, width=2)
d.polygon([(center_x+60, center_y-7), (center_x+60, center_y+7), (center_x+75, center_y)], MUTED)

# Label
d.rounded_rectangle([center_x-5, center_y-28, center_x+56, center_y-8], radius=4, fill=PANEL, outline=LINE_C, width=1)
d.text(((center_x-5+center_x+56)//2, center_y-18), "компілятор", MUTED, font=fs, anchor="mm")
d.rounded_rectangle([center_x-5, center_y+8, center_x+56, center_y+28], radius=4, fill=PANEL, outline=LINE_C, width=1)
d.text(((center_x-5+center_x+56)//2, center_y+18), "зливає", MUTED, font=fs, anchor="mm")

# ── RIGHT: Merged class ──
r_x, r_y = center_x+80, 60
r_w, r_h = 300, f2_y+f2_h - 60
d.rounded_rectangle([r_x, r_y, r_x+r_w, r_y+r_h], radius=8, fill=PANEL, outline=AMBER, width=2)
d.text((r_x+r_w//2, r_y+16), "Patient  (результат компіляції)", AMBER, font=fb, anchor="mm")
d.line([(r_x+10, r_y+30), (r_x+r_w-10, r_y+30)], LINE_C, width=1)
merged_lines = [
    ("public class Patient",           TEXT),
    ("{",                              MUTED),
    ("    // З PatientBase.cs:",       ACCENT),
    ("    string Name { get; }",       TEXT),
    ("    int Age { get; }",           TEXT),
    ("    Patient(string n, int a)",   TEXT),
    ("    void PrintBasicInfo()",      TEXT),
    ("",                               TEXT),
    ("    // З PatientMedical.cs:",    ACCENT),
    ("    string Diagnosis { get; set; }", TEXT),
    ("    void UpdateDiagnosis(..)",   TEXT),
    ("    void PrintMedicalInfo()",    TEXT),
    ("}",                              MUTED),
]
for i, (line, col) in enumerate(merged_lines):
    d.text((r_x+14, r_y+42+i*18), line, col, font=fc, anchor="lm")

# ── BOTTOM NOTE ──
note_y = r_y + r_h + 14
d.text((W//2, note_y),
    "partial — лише директива для компілятора. В IL-коді існує один тип з усіма членами.",
    MUTED, font=fs, anchor="mm")

out = "lectures/_assets/08-07/partial-class-merge.png"
img.save(out)
print(f"OK: {out}")
