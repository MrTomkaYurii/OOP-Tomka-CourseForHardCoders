# -*- coding: utf-8 -*-
# ObservableCollection — CollectionChanged event flow
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"

W,H=920,400
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

fb=load("C:/Windows/Fonts/arialbd.ttf",14); fr=load("C:/Windows/Fonts/arial.ttf",13)
fs=load("C:/Windows/Fonts/arial.ttf",11);  ft=load("C:/Windows/Fonts/arialbd.ttf",16)
fh=load("C:/Windows/Fonts/arialbd.ttf",13)

d.text((W//2,24),"ObservableCollection<T> — сповіщення про зміни (подія CollectionChanged)",font=ft,fill=ACCENT,anchor="mm")

# === LEFT: ObservableCollection box ===
oc_x,oc_y,oc_w,oc_h=50,80,200,230
d.rounded_rectangle([oc_x,oc_y,oc_x+oc_w,oc_y+oc_h],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((oc_x+oc_w//2,oc_y+18),"ObservableCollection",font=fh,fill=ACCENT,anchor="mm")
d.text((oc_x+oc_w//2,oc_y+34),"<Patient>",font=fs,fill=MUTED,anchor="mm")
d.line([(oc_x+10,oc_y+46),(oc_x+oc_w-10,oc_y+46)],fill=LINE,width=1)

ops=[("Add(patient)","додає"), ("Remove(id)","видаляє"), ("this[i]=p","замінює"), ("Clear()","очищує")]
for i,(op,desc) in enumerate(ops):
    oy=oc_y+58+i*40
    d.rounded_rectangle([oc_x+10,oy,oc_x+oc_w-10,oy+28],radius=4,fill=DARK)
    d.text((oc_x+oc_w//2,oy+8),op,font=fb,fill=ORANGE,anchor="mm")
    d.text((oc_x+oc_w//2,oy+20),desc,font=fs,fill=MUTED,anchor="mm")

# === MIDDLE: Event arrow ===
ev_x=oc_x+oc_w+16; ev_y=oc_y+oc_h//2
ev_mid_x=ev_x+90
d.rounded_rectangle([ev_x+10,ev_y-28,ev_x+170,ev_y+28],radius=6,fill=DARK,outline=ORANGE,width=2)
d.text((ev_x+90,ev_y-10),"CollectionChanged",font=fb,fill=ORANGE,anchor="mm")
d.text((ev_x+90,ev_y+8),"event",font=fs,fill=MUTED,anchor="mm")
# arrow left → event box
d.line([(oc_x+oc_w+2,ev_y),(ev_x+10,ev_y)],fill=ORANGE,width=2)
d.polygon([(ev_x+10,ev_y),(ev_x+2,ev_y-5),(ev_x+2,ev_y+5)],fill=ORANGE)

# === RIGHT: Subscribers ===
sub_x=ev_x+180+10; sub_y0=80
actions=[
    ("Add",    "NotifyCollectionChangedAction.Add",    "e.NewItems[0] — новий елемент"),
    ("Remove", "NotifyCollectionChangedAction.Remove",  "e.OldItems[0] — видалений"),
    ("Replace","NotifyCollectionChangedAction.Replace","e.NewItems / e.OldItems"),
    ("Reset",  "NotifyCollectionChangedAction.Reset",  "Clear() — скидання"),
]
sub_w=280; sub_h=58; sub_gap=8
for i,(label,action,detail) in enumerate(actions):
    sy=sub_y0+i*(sub_h+sub_gap)
    shade=PANEL if i%2==0 else DARK
    d.rounded_rectangle([sub_x,sy,sub_x+sub_w,sy+sub_h],radius=5,fill=shade,outline=LINE,width=1)
    d.text((sub_x+8,sy+12),action,font=fs,fill=ACCENT,anchor="lm")
    d.text((sub_x+8,sy+28),detail,font=fs,fill=TEXT,anchor="lm")
    d.text((sub_x+8,sy+44),f"e.Action == {label}",font=fs,fill=MUTED,anchor="lm")
    # arrow from event → subscriber
    arr_sy=sy+sub_h//2
    d.line([(ev_x+170,ev_y),(sub_x-2,arr_sy)],fill=LINE,width=1)
    d.polygon([(sub_x-2,arr_sy),(sub_x-10,arr_sy-4),(sub_x-10,arr_sy+4)],fill=LINE)

# Bottom
ly=H-55
d.line([(30,ly-8),(W-30,ly-8)],fill=LINE,width=1)
d.text((30,ly),    "Підписка: collection.CollectionChanged += MyHandler;",font=fh,fill=ACCENT)
d.text((30,ly+20), "Обробник: void MyHandler(object? sender, NotifyCollectionChangedEventArgs e) { ... }",font=fs,fill=TEXT)

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/10-06/observablecollection-event-flow.png"
img.save(out); print("OK:",out)
