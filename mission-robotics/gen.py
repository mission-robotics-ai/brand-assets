#!/usr/bin/env python3
"""Mission Robotics brand kit v2 — vector generator.

Single source of truth for the MARK geometry: the dot-matrix from the signage
band script (7x7 grid, per-dot size s = 0.50 + 0.42*(1-d), corner radius 0.29*s).
Emits true-vector SVGs per ink + the tokens files. Wordmark/lockups are built by
wordmark.py (fontTools outlines); PNG ladders are rasterized by raster.sh (Chrome).

Run:  python3 gen.py
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- canonical inks -------------------------------------------------------
INKS = {
    "near-black": "#17181a",
    "cream":      "#e8e6dd",
    "green":      "#4ADE80",   # THE accent — matches newtheory-adjacent green, site canonical
    "white":      "#ffffff",
}

# ---- MARK geometry (the canonical dot-matrix) -----------------------------
GRID = 7
S_BASE = 0.50          # min dot size (grid units) at the corners
S_SPAN = 0.42          # additional size toward center
RADIUS_RATIO = 0.29    # corner radius as fraction of dot size

def dot_size(r, c):
    d = math.hypot(r - 3, c - 3) / math.hypot(3, 3)   # normalized dist from center
    return S_BASE + S_SPAN * (1 - d)

def mark_svg(hex_ink, px=None):
    """True-vector mark. viewBox 0 0 7 7; optional width/height in px."""
    dims = f' width="{px}" height="{px}"' if px else ""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 7 7"{dims}'
             ' shape-rendering="geometricPrecision">']
    for r in range(GRID):
        for c in range(GRID):
            s = dot_size(r, c)
            x = c + 0.5 - s / 2
            y = r + 0.5 - s / 2
            parts.append(f'<rect x="{x:.4f}" y="{y:.4f}" width="{s:.4f}" height="{s:.4f}" '
                         f'rx="{s*RADIUS_RATIO:.4f}" fill="{hex_ink}"/>')
    parts.append('</svg>')
    return ''.join(parts)

def write_marks():
    d = os.path.join(HERE, "mark")
    os.makedirs(d, exist_ok=True)
    for name, hexv in INKS.items():
        open(os.path.join(d, f"mark-{name}.svg"), "w").write(mark_svg(hexv))
    print("marks:", ", ".join(f"mark-{n}.svg" for n in INKS))

# ---- TOKENS ---------------------------------------------------------------
TOKENS = {
    "$schema": "mission-robotics brand tokens v2",
    "color": {
        "near-black": {"value": "#17181a", "role": "primary ground / ink"},
        "cream":      {"value": "#e8e6dd", "role": "warm off-white ground / ink"},
        "white":      {"value": "#ffffff", "role": "pure white ink"},
        "green":      {"value": "#4ADE80", "role": "THE accent — matches newtheory-adjacent green, site canonical"},
    },
    "mark": {
        "grid": GRID,
        "dot_size_base": S_BASE,
        "dot_size_span": S_SPAN,
        "dot_size_formula": "s = 0.50 + 0.42*(1 - d);  d = dist_from_center / max_dist",
        "corner_radius_ratio": RADIUS_RATIO,
        "viewbox": "0 0 7 7",
    },
    "clearspace": {
        "rule": "half the mark height on all sides",
        "value": "0.5 * mark_height",
    },
    "min_size": {
        "mark_px": 24,
        "favicon_px": 16,
        "wordmark_one_line_px": 96,
        "lockup_px": 120,
    },
}

def write_tokens():
    d = os.path.join(HERE, "tokens")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "tokens.json"), "w").write(json.dumps(TOKENS, indent=2))
    css = [":root {",
           "  /* Mission Robotics brand tokens v2 */",
           "  --mr-near-black: #17181a;",
           "  --mr-cream: #e8e6dd;",
           "  --mr-white: #ffffff;",
           "  --mr-green: #4ADE80; /* THE accent — matches newtheory-adjacent green, site canonical */",
           "  /* mark geometry */",
           "  --mr-mark-grid: 7;",
           "  --mr-mark-dot-base: 0.50;",
           "  --mr-mark-dot-span: 0.42;",
           "  --mr-mark-radius-ratio: 0.29;",
           "  /* clear space = half mark height; min mark 24px, favicon 16px */",
           "}"]
    open(os.path.join(d, "tokens.css"), "w").write("\n".join(css) + "\n")
    print("tokens: tokens.json, tokens.css")

if __name__ == "__main__":
    write_marks()
    write_tokens()
