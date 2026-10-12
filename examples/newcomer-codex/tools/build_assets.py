"""Rebuild the small checklist mark: python3 tools/build_assets.py."""
from pathlib import Path
from svg_kit import Svg

OUT = Path(__file__).resolve().parents[1] / "assets"
# Motif from tiny-todo's task list; an illustration, not a test-status indicator.
s = Svg(80, 80, title="A small checklist for tiny-todo")
s.add('<rect x="1" y="1" width="78" height="78" rx="18" fill="#f7efe3"/>')
s.add('<rect x="23" y="16" width="39" height="49" rx="4" fill="#fffaf3" stroke="#9b563d" stroke-width="2"/>')
s.add('<path d="M18 26h9 M18 39h9 M18 52h9" stroke="#9b563d" stroke-width="2" stroke-linecap="round"/>')
s.add('<path d="m33 30 3 3 6-7 M46 30h8 M33 44h21 M33 54h15" fill="none" stroke="#704534" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
s.write(OUT / "checklist.svg")
