---
description: Make and schedule short videos. Usage - /reel <topic> [--style <name>] [--count N] [--account <label>]
argument-hint: <topic> [--style name] [--count N] [--account label]
---

Run the full ab-reelstudio pipeline for: $ARGUMENTS

Follow the `reel-pipeline` skill exactly. Summary:

1. Load the profile (`.ab-reelstudio/profile.json`). If missing, run the `reel-setup` skill first.
2. Resolve topic, style, count and target account from the arguments and the profile. Ask (AskUserQuestion) only for what is missing.
3. Delegate the script to the `script-writer` agent (Sonnet).
4. Delegate production to the `video-producer` agent (Opus), one video per script.
5. Build the review gallery (`review-gallery` skill) and show it to the user.
6. Only after explicit approval, schedule the approved videos with the `schedule-posts` skill. Never publish anything that was not approved.
