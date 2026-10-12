# Testing report

Run on 2026-10-12 on macOS, by the maintainers. Every result below was actually run. Anything not run is listed under "Not verified". Re-run everything with the commands in §6.

## 1. Package and scripts

| Check | Result |
|---|---|
| Official validator `uvx --from skills-ref agentskills validate skills/github-profile-studio` (skills-ref 0.1.1) | **pass** ("Valid skill") |
| `python3 tools/validate_skill.py` (name/dir match, description ≤ 1024 and contains "Use when", SKILL.md < 500 lines and ~5k tokens, every referenced file exists one level deep, every reference is mentioned in SKILL.md, all scripts `--help`) | **pass**, 0 problems. SKILL.md ≈ 1.8k tokens |
| `python3 -m unittest discover -s tests` | **pass**, 19 tests (checker rules, render-comparison, SVG lint/measure/escape, snapshot ranking, mosaic + mat geometry) |
| `github_snapshot.py octocat` against the live API (authenticated, then anonymous) | **pass**: 8 repos, forks flagged, pinned = [] with token / unknown without, 17 and 8 API calls |
| `check_profile.py --render` on the maintainer's own published profile (230 lines, 74 images, 7 folds) | **pass**: 0 errors, 0 warnings, all images and folds survive the real sanitizer |
| Sanitizer probe (every tag in `references/github-rendering.md` §1) through `POST /markdown` | done. The table in the reference *is* this result |

## 2. Scenario runs with fresh agents

Each run uses a clean workspace containing only the fixture (fictional persona) and the skill installed at project level. The prompt is the persona's request verbatim and **never names the skill** (`evals/run_case.sh`). Automatic assertions come from `evals/evals.json` (graded by `evals/grade.py`). Manual review was done by reading the README, brief and transcript.

| Case | Agent | Network | Auto | Manual review |
|---|---|---|---|---|
| 1 Newcomer (6 repos, one fork, one tutorial) | Codex CLI 0.160.0 (gpt-6-astra, medium) — round 2 | off | 9/9 | Honest learner positioning. tiny-todo leads with what was learned. The fork and the tutorial repo are omitted with reasons in the brief. Emits a small checklist mark. |
| 1 Newcomer | OpenCode 1.18.35 (opencode/big-pickle, user plugins on) | on | 9/9 | Hero + tiny-todo terminal art (light/dark pairs). weather-now credited as tutorial-based. Archive in one fold. The agent measured preview DOM and moved a card out of a table after finding it shrank to 111 px on phones. |
| 2 Seasoned (26 repos, 3 forks, talks) | Codex — round 2 | off | 7/7 | Leads with migra-lint + pgwhen framed as "before production · after an incident"; talks listed; forks excluded; no star counts as text. The theme-paired SVG quotes a real command from the README. No archive fold: the user asked not to list everything, and the brief records what was cut. |
| 3 Creative contrast (type designer, riso taste) | Codex (round 1) | on* | 7/7 | Editorial catalogue: serif typographic cover in teal/pink on paper, numbered works with full-width plates, English + Arabic (RTL) paragraphs, no badges, no terminal. Reads clearly unlike the origin profile. |
| 4 Improve existing template README | Codex (round 1) | off | 6/6 | Works on a copy (`improved/`). `existing/` byte-identical (hash). Keep-list verbatim (GIF, reading list, Spanish line). Removed snake, stats and badge wall. Writes `CHANGES.md` + `changes.diff`. Small regression: the GIF lost its `align="center"`. |
| Demo (cartographer) | Codex (round 1) | on* | 6/6 | Light/dark contour-and-river SVG from a 37-line generator, labelled "imagined landscape, not geographic data". Leads with contour-kit and riverline. Badges and stats removed after a baseline diff. |

\* Network was allowed, but the agents chose not to call GitHub's render API because the persona said "do not look the username up". The maintainers then ran `--render` on every output (§3).

### Iteration (what the evals changed)

Round 1 showed the content work was right but the visuals were too cautious. The newcomer and seasoned outputs were text-only, even though the seasoned persona asked for a terminal look. We added an explicit rule to `SKILL.md` step 4 ("Visual expression is part of the job … a requested look must show up in the artwork") and a line on small-but-not-bare pages to `content-architecture.md`. Round 2 of the same two cases produced original, theme-paired visuals with no loss in content scores. Round-1 READMEs are kept in `examples/round1/` for comparison.

## 3. Checks on all example outputs (run by maintainers)

| Check | Result |
|---|---|
| `check_profile.py --render` (GitHub's real sanitizer) on all 6 example READMEs | **pass**: 0 errors, 0 warnings; every image and fold kept |
| `svg_kit.py lint` on the 10 generated SVGs | **pass** |
| Generators re-run → byte-identical assets (5 generator scripts) | **pass** (reproducible) |
| SVG text geometry in Chromium (getBBox: text outside canvas / overlapping) | 5 files clean; `creative-codex/cover.svg` reports bounding-box overlap of two stacked 116 px display lines (tight leading). Needs a visual look; may be intended. |
| Preview pages (`render_preview.py`): images load, no horizontal overflow at 880 px and 375 px, dark panel uses dark sources | **pass** on all 7 pages (DOM inspection) |

## 4. Trigger accuracy (`evals/trigger_test.sh`)

Fresh read-only Codex workspace per query, skill installed, "plan only":

| Expected | Got | Query (abridged) |
|---|---|---|
| trigger | trigger | 帮我把我的 GitHub 个人主页做得好看一点… |
| trigger | trigger | My GitHub profile looks like every other template… redesign it? |
| trigger | trigger | I just made the repo with my username… what should I put on it? |
| trigger | trigger | Audit my profile README… |
| no | no | Fix the typo in the README of my Python library |
| no | no | Write a README for my CLI tool |
| no | no | Build a portfolio website with Next.js |
| no | no | Add a GitHub Actions workflow for pytest |

8/8 on Codex. OpenCode called its `skill` tool for this skill in 2 of 3 runs (not in the `--pure`, plugins-off run). Claude Code listed the skill in its session catalogue.

## 5. Compatibility matrix

| Client | Install path used | Discovery | Trigger | Full task | Notes |
|---|---|---|---|---|---|
| Codex CLI 0.160.0 | `.agents/skills/` | ✅ | ✅ 8/8 | ✅ 7 runs | Reads the user's global AGENTS/skills too (environment bleed: one run consulted an unrelated browser skill). |
| OpenCode 1.18.35 | `.agents/skills/` | ✅ | ⚠️ 2/3 runs | ✅ 1 run, ⚠️ 1 run, 1 aborted by us | With `--pure` (plugins off) and the free model, the skill was not loaded and the agent printed a README in chat instead of writing files. One early run was aborted because we edited the runner mid-run. |
| Claude Code 2.1.288 | `.claude/skills/` | ✅ (`github-profile-studio` in the session's skill list) | — | **not verified** | Headless CLI login on the test machine had expired ("OAuth session expired"); re-run `evals/run_case.sh claude <case>` after `claude /login`. |
| Gemini CLI 0.45.0 | `.agents/skills/` | **not verified** | — | — | Could not reach Google's auth endpoint from the test network (TLS reset). |
| Cursor | `.agents/skills/` or `.cursor/skills/` | **not verified** | — | — | Not installed on the test machine. Cursor documents both paths. |

Format compatibility (spec-valid frontmatter, relative paths, no client-specific fields) is a property of the package. Discovery and execution are properties of each client, and only the ✅ cells were observed.

## 6. Not verified (and why)

- **A real github.com profile page.** Nothing was published. Verified up to GitHub's sanitizer plus github-markdown-css. Not verified: page chrome, exact column width, camo fetching, OS fonts.
- **Claude Code, Gemini CLI and Cursor full runs** (see §5).
- **Aesthetic quality.** The maintainers deliberately reported facts and left visual judgement to a human reviewer. The `preview.html` files exist so a human can judge.
- **Windows/Linux font metrics** for SVG text. Estimates only (`svg_kit.measure`).
- **`github_snapshot.py` on very large accounts** (> 200 repos) and the GraphQL pinned query under fine-grained tokens.

## 7. Reproduce

```bash
uvx --from skills-ref agentskills validate skills/github-profile-studio
python3 tools/validate_skill.py
python3 -m unittest discover -s tests -v
python3 evals/make_fixtures.py
evals/run_case.sh codex newcomer          # or claude | opencode | gemini; cases: newcomer seasoned creative improve demo-ilse
python3 evals/grade.py newcomer evals/runs/<workspace>
evals/trigger_test.sh codex evals/trigger-codex.tsv
```
