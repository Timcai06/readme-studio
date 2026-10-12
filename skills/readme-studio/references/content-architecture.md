# Content architecture (profiles): what to show, in what order, at what density

For project READMEs, the reader and order differ: see `project-readme.md` §1. §4 (copy), §5 (folds) and §6 (cutting) below apply to both.

Output of this stage: a section plan in the brief. It lists each section's job, what goes in it, what is visible and what is folded, and a cut list.

## 1. Design for three reading speeds

| Speed | The visitor wants | Must be answered by |
|---|---|---|
| 5 seconds | Who is this, and what do they do? | The first screen: name/positioning + one concrete line. No scrolling, no folds. |
| 30 seconds | Is there proof? | Lead projects with a sentence each and a way in (link). |
| 3 minutes | Depth, range, personality, how to reach them | Featured work, practice/series, capabilities, archive in folds, contact. |

If the 5-second answer needs the visitor to read a paragraph, the opening is wrong.

## 2. Default reading order, and when to change it

`identity → proof (lead work) → distinctive practice → capabilities → archive → invitation/contact`

- **Identity**: one positioning line, and optionally one short paragraph. The person's own words where possible.
- **Proof**: 1–2 lead projects, then 2–4 featured. This is the heart of the page.
- **Distinctive practice** (optional): a series, research line, teaching, writing or art practice that isn't "a project". It gets its own layer. Do not mix it into the tool list. (Origin lesson: a music-video series was framed as a series first, with each work beneath it.)
- **Capabilities**: what they work with, *grouped by purpose* ("data & backend"), not a single logo wall. Short. Derived from projects or confirmed by the user.
- **Archive**: everything else worth keeping, folded, one line each.
- **Invitation**: what kind of contact is welcome and how. It closes the page and can mirror the opening visually.

These are **layers**, and each layer gets its own visual treatment in the page system (`art-direction.md` §3). Identity, lead work, series/practice, related projects and deep reading (folds) should be told apart at a glance. Lead work gets the strongest real material. Related projects are connected to the leads, not repeated in the same format.

Change the order when the purpose demands it: a job-seeker may put a one-line "currently open to …" in Identity. A researcher may put publications before projects. An artist may lead with the work image and keep words minimal.

## 3. Choosing and ranking projects

Score candidates (from the ledger) on:
1. **Owner's priority.** If they named it, it leads. This beats every metric.
2. **Fit with the through-line.** It shows what this person is about.
3. **Demonstrability.** It has a README, a demo, screenshots or a clear purpose a stranger can grasp.
4. **Substance.** Real scope and real authorship, not a tutorial clone.
5. **Recency and life.** Maintained or recently finished.
6. **Attention** (stars, users). A tie-breaker only.

Tiers:
- **Lead (1–2):** the largest treatment: image, two to three sentences, key facts, link.
- **Featured (2–4):** a smaller but consistent treatment.
- **Archive (any):** in a fold. Name, a few words of description, link.
- **Omit:** forks without contribution, empty repos, homework the user doesn't care about, anything the user wants hidden.

More than ~6 visible projects means the page has no lead. Ten projects of equal weight read as a pinned-repo list, which GitHub already shows.

## 4. Writing project copy

Formula: **name → what it is for (whose problem) → the one distinctive how → way in.**

- Good: "PulseGraph — a local-first workbench for watching PyTorch training: model graph, metrics, checkpoints and inference replay in one place."
- Weak: "An awesome, powerful ML tool built with modern technologies."

Rules: concrete nouns over adjectives. No "passionate", "cutting-edge", "seamless". One distinctive technical fact beats five generic ones. Keep the user's terminology. Match the language of the page. Emphasis goes on at most one phrase per project.

Stack chips or badges per project (when used): only what the repo shows (language stats, dependency files, README). 4–7 per project is the readable range. The shapes must be consistent.

## 5. Density and folds

- **Never fold identity.** The intro, positioning and lead work are always visible. In the origin project the owner asked for the bilingual intro to come *out* of a fold.
- Fold **archives and depth**: other projects, figures, long lists. Each fold's `<summary>` says what is inside and how much ("11 smaller projects: CLIs, course work").
- Avoid fold-inside-fold. One deliberate exception is fine, e.g. an "archive" fold containing per-item folds, if the owner wants it.
- Never put `<details>` inside table cells (renders inconsistently).
- Visual density does not equal information value. Every image must carry information or set the tone of the whole page. Decoration that repeats text above it is noise.

## 6. Cut, but cut the right thing

Cut:
- Anything GitHub already shows next to the README: avatar, follower counts, pinned list, contribution graph. Keep it only if your version adds narrative.
- Repetition between hero, intro and image. Say each thing once. In the origin project, a heading and a paragraph were accidentally duplicated between the hero and the intro; the owner spotted it at once.
- Generic sections: "Fun fact", "Ask me about anything", quote-of-the-day APIs, unless they are true to the person.
- Template defaults with no information (see the table in `github-rendering.md` §6).

Do **not** cut substance to fake minimalism. In the origin project the owner explicitly said not to keep deleting copy just to make the page feel clean. Move depth into folds instead.

## 7. Special cases

- **Newcomer, little history:** be honest and small. Positioning as a learner is fine: "Learning systems programming; currently building X". Show 1–2 projects with *what was learned or decided*, not inflated claims. No skill bars, no "expert". Short is fine, but short is not low-effort: the few things shown still get a real visual treatment from their actual work (the learning log's real chapters, the tool's real output).
- **Many repos (30+):** group by theme ("Geospatial", "Developer tools") and lead with 2. Aggregate claims only when verified ("maintains 4 published crates" means you checked 4).
- **Bilingual pages:** choose the primary language by audience. Keep both visible if they are part of identity. Two short parallel paragraphs read better than interleaved lines. Make sure each claim says the same thing in both languages.
- **Private / unreleased work:** name and one line. Status `in progress` where true. No links. Images only if the user supplies and approves them, cropped of browser chrome, URLs and personal data.
- **Improve mode:** the existing content is the owner's voice. Keep their phrasing and important links unless they are wrong. Restructure before you rewrite. Content kept is not a limit on the visual work: a page that keeps every original word can still gain a complete visual system.
