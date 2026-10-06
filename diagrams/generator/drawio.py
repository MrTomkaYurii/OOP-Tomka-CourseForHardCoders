"""Model → .drawio (XML) і експорт через draw.io desktop CLI."""

from __future__ import annotations

import html
import os
import shutil
import subprocess
import tempfile
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from .core import Theme
from .layout import Model


def _num(v):
    return f"{v:g}" if isinstance(v, float) else str(v)


def _style(d: dict) -> str:
    return ";".join(k if v is None else f"{k}={v}" for k, v in d.items()) + ";"


def runs_html(runs, theme: Theme) -> str:
    out = []
    for text, role in runs:
        r = theme.role(role)
        css = [f"color:{r['color']}", "font-variant-ligatures:none"]  # без лігатур: == не стає ═
        if r["bold"]:
            css.append("font-weight:bold")
        if r["italic"]:
            css.append("font-style:italic")
        if r["underline"]:
            css.append("text-decoration:underline")
        esc = html.escape(text, quote=False).replace(" ", "&nbsp;")
        out.append(f'<span style="{";".join(css)}">{esc}</span>')
    return "".join(out)


def to_xml(model: Model, theme: Theme, name: str) -> str:
    mx = ET.Element("mxfile", host="diagrams/generator", type="device")
    dg = ET.SubElement(mx, "diagram", id=f"{name}-{theme.name}", name=f"{name} ({theme.name})")
    gm = ET.SubElement(dg, "mxGraphModel", grid="1", gridSize="8", guides="1", page="0",
                       background=theme.bg, math="0", shadow="0")
    root = ET.SubElement(gm, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    def geom(cell, x, y, w, h):
        ET.SubElement(cell, "mxGeometry", x=_num(x), y=_num(y), width=_num(w), height=_num(h), **{"as": "geometry"})

    for r in model.rects:
        if r.kind == "bg":
            st = {"rounded": 0, "fillColor": theme.bg, "strokeColor": "none", "locked": 1}
        else:
            s = theme.shapes[r.kind]
            st = {"rounded": 1, "absoluteArcSize": 1, "arcSize": 16 if r.kind == "panel" else 10,
                  "whiteSpace": "wrap", "html": 1, "fillColor": s["fill"], "strokeColor": s["stroke"],
                  "strokeWidth": s["width"]}
            if s.get("dashed"):
                st.update({"dashed": 1, "dashPattern": "6 4"})
        cell = ET.SubElement(root, "mxCell", id=r.id, value="", style=_style(st), vertex="1", parent="1")
        geom(cell, r.x, r.y, r.w, r.h)

    for t in model.texts:
        st = {"text": None, "html": 1, "strokeColor": "none", "fillColor": "none", "align": t.align,
              "verticalAlign": "middle", "whiteSpace": "nowrap", "overflow": "visible", "spacing": 0,
              "spacingTop": 0, "spacingBottom": 0, "spacingLeft": 0, "spacingRight": 0,
              "fontFamily": theme.font, "fontSize": t.size, "fontColor": theme.role("text")["color"],
              "resizable": 0, "autosize": 0}
        cell = ET.SubElement(root, "mxCell", id=t.id, value=runs_html(t.runs, theme), style=_style(st),
                             vertex="1", parent="1")
        geom(cell, t.x, t.y, t.w, t.h)

    a = theme.arrow
    for e in model.edges:
        st = {"edgeStyle": "none", "html": 1, "rounded": 0, "endArrow": "block", "endFill": 1, "endSize": 6,
              "strokeColor": a["color"], "strokeWidth": a["width"],
              "exitX": _num(e.exit[0]), "exitY": _num(e.exit[1]), "exitDx": 0, "exitDy": 0,
              "entryX": _num(e.entry[0]), "entryY": _num(e.entry[1]), "entryDx": 0, "entryDy": 0}
        cell = ET.SubElement(root, "mxCell", id=e.id, value="", style=_style(st), edge="1", parent="1",
                             source=e.src, target=e.tgt)
        g = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
        ET.SubElement(g, "mxPoint", x=_num(e.p1[0]), y=_num(e.p1[1]), **{"as": "sourcePoint"})
        ET.SubElement(g, "mxPoint", x=_num(e.p2[0]), y=_num(e.p2[1]), **{"as": "targetPoint"})

    ET.indent(mx)
    return ET.tostring(mx, encoding="unicode")


# ─── Експорт ─────────────────────────────────────────────────────────────────
def find_drawio() -> list[str]:
    """Команда запуску draw.io CLI. Порядок: $DRAWIO, типові шляхи, PATH.
    На Linux без $DISPLAY додається xvfb-run."""
    cands = [os.environ.get("DRAWIO", "")]
    if sys.platform == "win32":
        cands += [os.path.expandvars(r"%LOCALAPPDATA%\Programs\draw.io\draw.io.exe"),
                  r"C:\Program Files\draw.io\draw.io.exe"]
    elif sys.platform == "darwin":
        cands += ["/Applications/draw.io.app/Contents/MacOS/draw.io"]
    cands += [shutil.which("drawio") or "", shutil.which("draw.io") or "", "/opt/drawio/drawio"]
    exe = next((p for p in cands if p and Path(p).exists()), None)
    if not exe:
        raise SystemExit("draw.io desktop не знайдено. Встановіть його або задайте змінну DRAWIO "
                         "(див. diagrams/CLAUDE.md, «Оточення»).")
    cmd = [exe]
    if sys.platform.startswith("linux"):
        # контейнери (хмара, CI, Docker): без sandbox-у Chromium, без GPU, і /dev/shm
        # замалий (64 МБ) — без --disable-dev-shm-usage рендерер падає
        cmd += ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
        if not os.environ.get("DISPLAY") and shutil.which("xvfb-run"):
            cmd = ["xvfb-run", "-a"] + cmd
    return cmd


def export(src: Path, fmt: str, out: Path, scale: int = 2):
    args = ["-x", "-f", fmt, "--border", "0", "-o", str(out)]
    if fmt == "png":
        args += ["-s", str(scale)]
    if fmt == "pdf":
        args += ["--crop"]
    # вивід — у тимчасовий файл, не в pipe: на Linux дочірні процеси Electron (dbus,
    # crashpad) успадковують pipe і тримають його відкритим — communicate() зависає
    with tempfile.TemporaryFile("w+", encoding="utf-8", errors="replace") as log:
        rc = subprocess.run(find_drawio() + args + [str(src)], stdout=log, stderr=subprocess.STDOUT,
                            stdin=subprocess.DEVNULL, timeout=180).returncode
        log.seek(0)
        if rc != 0 or not out.exists():
            raise RuntimeError(f"draw.io export {fmt} failed: {log.read()[-2000:]}")
