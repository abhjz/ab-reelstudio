# Quran reel templates

Three calm looks, one builder. Text and audio must come from the Tarteel connector (see the `quran-reels` skill).

| Template | Look |
|---|---|
| `sky.html` | night-sky glow with stars; `theme: sharh` (teal) or `duha` (night to dawn) |
| `mushaf.html` | illuminated cream page, current verse highlighted |
| `moon.html` | crescent with an audio-reactive ring, optional translation line under the Arabic |

```
python3 build_quran.py config.json                          # writes <out>/reel.html + recitation.wav
cd <out> && HTML=reel.html OUT=frames node <plugin>/templates/explainer/render.js all
```
Then encode the frames with `recitation.wav` using ffmpeg (30 fps, loudnorm about -14). No music, no effects.
Use a different template for each reel.
