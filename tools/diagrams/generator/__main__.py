"""CLI генератора схем.

    python -m generator                     # усі specs/*.yaml, усі теми
    python -m generator reflection-type     # одна схема
    python -m generator --themes dark       # лише одна тема
    python -m generator --no-export         # тільки .drawio + перевірки моделі
    python -m generator --publish           # скопіювати PNG у місця з specs (publish:)

Запускати з теки diagrams/ (make.ps1 / make.sh роблять це самі).
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml

from . import core
from .checks import check_model, check_render
from .core import REPO, ROOT, Metrics, load_themes
from .csharp import run_project, write_project
from .drawio import export, to_xml
from .layout import build


def main(argv=None):
    ap = argparse.ArgumentParser(prog="generator")
    ap.add_argument("specs", nargs="*", help="імена схем (без .yaml); за замовчуванням — усі")
    ap.add_argument("--themes", default="dark,light,bw")
    ap.add_argument("--no-export", action="store_true")
    ap.add_argument("--no-code", action="store_true", help="не компілювати код зі схеми")
    ap.add_argument("--publish", action="store_true", help="скопіювати PNG у шляхи з publish:")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    themes = load_themes()
    names = args.specs or sorted(p.stem for p in (ROOT / "specs").glob("*.yaml"))
    failed = False
    for name in names:
        spec = yaml.safe_load((ROOT / "specs" / f"{name}.yaml").read_text(encoding="utf-8"))
        spec.setdefault("id", name)
        print(f"\n━━ {name}")
        cs = None
        for tname in args.themes.split(","):
            theme = themes[tname]
            metrics = Metrics(theme.font)
            model, cs = build(spec, theme, metrics)
            out = ROOT / "out" / tname
            out.mkdir(parents=True, exist_ok=True)
            src = out / f"{name}.drawio"
            src.write_text(to_xml(model, theme, name), encoding="utf-8")
            errs = check_model(model, theme)
            ratio = model.w / model.h
            print(f"  [{tname}] {model.w}×{model.h} (співвідношення {ratio:.2f}, 16:9 = 1.78), "
                  f"блоків {len(model.rects) - 1}, текстів {len(model.texts)}, стрілок {len(model.edges)}")
            if not args.no_export:
                for fmt in ("png", "pdf"):
                    export(src, fmt, out / f"{name}.{fmt}")
                errs += check_render(out / f"{name}.png", model, theme)
            for e in errs:
                print(f"    ✗ {e}")
            failed |= bool(errs)
            if not errs:
                print("    ✓ перевірки пройдено")
        for w in dict.fromkeys(core.warnings):
            print(f"  ! {w}")
        core.warnings.clear()
        if not args.no_code:
            proj = write_project(spec, cs or [], ROOT / "out" / "check" / name)
            if proj:
                ok, log = run_project(proj)
                print(f"  [C#] {'✓ код зі схеми компілюється і твердження істинні' if ok else '✗ ' + log}")
                failed |= not ok
        if args.publish and not failed:
            for tname, dest in (spec.get("publish") or {}).items():
                d = (ROOT / dest).resolve()
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / "out" / tname / f"{name}.png", d)
                print(f"  → {tname}: {d.relative_to(REPO)}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
