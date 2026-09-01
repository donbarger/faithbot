# faithbot.tools

The public site for IMB Innovation's AI tools for missions and ministry.

**Live:** https://www.faithbot.tools

---

## Repo layout

**The site lives in `docs/`. That directory is the web root.** Everything at the repo root —
this file, `SBOM.md`, `CHANGELOG.md`, `.github/` — is deliberately *not* served.

```
docs/          the site. DigitalOcean source_dir and GitHub Pages both point here.
.github/       CI workflow + verify-site.py
README.md      you are here
SBOM.md        dependencies and third-party origins
CHANGELOG.md   what changed
tasks/         local planning notes, gitignored
```

Add a new page to `docs/`, not to the root. Every link in the site is relative and there are
no absolute `/...` paths, which is what made the move possible.

## What this repo actually is

A static site that has become, mostly, a **launcher**. The tools themselves no
longer live here — they run as their own applications, and this site's job is to
introduce them and send people to the right place in the right language.

That shows up in the file count: of 68 HTML files, **16 are real pages** and
**52 are redirect stubs**.

| Destination | Stubs |
|---|---|
| `https://www.engagelostness.com/` | 28 |
| `https://faithbot.donbarger.com/` | 23 |
| `recursos-en-espanol.html` | 1 |

A stub is not dead weight. Each one exists so that an old link, a bookmark, or a
**printed QR code** still lands somewhere useful. Retire a page by turning it
into a stub — do not delete it.

### The redirect stub pattern

Every stub follows the same shape, and new ones should too:

```html
<link rel="canonical" href="https://target/">
<meta http-equiv="refresh" content="0; url=https://target/">
<script>window.location.replace('https://target/');</script>
```

Plus the GA tag, the page's original `<title>`, and a visible fallback link for
anyone whose JS and meta-refresh both fail. `location.replace` is used rather
than `location =` so the stub stays out of session history and Back returns to
the site instead of bouncing through the redirect again.

---

## The tools, and where they live now

| Tool | Runs at | Language handling |
|---|---|---|
| FaithBot v3 | `faithbot.donbarger.com` | `?lang=<code>`, 50+ languages |
| Engage Lostness | `www.engagelostness.com` | `?lang=es` for Spanish |
| Bible Pics | `biblepics.donbarger.com` | — |
| Don's Blog | `blog.html` here, via Substack RSS | — |

**FaithBot v3 replaced the per-language pages.** There used to be one page per
language and one bot per worldview. The engine now handles both behind a single
picker, so `other-languages.html` and the whole `engage-*` family are stubs.

**Chipp is nearly gone.** Four pages still embed a `chipp.ai` bot:
`nxtgen-faithbot.html`, `spanish-copiloto-de-pastor.html`,
`spanish-alcanzar-a-las-naciones.html`, `spanish-ilustraciones-biblicas.html`.

---

## Navigation

One shared bar on every real page: **FaithBot · Engage Lostness · Bible Pics · Blog**

- Markup is `<nav class="site-nav">`, styles in **`site-nav.css`**.
- `site-nav.css` is **deliberately self-contained** — pages load different
  stylesheets (`main-styles.css`, `tool-styles.css`, or inline only), so it
  defines its own values instead of depending on either one's custom properties,
  and is scoped under `.site-nav`.
- It is `position: sticky`, not `fixed`. Sticky sits in normal flow, so no page
  needs a content offset to clear the bar.
- **Do not add a second nav toggle script.** Pages already ship one driving
  `.nav-toggle` / `.nav-links`. Two would toggle twice and cancel out, silently
  breaking the mobile menu.

### Spanish

`recursos-en-espanol.html` is the single canonical Spanish hub. There used to be
two, which had to be edited in tandem; don't reintroduce a second one.

Its three cards link straight out, no stub hop:
Bot de Fe → `faithbot.donbarger.com/?lang=es`,
**Alcanza a los Perdidos** → `www.engagelostness.com/?lang=es`,
Copiloto de Pastor → `spanish-copiloto-de-pastor.html`.

"Alcanza a los Perdidos" is a name coined here — Engage Lostness has no Spanish
name of its own and brands in English even under a Spanish UI.

Note: Spanish pages currently carry an **English** nav bar.

---

## Design

- **Primary:** IMB Innovation Blue `#1B365D` · white background · `#374151` body text
- **Font:** Inter, from Google Fonts
- **Nav breakpoints:** tightens at 1024px, collapses to a toggle at 860px
- **Logo:** `imb-innovation-logo.png`, 808×210. It is a *delivery* asset —
  displayed at 40px in the nav and 200px in the hero. It previously shipped at
  7392×1920 / 621K on every page. Do not re-upload a master here.

### Stylesheets

`site-nav.css` (shared nav) · `main-styles.css` · `tool-styles.css` ·
`blog-styles.css` · `post-styles.css` · `styles.css` · `spanish-nav-override.css`

These overlap and the old `.main-nav` / `.tool-nav` rules are now dead code.
Consolidation is tracked in issue #7.

---

## Deployment

**Pushing to `main` publishes immediately.** There is no staging step.

- **Platform:** DigitalOcean App Platform, app `c7a42ca2-46d8-49c8-aef6-b9d4c7a4ed3c`
- **CDN:** Cloudflare
- **`source_dir: /docs`** — not `/`
- **`deploy_on_push: true`** on `main`

**There is a second live copy.** GitHub Pages is also enabled on this repo
(source `main` / `/docs`) and publishes the whole site to
**https://donbarger.github.io/faithbot/**. Every push goes to both. They are
currently identical, but it is a duplicate of the site at a second indexable URL
with no canonical pointing back here. Turn Pages off, or add a canonical —
tracked in the issues.

```bash
git add -A && git commit -m "..." && git push origin main
```

### Verifying a deploy

Two rules, both learned the hard way:

1. **Check the deployed commit, not the newest deployment.** Listing deployments
   right after a push can return the *previous* build, which then goes ACTIVE and
   looks like success. Match the SHA:

   ```bash
   doctl apps list-deployments c7a42ca2-46d8-49c8-aef6-b9d4c7a4ed3c -o json \
     | python3 -c "import sys,json;[print(d['phase'],[c.get('source_commit_hash','')[:12] for c in d.get('static_sites') or []]) for d in json.load(sys.stdin)[:3]]"
   git rev-parse --short HEAD
   ```

2. **Changing the Pages source does not trigger a rebuild.** `PUT /repos/:o/:r/pages`
   accepts the new path and reports `status: built`, but the live artifact still comes from the
   old one until a build runs. Force one:

   ```bash
   gh api -X POST repos/donbarger/faithbot/pages/builds
   ```

3. **Use a check that can actually fail.** After the `docs/` move, `docs/` was a byte-identical
   copy of the root, so "index.html returns 200 with the right nav" was true either way and
   proved nothing. The discriminating probe is:

   ```bash
   curl -o /dev/null -w '%{http_code}\n' https://www.faithbot.tools/docs/index.html   # want 404
   ```

   404 there is the only evidence `docs/` is genuinely the web root.

4. **Verify against the live URL with a cache-buster, never the local file.**

   ```bash
   curl -s "https://www.faithbot.tools/index.html?cb=$RANDOM" | grep ...
   ```

Builds usually finish in under a minute, occasionally ~6.

### CI

`.github/workflows/ci.yml` runs `.github/verify-site.py` on push and on pull
requests. **Run it by hand too** — it needs nothing but `python3`:

```bash
python3 .github/verify-site.py
```

Seven checks, each guarding a class of bug that has actually shipped here: tag
balance, broken internal links, redirect-stub integrity, nav consistency, asset
size ceiling, a pinned Chipp-embed budget, and required `<head>` tags. The script
documents what is deliberately *not* checked, and why.

**CI does not gate the deploy.** `deploy_on_push` publishes the moment a push
lands, whether or not CI has finished or gone red. These checks tell you
something broke; they cannot stop it reaching production. Branch protection with
PR-only merges is what would actually gate it, and is not set up.

### What is and is not public

Only `docs/` is served. `README.md`, `SBOM.md`, `CHANGELOG.md` and `.github/` all return
**404** on both faithbot.tools and the GitHub Pages copy — verified.

This was not always true: `source_dir` used to be `/`, so every tracked file was fetchable,
`.github/verify-site.py` included. Anything you put in `docs/`, though, is public — and the
repo itself is public on GitHub regardless, so this is tidiness, not a security boundary.

---

## Local development

```bash
python3 -m http.server 5500   # then open http://localhost:5500
```

---

## Analytics

Google Analytics 4, `G-S8PE79TKZ1`, on every page including the redirect stubs.

---

## Known issues

Tracked at https://github.com/donbarger/faithbot/issues

- **#2** `spanish-bot-de-fé.html` is committed under two Unicode spellings of "é"
  (NFC and NFD). macOS collapses them; Linux serves two URLs.
- **#5** Real pages nothing links to: `biblepics.html`, `coffeecoach.html`,
  `goals.html`, `ripen.html`, `youversion.html`, `nxtgen-faithbot.html`,
  `spanish-alcanzar-a-las-naciones.html`, `spanish-ilustraciones-biblicas.html`,
  `old-home.html`.
- **#6** Three different Inter weight-sets are requested across pages.
- **#7** Five overlapping stylesheets, plus dead nav CSS.

---

*See `CHANGELOG.md` for what has changed.*
