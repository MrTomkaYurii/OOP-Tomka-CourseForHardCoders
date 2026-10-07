"""Базові речі генератора: шрифти й метрики, теми, контраст, розмітка тексту,
підсвітка C# через семантичні ролі та типографська нормалізація."""

from __future__ import annotations

import math
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent  # tools/diagrams/
REPO = ROOT.parent.parent                       # корінь репозиторію
GRID = 8


def snap(v: float) -> int:
    """Округлення вгору до кроку сітки."""
    return int(math.ceil(round(v, 3) / GRID) * GRID)


# ─── Типографічна шкала ──────────────────────────────────────────────────────
# назва → (кегль px, висота рядка px). Висоти рядків кратні 2, щоб центр рядка
# потрапляв на цілий піксель.
TYPE_SCALE = {
    "title":    (28, 40),
    "subtitle": (15, 24),
    "heading":  (18, 28),
    "boxtitle": (15, 24),
    "code":     (14, 22),
    "text":     (14, 22),
    "small":    (13, 20),
}


# ─── Шрифт і метрики ─────────────────────────────────────────────────────────
FONT_CANDIDATES = {
    "JetBrains Mono": ["JetBrainsMono-Regular.ttf", "JetBrainsMono[wght].ttf"],
    "Fira Code": ["FiraCode-Regular.ttf", "FiraCode[wght].ttf"],
}
FONT_DIRS = [
    Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts",
    Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/Windows/Fonts",
    Path.home() / ".local/share/fonts",
    Path.home() / ".fonts",
    Path("/usr/share/fonts"),
    Path("/usr/local/share/fonts"),
    Path.home() / "Library/Fonts",
    Path("/Library/Fonts"),
]


def find_font(family: str) -> Path | None:
    for d in FONT_DIRS:
        if not d.is_dir():
            continue
        for name in FONT_CANDIDATES.get(family, []):
            hits = list(d.rglob(name))
            if hits:
                return hits[0]
    return None


class Metrics:
    """Ширина тексту через Pillow — тим самим TTF, яким рендерить draw.io."""

    def __init__(self, family: str):
        path = find_font(family)
        if path is None:
            raise SystemExit(f"Шрифт «{family}» не знайдено. Встановіть його в систему "
                             f"(див. diagrams/CLAUDE.md, розділ «Оточення»).")
        self.family = family
        self.path = path
        self._cache: dict[int, ImageFont.FreeTypeFont] = {}

    def font(self, size: int) -> ImageFont.FreeTypeFont:
        if size not in self._cache:
            self._cache[size] = ImageFont.truetype(str(self.path), size)
        return self._cache[size]

    def width(self, text: str, size: int) -> float:
        # Pillow хінтує шрифт і округлює advance до цілого пікселя (14px → 8.0 замість 8.4),
        # а браузер у draw.io рендерить дробово. Міряємо у великому кеглі й масштабуємо.
        return self.font(1000).getlength(text) * size / 1000

    def runs_width(self, runs: list[tuple[str, str]], size: int) -> float:
        return self.width("".join(t for t, _ in runs), size)


# ─── Теми ────────────────────────────────────────────────────────────────────
@dataclass
class Theme:
    name: str
    font: str
    bg: str
    shapes: dict          # panel/box/box_accent/box_muted → {fill, stroke, width, dashed}
    arrow: dict           # {color, width}
    roles: dict           # роль → {color, bold, italic, underline}
    raw: dict = field(default_factory=dict)

    def role(self, name: str) -> dict:
        if name not in self.roles:
            raise KeyError(f"Тема {self.name}: невідома роль «{name}»")
        r = self.roles[name]
        return {"color": r["color"], "bold": r.get("bold", False),
                "italic": r.get("italic", False), "underline": r.get("underline", False)}


def load_themes(path: Path | None = None) -> dict[str, Theme]:
    data = yaml.safe_load((path or ROOT / "themes.yaml").read_text(encoding="utf-8"))
    themes = {}
    for name, t in data["themes"].items():
        roles = dict(t["ui"])
        roles.update(t["syntax"])
        themes[name] = Theme(name=name, font=data.get("font", "JetBrains Mono"), bg=t["bg"],
                             shapes=t["shapes"], arrow=t["arrow"], roles=roles, raw=t)
    return themes


# ─── Контраст (WCAG 2.x) ─────────────────────────────────────────────────────
def _lin(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ─── Типографіка ─────────────────────────────────────────────────────────────
CYR = "А-Яа-яЁёІіЇїЄєҐґ"
_APOS = re.compile(rf"(?<=[{CYR}])['’`](?=[{CYR}])")
_DASH = re.compile(r"(?<=\s)[-–](?=\s)")
_QUOTES = re.compile(r'"([^"]+)"')
SMART_TO_ASCII = str.maketrans({"“": '"', "”": '"', "„": '"', "‘": "'", "’": "'", "ʼ": "'"})

warnings: list[str] = []


def normalize_prose(s: str) -> str:
    """Український апостроф ʼ, тире «—» з пробілами, «ялинки», три крапки."""
    s = _APOS.sub("ʼ", s)
    s = _DASH.sub("—", s)
    s = _QUOTES.sub(r"«\1»", s)
    return s.replace("...", "…")


def normalize_code(s: str) -> str:
    fixed = s.translate(SMART_TO_ASCII)
    if fixed != s:
        warnings.append(f"Типографські лапки в коді замінено на ASCII: {s!r}")
    return fixed


# ─── Підсвітка C# ────────────────────────────────────────────────────────────
CS_KEYWORDS = set("""
abstract as base bool break byte case catch char checked class const continue decimal default
delegate do double else enum event explicit extern false finally fixed float for foreach goto if
implicit in int interface internal is lock long namespace new null object operator out override
params private protected public readonly ref return sbyte sealed short sizeof stackalloc static
string struct switch this throw true try typeof uint ulong unchecked unsafe ushort using virtual
void volatile while var not and or when record init get set value nameof async await yield
""".split())

KNOWN_TYPES = set("""
Type Assembly Module MemberInfo MethodBase MethodInfo ConstructorInfo FieldInfo PropertyInfo
EventInfo ParameterInfo TypeInfo BindingFlags Activator Console Object String Int32 Exception
List Dictionary Action Func EventHandler Task Attribute
""".split())

_TOKEN = re.compile(r"""
    (?P<comment>//.*$)
  | (?P<string>\$*"{3,}.*?"{3,}|\$?@?"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)')
  | (?P<number>\b0x[0-9A-Fa-f_]+\b|\b\d[\d_]*(?:\.\d+)?[fFdDmMuUlL]?\b)
  | (?P<ident>@?[A-Za-z_][A-Za-z0-9_]*)
  | (?P<ws>\s+)
  | (?P<punct>.)
""", re.X)


def tokenize_cs(line: str, extra_types: set[str] = frozenset()) -> list[tuple[str, str]]:
    """Рядок C# → [(текст, роль)]. Ролі: keyword, type, method, string, comment,
    number, plain. Фрагмент у [[…]] отримує роль changed (виділення зміни)."""
    out: list[tuple[str, str]] = []
    for i, part in enumerate(re.split(r"\[\[(.+?)\]\]", line)):
        if i % 2:
            out.append((part, "changed"))
            continue
        toks = [(m.lastgroup, m.group()) for m in _TOKEN.finditer(part)]
        for j, (kind, text) in enumerate(toks):
            if kind != "ident":
                role = {"ws": "plain", "punct": "plain"}.get(kind, kind)
                out.append((text, role))
                continue
            nxt = next(((k, t) for k, t in toks[j + 1:] if k != "ws"), (None, ""))
            prev = next(((k, t) for k, t in reversed(toks[:j]) if k != "ws"), (None, ""))
            if text in CS_KEYWORDS:
                role = "keyword"
            elif nxt[1] == "(":
                role = "method"
            elif (text in KNOWN_TYPES or text in extra_types) and prev[1] != ".":
                role = "type"
            elif text[0].isupper() and prev[1] != "." and (nxt[0] == "ident" or nxt[1] in ("?", "[", "<")):
                role = "type"
            else:
                role = "plain"
            out.append((text, role))
    return _merge(out)


def _merge(runs):
    merged: list[tuple[str, str]] = []
    for t, r in runs:
        if merged and merged[-1][1] == r:
            merged[-1] = (merged[-1][0] + t, r)
        else:
            merged.append((t, r))
    return merged


def rich(s: str, base_role: str, extra_types: set[str], code: bool = False) -> list[tuple[str, str]]:
    """Текст із `інлайн-кодом` → runs. Для code=True весь рядок — C#."""
    if code:
        return tokenize_cs(normalize_code(s), extra_types)
    runs = []
    s = re.sub(r"\[\[`([^`]+)`\]\]", lambda m: "`[[" + m.group(1) + "]]`", s)   # [[`код`]] = `[[код]]`
    for i, part in enumerate(s.split("`")):
        if not part:
            continue
        if i % 2:
            runs += tokenize_cs(normalize_code(part), extra_types)
        else:  # у прозі [[…]] — теж роль changed (виділення головного)
            for j, frag in enumerate(re.split(r"\[\[(.+?)\]\]", part)):
                if frag:
                    runs.append((normalize_prose(frag), "changed" if j % 2 else base_role))
    return _merge(runs)
