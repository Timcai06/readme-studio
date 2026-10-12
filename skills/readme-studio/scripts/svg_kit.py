#!/usr/bin/env python3
"""Small helpers for writing GitHub-safe SVG from code, plus an SVG linter.

Import it from your own generator script (keep the generator in the profile
repository so the art can be rebuilt):

    import sys; sys.path.insert(0, "<skill>/scripts")
    from svg_kit import Svg, esc, measure, wrap, effective_px, embed_raster, typewriter, FONTS

    s = Svg(1200, 360, title="Ada Park — maps, rivers and routing")
    s.add(f'<rect width="1200" height="360" fill="{bg}"/>')
    s.text(64, 120, "Ada Park", size=56, family="serif", fill=ink, weight=600)
    s.write("assets/hero-light.svg")

Or lint files:  python3 svg_kit.py lint assets/*.svg

Why these rules: a README image is rendered through <img>. Inside an <img>
the browser never runs scripts, never loads external files (fonts, images,
stylesheets) and never renders foreignObject HTML reliably. Text is drawn with
whatever fonts the *viewer* has, so widths are estimates; leave slack.

Standard library only; embed_raster() needs Pillow.
"""
from __future__ import annotations

import base64
import io
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

FONTS = {
    "sans": "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif",
    "serif": "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Noto Serif',serif",
    "mono": "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace",
    # CJK fallbacks appended automatically when text contains wide characters.
    "cjk": "'PingFang SC','Hiragino Sans','Noto Sans CJK SC','Microsoft YaHei',sans-serif",
}

# Average advance widths in em. Deliberately a little generous: overestimating
# keeps text inside its box on narrower fonts too.
_SANS = {"narrow": 0.30, "normal": 0.56, "wide": 0.80, "upper": 0.68, "digit": 0.58, "space": 0.28}
_SERIF = {"narrow": 0.30, "normal": 0.52, "wide": 0.82, "upper": 0.70, "digit": 0.54, "space": 0.26}


def esc(s: str) -> str:
    return escape(str(s), quote=True)


def is_wide(ch: str) -> bool:
    return unicodedata.east_asian_width(ch) in ("W", "F")


def measure(text: str, size: float, family: str = "sans", letter_spacing: float = 0.0) -> float:
    """Estimated rendered width in px. Mono = 0.6em, CJK = 1em, emoji ~1.1em."""
    total = 0.0
    table = _SERIF if family == "serif" else _SANS
    for ch in text:
        if is_wide(ch):
            w = 1.0
        elif ord(ch) > 0x1F000:
            w = 1.1
        elif family == "mono":
            w = 0.6
        elif ch == " ":
            w = table["space"]
        elif ch in "iljI.,:;'|!()[]{}tf":
            w = table["narrow"]
        elif ch in "mwMW@%&":
            w = table["wide"]
        elif ch.isdigit():
            w = table["digit"]
        elif ch.isupper():
            w = table["upper"]
        else:
            w = table["normal"]
        total += w * size + letter_spacing
    return total


def wrap(text: str, size: float, max_width: float, family: str = "sans") -> list[str]:
    """Greedy wrap. Splits on spaces; CJK runs may break between characters."""
    lines, line = [], ""
    tokens = re.findall(r"[⺀-鿿豈-﫿＀-￯]|\S+\s*", text)
    for tok in tokens:
        trial = line + tok
        if line and measure(trial.rstrip(), size, family) > max_width:
            lines.append(line.rstrip())
            line = tok.lstrip()
        else:
            line = trial
    if line.strip():
        lines.append(line.rstrip())
    return lines


def effective_px(font_px: float, viewbox_width: float, displayed_width: float) -> float:
    """Size a reader actually sees. Aim for >= 12 px at desktop width for body
    text in images, and remember phones show the image at ~343 px wide."""
    return font_px * displayed_width / viewbox_width


class Svg:
    def __init__(self, width: int, height: int, title: str, desc: str | None = None):
        self.width, self.height = width, height
        self.parts: list[str] = []
        self.defs: list[str] = []
        self.title, self.desc = title, desc

    def add(self, fragment: str) -> "Svg":
        self.parts.append(fragment)
        return self

    def define(self, fragment: str) -> "Svg":
        self.defs.append(fragment)
        return self

    def text(self, x, y, content, size=16, family="sans", fill="#24292f", weight=None,
             anchor=None, extra="") -> "Svg":
        stack = FONTS.get(family, family)
        if any(is_wide(c) for c in str(content)):
            stack = stack.rsplit(",", 1)[0] + "," + FONTS["cjk"]
        attrs = [f'x="{x}"', f'y="{y}"', f'font-size="{size}"', f'font-family="{esc(stack)}"', f'fill="{fill}"']
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if anchor:
            attrs.append(f'text-anchor="{anchor}"')
        if extra:
            attrs.append(extra)
        return self.add(f'<text {" ".join(attrs)} xml:space="preserve">{esc(content)}</text>')

    def render(self) -> str:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
                f'viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="t">'
                f'<title id="t">{esc(self.title)}</title>')
        if self.desc:
            head += f"<desc>{esc(self.desc)}</desc>"
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return head + defs + "".join(self.parts) + "</svg>\n"

    def write(self, path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.render(), encoding="utf-8")
        problems = [p for p in lint_svg(path) if p[0] == "error"]
        if problems:
            raise ValueError(f"{path}: " + "; ".join(p[1] for p in problems))
        return path


def typewriter(svg: "Svg", x: float, y: float, lines: list[str], size: float = 28, family: str = "mono",
               fill: str = "#1f2328", bg: str = "#ffffff", cursor: str | None = None, char_ms: int = 55,
               hold_ms: int = 1600, loop: bool = True, anchor_id: str = "tw") -> "Svg":
    """Typed-text animation that is safe inside <img> on GitHub.

    Each line is revealed by a background-coloured cover sliding right in
    steps (CSS @keyframes on transform; widely supported in SVG images), then
    erased, then the next line types. One line with loop=False types once and
    stays (a name). No scripts, no SMIL, no external fonts.
    Needs a solid background colour behind the text (pass it as bg).
    Reduced motion and no-animation renderers show the first line complete.
    """
    stack = FONTS.get(family, family)
    widths = [measure(line, size, family) + size * 0.2 for line in lines]
    type_ms = [max(1, len(line)) * char_ms for line in lines]
    slot = [t * 2 + hold_ms + 300 if loop else t + hold_ms for t in type_ms]
    total = sum(slot) if loop and len(lines) > 1 else slot[0]
    css = [f".{anchor_id}l{{opacity:0}}.{anchor_id}l0{{opacity:1}}"
           f".{anchor_id}c0{{transform:translateX({widths[0]:.1f}px)}}"]
    start = 0
    for i, line in enumerate(lines):
        w, t = widths[i], type_ms[i]
        pct = lambda ms: f"{100 * ms / total:.3f}%"
        if loop and len(lines) > 1:
            a, b, c, d = start, start + t, start + t + hold_ms, start + 2 * t + hold_ms
            frames = (f"0%{{transform:translateX(0)}}{pct(a)}{{transform:translateX(0);animation-timing-function:steps({len(line)})}}"
                      f"{pct(b)}{{transform:translateX({w:.1f}px)}}{pct(c)}{{transform:translateX({w:.1f}px);animation-timing-function:steps({len(line)})}}"
                      f"{pct(d)}{{transform:translateX(0)}}100%{{transform:translateX(0)}}")
            vis = (f"0%{{opacity:0}}{pct(a)}{{opacity:1}}{pct(d + 250)}{{opacity:1}}"
                   f"{pct(min(total, d + 260))}{{opacity:0}}100%{{opacity:0}}")
            css.append(f"@keyframes {anchor_id}k{i}{{{frames}}}@keyframes {anchor_id}v{i}{{{vis}}}"
                       f".{anchor_id}c{i}{{animation:{anchor_id}k{i} {total}ms linear infinite}}"
                       f".{anchor_id}l{i}{{animation:{anchor_id}v{i} {total}ms step-end infinite}}")
        else:
            css.append(f"@keyframes {anchor_id}k{i}{{from{{transform:translateX(0)}}to{{transform:translateX({w:.1f}px)}}}}"
                       f".{anchor_id}c{i}{{animation:{anchor_id}k{i} {t}ms steps({max(1, len(line))}) both}}")
        start += slot[i]
    css.append("@keyframes %sblink{50%%{opacity:0}}.%scur{animation:%sblink 1s step-end infinite}" % ((anchor_id,) * 3))
    css.append(f"@media (prefers-reduced-motion: reduce){{.{anchor_id}l,.{anchor_id}c,.{anchor_id}cur{{animation:none!important}}}}")
    svg.define(f"<style>{''.join(css)}</style>")
    h = size * 1.35
    for i, line in enumerate(lines):
        w = widths[i]
        cur = (f'<rect class="{anchor_id}cur" x="{x - size * 0.1:.1f}" y="{y - size * 0.95:.1f}" width="{size * 0.08:.1f}" '
               f'height="{size * 1.15:.1f}" fill="{cursor}"/>') if cursor else ""
        svg.add(f'<g class="{anchor_id}l {anchor_id}l{i}"><text x="{x}" y="{y}" font-size="{size}" '
                f'font-family="{esc(stack)}" fill="{fill}" xml:space="preserve">{esc(line)}</text>'
                f'<g class="{anchor_id}c {anchor_id}c{i}"><rect x="{x - 1:.1f}" y="{y - size:.1f}" width="{w + 2:.1f}" '
                f'height="{h:.1f}" fill="{bg}"/>{cur}</g></g>')
    return svg


def embed_raster(path, max_width: int | None = None, colors: int | None = None, fmt: str = "PNG") -> str:
    """Return a data: URI for a raster. Downscale to the size it is shown at
    (2x display width is plenty) and optionally quantize; both shrink SVGs a lot.
    Nearest-neighbour scaling for pixel art (colors set), Lanczos otherwise."""
    from PIL import Image  # optional dependency
    img = Image.open(path)
    img = img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB")
    if max_width and img.width > max_width:
        h = round(img.height * max_width / img.width)
        img = img.resize((max_width, h), Image.Resampling.NEAREST if colors else Image.Resampling.LANCZOS)
    if colors:
        img = img.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT,
                                          dither=Image.Dither.NONE)
    buf = io.BytesIO()
    if fmt.upper() == "JPEG":
        img.convert("RGB").save(buf, "JPEG", quality=82, optimize=True)
        mime = "image/jpeg"
    else:
        img.save(buf, "PNG", optimize=True)
        mime = "image/png"
    return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------- linting --
FORBIDDEN = {"script", "foreignObject", "iframe", "object", "embed", "audio", "video", "canvas"}
EVENT_ATTR = re.compile(r"^on[a-z]+$", re.I)
EXTERNAL = re.compile(r"^(https?:)?//", re.I)


def lint_svg(path, max_kb: int = 1024) -> list[tuple[str, str]]:
    """Return [(severity, message)]. Severity: error | warning | info."""
    path = Path(path)
    out: list[tuple[str, str]] = []
    raw = path.read_bytes()
    size_kb = len(raw) / 1024
    if size_kb > max_kb:
        out.append(("warning", f"{size_kb:.0f} KB; README images over ~1 MB load slowly, "
                               "downscale embedded rasters (embed_raster max_width/colors)"))
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as err:
        return [("error", f"not well-formed XML: {err}")]
    if not root.tag.endswith("svg"):
        return [("error", "root element is not <svg>")]
    if "viewBox" not in root.attrib:
        out.append(("warning", "no viewBox: the image will not scale cleanly with width=\"100%\""))
    if not any(el.tag.split("}")[-1] == "title" for el in root):
        out.append(("info", "no <title>; keep a meaningful alt text in the README instead"))
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag in FORBIDDEN:
            out.append(("error", f"<{tag}> is not rendered (or is blocked) inside <img>"))
        for key, value in el.attrib.items():
            name = key.split("}")[-1]
            if EVENT_ATTR.match(name):
                out.append(("error", f"event handler {name}= on <{tag}> never runs in <img>"))
            if name == "href" and EXTERNAL.match(value):
                out.append(("error", f"external reference {value[:60]} on <{tag}>: not loaded inside <img>; embed as data: URI"))
        if tag == "style" and el.text:
            css = el.text
            if "@import" in css or re.search(r"url\(\s*['\"]?(https?:)?//", css):
                out.append(("error", "external CSS/font in <style> is not loaded inside <img>"))
            if "@font-face" in css and "data:" not in css:
                out.append(("warning", "@font-face without embedded data: the font will not load"))
            if "@keyframes" in css and "prefers-reduced-motion" not in css:
                out.append(("info", "animated: consider @media (prefers-reduced-motion: reduce) to stop motion"))
        if tag in ("animate", "animateTransform", "animateMotion", "set"):
            out.append(("info", "SMIL animation: plays inside <img>; keep it subtle and finite where possible"))
    # dedupe while keeping order
    seen, unique = set(), []
    for item in out:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] != "lint":
        print("usage: svg_kit.py lint FILE.svg [...]", file=sys.stderr)
        return 2
    errors = 0
    for name in argv[1:]:
        problems = lint_svg(name)
        status = "ok" if not problems else ""
        print(f"{name}: {status}")
        for sev, msg in problems:
            errors += sev == "error"
            print(f"  {sev}: {msg}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
