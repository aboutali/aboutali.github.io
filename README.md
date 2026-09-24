# aboutali/aboutali.github.io

Source for [www.boutalikakis.com](https://www.boutalikakis.com/), the personal
site of Dr. Angelo Boutalikakis. It holds a portfolio of projects plus About,
Writing (research, publications, talks), and CV pages. All career facts come
from Angelo's career context file; see `CLAUDE.md` for the content rules.

Plain hand-written HTML and CSS served straight by GitHub Pages. No build
step, no frameworks, no package manager, no client-side JavaScript. Shared
design tokens and chrome (running head, sections, footer) live in
`assets/site.css`; page-specific rules are inlined in each page's `<head>`.
Fonts are Newsreader and JetBrains Mono, self-hosted from `assets/fonts/`.

## Pages

- `index.html`: homepage, with hero, live activity ticker, the project list
  ("Work") with status dots, and a guestbook rendered from GitHub issues.
- `about/index.html`: bio, ways of working, quick facts.
- `work/<slug>/index.html`: a case-study page per project (real screenshot or
  a typographic fallback cover, facts row, short prose). Linked from each
  project's `.name` on the homepage; cycle through them with "Next project →".
- `writing/index.html`: post index. Each post is a directory
  (e.g. `writing/hello-world/`). To add a post, copy an existing one, edit
  it, add a `<li>` to the index (newest first), add an `<entry>` to
  `writing/feed.xml`, and add the post URL to `sitemap.xml`.
- `cv/index.html`: CV with a print stylesheet (prints to a clean A4 resume).
- `404.html`: custom not-found page (uses absolute asset paths since Pages
  serves it from arbitrary URLs).
- `brand/foundation.md` and `brand/DESIGN_SYSTEM.md`: the v4 brand and
  design system notes.
- `.nojekyll`: makes Pages serve files literally, without Jekyll processing.

## Daily refresh automation

`.github/workflows/refresh.yml` runs `scripts/generate.py` (Python stdlib
only, no pip installs) on a daily schedule (06:17 UTC), on
`workflow_dispatch`, and on `issues` events. The script rewrites four
marked regions of `index.html` in place:

- `<!--LED:REPO-->…<!--/LED-->`: per-project status dot. Each project's
  live URL is pinged and the dot set to `led-up` / `led-down`.
- `<!--ACTIVITY:BEGIN-->…<!--ACTIVITY:END-->`: ticker of each repo's
  latest commit message + date, from the GitHub API.
- `<!--GUESTBOOK:BEGIN-->…<!--GUESTBOOK:END-->`: entries from this repo's
  open issues labelled `guestbook` (anyone can "Sign the guestbook", which
  opens such an issue). Bodies are truncated, HTML-escaped, and reduced to
  pure ASCII before injection. Close the issue or remove the label to drop
  an entry on the next refresh.
- `<!--UPDATED:BEGIN-->…<!--UPDATED:END-->`: today's date in the footer.

Everything is best-effort: network/API failures degrade gracefully (a
project shows "down", the ticker falls back, the guestbook shows its empty
state) and never fail the build.

The workflow's publish step is race-safe: in a loop (up to 5 attempts) it
resets to the freshest `origin/main`, regenerates, commits, and pushes;
if the push is rejected because another run (e.g. an issue event) landed
first, it re-syncs and retries with backoff. Commits are authored by
`github-actions[bot]`. Don't amend or rewrite them locally.

> Activity/status for **public** repos works with the default
> `GITHUB_TOKEN`. Private repos return 404 cross-repo and are simply
> skipped; to include them, add a PAT secret with `repo` scope and read it
> in the workflow.

### Deploy verification

`.github/workflows/verify-deploy.yml` guards against a stalled or partial
Pages deploy (this happened once: a queued build timed out and the site
served stale content for 10 minutes with no signal). It runs on every push
to `main`, daily, and on demand: it polls the Pages Builds API until the
latest build matches the pushed commit and is `built`, then checks that
`/`, `/about/`, `/writing/`, and `/cv/` all return 200. If that doesn't
happen in time, it requests a fresh Pages build and re-polls once before
failing. **A red run means the live site may be stale or broken.** Check
the Actions log; if it couldn't self-heal (403/404 on the rebuild request),
re-run the deploy manually from the Actions tab.

### Checks

`.github/workflows/checks.yml` runs `scripts/check.py` (stdlib only) on
every pull request and on push to `main`: it gates Action-marker integrity,
internal links, basic HTML sanity (one `<h1>`, a `<title>`, `lang`, `alt`,
no duplicate ids), and sitemap/feed XML validity. Run it locally before
pushing with `python3 scripts/check.py`.

## Adding a new project

Two edits, then commit to `main`:

1. **`scripts/generate.py`**: add the repo to the `PROJECTS` dict
   (~line 30): `"repo-slug": "https://live-url/"`. The URL is what the
   status dot pings; the slug is the GitHub repo the ticker reads commits
   from.
2. **`index.html`**: inside the `<!-- PROJECTS:BEGIN -->` /
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
   dot, and update the `NN projects` count in the section head. The `.name`
   link should point at the project's case-study page (`work/REPO/`, see next
   step); add a `.src`-styled `[ live ]` link next to `[ source ]` for the
   actual live URL.
3. **`work/REPO/`**: create the case-study page. Copy an existing one (e.g.
   `work/life-improver/`), swap the slug, facts, prose, and `cover.png`, and
   fix the "Next project →" links on this page and its neighbors so the cycle
   stays intact. Add the page to `sitemap.xml`.

Note: `aboutali.github.io/<repo>/` (which redirects to
`www.boutalikakis.com/<repo>/`) only resolves if that repo has GitHub
Pages enabled (Settings → Pages); until then the dot will show "down".
Projects hosted elsewhere work too. The dot pings whatever URL is in
`PROJECTS` (gesundheit-mcp points at its Cloud Run endpoint, which counts as
up on any status below 500).

## Brand

The site uses the v4 "Academic" identity: monochrome (ink `#141414` on
white), Newsreader for text, JetBrains Mono for project names and data,
no accent colour, no icons or logo mark. Full spec in
`brand/DESIGN_SYSTEM.md`; short summary in `brand/foundation.md`.

`brand/assets/` holds the generated PNGs (favicons, touch icon, avatar,
wordmarks, OG image, see `brand/assets/README.md` for the full table).
They are baked, font-independent rasters; regenerate with:

```bash
NODE_PATH=$(npm root -g) node brand/assets/generate.cjs
```

Requires Node with Playwright (Chromium) available. The script renders
each asset in headless Chromium and screenshots it.

## Custom domain

The site is served at `www.boutalikakis.com` (the `CNAME` file; apex
`boutalikakis.com` and `aboutali.github.io` redirect there). DNS lives at
Squarespace: four A records on `@` for GitHub Pages and a `www` CNAME to
`aboutali.github.io`. The iCloud Mail records (MX, TXT, DKIM) must stay
untouched. Absolute URLs in canonicals, og tags, JSON-LD, the sitemap and the
feed use `https://www.boutalikakis.com/`.
