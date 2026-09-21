#!/usr/bin/env python3
"""
Генератор схем структури проєкту для інструкцій лаб (Лаби 06-22).

Джерело правди — еталонні гілки `feature/*` (лінійний ланцюжок 05 → 22).
Для кожної лаби N:
  - початок = стан src/ наприкінці лаби N-1 (без позначок),
  - кінець  = стан src/ наприкінці лаби N   (🆕 новий, ✏ змінено).

Використання (з кореня репозиторію):
  python tools/structure/gen_structure.py --show 6 17 22   # надрукувати дерева
  python tools/structure/gen_structure.py --audit          # звірити git add у старих інструкціях з еталоном
  python tools/structure/gen_structure.py --apply          # вставити розділи в labs/lab-NN-*/instructions.md

Розділи, що вже є в файлі, не дублюються (перевірка за заголовком).
Номери задач (Тn) генератор НЕ ставить — вони додаються вручну під час переробки конкретної лаби,
бо мусять збігатись з комітами цієї лаби.
"""
import argparse, glob, os, re, subprocess, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# лаба -> гілка (17-20 лежать на одній гілці ef-core: беремо коміт останньої задачі лаби)
BRANCH = {5: "feature/encapsulation", 6: "feature/inheritance", 7: "feature/interfaces",
          8: "feature/polymorphism", 9: "feature/generics", 10: "feature/iterators",
          11: "feature/reflection", 12: "feature/files", 13: "feature/events",
          14: "feature/linq", 15: "feature/functional", 16: "feature/console-ui",
          21: "feature/async", 22: "feature/solid-di"}
EF_LABS = (17, 18, 19, 20)

# розходження «еталон ↔ інструкція», уже вирішені в інструкціях (Лаба 05)
PATH_OVERRIDE = {"GrowablePatientManager.cs": "Managers/GrowablePatientManager.cs"}

# початковий порядок файлів = порядок у дереві Лаби 05 (далі нові файли додаються в кінець)
SEED_ORDER = ["ClinicApp.csproj", "Program.cs", "Clinic.cs",
              "Enums/AppointmentStatus.cs", "Enums/BloodType.cs", "Enums/Speciality.cs",
              "Models/Patient.cs", "Models/Doctor.cs", "Models/Appointment.cs", "Models/WorkSchedule.cs",
              "Managers/PatientManager.cs", "Managers/DoctorManager.cs",
              "Managers/AppointmentManager.cs", "Managers/GrowablePatientManager.cs",
              "Utils/ClinicFormatter.cs", "Utils/ClinicValidator.cs"]
COLLAPSE_ALWAYS = {"Migrations"}   # генерується EF — показуємо одним рядком
MAX_UNCHANGED = 6                  # більше незмінених файлів у теці — згортаємо в «… ще N файлів»


def git(*args):
    r = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=REPO,
                       capture_output=True, text=True, encoding="utf-8")
    return r.stdout


def files_word(n):
    """українське відмінювання: 1 файл, 2-4 файли, 5+ файлів"""
    if n % 10 == 1 and n % 100 != 11: return f"{n} файл"
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14: return f"{n} файли"
    return f"{n} файлів"


def lab_ref(n):
    if n in BRANCH:
        return BRANCH[n]
    sha = git("log", "feature/ef-core", "--grep", f"^Lab{n} Task", "-1", "--format=%H").strip()
    if not sha:
        sys.exit(f"не знайдено коміт для Лаби {n} на feature/ef-core")
    return sha


def state_of(n):
    """{відносний шлях у ClinicApp/: sha блоба} на кінець лаби n."""
    st = {}
    for line in git("ls-tree", "-r", lab_ref(n), "--", "src/").splitlines():
        meta, path = line.split("\t", 1)
        sha = meta.split()[2]
        if not path.startswith("src/"):
            continue
        rel = path[4:]
        if rel.startswith((".claude", "bin/", "obj/")) or "/bin/" in rel or "/obj/" in rel:
            continue
        rel = PATH_OVERRIDE.get(rel, rel)
        st[rel] = sha
    return st


STATES = {n: state_of(n) for n in range(5, 23)}


def build_rank():
    rank, order = {}, []
    def add(p):
        if p not in rank:
            rank[p] = len(order); order.append(p)
    for p in SEED_ORDER:
        add(p)
    known_dirs = []
    for p in SEED_ORDER:
        d = p.split("/")[0] if "/" in p else ""
        if d and d not in known_dirs:
            known_dirs.append(d)
    for n in range(6, 23):
        new = sorted(set(STATES[n]) - set(STATES[n - 1]))
        for p in new:
            d = p.split("/")[0] if "/" in p else ""
            if d and d not in known_dirs:
                known_dirs.append(d)
        # нові файли: спочатку в існуючих теках (за порядком тек), потім у нових
        new.sort(key=lambda p: (known_dirs.index(p.split("/")[0]) if "/" in p else -1, p))
        for p in new:
            add(p)
    return rank


RANK = build_rank()


def changes(n):
    prev, cur = STATES[n - 1], STATES[n]
    new = {p for p in cur if p not in prev}
    chg = {p for p in cur if p in prev and cur[p] != prev[p]}
    gone = {p for p in prev if p not in cur}
    return new, chg, gone


def render(n, end):
    new, chg, gone = changes(n)
    files = set(STATES[n] if end else STATES[n - 1])
    touched = new | chg
    expanded = {""}
    for p in touched:
        parts = p.split("/")[:-1]
        for i in range(1, len(parts) + 1):
            expanded.add("/".join(parts[:i]))

    def rk(p): return RANK.get(p, 10 ** 6)

    def mark(p):
        if not end: return ""
        return "🆕" if p in new else ("✏" if p in chg else "")

    lines = []   # (текст ліворуч, позначка)

    def walk(d, prefix):
        sub = {}
        direct = []
        for p in files:
            if d and not p.startswith(d + "/"): continue
            rest = p[len(d) + 1:] if d else p
            if "/" in rest:
                sub.setdefault(rest.split("/")[0], []).append(p)
            else:
                direct.append(p)
        unchanged = [p for p in direct if p not in touched]
        hide = set()
        if d in expanded and len(unchanged) > MAX_UNCHANGED:
            hide = set(unchanged)
        entries = []
        for p in direct:
            if p in hide: continue
            entries.append((min(rk(p), 10 ** 6), "file", p))
        for name, ps in sub.items():
            entries.append((min(rk(x) for x in ps), "dir", (name, ps)))
        entries.sort(key=lambda e: e[0])
        if hide:
            entries.append((10 ** 7, "more", len(hide)))
        for i, (_, kind, val) in enumerate(entries):
            last = i == len(entries) - 1
            conn = "└── " if last else "├── "
            cp = prefix + ("    " if last else "│   ")
            if kind == "file":
                lines.append((prefix + conn + val.split("/")[-1], mark(val)))
            elif kind == "more":
                lines.append((prefix + conn + f"… ще {files_word(val)} без змін", ""))
            else:
                name, ps = val
                full = (d + "/" + name) if d else name
                if full in expanded and name not in COLLAPSE_ALWAYS:
                    lines.append((prefix + conn + name + "/", ""))
                    walk(full, cp)
                else:
                    cnt = len(ps)
                    extra = " — генерує EF" if name in COLLAPSE_ALWAYS else ""
                    m = ""
                    if end and any(x in new for x in ps): m = "🆕"
                    elif end and any(x in chg for x in ps): m = "✏"
                    lines.append((prefix + conn + name + "/" + f"  ({files_word(cnt)}{extra})", m))

    lines.append(("oop-course/", "__HDR__"))
    lines.append(("├── .gitignore", ""))
    lines.append(("├── oop-course.sln", ""))
    lines.append(("└── ClinicApp/", ""))
    walk("", "    ")
    width = max(len(t) for t, m in lines[1:]) + 3
    width = max(width, 38)
    out = []
    for t, m in lines:
        if m == "__HDR__":
            note = (f"← гілка Lab-{n:02d} (після злиття — main)" if end
                    else f"← гілка main (після злиття Лаби {n - 1:02d})")
            out.append(t.ljust(width) + note)
        else:
            out.append((t.ljust(width) + m).rstrip())
    return "\n".join(out)


LEGEND = ("**Легенда:** 🆕 — новий файл · ✏ — змінено вміст. Файли без позначки лишились такими, "
          "як були після попередньої лаби. Рядок «… ще N файлів без змін» — стислий запис незмінених файлів теки.")
DOMAIN_NOTE = ("Назви файлів наведено для домену «клініка»; у власному домені назви ваші — "
               "важливі теки та те, що саме створюється й змінюється.")


def start_section(n):
    return ("## Структура проєкту на початку лаби\n\n"
            f"Це результат Лаби {n - 1:02d} — стан `main` після її злиття:\n\n"
            "```text\n" + render(n, False) + "\n```\n\n"
            "Структуру **наприкінці** лаби (з позначками, що створюється і змінюється) наведено "
            "в розділі «Структура проєкту наприкінці лаби» перед перевіркою.\n\n---\n\n")


def end_section(n):
    return ("## Структура проєкту наприкінці лаби\n\n"
            "Так має виглядати `ClinicApp/`, коли всі завдання виконано:\n\n"
            "```text\n" + render(n, True) + "\n```\n\n" + LEGEND + "\n\n" + DOMAIN_NOTE + "\n\n---\n\n")


def lab_file(n):
    m = glob.glob(os.path.join(REPO, "labs", f"lab-{n:02d}-*", "instructions.md"))
    return m[0] if m else None


def audit(n):
    p = lab_file(n)
    txt = open(p, encoding="utf-8").read()
    cur = STATES[n]
    new, chg, gone = changes(n)
    used, missing = set(), []
    for line in re.findall(r"^git add (.+)$", txt, re.M):
        for tok in line.split():
            if tok.startswith("-"): continue
            rel = tok[4:] if tok.startswith("src/") else tok
            rel = PATH_OVERRIDE.get(rel, rel)
            if rel in cur:
                used.add(rel)
            elif rel.endswith("/") and any(f.startswith(rel) for f in cur):
                used |= {f for f in cur if f.startswith(rel)}
            elif rel.endswith("/."):
                continue
            else:
                missing.append(tok)
    uncovered = sorted((new | chg) - used)
    return missing, uncovered, sorted(gone)


END_ANCHORS = [r"^## Перевірка перед здачею", r"^## Перевірка\b", r"^## Питання для самоперевірки",
               r"^## Рефлексійні питання", r"^## Статус гілки", r"^## Злиття"]


def apply(n, dry=False):
    p = lab_file(n)
    raw = open(p, encoding="utf-8").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    txt = raw.replace("\r\n", "\n")
    status = []
    if not re.search(r"^#{2,3} Структура проєкту на початку лаби", txt, re.M):
        m = re.search(r"^## Гілка", txt, re.M)
        if m:
            txt = txt[:m.start()] + start_section(n) + txt[m.start():]
            status.append("початок ✔")
        else:
            status.append("початок ✘ (нема «## Гілка»)")
    else:
        status.append("початок вже є")
    if not re.search(r"^#{2,3} Структура проєкту наприкінці лаби", txt, re.M):
        pos = None
        for pat in END_ANCHORS:
            m = re.search(pat, txt, re.M)
            if m:
                pos = m.start()
                break
        if pos is not None:
            txt = txt[:pos] + end_section(n) + txt[pos:]
            status.append("кінець ✔")
        else:
            status.append("кінець ✘ (нема жодного якоря)")
    else:
        status.append("кінець вже є")
    if "Структура проєкту збігається" not in txt:
        m = re.search(r"^## Перевірка( перед здачею)?[ \t]*$", txt, re.M)
        if m:
            b = re.search(r"^- \[ \] ", txt[m.end():], re.M)
            if b:
                at = m.end() + b.start()
                txt = txt[:at] + "- [ ] Структура проєкту збігається зі схемою вище\n" + txt[at:]
                status.append("чекліст ✔")
            else:
                status.append("чекліст ✘ (нема «- [ ]» після «Перевірка»)")
        else:
            status.append("чекліст ✘ (нема розділу «Перевірка»)")
    if not dry:
        open(p, "w", encoding="utf-8", newline="").write(txt.replace("\n", nl))
    return status


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", nargs="*", type=int)
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--labs", nargs="*", type=int, default=list(range(6, 23)))
    a = ap.parse_args()
    if a.show:
        for n in a.show:
            print(f"\n######## Лаба {n}: початок\n{render(n, False)}\n\n######## Лаба {n}: кінець\n{render(n, True)}")
    if a.audit:
        for n in a.labs:
            missing, uncovered, gone = audit(n)
            print(f"Лаба {n:02d}: git add вказує на неіснуючі шляхи: {missing or '—'} | змінено в еталоні, але немає в git add: {uncovered or '—'}" + (f" | видалено: {gone}" if gone else ""))
    if a.apply:
        for n in a.labs:
            print(f"Лаба {n:02d}:", ", ".join(apply(n, a.dry)))
