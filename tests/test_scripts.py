"""Unit tests for the bundled scripts. Offline; Pillow tests skip if Pillow is missing.

    python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "readme-studio" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_readme  # noqa: E402
import github_snapshot  # noqa: E402
import svg_kit  # noqa: E402

try:
    import PIL  # noqa: F401
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False


def run_check(readme: Path, *extra) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = check_readme.main([str(readme), *extra])
    return code, buf.getvalue()


class CheckProfileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        (self.dir / "assets").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text: str) -> Path:
        path = self.dir / "README.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_clean_readme_passes(self):
        svg = svg_kit.Svg(400, 100, title="Hero")
        svg.text(20, 60, "Ada Park", size=40)
        svg.write(self.dir / "assets" / "hero.svg")
        code, out = run_check(self.write(
            '<p align="center"><img src="./assets/hero.svg" width="100%" alt="Ada Park"></p>\n\n'
            "Builds routing engines.\n\n"
            '<a href="https://github.com/ada/tiles"><kbd>Repository ↗</kbd></a>\n'))
        self.assertEqual(code, 0, out)
        self.assertIn("0 errors", out)

    def test_forbidden_tags_and_attributes(self):
        code, out = run_check(self.write(
            '<p style="color:red">x</p>\n<script>alert(1)</script>\n<svg><rect/></svg>\n<center>c</center>\n'))
        self.assertEqual(code, 1)
        self.assertIn("<script> ×1 is shown as literal text", out)
        self.assertIn("<svg> ×1 is removed", out)
        self.assertIn("<center> ×1 is dropped", out)
        self.assertIn('style="" on <p>', out)

    def test_code_blocks_are_ignored(self):
        code, out = run_check(self.write("```html\n<script>ok in a code sample</script>\n```\n"))
        self.assertEqual(code, 0, out)

    def test_missing_and_case_mismatched_paths(self):
        (self.dir / "assets" / "Logo.png").write_bytes(b"\x89PNG")
        code, out = run_check(self.write('<img src="./assets/logo.png" alt="l">\n<img src="./assets/none.png" alt="n">\n'))
        self.assertEqual(code, 1)
        self.assertIn("missing local file: ./assets/none.png", out)
        if (self.dir / "assets" / "logo.png").exists():  # case-insensitive disk
            self.assertIn("case differs on disk", out)

    def test_details_balance_and_table_fold(self):
        code, out = run_check(self.write("<table><tr><td><details><summary>s</summary>x</details></td></tr></table>\n<details>\n"))
        self.assertIn("<details> opened 2× but closed 1×", out)
        self.assertIn("inside a table cell", out)

    def test_markdown_inside_html_block(self):
        code, out = run_check(self.write("<table><tr><td>**bold**</td></tr></table>\n"))
        self.assertIn("Markdown inside an HTML block", out)

    def test_picture_needs_fallback_img(self):
        code, out = run_check(self.write(
            '<picture><source media="(prefers-color-scheme: dark)" srcset="https://x.test/d.svg"></picture>\n'))
        self.assertIn("without a fallback <img>", out)
        self.assertIn("do not cover both light and dark", out)

    def test_privacy_and_cliches(self):
        code, out = run_check(self.write(
            "token ghp_" + "a" * 36 + "\n![s](https://github-readme-stats.vercel.app/api?username=x)\n"
            "see /Users/someone/Desktop/x.png and me@example.org\n"))
        self.assertEqual(code, 1)
        self.assertIn("possible GitHub token", out)
        self.assertIn("local path", out)
        self.assertIn("GitHub stats card", out)
        self.assertIn("me@example.org", out)

    def test_in_page_anchor_links(self):
        code, out = run_check(self.write("## Quick start\n\n## API\n\n[go](#quick-start) [bad](#install) "
                                         '<a href="#api">api</a> <a name="legacy"></a> [old](#legacy)\n'))
        self.assertIn("#install matches no heading", out)
        self.assertNotIn("#quick-start matches", out)
        self.assertNotIn("#legacy matches", out)

    def test_root_relative_paths_resolve_from_repo_root(self):
        (self.dir / ".git").mkdir()
        (self.dir / "docs").mkdir()
        (self.dir / "assets" / "logo.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"/>')
        readme = self.dir / "docs" / "README.md"
        readme.write_text('<img src="/assets/logo.svg" alt="logo"><img src="/assets/nope.svg" alt="x">\n')
        code, out = run_check(readme)
        self.assertIn("missing local file: /assets/nope.svg", out)
        self.assertNotIn("missing local file: /assets/logo.svg", out)

    def test_portable_flags_registry_breakers(self):
        (self.dir / "assets" / "a.png").write_bytes(b"\x89PNG")
        code, out = run_check(self.write('<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/a.png">'
                                         '<img src="./assets/a.png" alt="a"></picture>\n'), "--portable")
        self.assertIn("relative image ./assets/a.png may break", out)
        self.assertIn("<picture> theme switching is GitHub-specific", out)

    def test_baseline_reports_removed_items(self):
        old = self.dir / "old.md"
        old.write_text('<img src="https://x.test/cat.gif" alt="cat">\n## Reading list\n', encoding="utf-8")
        code, out = run_check(self.write("## Something else\n"), "--baseline", str(old))
        self.assertIn("cat.gif", out)
        self.assertIn("reading list", out)
        self.assertIn("#reading-list", out)


class RenderComparisonTests(unittest.TestCase):
    def test_escaped_tags_in_code_are_not_errors(self):
        html = '<pre><code>&lt;you&gt;</code></pre><p>&lt;script&gt;x&lt;/script&gt;</p>'
        original = check_readme.github_render
        check_readme.github_render = lambda md, ctx: html
        try:
            with tempfile.TemporaryDirectory() as tmp:
                readme = Path(tmp) / "README.md"
                readme.write_text("```\n<you>\n```\n<script>x</script>\n", encoding="utf-8")
                report = check_readme.Report()
                check_readme.render_checks(readme, report, None, None)
            msgs = " ".join(i["message"] for i in report.items)
            self.assertIn("<script>", msgs)
            self.assertNotIn("<you>", msgs)
        finally:
            check_readme.github_render = original


class SvgKitTests(unittest.TestCase):
    def test_measure_monospace_and_cjk(self):
        self.assertAlmostEqual(svg_kit.measure("abcd", 10, "mono"), 24.0)
        self.assertAlmostEqual(svg_kit.measure("中文", 10), 20.0)

    def test_wrap_respects_width(self):
        lines = svg_kit.wrap("one two three four five six seven", 16, 120)
        self.assertGreater(len(lines), 1)
        for line in lines:
            self.assertLessEqual(svg_kit.measure(line, 16), 120 + 1e-6)

    def test_effective_px(self):
        self.assertAlmostEqual(svg_kit.effective_px(20, 1200, 600), 10.0)

    def test_lint_flags_unsafe_svg(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.svg"
            bad.write_text('<svg xmlns="http://www.w3.org/2000/svg"><script>x</script>'
                           '<image href="https://x.test/a.png"/><rect onclick="x"/>'
                           '<style>@import url(https://fonts.example/x.css);</style></svg>')
            msgs = " ".join(m for _, m in svg_kit.lint_svg(bad))
            for needle in ("<script>", "external reference", "event handler", "external CSS", "no viewBox"):
                self.assertIn(needle, msgs)

    def test_writer_refuses_unsafe_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = svg_kit.Svg(10, 10, title="t").add("<foreignObject/>")
            with self.assertRaises(ValueError):
                s.write(Path(tmp) / "x.svg")

    def test_typewriter_is_safe_and_reduced_motion_aware(self):
        s = svg_kit.Svg(600, 120, title="t")
        s.add('<rect width="600" height="120" fill="#0d1117"/>')
        svg_kit.typewriter(s, 20, 50, ["Hi, I'm Ada"], loop=False, bg="#0d1117", anchor_id="a")
        svg_kit.typewriter(s, 20, 100, ["maps", "routing"], bg="#0d1117", cursor="#7ee787", anchor_id="b")
        out = s.render()
        self.assertIn("prefers-reduced-motion", out)
        self.assertIn("steps(", out)
        self.assertNotIn("<script", out)
        with tempfile.TemporaryDirectory() as tmp:
            path = s.write(Path(tmp) / "hero.svg")
            self.assertEqual([p for p in svg_kit.lint_svg(path) if p[0] == "error"], [])

    def test_text_escapes_and_adds_cjk_fonts(self):
        s = svg_kit.Svg(100, 20, title="<t>")
        s.text(0, 10, "A & 中")
        out = s.render()
        self.assertIn("&amp;", out)
        self.assertIn("PingFang SC", out)
        self.assertIn("&lt;t&gt;", out)


class SlugTests(unittest.TestCase):
    def test_github_slug(self):
        self.assertEqual(check_readme.github_slug("Quick Start!"), "quick-start")
        self.assertEqual(check_readme.github_slug("`npm` & **Yarn**"), "npm--yarn")
        self.assertEqual(check_readme.github_slug("中文 标题"), "中文-标题")


class SnapshotTests(unittest.TestCase):
    def repo(self, name, stars=0, fork=False, archived=False, pushed="2026-01-01T00:00:00Z"):
        return {"name": name, "stars": stars, "fork": fork, "archived": archived, "pushed_at": pushed}

    def test_rank_prefers_pinned_then_originals(self):
        repos = [self.repo("forked", 900, fork=True), self.repo("old", 50, pushed="2019-01-01T00:00:00Z"),
                 self.repo("star", 300), self.repo("pin2"), self.repo("pin1"), self.repo("arch", 999, archived=True)]
        ranked = [r["name"] for r in github_snapshot.rank_repos(repos, ["pin1", "pin2"])]
        self.assertEqual(ranked[:2], ["pin1", "pin2"])
        self.assertEqual(ranked[2], "star")
        self.assertEqual(ranked[-1], "forked")
        self.assertLess(ranked.index("star"), ranked.index("arch"))

    def test_slim_repo_shape(self):
        raw = {"name": "x", "html_url": "u", "stargazers_count": 3, "license": None, "topics": ["a"]}
        slim = github_snapshot.slim_repo(raw)
        self.assertEqual(slim["stars"], 3)
        self.assertIsNone(slim["license"])
        self.assertEqual(slim["topics"], ["a"])


@unittest.skipUnless(HAVE_PIL, "Pillow not installed")
class ComposeTests(unittest.TestCase):
    def test_mosaic_and_mat(self):
        from PIL import Image
        import compose_images
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            for i, size in enumerate([(1600, 900), (800, 450), (800, 450), (1200, 300)]):
                Image.new("RGB", size, (40 * i, 80, 120)).save(t / f"f{i}.png")
            buf = io.StringIO()
            with redirect_stdout(buf):
                compose_images.main(["mosaic", "--lead", str(t / "f0.png"), "--side", str(t / "f1.png"),
                                     str(t / "f2.png"), "--out", str(t / "m.jpg")])
                compose_images.main(["mat", str(t / "f3.png"), str(t / "f1.png"), "--out-dir", str(t / "mats")])
            with Image.open(t / "m.jpg") as m:
                self.assertEqual(m.width, 2400)
            sizes = []
            for p in (t / "mats").glob("*.png"):
                with Image.open(p) as im:
                    sizes.append(im.width / im.height)
            self.assertEqual(len(sizes), 2)
            for r in sizes:
                self.assertAlmostEqual(r, 4 / 3, places=2)
            self.assertIn("very wide figure", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
