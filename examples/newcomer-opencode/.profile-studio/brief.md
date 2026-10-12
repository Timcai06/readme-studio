# Profile brief — rafa-souza-dev

> Working file for the agent and the owner. Keep it in `.profile-studio/` (not published).

## Mode and assumptions
- Mode: **Create** (snapshot confirms `profile_readme.exists: false`; user asked to "make the profile").
- Data source: `./snapshot.json` only (fictional persona; user said do not look the username up). No network lookups.
- Assumptions made without the owner (confirm or correct):
  - Audience = a personal home for now (peers, teachers, future collaborators), not an active job hunt. The page stays short and honest rather than recruiter-facing.
  - "One line in Portuguese" = one short motto line, kept out of the folds, mirroring his own bio.
  - Email `rafa.souza.dev@example.com` is meant to be shown publicly (he asked for it). Flagged to him as public.
  - Visuals: he gave taste words, not file assets. All artwork is generated from his real repo facts and README commands; nothing photographic exists in the snapshot.

## Purpose
- Audience: other students, future teammates/collaborators, and whoever lands on the profile curious who this is.
- What a visitor should do after reading: understand in five seconds that this is a student who finishes small things, click into `tiny-todo`, and reach him via GitHub or email.

## Positioning
- One sentence: *Second-year computer science student in Campinas, learning by building small, finished things.*
- Through-line: **small things, finished and tested** — one small tool at a time, in the open. It explains `tiny-todo` (tested properly), `rust-book-exercises` (learning in public), and the coursework.
- Anti-goal (his words): must **not** read like a senior engineer pretending. Positioning as a learner is deliberate.

## Evidence ledger
| Claim | Source | Status | Use |
|---|---|---|---|
| Second-year CS student, Campinas, Brazil | user (request.md) + snapshot `user.location` | user-stated / verified | identity line |
| Learning Rust | user (request.md) + `rust-book-exercises` repo | user-stated / verified | identity + featured |
| Proud of `tiny-todo`, "first thing I tested properly" | user (request.md) + tiny-todo README | user-stated / verified | lead project |
| `tiny-todo`: terminal to-do list, tasks in a local SQLite file | tiny-todo description + README | verified | lead copy |
| `tiny-todo` commands `todo add/list/done` | tiny-todo README code block | verified | terminal card art |
| `tiny-todo`: argparse subcommands, SQL schema + migrations by hand, **22 pytest tests**, GitHub Actions | tiny-todo README "What I learned" | verified | lead copy + card facts |
| `tiny-todo` is Python; topics cli, sqlite; MIT | snapshot repo record | verified | stack facts |
| `rust-book-exercises`: solutions while reading The Rust Programming Language, up to chapter 9 (error handling); "not meant as a reference" | repo README | verified | featured copy (kept honest) |
| `ds-assignments`: linked lists, stacks, chained hash table, BST; MC202 course work, 2025; C | repo README + description + languages | verified | archive |
| `weather-now`: freeCodeCamp weather tutorial, then he added a 5-day forecast and °C/°F toggle | repo README | verified | archive (only his additions noted) |
| `dotfiles`: "my terminal setup", Shell | snapshot repo record | verified | archive |
| `awesome-python` | snapshot: `fork: true` | verified fork | **omit** (fork, no stated contribution) |
| 3 stars on tiny-todo, 1 on weather-now | snapshot | verified but attention-only | **not published** (drifts, measures attention not quality) |
| Languages worked in: Python, Shell, C (coursework), Rust (learning), JS/CSS/HTML (tutorial) | derived from each repo's language + README | inferred→verified by repo | "what I'm using" list, framed as tools not skills |

## Section plan
| # | Section | Job | Content | Visible / folded |
|---|---|---|---|---|
| 1 | Identity | who/what in 5 s | hero art (name + prompt), one positioning line, short paragraph, PT motto; location as a sub | visible |
| 2 | Lead work | proof | `tiny-todo`: terminal card + 2–3 sentences + real facts + link | visible |
| 3 | Learning in public | range, honesty | `rust-book-exercises`: one honest line + link | visible |
| 4 | Smaller things | archive | `ds-assignments`, `weather-now`, `dotfiles` one line each | folded |
| 5 | What I'm using | capabilities | Python/Shell/SQLite/C (course), Rust (learning) — grouped, short | visible |
| 6 | Contact | invitation | GitHub first, then email | visible |

- Project tiers: **Lead:** tiny-todo · **Featured:** rust-book-exercises · **Archive:** ds-assignments, weather-now, dotfiles · **Omit:** awesome-python (fork).
- Cut list (and why): star counts (drift + attention ≠ quality); follower/repo counts and avatar (GitHub already shows them); a "skills" wall (would imply seniority he explicitly doesn't want); weather-now as a *featured* item (it is a tutorial — kept in archive, crediting only his additions).
- Keep-list: n/a (Create mode).

## Design spec
- Concept (one sentence): **the page is a quiet terminal session on warm paper — a prompt, a short list, everything checked off.**
- Direction mix: minimal (base) + developer-oriented (his real medium: a terminal CLI tool, monospace labels) + a little editorial warmth (paper tone, generous space, one pull quote).
- Grammar: soft rectangular plates with a 1px warm rule and a small `<sub>`-style label chip; square checkboxes as the recurring mark; monospace for labels/prompt, sans for reading text; one accent only.
- Per-item variation (motif from own content): hero mark = a short checklist (todo motif); tiny-todo card = a terminal prompt line with his **real** README commands and real fact chips. No fabricated output.
- Palette (warm, ≥4.5:1 text):
  - light: bg `#fbf7f0` (paper), ink `#2b2620`, muted `#6b6152`, accent `#b45309` (burnt amber), rail `#e8dfcf`
  - dark: bg `#17140f`, ink `#ece5da`, muted `#a99c88`, accent `#f0b866`, rail `#332c22`
- Type (stacks from `svg_kit.FONTS`): sans for reading; mono for prompt/labels/commands; name set in sans 600. Body ≥12 px effective at 880 px.
- Image treatment: two theme-pair sets via `<picture>` (hero, tiny-todo card). No photos exist, so no mosaics.
- Density and rhythm: centered hero → left reading text → one lead card → honest one-liner → fold → short tools line → centered contact (bookend echo of the hero).
- Motion: none (calm page; nothing to carry).
- Deliberately absent: stats cards, streak/trophy, badge wall, typing banner, visitor counter, skill bars, "expert/passionate/seamless" language.

## Build plan
| Output | Made by | From |
|---|---|---|
| README.md | hand-written | this brief |
| assets/hero-{light,dark}.svg | tools/build_assets.py | ledger + palette |
| assets/tiny-todo-{light,dark}.svg | tools/build_assets.py | ledger + palette + tiny-todo README commands |

## Open questions for the owner
- Is a short job-hunt line wanted later, or keep it purely personal for now? (Default: personal.)
- Happy for the email to be public on the page? (Default: yes, he asked for it.)
- Want the PT motto to stay exactly "Aprendo construindo coisas pequenas — uma de cada vez"?
