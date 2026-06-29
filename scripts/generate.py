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
    "life-improver": "https://aboutali.github.io/life-improver/",
    "bxl_eda_worker": "https://aboutali.github.io/bxl_eda_worker/",
    "fit-schedule": "https://aboutali.github.io/fit-schedule/",
    "cloudy-plag": "https://aboutali.github.io/cloudy-plag/",
    "edition-guru": "https://aboutali.github.io/edition-guru/",
    "iKoyomi": "https://ikoyomi.netlify.app/",
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.environ.get("INDEX_PATH", os.path.join(ROOT, "index.html"))
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
UA = "aboutali-index-bot"


def ascii_safe(s):
    """Render any non-ASCII as numeric HTML entities so the output stays pure
    ASCII and matches the page's iso-8859-1 charset regardless of input."""
    return s.encode("ascii", "xmlcharrefreplace").decode("ascii")


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
    """True if the URL responds with a non-error status."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            code = getattr(r, "status", None) or r.getcode()
            return 200 <= code < 400
    except urllib.error.HTTPError:
        return False  # 4xx/5xx (e.g. a Pages 404) means the link is down
    except Exception:
        return False


def set_leds(text):
    for repo, url in PROJECTS.items():
        up = is_up(url)
        cls = "led-up" if up else "led-down"
        title = "online" if up else "offline"
        led = '<span class="led %s" title="%s">&#9679;</span>' % (cls, title)
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
    msg = lines[0].strip() if lines else ""
    committer = c.get("committer") or {}
    date = (committer.get("date") or "")[:10]
    return date, msg


def set_activity(text):
    parts = []
    for repo in PROJECTS:
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
        user = ascii_safe(html.escape(it.get("user", {}).get("login", "someone")))
        date = (it.get("created_at") or "")[:10]
        # Hard sanitize: truncate raw, escape everything, keep line breaks, force ASCII.
        body = (it.get("body") or "").strip()[:280]
        body = html.escape(body).replace("\r\n", "\n").replace("\n", "<br>")
        body = ascii_safe(body)
        if not body:
            body = "<i>(no message)</i>"
        rows.append(
            '<p class="gb-entry"><b>%s</b> '
            '<span class="gb-date">%s</span><br>%s</p>'
            % (user, date, body)
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
