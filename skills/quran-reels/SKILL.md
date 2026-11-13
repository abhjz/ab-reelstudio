---
name: quran-reels
description: Quran recitation reels - verse-by-verse visuals synced to a reciter's audio from the Tarteel connector, with exact Uthmani text, calm styles, no music. Used by reel-pipeline path E (/reel --quran).
---

# Quran reels (path E)

Needs the **Tarteel connector** (tools such as `list_reciters`, `lookup_reciters`, `play_ayahs`, `search_ayahs_text`, `ayah_translation`). If absent, stop and tell the user to add it through `/mcp` (see `reel-doctor`).

## Inputs
`--quran <surah or surah:from-to>` (for example `94` or `93:1-11`), `--reciter <name>` (ask if missing; list options with `list_reciters`), optional `--translation <language>`.

## Rules
- **Text must come from the connector** (`search_ayahs_text` / ayah lookup). Never type or "fix" verses from memory.
- **No music, no sound effects.** Recitation only, loudness about -14 LUFS. This overrides profile music settings.
- Never add the "follow me" or promotional lines mid-recitation. A small handle watermark is allowed only if the profile asks for it.
- Keep the design calm and respectful: no flashing, no shake, no comic effects. Do not place text over faces/people (there are none).
- Use a **different visual style per reel**: for example a night-sky glow, an illuminated mushaf page with the current verse highlighted, a crescent with an audio-reactive ring (add a translation line under the Arabic).
- Caption each reel with the surah name, reciter, and a short reflection only if the user asked for one; do not invent tafsir. If a tafsir or translation is shown, take it from the connector and name the source.

## Steps
1. Resolve the reciter and surah/verse range; call `play_ayahs` to get per-verse audio URLs. Prepend the Basmala (verse 1:1) except for Surah 9 and for Surah 1 (where it is verse 1).
2. Download each verse's audio, convert to 48 kHz mono WAV, concatenate, and record each verse's start time (1.0 s of silence at the start).
3. Fetch the exact Uthmani text per verse (and the translation if requested).
4. Build the page with the shipped templates: write a `config.json` (template `sky`, `mushaf` or `moon`, items with the connector text and downloaded audio files) and run `python3 ${CLAUDE_PLUGIN_ROOT}/templates/quran/build_quran.py config.json`. It concatenates the audio, times each verse and writes `reel.html`. Pick a different template for each reel. Details: `templates/quran/README.md`.
5. Render frames with `HTML=reel.html OUT=frames node ${CLAUDE_PLUGIN_ROOT}/templates/explainer/render.js all` (needs `npm i puppeteer-core` and Chrome), then ffmpeg the frames at 30 fps with `recitation.wav`, loudnorm about -14. HyperFrames also works if the user prefers.
6. Verify: duration equals the audio length, text matches the connector output character for character, no clipped Arabic diacritics.
7. Review gallery, then schedule on the account the user designated for Quran content. Suggested slots come from the profile.
