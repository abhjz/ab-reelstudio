# Explainer templates (code-drawn, step by step)

Animated how-to explainers rendered from HTML. Two looks.

**Dark (style A): `common.py` + `common.css`**
Dark warm background, a code-drawn SVG object, live counters, a card with a headline and word-by-word captions.
Start from `example_dark.py` (a full worked example): copy it, change the chunks (word, start-second), the SVG scene and the phases.
Set `cfg['watermark']` for an optional handle (empty = none).

**Light (style B): `common_b.py`**
Cream paper with a grid, drifting colour blocks, a giant hero word per phase, takeaway cards and a two-option end card.
Objects should be **real photo cutouts**, not drawings:
1. Generate the object with Nano Banana (Gemini, in your Chrome) on a pure white background.
2. `python3 cutout.py raw.jpg out.png` (add `--thr 250` for white or pale objects). Needs pillow + numpy.
3. Place it with the `IMG`, `SCALE_IMG` and `WATCH_IMG` helpers. Optional: one 8 s Google Flow clip per reel, blended with `CLIP()`.
Set `cfg['handle']` for an optional top-right handle.

**Render**
```
npm i puppeteer-core                                   # once, in your project
HTML=reel_ar.html OUT=frames node <plugin>/templates/explainer/render.js all
```
Env: `PUPPETEER_PATH`, `CHROME_PATH`. Then mix narration (and music only if your rules allow it) with ffmpeg and loudnorm to about -14 LUFS.
