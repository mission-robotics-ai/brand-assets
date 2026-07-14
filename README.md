# Brand Assets

Canonical logo files for **New Theory** and **Mission Robotics**. Single source of truth so logo requests stop being an archaeology dig through old export folders.

Do not add partner/sponsor logos here (LiveKit, Modal, Rerun, etc.) — those aren't ours to redistribute.

## Mission Robotics — `mission-robotics/`

| File | Format | Notes / use |
|---|---|---|
| `mission-robotics-logo.svg` | SVG (raster-embedded) | Full wordmark lockup, light variant |
| `mission-robotics-logo-dark.svg` | SVG (raster-embedded) | Full wordmark lockup, dark variant |
| `mission-robotics-logo-300dpi.png` | PNG, 4000×1145, RGBA | Full lockup, light, print/hi-res |
| `mission-robotics-logo-72dpi.png` | PNG, 1400×401, RGBA | Full lockup, light, screen/web |
| `mission-robotics-logo-dark-300dpi.png` | PNG, 4000×1145, RGBA | Full lockup, dark, print/hi-res |
| `mission-robotics-logo-dark-72dpi.png` | PNG, 1400×401, RGBA | Full lockup, dark, screen/web |
| `mission-robotics-mark-300dpi.png` | PNG, 2000×1996, RGBA | Icon-only mark, light, hi-res |
| `mission-robotics-mark-dark-300dpi.png` | PNG, 2000×1996, RGBA | Icon-only mark, dark, hi-res |
| `mr-orb-mark-bright.png` | PNG, 471×470, RGBA | Orb mark, bright/glow treatment |
| `mr-orb-trim.png` | PNG, 471×470, RGB | Orb mark, trimmed/flat treatment |

Note: the two `logo*.svg` files are raster images embedded in an SVG wrapper, not true vector paths. No vector mark file exists yet — only PNG marks.

The "logo" and "dark" naming isn't independently verified against a style guide in this repo — when in doubt about which variant reads correctly on a given background, check both before shipping.

## New Theory — `new-theory/`

| File | Format | Notes / use |
|---|---|---|
| `nt-logo-white.svg` | SVG (true vector), 232×48 viewBox, white fill | Wordmark, white — for dark grounds only |
| `nt-white.png` | PNG, 1392×288, RGBA | Wordmark, white, raster fallback |

See `new-theory/GAPS.md` — only the white variant exists.

## Usage basics

- Dark-ground logo (white/light ink) goes on light backgrounds only if there's no light-ground alternative — check contrast before use.
- Use the dark-ink variant (`*-dark.svg` / `*-dark-*.png`) on light backgrounds, the light/white variant on dark backgrounds.
- The mark (orb / icon) stands alone at small sizes — favicons, avatars, anywhere the full wordmark lockup won't read. Don't shrink the full lockup below the point where the wordmark blurs; swap to the mark instead.
- Prefer SVG where one exists and is true vector (New Theory). For Mission Robotics, the SVGs are raster-embedded, so pick the PNG dpi that matches the output (72dpi screen, 300dpi print) rather than assuming the SVG scales cleanly.

## Brand tokens (Mission Robotics)

Pulled from `operation-logvy/outreach/social/card-brand.css` (source of truth for the Embodied Metal Hackathon card system) and cross-checked against `operation-logvy/outreach/social/mission-robotics-brand.html`. Both agree.

- **Display face:** Instrument Serif — used for the "Mission Robotics" wordmark and the hero/tagline treatment.
- **Body/UI face:** Inter — used for body copy, labels, and the "savant" lowercase wordmark.
- **One-off hero face:** Archivo Black — used only for the hackathon hero title, not the core MR lockup.
- **Color tokens** (as defined in `card-brand.css`, `:root`):
  - `--bg: #0b0e0c` — background
  - `--panel: #11150f`
  - `--line: #232b1d` — hairline rules
  - `--ink: #d7e0cf` — dim/light body ink
  - `--green: #46e07a` — the one green accent, used everywhere
  - `--mint: #b4ffcf`
  - `--dim: #2a8c4d` — deeper green, used for the "x" separator
  - `--cream: #e8e6dd` — warm off-white for hero + wordmarks
  - `--sponsor-label: #8a957c`

These tokens are documented for the hackathon card system specifically — treat them as the current working palette, not a formally ratified brand-wide spec.
