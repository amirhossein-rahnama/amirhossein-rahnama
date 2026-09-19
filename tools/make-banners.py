"""Generates every custom SVG asset for the GitHub profile README.

Run:  python tools/make-banners.py
Writes hero, timeline, metrics strip, divider, project cards and the LinkedIn cover.
"""
import math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ASSETS = os.path.join(OUT, "assets")
os.makedirs(ASSETS, exist_ok=True)

BG0, BG1 = "#0D1117", "#080B10"
A1, A2, A3 = "#58A6FF", "#39D0D8", "#A371F7"
TXT, MUT, LINE = "#E6EDF3", "#8B949E", "#21262D"
SANS = "ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,Consolas,monospace"


def wrap(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ───────────────────────────── shared defs ─────────────────────────────
def base_defs(extra=""):
    return f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="{BG0}"/><stop offset="55%" stop-color="#0A0E14"/><stop offset="100%" stop-color="{BG1}"/>
</linearGradient>
<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="{A1}"/><stop offset="50%" stop-color="{A2}"/><stop offset="100%" stop-color="{A3}"/>
</linearGradient>
<linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#FFFFFF"/><stop offset="42%" stop-color="{A1}"/>
  <stop offset="76%" stop-color="{A2}"/><stop offset="100%" stop-color="{A3}"/>
</linearGradient>
<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="{A1}" stop-opacity="0"/><stop offset="22%" stop-color="{A1}"/>
  <stop offset="55%" stop-color="{A2}"/><stop offset="82%" stop-color="{A3}"/>
  <stop offset="100%" stop-color="{A3}" stop-opacity="0"/>
</linearGradient>
<radialGradient id="au1"><stop offset="0%" stop-color="{A1}" stop-opacity="0.30"/><stop offset="100%" stop-color="{A1}" stop-opacity="0"/></radialGradient>
<radialGradient id="au2"><stop offset="0%" stop-color="{A2}" stop-opacity="0.26"/><stop offset="100%" stop-color="{A2}" stop-opacity="0"/></radialGradient>
<radialGradient id="au3"><stop offset="0%" stop-color="{A3}" stop-opacity="0.28"/><stop offset="100%" stop-color="{A3}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
  <path d="M32 0 L0 0 0 32" fill="none" stroke="#1B2029" stroke-width="1"/>
</pattern>
<filter id="soft" x="-90%" y="-90%" width="280%" height="280%">
  <feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
{extra}</defs>"""


def aurora(W, H):
    """Slow-drifting colour blobs behind everything."""
    return f"""<g filter="url(#glow)" opacity="0.9">
<ellipse cx="{W*0.18:.0f}" cy="{H*0.30:.0f}" rx="300" ry="170" fill="url(#au3)">
  <animateTransform attributeName="transform" type="translate" values="0 0; 60 24; 0 0" dur="17s" repeatCount="indefinite"/></ellipse>
<ellipse cx="{W*0.70:.0f}" cy="{H*0.62:.0f}" rx="330" ry="185" fill="url(#au2)">
  <animateTransform attributeName="transform" type="translate" values="0 0; -54 -30; 0 0" dur="21s" repeatCount="indefinite"/></ellipse>
<ellipse cx="{W*0.46:.0f}" cy="{H*0.14:.0f}" rx="270" ry="140" fill="url(#au1)">
  <animateTransform attributeName="transform" type="translate" values="0 0; 34 34; 0 0" dur="25s" repeatCount="indefinite"/></ellipse>
</g>"""


def brackets(x, y, w, h, s=17):
    """HUD corner brackets."""
    p = []
    for (cx, cy, dx, dy) in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        p.append(f'<path d="M{cx} {cy + dy*s} L{cx} {cy} L{cx + dx*s} {cy}" fill="none" '
                 f'stroke="{A2}" stroke-opacity="0.75" stroke-width="1.8" stroke-linecap="round"/>')
    return "".join(p)


def sine_path(x0, x1, y, amp, period, phase=0.0, step=4):
    pts = []
    x = x0
    while x <= x1:
        pts.append(f"{x:.1f},{y + amp*math.sin(2*math.pi*(x/period)+phase):.1f}")
        x += step
    return "M" + " L".join(pts)


def field(cx0, cy0, w, h, n=7, period=190):
    out = []
    for i in range(n):
        t = i / (n - 1)
        y = cy0 + t * h
        amp = 10 + 20 * math.sin(math.pi * t)
        op = 0.16 + 0.60 * math.sin(math.pi * t) ** 1.4
        col = [A1, A2, A3][i % 3]
        d = sine_path(cx0 - 10, cx0 + w + period + 20, y, amp, period, phase=i * 0.55)
        out.append(
            f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op:.2f}" '
            f'stroke-width="{1.6 if i % 2 else 1.1:.1f}" stroke-linecap="round">'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-{period} 0" '
            f'dur="{9+i*1.3:.1f}s" repeatCount="indefinite"/></path>')
    return "".join(out)


def mesh(cx0, cy0, w, h, cols=5, rows=4):
    pts = []
    for r in range(rows):
        for c in range(cols):
            pts.append((cx0 + (c + 0.5) * w / cols + 9 * math.sin(r * 2.1 + c * 1.3),
                        cy0 + (r + 0.5) * h / rows + 7 * math.cos(c * 1.7 + r * 0.9)))
    edges, nodes = [], []
    for i, (x1, y1) in enumerate(pts):
        for j, (x2, y2) in enumerate(pts):
            if j > i and math.hypot(x2 - x1, y2 - y1) < w / cols * 1.45:
                edges.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                             f'stroke="{A1}" stroke-opacity="0.18" stroke-width="0.9"/>')
    for i, (x, y) in enumerate(pts):
        col, d = [A1, A2, A3][i % 3], 2.6 + (i % 5) * 0.5
        dur = 2.8 + (i % 7) * 0.4
        nodes.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{d:.1f}" fill="{col}" fill-opacity="0.9" filter="url(#soft)">'
            f'<animate attributeName="r" values="{d:.1f};{d+1.7:.1f};{d:.1f}" dur="{dur:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="fill-opacity" values="0.9;0.35;0.9" dur="{dur:.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(edges) + "".join(nodes)


def chips(items, x, y, fs=13):
    out, cx = [], x
    for label in items:
        w = len(label) * fs * 0.62 + 26
        out.append(
            f'<g><rect x="{cx:.0f}" y="{y}" rx="13" width="{w:.0f}" height="26" fill="#12171F" '
            f'fill-opacity="0.9" stroke="#2A313C" stroke-width="1"/>'
            f'<text x="{cx+w/2:.0f}" y="{y+17.5}" font-family="{MONO}" font-size="{fs}" fill="{MUT}" '
            f'text-anchor="middle" letter-spacing="0.3">{label}</text></g>')
        cx += w + 9
    return "".join(out)


def stream(W, H, n=14):
    """Data packets drifting along the bottom rule."""
    out = []
    for i in range(n):
        d, delay = 7 + (i % 5) * 2.4, i * 0.72
        col = [A1, A2, A3][i % 3]
        out.append(
            f'<circle cy="{H-2.5}" r="{1.8 + (i%3)*0.6:.1f}" fill="{col}" fill-opacity="0.85" filter="url(#soft)">'
            f'<animate attributeName="cx" from="-20" to="{W+20}" dur="{d:.1f}s" begin="-{delay:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="fill-opacity" values="0;0.9;0.9;0" dur="{d:.1f}s" begin="-{delay:.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


# ───────────────────────────── hero / banner ─────────────────────────────
def banner(W, H, vx, vy, vw, vh, tx, name_size, sub_size, ys, chip_items, eyebrow, sub, tagline, cid):
    y_eye, y_name, y_sub, y_tag, y_chip = ys
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Edvin Rahnama — Data Scientist and ML Engineer">
{base_defs()}
<clipPath id="{cid}"><rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="16"/></clipPath>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{aurora(W, H)}
<rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.40"/>

<g clip-path="url(#{cid})">
  <rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="16" fill="#080C12" fill-opacity="0.66"/>
  {field(vx, vy+18, vw, vh-36)}
  {mesh(vx, vy, vw, vh)}
  <rect x="{vx}" y="{vy}" width="{vw}" height="46" fill="url(#accent)" opacity="0.10">
    <animateTransform attributeName="transform" type="translate" values="0 -60; 0 {vh}; 0 -60" dur="7s" repeatCount="indefinite"/>
  </rect>
</g>
<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="16" fill="none" stroke="{LINE}" stroke-width="1"/>
{brackets(vx, vy, vw, vh)}

<text x="{tx}" y="{y_eye}" font-family="{MONO}" font-size="13" fill="{A2}" letter-spacing="3.4">{eyebrow}<tspan fill="{A3}">&#9608;</tspan>
  <animate attributeName="opacity" values="1;1" dur="1s"/></text>
<text x="{tx}" y="{y_name}" font-family="{SANS}" font-size="{name_size}" font-weight="800" fill="url(#name)" letter-spacing="-1.6" filter="url(#glow)" opacity="0.32">EDVIN RAHNAMA</text>
<text x="{tx}" y="{y_name}" font-family="{SANS}" font-size="{name_size}" font-weight="800" fill="url(#name)" letter-spacing="-1.6">EDVIN RAHNAMA</text>
<text x="{tx}" y="{y_sub}" font-family="{SANS}" font-size="{sub_size}" font-weight="500" fill="{TXT}" fill-opacity="0.94">{sub}</text>
<text x="{tx}" y="{y_tag}" font-family="{SANS}" font-size="{sub_size-4}" fill="{MUT}">{tagline}</text>
{chips(chip_items, tx, y_chip)}

<rect x="0" y="{H-5}" width="{W}" height="5" fill="url(#bar)">
  <animate attributeName="opacity" values="0.6;1;0.6" dur="4.5s" repeatCount="indefinite"/></rect>
{stream(W, H)}
</svg>"""


hero = banner(1280, 360, 812, 52, 404, 256, 64, 56, 20, (100, 160, 198, 230, 258),
              ["Python", "PyTorch", "AWS", "Docker", "Kubernetes", "Terraform"],
              "DATA SCIENTIST &#183; ML ENGINEER &#183; KIEL, DE ",
              "Physics-Informed Neural Networks &#183; MLOps on AWS",
              "M.Sc. Data Science &#183; Helmholtz-Zentrum Hereon &#183; t2consult", "vc")
open(os.path.join(ASSETS, "hero.svg"), "w", encoding="utf-8").write(hero)

cover = banner(1584, 396, 1074, 58, 452, 268, 350, 60, 21, (122, 186, 226, 260, 288),
               ["Python", "PyTorch", "AWS", "Docker", "MLOps"],
               "DATA SCIENTIST &#183; ML ENGINEER &#183; KIEL, GERMANY ",
               "Physics-Informed Neural Networks &#183; MLOps on AWS",
               "edvin-rahnama.space", "bc")
open(os.path.join(OUT, "linkedin-banner.svg"), "w", encoding="utf-8").write(cover)


# ───────────────────────────── career timeline ─────────────────────────────
STOPS = [
    ("2017 &#8211; 19", "Junior Full Stack", "Ratin &#183; Tehran"),
    ("2019 &#8211; 22", "SysAdmin &#8594; BI Analyst", "EMU &#183; Satrap &#183; Cyprus"),
    ("2023 &#8211; 24", "NLP &amp; Recommenders", "80s80s Radio &#183; Kiel"),
    ("2025 &#8211;", "IT Systems &amp; Automation", "t2consult &#183; Preetz"),
    ("2025 &#8211; 26", "Data Scientist &#183; PINNs", "Hereon &#183; Geesthacht"),
]
W, H = 1280, 210
LY = 138
MARGIN = 152          # keeps the outermost centred labels off the canvas edge
xs = [MARGIN + i * (W - 2 * MARGIN) / (len(STOPS) - 1) for i in range(len(STOPS))]
nodes = []
for i, ((yr, role, org), x) in enumerate(zip(STOPS, xs)):
    col = [A1, A2, A3, A2, A1][i]
    last = i == len(STOPS) - 1
    nodes.append(f"""<g>
  <line x1="{x:.0f}" y1="{LY-30}" x2="{x:.0f}" y2="{LY-6}" stroke="{col}" stroke-opacity="0.45" stroke-width="1.4"/>
  <circle cx="{x:.0f}" cy="{LY}" r="16" fill="{col}" fill-opacity="0.12">
    <animate attributeName="r" values="13;21;13" dur="{3.4+i*0.5:.1f}s" repeatCount="indefinite"/>
    <animate attributeName="fill-opacity" values="0.18;0.02;0.18" dur="{3.4+i*0.5:.1f}s" repeatCount="indefinite"/></circle>
  <circle cx="{x:.0f}" cy="{LY}" r="{7 if last else 6}" fill="{BG0}" stroke="{col}" stroke-width="{2.6 if last else 2}" filter="url(#soft)"/>
  {'<circle cx="%.0f" cy="%d" r="3" fill="%s"/>' % (x, LY, col) if last else ''}
  <text x="{x:.0f}" y="{LY-58}" font-family="{SANS}" font-size="15" font-weight="700" fill="{TXT}" text-anchor="middle">{role}</text>
  <text x="{x:.0f}" y="{LY-40}" font-family="{SANS}" font-size="12.5" fill="{MUT}" text-anchor="middle">{org}</text>
  <text x="{x:.0f}" y="{LY+30}" font-family="{MONO}" font-size="12.5" fill="{col}" text-anchor="middle" letter-spacing="1.1">{yr}</text>
</g>""")

timeline = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Career timeline 2017 to 2026">
{base_defs()}
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{aurora(W, H)}
<rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.30"/>
<text x="{W/2:.0f}" y="44" font-family="{MONO}" font-size="12.5" fill="{MUT}" text-anchor="middle" letter-spacing="3.6">CAREER PATH</text>
<line x1="60" y1="{LY}" x2="{W-60}" y2="{LY}" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>
<line x1="60" y1="{LY}" x2="{W-60}" y2="{LY}" stroke="url(#accent)" stroke-width="2.4" stroke-linecap="round"
      stroke-dasharray="{W-120}" stroke-dashoffset="{W-120}">
  <animate attributeName="stroke-dashoffset" from="{W-120}" to="0" dur="2.6s" fill="freeze"/></line>
<circle r="3.4" fill="{A2}" filter="url(#soft)">
  <animate attributeName="cx" from="60" to="{W-60}" dur="6s" begin="2.6s" repeatCount="indefinite"/>
  <animate attributeName="cy" values="{LY};{LY}" dur="6s" begin="2.6s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;1;1;0" dur="6s" begin="2.6s" repeatCount="indefinite"/></circle>
{''.join(nodes)}
<rect x="0" y="{H-4}" width="{W}" height="4" fill="url(#bar)" opacity="0.8"/>
</svg>"""
open(os.path.join(ASSETS, "timeline.svg"), "w", encoding="utf-8").write(timeline)


# ───────────────────────────── metrics strip ─────────────────────────────
METRICS = [("6+", "YEARS SHIPPING DATA SYSTEMS"), ("~30%", "MANUAL REPORTING REMOVED"),
           ("5", "ENGINEERING ROLES"), ("4", "LANGUAGES SPOKEN")]
W, H, PAD, GAP = 1280, 132, 22, 16
cw = (W - 2 * PAD - GAP * (len(METRICS) - 1)) / len(METRICS)
cards = []
for i, (big, label) in enumerate(METRICS):
    x = PAD + i * (cw + GAP)
    col = [A1, A2, A3, A2][i]
    cards.append(f"""<g>
  <rect x="{x:.0f}" y="20" width="{cw:.0f}" height="92" rx="14" fill="#0E131A" fill-opacity="0.82" stroke="{LINE}"/>
  <rect x="{x:.0f}" y="20" width="{cw:.0f}" height="2.6" rx="1.3" fill="{col}" opacity="0.85"/>
  <text x="{x+cw/2:.0f}" y="72" font-family="{SANS}" font-size="38" font-weight="800" fill="{col}" text-anchor="middle" filter="url(#soft)">{big}</text>
  <text x="{x+cw/2:.0f}" y="95" font-family="{MONO}" font-size="10.5" fill="{MUT}" text-anchor="middle" letter-spacing="1.5">{label}</text>
</g>""")
metrics = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Career metrics">
{base_defs()}<rect width="{W}" height="{H}" fill="url(#bg)"/>{aurora(W, H)}
<rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.25"/>{''.join(cards)}</svg>"""
open(os.path.join(ASSETS, "metrics.svg"), "w", encoding="utf-8").write(metrics)


# ───────────────────────────── project cards ─────────────────────────────
CARDS = [
    ("card-poll", "01", "Live-Poll-App", "Real-time polling platform with live result streaming, built and shipped end to end.",
     ["Next.js", "TypeScript", "Prisma", "Vercel"], A1),
    ("card-price", "02", "Price_Prediction", "Regression and time-series models forecasting asset price movement.",
     ["Python", "scikit-learn", "Pandas"], A2),
    ("card-recsys", "03", "recommender-system", "Recommendation engine enriched with metadata pulled from external music APIs.",
     ["Python", "NLP", "scikit-learn"], A3),
    ("card-hft", "04", "HFT-Trading", "High-frequency market data analysis and trading signal exploration.",
     ["Python", "NumPy", "Jupyter"], A2),
]
CW, CH = 480, 204
for slug, num, title, desc, stack, col in CARDS:
    lines = wrap(desc, 46)
    assert len(lines) <= 2, f"{slug}: description needs {len(lines)} lines, card fits 2"
    body = "".join(f'<text x="28" y="{104+i*21}" font-family="{SANS}" font-size="13.5" fill="{MUT}">{t}</text>'
                   for i, t in enumerate(lines))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" role="img" aria-label="{title}">
{base_defs()}
<rect width="{CW}" height="{CH}" rx="16" fill="url(#bg)"/>
<ellipse cx="{CW-40}" cy="24" rx="190" ry="110" fill="url(#au2)" opacity="0.8"/>
<rect width="{CW}" height="{CH}" rx="16" fill="url(#grid)" opacity="0.30"/>
<rect x="0.5" y="0.5" width="{CW-1}" height="{CH-1}" rx="16" fill="none" stroke="{LINE}"/>
<rect x="0" y="0" width="4" height="{CH}" rx="2" fill="{col}" opacity="0.9"/>
<text x="{CW-26}" y="44" font-family="{MONO}" font-size="30" font-weight="700" fill="{col}" fill-opacity="0.22" text-anchor="end">{num}</text>
<text x="28" y="50" font-family="{SANS}" font-size="20" font-weight="700" fill="{TXT}">{title}</text>
<line x1="28" y1="64" x2="{28+64}" y2="64" stroke="{col}" stroke-width="2.4" stroke-linecap="round"/>
{body}
{chips(stack, 28, CH-50, 12)}
<circle cx="{CW-30}" cy="{CH-32}" r="3" fill="{col}" filter="url(#soft)">
  <animate attributeName="fill-opacity" values="1;0.25;1" dur="3s" repeatCount="indefinite"/></circle>
</svg>"""
    open(os.path.join(ASSETS, f"{slug}.svg"), "w", encoding="utf-8").write(svg)


# ───────────────────────────── divider ─────────────────────────────
W, H = 1280, 26
divider = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="">
{base_defs()}
<!-- rects, not lines: a gradient stroke on a zero-height line has a degenerate bbox and never paints.
     Two halves with a real gap, so nothing opaque is painted behind the diamond (which would
     show as a dark bar on light backgrounds). userSpaceOnUse keeps one gradient across both. -->
<linearGradient id="rule" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">
  <stop offset="0%" stop-color="{A1}" stop-opacity="0"/><stop offset="22%" stop-color="{A1}"/>
  <stop offset="55%" stop-color="{A2}"/><stop offset="82%" stop-color="{A3}"/>
  <stop offset="100%" stop-color="{A3}" stop-opacity="0"/>
</linearGradient>
<rect x="0" y="{H/2-1.1}" width="{W/2-17}" height="2.2" fill="url(#rule)" opacity="0.9"/>
<rect x="{W/2+17}" y="{H/2-1.1}" width="{W/2-17}" height="2.2" fill="url(#rule)" opacity="0.9"/>
<rect x="-5.5" y="-5.5" width="11" height="11" fill="none" stroke="{A2}" stroke-width="1.8"
      transform="translate({W/2} {H/2})">
  <animateTransform attributeName="transform" type="rotate" values="45;135;45" dur="9s"
                    additive="sum" repeatCount="indefinite"/>
</rect>
<circle r="2.4" cy="{H/2}" fill="{A2}" filter="url(#soft)">
  <animate attributeName="cx" from="-10" to="{W+10}" dur="8s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;1;1;0" dur="8s" repeatCount="indefinite"/></circle>
</svg>"""
open(os.path.join(ASSETS, "divider.svg"), "w", encoding="utf-8").write(divider)

print("wrote:", sorted(os.listdir(ASSETS)))
