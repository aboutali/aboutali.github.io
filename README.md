# aboutali/aboutali.github.io

Source for [aboutali.github.io](https://aboutali.github.io/) — Angelo
Boutalikakis's personal site ("Curiosity meets rigor"): a portfolio of
projects plus About, Writing, and CV pages.

Plain hand-written HTML and CSS served straight by GitHub Pages. No build
step, no frameworks, no package manager, no client-side JavaScript. Shared
design tokens and chrome (topbar, footer, sections) live in
`assets/site.css`; page-specific rules are inlined in each page's `<head>`.
Fonts are Archivo / Newsreader / JetBrains Mono from Google Fonts.

## Pages

- `index.html` — homepage: hero, live activity ticker, the project list
  ("Work") with status dots, and a guestbook rendered from GitHub issues.
- `about/index.html` — bio, ways of working, quick facts.
- `writing/index.html` — post index; each post is a directory
  (e.g. `writing/hello-world/`). To add a post, copy an existing one,
  edit it, and add a `<li>` to the index (newest first).
- `cv/index.html` — CV with a print stylesheet (prints to a clean A4 resume).
- `404.html` — custom not-found page (uses absolute asset paths since Pages
  serves it from arbitrary URLs).
- `brand/index.html` + `brand/foundation.md` — the brand guide (see below).
- `.nojekyll` — makes Pages serve files literally, without Jekyll processing.

## Daily refresh automation

`.github/workflows/refresh.yml` runs `scripts/generate.py` (Python stdlib
only, no pip installs) on a daily schedule (06:17 UTC), on
`workflow_dispatch`, and on `issues` events. The script rewrites four
marked regions of `index.html` in place:

- `<!--LED:REPO-->…<!--/LED-->` — per-project status dot; each project's
  live URL is pinged and the dot set to `led-up` / `led-down`.
- `<!--ACTIVITY:BEGIN-->…<!--ACTIVITY:END-->` — ticker of each repo's
  latest commit message + date, from the GitHub API.
- `<!--GUESTBOOK:BEGIN-->…<!--GUESTBOOK:END-->` — entries from this repo's
  open issues labelled `guestbook` (anyone can "Sign the guestbook", which
  opens such an issue). Bodies are truncated, HTML-escaped, and reduced to
  pure ASCII before injection. Close the issue or remove the label to drop
  an entry on the next refresh.
- `<!--UPDATED:BEGIN-->…<!--UPDATED:END-->` — today's date in the footer.

Everything is best-effort: network/API failures degrade gracefully (a
project shows "down", the ticker falls back, the guestbook shows its empty
state) and never fail the build.

The workflow's publish step is race-safe: in a loop (up to 5 attempts) it
resets to the freshest `origin/main`, regenerates, commits, and pushes;
if the push is rejected because another run (e.g. an issue event) landed
first, it re-syncs and retries with backoff. Commits are authored by
`github-actions[bot]` — don't amend or rewrite them locally.

> Activity/status for **public** repos works with the default
> `GITHUB_TOKEN`. Private repos return 404 cross-repo and are simply
> skipped; to include them, add a PAT secret with `repo` scope and read it
> in the workflow.

## Adding a new project

Two edits, then commit to `main`:

1. **`scripts/generate.py`** — add the repo to the `PROJECTS` dict
   (~line 30): `"repo-slug": "https://live-url/"`. The URL is what the
   status dot pings; the slug is the GitHub repo the ticker reads commits
   from.
2. **`index.html`** — inside the `<!-- PROJECTS:BEGIN -->` /
   `<!-- PROJECTS:END -->` block (~line 132), copy an existing `<li>` and
   swap the repo slug (in **both** the LED marker and the links) and the
   text:

   ```html
   <li>
     <!--LED:REPO--><span class="led led-unknown">&#9679;</span><!--/LED-->
     <div class="p-head">
       <a class="name" href="https://aboutali.github.io/REPO/">REPO</a>
       <a class="src" href="https://github.com/aboutali/REPO">[ source ]</a>
     </div>
     <p>One-sentence description.</p>
     <div class="tags"><span>Tag</span><span>Tag</span></div>
   </li>
   ```

   Keep the LED markers exactly as shown so the daily Action can light the
   dot, and update the `NN projects` count in the section head.

Note: `aboutali.github.io/<repo>/` only resolves if that repo has GitHub
Pages enabled (Settings → Pages); until then the dot will show "down".
Off-GitHub-Pages projects work too (e.g. iKoyomi on Netlify) — the dot
pings whatever URL is in `PROJECTS`.

## Brand

`brand/foundation.md` is the written brand foundation (strategy, tagline,
personality, voice, design principles); `brand/index.html` is the visual
guide. The locked anchors: cobalt `#2C46C8` accent, Archivo type, tagline
*"Curiosity meets rigor."*

`brand/assets/` holds the generated PNGs (favicons, touch icon, avatar,
wordmarks, OG image — see `brand/assets/README.md` for the full table).
They are baked, font-independent rasters; regenerate with:

```bash
NODE_PATH=$(npm root -g) node brand/assets/generate.cjs
```

Requires Node with Playwright (Chromium) available — the script renders
each asset in headless Chromium and screenshots it.
