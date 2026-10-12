#!/usr/bin/env python3
"""Generate illustrative contours, not geographic data or project output."""
from math import sin, cos, pi
from pathlib import Path
from svg_kit import Svg

OUT = Path(__file__).resolve().parents[1] / 'assets'
PALETTES = {
    'light': ('#f6f7f3', '#899583', '#64765f', '#397887'),
    'dark': ('#111a1d', '#52685d', '#829780', '#83b8c2'),
}

def build(theme, palette):
    bg, contour, index, river = palette
    s = Svg(1200, 200, title='An imagined landscape: contour lines and a river')
    s.add(f'<rect width="1200" height="200" fill="{bg}"/>')
    for cx, cy, phase in [(165, 68, .3), (1050, 215, 1.8)]:
        for level in range(1, 12):
            pts = []
            for i in range(161):
                a = 2 * pi * i / 160
                r = (20 + level * 22) * (1 + .1*sin(3*a+phase) + .055*cos(5*a))
                pts.append(f'{cx+r*cos(a)*1.36:.1f},{cy+r*sin(a)*.62:.1f}')
            major = level % 4 == 0
            s.add(f'<path d="M {" L ".join(pts)} Z" fill="none" stroke="{index if major else contour}" stroke-width="{1.5 if major else .8}"/>')
    for path, width in [
        ('M 615 -10 C 580 35 670 42 645 78 S 530 108 560 140 S 686 160 660 210', 3),
        ('M 785 -5 C 740 26 758 64 645 78', 1.6),
        ('M 455 -5 C 470 43 553 39 587 105', 1.2),
    ]:
        s.add(f'<path d="{path}" fill="none" stroke="{river}" stroke-width="{width}" stroke-linecap="round"/>')
    s.write(OUT / f'watershed-{theme}.svg')

if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for theme, palette in PALETTES.items():
        build(theme, palette)
