#!/usr/bin/env python3
"""CI quality gates for aboutali.github.io.

Stdlib only (no pip installs), matching the repo's no-build-step posture.
Run locally before pushing:

    python3 scripts/check.py

Exits non-zero if any check fails, with a readable per-check report. Checks:

  1. Marker integrity + rewrite simulation (index.html Action markers).
  2. Internal links — every href/src in a tracked *.html resolves to a file.
  3. HTML sanity — one <h1>, a <title>, lang on <html>, alt on every <img>,
     no duplicate ids, per tracked *.html.
  4. XML validity — sitemap.xml / writing/feed.xml, when present.
  5. scripts/generate.py compiles.
  6. No em dashes in visible text (text, titles, meta/og, alt, JSON-LD, feed).
  7. Guard terms: no client names or internal jargon in visible text. The
     list lives in the GUARD_TERMS secret or a git-ignored .guard-terms file.
"""

import importlib.util
import os
import re
import subprocess
import sys
import xml.dom.minidom
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "javascript:", "//")


def tracked_html_files():
    """Every *.html file tracked by git, repo-root-relative, forward slashes."""
    try:
        out = subprocess.run(
            ["git", "-C", ROOT, "ls-files", "*.html"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        files = [line.strip() for line in out.splitlines() if line.strip()]
        if files:
            return sorted(files)
    except Exception:
        pass
    # Fallback (no git available): walk the tree, skip .git.
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            if name.endswith(".html"):
                rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
                files.append(rel.replace(os.sep, "/"))
    return sorted(files)


class PageParser(HTMLParser):
    """One pass over a page collecting everything the sanity + link checks need."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1_count = 0
        self.has_title = False
        self.html_lang = None
        self.img_missing_alt = []  # [(line, col)]
        self.ids = []  # [(id, line, col)]
        self.links = []  # [(attr, value, line, col)]

    def handle_starttag(self, tag, attrs):
        self._handle(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        # Default HTMLParser behavior calls handle_starttag then handle_endtag;
        # be explicit so self-closing tags (e.g. <img .../>) are still counted.
        self._handle(tag, attrs)

    def _handle(self, tag, attrs):
        d = {}
        for name, value in attrs:
            d[name] = value
        pos = self.getpos()
        tag = tag.lower()
        if tag == "html":
            self.html_lang = d.get("lang")
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self.has_title = True
        elif tag == "img":
            if "alt" not in d:
                self.img_missing_alt.append(pos)
        if d.get("id"):
            self.ids.append((d["id"], pos))
        for attr in ("href", "src"):
            if d.get(attr):
                self.links.append((attr, d[attr], pos))


def parse_file(relpath):
    path = os.path.join(ROOT, relpath)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    parser = PageParser()
    parser.feed(text)
    parser.close()
    return parser


# --- Check 1: marker integrity + rewrite simulation ------------------------


def check_markers():
    failures = []
    index_path = os.path.join(ROOT, "index.html")
    text = open(index_path, encoding="utf-8").read()

    # Derived from generate.py's PROJECTS map (not hardcoded here) so the two
    # stay in sync: whatever repo generate.py knows how to light an LED for
    # is exactly what index.html must carry a marker for.
    spec = importlib.util.spec_from_file_location(
        "gen", os.path.join(ROOT, "scripts", "generate.py")
    )
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    repos = list(gen.PROJECTS)

    for r in repos:
        if not re.search(r"<!--LED:%s-->.*?<!--/LED-->" % re.escape(r), text, re.S):
            failures.append("index.html: missing LED marker for %r" % r)
    for name, pat in [
        ("ACTIVITY", r"<!--ACTIVITY:BEGIN-->.*?<!--ACTIVITY:END-->"),
        ("GUESTBOOK", r"<!--GUESTBOOK:BEGIN-->.*?<!--GUESTBOOK:END-->"),
        ("UPDATED", r"<!--UPDATED:BEGIN-->.*?<!--UPDATED:END-->"),
    ]:
        if not re.search(pat, text, re.S):
            failures.append("index.html: missing %s marker" % name)

    if failures:
        return failures  # no point simulating a rewrite on a broken page

    gen.is_up = lambda u: True
    gen.latest_commit = lambda r: ("2026-01-01", "Test message")
    gen.gh_api = lambda p: [
        {
            "user": {"login": "tester"},
            "created_at": "2026-01-01T00:00:00Z",
            "body": "Hi",
        }
    ]
    t2 = gen.set_leds(text)
    t2 = gen.set_activity(t2)
    t2 = gen.set_guestbook(t2)
    t2 = gen.set_updated(t2)
    if "tester" not in t2 or "Test message" not in t2:
        failures.append("rewrite simulation: stub content did not land in output")
    for marker in (
        "<!--/LED-->",
        "<!--ACTIVITY:END-->",
        "<!--GUESTBOOK:END-->",
        "<!--UPDATED:END-->",
    ):
        if marker not in t2:
            failures.append("rewrite simulation: %s missing after rewrite" % marker)
    return failures


# --- Check 2: internal links ------------------------------------------------


def resolve_link(from_file, value):
    """Return the repo-root-relative target path for an internal href/src."""
    path_part = value.split("#", 1)[0].split("?", 1)[0]
    if path_part == "":
        return None  # pure fragment/query, nothing to resolve
    if path_part.startswith("/"):
        target = os.path.normpath(os.path.join(ROOT, path_part.lstrip("/")))
    else:
        from_dir = os.path.dirname(os.path.join(ROOT, from_file))
        target = os.path.normpath(os.path.join(from_dir, path_part))
    if path_part.endswith("/") or os.path.isdir(target):
        target = os.path.join(target, "index.html")
    return target


def check_links(files):
    failures = []
    for relpath in files:
        parser = parse_file(relpath)
        for attr, value, pos in parser.links:
            if value.startswith(EXTERNAL_PREFIXES) or value.startswith("#"):
                continue
            target = resolve_link(relpath, value)
            if target is None:
                continue
            if not os.path.isfile(target):
                failures.append(
                    "%s:%d: %s=%r resolves to missing file %s"
                    % (relpath, pos[0], attr, value, os.path.relpath(target, ROOT))
                )
    return failures


# --- Check 3: HTML sanity ---------------------------------------------------


def check_html_sanity(files):
    failures = []
    for relpath in files:
        parser = parse_file(relpath)
        if parser.h1_count != 1:
            failures.append(
                "%s: expected exactly one <h1>, found %d" % (relpath, parser.h1_count)
            )
        if not parser.has_title:
            failures.append("%s: missing <title>" % relpath)
        if not parser.html_lang:
            failures.append("%s: <html> missing lang attribute" % relpath)
        for pos in parser.img_missing_alt:
            failures.append("%s:%d: <img> missing alt attribute" % (relpath, pos[0]))
        seen = {}
        for id_, pos in parser.ids:
            seen.setdefault(id_, []).append(pos)
        for id_, positions in seen.items():
            if len(positions) > 1:
                lines = ", ".join(str(p[0]) for p in positions)
                failures.append(
                    "%s: duplicate id=%r at lines %s" % (relpath, id_, lines)
                )
    return failures


# --- Check 4: XML validity --------------------------------------------------


def check_xml():
    failures = []
    for relpath in ("sitemap.xml", "writing/feed.xml"):
        path = os.path.join(ROOT, relpath)
        if not os.path.isfile(path):
            continue  # skip silently if absent
        try:
            xml.dom.minidom.parse(path)
        except Exception as e:
            failures.append("%s: invalid XML — %s" % (relpath, e))
    return failures


# --- Check 5: generate.py compiles -----------------------------------------


def check_generate_compiles():
    failures = []
    import py_compile

    path = os.path.join(ROOT, "scripts", "generate.py")
    try:
        py_compile.compile(path, doraise=True)
    except py_compile.PyCompileError as e:
        failures.append(str(e))
    return failures


# --- 6 + 7. Visible-text checks ------------------------------------------------

EM_DASH = "—"

# Attributes whose values readers see (tooltips, alt text, link previews).
VISIBLE_ATTRS = ("alt", "title", "aria-label")
VISIBLE_META = ("description", "og:title", "og:description", "og:site_name",
                "twitter:title", "twitter:description")


class VisibleTextParser(HTMLParser):
    """Collects (line, text) pairs a visitor or a link preview can see.

    Skips <style> and non-JSON-LD <script>. Skips the ACTIVITY marker region:
    it holds commit messages the daily Action injects, which generate.py
    sanitizes on its own.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.chunks = []
        self._skip = 0
        self._in_activity = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "style" or (tag == "script" and a.get("type") != "application/ld+json"):
            self._skip += 1
        for name in VISIBLE_ATTRS:
            if a.get(name):
                self.chunks.append((self.getpos()[0], a[name]))
        if tag == "meta":
            key = a.get("name") or a.get("property") or ""
            if key in VISIBLE_META and a.get("content"):
                self.chunks.append((self.getpos()[0], a["content"]))

    def handle_endtag(self, tag):
        if tag in ("style", "script") and self._skip:
            self._skip -= 1

    def handle_comment(self, data):
        if data.strip() == "ACTIVITY:BEGIN":
            self._in_activity = True
        elif data.strip() == "ACTIVITY:END":
            self._in_activity = False

    def handle_data(self, data):
        if not self._skip and not self._in_activity and data.strip():
            self.chunks.append((self.getpos()[0], data))


def visible_text(relpath):
    path = os.path.join(ROOT, relpath)
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    if relpath.endswith(".xml"):
        return [(i + 1, line) for i, line in enumerate(raw.splitlines())]
    p = VisibleTextParser()
    p.feed(raw)
    return p.chunks


def text_sources(files):
    extra = [f for f in ("writing/feed.xml",) if os.path.exists(os.path.join(ROOT, f))]
    return list(files) + extra


def check_em_dashes(files):
    failures = []
    for rel in text_sources(files):
        for line, text in visible_text(rel):
            if EM_DASH in text:
                snippet = text.strip().replace("\n", " ")[:70]
                failures.append("%s:%d: em dash in %r" % (rel, line, snippet))
    return failures


def load_guard_terms():
    """Guard terms name real clients, so they never live in this public repo.

    Sources, first match wins: the GUARD_TERMS env var (a GitHub Actions
    secret, one term per line), or a git-ignored .guard-terms file at the
    repo root for local runs.
    """
    raw = os.environ.get("GUARD_TERMS", "")
    if not raw.strip():
        local = os.path.join(ROOT, ".guard-terms")
        if os.path.exists(local):
            with open(local, encoding="utf-8") as fh:
                raw = fh.read()
    return [t.strip() for t in raw.splitlines() if t.strip()]


def check_guard_terms(files):
    terms = load_guard_terms()
    if not terms:
        print("  SKIP: no guard-term list (set the GUARD_TERMS secret or add .guard-terms)")
        if os.environ.get("GITHUB_ACTIONS"):
            print("::warning::Guard-term check skipped: GUARD_TERMS secret is not set.")
        return []
    patterns = [
        (i + 1, re.compile(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(t)))
        for i, t in enumerate(terms)
    ]
    failures = []
    for rel in text_sources(files):
        for line, text in visible_text(rel):
            for idx, pat in patterns:
                if pat.search(text):
                    # Report the term's list position only: CI logs are public.
                    failures.append("%s:%d: matches guard term #%d" % (rel, line, idx))
    return failures


# --- Runner ------------------------------------------------------------------


def run_check(name, fn):
    print("== %s ==" % name)
    failures = fn()
    if failures:
        for f in failures:
            print("  FAIL: %s" % f)
        print("%s: FAIL (%d issue%s)" % (name, len(failures), "" if len(failures) == 1 else "s"))
    else:
        print("%s: PASS" % name)
    print()
    return not failures


def main():
    files = tracked_html_files()

    results = []
    results.append(run_check("1. Marker integrity + rewrite simulation", check_markers))
    results.append(run_check("2. Internal links", lambda: check_links(files)))
    results.append(run_check("3. HTML sanity", lambda: check_html_sanity(files)))
    results.append(run_check("4. XML validity", check_xml))
    results.append(run_check("5. generate.py compiles", check_generate_compiles))
    results.append(run_check("6. No em dashes in visible text", lambda: check_em_dashes(files)))
    results.append(run_check("7. Guard terms", lambda: check_guard_terms(files)))

    passed = sum(1 for r in results if r)
    total = len(results)
    print("%d/%d checks passed." % (passed, total))
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
