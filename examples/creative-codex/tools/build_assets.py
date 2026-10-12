#!/usr/bin/env python3
"""Rebuild the cover and copy owner-supplied artwork without altering it.
Run from any directory: python3 tools/build_assets.py
"""
from pathlib import Path
import shutil
from svg_kit import Svg, measure

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
PAPER, TEAL, PINK = "#f6f0e4", "#00838a", "#ff48b0"
# Cover copy: snapshot.json user.bio; colours: artwork/kufic-grid.png.
s = Svg(1200, 400, title="Letters, tides, print.")
s.add(f'<rect width="1200" height="400" fill="{PAPER}"/>')
s.add(f'<rect x="68" y="58" width="40" height="8" fill="{PINK}"/>')
for y, text in [(187, "Letters,"), (315, "tides, print.")]:
    assert measure(text, 116, "serif") < 1010
    s.text(64, y, text, size=116, family="serif", fill=TEAL)
s.add(f'<path d="M1064 270v62m-31-31h62" stroke="{PINK}" stroke-width="3"/>')
s.write(OUT / "cover.svg")
for name in ("kufic-grid.png", "qamar-specimen.png", "tide-sketches.png"):
    shutil.copyfile(ROOT / "artwork" / name, OUT / name)
print("Built cover.svg and copied 3 unchanged source artworks.")
