# Profile brief — ingridh-demo

## Mode and assumptions
Create: snapshot profile_readme.exists is false. Fictional evaluation persona.
Only snapshot.json and the user's stated positioning supply personal facts.
No network requests, live identity lookup, commits, or publication authorized.
English; static assets; reviewable first draft using the explicitly requested terminal aesthetic.

## Purpose and positioning
Developers should find an appropriate Postgres operations tool; hiring managers should immediately understand Ingrid's focus.
“I build tools that make Postgres safer to operate.”
Through-line: migration risk prevention, incident forensics, operational visibility.

## Evidence ledger
| Claim | Source | Status | Use |
|---|---|---|---|
| Ingrid; staff-level engineer; previously SRE; builds safer Postgres tools | User request; snapshot user.name and bio corroborate name/domain/history | user-stated | Intro |
| Conference speaker | User request; repos[talks].readme_excerpt | user-stated and export-supported | Intro/talks |
| migra-lint flags locks, table rewrites, blocked writes and suggests safe alternatives; CLI/library/Action | repos[migra-lint].readme_excerpt | verified against export only | Lead |
| migra-lint check migrations/*.sql | Same excerpt, exact command | verified against export only | Command artwork |
| Check migrations before production | repos[migra-lint].description | editorial paraphrase | Artwork caption |
| pgwhen read-only timestamp endpoint; WAL reconstruction; incident forensics; pgBackRest/WAL-G | repos[pgwhen].readme_excerpt | verified against export only | Lead |
| pg-lockviz wait-for graph from pg_locks; blocking relations | repos[pg-lockviz].readme_excerpt | verified against export only | Featured |
| tracehound query latency via eBPF without app changes; experimental; Linux ≥5.15 | repos[tracehound].description and readme_excerpt | verified against export only | Featured |
| Three conference titles, venues, years; slides/notes and recordings where available | repos[talks].readme_excerpt and description | verified against export only | Talks |
| Project links | Relevant repos[].html_url | copied from export, not live-verified | Links |
| Blog, Mastodon, LinkedIn | user.blog; social_accounts | export-supported, user-approved channels | Footer |

## Section plan
All visible: identity → command artwork → two lead tools → two diagnostic tools → talks → contact.
Lead: migra-lint, pgwhen. Featured: pg-lockviz, tracehound. Separate practice: talks.
No archive. Omit the other 21 repos: smaller utilities dilute the four-tool narrative; config/learning/personal repos are peripheral; kafka-replay is archived; postgres/cockroach/kubernetes are forks without contribution evidence.
No skill inventory derived from language bytes, unsupported adoption claims, employment details, or hiring availability.

## Design spec
Three candidates: (1) operator's notebook with a real CLI specimen, (2) WAL timeline diagram, (3) lock wait-for graph.
Selected (1): most direct fit for terse developer-oriented terminal aesthetics. Shown in progress update before build; user requested build then review.
One understated SVG pair, single accent rail, no window buttons, prompts, pretend output or status lights.
Minimal + developer direction. Single-column native Markdown. No tables or folds on the public page.
720×132 command image; 27px mono command (12.86px at 343px width), 16px secondary label. Native text keeps all essential claims accessible.
Dark: slate surface / pale text / muted mint accent. Light: light-grey surface / graphite / deep teal.
System monospace fonts; 10% width slack; no motion or external image dependencies.
No stats, streaks, badges, avatar, or repo inventory.

## Build plan
README.md: ledger-based prose. assets/migration-{light,dark}.svg: tools/build_assets.py with vendored svg_kit.py.
.profile-studio/: brief, offline preview, checks, publishing notes. Excluded by .gitignore.

## Open questions
None required to build. Owner's visual and editorial acceptance pending.

## Checklist
- [x] Discover
- [x] Architect content
- [x] Art direction
- [x] Build README + assets
- [x] Verify, fix, re-verify (offline checks; browser and GitHub limitations recorded)
- [x] Hand over
