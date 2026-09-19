# Install

Your profile README lives in a repo named exactly after your username.

```bash
git clone https://github.com/amirhossein-rahnama/amirhossein-rahnama.git
cd amirhossein-rahnama
```

Copy `README.md` and the `assets/` folder in, then:

```bash
git add README.md assets
git commit -m "Redesign profile README with custom hero"
git push
```

If the repo doesn't exist yet: create a **public** repo named `amirhossein-rahnama`, tick
"Add a README", then push over it. GitHub shows it on your profile automatically.

**LinkedIn cover:** upload `linkedin-banner.png` (1584×396, already exact size) via
Profile → camera icon on the banner → Upload.

---

# What was broken in the old version

| Issue | Detail |
|---|---|
| **LinkedIn link 404'd** | URL was `linkedin.com/in/https://www.linkedin.com/in/...` — the full URL was pasted into the slug field. Your slug has also since changed to `edvin-rahnama-908b1b179`. |
| **Wrong email** | README had `amirhosseinrahnama@outlook.com`; your CV uses `amirhossein.rahnama@outlook.com` (with the dot). Mail to the old one bounces. |
| **4 dead badge logos** | Simple Icons removed the AWS, LinkedIn, Power BI and Redshift marks over trademark policy — those badges rendered as blank chips. They're now embedded as inline SVG data-URIs, so they can't break again. |
| **Name mismatch** | CV and LinkedIn say **Edvin**; README said nothing. Now consistent with the CV. |
| **GitLab badge used GitHub's colour** | `#181717` is GitHub's hex, not GitLab's. Badge removed. |
| **Stats widgets** | Removed — your 2026 graph shows 9 contributions, so they advertised inactivity. See below. |
| **GPRM footer comment** | `<!-- Proudly created with GPRM -->` told every reader it was a generator template. Gone. |

---

# Two things worth doing next

**1. Your contribution graph is probably lying.** Nine contributions in a year doesn't match six
years of professional work. The usual cause is commits authored under an email GitHub doesn't
know about. Check what you're committing as:

```bash
git config user.email
```

If that isn't an email listed under **Settings → Emails**, add it there. GitHub **retroactively**
recounts past commits once the address is linked — graphs often fill in years of history. Also
enable **Settings → Profile → Include private contributions on my profile**.

**2. Set descriptions and topics on the four featured repos.** They're all currently blank, so
anyone who clicks through from the README lands on a bare file list. Repo page → ⚙️ next to
"About" → add one sentence and 3–5 topics. This is 20 minutes and does more for how the profile
reads than anything else here.

---

# Editing the hero later

`tools/make-banners.py` regenerates both banners — edit the text near the bottom and run:

```bash
python tools/make-banners.py
```

It writes `hero.svg` and `linkedin-banner.svg`. The hero animates (drifting wave field, pulsing
nodes) via SMIL, which GitHub allows. If your browser ever shows it static, swap the README's
`assets/hero.svg` for `assets/hero.png`.

Verify the title claims stay true as things change — the hero currently hardcodes
"M.Sc. Data Science · Helmholtz-Zentrum Hereon · t2consult", which needs an edit after
you graduate in July 2026.
