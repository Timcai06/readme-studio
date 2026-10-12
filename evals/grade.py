#!/usr/bin/env python3
"""Grade a finished eval workspace against evals.json (automatic assertions only).

    python3 evals/grade.py <case> <workspace> [--readme path/inside/workspace]

Finds the produced README (README.md at the workspace root, else profile/README.md,
else the newest README.md outside .agents/.claude/existing/.profile-studio), runs
check_profile.py on it and evaluates every "auto" assertion. Manual assertions are
listed for a human reviewer. Prints a table and writes <workspace>/.eval/grade.json.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "github-profile-studio" / "scripts"))
import check_profile  # noqa: E402

TEMPLATE_DEFAULTS = ["github-readme-stats", "streak-stats", "github-profile-trophy", "komarev", "snk",
                     "contribution-grid-snake", "readme-typing-svg", "profile-summary-cards", "activity-graph"]
ORIGIN_MARKERS = ["about.ts", "workspace.svg", "EXPLORER", "pixel-lab", "Ln 13, Col", "⎇ main", "TIMCAI06",
                  "Thanks for stopping by"]
SKIP = (".agents", ".claude", "existing", ".profile-studio", ".eval", ".git", "node_modules")


def find_readme(ws: Path, hint: str | None) -> Path | None:
    if hint:
        return ws / hint
    for cand in (ws / "README.md", ws / "profile" / "README.md"):
        if cand.exists():
            return cand
    found = [p for p in ws.rglob("README.md") if not any(s in p.parts for s in SKIP)]
    return max(found, key=lambda p: p.stat().st_mtime) if found else None


def visible_text(md: str) -> str:
    return re.sub(r"<[^>]+>", " ", md)


def tree_hash(path: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(path.rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(path)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def grade(case: str, ws: Path, hint: str | None = None) -> dict:
    spec = next(e for e in json.loads((ROOT / "evals" / "evals.json").read_text())["evals"] if e["id"] == case)
    readme = find_readme(ws, hint)
    results = []

    def add(name, passed, detail=""):
        results.append({"assertion": name, "passed": bool(passed), "detail": detail})

    md = readme.read_text(encoding="utf-8") if readme and readme.exists() else ""
    low = md.lower()
    report_text = ""
    if md:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = check_profile.main([str(readme)])
        report_text = buf.getvalue()
    for a in spec["assertions"]:
        if "auto" not in a:
            continue
        kind = a["auto"]
        if kind == "readme_exists":
            add(kind, bool(md), str(readme.relative_to(ws)) if md else "no README produced")
        elif not md:
            add(kind, False, "no README")
        elif kind == "check_profile_no_errors":
            m = re.search(r"result: (\d+) errors, (\d+) warnings", report_text)
            add(kind, m and m.group(1) == "0", m.group(0) if m else "checker did not run")
        elif kind == "no_template_defaults":
            hits = [t for t in TEMPLATE_DEFAULTS if t in low]
            add(kind, not hits, ", ".join(hits))
        elif kind == "mentions":
            missing = [v for v in a["values"] if v.lower() not in low]
            add(f"mentions {a['values']}", not missing, "missing: " + ", ".join(missing) if missing else "")
        elif kind == "not_mentions":
            hits = [v for v in a["values"] if v.lower() in low]
            add(f"does not mention {a['values']}", not hits, ", ".join(hits))
        elif kind == "no_inflation":
            text = visible_text(low)
            hits = [v for v in a["values"] if re.search(rf"\b{re.escape(v)}\b", text)]
            add("no inflated wording", not hits, ", ".join(hits))
        elif kind == "contains_text":
            missing = [v for v in a["values"] if v not in md]
            add("keeps/contains exact text", not missing, "missing: " + " | ".join(missing) if missing else "")
        elif kind == "max_words":
            words = len(re.findall(r"[A-Za-zÀ-ÿ0-9']+", visible_text(md)))
            add(f"<= {a['value']} words", words <= a["value"], f"{words} words")
        elif kind == "has_fold":
            add("has a <details> fold", "<details" in low)
        elif kind == "lead_before":
            def pos(v):
                i = low.find(v.lower())
                return i if i >= 0 else None
            firsts = [pos(v) for v in a["first"]]
            thens = [pos(v) for v in a["then"] if pos(v) is not None]
            ok = all(f is not None for f in firsts) and all(max(firsts) < t for t in thens)
            add(f"{a['first']} appear before {a['then']}", ok, f"positions {firsts} vs {thens}")
        elif kind == "no_shields_badges":
            add("no shields.io badges", "shields.io" not in low)
        elif kind == "not_like_origin":
            corpus = md + "".join(p.read_text(errors="ignore") for p in readme.parent.rglob("*.svg")
                                  if not any(s in p.parts for s in SKIP))
            hits = [m for m in ORIGIN_MARKERS if m in corpus]
            add("not a clone of the origin profile", not hits, ", ".join(hits))
        elif kind == "contains_arabic":
            add("contains Arabic text", re.search(r"[؀-ۿ]", md) is not None)
        elif kind in ("uses_assets", "uses_svg"):
            pattern = r'(?:src|srcset)="\./?([^"#]+\.svg)' if kind == "uses_svg" else r'(?:src|srcset)="\./?([^"#]+\.(?:svg|png|jpg|jpeg|gif|webp))'
            local = {m for m in re.findall(pattern, md) if not m.startswith("http")}
            add(f"{kind} >= {a['min']}", len(local) >= a["min"], ", ".join(sorted(local))[:200])
        elif kind == "existing_untouched":
            fixture = ROOT / "evals" / "fixtures" / case / "existing"
            add("./existing untouched", tree_hash(fixture) == tree_hash(ws / "existing"))
        else:
            add(kind, False, "unknown assertion")
    manual = [a["manual"] for a in spec["assertions"] if "manual" in a]
    out = {"case": case, "workspace": str(ws), "readme": str(readme) if readme else None,
           "passed": sum(r["passed"] for r in results), "total": len(results), "results": results,
           "manual": manual, "check_profile": report_text}
    (ws / ".eval").mkdir(exist_ok=True)
    (ws / ".eval" / "grade.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    return out


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    hint = argv[argv.index("--readme") + 1] if "--readme" in argv else None
    out = grade(argv[0], Path(argv[1]).resolve(), hint)
    print(f"{out['case']}: {out['passed']}/{out['total']} automatic assertions — {out['readme']}")
    for r in out["results"]:
        print(f"  {'PASS' if r['passed'] else 'FAIL'}  {r['assertion']}  {r['detail']}")
    for m in out["manual"]:
        print(f"  TODO  (manual) {m}")
    return 0 if out["passed"] == out["total"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
