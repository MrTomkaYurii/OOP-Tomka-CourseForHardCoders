from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.dirname(__file__)
BG=("#111413"); ACCENT=("#76c7ad"); TEXT=("#e5e9e7"); MUTED=("#a1aaa6")
LINE=("#2c3531"); PANEL=("#191e1c"); YELLOW=("#c7b876"); RED=("#e07070")

def h(c):
    c=c.lstrip("#"); return tuple(int(c[i:i+2],16) for i in (0,2,4))
def save_if_new(img,name):
    p=os.path.join(OUTPUT_DIR,name)
    if not os.path.exists(p): img.save(p); print(f"Saved: {name}")
    else: print(f"Skipped: {name}")
def font(size,bold=False):
    try: return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf",size)
    except: return ImageFont.load_default()

def draw_program_structure():
    W,H=820,300
    img=Image.new("RGB",(W,H),h(BG)); d=ImageDraw.Draw(img)
    d.text((W//2,18),"Структура програми C#",font=font(17,True),fill=h(ACCENT),anchor="mm")

    blocks=[
        ("Program.cs",        "Головний файл\nВхідна точка програми",   ACCENT,  40, 50),
        ("Інструкції\n(statements)","Дії: виклики методів,\nоголошення змінних, оператори", YELLOW, 220, 50),
        ("Блок коду { }",     "Група інструкцій\nу фігурних дужках",    MUTED,   420, 50),
        (".csproj",           "Конфігурація проекту:\nTargetFramework, OutputType", RED, 620, 50),
    ]
    for title,note,color,bx,by in blocks:
        bw,bh=160,100
        d.rounded_rectangle([bx,by,bx+bw,by+bh],radius=8,fill=h(PANEL),outline=h(color),width=2)
        for i,ln in enumerate(title.split("\n")):
            d.text((bx+bw//2,by+18+i*18),ln,font=font(12,True),fill=h(color),anchor="mm")
        d.line([(bx+10,by+38),(bx+bw-10,by+38)],fill=h(LINE),width=1)
        for i,ln in enumerate(note.split("\n")):
            d.text((bx+bw//2,by+52+i*17),ln,font=font(11),fill=h(MUTED),anchor="mm")

    # arrows
    pairs=[(200,100),(400,100),(600,100)]
    for ax,ay in pairs:
        d.line([(ax,ay),(ax+20,ay)],fill=h(LINE),width=2)
        d.polygon([(ax+20,ay-5),(ax+20,ay+5),(ax+28,ay)],fill=h(LINE))

    # bottom: top-level statements note
    ny=175
    d.rounded_rectangle([40,ny,W-40,ny+90],radius=8,fill=h(PANEL),outline=h(LINE),width=1)
    d.text((W//2,ny+18),"Top-level statements (C# 9+)",font=font(13,True),fill=h(YELLOW),anchor="mm")
    d.line([(60,ny+32),(W-60,ny+32)],fill=h(LINE),width=1)
    d.text((W//2,ny+50),'Починаючи з C# 9, клас Program і метод Main не обов\'язкові.',font=font(11),fill=h(TEXT),anchor="mm")
    d.text((W//2,ny+68),'Код у Program.cs виконується напряму: Console.WriteLine("Привіт!");',font=font(11),fill=h(MUTED),anchor="mm")

    save_if_new(img,"program-structure.png")

draw_program_structure()
print("Done.")
