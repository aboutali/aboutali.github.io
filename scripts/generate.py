#!/usr/bin/env python3
"""Regenerate the live bits of index.html in place.

Run by .github/workflows/refresh.yml. Uses only the Python standard library
(no pip installs), so the site stays dependency-free.

It rewrites four marked regions:
  * <!--LED:REPO-->...<!--/LED-->        per-project up/down status dot
  * <!--ACTIVITY:BEGIN-->...END-->        marquee of each repo's latest commit
  * <!--GUESTBOOK:BEGIN-->...END-->       entries from this repo's `guestbook` issues
  * <!--UPDATED:BEGIN-->...END-->         today's date

Everything is best-effort: network/API failures degrade gracefully (a project
shows "down", activity falls back, guestbook shows the empty-state) and never
crash the build.
"""

import os
import re
import json
import html
import datetime
import urllib.request
import urllib.error

OWNER = "aboutali"
INDEX_REPO = "aboutali.github.io"  # this repo, where guestbook issues live

# repo slug -> live URL the status dot pings
PROJECTS = {
    "gesundheit-mcp": "https://gesundheit-mcp-17797849230.europe-west6.run.app/mcp",
    "life-improver": "https://aboutali.github.io/life-improver/",
    "edition-guru": "https://aboutali.github.io/edition-guru/",
    "bxl_eda_worker": "https://aboutali.github.io/bxl_eda_worker/",
    "cloudy-plag": "https://aboutali.github.io/cloudy-plag/",
    "cleardoc": "https://aboutali.github.io/cleardoc/",
}

# gesundheit-mcp's GitHub repo is private: the workflow's token cannot read
# its commits, so latest_commit() is skipped for it entirely (see
# set_activity). Its endpoint also answers a plain GET with a 4xx because it
# expects an MCP session, not a browser GET, so is_up() below treats any
# status under 500 as "up" for this one URL instead of requiring 2xx/3xx.
PRIVATE_REPOS = {"gesundheit-mcp"}
LENIENT_STATUS_URLS = {PROJECTS["gesundheit-mcp"]: 500}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.environ.get("INDEX_PATH", os.path.join(ROOT, "index.html"))
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
UA = "aboutali-index-bot"


def ascii_safe(s):
    """Render any non-ASCII as numeric HTML entities so the output stays pure
    ASCII and matches the page's iso-8859-1 charset regardless of input."""
    return s.encode("ascii", "xmlcharrefreplace").decode("ascii")


def dedash(s):
    """Strip em dashes from any text this script injects into the page (commit
    messages, guestbook text). " — " (spaced) becomes ", "; any remaining
    "—" becomes "-"."""
    return s.replace(" — ", ", ").replace("—", "-")


def gh_api(path):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={"Accept": "application/vnd.github+json", "User-Agent": UA},
    )
    if TOKEN:
        req.add_header("Authorization", "Bearer " + TOKEN)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def is_up(url):
    """True if the URL responds with a non-error status.

    Most project URLs must answer 2xx/3xx. A few (see LENIENT_STATUS_URLS,
    e.g. an MCP endpoint that expects a session rather than a browser GET)
    only need to answer below a higher status ceiling: any response short of
    a hard server failure counts as up.
    """
    max_status = LENIENT_STATUS_URLS.get(url, 400)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            code = getattr(r, "status", None) or r.getcode()
            return code < max_status
    except urllib.error.HTTPError as e:
        return e.code < max_status  # 4xx/5xx (e.g. a Pages 404) means down
    except Exception:
        return False


def set_leds(text):
    for repo, url in PROJECTS.items():
        up = is_up(url)
        cls = "led-up" if up else "led-down"
        title = "online" if up else "offline"
        led = '<span class="led %s" title="%s" role="img" aria-label="%s">&#9679;</span>' % (
            cls,
            title,
            title,
        )
        pat = re.compile(r"(<!--LED:%s-->).*?(<!--/LED-->)" % re.escape(repo), re.S)
        text = pat.sub(lambda m: m.group(1) + led + m.group(2), text)
    return text


def latest_commit(repo):
    try:
        commits = gh_api("/repos/%s/%s/commits?per_page=1" % (OWNER, repo))
    except Exception:
        return None
    if not commits:
        return None
    # Defensive: the commit, committer, or message can be absent/null on some
    # bot/imported commits — degrade rather than crash the whole build.
    c = commits[0].get("commit") or {}
    lines = (c.get("message") or "").splitlines()
    msg = dedash(lines[0].strip()) if lines else ""
    committer = c.get("committer") or {}
    date = (committer.get("date") or "")[:10]
    return date, msg


def set_activity(text):
    parts = []
    for repo in PROJECTS:
        if repo in PRIVATE_REPOS:
            continue  # token can't read a private repo's commits; no ticker entry
        lc = latest_commit(repo)
        if not lc:
            continue
        date, msg = lc
        if len(msg) > 60:
            msg = msg[:57] + "..."
        parts.append("%s &middot; %s (%s)" % (repo, ascii_safe(html.escape(msg)), date))
    if parts:
        ticker = " &nbsp;&nbsp;&#10022;&nbsp;&nbsp; ".join(parts)
    else:
        ticker = "Latest commits will appear here."
    return re.sub(
        r"(<!--ACTIVITY:BEGIN-->).*?(<!--ACTIVITY:END-->)",
        lambda m: m.group(1) + ticker + m.group(2),
        text,
        flags=re.S,
    )


def set_guestbook(text):
    try:
        issues = gh_api(
            "/repos/%s/%s/issues?labels=guestbook&state=open&per_page=50"
            % (OWNER, INDEX_REPO)
        )
    except Exception:
        issues = []
    rows = []
    for it in issues:
        if "pull_request" in it:
            continue
        user = ascii_safe(html.escape(dedash(it.get("user", {}).get("login", "someone"))))
        date = (it.get("created_at") or "")[:10]
        # Hard sanitize: truncate raw, strip em dashes, escape everything,
        # keep line breaks, force ASCII.
        body = dedash((it.get("body") or "").strip()[:280])
        body = html.escape(body).replace("\r\n", "\n").replace("\n", "<br>")
        body = ascii_safe(body)
        if not body:
            body = "<i>(no message)</i>"
        rows.append(
            '<p class="gb-entry">'
            '<img class="gb-avatar" src="https://github.com/%s.png?size=64" '
            'width="32" height="32" loading="lazy" alt="">'
            '<b>%s</b> '
            '<span class="gb-date">%s</span><br>%s</p>'
            % (user, user, date, body)
        )
    block = "\n".join(rows) if rows else '<p class="gb-empty">Be the first to sign the guestbook.</p>'
    return re.sub(
        r"(<!--GUESTBOOK:BEGIN-->).*?(<!--GUESTBOOK:END-->)",
        lambda m: m.group(1) + "\n" + block + "\n" + m.group(2),
        text,
        flags=re.S,
    )


def set_updated(text):
    today = datetime.date.today()
    stamp = "%s %d, %d" % (today.strftime("%B"), today.day, today.year)
    return re.sub(
        r"(<!--UPDATED:BEGIN-->).*?(<!--UPDATED:END-->)",
        lambda m: m.group(1) + stamp + m.group(2),
        text,
        flags=re.S,
    )


def main():
    with open(INDEX, "r", encoding="utf-8") as f:
        text = f.read()
    original = text
    text = set_leds(text)
    text = set_activity(text)
    text = set_guestbook(text)
    text = set_updated(text)
    if text != original:
        with open(INDEX, "w", encoding="utf-8") as f:
            f.write(text)
        print("index.html updated.")
    else:
        print("No changes.")


if __name__ == "__main__":
    main()
