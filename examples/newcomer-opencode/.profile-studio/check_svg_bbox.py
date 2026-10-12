#!/usr/bin/env python3
"""Render each SVG, inlined into a page, and report text that overflows the
canvas or overlaps other text (the svg-craft.md §6 snippet). Visual judgement
stays with the owner; this only proves geometry."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SNIPPET = r"""
(() => { const s = document.querySelector('svg'), vb = s.viewBox.baseVal, out = [];
  const ts = [...s.querySelectorAll('text')].map(t => ({t: t.textContent.slice(0,40), b: t.getBBox()}));
  ts.forEach(({t,b}) => { if (b.x < -0.5 || b.y < 0 || b.x+b.width > vb.width+0.5 || b.y+b.height > vb.height+0.5) out.push('outside: '+t); });
  for (let i=0;i<ts.length;i++) for (let j=i+1;j<ts.length;j++){const a=ts[i].b,c=ts[j].b;
    if (a.x<c.x+c.width && c.x<a.x+a.width && a.y<c.y+c.height && c.y<a.y+a.height) out.push('overlap: '+ts[i].t+' | '+ts[j].t);}
  return out.length ? out : ['no text overflow/overlap']; })()
"""


def check(svg: Path) -> list[str]:
    html = f'<html><body><pre id="out">pending</pre>{svg.read_text()}' \
           f'<script>document.getElementById("out").textContent=' \
           f'JSON.stringify({SNIPPET});</script></body></html>'
    tmp = ROOT / ".profile-studio" / "_bbox.html"
    tmp.write_text(html)
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--dump-dom",
                        f"file://{tmp}"], capture_output=True, text=True, timeout=60)
    m = re.search(r'<pre id="out">(.*?)</pre>', r.stdout, re.S)
    return json.loads(m.group(1)) if m else ["no result"]


def main() -> int:
    files = sorted((ROOT / "assets").glob("*.svg"))
    bad = 0
    for f in files:
        res = check(f)
        print(f"{f.name}: {res}")
        bad += any(not x.startswith("no text") for x in res)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
