---
name: review-gallery
description: Builds a local review page showing every produced video with its script, caption, target account and proposed time slot so the user can approve, change or reject each one. Use after videos are rendered and before scheduling.
---

# Review gallery

1. Create `<run>/review/index.html` (self-contained, relative `<video controls playsinline>` pointing at `../videos/*.mp4`, poster = the `.jpg`). Per video show: title, hook, full script, caption + hashtags, platform/account label, proposed slot (local time), style used, duration, and any warnings from the producer.
   Layout: 9:16 player on the left, details on the right; responsive; light/dark safe; no external requests.
2. Show it to the user: open it in the built-in browser pane (serve the folder with a tiny static server, for example `python3 -m http.server`, and open the localhost URL) or reveal the folder. If a published Artifact fits (videos small enough and the user wants a shareable page), offer it, otherwise stay local.
3. Collect decisions with AskUserQuestion, one question per video (max 4 per call, repeat as needed): **Approve** / **Change** (ask for the note) / **Reject**.
4. Record decisions in `<run>/review/decisions.json`: `{id, decision, note, account, slot}`.
5. Return the approved list to the pipeline. Changes go back to a `video-producer` agent with the note, then re-enter this skill for that video only.
