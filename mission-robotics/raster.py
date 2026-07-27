#!/usr/bin/env python3
"""Rasterize brand SVGs to transparent PNGs at exact pixel sizes via headless Chrome.

Chrome is the rasterizer of record for this kit (matches how the signage renders
and handles transparency + SVG faithfully). Usage:
    python3 raster.py <svg_path> <out_path> <px> [--bg RRGGBBAA]
"""
import os, subprocess, sys, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def raster(svg, out, px, bg="00000000", scale=1):
    svg_abs = os.path.abspath(svg)
    html = (f'<!doctype html><html><head><style>'
            f'*{{margin:0;padding:0}}html,body{{width:{px}px;height:{px}px;background:transparent}}'
            f'img{{width:{px}px;height:{px}px;display:block}}'
            f'</style></head><body><img src="file://{svg_abs}"></body></html>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=os.path.dirname(svg_abs)) as f:
        f.write(html); htmlpath = f.name
    try:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--force-device-scale-factor={scale}", f"--window-size={px},{px}",
                        f"--default-background-color={bg}", f"--screenshot={os.path.abspath(out)}",
                        f"file://{htmlpath}"],
                       check=True, capture_output=True)
    finally:
        os.unlink(htmlpath)

if __name__ == "__main__":
    a = sys.argv[1:]
    bg = "00000000"
    if "--bg" in a:
        i = a.index("--bg"); bg = a[i+1]; a = a[:i] + a[i+2:]
    svg, out, px = a[0], a[1], int(a[2])
    raster(svg, out, px, bg)
    print(f"rasterized {out} @ {px}px (bg {bg})")
