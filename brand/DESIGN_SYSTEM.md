# Academic, design system for www.boutalikakis.com

The personal site of Dr. Angelo Boutalikakis (operator, product builder,
transformation leader, Zurich). This is the v4 identity, chosen over the
"Maison" and "Thread" directions. It replaces the v3 cobalt and Archivo
identity.

Source repo: `aboutali/aboutali.github.io` (branch `main`). Plain HTML and
CSS on GitHub Pages. No build, no frameworks, no client-side JS.

## Index

- `assets/site.css`: tokens, typography, spacing and every component class
  in one file (no build step, so no `@import` chain)
- `assets/fonts/`: self-hosted Newsreader (roman, italic) and JetBrains
  Mono, OFL

## Components (CSS classes)

`.desk` `.sheet` · `.runhead` · `.titleblock` `.kicker`
`.subtitle` `.abstract` `.keywords` · `h2.sec` `h3.sub` `.prose`
· `.caption` `.table` `.table.facts` `.led-up` `.led-down` ·
`.remark` · `.refs` `.doi` `.fn-rule` `.fn` `.folio` · `.btn`
`.mono` `.link` `.box` · `.cv-item`

Intentional: no React components. The live site has no JS, so components
ship as CSS classes.

## Content fundamentals

- Plain and exact. Short declarative sentences. Explains, never sells.
- No em dashes anywhere (site rule, enforced by `scripts/check.py`). En
  dashes only in number and date ranges.
- Third person in bio copy ("Angelo builds..."), first person in project
  and note copy ("I build and ship tools with AI").
- Sentence case for headings. Lowercase small caps in the running head.
- No emoji. Unicode glyphs only as data: `●` live, `○` offline, `→` `←`
  for navigation.
- Facts come only from Angelo's career context file. Never invent clients,
  figures or dates. Name employers only; describe clients by descriptor.

## Visual foundations

- **Metaphor:** a well-set academic paper. Every page is a white sheet
  (max 880px) on a stone desk (`#ECEAE4`), with a soft sheet shadow. LaTeX
  conventions are applied lightly: numbered sections, booktabs tables,
  citations `[1]`, footnotes, a centred page number (folio).
- **Colour:** monochrome. Ink `#141414` on white, greys for hierarchy.
  There is no accent colour. Status uses shape (`●`/`○`), not hue.
- **Type:** Newsreader for everything textual (500 titles, 700 headings,
  400 body, italic for subtitles and captions). All-small-caps for labels
  (Table 1, Remark 0.1, running head). JetBrains Mono for project names,
  file-like links and data.
- **Layout:** centred title block; 560px centred abstract; text measure
  about 68ch, justified with hyphens; sections 56px apart; numbers before
  headings carry hierarchy, so size steps stay small.
- **Rules:** 1.5px table top and bottom, 0.75px header rule, 0.5px
  hairlines. No vertical rules or zebra rows.
- **Corners and shadows:** radius 0 everywhere. The only shadow is on the
  sheet. Nothing inside the page has one.
- **Buttons:** bracketed mono labels `[ CV.pdf ]`, 0.5px outline; hover
  inverts to ink fill.
- **Links:** ink colour, no underline; underline on hover. `.link` for
  always-underlined inline links.
- **Imagery:** real screenshots only, shown greyscale with a hairline
  border and a "Figure n:" caption.
- **Motion:** none, apart from smooth scroll. Respect reduced motion.
- **Backgrounds:** no gradients, textures, blur or transparency.

## Iconography

None. There is no icon set and no logo mark. The name set in Newsreader is
the identity. Unicode `● ○ → ←` are the only glyphs.

## Fonts

Newsreader (roman, variable weight 200 to 800, and italic, variable weight
200 to 800) and JetBrains Mono (variable weight 400 to 800), latin subset,
self-hosted from `assets/fonts/`. Both are OFL. See
`assets/fonts/LICENSE-NOTE.md` for the source and license text.

## Design tokens

Colours: paper `#FFFFFF`, desk `#ECEAE4`, ink `#141414`, ink-2 `#333333`,
graphite `#555555`, muted `#888888`, rule `#BBBBBB`, row rule `#E2E2E2`.

Type: Newsreader. Title 500 clamp(38px, 6.4vw, 62px)/1.05. Subtitle
italic clamp(19px, 2.4vw, 23px). h2 700 24px. h3 700 19px. Body 17.5/1.6.
Small 15.5/1.45. Caption italic 14. Label all-small-caps 17px +0.06em.
JetBrains Mono 500 13.5 (names) and 400 12 (links, dates).

Spacing: 4, 8, 14, 18, 28, 40, 56, 72, 96. Sections 56px apart.

Rules: 1.5px (table top and bottom), 0.75px (table head), 0.5px
(hairlines).

Radius: 0. Shadow: the sheet only, `0 1px 2px rgba(0,0,0,.06), 0 12px 40px
rgba(0,0,0,.06)`.
