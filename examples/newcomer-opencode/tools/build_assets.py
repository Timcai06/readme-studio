#!/usr/bin/env python3
"""Generate the profile artwork for rafa-souza-dev.

Two image sets, each as a light/dark pair (see .profile-studio/brief.md):

  assets/hero-light.svg       assets/hero-dark.svg
  assets/tiny-todo-light.svg  assets/tiny-todo-dark.svg

Concept: "a quiet terminal session on warm paper". Every string in the art is
drawn from the evidence ledger in .profile-studio/brief.md — the name, the
location, and the literal tiny-todo commands quoted from that repo's README.
Nothing here is invented.

Run:  python3 tools/build_assets.py     (needs svg_kit.py next to it)
"""
from pathlib import Path

from svg_kit import Svg

OUT = Path(__file__).resolve().parent.parent / "assets"

# Warm palette. Light = paper; dark = warm charcoal. One accent in both.
PALETTES = {
    "light": {
        "bg": "#fbf7f0", "panel": "#fffdf9", "ink": "#2b2620",
        "muted": "#6b6152", "accent": "#b45309", "rail": "#e8dfcf", "box": "#c9bfa8",
    },
    "dark": {
        "bg": "#17140f", "panel": "#1c1812", "ink": "#ece5da",
        "muted": "#a99c88", "accent": "#f0b866", "rail": "#332c22", "box": "#4a4030",
    },
}

W, H = 1200, 300
CX = W / 2


def hero(p: dict) -> Svg:
    """Identity plate: name, location label, rule, and the signature checklist mark."""
    s = Svg(
        W, H,
        title="Rafael Souza — CS student, Campinas, Brasil",
        desc="A warm paper panel: the name Rafael Souza, the label Campinas · Brasil, "
             "a short rule, and a small checklist mark.",
    )
    s.add(f'<rect width="{W}" height="{H}" fill="{p["bg"]}"/>')
    s.add(f'<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" '
          f'fill="none" stroke="{p["rail"]}" stroke-width="1.5"/>')

    s.text(CX, 66, "CAMPINAS · BRASIL", size=20, family="mono", fill=p["muted"],
           anchor="middle", extra='letter-spacing="4"')
    s.text(CX, 170, "Rafael Souza", size=72, family="sans", fill=p["ink"],
           weight="600", anchor="middle")
    s.add(f'<line x1="{CX - 80}" y1="206" x2="{CX + 80}" y2="206" '
          f'stroke="{p["accent"]}" stroke-width="2"/>')

    # Signature mark: three small checkboxes, two checked — small things, finishing them.
    size, gap, box_top = 24, 34, 232
    span = 2 * gap + size
    x0 = CX - span / 2
    for i in range(3):
        x = x0 + i * gap
        s.add(f'<rect x="{x:.0f}" y="{box_top}" width="{size}" height="{size}" rx="5" '
              f'fill="none" stroke="{p["box"]}" stroke-width="2"/>')
        if i < 2:
            s.add(f'<path d="M{x + 5:.0f} {box_top + 12} l5 5 l9 -10" fill="none" '
                  f'stroke="{p["accent"]}" stroke-width="3" stroke-linecap="round" '
                  f'stroke-linejoin="round"/>')
    return s


def todo_card(p: dict) -> Svg:
    """Lead-project terminal plate using the real tiny-todo commands from its README."""
    commands = ['todo add "read chapter 4"', "todo list --open", "todo done 3"]
    s = Svg(
        W, H,
        title="tiny-todo — terminal commands",
        desc='A terminal panel showing three real tiny-todo commands: '
             'todo add "read chapter 4", todo list --open, todo done 3.',
    )
    s.add(f'<rect width="{W}" height="{H}" fill="{p["panel"]}"/>')
    s.add(f'<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" '
          f'fill="none" stroke="{p["rail"]}" stroke-width="1.5"/>')

    # Title bar.
    s.add(f'<line x1="0" y1="56" x2="{W}" y2="56" stroke="{p["rail"]}" stroke-width="1.5"/>')
    s.text(40, 36, "~/tiny-todo", size=20, family="mono", fill=p["muted"])
    for i in range(3):
        s.add(f'<rect x="{W - 92 + i * 24}" y="23" width="10" height="10" rx="2" '
              f'fill="{p["rail"]}"/>')

    # Prompt lines: "$" in the accent, the command in ink. No fabricated output.
    y = 118
    for line in commands:
        s.text(40, y, "$", size=26, family="mono", fill=p["accent"], weight="700")
        s.text(66, y, line, size=26, family="mono", fill=p["ink"])
        y += 56
    return s


def main() -> None:
    for theme, palette in PALETTES.items():
        hero(palette).write(OUT / f"hero-{theme}.svg")
        todo_card(palette).write(OUT / f"tiny-todo-{theme}.svg")
    print(f"wrote 4 SVGs to {OUT}")


if __name__ == "__main__":
    main()
