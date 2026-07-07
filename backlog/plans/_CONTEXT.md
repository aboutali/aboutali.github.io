# Executor context — read this FIRST before any backlog plan

You are working on **aboutali.github.io** — Angelo Boutalikakis's personal site.
Every plan in this directory assumes you have read this file. It encodes the
repo's invariants, brand system, and verification recipes. Do not skip it.

## The five invariants (violating any of these fails the task)

1. **No build step, no frameworks, no package manager.** Plain hand-written
   HTML/CSS (and stdlib-only Python in `scripts/`). Client-side JS only where a
   plan explicitly allows it. If your solution needs npm install, webpack, Jekyll,
   or a static-site generator, it is the wrong solution for this repo.
2. **Never break the Action markers in `index.html`.** The daily workflow
   (`.github/workflows/refresh.yml` → `scripts/generate.py`) regex-rewrites four
   marked regions in place: `<!--LED:REPO-->…<!--/LED-->` (×6),
   `<!--ACTIVITY:BEGIN-->…<!--ACTIVITY:END-->`,
   `<!--GUESTBOOK:BEGIN-->…<!--GUESTBOOK:END-->`,
   `<!--UPDATED:BEGIN-->…<!--UPDATED:END-->`. Any `index.html` edit must keep all
   markers intact and must pass the marker simulation (recipe below).
3. **Stay on brand.** Tokens live in `assets/site.css` `:root` and are canonical:
   Ink `#17171A`, Paper `#FAF8F4`, Stone `#6E6A60` / `#9B9890`, Hairline `#E6E2DA`,
   Cobalt `#2C46C8` (the ONE accent), Cobalt-deep `#1B2E8F`, status green `#1F9D57` /
   red `#C0563D`. Type: Archivo (grotesque, does the work), Newsreader italic
   (serif moments only), JetBrains Mono (data/labels). Tagline: *"Curiosity meets
   rigor."* Full rationale: `brand/foundation.md`. One accent, used with intent —
   never introduce new hues.
4. **Branch discipline.** Develop on the designated `claude/...` branch for your
   session. If the branch's previous PR was merged, restart it from `origin/main`
   (`git fetch origin main && git checkout -B <branch> origin/main`), then push
   with `--force-with-lease` only when the remote holds nothing but merged
   history. Never push to `main` directly. Do not open a PR unless asked.
5. **Placeholders are owner-gated.** Content marked `[REPLACE]` (CV) or
   `<!-- TODO: personalize -->` / `<!-- TODO: add email when ready -->` needs
   input from Angelo. Never invent real-world facts (jobs, degrees, email
   addresses) to fill them.

## Repo map

```
index.html            homepage (hero, ticker, Work list w/ status dots, guestbook)
about/ writing/ cv/   subpages; writing posts are directories (writing/<slug>/)
404.html              branded not-found (absolute asset paths — Pages serves it anywhere)
assets/site.css       shared tokens + chrome (topbar, footer, sections, buttons)
brand/                foundation.md (strategy) · index.html (visual guide) · assets/ (PNGs + generate.cjs)
scripts/generate.py   daily-refresh script (stdlib only, best-effort, race-safe publish)
.github/workflows/refresh.yml   daily 06:17 UTC + workflow_dispatch + issues events
backlog/              this backlog + plans
```

Shared page chrome (topbar with `wm-full`/`wm-mini` wordmark swap ≤640px, footer
with `.f-contact` row) is **duplicated per page** — a deliberate no-build
trade-off. When you change chrome, change it in every page: `index.html`,
`about/index.html`, `writing/index.html`, `writing/hello-world/index.html`
(and any newer post), `cv/index.html`. `404.html` has minimal chrome.

## Environment notes (Claude Code remote container)

- Playwright is preinstalled globally: `export NODE_PATH=$(npm root -g)` and
  `require("playwright")`; Chromium at `/opt/pw-browsers`. Never run
  `playwright install`.
- Chromium cannot reach arbitrary hosts directly; `curl` goes through the
  proxy fine. To render the site, serve locally:
  `python3 -m http.server 8642 --bind 127.0.0.1` from the repo root and load
  `http://127.0.0.1:8642/...` (absolute `/...` paths then resolve correctly).
- Wait for fonts before screenshots:
  `await page.evaluate(()=>document.fonts.ready)` then poll
  `document.fonts.check('700 40px Archivo')`. Race with a timeout — Google
  Fonts over the proxy is slow; cap waits (~2.5s) or your run times out.
- No `gh` CLI. Use `mcp__github__*` tools for GitHub API work.

## Verification recipes (run the ones your plan names)

**R1 — Marker integrity + rewrite simulation** (required for ANY index.html edit):
```bash
cd <repo> && python3 - <<'PY'
import re, importlib.util
t=open("index.html").read()
repos=["life-improver","bxl_eda_worker","fit-schedule","cloudy-plag","edition-guru","iKoyomi"]
ok=all(re.search(r"<!--LED:%s-->.*?<!--/LED-->"%re.escape(r),t,re.S) for r in repos)
ok&=all(re.search(p,t,re.S) for p in [r"<!--ACTIVITY:BEGIN-->.*?<!--ACTIVITY:END-->",
  r"<!--GUESTBOOK:BEGIN-->.*?<!--GUESTBOOK:END-->",r"<!--UPDATED:BEGIN-->.*?<!--UPDATED:END-->"])
assert ok, "MARKERS MISSING"
spec=importlib.util.spec_from_file_location("gen","scripts/generate.py")
gen=importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
gen.is_up=lambda u: True
gen.latest_commit=lambda r: ("2026-01-01","Test message")
gen.gh_api=lambda p: [{"user":{"login":"tester"},"created_at":"2026-01-01T00:00:00Z","body":"Hi"}]
t2=gen.set_leds(t); t2=gen.set_activity(t2); t2=gen.set_guestbook(t2); t2=gen.set_updated(t2)
assert "tester" in t2 and "Test message" in t2
assert all(m in t2 for m in ["<!--/LED-->","<!--ACTIVITY:END-->","<!--GUESTBOOK:END-->","<!--UPDATED:END-->"])
print("R1 PASS")
PY
```

**R2 — Render + overflow check** (required for any visual change): serve locally
(see above), load each changed page at widths **390 and 1280** in Playwright,
assert `document.documentElement.scrollWidth <= clientWidth+1` (no horizontal
overflow), zero `pageerror` events, and take full-page screenshots. Actually
LOOK at the screenshots (Read the PNGs) before declaring success.

**R3 — Link check**: every internal `href`/`src` in changed pages resolves to a
file in the repo (respecting each page's directory depth; root-absolute `/...`
paths resolve from repo root).

**R4 — CV print**: `page.emulateMedia({media:'print'})` on `/cv/` — topbar and
footer hidden, black text, no `[REPLACE]` regressions.

## Definition of done (every plan)

- All named verification recipes pass; screenshots reviewed.
- Working tree clean; committed with a descriptive message; pushed to the
  designated branch. Commit messages must end with the Claude Code attribution
  footer per session instructions.
- Summary states what changed, what was verified, and anything owner-gated
  that remains.
