# Plan 11: Accessibility re-audit of the v4 design

Read `CLAUDE.md` and `_CONTEXT.md` first. Effort: M. Model: Sonnet is fine.

## Goal
Bring every page of the v4 "Academic" design to WCAG 2.2 AA. Plan 04 audited
the v3 design; v4 replaced the stylesheet and markup and was never audited.

## Known finding
`.gb-date` (guestbook entry dates, emitted by `scripts/generate.py`) uses
`--muted` #888888 on white: 3.54:1, below the 4.5:1 minimum for small text.
The status circles also use `--muted`, but they are non-text symbols (3:1
applies) and carry `role="img"` with an `aria-label`.

## Steps
1. Run axe-core (cdnjs `axe-core/4.10.2/axe.min.js`, kept in the scratchpad,
   never committed) with Playwright on every page at 390 and 1280 px:
   `/`, `/about/`, `/writing/`, `/writing/hello-world/`, `/cv/`, all six
   `/work/<slug>/`, `/404.html`. Record serious and critical violations.
2. Compute contrast for every text colour token actually used as text
   (`--ink`, `--ink-2`, `--graphite`, `--muted`, any literal greys in
   page-local CSS such as `#222`) on `--paper` and on `--desk`.
3. Fix: text below 4.5:1 moves to `--graphite` (7.46:1) or darker. Keep the
   monochrome identity; add no colours. Prefer token changes per selector over
   changing `--muted` globally, since the status circles rely on it.
4. Keyboard pass: the skip link is the first tab stop and moves focus to
   `#main`; every link and button shows the focus outline; the ticker scrolls
   with the keyboard.
5. Reduced motion: smooth scroll is off under `prefers-reduced-motion`.
6. If `assets/site.css` changes, bump `site.css?v=N` on every page AND
   `STYLE_VERSION` in `scripts/build_posts.py`, then run
   `python3 scripts/build_posts.py` so the post pages pick it up.

## Acceptance
Zero serious or critical axe violations on every page at both widths; every
text pair at or above 4.5:1 (or documented as large or non-text);
`python3 scripts/check.py` passes; no visual change beyond darker greys.
