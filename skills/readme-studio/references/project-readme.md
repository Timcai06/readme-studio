# Project READMEs: the same method, a different job

Use this for any repository README that is not a personal profile: libraries, CLIs, apps, research code, datasets, templates, monorepos, organisation `.github/profile/README.md`. The workflow is the same as for profiles. What changes is the reader, the source of truth, and where the README is shown.

## 1. Reader and job

A profile answers *who is this person*. A project README answers, in this order:
1. **What is it, and is it for me?** One line of value in the user's terms, plus immediate proof: a real screenshot, demo GIF, terminal recording, output, figure or minimal code example.
2. **How do I start?** Install and the shortest working example, copy-pasteable, under a minute.
3. **What can it do?** The real capabilities, each shown with a true example. This is not a list of adjectives.
4. **Where do I go deeper?** Docs, API reference, examples, FAQ, changelog.
5. **How do I take part?** Contributing, support channels, licence, credits, sponsors.

Layers map to this order: identity (name, mark, one line, proof) → quick start → capabilities → depth (links and folds) → community/licence. Each layer gets its own treatment in the page system, as on profiles.

Readers differ by project. A library needs evaluators and integrators; an app needs end users and screenshots; research code needs the paper, citation and reproduction steps; a dataset needs schema, licence and provenance; a template needs "use this template" and what you get. Decide the primary reader in the brief.

## 2. The code is the source of truth

- Every command, flag, option name, import path, default value and version range must exist in the code or the manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, CLI help text). Read them. Don't invent a feature from the project name.
- Code examples must be runnable as written: correct imports, correct API names, consistent variable names. Show real output only if you ran it or it is quoted from the project's own docs or tests.
- Run anything only in the user's own repository and with their agreement. For someone else's repo, quote and don't execute.
- Claims about performance, compatibility, users or adoption need a source (benchmarks in the repo, CI matrix, a citation). Otherwise leave them out.

## 3. Opening (the identity layer for projects)

The loudest moment is the project's name, mark and one-line value, followed straight away by proof. Proof should be *seen* whenever the project has visible output: plot the library's real results from its own example data, render the CLI's real session as a terminal figure with real output, show the real UI, draw the real data flow. A README that only quotes code is the floor, not the target. A figure drawn by the README's own build script (`tools/build_assets.py`) from the project's real output does not imply the project has that feature. Caption it truthfully ("levels computed by `tidecalc predict examples/harbour.csv`, plotted for this README") and keep the copyable text output next to it. The profile default (an animated typed name) is **not** the project default. For projects, motion belongs in the proof: a short terminal recording or demo GIF/WebP of the real thing (≤ ~5 MB; loop it calmly; the README states the essentials as text too). A typed tagline fits when the product *is* text-first (CLI, language, editor tooling) and says something true.

Logos and wordmarks: use the project's own. If none exists, a typographic wordmark generated in the page system is fine. A fake logo is not.

## 4. Badges are information here

On projects, some badges carry real facts: CI status, latest version, licence, coverage, downloads, docs link, supported runtimes. Keep the ones a reader would act on (usually 3–6), with one style and one shape, in one row near the top. Drop vanity badges (stars, "made with ❤", follower counts, PRs welcome without a CONTRIBUTING file).

## 5. Where else the README is rendered

- **GitHub** shows a README from `.github/`, the root, or `docs/`, in that order of precedence. Content beyond 500 KiB is truncated. GitHub builds an outline from the headings, so headings should form a clean hierarchy.
- **Package registries** (npm, PyPI, crates.io, the VS Code Marketplace, Docker Hub…) render the same file with their own sanitizers and without your repository around it. Relative image paths and `<picture>` theme switching can break there. A registry is a reason to make images portable, not a reason to have none. If the README is published to a registry, use absolute image URLs pinned to a tag or commit (`https://raw.githubusercontent.com/<owner>/<repo>/<tag>/path.svg`), make sure no essential fact depends on a dark/light variant, and run `check_readme.py --portable`. Registry rendering is **not verified** unless you actually looked at it; say so.
- **Docs sites** often reuse the README. Avoid GitHub-only syntax in sections that are included elsewhere, or note it.

## 6. Improving an existing project README

- Keep technical content exact: commands, API docs, version tables, citations, licence text.
- **Keep heading anchors stable.** Issues, docs, Stack Overflow answers and other READMEs link to `#installation`-style anchors. Renaming a heading breaks those links. Keep the old heading text, or add an explicit anchor such as `<a name="installation"></a>`, and list every changed anchor in the handover. `check_readme.py --baseline` reports removed headings.
- Move long reference material to docs or folds rather than deleting it, and only with the owner's agreement.
- Content scope and visual scope are separate decisions, as on profiles.

## 7. Material study for projects

The project's own outputs are the material: screenshots of the real UI, real CLI sessions, rendered examples, plots from the test data, architecture as the code actually structures it, the API surface. Libraries without a UI still have material: the shortest real example and its real result, a real before/after, the real module graph, the real config. Use `compose_images.py` for screenshots (crop away browser chrome and local paths). Record a terminal session only in the owner's repo.

## 8. Extras worth offering (owner does them)

- A **social preview image** (1280×640) made from the same page system. The owner uploads it under *Settings → Social preview*: it is not set through git.
- Repository description, topics and homepage URL that match the README's one-liner. Again, the owner sets these.
- `CONTRIBUTING.md`, `CITATION.cff` or `SECURITY.md`, only if the project needs them and the owner asks.
