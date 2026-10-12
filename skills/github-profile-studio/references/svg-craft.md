# SVG craft: original, GitHub-safe artwork written as code

Read this when the design needs custom images: hero, project cards, diagrams, data visuals, footer.

## 1. Workflow

1. **Write a generator, not a file.** Put a script in the profile repo (`tools/build_assets.py`) that writes every SVG from data (a small JSON or a dict at the top). Edit the script and re-run it; never hand-edit the output. This keeps text, colours and positions consistent, makes light/dark pairs trivial, and lets the owner update a project line in a year.
2. **Use `scripts/svg_kit.py`** for escaping, width estimates, wrapping, raster embedding and the safety lint (copy it next to the generator, or import it from the skill folder).
3. **Data in, art out.** Text in the art (project names, taglines, commands) comes from the evidence ledger. If it isn't in the ledger, it doesn't go in the picture.
4. **Re-run and lint** (`python3 scripts/svg_kit.py lint assets/*.svg`), then look at it (§6).

## 2. Hard constraints (an SVG inside `<img>`)

- No `<script>`, event handlers, `<foreignObject>`, `<iframe>`, or external `href`s (images, fonts, CSS). Embed rasters as `data:` URIs.
- Fonts: system stacks only. Plan for ±10% width variation and no font fallback for rare glyphs.
- Always set `viewBox`, `width`, `height`, `role="img"` and a `<title>`. Describe the content again in the README `alt`.
- Prefix ids per component when composing several sources (gradients named `g1` will collide).
- Size budget: ≤ 300 KB per SVG is comfortable. Most of the weight comes from embedded rasters. Downscale them to 2× their displayed size, and quantize illustrations (`embed_raster(path, max_width=..., colors=8)`). Origin numbers: 3.5 MB → 52–145 KB.

## 3. Recipes (adapt, don't copy)

**Frame grammar + per-item motif.** Draw one function `frame(x, y, w, h, motif)` that renders the shared parts (rail, corner marks, index label) and calls a motif function per item. Motifs come from each item's content: a river project gets a meander line, a compiler gets a parse-tree corner, a teaching tool gets ruled notebook lines. Same stroke weight and colour roles everywhere.

**Typographic hero.** The name and positioning set large, with one structural element: a rule, an index number, a small diagram drawn from their domain. Measure with `measure()` and centre with `text-anchor="middle"`. Avoid letter-spacing tricks that depend on a specific font.

**Data-derived visual.** Built from the snapshot, honest and static:
- repo timeline: one tick per original repo at its `created_at`, lead projects labelled;
- language composition bar: labelled "bytes in public repos", never "skills";
- topic constellation: topics as nodes, repos as edges.
Write the caption so it says exactly what the data is. Regenerate when data changes; don't fake liveness.

**Interface vignette** (editor, terminal, notebook, map legend). Only when it is truly the person's medium. Show *real* content: their commands, their file names, their outputs. Syntax colour token by token (one `<tspan>` per token) rather than whole lines. Keep code ≥ 12 effective px. Remember monospace = 0.6 em per character for positioning cursors and guides, and that this is an estimate.

**Theme pair.** Generate both from one function with a palette dict:
```python
PALETTES = {"light": {"bg": "#ffffff", "ink": "#1f2328", "muted": "#59636e", "accent": "#0f766e"},
            "dark":  {"bg": "#0d1117", "ink": "#e6edf3", "muted": "#9198a1", "accent": "#5eead4"}}
for theme, p in PALETTES.items():
    build(p).write(f"assets/hero-{theme}.svg")
```
Then use the `<picture>` recipe from `github-rendering.md`.

**Calm background plates.** If a raster sits behind content: low contrast, large flat areas, the centre mostly empty (content covers it), no text, no faces, no UI. Busy plates were the first thing rejected in the origin project. Quantize when embedding.

**Real-work mosaics and figure mats.** Use `scripts/compose_images.py` (crop browser chrome first; mosaic for frames of one work; mat for figures with mixed ratios). Check the reported desktop/phone widths.

## 4. Motion (optional, opt-in)

- CSS `@keyframes` inside the SVG's `<style>`, or SMIL. Both play inside `<img>`.
- Keep it slow and small: a cursor blink, a line drawing in once, a gentle drift. Avoid infinite attention-grabbing loops near text.
- Respect `@media (prefers-reduced-motion: reduce) { * { animation: none } }`. Whether a given viewer's browser applies it inside `<img>` varies, so the static first frame must be a complete design.
- The animation must not carry information. A viewer with motion off loses nothing.

## 5. Accessibility

- `alt` says what the image communicates ("Ada Park — maps of rivers, routing engines and tiles"), not "banner".
- Don't put the only copy of important text in an image.
- Contrast ≥ 4.5:1 for text in images, against the image's own background.

## 6. Looking at the result

- Open each SVG in a browser at 100% and at the size it will appear (e.g. 880 px and 343 px wide).
- With a browser automation tool, this snippet reports text that runs outside the canvas or overlaps other text (open the SVG file directly, then evaluate):
  ```js
  (() => { const s = document.querySelector('svg'), vb = s.viewBox.baseVal, out = [];
    const ts = [...s.querySelectorAll('text')].map(t => ({t: t.textContent.slice(0, 40), b: t.getBBox()}));
    ts.forEach(({t, b}) => { if (b.x < 0 || b.y < 0 || b.x + b.width > vb.width || b.y + b.height > vb.height) out.push('outside: ' + t); });
    for (let i = 0; i < ts.length; i++) for (let j = i + 1; j < ts.length; j++) { const a = ts[i].b, c = ts[j].b;
      if (a.x < c.x + c.width && c.x < a.x + a.width && a.y < c.y + c.height && c.y < a.y + a.height) out.push('overlap: ' + ts[i].t + ' | ' + ts[j].t); }
    return out.length ? out : 'no text overflow/overlap'; })()
  ```
  Overlaps that are intentional (text on a label chip) will show too; judge each one.
- If you can view images, look for clipping, crowding and stray elements. Whether it is *beautiful* is the owner's call. Report facts and let them judge.
