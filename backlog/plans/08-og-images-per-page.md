# Plan 08 — Per-page OG images

**Read `_CONTEXT.md` first.** · Effort: S–M (~1–2h) · Model: any (Sonnet fine) ·
Requires: none (better after plan 05 exists, to cover /work/ pages too).

## Goal

Each section shares with its own branded card instead of the one generic
`og-image.png`: About, Writing (+ per-post), CV. Same identity, per-page
context line — links previewed in Slack/LinkedIn/iMessage look deliberate.

## How

Extend the existing generator — `brand/assets/generate.cjs` already renders
1200×630 cards in headless Chromium with the brand fonts baked in (see its
`og()` function and the `JOBS` table; run with
`NODE_PATH=$(npm root -g) node brand/assets/generate.cjs`).

### 1. Generalize `og()` → `ogCard(kicker, line2serif)`

Parameterize the two text slots of the existing card (keep layout identical):
- kicker (mono, uppercase): e.g. `ANGELO BOUTALIKAKIS — ABOUT`
- bottom-left serif italic line: per-page context.

Wordmark block stays exactly as-is. Add to `JOBS`:

| file | kicker | serif line |
|------|--------|-----------|
| `og-about.png` | …— ABOUT | A curious mind that ships. |
| `og-writing.png` | …— WRITING | Notes on building small things. |
| `og-cv.png` | …— CURRICULUM VITAE | Curiosity meets rigor. |
| `og-post-hello-world.png` | …— WRITING | Hello, world — what this site is |

(If `/work/` case studies exist by execution time, add `og-work-<slug>.png`
with the project one-liner — check first.)

Keep the base `og-image.png` untouched for the homepage.

### 2. Regenerate & wire up

Run the generator (it re-renders ALL assets — that's fine, they're
deterministic; `git diff` should show only new files unless fonts drifted —
if existing PNGs churn with no visual change, restore them and only add the
new ones). Then point each page's `og:image` (and add
`og:image:width/height` 1200/630 + `twitter:card` where missing) at its card,
absolute URLs: `https://aboutali.github.io/brand/assets/og-<page>.png`.

Files: `about/index.html`, `writing/index.html`,
`writing/hello-world/index.html`, `cv/index.html`. Homepage unchanged.

### 3. Document

Add the new files to the table in `brand/assets/README.md`.

## Constraints

- The card layout/brand must not drift — same template, only text differs.
- Each PNG ≤ ~150 KB (the current og-image.png is ~100 KB — flag if far off).
- Wait for `document.fonts.check('700 40px Archivo')` before screenshotting
  (the generator does this — don't regress it; serif line needs Newsreader
  loaded too).

## Verification

- Read every generated PNG and LOOK at it: correct kicker, correct serif line,
  no fallback serif in the wordmark (Archivo must render — compare letterforms
  against the existing og-image.png).
- Recipe **R3** on changed pages; grep confirms every `og:image` URL maps to a
  committed file.

## Acceptance criteria

- 4+ per-page cards generated, on-brand, wired into page heads with correct
  dimensions meta; assets README updated; backlog row 08 ✅ with date + PR#.
