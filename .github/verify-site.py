#!/usr/bin/env python3
"""
Static-site checks for faithbot.tools.

Runnable by hand (`python3 .github/verify-site.py`) as well as in CI, because a check you
cannot run locally is one you only meet when it is already red.

Scope note: this site has no build step, no dependencies and no test suite — it is HTML and
CSS served straight from the repo root. So these are not unit tests. Each one guards a class
of bug that has ACTUALLY shipped here, named in the docstrings below.

Deliberately NOT checked:
  * Inline <script>/<style>. engage-lostness-v3 forbids these because its production Caddy
    sends a CSP without 'unsafe-inline'. faithbot.tools sends no CSP, and 58 of 68 pages use
    inline <style> — the GA tag itself is inline. That check would be red on arrival.
  * NFC/NFD duplicate filenames. macOS collapses the two spellings of spanish-bot-de-fé.html
    into one file; a Linux runner checks out both. The check is correct but would be red until
    issue #2 is fixed, and a permanently-red check is decoration. Add it when #2 closes.
"""
import glob, os, re, sys, unicodedata
from urllib.parse import urljoin

BASE = 'https://www.faithbot.tools/'
ASSET_CEILING = 150 * 1024
CHIPP_BUDGET = 4
EXPECTED_NAV = ['FaithBot', 'Engage Lostness', 'Bible Pics', 'Blog']
NO_NAV = {'old-home.html'}          # dead archive, queued for deletion in #5

failures = []

def fail(check, detail, path=None):
    failures.append((check, detail, path))

def read(p):
    with open(p, encoding='utf-8', errors='replace') as fh:
        return fh.read()

pages = sorted(glob.glob('*.html'))
docs = {p: read(p) for p in pages}
stubs = [p for p in pages if 'location.replace' in docs[p]]
real = [p for p in pages if p not in stubs]


def check_tag_balance():
    """The nav in other-languages.html shipped with a stray </a>, a duplicated link outside
    its container and an unbalanced </div>. Browsers recovered; a reader would have seen a
    stray duplicate link. It was live and unnoticed."""
    for p in pages:
        s = docs[p]
        for open_t, close_t in (('<div', '</div>'), ('<a ', '</a>')):
            o, c = s.count(open_t), s.count(close_t)
            if o != c:
                fail('tag-balance', f'{open_t.strip()} {o} vs {close_t} {c}', p)


def check_internal_links():
    """Retiring a page means turning it into a redirect stub, never deleting it — printed QR
    codes and bookmarks still point at the old URLs. This catches a delete done by mistake."""
    for p in pages:
        for target in re.findall(r'href="([^"]+)"', docs[p]):
            if target.startswith(('http://', 'https://', '#', 'mailto:', 'data:')):
                continue
            base = target.split('#')[0].split('?')[0]
            if base.endswith('.html') and not os.path.exists(base):
                fail('broken-link', f'-> {target}', p)


def check_stub_integrity():
    """52 of 68 pages are hand-written redirect stubs. Each carries the destination THREE
    times (canonical, meta-refresh, location.replace). One typo and a stub silently sends
    people somewhere else, or nowhere. Compared as resolved absolute URLs, because a relative
    refresh alongside an absolute canonical is correct, not a mismatch."""
    for p in stubs:
        s = docs[p]
        found = {
            'canonical': re.search(r'rel="canonical"\s+href="([^"]+)"', s),
            'refresh':   re.search(r'http-equiv="refresh"\s+content="0;\s*url=([^"]+)"', s),
            'replace':   re.search(r"location\.replace\('([^']+)'\)", s),
        }
        missing = [k for k, v in found.items() if not v]
        if missing:
            fail('stub-integrity', f'missing {", ".join(missing)}', p)
            continue
        resolved = {k: urljoin(BASE, v.group(1)) for k, v in found.items()}
        if len(set(resolved.values())) != 1:
            fail('stub-integrity', f'destinations disagree: {resolved}', p)


def check_nav_consistency():
    """The site once had three different navs — a white IMB bar on 3 pages, a dark espresso
    bar on 10, and none at all on index.html. Nothing detected the drift."""
    for p in real:
        if p in NO_NAV:
            continue
        s = docs[p]
        n = s.count('class="site-nav"')
        if n != 1:
            fail('nav', f'expected 1 .site-nav, found {n}', p)
            continue
        labels = re.findall(r'class="nav-link(?: active)?"[^>]*>([^<]*)</a>', s)
        if labels != EXPECTED_NAV:
            fail('nav', f'{labels} != {EXPECTED_NAV}', p)


def check_asset_sizes():
    """The nav logo shipped at 7392x1920 / 621K on every page load while never being displayed
    above 200px. Nothing here needs to be large."""
    for p in glob.glob('*.png') + glob.glob('*.css') + glob.glob('*.svg') + glob.glob('*.jpg'):
        size = os.path.getsize(p)
        if size > ASSET_CEILING:
            fail('asset-size', f'{size // 1024}K > {ASSET_CEILING // 1024}K ceiling', p)


def check_chipp_budget():
    """Migration off Chipp is nearly done. This pins the remaining count so it can only go
    down: re-adding an embed is a deliberate act that has to change this number."""
    hits = [p for p in pages if re.search(r'(src|href)="[^"]*chipp\.ai', docs[p])]
    if len(hits) > CHIPP_BUDGET:
        fail('chipp-budget', f'{len(hits)} embeds > budget {CHIPP_BUDGET}: {hits}')


def check_head_essentials():
    """Every page, stubs included, is a real landing target and needs to be mobile-viewable,
    language-tagged, and measured."""
    for p in pages:
        s = docs[p]
        if 'name="viewport"' not in s:
            fail('head', 'no viewport meta', p)
        if not re.search(r'<html[^>]*\slang=', s):
            fail('head', 'no lang attribute on <html>', p)
        if 'G-S8PE79TKZ1' not in s:
            fail('head', 'no GA tag', p)


CHECKS = [
    ('tag balance',        check_tag_balance),
    ('internal links',     check_internal_links),
    ('redirect stubs',     check_stub_integrity),
    ('nav consistency',    check_nav_consistency),
    ('asset sizes',        check_asset_sizes),
    ('chipp budget',       check_chipp_budget),
    ('head essentials',    check_head_essentials),
]

print(f'{len(pages)} pages: {len(real)} real, {len(stubs)} redirect stubs\n')
for name, fn in CHECKS:
    before = len(failures)
    fn()
    added = len(failures) - before
    print(f'  {"FAIL" if added else "ok  "}  {name}' + (f'  ({added})' if added else ''))

if failures:
    print()
    for check, detail, path in failures:
        loc = f'file={path}::' if path else ''
        print(f'::error {loc}[{check}] {path or ""} {detail}'.replace('  ', ' '))
    print(f'\n{len(failures)} failure(s)')
    sys.exit(1)

print('\nall checks passed')
