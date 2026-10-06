"""Розкладка: дерево вузлів із spec.yaml → примітиви (прямокутники, тексти, стрілки)
з абсолютними координатами. Координат у специфікації немає — усі розміри
обчислюються з реальної ширини тексту, позиції — по сітці 8 px."""

from __future__ import annotations

from dataclasses import dataclass, field

from .core import GRID, TYPE_SCALE, Metrics, Theme, rich, snap

# ─── Відступи (усі кратні сітці) ─────────────────────────────────────────────
MARGIN = 32          # поле навколо всієї схеми
PANEL_PAD = 16       # внутрішній відступ розділу
PANEL_GAP = 16       # між дітьми розділу
BOX_PAD_X = 16
BOX_PAD_Y = 12
SECTION_GAP = 8      # між заголовком, кодом і приміткою всередині блока
ARROW_MIN = 48       # мінімальна довжина стрілки
CHAIN_GAP = 40       # вертикальний проміжок між ланками ланцюжка (стрілка + підпис)
LABEL_PAD = 8        # відступ підпису від стрілки


# ─── Примітиви ───────────────────────────────────────────────────────────────
@dataclass
class Rect:
    id: str
    x: float
    y: float
    w: float
    h: float
    kind: str                  # bg | panel | box | box_accent | box_muted
    parent: str | None = None


@dataclass
class Text:
    id: str
    x: float
    y: float
    w: float
    h: float
    runs: list
    size: int
    align: str
    parent: str | None         # прямокутник, у якому стоїть текст
    natural_w: float = 0.0


@dataclass
class Edge:
    id: str
    src: str
    tgt: str
    p1: tuple
    p2: tuple
    exit: tuple
    entry: tuple
    label: str | None = None   # id текстового підпису


@dataclass
class Model:
    w: int = 0
    h: int = 0
    rects: list = field(default_factory=list)
    texts: list = field(default_factory=list)
    edges: list = field(default_factory=list)
    equal_width: list = field(default_factory=list)   # групи id прямокутників однакової ширини
    arrow_groups: list = field(default_factory=list)  # групи id стрілок однакової довжини

    def rect(self, rid):
        return next(r for r in self.rects if r.id == rid)


class Ctx:
    def __init__(self, theme: Theme, metrics: Metrics, types: set[str]):
        self.theme, self.m, self.types = theme, metrics, types
        self.model = Model()
        self._n = 0

    def nid(self, prefix):
        self._n += 1
        return f"{prefix}{self._n}"

    def width(self, runs, style):
        return self.m.runs_width(runs, TYPE_SCALE[style][0])

    def rect(self, x, y, w, h, kind, parent=None):
        r = Rect(self.nid("r"), x, y, w, h, kind, parent)
        self.model.rects.append(r)
        return r.id

    def text(self, x, y, w, runs, style, parent, align="left"):
        size, lh = TYPE_SCALE[style]
        t = Text(self.nid("t"), x, y, w, lh, runs, size, align, parent, self.width(runs, style))
        self.model.texts.append(t)
        return t.id

    def edge(self, src, tgt, p1, p2, exit_, entry, label=None):
        e = Edge(self.nid("e"), src, tgt, p1, p2, exit_, entry, label)
        self.model.edges.append(e)
        return e.id


# ─── Рядки тексту ────────────────────────────────────────────────────────────
@dataclass
class Line:
    """Один рядок: runs + стиль шкали (code/text/small/…)."""
    runs: list
    style: str

    def w(self, c: Ctx):
        return c.width(self.runs, self.style)

    @property
    def lh(self):
        return TYPE_SCALE[self.style][1]


def lines_h(lines):
    return sum(l.lh for l in lines)


# ─── Вузли ───────────────────────────────────────────────────────────────────
class Node:
    def measure(self, c: Ctx) -> tuple[int, int]:
        raise NotImplementedError

    def place(self, c: Ctx, x, y, w, h, parent):
        raise NotImplementedError


class TextBlock(Node):
    def __init__(self, lines: list[Line], align="left"):
        self.lines, self.align = lines, align

    def measure(self, c):
        return snap(max(l.w(c) for l in self.lines)), snap(lines_h(self.lines))

    def place(self, c, x, y, w, h, parent):
        cy = y + (h - lines_h(self.lines)) / 2
        for l in self.lines:
            c.text(x, cy, w, l.runs, l.style, parent, self.align)
            cy += l.lh


class Box(Node):
    """Блок: заголовок (+ тег праворуч), рядки коду, примітки."""

    def __init__(self, kind="box", title=None, tag=None, code=(), notes=(), valign="top", align="left"):
        self.kind, self.title, self.tag = kind, title, tag
        self.code, self.notes = list(code), list(notes)
        self.valign, self.align = valign, align
        self.rect_id = None

    def _sections(self):
        secs = []
        if self.title:
            secs.append([self.title])
        if self.code:
            secs.append(self.code)
        if self.notes:
            secs.append(self.notes)
        return secs

    def content_h(self):
        secs = self._sections()
        return sum(lines_h(s) for s in secs) + SECTION_GAP * (len(secs) - 1)

    def measure(self, c):
        ws = [l.w(c) for s in self._sections() for l in s]
        if self.title and self.tag:
            ws.append(self.title.w(c) + 24 + self.tag.w(c))
        return snap(max(ws) + 2 * BOX_PAD_X), snap(self.content_h() + 2 * BOX_PAD_Y)

    def place(self, c, x, y, w, h, parent):
        self.rect_id = c.rect(x, y, w, h, self.kind, parent)
        cy = y + BOX_PAD_Y if self.valign == "top" else y + (h - self.content_h()) / 2
        tx, tw = x + BOX_PAD_X, w - 2 * BOX_PAD_X
        for i, sec in enumerate(self._sections()):
            for l in sec:
                c.text(tx, cy, tw, l.runs, l.style, self.rect_id, self.align)
                if l is self.title and self.tag:
                    c.text(tx, cy, tw, self.tag.runs, self.tag.style, self.rect_id, "right")
                cy += l.lh
            cy += SECTION_GAP


class Stack(Node):
    def __init__(self, children, gap=PANEL_GAP, spread=False):
        self.children, self.gap, self.spread = children, gap, spread

    def measure(self, c):
        sz = [ch.measure(c) for ch in self.children]
        return max(w for w, _ in sz), sum(h for _, h in sz) + self.gap * (len(sz) - 1)

    def place(self, c, x, y, w, h, parent):
        """Зайва висота: стовпчик розділів ділить її між розділами, інакше — рівномірно
        розширює проміжки (кроками сітки), щоб не лишалося порожнього низу."""
        boxes = []
        hs = [ch.measure(c)[1] for ch in self.children]
        extra = int(h - sum(hs) - self.gap * (len(hs) - 1)) // GRID
        gaps = [self.gap] * len(hs)
        k = 0
        growable = [i for i, ch in enumerate(self.children) if isinstance(ch, (KV, Chain))]
        if extra > 0 and (len(hs) == 1 or (growable and not self.spread)):
            # висоту забирає єдиний нащадок або останній «гнучкий» (таблиця/ланцюжок):
            # він розподілить її по рядках/стрілках, а не лишить порожнього низу
            hs[growable[-1] if growable else 0] += extra * GRID
            extra = 0
        panels = all(isinstance(ch, Panel) for ch in self.children)
        while extra > 0 and len(hs) > 1 and (panels or self.spread):
            if panels:
                hs[k % len(hs)] += GRID
            else:
                gaps[k % (len(hs) - 1)] += GRID
            extra -= 1
            k += 1
        for ch, ch_h, gap in zip(self.children, hs, gaps):
            ch.place(c, x, y, w, ch_h, parent)
            if isinstance(ch, (Box, Panel)):
                boxes.append(ch.rect_id)
            y += ch_h + gap
        if len(boxes) > 1:
            c.model.equal_width.append(boxes)


class Row(Node):
    """Горизонтальний ряд. equal=True — усі діти однакової ширини.
    Висота дітей вирівнюється. Зайва ширина розподіляється кроками сітки."""

    def __init__(self, children, gap=24, equal=False):
        self.children, self.gap, self.equal = children, gap, equal

    def _widths(self, c):
        ws = [ch.measure(c)[0] for ch in self.children]
        return [max(ws)] * len(ws) if self.equal else ws

    def measure(self, c):
        ws = self._widths(c)
        return sum(ws) + self.gap * (len(ws) - 1), max(ch.measure(c)[1] for ch in self.children)

    def place(self, c, x, y, w, h, parent):
        ws = self._widths(c)
        extra = (w - sum(ws) - self.gap * (len(ws) - 1)) // GRID
        if self.equal:   # рівні ширини важливіші: залишок (< n кроків) — симетрично по краях
            ws = [ws[0] + extra // len(ws) * GRID] * len(ws)
            x += extra % len(ws) // 2 * GRID
            extra = 0
        i = 0
        while extra > 0:  # по 8 px кожному по черзі — ширини лишаються кратні сітці
            ws[i % len(ws)] += GRID
            extra -= 1
            i += 1
        for ch, cw in zip(self.children, ws):
            ch.place(c, x, y, cw, h, parent)
            x += cw + self.gap
        if self.equal:
            c.model.equal_width.append([ch.rect_id for ch in self.children if getattr(ch, "rect_id", None)])


class Panel(Node):
    """Розділ схеми: рамка-акцент, заголовок по центру, діти в стовпчик
    (усі діти розтягуються на внутрішню ширину — однакова ширина стовпчика)."""

    def __init__(self, heading: Line | None, children, kind="panel", gap=PANEL_GAP):
        self.heading, self.kind = heading, kind
        self.body = Stack(children, gap)
        self.rect_id = None

    def _head_h(self):
        return snap(self.heading.lh + 4) if self.heading else 0

    def measure(self, c):
        bw, bh = self.body.measure(c)
        hw = snap(self.heading.w(c)) if self.heading else 0
        return max(bw, hw) + 2 * PANEL_PAD, self._head_h() + bh + 2 * PANEL_PAD

    def place(self, c, x, y, w, h, parent):
        self.rect_id = c.rect(x, y, w, h, self.kind, parent)
        iy = y + PANEL_PAD
        if self.heading:
            c.text(x + PANEL_PAD, iy, w - 2 * PANEL_PAD, self.heading.runs, self.heading.style, self.rect_id, "center")
            iy += self._head_h()
        self.body.place(c, x + PANEL_PAD, iy, w - 2 * PANEL_PAD, y + h - PANEL_PAD - iy, self.rect_id)


class Chain(Node):
    """Вертикальний ланцюжок блоків; між ними стрілка вниз з підписом праворуч."""

    def __init__(self, nodes: list[Box], vias: list[Line | None]):
        self.nodes, self.vias = nodes, vias   # vias[i] — підпис стрілки ДО nodes[i]

    def measure(self, c):
        sz = [n.measure(c) for n in self.nodes]
        w = max(w for w, _ in sz)
        for v in self.vias:                    # підпис має вміститися праворуч від центру
            if v:
                w = max(w, snap(2 * (v.w(c) + LABEL_PAD)))
        return w, sum(h for _, h in sz) + CHAIN_GAP * (len(sz) - 1)

    def place(self, c, x, y, w, h, parent):
        """Зайва висота рівномірно подовжує стрілки (кроками сітки) — без порожнього низу."""
        prev = None
        cx = x + snap(w / 2 - GRID / 2)  # центр по сітці
        _, nat = self.measure(c)
        k = len(self.nodes) - 1
        gap = CHAIN_GAP + (int(h - nat) // (k * GRID) * GRID if k and h > nat else 0)
        for n, via in zip(self.nodes, self.vias):
            _, nh = n.measure(c)
            n.place(c, x, y, w, nh, parent)
            if prev:
                p1, p2 = (cx, y - gap), (cx, y)
                lab = None
                if via:
                    lab = c.text(cx + LABEL_PAD, y - gap / 2 - via.lh / 2, x + w - cx - LABEL_PAD,
                                 via.runs, via.style, parent)
                c.edge(prev.rect_id, n.rect_id, p1, p2, ((cx - x) / w, 1), ((cx - x) / w, 0), lab)
            prev = n
            y += nh + gap
        c.model.equal_width.append([n.rect_id for n in self.nodes])


class Flow(Node):
    """Ряди «блок → (підпис) → блок». Ліві блоки однакової ширини, праві — теж,
    стрілки однакової довжини, строго горизонтальні; підпис над стрілкою по центру."""

    def __init__(self, rows: list[tuple[Box, Line | None, Box]], gap=8):
        self.rows, self.gap = rows, gap

    def _dims(self, c):
        lw = max(l.measure(c)[0] for l, _, _ in self.rows)
        rw = max(r.measure(c)[0] for _, _, r in self.rows)
        labs = [lab.w(c) for _, lab, _ in self.rows if lab]
        aw = max(ARROW_MIN, snap(max(labs) + 2 * LABEL_PAD) if labs else 0)
        rh = [max(l.measure(c)[1], r.measure(c)[1] + 0) for l, _, r in self.rows]
        return lw, aw, rw, rh

    def measure(self, c):
        lw, aw, rw, rh = self._dims(c)
        return lw + aw + rw, sum(rh) + self.gap * (len(rh) - 1)

    def place(self, c, x, y, w, h, parent):
        lw, aw, rw, rh = self._dims(c)
        extra = w - (lw + aw + rw)
        lw += (extra // (2 * GRID)) * GRID
        rw = w - lw - aw
        arrows = []
        for (l, lab, r), hh in zip(self.rows, rh):
            l.place(c, x, y, lw, hh, parent)
            r.place(c, x + lw + aw, y, rw, hh, parent)
            mid = y + hh / 2
            lid = None
            if lab:
                lid = c.text(x + lw, mid - lab.lh - 2, aw, lab.runs, lab.style, parent, "center")
            arrows.append(c.edge(l.rect_id, r.rect_id, (x + lw, mid), (x + lw + aw, mid), (1, 0.5), (0, 0.5), lid))
            y += hh + self.gap
        c.model.equal_width += [[l.rect_id for l, _, _ in self.rows], [r.rect_id for _, _, r in self.rows]]
        c.model.arrow_groups.append(arrows)


class KV(Node):
    """Таблиця групами: перша колонка — код (ключ), решта — текст; ширини колонок
    спільні для всіх груп. columns — необов'язковий рядок-заголовок над першою групою."""

    COL_GAP = 24

    def __init__(self, groups: list[tuple[Line | None, list[list[Line]]]], columns: list[Line] | None = None,
                 gap=16):
        self.groups, self.columns, self.gap = groups, columns, gap
        self.rect_id = None
        self.pad = 0   # додаткова висота рядка (заповнення стовпчика)

    def _all_rows(self):
        rows = [r for _, rs in self.groups for r in rs]
        return rows + ([self.columns] if self.columns else [])

    def _cw(self, c):
        n = max(len(r) for r in self._all_rows())
        return [max((r[i].w(c) for r in self._all_rows() if len(r) > i), default=0) for i in range(n)]

    @staticmethod
    def _rh(row):
        return max(cell.lh for cell in row)

    def _gh(self, gi, head, rows, pad=0):
        top = (head.lh + SECTION_GAP if head else 0)
        if gi == 0 and self.columns:
            top += self._rh(self.columns) + SECTION_GAP
        return snap(top + sum(self._rh(r) + pad for r in rows) + 2 * BOX_PAD_Y)

    def measure(self, c):
        cw = self._cw(c)
        w = sum(cw) + self.COL_GAP * (len(cw) - 1)
        for head, _ in self.groups:
            if head:
                w = max(w, head.w(c))
        h = sum(self._gh(i, hd, rows) for i, (hd, rows) in enumerate(self.groups)) + self.gap * (len(self.groups) - 1)
        return snap(w + 2 * BOX_PAD_X), h

    def _row(self, c, x, y, row, cw, rid, right):
        rh = self._rh(row)
        for i, cell in enumerate(row):
            last = i == len(row) - 1
            cx = x + sum(cw[:i]) + self.COL_GAP * i
            c.text(cx, y + (rh - cell.lh) / 2, (right - cx) if last else cw[i], cell.runs, cell.style, rid)
        return rh

    def place(self, c, x, y, w, h, parent):
        """Зайву висоту таблиця віддає рядкам (до +12 px на рядок, кратно 2; решту — останній групі):
        стовпчик вирівнюється за висотою без порожнього низу й дірок між блоками."""
        cw = self._cw(c)
        ids, y0 = [], y
        n = sum(len(rows) for _, rows in self.groups)
        _, nat = self.measure(c)
        self.pad = min(12, int((h - nat) / n) // 2 * 2) if h > nat else 0
        for gi, (head, rows) in enumerate(self.groups):
            gh = self._gh(gi, head, rows, self.pad)
            if gi == len(self.groups) - 1:      # остання група дотягується до низу стовпчика
                gh = max(gh, int((h - (y - y0)) // GRID * GRID))
            rid = c.rect(x, y, w, gh, "box", parent)
            ids.append(rid)
            cy, tx, right = y + BOX_PAD_Y, x + BOX_PAD_X, x + w - BOX_PAD_X
            if head:
                c.text(tx, cy, w - 2 * BOX_PAD_X, head.runs, head.style, rid)
                cy += head.lh + SECTION_GAP
            if gi == 0 and self.columns:
                cy += self._row(c, tx, cy, self.columns, cw, rid, right) + SECTION_GAP
            for row in rows:
                cy += self._row(c, tx, cy + self.pad / 2, row, cw, rid, right) + self.pad
            y += gh + self.gap
        c.model.equal_width.append(ids)


# ─── Розбір специфікації ─────────────────────────────────────────────────────
class SpecError(Exception):
    pass


class Builder:
    """YAML-вузли → дерево Node. Паралельно збирає фрагменти C# для перевірки компіляцією."""

    def __init__(self, spec: dict):
        self.spec = spec
        self.types = set(spec.get("types", []))
        self.cs: list[str] = []      # інструкції з блоків коду — у порядку специфікації
        self.cs_expr: list[str] = [] # перевірки виразів (kv/flow/via) — після всіх інструкцій

    # рядки
    def line(self, s, role="text", style="text", code=False):
        return Line(rich(str(s), role, self.types, code=code), style)

    def code_lines(self, block):
        if not block:
            return []
        return [self.line(s, style="code", code=True) for s in str(block).rstrip("\n").split("\n")]

    def note_lines(self, notes, role="muted"):
        if not notes:
            return []
        notes = [notes] if isinstance(notes, str) else notes
        return [self.line(n, role, "small") for n in notes]

    def _check(self, template, text):
        if template and template != "skip":
            self.cs_expr.append(template.replace("{}", text))

    # вузли
    def node(self, d) -> Node:
        if not isinstance(d, dict) or len(d) != 1:
            raise SpecError(f"Вузол має бути словником з одним ключем-типом: {d!r}")
        (kind, v), = d.items()
        fn = getattr(self, f"n_{kind}", None)
        if fn is None:
            raise SpecError(f"Невідомий тип вузла «{kind}»")
        return fn(v or {})

    def nodes(self, lst):
        return [self.node(x) for x in lst]

    def n_row(self, v):
        return Row(self.nodes(v["children"]), gap=v.get("gap", 24), equal=v.get("equal", False))

    def n_stack(self, v):
        return Stack(self.nodes(v["children"]), gap=v.get("gap", PANEL_GAP), spread=v.get("spread", False))

    def n_panel(self, v):
        head = self.line(v["heading"], "heading", "heading") if v.get("heading") else None
        return Panel(head, self.nodes(v.get("children", [])), gap=v.get("gap", PANEL_GAP))

    def n_box(self, v):
        if v.get("code") and v.get("check", "stmt") != "skip":
            self.cs.append(f"// --- {v.get('title', 'box')}")
            self.cs += [normalize_line(s) for s in str(v["code"]).rstrip("\n").split("\n")]
        return Box(kind=v.get("kind", "box"),
                   title=self.line(v["title"], "boxtitle", "boxtitle") if v.get("title") else None,
                   tag=self.line(v["tag"], "tag", "small") if v.get("tag") else None,
                   code=self.code_lines(v.get("code")) + [self.line(s) for s in v.get("text", [])],
                   notes=self.note_lines(v.get("notes")),
                   valign=v.get("valign", "top"), align=v.get("align", "left"))

    def n_note(self, v):
        return Box(kind=v.get("kind", "box_muted"), notes=self.note_lines(v["text"], v.get("role", "muted")),
                   valign="middle", align=v.get("align", "left"))

    def n_text(self, v):
        return TextBlock(self.note_lines(v["text"], v.get("role", "muted")), v.get("align", "left"))

    def n_chain(self, v):
        nodes, vias = [], []
        for item in v["nodes"]:
            if item.get("lines") and item.get("lines_check", "stmt") == "stmt":
                self.cs += [normalize_line(x) for x in str(item["lines"]).rstrip("\n").split("\n")]
            nodes.append(Box(kind=item.get("kind", "box"),
                             title=self.line(item["title"], "boxtitle", "boxtitle", code=item.get("code", False)),
                             code=self.code_lines(item.get("lines")),
                             notes=self.note_lines(item.get("sub")), valign="middle",
                             align=v.get("align", "center")))
            via = item.get("via")
            vias.append(self.line(via, "label", "small") if via else None)
            if via:
                self._check(item.get("check"), via.strip("`"))
        return Chain(nodes, vias)

    def n_flow(self, v):
        rows = []
        tmpl = v.get("check")
        for r in v["rows"]:
            left, right = r["left"], r["right"]
            if v.get("left_code", True):
                self._check(tmpl, left)
            cell = lambda s, code: Box(code=[self.line(s, style="code", code=True) if code
                                             else self.line(s, "text", "small")], valign="middle")
            lab = self.line(r["label"], "label", "small") if r.get("label") else None
            rows.append((cell(left, v.get("left_code", True)), lab, cell(right, v.get("right_code", True))))
        flow = Flow(rows, gap=v.get("gap", 8))
        if v.get("caption"):
            return Stack([TextBlock(self.note_lines(v["caption"])), flow], gap=8)
        return flow

    def n_kv(self, v):
        groups = []
        tmpl = v.get("check")
        key_code = v.get("key_code", True)
        for g in v["groups"]:
            head = self.line(g["heading"], "muted", "small") if g.get("heading") else None
            rows = []
            for r in g["rows"]:
                k, *vals = r
                if key_code and k:
                    self._check(g.get("check", tmpl), k)   # група може перевизначити (напр. skip для сигнатур)
                key = self.line(k, style="code", code=True) if key_code else self.line(k, "text", "small")
                rows.append([key] + [self.line(x, "text", "small") for x in vals])
            groups.append((head, rows))
        cols = [self.line(x, "muted", "small") for x in v["columns"]] if v.get("columns") else None
        return KV(groups, cols)

    def root(self) -> Node:
        s = self.spec
        head = [self.line(s["title"], "title", "title")]
        if s.get("subtitle"):
            head.append(self.line(s["subtitle"], "subtitle", "subtitle"))
        return Stack([TextBlock(head, "center")] + self.nodes(s["body"]), gap=24)


def normalize_line(s):
    from .core import normalize_code
    return normalize_code(s.replace("[[", "").replace("]]", ""))


def build(spec: dict, theme: Theme, metrics: Metrics) -> tuple[Model, list[str]]:
    b = Builder(spec)
    root = b.root()
    c = Ctx(theme, metrics, b.types)
    w, h = root.measure(c)
    W, H = w + 2 * MARGIN, h + 2 * MARGIN
    c.model.w, c.model.h = W, H
    c.model.rects.append(Rect("bg", 0, 0, W, H, "bg"))
    root.place(c, MARGIN, MARGIN, w, h, "bg")
    return c.model, b.cs + ["// --- вирази з таблиць і стрілок"] + b.cs_expr
