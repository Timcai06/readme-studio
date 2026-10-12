# Material study: look at the work before designing anything

Discovery (`discovery.md`) tells you what is **true**. This step tells you what the work **looks and behaves like**. These are different jobs. Reading a README finishes the first and barely starts the second: a README describes a project in words, and the page has to show it. For a project README, the project itself is the lead item.

Do this for the lead projects (and any series or practice that will get its own layer). Skip archive items.

## 1. Where the material is

Check what each lead project actually exposes in public. Typical places:

- **The running thing:** demo site, playground, docs site with live examples, gallery, app store page, hosted notebook, video or talk recording.
- **Inside the repo:** `docs/`, `assets/`, `public/`, `examples/`, `screenshots/`, `media/`, `figures/`, test fixtures, sample data, theme or design-token files, the logo, the social preview image, README images and GIFs.
- **What it produces:** real command output quoted in the README, generated files in the repo, rendered examples, figures in papers, exported sketches.
- **The person's own visual identity:** their website (colours, typefaces, layout habits are readable from its CSS), avatar, slides, previous profile, logos they made.

You may read and view this material. Don't run code from a repository you don't own just to get a picture. When the owner is present and agrees, running their own demo is fine.

If you can't view images, you can still study a lot: CSS colours and font stacks, SVG sources, image dimensions and counts, page structure, the text of examples and outputs. Record what you could not see.

## 2. What to write down

For each lead item, note the features that could change a composition. Write observations, not keywords:

| Feature | Ask | Weak note | Useful note |
|---|---|---|---|
| Form | What shapes, structures, layouts recur? | "creative coding" | "each sketch is one square canvas, black ground, a single generative system per day, numbered" |
| Colour | What colours does it really use, and where? | "colourful" | "docs use one teal accent on grey; code blocks carry the only saturated colour" |
| Density | Sparse or packed? Many small things or one big one? | "minimal" | "a utility list of 200+ small functions, each with a tiny live demo" |
| Interaction | How is it used? Typed, clicked, watched, read, printed? | "interactive" | "you write markdown and slides appear beside it; the editor/preview split *is* the product" |
| Medium | Terminal, browser, paper, video, hardware, data? | "web" | "a CLI whose whole UI is three lines of coloured output" |
| Voice | How do the person and project talk? | "friendly" | "lowercase, terse, playful names, almost no adjectives" |
| Real material | What can appear on the page as-is? | "has screenshots" | "4 docs screenshots usable; demo GIF too heavy; 12 exported sketches under MIT" |

Also note what is **missing**. "No screenshots, but the README has a 20-line config example and a diagram of the plugin pipeline" is a material finding.

## 3. When there are no screenshots

No screenshots does not mean "use geometric decoration". Build the visual from the work's real structure or content:

- **Structure:** module graph from the repo's real imports or package list; plugin pipeline as the README describes it; a file tree; an API surface; the sections of a paper.
- **Content:** real command, real input → output pair, real config, real data file plotted honestly, real figure re-set, real error message the tool catches, real example the docs use.
- **Process and time:** release history, the days of a daily practice, the chapters of a learning log, the stages of a pipeline. Use real dates and counts only.
- **Voice:** the person's own words, set typographically, can carry a page with no picture at all.

Each of these is specific to this person by construction. A field of abstract shapes "inspired by" a project name is not.

## 4. How much is enough

Enough material means you can say, for each lead item, what a visitor would see and why it could only be this project. The aim is not a quota of screenshots: one well-chosen real artefact or one faithful structural drawing per lead item is often plenty. A text-led page is a valid outcome only when the material study shows the work is truly best expressed in words (an essay collection, a spec, a poem generator whose output *is* text set well). Say why in the brief. "It's small" is not that reason: small projects with real output usually have one strong figure in them.

Record the study in the brief's **Material notes** table, then go to concepts (`art-direction.md`). Anything you mark **usable** is a commitment: later steps either place it or record why it was dropped.
