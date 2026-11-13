---
name: palette-603010
description: Nine tested 60/30/10 color palettes (base / support / accent) with exact hex codes, roles, and contrast rules, for designing posts, carousels, stories, posters, ads, thumbnails, product shots and UI. Use when the user asks for colors, a palette, a color scheme, "which colors go together", or names one of these palettes (Sky Fresh, Petrol Gaming, Monochrome Brown, Teal Brand, Midnight Neon, Navy Idea, Mauve Loud, Olive Standout, Brick Hook), or says ألوان / باليت / لوحة ألوان / 60 30 10.
---

# 60·30·10 Palette Book

Every palette follows one rule:

| Share | Role | What it colors |
|---|---|---|
| **60%** | Base | Background, large surfaces, the set. Sets the mood. One flat color or a soft gradient of the same hue. |
| **30%** | Support | The product/subject, pedestal, panels, or main text. Must separate clearly from the base (light-on-dark or dark-on-light). |
| **10%** | Accent | ONE focal thing: a highlighted word, the CTA, a rim light/glow, or a single object. The most saturated color. Use once per frame. |

## The nine palettes

| Palette | Mood | 60% base | 30% support | 10% accent | Why the accent works |
|---|---|---|---|---|---|
| **Sky Fresh** (سماوي · أبيض · فوشيا) | light, clean, skincare | `#52C5FF` sky blue | `#FFFFFF` white | `#FF1088` fuchsia | Breaks the calm; high contrast pulls the eye to the product |
| **Petrol Gaming** (بترولي · بيج · برتقالي) | dark, premium, gaming | `#062C30` petrol | `#E5D4B8` beige | `#FF4E00` orange | Strong focal point; edge glow on the product |
| **Monochrome Brown** (بني · عاجي · سيان) | warm, classic, fashion | `#3D231A` brown | `#F3EBDD` ivory | `#00F0FF` neon cyan | Visual separation of the foreground object (light ring) |
| **Teal Brand** (بترولي · أبيض · برتقالي نيون) | dark, corporate-bold | `#0B434C` dark teal | `#FFFFFF` white | `#FF5533` neon orange | Sets the focal point on the hero + label pill |
| **Midnight Neon** (أسود · أبيض · أخضر نيون) | dark, tech, games | `#0A0A0A` midnight black | `#FFFFFF` white | `#55FF00` neon green | Black + white has no identity; neon gives it one (glowing path, last headline line) |
| **Navy Idea** (كحلي · أبيض · موف نيون) | dark, serious, marketing | `#031326` dark navy | `#FFFFFF` white | `#D100D1` neon purple | Color only the "idea" object so the message is obvious |
| **Mauve Loud** (موف · بيج · أصفر) | warm, bold, playful | `#913768` mauve | `#C29A74` beige | `#FDD001` yellow | Accent is taken from the subject's own colors, so it feels natural |
| **Olive Standout** (أخضر · بني · برتقالي) | warm, natural, earthy | `#778A3F` olive green | `#6E4B2C` brown | `#F16619` orange | Natural/comfortable base; the one orange element *is* the "stand out" message |
| **Brick Hook** (طوبي · رمادي · تركواز) | warm, confident | `#C15B46` brick | `#ABA6A3` grey | `#45DBE1` turquoise* | Turquoise is brick's opposite, so it dominates the scene |

\* `#45DBE1` was sampled from video (label partly covered); treat as approximate.

## Pairing rules (which color with which)

1. **Accent = opposite hue of the base.** blue↔pink, teal/petrol↔orange, brown↔cyan, navy↔purple, mauve↔yellow, olive↔orange, brick↔turquoise. If you invent a new accent, pick it ~150–180° away from the base hue.
2. **Bright bases need dark text.** Sky blue, cyan, yellow, neon green, turquoise are too light for white text. Put the palette's darkest color or near-black on them, or use them only for shapes/pills. (White on `#52C5FF` ≈ 2:1 — fails.)
3. **Neon only on dark.** Neon green / cyan / magenta / orange glow on black, navy, petrol, brown. On white or beige they wash out and fail text contrast.
4. **Highlight pill text:** on a bright accent pill (yellow, green, cyan, turquoise) use the base color or near-black for the word; on a deep accent (fuchsia, purple, orange-red) use white.
5. **Series trick:** keep 60 and 30 fixed, swap only the 10 to show a new mood while staying on-brand.
6. **Don't spread the accent.** If the 10% color appears in more than one or two places, it stops being a focal point.

## Contrast check (always do it)

Before finalizing text, compute WCAG contrast for each text/background pair:
- ≥ 4.5:1 → body text OK; ≥ 7 → any text.
- 3–4.5 → large/bold headlines only.
- < 3 → shapes, glows, pills only — never text.

Quick formula: relative luminance L = 0.2126R + 0.7152G + 0.0722B (linearized sRGB); ratio = (L1+0.05)/(L2+0.05).

## How to apply

1. Pick the palette by mood (light/clean, dark/premium, warm/earthy) or the one the user names. If unclear, suggest 2–3 that fit and say why in one line each.
2. Map roles: base → background; support → subject and main text; accent → one word / CTA / glow / single object.
3. Run the contrast check on every text pair and fix failures (swap text to the highest-contrast palette color, white, or `#0A0A0A`).
4. When handing colors to the user, give hex codes with role labels, e.g. `60 #062C30 · 30 #E5D4B8 · 10 #FF4E00`.

Reference page with sample posters and contrast tables: https://claude.ai/artifact/Qo21J2N3EhPdpPzaWngacn

## Using it with Ab ReelStudio
- Profile mapping: `palette.base` = 60% base, `palette.support` = 30% support, `palette.accent` = 10% accent (saved by `reel-setup`). A palette the user already owns wins; use this book to pick one when none is set, to choose the accent, and to fix contrast.
- In reels the palette colors captions, hook cards, lower thirds, progress bars and graphics. It never recolors the user's own footage.
- Captions sit over moving video: treat any caption pair below 4.5:1 as a fail and add a base-color plate or outline behind it. Check pairs with `python3 scripts/contrast.py "#FFFFFF" "#062C30"` or `--palette petrol-gaming` (path relative to this skill's folder).
- Machine-readable data: `palettes.json` (slug, Arabic name, mood, base, support, accent).
- Series trick for reels: keep 60 and 30 fixed across a series and swap only the 10% accent per episode, so every video looks like the same channel.
