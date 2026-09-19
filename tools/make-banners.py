"""Generates the custom hero + LinkedIn banner SVGs for the GitHub profile README."""
import math, os, io

OUT = r"D:\backup pc\claude\profile-assets"
os.makedirs(OUT, exist_ok=True)

BG0, BG1 = "#0D1117", "#090C10"
A1, A2, A3 = "#58A6FF", "#39D0D8", "#A371F7"
TXT, MUT = "#E6EDF3", "#8B949E"
SANS = "ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,Consolas,monospace"


def sine_path(x0, x1, y, amp, period, phase=0.0, step=4):
    """Smooth sine polyline; extends past x1 so a -period translate loops seamlessly."""
    pts = []
    x = x0
    while x <= x1:
        pts.append(f"{x:.1f},{y + amp * math.sin(2 * math.pi * (x / period) + phase):.1f}")
        x += step
    return "M" + " L".join(pts)


def field(cx0, cy0, w, h, nwaves=7, period=190, seed=0):
    """Stacked sine contours = the 'PDE solution field' motif."""
    out = []
    for i in range(nwaves):
        t = i / (nwaves - 1)
        y = cy0 + t * h
        amp = 10 + 20 * math.sin(math.pi * t)
        op = 0.16 + 0.60 * math.sin(math.pi * t) ** 1.4
        col = [A1, A2, A3][i % 3]
        d = sine_path(cx0 - 10, cx0 + w + period + 20, y, amp, period, phase=seed + i * 0.55)
        dur = 9 + i * 1.3
        out.append(
            f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op:.2f}" '
            f'stroke-width="{1.6 if i % 2 else 1.1:.1f}" stroke-linecap="round">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="0 0" to="-{period} 0" dur="{dur:.1f}s" repeatCount="indefinite"/></path>'
        )
    return "".join(out)


def mesh(cx0, cy0, w, h, cols=5, rows=4):
    """Neural-mesh nodes + edges layered over the field."""
    pts = []
    for r in range(rows):
        for c in range(cols):
            jx = 9 * math.sin(r * 2.1 + c * 1.3)
            jy = 7 * math.cos(c * 1.7 + r * 0.9)
            pts.append((cx0 + (c + 0.5) * w / cols + jx, cy0 + (r + 0.5) * h / rows + jy))
    edges, nodes = [], []
    for i, (x1, y1) in enumerate(pts):
        for j, (x2, y2) in enumerate(pts):
            if j <= i:
                continue
            if math.hypot(x2 - x1, y2 - y1) < w / cols * 1.45:
                edges.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{A1}" stroke-opacity="0.18" stroke-width="0.9"/>'
                )
    for i, (x, y) in enumerate(pts):
        col = [A1, A2, A3][i % 3]
        d = 2.6 + (i % 5) * 0.5
        nodes.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{d:.1f}" fill="{col}" fill-opacity="0.9" filter="url(#soft)">'
            f'<animate attributeName="r" values="{d:.1f};{d + 1.6:.1f};{d:.1f}" '
            f'dur="{2.8 + (i % 7) * 0.4:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="fill-opacity" values="0.9;0.35;0.9" '
            f'dur="{2.8 + (i % 7) * 0.4:.1f}s" repeatCount="indefinite"/></circle>'
        )
    return "".join(edges) + "".join(nodes)


def chips(items, x, y, fs=13):
    """Rounded 'stack chip' pills with measured widths."""
    out, cx = [], x
    for label in items:
        w = len(label) * fs * 0.62 + 26
        out.append(
            f'<g><rect x="{cx:.0f}" y="{y}" rx="13" ry="13" width="{w:.0f}" height="26" '
            f'fill="#161B22" stroke="#30363D" stroke-width="1"/>'
            f'<text x="{cx + w / 2:.0f}" y="{y + 17.5}" font-family="{MONO}" font-size="{fs}" '
            f'fill="{MUT}" text-anchor="middle" letter-spacing="0.3">{label}</text></g>'
        )
        cx += w + 9
    return "".join(out)


def defs(W):
    return f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="{BG0}"/><stop offset="55%" stop-color="#0B0F15"/><stop offset="100%" stop-color="{BG1}"/>
</linearGradient>
<linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#FFFFFF"/><stop offset="45%" stop-color="{A1}"/>
  <stop offset="78%" stop-color="{A2}"/><stop offset="100%" stop-color="{A3}"/>
</linearGradient>
<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="{A1}" stop-opacity="0"/><stop offset="22%" stop-color="{A1}"/>
  <stop offset="55%" stop-color="{A2}"/><stop offset="82%" stop-color="{A3}"/>
  <stop offset="100%" stop-color="{A3}" stop-opacity="0"/>
</linearGradient>
<radialGradient id="glowR" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="{A2}" stop-opacity="0.20"/><stop offset="100%" stop-color="{A2}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowL" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="{A3}" stop-opacity="0.16"/><stop offset="100%" stop-color="{A3}" stop-opacity="0"/>
</radialGradient>
<pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">
  <path d="M34 0 L0 0 0 34" fill="none" stroke="#1F2430" stroke-width="1"/>
</pattern>
<filter id="soft" x="-80%" y="-80%" width="260%" height="260%">
  <feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
</defs>"""


def build(W, H, vx, vy, vw, vh, tx, name_size, sub_size, chip_items,
          y_eyebrow, y_name, y_sub, y_tag, y_chips,
          tagline, eyebrow, sub, clip_id="vclip"):
    ty = y_name
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Edvin Rahnama — Data Scientist and ML Engineer">
{defs(W)}
<clipPath id="{clip_id}"><rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="16"/></clipPath>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.45"/>
<ellipse cx="{vx + vw * 0.55}" cy="{vy + vh * 0.45}" rx="{vw * 0.85}" ry="{vh * 0.95}" fill="url(#glowR)"/>
<ellipse cx="{tx + 40}" cy="{ty + 30}" rx="360" ry="200" fill="url(#glowL)"/>
<g clip-path="url(#{clip_id})">
  <rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="16" fill="#0B0F16" fill-opacity="0.55"/>
  {field(vx, vy + 18, vw, vh - 36)}
  {mesh(vx, vy, vw, vh)}
</g>
<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="16" fill="none" stroke="#21262D" stroke-width="1"/>

<text x="{tx}" y="{y_eyebrow}" font-family="{MONO}" font-size="13" fill="{A2}" letter-spacing="3.4">{eyebrow}</text>
<text x="{tx}" y="{y_name}" font-family="{SANS}" font-size="{name_size}" font-weight="800" fill="url(#name)" letter-spacing="-1.6">EDVIN RAHNAMA</text>
<text x="{tx}" y="{y_sub}" font-family="{SANS}" font-size="{sub_size}" font-weight="500" fill="{TXT}" fill-opacity="0.92">{sub}</text>
<text x="{tx}" y="{y_tag}" font-family="{SANS}" font-size="{sub_size - 4}" fill="{MUT}">{tagline}</text>
{chips(chip_items, tx, y_chips)}

<rect x="0" y="{H - 5}" width="{W}" height="5" fill="url(#bar)">
  <animate attributeName="opacity" values="0.6;1;0.6" dur="4.5s" repeatCount="indefinite"/>
</rect>
</svg>"""


# ---- README hero: 1280 x 360 ----
hero = build(
    W=1280, H=360, vx=812, vy=52, vw=404, vh=256, tx=64,
    name_size=56, sub_size=20,
    y_eyebrow=100, y_name=160, y_sub=198, y_tag=230, y_chips=258,
    chip_items=["Python", "PyTorch", "AWS", "Docker", "Kubernetes", "Terraform"],
    eyebrow="DATA SCIENTIST &#183; ML ENGINEER &#183; KIEL, DE",
    sub="Physics-Informed Neural Networks &#183; MLOps on AWS",
    tagline="M.Sc. Data Science &#183; Helmholtz-Zentrum Hereon &#183; t2consult",
)
open(os.path.join(OUT, "hero.svg"), "w", encoding="utf-8").write(hero)

# ---- LinkedIn cover: 1584 x 396 (photo overlaps bottom-left ~ x<300, y>210) ----
banner = build(
    W=1584, H=396, vx=1074, vy=58, vw=452, vh=268, tx=350,
    name_size=60, sub_size=21,
    y_eyebrow=122, y_name=186, y_sub=226, y_tag=260, y_chips=288,
    chip_items=["Python", "PyTorch", "AWS", "Docker", "MLOps"],
    eyebrow="DATA SCIENTIST &#183; ML ENGINEER &#183; KIEL, GERMANY",
    sub="Physics-Informed Neural Networks &#183; MLOps on AWS",
    tagline="edvin-rahnama.space",
    clip_id="bclip",
)
open(os.path.join(OUT, "linkedin-banner.svg"), "w", encoding="utf-8").write(banner)

print("wrote:", os.listdir(OUT))
