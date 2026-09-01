# SBOM — faithbot.tools

Direct dependencies only, and what leaves the visitor's machine. Reviewed by hand.

**Last reviewed:** 2026-08-31

---

## Build & runtime dependencies

**None.** This is static HTML and CSS served from the repo root. There is no
`package.json`, no build step, no bundler, no server-side code, and nothing is
installed to deploy it. That is deliberate and worth preserving — it is why the
site has no supply chain to speak of.

CI runs one Python script against the stdlib (`.github/verify-site.py`); Ubuntu
runners ship `python3`, so it installs nothing either.

---

## What the browser loads from third parties

Every one of these is a live third-party request made from the visitor's browser.

| Origin | What | Where | Why it's here |
|---|---|---|---|
| `googletagmanager.com` | Google Analytics 4 (`G-S8PE79TKZ1`) | every page, stubs included | traffic measurement |
| `fonts.googleapis.com` / `fonts.gstatic.com` | Inter (and Merriweather on one page) | most pages | typography |
| `chipp.ai` | embedded chatbots | 4 pages | legacy tools not yet migrated |
| `rss2json.com` | Substack feed → JSON | `blog.html`, `post.html` | renders Don's blog list |

**Privacy note:** GA and Google Fonts both mean every page view is visible to
Google, including views of the redirect stubs. Fonts could be self-hosted to
remove one of those; nothing here requires the CDN.

---

## Where the site sends people

Outbound only — these receive visitors, not data from this site.

| Destination | From |
|---|---|
| `faithbot.donbarger.com` | nav, 23 redirect stubs |
| `www.engagelostness.com` | nav, 28 redirect stubs |
| `biblepics.donbarger.com` | nav, home card |
| `donbarger.substack.com` | blog articles |
| `imb.org/give` | home page support CTA |
| `thegreatpursuit.faith`, `told.thegreatpursuit.faith` | home cards |

---

## Hosting

| | |
|---|---|
| **Platform** | DigitalOcean App Platform, app `c7a42ca2-46d8-49c8-aef6-b9d4c7a4ed3c`, `source_dir: /docs` |
| **CDN** | Cloudflare |
| **Also published** | GitHub Pages, `https://donbarger.github.io/faithbot/`, source `main` / `/docs` — a second live copy of the whole site |
| **Deploy** | `deploy_on_push: true` on `main`, no staging |

---

## Secrets

**None in this repo, and none needed.** No API keys, no tokens, no `.env`. The
GA measurement ID is a public identifier, not a credential.

Only `docs/` is served. This file, `README.md`, `CHANGELOG.md` and `.github/`
return 404 on both live URLs. The repo is public on GitHub regardless, so that
is tidiness rather than a security boundary. Local planning notes live in
`tasks/`, which is gitignored.
