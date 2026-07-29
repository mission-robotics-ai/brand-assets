#!/usr/bin/env python3
"""Wordmark generator — 'Mission Robotics' in Instrument Serif 400, outlined to
true vector paths via fontTools (no live-type dependency in the final asset).

Glyph outlines come from the OFL TTF; horizontal placement uses the font's own
advance widths (hmtx). Emits one-line and two-line layouts per ink. Verify with
wordmark_probe (overlay-diff vs a Chrome live-type render).

Run:  python3 wordmark.py
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from byline import byline_group, BYLINE_H_RATIO, BYLINE_GAP_RATIO, BYLINE_X_RATIO

HERE = os.path.dirname(os.path.abspath(__file__))
TTF = os.path.join(HERE, "wordmark", "InstrumentSerif-Regular.ttf")
INKS = {"near-black": "#17181a", "cream": "#e8e6dd",
        "green": "#4ADE80", "white": "#ffffff"}

font = TTFont(TTF)
UPM = font['head'].unitsPerEm            # 1000
ASC = font['OS/2'].sTypoAscender         # 990
DESC = font['OS/2'].sTypoDescender       # -310
glyphset = font.getGlyphSet()
cmap = font.getBestCmap()
hmtx = font['hmtx']

def line_glyphs(text):
    """Return [(path_d, x_offset)] and total advance width for a string."""
    out, x = [], 0
    for ch in text:
        g = cmap[ord(ch)]
        pen = SVGPathPen(glyphset)
        glyphset[g].draw(pen)
        out.append((pen.getCommands(), x))
        x += hmtx[g][0]
    return out, x

def svg_wordmark(lines, ink, line_advance=960):
    """lines: list of strings (1 or 2). Baselines spaced by line_advance units."""
    rendered = [line_glyphs(t) for t in lines]
    width = max(total for _, total in rendered)
    height = ASC + (len(lines) - 1) * line_advance - DESC
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height:.0f}" '
             f'shape-rendering="geometricPrecision">']
    for i, (glyphs, total) in enumerate(rendered):
        baseline = ASC + i * line_advance
        # flip y (font is y-up) and drop to this line's baseline
        parts.append(f'<g transform="translate(0 {baseline}) scale(1 -1)" fill="{ink}">')
        for d, xoff in glyphs:
            parts.append(f'<path transform="translate({xoff} 0)" d="{d}"/>')
        parts.append('</g>')
    parts.append('</svg>')
    return ''.join(parts)

def lines_ink_bbox(lines, line_advance=960):
    """Ink bbox of placed lines in y-up font coords (baselines line_advance apart)."""
    minx = miny = 1e18; maxx = maxy = -1e18
    for i, text in enumerate(lines):
        ybase, x = -i * line_advance, 0
        for ch in text:
            g = cmap[ord(ch)]
            bp = BoundsPen(glyphset); glyphset[g].draw(bp)
            if bp.bounds:
                x0, y0, x1, y1 = bp.bounds
                minx = min(minx, x0 + x); maxx = max(maxx, x1 + x)
                miny = min(miny, y0 + ybase); maxy = max(maxy, y1 + ybase)
            x += hmtx[g][0]
    return minx, miny, maxx, maxy

def svg_wordmark_byline(lines, ink, line_advance=960):
    """Wordmark with the 'by New Theory' byline underneath, left-aligned per the
       measured site ratios. viewBox is ink-tight (wordmark ink top -> byline ink
       bottom), in font units. Byline ratios couple to a single line's type size,
       so for two-line layouts they scale from the one-line ink height."""
    minx, miny, maxx, maxy = lines_ink_bbox(lines, line_advance)
    wm_h = maxy - miny
    x0, y0, x1, y1 = lines_ink_bbox(["Mission Robotics"])
    h1 = y1 - y0                                   # one-line ink height at this scale
    b_h = BYLINE_H_RATIO * h1
    b_gap = BYLINE_GAP_RATIO * h1
    b_x = BYLINE_X_RATIO * h1
    byg, b_w = byline_group(b_h, b_x, wm_h + b_gap)
    width = max(maxx - minx, b_x + b_w)
    height = wm_h + b_gap + b_h
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {height:.1f}" '
             f'shape-rendering="geometricPrecision">',
             # flip y, ink top-left of the wordmark block to (0,0)
             f'<g transform="translate({-minx:.1f} {maxy:.1f}) scale(1 -1)" fill="{ink}">']
    for i, text in enumerate(lines):
        ybase = -i * line_advance
        glyphs, _ = line_glyphs(text)
        for d, xoff in glyphs:
            parts.append(f'<path transform="translate({xoff} {ybase})" d="{d}"/>')
    parts.append('</g>')
    parts.append(byg)
    parts.append('</svg>')
    return ''.join(parts)

if __name__ == "__main__":
    d = os.path.join(HERE, "wordmark")
    for name, ink in INKS.items():
        open(os.path.join(d, f"wordmark-oneline-{name}.svg"), "w").write(
            svg_wordmark(["Mission Robotics"], ink))
        open(os.path.join(d, f"wordmark-twoline-{name}.svg"), "w").write(
            svg_wordmark(["Mission", "Robotics"], ink))
        open(os.path.join(d, f"wordmark-oneline-by-new-theory-{name}.svg"), "w").write(
            svg_wordmark_byline(["Mission Robotics"], ink))
        open(os.path.join(d, f"wordmark-twoline-by-new-theory-{name}.svg"), "w").write(
            svg_wordmark_byline(["Mission", "Robotics"], ink))
    print("wordmarks: (oneline + twoline) x (plain + by-new-theory) x", len(INKS), "inks")
