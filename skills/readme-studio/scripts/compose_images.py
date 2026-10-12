#!/usr/bin/env python3
"""Turn real screenshots, frames and figures into README-ready images.

Requires Pillow (`pip install pillow`).

  crop    Cut browser chrome, bookmarks, URLs and desktop edges out of a screenshot.
          python3 compose_images.py crop shot.png --box 0 308 3024 1900 --out page.png

  mosaic  One lead frame plus up to 3 supporting frames stacked on the right,
          edge to edge with thin gutters and no text (titles belong in HTML).
          python3 compose_images.py mosaic --lead a.png --side b.png c.png d.png --out work.jpg

  mat     Put figures of mixed aspect ratios on mats of one shared shape so a
          row of them lines up.
          python3 compose_images.py mat fig1.png fig2.png --ratio 4:3 --out-dir assets/figures

Every command prints dimensions, size, and how wide the smallest part will be
on a ~880 px desktop README column and a ~343 px phone column, so you can see
when a detail becomes unreadable *before* you look at it.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:  # pragma: no cover
    sys.exit("compose_images.py needs Pillow: pip install pillow")

DESKTOP, PHONE = 880, 343  # approximate README column widths in CSS px


def ratio(value: str) -> float:
    a, b = value.split(":")
    return float(a) / float(b)


def save(img: Image.Image, out: Path, max_kb: int) -> str:
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() in (".jpg", ".jpeg"):
        quality = 88
        while True:
            img.convert("RGB").save(out, quality=quality, optimize=True, progressive=True)
            if out.stat().st_size <= max_kb * 1024 or quality <= 55:
                break
            quality -= 5
        note = f"jpeg q{quality}"
    else:
        img.save(out, optimize=True)
        note = "png"
    kb = out.stat().st_size / 1024
    warn = "  WARNING: over budget" if kb > max_kb else ""
    return f"{out}: {img.width}×{img.height}, {kb:.0f} KB ({note}){warn}"


def report_widths(label: str, part_w: int, total_w: int):
    d, p = part_w * DESKTOP / total_w, part_w * PHONE / total_w
    flag = "  <- small: keep text/details out of this part" if d < 300 else ""
    print(f"  {label}: ~{d:.0f}px desktop, ~{p:.0f}px phone{flag}")


def cmd_crop(a):
    img = Image.open(a.image)
    x0, y0, x1, y1 = a.box
    if not (0 <= x0 < x1 <= img.width and 0 <= y0 < y1 <= img.height):
        sys.exit(f"box {a.box} outside image {img.width}×{img.height}")
    print(save(img.crop((x0, y0, x1, y1)), Path(a.out), a.max_kb))
    print("  check the result for leftover URLs, tabs, bookmarks, names or notifications before publishing")


def cmd_mosaic(a):
    frame_ratio = ratio(a.ratio)
    width, gap = a.width, a.gap
    side = a.side or []
    if len(side) > 3:
        sys.exit("use at most 3 side frames; more become unreadable slivers")
    if side:
        n = len(side)
        # lead_h == n*side_h + (n-1)*gap, lead_w + gap + side_w == width
        side_w = round((width - gap - (n - 1) * gap * frame_ratio) / (n + 1))
        lead_w = width - gap - side_w
    else:
        side_w, lead_w = 0, width
    lead_h = round(lead_w / frame_ratio)
    canvas = Image.new("RGB", (width, lead_h), a.bg)
    fit = lambda path, size: ImageOps.fit(Image.open(path).convert("RGB"), size, method=Image.Resampling.LANCZOS)
    canvas.paste(fit(a.lead, (lead_w, lead_h)), (0, 0))
    if side:
        side_h = (lead_h - (len(side) - 1) * gap) // len(side)
        for i, path in enumerate(side):
            canvas.paste(fit(path, (side_w, side_h)), (lead_w + gap, i * (side_h + gap)))
    print(save(canvas, Path(a.out), a.max_kb))
    report_widths("lead", lead_w, width)
    if side:
        report_widths("each side frame", side_w, width)


def cmd_mat(a):
    shape = ratio(a.ratio)
    out_dir = Path(a.out_dir)
    for path in a.images:
        img = Image.open(path).convert("RGBA")
        w = min(a.max_width, max(img.width, round(img.height * shape)))
        h = round(w / shape)
        inner_w, inner_h = round(w * (1 - 2 * a.pad)), round(h * (1 - 2 * a.pad))
        img = ImageOps.contain(img, (inner_w, inner_h), method=Image.Resampling.LANCZOS)
        mat = Image.new("RGBA", (w, h), a.bg)
        mat.alpha_composite(img, ((w - img.width) // 2, (h - img.height) // 2))
        if a.border:
            from PIL import ImageDraw
            ImageDraw.Draw(mat).rectangle([0, 0, w - 1, h - 1], outline=a.border, width=max(1, w // 800))
        out = out_dir / (Path(path).stem + a.suffix)
        print(save(mat.convert("RGB"), out, a.max_kb))
        if img.width / img.height >= 2 * shape:
            print("  very wide figure: give it its own full-width row instead of a shared mat")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("crop")
    c.add_argument("image")
    c.add_argument("--box", nargs=4, type=int, required=True, metavar=("X0", "Y0", "X1", "Y1"))
    c.add_argument("--out", required=True)
    c.add_argument("--max-kb", type=int, default=900)
    m = sub.add_parser("mosaic")
    m.add_argument("--lead", required=True)
    m.add_argument("--side", nargs="*")
    m.add_argument("--out", required=True)
    m.add_argument("--width", type=int, default=2400, help="output width; 2x a ~1200px display")
    m.add_argument("--gap", type=int, default=12)
    m.add_argument("--ratio", default="16:9", help="shape of every frame")
    m.add_argument("--bg", default="#0d1117", help="gutter colour")
    m.add_argument("--max-kb", type=int, default=800)
    t = sub.add_parser("mat")
    t.add_argument("images", nargs="+")
    t.add_argument("--out-dir", required=True)
    t.add_argument("--ratio", default="4:3")
    t.add_argument("--pad", type=float, default=0.05, help="margin as a fraction of the mat")
    t.add_argument("--bg", default="#ffffff")
    t.add_argument("--border", default="#d0d7de", help="'' for none")
    t.add_argument("--max-width", type=int, default=1600)
    t.add_argument("--suffix", default="-mat.png")
    t.add_argument("--max-kb", type=int, default=600)
    a = ap.parse_args(argv)
    {"crop": cmd_crop, "mosaic": cmd_mosaic, "mat": cmd_mat}[a.cmd](a)


if __name__ == "__main__":
    main()
