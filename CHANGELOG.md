# Changelog

Notable changes to faithbot.tools. Newest first.

Format follows [Keep a Changelog](https://keepachangelog.com/). Dates are the
day the change went live — pushing to `main` publishes immediately.

---

## 2026-09-01

### Fixed
- **The "identical" nav was not identical.** Scoping `site-nav.css` under `.site-nav` was
  not enough: `tool-styles.css` defines *bare* `.nav-links { flex: 1; justify-content:
  center }` and `.nav-link { padding: .5rem .875rem; border-radius: 6px }`, which still
  match inside `.site-nav` and were never reset. So on its ten pages the nav rendered
  stretched, centred and pill-padded, while elsewhere it was flush right. Measured in the
  browser: `flex-grow: 1`, `justify-content: center`, `padding: 8px 14px`.
  Phase 1 was verified on markup only, which could not see this.
- **The Chipp check had a blind spot.** It grepped `chipp.ai` and reported 4 embeds. Chipp is
  also reachable through `*.faithbot.io` vanity domains that 308 into `/w/chat/<Bot>-<id>/`,
  and `youversion.html` embeds `youversionplan.faithbot.io`. The real count was 5. The check
  now matches both and the budget is 5.

### Changed
- **Logo now uses the right asset for each background.** The single logo file was a white
  wordmark on a baked-in navy plate (60% of the image), so it read as a navy sticker on the
  white nav bar and only looked correct on the navy hero. Replaced with two plate-free
  variants generated from the `CLAUDE.md` canonical master (navy on transparent, 5.72:1):
  `imb-innovation-logo-navy.png` for the light nav bar and
  `imb-innovation-logo-white.png` (white knockout) for the navy hero. Both 1201×210, which
  is the size `CLAUDE.md` prescribes for a nav bar and covers the 200px hero too.
  Verified in the browser rather than assumed.

### Fixed (dead embeds)
- **`goals.html`, `ripen.html` and `coffeecoach.html` embedded hosts that no longer exist.**
  `goals1`/`ripen1`/`coffeecoach.donbarger.com` have no DNS record, no Caddy vhost among the
  45 on the shared droplet, no systemd unit and no DigitalOcean app. All three rendered an
  empty grey frame with no error. Each now shows a short retirement notice with a link to the
  current tools, keeping the shared nav.

  Deliberately not deleted and not silently redirected: nothing links to these pages, so the
  only arrivals are old links and printed QR codes, and those people asked for that tool
  specifically.

### Previously known broken (now fixed above — was #5)
- `goals.html`, `ripen.html` and `coffeecoach.html` embed `goals1.donbarger.com`,
  `ripen1.donbarger.com` and `coffeecoach.donbarger.com`. **None of those hosts resolve in
  DNS.** All three pages are live and render an empty grey frame. They are unreachable from
  the nav, so nobody arrives except by old link or QR code.

### Noted
- The nav logo asset is a white wordmark on a **baked-in navy plate** (60% of the image), so
  on the white nav bar it reads as a navy sticker. It looks correct only on the navy hero,
  where the plate blends in. `CLAUDE.md` specifies a navy-on-transparent master and says not
  to put a box or pill behind the mark. Pre-existing — the pixels are identical before and
  after the 2026-08-31 downscale.

---

## 2026-08-31

### Changed
- **The 17 `engage-*.html` stubs now carry their worldview across.** They already
  redirected to www.engagelostness.com, but every one landed on the bare root, so
  someone who clicked "Engage Muslims" got a cold picker asking who they'd like to
  practise with. Each now deep-links to the audience it used to embed
  (`?worldview=muslims`). Three are not one-to-one: `engage-turks` and
  `engage-latin-american-catholics` were folded into a parent worldview's region
  and carry `&region=` as well, and `engage-postmoderns` points at `secular` —
  that worldview was renamed *and* rewritten on the other side.
  Generated from `spec/wrapper-redirects.mjs` in `donbarger/engage-lostness-v3`
  by `scripts/write-wrappers.mjs`, so the mapping lives in one place and is
  covered by a test there; a worldview renamed over there would otherwise orphan
  a printed QR code here in silence.
  `rel=canonical` deliberately stays on the bare app root: seventeen stubs
  pointing into one single-page app should consolidate onto one canonical URL,
  not declare seventeen query-string variants of the same document.

### Fixed
- **`verify-site.py` stub-integrity check** adjusted for the above, keeping every
  bug it was written to catch. meta-refresh and `location.replace` must still
  agree **exactly** — they are the two things that actually navigate, and a
  disagreement lands JS-off and JS-on visitors in different places. `canonical`
  is now compared ignoring the query string, so it still fails on a wrong scheme,
  host or path. Verified by reintroducing all three bug classes.
  The check also has to unescape the two HTML attributes but *not* the JavaScript
  string literal: `html.unescape` applies the legacy no-semicolon rule, so
  `&region=` in a bare string silently becomes `®ion=`.

### Removed
- **"Other Languages" retired.** Dropped from the site nav on every page, and
  `other-languages.html` is now a redirect stub to the FaithBot engine. The page
  was a grid of one card per language, from when each language was its own bot;
  FaithBot v3 handles 50+ languages behind a single picker.
  The 21 `lang-*.html` stubs are **kept** — each carries a `?lang=` code that
  printed QR codes and bookmarks still point at.
- **Buy Me a Coffee button removed** from all pages (`coffeecoach`, `goals`,
  `nxtgen-faithbot`, `ripen`, `youversion`, `old-home`, and the retired
  `other-languages`).
- **The espresso "coffee" nav identity** is gone from 10 pages, replaced by the
  shared IMB Innovation bar.

### Changed
- **One navigation on every page** (#3): FaithBot · Engage Lostness · Bible Pics ·
  Blog. The site previously had three different answers to "where am I?" — a white
  IMB bar on 3 pages, a dark espresso bar on 10, and no bar at all on `index.html`
  and four others. New self-contained `site-nav.css`, `position: sticky` so no page
  needs a content offset.
- **Spanish hubs collapsed to one** (#4). `recursos-en-espanol.html` is canonical;
  `lang-spanish.html` redirects to it. The two carried identical card sets and had
  to be edited in tandem.
- **Spanish lede** on `recursos-en-espanol.html` now reads "Herramientas impulsadas
  por IA para la fe, el ministerio y el alcance. Recursos diseñados para el mundo
  hispanohablante."
- **Nav logo downscaled**: 7392×1920 / 621K → 808×210 / 37K, ~94% off every page
  load. Aspect ratio and lockup unchanged.
- **Copiloto de Pastor restored** as a third card on the Spanish hub.
- **Engage Lostness card named in Spanish** — "Alcanza a los Perdidos". The app has
  no Spanish name of its own, so this was coined to match the site's imperative
  naming pattern.

### Fixed
- **`spanish-bot-de-fé.html` was committed under two Unicode spellings of "é"** (#2). Both
  blobs were byte-identical, and no `href` in any commit ever used the NFD spelling — it was
  an upload artifact from 2026-01-18. The NFD entry is removed; the NFC one, which every link
  has always pointed at, stays. CI now has a check to stop it recurring.
  (Note for anyone repeating this: `core.precomposeunicode=true` rewrites an NFD path argument
  to NFC, so `git rm` on the NFD path removes the *NFC* entry. Disable it for that one command.)
- Malformed nav markup in `other-languages.html` — a stray `</a>`, a duplicated
  nav link outside the container, and an unbalanced `</div>`.

### Added
- **CI** (`.github/workflows/ci.yml` + `.github/verify-site.py`) — seven static-site
  checks on push and pull request, each guarding a bug class that has actually shipped
  here. Every check was verified by deliberately breaking the thing it guards and
  watching it go red. Note CI does *not* gate the deploy: `deploy_on_push` publishes
  regardless.
- **`SBOM.md`** — no build or runtime dependencies; documents the four third-party
  origins the browser contacts (GA, Google Fonts, chipp.ai, rss2json).
- **Branch protection on `main`**, so CI actually gates the deploy. Until now
  `deploy_on_push` published the instant a push landed, red CI or not. `main` now
  requires the `verify` check, blocks force-pushes and deletions, and sets
  `enforce_admins: true` — so it applies to everyone, including repo admins.

  **Direct pushes to `main` no longer work. Every change goes via a pull request.**
  Verified by attempting a direct push and confirming it was rejected, rather than
  trusting the settings. To lift it in an emergency:
  `gh api -X DELETE repos/donbarger/faithbot/branches/main/protection`.
- **Eighth CI check: duplicate Unicode filenames**, unblocked by the #2 fix below. It
  can only observe a duplicate on a normalisation-sensitive filesystem, so it is
  meaningful on the Linux runner and vacuous on macOS.

### Documentation
- **Discovered a second live copy of the site**: GitHub Pages is still enabled and
  publishes to `https://donbarger.github.io/faithbot/` on every push. The old README's
  "Platform: GitHub Pages" line was not stale as assumed — it was incomplete. Both are
  real. Now documented.
- `README.md` rewritten. The previous version described GitHub Pages deployment,
  `chat.faithbot.io` iframes, and a live Engage Lostness hub — none of which had
  been true for some time.
- Added this changelog.

---

## 2026-08-30

### Changed
- **Engage Lostness moved off this site.** `engage-lostness.html` and all 17
  worldview card pages became redirect stubs to `www.engagelostness.com`. The nav
  tab and home-page card link straight out. This retired the last 5 English Chipp
  embeds.
- **Spanish worldview pages retired**: the 10 `spanish-*` worldview pages became
  redirect stubs to `www.engagelostness.com/?lang=es`.
- **Spanish hub cut to its essentials** — from 13 cards to a focused set linking
  directly out, with no redirect-stub hop.

---

## Earlier

- All 20 language pages and Bot de Fé redirect to FaithBot v3 with `?lang=<code>`,
  retiring the `*.faithbot.io` Chipp vanity domains.
- Site moved to DigitalOcean App Platform with `deploy_on_push` (the README long
  claimed GitHub Pages).
- FaithBot v3 announced on the home page: 50+ languages.
