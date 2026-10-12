# Engineering checks before delivery

These checks prove the page is **correct**: GitHub-compatible, truthful, safe, legible in both themes and accessible. They do not judge whether the design is good. That judgment happened in the design check (SKILL.md step 5) and belongs to the owner. Never summarise passing checks as "design complete" or "looks good". Keep the effort proportionate: run what applies once, fix, re-run. Don't produce extra check artifacts beyond the report table.

Run every applicable check. Report each result as **passed**, **failed (fixed)**, **failed (open)** or **not verified (why)**. Never write "passed" for something you did not run.

## 1. Automated

```bash
python3 scripts/check_profile.py README.md                       # always (offline)
python3 scripts/check_profile.py README.md --render --context <user>/<user> --save-html .profile-studio/github.html   # when online
python3 scripts/check_profile.py README.md --online              # when online: every external URL
python3 scripts/check_profile.py README.md --baseline .profile-studio/original/README.md   # Improve mode
python3 scripts/svg_kit.py lint assets/*.svg
python3 scripts/render_preview.py README.md --context <user>/<user>   # light / dark / phone preview page
```

Fix every **error**. Read every **warning** and either fix it or say why it stays. **Info** lines are an inventory. Mention the relevant ones (emails shown, third-party services, removed items) to the user.

If the generator script exists, re-run it and confirm a clean diff:

```bash
python3 tools/build_assets.py && git status --short assets/
```

The command is only an example; use the profile repo's own generator. No diff means the art is reproducible.

## 2. Content truth (manual, every time)

- [ ] Every factual sentence maps to a ledger row (verified or user-stated). No invented metrics, roles, dates, users, awards.
- [ ] Technologies listed per project appear in that repo (language stats, dependency files or README).
- [ ] Skill or capability lists are confirmed by the user or shown by projects, not taken from language bytes.
- [ ] Links to private repositories: none. Check with `--online`; 404 on a github.com link usually means private.
- [ ] Contact channels are exactly the ones the user approved.
- [ ] Improve mode: everything on the user's keep-list is still present, verbatim where they asked.

## 3. Rendering and legibility (engineering, not taste)

Use the preview page. Inspect DOM and SVG geometry if you can't view images. Screenshot review is optional unless the user asks for visual verification.

- [ ] Light **and** dark: no invisible text, `<picture>` pairs switch.
- [ ] Phone width: essential facts exist as text; nothing wider than the column.
- [ ] Text in images has effective size ≥ 12 px on desktop and stays inside its canvas (bbox snippet in `svg-craft.md`).
- [ ] Alt text says what each image communicates.

## 4. Publishing readiness (don't publish, just check)

- [ ] Files are local. Nothing committed or pushed unless the user said so explicitly in this session.
- [ ] `.profile-studio/` (brief, snapshot, previews, originals) is listed in `.gitignore`, or the user chose to commit it.
- [ ] No local absolute paths, `localhost` URLs, tokens, private emails or screenshots with browser chrome (the checker covers most; read the images yourself).
- [ ] Assets within budget (SVG ≤ ~300 KB, photos ≤ ~800 KB, page total ≤ ~6 MB).

## 5. What the API cannot prove (say so)

The Markdown API proves the sanitizer result. It does not show github.com's CSS: table borders, link colour, `<kbd>` styling, theme switching, column width, the camo proxy fetching your external images, or font rendering on other OSes. The preview approximates these. Only a real profile page proves them. Offer the user a check after they publish, or a private-preview approach: push to a scratch repository they own and open its README. Never create that repository yourself without explicit permission.

## 6. Report template

```markdown
## Checks
| Check | Result |
|---|---|
| check_profile.py (static) | passed — 0 errors, 2 warnings (explained below) |
| GitHub sanitizer (--render) | passed — 14 images, 2 folds kept, nothing escaped |
| External links (--online) | not verified — offline |
| SVG lint | passed (4 files, 38–212 KB) |
| Light / dark / phone preview | generated at .profile-studio/preview.html |
| Design | not judged by these checks: for the owner to review |
| Real github.com page | not verified — not published |
```
