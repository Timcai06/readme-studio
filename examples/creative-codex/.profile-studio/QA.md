# Local draft checks

| Check | Result |
|---|---|
| Static check_profile.py | Passed: 0 errors, 0 warnings |
| SVG lint | Passed: cover.svg |
| Asset generation | Passed: identical SHA-256 values before and after rebuilding |
| Owner artwork | Passed: all three assets byte-identical to artwork/ originals; source images visually inspected |
| Content truth | Reviewed against supplied snapshot and prompt; no live verification claimed |
| Bilingual structure | English first; five Arabic description paragraphs use lang=ar and dir=rtl; bilingual links |
| Privacy/contact | Only the supplied studio site is a contact channel; project links sourced from snapshot |
| Assets | 81,905 bytes total, four files; all images have alt text |
| Restraint | No badges, stats, terminals, editor styling, tables, animation or remote images |
| GitHub sanitizer / external links | Not verified: source-only fictional fixture; no network lookups performed |
| Light / dark / 375 px previews | Generated locally; not visually verified because ego-browser failed to connect in the sandbox |
| Live GitHub profile | Not verified: not published |
| Owner visual and Arabic-copy acceptance | Pending review |

## Review
Open preview.html for light/dark desktop and 375 px frames. It is an offline approximation with local CSS, not GitHub's actual sanitized rendering. Native links adopt GitHub's theme colour; the two spot inks apply to the artwork. Paper plates intentionally stay warm in dark mode. SVG serif fonts vary between devices. The fictional example.org studio address is preserved exactly as supplied.

## Files and regeneration
README.md is the deliverable. assets/ contains the cover and three artwork copies. tools/build_assets.py regenerates the assets using tools/svg_kit.py and the original artwork/ directory. Run `python3 tools/build_assets.py`. .profile-studio/ is ignored and contains only local review materials.

## Publishing later — owner action only
After reviewing, use a public repository named exactly noor-haddad-studio for this fictional persona. Add README.md, assets/, tools/, artwork/ (generator inputs), and .gitignore; review, commit, and push to that repository. Exclude the evaluation inputs and .agents/ and .eval/. Check the actual profile in light/dark and on a phone after publishing. No repository creation, commit, upload or push was performed here.
