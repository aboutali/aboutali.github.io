# CLAUDE.md for aboutali.github.io

Angelo Boutalikakis's personal site. Plain hand-written HTML and stylesheets
on GitHub Pages. No build step, no frameworks, no package manager. Read
`README.md` for how the site works.

## Content rules (binding)

1. **One content source.** Every career fact on the site comes from Angelo's
   career context file ("32.02 Website context"). It is kept outside this
   public repo. If a task needs a fact that is not already on the site, ask
   Angelo for the file. Never invent facts, figures, clients, or dates.
2. **No em dashes.** Angelo bans them in all site text, titles, meta and og
   tags, alt text, JSON-LD and the feed. En dashes stay inside number and
   date ranges only. Write short declarative sentences; no dash-led or
   colon-led explanations, no "not X but Y", no filler words.
3. **Guard terms.** A list of client names and internal jargon must never
   appear in visible text. The list lives in the `GUARD_TERMS` Actions secret
   and in a git-ignored `.guard-terms` file for local runs. Never copy it
   into the repo, a commit message, or a CI log.
4. **Anonymity.** Name employers only. Describe clients by their descriptor.

`python3 scripts/check.py` enforces rules 2 and 3 plus markers, links and
HTML sanity. Run it before every commit.

## Before changing anything

- **`index.html` has four Action-owned marker regions** (`LED:*`,
  `ACTIVITY`, `GUESTBOOK`, `UPDATED`) rewritten daily by
  `.github/workflows/refresh.yml` via `scripts/generate.py`. Keep them intact.
  The project list lives in `PROJECTS` in `generate.py`; `check.py` reads it.
- **The v4 "Academic" identity is locked.** Monochrome, no accent colour.
  Newsreader and JetBrains Mono only. Components and tokens live in
  `assets/site.css`; the full spec is `brand/DESIGN_SYSTEM.md`.

## Planned work

The roadmap lives in `backlog/README.md` with execution plans in
`backlog/plans/` (read `_CONTEXT.md` first, then one plan).

## Practical notes

- Page chrome (topbar, footer) is duplicated per page by design. Change it
  everywhere: `index.html`, `about/`, `writing/`, `writing/<post>/`, `cv/`,
  `work/<slug>/`, `404.html`.
- Rendering: serve `python3 -m http.server 8642` from the repo root;
  Playwright is global (`NODE_PATH=$(npm root -g)`).
- Share cards regenerate via
  `NODE_PATH=$(npm root -g) node brand/assets/generate.cjs`.
