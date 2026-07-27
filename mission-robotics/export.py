#!/usr/bin/env python3
"""Export the SVG matrix to transparent PNG ladders via headless Chrome.
Handles non-square art (wordmark/lockup) by reading the SVG viewBox aspect.

  MARK    per ink : 2000, 512, 128   (favicon 64/32/16 come from fav.py)
  WORDMARK        : 2000 (long edge), one-line + two-line, per ink
  LOCKUP          : 2000 (long edge), horizontal + one-line, per ink
  AVATAR          : 1024, 512, 256, 64
"""
import os, re, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
INKS = ["near-black", "cream", "green", "white"]

def aspect(svg_path):
    vb = re.search(r'viewBox="([\d.\s-]+)"', open(svg_path).read()).group(1).split()
    w, h = float(vb[2]), float(vb[3])
    return w / h

def export(svg, out, long_px):
    a = aspect(svg)
    w, h = (long_px, round(long_px / a)) if a >= 1 else (round(long_px * a), long_px)
    svg_abs = os.path.abspath(svg)
    html = (f'<!doctype html><html><head><style>*{{margin:0;padding:0}}'
            f'html,body{{width:{w}px;height:{h}px;background:transparent}}'
            f'img{{width:{w}px;height:{h}px;display:block}}</style></head>'
            f'<body><img src="file://{svg_abs}"></body></html>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=os.path.dirname(svg_abs)) as f:
        f.write(html); hp = f.name
    try:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={w},{h}",
                        "--default-background-color=00000000", f"--screenshot={os.path.abspath(out)}",
                        f"file://{hp}"], check=True, capture_output=True)
    finally:
        os.unlink(hp)

if __name__ == "__main__":
    png = os.path.join(HERE, "png"); os.makedirs(png, exist_ok=True)
    for ink in INKS:
        for px in (2000, 512, 128):
            export(f"{HERE}/mark/mark-{ink}.svg", f"{png}/mark-{ink}-{px}.png", px)
        for lay in ("oneline", "twoline"):
            export(f"{HERE}/wordmark/wordmark-{lay}-{ink}.svg", f"{png}/wordmark-{lay}-{ink}-2000.png", 2000)
        for lay in ("horizontal", "oneline"):
            export(f"{HERE}/lockups/lockup-{lay}-{ink}.svg", f"{png}/lockup-{lay}-{ink}-2000.png", 2000)
    for name in ("transparent", "on-near-black", "on-cream"):
        for px in (1024, 512, 256, 64):
            export(f"{HERE}/avatar/avatar-{name}.svg", f"{png}/avatar-{name}-{px}.png", px)
    print("PNG ladders exported to png/")
