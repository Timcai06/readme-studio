# Profile brief — Tomás

## Scope and plan
Improve mode. Fictional fixture only; no network or account discovery.
User authorized a calmer minimal-editorial copy focused on Cartero and queue-bench.
Assume English remains primary, Spanish sign-off preserved, audience is fellow backend builders.
[x] Discover supplied files
[x] Diagnose and architect content
[x] Select direction within requested scope
[x] Build independent copy
[x] Static verification and source-integrity checks
[x] Handover with limitations

## Diagnosis before redesign
- Content: existing README lines 6–10 retain personal voice, but Cartero has only one bullet and queue-bench is absent. Give each project a visible description and direct link; retain personal statements.
- Visual: lines 3, 13, 15–22 contain typing animation, 12 badges, stats, streak and snake. Remove these to give project text priority. Keep the supplied pixel art.
- Engineering: original checker found 0 errors and 3 warnings: missing alt on stats/streak images at lines 17, 18, 20. It also identified external image-service dependencies. Replacement has only a local image with alt.

## Evidence ledger
| Claim | Source | Status | Use |
|---|---|---|---|
| Name Tomás; calmer minimal-editorial; lead projects | User request | user-stated | identity and ordering |
| Builds Cartero and queue benchmarks | User request; snapshot repos | fixture-supported | opening |
| Cartero self-hosted relay, durable Postgres storage, retries/backoff, Phoenix delivery dashboard and replay | snapshot repos[name=cartero].description/readme_excerpt | fixture-supported, not independently verified | lead project |
| Oban, river, pgmq; same workload, throughput/latency under contention, reproducible scripts | snapshot repos[name=queue-bench].description/readme_excerpt | fixture-supported | second project |
| Learning Elixir/OTP, collaboration interest, Postgres/queues/coffee, ferry anecdote | existing README lines 7–10 | owner-authored fixture | personal paragraph |
| Postgres internals notes | snapshot repos[name=pg-notes].description | fixture-supported | supporting link |
| pixel-me makes supplied profile avatar | snapshot repos[name=pixel-me].readme_excerpt | fixture-supported | supporting link |
| Reading entries and Spanish sign-off | existing README lines 25–31 | owner-authored, explicit keep | verbatim |
| Four project URLs | snapshot repos[*].html_url | fixture-supported, not visited | direct links |

## Content architecture
Visible: identity → Cartero → queue-bench → personal notes and two supporting links → reading → avatar/sign-off.
Lead: Cartero, queue-bench. Supporting: pg-notes, pixel-me. Omit: lumen (outside focus), profile repo (self-reference).
Keep: avatar file byte-for-byte including four frames, all three reading entries verbatim, exact Spanish phrase; retain personal substance.
Cut: badges, typing banner, stats, streak, snake; old service URLs were decorative image sources, not contact links.

## Art direction
Candidates: backend notebook; Cartero postal dispatch; queue comparison lab sheet.
Chosen: backend notebook, a text-first page with concrete project entries and a personal reading/sign-off section. Fits the explicit brief without introducing invented charts or extra imagery.
Alternative: postal dispatch would give Cartero more visual identity but overemphasize one project.
Grammar: single left-aligned column, native h1 masthead and h3 entries, two native rules, descriptive blue project links. No cards or tables.
Palette/type: GitHub native light/dark text and system typography. No custom font dependency.
Images: original 32×32 GIF at existing 96px display size; four animation frames preserved. No generated imagery.
Motion: supplied avatar only. Density: short project paragraphs, no folded primary content.
No open factual questions. Aesthetic approval remains the owner's.

## Verification limits
Static checker: 0 errors / 0 warnings. Baseline removals match documented cut list.
No SVGs to lint, no new image generator needed.
Offline HTML preview approximates Markdown and themes using local CSS; not GitHub sanitizer output.
Actual browser layout, live GitHub rendering, and external URL availability not verified. No publishing or network calls.
