# Plan 05 — Project case-study pages (×6, with real screenshots)

**Read `_CONTEXT.md` first.** · Effort: L (~4–6h) · Model: Opus recommended
(multi-page content design + image pipeline) · Best after plans 01/02; not blocked.

## Goal

Every project gets a page at `/work/<slug>/` with real screenshots, a short
narrative, and structured facts — turning the homepage list into an index of
case studies. This is the single biggest credibility upgrade available without
owner input.

## Projects (slug · live URL · status at last check)

| slug | live URL | notes |
|------|----------|-------|
| life-improver | https://aboutali.github.io/life-improver/ | up |
| bxl_eda_worker | https://aboutali.github.io/bxl_eda_worker/ | up |
| fit-schedule | https://aboutali.github.io/fit-schedule/ | down — screenshot repo README or skip imagery |
| cloudy-plag | https://aboutali.github.io/cloudy-plag/ | down — same fallback |
| edition-guru | https://aboutali.github.io/edition-guru/ | down — same fallback |
| iKoyomi | https://ikoyomi.netlify.app/ | up |

Re-check status at execution time (`curl -s -o /dev/null -w "%{http_code}"`).

## Steps

### 1. Screenshot pipeline → `work/<slug>/cover.png` (+ optional `detail.png`)

Playwright (see `_CONTEXT.md` env notes) at 1440×900, `deviceScaleFactor: 2`,
`fullPage: false` for covers (above-the-fold is the cover; a full-page shot may
be the detail). **Chromium goes through the proxy — if a target site won't load
in Chromium but curls fine, fall back to rendering the curl-fetched HTML
locally** (assets may be missing; judge whether the result is presentable —
a broken-looking screenshot is worse than none). For DOWN projects: screenshot
the GitHub repo page (`https://github.com/aboutali/<slug>`) as a fallback
cover, or use a typographic cover card (brand tokens, project name + tags) —
generate it the way `brand/assets/generate.cjs` renders cards. Keep each PNG
< 400 KB (resize to 1440w, PNG→ consider JPEG/WebP? **No** — stay PNG for
simplicity; downscale to 1200w if needed).

### 2. Page template → `work/<slug>/index.html`

Follow the existing subpage pattern exactly (copy `about/index.html`'s chrome:
head with favicons/OG/fonts/`../../assets/site.css`… wait — depth is 2, so
`../../assets/site.css`, and nav links `../../#work` etc. — mirror
`writing/hello-world/index.html`, which is the same depth).

Structure per page:
- `.page-head`: kicker `Work · NN`, `<h1><slug></h1>`, lede = the one-liner
  from the homepage list (source of truth — copy verbatim).
- Facts row (reuse About's `.facts` grid pattern): Year · Role (Concept,
  design & build) · Stack (from repo README if fetchable; else omit) ·
  Status (live/offline) · Links (Live site, Source).
- `<img>` cover: `width`/`height` attributes set, `alt` describing the screen,
  `loading="lazy"` for any image below the fold only.
- 2–4 short prose sections: What it is · How it works · Decisions & trade-offs.
  Write from *verifiable material only*: the homepage descriptions, each repo's
  README (fetch via `mcp__github__get_file_contents` or raw.githubusercontent
  curl), and what's visible in the screenshots. **No invented metrics, users,
  or outcomes.** Keep total prose ≤ 250 words/page; plain, exact voice.
- "Next project →" footer link (cycle through the six).

### 3. Wire into the site

- Homepage: each project row's `.name` currently links to the live URL. Change
  it to the case-study page (`work/<slug>/`), and add a `.src`-styled
  `[ live ]` link next to `[ source ]` pointing at the live URL. **The LED
  markers and `PROJECTS:BEGIN/END` comments must stay byte-identical** —
  only the anchors change. Run recipe **R1**.
- `sitemap.xml`: add the six URLs (if plan 01 has run).
- README "Adding a new project": add step 3 — create `work/<slug>/` from an
  existing page.

## Verification

- **R1** (homepage edit), **R2** on all six new pages + homepage (390/1280),
  **R3** links, screenshots reviewed by eye.
- Every cover image < 400 KB; total added weight reported in PR body.
- `curl` each live-URL link and source link → non-4xx (except known-down
  projects; note them).

## Acceptance criteria

- Six case-study pages live under `/work/`, on-brand, real imagery (or honest
  fallback covers), factual prose; homepage links to them; R1/R2/R3 pass;
  backlog row 05 ✅ with date + PR#.
