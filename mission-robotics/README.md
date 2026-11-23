# Mission Robotics — brand kit

Generated vector brand assets. Every file here is emitted from geometry by the
scripts in this repo, not hand-exported — the mark is a dot-matrix defined by a
formula, and the wordmark is Instrument Serif outlined to true paths. Regenerate
anytime with the scripts below.

## Directories

| Dir | Holds |
|-----|-------|
| `mark/` | The dot-matrix mark, one true-vector SVG per ink. |
| `wordmark/` | "Mission Robotics" outlined to paths — `oneline` and `twoline`, per ink, plus `-by-new-theory` variants. Also the source TTFs (`InstrumentSerif-Regular.ttf`, `Inter-Regular.ttf`). |
| `lockups/` | Mark + wordmark, at signage-band proportions — `horizontal` (two-line) and `oneline`, per ink, plus `-by-new-theory` variants. |
| `avatar/` | Mark centered in a square with clear space — transparent, on near-black, on cream. |
| `png/` | Rasterized ladders (transparent): mark 2000/512/128, wordmark & lockup 2000, avatar 1024/512/256/64, favicons 16/32/64. |
| `tokens/` | `tokens.json` and `tokens.css` — colors, mark geometry, clear-space and min-size rules. |
| `morrigan/` | Morrigan's avatar, a crow in profile on the same 7×7 dot-matrix grid as the mark (SVG and 1024px PNG). Hand-drawn bitmap – not made by the scripts below. Used as her Slack avatar. |
| `effects/` | Legacy raster glow-orb marks from v1. A texture/treatment, **not** the logo — do not use as the primary mark or favicon. |

## Colors

| Token | Hex | Role |
|-------|-----|------|
| near-black | `#17181a` | Primary ground and ink. |
| cream | `#e8e6dd` | Warm off-white ground / ink. |
| white | `#ffffff` | Pure-white needs. |
| green | `#4ADE80` | The one accent (matches the newtheory-adjacent green, site canonical). |

## Which ink on which ground

| Ground | Use ink |
|--------|---------|
| near-black `#17181a` | cream (default) or white; green for an accent moment |
| cream `#e8e6dd` | near-black |
| white `#ffffff` | near-black |
| green `#4ADE80` | near-black |
| photo / busy | white, with full clear space |

Green is an accent, not a default ink — the mark is near-black or cream in almost every context.

## "by New Theory" variants

Every text-bearing asset also ships a `-by-new-theory` variant — wordmark
(one-line and two-line) and lockup (oneline and horizontal), per ink — with the
"by New Theory" byline underneath the wordmark, matching the website header
treatment exactly (Inter 400, +0.025em tracking, proportions measured from the
live header by `measure_byline.py`).

- **Byline color is fixed `#6b7280` on every ink** — it matches the site's
  gray-500 and stays put whether the wordmark is near-black, cream, green, or white.
- **When to use:** anything where the New Theory relationship should be visible —
  event pages, decks, partner-facing material.
- **On busy photo grounds** the plain (no-byline) white lockup is safer — the
  gray byline needs a quiet ground to stay legible.
- **Minimum sizes:** the byline renders at ~46% of the wordmark's type size, so
  keep it above ~9px — that means lockup-by-new-theory at ≥180px wide and
  wordmark-by-new-theory at ≥140px wide.

## Clear space & minimum sizes

- **Clear space:** half the mark height on all sides (the `avatar/` files bake this in).
- **Minimum sizes:** mark 24px · favicon 16px · one-line wordmark 96px · lockup 120px.

## Favicons

The favicon PNGs (`png/mark-*-16/32/64.png`) are a **pixel-snapped** variant of the
mark, not a straight downscale. The analog geometry (7 cells across the width) lands
between pixels at these sizes and renders mushy, so the favicon generator quantizes the
same dot-size law to integer cells, integer dot sizes, and integer positions — crisp on
the pixel grid. Use these for favicons; use the SVG (or 128px+ PNG) everywhere else.

## Type

- **Wordmark:** Instrument Serif 400 — already outlined to paths in `wordmark/` and
  `lockups/`, so rendering them needs no font installed.
- **UI / body:** Inter (400 / 500 / 600). The "by New Theory" byline is Inter 400,
  outlined from the committed `wordmark/Inter-Regular.ttf`.
- **Display one-offs:** Archivo Black.

All three are Google Fonts under the SIL Open Font License.

## Tokens

`tokens/tokens.json` and `tokens/tokens.css` are the machine-readable source for colors,
the mark geometry constants (7×7 grid; dot size `s = 0.50 + 0.42·(1 − d)`; corner radius
`0.29·s`), clear space, and min sizes. Import the CSS for `--mr-*` custom properties.

## Regenerating

Scripts are ordered; run from this directory.

```bash
python3 gen.py                              # mark SVGs (all inks) + tokens
uv run --with fonttools python3 wordmark.py       # outlined wordmark SVGs
uv run --with fonttools python3 build_assets.py   # lockups + avatars
uv run --with pillow python3 fav.py               # pixel-snapped favicon PNGs
python3 export.py                            # PNG ladders (needs Google Chrome)
```

`gen.py` is the source of truth for the mark geometry and the ink set — change a color or
the dot formula there and re-run the chain.
