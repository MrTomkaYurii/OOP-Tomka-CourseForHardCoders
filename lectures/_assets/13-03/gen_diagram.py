# -*- coding: utf-8 -*-
# Convert class overview: numeric, string, bool, base64, ChangeType + cast vs Convert
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"; RED="#c77676"

W,H=960,530
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11)
ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)
fcc=load("C:/Windows/Fonts/arial.ttf",9)

d.text((W//2,22),"Клас Convert — перетворення типів",
       font=ft,fill=ACCENT,anchor="mm")

# === ROW 1: 4 panels ===
panels_top = [
    {
        "title": "Числові перетворення",
        "color": ACCENT,
        "items": [
            ("Convert.ToInt32(x)",    "double/string → int"),
            ("Convert.ToInt64(x)",    "→ long"),
            ("Convert.ToDouble(x)",   "→ double"),
            ("Convert.ToDecimal(x)",  "→ decimal"),
            ("Convert.ToSingle(x)",   "→ float"),
            ("Convert.ToByte(x)",     "→ byte (0–255)"),
        ]
    },
    {
        "title": "Рядкові перетворення",
        "color": ORANGE,
        "items": [
            ("Convert.ToString(x)",      "будь-який тип → string"),
            ("Convert.ToString(null)",   "→ \"\" (не NullRef!)"),
            ("Convert.ToInt32(\"42\")",  "string → int (або Exception)"),
            ("Convert.ToDouble(\"3.14\")","string → double"),
            ("Convert.ToDateTime(s)",    "string → DateTime"),
        ]
    },
    {
        "title": "Булеві перетворення",
        "color": RED,
        "items": [
            ("Convert.ToBoolean(1)",       "1 → true"),
            ("Convert.ToBoolean(0)",       "0 → false"),
            ("Convert.ToBoolean(\"True\")", "\"True\" → true"),
            ("Convert.ToInt32(true)",      "true → 1"),
            ("Convert.ToInt32(false)",     "false → 0"),
        ]
    },
    {
        "title": "Base64",
        "color": ACCENT,
        "items": [
            ("Convert.ToBase64String(bytes)","byte[] → string"),
            ("Convert.FromBase64String(s)",  "string → byte[]"),
            ("","DICOM / HL7 FHIR:"),
            ("","документи у JSON/API"),
            ("","передаються як Base64"),
        ]
    },
]

PW = (W - 40 - 3*10) // 4
py = 45; ph = 180

for i, panel in enumerate(panels_top):
    px = 20 + i*(PW+10)
    col = panel["color"]
    d.rounded_rectangle([px,py,px+PW,py+ph],radius=8,fill=PANEL,outline=col,width=2)
    d.text((px+PW//2, py+13), panel["title"], font=fh, fill=col, anchor="mm")
    d.line([(px+6, py+27),(px+PW-6, py+27)], fill=LINE, width=1)
    for j,(name,desc) in enumerate(panel["items"]):
        iy = py + 34 + j*25
        if name:
            d.rounded_rectangle([px+6,iy-8,px+PW-6,iy+13],radius=3,fill=DARK,outline=LINE,width=1)
            d.text((px+10, iy-1), name, font=fc, fill=col, anchor="lm")
            d.text((px+10, iy+9), f"  // {desc}", font=fcc, fill=MUTED, anchor="lm")
        else:
            d.text((px+10, iy+2), desc, font=fcc, fill=MUTED, anchor="lm")

# === ROW 2: ChangeType + cast vs Convert comparison ===
row2_y = py + ph + 14

# ChangeType panel
ctw = 290
d.rounded_rectangle([20,row2_y,20+ctw,row2_y+200],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((20+ctw//2, row2_y+13),"Convert.ChangeType", font=fh, fill=ORANGE, anchor="mm")
d.line([(26, row2_y+27),(20+ctw-6, row2_y+27)], fill=LINE, width=1)

ct_items = [
    ("Convert.ChangeType(val, type)", "динамічне перетворення"),
    ("object r = ChangeType(\"42\",", "typeof(int)) → (object)42"),
    ("","Використання:"),
    ("","• десеріалізація JSON"),
    ("","• generic-код з Type"),
    ("","• відображення властивостей"),
]
for j,(name,desc) in enumerate(ct_items):
    iy = row2_y + 34 + j*26
    if name:
        d.rounded_rectangle([26,iy-8,20+ctw-6,iy+13],radius=3,fill=DARK,outline=LINE,width=1)
        d.text((30, iy-1), name, font=fcc, fill=ORANGE, anchor="lm")
        d.text((30, iy+9), f"  // {desc}", font=fcc, fill=MUTED, anchor="lm")
    else:
        d.text((30, iy+2), desc, font=fcc, fill=MUTED, anchor="lm")

# cast vs Convert comparison table
cx = 20 + ctw + 14; cw = W - cx - 20
d.rounded_rectangle([cx,row2_y,cx+cw,row2_y+200],radius=8,fill=PANEL,outline=RED,width=2)
d.text((cx+cw//2, row2_y+13),"Cast (int) vs Convert.ToInt32", font=fh, fill=RED, anchor="mm")
d.line([(cx+6, row2_y+27),(cx+cw-6, row2_y+27)], fill=LINE, width=1)

# Table headers
hx = [cx+8, cx+160, cx+310, cx+460]
hdrs = ["Операція", "(int) cast", "Convert.ToInt32", "Примітка"]
for j,(h,x) in enumerate(zip(hdrs,hx)):
    d.text((x, row2_y+32), h, font=fcc, fill=MUTED, anchor="lm")
d.line([(cx+8, row2_y+42),(cx+cw-8, row2_y+42)], fill=LINE, width=1)

rows = [
    ("double 3.9",   "(int)3.9 = 3",       "ToInt32(3.9) = 4",        "cast: Truncate; Cvt: Round"),
    ("double 3.5",   "(int)3.5 = 3",       "ToInt32(3.5) = 4",        "банківське заокруглення"),
    ("string \"42\"","(int)\"42\" = ERROR", "ToInt32(\"42\") = 42",    "cast не може рядок"),
    ("null",         "(int)null = 0",       "ToInt32(null) = 0",       "обидва дають 0"),
    ("bool true",    "(int)true = ERROR",   "ToInt32(true) = 1",       "cast не може bool"),
    ("overflow",     "(int)3e10 = garbage", "ToInt32(3e10) = Exception","checked vs unchecked"),
]
for j,row in enumerate(rows):
    iy = row2_y + 48 + j*22
    bg = DARK if j%2==0 else BG
    d.rectangle([cx+6,iy-4,cx+cw-6,iy+14], fill=bg)
    cols_data = [row[0], row[1], row[2], row[3]]
    text_cols = [ACCENT, RED, ACCENT, MUTED]
    for k,(val,x) in enumerate(zip(cols_data,hx)):
        d.text((x, iy+5), val, font=fcc, fill=text_cols[k], anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/13-03/convert-overview.png"
img.save(out); print("OK:",out)
