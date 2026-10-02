# Plan 13: Offline projects, drop dead links

Read `CLAUDE.md` first. Effort: S.

## Finding (2026-10-02)
edition-guru: live site https://aboutali.github.io/edition-guru/ returns 404;
source https://github.com/aboutali/edition-guru returns 404 (private repo).
cloudy-plag: live site returns 404; source returns 403 or 404 (not public).
Visitors following either link hit an error page.

## Change
- Homepage project table: remove the `live` and `src` links for these two
  rows. Keep the row, description and LED marker (the daily Action keeps
  showing the open circle for offline).
- Their work pages: remove the Live and Source rows from the facts table.
- Leave `PROJECTS` in `scripts/generate.py` unchanged so the status check
  keeps pinging the old URLs and flips to "live" if hosting returns.

## Reversal
When Angelo restores hosting (backlog item 21), restore the links from git
history.
