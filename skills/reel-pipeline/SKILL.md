---
name: reel-pipeline
description: Orchestrates the full flow - detect the input (topic, own script, podcast link/video file, or folder of clips), run the matching path, then review and schedule. The script is optional. Used by /reel; load it whenever the user asks to make and post videos.
---

# Ab ReelStudio pipeline

Work folder: `./ab-reelstudio-runs/<YYYY-MM-DD-slug>/` with `scripts/`, `source/`, `videos/`, `review/`.

## 0. Profile
Read `.ab-reelstudio/profile.json`. Missing or no accounts connected → run `reel-setup` first, then continue.
Relevant fields: `palette` + `paletteMode` (colors, see `palette-603010`), `checkpoint` (default true), `teaser` (default false), `voice.method` (`own|tts|none`), `generators`, `rules[]`, `accounts[]`.

## 1. Detect the input (the script is optional)

| Input | Detect | Path |
|---|---|---|
| **Topic** | short text, no URL, no path | **A** |
| **Own script** | `--script <file or text>`, or a long multi-sentence text | **B** |
| **Link or video file** | URL (`http...`), or `--from <file>` pointing to a video/audio file | **C** |
| **Folder of clips/images** | `--from <folder>`, or a path that is a directory | **D** |
| **Quran recitation** | `--quran <surah[:from-to]>` | **E** |

If it is ambiguous, ask once with AskUserQuestion. Flags override detection: `--script`, `--from`, `--quran`, `--reciter`, `--style`, `--count`, `--account`, `--voice own|tts|none`, `--teaser`, `--ai`, `--no-checkpoint`.
Resolve topic/style/count/account from args + profile; ask only for what is missing.

## 2. Paths

### A. Topic
1. `script-writer` (Sonnet), mode `write` → `scripts/NN-slug.json`.
2. Checkpoint (if `checkpoint`): show the hooks, one line each; user vetoes/edits.
3. Voice per `voice.method` (see below).
4. `video-producer` (Opus), mode `build`.

### B. Own script
1. `script-writer`, mode `check` on the user's text: length, hook, caption, hashtags. Suggest fixes; never rewrite without the user's OK. Save as `scripts/NN-slug.json` with `voiceoverFull` = the user's text unchanged.
2. Checkpoint (if on): show the checked hook and any suggestions.
3. Voice, then `video-producer` mode `build`.

### C. Link or video file (no script)
Run the `source-reels` skill: rights check → download → transcribe → `script-writer` mode `pick-moments` → checkpoint on the clip picks (if on) → `video-producer` mode `edit`.
The speaker's original audio is kept (no voice step).

### D. Folder of clips
1. Scan the clips (`source-reels`, footage section): best moment per clip, audio beat if there is music.
2. Optional: `script-writer` mode `captions` only if the user wants text over the clips.
3. Checkpoint on the plan (if on), then `video-producer` mode `edit`.

### E. Quran recitation
Run the `quran-reels` skill (needs the Tarteel connector). Text and audio come from the connector; no script is written; no music or effects. Then review and schedule as usual.

## 3. Voice (paths A, B, D)
- `own`: ask the user to record or provide the audio; trim and time it to words.
- `tts`: `video-producer` generates narration in the profile language/dialect (installed TTS, or AI Studio through the user's Chrome per `ai-generators`).
- `none`: captions and music only (unless rules say no music).

## 4. Optional extras (any path)
- `--teaser` or profile `teaser: true`: producer cuts a 3-second cold open of the strongest moment, then a white flash into the full clip.
- `generators` enabled: producer may add a hook clip or B-roll (see `ai-generators`); skip on quota errors.

## 5. Videos
One `video-producer` per video; independent videos may run in parallel (max 3). Use a different style per video when the user chose "rotate" or the series has more than one video.

## 6. Review
Run `review-gallery`. Per video: approve / change (with note) / reject. "Change" goes back to a `video-producer` with the note. Loop until all are approved or rejected.

## 7. Schedule
Only approved videos, via `schedule-posts`. Confirm the final list (video, account, time) before the first write; report each post id.

## Hard rules
- Nothing is posted or scheduled before the user approves that exact video.
- Path C only after the user confirms they own the content or have permission.
- Profile `rules[]` beat every default (music, SFX, branding, voice, CTA).
- Model split: Sonnet picks/writes, Opus builds. Do not swap them.
- No personal data in repo files or in prompts to outside services beyond what Zernio calls need.
