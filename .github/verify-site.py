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
"""
import glob, html, os, re, sys, unicodedata
from urllib.parse import urljoin, urlsplit

# The served root is docs/ — DigitalOcean's source_dir and GitHub Pages both point there. That is
# what gets checked. Falls back to the repo root, where the site used to live, so this script still
# works on older commits and during the transition while both trees exist.
if os.path.isdir('docs') and os.path.exists(os.path.join('docs', 'index.html')):
    os.chdir('docs')
    print('checking docs/ (the served root)\n')

BASE = 'https://www.faithbot.tools/'
ASSET_CEILING = 150 * 1024
# Chipp is reachable two ways: chipp.ai directly, and *.faithbot.io vanity domains that
# 308-redirect to /w/chat/<Bot>-<id>/. A check that greps only chipp.ai misses the vanity ones —
# youversion.html embeds youversionplan.faithbot.io and went uncounted.
CHIPP_HOSTS = r'(?:chipp\.ai|[a-z0-9-]+\.faithbot\.io)'
CHIPP_BUDGET = 5
EXPECTED_NAV = ['FaithBot', 'Engage Lostness', 'Bible Pics', 'Blog']
NO_NAV = {'old-home.html'}          # dead archive, queued for deletion in #5
FONT_EXEMPT = {'old-home.html'}     # ditto — sole user of styles.css and its font-weight: 800

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
    refresh alongside an absolute canonical is correct, not a mismatch.

    Two wrinkles, both of which produce false failures if ignored:

      * meta-refresh and location.replace must agree EXACTLY — they are the two things that
        actually navigate, and a disagreement between them means JS-on and JS-off visitors
        land in different places. That is the bug this check was written for.
      * canonical is compared IGNORING the query string. It is an SEO declaration, not a
        navigation path. The seventeen engage-* stubs deep-link into a single-page app
        (?worldview=muslims, and two carry &region= as well); their canonical deliberately
        stays on the bare app root so seventeen near-identical stubs consolidate onto one
        canonical URL instead of declaring seventeen query-string variants of one document.
        A typo in the scheme, host or path still fails, which is what the check is for.

    The refresh URL is an HTML attribute and so carries `&amp;`, while location.replace holds
    a JavaScript string literal carrying a bare `&`. Both are correct in context, so the two
    attribute-sourced values are unescaped and the JS literal is not. Unescaping the JS string
    too is a trap: html.unescape applies the legacy no-semicolon rule, so `&region=` in a
    bare string becomes `®ion=` and the two region-carrying stubs fail spuriously."""
    same_doc = lambda u: urlsplit(u)._replace(query='', fragment='').geturl()
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
        # canonical and refresh come out of HTML attributes; replace is a JS string literal.
        resolved = {k: urljoin(BASE, html.unescape(v.group(1)) if k != 'replace' else v.group(1))
                    for k, v in found.items()}
        if resolved['refresh'] != resolved['replace']:
            fail('stub-integrity',
                 f"refresh and replace disagree, so JS-off and JS-on visitors land differently: "
                 f"{resolved['refresh']} vs {resolved['replace']}", p)
            continue
        if same_doc(resolved['canonical']) != same_doc(resolved['refresh']):
            fail('stub-integrity',
                 f"canonical names a different document than the redirect: "
                 f"{resolved['canonical']} vs {resolved['refresh']}", p)


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
    down: re-adding an embed is a deliberate act that has to change this number.

    Counts BOTH chipp.ai and the *.faithbot.io vanity domains. The first version of this check
    grepped chipp.ai alone and reported 4 while the real figure was 5 — youversion.html embeds
    youversionplan.faithbot.io, which 308s straight into Chipp."""
    hits = [p for p in pages if re.search(r'(src|href)="[^"]*' + CHIPP_HOSTS, docs[p])]
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


def check_unicode_duplicate_filenames():
    """Issue #2: spanish-bot-de-fé.html was committed under BOTH Unicode spellings of "é" — NFC
    (U+00E9) and NFD (e + combining acute). macOS normalises them to one file so the duplicate is
    invisible locally; Linux serves two URLs, and CI counted 69 pages where a Mac counted 68.

    This check only works on a case- and normalisation-sensitive filesystem, i.e. the CI runner.
    On macOS it passes vacuously because the duplicate cannot be observed."""
    seen = {}
    for p in pages:
        key = unicodedata.normalize('NFC', p)
        if key in seen:
            fail('unicode-filename', f'duplicate of {seen[key]} under a different Unicode spelling', p)
        seen[key] = p


def check_font_consistency():
    """Pages once requested three different Inter weight-sets (400;500;600;700 / 400;600;700 /
    300;400;500;600;700;800), so different pages pulled different font files instead of sharing one
    cached request. Every page that asks for Inter must ask for the same weights.

    old-home.html is exempt: it is an unreachable archive (deletion proposed in #5) and the only
    page loading styles.css, whose .hero-title is the site's sole font-weight: 800.

    Merriweather is not a violation — post.html genuinely uses it for serif body copy — so only the
    Inter portion of the URL is compared."""
    canonical = '400;500;600;700'
    for p in pages:
        if p in FONT_EXEMPT:
            continue
        for weights in re.findall(r'family=Inter:wght@([^&"]*)', docs[p]):
            if weights != canonical:
                fail('fonts', f'Inter:wght@{weights} != {canonical}', p)


CHECKS = [
    ('tag balance',        check_tag_balance),
    ('internal links',     check_internal_links),
    ('redirect stubs',     check_stub_integrity),
    ('nav consistency',    check_nav_consistency),
    ('asset sizes',        check_asset_sizes),
    ('chipp budget',       check_chipp_budget),
    ('head essentials',    check_head_essentials),
    ('unicode filenames',  check_unicode_duplicate_filenames),
    ('font consistency',   check_font_consistency),
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
