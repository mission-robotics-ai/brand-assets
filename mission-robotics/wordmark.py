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

if __name__ == "__main__":
    d = os.path.join(HERE, "wordmark")
    for name, ink in INKS.items():
        open(os.path.join(d, f"wordmark-oneline-{name}.svg"), "w").write(
            svg_wordmark(["Mission Robotics"], ink))
        open(os.path.join(d, f"wordmark-twoline-{name}.svg"), "w").write(
            svg_wordmark(["Mission", "Robotics"], ink))
    print("wordmarks: oneline + twoline x", len(INKS), "inks")
