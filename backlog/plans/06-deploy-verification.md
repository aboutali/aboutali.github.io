# Plan 06 — Deploy self-verification workflow

**Read `_CONTEXT.md` first.** · Effort: S–M (~1–2h) · Model: any (Sonnet fine) ·
Independent of other plans.

## Goal

Catch failed GitHub Pages deploys automatically. On 2026-07-02 a merge to
`main` produced a Pages deploy that sat in `deployment_queued` for 10 minutes
and timed out — the site silently kept serving stale content until a manual
re-run. This workflow makes that failure mode self-announcing and (safely)
self-healing.

## Design

New workflow `.github/workflows/verify-deploy.yml`:

- **Triggers:** `workflow_run` on "pages build and deployment" is NOT available
  (GitHub-managed dynamic workflow). Use instead: `push` to `main` (wait, then
  verify) + daily `schedule` (belt-and-braces) + `workflow_dispatch`.
- **Verify job** (`runs-on: ubuntu-latest`, `permissions: contents: write`):
  1. Wait 90s after push (give Pages a head start), then poll up to ~8 min
     (16 × 30s): `curl -fsS https://aboutali.github.io/` and compare a content
     fingerprint against the repo's checked-out `index.html`. Fingerprint: the
     first 12 hex of `sha256` of the `<!--UPDATED:BEGIN-->…<!--UPDATED:END-->`
     region is WRONG (Action updates it but a stale deploy can coincidentally
     match) — instead embed a deploy stamp: as step 0, this workflow does NOT
     modify files. Simplest robust fingerprint: compare `git rev-parse HEAD`
     against the deployed commit via the Pages API:
     `curl -s https://api.github.com/repos/aboutali/aboutali.github.io/pages/builds/latest`
     (with `GITHUB_TOKEN`) → `.commit` field. Poll until `.commit == GITHUB_SHA`
     and `.status == "built"`.
  2. Also curl `/`, `/about/`, `/writing/`, `/cv/` and require HTTP 200 each
     (catches partial deploys).
  3. **On failure after the polling window:** request a fresh build via the
     Pages API — `POST /repos/{owner}/{repo}/pages/builds` with `GITHUB_TOKEN`
     (this endpoint re-requests a Pages build without a commit; it's the clean
     alternative to empty commits). Then poll once more (~8 min). If still not
     built, exit 1 so the run shows red and (optional) `gh api` is unavailable —
     just let the failed run notify via GitHub's default failure email/UI.
- **Schedule run** does the same check against `origin/main`'s HEAD (fresh
  checkout gives that), so a missed failure is caught within 24h.

Keep it stdlib/curl/jq only (ubuntu-latest has curl + jq preinstalled). No
actions beyond `actions/checkout`.

## Why not `workflow_run` / marketplace actions

The Pages workflow is GitHub-managed ("dynamic") — not targetable by
`workflow_run`, and re-run APIs need permissions the default token may lack.
The `pages/builds` REST endpoints work with the default `GITHUB_TOKEN` on
legacy branch-built Pages (this repo's mode). Test this assumption first (step
below) and fall back to "fail loudly, no self-heal" if the POST is 403.

## Steps

1. Write the workflow (single job, bash steps, comments explaining each phase).
2. **Assumption test before merging:** from the feature branch, run the POST
   `pages/builds` call via `mcp__github__*` or curl with a token if available;
   if it 403s, keep the verification but replace self-heal with a clear
   `::error::` message telling the owner to click "Re-run failed jobs".
3. Add a "Deploy verification" subsection to README's automation section
   (3–4 lines: what it does, what a red run means).

## Verification

- `python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/verify-deploy.yml')); print('YAML OK')"`
  (pyyaml is preinstalled on the runner image but maybe not locally — if the
  import fails locally, use `ruby -ryaml -e ...` or careful review; do not pip install).
- Dry-run the poll logic locally as a bash script against the live site
  (should pass immediately since the site is currently in sync).
- After merge (owner action or next PR merge), watch one real run go green.

## Acceptance criteria

- Workflow exists, YAML-valid, documented in README; poll logic proven locally;
  self-heal path implemented or explicitly downgraded with the 403 rationale
  in the PR body; backlog row 06 ✅ with date + PR#.
