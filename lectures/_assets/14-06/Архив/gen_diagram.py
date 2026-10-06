# -*- coding: utf-8 -*-
# Attributes: Attribute class, custom attributes, AttributeUsage, IsDefined/GetCustomAttributes
from PIL import Image, ImageDraw, ImageFont

BG="#111413"; ACCENT="#76c7ad"; TEXT="#e5e9e7"; MUTED="#a1aaa6"
LINE="#2c3531"; PANEL="#191e1c"; ORANGE="#c7a276"; DARK="#161c1a"; RED="#c77676"

W,H=960,560
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

def load(p,s):
    try: return ImageFont.truetype(p,s)
    except: return ImageFont.load_default()

ft=load("C:/Windows/Fonts/arialbd.ttf",15)
fh=load("C:/Windows/Fonts/arialbd.ttf",12)
fc=load("C:/Windows/Fonts/arial.ttf",10)
fcc=load("C:/Windows/Fonts/arial.ttf",9)

d.text((W//2,22),"Атрибути — Attribute, AttributeUsage, читання через рефлексію",
       font=ft,fill=ACCENT,anchor="mm")

# ============================================================
# LEFT: Attribute class + built-in attributes
# ============================================================
lx=20; ly=42; lw=270; lh=316
d.rounded_rectangle([lx,ly,lx+lw,ly+lh],radius=8,fill=PANEL,outline=ACCENT,width=2)
d.text((lx+lw//2,ly+13),"Клас Attribute",font=fh,fill=ACCENT,anchor="mm")
d.line([(lx+6,ly+27),(lx+lw-6,ly+27)],fill=LINE,width=1)

d.text((lx+lw//2,ly+38),"Вбудовані атрибути",font=fcc,fill=MUTED,anchor="mm")
builtin=[
    ("[Obsolete]",             "застарілий API"),
    ("[Serializable]",         "серіалізація"),
    ("[NonSerialized]",        "поле не серіалізується"),
    ("[DllImport]",            "P/Invoke до нативного коду"),
    ("[Flags]",                "enum як бітова маска"),
    ("[AttributeUsage]",       "обмеження атрибута"),
    ("[CallerMemberName]",     "ім'я викликача"),
    ("[Required] (DataAnnot.)","валідація"),
    ("[JsonPropertyName]",     "серіалізація JSON"),
    ("[CompilerGenerated]",    "згенероване компілятором"),
]
ay=ly+48
for name,desc in builtin:
    d.rounded_rectangle([lx+8,ay-3,lx+lw-8,ay+12],radius=2,fill=DARK,outline=LINE,width=1)
    d.text((lx+12,ay+3),name,font=fcc,fill=ACCENT,anchor="lm")
    d.text((lx+12,ay+11),f"  // {desc}",font=fcc,fill=MUTED,anchor="lm")
    ay+=16

# AttributeBase
d.line([(lx+10,ay+2),(lx+lw-10,ay+2)],fill=LINE,width=1)
d.text((lx+lw//2,ay+12),"Базовий клас System.Attribute",font=fcc,fill=MUTED,anchor="mm")
base_rows=[
    ("public abstract class Attribute","успадкування"),
    ("Суфікс Attribute — конвенція",   "можна без суфікса"),
    ("один рядок = один клас",         "C# зручний синтаксис"),
]
ay+=22
for code,note in base_rows:
    d.text((lx+12,ay),code,font=fcc,fill=ORANGE,anchor="lm")
    d.text((lx+12,ay+9),f"  // {note}",font=fcc,fill=MUTED,anchor="lm")
    ay+=19

# ============================================================
# MIDDLE: AttributeUsage + custom attribute anatomy
# ============================================================
mx=lx+lw+14; my=ly; mw=320; mh=lh
d.rounded_rectangle([mx,my,mx+mw,my+mh],radius=8,fill=PANEL,outline=ORANGE,width=2)
d.text((mx+mw//2,my+13),"[AttributeUsage] та власні атрибути",font=fh,fill=ORANGE,anchor="mm")
d.line([(mx+6,my+27),(mx+mw-6,my+27)],fill=LINE,width=1)

# AttributeUsage params
d.text((mx+mw//2,my+38),"AttributeUsage параметри",font=fcc,fill=MUTED,anchor="mm")
usage_params=[
    ("AttributeTargets.Class",    "тільки на класах"),
    ("AttributeTargets.Property", "тільки на властивостях"),
    ("AttributeTargets.Method",   "тільки на методах"),
    ("AttributeTargets.All",      "будь-який елемент"),
    ("AllowMultiple = true",      "кілька на одному елементі"),
    ("Inherited = false",         "не передається нащадкам"),
]
cy=my+48
for name,desc in usage_params:
    d.rounded_rectangle([mx+8,cy-3,mx+mw-8,cy+12],radius=2,fill=DARK,outline=ORANGE,width=1)
    d.text((mx+12,cy+3),name,font=fcc,fill=ORANGE,anchor="lm")
    d.text((mx+12,cy+11),f"  // {desc}",font=fcc,fill=MUTED,anchor="lm")
    cy+=16

d.line([(mx+10,cy+2),(mx+mw-10,cy+2)],fill=LINE,width=1)

# Custom attribute anatomy
d.text((mx+mw//2,cy+12),"Анатомія власного атрибута",font=fcc,fill=MUTED,anchor="mm")
anatomy=[
    "[AttributeUsage(AttributeTargets.Property,",
    "    AllowMultiple=false, Inherited=true)]",
    "public sealed class ValidationRangeAttribute",
    "    : Attribute",
    "{",
    "    public double Min { get; }",
    "    public double Max { get; }",
    "    public string? Message { get; set; }",
    "    public ValidationRangeAttribute(double min, double max)",
    "        => (Min, Max) = (min, max);",
    "}",
]
cy+=22
for line in anatomy:
    col = ORANGE if line.startswith("[") or line.startswith("public") or line == "}" else TEXT
    d.text((mx+12,cy),line,font=fcc,fill=col,anchor="lm")
    cy+=11

# ============================================================
# RIGHT: Reading attributes via reflection
# ============================================================
rx=mx+mw+14; ry=my; rw=W-rx-20; rh=mh
d.rounded_rectangle([rx,ry,rx+rw,ry+rh],radius=8,fill=PANEL,outline=RED,width=2)
d.text((rx+rw//2,ry+13),"Читання атрибутів через рефлексію",font=fh,fill=RED,anchor="mm")
d.line([(rx+6,ry+27),(rx+rw-6,ry+27)],fill=LINE,width=1)

read_api=[
    ("IsDefined(type, inherit)",     "чи є атрибут (швидко)"),
    ("GetCustomAttribute<T>()",      "один атрибут → T?"),
    ("GetCustomAttributes<T>()",     "масив атрибутів → T[]"),
    ("GetCustomAttributes(inherit)", "всі атрибути → object[]"),
    ("GetCustomAttributesData()",    "CustomAttributeData[]"),
]
sy=ry+34
for name,desc in read_api:
    d.rounded_rectangle([rx+8,sy-3,rx+rw-8,sy+13],radius=2,fill=DARK,outline=RED,width=1)
    d.text((rx+12,sy+4),name,font=fcc,fill=RED,anchor="lm")
    d.text((rx+12,sy+12),f"  // {desc}",font=fcc,fill=MUTED,anchor="lm")
    sy+=17

d.line([(rx+10,sy+2),(rx+rw-10,sy+2)],fill=LINE,width=1)

# Targets that support GetCustomAttributes
d.text((rx+rw//2,sy+12),"Де можна читати атрибути",font=fcc,fill=MUTED,anchor="mm")
targets=[
    ("Type",            "typeof(T).GetCustomAttribute<A>()"),
    ("MethodInfo",      "method.GetCustomAttribute<A>()"),
    ("PropertyInfo",    "prop.GetCustomAttribute<A>()"),
    ("FieldInfo",       "field.GetCustomAttribute<A>()"),
    ("ParameterInfo",   "param.GetCustomAttribute<A>()"),
    ("Assembly",        "asm.GetCustomAttribute<A>()"),
]
sy+=22
for target,example in targets:
    d.rounded_rectangle([rx+8,sy-3,rx+rw-8,sy+13],radius=2,fill=DARK,outline=LINE,width=1)
    d.text((rx+12,sy+4),target,font=fcc,fill=ORANGE,anchor="lm")
    d.text((rx+70,sy+4),example,font=fcc,fill=MUTED,anchor="lm")
    sy+=16

d.line([(rx+10,sy+2),(rx+rw-10,sy+2)],fill=LINE,width=1)

# Inherit parameter
d.text((rx+rw//2,sy+12),"Параметр inherit",font=fcc,fill=MUTED,anchor="mm")
inherit_rows=[
    ("inherit=true", "шукати і в базових класах"),
    ("inherit=false","тільки на цьому елементі"),
    ("для Interface","inherit завжди false (CLR)"),
]
sy+=22
for k,v in inherit_rows:
    d.text((rx+12,sy),k,font=fcc,fill=RED,anchor="lm")
    d.text((rx+90,sy),f"// {v}",font=fcc,fill=MUTED,anchor="lm")
    sy+=12

# ============================================================
# BOTTOM: Use cases
# ============================================================
bot_y=ly+lh+12; bot_h=68
d.rounded_rectangle([20,bot_y,W-20,bot_y+bot_h],radius=6,fill=PANEL,outline=ORANGE,width=1)
d.text((W//2,bot_y+11),"Практичне застосування атрибутів",font=fh,fill=ORANGE,anchor="mm")
d.line([(30,bot_y+24),(W-30,bot_y+24)],fill=LINE,width=1)

cases=[
    ("Валідація","[Required],[Range]\nValidate(obj):\nGetCustomAttributes→check"),
    ("ORM/EF Core","[Table],[Column]\nмаппінг на\nтаблицю/колонку БД"),
    ("Серіалізація","[JsonIgnore]\n[JsonPropertyName]\nSystem.Text.Json"),
    ("Тестування","[Test],[TestCase]\nNUnit знаходить\nчерез GetMethods+attr"),
    ("DI scanning","[Singleton],[Scoped]\nсканування збірки\nта авто-реєстрація"),
]
uw=(W-50)//len(cases)
for i,(title,desc) in enumerate(cases):
    ux=28+i*uw
    d.text((ux,bot_y+30),title,font=fcc,fill=ACCENT,anchor="lm")
    for j,line in enumerate(desc.split("\n")):
        d.text((ux,bot_y+40+j*9),line,font=fcc,fill=TEXT,anchor="lm")

out="C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/14-06/attributes.png"
img.save(out); print("OK:",out)
