# aboutali/aboutali.github.io

Source for [aboutali.github.io](https://aboutali.github.io/) — a master index
of all my projects.

The site is a single `index.html` with a mid-'90s Apple/Mac "platinum" look —
light gray, dark text, and the classic six-color rainbow stripe. The static
markup needs no build; the live bits are refreshed by one GitHub Action, and
two small extras use vanilla JS (no frameworks, no package manager).

## Features

- **Status dots** — a green/red LED next to each project shows whether its live
  link actually responds. Refreshed daily by the Action (see below).
- **Activity ticker** — the marquee shows each repo's latest commit + date,
  pulled from the GitHub API at refresh time.
- **Guestbook** — rendered straight from this repo's GitHub Issues. Anyone can
  "Sign the guestbook" (opens an issue labelled `guestbook`); messages are
  HTML-escaped before they reach the page. Close the issue or remove the label
  to drop an entry on the next refresh.
- **Night Shift** — a toggle (saved to `localStorage`) that flips the platinum
  theme to an amber CRT theme with scanlines. Pure CSS/JS, degrades to the
  light theme with JS off.
- **Konami code** — `↑ ↑ ↓ ↓ ← → ← → B A` launches a flying-toasters
  screensaver (After Dark tribute). Press any key to dismiss.

## How the live bits work

`.github/workflows/refresh.yml` runs `scripts/generate.py` (Python stdlib only,
no installs) on a daily schedule, on `workflow_dispatch`, and on `issues`
events. The script rewrites four marked regions in `index.html`
(`LED:*`, `ACTIVITY`, `GUESTBOOK`, `UPDATED`) and commits the result back to
`main`, which redeploys Pages. All injected content is escaped and reduced to
pure ASCII, and every network call degrades gracefully — a build never fails
because a project is private, missing, or offline.

> Activity/status for **public** repos works with the default `GITHUB_TOKEN`.
> Private repos (e.g. `fit-schedule`, `edition-guru`) return 404 cross-repo and
> are simply skipped; to include them, add a PAT secret with `repo` scope and
> read it in the workflow.

## Adding a new project

1. Open `index.html`.
2. Find the block between `<!-- PROJECTS:BEGIN -->` and `<!-- PROJECTS:END -->`.
3. Add a new `<li>` (followed by `<br>`). Include a status-LED placeholder so
   the Action can light it up:

   ```html
   <li>
     <!--LED:REPO--><span class="led led-unknown">&#9679;</span><!--/LED-->
     <b><a href="https://aboutali.github.io/REPO/">REPO</a></b>
     <font size="2">[<a href="https://github.com/aboutali/REPO">source</a>]</font><br>
     One-sentence description.
   </li>
   <br>
   ```

4. Replace `REPO` (in both the `LED:` marker and the links) and the description,
   then add the repo to the `PROJECTS` dict in `scripts/generate.py`. Commit and
   push to `main`.

## Notes

- The Pages URL `aboutali.github.io/<repo>/` only resolves if that repo has
  GitHub Pages enabled (Settings → Pages → Source). Private repos require a
  paid plan to serve via Pages.
- `.nojekyll` is present so GitHub Pages serves files literally without
  Jekyll processing.
- Claude Code can scaffold/maintain this file — just ask it to add or remove
  a project.
