# Art direction: derive a look from the person, then hold it with restraint

This file is about judgment, not presets. The five directions below are starting stances. Mix them, push them, or drop them. The test for every decision: **would this design fit a different person just as well?** If yes, it is a template, and you are not done.

## 1. Method

1. **Read the person** (from the brief): their domain and material, their temperament (dry? playful? precise? warm?), their audience, their stated taste and dislikes.
2. **Find concept candidates in their actual material.** List 3, each in one line:
   - *Their medium*: a cartographer → contour lines and map legends; an ML engineer → loss curves, graphs; a type designer → specimens; a teacher → notebook, margins; a game dev → sprite sheets; a hardware hacker → schematics.
   - *Their artifacts*: screenshots, figures, renders, terminal sessions, outputs the projects really produce.
   - *Their through-line*: "inspectable systems" → things shown with their internals; "slow, careful tools" → quiet editorial layout.
   Avoid stock metaphors that fit everyone (circuit boards, matrix rain, rockets, generic "code" brackets) unless the person truly owns them.
3. **Pick one concept** and write it as one sentence: *"The page is a field notebook: each project is a numbered survey sheet."*
4. **Write the design spec** into the brief (template in `assets/brief-template.md`): concept, direction mix, grammar, palette, type, motifs, image treatment, density, motion, what is deliberately absent.
5. **Define a grammar, then vary within it.** Fix the shared rules: frame style, corner radius, rule weights, label style, numbering, image ratios. Then let each item carry its own motif from its own content. (Origin example: five project cards shared one broken outer rail and numbered label. Each card had a signature mark from its domain: page layers for a learning tool, reference brackets for a research tool, a truss for a bridge-inspection tool, nodes and a signal line for a training monitor.)
6. **Present before building, when the user is around.** Give the recommended direction with its reason and one real alternative, plus a 6–10 line wireframe. Defaults, not menus. If running unattended, choose and record why.
7. **Restraint pass** after building (see §7).

## 2. Directions

### Minimal
- **Idea:** content does all the work; typography is the only ornament.
- **Fits:** strong, specific work; people who dislike decoration; senior engineers; anyone whose taste says "quiet".
- **Moves:** an exact positioning line; generous vertical space (`<br>`, few headings); left-aligned reading text; at most one small mark (a monogram SVG, a single rule, a tiny map); project list as short prose or a definition list (`<dl>`); grey `<kbd>` links.
- **Pitfalls:** bland if the words are generic. Minimal pages need *sharper* copy, not less of it. Don't remove the one thing that makes it theirs.

### Editorial
- **Idea:** the page as a magazine spread: chapters, captions, a clear reading rhythm.
- **Fits:** writers, researchers, designers, people with a body of work and things to say.
- **Moves:** a masthead (name set large in an SVG, or a plain centered h1); numbered chapter openers; image + caption pairs (`<sub>` captions); a pull quote in `<blockquote>`; rhythm that alternates full-width and two-up; restrained palette with one accent; serif or contrasting type in the SVG art.
- **Pitfalls:** serif fonts in SVG vary by OS (use stacks, check widths); too many chapters for too little content. Three chapters is plenty for most people.

### Developer-oriented
- **Idea:** the person's real tools and outputs are the visual language.
- **Fits:** tool builders, infra, CLI and editor people, anyone whose work *is* an interface.
- **Moves:** real commands quoted from their READMEs in terminal-style art; data-derived visuals made from the snapshot (a commit-time strip, a language composition bar labelled honestly as "bytes by language in public repos"); monospace labels; diagrams of their systems (Mermaid or SVG).
- **Pitfalls:** invented terminal output, fake metrics, fake test counts (never). IDE kitsch for its own sake. Code text too small to read once scaled. Check effective px.

### Creative
- **Idea:** the image carries the message; the page is a small exhibition.
- **Fits:** artists, creative coders, motion and game people, anyone whose taste says "bold".
- **Moves:** one strong original visual: generative art seeded by their data, an illustration in their style, a mosaic of their real frames. A bolder palette. Subtle motion is allowed in SVG. Captions do the explaining.
- **Pitfalls:** illegible type over busy art; multi-MB images; art that ignores dark mode; art unrelated to the person. A busy image behind text is the classic failure. Backgrounds must be calm and mostly empty where content sits.

### Custom
- **Idea:** the user names a reference ("like a museum placard", "Swiss poster", "my blog").
- **Moves:** translate the reference into **properties**: grid, contrast, type mood, palette, density, ornament level, voice. Build those. Never copy another brand's assets, logos or exact layouts. If the reference is the user's own site, reuse its colours and marks with permission.

## 3. Colour that survives both themes

GitHub's surfaces (approximate): light page `#ffffff`, subtle `#f6f8fa`, text `#1f2328`, muted `#59636e`, border `#d1d9e0`. Dark page `#0d1117`, subtle `#151b23`, text `#e6edf3`, muted `#9198a1`, border `#3d444d`.

Three valid strategies:
1. **Theme pairs:** two SVGs via `<picture>`, same layout, palette swapped. Most polished, twice the files. Generate both from one script.
2. **Self-contained plates:** the image brings its own background, as a card with deliberate edges or rounded corners. It looks intentional on either page. The simplest robust choice for photos and illustrations.
3. **Transparent with mid-tone ink:** only for simple line art. Check contrast against both `#ffffff` and `#0d1117`.

Keep 1 accent, maybe 2, plus neutrals. Text inside images needs a contrast ratio ≥ 4.5:1. Colour lives in images: README text itself is always default or link-blue.

## 4. Type inside images

- System stacks only (`svg_kit.FONTS`). Web fonts don't load in `<img>`. If a specific typeface is essential, convert the few words to outlined paths offline and say so.
- Legibility math: `effective_px = font_px × displayed_width / viewBox_width`. Aim for **≥ 12 px** effective on desktop for any text a visitor should read. On phones the README column is ~343 px, so anything inside a half-width table cell shrinks to ~150 px. That is why essential information must also exist as HTML text.
- Estimate widths with `svg_kit.measure()` and leave 10% slack. CJK characters are ~1em wide. Avoid hairline weights. Track uppercase labels slightly.

## 5. Composition on a single GitHub column

- **Axes:** centre is for openers, hero, invitations. Left is for reading. Switching axes marks a change of section; switching randomly looks careless.
- **Rhythm:** alternate dense and open. A full-width image, then text, then a two-up row, then a fold. Avoid the same block repeated eight times. (Origin lesson: "title strip + card + sentence + fold" repeated per section felt mechanical and was rebuilt with real hierarchy.)
- **Hierarchy with native elements:** chapter = centered `<h1>` with a small `<samp>` index and `<sub>` subtitle. Item = `<h3>` + `<sub>` tagline. Label = `<kbd>`. Keep levels distinct: if chapters and items are both bold left-aligned text one size apart, the hierarchy collapses.
- **Image sets:** one aspect ratio per group. Mixed figures go on mats of a shared shape (`compose_images.py mat`). Very wide ones get their own row. Use lead + supporting mosaics only if the supporting frames stay legible. In the origin project small mosaic tiles of charts were rejected as unreadable and replaced by a full-width lead and pairs.
- **Bookends:** an ending that answers the opening (same art language, smaller) makes the page feel finished.

## 6. Emphasis economy

README text cannot be coloured. GitHub's native tags give a grey system: `<code>` grey pill (key phrases), `<kbd>` keycap (labels, numbers, link "buttons"), `<blockquote>` muted note, `<sub>` quieter secondary text, `<b>` weight. Budget: ≤ 1 emphasis per paragraph, ≤ ~6 `<code>` highlights per page. `<mark>` is yellow in both themes and usually too loud (the origin owner rejected it). Coloured alerts (`[!TIP]`) are loud too; use at most one, deliberately.

Blue link text is the loudest colour on a calm page. Options: wrap links around images or `<kbd>` labels, or accept blue and make it count by keeping only a few links.

## 7. Restraint pass (do it every time)

- Squint: is there exactly one first thing to look at?
- Count distinct visual styles (frames, badge shapes, corner radii, fonts). More than ~3 of each is noise.
- Does every image carry information or set the page's tone? If not, delete it.
- Is anything repeated? (Hero says X, intro says X, image says X.)
- Square icons and rectangular badges in one row look ragged. Separate them by row or by section.
- Would a phone visitor still get name, positioning, lead projects and contact as text?
- Is anything fake? A timeline that was never real, made-up terminal output, a mock "screenshot". In the origin project an illustrated "animation timeline" was replaced by real frames, and the result was immediately better.

## 8. Don't clone the origin

`origin-case-study.md` documents one profile (pixel-night backdrop, VS Code-style editor art, grey-only emphasis, chapter openers). Learn its **reasons**, not its look. Use editor or pixel imagery only when the person's own material leads there *and* they want it. If two different users would get similar pages from you, go back to step 2.
