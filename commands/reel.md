---
description: Make and schedule short videos from a topic, your own script, a podcast link/video file, or a folder of clips.
argument-hint: <topic | link | --script text/file | --from file/folder | --quran surah[:from-to]> [--style name] [--count N] [--account label] [--voice own|tts|none] [--teaser] [--ai] [--no-checkpoint]
---

Run the Ab ReelStudio pipeline for: $ARGUMENTS

Follow the `reel-pipeline` skill exactly:

1. Load the profile (`.ab-reelstudio/profile.json`); if missing, run `reel-setup`.
2. Detect the input. The script is optional:
   - a topic -> script written by Sonnet
   - `--script` or a long text -> your own script, checked not rewritten
   - a link or `--from <video>` -> no script; best moments picked from the transcript (rights check first)
   - `--from <folder>` -> no script; clips cut to the beat
   - `--quran 93:1-11 --reciter <name>` -> recitation reel from the Tarteel connector, no music
3. Run the matching path, build with Opus, show the review gallery.
4. Only after explicit approval, schedule the approved videos on Zernio. Never publish anything that was not approved.
