# Noor — local profile brief

## Workflow
- [x] Discover: snapshot.json and artwork only; no account lookup.
- [x] Architect content.
- [x] Art direction: explicit user brief authorizes catalogue/riso treatment.
- [x] Build README + assets.
- [x] Verify, fix, re-verify: static and reproducibility checks passed; browser/live checks unavailable (see QA.md).
- [x] Hand over local preview and README for owner review; acceptance pending.

## Mode and purpose
Create. Fictional evaluation persona. Audience assumed: visitors interested in type and creative coding. Purpose: show selected work, then direct contact to the studio site. No publishing, commits, network discovery or new contact channels.

## Evidence ledger
| Claim | Source | Status | Use |
|---|---|---|---|
| Noor Haddad; type designer and creative coder; Berlin / Amman | user prompt; snapshot.user | supplied fixture / user-stated | identity |
| Letters, tides, print. | snapshot.user.bio | supplied fixture | cover |
| kufic-grid: Arabic/Latin input, modular square Kufic, editable joins, SVG export for print and laser cutting | snapshot.repos[kufic-grid].readme_excerpt | supplied fixture | lead 01 |
| Qamar: Arabic/Latin display typeface, single crescent-to-full-moon axis, SIL OFL | snapshot.repos[qamar-variable].readme_excerpt | supplied fixture | lead 02 |
| Tide Sketches: 120 daily p5.js studies, seeds and rules, water under moon | snapshot.repos[tide-sketches].description/readme_excerpt | supplied fixture | supporting practice |
| riso-sep: 2–4 spot layers, halftone and trapping | snapshot.repos[riso-sep].readme_excerpt | supplied fixture | supporting tool |
| Project URLs and studio URL | snapshot.repos[].html_url; snapshot.user.blog | supplied fixture, not live verified | links |
| Three artwork images are Noor's and OK to publish | user prompt | user-stated | unaltered plates |
| Arabic paragraphs | translations of the English claims above | editorial translation, owner review pending | visible parallel text |

## Architecture
Identity → typographic cover → kufic-grid → Qamar → Tide Sketches → riso-sep → studio.
Lead: kufic-grid, Qamar (user priority). Supporting: tides and riso tool. Omit shader-notes (less aligned with chosen selection), studio-site repository (studio contact already provided), all attention metrics and technology badges. Nothing folded. No proficiency claims inferred from languages.

## Three concepts
1. Exhibition catalogue: quiet cover, numbered full-width plates and bilingual captions. Selected: best match for whitespace and editorial request.
2. Type specimen sheet: a denser modular grid bringing Kufic and Qamar side by side. Rejected for phone legibility and desired breathing room.
3. Tide zine: wave-led opener and loose print rhythm. Rejected because it would diminish the requested lead projects.

## Design spec
Paper #f6f0e4, teal #00838a, fluorescent pink #ff48b0 sampled from supplied artwork. Paper is substrate, teal the type ink, pink small accents; no other authored ink. Original images unchanged. Cover uses system serif at 116/1200 of width, about 33 px at 343 px display. No artificial Qamar font specimen: actual font files were not supplied. The supplied Qamar artwork is captioned as a crescent-to-disc study.
Self-contained paper plates remain paper in dark mode; native HTML follows GitHub's theme. Native link blue is a platform constraint, not a third authored spot ink. No CSS in README, tables, badges, terminal/editor styling, animations or external image services. Single column with generous artwork margins; English first, visible Arabic paragraphs use dir=rtl and lang=ar. Arabic wording and aesthetic acceptance remain for Noor's review.

## Outputs
README.md; assets/cover.svg; three byte-identical artwork copies; tools/build_assets.py and svg_kit.py; local-only preview and QA notes. Generator sources are the supplied artwork and snapshot bio phrase. Shipping artwork/ is necessary only to regenerate assets; README uses assets/.
