from PIL import Image, ImageDraw, ImageFont
import os

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; YELLOW="#c7b876"; RED="#e07070"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def rgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def save_if_new(img, name):
    p = os.path.join(SCRIPT_DIR, name)
    if os.path.exists(p): print(f"SKIP: {name}"); return
    img.save(p); print(f"CREATED: {name}")

def font(size, bold=False):
    cands = (["C:/Windows/Fonts/consolab.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"] if bold else
             ["C:/Windows/Fonts/consola.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"])
    for c in cands:
        if os.path.exists(c): return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def arrow(d, x1, y1, x2, y2, color, width=2):
    d.line([(x1,y1),(x2,y2)], fill=rgb(color), width=width)
    import math
    dx,dy = x2-x1, y2-y1
    L = math.sqrt(dx*dx+dy*dy)
    if L == 0: return
    ux,uy = dx/L, dy/L
    px,py = -uy, ux
    s = 8
    d.polygon([(x2,y2),(x2-ux*s+px*4,y2-uy*s+py*4),(x2-ux*s-px*4,y2-uy*s-py*4)],
              fill=rgb(color))

def make_flow():
    W,H = 700,560
    img = Image.new("RGB",(W,H),rgb(BG))
    d = ImageDraw.Draw(img)
    d.text((W//2,22),"Потік виконання try..catch..finally",
           font=font(17,True),fill=rgb(ACCENT),anchor="mm")

    def block(x,y,w,h,label,color,sub=None):
        d.rounded_rectangle([x+2,y+2,x+w+2,y+h+2],radius=7,fill=rgb(LINE))
        d.rounded_rectangle([x,y,x+w,y+h],radius=7,fill=rgb(PANEL),outline=rgb(color),width=2)
        d.rounded_rectangle([x+2,y+2,x+w-2,y+28],radius=6,fill=rgb(color))
        d.text((x+w//2,y+15),label,font=font(13,True),fill=rgb(BG),anchor="mm")
        if sub:
            d.text((x+w//2,y+h//2+8),sub,font=font(11),fill=rgb(MUTED),anchor="mm")

    cx = W//2
    bw = 240

    # try block
    block(cx-bw//2, 50, bw, 65, "try {}", ACCENT, "Виконується код")
    # diamond — виняток?
    dy_y = 160
    pts = [(cx,dy_y-25),(cx+70,dy_y),(cx,dy_y+25),(cx-70,dy_y)]
    d.polygon(pts, fill=rgb(PANEL), outline=rgb(YELLOW), width=2)
    d.text((cx,dy_y),"Виняток?",font=font(12,True),fill=rgb(YELLOW),anchor="mm")

    arrow(d, cx, 115, cx, dy_y-25, MUTED)

    # NO → finally directly
    arrow(d, cx+70, dy_y, cx+160, dy_y, MUTED)
    d.text((cx+110, dy_y-14),"Ні",font=font(11),fill=rgb(ACCENT))

    # YES → catch
    catch_y = 260
    arrow(d, cx, dy_y+25, cx, catch_y, RED)
    d.text((cx+6, dy_y+38),"Так",font=font(11),fill=rgb(RED))
    block(cx-bw//2, catch_y, bw, 65, "catch {}", RED, "Обробка винятку")

    # finally
    fin_y = 390
    # from catch
    arrow(d, cx, catch_y+65, cx, fin_y, MUTED)
    # from no-exception path
    arrow(d, cx+160, dy_y, cx+160, fin_y+32, MUTED)
    arrow(d, cx+160, fin_y+32, cx+bw//2, fin_y+32, MUTED)

    block(cx-bw//2, fin_y, bw, 65, "finally {}", YELLOW, "Завжди виконується")

    # end
    end_y = 500
    arrow(d, cx, fin_y+65, cx, end_y, MUTED)
    d.text((cx, end_y+10),"Продовження програми",font=font(12),fill=rgb(MUTED),anchor="mm")

    save_if_new(img,"try-catch-flow.png")

make_flow()
print("Done.")
