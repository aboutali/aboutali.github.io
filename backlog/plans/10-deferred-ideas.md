# Plan 10 — Deferred ideas (parked; owner decision required)

**Read `_CONTEXT.md` first.** These were explicitly deferred by Angelo or need
a decision only he can make. **Do not start any of these unprompted.** Each has
just enough of a sketch that a future session can expand it into a full plan
when green-lit.

## 10a — Dark mode  *(deferred by owner 2026-07-02)*

Brand-consistent dark theme: ink surface `#17171A`→ background, paper→ text,
cobalt stays the accent (test contrast — cobalt on ink ≈ 3.2:1 → needs a
lightened dark-mode cobalt token, e.g. `#5B72E8`, verified ≥4.5:1). Implement
as `@media (prefers-color-scheme: dark)` overrides of the `:root` tokens in
`assets/site.css` + a small localStorage toggle only if Angelo wants manual
control (echo of the old site's Night Shift). Gate: owner go-ahead + accent
token decision.

## 10b — /now page  *(declined 2026-07-02 — revisit if writing habit sticks)*

`now/index.html` in the subpage template: what Angelo is focused on this
season, 3–5 bullets, `Last reviewed <date>`. Nav stays 5 links max — /now
would live in the footer, not the topbar.

## 10c — Custom domain

Needs: Angelo buying a domain + a decision on the name. Then: `CNAME` file in
repo root, DNS A/AAAA or CNAME per GitHub Pages docs, Pages settings update,
enforce HTTPS, and a sweep of every absolute `https://aboutali.github.io`
URL in the repo (canonicals, og:url, sitemap, feed, JSON-LD, README) — grep
will find them all. Old URLs keep working (Pages redirects), but update
LinkedIn afterwards.

## 10d — Privacy-first analytics

Only if Angelo wants numbers. GoatCounter (free, no cookies, EU-friendly) is
the fit: one `<script>` per page — the repo's only third-party JS, so it needs
an explicit owner OK. Alternative: zero-JS pixel via GoatCounter's image mode.
Decision needed: provider + account creation (owner does signup).

## 10e — Guestbook avatars

`scripts/generate.py` already has each issue's `user.login`; avatars are
`https://github.com/<login>.png?size=64`. Emit an `<img>` in `.gb-entry`
(fixed 32px, `loading="lazy"`, alt=""). Small, safe, cute — just needs a nod.

## 10f — Uses / colophon page  *(declined as a tab 2026-07-02)*

If revived: a footer-linked page describing the stack (hand-written HTML,
Pages, the daily Action, the brand system) — half of this text already exists
in `writing/hello-world/`. Low priority by design.

## 10g — Internationalization (DE/EL)

Only worth it if Angelo's audience needs it. Cost is real (every page ×
language, hreflang, nav duplication) and it fights the no-build ethos.
Recommendation on file: don't, unless a concrete need appears.
