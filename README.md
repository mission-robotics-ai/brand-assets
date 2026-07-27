# Brand Assets

Canonical logo files for **New Theory** and **Mission Robotics**. Single source of truth so logo requests stop being an archaeology dig through old export folders.

Do not add partner/sponsor logos here (LiveKit, Modal, Rerun, etc.) — those aren't ours to redistribute.

## Mission Robotics — `mission-robotics/`

**v2 (July 2026): fully generated vector kit.** Every asset is emitted from geometry by `build_assets.py` — the dot-matrix mark from its size-falloff formula, the wordmark as Instrument Serif outlined to true paths. No raster-embedded SVGs, no fuzzy exports. See [`mission-robotics/README.md`](mission-robotics/README.md) for the full usage guide (inks per ground, min sizes, clear space, favicon variant, regeneration).

Quick map: `mark/` `wordmark/` `lockups/` `avatar/` (SVG, per ink: near-black / cream / white / green) · `png/` (raster ladders incl. pixel-snapped favicons) · `tokens/` (tokens.json + tokens.css) · `effects/` (legacy glow orbs — a treatment, not the logo).

Canonical green: `#4ADE80`. (The card system CSS still carries the older `#46e07a` — migrate on next card regen.)

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
- Prefer SVG everywhere — Mission Robotics SVGs are true vector as of v2. Use the PNG ladders when a raster is required, matching size to output.

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
