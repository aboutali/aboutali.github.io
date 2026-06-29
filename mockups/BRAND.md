# Angelo Boutalikakis — Brand Identity (v0 exploration)

A first-pass brand system for a professional personal site, taking *inspiration*
(not copying) from [pentagram.com/work](https://www.pentagram.com/work): the
restrained black-on-white palette, the confident grotesque typography, generous
negative space, and the idea that **the work is the hero** — colour and energy
come from the projects themselves, not from decoration.

> This is a mockup / exploration. Nothing here touches the live site
> (`/index.html`). Treat the tagline and positioning as editable placeholders.

---

## 1. Positioning (placeholder — confirm this)

> **Angelo Boutalikakis** — independent builder. I design and ship small,
> opinionated web products at the intersection of **policy, culture, and
> wellbeing**.

Inferred from the current project set (an EU foreign-policy digest, a life
framework, a Zurich fitness aggregator, a plagiarism-integrity wiki, an
art-edition newsletter, a Zen microseasons PWA). Swap this line for whatever
you actually want to be known for — it drives everything below.

**Voice:** precise, curious, quietly witty. Short sentences. No hype. Lets the
work carry the weight.

---

## 2. Logotype & monogram

- **Wordmark:** `Angelo Boutalikakis` set in a tight neo-grotesque, all in one
  weight, slightly negative letter-spacing. No icon needed — the name *is* the
  mark, Pentagram-style.
- **Monogram:** `AB` for favicons, avatars, and tight spaces. Optionally framed
  in a square (the "index tile").
- **Signature device:** a thin top rule + a small caret/index motif (`→` / `·`)
  used as a wayfinding accent, echoing how Pentagram filters work by discipline.

---

## 3. Typography

Neo-grotesque, system-available so the site stays dependency-free (matching the
repo's "no build, no frameworks" ethos):

```
Display / Wordmark : "Helvetica Neue", Helvetica, Arial, sans-serif — 700, tight tracking
Headings           : same family, 600–700
Body               : same family, 400–500, 1.5 line-height
Mono accents       : "SFMono", "Courier New", monospace — for tags, years, metadata
```

Scale is fluid (`clamp()`): huge on desktop, calm on mobile. Big type contrast
is the whole point — a 100px name above 16px body copy.

---

## 4. Colour

The system is **ink on paper**; project accents supply the colour.

| Token        | Hex        | Use                                  |
|--------------|------------|--------------------------------------|
| Ink          | `#111111`  | Text, wordmark                       |
| Paper        | `#FAFAF8`  | Background (warm off-white)          |
| Paper / pure | `#FFFFFF`  | Cards, panels                        |
| Hairline     | `#E3E3DF`  | Rules, borders                       |
| Muted        | `#6E6E6A`  | Metadata, captions                   |
| Signal       | `#E8542F`  | Single accent — links, active state  |

**Per-project accents** (used on the generated tile covers):

| Project          | Accent     |
|------------------|------------|
| life-improver    | `#2F7D55`  |
| bxl_eda_worker   | `#1A3C6E`  |
| fit-schedule     | `#E8542F`  |
| cloudy-plag      | `#6B4FA0`  |
| edition-guru     | `#C0392B`  |
| iKoyomi          | `#2B3A67`  |

---

## 5. Layout principles

1. **The work is the hero.** Big project tiles, minimal chrome.
2. **One screen, one idea.** Name → statement → work → contact.
3. **Negative space is a feature.** Don't fill it.
4. **Categorise like an index.** Tags/disciplines under each project, filterable.
5. **Black & white frame, colour from work.** No gradients on the UI itself.

---

## 6. Chosen direction — Case study (à la `pentagram.com/work/capacity`)

The site reads like a **Pentagram case study**, not just a project list:
long vertical scroll, full-bleed visuals alternating with text blocks, a large
pull-quote, and a structured credits block at the foot.

| File | Page | Structure |
|------|------|-----------|
| `capacity-home.html` | **Homepage** | Big hero statement → work as full-bleed alternating sections → pull-quote statement → credits-style contact. |
| `capacity-case.html` | **Project case study** | Hero visual → title + tagline + discipline tags → lead → full-bleed media → two-up grid → pull-quote → body → credits → next project. |

Every project gets its own case-study page in this template; the homepage strings
them together. Visuals are pure CSS "brand-system" art (domain wheel, practice-card
grid, type specimens) standing in for real project imagery.

### Earlier explorations (superseded, kept for reference)

| File | Direction | Feel |
|------|-----------|------|
| `direction-01-editorial.html` | Editorial Index | Giant wordmark + masonry project grid. |
| `direction-02-specimen.html`  | Type Specimen | Ultra-minimal, type-driven index. |
| `direction-03-modular.html`   | Modular Colour | Bold modular colour panels. |

Open `mockups/index.html` for a side-by-side overview.

All mockups are **self-contained, dependency-free HTML** (no fonts, no JS
frameworks, no external assets — project "covers" are pure CSS), so they run
straight from GitHub Pages or a local file the same way your current site does.
