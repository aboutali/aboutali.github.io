# Plan 02 — Self-host the fonts

**Read `_CONTEXT.md` first.** · Effort: M (~2h) · Model: Opus recommended
(binary asset handling + careful verification) · Independent of other plans.

## Goal

Serve Archivo, Newsreader, and JetBrains Mono from `/assets/fonts/` instead of
Google Fonts: faster first paint (no third-party round trips), no GDPR
questions, works offline, and the site keeps its "self-reliant" ethos.

## What loads today (in every page `<head>`)

Two `preconnect` links + one Google Fonts stylesheet requesting:
Archivo 400/500/600/700/800 · Newsreader ital,opsz,wght 0,6..72,400 / 1,6..72,400 /
1,6..72,500 · JetBrains Mono 400/500. (Some pages request slightly fewer weights —
unify on this superset.)

## Steps

### 1. Obtain WOFF2 files (latin subset only)

Fetch Google's CSS with a WOFF2-capable User-Agent, then download the latin
subset URLs it references:

```bash
mkdir -p assets/fonts && cd assets/fonts
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
curl -s -A "$UA" "https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400;1,6..72,500&family=JetBrains+Mono:wght@400;500&display=swap" -o gf.css
# In gf.css, keep only the /* latin */ blocks; download each src url() to a
# descriptive filename, e.g. archivo-latin-var.woff2, newsreader-italic-latin-var.woff2 …
# Delete gf.css afterwards — don't commit it.
```

Note: Archivo and Newsreader are variable fonts on Google Fonts — the CSS may
serve ONE variable file per family/style covering the whole weight range.
Prefer that (fewer files). JetBrains Mono comes as static 400/500. Expected
total: ~5–7 files, ~300–500 KB. All three are OFL-licensed — add
`assets/fonts/LICENSE-NOTE.md` naming the families, the OFL, and source URLs.

### 2. `@font-face` in `assets/site.css` (top of file)

One rule per file. For variable files use the weight range gf.css declares
(e.g. `font-weight:100 900`) — copy it exactly. Newsreader italic:
`font-style:italic`. Every rule gets `font-display:swap;` and
`src:url("fonts/<file>.woff2") format("woff2");` (site.css lives in `assets/`,
so the relative path is `fonts/…`). Copy the latin `unicode-range` from gf.css.

### 3. Update every page `<head>`

Remove the two `preconnect` lines and the Google Fonts `<link>`. Add a preload
for the Archivo file only:
`<link rel="preload" href="/assets/fonts/<archivo-file>.woff2" as="font" type="font/woff2" crossorigin>`
— root-absolute path so it works everywhere including 404.html. Files:
`index.html`, `about/index.html`, `writing/index.html`,
`writing/hello-world/index.html`, `cv/index.html`, `404.html`,
`brand/index.html` (the brand guide loads fonts too — same swap).

### 4. Keep fallback stacks

`--sans/--serif/--mono` token stacks in site.css already include system
fallbacks — leave them untouched.

## Constraints

- WOFF2 binaries are committed to the repo (no CDN, no build). That's the point.
- Confirm `git status` shows the font files staged (gitignore rules
  `brand/*.png` / `mockups/*.png` don't affect them, but verify).
- Any `index.html` edit → recipe **R1** required.

## Verification

1. Local serve + Playwright on `/`, `/cv/`, `/brand/` **with Google Fonts
   blocked** (`page.route('**fonts.g**', r => r.abort())`):
   `document.fonts.check('700 40px Archivo')`, `('italic 20px Newsreader')`,
   `('400 14px "JetBrains Mono"')` must all be true — proves self-hosting.
2. Grep: zero references to `fonts.googleapis.com` / `fonts.gstatic.com` remain
   in tracked files.
3. Recipes **R1** and **R2** (screenshots at 390/1280; the faces must look
   identical to before — compare against fresh pre-change screenshots).
4. Report total added weight in the PR body (target < 600 KB).

## Acceptance criteria

- No third-party font requests; all three families render from `/assets/fonts/`;
  OFL note present; R1/R2 pass; backlog row 02 ✅ with date + PR#.
