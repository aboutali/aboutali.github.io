# Plan 03 — RSS feed for Writing

**Read `_CONTEXT.md` first.** · Effort: S (~1h) · Model: any (Sonnet fine) ·
Best done after plan 01 (canonical URLs), but not blocked by it.

## Goal

A subscribable Atom feed at `/writing/feed.xml`, hand-maintained like the rest
of the site (no generator — a new post means adding one `<entry>`, same as the
post index gets one `<li>`).

## Deliverables

### 1. `writing/feed.xml` (new)

Atom 1.0 (better-specified than RSS 2.0 and equally supported):

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- When adding a post: copy an <entry>, update id/title/updated/link/summary,
     and bump the feed-level <updated>. Keep entries newest-first. -->
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Writing — Angelo Boutalikakis</title>
  <subtitle>Curiosity meets rigor.</subtitle>
  <link href="https://aboutali.github.io/writing/feed.xml" rel="self"/>
  <link href="https://aboutali.github.io/writing/"/>
  <id>https://aboutali.github.io/writing/</id>
  <updated>2026-07-02T00:00:00Z</updated>
  <author><name>Angelo Boutalikakis</name><uri>https://aboutali.github.io/</uri></author>
  <entry>
    <title>Hello, world — what this site is</title>
    <link href="https://aboutali.github.io/writing/hello-world/"/>
    <id>https://aboutali.github.io/writing/hello-world/</id>
    <updated>2026-07-02T00:00:00Z</updated>
    <summary>Why this site exists, how it's built (no frameworks, no build step),
    and what "curiosity meets rigor" means in practice.</summary>
  </entry>
</feed>
```

Use the real post title/summary from `writing/index.html` (source of truth) —
if more posts exist by execution time, include them all, newest first.

### 2. Feed discovery + visible link

- In `writing/index.html` `<head>`:
  `<link rel="alternate" type="application/atom+xml" title="Writing — Angelo Boutalikakis" href="/writing/feed.xml">`
  (also add the same line to `index.html` `<head>` — feed readers often check
  the site root; that edit then requires recipe **R1**).
- In `writing/index.html`, add a small RSS link in the page (e.g. next to the
  `.page-head .lede` or as a mono-styled link under the post list):
  `<a class="feed-link" href="feed.xml">RSS feed →</a>` styled with existing
  tokens (mono, 13px, stone → cobalt on hover). Keep it subtle.

### 3. Document the ritual

In `README.md`, the "Pages" section describes adding a post — extend that
sentence: "…add a `<li>` to the index (newest first), **add an `<entry>` to
`writing/feed.xml`, and add the post URL to `sitemap.xml`**" (sitemap exists if
plan 01 ran; otherwise omit that clause).

## Verification

1. `python3 -c "import xml.dom.minidom; xml.dom.minidom.parse('writing/feed.xml'); print('feed XML OK')"`
2. Entry `<id>`s equal the canonical post URLs; feed `<updated>` ≥ newest entry.
3. Recipes **R1** (index.html head edit), **R2** on `writing/` (the visible link),
   **R3**.

## Acceptance criteria

- Valid Atom feed with all current posts; discovery links on home + writing
  index; visible RSS link on the writing page; README ritual updated; backlog
  row 03 ✅.
