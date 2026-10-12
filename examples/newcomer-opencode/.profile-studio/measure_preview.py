#!/usr/bin/env python3
"""Measure the rendered preview (light/dark/phone panels) with real DOM
geometry: image sizes, horizontal overflow, text that overflows its element.
Facts only — the owner judges beauty."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

MEASURE = r"""
function measure() {
  const out = [];
  document.querySelectorAll('iframe').forEach((f, i) => {
    const d = f.contentDocument; if (!d) return;
    const body = d.querySelector('.markdown-body'); if (!body) return;
    const panelW = f.clientWidth - 2;
    const marks = d.querySelectorAll('.markdown-body *');
    let hOverflow = 0, wideEls = [];
    const bodyRect = body.getBoundingClientRect();
    marks.forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.right > bodyRect.right + 1 || r.left < bodyRect.left - 1) {
        hOverflow++; if (wideEls.length < 8) wideEls.push(el.tagName + ' ' + (el.textContent || '').trim().slice(0, 25));
      }
    });
    const tOverflow = [];
    body.querySelectorAll('p,li,h2,h3,td,blockquote,summary,kbd,code').forEach(el => {
      if (el.scrollWidth > el.clientWidth + 2) tOverflow.push(el.tagName + ':' + (el.textContent || '').trim().slice(0, 35));
    });
    const imgs = [...body.querySelectorAll('img')].map(img => {
      const r = img.getBoundingClientRect();
      return { alt: (img.getAttribute('alt') || '').slice(0, 30), w: Math.round(r.width), h: Math.round(r.height) };
    });
    const text = body.innerText.slice(0, 40).replace(/\n/g, ' ');
    out.push({
      panel: i, label: (f.getAttribute('title') || ''), panelW: Math.round(panelW),
      bodyScrollW: body.scrollWidth, bodyClientW: body.clientWidth,
      hOverflow, wideEls: wideEls.slice(0, 5), tOverflow: tOverflow.slice(0, 8), imgs
    });
  });
  return JSON.stringify(out);
}
document.addEventListener('DOMContentLoaded', () => {
  const out = document.createElement('pre'); out.id = 'measure-out';
  document.body.appendChild(out);
  let pending = document.querySelectorAll('iframe').length;
  const done = () => { if (--pending <= 0) out.textContent = measure(); };
  document.querySelectorAll('iframe').forEach(f => { f.addEventListener('load', done); if (f.contentDocument && f.contentDocument.readyState === 'complete') done(); });
});
"""


def main() -> int:
    src = (ROOT / ".profile-studio" / "preview.html").read_text()
    html = src.replace("</body>", f"<script>{MEASURE}</script></body>")
    (ROOT / ".profile-studio" / "_measure.html").write_text(html)
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--dump-dom",
                        "--virtual-time-budget=8000", f"file://{ROOT / '.profile-studio' / '_measure.html'}"],
                       capture_output=True, text=True, timeout=90)
    m = re.search(r'<pre id="measure-out">(.*?)</pre>', r.stdout, re.S)
    if not m:
        print("no measurement result", file=sys.stderr)
        print(r.stdout[-2000:], file=sys.stderr)
        return 1
    data = json.loads(m.group(1))
    print(json.dumps(data, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())