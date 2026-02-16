# IMB Innovation - FaithBot Platform

## 🌟 Overview

A clean, modern web platform showcasing IMB Innovation's AI-powered tools for missions and ministry. Built with a minimalist design featuring Sarum Blue branding and responsive navigation.

---

## 🗂️ Site Structure

### **Main Pages**
- `index.html` - FaithBot homepage with language selector (20 languages)
- `engage-lostness.html` - Worldview engagement hub with 17 worldview options
- `biblepics.html` - Bible story image generator
- `blog.html` - Don's Blog with Substack integration
- `post.html` - Blog post preview pages

### **FaithBot Language Pages**
20 languages with alphabetized dropdown navigation:
- English (default)
- Arabic, Bengali, Burmese, Cantonese
- Hindi, Hokkien, Indonesian, Japanese, Javanese
- Khmer, Korean, Lao, Malay
- Mandarin (Simplified & Traditional)
- Mongolian, Shona, Thai, Vietnamese

### **Engage Lostness Worldview Pages (17 files)**
Iframe-based pages for engaging different worldviews:
1. `engage-african-traditional.html` - African Traditional Religions
2. `engage-animism.html` - Animism
3. `engage-buddhists.html` - Buddhists
4. `engage-catholicism.html` - Catholicism
5. `engage-chinese-religions.html` - Chinese Religions
6. `engage-cultural-christians.html` - Cultural Christians
7. `engage-gen-alpha.html` - Gen Alpha
8. `engage-gen-z.html` - Gen Z
9. `engage-hindus.html` - Hindus
10. `engage-japanese.html` - Japanese
11. `engage-jehovah-witnesses.html` - Jehovah's Witnesses
12. `engage-latin-american-catholics.html` - Latin American Catholics
13. `engage-mormons.html` - Mormons
14. `engage-muslims.html` - Muslims
15. `engage-orthodox.html` - Orthodox
16. `engage-postmoderns.html` - Postmoderns
17. `engage-turks.html` - Turks

### **CSS Files**
- `main-styles.css` - Primary stylesheet with Sarum Blue design system
- `blog-styles.css` - Blog-specific styling
- `post-styles.css` - Blog post preview styling
- `tool-styles.css` - Legacy tool styling (retained for compatibility)

### **Assets**
- `imb-innovation-logo.png` - IMB Innovation navigation logo

---


### **Color Palette**

- **Primary:** Sarum Blue `#003DA5`
- **Background:** White `#FFFFFF`
- **Text:** Black `#000000`
- **Accent:** Light Gray `#f5f5f5`

### **Typography**

- **Font Family:** Inter (sans-serif)
- **Navigation:** 16px regular
- **Headings:** Bold weights
- **Body:** 400 regular

### **Responsive Breakpoints**

- **Desktop:** >768px - Full horizontal navigation
- **Mobile:** ≤768px - Hamburger menu with slide-down navigation

---

## 🚀 Features

### **FaithBot Integration**

Multi-language AI chatbot for Biblical questions and faith discussions:

- 20 language options with dropdown navigation
- Embedded iframe integration with `chat.faithbot.io`
- Language-specific subdomains (e.g., `spanish.chat.faithbot.io`)
- Clean, minimal interface for optimal user experience

### **Engage Lostness System**

17 worldview-specific engagement tools:

- Dual dropdown navigation (FaithBot languages + worldview selection)
- Iframe-based tool pages for seamless integration
- Worldview options include: Cultural Christians, Gen Alpha, Gen Z, Postmoderns, various world religions (Muslims, Hindus, Buddhists, etc.)
- External integrations: `faithbot.io` and `chipp.ai` endpoints

### **BiblePics Tool**

AI-powered Bible story image generator:

- Embedded `chipp.ai` chatbot (biblepicsbot-10020460)
- Consistent navigation with main site
- Full-screen iframe experience

### **Don's Blog**

Substack RSS integration:

- Auto-updating feed from `donbarger.substack.com`
- Article preview system via `post.html`
- "Click Here" CTA button to full Substack articles
- Clean card-based layout

---

## 🛠️ Technical Stack

### **Frontend**

- **HTML5:** Semantic markup, iframe integration
- **CSS3:** CSS custom properties (variables), Flexbox, responsive design
- **JavaScript:** Vanilla JS for dropdown navigation, iframe src updates, RSS parsing

### **External Integrations**

- **FaithBot API:** `chat.faithbot.io` and language subdomains
- **Chipp.ai:** Embedded chatbots for worldview tools and BiblePics
- **RSS2JSON API:** Substack blog feed parsing
- **Google Analytics 4:** Site tracking (G-S8PE79TKZ1)

### **Deployment**

- **Platform:** GitHub Pages
- **Repository:** github.com/donbarger/faithbot
- **Live Site:** https://donbarger.github.io

---

## 📂 Development

### **Local Development**

```bash
# Clone repository
git clone https://github.com/donbarger/faithbot.git
cd donbarger.github.io

# Start local server (Python)
python -m http.server 5500

# Or using Node.js
npx http-server -p 5500

# Visit in browser
open http://localhost:5500
```

### **Making Changes**

1. Edit HTML/CSS files directly
2. Test locally before committing
3. Commit and push to main branch
4. GitHub Pages auto-deploys in 2-3 minutes

### **Git Workflow**

```bash
# Stage changes
git add -A

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

---

## 🎯 Page Structure

### **index.html** - FaithBot Homepage

```
Components:
- IMB Innovation logo (links to index.html)
- Language dropdown (20 options)
- Main iframe → chat.faithbot.io
- Mobile hamburger menu
```

### **engage-lostness.html** - Worldview Hub

```
Components:
- IMB Innovation logo
- FaithBot language dropdown
- Worldview dropdown (17 options)
- Main iframe → loads engage-*.html pages
- Dual navigation system
```

### **engage-*.html** - Worldview Tools (17 files)

```
Structure:
- Minimal HTML (iframe-only)
- No navigation (loaded inside parent iframe)
- Full-viewport iframe
- External endpoint integration
```

### **biblepics.html** - BiblePics Tool

```
Components:
- IMB Innovation logo
- Standard navigation
- Main iframe → biblepicsbot-10020460.chipp.ai
```

### **blog.html** - Blog Hub

```
Components:
- IMB Innovation logo
- Standard navigation
- RSS feed integration (donbarger.substack.com)
- Article cards with onclick → post.html
```

### **post.html** - Article Preview

```
Components:
- IMB Innovation logo
- Article content preview
- Fade overlay
- "Click Here" CTA button → Substack
```

---

## 🎨 Design Principles

1. **Minimalism:** Clean, uncluttered interface
2. **Consistency:** IMB Innovation branding across all pages
3. **Responsive:** Mobile-first design approach
4. **Accessibility:** Clear navigation, readable typography
5. **Performance:** Fast loading, optimized iframes

---

## 📊 Analytics

**Google Analytics 4** tracking installed on all pages:

- **Tracking ID:** G-S8PE79TKZ1
- **Metrics:** Page views, sessions, user flow, device types
- **Dashboard:** https://analytics.google.com

---

## 🔄 Version History

### **v2.0 - IMB Innovation Platform** (Current)

- ✅ Complete rebrand from coffee theme to IMB Innovation
- ✅ Sarum Blue design system
- ✅ Minimalist navigation with logo
- ✅ 20 FaithBot languages
- ✅ 17 Engage Lostness worldviews
- ✅ BiblePics integration
- ✅ Blog with Substack RSS
- ✅ Mobile-responsive design

### **v1.0 - Original Portfolio**

- Coffee-themed personal portfolio
- 59 files (55 HTML, 4 CSS)
- Multiple tools and languages

---

## 📧 Contact

**Don Barger**

- Website: https://donbarger.github.io
- Blog: https://donbarger.substack.com
- Organization: IMB Innovation

---

*Last Updated: January 2025*  
*Design: Sarum Blue Minimalist*  
*Platform: GitHub Pages*
