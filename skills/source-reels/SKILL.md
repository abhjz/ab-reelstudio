---
name: source-reels
description: Turns an existing video (podcast/interview link, video file, or a folder of clips) into vertical reels with no script - rights check, download, transcript with word timings, clip picking, cutting, captions, hook and optional teaser. Used by reel-pipeline paths C and D.
---

# Reels from existing footage

## C. Podcast link or video file

### 1. Rights check (mandatory)
AskUserQuestion: "Do you own this content, or do you have permission to clip and repost it?" Options: yes I own it / yes I have permission / no. On "no" stop and say so. Never circumvent DRM, logins or paywalls. For a local file, still ask.

### 2. Get the source
- File: copy or symlink into `<run>/source/`.
- URL: needs `yt-dlp`. If missing, ask before installing (`bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-styles.sh source-tools`). Download the best mp4 plus audio into `<run>/source/`. Show title, duration, size and ask before downloading anything over ~1 GB.

### 3. Transcribe
Whisper with word timestamps, in the profile language (give the dialect hint as the initial prompt). Use `mlx-whisper` on Apple Silicon, else `faster-whisper`. Save `<run>/source/words.json`: sentences with words `{w, s, e}` in seconds. Spoken numbers stay digits; keep the speaker's wording.

### 4. Pick moments
Spawn `script-writer` in mode `pick-moments` with the transcript, count N, length target and profile rules. It returns `scripts/clips.json`. Show the picks (hook, time range, one-line reason) and let the user veto or adjust when the checkpoint is on.

### 5. Edit (Opus, `video-producer` mode `edit`)
1. Cut each range from the first word's start to the last word's end, trim silences over ~0.6 s (keep the speaker's rhythm).
2. Vertical 1080x1920: crop to the active speaker (face detection or manual crop per shot); for split screens stack the speakers. Never crop a face off.
3. Captions in the profile language, word-timed, dialect-corrected, numbers as digits; keep top ~8% and bottom ~20% clear.
4. Hook card in the first ~2 s with the clip's hook line.
5. Optional teaser: take the strongest 3 s, `xfade=fadewhite` (0.2 s) into the full clip from its start.
6. Audio: the original voice, cleaned and loudness-normalised (about -14 LUFS). No music or SFX unless the profile allows.
7. If an editing skill is installed (`podcast-video`, `montage-video`, `video-ad-editor`) use it; otherwise ffmpeg.
8. Verify: duration, freeze check, audio level, 4-6 sampled frames for cut-off text or faces covered.

## D. Folder of clips
1. List clips (mp4/mov/jpg/png). Per clip find the best 1-3 s window (motion, sharpness, faces) with ffmpeg scene/motion analysis; if there is music, detect beats.
2. Plan the sequence and show it when the checkpoint is on.
3. Cut to the beat, vertical, with optional text overlays; add music only if the profile allows.
4. Same verification as above.

## Rules
- Quote the speaker accurately in captions; fix only obvious transcription errors.
- Never present clipped content as something the speaker did not say. Do not reorder words inside a clip.
- Respect every profile rule.
