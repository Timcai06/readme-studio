# What GitHub actually renders in a profile README

Read this before writing any HTML in a README, and again when something "works locally but not on GitHub".

Status labels used below:
- **Verified (API)**: checked by posting a probe file to `POST /markdown` (`mode=gfm`), the sanitizer GitHub uses for READMEs, on 2026-10-12. Re-run `scripts/check_readme.py README.md --render` to check your own file.
- **Verified (live page)**: seen working on a published profile README.
- **Documented**: stated in GitHub's docs, not re-tested here.
- **Known behaviour**: established practice that the API cannot show (it is CSS or client-side). Check it on a real page when it matters.

## 1. The sanitizer, in one table (Verified, API)

| You write | GitHub keeps | Notes |
|---|---|---|
| `<p align>`, `<div align>`, `<h1>`…`<h6> align` | yes | `align="center"`/`"right"` is the only layout control you get. |
| `id="x"` | becomes `id="user-content-x"` | Fragment links `#x` still work on github.com: its script maps them. Heading anchors are added client-side. |
| `style=`, `class=` | **stripped** | No CSS at all. No colour, font, spacing, flex or grid. |
| `<img src width height align alt>` | yes | `width="50%"` or pixels works. `height` becomes `max-height`. `loading`, `style` stripped. An `<img>` not wrapped in `<a>` gets auto-wrapped in a link to the image itself. |
| `<picture><source media="(prefers-color-scheme: dark)" srcset>…<img></picture>` | yes | Wrapped in `<themed-picture>`. The way to ship light/dark artwork. Always include the fallback `<img>`. |
| `<table width align cellpadding>`, `<td width valign align colspan rowspan>` | yes | `border` on `<table>` and `bgcolor` on cells are stripped. |
| `<details open>`, `<summary>` | yes | Nesting works. |
| `<kbd> <samp> <sub> <sup> <ins> <del> <s> <strike> <mark> <var> <q> <tt> <code> <b> <i> <em> <strong>` | yes | `<code>` gains `class="notranslate"`. |
| `<dl><dt><dd>`, `<ruby><rt>`, `<hr width>`, `<br clear>` | yes | |
| `<span title>` | span kept, `style` stripped | Useless for styling. |
| `<a href title name>` | yes | `target` and `rel` are replaced by GitHub's own. `name` gets the `user-content-` prefix. |
| `<font>`, `<center>`, `<u>`, `<small>`, `<big>`, `<abbr>`, `<cite>`, `<dfn>`, `<figure>`, `<figcaption>`, `<button>` | **tag dropped, text kept** | Their effect is lost silently. Use `align`, `<sub>` instead. |
| `<svg>` inline, `<video>`, `<audio>`, `<input>`, `<form>` | **removed entirely** | Ship SVG as a file in `<img>`. |
| `<script>`, `<style>`, `<iframe>` | **escaped and shown as literal text** | Worse than removal: visitors see the code. |

Also verified in the same probe: GitHub alerts (`> [!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, `[!CAUTION]`), Mermaid fences (rendered client-side in an iframe), math (`$…$`, `$$…$$`), task lists, footnotes, emoji shortcodes, column alignment in Markdown tables. External images are rewritten to `camo.githubusercontent.com` proxy URLs.

### Markdown inside HTML (Verified, API)

An HTML block such as `<td>`, `<div>`, `<p>`, `<details>` turns off Markdown until the next blank line. So:

```html
<td>

**This is bold**, because blank lines surround it.

</td><td>**This stays literal**</td>
```

Inside HTML blocks, prefer HTML (`<b>`, `<a>`, `<img>`) and you never hit this.

## 2. CSS effects you cannot see in the API (Known behaviour)

- Links are always in the theme's link colour (blue). You cannot change it. A link wrapped around an `<img>` shows no blue text. A link around `<kbd>` keeps the kbd's grey text in practice; that is how the origin profile got grey "buttons" (Verified, live page).
- Tables get cell borders and alternating row backgrounds. You cannot remove them. Tables also don't stack on phones: a two-column table stays two columns at 343 px.
- `<h1>` and `<h2>` get a bottom border line. Use it as a section divider or avoid h1/h2.
- `<blockquote>` text is muted grey with a left bar. `<kbd>` looks like a key with a border. `<code>` is a grey pill. `<mark>` is a yellow/amber highlight in both themes, which is loud on a calm page. `<sub>` text is smaller and visually lighter.
- The README column on a desktop profile page is roughly 830–900 px wide, depending on the page layout. Plan images at 2× that width (about 1600–1800 px), or an SVG viewBox of 1200–1600 px with `width="100%"`.
- `#gh-dark-mode-only` / `#gh-light-mode-only` URL fragments hide an image in the other theme (Documented). `<picture>` is clearer and works in more places; prefer it.
- On phones, `width="50%"` images inside a table get very small, around 120–170 px. Text inside those images becomes unreadable. Keep every essential fact as real text.

## 3. Images and SVG on GitHub

- Relative paths (`./assets/x.svg`) resolve inside the repository, on the current branch. A leading `/` resolves from the repository root (Documented). Paths are **case-sensitive** on GitHub but often not on your disk. `check_readme.py` catches the mismatch.
- An SVG shown through `<img>` cannot run scripts, cannot load external files (fonts, images, CSS) and should not use `<foreignObject>`. CSS `@keyframes` and SMIL animations inside the SVG do play. Animated third-party SVGs such as typing banners rely on this (Verified, live page).
- Text inside SVG uses the viewer's installed fonts. Use system font stacks (`scripts/svg_kit.py: FONTS`). Expect width differences of ±10% between macOS, Windows and Linux.
- Large embedded rasters make huge SVGs. In the origin project, 1.6–3.5 MB editor SVGs dropped to 52–145 KB after quantizing the embedded background to 8 colours. Budget about ≤ 300 KB per SVG and ≤ 800 KB per photo/JPEG.
- GIF/APNG/WebP animation plays. Video does not, except as an uploaded `user-images` attachment URL, which only works if the user uploads it themselves.

## 4. Where READMEs are shown (Documented)

- Repository README: GitHub picks it from `.github/`, then the root, then `docs/`. Content beyond 500 KiB is truncated. GitHub builds an outline (table of contents) from the headings, and every heading gets an anchor.
- Package registries render the same file with their own rules; see `project-readme.md` §5.

**Profile READMEs:**

- The README shows on `github.com/<username>` when a **public** repository named exactly `<username>` has a `README.md` in its root. GitHub offers to create it with a README when you make that repo.
- Organisation profiles are different: a public `.github` repository with `profile/README.md`. Member-only versions go in `.github-private`.
- The page already shows the avatar, name, bio, location, links, pinned repositories and the contribution graph. Don't repeat them unless you add something they lack.

## 5. Layout recipes that hold up

Use these as building blocks. They are not a page template.

**Centered block**
```html
<p align="center"><img src="./assets/hero.svg" width="100%" alt="…"></p>
```

**Theme-aware artwork**
```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/hero-light.svg">
  <img src="./assets/hero-light.svg" width="100%" alt="Describe what the image says, not 'banner'">
</picture>
```

**Two-up cards.** Remember the table borders, and that cells stay side by side on phones.
```html
<table><tr>
<td width="50%" valign="top">
<a href="https://github.com/u/a"><img src="./assets/a.svg" width="100%" alt="…"></a>
<h3>Project A</h3>
<p>One sentence of what it is for.</p>
</td>
<td width="50%" valign="top">…</td>
</tr></table>
```

**Media row** (image left, text right; uniform image column width)
```html
<table><tr>
<td width="40%" valign="middle"><img src="./assets/b.png" width="100%" alt="…"></td>
<td valign="middle"><h3>Project B</h3><p>…</p></td>
</tr></table>
```

**Grey "button" links instead of blue text** (Verified, live page)
```html
<a href="https://github.com/u/a"><kbd>Repository ↗</kbd></a>
```

**Chapter opener**: centered h1 with a small index and subtitle; GitHub adds the rule underneath.
```html
<h1 align="center"><sub><samp>01</samp></sub><br>Selected work<br><sub>Things I built and still maintain</sub></h1>
```

**Fold with an informative summary**: say what is inside so nobody has to open it to know.
```html
<details>
<summary><b>Archive</b> — 11 smaller projects: CLI tools, course work, experiments</summary>

…content (blank line above and below if Markdown)…

</details>
```

## 6. Third-party image services (decide deliberately)

| Service type | Examples | Risk | Default |
|---|---|---|---|
| Static badges | shields.io `/badge/…` | Low. Cached by camo, simple URL. | Use sparingly, for real facts (stack of a project, a link). |
| Live stats / langs / streak / trophies | github-readme-stats, streak-stats, trophy | Public instances get rate-limited or go down. The numbers often flatter or mislead (e.g. "top languages" by bytes). | Off, unless the user asks or a number really tells their story. |
| Typing / animated text | readme-typing-svg | Depends on a free service. | Animated identity text is welcome when it says something true. Prefer generating it in the repo (`svg_kit.typewriter`); use the service only if the user wants it. |
| Contribution snake, activity graphs | Platane/snk via Actions | Needs a workflow committed to the user's repo. Mostly decoration. | Off unless asked. If asked, explain the Action it requires. |
| Icon sets | skillicons.dev, simple-icons via shields | External, and square icons mixed with rectangular badges look ragged. | Vendor (download into `assets/`) when the set is stable. |

When a dynamic service is used, the README breaks when the service does. Static, vendored assets don't.
