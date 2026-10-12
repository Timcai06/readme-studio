"""Project-README eval case: a small, real, runnable Python library + CLI by a fictional author.

Called from make_fixtures.py. The CLI output in examples/output.txt is produced by running the
fixture's own code, so it is real output an agent may quote.
"""
from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path

INIT = '''"""Tide predictions from harmonic constituents."""
import math
from dataclasses import dataclass

__version__ = "0.4.1"
SPEEDS = {"M2": 28.9841042, "S2": 30.0, "N2": 28.4397295, "K1": 15.0410686, "O1": 13.9430356}


@dataclass
class Constituent:
    name: str
    amplitude: float  # metres
    phase: float      # degrees


def predict(constituents, hours, datum=0.0):
    """Water level (m) at each hour offset: datum + sum(A*cos(speed*t - phase))."""
    out = []
    for t in hours:
        h = datum
        for c in constituents:
            h += c.amplitude * math.cos(math.radians(SPEEDS[c.name] * t - c.phase))
        out.append(round(h, 3))
    return out


def load_csv(path):
    rows = [line.strip().split(",") for line in open(path) if line.strip() and not line.startswith("#")]
    return [Constituent(n, float(a), float(p)) for n, a, p in rows[1:]]
'''

CLI = '''import argparse
from . import load_csv, predict


def sparkline(values):
    bars = "▁▂▃▄▅▆▇█"
    lo, hi = min(values), max(values)
    return "".join(bars[int((v - lo) / (hi - lo or 1) * 7)] for v in values)


def main(argv=None):
    p = argparse.ArgumentParser(prog="tidecalc")
    sub = p.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("predict", help="predict water levels")
    pr.add_argument("station", help="CSV of constituents: name,amplitude,phase")
    pr.add_argument("--hours", type=int, default=24)
    pr.add_argument("--step", type=float, default=1.0)
    pr.add_argument("--datum", type=float, default=0.0)
    pr.add_argument("--spark", action="store_true", help="print a one-line sparkline")
    a = p.parse_args(argv)
    hours = [i * a.step for i in range(int(a.hours / a.step) + 1)]
    levels = predict(load_csv(a.station), hours, a.datum)
    if a.spark:
        print(sparkline(levels))
    else:
        for t, h in zip(hours, levels):
            print(f"{t:5.1f}h  {h:+.3f} m")


if __name__ == "__main__":
    main()
'''

PYPROJECT = '''[project]
name = "tidecalc"
version = "0.4.1"
description = "Tide predictions from harmonic constituents, in pure Python."
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [{name = "Mara Okonkwo"}]

[project.scripts]
tidecalc = "tidecalc.cli:main"
'''

REQUEST = '''This is a fictional test project for an evaluation. Everything you need is in ./repo (my library);
do not look anything up on GitHub or PyPI.

I'm Mara. ./repo is tidecalc, my small Python library + CLI for tide predictions. The README is a
one-line stub. Please write a proper README for it, in place in ./repo. It is also published to
PyPI, so it has to work there. People who find it are mostly hobby sailors and coastal-science
students. Keep it honest — it's a small library. I'll review before committing anything.
'''


def build(here: Path):
    root = here / "project-tidecalc"
    repo = root / "repo"
    for d in ("src/tidecalc", "examples", "tests"):
        (repo / d).mkdir(parents=True, exist_ok=True)
    (repo / "pyproject.toml").write_text(PYPROJECT)
    (repo / "src/tidecalc/__init__.py").write_text(INIT)
    (repo / "src/tidecalc/cli.py").write_text(CLI)
    (repo / "examples/harbour.csv").write_text(
        "# fictional harbour, illustrative values\nname,amplitude,phase\nM2,1.21,112\nS2,0.42,148\nN2,0.24,96\nK1,0.11,201\nO1,0.08,187\n")
    (repo / "tests/test_predict.py").write_text(textwrap.dedent("""\
        from tidecalc import Constituent, predict


        def test_single_constituent_peaks_at_phase():
            assert predict([Constituent("M2", 1.0, 0.0)], [0])[0] == 1.0
        """))
    env = {**os.environ, "PYTHONPATH": str(repo / "src"), "PYTHONDONTWRITEBYTECODE": "1"}
    run = lambda *args: subprocess.run([sys.executable, "-m", "tidecalc.cli", *args], cwd=repo,
                                       capture_output=True, text=True, env=env, check=True).stdout
    table = run("predict", "examples/harbour.csv", "--hours", "12", "--step", "3")
    spark = run("predict", "examples/harbour.csv", "--hours", "48", "--step", "0.5", "--spark")
    (repo / "examples/output.txt").write_text(
        "$ tidecalc predict examples/harbour.csv --hours 12 --step 3\n" + table +
        "$ tidecalc predict examples/harbour.csv --hours 48 --step 0.5 --spark\n" + spark)
    (repo / "README.md").write_text("# tidecalc\n\nTide predictions. `pip install tidecalc`\n")
    (repo / "LICENSE").write_text("MIT License\n\nCopyright (c) 2026 Mara Okonkwo (fictional)\n")
    (root / "request.md").write_text(REQUEST)
    print("fixtures/project-tidecalc: runnable repo + real CLI output")
