# Changelog

Notable changes to faithbot.tools. Newest first.

Format follows [Keep a Changelog](https://keepachangelog.com/). Dates are the
day the change went live — pushing to `main` publishes immediately.

---

## 2026-08-31

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
- Malformed nav markup in `other-languages.html` — a stray `</a>`, a duplicated
  nav link outside the container, and an unbalanced `</div>`.

### Documentation
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
