# Plan 04 — Accessibility pass (WCAG 2.2 AA)

**Read `_CONTEXT.md` first.** · Effort: M (~2–3h) · Model: Opus recommended
(judgment calls on contrast/semantics) · Independent of other plans.

## Goal

Bring every page to WCAG 2.2 AA. The site already has good bones (skip link,
`:focus-visible`, `scroll-margin-top`, semantic landmarks) — this plan closes
the remaining gaps and proves it with an automated audit.

## Known gaps to fix (verified against current markup)

1. **Reduced motion.** `html{scroll-behavior:smooth}` and hover transitions
   have no `prefers-reduced-motion` guard. In `assets/site.css` add:
   ```css
   @media (prefers-reduced-motion: reduce){
     html{scroll-behavior:auto}
     *,*::before,*::after{transition-duration:.01ms !important;animation-duration:.01ms !important}
   }
   ```
2. **Contrast audit.** Check every token pair actually used (WCAG relative-
   luminance formula; write a ~30-line dependency-free python checker):
   - `--stone-soft #9B9890` on `--paper #FAF8F4` (~2.6:1) is used for `.count`,
     `.legend`, post dates, and footer rows — **fails AA** for normal text.
     Fix per-selector: switch those selectors to `--stone #6E6A60` (≈4.6:1,
     passes) where the text is ≤17px. Do NOT change the token globally —
     check each use.
   - `.tags span` (stone on paper) — verify ≥4.5:1 after the fix.
   - `.btn` paper-on-cobalt (≈6.8:1) — passes; leave.
   - Status dots (green/red on paper) are non-text indicators backed by the
     visible legend — document as 3:1 non-text, don't change hues.
3. **Status LEDs.** The dot spans carry only `title` and their inner HTML is
   owned by `scripts/generate.py` (Action rewrites it daily). Default: leave
   as-is and document the trade-off — each row's visible text stands alone.
   Optional stretch (only if you also update the seed spans in `index.html`
   and recipe R1 still passes): make `set_leds()` in `scripts/generate.py`
   emit `role="img" aria-label="online|offline"` alongside `title`.
4. **Ticker.** Has `role="region"` + `tabindex="0"` + `aria-labelledby`.
   Replace `aria-labelledby` with a direct `aria-label="Latest commits"` (one
   labelling mechanism, no id dependency) and verify keyboard scrolling works.
5. **Headings & landmarks sweep.** Exactly one `<h1>` per page; no skipped
   heading levels; nav labelled (already `aria-label="Site"`).
6. **Focus order.** Tab through each page in Playwright: skip link must be
   first focusable and must move focus to `#main`.
7. **CV `.replace` highlight** (ink on `#FFF3C4` ≈ 12:1) — passes; leave.

## Automated audit (required)

Run axe-core in Playwright on all 6 pages (`/`, `/about/`, `/writing/`,
`/writing/hello-world/`, `/cv/`, `/404.html`) at widths 390 and 1280:

```bash
curl -sL https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js -o "$SCRATCHPAD/axe.min.js"
```
```js
await page.addScriptTag({path: process.env.SCRATCHPAD + "/axe.min.js"});
const results = await page.evaluate(() => axe.run());
// zero violations with impact "serious" or "critical" allowed
```

axe stays in the scratchpad — do NOT commit it. Quote the per-page violation
counts (before → after) in the PR body.

## Constraints

- The visual character must not change materially — greys getting slightly
  darker is expected; layout, type, and the cobalt accent must not move.
- `index.html` edits → recipe **R1**. All changed pages → **R2** + **R3**.
- If the LED stretch is taken, `scripts/generate.py` must stay stdlib-only and
  `python3 -m py_compile` clean.

## Acceptance criteria

- axe: 0 serious/critical on every page at both widths; contrast script output
  shows all normal-text pairs ≥4.5:1 (or documented as large/non-text);
  reduced-motion guard active; R1/R2/R3 pass; trade-offs documented in PR body;
  backlog row 04 ✅ with date + PR#.
