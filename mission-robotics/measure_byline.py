#!/usr/bin/env python3
"""Measure the "by New Theory" byline treatment from the solarpunk-loft header.

Reproduces the site header's text column (mission-robotics-ops/prototypes/
solarpunk-loft/index.html) as a minimal HTML snippet — Instrument Serif 24px
wordmark over Inter 11px byline (#6b7280 on site; solid red/blue here so pixels
are attributable) — renders it with headless Chrome at 8x device scale, and
measures ink boxes with pillow. The ratios printed here are baked into
byline.py as BYLINE_H_RATIO / BYLINE_GAP_RATIO / BYLINE_X_RATIO.

Site treatment (index.html header, Tailwind 3.4.17):
  wordmark: Instrument Serif 400, text-2xl (24px), leading-none, tracking-tight (-0.025em)
  byline:   Inter 400, text-[11px], text-gray-500 (#6b7280), tracking-wide (+0.025em),
            mt-1 (4px), leading-none inherited, left-aligned with the wordmark

Run:  uv run --with pillow --with fonttools python3 measure_byline.py
"""
import os, subprocess, tempfile
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCALE = 8  # --force-device-scale-factor

HTML = """<!doctype html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400&family=Instrument+Serif&display=swap" rel="stylesheet">
<style>
  * { margin:0; padding:0; }
  body { background:#ffffff; }
  .col { display:flex; flex-direction:column; align-items:flex-start; line-height:1; padding:20px; }
  .wm { font-family:'Instrument Serif',Georgia,serif; font-weight:400; font-size:24px;
        letter-spacing:-0.025em; color:#ff0000; }
  .by { font-family:'Inter',sans-serif; font-weight:400; font-size:11px;
        letter-spacing:0.025em; margin-top:4px; color:#0000ff; }
</style></head><body>
<div class="col"><span class="wm">Mission Robotics</span><span class="by">by New Theory</span></div>
</body></html>"""

def ink_bbox(img, channel):
    """bbox of pixels whose `channel` dominates by >50 (red=0, blue=2)."""
    px = img.load()
    minx = miny = 10**9; maxx = maxy = -1
    for y in range(img.height):
        for x in range(img.width):
            p = px[x, y]
            others = [p[c] for c in (0, 1, 2) if c != channel]
            if p[channel] - max(others) > 50:
                minx = min(minx, x); maxx = max(maxx, x)
                miny = min(miny, y); maxy = max(maxy, y)
    assert maxx >= 0, "no ink found for channel %d" % channel
    return minx, miny, maxx, maxy

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(HTML); hp = f.name
    shot = hp.replace(".html", ".png")
    try:
        # virtual-time-budget lets the Google Fonts load land before the shot;
        # a fallback-font render would invalidate every measurement.
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--force-device-scale-factor={SCALE}", "--window-size=400,100",
                        "--virtual-time-budget=10000", f"--screenshot={shot}",
                        f"file://{hp}"], check=True, capture_output=True)
        img = Image.open(shot).convert("RGB")
        wx0, wy0, wx1, wy1 = ink_bbox(img, 0)   # wordmark (red)
        bx0, by0, bx1, by1 = ink_bbox(img, 2)   # byline (blue)
    finally:
        os.unlink(hp)
        if os.path.exists(shot): os.unlink(shot)

    wm_h = wy1 - wy0 + 1                 # "Mission Robotics" has no descenders
    by_h = by1 - by0 + 1                 # ascenders b/N/Th + descender y
    gap = by0 - wy1 - 1                  # wordmark ink bottom -> byline ink top
    dx = bx0 - wx0                       # byline ink left - wordmark ink left
    by_w = bx1 - bx0 + 1

    print(f"@{SCALE}x px  wm ink h={wm_h}  byline ink h={by_h}  gap={gap}  dx={dx}  byline w={by_w}")
    print(f"BYLINE_H_RATIO   = {by_h / wm_h:.4f}   # byline ink height / wordmark ink height")
    print(f"BYLINE_GAP_RATIO = {gap / wm_h:.4f}   # wm ink bottom -> byline ink top / wm ink height")
    print(f"BYLINE_X_RATIO   = {dx / wm_h:.4f}   # byline ink left - wm ink left / wm ink height")

    # sanity: did Inter actually render? (Helvetica fallback runs wider/narrower)
    from fontTools.ttLib import TTFont
    ft = TTFont(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "wordmark", "Inter-Regular.ttf"))
    upm = ft['head'].unitsPerEm; cmap = ft.getBestCmap(); hmtx = ft['hmtx']
    from fontTools.pens.boundsPen import BoundsPen
    gs = ft.getGlyphSet()
    x = 0; minx = 10**9; maxx = -10**9
    for ch in "by New Theory":
        g = cmap[ord(ch)]
        bp = BoundsPen(gs); gs[g].draw(bp)
        if bp.bounds:
            minx = min(minx, bp.bounds[0] + x); maxx = max(maxx, bp.bounds[2] + x)
        x += hmtx[g][0] + 0.025 * upm
    expect = (maxx - minx) / upm * 11 * SCALE
    dev = abs(by_w - expect) / expect * 100
    print(f"byline width check: measured {by_w}px vs Inter-metrics {expect:.0f}px ({dev:.1f}% off)")
    assert dev < 3, "byline width deviates — Inter likely did not load"
