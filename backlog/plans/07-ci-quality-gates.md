# Plan 07 — CI quality gates on pull requests

**Read `_CONTEXT.md` first.** · Effort: M (~2h) · Model: any (Sonnet fine) ·
Best after plans 01/03 exist (they add files worth checking); not blocked.

## Goal

A PR check that catches the regressions most likely to slip in: broken Action
markers, broken internal links, invalid XML (sitemap/feed), and malformed HTML.
Everything the executor models verify by hand today, mechanized.

## Deliverables

### 1. `scripts/check.py` (new — stdlib only, no pip installs)

One script, exit non-zero on any failure, clear per-check output. Checks:

1. **Marker integrity + rewrite simulation** — exactly recipe R1 from
   `_CONTEXT.md`: all four marker types present in `index.html`; import
   `scripts/generate.py` with stubbed `is_up`/`latest_commit`/`gh_api`, run all
   four `set_*` functions, assert markers survive and stub content lands.
2. **Internal links** — walk every tracked `*.html`; for each `href`/`src`
   that is not `http(s):`, `mailto:`, or `#...`: resolve root-absolute paths
   from repo root, relative paths from the file's directory; assert the target
   file exists (directory links resolve to `<dir>/index.html`). Use
   `html.parser.HTMLParser` (stdlib) — not regex.
3. **HTML sanity** — stdlib HTMLParser pass per file: every page has exactly
   one `<h1>`, a `<title>`, `lang` on `<html>`, `alt=` present on every
   `<img>`, and no duplicate `id` attributes.
4. **XML validity** — `xml.dom.minidom.parse` on `sitemap.xml` and
   `writing/feed.xml` when they exist (skip silently if absent so the check
   works before plans 01/03 merge).
5. **generate.py compiles** — `py_compile` it.

### 2. `.github/workflows/checks.yml` (new)

```yaml
name: Checks
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v6
        with: {python-version: '3.x'}
      - run: python3 scripts/check.py
```

Note the refresh workflow's bot commits to `main` will also run this on push —
that's desirable (a bad injection would surface immediately) and safe (checks
are read-only).

### 3. README

Add 3 lines under the automation section: what `checks.yml` gates and how to
run `python3 scripts/check.py` locally before pushing.

## Constraints

- Stdlib only; no external actions beyond checkout/setup-python (matches
  refresh.yml's dependency posture).
- The script must pass against the CURRENT repo state before you add the
  workflow — if a check fails on existing content, fix the content in the same
  PR (e.g. a missing `alt`) and say so in the PR body.

## Verification

- `python3 scripts/check.py` exits 0 locally with all checks reporting PASS.
- Break something deliberately in a scratch copy (delete an LED marker, point
  a link at a missing file) and confirm the script exits non-zero with a
  readable message for each case. Quote this negative test in the PR body.
- Workflow YAML parses.

## Acceptance criteria

- `scripts/check.py` + `checks.yml` merged; local run green; negative tests
  demonstrated; README updated; backlog row 07 ✅ with date + PR#.
