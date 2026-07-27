#!/usr/bin/env python3
"""Pixel-snapped favicon ladder for the mark.

At favicon sizes the analog dot geometry (7 cells over 32px = 4.57px/cell) falls
between pixels and renders mushy. This emits a pixel-aligned variant: integer
cell size, integer dot size, integer position — crisp on the pixel grid. Same
dot-size law as the vector mark, quantized. PNG, transparent bg.

Run:  python3 fav.py
"""
import math, os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
INKS = {"near-black": (23,24,26,255), "cream": (232,230,221,255),
        "green": (74,222,128,255), "white": (255,255,255,255)}
SIZES = [16, 32, 64]

def dot_frac(r, c):
    d = math.hypot(r-3, c-3) / math.hypot(3, 3)
    return 0.50 + 0.42 * (1 - d)

def favicon(px, rgba):
    img = Image.new("RGBA", (px, px), (0,0,0,0))
    dr = ImageDraw.Draw(img)
    cell = px // 7
    if cell < 1: cell = 1
    margin = (px - cell*7) // 2
    for r in range(7):
        for c in range(7):
            # clamp to cell-1 so every dot keeps at least a 1px gap (no merging)
            dp = max(1, min(round(dot_frac(r, c) * cell), cell - 1))
            x = margin + c*cell + (cell - dp)//2
            y = margin + r*cell + (cell - dp)//2
            rad = round(0.29 * dp)
            if dp >= 6 and rad >= 1:              # only round when big enough to read as a dot
                dr.rounded_rectangle([x, y, x+dp-1, y+dp-1], radius=rad, fill=rgba)
            else:                                  # square dots stay crisp on the pixel grid
                dr.rectangle([x, y, x+dp-1, y+dp-1], fill=rgba)
    return img

if __name__ == "__main__":
    d = os.path.join(HERE, "png"); os.makedirs(d, exist_ok=True)
    for name, rgba in INKS.items():
        for px in SIZES:
            favicon(px, rgba).save(os.path.join(d, f"mark-{name}-{px}.png"))
    print("favicons:", ", ".join(f"mark-<ink>-{s}.png" for s in SIZES))
