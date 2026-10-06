"""Автоматичний контроль якості: геометрія моделі, контраст, перевірка рендеру."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from .core import GRID, Theme, contrast
from .layout import Model

TEXT_INSET = 4      # мінімальний зазор тексту до рамки, px
MIN_TEXT = 4.5      # WCAG AA, основний текст
MIN_LARGE = 3.0     # WCAG AA, великий текст (≥ 24 px або ≥ 18.66 px жирний)
MIN_NONTEXT = 3.0   # WCAG 1.4.11 — рамки розділів, акцентні рамки, стрілки


def _overlap(a, b, eps=0.5):
    return a[0] < b[2] - eps and b[0] < a[2] - eps and a[1] < b[3] - eps and b[1] < a[3] - eps


def _inside(inner, outer, inset=0):
    return (inner[0] >= outer[0] + inset - 0.01 and inner[1] >= outer[1] - 0.01 and
            inner[2] <= outer[2] - inset + 0.01 and inner[3] <= outer[3] + 0.01)


def text_bbox(t):
    """Реальна (а не відведена) рамка тексту з урахуванням вирівнювання."""
    if t.align == "left":
        x0 = t.x
    elif t.align == "right":
        x0 = t.x + t.w - t.natural_w
    else:
        x0 = t.x + (t.w - t.natural_w) / 2
    return (x0, t.y, x0 + t.natural_w, t.y + t.h)


def rbox(r):
    return (r.x, r.y, r.x + r.w, r.y + r.h)


def check_model(m: Model, theme: Theme) -> list[str]:
    errs: list[str] = []
    rects = {r.id: r for r in m.rects}
    shapes = [r for r in m.rects if r.kind != "bg"]

    # 1. Сітка
    for r in shapes:
        bad = [k for k in ("x", "y", "w", "h") if getattr(r, k) % GRID]
        if bad:
            errs.append(f"сітка: {r.id} ({r.kind}) {bad} не кратні {GRID}")

    # 2. Прямокутники: сусіди не перетинаються, діти всередині батька
    for i, a in enumerate(shapes):
        if a.parent in rects and not _inside(rbox(a), rbox(rects[a.parent])):
            errs.append(f"вкладеність: {a.id} виходить за {a.parent}")
        for b in shapes[i + 1:]:
            if a.parent == b.parent and _overlap(rbox(a), rbox(b)):
                errs.append(f"перетин блоків: {a.id} × {b.id}")

    # 3. Тексти: всередині своєї рамки з відступом, не перетинаються між собою і з чужими блоками
    tb = [(t, text_bbox(t)) for t in m.texts]
    for t, b in tb:
        if t.natural_w > t.w + 0.5:
            errs.append(f"текст ширший за відведене місце: {t.id} «{_plain(t)}» {t.natural_w:.0f} > {t.w:.0f}")
        p = rects.get(t.parent)
        if p and not _inside(b, rbox(p), 0 if p.kind == "bg" else TEXT_INSET):
            errs.append(f"текст за рамкою: {t.id} «{_plain(t)}» у {p.id}")
        for r in shapes:
            if r.id != t.parent and r.parent == t.parent and _overlap(b, rbox(r)):
                errs.append(f"текст на чужому блоці: {t.id} «{_plain(t)}» × {r.id}")
    for i, (a, ba) in enumerate(tb):
        for c, bc in tb[i + 1:]:
            if _overlap(ba, bc):
                errs.append(f"перетин текстів: «{_plain(a)}» × «{_plain(c)}»")

    # 4. Стрілки: горизонтальні або вертикальні, не перетинають тексти, рівні в групі
    for e in m.edges:
        (x1, y1), (x2, y2) = e.p1, e.p2
        if x1 != x2 and y1 != y2:
            errs.append(f"стрілка {e.id} не горизонтальна/вертикальна")
        seg = (min(x1, x2) - 1, min(y1, y2) - 1, max(x1, x2) + 1, max(y1, y2) + 1)
        for t, b in tb:
            if _overlap(seg, b):
                errs.append(f"стрілка {e.id} торкається тексту «{_plain(t)}»")
        src, tgt = rects[e.src], rects[e.tgt]
        if not (_on_border(e.p1, src) and _on_border(e.p2, tgt)):
            errs.append(f"стрілка {e.id} не прив'язана до меж блоків")
    for g in m.arrow_groups:
        lens = {round(abs(e.p2[0] - e.p1[0]) + abs(e.p2[1] - e.p1[1]), 1)
                for e in m.edges if e.id in g}
        if len(lens) > 1:
            errs.append(f"стрілки однієї групи різної довжини: {lens}")

    # 5. Однакові ширини в стовпчиках
    for g in m.equal_width:
        ws = {rects[i].w for i in g if i in rects}
        if len(ws) > 1:
            errs.append(f"різні ширини в стовпчику {g}: {ws}")

    # 6. Контраст тексту до фону його контейнера
    for t in m.texts:
        p = rects.get(t.parent)
        fill = theme.bg if (p is None or p.kind == "bg") else theme.shapes[p.kind]["fill"]
        for _, role in t.runs:
            r = theme.role(role)
            large = t.size >= 24 or (t.size >= 18.66 and r["bold"])
            need = MIN_LARGE if large else MIN_TEXT
            cr = contrast(r["color"], fill)
            if cr < need:
                errs.append(f"контраст {theme.name}: роль {role} {r['color']} на {fill} = {cr:.2f} < {need}")
    for kind in ("panel", "box_accent", "box_muted"):
        s = theme.shapes[kind]
        if contrast(s["stroke"], theme.bg) < MIN_NONTEXT:
            errs.append(f"контраст {theme.name}: рамка {kind} {s['stroke']} на фоні < {MIN_NONTEXT}")
    for fill in {theme.bg, theme.shapes["panel"]["fill"]}:
        if contrast(theme.arrow["color"], fill) < MIN_NONTEXT:
            errs.append(f"контраст {theme.name}: стрілка на {fill} < {MIN_NONTEXT}")

    return sorted(set(errs), key=errs.index)


def _on_border(p, r, eps=0.6):
    x, y = p
    on_v = abs(x - r.x) < eps or abs(x - (r.x + r.w)) < eps
    on_h = abs(y - r.y) < eps or abs(y - (r.y + r.h)) < eps
    return (on_v and r.y - eps <= y <= r.y + r.h + eps) or (on_h and r.x - eps <= x <= r.x + r.w + eps)


def _plain(t):
    return "".join(x for x, _ in t.runs)[:40]


def check_render(png: Path, m: Model, theme: Theme, scale: int = 2) -> list[str]:
    errs = []
    im = Image.open(png).convert("RGB")
    ew, eh = m.w * scale, m.h * scale
    if abs(im.width - ew) > 4 or abs(im.height - eh) > 4:
        errs.append(f"рендер {png.name}: розмір {im.size}, очікувано ≈ {(ew, eh)}")
    # фон по кутах — колір теми (експорт не підмінив і не обрізав фон)
    bg = tuple(int(theme.bg[i:i + 2], 16) for i in (1, 3, 5))
    for px in [(2, 2), (im.width - 3, 2), (2, im.height - 3), (im.width - 3, im.height - 3)]:
        if max(abs(a - b) for a, b in zip(im.getpixel(px), bg)) > 6:
            errs.append(f"рендер {png.name}: фон у {px} = {im.getpixel(px)}, очікувано {theme.bg}")
    errs += check_border_strips(im, m, theme, scale)
    if theme.name == "bw":
        errs += check_grayscale(im, png.name)
    return errs


def check_border_strips(im, m: Model, theme: Theme, scale: int) -> list[str]:
    """Перевірка «текст не вилазить» на реальному рендері, а не на моделі:
    смужка всередині лівої та правої рамки кожного блока (у зоні відступу)
    має бути чистою — лише колір заливки. Ловить розбіжність метрик
    Pillow ↔ браузер, лігатури, підміну шрифту."""
    errs = []
    px = im.load()
    for r in m.rects:
        if r.kind not in ("box", "box_accent", "box_muted"):
            continue
        fill = tuple(int(theme.shapes[r.kind]["fill"][i:i + 2], 16) for i in (1, 3, 5))
        y0, y1 = int((r.y + 12) * scale), int((r.y + r.h - 12) * scale)
        for side, (a, b) in {"праворуч": (r.x + r.w - 12, r.x + r.w - 5),
                             "ліворуч": (r.x + 5, r.x + 12)}.items():
            dirty = sum(1 for x in range(int(a * scale), int(b * scale))
                        for y in range(y0, y1, 2)
                        if max(abs(p - q) for p, q in zip(px[x, y], fill)) > 40)
            if dirty > 3:
                texts = [_plain(t) for t in m.texts if t.parent == r.id]
                errs.append(f"рендер: текст заходить у відступ {side} у {r.id} ({dirty} px): «{texts[:1]}»")
    return errs


def check_grayscale(im: Image.Image, name: str) -> list[str]:
    """ч/б: зображення не має кольору, а після переведення в градації сірого
    не з'являються «злиплі» рівні (текст і фон розрізняються)."""
    errs = []
    r, g, b = im.split()
    from PIL import ImageChops
    chroma = max(ImageChops.difference(r, g).getextrema()[1], ImageChops.difference(g, b).getextrema()[1])
    if chroma > 12:
        errs.append(f"{name}: у ч/б темі є кольорові пікселі (розбіжність каналів {chroma})")
    hist = im.convert("L").histogram()
    dark = sum(hist[:96]) / sum(hist)
    if dark < 0.01:
        errs.append(f"{name}: після grayscale майже немає темних пікселів — текст злився з фоном")
    return errs
