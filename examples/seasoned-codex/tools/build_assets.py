#!/usr/bin/env python3
"""Rebuild the static command artwork. No network or third-party packages.
Copy source: snapshot.json, repos[name=migra-lint].readme_excerpt.
The caption is editorial; this is a command specimen, not captured output.
"""
from pathlib import Path
from svg_kit import Svg, measure

ROOT = Path(__file__).resolve().parents[1]
COMMAND = "migra-lint check migrations/*.sql"
CAPTION = "CHECK MIGRATIONS BEFORE PRODUCTION"
PALETTES = {
    "dark": ("#151b23", "#e6edf3", "#99a6b5", "#70d6bf", "#3d444d"),
    "light": ("#f6f8fa", "#1f2328", "#59636e", "#096b59", "#d1d9e0"),
}

for theme, (bg, ink, muted, accent, border) in PALETTES.items():
    svg = Svg(720, 132, "Check migrations before production",
              "Command from the migra-lint README: " + COMMAND)
    svg.add(f'<rect x="0.5" y="0.5" width="719" height="131" rx="6" fill="{bg}" stroke="{border}"/>')
    svg.add(f'<path d="M24 28V104" stroke="{accent}" stroke-width="3"/>')
    svg.text(44, 43, CAPTION, size=16, family="mono", fill=muted)
    svg.text(44, 88, COMMAND, size=27, family="mono", fill=ink)
    assert 44 + measure(COMMAND, 27, "mono") * 1.1 < 696
    svg.write(ROOT / "assets" / f"migration-{theme}.svg")
