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

# The contribution graph

It is **not part of the README** — it's GitHub's own profile UI, rendered below whatever your
README contains. No README edit can remove it.

**To actually hide it:** Settings → Public profile → Contributions & Activity →
**"Make profile private and hide activity."**

Per [GitHub's docs](https://docs.github.com/en/account-and-profile/concepts/about-your-profile),
a private profile hides:

> Achievements and highlights · Activity overview and activity feed · **Contribution graph** ·
> Follower and following counts · Follow and Sponsor buttons · Organization memberships ·
> Stars, projects, packages, and sponsoring tabs · Your pronouns

and keeps **README, bio and profile picture** publicly visible. So the README you just installed
survives intact and effectively becomes your whole profile — which is the outcome you want.

Two caveats: the docs don't state whether **pinned repositories** survive, so check your profile
after toggling and untick it if they vanish. And it only applies going forward — it doesn't erase
past activity, and your activity on public repos stays visible on those repos.

**Consider filling the graph instead of hiding it.** Nine contributions in a year doesn't match
six years of professional work. The usual cause is commits authored under an email GitHub doesn't
recognise. Check what you commit as:

```bash
git config user.email
```

If that isn't listed under **Settings → Emails**, add it. GitHub **retroactively** recounts past
commits once the address is linked — graphs often fill in years of history at once. Also enable
**Settings → Public profile → Include private contributions on my profile**. Try this first; a
full graph beats a hidden one.

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
