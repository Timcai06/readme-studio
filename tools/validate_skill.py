#!/usr/bin/env python3
"""Repository checks for the skill package (run in CI and before releases).

    python3 tools/validate_skill.py

- frontmatter follows the Agent Skills spec (name, description, compatibility, metadata)
- the skill directory name matches `name`
- SKILL.md stays inside the progressive-disclosure budget (< 500 lines, ~5k tokens)
- every relative file SKILL.md mentions exists, one level deep
- bundled scripts compile and show --help without third-party packages
Standard library only. For the official validator also run:
    uvx --from skills-ref agentskills validate skills/github-profile-studio
"""
from __future__ import annotations

import py_compile
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "github-profile-studio"
errors: list[str] = []


def fail(msg: str):
    errors.append(msg)
    print(f"FAIL {msg}")


def ok(msg: str):
    print(f"ok   {msg}")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("SKILL.md must start with YAML frontmatter between --- lines")
    meta, current = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\S[^:]*:", line):
            key, _, value = line.partition(":")
            current = key.strip()
            meta[current] = value.strip() if value.strip() else {}
        elif current and isinstance(meta[current], dict) and line.startswith("  "):
            k, _, v = line.strip().partition(":")
            meta[current][k.strip()] = v.strip().strip('"')
    return meta, m.group(2)


def main() -> int:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    name = meta.get("name", "")
    if re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and len(name) <= 64:
        ok(f"name '{name}'")
    else:
        fail(f"name '{name}' violates spec (lowercase, digits, single hyphens, <= 64)")
    if SKILL.name == name:
        ok("directory name matches name")
    else:
        fail(f"directory '{SKILL.name}' != name '{name}'")
    desc = meta.get("description", "")
    if 1 <= len(desc) <= 1024:
        ok(f"description {len(desc)} chars")
    else:
        fail(f"description length {len(desc)} (1..1024)")
    if "Use when" not in desc:
        fail("description should say when to use the skill ('Use when …')")
    comp = meta.get("compatibility", "")
    if comp and len(comp) > 500:
        fail(f"compatibility {len(comp)} chars (> 500)")
    if not isinstance(meta.get("metadata", {}), dict):
        fail("metadata must be a mapping")

    lines = text.count("\n") + 1
    tokens = round(len(re.findall(r"\S+", body)) * 1.35)
    (ok if lines < 500 else fail)(f"SKILL.md {lines} lines")
    (ok if tokens < 5000 else fail)(f"SKILL.md body ~{tokens} tokens (estimate)")

    refs = sorted(set(re.findall(r"`((?:references|scripts|assets)/[^`\s]+?)`", body)))
    for ref in refs:
        target = SKILL / ref.split(" ")[0]
        if "*" in ref or "…" in ref or ref.endswith("/"):
            continue
        (ok if target.exists() else fail)(f"reference {ref}")
        if len(Path(ref).parts) > 2:
            fail(f"{ref} is nested deeper than one level")
    for path in sorted((SKILL / "references").glob("*.md")):
        if path.name not in body:
            fail(f"references/{path.name} is never mentioned in SKILL.md (agents won't know to load it)")

    for script in sorted((SKILL / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as err:
            fail(f"{script.name} does not compile: {err}")
            continue
        args = [sys.executable, str(script), "--help"]
        if script.name == "svg_kit.py":
            args = [sys.executable, str(script)]  # prints usage, exit 2
        run = subprocess.run(args, capture_output=True, text=True, timeout=30)
        if run.returncode in (0, 2) and ("usage" in (run.stdout + run.stderr).lower()):
            ok(f"scripts/{script.name} --help")
        else:
            fail(f"scripts/{script.name} --help failed: {run.stderr.strip()[:200]}")

    print(f"\n{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
