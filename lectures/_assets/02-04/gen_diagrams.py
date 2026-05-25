from PIL import Image, ImageDraw, ImageFont
import os
OUTPUT_DIR=os.path.dirname(__file__)
BG="#111413";ACCENT="#76c7ad";TEXT="#e5e9e7";MUTED="#a1aaa6"
LINE="#2c3531";PANEL="#191e1c";YELLOW="#c7b876";RED="#e07070"
def h(c):
    c=c.lstrip("#");return tuple(int(c[i:i+2],16) for i in (0,2,4))
def save_if_new(img,name):
    p=os.path.join(OUTPUT_DIR,name)
    if not os.path.exists(p):img.save(p);print(f"Saved:{name}")
    else:print(f"Skipped:{name}")
def font(s,b=False):
    try:return ImageFont.truetype("arialbd.ttf"if b else"arial.ttf",s)
    except:return ImageFont.load_default()

def draw_types():
    W,H=900,400
    img=Image.new("RGB",(W,H),h(BG));d=ImageDraw.Draw(img)
    d.text((W//2,18),"Базові типи даних C#",font=font(17,True),fill=h(ACCENT),anchor="mm")

    groups=[
        ("Цілочисленні",YELLOW,[
            ("bool","true/false","1 б","System.Boolean"),
            ("byte","0..255","1 б","System.Byte"),
            ("short","-32K..32K","2 б","System.Int16"),
            ("int","-2.1B..2.1B","4 б","System.Int32"),
            ("long","±9.2×10¹⁸","8 б","System.Int64"),
        ]),
        ("Речові",ACCENT,[
            ("float","±3.4×10³⁸","4 б","System.Single"),
            ("double","±1.7×10³⁰⁸","8 б","System.Double"),
            ("decimal","28 знаків","16 б","System.Decimal"),
        ]),
        ("Інші",RED,[
            ("char","Unicode символ","2 б","System.Char"),
            ("string","рядок Unicode","ref","System.String"),
            ("object","будь-який тип","ref","System.Object"),
        ]),
    ]

    col_w=(W-40)//3
    for gi,(gname,gcolor,rows) in enumerate(groups):
        gx=20+gi*col_w
        gy=45
        d.text((gx+col_w//2,gy+12),gname,font=font(13,True),fill=h(gcolor),anchor="mm")
        for ri,(kw,rng,size,stype) in enumerate(rows):
            ry=gy+32+ri*56
            d.rounded_rectangle([gx+4,ry,gx+col_w-4,ry+50],radius=6,fill=h(PANEL),outline=h(gcolor),width=2)
            d.text((gx+8,ry+12),kw,font=font(13,True),fill=h(gcolor),anchor="lm")
            d.text((gx+col_w-8,ry+12),size,font=font(11),fill=h(MUTED),anchor="rm")
            d.text((gx+8,ry+30),rng,font=font(10),fill=h(TEXT),anchor="lm")
            d.text((gx+col_w-8,ry+30),stype,font=font(10),fill=h(MUTED),anchor="rm")

    save_if_new(img,"data-types.png")

draw_types()
print("Done.")
