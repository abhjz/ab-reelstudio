---
name: reel-pipeline
description: Orchestrates the full flow topic → script (Sonnet) → video (Opus) → user approval → scheduled posts. Used by /reel; load it whenever the user asks to make and post videos.
---

# Ab ReelStudio pipeline

Work folder: `./ab-reelstudio-runs/<YYYY-MM-DD-topic-slug>/` containing `scripts/`, `videos/`, `review/`.

## 0. Profile
Read `.ab-reelstudio/profile.json`. Missing or no accounts connected → run the `reel-setup` skill, then continue.

## 1. Brief
Resolve from arguments + profile: topic(s), style, count, account(s), language. Ask with AskUserQuestion only for missing items. Offer the topic list as free text: the user can give one topic, several, or "surprise me" (then propose topics from the profile niche and recent post analytics via Zernio if available).

## 2. Scripts (Sonnet)
Spawn the `script-writer` agent with the brief. When done, show the user hooks only (one line each) and let them veto or edit before spending render time. Skip this checkpoint if the profile has `autoApproveScripts: true`.

## 3. Videos (Opus)
Spawn one `video-producer` agent per script. Independent videos may run in parallel (max 3 at once). Use a different style per video when the user chose "rotate" or the series has more than one video.

## 4. Review
Run the `review-gallery` skill. Present videos, captions, accounts and proposed time slots. Ask per video: approve / change (with note) / reject. For "change", send the note back to a `video-producer` and re-review. Loop until every video is approved or rejected.

## 5. Schedule
Only for approved videos, run the `schedule-posts` skill. Confirm the final list (video, account, time) before the first write, then report each created post id.

## Hard rules
- Nothing is posted or scheduled before the user approves that exact video.
- Never put personal data (names, account ids, tokens) in repo files or prompts to outside services beyond what Zernio calls need.
- Model split: Sonnet writes scripts, Opus produces videos. Do not swap them.
