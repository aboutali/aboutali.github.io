# Site backlog for www.boutalikakis.com

The ordered work for Angelo's personal site. Executable items link to a plan in
`plans/` that a fresh Claude session can pick up cold. Every executor reads
[`plans/_CONTEXT.md`](plans/_CONTEXT.md) and the repo's `CLAUDE.md` first.

## What the site is for

1. **Credible in ten seconds.** A recruiter, collaborator or peer sees who
   Angelo is, what he has built, and how to reach him.
2. **The canonical result for his name.** Ranks for "Angelo Boutalikakis",
   previews well when shared, and is machine-readable.
3. **Fast and self-reliant.** Hand-written HTML and CSS, self-hosted fonts, no
   third-party scripts.
4. **Usable by everyone.** WCAG 2.2 AA on every page.
5. **Alive without labor.** The daily Action keeps status, activity and
   guestbook fresh; CI guards regressions; deploys verify themselves.

Binding rules live in `CLAUDE.md`: one content source (the career context
file), no em dashes, guard terms, sector-and-theme level of detail, and the
locked v4 "Academic" identity (`brand/DESIGN_SYSTEM.md`).

## Status snapshot (2026-10-02)

Live at www.boutalikakis.com (apex and aboutali.github.io redirect there):
v4 Academic design on every page, homepage with project table and live status,
About with a quick-facts margin column, Writing with publications and talks,
CV with portrait and a PDF export, six project pages, Markdown post pipeline
(`content/writing/`, `scripts/build_posts.py`), daily refresh Action, CI checks
(markers, links, HTML sanity, XML, em dashes, guard terms), deploy
verification.

## Round 2 (opened 2026-10-02)

**Technical, executable now**

| # | Item | Plan | Status |
|---|------|------|--------|
| 11 | Accessibility re-audit of the v4 design | [plans/11-v4-accessibility-audit.md](plans/11-v4-accessibility-audit.md) | ☐ in progress |
| 12 | Rebuild the CV PDF automatically when the CV changes | [plans/12-cv-pdf-automation.md](plans/12-cv-pdf-automation.md) | ☐ in progress |
| 13 | Offline projects: drop dead live and source links | [plans/13-offline-project-links.md](plans/13-offline-project-links.md) | ☐ in progress |
| 14 | Publications as structured data on the Writing page | [plans/14-publication-structured-data.md](plans/14-publication-structured-data.md) | ☐ in progress |
| 15 | Refresh this backlog (status, stale entries) | this file | ✅ 2026-10-02 |

**Content, needs Angelo**

| # | Item | Needs | Status |
|---|------|-------|--------|
| 16 | First real notes (theme: applied AI in regulated industries) | drafts; write them as Markdown in `content/writing/` | ⏸ owner |
| 17 | gesundheit-mcp page: add tests, eval metric, README, walkthroughs as they ship; source link once public | each shipped item | ⏸ owner |
| 18 | Guest lecture: slides or abstract after the winter term 2026/27 lecture | material | ⏸ owner |
| 19 | Master's thesis book on the Writing page | publisher and year | ⏸ owner |
| 20 | After 31 December 2026: McKinsey end date; decide on the "Now" and "What I am looking for" sections | decision | ⏸ owner, 2027 |
| 21 | Restore hosting for edition-guru and cloudy-plag, then bring back their live and source links (see plan 13) | decision | ⏸ owner |

**Settings only Angelo can change**

- GitHub repo Settings, Pages: tick "Enforce HTTPS".
- GitHub repo Settings, Secrets and variables, Actions: add `GUARD_TERMS` (one term per line).
- Optional: point the DMARC `rua` address at hello@boutalikakis.com.

**Parked**

- Privacy-friendly visitor statistics (for example GoatCounter). Needs an owner decision and account.
- Uses or colophon page; internationalization. Recommended against.

## Round 1 (2026-07 to 2026-09, all done)

| # | Item | Plan | Status |
|---|------|------|--------|
| 01 | SEO foundations: sitemap, robots, canonicals, JSON-LD | [plans/01-seo-foundations.md](plans/01-seo-foundations.md) | ✅ PR #6 |
| 02 | Self-hosted fonts | [plans/02-self-hosted-fonts.md](plans/02-self-hosted-fonts.md) | ✅ PR #6 |
| 03 | Atom feed for Writing | [plans/03-rss-feed.md](plans/03-rss-feed.md) | ✅ PR #6 |
| 04 | Accessibility pass (v3 design) | [plans/04-accessibility-pass.md](plans/04-accessibility-pass.md) | ✅ PR #6, superseded by 11 for v4 |
| 05 | Project case-study pages | [plans/05-project-case-studies.md](plans/05-project-case-studies.md) | ✅ PR #6, rebuilt in PR #8 |
| 06 | Deploy self-verification | [plans/06-deploy-verification.md](plans/06-deploy-verification.md) | ✅ PR #6 |
| 07 | CI quality gates | [plans/07-ci-quality-gates.md](plans/07-ci-quality-gates.md) | ✅ PR #6, extended in PR #8 |
| 08 | Per-page share cards | [plans/08-og-images-per-page.md](plans/08-og-images-per-page.md) | ✅ PR #6, restyled in PR #9 |
| 09 | Real CV, About and email | [plans/09-cv-and-about-completion.md](plans/09-cv-and-about-completion.md) | ✅ PR #7, rebuilt in PR #8 |
| 10a | Dark mode | [plans/10-deferred-ideas.md](plans/10-deferred-ideas.md) | Shipped in PR #7, removed by the v4 design (PR #9) |
| 10c | Custom domain www.boutalikakis.com | [plans/10-deferred-ideas.md](plans/10-deferred-ideas.md) | ✅ PR #10 |
| 10e | Guestbook avatars | [plans/10-deferred-ideas.md](plans/10-deferred-ideas.md) | ✅ PR #7 |
| | Content rebuild from the career context file | owner brief | ✅ PR #8 |
| | v4 "Academic" redesign | [../brand/DESIGN_SYSTEM.md](../brand/DESIGN_SYSTEM.md) | ✅ PR #9 |
| | Follow-ups: hello@ address, portrait on CV, tagline, vaguer client detail, About margin column, phone text alignment | owner requests | ✅ PRs #11 to #22 |

## Working agreement for executors

- Read `CLAUDE.md`, `plans/_CONTEXT.md`, then the one plan you execute.
- Verify with the recipes the plan names and look at your screenshots.
- Run `python3 scripts/check.py` before committing.
- Update this table's Status column in the same PR as the work.
