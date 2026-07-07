# Site backlog — aboutali.github.io

What an ideal personal website looks like for Angelo, and the ordered work to
get there. Each item links to an execution-ready plan in `plans/` written so
that Claude (Opus or a smaller model) can pick it up cold — **every executor
must read [`plans/_CONTEXT.md`](plans/_CONTEXT.md) first.**

## The ideal (what we're building toward)

A personal site that is:

1. **Credible in 10 seconds** — a visitor (recruiter, collaborator, peer)
   immediately understands who Angelo is, what he's built, and how to reach him.
   Real CV, real bio, real screenshots — zero placeholders.
2. **The canonical "Angelo Boutalikakis" result** — ranks for his name, previews
   beautifully when shared, is machine-readable (structured data), and
   subscribable (RSS).
3. **Fast and self-reliant** — loads in one round trip, no third-party
   render-blocking dependencies, Lighthouse ≳95 across the board.
4. **Usable by everyone** — WCAG 2.2 AA; keyboard, screen-reader, and
   reduced-motion friendly.
5. **Alive without labor** — the daily automation keeps status/activity/guestbook
   fresh; CI guards regressions; deploys verify themselves (a Pages queue-timeout
   already bit us once — see plan 06).
6. **Depth on demand** — each project has a case-study page with real imagery;
   writing accumulates into a body of thought.

Principles it must never lose: no build step, one cobalt accent, the work is the
hero, curiosity meets rigor.

## Status snapshot (2026-07-07)

Live: brand system v3 · homepage (live ticker, status dots, guestbook) · About ·
Writing (1 post) · CV (structure + print CSS) · 404 · daily refresh Action ·
favicons/OG assets. Known gaps: CV/About placeholders, no per-project pages, no
sitemap/RSS/structured data, Google-Fonts render dependency, no CI checks, no
deploy self-verification, no email address published.

## Backlog

**P0 — credibility (owner-gated content)**

| # | Item | Plan | Status |
|---|------|------|--------|
| 09 | Fill CV Experience/Education + personalize About bio | [plans/09-cv-and-about-completion.md](plans/09-cv-and-about-completion.md) | ⏸ blocked on owner input |
| — | Publish an email address (footer TODOs mark the spots) | (part of 09) | ⏸ blocked on owner |

**P1 — technical foundation (fully executable now)**

| # | Item | Plan | Status |
|---|------|------|--------|
| 01 | SEO & sharing foundations: sitemap, robots, canonicals, JSON-LD | [plans/01-seo-foundations.md](plans/01-seo-foundations.md) | ☐ ready |
| 02 | Self-host fonts (drop Google Fonts dependency) | [plans/02-self-hosted-fonts.md](plans/02-self-hosted-fonts.md) | ☐ ready |
| 04 | Accessibility pass to WCAG 2.2 AA | [plans/04-accessibility-pass.md](plans/04-accessibility-pass.md) | ☐ ready |
| 06 | Deploy self-verification workflow (Pages queue-timeout guard) | [plans/06-deploy-verification.md](plans/06-deploy-verification.md) | ☐ ready |

**P2 — depth & durability (fully executable now)**

| # | Item | Plan | Status |
|---|------|------|--------|
| 05 | Project case-study pages with real screenshots (×6) | [plans/05-project-case-studies.md](plans/05-project-case-studies.md) | ☐ ready |
| 03 | RSS feed for Writing | [plans/03-rss-feed.md](plans/03-rss-feed.md) | ☐ ready |
| 07 | CI quality gates on PRs (links, markers, HTML sanity) | [plans/07-ci-quality-gates.md](plans/07-ci-quality-gates.md) | ☐ ready |
| 08 | Per-page OG images | [plans/08-og-images-per-page.md](plans/08-og-images-per-page.md) | ☐ ready |

**P3 — deferred / owner decisions** — see [plans/10-deferred-ideas.md](plans/10-deferred-ideas.md)
(dark mode, Now page, custom domain, privacy-first analytics, guestbook avatars,
uses/colophon page, i18n). Each was either explicitly deferred by Angelo or needs
a decision only he can make. Do not start these unprompted.

## Suggested execution order

`01 → 02 → 04 → 06` (foundation, each independent, small) · then `05` (the big
content win) · then `03 → 08 → 07`. Item 09 whenever Angelo supplies content —
it jumps the queue when he does. One plan per branch/PR; don't batch.

## Working agreement for executor models

- Read `plans/_CONTEXT.md`, then the one plan you're executing. Plans are
  self-contained by design; don't improvise scope.
- Verify with the recipes the plan names (R1–R4 in `_CONTEXT.md`) before
  declaring done. Look at your screenshots.
- Update this table's Status column (☐ ready → ✅ done, with date + PR#) in the
  same PR as the work.
- If a plan conflicts with reality (file moved, markup drifted), the invariants
  in `_CONTEXT.md` win; adapt the plan minimally and note the deviation in the
  PR body.
