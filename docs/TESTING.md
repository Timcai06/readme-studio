# Testing report (v0.3, 2026-10-12)

Only results that were actually run are listed. Anything not run is under "Not verified". Earlier versions' results are in git history.

## Package and scripts

| Check | Result |
|---|---|
| `uvx --from skills-ref agentskills validate skills/readme-studio` | pass |
| `python3 tools/validate_skill.py` (spec fields, SKILL.md budget, every reference exists and is named in SKILL.md, scripts `--help`) | pass |
| `python3 -m unittest discover -s tests` | pass, 24 tests |
| `github_snapshot.py` live: user `octocat`; `--repo octocat/Hello-World`, `--repo sindresorhus/slugify` | pass |
| `check_readme.py --render` on a published profile (230 lines, 74 images, 7 folds) | 0 errors |
| Sanitizer probe through `POST /markdown` | done; it is the table in `references/github-rendering.md` |
| `svg_kit.typewriter()` timeline sampled in Chromium (typed-once name, cycling lines) | as designed |

## Agent runs

| Case | Agent | Result |
|---|---|---|
| Trigger test, 11 queries (`evals/trigger_test.sh`) | Codex CLI 0.160.0 | 11/11 (`evals/trigger-codex.tsv`) |
| Project README, runnable fictional library `tidecalc` (`evals/fixtures/project-tidecalc`), 3 runs | Codex | 7/8 automatic assertions each run. Every CLI flag and both code examples were verified against the code (re-run by us: identical output). The agents also found a real packaging gap. All three runs chose a text-only README (see Open). |
| Profile Improve on a real public account (local, unpublished concept) | Codex | Material study of real artefacts, concrete concepts plus swap test, animated identity opening, real work frames with licence notes, 11/11 original links kept, sanitizer clean. Visual judgement: owner. |

## Open

- Tiny text-output projects: agents keep choosing text-only READMEs. The skill demands a named reason. Whether a figure from real output should be mandatory is undecided.
- One project run skipped the brief and design check entirely: an execution deviation at default effort.

## Not verified

- A published github.com page; npm/PyPI rendering.
- Full runs in Claude Code (headless login expired on the test machine), Gemini CLI (network), Cursor (not installed).
- SVG text metrics on Windows/Linux.

## Reproduce

```bash
uvx --from skills-ref agentskills validate skills/readme-studio
python3 tools/validate_skill.py && python3 -m unittest discover -s tests
python3 evals/make_fixtures.py
evals/run_case.sh codex project-tidecalc     # cases: newcomer seasoned creative improve demo-ilse project-tidecalc
python3 evals/grade.py project-tidecalc evals/runs/<workspace>
evals/trigger_test.sh codex evals/trigger-codex.tsv
```
