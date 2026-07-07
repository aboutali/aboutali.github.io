# Plan 09 — CV & About completion (owner-gated)

**Read `_CONTEXT.md` first.** · Effort: S once unblocked (~1h) · Model: any ·
**Status: ⏸ BLOCKED — needs facts only Angelo can provide. Do not invent them.**

## Goal

Zero placeholders on the live site: real Experience/Education in the CV, a
personalized About bio, and (optionally) a published email address.

## What's needed from Angelo (ask exactly this, once)

1. **Experience** — for each role: title, organisation, city, years, one line
   on what changed because you were there. (2–4 roles is plenty.)
2. **Education** — degree, field, university, city, years. (Repeat per degree.)
3. **Skills** — confirm/extend the current chips: HTML/CSS/JS, Python, GitHub
   Actions, LLM tooling, Product design, Automation.
4. **About bio** — read `/about/` and reply with corrections in plain prose
   (or "fine as is").
5. **Email** — an address to publish, or "keep unpublished".
6. **CV framing** — is "Independent builder" the right lead, or should an
   employed role lead?

## Where the placeholders live (exact locations)

- `cv/index.html` — Experience: two `.cv-item` blocks with `[REPLACE]` spans
  (role/org/years/impact). Education: one `.cv-item` `[REPLACE]` block.
  Skills: one `[+ your own]` chip. The big TODO banner comment above
  Experience gets deleted when real data lands.
- `about/index.html` — `<!-- TODO: personalize -->` above the `.prose` block;
  facts grid (`Based in / Focus / Currently / Contact`) may need updating.
- **Email TODOs** (only if an address is provided) — replace
  `<!-- TODO: add email when ready -->` with
  `<a href="mailto:ADDR">ADDR</a><span class="sep">·</span>` as the first item
  in each `.f-contact` row: `index.html`, `about/index.html`,
  `writing/index.html`, `writing/hello-world/index.html`, `cv/index.html`
  (footer + the `.cv-contact` block, where email gets its own `<br>` line).
  Also update About's facts-grid Contact entry.

## Execution once data arrives

1. Fill everything verbatim from Angelo's answers — edit for typography (en
   dashes, date format `2023 — present`) but never for substance.
2. Remove the `.replace` CSS class from filled entries (keep the class
   definition — future placeholders may use it); delete stale TODO comments.
3. If email lands: update all five footers + CV contact + About facts +
   consider adding it to the JSON-LD Person only if Angelo says the address is
   public-by-intent (else leave out of structured data — scrapers).
4. Verification: **R1** (if index.html touched), **R2** on changed pages,
   **R4** (CV print — confirm no `[REPLACE]`/dashed outlines remain in print),
   grep `REPLACE` and `TODO: personalize` return nothing in `cv/` & `about/`.

## Acceptance criteria

- No placeholder text or TODO comments remain on CV/About; print CV is a real
  resume; contact rows updated per Angelo's choice; backlog row 09 ✅ with
  date + PR#.
