#!/usr/bin/env python3
"""Shared "by New Theory" byline — Inter Regular 400 outlined to true paths.

Used by wordmark.py and build_assets.py for the -by-new-theory variants.
Byline color is FIXED #6b7280 (site gray-500) on every ink; tracking is
+0.025em (site tracking-wide). Proportions were measured from the actual
solarpunk-loft header at 8x device scale — see measure_byline.py.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
INTER_TTF = os.path.join(HERE, "wordmark", "Inter-Regular.ttf")

BYLINE_TEXT = "by New Theory"
BYLINE_HEX = "#6b7280"     # site gray-500 — fixed across all inks
TRACKING_EM = 0.025        # tracking-wide, applied to every glyph advance

# measured from solarpunk-loft header @8x (measure_byline.py)
BYLINE_H_RATIO = 0.5793    # byline ink height / wordmark ink height
BYLINE_GAP_RATIO = 0.4966  # wordmark ink bottom -> byline ink top / wm ink height
BYLINE_X_RATIO = 0.0276    # byline ink left - wordmark ink left / wm ink height

_font = TTFont(INTER_TTF)
_TRACK = TRACKING_EM * _font['head'].unitsPerEm
_glyphset = _font.getGlyphSet()
_cmap = _font.getBestCmap()
_hmtx = _font['hmtx']

def _compose():
    """Place byline glyphs in y-up font coords; return (paths[(d,x)], ink_bbox)."""
    placed = []
    minx = miny = 1e18; maxx = maxy = -1e18
    x = 0
    for ch in BYLINE_TEXT:
        g = _cmap[ord(ch)]
        spen = SVGPathPen(_glyphset); _glyphset[g].draw(spen)
        if spen.getCommands():                      # spaces produce no path
            placed.append((spen.getCommands(), x))
        bp = BoundsPen(_glyphset); _glyphset[g].draw(bp)
        if bp.bounds:
            x0, y0, x1, y1 = bp.bounds
            minx = min(minx, x0 + x); maxx = max(maxx, x1 + x)
            miny = min(miny, y0); maxy = max(maxy, y1)
        x += _hmtx[g][0] + _TRACK
    return placed, (minx, miny, maxx, maxy)

def byline_group(target_ink_h, x_off, y_off):
    """SVG <g> with byline ink height = target, ink top-left at (x_off, y_off).
       Returns (group_svg, ink_width)."""
    placed, (minx, miny, maxx, maxy) = _compose()
    k = target_ink_h / (maxy - miny)
    g = [f'<g transform="translate({x_off:.3f} {y_off:.3f}) scale({k:.5f} {-k:.5f}) '
         f'translate({-minx:.3f} {-maxy:.3f})" fill="{BYLINE_HEX}">']
    for d, gx in placed:
        g.append(f'<path transform="translate({gx:.1f} 0)" d="{d}"/>')
    g.append('</g>')
    return "".join(g), (maxx - minx) * k
