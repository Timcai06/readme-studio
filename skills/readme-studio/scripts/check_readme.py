#!/usr/bin/env python3
"""Check a GitHub README (profile or project) and its local assets before delivery.

Usage:
    python3 check_readme.py README.md                 # static checks, offline
    python3 check_readme.py README.md --render        # + GitHub's real sanitizer (network)
    python3 check_readme.py README.md --online        # + fetch every external URL
    python3 check_readme.py README.md --baseline old/README.md   # Improve mode: what disappeared?
    python3 check_readme.py README.md --portable      # also published to npm/PyPI/…: GitHub-only constructs
    python3 check_readme.py README.md --json report.json

Severities: error (broken on GitHub or unsafe to publish), warning (likely a
mistake or has no effect), info (inventory a human should glance at).
Exit code 1 when any error is found.

--render posts the README to GitHub's Markdown API (the same sanitizer that
renders profile pages) and compares tags before/after. It uses GITHUB_TOKEN /
GH_TOKEN, or `gh auth token`, or goes anonymous (60 requests/hour). It cannot
show CSS effects (table borders, link colour, theme switching); see the QA
reference for what still needs a real page view.

Standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

sys.dont_write_bytecode = True  # keep the skill folder clean
sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_kit import lint_svg  # noqa: E402

# Verified against POST /markdown (mode=gfm) on 2026-10-12; see references/github-rendering.md
ESCAPED_AS_TEXT = {"script", "style", "iframe", "noscript", "plaintext", "textarea", "title", "xmp", "noembed", "noframes"}
REMOVED_WITH_CONTENT = {"svg", "video", "audio", "input", "form", "object", "embed", "canvas", "link", "meta", "math"}
UNWRAPPED = {"font", "center", "u", "small", "big", "abbr", "cite", "dfn", "figure", "figcaption", "button",
             "section", "article", "aside", "nav", "header", "footer", "main", "label", "select", "option"}
STRIPPED_ATTRS = {"style", "class", "bgcolor", "border", "color", "face", "onclick", "onload", "onerror",
                  "target", "loading", "background"}
CLICHE_SERVICES = {
    "github-readme-stats": "GitHub stats card",
    "github-readme-streak-stats": "streak counter",
    "streak-stats.demolab.com": "streak counter",
    "github-profile-trophy": "trophy wall",
    "github-profile-summary-cards": "summary cards",
    "komarev.com/ghpvc": "visitor counter",
    "profile-counter": "visitor counter",
    "snk": "contribution snake",
    "github-contribution-grid-snake": "contribution snake",
    "readme-typing-svg": "third-party typing banner (a self-generated svg_kit.typewriter SVG avoids the service dependency)",
    "activity-graph": "activity graph",
}
DYNAMIC_HOSTS = ("shields.io", "skillicons.dev", "readme-typing-svg", "vercel.app", "herokuapp.com",
                 "komarev.com", "demolab.com", "github-readme", "wakatime", "spotify", "metrics.lecoq.io")
SECRET_PATTERNS = [
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"), "GitHub token"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{40,}"), "GitHub fine-grained token"),
    (re.compile(r"sk-[A-Za-z0-9_\-]{20,}"), "API secret key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
]
LOCAL_LEAKS = re.compile(r"(file://|/Users/[^/\s\"')]+|/home/[^/\s\"')]+|[A-Za-z]:\\\\Users|"
                         r"https?://(localhost|127\.0\.0\.1|0\.0\.0\.0|192\.168\.)[^\s\"')]*)")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
MD_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
MD_REFDEF = re.compile(r"^\s{0,3}\[([^\]^][^\]]*)\]:\s*<?(\S+?)>?(\s|$)", re.M)


class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags: Counter = Counter()
        self.events: list[tuple] = []  # (kind, tag, attrs, line)
        self.stack: list[str] = []
        self.max_details_depth = 0
        self.svg_depth = 0  # children of inline <svg> are not counted separately

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        if self.svg_depth:
            if tag == "svg":
                self.svg_depth += 1
            return
        if tag == "svg":
            self.svg_depth = 1
        self.tags[tag] += 1
        self.events.append(("start", tag, dict(attrs), line))
        if tag not in ("img", "br", "hr", "source", "input", "meta", "link", "wbr"):
            self.stack.append(tag)
        if tag == "details":
            self.max_details_depth = max(self.max_details_depth, self.stack.count("details"))

    def handle_startendtag(self, tag, attrs):
        if self.svg_depth:
            return
        self.tags[tag] += 1
        self.events.append(("start", tag, dict(attrs), self.getpos()[0]))

    def handle_endtag(self, tag):
        if self.svg_depth:
            if tag == "svg":
                self.svg_depth -= 1
                if self.svg_depth == 0:
                    self.events.append(("end", tag, {}, self.getpos()[0]))
            return
        self.events.append(("end", tag, {}, self.getpos()[0]))
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == tag:
                del self.stack[i:]
                break


class Report:
    def __init__(self):
        self.items: list[dict] = []

    def add(self, severity, check, message, line=None):
        self.items.append({"severity": severity, "check": check, "message": message, "line": line})

    def count(self, severity):
        return sum(1 for i in self.items if i["severity"] == severity)


def strip_code(text: str) -> str:
    """Blank out fenced and inline code so examples inside them are not flagged."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", blank, text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]+`", blank, text)


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def exists_case_sensitive(base: Path, rel: str) -> tuple[bool, str | None]:
    """GitHub paths are case-sensitive; macOS/Windows disks usually are not."""
    target = (base / rel)
    if not target.exists():
        return False, None
    parts = Path(os.path.normpath(rel)).parts
    cur = base
    for part in parts:
        if part in ("", "."):
            continue
        if part == "..":
            cur = cur.parent
            continue
        names = {p.name for p in cur.iterdir()} if cur.is_dir() else set()
        if part not in names:
            match = next((n for n in names if n.lower() == part.lower()), None)
            return True, f"case differs on disk: '{part}' vs '{match}' (breaks on GitHub)"
        cur = cur / part
    return True, None


def repo_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / ".git").exists():
            return p
    return start


def github_slug(heading: str) -> str:
    """GitHub's heading anchor: lowercase, drop punctuation except - and _, spaces to hyphens."""
    text = re.sub(r"<[^>]+>", "", heading)
    text = re.sub(r"[`*_~]|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def anchors_in(text: str, col: "Collector") -> set[str]:
    seen: dict[str, int] = {}
    anchors = set()
    headings = re.findall(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", text, re.M)
    headings += re.findall(r"<h[1-6][^>]*>(.*?)</h[1-6]>", text, re.S | re.I)
    for h in headings:
        slug = github_slug(h)
        n = seen.get(slug, 0)
        anchors.add(slug if n == 0 else f"{slug}-{n}")
        seen[slug] = n + 1
    for kind, tag, attrs, _ in col.events:
        if kind == "start":
            for key in ("id", "name"):
                if attrs.get(key):
                    anchors.add(attrs[key].lower())
    return anchors


def collect_refs(text: str, collector: Collector):
    """Yield (kind, url, alt_or_text, line) for every image and link."""
    refs = []
    for kind, tag, attrs, line in collector.events:
        if kind != "start":
            continue
        if tag == "img":
            refs.append(("image", attrs.get("src") or "", attrs.get("alt"), line))
        elif tag == "source":
            for part in (attrs.get("srcset") or "").split(","):
                url = part.strip().split(" ")[0]
                if url:
                    refs.append(("image", url, "<source>", line))
        elif tag == "a" and attrs.get("href"):
            refs.append(("link", attrs["href"], None, line))
    for m in MD_IMAGE.finditer(text):
        refs.append(("image", m.group(2), m.group(1), line_of(text, m.start())))
    for m in MD_LINK.finditer(text):
        refs.append(("link", m.group(2), m.group(1), line_of(text, m.start())))
    for m in MD_REFDEF.finditer(text):
        refs.append(("link", m.group(2), m.group(1), line_of(text, m.start())))
    return refs


def static_checks(readme: Path, report: Report, max_asset_kb: int):
    raw = readme.read_text(encoding="utf-8")
    text = strip_code(raw)
    base = readme.parent
    col = Collector()
    col.feed(text)
    col.close()

    # --- tags and attributes GitHub will not keep
    for tag in sorted(col.tags):
        n = col.tags[tag]
        if tag in ESCAPED_AS_TEXT:
            report.add("error", "sanitizer", f"<{tag}> ×{n} is shown as literal text on GitHub")
        elif tag in REMOVED_WITH_CONTENT:
            report.add("error", "sanitizer", f"<{tag}> ×{n} is removed by GitHub (use an image instead)")
        elif tag in UNWRAPPED:
            report.add("warning", "sanitizer", f"<{tag}> ×{n} is dropped (its text stays, its effect does not)")
    attr_hits = Counter()
    for kind, tag, attrs, line in col.events:
        if kind == "start":
            for a in attrs:
                if a in STRIPPED_ATTRS or a.startswith("on") or a.startswith("data-"):
                    attr_hits[(tag, a)] += 1
    for (tag, a), n in sorted(attr_hits.items()):
        report.add("warning", "sanitizer", f'{a}="" on <{tag}> ×{n} is stripped by GitHub (no effect)')

    # --- structure
    opens = sum(1 for e in col.events if e[0] == "start" and e[1] == "details")
    closes = sum(1 for e in col.events if e[0] == "end" and e[1] == "details")
    if opens != closes:
        report.add("error", "structure", f"<details> opened {opens}× but closed {closes}×")
    summaries = sum(1 for e in col.events if e[0] == "start" and e[1] == "summary")
    if summaries < opens:
        report.add("warning", "structure", f"{opens - summaries} <details> without <summary> show a bare 'Details' label")
    if col.max_details_depth > 1:
        report.add("info", "structure", f"nested folds (depth {col.max_details_depth}); keep identity content out of folds")
    for i, (kind, tag, attrs, line) in enumerate(col.events):
        if kind == "start" and tag == "picture":
            j, has_img, sources = i + 1, False, []
            while j < len(col.events) and not (col.events[j][0] == "end" and col.events[j][1] == "picture"):
                if col.events[j][1] == "img" and col.events[j][0] == "start":
                    has_img = True
                if col.events[j][1] == "source":
                    sources.append(col.events[j][2].get("media", ""))
                j += 1
            if not has_img:
                report.add("error", "theme", "<picture> without a fallback <img> renders nothing", line)
            schemes = " ".join(sources)
            if sources and not ("dark" in schemes and "light" in schemes):
                report.add("warning", "theme", "<picture> sources do not cover both light and dark", line)
    if col.tags.get("table") and col.tags.get("details"):
        # Known breakage in practice: folds inside table cells collapse oddly.
        depth, in_table = 0, 0
        for kind, tag, _, line in col.events:
            if tag == "table":
                in_table += 1 if kind == "start" else -1
            if tag == "details" and kind == "start" and in_table > 0:
                report.add("warning", "structure", "<details> inside a table cell: renders inconsistently; move it out", line)

    # Markdown syntax directly inside an HTML block without a blank line stays literal.
    lines = text.split("\n")
    md_syntax = re.compile(r"(\*\*[^*]+\*\*|(?<!!)\[[^\]]+\]\([^)]+\)|^\s*#{1,6}\s|^\s*[-*]\s+\S)")
    in_html_block = False
    for n, ln in enumerate(lines, 1):
        stripped = ln.strip()
        if re.match(r"^</?(table|tr|td|th|div|p|details|summary|picture|h[1-6]|blockquote|ul|ol|li|dl)\b", stripped, re.I):
            in_html_block = True
        if stripped == "":
            in_html_block = False
            continue
        if in_html_block and md_syntax.search(re.sub(r"<[^>]*>", " ", ln)):
            report.add("warning", "markdown", "Markdown inside an HTML block needs a blank line before it, "
                       "or it renders literally", n)

    # --- images and links
    refs = collect_refs(text, col)
    images = [r for r in refs if r[0] == "image"]
    seen_local = set()
    reported = set()
    for kind, url, label, line in refs:
        if url in reported:
            continue
        if not url or url.startswith("#") or url.startswith("mailto:"):
            continue
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme in ("http", "https", "data"):
            continue
        rel = urllib.parse.unquote(parsed.path)
        root = base
        if rel.startswith("/"):  # GitHub resolves "/x" from the repository root
            root = repo_root(base)
            rel = rel.lstrip("/")
        if not rel:
            continue
        ok, case_issue = exists_case_sensitive(root, rel)
        if not ok:
            reported.add(url)
            report.add("error", "paths", f"missing local file: {url}", line)
        elif case_issue:
            report.add("error", "paths", f"{url}: {case_issue}", line)
        else:
            seen_local.add((root / rel).resolve())
    anchors = anchors_in(text, col)
    for kind, url, label, line in refs:
        if kind == "link" and url.startswith("#") and len(url) > 1:
            target = urllib.parse.unquote(url[1:]).lower()
            if target not in anchors:
                report.add("warning", "anchors", f"in-page link {url} matches no heading or id", line)
    for kind, url, label, line in images:
        if label is None or (label != "<source>" and label.strip() == ""):
            report.add("warning", "a11y", f"image without alt text: {url[:70]}", line)

    total_kb = 0.0
    for path in sorted(seen_local):
        if path.is_file():
            kb = path.stat().st_size / 1024
            total_kb += kb
            if kb > max_asset_kb:
                report.add("warning", "size", f"{os.path.relpath(path, base.resolve())}: {kb:.0f} KB (budget {max_asset_kb} KB)")
            if path.suffix.lower() == ".svg":
                for sev, msg in lint_svg(path, max_kb=max_asset_kb):
                    report.add(sev, "svg", f"{os.path.relpath(path, base.resolve())}: {msg}")
    if total_kb > 6000:
        report.add("warning", "size", f"local assets total {total_kb/1024:.1f} MB; first paint will be slow on mobile")

    # --- content safety
    for pattern, label in SECRET_PATTERNS:
        for m in pattern.finditer(raw):
            report.add("error", "privacy", f"possible {label} in README", line_of(raw, m.start()))
    for m in LOCAL_LEAKS.finditer(raw):
        report.add("error", "privacy", f"local path or local URL: {m.group(0)[:60]}", line_of(raw, m.start()))
    emails = sorted(set(EMAIL.findall(raw)) - {"noreply@github.com"})
    emails = [e for e in emails if not e.endswith((".png", ".svg", ".jpg"))]
    if emails:
        report.add("info", "privacy", "public email address(es): " + ", ".join(emails) + " — confirm the owner wants them shown")

    # --- dependency and cliché inventory
    hosts = Counter()
    for kind, url, *_ in refs:
        host = urllib.parse.urlparse(url).netloc
        if host:
            hosts[host] += 1
    dynamic = sorted(h for h in hosts if any(d in h for d in DYNAMIC_HOSTS))
    if dynamic:
        report.add("info", "dependencies", "third-party image services (can rate-limit, change or disappear): "
                   + ", ".join(f"{h}×{hosts[h]}" for h in dynamic))
    lower = raw.lower()
    found = sorted({label for key, label in CLICHE_SERVICES.items() if key in lower})
    if found:
        report.add("info", "defaults", "template defaults present: " + ", ".join(found)
                   + " — keep only if the owner asked for them or they carry real information")

    text_links = 0
    for i, (kind, tag, attrs, line) in enumerate(col.events):
        if kind == "start" and tag == "a":
            nxt = col.events[i + 1] if i + 1 < len(col.events) else None
            if not (nxt and nxt[0] == "start" and nxt[1] in ("img", "kbd", "picture")):
                text_links += 1
    text_links += len(MD_LINK.findall(text))
    summary = {
        "lines": raw.count("\n") + 1,
        "words": len(re.findall(r"[A-Za-z0-9']+|[一-鿿]", re.sub(r"<[^>]+>|\([^)]*\)", " ", text))),
        "images": len([i for i in images if i[2] != "<source>"]),
        "folds": opens,
        "text_links": text_links,
        "local_assets_kb": round(total_kb),
        "headings": len(re.findall(r"^\s{0,3}#{1,6}\s", text, re.M)) + sum(col.tags.get(f"h{i}", 0) for i in range(1, 7)),
    }
    return summary


def api_token():
    for name in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(name):
            return os.environ[name]
    if shutil.which("gh"):
        try:
            out = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10)
            if out.returncode == 0:
                return out.stdout.strip() or None
        except (OSError, subprocess.TimeoutExpired):
            return None
    return None


def github_render(markdown: str, context: str | None) -> str:
    payload = {"text": markdown, "mode": "gfm"}
    if context:
        payload["context"] = context
    req = urllib.request.Request("https://api.github.com/markdown", data=json.dumps(payload).encode(),
                                 headers={"Accept": "text/html", "Content-Type": "application/json",
                                          "User-Agent": "readme-studio-check",
                                          "X-GitHub-Api-Version": "2022-11-28"})
    token = api_token()
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def render_checks(readme: Path, report: Report, context: str | None, save: Path | None):
    source = strip_code(readme.read_text(encoding="utf-8"))
    try:
        html = github_render(readme.read_text(encoding="utf-8"), context)
    except (urllib.error.URLError, TimeoutError) as err:
        report.add("warning", "render", f"GitHub render API unavailable ({err}); sanitizer behaviour NOT verified")
        return None
    if save:
        save.write_text(html, encoding="utf-8")
    before, after = Collector(), Collector()
    before.feed(source)
    after.feed(html)
    ignore = {"p", "a", "div", "span", "svg", "path", "section", "pre", "code", "markdown-accessiblity-table",
              "themed-picture", "tbody", "thead", "ul", "ol", "li", "strong", "em", "h1", "h2", "h3", "h4",
              "h5", "h6", "blockquote", "table", "tr", "td", "th", "img", "input", "circle", "math-renderer", "sup"}
    lost = []
    for tag, n in before.tags.items():
        if tag in ignore:
            continue
        if after.tags.get(tag, 0) < n:
            lost.append(f"<{tag}> {n}→{after.tags.get(tag, 0)}")
    if lost:
        report.add("error", "render", "GitHub removed: " + ", ".join(sorted(lost)))
    prose = re.sub(r"<pre[^>]*>.*?</pre>|<code[^>]*>.*?</code>", " ", html, flags=re.S)  # code samples may show tags
    escaped = sorted(set(re.findall(r"&lt;(/?[a-zA-Z][a-zA-Z0-9-]*)", prose)) - {"/"})
    if escaped:
        report.add("error", "render", "shown as literal text on GitHub: " + ", ".join(f"<{t}>" for t in escaped))
    if before.tags.get("img", 0) > after.tags.get("img", 0):
        report.add("error", "render", f"images: {before.tags['img']} in source, {after.tags.get('img', 0)} after rendering")
    report.add("info", "render", f"rendered by GitHub's Markdown API: {sum(after.tags.values())} elements, "
               f"{after.tags.get('img', 0)} images, {after.tags.get('details', 0)} folds kept")
    return html


def online_checks(readme: Path, report: Report):
    text = strip_code(readme.read_text(encoding="utf-8"))
    col = Collector()
    col.feed(text)
    urls = sorted({u for k, u, *_ in collect_refs(text, col) if u.startswith(("http://", "https://"))})
    for url in urls:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "Mozilla/5.0 readme-studio-check"})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                status = resp.status
                ctype = resp.headers.get("Content-Type", "")
        except urllib.error.HTTPError as err:
            status, ctype = err.code, ""
        except Exception as err:  # noqa: BLE001 - report any network failure
            report.add("warning", "links", f"unreachable: {url[:90]} ({type(err).__name__})")
            continue
        if status == 999 or (status in (403, 429) and any(h in url for h in ("linkedin.com", "x.com", "twitter.com", "instagram.com"))):
            report.add("info", "links", f"{status} from {urllib.parse.urlparse(url).netloc} (blocks bots); open it by hand")
        elif status >= 400:
            report.add("error", "links", f"HTTP {status}: {url[:100]}")
        elif "github.com" in url and status == 404:
            report.add("error", "links", f"404 (private or renamed repository?): {url}")
    report.add("info", "links", f"checked {len(urls)} external URLs")


def portable_checks(readme: Path, report: Report):
    """For READMEs also published to package registries (npm, PyPI, crates.io, marketplaces)."""
    text = strip_code(readme.read_text(encoding="utf-8"))
    col = Collector()
    col.feed(text)
    rel_images = sorted({u for k, u, *_ in collect_refs(text, col)
                         if k == "image" and u and not re.match(r"^(https?:|data:)", u)})
    for u in rel_images:
        report.add("warning", "portable", f"relative image {u} may break on package registries; "
                   "use an absolute URL pinned to a tag/commit")
    if col.tags.get("picture"):
        report.add("warning", "portable", "<picture> theme switching is GitHub-specific; registries show "
                   "only the fallback <img> (make sure it works on both light and dark pages)")
    if col.tags.get("details"):
        report.add("info", "portable", "<details> folds may render expanded or unstyled on some registries")
    report.add("info", "portable", "registry rendering itself is not verified by this script")


def baseline_checks(readme: Path, baseline: Path, report: Report):
    """Improve mode: list every image/link/heading of the original that is gone."""
    def inventory(path):
        text = strip_code(path.read_text(encoding="utf-8"))
        col = Collector()
        col.feed(text)
        refs = {(k, u) for k, u, *_ in collect_refs(text, col) if u}
        heads = {h.strip().lower() for h in re.findall(r"^\s{0,3}#{1,6}\s+(.+)$", text, re.M)}
        return refs, heads
    old_refs, old_heads = inventory(baseline)
    new_refs, new_heads = inventory(readme)
    for kind, url in sorted(old_refs - new_refs):
        report.add("info", "baseline", f"{kind} from the original is no longer referenced: {url[:100]} "
                   "— confirm this removal was agreed")
    for h in sorted(old_heads - new_heads):
        report.add("info", "baseline", f"original heading no longer present: '{h[:60]}' — its #{github_slug(h)} "
                   "anchor may be linked from elsewhere; keep it or add <a name=\"...\"></a>")
    kept = len(old_refs & new_refs)
    report.add("info", "baseline", f"{kept}/{len(old_refs)} original links/images kept")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Check a GitHub README (profile or project) before delivery.")
    ap.add_argument("readme", type=Path)
    ap.add_argument("--render", action="store_true", help="verify with GitHub's Markdown API (network)")
    ap.add_argument("--context", help="owner/repo for rendering context, e.g. octocat/octocat")
    ap.add_argument("--save-html", type=Path, help="with --render: save GitHub's HTML here")
    ap.add_argument("--online", action="store_true", help="request every external URL (network)")
    ap.add_argument("--baseline", type=Path, help="original README, to list removed links/images (Improve mode)")
    ap.add_argument("--portable", action="store_true", help="also published to a package registry: flag GitHub-only constructs")
    ap.add_argument("--max-asset-kb", type=int, default=1024)
    ap.add_argument("--json", type=Path, help="also write the report as JSON")
    args = ap.parse_args(argv)
    if not args.readme.is_file():
        print(f"error: {args.readme} not found", file=sys.stderr)
        return 2

    report = Report()
    summary = static_checks(args.readme, report, args.max_asset_kb)
    if args.render:
        render_checks(args.readme, report, args.context, args.save_html)
    else:
        report.add("info", "render", "GitHub sanitizer not checked (run with --render when online)")
    if args.online:
        online_checks(args.readme, report)
    if args.baseline:
        baseline_checks(args.readme, args.baseline, report)
    if args.portable:
        portable_checks(args.readme, report)

    order = {"error": 0, "warning": 1, "info": 2}
    print(f"{args.readme}: " + ", ".join(f"{k} {v}" for k, v in summary.items()))
    for item in sorted(report.items, key=lambda i: order[i["severity"]]):
        where = f" (line {item['line']})" if item["line"] else ""
        print(f"  {item['severity']:<7} [{item['check']}] {item['message']}{where}")
    print(f"result: {report.count('error')} errors, {report.count('warning')} warnings, {report.count('info')} info")
    if args.json:
        args.json.write_text(json.dumps({"summary": summary, "items": report.items}, indent=2, ensure_ascii=False))
    return 1 if report.count("error") else 0


if __name__ == "__main__":
    sys.exit(main())
