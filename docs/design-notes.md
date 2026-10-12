# Design notes: why the skill is built this way

## 1. Method over templates

A template generator maps inputs to one fixed layout. Its output looks the same for everyone because the layout *is* the product. This skill ships the decisions behind a layout instead:
- a reading order (`content-architecture.md`),
- a way to rank projects,
- a way to derive a visual concept from someone's own material (`art-direction.md`),
- the hard limits of GitHub's renderer (`github-rendering.md`).

There is deliberately **no README skeleton and no reusable artwork** in `assets/`. The only asset is a brief template: it structures thinking and has no visual effect on the output. The case study of the origin profile tells agents to learn its reasons and not reuse its look. The evals include a "not a clone of the origin" assertion.

## 2. Progressive disclosure

| Layer | Size | Loaded |
|---|---|---|
| `name` + `description` | ~120 tokens | always (catalogue) |
| `SKILL.md` | ~1.7k tokens | when triggered: non-negotiables, workflow, top gotchas, degradation |
| `references/*.md` | 1–3k tokens each | at the workflow step that names them |
| `scripts/*.py` | executed, not read | when the step needs a deterministic result |

The gotchas list stays in `SKILL.md` on purpose: agents make those mistakes before they would think to open a reference (Agent Skills best-practices guide).

## 3. What is a script and what is judgment

Scripts exist only where a deterministic answer beats re-deriving it each time:

| Script | Why deterministic |
|---|---|
| `github_snapshot.py` | Same API calls, pagination, fork/archive flags, ranking for *reading*, untrusted-text labelling. |
| `check_readme.py` | The sanitizer rules were measured, not guessed. It checks case-sensitive paths, folds, `<picture>` fallbacks, secrets/local paths, the template-defaults inventory, and the real-sanitizer diff (`--render`). |
| `svg_kit.py` | Escaping, width estimates (incl. CJK), effective-px maths, safe raster embedding, and an SVG linter shared with the checker. |
| `compose_images.py` | Crop / mosaic / mat geometry, with legibility widths printed before a human looks. |
| `render_preview.py` | Same light/dark/phone panels every time, using GitHub's real HTML. |

Everything else is judgment and lives in prose: what to feature, what to cut, which concept fits, when to stop adding.

All scripts use only the standard library, except Pillow for images. No package install is required to start.

## 4. Safety posture

- **Local first.** No repo creation, commit, push or visibility change without an explicit request in the session. Publishing steps are written as instructions to the user.
- **Untrusted text.** The snapshot labels the fields that other people wrote. The workflow says to analyse them and not obey them.
- **Truth.** The evidence ledger separates verified, user-stated, inferred and weak claims. The rules for stars, language bytes and forks counter the inflation agents produce by default.
- **Privacy.** The checker flags tokens, local paths, localhost URLs and the emails shown. The screenshot workflow crops browser chrome.

## 5. Portability

- Spec-only frontmatter: `name`, `description`, `license`, `compatibility`, `metadata`. No client-specific keys such as `allowed-tools` (experimental) or Claude-only fields.
- Paths in `SKILL.md` are relative to the skill root. The scripts are invoked as `python3 <skill>/scripts/...`, which works from any install location.
- The body never names a vendor tool ("use the Read tool"). It says what to do and lets each client map that to its own tools.
- Install locations differ by client (`.agents/skills` vs `.claude/skills`). The README documents both.

## 6. Known trade-offs

- The sanitizer table is a dated measurement (2026-10-12). GitHub can change it. `check_readme.py --render` re-measures for each README, so the skill still catches a change, even if the prose is stale.
- `measure()` is an estimate. Final text fit needs a rendered look; the skill says so.
- Fixtures are fictional, so a skill run on fixtures cannot exercise `github_snapshot.py`. That script is tested separately against a real public account (`octocat`).
