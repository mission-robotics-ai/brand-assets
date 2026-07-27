#!/usr/bin/env python3
"""Lockups + avatars — composed from the vector mark and the outlined wordmark.

Lockup proportions are measured from the actual signage band (measure script):
  mark is square; gap = 0.327 * mark_height; two-line wordmark ink = 1.245 * mark_height.
Avatar: mark centered in a square with clear space = half mark height.

Run:  python3 build_assets.py
"""
import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
TTF = os.path.join(HERE, "wordmark", "InstrumentSerif-Regular.ttf")
INKS = {"near-black": "#17181a", "cream": "#e8e6dd",
        "green": "#4ADE80", "white": "#ffffff"}

# ---- band-measured ratios ----
GAP_RATIO = 0.327          # gap / mark_height
WM2_RATIO = 1.245          # two-line wordmark ink height / mark_height
LINE_ADV = 960             # baseline-to-baseline (font units), matches band line-height

font = TTFont(TTF)
ASC = font['OS/2'].sTypoAscender
glyphset = font.getGlyphSet()
cmap = font.getBestCmap()
hmtx = font['hmtx']

def mark_dots(hex_ink):
    out = []
    for r in range(7):
        for c in range(7):
            d = math.hypot(r-3, c-3)/math.hypot(3, 3); s = 0.50 + 0.42*(1-d)
            out.append(f'<rect x="{c+0.5-s/2:.4f}" y="{r+0.5-s/2:.4f}" width="{s:.4f}" '
                       f'height="{s:.4f}" rx="{s*0.29:.4f}" fill="{hex_ink}"/>')
    return "".join(out)

def compose_lines(lines):
    """Place glyphs in y-up font coords; return (paths[(d,x,ybaseline)], ink_bbox)."""
    placed = []
    minx = miny = 1e18; maxx = maxy = -1e18
    for i, text in enumerate(lines):
        ybase = -i * LINE_ADV                      # line 0 at 0, line 1 lower (y-up → negative)
        x = 0
        for ch in text:
            g = cmap[ord(ch)]
            spen = SVGPathPen(glyphset); glyphset[g].draw(spen)
            placed.append((spen.getCommands(), x, ybase))
            bp = BoundsPen(glyphset); glyphset[g].draw(bp)
            if bp.bounds:
                x0, y0, x1, y1 = bp.bounds
                minx = min(minx, x0 + x); maxx = max(maxx, x1 + x)
                miny = min(miny, y0 + ybase); maxy = max(maxy, y1 + ybase)
            x += hmtx[g][0]
    return placed, (minx, miny, maxx, maxy)

def wordmark_group(lines, ink, target_ink_h, x_off, y_off=0.0):
    placed, (minx, miny, maxx, maxy) = compose_lines(lines)
    k = target_ink_h / (maxy - miny)
    # flip y, scale so ink height = target, shift ink-top to y_off and ink-left to x_off
    g = [f'<g transform="translate({x_off:.3f} {y_off:.3f}) scale({k:.5f} {-k:.5f}) '
         f'translate({-minx:.3f} {-maxy:.3f})" fill="{ink}">']
    for d, gx, gy in placed:
        g.append(f'<path transform="translate({gx} {gy})" d="{d}"/>')
    g.append('</g>')
    return "".join(g), (maxx - minx) * k

def lockup(lines, ink, mark_h=100.0):
    gap = GAP_RATIO * mark_h
    if len(lines) == 2:
        wm_h = WM2_RATIO * mark_h
    else:
        wm_h = mark_h * 0.62                        # one-line: cap-height ~ scaled to sit with mark
    total_h = max(mark_h, wm_h)
    mark_y = (total_h - mark_h) / 2
    wm_x = mark_h + gap
    wm_y = (total_h - wm_h) / 2
    wmg, wm_w = wordmark_group(lines, ink, wm_h, wm_x, wm_y)
    total_w = wm_x + wm_w
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.2f} {total_h:.2f}" shape-rendering="geometricPrecision">']
    svg.append(f'<svg x="0" y="{mark_y:.3f}" width="{mark_h}" height="{mark_h}" viewBox="0 0 7 7">{mark_dots(ink)}</svg>')
    svg.append(wmg)
    svg.append('</svg>')
    return "".join(svg)

def avatar(ink, ground=None):
    """Mark centered in a square, clear space = half mark height on each side.
       mark_h + 2*(0.5*mark_h) = 2*mark_h → canvas is 2x mark. viewBox 0 0 200 200, mark 100 centered."""
    bg = f'<rect width="200" height="200" fill="{ground}"/>' if ground else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" shape-rendering="geometricPrecision">'
            f'{bg}<svg x="50" y="50" width="100" height="100" viewBox="0 0 7 7">{mark_dots(ink)}</svg></svg>')

if __name__ == "__main__":
    ld = os.path.join(HERE, "lockups"); os.makedirs(ld, exist_ok=True)
    for name, ink in INKS.items():
        open(os.path.join(ld, f"lockup-horizontal-{name}.svg"), "w").write(lockup(["Mission", "Robotics"], ink))
        open(os.path.join(ld, f"lockup-oneline-{name}.svg"), "w").write(lockup(["Mission Robotics"], ink))
    print("lockups: horizontal + oneline x", len(INKS))
    ad = os.path.join(HERE, "avatar"); os.makedirs(ad, exist_ok=True)
    open(os.path.join(ad, "avatar-transparent.svg"), "w").write(avatar("#17181a", None))
    open(os.path.join(ad, "avatar-on-near-black.svg"), "w").write(avatar("#e8e6dd", "#17181a"))
    open(os.path.join(ad, "avatar-on-cream.svg"), "w").write(avatar("#17181a", "#e8e6dd"))
    print("avatars: transparent, on-near-black, on-cream")
