#!/usr/bin/env python3
"""Build a local preview page of a profile README: light, dark and phone width.

Usage:
    python3 render_preview.py README.md [--out .readme-studio/preview.html] [--context user/user]

The HTML comes from GitHub's own Markdown API when online (so the sanitizer
is real), styled with the public github-markdown-css stylesheet. Offline, the
page shows the raw source with a banner saying nothing was rendered.

This is an approximation, not a github.com screenshot: GitHub's page chrome,
exact column width, fonts and the camo image proxy differ. <picture> theme
switching is resolved statically per panel (light panel = light source, dark
panel = dark source), and `#gh-dark-mode-only` / `#gh-light-mode-only` images
are hidden in the other panel, mirroring what github.com does.

Open the file in a browser. Standard library only.
"""
from __future__ import annotations

import argparse
import html as htmllib
import os
import re
import sys
import urllib.error
from pathlib import Path

sys.dont_write_bytecode = True  # keep the skill folder clean
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_readme import github_render  # noqa: E402


def offline_render(md: str) -> str:
    """Rough Markdown → HTML for previews without network. HTML blocks pass
    through; headings, paragraphs, lists, fences, links, images, emphasis and
    code are converted. NOT GitHub's sanitizer: style/class/script survive here."""
    out, para, lst, fence = [], [], None, None

    def inline(t):
        t = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)[^)]*\)", r'<img src="\2" alt="\1">', t)
        t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)[^)]*\)", r'<a href="\2">\1</a>', t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        return re.sub(r"(?<![*\w])\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", t)

    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []
        if lst:
            out.append(f"<{lst[0]}>" + "".join(f"<li>{inline(i)}</li>" for i in lst[1]) + f"</{lst[0]}>")
            lst = None
    for line in md.split("\n"):
        if fence is not None:
            if line.strip().startswith(fence):
                out.append("</code></pre>")
                fence = None
            else:
                out.append(htmllib.escape(line) + "\n")
            continue
        m = re.match(r"^\s*(```|~~~)", line)
        if m:
            flush()
            fence = m.group(1)
            out.append("<pre><code>")
            continue
        if not line.strip():
            flush()
            continue
        if re.match(r"^\s*<", line):
            flush()
            out.append(line)
            continue
        h = re.match(r"^(#{1,6})\s+(.*)", line)
        if h:
            flush()
            out.append(f"<h{len(h.group(1))}>{inline(h.group(2))}</h{len(h.group(1))}>")
            continue
        if re.match(r"^\s*([-*_])\s*\1\s*\1[\s\1]*$", line):
            flush()
            out.append("<hr>")
            continue
        li = re.match(r"^\s*(?:([-*+])|\d+[.)])\s+(.*)", line)
        if li:
            kind = "ul" if li.group(1) else "ol"
            if para:
                flush()
            if not lst or lst[0] != kind:
                flush()
                lst = (kind, [])
            lst[1].append(li.group(2))
            continue
        if line.startswith(">"):
            flush()
            out.append("<blockquote><p>" + inline(line.lstrip("> ")) + "</p></blockquote>")
            continue
        para.append(line.strip())
    flush()
    return "\n".join(out)

CSS = "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown-{theme}.min.css"


def fix_urls(rendered: str, readme_dir: Path, out_dir: Path) -> str:
    # camo-proxied images: use the original URL for local preview
    rendered = re.sub(r'src="https://camo\.githubusercontent\.com/[^"]+"([^>]*?)data-canonical-src="([^"]+)"',
                      r'src="\2"\1', rendered)
    rel = os.path.relpath(readme_dir, out_dir)

    def local(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"^(https?:|data:|#|mailto:)", url):
            return m.group(0)
        return f'{attr}="{Path(rel, url).as_posix()}"'
    rendered = re.sub(r'(src|srcset|href)="([^"]+)"', local, rendered)
    return rendered


def resolve_theme(rendered: str, theme: str) -> str:
    def pick(m):
        block = m.group(0)
        source = re.search(rf'<source[^>]*media="\(prefers-color-scheme:\s*{theme}\)"[^>]*srcset="([^"]+)"', block)
        img = re.search(r"<img[^>]*>", block)
        if not img:
            return block
        tag = img.group(0)
        if source:
            tag = re.sub(r'src="[^"]*"', f'src="{source.group(1)}"', tag)
        return tag
    rendered = re.sub(r"<picture>.*?</picture>", pick, rendered, flags=re.S)
    other = "light" if theme == "dark" else "dark"
    rendered = re.sub(rf'<img([^>]*?)src="([^"]*#gh-{other}-mode-only)"', r'<img\1 hidden src="\2"', rendered)
    return rendered


def page(light: str, dark: str, banner: str, title: str) -> str:
    def panel(theme, body, width, label):
        doc = (f'<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="{CSS.format(theme=theme)}">'
               f'<style>body{{margin:0;background:{"#0d1117" if theme=="dark" else "#ffffff"}}}'
               f'.markdown-body{{box-sizing:border-box;max-width:{width}px;padding:24px 16px}}</style>'
               f'<article class="markdown-body">{body}</article>')
        return (f'<figure><figcaption>{label}</figcaption><iframe title="{label}" style="width:{width + 2}px" '
                f'srcdoc="{htmllib.escape(doc, quote=True)}"></iframe></figure>')
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{htmllib.escape(title)}</title>
<style>
:root{{--bg:#f6f8fa;--ink:#1f2328;--muted:#59636e;--warn:#fff8c5}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#010409;--ink:#e6edf3;--muted:#9198a1;--warn:#3b2e00}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,Segoe UI,sans-serif}}
.note{{background:var(--warn);padding:8px 12px;border-radius:6px;margin-bottom:16px}}
.row{{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}}
figure{{margin:0}} figcaption{{color:var(--muted);margin-bottom:6px}}
iframe{{border:1px solid #d1d9e0;border-radius:6px;height:85vh;max-width:calc(100vw - 32px);background:#fff}}
</style></head><body>
<div class="note">{banner}</div>
<div class="row">
{panel("light", light, 880, "Light · ~880px desktop column")}
{panel("dark", dark, 880, "Dark · ~880px desktop column")}
{panel("light", light, 375, "Phone · 375px")}
</div></body></html>"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("readme", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--context", help="owner/repo, e.g. octocat/octocat")
    a = ap.parse_args(argv)
    readme = a.readme.resolve()
    out = (a.out or readme.parent / ".readme-studio" / "preview.html").resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    source = readme.read_text(encoding="utf-8")
    try:
        rendered = github_render(source, a.context)
        banner = ("Rendered by GitHub's Markdown API (real sanitizer) + github-markdown-css. "
                  "Approximation of github.com: page chrome, fonts and column width differ.")
    except (urllib.error.URLError, TimeoutError) as err:
        rendered = offline_render(source)
        banner = (f"OFFLINE ({err}): rough local Markdown conversion. GitHub's sanitizer was NOT applied — "
                  "style/class/script would still show here but are stripped on GitHub. Run check_readme.py.")
    rendered = fix_urls(rendered, readme.parent, out.parent)
    html = page(resolve_theme(rendered, "light"), resolve_theme(rendered, "dark"), banner,
                f"Preview · {readme.parent.name}")
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out}")
    print(banner)
    return 0


if __name__ == "__main__":
    sys.exit(main())
