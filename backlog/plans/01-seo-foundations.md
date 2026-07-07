# Plan 01 — SEO & sharing foundations

**Read `_CONTEXT.md` first.** · Effort: S (~1h) · Model: any (Sonnet fine) ·
Independent of all other plans.

## Goal

Make the site the canonical, machine-readable "Angelo Boutalikakis" result:
sitemap, robots, canonical URLs, and JSON-LD structured data. No visual changes.

## Why

The site has good per-page titles/descriptions/OG tags but no sitemap, no
robots.txt, no `rel=canonical`, and no structured data — search engines are
guessing. This is the highest SEO leverage per line of code on a static site.

## Deliverables

### 1. `sitemap.xml` (new, repo root)

List exactly these URLs (site root `https://aboutali.github.io/`):
`/`, `/about/`, `/writing/`, `/writing/hello-world/`, `/cv/`.
Standard `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`; one
`<url><loc>…</loc></url>` each. Omit `priority`/`changefreq` (ignored by Google).
Do NOT list `404.html` or `/brand/`. Add a one-line HTML comment at the top:
`<!-- When adding a page or post, add its <url> here (see backlog plan 01) -->`.

### 2. `robots.txt` (new, repo root)

```
User-agent: *
Allow: /

Sitemap: https://aboutali.github.io/sitemap.xml
```

### 3. `rel=canonical` on every page

In each `<head>`, after the `og:url`/meta block:
`<link rel="canonical" href="https://aboutali.github.io/PATH/">` with the
page's own absolute URL (home: `https://aboutali.github.io/`). Files:
`index.html`, `about/index.html`, `writing/index.html`,
`writing/hello-world/index.html`, `cv/index.html`. Also add the missing
`og:url` to the four subpages while there (home already has one) — keep it
identical to the canonical.

### 4. JSON-LD structured data

One `<script type="application/ld+json">` per page, placed before `</head>`.
Facts must come only from what's already on the pages — invent nothing.

- **Home + About** — `Person`:
  `{"@context":"https://schema.org","@type":"Person","name":"Angelo Boutalikakis",
  "url":"https://aboutali.github.io/","jobTitle":"Independent builder",
  "sameAs":["https://github.com/aboutali","https://www.linkedin.com/in/angelo-boutalikakis/"]}`
  (About page: identical object; its `url` stays the site root — it identifies
  the person, not the page.)
- **writing/hello-world/** — `BlogPosting`: headline (the `<h1>` text),
  `datePublished":"2026-07-02"`, author = the Person object (name + url),
  `mainEntityOfPage` = the canonical URL.
- **writing/index.html** — `Blog` with `name":"Writing — Angelo Boutalikakis"`
  and `author` = Person.
- **cv/** — `ProfilePage` with `mainEntity` = the same Person object.

## Constraints

- `index.html` edits touch `<head>` only — but run recipe **R1** anyway (any
  index.html edit requires it).
- Keep JSON-LD minimal and factual. No ratings, no fake organizations, no email.

## Verification

1. `python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse('sitemap.xml'); print('sitemap XML OK')"`
2. Each JSON-LD block parses: extract and `json.loads` it (write a 10-line
   python check that pulls `application/ld+json` blocks from each file via regex).
3. Recipe **R1** (marker integrity) passes.
4. Recipe **R3** (links) on changed pages.
5. `curl -s localhost:8642/robots.txt` and `/sitemap.xml` return the files when
   served locally (spot-check paths).

## Acceptance criteria

- All five pages have canonical + valid JSON-LD; sitemap + robots exist and are
  consistent with each other; R1 passes; no visual diff (no CSS/body changes).
- Backlog table row 01 set to ✅ with date + PR#.
