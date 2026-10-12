# Examples

Real outputs from fresh agents that had only the skill and a fictional persona (`evals/fixtures/`). They are not hand-made showcases and have not been edited. Their quirks are left in, because they are what the skill produced.

| Folder | Agent | Persona → what to look at |
|---|---|---|
| `newcomer-codex/` | Codex CLI 0.160.0 | Student, 6 repos → honest, short; a small mark; fork and tutorial left out with reasons in `.profile-studio/brief.md` |
| `newcomer-opencode/` | OpenCode 1.18.35 | Same student → a different design: hero + terminal art, archive fold, tutorial credited |
| `seasoned-codex/` | Codex | Postgres engineer, 26 repos → two leads, lifecycle framing, talks, theme-paired SVG with a real command |
| `creative-codex/` | Codex | Type designer → editorial catalogue, English + Arabic, the user's own artwork, no badges |
| `improve-codex/improved/` | Codex | Existing template README → keep-list preserved, `CHANGES.md`, `changes.diff`, original under `.profile-studio/original/` |
| `demo-ilse-codex/profile/` | Codex | The video demo: template → cartographic profile, contour/river SVG generator |
| `round1/` | Codex | First-round READMEs for newcomer/seasoned, before the visual-expression rule was added |

Each folder has `grade.json` (automatic assertions) and, where generated, `preview.html`. Open it locally to see light / dark / phone panels rendered from GitHub's real HTML. Re-run any generator with `python3 tools/build_assets.py`; the outputs are byte-identical.
