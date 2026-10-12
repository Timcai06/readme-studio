# Art direction: from the work to a whole-page system

This file is about judgment, not presets. Its input is the brief's **Material notes** (`material-study.md`), not a list of keywords. Its output is a **page system**: one set of shared rules that every section follows, with room for each project to look like itself.

## 1. Concept candidates are page sketches, not names

Write three candidates. Each one must be concrete enough that two designers would build roughly the same page from it:

| Field | What to write |
|---|---|
| Sources | Which material-note observations it comes from (cite them, e.g. "M2: editor/preview split", "M4: lowercase terse voice") |
| Opening | What the first screen shows and how it is composed: what is big, what is text, what is image |
| Lead vs secondary | How lead projects are shown, and how that differs from secondary ones |
| Material | Which real artefacts appear; which original assets are generated, and the job each one does (shows structure X, shows output Y, carries the identity line) |
| Rhythm | The page's sequence of layouts, e.g. full-bleed opening → two-up leads → dense list → fold → quiet close |
| Why this person | One or two sentences tying it to their work and voice |

The three must differ in **substance**: composition, what real material carries the page, how projects are treated. Three palettes for the same layout count as one candidate.

**Weak:** "Lab notebook: soft paper background, abstract waveforms inspired by signal processing, lots of white space."
**Concrete** (for a researcher who builds spectroscopy tools): "Opening: her paper's Figure 2 re-plotted from the repo's sample data at full width, under her one-sentence claim. Leads: each tool shown by its real input → output, a raw spectrum beside the cleaned one from `examples/`, with the exact CLI line between them. The dataset project as its real schema, set as a table. Talks: a dense dated list in her own terse wording. Rhythm: wide figure → two input/output pairs → schema table → list → fold."

## 2. The swap test

Replace the name and project names in your chosen candidate with another developer's. If the design still basically works, it is not specific yet. Go back to the material notes and find what only this person's work has: a real structure, real output, a real artefact, a voice. Keyword associations ("creative coding → generative shapes", "maps → contour lines", "ML → loss curve") are where swap tests fail. They point at a topic, not at this work.

Write the swap test result in the brief in one or two lines: what would break if you swapped people. "It is not a template" is not a result.

## 3. The page system

Before building, fix the shared rules and the per-item freedom.

**Shared (decide once, use everywhere):**
- *Type roles:* what carries names, what carries body, what carries labels and numbers. In SVG pick from `svg_kit.FONTS` or the person's own stack; in README text use native elements (`<h1>`/`<h3>`/`<sub>`/`<samp>`/`<kbd>`).
- *Frame:* how an image or card is bounded: edge-to-edge, rule, plate, rounded panel, none. One frame language for the page.
- *Colour jobs:* what each colour means (identity accent, per-project accent, neutral ground, data). Not just a list of hex codes.
- *Image treatment:* how real material is shown (cropped screenshots on plates, mats for figures, mosaics) and how generated assets sit next to them, so both look like one family.

**Per item (each project expresses itself):** its own real material, its own accent or motif taken from its own content, and copy in its own terms. In the origin profile, five project cards shared one frame and label system. Each carried its own project's README text, real quick-start commands and a mark from its domain.

**Layers:** give each content layer (`content-architecture.md` §2) a recognisably different treatment: identity, lead work, series/practice, related projects, deep reading. If lead and related projects look the same, the hierarchy is gone. Varying the layout between layers also creates the page's rhythm.

**Original assets have jobs.** Each generated image must show something real (a structure, an output, a relation, a timeline) or carry the identity. A generated image with no job is decoration. Count of files is not a measure of quality.

## 4. Opening and craft fidelity

**The opening is the loudest moment.** In five seconds a visitor should meet the person: name or positioning set large in the page's own art (not only a GitHub `<h1>`), in the page system's type roles, theme-paired. **Default: an animated identity opening.** The name types once and stays, and beneath it 2–4 short true lines cycle (roles, current focus, what they make, in their own wording). Generate it in the profile repo with `svg_kit.typewriter()`: no third-party service, it stops under reduced motion, and the static frame is complete. Style it in the page system (type roles, palette, frame) so it belongs to this page and isn't a stock banner. Go still only when the owner asks for stillness or their material clearly argues for it (e.g. a print-like practice), and write that reason in the brief. "Quieter" alone is not a reason.

**Finished fidelity, not sketches.** A generated asset should hold up next to a real screenshot of the work. When the concept shows an interface, code, a document, a terminal, a map or a figure, render it as that object at full detail: real content, token-level syntax colour, real structure and labels, the small details that make it read as a thing (gutters, line numbers, tabs, legends, scales, captions, layered depth). This is about *how finished* an asset is, not about any one look. An IDE treatment is right when the work is code and editors are its medium, as for many tool authors, and wrong when it isn't. A handful of boxes and arrows in a few KB is usually a diagram sketch: either finish it or replace it with real material. File size is not the goal; detail that carries real content is.

## 5. Directions are stances, not looks

Use these to talk about intent; mix them freely.

- **Minimal:** content and type do the work. Needs *sharper* copy and one exact detail. Minimal is not "fewer decisions".
- **Editorial:** chapters, captions, pull quotes, deliberate rhythm. Fits people with a body of work and things to say.
- **Developer-oriented:** the person's real interfaces, commands and outputs are the visual language. Never invent output.
- **Creative:** the image carries the message. Bold colour, dense composition and motion are allowed when the work is like that.
- **Custom:** translate a named reference into properties (grid, contrast, type mood, density, palette, voice). Never copy another brand's assets.

**Watch your own default.** Agents converge on one "safe" look: off-white paper, hairlines, a single muted accent, abstract shapes and lots of white space. That look is itself a template. Use it only when the material notes point there. Dense, loud, colourful, photographic or typographically heavy pages are equally valid when the person's work is like that.

## 6. Restraint means every element earns its place

Restraint is not low visual effort and not "fewer images". A dense page can be restrained if everything on it does a job; a sparse page can be lazy.

- In **Improve mode**, keeping the author's content and voice is a content decision. The visual scope comes from the diagnosis and the concept, not from how simple the original was. A plain original may deserve a full visual system; a rich original may deserve to keep every section and gain structure.
- Remove only what repeats, misleads or carries nothing.

## 7. Colour that survives both themes

GitHub's surfaces (approximate): light page `#ffffff`, subtle `#f6f8fa`, text `#1f2328`, muted `#59636e`, border `#d1d9e0`. Dark page `#0d1117`, subtle `#151b23`, text `#e6edf3`, muted `#9198a1`, border `#3d444d`.

Three strategies:
1. **Theme pairs** via `<picture>`: one generator, two palettes.
2. **Self-contained plates:** the image brings its own deliberate background. Robust for photos and screenshots.
3. **Transparent with mid-tone ink:** simple line art only.

Text inside images needs a contrast ratio ≥ 4.5:1. README text itself is always default or link-blue; colour lives in images.

## 8. Type inside images

- System stacks only. Web fonts don't load in `<img>`. If a typeface is essential, outline the few words offline.
- `effective_px = font_px × displayed_width / viewBox_width`. Aim for ≥ 12 px on desktop for text a visitor should read. Phones show the column at ~343 px, so essential facts also live in HTML text.
- Estimate widths with `svg_kit.measure()` and leave 10% slack. CJK is ~1em per character.

## 9. Composition on one GitHub column

- **Axes:** centre for openers, hero and invitations; left for reading. Change axis to mark a new layer, not at random.
- **Native hierarchy:** chapter, item and label must look different at a glance.
- **Image sets:** one aspect ratio per group. Use mats for mixed figures (`compose_images.py mat`). Use mosaics only if the small frames stay legible.
- **Bookends:** an ending that answers the opening makes the page feel finished.

## 10. Emphasis economy

README emphasis comes from native tags: `<code>`, `<kbd>`, `<blockquote>`, `<sub>`, `<b>`. Use about one per paragraph. `<mark>` and coloured alerts are loud: use them deliberately or not at all. Blue link text is loud too. Wrap links around images or `<kbd>`, or keep few links so the blue counts.

## 11. Quality killers

Busy images behind text. Fake terminals, fake screenshots, invented numbers. Square icons and rectangular badges in one row. Saying the same thing in the hero, the intro and the image. Abstract decoration standing in for work that has real material.

`origin-case-study.md` documents one profile. Learn why its system worked; do not reuse its pixel-night, editor-window or chapter look unless this person's material independently leads there.
