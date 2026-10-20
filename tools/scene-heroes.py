#!/usr/bin/env python3
"""Draw the self-made scene heroes with a title block, then render them to PNG.

Each scene is an abstract SVG of the post's subject at 1600x840. The subject
sits on the right. A dark scrim on the left holds a kicker, the title and a
tagline, in the style of the groundgate heroes. Headless Chrome renders each
SVG to assets/synapse/<name>.png, and gen-assets.py turns that PNG into the
post's JPEG hero through PHOTO_HEROES.

Usage: python3 tools/scene-heroes.py [name ...]
"""

import math
import random
import re
import subprocess
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "synapse"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1600, 840

SANS = "-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif"
SERIF = "'Source Serif 4', Charter, Georgia, serif"
FONT_CSS = ("@import url('https://fonts.googleapis.com/css2?family="
            "Source+Serif+4:ital,opsz,wght@1,8..60,400&amp;display=swap');")


# ---------------------------------------------------------------- helpers


def stars(rng, n, x0=0, x1=W, y0=0, y1=H, color="#dfe6ff", rmax=1.4):
    out = []
    for _ in range(n):
        out.append(f'<circle cx="{rng.uniform(x0, x1):.0f}" cy="{rng.uniform(y0, y1):.0f}" '
                   f'r="{rng.uniform(0.5, rmax):.1f}" fill="{color}" '
                   f'opacity="{rng.uniform(0.2, 0.7):.2f}"/>')
    return "\n".join(out)


def vgrad(gid, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="{H}" '
            f'gradientUnits="userSpaceOnUse">{s}</linearGradient>')


def glow(gid, cx, cy, r, color, op):
    return (f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')


def wrap(text, size, width, em=0.5):
    cap = max(8, int(width / (em * size)))
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if len(trial) <= cap or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    if cap > 8 and len(lines) > 1:
        # Shorten the cap while the line count holds, so lines come out even.
        tighter = wrap(text, size, width * (cap - 1) / cap, em)
        if len(tighter) == len(lines):
            return tighter
    return lines


def title_block(kicker, title, tagline):
    for size in (66, 60, 56, 52, 48):
        lines = wrap(title, size, 660)
        if len(lines) <= 3:
            break
    lead = size * 1.1
    tag = wrap(tagline, 31, 660, em=0.43)
    block_h = 34 + len(lines) * lead + 24 + len(tag) * 42
    y = (H - block_h) / 2 + 22
    parts = [f'<text x="110" y="{y:.0f}" font-family="{SANS}" font-size="21" font-weight="600" '
             f'letter-spacing="3.5" fill="#8fd8ff">{escape(kicker.upper())}</text>']
    y += 34 + size * 0.86
    for line in lines:
        parts.append(f'<text x="108" y="{y:.0f}" font-family="{SANS}" font-size="{size}" '
                     f'font-weight="700" letter-spacing="-1" fill="#ffffff">{escape(line)}</text>')
        y += lead
    y += 24 + 31 * 0.86 - lead + size * 0.3
    for line in tag:
        parts.append(f'<text x="110" y="{y:.0f}" font-family="{SERIF}" font-size="31" '
                     f'font-style="italic" fill="#d9def0">{escape(line)}</text>')
        y += 42
    return "\n".join(parts)


def page(defs, body, kicker, title, tagline):
    scrim = ('<linearGradient id="scrim" x1="0" y1="0" x2="1100" y2="0" gradientUnits="userSpaceOnUse">'
             '<stop offset="0" stop-color="#050a18" stop-opacity="0.92"/>'
             '<stop offset="0.5" stop-color="#050a18" stop-opacity="0.72"/>'
             '<stop offset="1" stop-color="#050a18" stop-opacity="0"/></linearGradient>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
            f'<style>{FONT_CSS}</style>\n<defs>\n{defs}\n{scrim}\n'
            '<filter id="soft" x="-50%" y="-50%" width="200%" height="200%">'
            '<feGaussianBlur stdDeviation="3"/></filter>\n'
            '<filter id="blur12" x="-50%" y="-50%" width="200%" height="200%">'
            '<feGaussianBlur stdDeviation="12"/></filter>\n</defs>\n'
            f'{body}\n<rect width="{W}" height="{H}" fill="url(#scrim)"/>\n'
            f'{title_block(kicker, title, tagline)}\n</svg>\n')


# ---------------------------------------------------------------- scenes


def apollo(rng):
    defs = "\n".join([
        vgrad("sky", [(0, "#03050c"), (1, "#0e1426")]),
        glow("sun", 1250, 300, 190, "#ffd38a", 0.55),
        glow("pool", 1235, 640, 150, "#fff4d6", 0.7),
        vgrad("ground", [(0.7, "#5b5f69"), (1, "#24262d")]),
    ])
    body = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>', stars(rng, 220)]
    body.append('<circle cx="1250" cy="300" r="190" fill="url(#sun)"/>')
    body.append('<circle cx="1250" cy="300" r="46" fill="#ffe2a8"/>')
    for i, (rx, ry, op) in enumerate([(300, 70, 0.35), (250, 56, 0.25), (350, 84, 0.18)]):
        body.append(f'<ellipse cx="1250" cy="300" rx="{rx}" ry="{ry}" fill="none" stroke="#c98a52" '
                    f'stroke-width="{10 - 3 * i}" opacity="{op}" transform="rotate(-12 1250 300)" filter="url(#soft)"/>')
    for _ in range(160):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(220, 360)
        x, y = 1250 + rr * math.cos(a), 300 + rr * 0.23 * math.sin(a)
        xr = 1250 + (x - 1250) * math.cos(-0.21) - (y - 300) * math.sin(-0.21)
        yr = 300 + (x - 1250) * math.sin(-0.21) + (y - 300) * math.cos(-0.21)
        body.append(f'<circle cx="{xr:.0f}" cy="{yr:.0f}" r="{rng.uniform(0.8, 2.2):.1f}" '
                    f'fill="#e0a868" opacity="{rng.uniform(0.2, 0.6):.2f}"/>')
    body.append('<path d="M0 640 Q800 560 1600 600 L1600 840 L0 840 Z" fill="url(#ground)"/>')
    for _ in range(26):
        cx, cy = rng.uniform(560, 1600), rng.uniform(650, 830)
        rx = rng.uniform(14, 60)
        body.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{rx * 0.22:.0f}" '
                    f'fill="#1d1f25" opacity="0.55"/>'
                    f'<ellipse cx="{cx:.0f}" cy="{cy - rx * 0.06:.0f}" rx="{rx:.0f}" ry="{rx * 0.2:.0f}" '
                    f'fill="none" stroke="#8a8e98" stroke-width="1.2" opacity="0.35"/>')
    body.append('<ellipse cx="1235" cy="660" rx="260" ry="62" fill="url(#pool)"/>')
    body.append('<path d="M1188 664 L1196 632 L1222 618 L1258 622 L1280 640 L1276 664 Z" fill="#3a3c44"/>'
                '<path d="M1196 632 L1222 618 L1258 622 L1240 640 Z" fill="#9a9ea8"/>'
                '<path d="M1258 622 L1280 640 L1276 664 L1250 650 Z" fill="#6a6e78"/>')
    body.append('<circle cx="1236" cy="636" r="70" fill="url(#pool)" opacity="0.5"/>')
    return defs, "\n".join(body)


def boston(rng):
    defs = "\n".join([
        vgrad("sky", [(0, "#070d1c"), (0.62, "#1b2a46"), (1, "#1b2a46")]),
        vgrad("sea", [(0.6, "#0f1c30"), (1, "#060b16")]),
        glow("moon", 1450, 150, 160, "#e8eefc", 0.35),
    ])
    body = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>', stars(rng, 120, y1=480)]
    body.append('<circle cx="1450" cy="150" r="160" fill="url(#moon)"/><circle cx="1450" cy="150" r="26" fill="#eef2fb"/>')
    x = 700
    while x < W:
        w, h = rng.uniform(24, 70), rng.uniform(16, 60)
        body.append(f'<rect x="{x:.0f}" y="{520 - h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#24324d" opacity="0.8"/>')
        x += w + rng.uniform(0, 8)
    body.append('<rect x="0" y="520" width="1600" height="320" fill="url(#sea)"/>')
    for _ in range(90):
        y = rng.uniform(530, 840)
        x0 = rng.uniform(0, 1600)
        body.append(f'<line x1="{x0:.0f}" y1="{y:.0f}" x2="{x0 + rng.uniform(20, 90):.0f}" y2="{y:.0f}" '
                    f'stroke="#9fb4d8" stroke-width="1" opacity="{0.06 + (y - 520) / 320 * 0.12:.2f}"/>')
    for sx, s in [(930, 0.75), (1170, 1.0), (1420, 0.85)]:
        base = 560 + 30 * s
        body.append(f'<g transform="translate({sx} {base}) scale({s})" fill="#050912">'
                    '<path d="M-140 0 L140 0 L115 34 L-120 34 Z"/>'
                    '<rect x="-62" y="-210" width="5" height="210"/><rect x="18" y="-250" width="6" height="250"/>'
                    '<rect x="88" y="-170" width="4" height="170"/>'
                    '<path d="M-100 -150 L-20 -150 L-24 -60 L-96 -60 Z" opacity="0.85"/>'
                    '<path d="M-20 -200 L70 -200 L66 -70 L-16 -70 Z" opacity="0.85"/>'
                    '<path d="M60 -130 L120 -130 L116 -50 L64 -50 Z" opacity="0.85"/>'
                    '<line x1="24" y1="-250" x2="140" y2="0" stroke="#050912" stroke-width="1.5"/>'
                    '<line x1="-60" y1="-210" x2="-140" y2="0" stroke="#050912" stroke-width="1.5"/></g>')
        body.append(f'<rect x="{sx - 110 * s:.0f}" y="{base + 34 * s:.0f}" width="{230 * s:.0f}" height="6" '
                    'fill="#2a3a58" opacity="0.4" filter="url(#soft)"/>')
    for _ in range(14):
        cx, cy = rng.uniform(820, 1560), rng.uniform(650, 800)
        body.append(f'<ellipse cx="{cx:.0f}" cy="{cy + 6:.0f}" rx="{rng.uniform(50, 110):.0f}" ry="{rng.uniform(10, 22):.0f}" '
                    'fill="#8a5426" opacity="0.38" filter="url(#blur12)"/>')
    for _ in range(11):
        cx, cy = rng.uniform(840, 1540), rng.uniform(640, 790)
        s = 14 + (cy - 640) / 150 * 14
        body.append(f'<g transform="translate({cx:.0f} {cy:.0f}) rotate({rng.uniform(-30, 30):.0f})">'
                    f'<rect x="{-s:.0f}" y="{-s * 0.7:.0f}" width="{2 * s:.0f}" height="{1.4 * s:.0f}" fill="#6b4422" stroke="#c08a50" stroke-width="1.5"/>'
                    f'<line x1="{-s:.0f}" y1="0" x2="{s:.0f}" y2="0" stroke="#c08a50" stroke-width="1"/></g>')
    return defs, "\n".join(body)


def delaware(rng):
    defs = "\n".join([
        vgrad("sky", [(0, "#081022"), (1, "#101c34")]),
        glow("court", 1240, 420, 230, "#ffcf7a", 0.45),
    ])
    body = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    for gx in range(0, W, 80):
        body.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="#2a3a5c" stroke-width="1" opacity="0.25"/>')
    for gy in range(0, H, 80):
        body.append(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="#2a3a5c" stroke-width="1" opacity="0.25"/>')
    body.append('<path d="M1060 0 L1080 60 C1150 140 1120 230 1170 300 C1220 380 1300 420 1330 500 C1360 590 1310 680 '
                '1360 760 L1380 840 L1600 840 L1600 0 Z" fill="#163128" opacity="0.85"/>'
                '<path d="M1060 0 L1080 60 C1150 140 1120 230 1170 300 C1220 380 1300 420 1330 500 C1360 590 1310 680 '
                '1360 760 L1380 840" fill="none" stroke="#4f8a70" stroke-width="2" opacity="0.6"/>')
    for _ in range(46):
        sx, sy = rng.uniform(0, 1600), rng.choice([rng.uniform(0, 120), rng.uniform(720, 840), rng.uniform(0, 840)])
        if abs(sx - 1240) < 260 and abs(sy - 420) < 200:
            continue
        mx, my = (sx + 1240) / 2 + rng.uniform(-160, 160), (sy + 420) / 2 + rng.uniform(-160, 160)
        body.append(f'<path d="M{sx:.0f} {sy:.0f} Q{mx:.0f} {my:.0f} 1240 430" fill="none" stroke="#f0c070" '
                    f'stroke-width="{rng.uniform(0.8, 1.8):.1f}" opacity="{rng.uniform(0.15, 0.4):.2f}"/>'
                    f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="3" fill="#f0c070" opacity="0.5"/>')
    body.append('<circle cx="1240" cy="420" r="230" fill="url(#court)"/>')
    body.append('<g transform="translate(1240 430)" fill="#fbe6b8">'
                '<path d="M-110 -70 L0 -125 L110 -70 Z"/><rect x="-115" y="-66" width="230" height="12"/>'
                + "".join(f'<rect x="{-100 + i * 44}" y="-48" width="16" height="104"/>' for i in range(5)) +
                '<rect x="-122" y="58" width="244" height="12"/><rect x="-136" y="72" width="272" height="12"/></g>')
    return defs, "\n".join(body)


def genome(rng):
    defs = "\n".join([vgrad("sky", [(0, "#070c1c"), (1, "#130f2a")])])
    body = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>', stars(rng, 80, color="#b9c6ff")]

    def cy(x):
        if x < 1150:
            return 190 + (x - 760) * 0.28
        t = (x - 1150) / 410
        return 299 + 470 * (1 - (1 - t) ** 2.2) if t <= 1 else 769

    body.append('<line x1="760" y1="190" x2="1560" y2="470" stroke="#7aa8ff" stroke-width="3" '
                'stroke-dasharray="14 10" opacity="0.75"/>')
    body.append('<line x1="1150" y1="120" x2="1150" y2="800" stroke="#c9d3f5" stroke-width="1.5" '
                'stroke-dasharray="3 7" opacity="0.4"/>')
    a, strand1, strand2, rungs = 26, [], [], []
    x = 760
    while x <= 1560:
        ph = x / 34.0
        c = cy(x)
        y1, y2 = c + a * math.sin(ph), c - a * math.sin(ph)
        strand1.append(f"{x:.0f},{y1:.1f}")
        strand2.append(f"{x:.0f},{y2:.1f}")
        if int(x) % 18 == 0:
            rungs.append(f'<line x1="{x:.0f}" y1="{y1:.1f}" x2="{x:.0f}" y2="{y2:.1f}" stroke="#e7d8ff" '
                         'stroke-width="2" opacity="0.35"/>')
        x += 3
    body += rungs
    body.append(f'<polyline points="{" ".join(strand1)}" fill="none" stroke="#54e0c8" stroke-width="5" stroke-linecap="round"/>')
    body.append(f'<polyline points="{" ".join(strand2)}" fill="none" stroke="#ff6fb4" stroke-width="5" stroke-linecap="round"/>')
    return defs, "\n".join(body)


def gpu(rng):
    defs = "\n".join([
        vgrad("sky", [(0, "#05080f"), (1, "#0b1220")]),
        glow("near", 1450, 450, 420, "#3fb7ff", 0.22),
    ])
    body = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
            '<circle cx="1450" cy="450" r="420" fill="url(#near)"/>',
            '<path d="M760 840 L1100 470 L1600 470 L1600 840 Z" fill="#0c1424" opacity="0.8"/>']
    vx, vy = 1020, 400
    for i in reversed(range(12)):
        s = 0.92 ** (i * 2.2)
        x = vx + (1520 - vx) * s
        hgt = 560 * s
        wdt = 150 * s
        top = vy - hgt * 0.42
        warm = 1 - i / 11
        body.append(f'<rect x="{x - wdt:.1f}" y="{top:.1f}" width="{wdt:.1f}" height="{hgt:.1f}" '
                    f'fill="#141c2c" stroke="#3b4d6e" stroke-width="{max(0.5, 2 * s):.1f}" opacity="{0.45 + 0.55 * warm:.2f}"/>')
        rows = 14
        for r in range(rows):
            ry = top + hgt * (r + 0.6) / (rows + 0.4)
            for k in range(3):
                lx = x - wdt + wdt * (0.2 + 0.25 * k)
                col = "#5cf0a8" if rng.random() < 0.6 else "#5cc8ff"
                if rng.random() < 0.7:
                    body.append(f'<rect x="{lx:.1f}" y="{ry:.1f}" width="{max(0.8, 6 * s):.1f}" '
                                f'height="{max(0.6, 3 * s):.1f}" fill="{col}" opacity="{0.08 + 0.85 * warm ** 1.6:.2f}"/>')
    return defs, "\n".join(body)


def sun(rng):
    defs = "\n".join([
        vgrad("sky", [(0, "#1a2338"), (0.66, "#7d8aa3"), (1, "#7d8aa3")]),
        glow("halo", 1260, 230, 220, "#fff6dc", 0.55),
        vgrad("ice", [(0.66, "#c7d4e4"), (1, "#8597b0")]),
    ])
    body = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
            '<circle cx="1260" cy="230" r="220" fill="url(#halo)"/><circle cx="1260" cy="230" r="78" fill="#fff8e6"/>',
            '<path d="M0 555 Q800 535 1600 560 L1600 840 L0 840 Z" fill="url(#ice)"/>']
    for _ in range(18):
        x0, y0 = rng.uniform(700, 1600), rng.uniform(600, 840)
        pts = [f"{x0:.0f},{y0:.0f}"]
        for _ in range(4):
            x0 += rng.uniform(20, 70)
            y0 += rng.uniform(-12, 12)
            pts.append(f"{x0:.0f},{y0:.0f}")
        body.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#6f84a3" stroke-width="1" opacity="0.5"/>')

    def tree(x, y, h, depth=0):
        out = []
        ang = -math.pi / 2

        def br(x, y, ang, ln, d):
            if d > 5 or ln < 4:
                return
            x2, y2 = x + ln * math.cos(ang), y + ln * math.sin(ang)
            out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#2a2f3c" '
                       f'stroke-width="{max(1, 7 - d * 1.4):.1f}" stroke-linecap="round"/>')
            for da in (-0.45, 0.4):
                br(x2, y2, ang + da + rng.uniform(-0.15, 0.15), ln * rng.uniform(0.62, 0.75), d + 1)
        br(x, y, ang, h, 0)
        return "\n".join(out)

    for tx, th in [(780, 120), (1520, 140), (1580, 90), (860, 80)]:
        body.append(tree(tx, 555, th))
    for _ in range(9):
        tx, ty = rng.uniform(880, 1500), rng.uniform(600, 700)
        s = 0.7 + (ty - 600) / 100 * 0.6
        col = rng.choice(["#8a3b3b", "#3e5a7a", "#7a6a3b", "#5a3b6a"])
        body.append(f'<path d="M{tx - 28 * s:.0f} {ty:.0f} L{tx:.0f} {ty - 40 * s:.0f} L{tx + 28 * s:.0f} {ty:.0f} Z" fill="{col}"/>'
                    f'<line x1="{tx:.0f}" y1="{ty - 40 * s:.0f}" x2="{tx:.0f}" y2="{ty - 52 * s:.0f}" stroke="#2a2f3c" stroke-width="1.5"/>')
    for _ in range(36):
        px, py = rng.uniform(820, 1560), rng.uniform(640, 800)
        s = 0.6 + (py - 640) / 160 * 0.7
        body.append(f'<circle cx="{px:.0f}" cy="{py - 18 * s:.0f}" r="{3.2 * s:.1f}" fill="#262a36"/>'
                    f'<path d="M{px - 4 * s:.0f} {py:.0f} L{px:.0f} {py - 15 * s:.0f} L{px + 4 * s:.0f} {py:.0f} Z" fill="#262a36"/>')
    for _ in range(140):
        body.append(f'<circle cx="{rng.uniform(0, 1600):.0f}" cy="{rng.uniform(0, 840):.0f}" r="{rng.uniform(0.8, 2):.1f}" '
                    f'fill="#ffffff" opacity="{rng.uniform(0.3, 0.7):.2f}"/>')
    return defs, "\n".join(body)


def disruption(rng):
    defs = "\n".join([
        vgrad("sky", [(0, "#06091a"), (1, "#0d1428")]),
        '<linearGradient id="b1" x1="1500" y1="0" x2="1230" y2="640" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#ff9a4a" stop-opacity="0.75"/><stop offset="1" stop-color="#ff9a4a" stop-opacity="0.1"/></linearGradient>',
        '<linearGradient id="b2" x1="1600" y1="480" x2="1230" y2="640" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#46e0d0" stop-opacity="0.75"/><stop offset="1" stop-color="#46e0d0" stop-opacity="0.1"/></linearGradient>',
        '<linearGradient id="b3" x1="980" y1="0" x2="900" y2="560" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#b48cff" stop-opacity="0.7"/><stop offset="1" stop-color="#b48cff" stop-opacity="0.08"/></linearGradient>',
    ])
    body = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>', stars(rng, 90, y1=420),
            '<rect x="0" y="420" width="1600" height="420" fill="#0a0f1c"/>',
            '<path d="M1150 420 L1190 420 L1480 840 L860 840 Z" fill="#1a2132"/>']
    for i in range(9):
        t0, t1 = (i / 9) ** 1.6, ((i + 0.5) / 9) ** 1.6
        y0, y1 = 420 + 420 * t0, 420 + 420 * t1
        w0, w1 = 2 + 10 * t0, 2 + 10 * t1
        x0, x1 = 1170 + (1170 - 1170) * t0, 1170
        body.append(f'<path d="M{1170 - w0 / 2:.0f} {y0:.0f} L{1170 + w0 / 2:.0f} {y0:.0f} L{1170 + w1 / 2:.0f} {y1:.0f} '
                    f'L{1170 - w1 / 2:.0f} {y1:.0f} Z" fill="#c9cfdc" opacity="0.5"/>')
    body.append('<path d="M1430 0 L1560 0 L1270 640 L1190 640 Z" fill="url(#b1)" opacity="0.6"/>')
    body.append('<path d="M1600 420 L1600 540 L1280 670 L1260 610 Z" fill="url(#b2)" opacity="0.6"/>')
    body.append('<path d="M930 0 L1040 0 L960 560 L880 560 Z" fill="url(#b3)" opacity="0.55"/>')
    body.append('<ellipse cx="920" cy="560" rx="70" ry="12" fill="#b48cff" opacity="0.35" filter="url(#soft)"/>')
    body.append('<ellipse cx="1232" cy="650" rx="120" ry="22" fill="#fff0d0" opacity="0.35" filter="url(#blur12)"/>')
    body.append('<g transform="translate(1232 640)">'
                '<path d="M-70 0 L-70 -24 Q-62 -30 -40 -32 L-24 -54 Q-18 -60 -6 -60 L28 -60 Q40 -60 46 -52 L62 -32 '
                'Q74 -30 74 -22 L74 0 Z" fill="#eef1f8"/>'
                '<path d="M-18 -52 L-6 -54 L26 -54 L40 -34 L-32 -34 Z" fill="#1a2132"/>'
                '<circle cx="-40" cy="2" r="13" fill="#0a0f1c"/><circle cx="44" cy="2" r="13" fill="#0a0f1c"/>'
                '<circle cx="-40" cy="2" r="5" fill="#8f97a8"/><circle cx="44" cy="2" r="5" fill="#8f97a8"/></g>')
    return defs, "\n".join(body)


def turing(rng):
    defs = "\n".join([
        vgrad("sky", [(0, "#0d0820"), (1, "#1a1036")]),
        glow("g1", 1010, 400, 200, "#ffd27a", 0.35),
        glow("g2", 1390, 400, 200, "#ffd27a", 0.35),
        '<radialGradient id="metal" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#ffe7a8"/>'
        '<stop offset="0.6" stop-color="#d8a74a"/><stop offset="1" stop-color="#8a6420"/></radialGradient>',
    ])
    body = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    nodes = [(rng.uniform(760, 1600), rng.uniform(80, 800)) for _ in range(44)]
    for i, (x, y) in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            x2, y2 = nodes[j]
            if math.hypot(x - x2, y - y2) < 150:
                body.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#7d6bd6" stroke-width="1" opacity="0.35"/>')
    for x, y in nodes:
        body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.5" fill="#a99bff" opacity="0.7"/>')
    body.append('<path d="M1120 400 C1160 300 1240 500 1280 400" fill="none" stroke="#ffd27a" stroke-width="3" opacity="0.85"/>'
                '<circle cx="1160" cy="365" r="5" fill="#ffd27a"/><circle cx="1240" cy="435" r="5" fill="#ffd27a"/>')
    for cx, gid in [(1010, "g1"), (1390, "g2")]:
        body.append(f'<circle cx="{cx}" cy="400" r="200" fill="url(#{gid})"/>'
                    f'<line x1="{cx}" y1="140" x2="{cx}" y2="292" stroke="#c9a0ff" stroke-width="3" opacity="0.6"/>'
                    f'<circle cx="{cx}" cy="400" r="108" fill="url(#metal)"/>'
                    f'<circle cx="{cx}" cy="400" r="96" fill="none" stroke="#fff1c8" stroke-width="2" opacity="0.6"/>')
    trace = []
    for k in range(9):
        y = 340 + k * 15
        x0 = 1010 - math.sqrt(max(0, 80 ** 2 - (y - 400) ** 2))
        x1 = 1010 + math.sqrt(max(0, 80 ** 2 - (y - 400) ** 2))
        mid = rng.uniform(x0 + 20, x1 - 20)
        trace.append(f'<polyline points="{x0:.0f},{y} {mid:.0f},{y} {mid + 8:.0f},{y + 7} {x1:.0f},{y + 7}" '
                     'fill="none" stroke="#7a5512" stroke-width="2"/>'
                     f'<circle cx="{mid:.0f}" cy="{y}" r="3" fill="#7a5512"/>')
    body += trace
    leaves = []
    for side in (-1, 1):
        for k in range(10):
            a = math.radians(110 + k * 14) if side < 0 else math.radians(70 - k * 14)
            x, y = 1390 + 72 * math.cos(a), 400 + 72 * math.sin(a)
            rot = math.degrees(a) + (90 if side < 0 else -90) - 25 * side
            leaves.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="7" ry="16" fill="#7a5512" '
                          f'transform="rotate({rot:.0f} {x:.0f} {y:.0f})"/>')
    body += leaves
    return defs, "\n".join(body)


def agents(rng):
    defs = "\n".join([
        vgrad("sky", [(0, "#06121a"), (1, "#0b1a2a")]),
        glow("hub", 1300, 440, 220, "#7fe6ff", 0.4),
    ])
    body = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    lanes = [180, 300, 420, 540, 660]
    cols = ["#5ad1b0", "#7fb4ff", "#c79bff", "#ffb86b", "#6fe0ff"]
    for y, c in zip(lanes, cols):
        body.append(f'<path d="M800 {y} L1080 {y} C1180 {y} 1200 440 1300 440" fill="none" stroke="{c}" '
                    'stroke-width="3" opacity="0.75"/>')
        for k in range(4):
            x = 850 + k * 46 + rng.uniform(-12, 12)
            body.append(f'<circle cx="{x:.0f}" cy="{y}" r="7" fill="#06121a" stroke="{c}" stroke-width="3"/>')
        body.append(f'<rect x="1030" y="{y - 16}" width="40" height="32" rx="6" fill="{c}" opacity="0.9"/>')
    body.append('<circle cx="1300" cy="440" r="220" fill="url(#hub)"/>')
    for r, op in [(80, 0.25), (60, 0.4)]:
        body.append(f'<circle cx="1300" cy="440" r="{r}" fill="none" stroke="#bff3ff" stroke-width="2" opacity="{op}"/>')
    body.append('<circle cx="1300" cy="440" r="36" fill="#e9fbff"/>'
                '<line x1="1336" y1="440" x2="1600" y2="440" stroke="#e9fbff" stroke-width="8"/>')
    for k in range(4):
        body.append(f'<circle cx="{1400 + k * 60}" cy="440" r="9" fill="#06121a" stroke="#e9fbff" stroke-width="3"/>')
    return defs, "\n".join(body)


def kurinji(rng):
    src = (OUT / "kurinji-night.svg").read_text()
    inner = re.sub(r"^.*?<svg[^>]*>", "", src, count=1, flags=re.S)
    inner = inner.rsplit("</svg>", 1)[0]
    return "", f"<g>{inner}</g>"


# name, slug, scene, kicker, title, tagline
HEROES = [
    ("apollo-moon-rock", "apollo-first-moon-age", apollo, "Midweek Synapse #8",
     "Apollo's first Moon age came out older than the solar system",
     "The number was impossible. Nobody made a mistake."),
    ("boston-harbor-tea", "boston-tea-party-bailout", boston, "Midweek Synapse #14",
     "The bailout behind the Boston Tea Party", "Cheaper tea, with a tax hidden inside."),
    ("delaware-chancery-lines", "delaware-c-corporation-default", delaware, "Midweek Synapse #10",
     "Why nearly every startup is a Delaware C corporation",
     "The reason sits several steps up the chain of money."),
    ("genome-helix-curve", "genome-sequencing-moores-law", genome, "Midweek Synapse #11",
     "The day genome sequencing outran Moore's Law", "From $95 million to $525, with the break in 2008."),
    ("server-row-fading", "gpu-useful-life-and-the-ai-buildout", gpu, "Midweek Synapse #7",
     "The AI boom runs on a guess about how long a server lasts",
     "One estimate. Amazon shortened it, Meta lengthened it."),
    ("frost-fair-quiet-sun", "the-sun-and-the-little-ice-age", sun, "Midweek Synapse #9",
     "The Sun went quiet for seventy years. The cold lasted five centuries.",
     "The standard story fails on three counts."),
    ("three-beams-road", "three-theories-of-disruption", disruption, "Midweek Synapse #6",
     "Everyone calls it disruptive. Two of three theories agree.",
     "Three fields, three meanings of one word."),
    ("two-medals-network", "turing-nobel-double", turing, "Midweek Synapse #3",
     "Only two people have won both a Turing Award and a Nobel Prize",
     "Two AI researchers, on opposite sides of the field's oldest argument."),
    ("agent-lanes-coordinator", "parallel-coding-agents-authority", agents, "Agent operations",
     "Parallel coding agents fail at authority, not isolation",
     "Every arrow to main passes through one identity."),
    ("kurinji-night-titled", "why-ancient-tamil-love-poems-are-short", kurinji, "Midweek Synapse #21",
     "Why ancient Tamil love poems are so short", "A whole love story in five lines."),
]


def main():
    want = set(sys.argv[1:])
    for name, slug, scene, kicker, title, tagline in HEROES:
        if want and name not in want and slug not in want:
            continue
        defs, body = scene(random.Random(name))
        svg = OUT / f"{name}.svg"
        svg.write_text(page(defs, body, kicker, title, tagline))
        png = OUT / f"{name}.png"
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--disable-gpu",
                        f"--window-size={W},{H}", "--virtual-time-budget=6000",
                        f"--screenshot={png}", svg.as_uri()],
                       check=True, capture_output=True)
        print(f"{png.name}  <- {svg.name}")


if __name__ == "__main__":
    main()
