#!/usr/bin/env python3
"""Generate the site's brand assets: favicons and per-post hero images.

Run from the repo root:  python3 tools/gen-assets.py

Heroes are self-made abstract art (no licensing to track — see
assets/synapse/CREDITS.md for the rule). One PNG per post serves as both the
on-page hero and the og:image for social cards, so there is exactly one file
per post to keep track of. The on-page fade-out is a CSS mask, not baked in.

Hue comes from the post slug by default, so a new post gets a hero with no
config at all. Override with `hero_hue: 205` in the post's frontmatter when the
generated colour fights the subject.

Assets are committed. Re-run only when adding a post or changing the design;
existing heroes are left alone unless --force is passed.
"""

import colorsys
import hashlib
import math
import random
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
HERO_DIR = ROOT / "assets" / "heroes"
ASSET_DIR = ROOT / "assets"
POST_DIRS = [ROOT / "_tech", ROOT / "_synapse"]

# 1.90:1 — inside og:image's 1.91:1 recommendation, and 2x the 800px column.
HERO_W, HERO_H = 1600, 840

# Hues are picked from this ring rather than straight off the hash. A raw
# `hash % 360` clustered three of six Synapse posts in the same violet and put
# the tech post in maroon; these eight are spaced and all sit in the cool
# editorial family the rest of the site uses (plus two warms for contrast).
HUE_RING = [205, 190, 258, 32, 168, 285, 222, 12]

# The three landing pages aren't posts, so they get their heroes named here.
# These double as the og:image for /, /tech and /synapse.
PAGE_HEROES = {"home": 205, "tech": 222, "synapse": 258}

# Posts whose own lead image is strong enough to be the hero. Cropped to the
# hero aspect here rather than left to CSS object-fit, so the og:image is a
# real 1.9:1 card — and re-encoded to JPEG because LinkedIn's crawler does not
# reliably render the WebP originals. Provenance for every source is in
# assets/synapse/CREDITS.md.
# slug -> (source file under assets/synapse/, vertical focal point 0..1)
PHOTO_HEROES = {
    "enceladus-and-the-erased-origin-of-life": ("enceladus-plume.jpg", 0.5),
    "what-enceladus-doesnt-need": ("enceladus-tiger-stripes.webp", 0.5),
    "geomythology-oral-tradition-as-geological-memory": ("crater-lake.jpg", 0.45),
    "culture-anthropology-marketing": ("iceberg-underside.webp", 0.5),
}

FAVICON_TEXT = "வி"
FAVICON_FONT = "/System/Library/Fonts/Supplemental/Tamil Sangam MN.ttc"
INK = (10, 22, 40)  # --synapse-ink, the deep night blue
GLYPH = (143, 216, 255)  # --synapse-accent in dark, the caption blue


# ---------------------------------------------------------------- heroes


def hsv(h_deg, s, v):
    r, g, b = colorsys.hsv_to_rgb((h_deg % 360) / 360.0, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


def radial_wash(w, h, hue):
    """Two soft glows over a near-black base.

    Painted on a thumbnail and scaled up: a 100x53 loop is instant, and BICUBIC
    upscaling gives a smoother falloff than anything worth hand-rolling at full
    resolution.
    """
    sw, sh = 100, 53
    # The second glow sits 45 degrees away. Which way matters: +45 from a warm
    # base lands on olive and the whole image goes muddy, so warm hues rotate
    # towards rose instead.
    offset = -45 if hue % 360 < 90 else 45
    base = hsv(hue, 0.58, 0.085)
    glow_a = hsv(hue, 0.62, 0.62)
    glow_b = hsv(hue + offset, 0.55, 0.40)

    img = Image.new("RGB", (sw, sh), base)
    px = img.load()
    # (centre x, centre y, radius, colour) in thumbnail space
    lights = [(0.20, -0.10, 0.85, glow_a), (0.86, 0.30, 0.75, glow_b)]

    for y in range(sh):
        for x in range(sw):
            r, g, b = base
            for cx, cy, rad, col in lights:
                dx = (x / sw - cx)
                dy = (y / sh - cy) * (sh / sw)  # keep the glow circular
                d = math.hypot(dx, dy) / rad
                if d >= 1:
                    continue
                # smoothstep falloff — no hard rim
                t = (1 - d) ** 2
                t = t * t * (3 - 2 * t)
                r = min(255, int(r + col[0] * t))
                g = min(255, int(g + col[1] * t))
                b = min(255, int(b + col[2] * t))
            px[x, y] = (r, g, b)

    return img.resize((w, h), Image.BICUBIC)


def network_motif(w, h, hue, rng):
    """A sparse node-and-edge figure — the synapse, drawn faintly.

    Same construction on every post so the series reads as one thing; the seed
    moves the nodes so no two are the same picture.
    """
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    line = hsv(hue, 0.25, 1.0)

    nodes = []
    for _ in range(7):
        nodes.append((rng.uniform(0.08, 0.95) * w, rng.uniform(0.12, 0.92) * h))

    # Edges: each node to its nearest two neighbours. Enough structure to read
    # as a network, sparse enough to stay background.
    for i, a in enumerate(nodes):
        others = sorted(
            (j for j in range(len(nodes)) if j != i),
            key=lambda j: math.dist(a, nodes[j]),
        )[:2]
        for j in others:
            d.line([a, nodes[j]], fill=line + (26,), width=2)

    for x, y in nodes:
        r = rng.uniform(3, 7)
        d.ellipse([x - r, y - r, x + r, y + r], fill=line + (70,))

    # One node gets concentric rings — the firing one.
    hx, hy = nodes[0]
    for k in range(1, 6):
        r = k * rng.uniform(52, 68)
        d.ellipse([hx - r, hy - r, hx + r, hy + r], outline=line + (30 - k * 4,), width=2)

    return layer.filter(ImageFilter.GaussianBlur(0.6))


def grain(w, h, strength=7):
    """Fine noise. Without it, smooth gradients band badly once PNG-quantised."""
    n = Image.effect_noise((w, h), strength).convert("L")
    return Image.merge("RGB", (n, n, n))


def make_hero(slug, hue, out):
    rng = random.Random(slug)
    img = radial_wash(HERO_W, HERO_H, hue)
    img = Image.alpha_composite(
        img.convert("RGBA"), network_motif(HERO_W, HERO_H, hue, rng)
    ).convert("RGB")
    # Just enough grain to break up the gradient. More than this and the noise
    # stops compressing — it was the whole reason these were 300KB.
    img = Image.blend(img, grain(HERO_W, HERO_H), 0.022)
    img.convert("P", palette=Image.ADAPTIVE, colors=128).save(out, optimize=True)
    return out.stat().st_size


def make_photo_hero(src, focal, out):
    """Crop a post's own photo to the hero aspect and re-encode as JPEG."""
    img = Image.open(ASSET_DIR / "synapse" / src).convert("RGB")
    w, h = img.size
    target = HERO_W / HERO_H

    if w / h > target:  # too wide — trim the sides, keeping the centre
        new_w = int(h * target)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:  # too tall — trim vertically around the focal point
        new_h = int(w / target)
        top = max(0, min(h - new_h, int(h * focal - new_h / 2)))
        img = img.crop((0, top, w, top + new_h))

    # q78 progressive: the hero is the LCP element, and the detailed textures
    # were landing at ~250KB at higher quality with no visible gain.
    img.resize((HERO_W, HERO_H), Image.LANCZOS).save(
        out, quality=78, optimize=True, progressive=True
    )
    return out.stat().st_size


# ---------------------------------------------------------------- favicons


def make_icon(size):
    """The வி mark, light on deep navy. Rendered to PNG so it never depends on
    the reader's machine having a Tamil font."""
    # Draw at 4x and downsample — cheaper than fighting PIL's hinting at 16px.
    s = size * 4
    img = Image.new("RGB", (s, s), INK)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FAVICON_FONT, int(s * 0.72), index=0)
    box = d.textbbox((0, 0), FAVICON_TEXT, font=font)
    d.text(
        ((s - (box[2] - box[0])) / 2 - box[0], (s - (box[3] - box[1])) / 2 - box[1]),
        FAVICON_TEXT,
        font=font,
        fill=GLYPH,
    )
    return img.resize((size, size), Image.LANCZOS)


# ---------------------------------------------------------------- frontmatter


def posts():
    """(slug, path, frontmatter_text) for every post."""
    for d in POST_DIRS:
        for p in sorted(d.glob("*.md")):
            yield p.stem, p, p.read_text()


def hue_for(slug, fm):
    m = re.search(r"^hero_hue:\s*(\d+)", fm, re.M)
    if m:
        return int(m.group(1))
    # Stable per slug, and picked off the curated ring rather than the raw wheel.
    return HUE_RING[int(hashlib.sha256(slug.encode()).hexdigest()[:4], 16) % len(HUE_RING)]


def main():
    force = "--force" in sys.argv
    HERO_DIR.mkdir(parents=True, exist_ok=True)

    for size, name in [(180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")]:
        make_icon(size).save(ASSET_DIR / name, optimize=True)
        print(f"icon  {name}")
    make_icon(48).save(
        ASSET_DIR / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print("icon  favicon.ico")

    for slug, (src, focal) in PHOTO_HEROES.items():
        out = HERO_DIR / f"{slug}.jpg"
        if out.exists() and not force:
            print(f"skip  {out.name} (exists)")
            continue
        kb = make_photo_hero(src, focal, out) // 1024
        print(f"photo {out.name}  <- {src}  {kb}KB")

    wanted = [(s, hue_for(s, fm)) for s, _, fm in posts() if s not in PHOTO_HEROES]
    wanted += list(PAGE_HEROES.items())

    for slug, hue in wanted:
        out = HERO_DIR / f"{slug}.png"
        if out.exists() and not force:
            print(f"skip  {out.name} (exists)")
            continue
        kb = make_hero(slug, hue, out) // 1024
        print(f"hero  {out.name}  hue={hue}  {kb}KB")


if __name__ == "__main__":
    main()
