# CLAUDE.md — aboutali.github.io

Angelo Boutalikakis's personal site. Plain hand-written HTML/CSS on GitHub
Pages — **no build step, no frameworks, no package manager**. Read `README.md`
for how the site works.

## Before changing anything

1. **`index.html` contains four Action-owned marker regions** (`LED:*`,
   `ACTIVITY`, `GUESTBOOK`, `UPDATED`) rewritten daily by
   `.github/workflows/refresh.yml` → `scripts/generate.py`. Any edit to
   `index.html` must keep them intact — run recipe **R1** in
   `backlog/plans/_CONTEXT.md` before committing.
2. **Brand is locked** (cobalt `#2C46C8`, Archivo/Newsreader/JetBrains Mono,
   warm ink-on-paper, tagline *"Curiosity meets rigor."*). Tokens:
   `assets/site.css`. Rationale: `brand/foundation.md`. One accent; don't add
   hues.
3. **Placeholders are owner-gated** — never invent CV facts, bio details, or
   an email address to fill `[REPLACE]` / TODO markers.

## Planned work

The roadmap lives in **`backlog/README.md`** with execution-ready plans in
`backlog/plans/` (read `_CONTEXT.md` first, then exactly one plan). Verify
with the recipes it names; update the backlog status table in the same PR.

## Practical notes

- Page chrome (topbar/footer) is duplicated per page by design — change it
  everywhere: `index.html`, `about/`, `writing/`, `writing/<post>/`, `cv/`.
- Rendering: serve `python3 -m http.server 8642` from repo root; Playwright is
  global (`NODE_PATH=$(npm root -g)`); wait for Archivo via
  `document.fonts.check` with a capped timeout.
- Brand asset PNGs regenerate via
  `NODE_PATH=$(npm root -g) node brand/assets/generate.cjs`.
